# Network Configuration Backup System

A FastAPI service that maintains a device inventory and backs up network
device configurations, using Nornir to orchestrate Netmiko connections in
parallel.

```
FastAPI
   │
   ▼
Device Inventory   (SQLite via SQLAlchemy)
   │
   ▼
Nornir             (parallel orchestration across many devices)
   │
   ▼
Netmiko            (SSH connection + command execution per device)
   │
   ▼
Network Devices
```

## Project layout

```
network_backup_system/
├── app/
│   ├── main.py            # FastAPI app + routes
│   ├── database.py         # SQLAlchemy engine/session
│   ├── models.py           # Device ORM model
│   ├── schemas.py          # Pydantic request/response models
│   └── backup_service.py   # Netmiko (single) + Nornir (fan-out) backup logic
├── backups/                 # Saved config backups land here (as .txt files)
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Then open **http://127.0.0.1:8000/docs** for interactive Swagger docs.

## API

| Method | Path | Description |
|---|---|---|
| `POST` | `/devices` | Register a new device in the inventory |
| `GET` | `/devices` | List all devices |
| `GET` | `/devices/{id}` | Get one device |
| `DELETE` | `/devices/{id}` | Remove a device |
| `POST` | `/devices/{id}/backup` | Back up a single device (direct Netmiko connection) |
| `POST` | `/backup/all` | Back up every device in parallel (Nornir + Netmiko) |
| `GET` | `/backups` | List saved backup files with timestamps and sizes |

### Example: register a device

```bash
curl -X POST http://127.0.0.1:8000/devices \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "router1",
    "ip": "192.168.10.1",
    "vendor": "cisco",
    "device_type": "cisco_ios",
    "username": "admin",
    "password": "password"
  }'
```

`device_type` must be a valid [Netmiko `device_type`](https://github.com/ktbyers/netmiko#supports)
string, e.g. `cisco_ios`, `cisco_nxos`, `arista_eos`, `juniper_junos`.

### Example: back up everything

```bash
curl -X POST http://127.0.0.1:8000/backup/all
```

Response:

```json
{
  "total": 3,
  "success": 2,
  "failed": 1,
  "results": [
    {"device_id": 1, "hostname": "router1", "status": "success", "message": "Backup completed successfully.", "backup_file": "router1_20260903_120006.txt"},
    {"device_id": 2, "hostname": "router2", "status": "success", "message": "Backup completed successfully.", "backup_file": "router2_20260903_120006.txt"},
    {"device_id": 3, "hostname": "switch1", "status": "failed", "message": "Backup failed: ...", "backup_file": null}
  ]
}
```

## What each layer does

- **Device Inventory** (`models.py` / `database.py`) — a SQLite table (via SQLAlchemy)
  storing `hostname`, `ip`, `vendor`, `device_type`, credentials, `last_backup`, and `status`.
- **Nornir** (`backup_service._build_nornir_inventory` / `backup_all_devices`) — device
  rows from the database are translated into an in-memory Nornir `Inventory` (no YAML
  files needed), then `Nornir(..., runner=ThreadedRunner(num_workers=10))` fans the
  backup task out across every device concurrently.
- **Netmiko** (`backup_service.backup_single_device` for one device; the
  `nornir_netmiko` plugin's `netmiko_send_command` task for the fan-out case) — opens
  the SSH session, runs `show running-config`, and returns the output.
- **Storage** — each backup is written to `backups/<hostname>_<UTC timestamp>.txt`,
  and the device's `last_backup` timestamp and `status` (`backed_up` / `failed` /
  `auth_failed` / `unreachable`) are updated in the database.

## Testing without real devices

The whole API can be exercised with FastAPI's `TestClient` and Netmiko mocked out —
useful in CI or before you have lab devices to point at:

```python
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.post("/devices", json={
    "hostname": "router1", "ip": "192.168.10.1", "vendor": "cisco",
    "device_type": "cisco_ios", "username": "admin", "password": "password",
})

with patch("app.backup_service.ConnectHandler") as mock_connect:
    mock_conn = MagicMock()
    mock_conn.send_command.return_value = "hostname router1\n..."
    mock_connect.return_value = mock_conn
    resp = client.post("/devices/1/backup")
    print(resp.json())
```

## Notes / production hardening ideas

- **Credentials are stored in plaintext** in this demo for simplicity. In production,
  encrypt them at rest (e.g. `cryptography.Fernet`) or pull them from a secrets
  manager (Vault, AWS Secrets Manager) instead of the database.
- Add authentication/authorization to the API itself (it's currently open).
- Add a scheduler (e.g. APScheduler or a cron job hitting `POST /backup/all`) for
  automatic nightly backups.
- Add config **diffing** between the latest two backups per device to alert on
  unexpected changes.
- Swap SQLite for Postgres in production by changing `DATABASE_URL` in `database.py`.
