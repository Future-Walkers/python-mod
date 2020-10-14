# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_time_util.py
# Time       ：2020/8/12 16:32
# Author     ：Rodney Cheung
"""
import unittest

from wisbec.date.time import TimeUtil


class TestTimeUtil(unittest.TestCase):
    def test_format_seconds(self):
        print(TimeUtil.format_seconds(100, '{:d}h{:d}m{:d}s'))

    def test_get_current_timestamp(self):
        print(TimeUtil.get_current_timestamp())

    def test_now(self):
        print(TimeUtil.now('%Y-%m-%d_%H-%M-%S'))


if __name__ == '__main__':
    unittest.main()
