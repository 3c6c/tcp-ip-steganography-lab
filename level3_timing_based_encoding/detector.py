# Author: Ayush Kunwar

from scapy.all import *

last_packet_time = None
delays = []

WINDOW_SIZE = 30

def analyse(pkt):
    global last_packet_time, delays

    current_time = pkt.time

    if last_packet_time is None:
        last_packet_time = current_time
        return

    delay = current_time - last_packet_time
    last_packet_time = current_time

    if delay < 0.1:
        return

    delays.append(delay)

    if len(delays) > WINDOW_SIZE:
        delays.pop(0)

    if len(delays) < WINDOW_SIZE:
        return

    short_delays = [d for d in delays if 0.2 <= d <= 0.38]
    long_delays  = [d for d in delays if 0.42 <= d <= 0.7]

    total = len(delays)

    short_ratio = len(short_delays) / total
    long_ratio  = len(long_delays) / total

    if short_ratio > 0.2 and long_ratio > 0.2:
        print("\n[!] Suspicious timing pattern detected!")
        print(f"Short delays: {len(short_delays)} | Long delays: {len(long_delays)}")
        print(f"Ratios → short: {short_ratio:.2f}, long: {long_ratio:.2f}")

sniff(iface="lo", prn=analyse, filter="tcp and port 5000", store=0)