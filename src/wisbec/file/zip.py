# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : zip.py
# Time       ：2020/8/19 15:50
# Author     ：Rodney Cheung
"""
import shutil


class ZipUtil:
    @staticmethod
    def zip_file(src_path, dst_path):
        shutil.make_archive(src_path, 'zip', dst_path)

    @staticmethod
    def unzip_file(src_zip, dst_dir=None, fmt=None):
        shutil.unpack_archive(src_zip, dst_dir, fmt)
