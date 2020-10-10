#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Author: Sphantix Hang
Date: 2020-10-10 11:23:02
LastEditors: Sphantix Hang
LastEditTime: 2020-10-10 11:46:31
FilePath: /python-mod/src/wisbec/decorator/__init__.py
'''

from functools import wraps
from time import time


def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        print('Elapsed time: {} sec'.format(end-start))
        return result
    return wrapper