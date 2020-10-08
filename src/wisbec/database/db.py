#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Time    : 8/18/20 1:56 PM
@Author  : Rodney Cheung
@File    : db.py
"""


import sqlite3
import pymysql
from sshtunnel import SSHTunnelForwarder
from wisbec.design_patterns.singleton import SingletonType
from dbutils.pooled_db import PooledDB


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


class MySqlDataBaseWithConnectionPool(metaclass=SingletonType):
    __connection_pool = None

    def __init__(self,
                 username,
                 password,
                 host,
                 port,
                 database_name,
                 raise_on_warnings=True):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.raise_on_warnings = raise_on_warnings
        self.tunnel = None

    # 创建数据库连接conn和游标cursor
    def __enter__(self):
        self.conn = self.__get_conn()
        self.cursor = self.conn.cursor()

    # 创建数据库连接池
    def __get_conn(self):
        if self.__connection_pool is None:
            self.__connection_pool = PooledDB(
                creator=pymysql,
                maxconnections=100,
                blocking=True,
                host=self.host,
                port=self.port,
                user=self.username,
                passwd=self.password,
                db=self.database_name,
                use_unicode=False,
                charset='utf8'
            )
        return self.__connection_pool.connection()

    # 释放连接池资源
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    # 从连接池中取出一个连接
    def getconn(self):
        conn = self.__get_conn()
        cursor = conn.cursor()
        return cursor, conn
