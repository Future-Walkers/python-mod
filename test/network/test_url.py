#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Author: Sphantix Hang
date: 2020-11-30 11:04:01
last_author: Sphantix Hang
last_edit_time: 2020-11-30 11:37:37
FilePath: /python-mod/test/network/test_url.py
'''
import unittest
from wisbec.network.url import UrlUtil


class TestUrl(unittest.TestCase):
    test_url = 'https://docs.python.org/3/library/json.html'

    def test_get_ip_from_url(self):
        ip = UrlUtil.get_ip_from_url(self.test_url)
        print(ip)

    def test_get_domain_from_url(self):
        domain = UrlUtil.get_domain_from_url(self.test_url)
        self.assertEqual(domain, 'python.org')

    def test_is_url_accessible(self):
        is_accessible = UrlUtil.is_url_accessible(self.test_url, UrlUtil.USER_AGENT['Android'])
        self.assertEqual(is_accessible, True)


if __name__ == '__main__':
    unittest.main()
