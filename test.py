#!/usr/bin/python
from scapy.all import *


def http_header(packet):
    http_packet = str(packet)
    if http_packet.find('GET'):
        print(GET_print(packet))
    print(packet)


def GET_print(packet1):
    ret = "***************************************GET PACKET****************************************************\n"
    ret += "\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    ret += "*****************************************************************************************************\n"
    return ret


sniff(iface='ens33', prn=http_header)
