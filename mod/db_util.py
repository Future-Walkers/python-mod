#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''
@Author: Rodney Cheung
@Date: 2020-06-29 11:02:22
@LastEditors: Rodney Cheung
@LastEditTime: 2020-06-29 16:35:59
@FilePath: /python-mod/mod/db_util.py
'''
import sqlite3
import mysql.connector
from mysql.connector import errorcode
import sshtunnel


class DataBase(object):
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        pass

    def close(self):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()


class Sqlite3DataBase(DataBase):
    def __init__(self, db_path):
        super(Sqlite3DataBase, self).__init__()
        self.db_path = db_path

    def connect(self):
        self.connection = sqlite3.connect(self.db_path,
                                          check_same_thread=False)
        self.cursor = self.connection.cursor()


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
        try:
            config = {
                'user': self.username,
                'password': self.password,
                'host': self.host,
                'port': self.port,
                'database': self.database_name,
                'raise_on_warnings': self.raise_on_warnings
            }
            self.connection = mysql.connector.connect(config)
            self.cursor = self.connection.cursor
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def connect_by_ssh_tunnel(self, ssh_host, ssh_port, ssh_username,
                              ssh_private_key):
        try:
            with open(ssh_private_key) as f:
                pkey = f.read()
                self.tunnel = sshtunnel.SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_username,
                    ssh_pkey=pkey,
                    remote_bind_address=(self.host, self.port))
                self.tunnel.start()
                config = {
                    'user': self.username,
                    'password': self.password,
                    'host': '127.0.0.1',
                    'port': self.tunnel.local_bind_port,
                    'database': self.database_name,
                    'raise_on_warnings': self.raise_on_warnings
                }
                self.connection = mysql.connector.connect(config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close(self):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()
        if self.tunnel is not None:
            self.tunnel.stop()