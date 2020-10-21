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

    def test_shell(self):
        print(Adb.shell(self.device_id, 'am', 'startservice', '-n' 'org.proxydroid/.ProxyDroidService', '--es',
                        'proxyType', 'http', '--es', 'host', '10.251.0.219', '--ei', 'port', '6666', '--ez',
                        'tweezer.isTweezer', 'true', '--es', 'tweezer.proxyApp', 'com.ttyouqu.app'))

    def test_top_app(self):
        print(Adb.top_app(self.device_id, Adb.get_sdk_level(self.device_id)))

    def test_get_sdk_level(self):
        print(Adb.get_sdk_level(self.device_id))

    def test_get_system_packages(self):
        print(Adb.get_system_packages(self.device_id))

    def test_is_rooted(self):
        print(Adb.is_rooted(self.device_id))

    def test_is_system_partition_rw(self):
        print(Adb.is_system_partition_rw(self.device_id))


if __name__ == '__main__':
    unittest.main()
