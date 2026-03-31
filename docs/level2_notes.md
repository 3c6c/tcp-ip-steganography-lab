# 🧠 Developer Notes: Level 2 Deep Dive

<p align="center">
  <img src="https://img.shields.io/badge/Focus-Header%20Encoding-purple"/>
  <img src="https://img.shields.io/badge/Audience-Developers%20%26%20Engineers-blue"/>
</p>

## 📖 Introduction

In Level 1, we utilized a designated (albeit unused) protocol flag to signal hidden data. While educational, real-world network defenders can easily flag unexpected binary toggles. 

Level 2 shifts the paradigm entirely by hiding the covert channel inside a perfectly normal, necessary, and constantly fluctuating protocol field: the **IP Time-To-Live (TTL)**. This document captures the engineering decisions, state management challenges, and the introduction of statistical detection mechanics required for this level.

---

## 🏗️ 1. Protocol Design: From Flags to Field Abuse

**The Challenge:** 
Finding a packet header field that is easy to manipulate, visible to network analysis tools, and capable of holding meaningful data without instantly breaking the protocol.

**The Solution:** 
The 8-bit `TTL` field was chosen over alternatives like the IP ID or TCP Sequence Numbers for its simplicity. Because it's exactly 8 bits long, it maps perfectly 1:1 with standard ASCII integer values (0-255). 

Instead of treating the covert channel as just "sneaking data in", it was established as a rigid communication protocol:
- One packet = one character.
- Encoding relies strictly on the naturally occurring IP TTL field.
- Only TCP `SYN` packets are evaluated by the receiver.

> **Key Insight:** Real covert channels avoid explicit "malicious" markers. The safest place to hide data is inside a legitimate field that network firewalls expect to see fluctuating natively.

---

## 🎭 2. Building the Encoder: Signal vs. Realistic Noise

**The Challenge:** 
Directly encoding the message into the TTL of every single packet results in a highly concentrated anomaly. Furthermore, if random decoy noise packets happen to overlap with the ASCII range, the receiver will accidentally decode "garbage" figures and corrupt the secret message string.

**The Solution:** 
Strict numerical boundaries had to be established. 
- **The Signal:** Covert data is restricted exclusively to printable ASCII integers (TTL `32` to `126`).
- **The Noise:** Random decoy packets are assigned TTLs strictly between `130` and `255`, ensuring they never mathematically overlap with the signal range.

To balance stealth and reliability, the sender script was tuned to emit roughly ~20% covert packets mixed into ~80% noise.

> **Key Insight:** A successful covert channel relies on absolute mathematical separation between the intended signal range and the decoy noise range. 

---

## ⏱️ 3. State Management & Message Control

**The Challenge:** 
Initial prototypes generated a fixed number of packets (e.g., exactly 500 packets via a `for` loop). If the randomized noise-to-signal probability skewed heavily toward noise during a particular run, the script would finish before the entire hidden message could be transmitted.

**The Solution:** 
The sender was redesigned to be **data-driven** rather than iteration-driven. The loop now dynamically evaluates the state of the message transmission (`if current_flag_index == len(hidden_flag)`). It only terminates the transmission after the entire string (plus a randomized trailer of extra noise packets) has been successfully pushed over the socket.

> **Key Insight:** Network scripts should rely on dynamic state evaluation rather than hard-coded loops to ensure reliable data delivery regardless of randomized elements.

---

## 🚦 4. Receiver Architecture & Interface Quirks

**The Challenge:** 
Extracting the signal from an infinite, noisy flow of traffic required careful filtering. Furthermore, just like in Level 1, utilizing the loopback interface (`127.0.0.1`) caused immediate packet duplication (capturing both the outbound push and inbound routing reflection).

**The Solution:** 
The receiver logic was made highly selective. It performs a multi-stage validation check on every single packet:
1. Is it a TCP packet?
2. Is the `SYN` flag set? (`0x02`)
3. Is the TTL within the bounded ASCII range? (`32` <= `ttl` <= `126`)

To handle the loopback duplication artifact, the script tracks the `last_char` and implements packet-level deduplication before flushing the character to standard output. Finally, a defined delimiter (`!`) was introduced as a termination signal to allow the receiver to cleanly close its listening socket.

> **Key Insight:** In networking, extracting the signal from the noise is often significantly harder algorithmically than embedding it in the first place.

---

## 🕵️ 5. The Cat and Mouse Game: Statistical Detection

**The Challenge:** 
How does a defender detect a covert channel when the packets are structurally perfect, and the TTL values are technically valid integers? 

Initial detection models attempted simple hardcoded rules (e.g., `If TTL is not exactly 64, 128, or 255 -> throw alert`). However, real networks are messy; varying OS defaults and random router hops mean legitimate TTLs fluctuate frequently. Hardcoded rules generate massive false positives.

**The Solution:** 
The `detector.py` script was introduced. Instead of looking at individual packets, it evaluates traffic structurally using a **sliding window** of the last 20 sequential packets. It calculates a statistical ratio: if more than 50% of the recent TTL values strangely fall exactly within the human-readable ASCII range, it flags an anomaly.

> **Key Insight:** Modern intrusion detection relies on tracking statistical behavior and analyzing anomalies over time, rather than just pattern-matching individual packet flags.
