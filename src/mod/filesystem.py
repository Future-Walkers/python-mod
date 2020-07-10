#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Author: Rodney Cheung
@Date: 2020-06-29 10:29:37
@LastEditors: Rodney Cheung
@LastEditTime: 2020-06-29 10:33:00
@FilePath: /python-mod/core/filesystem.py
"""
import os
import shutil
import hashlib


def is_directory_exist(dir_full_path):
    return os.path.exists(dir_full_path) and os.path.isdir(dir_full_path)


def is_file_exist(file_full_path):
    return os.path.exists(file_full_path) and os.path.isfile(file_full_path)


def create_directory(dir_full_path):
    if not is_directory_exist(dir_full_path):
        os.makedirs(dir_full_path)


def remove(full_path):
    if not os.path.exists(full_path):
        return
    else:
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path, ignore_errors=True)


def create_file(full_path):
    if os.path.exists(full_path):
        print("{0} already existed.".format(full_path))
        return

    f = open(full_path, 'w')
    f.close()


def copy_file(src_full_path, dst_full_path):
    shutil.copy2(src_full_path, dst_full_path)


def get_file_md5(file_full_path):
    if not os.path.isfile(file_full_path):
        return
    md5hash = hashlib.md5()
    with open(file_full_path, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            md5hash.update(b)

    return md5hash.hexdigest()


def create_zip_file(output_full_path, input_dir):
    shutil.make_archive(output_full_path, 'zip', input_dir)
