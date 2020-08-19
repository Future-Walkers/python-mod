#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
# File       : test_filesystem.py
# Time       ：2020/8/19 15:53
# Author     ：Rodney Cheung
"""
import os
import unittest

from wisbec.file import filesystem


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
        filesystem.create_directories(self.test_dir)
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

    def test_replace_extension(self):
        self.assertEqual(filesystem.replace_extension(os.path.join(os.getcwd(), 'requirements.txt'), ''),
                         os.path.join(os.getcwd(), 'requirements'))
        self.assertEqual(filesystem.replace_extension(os.path.join(os.getcwd(), 'requirements.txt'), 'png'),
                         os.path.join(os.getcwd(), 'requirements.png'))

    def test_list_dir_recursively(self):
        res = filesystem.list_dir_recursively('/Users/jsrdzhk/PycharmProjects', '.xml')
        print(res)


if __name__ == '__main__':
    unittest.main()
