# Author: Ayush Kunwar
from scapy.all import *
import random

hidden_flag = "Welcome to the flag section here is your flag: flag{found_me}"

print(len(hidden_flag))
counter = 0
for i in range(500):
    rand_num = random.randint(0,500)
    if rand_num < 200:
        
        if counter == len(hidden_flag):
            continue
        elif counter < len(hidden_flag):
            send(
                IP(
                    src="127.0.0.1",
                    dst="127.0.0.1",
                    flags="evil"
                )/
                TCP(
                    sport=5000, dport=5000
                )/ Raw(hidden_flag[counter])
            )
            counter += 1
        else:
            IndexError()
    elif not rand_num / 2:
        send(
            IP(
                src="127.0.0.1",
                dst="127.0.0.1",
            )/
            TCP(
                sport=5000, dport=5000
            )
        )
    else:
        continue
