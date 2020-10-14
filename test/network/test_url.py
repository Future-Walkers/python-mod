# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_url.py
# Time       ：2020/8/31 14:22
# Author     ：Rodney Cheung
"""
import unittest
from wisbec.network.url import UrlUtil


class TestUrl(unittest.TestCase):
    test_url = 'https://docs.python.org/3/library/json.html'

    def test_get_ip_from_url(self):
        ip = UrlUtil.get_ip_from_url(self.test_url)
        print(ip)

    def test_get_domain_from_url(self):
        domain = UrlUtil.get_domain_from_url(self.test_url)
        self.assertEqual(domain, 'docs.python.org')

    def test_is_url_accessible(self):
        is_accessible = UrlUtil.is_url_accessible(self.test_url, UrlUtil.USER_AGENT['Android'])
        self.assertEqual(is_accessible, True)


if __name__ == '__main__':
    unittest.main()
