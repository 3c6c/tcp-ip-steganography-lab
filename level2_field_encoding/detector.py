# Author: Ayush Kunwar
from scapy.all import *

min_ascii = 32
max_ascii = 126

window = []
window_size = 20

def analyse_packet(pkt):
    if not (pkt.haslayer(IP) and pkt.haslayer(TCP)):
        return

    if pkt[TCP].flags != 0x02:
        return

    ttl = pkt[IP].ttl

    window.append(ttl)

    if len(window) > window_size:
        window.pop(0)

    ascii_like = [t for t in window if min_ascii <= t <= max_ascii]

    if len(ascii_like) > (window_size * 0.5):
        print(
            f"[!] Suspicious pattern detected: "
            f"{len(ascii_like)}/{window_size} TTL values look like ASCII → possible covert channel"
        )


sniff(
    iface="lo",
    prn=analyse_packet,
    filter="tcp and port 5000",
    store=0
)