# 📡 Level 3: Network Steganography - Timing-Based Encoding

<p align="center">
  <img src="https://img.shields.io/badge/Difficulty-Advanced-red"/>
  <img src="https://img.shields.io/badge/Concept-Timing%20Channels-blue"/>
  <img src="https://img.shields.io/badge/Tool-Scapy-orange"/>
</p>

## 📖 Overview

Welcome to Level 2 of the Network Steganography Lab! 

In Level 1, we learned how to use a simple binary ON/OFF flag (the "Evil bit") to signal that our regular packets contained hidden payload data. Level 2 takes things a step further. We are no longer relying on the payload at all; instead, we are hiding our data directly inside a standard numeric header field: **The IP Time-to-Live (TTL)**.

This exercise is designed for beginners to understand how protocol fields with variable numeric values can be repurposed to carry ASCII text characters. It also introduces the concept of **statistical detection** from a network defender's perspective.

**Learning Objectives:**
- Understand the legitimate purpose of the IP TTL field.
- Learn how to convert text strings into raw ASCII integers, replacing header fields to encode data.
- Understand the difference between extracting data and merely detecting anomalous traffic patterns using sliding windows.

---

## 🛠️ The Concept: IP TTL Encoding

The **Time to Live (TTL)** is an 8-bit numeric field in the IPv4 header. Its legitimate purpose is to act as a lifecycle counter that decreases by `1` every time a packet passes through a network router. Once the TTL reaches `0`, the packet is intentionally dropped, preventing infinite network loops. 

Because it is an 8-bit field, the TTL can hold values from `0` to `255`... which perfectly aligns with the length required to hold a standard ASCII text string character!

### Our Covert Protocol
Instead of carrying data in the payload, our covert sender takes a single letter of our hidden message, evaluates its numerical value, and writes it directly over the IP TTL field.

- **Legitimate Character Range:** Standard readable ASCII characters fall roughly between `32` ('Space') and `126` ('~').
- **The Signal:** Packets containing a TTL falling between `32` and `126` are parsed by the receiver and decoded back into text.
- **The Noise:** Packets containing a randomly generated TTL between `130` and `255` (outside typical readable ASCII ranges) are sent as decoy traffic.
- **The Delimeter:** The receiver is programmed to stop listening when it witnesses the ASCII value for `!` (Exclamation mark).

To blend in, our sender only converts about ~20% of its generated packets into the covert signal, while the rest acts as randomized high-TTL noise.

---

## 🚀 Lab Walkthrough

### 📋 Prerequisites
- Python 3.x
- `scapy` library (`pip install scapy`)
- Root/Administrator privileges (required for raw packet sniffing)

### 💻 Step 1: Start the Receiver
The receiver script sniffs network traffic on the loopback (`lo`) interface and examines the TTL of incoming TCP packets on port 5000. If the TTL value falls into the specific ASCII range (32-126), it converts the integer back to a text character.

Open a terminal and run:
```bash
sudo python receiver.py
```
*The script will block and stand by.*

### 💻 Step 2: Run the Sender
Open a second terminal and run our sender script. It will begin injecting high-TTL noise packets mixed intermittently with our covert TTL-encoded message.
```bash
sudo python sender.py
```

### 🎉 Step 3: Observe the Extraction
Return to your receiver terminal. You should see it cleanly strip away the noise packets and reconstruct the message from the 32-126 TTL ranges:
```text
Reach at the decided location. Tony!
[+] Message complete: Reach at the decided location. Tony!
```

---

## 🛡️ Defending It: Running the Detector

This level includes a brand new element: **A Defender's perspective**.

Even without knowing the exact secret protocol or the target message, a defender can easily unmask this covert channel by looking for statistical anomalies. 

Real-world operating systems usually stick to predictable default TTL values (e.g., Linux uses 64, Windows typically uses 128, routers use 255). Seeing a stream of packets originating from the same machine with wildly fluctuating TTL values like `114`, `101`, `97` (r, e, a) is an incredibly bizarre networking event.

The `detector.py` script acts as an Intrusion Detection System (IDS). It uses a "sliding window" to evaluate the last 20 network packets. If more than 50% of the recent TTL values appear to be in the ASCII range, it throws a warning.

**Try it out:**
1. Start the detector: `sudo python detector.py`
2. Run the sender (in a separate terminal): `sudo python sender.py`
3. Watch the detector terminal alert on the anomalous statistical distribution:
   `[!] Suspicious pattern detected: 12/20 TTL values look like ASCII → possible covert channel`

---

## ⚠️ Limitations of this Method

- **Physical Network Interference:** Over a real network spanning across the internet, the TTL field naturally decreases by `1` at each router hop! Your receiver would receive the ASCII values "shifted" down by however many hops the packet took. You would have to know the exact hop-count to accurately reverse the math.
- **Trivial Detection:** As demonstrated by our detector script, bouncing TTL values are not natural. It's an easy signature for almost any default firewall rule to flag.

---

## 🧠 Key Takeaway
> **When encoding data inside existing numeric protocol fields, you have to account for both statistical variations (which firewalls will flag) and physical characteristics of your network path (like routers naturally altering those numbers).**
