#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
# File       : url.py
# Time       ：2020/8/19 15:15
# Author     ：Rodney Cheung
"""
import random
import socket
import urllib.request
from urllib.parse import urlparse

USER_AGENT = {
    "Android": [
        "Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0; MotoG3 Build/MPIS24.65-33.1-2-16) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/67.0.3396.87 Mobile Safari/537.36 "
    ],
    "iOS": [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "CriOS/78.0.3904.84 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    ],
}


def get_ip_from_url(url):
    netloc = urlparse(url).netloc
    domain = netloc.split(":")[0]
    addr = socket.getaddrinfo(domain, 'http')
    return addr[0][4][0]


def get_domain_from_url(url: str) -> str:
    netloc = urlparse(url).netloc
    domain = netloc.split(":")[0]
    return domain


def check_url_access(url: str, user_agent: tuple) -> bool:
    """
    check if url accessible
    Args:
        url: target url
        user_agent: user agent,use USER_AGENT['Android'] or USER_AGENT['iOS']

    Returns:
        url accessible
    """
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent',
                          user_agent[random.randint(
                              0,
                              len(user_agent) - 1)])]
    try:
        opener.open(url)
        return True
    except Exception as e:
        print("Current URL[{0}] connect failed!".format(url), e)
        return False
