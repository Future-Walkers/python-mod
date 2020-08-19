#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 8/18/20 2:05 PM
@Author  : Rodney Cheung
@File    : file_reader.py
@Software: PyCharm
"""
import hashlib
import os
import typing


def get_file_md5(file_full_path):
    if not os.path.isfile(file_full_path):
        return
    md5hash = hashlib.md5()
    with open(file_full_path, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            md5hash.update(b)

    return md5hash.hexdigest()


def read_file(path, bytes_num=-1) -> typing.AnyStr:
    with open(path, 'rb') as f:
        return f.read(bytes_num)


def last_line(file_path):
    with open(file_path) as fp:
        lines = fp.readlines()
        if len(lines) == 0:
            return ""
        return lines[-1].strip()
