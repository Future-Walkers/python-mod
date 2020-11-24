# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : resource.py
# Time       ：10/27/20 10:36
# Author     ：Rodney Cheung
"""
from os.path import join, dirname, abspath


class PackageResource:
    @classmethod
    def get_installation_pkg_path(cls):
        return join(dirname(abspath(__file__)), 'installation_pkg')

    @classmethod
    def get_android_tool_path(cls):
        return join(cls.get_installation_pkg_path(), 'android-tool.apk')
