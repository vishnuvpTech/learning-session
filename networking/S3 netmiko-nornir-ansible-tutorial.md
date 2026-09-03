# Day 3: Netmiko + Nornir + Ansible

## 🎯 Objective

This is where you move from:

```
Network Engineer
```

towards:

```
Network Automation Engineer
```

By the end of today, you should be able to answer:

1. How does Netmiko connect to and control a network device?
2. When should I use Netmiko vs Nornir vs Ansible?
3. How do I run the same command against many devices in parallel?
4. What's the fundamental philosophical difference between Netmiko and Ansible?
5. What is Jinja2's role in Ansible network automation?

---

## 1. Netmiko

Netmiko is a Python library built on top of Paramiko that simplifies SSH connections to network devices (Cisco, Juniper, Arista, etc.), handling things like prompt detection, paging, and command execution that raw SSH doesn't handle well for network gear.

Basic flow:

```
Python
  ↓
SSH
  ↓
Router/Switch
  ↓
Execute command
```

Example:

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.10",
    "username": "admin",
    "password": "password",
}

connection = ConnectHandler(**device)

output = connection.send_command("show ip interface brief")

print(output)

connection.disconnect()
```

### Key methods to learn

| Method | Purpose |
|---|---|
| `send_command()` | Sends a single "show"-type command and waits intelligently for the prompt to return (best for most read-only commands) |
| `send_command_timing()` | Sends a command and waits based on timing/delay rather than detecting the prompt — useful when a device's prompt behavior is unpredictable |
| `send_config_set()` | Enters config mode and applies a list of configuration commands, then exits config mode |
| `save_config()` | Saves the running configuration to the device's startup configuration (e.g., `write memory` on Cisco) |
| `disconnect()` | Cleanly closes the SSH session |

---

## 🧪 Netmiko Practical

Goal: connect to multiple devices, run a set of commands, and save the output per device.

Suggested project structure:

```
devices/
    router1
    router2
    switch1
backup/
    router1.txt
    router2.txt
    switch1.txt
```

Example script (`backup_devices.py`):

```python
from netmiko import ConnectHandler
import os

devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.10.1",
        "username": "admin",
        "password": "password",
        "name": "router1",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.10.2",
        "username": "admin",
        "password": "password",
        "name": "router2",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.10.3",
        "username": "admin",
        "password": "password",
        "name": "switch1",
    },
]

commands = [
    "show version",
    "show ip interface brief",
    "show ip route",
]

os.makedirs("backup", exist_ok=True)

for dev in devices:
    name = dev.pop("name")
    print(f"Connecting to {name}...")

    try:
        conn = ConnectHandler(**dev)
        output = ""
        for cmd in commands:
            output += f"\n===== {cmd} =====\n"
            output += conn.send_command(cmd)
        conn.disconnect()

        with open(f"backup/{name}.txt", "w") as f:
            f.write(output)

        print(f"{name}: backup saved.")
    except Exception as e:
        print(f"{name}: FAILED - {e}")
```

This produces `backup/router1.txt`, `backup/router2.txt`, `backup/switch1.txt`, each containing the output of the three commands for that device.

---

## 2. Nornir

Netmiko is excellent for:

```
One / a few devices
```

Nornir is a Python **automation framework** that helps orchestrate:

```
10
100
500+
devices
```

...in parallel, with structured inventory, task management, and result aggregation. Under the hood, Nornir's plugins can still use Netmiko to actually talk to each device — Nornir adds the orchestration layer on top.

Architecture:

```
             Nornir
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
      R1       R2       R3
       │        │        │
    Netmiko  Netmiko  Netmiko
```

### Key terms to learn

| Term | Meaning |
|---|---|
| Inventory | The definition of your devices (hosts) and their connection details, usually in YAML files |
| Hosts | Individual devices in the inventory |
| Groups | Logical collections of hosts that share settings (e.g., all "core-routers") |
| Tasks | A unit of work you run against hosts (e.g., "run this command", "push this config") |
| Results | The structured output returned after running a task against your hosts, including success/failure per host |
| Filters | Ways to select a subset of hosts to target (e.g., by group, platform, or custom attribute) |
| Parallel execution | Nornir runs tasks against multiple hosts concurrently (using threads) rather than one at a time |

---

## 🧪 Nornir Scenario

Requirement: across 100 routers, check whether `GigabitEthernet0/1` is UP, and produce a summary.

```
Nornir
  ↓
100 devices
  ↓
