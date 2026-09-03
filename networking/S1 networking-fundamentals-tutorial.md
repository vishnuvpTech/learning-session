# Networking Fundamentals for Automation Engineers

## Learning Objectives

By the end of this tutorial, you should be able to answer:

1. What happens when I open google.com?
2. What is an IP address?
3. What is a subnet?
4. How does a router select a route?
5. What is a MAC address?
6. Router vs switch?
7. What is a VLAN?
8. What is TCP?
9. TCP vs UDP?
10. What happens when ping fails?
11. How does traffic move between two networks?

---

## 1. The OSI Model

Don't memorize every detail on day one — understand the **flow** first.

```
Layer 7   Application      HTTP, DNS, SSH
Layer 6   Presentation     Encryption, encoding
Layer 5   Session          Session management
Layer 4   Transport        TCP / UDP
Layer 3   Network          IP / ICMP / Routing
Layer 2   Data Link        MAC / Ethernet / VLAN
Layer 1   Physical         Cables, signals, NICs
```

For automation/network engineering, **Layers 2–4** matter most day-to-day.

Example — sending an HTTP request:

```
HTTP
 ↓
TCP
 ↓
IP
 ↓
Ethernet
 ↓
Physical Network
```

---

## 2. TCP/IP in Practice

### What happens when I open google.com? (Q1)

This ties the whole stack together. At a high level:

1. **DNS resolution** — your browser asks a DNS resolver "what is the IP for google.com?" and gets back something like `142.250.x.x`.
2. **TCP connection** — your OS opens a TCP connection to that IP on port 443 (HTTPS), using a 3-way handshake: `SYN → SYN-ACK → ACK`.
3. **TLS handshake** — client and server negotiate encryption and verify certificates.
4. **HTTP request/response** — the browser sends an HTTP GET request over the encrypted TCP connection; the server responds with the page data.
5. **Routing/switching** — each packet is wrapped in IP (Layer 3) to get routed across networks, and in Ethernet frames (Layer 2) to move across each local link, hop by hop, until it reaches Google's server — and the response follows the reverse path back.
6. **Rendering** — the browser parses the HTML/CSS/JS and renders the page, often triggering more DNS lookups and TCP connections for images, scripts, etc.

Conceptually, running `curl https://example.com` follows the same path:

```
Application
    ↓
HTTP/HTTPS
    ↓
TCP
    ↓
IP
    ↓
Ethernet
    ↓
Network
```

### What is TCP? (Q8)

TCP (Transmission Control Protocol) is a **connection-oriented, reliable** Layer 4 protocol. It provides:

- **Connection establishment** — 3-way handshake (SYN, SYN-ACK, ACK)
- **Reliable delivery** — lost packets are detected and retransmitted
- **Ordering** — packets are reassembled in the correct sequence even if they arrive out of order
- **Flow control** — prevents a fast sender from overwhelming a slow receiver

### What is UDP, and TCP vs UDP? (Q9)

UDP (User Datagram Protocol) is **connectionless** and lightweight. It provides:

- No handshake — just sends the data
- Lower overhead, lower latency
- **No guarantee** of delivery, ordering, or retransmission — the application must handle that itself if needed

| | TCP | UDP |
|---|---|---|
| Connection | Yes (handshake) | No |
| Reliability | Guaranteed delivery | Best-effort, no guarantee |
| Ordering | Guaranteed | Not guaranteed |
| Speed/overhead | Slower, more overhead | Faster, less overhead |
| Use case | Needs accuracy | Needs speed |

```
TCP                          UDP
├── HTTP/HTTPS                ├── DNS
├── SSH                       ├── DHCP
├── PostgreSQL                ├── VoIP
└── SMTP                      └── Streaming
```

**Rule of thumb:** TCP when correctness matters more than speed (file transfer, web pages, database queries). UDP when speed matters more than occasional loss (live video, voice calls, DNS lookups).

### Practical commands

Run these and understand what each one tells you:

```bash
ping 8.8.8.8          # Is the host reachable? What's the round-trip latency?
traceroute 8.8.8.8     # What path (hops) does traffic take to get there?
tracepath 8.8.8.8      # Linux alternative to traceroute, no root needed
curl -v https://example.com   # Shows DNS, TCP connect, TLS handshake, HTTP request/response
ss -tulnp             # Shows which processes are listening on which TCP/UDP ports
```

