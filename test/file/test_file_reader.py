# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_file_reader.py
# Time       ：2020/8/19 15:53
# Author     ：Rodney Cheung
"""
import unittest

from wisbec.file import file_reader


class TestFile(unittest.TestCase):
    def test_get_file_md5(self):
        print(file_reader.get_file_md5('/home/rodneycheung/.mitmproxy/mitmproxy-ca-cert.pem'))
        print(file_reader.get_file_md5('/home/rodneycheung/workspace/Tweezer/tweezer/src/c8750f0d.0'))


if __name__ == '__main__':
    unittest.main()
