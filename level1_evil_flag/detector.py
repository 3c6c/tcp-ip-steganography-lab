# Author: Ayush Kunwar

from scapy.all import *

def analyse_packet(pkt):
    if pkt.haslayer(IP):
        # Evil bit = 0x4
        if pkt[IP].flags == 0x4:
            print("\n[!] Suspicious packet detected (Evil Bit Set)")
            print(f"Source: {pkt[IP].src} → Destination: {pkt[IP].dst}")

            if pkt.haslayer(Raw):
                try:
                    data = pkt[Raw].load.decode(errors="ignore")
                    print(f"Payload: {data}")
                except:
                    print("Payload: <non-decodable>")

sniff(iface="lo", prn=analyse_packet, filter="tcp", store=0)