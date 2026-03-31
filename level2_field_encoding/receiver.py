# Author: Ayush Kunwar
from scapy.all import *

sentence = ""
last_char = None
delimeter = "!"
def has_pkt(pkt):
    global sentence, last_char

    if pkt.haslayer(IP) and pkt.haslayer(TCP):
        if pkt[TCP].flags == 0x02:
            if 32 <= pkt[IP].ttl <= 126:

                char = chr(pkt[IP].ttl)
                # skip duplicate (loopback)
                if char == last_char:
                    return

                last_char = char
                sentence += char
                print(char, end="", flush=True)
                if last_char == delimeter:
                    print("\n[+] Message complete:", sentence)
                    exit(0)

sniff(iface="lo", prn=has_pkt, filter="tcp and port 5000", store=0)