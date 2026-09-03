"""
Core backup logic.

- backup_single_device(): connects to ONE device directly via Netmiko.
  Used by POST /devices/{id}/backup.

- backup_all_devices(): builds an in-memory Nornir inventory from the
  devices stored in the database, then uses Nornir (with the Netmiko
  plugin) to fan the backup out to every device IN PARALLEL.
  Used by POST /backup/all.

Both paths save the retrieved "show running-config" output to a
timestamped text file under BACKUP_DIR and update the device's
last_backup / status fields in the database.
"""

import os
from datetime import datetime, timezone
from typing import List

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
from nornir.core import Nornir
from nornir.core.inventory import Defaults, Groups, Host, Hosts, Inventory
from nornir.plugins.runners import ThreadedRunner
from nornir_netmiko.tasks import netmiko_send_command
from sqlalchemy.orm import Session

from . import models

BACKUP_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backups"
)
os.makedirs(BACKUP_DIR, exist_ok=True)


def _save_backup_file(hostname: str, config_text: str) -> str:
    """Write config_text to backups/<hostname>_<timestamp>.txt and return the filename."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{hostname}_{timestamp}.txt"
    filepath = os.path.join(BACKUP_DIR, filename)
    with open(filepath, "w") as f:
        f.write(config_text)
    return filename


def _netmiko_params(device: models.Device) -> dict:
    return {
        "device_type": device.device_type,
        "host": device.ip,
        "username": device.username,
        "password": device.password,
        "timeout": 15,
        "banner_timeout": 15,
    }


def backup_single_device(db: Session, device: models.Device) -> dict:
    """Connect directly via Netmiko and back up one device's running-config."""
    try:
        conn = ConnectHandler(**_netmiko_params(device))
        config = conn.send_command("show running-config")
        conn.disconnect()

        filename = _save_backup_file(device.hostname, config)

        device.last_backup = datetime.now(timezone.utc)
        device.status = "backed_up"
        db.commit()

        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "status": "success",
            "message": "Backup completed successfully.",
            "backup_file": filename,
        }

    except NetmikoAuthenticationException:
        device.status = "auth_failed"
        db.commit()
        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "status": "failed",
            "message": "Authentication failed.",
            "backup_file": None,
        }
    except NetmikoTimeoutException:
        device.status = "unreachable"
        db.commit()
        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "status": "failed",
            "message": "Device unreachable (connection timed out).",
            "backup_file": None,
        }
    except Exception as e:  # noqa: BLE001 - surface any other failure to the caller
        device.status = "error"
        db.commit()
        return {
            "device_id": device.id,
            "hostname": device.hostname,
            "status": "failed",
            "message": f"Unexpected error: {e}",
            "backup_file": None,
        }


def _build_nornir_inventory(devices: List[models.Device]) -> Inventory:
    """Translate DB device rows into an in-memory Nornir Inventory (no YAML files needed)."""
    hosts = Hosts()
    for d in devices:
        hosts[d.hostname] = Host(
            name=d.hostname,
            hostname=d.ip,
            username=d.username,
            password=d.password,
            platform=d.device_type,
            data={"db_id": d.id, "vendor": d.vendor},
        )
    return Inventory(hosts=hosts, groups=Groups(), defaults=Defaults())


def _backup_task(task):
    """A single Nornir task: run 'show running-config' via the Netmiko plugin."""
    result = task.run(
        task=netmiko_send_command,
        command_string="show running-config",
    )
    return result.result


def backup_all_devices(
    db: Session, devices: List[models.Device], num_workers: int = 10
) -> List[dict]:
    """Use Nornir to fan Netmiko backups out across all devices in parallel."""
    if not devices:
        return []

    inventory = _build_nornir_inventory(devices)
    nr = Nornir(inventory=inventory, runner=ThreadedRunner(num_workers=num_workers))

    devices_by_hostname = {d.hostname: d for d in devices}
    agg_result = nr.run(task=_backup_task)

    results = []
    for hostname, multi_result in agg_result.items():
        device = devices_by_hostname[hostname]

        if multi_result.failed:
            device.status = "failed"
            db.commit()
            error = multi_result[0].exception if multi_result else None
            results.append(
                {
                    "device_id": device.id,
                    "hostname": hostname,
                    "status": "failed",
                    "message": f"Backup failed: {error}",
                    "backup_file": None,
                }
            )
            continue

        config_text = multi_result[0].result
        filename = _save_backup_file(hostname, config_text)

        device.last_backup = datetime.now(timezone.utc)
        device.status = "backed_up"
        db.commit()

        results.append(
            {
                "device_id": device.id,
                "hostname": hostname,
                "status": "success",
                "message": "Backup completed successfully.",
                "backup_file": filename,
            }
        )

    return results


def list_backups() -> List[dict]:
    """List every backup file on disk with its host, timestamp, and size."""
    records = []
    for filename in sorted(os.listdir(BACKUP_DIR)):
        filepath = os.path.join(BACKUP_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        stat = os.stat(filepath)
        name_part = filename.rsplit(".", 1)[0]

        try:
            hostname, date_part, time_part = name_part.rsplit("_", 2)
            timestamp = datetime.strptime(f"{date_part}_{time_part}", "%Y%m%d_%H%M%S")
        except ValueError:
            hostname = name_part
            timestamp = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)

        records.append(
            {
                "hostname": hostname,
                "filename": filename,
                "timestamp": timestamp,
                "size_bytes": stat.st_size,
            }
        )
    return records
