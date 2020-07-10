#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Author: Rodney Cheung
@Date: 2020-06-29 11:02:22
@LastEditors: Rodney Cheung
@LastEditTime: 2020-06-30 09:58:10
@FilePath: /python-mod/mod/db_util.py
"""
import sqlite3
from sshtunnel import SSHTunnelForwarder
import pymysql


class DataBase(object):
    def __init__(self):
        self.connection = None

    def connect(self):
        pass

    def close(self):
        self.connection.commit()
        self.connection.close()

    def __del__(self):
        self.close()


class Sqlite3DataBase(DataBase):
    def __init__(self, db_path):
        super(Sqlite3DataBase, self).__init__()
        self.db_path = db_path

    def connect(self):
        self.connection = sqlite3.connect(self.db_path,
                                          check_same_thread=False)


class MySqlDataBase(DataBase):
    def __init__(self,
                 username,
                 password,
                 host,
                 port,
                 database_name,
                 raise_on_warnings=True):
        super(MySqlDataBase, self).__init__()
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.raise_on_warnings = raise_on_warnings
        self.tunnel = None

    def connect(self):
        self.connection = pymysql.connect(host=self.host,
                                          port=self.port,
                                          user=self.username,
                                          password=self.password,
                                          db=self.database_name)

    def connect_by_ssh_tunnel(self, ssh_host, ssh_port, ssh_username,
                              ssh_private_key):
        self.tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_pkey=ssh_private_key,
            remote_bind_address=(self.host, self.port))
        self.tunnel.start()
        self.connection = pymysql.connect(host='127.0.0.1',
                                          port=self.tunnel.local_bind_port,
                                          user=self.username,
                                          password=self.password,
                                          db=self.database_name)

    def close(self):
        self.connection.commit()
        self.connection.close()
        if self.tunnel is not None:
            self.tunnel.stop()