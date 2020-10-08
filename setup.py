'''
Author: Sphantix Hang
Date: 2020-10-08 08:54:31
LastEditors: Sphantix Hang
LastEditTime: 2020-10-08 11:48:35
FilePath: /python-mod/setup.py
'''
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
# File       : setup.py
# Time       ：2020/8/19 15:53
# Author     ：Rodney Cheung
"""


from glob import glob
from os.path import basename
from os.path import splitext
import setuptools
with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE') as f:
    lic = f.read()


def find_version(file_name):
    with open(file_name) as file_handle:
        lines = file_handle.readlines()
        latest_version = lines[0].strip("\n").rstrip(']').lstrip('[')
        print("wisbec:", latest_version)
        return latest_version


setuptools.setup(
    name='wisbec',
    version=find_version('./ChangeLog'),
    author='rodneycheung',
    author_email='jsrdzhk@gmail.com',
    description='python wrappers',
    long_description='python wrappers',
    long_description_content_type='text/markdown',
    url='https://github.com/Future-Walkers/python-mod',
    license=lic,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    platforms=['any'],
    install_requires=['sshtunnel', 'pymysql', 'colorlog', 'DBUtils'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    zip_safe=False)
