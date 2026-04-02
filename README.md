# 🕵️‍♂️ Network Steganography Lab
### *Hide data in plain sight. Detect what shouldn’t be visible.*

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python%203-blue?logo=python&logoColor=white" alt="Python Badge">
  <img src="https://img.shields.io/badge/Library-Scapy-orange" alt="Scapy Badge">
  <img src="https://img.shields.io/badge/Networking-TCP%2FIP-critical" alt="Networking Badge">
  <img src="https://img.shields.io/badge/Type-Covert%20Channels-success" alt="Covert Channels Badge">
</p>

<p align="center">
  <img src="demo/output2.gif" alt="Network Steganography Lab Demo" width="800">
</p>

---

## 🌌 Overview

Welcome to the **Network Steganography Lab**! This project is a multi-level, hands-on engineering lab designed to explore the fascinating world of **Network Covert Channels**. 

It demonstrates how arbitrary data can be securely and covertly transmitted over standard network infrastructure without triggering traditional security alerts, and progressively explores the cat-and-mouse game of evading detection. The lab evolves across three distinct tiers of stealth: 
**Explicit Signaling ➡️ Field-based Encoding ➡️ Behavioral Timing Channels**.

---

## 🏗️ Project Architecture

```text
network-steganography-lab/
│
├── level1_evil_flag/              # Level 1: Explicit Protocol Flags
├── level2_field_encoding/         # Level 2: Numeric Header Manipulation 
├── level3_timing_based_encoding/  # Level 3: Behavioral Delay Shifts
│
├── docs/                          # Developer Technical Deep Dives
│   ├── level1_notes.md
│   ├── level2_notes.md
│   └── level3_notes.md
│
└── README.md                      # You are here!
```

---

## 📈 The Three Stages of Evasion

This repository acts as a progressive learning tool. Each level increases the difficulty of embedding the data and the complexity of detecting it.

### 🔴 Level 1: The "Evil Bit" Channel (Explicit Signaling)
Data is hidden within the TCP payload, but the receiver is signaled utilizing the unused "Reserved Bit" in the IPv4 header (satirically known as the Evil Bit).
* **Technique**: Protocol flag manipulation.
* **Detection**: Trivial (Rule-based IDS firewalls).

```text
+------------------------------+     +------------------------------+
| IP Header                    |     | TCP Header + Payload         |
|  ├─ src: 127.0.0.1           |     |                              |
|  ├─ dst: 127.0.0.1           | ==> |       [ "Secret Message" ]   |
|  ├─ flags: EVIL (1)   ← 🔴   |     |                              |
+------------------------------+     +------------------------------+
```

### 🟡 Level 2: Header Field Encoding (Implicit Signaling)
Data is moved out of the payload entirely. ASCII characters are converted to integers and injected directly into legitimate, natural-looking numerical protocol headers.
* **Technique**: IP Time-To-Live (TTL) field replacement.
* **Detection**: Statistical Anomaly Detection (Sliding windows).

```text
+------------------------------+     +------------------------------+
| IP Header                    |     | IP Header Decoding           |
|  ├─ TTL: 72   (ASCII 'H')    |     |   72  → H                    |
|  ├─ TTL: 101  (ASCII 'e')    | ==> |   101 → e                    |
|  ├─ TTL: 108  (ASCII 'l')    |     |   108 → l                    |
+------------------------------+     +------------------------------+
```

### 🔵 Level 3: Timing-Based Encoding (Behavioral Signaling)
Data is no longer explicitly written in the packet data at all. The secret message is transmitted exclusively through the microscopic time delays between legitimately formatted, decoy packets.
* **Technique**: Behavioral Timing Delays & Packet Gap Manipulation.
* **Detection**: Very Hard (Requires advanced statistical/machine-learning heuristics).

```text
       0.3s           0.5s           0.3s           0.5s        
[Pkt] ──────> [Pkt] ──────> [Pkt] ──────> [Pkt] ──────> [Pkt]
  |             |             |             |             |
  +--- (0) -----+---- (1) ----+---- (0) ----+---- (1) ----+
```

---

## 🧠 Core Engineering Concepts Covered

- **Packet Forging & Sniffing:** Utilizing Python's `scapy` library to raw-socket build and deconstruct TCP/IP frames.
- **Protocol Internals:** Deep understanding of IPv4 headers, TTL lifecycles, and TCP Handshake flags (`SYN`, `ACK`, `RST`).
- **OS Network Interactions:** Working around Loopback (`lo`) artifacts, ARP resolution timeouts, and OS Kernel overrides.
- **Defensive Engineering:** Writing dynamic Intrusion Detection Systems (IDS) utilizing statistical sliding windows.

---

## 🚀 Getting Started

To explore this lab, navigate to any specific level directory. Each level contains its own specialized `.py` scripts alongside a standalone `README.md` walkthrough.

### Prerequisites:
- Python 3.x
- `scapy` (`pip install scapy`)
- Root access (required for socket-level sniffing/forging)
- Wireshark (highly recommended for live traffic analysis)

**Example execution (from inside any Level directory):**
1. Unfurl the receiver socket: `sudo python receiver.py`
2. Launch the covert signal injector: `sudo python sender.py`

---

## 👨‍💻 Author

**Ayush Kunwar**  
*Turning standard networking protocols against themselves.*

> *"The most dangerous exfiltration techniques are the ones that look completely normal."*
