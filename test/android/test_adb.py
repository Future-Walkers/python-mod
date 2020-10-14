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
    @classmethod
    def setUpClass(cls) -> None:
        cls.device_id = Adb.devices(True)[0]

    def test_adb_devices(self):
        print(Adb.exec('version'))
        print(Adb.devices(True))

    def test_su_shell(self):
        print(Adb.su_shell(self.device_id, 'id'))

    def test_top_app(self):
        print(Adb.top_app(self.device_id, Adb.get_sdk_level(self.device_id)))

    def test_get_sdk_level(self):
        print(Adb.get_sdk_level(self.device_id))

    def test_get_system_packages(self):
        print(Adb.get_system_packages(self.device_id))


if __name__ == '__main__':
    unittest.main()
