#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Author: Rodney Cheung
@Date: 2020-06-30 09:58:50
@LastEditors: Rodney Cheung
@LastEditTime: 2020-07-01 09:39:11
@FilePath: /python-wisbec/test/test_db_util.py
"""
from wisbec.database.db import MySqlDataBase
import unittest


class TestDbUtils(unittest.TestCase):
    def test_connect_by_ssh_tunnel(self):
        mysql_db = MySqlDataBase('sherry', 'sherry', '192.168.37.5', 3306, 'sherry',
                                True)
        mysql_db.connect_by_ssh_tunnel('192.168.49.59', 22, 'ubuntu',
                                      '/Users/rodneycheung/.ssh/id_rsa')
        query = 'SELECT count(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'sherry\''
        with mysql_db.connection.cursor() as cursor:
            cursor.execute(query)
            query_res = cursor.fetchall()
            self.assertEqual(query_res, 8)

    def test_connect(self):
        mysql_db = MySqlDataBase('root', 'wq', '127.0.0.1', 3306, 'sherry')
        mysql_db.connect()
        query = 'SELECT count(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'sherry\''
        with mysql_db.connection.cursor() as cursor:
            cursor.execute(query)
            query_res = cursor.fetchall()
            self.assertEqual(query_res, 8)
