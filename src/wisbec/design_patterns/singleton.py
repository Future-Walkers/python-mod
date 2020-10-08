#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Author: Sphantix Hang
Date: 2020-10-08 09:21:48
LastEditors: Sphantix Hang
LastEditTime: 2020-10-08 11:56:54
'''

import threading


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(
                        SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance
