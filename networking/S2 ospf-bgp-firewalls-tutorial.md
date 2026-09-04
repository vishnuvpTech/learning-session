# OSPF + BGP + Firewalls

## 🎯 Objective

Understand dynamic routing and security.

---

## 1. Static vs Dynamic Routing

**Static routing** — an admin manually configures each route:

```
Admin
 ↓
Manual route
 ↓
Router
```

- Simple, predictable, no protocol overhead
- Doesn't adapt automatically if a link fails
- Fine for small/simple networks or a single point-to-point link

**Dynamic routing** — routers automatically exchange routing information with each other:

```
Router A ←→ Router B
     OSPF/BGP
Router C ←→ Router D
```

- Adapts automatically to topology changes (link failures, new networks)
- Scales to large/complex networks
- Requires protocol configuration and consumes some CPU/bandwidth for updates

**Rule of thumb:** static routing for small, stable, simple topologies; dynamic routing for anything that needs to scale or self-heal.

---

## 2. OSPF (Open Shortest Path First)

**OSPF = an interior gateway protocol** — it runs *inside* a single organization/network (an Autonomous System), not between separate organizations.

Architecture example:

```
          R2
         /  \
        /    \
      R1 ---- R3
```

How it works, conceptually:

1. Routers discover each other and become **neighbors**, then form **adjacencies**.
2. Each router advertises information about its directly connected links using **LSAs (Link State Advertisements)**.
3. Every router collects all LSAs into an identical **LSDB (Link State Database)** — a full map of the network topology.
4. Each router independently runs the **SPF (Shortest Path First / Dijkstra) algorithm** against the LSDB to calculate the best (lowest-cost) path to every destination.
5. The best paths are installed into the router's **routing table**.

### Key terms to learn

| Term | Meaning |
|---|---|
| Router ID | A unique identifier for each router running OSPF (often the highest loopback/interface IP) |
| Neighbor | A directly connected router running OSPF that has been discovered via Hello packets |
| Adjacency | A fully formed relationship between two neighbors where they exchange full routing info |
| Area | A logical grouping of routers/networks to keep LSDBs smaller and limit flooding |
| Area 0 | The mandatory "backbone" area — all other areas must connect to it |
| LSA | Link State Advertisement — the unit of information routers flood describing their links |
| LSDB | Link State Database — the collected set of all LSAs; identical on every router in an area |
| SPF | Shortest Path First algorithm — computes the best path tree from the LSDB |
| Cost | OSPF's metric, typically derived from interface bandwidth (lower cost = preferred path) |
| DR | Designated Router — elected on multi-access segments to reduce the number of adjacencies |
| BDR | Backup Designated Router — takes over if the DR fails |

Don't try to memorize every LSA type yet — that comes later.

---

## 3. OSPF Practical

Build this topology:

```
R1 -------- R2
 \          /
  \        /
      R3
```

Configure OSPF on all three routers, then verify with:

```bash
show ip ospf neighbor
show ip route
show ip ospf
```

**Objective:** networks behind R3 should be automatically learned by R1, via OSPF:

```
R1
 ↓
OSPF
 ↓
R2
 ↓
R3
```

Then **disconnect a link** (e.g., between R2 and R3) and observe:

- OSPF detects the topology change (Hello timeout or link-down event)
- LSAs are re-flooded to reflect the new topology
- SPF recalculates, and traffic reroutes automatically via the remaining path (R1 → R3 direct, if available) — or the route disappears if no path exists

This hands-on observation of convergence is far more valuable at this stage than memorizing OSPF definitions.

---

## 4. BGP (Border Gateway Protocol)

The key distinction to understand first:

```
OSPF  →  Inside an organization (interior gateway protocol)
BGP   →  Between autonomous systems / large routing domains (exterior gateway protocol)
```

Example — how an enterprise connects to the Internet via two ISPs:

```
          Internet
        /          \
     ISP-A        ISP-B
       │            │
      AS65001      AS65002
        \          /
         Enterprise
          AS65010
```

### Key terms to learn

