# Networking + Routing + Automation — Interview Prep Q&A

A condensed review covering the full track: core networking, routing, and network automation.

---

## Networking

### 1. What happens when you type a URL in a browser?

1. **DNS resolution** — the browser asks a resolver for the IP behind the domain name.
2. **TCP handshake** — `SYN → SYN-ACK → ACK` opens a connection to that IP (usually port 443).
3. **TLS handshake** — client and server negotiate encryption and verify the server's certificate.
4. **HTTP request/response** — the browser sends a GET request over the encrypted connection; the server responds with the page.
5. **Routing/switching** — every packet is carried in IP (Layer 3) across networks and Ethernet frames (Layer 2) across each local link, hop by hop, in both directions.
6. **Rendering** — the browser parses and renders the HTML/CSS/JS, often triggering more requests for images, scripts, etc.

### 2. TCP vs UDP?

- **TCP**: connection-oriented (3-way handshake), reliable (retransmits lost data), ordered, flow-controlled. Higher overhead. Used by HTTP/HTTPS, SSH, databases.
- **UDP**: connectionless, no delivery/order guarantees, minimal overhead, lower latency. Used by DNS, DHCP, VoIP, streaming.
- Rule of thumb: TCP when correctness matters more than speed; UDP when speed matters more than occasional loss.

### 3. What is a subnet?

A logical subdivision of an IP network that defines which addresses can reach each other directly (same subnet) versus which require a router to reach (different subnet). Defined by a mask/prefix, e.g. `192.168.1.0/24`.

### 4. What is CIDR?

**Classless Inter-Domain Routing** — the notation and system (`a.b.c.d/n`) for representing an IP network and its prefix length, replacing old class-based (A/B/C) addressing. It lets networks be sized flexibly (any prefix length, not just /8, /16, /24) and enables **route summarization/aggregation**, which keeps routing tables smaller.

### 5. What is a default gateway?

The router a host sends traffic to when the destination address is **not** on its local subnet. It's the host's "exit door" to every other network, configured alongside the host's IP and subnet mask.

### 6. Router vs switch?

| | Switch | Router |
|---|---|---|
| Layer | 2 (Data Link) | 3 (Network) |
| Forwards by | MAC address | IP address |
| Connects | Devices within a network | Separate networks |
| Learns | MAC → port | Network → next hop |

### 7. What is a VLAN?

A **Virtual LAN** — a way to logically separate devices on the same physical switch into independent broadcast domains, as if they were on separate physical networks (e.g. VLAN 10 = Engineering, VLAN 20 = HR). Devices in different VLANs can't reach each other without going through a router (inter-VLAN routing).

### 8. Access vs trunk?

- **Access port**: belongs to a single VLAN; connects end devices (PCs, printers). Frames leave/enter untagged.
- **Trunk port**: carries traffic for multiple VLANs simultaneously, tagging each frame with its VLAN ID via **802.1Q**. Used between switches, or between a switch and a router doing inter-VLAN routing.

### 9. What is ARP?

**Address Resolution Protocol** — resolves a known IP address to its MAC address on a local segment. Before a host can send a frame to another host on the same subnet, it broadcasts "who has this IP?" and caches the MAC address it gets back in its ARP table.

### 10. What is NAT?

**Network Address Translation** — rewrites source/destination IP addresses (and often ports) as traffic crosses a router/firewall, most commonly to translate many private internal IPs to one public IP for internet access. Benefits: conserves scarce public IPv4 addresses and hides internal network topology from the outside.

---

## Routing

### 11. Static vs dynamic routing?

- **Static**: an admin manually configures each route. Simple and predictable but doesn't adapt to topology changes.
- **Dynamic**: routers automatically exchange routing information (OSPF, BGP, etc.) and adapt to link failures/topology changes. Scales better for complex networks.

### 12. How does a router select a route?

For a given destination, among all matching routes, the router picks by:

1. **Longest prefix match** — the most specific matching route wins (see Q13).
2. **Administrative distance** — if multiple *protocols/sources* offer a route to the same prefix, the one with the lowest AD (most trusted source) wins (e.g. directly connected > static > eBGP > OSPF > iBGP).
3. **Metric/cost** — if still tied within the same protocol, the lowest metric (OSPF cost, BGP attributes, etc.) wins.

### 13. What is longest prefix match?

When multiple routes in the table could match a destination, the router selects the **most specific** one (the longest subnet mask/prefix). Example: with routes `10.0.0.0/8`, `10.10.0.0/16`, and `10.10.10.0/24` all in the table, a packet to `10.10.10.50` is forwarded via the `/24` route — it's the longest (most specific) match.

