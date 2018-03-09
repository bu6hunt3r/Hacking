#!/usr/bin(env python
#-*- coding: utf-8 -*-
from __future__ import print_function
from scapy.all import *
from argparse import ArgumentParser
import logging
import os

IP_FORWARD='/proc/net/ipv4/ip_forward'

TIMEOUT=2
RETRY=1

def set_configs():
    parser=ArgumentParser()

    parser.add_argument("-t",
                        "--victim",
                        required=True,
                        type=str,
                        help='The victim\'s ip address')
    
    parser.add_argument("-g",
                        "--gateway",
                        required=True,
                        type=str,
                        help='The gateway\'s ip address')

    parser.add_argument("-i",
                        "--interface",
                        required=True,
                        type=str,
                        help='Use this interface')

    args=parser.parse_args()

    return {
        'victim':       { 
            'ip':   args.victim,
            'mac':  ip_to_mac(args.victim),
        },

        'gateway':      { 
            'ip':   args.gateway,
            'mac':  ip_to_mac(args.gateway),
        },

        'iface':    args.interface
    }

def ip_to_mac(ip, retry=RETRY, timeout=TIMEOUT):
    
    #print("Investigating MAC...")
    
    arp=ARP()

    # op mode 1 => query  
    arp.op=1 
    
    # broadcast
    arp.hwdst="ff:ff:ff:ff:ff:ff"

    arp.pdst=ip

    response, unanswered = sr(arp, retry=retry, timeout=timeout, verbose=0)

    for s, r in response:
        return r[ARP].underlayer.src

    return None

def enable_packet_forwarding():
    with open(IP_FORWARD,'w') as f:
        f.write('1')

def disable_packet_forwarding():
    with open(IP_FORWARD,'w') as f:
        f.write('0')

def poison_victim(configs):
    victim_mac=configs['victim']['mac']
    logging.info("[*] victim MAC: %s".format(victim_mac))

def main():
    logging.basicConfig(level=logging.INFO)
    logger=logging.getLogger()
    logger.handlers=[]

    handler=logging.StreamHandler()
    handler.setLevel(level=logging.INFO)
    formatter=logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    config=set_configs()

    logger.info("[*] Using interface %s" % set_configs()['iface'])
    logger.info("[*] Target \033[1;31m(%s)\033[0m MAC is \033[1;32m%s\033[0m" % (set_configs()['victim']['ip'], set_configs()['victim']['mac']))


if __name__ == '__main__':
    main()