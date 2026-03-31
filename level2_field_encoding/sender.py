# Author: Ayush Kunwar
from scapy.all import *
import random

hidden_flag = "Reach at the decided location. Tony!"

print(len(hidden_flag))
current_flag_index = 0
counter = 0
while True:
    if current_flag_index == len(hidden_flag):
        if counter >= 50:
            break
        else:
            counter+=1
    rand_num = random.randint(0,500)
    if 100 <= rand_num <= 200:
        
        if current_flag_index == len(hidden_flag):
            continue
        elif current_flag_index < len(hidden_flag):
            send(
                IP(
                    src="127.0.0.1",
                    dst="127.0.0.1",
                    ttl=ord(hidden_flag[current_flag_index])
                )/
                TCP(
                    sport=5000, dport=5000
                )
            )
            current_flag_index += 1
    else:
        send(
            IP(
                src="127.0.0.1",
                dst="127.0.0.1",
                ttl=random.randint(130,255)
            )/
            TCP(
                sport=5000, dport=5000
            )
        )