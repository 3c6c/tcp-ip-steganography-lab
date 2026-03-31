# Author: Ayush Kunwar
from scapy.all import *

sentence = ""
last_char = None

def has_pkt(pkt):
    global sentence, last_char

    if pkt.haslayer(IP) and pkt.haslayer(TCP):
        if pkt[TCP].flags == 0x02:
            if pkt[IP].flags == 0x4:
                if pkt.haslayer(Raw):
                    char = pkt[Raw].load.decode()

                    # skip duplicate (loopback)
                    if char == last_char:
                        return

                    last_char = char
                    sentence += char
                    print(char, end="", flush=True)

sniff(iface="lo", prn=has_pkt, filter="tcp and port 5000", store=0)