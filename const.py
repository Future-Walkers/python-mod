#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
@Author: Sphantix Hang
@Date: 2020-04-22 11:11:08
@LastEditors: Sphantix Hang
@LastEditTime: 2020-04-22 11:31:20
@FilePath: /urldownload/const.py
'''
import sys


class Const(object):
    # pylint: disable=too-few-public-methods
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError("Can't change const.{0}!".format(key))
        if not key.isupper():
            raise self.ConstCaseError(("cosnt name '{0}' is not all uppercase!"
                                       .format(key)))
        self.__dict__[key] = value


sys.modules[__name__] = Const()