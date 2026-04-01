# 🧠 Developer Notes: Level 3 Deep Dive

<p align="center">
  <img src="https://img.shields.io/badge/Focus-Timing%20Analysis-purple"/>
  <img src="https://img.shields.io/badge/Audience-Advanced%20Networking-blue"/>
</p>

---

## 📖 Introduction

Level 3 introduces a fundamentally different class of covert channel: **timing-based communication**.

Unlike previous levels, no packet fields or payloads are modified. Instead, information is encoded in the **time delay between packets**.

This document captures the engineering challenges, synchronization issues, timing inaccuracies, and detection insights encountered while building a reliable timing channel.

---

## ⏱️ 1. The Timing vs Packet Misconception

**The Observation:**
Initial implementations attempted to encode data by delaying before sending packets (`sleep → send`), but decoding failed.

**The Root Cause:**
The receiver measures:

```text
time between packet arrivals
```

If delay occurs *before* sending, the first packet has no reference point, and timing becomes inconsistent.

**The Solution:**

```text
send → sleep → send → sleep
```

This ensures each delay is measurable between two packets.

> **Key Insight:** Timing channels encode **inter-packet intervals**, not absolute send times.

---

## 🧠 2. Synchronization Problem (Start of Transmission)

**The Observation:**
Receiver could not determine where actual encoded data begins within noise traffic.

**The Root Cause:**
Unlike Level 1 and 2, there is no explicit marker (flag or field) indicating:

```text
"start decoding now"
```

**The Solution: Preamble**

A known bit pattern was introduced:

```text
11111111
```

This creates a recognizable sequence of long delays:

```text
Packet ─0.5─ Packet ─0.5─ Packet ─0.5─ ...
```

The receiver detects this pattern and begins decoding afterward.

> **Key Insight:** Timing channels require **explicit synchronization**, or decoding becomes impossible.

---

## 🐢 3. Timing Inaccuracy & OS Scheduling

**The Observation:**
Expected delays (0.3s, 0.5s) were inconsistent during capture.

**The Root Cause:**

* Python `sleep()` is not precise
* OS scheduler introduces jitter
* Background processes interfere

Actual delays observed:

```text
0 → 0.27–0.35  
1 → 0.45–0.60
```

**The Solution: Threshold-Based Decoding**

Instead of exact matching:

```text
delay < 0.4 → 0  
delay ≥ 0.4 → 1
```

**Improved Solution (Dead Zone):**

```text
0 → 0.2–0.38  
1 → 0.42–0.6  
ignore → 0.38–0.42
```

> **Key Insight:** Timing channels rely on **ranges, not exact values**.

---

## 🎭 4. Signal vs Noise Separation

**The Observation:**
Mixing noise packets within encoded data caused incorrect decoding and bit misalignment.

**The Root Cause:**
Timing channels depend on a **continuous stream** of delays. Noise packets disrupt:

```text
packet → delay → packet → delay
```

by inserting unpredictable gaps.

**The Solution: Phase Separation**

```text
[Noise] → [Preamble] → [Data] → [Noise]
```

Noise is only allowed:

* before transmission
* after transmission

Never during encoding.

> **Key Insight:** Timing channels require **clean signal windows** for reliable decoding.

---

## 🔢 5. Bit Alignment & Single Bit Failure

**The Observation:**
Decoded message appeared almost correct but contained small errors:

```text
anybod}!   ❌
anybody!   ✅
```

**The Root Cause:**
A single delay was misclassified due to borderline timing → one bit flipped → entire character corrupted.

Example:

```text
y  → 01111001  
}  → 01111101
```

**The Solution:**

* Introduce dead zones
* Increase delay gap (0.3 vs 0.5 → optionally 0.25 vs 0.6)
* Ignore ambiguous values

> **Key Insight:** Timing channels are highly sensitive — **1 bit error = corrupted character**.

---

## 🔄 6. Stream Processing vs Batch Processing

**The Observation:**
Initial decoding logic attempted to collect all bits and decode at once.

**The Root Cause:**

* inefficient
* hard to debug
* delays error detection

**The Solution: Streaming Decode**

```text
collect 8 bits → decode immediately → reset buffer
```

This ensures:

* real-time decoding
* easier debugging
* minimal state complexity

> **Key Insight:** Timing channels behave like **continuous data streams**, not batches.

---

## 📡 7. Receiver as a Time-Series Analyzer

**The Observation:**
Traditional packet inspection methods failed to detect covert data.

**The Root Cause:**
Packets themselves appear normal:

```text
No abnormal headers ❌  
No suspicious payloads ❌  
```

The only signal exists in:

```text
temporal behavior
```

**The Solution:**

Receiver logic was redesigned to:

1. Capture timestamps
2. Compute delays
3. Convert delays → bits
4. Decode bits → characters

> **Key Insight:** Level 3 shifts from **network parsing → signal processing**.

---

## 📊 8. Detection Strategy Evolution

**The Observation:**
Rule-based detection (used in Level 1) and simple anomaly detection (Level 2) failed.

**The Root Cause:**
Timing channels do not violate protocol rules.

**The Solution: Statistical Detection**

Analyze delay distributions:

```text
Normal traffic → random spread  
Covert channel → clustered delays (~0.3 & ~0.5)
```

Detection is based on identifying **structured timing patterns**.

> **Key Insight:** Advanced covert channels require **behavioral and statistical analysis**.

---

## 🚀 Final Takeaways

* Timing channels hide data in **behavior, not packets**
* Synchronization (preamble) is mandatory
* Noise must be isolated from signal
* Small timing errors can corrupt data
* Detection shifts from rules → statistics

---

## 🧠 Closing Thought

> The most sophisticated covert channels don’t modify data —
> they modify **when data is sent**.

---

## Lab by Ayush Kunwar
