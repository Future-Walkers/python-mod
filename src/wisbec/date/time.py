#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
@Time    : 8/18/20 2:05 PM
@Author  : Rodney Cheung
@File    : time.py
@Software: PyCharm
"""

import time


def format_seconds(seconds, time_format):
    """
    convert seconds to specified format
    Args:
        seconds: seconds
        time_format: specified time format,hour minute & second
        can be used

    Returns:
        formatted time str
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return str(time_format).format(h, m, s)


def get_current_timestamp():
    """
    get current timestamp
    Returns:
        current timestamp
    """
    return time.time()


def now(time_format: str) -> str:
    return time.strftime(time_format, time.localtime())
