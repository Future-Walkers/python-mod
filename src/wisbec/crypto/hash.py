# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : hash.py
# Time       ：2020/10/13 17:19
# Author     ：Rodney Cheung
"""
import hashlib
import os
from typing import Optional

from wisbec.console import shell


class HashUtil:
    @staticmethod
    def get_file_md5(file_path: str) -> Optional[str]:
        if not os.path.isfile(file_path):
            return None
        md5hash = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                b = f.read(8096)
                if not b:
                    break
                md5hash.update(b)
        return md5hash.hexdigest()

    @staticmethod
    def calc_hash_name_by_openssl_x509(cacert_path: str) -> Optional[str]:
        args = ['openssl', 'x509', '-subject_hash_old', '-in', cacert_path]
        code, out, err = shell.exec_cmd(args)
        if code != 0:
            return None
        return '{}.0'.format(out.split(os.linesep)[0])
