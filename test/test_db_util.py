#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Author: Rodney Cheung
@Date: 2020-06-30 09:58:50
@LastEditors: Rodney Cheung
@LastEditTime: 2020-06-30 10:33:17
@FilePath: /python-mod/test/test_db_util.py
'''
import pytest
import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from mod.db_util import MySqlDataBase

def test_connect_by_ssh_tunnel():
    mysqlDb=MySqlDataBase('sherry', 'sherry', '192.168.37.5', 3306,
                                  'sherry', True)
    mysqlDb.connect_by_ssh_tunnel('192.168.49.59', 22, 'ubuntu',
                                        '/Users/rodneycheung/.ssh/id_rsa')
    query='SELECT count(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA=\'sherry\''
    mysqlDb.connection.cursor().execute(query)