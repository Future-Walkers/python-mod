# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_console_shell.py
# Time       ：2020/8/20 17:37
# Author     ：Rodney Cheung
"""
import unittest
from wisbec.console import shell


class TestConsoleShell(unittest.TestCase):
    def test_exec_cmd(self):
        code, output, err = shell.exec_cmd(['which', 'mitmdump'])
        print(code)
        print(output)
        print(err)


if __name__ == '__main__':
    unittest.main()
