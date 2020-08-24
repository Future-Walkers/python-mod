# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_interface.py
# Time       ：2020/8/24 09:03
# Author     ：Rodney Cheung
"""
import unittest
from wisbec.network.interface import Interface


class TestInterface(unittest.TestCase):
    def test_get_active_interfaces(self):
        print(Interface.get_active_interfaces())


if __name__ == '__main__':
    unittest.main()
