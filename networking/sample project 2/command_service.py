"""
Module 2 — Device Connectivity
Module 3 — Command Execution (single device)
Module 4 — Bulk Command Execution (many devices, in parallel via Nornir)
"""

from typing import List

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
from nornir.core import Nornir
from nornir.core.inventory import Defaults, Groups, Host, Hosts, Inventory
from nornir.plugins.runners import ThreadedRunner
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config
from sqlalchemy.orm import Session

from . import models
from .netmiko_utils import netmiko_params


# ---------------------------------------------------------------------------
# Module 2 — Connectivity
# ---------------------------------------------------------------------------

def connect_device(db: Session, device: models.Device) -> dict:
    """Open an SSH session and confirm the device is reachable and credentials work."""
    try:
        conn = ConnectHandler(**netmiko_params(device))
        prompt = conn.find_prompt()
        conn.disconnect()

        device.status = "reachable"
        db.commit()

        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "reachable": True,
            "detail": "Connection established successfully.",
            "device_prompt": prompt,
        }
    except NetmikoAuthenticationException:
        device.status = "auth_failed"
        db.commit()
        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "reachable": False,
            "detail": "Authentication failed.",
            "device_prompt": None,
        }
    except NetmikoTimeoutException:
        device.status = "unreachable"
        db.commit()
        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "reachable": False,
            "detail": "Connection timed out — device unreachable.",
            "device_prompt": None,
        }
    except Exception as e:  # noqa: BLE001
        device.status = "error"
        db.commit()
        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "reachable": False,
            "detail": f"Unexpected error: {e}",
            "device_prompt": None,
        }


# ---------------------------------------------------------------------------
# Module 3 — Single-device command execution
# ---------------------------------------------------------------------------

def run_command(device: models.Device, command: str, is_config: bool) -> dict:
    try:
        conn = ConnectHandler(**netmiko_params(device))
        if is_config:
            output = conn.send_config_set([command])
        else:
            output = conn.send_command(command)
        conn.disconnect()

        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "success": True,
            "output": output,
            "error": None,
        }
    except Exception as e:  # noqa: BLE001
        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "success": False,
            "output": None,
            "error": str(e),
        }


# ---------------------------------------------------------------------------
# Module 4 — Bulk command execution across many devices, in parallel
# ---------------------------------------------------------------------------

def _build_inventory(devices: List[models.Device]) -> Inventory:
    hosts = Hosts()
    for d in devices:
        hosts[d.hostname] = Host(
            name=d.hostname,
            hostname=d.ip,
            username=d.username,
            password=d.password,
            platform=d.device_type,
            data={"db_id": d.id},
        )
    return Inventory(hosts=hosts, groups=Groups(), defaults=Defaults())


def run_bulk_command(
    devices: List[models.Device], command: str, is_config: bool, num_workers: int = 10
) -> List[dict]:
    if not devices:
        return []

    inventory = _build_inventory(devices)
    nr = Nornir(inventory=inventory, runner=ThreadedRunner(num_workers=num_workers))
    devices_by_hostname = {d.hostname: d for d in devices}

    def _task(task):
        if is_config:
            result = task.run(task=netmiko_send_config, config_commands=[command])
        else:
            result = task.run(task=netmiko_send_command, command_string=command)
        return result.result

    agg_result = nr.run(task=_task)

    results = []
    for hostname, multi_result in agg_result.items():
        device = devices_by_hostname[hostname]
        if multi_result.failed:
            results.append(
                {
                    "device_id": device.id,
                    "hostname": hostname,
                    "success": False,
                    "output": None,
                    "error": str(multi_result[0].exception) if multi_result else "Unknown error",
                }
            )
        else:
            results.append(
                {
                    "device_id": device.id,
                    "hostname": hostname,
                    "success": True,
                    "output": multi_result[0].result,
                    "error": None,
                }
            )
    return results