### 14. OSPF vs BGP?

| | OSPF | BGP |
|---|---|---|
| Type | Interior Gateway Protocol (IGP) | Exterior Gateway Protocol (EGP) |
| Scope | Inside one organization/AS | Between autonomous systems |
| Algorithm | Link-state (SPF/Dijkstra) | Path-vector |
| Goal | Fastest internal convergence | Policy-based reachability between networks |

### 15. What is an OSPF neighbor?

A directly connected router running OSPF that has been discovered via **Hello packets** and matches the required parameters (same area, timers, subnet, etc.). Neighbors may go on to form a full **adjacency**, where they exchange complete routing (link-state) information.

### 16. What is Area 0?

OSPF's mandatory **backbone area**. In a multi-area OSPF design, every other area must connect directly to Area 0 — inter-area traffic always transits through it. This structure keeps link-state databases smaller per area while still allowing full reachability.

### 17. What is a BGP ASN?

An **Autonomous System Number** — a unique number identifying a routing domain (an organization's or ISP's network) under a single administrative routing policy. BGP uses ASNs to identify where routes originate and to build the AS_PATH.

### 18. eBGP vs iBGP?

- **eBGP** (external): a BGP session between routers in **different** autonomous systems — how organizations exchange routes with each other/the internet.
- **iBGP** (internal): a BGP session between routers **within the same** AS — used to carry externally-learned BGP routes consistently across an organization's internal network.

### 19. What is AS_PATH?

A BGP path attribute listing the sequence of AS numbers a route advertisement has passed through. It serves two purposes: **loop prevention** (a router rejects a route if its own ASN is already in the path) and as an input to **best-path selection** (shorter AS_PATH is generally preferred).

### 20. What is LOCAL_PREF?

A BGP attribute used to express preference among multiple **outbound** paths to the same destination, *within your own AS* — higher LOCAL_PREF wins. Unlike AS_PATH/MED, it's only exchanged over iBGP (never advertised to external peers), so it lets an organization control which of its own exit points (e.g. which ISP) its internal traffic uses.

---

## Automation

### 21. Why Netmiko?

Because raw SSH (e.g. Paramiko) doesn't handle network-device quirks well — inconsistent prompts, pagination ("--More--"), and vendor-specific CLI behavior. Netmiko wraps SSH with device-aware logic (prompt detection, disabling paging, config-mode entry/exit) across many vendors, so you can write `send_command()`/`send_config_set()` instead of hand-rolling terminal handling for each platform.

### 22. Netmiko vs Nornir?

- **Netmiko** is a library for connecting to and controlling *one* device (or a hand-rolled loop over a few).
- **Nornir** is an orchestration **framework** built for running tasks (often via the Netmiko plugin under the hood) across many devices *in parallel*, with structured inventory, filtering, and aggregated results.
- In short: Netmiko is the "how do I talk to a device," Nornir is the "how do I run this across my whole fleet."

### 23. Why use Nornir?

- Built-in **inventory** (hosts, groups, defaults) instead of hand-written device loops.
- **Parallel execution** out of the box (threaded runner), so 500 devices don't run one at a time.
- **Structured results** per host (success/failure, exceptions) instead of parsing print statements.
- **Pure Python** — full programming power (conditionals, custom logic, existing Python libraries) rather than being constrained to a DSL.
- Pluggable — swap in different connection plugins (Netmiko, NAPALM, Scrapli) without rewriting task logic.

### 24. Nornir vs Ansible?

| | Nornir | Ansible |
|---|---|---|
| Style | Imperative — you write the Python logic | Declarative — you describe desired state |
| Idempotency | Not automatic — you implement it | Built into most modules |
| Language | Python | YAML (+ Jinja2) |
| Best for | Custom logic, tight control, complex conditional workflows | Standardized, repeatable, declarative config management; huge existing module ecosystem |

Many teams use both: Nornir/Python for custom orchestration and data processing, Ansible for standardized, idempotent config pushes.

### 25. What is idempotency?