---

## 3. IP Addressing

### What is an IP address? (Q2)

An IP address is a numeric label assigned to a device on a network, used to identify it and route traffic to it — like a postal address for a computer. IPv4 addresses look like `192.168.1.10` (32 bits, four 8-bit octets).

### What is a subnet? (Q3)

A subnet is a logical subdivision of an IP network. It defines which addresses belong to the same local network (and can talk directly to each other) versus which addresses are "elsewhere" and require a router to reach.

The subnet is expressed with a **mask** or **CIDR prefix**. Example:

```
192.168.1.10/24
```

This means:

```
Network: 192.168.1.0
Host:    192.168.1.10
Mask:    255.255.255.0
```

The `/24` says: "the first 24 bits identify the network, the remaining 8 bits identify the host."

### Common CIDR blocks

| CIDR | Addresses | Typical use |
|---|---|---|
| /8  | ~16,777,216 | Very large network |
| /16 | 65,536 | Large network |
| /24 | 256 | Common LAN |
| /25 | 128 | Smaller LAN |
| /26 | 64 | Smaller subnet |
| /27 | 32 | Small subnet |
| /28 | 16 | Very small subnet |
| /30 | 4 | Point-to-point link |
| /32 | 1 | Single host |

For a `/24`:

```
192.168.1.0/24
Network     192.168.1.0
Hosts       192.168.1.1 - 192.168.1.254
Broadcast   192.168.1.255
```

(2 addresses in every subnet are reserved — the network address and the broadcast address — so usable hosts = total addresses − 2.)

---

## 4. Routing

### How does traffic move between two networks? (Q11)

Imagine:

```
PC1
192.168.1.10
     │
     ▼
Router
     │
     ▼
10.10.10.0/24
     │
     ▼
Server
10.10.10.20
```

PC1 wants to reach `10.10.10.20`:

