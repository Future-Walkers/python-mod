# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : zip.py
# Time       ：2020/8/19 15:50
# Author     ：Rodney Cheung
"""
import shutil


def zip_file(output_full_path, input_dir):
    shutil.make_archive(output_full_path, 'zip', input_dir)


def unzip_file(filename, dest_dir=None, fmt=None):
    shutil.unpack_archive(filename, dest_dir, fmt)
