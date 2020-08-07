#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Author: Rodney Cheung
@Date: 2020-06-24 09:14:52
@LastEditors: Rodney Cheung
@LastEditTime: 2020-07-01 09:25:48
@FilePath: /python-mod/setup.py
'''
import setuptools
from os.path import splitext
from os.path import basename
from glob import glob

with open('README.md', 'r') as f:
    long_description = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name='wisbec',
    version='0.0.2',
    author='rodneycheung',
    author_email='jsrdzhk@gmail.com',
    description='python wrappers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Future-Walkers/python-mod',
    license=license,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    platforms=['any'],
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
