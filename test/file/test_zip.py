# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_zip.py
# Time       ：2020/8/19 15:54
# Author     ：Rodney Cheung
"""
import os
import unittest

from wisbec.file import zip


class TestZip(unittest.TestCase):
    def test_create_zip_file(self):
        zip.zip_file(os.path.join(self.test_data_dir, 'test.zip'),
                     os.path.join(os.path.pardir, 'wisbec'))


if __name__ == '__main__':
    unittest.main()
