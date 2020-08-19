# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : zip.py
# Time       ：2020/8/19 15:50
# Author     ：Rodney Cheung
"""
import shutil


def create_zip_file(output_full_path, input_dir):
    shutil.make_archive(output_full_path, 'zip', input_dir)
