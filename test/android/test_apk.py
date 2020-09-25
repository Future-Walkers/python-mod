# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_apk.py
# Time       ：2020/9/25 09:43
# Author     ：Rodney Cheung
"""
import unittest

from wisbec.android.apk import Apk


class TestApk(unittest.TestCase):
    def test_get_pkg_name(self):
        print(Apk.get_pkg_name('/Users/jsrdzhk/statistics/apks/chubao/0B42C264920227D93C57470FF5D9148C.apk'))


if __name__ == '__main__':
    unittest.main()