1. PC1 checks: **is 10.10.10.20 in my local subnet?** No (it's not in `192.168.1.0/24`).
2. So PC1 sends the packet to its **default gateway** (`192.168.1.1`), the router.
3. The router looks up its **routing table** to decide where to forward the packet next.

Example routing table:

```
Destination       Next Hop
192.168.1.0/24    Connected
10.10.10.0/24     172.16.1.2
0.0.0.0/0         ISP
```

4. The router forwards the packet toward `10.10.10.0/24`, and this repeats hop-by-hop until the packet reaches the destination network, where the local router/switch delivers it to the server. Return traffic follows the same process in reverse.

### How does a router select a route? (Q4) — Longest Prefix Match

When multiple routes could match a destination, the router picks the **most specific** one — this is called **Longest Prefix Match**.

Suppose the routing table contains:

```
10.0.0.0/8
10.10.0.0/16
10.10.10.0/24
```

Destination: `10.10.10.50`

**Which route wins? `10.10.10.0/24`** — because it is the most specific (longest prefix) route that matches the destination address. This is a very common interview question.

---

## 5. Switching

### What is a MAC address? (Q5)

A MAC address is a hardware identifier burned into a network interface card (NIC), used at Layer 2 to deliver frames within the same local network segment. It looks like `AA:BB:CC:DD:EE:FF` and, unlike an IP address, is (in theory) globally unique and doesn't change based on what network you connect to.

### Router vs switch? (Q6)

| | Switch | Router |
|---|---|---|
| Layer | Layer 2 (Data Link) | Layer 3 (Network) |
| Works with | MAC addresses | IP addresses |
| Purpose | Connects devices *within* a network | Connects *different* networks |
| Learns | MAC → Port mappings | Network → Next Hop mappings |

```
PC1 ─── Switch ─── Router ─── Switch ─── PC2
```

The switch learns which MAC address lives on which physical port and forwards frames locally. The router looks at destination IP addresses and decides which network to forward the packet toward, connecting otherwise-separate networks.

---

## 6. VLAN

### What is a VLAN? (Q7)

A VLAN (Virtual LAN) lets you logically separate devices on the *same physical switch* into different broadcast domains, as if they were on separate physical networks.

Example: one physical switch carrying three logical networks:

```
VLAN 10 → Developers
VLAN 20 → HR
VLAN 30 → Management
```

Devices in VLAN 10 cannot talk directly to devices in VLAN 20, even though they're plugged into the same switch — traffic between VLANs must pass through a router (inter-VLAN routing).

Key terms:

- **Access port** — belongs to a single VLAN; connects end devices (PCs, printers)
- **Trunk port** — carries traffic for multiple VLANs, tagged with **802.1Q** headers; used between switches or to a router
- **VLAN ID** — the number identifying each VLAN (1–4094)
- **Inter-VLAN routing** — a router (or Layer 3 switch) forwards traffic between VLANs

```
                 Router
                   │
                 Trunk
                   │
                Switch
             /     |     \
          VLAN10 VLAN20 VLAN30
```

---

## 7. Practical Lab

Build this topology in Cisco Packet Tracer, GNS3, or EVE-NG:

```
PC1
 |
Switch1
 |
Router1
 |
Router2
 |
Switch2
 |
PC2
```

**Addressing plan:**

```
PC1 = 192.168.10.10/24
GW  = 192.168.10.1

PC2 = 192.168.20.10/24
GW  = 192.168.20.1

Router link:
Router1 = 10.0.0.1
Router2 = 10.0.0.2
```

**Steps:**

1. Configure the IP addresses above on PC1, PC2, and both router interfaces.
2. Configure **static routes** so Router1 knows how to reach `192.168.20.0/24` (via Router2) and Router2 knows how to reach `192.168.10.0/24` (via Router1).
3. Verify connectivity:

```bash
ping 192.168.20.10
```

4. **Break it intentionally:** change PC2's gateway to an incorrect address (e.g. `192.168.20.99`), then troubleshoot why ping fails.
5. **Remove the static route** from Router1, then troubleshoot again.

### What happens when ping fails? (Q10) — Troubleshooting flow

Work through this checklist in order:

```
Ping failure
     ↓
IP?          — Does the source/destination have a valid, correctly-configured IP address?
     ↓
Gateway?     — Is the default gateway set correctly, and is it reachable?
     ↓
Route?       — Does a route exist (in the routing table) to the destination network?
     ↓
Interface?   — Is the physical/logical interface up, and is the cable/link healthy?
     ↓
Firewall?    — Is a firewall (host-based or network) blocking ICMP or the traffic path?
```

Practical diagnostic commands at each stage:

- **IP** — `ip addr` / `ipconfig`
- **Gateway** — `ip route` / `route print`, then `ping <gateway>`
- **Route** — `traceroute` / `tracepath` to see where the path breaks
- **Interface** — `ip link` / check interface status lights, `show interfaces` on Cisco gear
- **Firewall** — check `iptables`/`nftables`, Windows Firewall, or router ACLs for ICMP-blocking rules

---

## Quick-Reference Answer Sheet

| Question | Short Answer |
|---|---|
| What happens when I open google.com? | DNS resolves the name → TCP handshake → TLS handshake → HTTP request/response, routed via IP/Ethernet hop by hop |
| What is an IP address? | A numeric address identifying a device on a network, used for routing |
| What is a subnet? | A logical subdivision of an IP network defining which hosts are "local" |
| How does a router select a route? | Longest Prefix Match — the most specific matching route wins |
| What is a MAC address? | A hardware address identifying a NIC on a local network segment |
| Router vs switch? | Switch = Layer 2, forwards by MAC within a network; Router = Layer 3, forwards by IP between networks |
| What is a VLAN? | A logical separation of devices on one physical switch into isolated broadcast domains |
| What is TCP? | A reliable, connection-oriented Layer 4 protocol with handshake, ordering, and retransmission |
| TCP vs UDP? | TCP = reliable but slower; UDP = fast but no delivery guarantee |
| What happens when ping fails? | Troubleshoot in order: IP → Gateway → Route → Interface → Firewall |
| How does traffic move between two networks? | Host sends to its default gateway → router forwards via its routing table hop-by-hop to the destination network |
