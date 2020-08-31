# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_url.py
# Time       ：2020/8/31 14:22
# Author     ：Rodney Cheung
"""
import unittest
from wisbec.network import url


class TestUrl(unittest.TestCase):
    def test_get_domain_from_url(self):
        print(url.get_domain_from_url('https://docs.python.org/3/library/json.html'))


if __name__ == '__main__':
    unittest.main()
