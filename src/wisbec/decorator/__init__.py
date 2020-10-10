#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Author: Sphantix Hang
Date: 2020-10-10 11:23:02
LastEditors: Sphantix Hang
LastEditTime: 2020-10-10 11:24:42
FilePath: /python-mod/src/wisbec/decorator/__init__.py
'''

import time

def timer(func):
    def inner():
        start_time = time.time()
        res = func()
        end_time = time.time()
        print("函数的运行时间：{}".format(end_time - start_time))
        return  res
    return inner