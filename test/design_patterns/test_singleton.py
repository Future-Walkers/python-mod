# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Author: Sphantix Hang
Date: 2020-10-08 11:28:39
LastEditors: Sphantix Hang
LastEditTime: 2020-10-08 12:03:29
FilePath: /python-mod/test/design_patterns/test_singleton.py
"""

from wisbec.design_patterns.singleton import SingletonType
import unittest


class Foo(metaclass=SingletonType):
    def __init__(self, name):
        self.name = name


class TestSingletonType(unittest.TestCase):
    def test_singletontype(self):
        obj1 = Foo('name')
        obj2 = Foo('name')
        self.assertEqual(obj1, obj2)
