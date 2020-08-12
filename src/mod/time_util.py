#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Author: Rodney Cheung
@Date: 2020-06-29 10:31:03
@LastEditors: Rodney Cheung
@LastEditTime: 2020-06-29 10:41:21
@FilePath: /python-mod/core/time_util.py
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
