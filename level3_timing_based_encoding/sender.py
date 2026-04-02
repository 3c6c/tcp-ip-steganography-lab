# Author: Ayush Kunwar

import random, time
from scapy.all import *

flag = "Flag!"

def send_packet():
    send(
        IP(
            src="127.0.0.1",
            dst="127.0.0.1",
        )/
        TCP(
            sport=5000, dport=5000
        )
    )
def send_preamble_packet():
    byte = "11111111"
    for bit in byte:
        print("Bit: ", bit)
        send_packet()
        print("Sent the packet")
        print("Sleeping for 500 milliseconds")
        time.sleep(0.5)
        print("Slept for 500 milliseconds")
def gen_random_number():
    return random.randint(0,500)

for i in range(10):
    send_packet() # To add noise
    time.sleep(0.1)
    print(f"Adding 100 noise, current: {i}")

send_preamble_packet()
for char in flag:
    current_value = char
    ascii_value = ord(current_value)
    byte = format(ascii_value, '08b')
    print(f"Generated ascii value for: {current_value} as: {ascii_value} and binary value: {byte}")
    for bit in byte:
        print("Bit: ", bit)
        # Check if the current bit is 0
        print("Checking if bit is 0 or 1")
        if int(bit) == 0:
            send_packet()
            print("Sleeping for 300 milliseconds")
            time.sleep(0.3)
            print("Slept for 300 milliseconds")
            print("Sent the packet")
        # Check if the current bit is 1
        elif int(bit) == 1:
            send_packet()
            print("Sleeping for 500 milliseconds")
            time.sleep(0.6)
            print("Slept for 500 milliseconds")
            print("Sent the packet")

for i in range(50):
    send_packet() # To add noise
    time.sleep(0.1)
    print(f"Adding 50 noise, current: {i}")
