#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Author: Rodney Cheung
@Date: 2020-06-29 10:37:23
@LastEditors: Rodney Cheung
@LastEditTime: 2020-06-29 11:00:20
@FilePath: /python-mod/core/network_util.py
"""
import socket
import random
import urllib.request
from urllib.parse import urlparse
from . import const

const.USER_AGENT = {
    "Android": [
        "Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0; MotoG3 Build/MPIS24.65-33.1-2-16) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"
    ],
    "iOS": [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/78.0.3904.84 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    ],
}


def get_ip_from_url(url):
    netloc = urlparse(url).netloc
    domain = netloc.split(":")[0]
    addr = socket.getaddrinfo(domain, 'http')
    return addr[0][4][0]


def check_url_access(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent',
                          const.USER_AGENT["Android"][random.randint(
                              0,
                              len(const.USER_AGENT["Android"]) - 1)])]
    try:
        opener.open(url)
        return True
    except Exception as e:
        print("Current URL[{0}] connect failed!".format(url), e)
        return False
