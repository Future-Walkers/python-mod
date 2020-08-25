# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_shell.py
# Time       ：2020/8/24 17:35
# Author     ：Rodney Cheung
"""
import unittest
from wisbec.console import shell


class TestShell(unittest.TestCase):
    def test_get_current_shell(self):
        print(shell.get_current_shell())


if __name__ == '__main__':
    unittest.main()
