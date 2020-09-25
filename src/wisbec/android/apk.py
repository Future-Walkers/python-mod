# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : apk.py
# Time       ：2020/9/18 15:21
# Author     ：Rodney Cheung
"""
import re

from wisbec.android.aapt import Aapt


class Apk:
    @classmethod
    def init(cls, aapt_path: str):
        Aapt.init(aapt_path)

    @classmethod
    def get_pkg_name(cls, apk_path: str) -> str:
        code, out, err = Aapt.dump_label(apk_path)
        if code != 0:
            return ''
        package_name_pattern: re.Pattern = re.compile(r'package: name=\'\S+\'')
        matched: re.Match = package_name_pattern.search(out)
        if matched is None:
            return ''
        return out[matched.span()[0] + 15: matched.span()[1] - 1]