The property that applying an operation multiple times produces the same end result as applying it once — running the same playbook/task twice causes no unintended side effects, and if the device is already in the desired state, nothing changes (and it's reported as "ok," not "changed"). This is central to Ansible's model and to any safe automation workflow, since it means retries and periodic enforcement runs are safe by default.

### 26. How do you automate 500 devices?

- **Inventory-driven**: pull the device list from a source of truth (DB/NetBox/CMDB), grouped logically (site, role, vendor).
- **Parallel execution** with a bounded worker pool (Nornir's `ThreadedRunner`, Ansible's `forks`) so you're not serial, but also not overwhelming devices/links.
- **Batch/stagger rollout**: canary a small subset first, then wave the rest, rather than pushing to all 500 simultaneously.
- **Async task queue** (Celery + Redis, or similar) so the API request returns immediately and the job runs in the background, with a job-status endpoint to poll.
- **Per-device isolation**: one device's failure must never abort the whole batch — collect results independently (see Q27).
- **Idempotent, verified changes**: pre-check/post-check every change so partial failures are detected, not assumed.
- **Structured logging + audit** for every device's outcome, and a clear summary report at the end.

### 27. How do you handle failed devices?

- **Isolate failures per device** — one unreachable/broken device shouldn't stop or corrupt the run for the other 499 (this is exactly why Nornir/Ansible return per-host results rather than a single pass/fail).
- **Classify the failure** (auth failure vs timeout vs command error vs post-check mismatch) so the response is actionable, not just "failed."
- **Retry transient failures** (timeouts, transient SSH errors) with backoff; don't retry permanent ones (bad credentials, syntax errors).
- **Never mark success without verification** — a device that accepted the config but fails post-check should be treated as failed (and rolled back), not successful.
- **Log and surface it** — write to the audit trail, return it in the API response, and alert if the failure rate crosses a threshold.

### 28. How do you implement rollback?

1. **Snapshot before changing** — capture a pre-check baseline (either the specific relevant config, e.g. `show vlan brief`, or a full `show running-config` backup) before touching anything.
2. **Define the inverse commands up front** — for every change, know its rollback (`vlan 100` → `no vlan 100`), not something you improvise after the fact.
3. **Verify after changing** — run a post-check against a known success pattern.
4. **Auto-rollback on failed verification** — if the post-check doesn't confirm the expected state, immediately send the rollback commands rather than leaving the device in an unknown state.
5. **Log everything** — record the before state, after state, and rollback outcome to the audit trail either way.
6. For bigger/riskier changes, prefer platform features like Cisco's `configure replace` (full config rollback to a saved checkpoint) over hand-written inverse commands.

### 29. How do you securely store device credentials?

- **Never store plaintext** in a database, config file, or source control.
- **Encrypt at rest** (e.g. `cryptography.Fernet`) if credentials must live in your own datastore, with keys managed separately from the data.
- Prefer a dedicated **secrets manager** (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) so credentials are fetched at runtime, not persisted in your app's DB at all.
- Where possible, use **AAA/TACACS+/RADIUS** for centralized device authentication instead of static local accounts — this also centralizes auditing of who logged into what.
- Prefer **SSH keys/certificates** over passwords where the platform supports it.
- Apply **least privilege**: automation service accounts should have only the access they need (e.g. read-only accounts for backup jobs vs. privileged accounts for config changes).
- **Rotate credentials** regularly and **audit access** to the secrets store itself.

### 30. How would you design a network automation platform?

At a high level:

```
User / API client
      │
      ▼
   FastAPI (or similar) — auth/RBAC, request validation
      │
      ├── Device Inventory  (source of truth: DB, synced from NetBox/CMDB)
      ├── Jobs API           (submit/track automation jobs)
      └── Monitoring          (device status, job history)
      │
      ▼
  Task Queue (Celery + Redis)  — decouples the API from long-running work,
                                  enables scaling workers horizontally
      │
      ├── Nornir  (custom orchestration/parallel execution)
      └── Ansible (standardized, idempotent config modules)
      │
      ▼
  Netmiko / NAPALM / Scrapli — the actual device connections
      │
      ▼
  Network Devices
```

Key design principles to call out:

- **Every change follows**: Validate → Authorize → Approve → Pre-check → Configure → Post-check → Success/Rollback → Audit. Never blindly execute a request.
- **Async by default** for anything touching more than a handful of devices — return a job ID immediately, let workers process in the background.
- **Full audit trail**: who, what, when, which device, old config, new config, result — for every configuration-affecting action.
- **Secrets management** as described in Q29, not credentials sitting in the app database in plaintext.
- **Idempotent, verified operations** everywhere — a "successful" change is one that was verified, not just one that didn't error.
- **Extensibility**: pluggable connection backends (Netmiko today, maybe NAPALM/Scrapli/gNMI tomorrow) and pluggable automation modules (VLAN/OSPF/BGP today, more later) without rearchitecting the core workflow engine.
- **Observability**: structured logging, metrics (success/failure rates, job duration), and alerting on abnormal failure rates — not just an audit log nobody looks at until something breaks.
