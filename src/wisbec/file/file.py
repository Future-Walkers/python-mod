# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : file.py
# Time       ：2020/10/14 10:37
# Author     ：Rodney Cheung
"""
from typing import AnyStr


class FileUtil:
    @staticmethod
    def read_file(path: str, bytes_num=-1) -> AnyStr:
        """
        read file content
        Args:
            path: file path
            bytes_num: read bytes,default is read all bytes
        Returns:
            file content
        """
        with open(path, 'rb') as f:
            return f.read(bytes_num)

    @staticmethod
    def last_line(file_path: str) -> str:
        """
        get last line of file,line separator will be ignored
        Args:
            file_path: file path
        Returns:
            content of last line,empty str if there is no content in file
        """
        with open(file_path) as fp:
            lines = fp.readlines()
            if len(lines) == 0:
                return ""
            return lines[-1].strip()

    @staticmethod
    def write_file(path: str, mode: str, data: AnyStr):
        with open(path, mode) as f:
            f.write(data)