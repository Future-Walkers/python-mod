# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : aapt.py
# Time       ：2020/9/18 15:29
# Author     ：Rodney Cheung
"""
from wisbec.console.shell import exec_cmd


class Aapt:
    c_aapt_path: str = ''

    @classmethod
    def init(cls, aapt_path: str):
        cls.c_aapt_path = aapt_path

    @classmethod
    def exec(cls, *args):
        if cls.c_aapt_path == '':
            cmd = ['aapt'] + list(args)
        else:
            cmd = [cls.c_aapt_path] + list(args)
        return exec_cmd(cmd)

    @classmethod
    def dump(cls, *args):
        return cls.exec('dump', *args)

    @classmethod
    def dump_label(cls, apk_path: str):
        return cls.dump('badging', apk_path)
