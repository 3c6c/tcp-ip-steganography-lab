# 🧠 Developer Notes: Level 1 Deep Dive

<p align="center">
  <img src="https://img.shields.io/badge/Focus-Network%20Internals-purple"/>
  <img src="https://img.shields.io/badge/Audience-Developers%20%26%20Engineers-blue"/>
</p>

## 📖 Introduction

While the main lab documentation explains *how* to use the Level 1 covert channel, this document captures the real-world engineering challenges, network quirks, and insights discovered while building it. 

Networking is rarely as simple as sending a packet from point A to point B. The underlying Operating System (OS) network stack, interface artifacts, and protocol rules constantly interfere. These notes document those pitfalls and the solutions implemented.

---

## 🏗️ 1. The Loopback Duplication Phenomenon

**The Observation:** 
When sending crafted packets to `127.0.0.1` (localhost), the receiver script captured every packet twice (e.g., `WWeellccoommee`).

**The Root Cause:**
The loopback interface (`lo`) operates differently from a physical Network Interface Card (NIC). Every packet sent to `127.0.0.1` is captured twice by a packet sniffer:
1. As an **outgoing** packet from the application to the network stack.
2. As an **incoming** packet routed back to the application.

**The Solution:**
Rather than implementing a complex deduplication system, the receiver script was updated to keep track of the most recently received character. If an immediate duplicate is detected, it is ignored before rebuilding the hidden message string.

> **Key Insight:** Packet sniffers capture traffic at the interface level, meaning interface quirks (like loopback mirroring) must be handled by the application logic.

---

## 🚦 2. OS Network Interference (TCP RST Packets)

**The Observation:**
Unexpected `RST` (Reset) and `ACK` (Acknowledgment) packets were appearing alongside our crafted covert packets in the network capture.

**The Root Cause:**
When our Python script crafts and sends raw TCP packets using `scapy`, the host OS network stack is still actively managing the network interfaces. Since our script isn't running an actual TCP service on port 5000, the OS's kernel observes incoming `SYN` packets to a closed port and automatically replies with a `RST`/`ACK` packet to reject the connection based on the TCP specification.

**The Solution:**
This is treated as part of the environment's "noise." Our receiver simply ignores these irrelevant kernel responses and looks exclusively for packets bearing the covert "Evil Bit".

> **Key Insight:** Raw sockets allow you to inject traffic, but you are not the sole entity on the network. The OS stack acts independently and will enforce standard TCP/IP behaviors.

---

## 🐢 3. ARP Resolution and Packet Speed Bottlenecks

**The Observation:**
Initially attempting to send packets to randomly generated, non-existent "fake" IP addresses caused massive delays and performance issues, throwing warnings like: `WARNING: MAC address not found → using broadcast`.

**The Root Cause:**
When utilizing the Layer 3 `send()` function in `scapy`, the OS is still responsible for routing. Before an IP packet can hit the wire, the OS must resolve the destination MAC address using the **Address Resolution Protocol (ARP)**. When sending packets to non-existent IPs, ARP requests fail and timeout, creating a massive bottleneck for every single packet.

**The Decision (send vs. sendp):**
We could have utilized `sendp()` to inject traffic directly at Layer 2 (Ethernet), which circumvents ARP resolution completely. However, using `send()` was chosen for this level as it better simulates realistic, routable Layer 3 traffic. Instead of random IPs, we constrain traffic to localhost, avoiding ARP timeouts while maintaining realism.

> **Key Insight:** Bypassing ARP requires dropping to Layer 2, but doing so heavily sacrifices real-world routing simulation.

---

## 💻 4. Packet Crafting Nuances with Scapy

**The Challenge:**
Understanding how to access nested data effectively within Scapy packet structures. Novice developers often attempt flat object property access (e.g., `packet.dst`), leading to errors.

**The Solution:**
A network packet is a stacked Matryoshka doll of layers. Scapy reflects this accurately. Data must be accessed explicitly by layer:
- `pkt[IP].src` for Layer 3 data.
- `pkt[TCP].flags` for Layer 4 data.
- `pkt[Raw].load` for application payloads.

Additionally, raw payloads are inherently `bytes` objects in Python (e.g., `b'Hello'`). These must be explicitly decoded into string literals for logical evaluation.

> **Key Insight:** Network data is raw bytes wrapped in nested headers. Interpretations (like strings) are purely application responsibilities.

---

## 🎭 5. The Philosophy of Stealth: Signal vs. Noise

**The Challenge:**
A covert channel that consists of 100% malicious traffic isn't covert—it's incredibly obvious. The original randomization logic for injecting the covert signal into the noise floor had an accidental bug (`if rand_num / 2:` always resolved to `True`), meaning every packet transmitted data.

**The Solution:**
The logic was rewritten to be strictly probability-based. In the current iteration, realistic network "noise" (empty packets, half-open connections) represents 70-80% of the traffic, while the covert "signal" hides within the remaining 20-30%. 

Balancing probability is the fundamental challenge of network steganography:
- **High Covert Percentage:** Fast data transmission, but highly detectable.
- **Low Covert Percentage:** Very stealthy, but painfully slow.

> **Key Takeaway:** Building a covert channel is easy; blending it into normal network behavior is the true engineering challenge.


## Lab by Ayush Kunwar