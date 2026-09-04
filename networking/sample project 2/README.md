# Network Automation & Troubleshooting Platform

A FastAPI platform that combines device inventory, remote command execution,
configuration backup, templated automation (with automatic pre-check /
post-check / rollback), troubleshooting, and a full audit trail — built on
Nornir + Netmiko.

```
FastAPI
   │
   ▼
Device Inventory (Module 1)
   │
   ├── Connectivity (Module 2)
   ├── Command Execution (Modules 3 & 4)
   ├── Backup (Module 5)
   ├── Automation (Module 6)   ──► Validate → Pre-check → Configure → Post-check → Success/Rollback → Audit
   └── Troubleshooting (Module 7)
   │
   ▼
Audit Log (Module 8)
```

## Project layout

```
network_automation_platform/
├── app/
│   ├── main.py                # FastAPI app + all routes (8 modules)
│   ├── database.py             # SQLAlchemy engine/session
│   ├── models.py               # Device + AuditLog ORM models
│   ├── schemas.py               # Pydantic request/response models
│   ├── netmiko_utils.py         # Shared Device -> Netmiko connection params
│   ├── command_service.py       # Modules 2, 3, 4
│   ├── backup_service.py        # Module 5
│   ├── automation_service.py    # Module 6
│   ├── troubleshoot_service.py  # Module 7
│   └── audit_service.py         # Module 8
├── backups/                      # Saved config backups (.txt files)
├── requirements.txt
└── README.md
```

## Setup & run

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for interactive Swagger docs — every
endpoint below is grouped there by module.

---

## Module 1 — Device Inventory

| Method | Path | Description |
|---|---|---|
| `POST` | `/devices` | Register a device (hostname, ip, vendor, device_type, credentials) |
| `GET` | `/devices` | List all devices |
| `DELETE` | `/devices/{id}` | Remove a device |

## Module 2 — Device Connectivity

| `POST` | `/devices/{id}/connect` | Opens an SSH session (Netmiko) and confirms the device answers and credentials work. Updates `status` to `reachable` / `unreachable` / `auth_failed`. |

## Module 3 — Command Execution

| `POST` | `/devices/{id}/command` | Runs one command on one device. Body: `{"command": "show ip interface brief", "is_config": false}`. Set `is_config: true` to push a single configuration line instead of a show command. |

## Module 4 — Bulk Command Execution

| `POST` | `/devices/bulk-command` | Runs the same command across many devices **in parallel** via Nornir. Body: `{"device_ids": [1,2,3], "command": "show version"}` or `{"all": true, "command": "..."}` to target the whole inventory (10, 50, 100+ devices). |

## Module 5 — Configuration Backup

| Method | Path |
|---|---|
| `POST` | `/backup/{device_id}` |
| `POST` | `/backup/all` |
| `GET` | `/backups` |

Each backup saves `show running-config` output to
`backups/<hostname>_<UTC timestamp>.txt` and updates the device's
`last_backup` / `status`.

## Module 6 — Automation (VLAN / OSPF / BGP)

| `POST` | `/automation/vlan` | `{"device_ids":[1], "vlan_id":100, "vlan_name":"AUTOMATION", "requested_by":"alice"}` |
| `POST` | `/automation/ospf` | `{"device_ids":[1], "process_id":1, "area":0, "networks":[{"network":"10.10.10.0","wildcard":"0.0.0.255"}], "requested_by":"alice"}` |
| `POST` | `/automation/bgp` | `{"device_ids":[1], "local_asn":65010, "neighbors":[{"ip":"10.0.0.2","remote_asn":65020}], "requested_by":"alice"}` |

Every automation call runs the same workflow, per device:

```
Validate  →  Pre-check  →  Configure  →  Post-check  →  Success
                                                     └──→  Rollback (auto)
                                                            │
                                                            ▼
                                                          Audit
```

