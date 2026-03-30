# 📡 Level 1: Network Steganography - The "Evil Bit" Covert Channel

<p align="center">
  <img src="https://img.shields.io/badge/Difficulty-Beginner-brightgreen"/>
  <img src="https://img.shields.io/badge/Concept-Covert%20Channels-blue"/>
  <img src="https://img.shields.io/badge/Tool-Scapy-orange"/>
</p>

## 📖 Overview

Welcome to Level 1 of the Network Steganography Lab. This lab demonstrates how data can be stealthily transmitted across a network by manipulating network packet headers specifically, the IPv4 "Evil Bit."

This exercise is designed for beginners to understand the concept of **covert channels**: methods of communication that bypass security policies by hiding data in places it doesn't belong.

**Learning Objectives:**
- Understand the structure of IPv4 and TCP packets.
- Learn how isolated header fields (like the Reserved Bit) can encode hidden information.
- Use Python's `scapy` library to craft, send, and sniff network packets.
- Analyze network traffic using Wireshark to detect anomalies.

---

## 🛠️ The Concept: What is the "Evil Bit"?

Network packets are structured in layers (Ethernet -> IP -> TCP -> Payload). In the **IPv4 Header**, there is a 3-bit `Flags` field. One of these bits is the **Reserved Bit**, which protocol specifications state must be zero (`0`). 

In [RFC 3514](https://datatracker.ietf.org/doc/html/rfc3514) (a humorous April Fools' Day RFC), this bit was jokingly designated as the "Evil Bit" to indicate whether a packet contained malicious intent (`1` for evil, `0` for normal).

While real networks don't use this bit for its "intended" joke purpose, this lab exploits the fact that it is generally ignored by networking equipment. By toggling this bit to `1` (0x4 in IP flags), we signal to a listening receiver that the packet's payload contains part of our hidden message.

### Our Covert Protocol
- **Signal**: Packets with the IP Reserved Bit ("Evil Bit") set to `1` contain a hidden character.
- **Noise**: Packets with the bit set to `0` are standard decoy traffic.
- **Encoding**: 1 Packet = 1 Character hidden in the raw TCP payload.

To simulate realistic stealth, only ~20-30% of the generated traffic contains the hidden message. The rest acts as noise to blend in.

---

## 🚀 Lab Walkthrough

### 📋 Prerequisites
- Python 3.x
- `scapy` library (`pip install scapy`)
- Root/Administrator privileges (required for raw packet manipulation)
- Wireshark (for packet analysis)

### 💻 Step 1: Start the Receiver
The receiver script sniffs network traffic on the loopback (`lo`) interface, filters for packets on port 5000, and looks for the characteristic "Evil Bit".

Open a terminal and run:
```bash
sudo python receiver.py
```
*The script will block and start listening for packets.*

### 💻 Step 2: Run the Sender
The sender script crafts 500 TCP packets, intertwining regular noise packets with special packets bearing the "Evil Bit" and our hidden message payload.

Open a second terminal and run:
```bash
sudo python sender.py
```

### 🎉 Step 3: Observe the Output
Return to your receiver terminal. You should see the hidden message being reconstructed character-by-character out of the noise:
```text
Welcome to the flag section here is your flag: flag{found_me}
```

---

## 🔍 Network Analysis with Wireshark

To truly understand what is happening on the wire, analyze the traffic using Wireshark. A sample capture file is provided: `level1_wireshark.pcapng`.

1. Open `level1_wireshark.pcapng` in Wireshark.
2. Apply the following display filter to isolate packets containing the "Evil Bit":
   ```text
   ip.flags.rb == 1
   ```
3. Look at the isolated packets:
   - Expand the **Internet Protocol Version 4** section -> inspect the **Flags** field. You will see the Reserved bit is Set.
   - Inspect the **TCP > Payload** to see the raw ASCII character transmitted.

---

## 🛡️ Detection & Limitations

**How to detect this?**
In the real world, the IP Reserved bit is almost never set. An Intrusion Detection System (IDS) like Snort or Suricata can easily be configured to trigger an alert if `ip.flags.rb == 1`. 

**Limitations of this Level:**
- **No Encryption**: The payload is sent in plaintext ASCII.
- **No Ordering**: Characters are read in order of arrival, which is fine for the loopback interface, but real networks might deliver packets out of order or drop them.
- **High Visibility**: Relying on an anomalous protocol flag is easily detectable by modern firewalls. 

---

## 🧠 Key Takeaway
> **Covert channels don't just rely on hiding data in the payload—they exploit the structural design and expected behaviors of network protocols.**

Ready for more? Proceed to the next level to explore more sophisticated embedding techniques.

## Lab By Ayush Kunwar