| Term | Meaning |
|---|---|
| ASN | Autonomous System Number — uniquely identifies a routing domain |
| eBGP | BGP between routers in *different* autonomous systems |
| iBGP | BGP between routers *within the same* autonomous system |
| BGP peer | A router you've established a BGP session with |
| Prefix | A network/subnet being advertised (e.g., `10.10.10.0/24`) |
| Route advertisement | Announcing "I can reach this prefix" to a peer |
| AS_PATH | The list of AS numbers a route has passed through (also used as a loop-prevention mechanism) |
| NEXT_HOP | The IP address to forward traffic to in order to reach the advertised prefix |
| LOCAL_PREF | A value used to prefer one outbound path over another *within* your own AS |
| MED | Multi-Exit Discriminator — a hint to a neighboring AS about which of your entry points to prefer |
| Communities | Tags attached to routes used for policy (e.g., "don't advertise this externally") |
| Route filtering | Controlling which routes are accepted or advertised, for security and policy reasons |
| Best path | The single route BGP selects among multiple options, based on its path-selection algorithm |

### ⭐ BGP Mental Model

Don't try to memorize the full path-selection algorithm yet. Think of it simply as:

```
Router A
"I know 10.10.10.0/24"
        ↓ advertise
Router B
"I learned 10.10.10.0/24 through Router A"
```

**The fundamental job of BGP:** exchange reachability information between autonomous systems, and select the best path when multiple options exist.

---

## 5. Firewalls

Basic flow:

```
Client
  ↓
Firewall
  ↓
Server
```

A firewall evaluates traffic against a policy based on:

```
Source IP
Destination IP
Source Port
Destination Port
Protocol
Direction
Policy (allow/deny)
```

Example rules:

```
ALLOW
10.10.1.0/24 → 10.10.2.10   TCP/443

DENY
Internet → 10.10.2.10       TCP/22
```

The first rule allows an internal subnet to reach a server over HTTPS. The second explicitly blocks SSH access from the public Internet to that same server.

---

## 🧪 Day 2 Scenario

Company topology:

```
Internet
    │
Firewall
    │
Core Router
    │
 ┌──┴────┐
 │       │
App     DB
```

**Requirements:**

```
Internet → App : HTTPS only
App → DB      : PostgreSQL
Internet → DB : DENY
```

### Suggested firewall rule design

```
1. ALLOW  Internet  → App   TCP/443           (public web access)
2. ALLOW  App       → DB    TCP/5432          (application to database)
3. DENY   Internet  → DB    ANY                (explicit deny, defense in depth)
4. DENY   Internet  → App   ANY (all other ports, e.g. SSH/RDP from Internet)
5. DENY   *         → *     ANY                (default-deny / implicit deny at the end)
```

Notes on the design:
- Rule order matters — the firewall checks rules top-to-bottom and stops at the first match, so specific ALLOW rules go before broader DENY rules.
- Rule 3 is technically redundant if the default policy is deny-all, but making it explicit is good practice (defense in depth, clarity, auditability).
- Only the exact port needed (443, 5432) is opened — not entire IP ranges or protocols.

### Why should the database not be directly accessible from the Internet?

This should tie together four ideas:

- **Segmentation** — separating the App and DB into different network zones (with a firewall between them) means a compromise in one zone doesn't automatically grant access to the other. The DB sits behind an additional layer (the App tier), not directly exposed.
- **Least privilege** — each component should only have the access it strictly needs to do its job. The App needs to talk to the DB; the general public/Internet does not. Granting no more access than necessary limits what an attacker can do even if they get in somewhere.
- **Ports** — exposing a database port (e.g., PostgreSQL's 5432) to the Internet directly exposes the database's authentication and query interface to anyone in the world, including automated scanners constantly probing for open DB ports.
- **Attack surface** — every service reachable from the Internet is a potential entry point. Keeping the DB reachable *only* from the App tier (not the Internet) dramatically shrinks the number of ways an attacker could reach sensitive data — they'd first have to compromise the App tier, which is itself protected and monitored.

In short: the App tier acts as a controlled gatekeeper — it validates requests, enforces business logic and authentication, and only *it* is trusted to talk to the database. Removing that gatekeeper by exposing the DB directly would mean anyone on the Internet could attempt to authenticate against (or exploit vulnerabilities in) the database engine itself, with no application-layer protection in between.
