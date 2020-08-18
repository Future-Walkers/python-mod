#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 8/18/20 2:05 PM
@Author  : Rodney Cheung
@File    : file_util.py
@Software: PyCharm
"""


def last_line(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()
        if len(lines) == 0:
            return ""
        return lines[-1].strip()
