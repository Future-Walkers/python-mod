#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Author: Rodney Cheung
@Date: 2020-06-29 10:31:03
@LastEditors: Rodney Cheung
@LastEditTime: 2020-06-29 10:41:21
@FilePath: /python-mod/core/time_util.py
"""

import datetime
import time


def format_time_use(time):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return "Cost: %dh%02dm%02ds" % (h, m, s)
    elif m > 0:
        return "Cost: %02dm%02ds" % (m, s)
    else:
        return "Cost: %02ds" % s


def get_current_timestamp():
    return time.mktime(
        time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      "%Y-%m-%d %H:%M:%S"))
