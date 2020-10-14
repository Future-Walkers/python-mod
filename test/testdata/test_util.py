# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_util.py
# Time       ：2020/10/13 17:00
# Author     ：Rodney Cheung
"""
import os
from typing import List


class TestUtil:
    @staticmethod
    def get_test_data_path() -> str:
        test_root_path_component: List[str] = list()
        for path_component in os.getcwd().split(os.path.sep):
            if path_component != 'test':
                test_root_path_component.append(path_component)
            else:
                test_root_path_component.append(path_component)
                break
        test_root_path = os.path.sep.join(test_root_path_component)
        return os.path.join(test_root_path, 'testdata')
