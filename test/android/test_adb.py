# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_adb.py
# Time       ：2020/8/24 18:27
# Author     ：Rodney Cheung
"""
import unittest
from wisbec.android.adb import Adb


class TestAdb(unittest.TestCase):
    def setUp(self) -> None:
        if len(Adb.devices(True)) == 0:
            Adb.init('/Users/jsrdzhk/workspace/Tweezer/tweezer/'
                     'tweezer/resource/installation_pkg/adb_tool/platform-tools/adb')

    def test_adb_devices(self):
        print(Adb.exec('version'))
        print(Adb.devices(True))

    def test_su_shell(self):
        print(Adb.su_shell(Adb.devices(True)[0], 'id'))

    def test_top_app(self):
        print(Adb.top_app(Adb.devices(True)[0]))

    def test_get_sdk_level(self):
        print(Adb.get_sdk_level(Adb.devices(True)[0]))


if __name__ == '__main__':
    unittest.main()
