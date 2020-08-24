# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : interface.py
# Time       ：2020/8/24 08:48
# Author     ：Rodney Cheung
"""
import re
import sys

from wisbec.console import shell


class Interface:
    @classmethod
    def __get_interface_from_ifconfig(cls) -> list:
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
        list_interface = []
        code, out, err = shell.exec_cmd('ifconfig')
        out = out.replace('\n\n', '\n')
        list_blocks = re.split('\n[a-zA-Z0-9]', out)
        for block in list_blocks:
            if ('inet ' not in block) or ('loop ' in block):
                continue
            it_name = re.search(r'(\S+):', block).groups()[0]
            it_ip = re.search(r'inet (\S+) ', block).groups()[0].replace('addr:', '')
            list_interface.append((it_name, it_ip))
        return list_interface

    @classmethod
    def __get_interface_from_ipconfig(cls) -> list:
        interface_list = []
        code, out, err = shell.exec_cmd(['cmd.exe', '/c', 'ipconfig'])
        out = out.replace('\n{2,}', '\n')
        list_blocks = re.split('\n[a-zA-Z0-9]', out)
        for block in list_blocks:
            if 'IPv4 Address' not in block:
                continue
            iface_name_group = re.search(r'(\S+):', block).groups()
            iface_name = iface_name_group[0]
            iface_ip_group = re.search(r'IPv4 Address(. )+:', block).groups()
            iface_ip=iface_ip_group[0]
            interface_list.append((iface_name,iface_ip))
        return interface_list

    @classmethod
    def get_active_interfaces(cls) -> list:
        current_os = sys.platform
        if current_os == 'win32':
            return cls.__get_interface_from_ipconfig()
        elif current_os == 'darwin' or current_os == 'linux':
            return cls.__get_interface_from_ifconfig()
        else:
            return []
