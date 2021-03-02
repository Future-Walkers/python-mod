# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : ps_info.py
# Time       ：12/11/20 11:09
# Author     ：Rodney Cheung
"""


class PsInfo:
    def __init__(self, user='', pid=0, ppid=0, vsz='', rss='', wchan='', addr='', status='', name=''):
        self.__user = user
        self.__pid = pid
        self.__ppid = ppid
        self.__vsz = vsz
        self.__rss = rss
        self.__wchan = wchan
        self.__addr = addr
        self.__status = status
        self.__name = name

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    @property
    def pid(self):
        return self.__pid

    @pid.setter
    def pid(self, value):
        self.__pid = value

    @property
    def ppid(self):
        return self.__ppid

    @ppid.setter
    def ppid(self, value):
        self.__ppid = value

    @property
    def vsz(self):
        return self.__vsz

    @vsz.setter
    def vsz(self, value):
        self.__vsz = value

    @property
    def rss(self):
        return self.__rss

    @rss.setter
    def rss(self, value):
        self.__rss = value

    @property
    def wchan(self):
        return self.__wchan

    @wchan.setter
    def wchan(self, value):
        self.__wchan = value

    @property
    def addr(self):
        return self.__addr

    @addr.setter
    def addr(self, value):
        self.__addr = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
