# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_zip.py
# Time       ：2020/8/19 15:54
# Author     ：Rodney Cheung
"""
import os
import unittest

from test.testdata.test_util import TestUtil
from wisbec.file.zip import ZipUtil
from wisbec.filesystem.filesystem import FilesystemUtil


class TestZip(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_data_dir = os.path.join(TestUtil.get_test_data_path(), 'file', 'zip')

    def test_zip_and_unzip_file(self):
        ZipUtil.zip_file(os.path.join(self.test_data_dir, 'test2.xml'),
                         self.test_data_dir)
        zipped_file_path = os.path.join(self.test_data_dir, 'test2.xml.zip')
        ZipUtil.unzip_file(zipped_file_path, self.test_data_dir)
        FilesystemUtil.remove(zipped_file_path)


if __name__ == '__main__':
    unittest.main()
