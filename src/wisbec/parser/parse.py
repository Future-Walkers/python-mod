# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : parse.py
# Time       ：2/2/21 09:20
# Author     ：Rodney Cheung
"""
import re
from typing import List


class InterfaceInfo:
    def __init__(self, iface_name, ip_addr):
        self.m_ip_addr: str = ip_addr
        self.m_iface_name: str = iface_name

class Parser:
    @classmethod
    def parse_ifconfig(cls, ifconfig_output: str) -> List[InterfaceInfo]:
        """
                enx000ec6c0c623: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
                        ether 00:0e:c0:c0:56:23  txqueuelen 1000  (Ethernet)
                        RX packets 0  bytes 0 (0.0 B)
                        RX errors 0  dropped 0  overruns 0  frame 0
                        TX packets 0  bytes 0 (0.0 B)
                        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
                lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
                        inet 127.0.0.1  netmask 255.0.0.0
                        inet6 ::1  prefixlen 128  scopeid 0x10<host>
                        loop  txqueuelen 1000  (Local Loopback)
                        RX packets 1134271  bytes 1046040386 (1.0 GB)
                        RX errors 0  dropped 0  overruns 0  frame 0
                        TX packets 1134271  bytes 1046040386 (1.0 GB)
                        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
                """
        iface_info_list: List[InterfaceInfo] = list()
        # code, out, err = shell.exec_cmd('ifconfig')
        out = ifconfig_output.replace('\n\n', '\n')
        list_blocks = re.split('\n[a-zA-Z0-9]', out)
        for block in list_blocks:
            if ('inet ' not in block) or ('loop ' in block):
                continue
            iface_name = re.search(r'(\S+):', block).groups()[0]
            iface_ip = re.search(r'inet (\S+) ', block).groups()[0].replace('addr:', '')
            if iface_ip == '127.0.0.1':
                continue
            iface_info_list.append(InterfaceInfo(iface_name, iface_ip))
        return iface_info_list
