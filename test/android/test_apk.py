# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_apk.py
# Time       ：2020/9/25 09:43
# Author     ：Rodney Cheung
"""
import os
import unittest

from test.testdata.test_util import TestUtil
from wisbec.android.apk import Apk


class TestApk(unittest.TestCase):
    @staticmethod
    def __get_test_data_path():
        return os.path.join(TestUtil.get_test_data_path(), 'android', 'aapt')

    def test_get_pkg_name(self):
        pkg_name = Apk.get_pkg_name(os.path.join(self.__get_test_data_path(), 'test.apk'))
        self.assertEqual(pkg_name, 'com.cootek.smartinputv5.skin.keyboard_theme_colorful_thunder_neon_lights')


if __name__ == '__main__':
    unittest.main()
