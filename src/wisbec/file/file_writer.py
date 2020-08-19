# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : file_writer.py
# Time       ：2020/8/19 16:05
# Author     ：Rodney Cheung
"""


def write_file(path, mode, data):
    with open(path, mode) as f:
        f.write(data)
