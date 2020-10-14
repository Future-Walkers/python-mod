#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
# File       : filesystem.py
# Time       ：2020/8/19 15:09
# Author     ：Rodney Cheung
"""
import os
import shutil
import stat
from typing import List


class FilesystemUtil:
    @staticmethod
    def is_directory_exist(dir_path: str) -> bool:
        """
        symbolic link or dir
        Args:
            dir_path: dir path

        Returns:

        """
        return os.path.isdir(dir_path)

    @staticmethod
    def is_file_exist(dir_path: str) -> bool:
        """
        symbolic link or file
        Args:
            dir_path:file path

        Returns:

        """
        return os.path.isfile(dir_path)

    @classmethod
    def create_directories(cls, dir_path: str):
        """
        create directory recursively
        Args:
            dir_path: dir path

        Returns:

        """
        if not cls.is_directory_exist(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def remove(file_path: str):
        if not os.path.exists(file_path):
            return
        else:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path, ignore_errors=True)

    @staticmethod
    def create_file(file_path: str):
        if os.path.exists(file_path):
            print("{0} already existed.".format(file_path))
            return

        f = open(file_path, 'w')
        f.close()

    @staticmethod
    def copy_file(src_full_path, dst_full_path):
        shutil.copy2(src_full_path, dst_full_path)

    @staticmethod
    def replace_extension(file_path: str, replacement: str):
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

    @classmethod
    def list_dir_recursively(cls, path: str, include_ext_name=None) -> list:
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
                res.extend(cls.list_dir_recursively(filepath, include_ext_name))
            else:
                if (include_ext_name is None) or (include_ext_name is not None and filepath.endswith(include_ext_name)):
                    res.append(filepath)
        return res

    @classmethod
    def list_dir(cls, path: str, depth=1, include_ext_name=None) -> list:
        files = os.listdir(path)
        res = list()
        if depth <= 0:
            return res
        for file in files:
            filepath = os.path.join(path, file)
            if os.path.isdir(filepath):
                depth -= 1
                res.extend(cls.list_dir(filepath, depth, include_ext_name))
                depth += 1
            else:
                if (include_ext_name is None) or (include_ext_name is not None and filepath.endswith(include_ext_name)):
                    res.append(filepath)
        return res

    @staticmethod
    def list_dirs_on_dir(path: str) -> List[str]:
        files = os.listdir(path)
        res = list()
        for file in files:
            filepath = os.path.join(path, file)
            if os.path.isdir(filepath):
                res.append(filepath)
        return res

    @staticmethod
    def add_executable(file_path: str):
        """
        equivalent of chmod +x file_path,posix supported only,do not call it on windows
        Args:
            file_path:

        Returns:

        """
        file_mode = os.stat(file_path).st_mode
        os.chmod(file_path, file_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    @staticmethod
    def remove_executable(file_path: str):
        """
        equivalent of chmod -x file_path,posix supported only,do not call it on windows
        Args:
            file_path:

        Returns:

        """
        file_mode = os.stat(file_path).st_mode
        os.chmod(file_path, file_mode & ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH)
