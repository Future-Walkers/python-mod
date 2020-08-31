# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_time_util.py
# Time       ：2020/8/12 16:32
# Author     ：Rodney Cheung
"""
import unittest
from wisbec.date import time


class TestTimeUtil(unittest.TestCase):
    def test_format_time_use(self):
        print(time.format_seconds(100, '{:d}h{:d}m{:d}s'))

    def test_get_current_timestamp(self):
        print(time.get_current_timestamp())


if __name__ == '__main__':
    unittest.main()
