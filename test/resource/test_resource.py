# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_resource.py
# Time       ：10/27/20 10:39
# Author     ：Rodney Cheung
"""
import unittest

from wisbec.resource.resource import PackageResource


class TestResource(unittest.TestCase):
    def test_get_android_tool_path(self):
        print(PackageResource.get_android_tool_path())


if __name__ == '__main__':
    unittest.main()
