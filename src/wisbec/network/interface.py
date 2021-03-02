# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : interface.py
# Time       ：2020/8/24 08:48
# Author     ：Rodney Cheung
"""
import re
from typing import List

from wisbec import system
from wisbec.console import shell
from wisbec.parser.parse import Parser, InterfaceInfo


class Interface:
    @classmethod
    def __get_interface_from_ifconfig(cls) -> List[InterfaceInfo]:
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
        # iface_info_list: List[InterfaceInfo] = list()
        code, out, err = shell.exec_cmd('ifconfig')
        return Parser.parse_ifconfig(out)
        # out = out.replace('\n\n', '\n')
        # list_blocks = re.split('\n[a-zA-Z0-9]', out)
        # for block in list_blocks:
        #     if ('inet ' not in block) or ('loop ' in block):
        #         continue
        #     iface_name = re.search(r'(\S+):', block).groups()[0]
        #     iface_ip = re.search(r'inet (\S+) ', block).groups()[0].replace('addr:', '')
        #     if iface_ip == '127.0.0.1':
        #         continue
        #     iface_info_list.append(InterfaceInfo(iface_name, iface_ip))
        # return iface_info_list

    @classmethod
    def __get_interface_from_ipconfig(cls) -> List[InterfaceInfo]:
        """
        Windows IP Configuration

        Ethernet adapter 以太网:

           Media State . . . . . . . . . . . : Media disconnected
           Connection-specific DNS Suffix  . :

        Wireless LAN adapter 本地连接* 2:

           Media State . . . . . . . . . . . : Media disconnected
           Connection-specific DNS Suffix  . :

        Wireless LAN adapter WLAN:

           Connection-specific DNS Suffix  . :
           IPv4 Address. . . . . . . . . . . : 10.251.0.49
           Subnet Mask . . . . . . . . . . . : 255.255.254.0
           Default Gateway . . . . . . . . . : 10.251.0.1

        Ethernet adapter 蓝牙网络连接:

           Media State . . . . . . . . . . . : Media disconnected
           Connection-specific DNS Suffix  . :
        """
        iface_info_list: List[InterfaceInfo] = list()
        code, out, err = shell.exec_cmd(['cmd.exe', '/c', 'chcp 65001 & ipconfig'])
        if code != 0:
            return iface_info_list
        out = re.sub(r'(\r\n){2,}', r'\r\n', out)
        list_blocks = re.split(r'\r\n[a-zA-Z0-9]', out)
        for block in list_blocks:
            if 'IPv4 Address' not in block:
                continue
            iface_name_group_span = re.search(r'(\S+):', block).span()
            iface_name = block[iface_name_group_span[0]:iface_name_group_span[1]].replace(':', '')
            search_res = re.search(r'IPv4 Address(. )+: \S+', block)
            if search_res is None:
                continue
            search_res_span = search_res.span()
            ip_addr = block[search_res_span[0]:search_res_span[1]]
            ip_addr = ip_addr.split(': ')[-1]
            if ip_addr == '127.0.0.1':
                continue
            iface_info_list.append(InterfaceInfo(iface_name, ip_addr))
        return iface_info_list

    @classmethod
    def get_active_interfaces(cls) -> List[InterfaceInfo]:
        """
        get active net interface,support mac os,linux an windows
        Returns:
            [(iface_name1,iface_ip1),...]
        """
        if system.is_windows():
            return cls.__get_interface_from_ipconfig()
        elif system.is_mac_os() or system.is_linux():
            return cls.__get_interface_from_ifconfig()
        else:
            return []
