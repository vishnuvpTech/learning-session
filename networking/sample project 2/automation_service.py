"""
Module 6 — Automation (VLAN / OSPF / BGP)

Implements the senior-engineer workflow discussed for network changes:

    Validate -> Pre-check -> Configure -> Post-check -> Success/Rollback -> Audit

Each `apply_*` function renders device configuration from a Jinja2 template,
then hands off to the shared `apply_change()` state machine, which is the
same for every automation type: it captures a "before" snapshot, applies the
change, captures an "after" snapshot, checks a success pattern against the
"after" snapshot, and either records success or automatically rolls back —
logging every outcome to the audit trail (Module 8).
"""

import re
from typing import List

from jinja2 import Template
from netmiko import ConnectHandler
from sqlalchemy.orm import Session

from . import audit_service, models, schemas
from .netmiko_utils import netmiko_params

# ---------------------------------------------------------------------------
# Jinja2 templates
# ---------------------------------------------------------------------------

VLAN_TEMPLATE = Template(
    "vlan {{ vlan_id }}\n"
    " name {{ vlan_name }}"
)

OSPF_TEMPLATE = Template(
    "router ospf {{ process_id }}\n"
    "{% for net in networks %}"
    " network {{ net.network }} {{ net.wildcard }} area {{ area }}\n"
    "{% endfor %}"
)

BGP_TEMPLATE = Template(
    "router bgp {{ local_asn }}\n"
    "{% for n in neighbors %}"
    " neighbor {{ n.ip }} remote-as {{ n.remote_asn }}\n"
    "{% endfor %}"
)


# ---------------------------------------------------------------------------
# Shared workflow engine
# ---------------------------------------------------------------------------

def _result(device: models.Device, stage: str, outcome: str, detail: str) -> dict:
    return {
        "device_id": device.id,
        "hostname": device.hostname,
        "stage_reached": stage,
        "result": outcome,
        "detail": detail,
    }


def apply_change(
    db: Session,
    device: models.Device,
    action: str,
    requested_by: str,
    config_commands: List[str],
    rollback_commands: List[str],
    verify_command: str,
    success_pattern: str,
) -> dict:
    stage = "validate"

    if not config_commands:
        detail = "No configuration commands generated — nothing to apply."
        audit_service.log_audit(db, requested_by, action, device.hostname, "failed", detail=detail)
        return _result(device, stage, "failed", detail)

    try:
        conn = ConnectHandler(**netmiko_params(device))
    except Exception as e:  # noqa: BLE001
        detail = f"Could not connect to device: {e}"
        audit_service.log_audit(db, requested_by, action, device.hostname, "failed", detail=detail)
        return _result(device, stage, "failed", detail)

    try:
        stage = "pre_check"
        before = conn.send_command(verify_command)

        stage = "configure"
        conn.send_config_set(config_commands)

        stage = "post_check"
        after = conn.send_command(verify_command)

        success = re.search(success_pattern, after, re.IGNORECASE | re.MULTILINE) is not None

        if success:
            audit_service.log_audit(
                db, requested_by, action, device.hostname, "success",
                old_config=before, new_config=after,
                detail="Post-check verification pattern matched — change confirmed.",
            )
            return _result(device, "success", "success", "Change applied and verified successfully.")

        stage = "rollback"
        if rollback_commands:
            conn.send_config_set(rollback_commands)
        audit_service.log_audit(
            db, requested_by, action, device.hostname, "rolled_back",
            old_config=before, new_config=after,
            detail="Post-check verification failed; rollback commands applied.",
        )
        return _result(device, "rollback", "rolled_back", "Post-check failed; rollback applied.")

    except Exception as e:  # noqa: BLE001
        detail = f"Error during stage '{stage}': {e}"
        audit_service.log_audit(db, requested_by, action, device.hostname, "failed", detail=detail)
        return _result(device, stage, "failed", detail)
    finally:
        conn.disconnect()


# ---------------------------------------------------------------------------
# VLAN
# ---------------------------------------------------------------------------

def apply_vlan(db: Session, device: models.Device, req: "schemas.VlanAutomationRequest") -> dict:
    config = VLAN_TEMPLATE.render(vlan_id=req.vlan_id, vlan_name=req.vlan_name).splitlines()
    rollback = [f"no vlan {req.vlan_id}"]
    verify_command = "show vlan brief"
    success_pattern = rf"^{req.vlan_id}\s"

    return apply_change(
        db, device, "automation.vlan", req.requested_by,
        config, rollback, verify_command, success_pattern,
    )


# ---------------------------------------------------------------------------
# OSPF
# ---------------------------------------------------------------------------

def apply_ospf(db: Session, device: models.Device, req: "schemas.OspfAutomationRequest") -> dict:
    config = OSPF_TEMPLATE.render(
        process_id=req.process_id,
        area=req.area,
        networks=[n.model_dump() for n in req.networks],
    ).splitlines()
    config = [line for line in config if line.strip()]
    rollback = [f"no router ospf {req.process_id}"]
    verify_command = f"show ip ospf {req.process_id}"
    success_pattern = rf"Routing Process \"ospf {req.process_id}\""

    return apply_change(
        db, device, "automation.ospf", req.requested_by,
        config, rollback, verify_command, success_pattern,
    )


# ---------------------------------------------------------------------------
# BGP
# ---------------------------------------------------------------------------

def apply_bgp(db: Session, device: models.Device, req: "schemas.BgpAutomationRequest") -> dict:
    config = BGP_TEMPLATE.render(
        local_asn=req.local_asn,
        neighbors=[n.model_dump() for n in req.neighbors],
    ).splitlines()
    config = [line for line in config if line.strip()]
    rollback = [f"no router bgp {req.local_asn}"]
    verify_command = "show ip bgp summary"
    success_pattern = rf"local AS number {req.local_asn}"

    return apply_change(
        db, device, "automation.bgp", req.requested_by,
        config, rollback, verify_command, success_pattern,
    )
