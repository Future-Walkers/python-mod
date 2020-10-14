#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
# File       : test_filesystem.py
# Time       ：2020/8/19 15:53
# Author     ：Rodney Cheung
"""
import os
import unittest

from test.testdata.test_util import TestUtil
from wisbec.filesystem.filesystem import FilesystemUtil


class TestFilesystemUtil(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_data_dir = os.path.join(TestUtil.get_test_data_path(), 'file', 'filesystem')
        cls.test_filesystem_py = os.path.abspath(__file__)
        cls.test_dir = os.path.join(cls.test_data_dir, 'test_directory')
        cls.test_file = os.path.join(cls.test_data_dir, "test_file.txt")

    def test_filesystem(self):
        # test is_dir_exist
        self.assertEqual(FilesystemUtil.is_directory_exist('/test/wq/code/Future-Walkers'), False)
        self.assertEqual(FilesystemUtil.is_directory_exist(self.test_data_dir), True)
        # test is_file_exist
        self.assertEqual(FilesystemUtil.is_file_exist(self.test_filesystem_py), True)
        # test create_directory
        FilesystemUtil.create_directories(self.test_dir)
        self.assertEqual(FilesystemUtil.is_directory_exist(self.test_dir), True)
        # test remove directory
        FilesystemUtil.remove(self.test_dir)
        self.assertEqual(FilesystemUtil.is_directory_exist(self.test_dir), False)
        # test create_file
        FilesystemUtil.create_file(self.test_file)
        self.assertEqual(FilesystemUtil.is_file_exist(self.test_file), True)
        # test remove file
        FilesystemUtil.remove(self.test_file)
        self.assertEqual(FilesystemUtil.is_file_exist(self.test_file), False)

    def test_replace_extension(self):
        self.assertEqual(FilesystemUtil.replace_extension(os.path.join(os.getcwd(), 'requirements.txt'), ''),
                         os.path.join(os.getcwd(), 'requirements'))
        self.assertEqual(FilesystemUtil.replace_extension(os.path.join(os.getcwd(), 'requirements.txt'), 'png'),
                         os.path.join(os.getcwd(), 'requirements.png'))

    def test_list_dir_recursively(self):
        res = FilesystemUtil.list_dir_recursively(self.test_data_dir, '.xml')
        print(res)

    def test_list_dir(self):
        res = FilesystemUtil.list_dir(self.test_data_dir, depth=3, include_ext_name='.py')
        self.assertEqual(res, [])

    def test_list_dirs_on_dir(self):
        print(FilesystemUtil.list_dirs_on_dir(self.test_data_dir))

    def test_add_executable(self):
        print(os.stat(__file__).st_mode)
        FilesystemUtil.add_executable(__file__)
        print(os.stat(__file__).st_mode)

    def test_remove_executable(self):
        print(os.stat(__file__).st_mode)
        FilesystemUtil.remove_executable(__file__)
        print(os.stat(__file__).st_mode)


if __name__ == '__main__':
    unittest.main()