1. **Validate** — reject empty/invalid config.
2. **Pre-check** — capture the "before" state (e.g. `show vlan brief`).
3. **Configure** — render the change from a Jinja2 template and push it.
4. **Post-check** — capture the "after" state and check it against a
   success pattern (e.g. does VLAN 100 now appear?).
5. **Success or Rollback** — if the pattern matches, the change is marked
   successful. If not, the platform automatically sends the rollback
   commands (e.g. `no vlan 100`) and marks the change `rolled_back` — the
   device is never left in an unverified state.
6. **Audit** — every outcome (success, rollback, or failure) is written to
   the audit log with the before/after config, regardless of result.

> Note: `authorization` and `approval` gates are called out explicitly in
> the code path as places to plug in real RBAC / change-ticket integration
> — this demo auto-approves, since there's no auth system in place yet.

## Module 7 — Troubleshooting

`POST /troubleshoot`

```json
{
    "source": "192.168.10.1",
    "destination": "10.20.20.10",
    "port": 443
}
```

`source` must already be a registered device (Module 1) — the platform
connects to it via Netmiko and runs the diagnostic pipeline **from that
device's perspective**:

```
ping → traceroute → arp → routing table → interface status → firewall/ACL → TCP port
```

It stops at the first failing step. Example response when everything looks
healthy at the network layer but the application port never answers:

```json
{
    "connectivity": false,
    "failed_at": "firewall",
    "port": 443,
    "recommendation": "Check firewall policy",
    "steps": [ ... ]
}
```

The final TCP check is a direct socket connection from the API server
itself — the application-layer reachability test — which is why an
otherwise-healthy path with no response on the port is attributed to a
firewall/ACL.

## Module 8 — Audit

`GET /audit` returns every configuration-affecting action, newest first:

| Field | Meaning |
|---|---|
| `requested_by` | **Who** made the request |
| `action` | **What** happened (e.g. `automation.vlan`) |
| `timestamp` | **When** |
| `device_hostname` | **Which device** |
| `old_config` | Config snapshot before the change |
| `new_config` | Config snapshot after the change |
| `result` | `success` / `rolled_back` / `failed` |

---

## Testing without real devices

Every module can be exercised with FastAPI's `TestClient` and Netmiko/Nornir
mocked out:

```python
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
client.post("/devices", json={
    "hostname": "router1", "ip": "192.168.10.1", "vendor": "cisco",
    "device_type": "cisco_ios", "username": "admin", "password": "pw",
})

with patch("app.command_service.ConnectHandler") as mock_ch:
    mock_conn = MagicMock()
    mock_conn.find_prompt.return_value = "router1#"
    mock_ch.return_value = mock_conn
    print(client.post("/devices/1/connect").json())
```

This is exactly how the platform was validated during development — every
module (inventory, connect, single/bulk command, backup, VLAN automation
success *and* rollback paths, troubleshooting, and audit) was run end-to-end
against mocked device connections before delivery.

## Notes / production hardening ideas

- **Credentials are stored in plaintext** in this demo. Encrypt at rest
  (e.g. `cryptography.Fernet`) or use a secrets manager in production.
- Add real authentication/authorization and wire it into the `validate` /
  `authorize` stages of Module 6, and record the real caller identity in
  `requested_by` instead of a free-text field.
- Add a genuine **approval gate** (e.g. a change-ticket integration) between
  `authorize` and `pre_check` for anything touching production devices.
- Offload long-running bulk jobs (Module 4/6 against 100+ devices) to a task
  queue (Celery + Redis) instead of blocking the HTTP request, and expose a
  `GET /jobs/{id}` status endpoint.
- The troubleshooting and automation success-pattern parsing use
  intentionally simple regexes tuned for common Cisco IOS phrasing — adapt
  per-vendor for production use (NX-OS, EOS, JunOS output differs).
- Swap SQLite for Postgres in production via `DATABASE_URL` in `database.py`.
