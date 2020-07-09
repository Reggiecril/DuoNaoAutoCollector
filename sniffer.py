# coding=utf-8
#
import scapy.all as scapy
from scapy.layers.http import HTTPRequest, HTTPResponse, HTTP
import json

dpkt  = scapy.sniff(iface = "en0", count = 10)
scapy.wrpcap("demo.pcap", dpkt)

packets = scapy.rdpcap('demo.pcap')
print(packets)
# s=scapy.sniff(offline='demo.pcap', prn=fengxi)
# print(s)
# packets = scapy.rdpcap('demo.pcap')
# for p in dpkt:
#     print ('=' * 78)
#     p.show()