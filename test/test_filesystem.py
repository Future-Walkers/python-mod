#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Author: Rodney Cheung
@Date: 2020-06-30 18:30:55
@LastEditors: Rodney Cheung
@LastEditTime: 2020-07-02 09:18:01
@FilePath: /python-mod/test/test_filesystem.py
"""
import unittest

from mod import filesystem
import os


class TestFilesystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_data_dir = os.path.join(os.getcwd(), 'test_data')
        cls.test_filesystem_py = os.path.abspath(__file__)
        cls.test_dir = os.path.join(cls.test_data_dir, 'test_directory')
        cls.test_file = os.path.join(cls.test_data_dir, "test_file.txt")

    def test_filesystem(self):
        # test is_dir_exist
        self.assertEqual(filesystem.is_directory_exist('/test/wq/code/Future-Walkers'), False)
        self.assertEqual(filesystem.is_directory_exist(self.test_data_dir), True)
        # test is_file_exist
        self.assertEqual(filesystem.is_file_exist(self.test_filesystem_py), True)
        # test create_directory
        filesystem.create_directory(self.test_dir)
        self.assertEqual(filesystem.is_directory_exist(self.test_dir), True)
        # test remove directory
        filesystem.remove(self.test_dir)
        self.assertEqual(filesystem.is_directory_exist(self.test_dir), False)
        # test create_file
        filesystem.create_file(self.test_file)
        self.assertEqual(filesystem.is_file_exist(self.test_file), True)
        # test remove file
        filesystem.remove(self.test_file)
        self.assertEqual(filesystem.is_file_exist(self.test_file), False)

    def test_get_file_md5(self):
        md5 = filesystem.get_file_md5(self.test_filesystem_py)

    def test_create_zip_file(self):
        filesystem.create_zip_file(os.path.join(self.test_data_dir, 'test.zip'),
                                   os.path.join(os.path.pardir, 'mod'))


if __name__ == '__main__':
    unittest.main()
