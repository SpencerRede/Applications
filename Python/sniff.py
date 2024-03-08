import sys
import json
import socket

from scapy.all import *

output_file = "network_Activity"
_iface = "en0"
network_activity = {}

def getDomain(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return "No domain name found"

def packet(t):
    keySrc = str(t[IP].src)
    keyDst = str(t[IP].dst)

    if keySrc not in network_activity:
        print('new IP detected: ' + keySrc)
        network_activity[keySrc] = {
            "pktsSent" : 1,
            "destIPAddrs" : [keyDst],
            "destDomains" : []
        }
    else:
        if network_activity[keySrc]["destIPAddrs"] is not None and keyDst not in network_activity[keySrc]["destIPAddrs"]:
            print('new Connection detected: ' + keySrc + ' -> ' + keyDst)
            network_activity[keySrc]["destIPAddrs"].append(keyDst)
        network_activity[keySrc]["pktsSent"] = network_activity[keySrc]["pktsSent"] + 1

print("Welcome to my pkt sniffer, at anytime use the Cmd+C interrupt to close\n")
t_ = sniff(iface=_iface, lfilter = lambda s: s.haslayer(IP), prn=packet)

# sort the dict and determine the domainName of the desintation Ip address
sorted_keys = sorted(network_activity, key=lambda x:network_activity[x]['pktsSent'], reverse=True)
sorted_network_Activity = {}
for key in sorted_keys:
    sorted_network_Activity[key] = network_activity[key]
    for destIP in sorted_network_Activity[key]['destIPAddrs']:
        sorted_network_Activity[key]['destDomains'].append(getDomain(destIP))

# Save the sorted dict to a .json file
with open( output_file + '.json', 'w') as fp:
    json.dump(sorted_network_Activity, fp)
fp.close()

print('\nSniff finished, data saved to ' + output_file)
