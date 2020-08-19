#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 8/18/20 2:01 PM
@Author  : Rodney Cheung
@File    : test_log.py
@Software: PyCharm
"""

import logging
import os
import unittest

from wisbec.logging.log import Log


class TestLog(unittest.TestCase):
    def setUp(self):
        Log.init_logger(os.path.join(os.getcwd(), 'log'))
        self.assertEqual(Log.is_log_to_file, True)
        self.assertEqual(Log.is_log_to_console, True)

    def tearDown(self):
        Log.close()
        self.assertEqual(len(Log.file_loggers), 0)

    def test_debug(self):
        log_content = 'test_debug{}{}'
        try:
            raise RuntimeWarning('runtime warning')
        except RuntimeWarning as e:
            Log.debug('catch exception: ', e)
        Log.debug(log_content, ' another', ' test_debug')

    def test_warning(self):
        log_content = 'test_warning{}{}'
        Log.warning(log_content, ' another', ' test_warning')

    def test_error(self):
        log_content = 'test_error{}{}'
        Log.error(log_content, ' another', ' test_error')

    def test_info(self):
        log_content = 'test_info{}{}'
        Log.info(log_content, ' another', ' test_info')

    def test_critical(self):
        placeholder = 'placeholder'
        Log.critical('{} test', placeholder)
        log_content = 'test_critical {} {}'
        another = 'another'
        test_critical = 'test_critical'
        Log.critical(log_content, another, test_critical)

    def test_set_console_log_level(self):
        Log.set_console_log_level(logging.ERROR)
        Log.warning('test_set_console_log_level')


if __name__ == '__main__':
    unittest.main()
