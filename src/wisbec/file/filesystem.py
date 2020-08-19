#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
# File       : filesystem.py
# Time       ：2020/8/19 15:09
# Author     ：Rodney Cheung
"""
import os
import shutil


def is_directory_exist(dir_full_path) -> bool:
    """
    symbolic link or dir
    Args:
        dir_full_path: dir path

    Returns:

    """
    return os.path.isdir(dir_full_path)


def is_file_exist(file_full_path) -> bool:
    """
    symbolic link or file
    Args:
        file_full_path:file path

    Returns:

    """
    return os.path.isfile(file_full_path)


def create_directories(dir_full_path):
    """
    create directory recursively
    Args:
        dir_full_path: dir path

    Returns:

    """
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


def replace_extension(file_path, replacement):
    """
    replace file name's extension
    Args:
        file_path: file path
        replacement: target extension

    Returns:
        replaced file name
    """
    base_name, extension = os.path.splitext(file_path)
    if len(replacement) == 0:
        return base_name
    else:
        return base_name + '.' + replacement


def list_dir_recursively(path: str, include_ext_name=None) -> list:
    """
    list files on path
    Args:
        path: target path
        include_ext_name: include extensions,if None,all files are listed

    Returns:
        file lists
    """
    files = os.listdir(path)
    res = list()
    for file in files:
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            res.extend(list_dir_recursively(filepath, include_ext_name))
        else:
            if (include_ext_name is None) or (include_ext_name is not None and filepath.endswith(include_ext_name)):
                res.append(filepath)
    return res
