#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Author: Rodney Cheung
@Date: 2020-06-24 09:14:52
@LastEditors: Rodney Cheung
@LastEditTime: 2020-06-29 15:23:02
@FilePath: /python-mod/setup.py
'''
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name = 'mod',
    version = '0.0.1',
    author = 'wq',
    author_email = 'wq@antiy.cn',
    description = 'python wrappers',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Future-Walkers/python-mod',
    license = license,
    packages = setuptools.find_packages(),
    zip_safe = False
)