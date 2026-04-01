# Author Ayush Kunwar

from scapy.all import *
from datetime import datetime

last_packet_time = None
byte = ""
preamble_buffer = ""
preamble_detected = False
decoded_message = ""

def do_something(pkt):
    global last_packet_time, byte, preamble_buffer, preamble_detected, decoded_message

    readable_time = datetime.fromtimestamp(float(pkt.time)).strftime('%Y-%m-%d %H:%M:%S.%f')
    current_packet_timestamp = pkt.time

    if last_packet_time is not None:
        delay = pkt.time - last_packet_time

        if delay < 0.2:
            last_packet_time = current_packet_timestamp
            return

        if delay < 0.4:
            bit = "0"
        else:
            bit = "1"

        if not preamble_detected:
            preamble_buffer += bit

            if len(preamble_buffer) > 8:
                preamble_buffer = preamble_buffer[-8:]

            if preamble_buffer == "11111111":
                print("\n[+] Preamble detected. Starting decoding...\n")
                preamble_detected = True
                byte = ""
            last_packet_time = current_packet_timestamp
            return

        byte += bit

        if len(byte) == 8:
            ascii_value = int(byte, 2)
            char = chr(ascii_value)

            decoded_message += char
            print(char, end="", flush=True)

            byte = ""

            if decoded_message and decoded_message[-1] == "!":
                print("\n[+] Message completed. Final message:", decoded_message)
                exit(0)

    else:
        print(f"Time: {readable_time} | First packet captured. Please wait ...")

    last_packet_time = current_packet_timestamp


sniff(iface="lo", prn=do_something, filter="tcp and port 5000", store=0)