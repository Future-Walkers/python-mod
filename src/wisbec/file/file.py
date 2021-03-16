# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : file.py
# Time       ：2020/10/14 10:37
# Author     ：Rodney Cheung
"""
from typing import AnyStr

import chardet


class FileUtil:
    @staticmethod
    def read_file(path: str, bytes_num=-1) -> AnyStr:
        """
        read file content
        Args:
            path: file file_path
            bytes_num: read bytes,default is read all bytes
        Returns:
            file content
        """
        with open(path, 'rb') as f:
            return f.read(bytes_num)

    @classmethod
    def get_file_encoding(cls, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            out = chardet.detect(f.read())
            return out['encoding']

    @classmethod
    def read_file_by_encoding(cls, file_path: str, bytes_num: int = -1) -> AnyStr:
        file_encoding = cls.get_file_encoding(file_path)
        with open(file_path, encoding=file_encoding) as f:
            return f.read(bytes_num)

    @staticmethod
    def last_line(file_path: str) -> str:
        """
        get last line of file,line separator will be ignored
        Args:
            file_path: file file_path
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
