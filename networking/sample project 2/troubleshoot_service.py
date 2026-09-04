"""
Module 7 — Automated Troubleshooting

POST /troubleshoot runs a sequential diagnostic pipeline, originating from a
registered "source" device (reached over SSH via Netmiko), stopping at the
first step that indicates a problem:

    ping -> traceroute -> arp -> routing table -> interface status
         -> firewall/ACL -> TCP port

Design notes:
- ping / traceroute / arp / routing table / interface status / ACL are all
  run AS COMMANDS ON THE SOURCE DEVICE, so results reflect that device's
  real view of the network (this is how a real Netmiko/Nornir-based
  platform would do it - see Day 3/4).
- The final TCP port check is a direct socket connection from the API
  server itself, simulating the actual application-layer reachability
  test - if everything up to this point looked healthy but the port
  doesn't respond, that's attributed to a firewall/ACL blocking the
  specific port, which matches the sample output in the spec.
- Output parsing uses simple, documented regexes for common Cisco IOS
  phrasing. Real deployments should adapt these per-vendor/per-OS.
"""

import re
import socket

from netmiko import ConnectHandler

from . import models
from .netmiko_utils import netmiko_params


def _step(step: str, passed: bool, detail: str) -> dict:
    return {"step": step, "passed": passed, "detail": detail}


def _check_ping(conn, destination: str) -> dict:
    output = conn.send_command(f"ping {destination}")
    match = re.search(r"Success rate is (\d+) percent", output)
    if match and int(match.group(1)) > 0:
        return _step("ping", True, f"Ping success rate: {match.group(1)}%.")
    return _step("ping", False, f"Ping failed. Raw output: {output.strip()[-200:]}")


def _check_traceroute(conn, destination: str) -> dict:
    output = conn.send_command(f"traceroute {destination}", read_timeout=30)
    if destination in output:
        return _step("traceroute", True, "Traceroute reached the destination.")
    return _step(
        "traceroute", False,
        f"Traceroute did not reach the destination. Raw output: {output.strip()[-300:]}",
    )


def _check_arp(conn, destination: str) -> dict:
    # ARP is only meaningful for directly-connected destinations; for remote
    # destinations this step is informational only and never fails the pipeline.
    output = conn.send_command("show ip arp")
    if destination in output:
        return _step("arp", True, f"ARP entry found for {destination}.")
    return _step("arp", True, "No direct ARP entry (destination is likely remote/routed).")


def _check_routing(conn, destination: str) -> dict:
    output = conn.send_command(f"show ip route {destination}")
    if "% Network not in table" in output or "% Subnet not in table" in output:
        return _step("routing", False, f"No route to {destination} in the routing table.")
    return _step("routing", True, f"A route to {destination} exists.")


def _check_interface(conn, route_output: str) -> dict:
    match = re.search(r"via\s+([A-Za-z0-9/.]+)", route_output)
    if not match:
        return _step("interface", True, "Could not determine outbound interface from routing table; skipped.")
    iface = match.group(1)
    output = conn.send_command(f"show ip interface brief {iface}")
    lowered = output.lower()
    if " up " in f" {lowered} " and "down" not in lowered:
        return _step("interface", True, f"Outbound interface {iface} is up.")
    return _step("interface", False, f"Outbound interface {iface} appears down. Output: {output.strip()}")


def _check_firewall_acl(conn, destination: str, port: int) -> dict:
    output = conn.send_command("show access-lists")
    deny_pattern = re.compile(
        rf"deny\s+\S+\s+\S*{re.escape(destination)}\S*.*eq\s+{port}", re.IGNORECASE
    )
    if deny_pattern.search(output):
        return _step("firewall", False, f"An ACL rule denies traffic to {destination} on port {port}.")
    return _step("firewall", True, "No explicit denying ACL rule found on the source device.")


def _check_tcp_port(destination: str, port: int, timeout: float = 3.0) -> dict:
    try:
        with socket.create_connection((destination, port), timeout=timeout):
            return _step("tcp_port", True, f"TCP port {port} is open on {destination}.")
    except Exception as e:  # noqa: BLE001
        return _step("tcp_port", False, f"TCP connection to {destination}:{port} failed: {e}")


_RECOMMENDATIONS = {
    "ping": "Host is unreachable — verify the destination is powered on and the network path exists.",
    "traceroute": "Check routing at the hop where the trace stops responding.",
    "routing": "Add or fix the route to the destination network on the source device.",
    "interface": "Bring up the outbound interface, or check for a cabling/hardware issue.",
    "firewall": "Check firewall/ACL policy for this source-destination-port combination.",
}


def run_troubleshoot(source_device: models.Device, destination: str, port: int) -> dict:
    steps = []

    try:
        conn = ConnectHandler(**netmiko_params(source_device))
    except Exception as e:  # noqa: BLE001
        steps.append(_step("connect_to_source", False, f"Could not connect to source device: {e}"))
        return {
            "connectivity": False,
            "failed_at": "connect_to_source",
            "port": port,
            "recommendation": "Verify the source device is reachable and its credentials are correct.",
            "steps": steps,
        }

    try:
        ping = _check_ping(conn, destination)
        steps.append(ping)
        if not ping["passed"]:
            return _finalize(steps, "ping", port)

        trace = _check_traceroute(conn, destination)
        steps.append(trace)
        if not trace["passed"]:
            return _finalize(steps, "traceroute", port)

        steps.append(_check_arp(conn, destination))  # informational, never fails the pipeline

        route_output = conn.send_command(f"show ip route {destination}")
        routing = _check_routing(conn, destination)
        steps.append(routing)
        if not routing["passed"]:
            return _finalize(steps, "routing", port)

        interface = _check_interface(conn, route_output)
        steps.append(interface)
        if not interface["passed"]:
            return _finalize(steps, "interface", port)

        firewall = _check_firewall_acl(conn, destination, port)
        steps.append(firewall)
        if not firewall["passed"]:
            return _finalize(steps, "firewall", port)

        tcp = _check_tcp_port(destination, port)
        steps.append(tcp)
        if not tcp["passed"]:
            # All device-level checks looked healthy; a non-responding port at
            # this stage is attributed to a firewall/ACL (possibly upstream of
            # the source device) or the destination service simply not listening.
            return {
                "connectivity": False,
                "failed_at": "firewall",
                "port": port,
                "recommendation": (
                    "Port did not respond even though routing/interface look healthy — "
                    "likely blocked by a firewall, or the service isn't listening. "
                    "Check firewall policy."
                ),
                "steps": steps,
            }

        return {
            "connectivity": True,
            "failed_at": None,
            "port": port,
            "recommendation": "All checks passed.",
            "steps": steps,
        }
    finally:
        conn.disconnect()


def _finalize(steps: list, failed_at: str, port: int) -> dict:
    return {
        "connectivity": False,
        "failed_at": failed_at,
        "port": port,
        "recommendation": _RECOMMENDATIONS.get(failed_at, "Investigate further."),
        "steps": steps,
    }