Execute command
  ↓
Parse result
  ↓
Return

R1 → UP
R2 → UP
R3 → DOWN
R4 → UP
...
```

Example inventory (`inventory/hosts.yaml`):

```yaml
R1:
  hostname: 192.168.10.1
  groups:
    - routers
R2:
  hostname: 192.168.10.2
  groups:
    - routers
# ... up to R100
```

```yaml
# inventory/groups.yaml
routers:
  platform: ios
  username: admin
  password: password
```

Example task script (`check_interface.py`):

```python
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def check_interface_status(task):
    result = task.run(
        task=netmiko_send_command,
        command_string="show ip interface brief"
    )
    output = result.result

    status = "DOWN"
    for line in output.splitlines():
        if "GigabitEthernet0/1" in line:
            status = "UP" if "up" in line.lower() else "DOWN"

    return status

results = nr.run(task=check_interface_status)

up_count = 0
down_count = 0
summary_lines = []

for host, multi_result in results.items():
    status = multi_result[0].result
    summary_lines.append(f"{host} → {status}")
    if status == "UP":
        up_count += 1
    else:
        down_count += 1

print("\n".join(summary_lines))
print(f"\nTotal Devices: {len(results)}")
print(f"UP:            {up_count}")
print(f"DOWN:          {down_count}")
```

Expected output shape:

```
Total Devices: 100
UP:             96
DOWN:            4
```

This is the core value of Nornir: instead of writing a loop over Netmiko connections yourself, Nornir handles inventory, parallel execution, and structured result collection for you — and scales cleanly from 10 to 500+ devices.

---

## 3. Ansible

The fundamental distinction to understand:

```
Netmiko
=
"Execute this command"
(imperative — you specify the steps)

Ansible
=
"Make the network look like this desired state"
(declarative — you specify the outcome)
```

This distinction matters a lot in practice:

- With Netmiko/Nornir, **you** write the logic: check the current state, decide what to change, send the exact commands.
- With Ansible, you describe the **desired end state** (e.g., "VLAN 10 should exist with this name"), and the underlying module figures out what commands are needed to get there — and often does nothing if the device is already in that state (idempotency).

Example playbook:

```yaml
- name: Configure VLAN
  hosts: switches
  gather_facts: no
  tasks:
    - name: Create VLAN 10
      cisco.ios.ios_vlans:
        config:
          - vlan_id: 10
            name: Developers
        state: merged
```

Running this playbook a second time with no changes needed will report "ok" (no change) rather than re-applying the same commands — that's idempotency, a core Ansible concept that Netmiko scripts don't give you automatically.

### Key concepts to learn

```
Inventory
   ↓
Playbook
   ↓
Tasks
   ↓
Variables
   ↓
Jinja2
   ↓
Network device
```

| Concept | Meaning |
|---|---|
| Inventory | The list of hosts/groups Ansible manages, similar to Nornir's inventory |
| Playbook | A YAML file describing a set of plays (hosts + tasks) to run |
| Tasks | Individual actions within a play, usually calling a module (e.g., `ios_vlans`, `ios_config`) |
| Variables | Reusable values (per host, group, or playbook) that parameterize your tasks |
| Jinja2 | A templating language Ansible uses to generate dynamic configuration (e.g., building a full device config file from variables) |

### Jinja2 example

Template (`vlan_config.j2`):

```
{% for vlan in vlans %}
vlan {{ vlan.id }}
 name {{ vlan.name }}
{% endfor %}
```

With variables:

```yaml
vlans:
  - id: 10
    name: Developers
  - id: 20
    name: HR
```

Rendered output:

```
vlan 10
 name Developers
vlan 20
 name HR
```

This is how Ansible generates device-specific configuration from a single reusable template plus per-host or per-group variables — instead of writing the same VLAN commands by hand for every switch.

---

## Quick-Reference: Netmiko vs Nornir vs Ansible

| | Netmiko | Nornir | Ansible |
|---|---|---|---|
| Type | Library | Framework | Tool/platform |
| Scale | 1–few devices | Many devices, in parallel | Many devices, in parallel |
| Style | Imperative (run this command) | Imperative, but orchestrated | Declarative (desired state) |
| Idempotency | No — you handle it yourself | No — you handle it yourself | Yes, built into most modules |
| Best for | Quick scripts, custom logic, tight control | Custom Python automation at scale | Standardized, repeatable, declarative config management |
| Language | Python | Python | YAML (with Jinja2) |
