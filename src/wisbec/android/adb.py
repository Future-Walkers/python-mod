# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : adb.py
# Time       ：2020/8/19 15:09
# Author     ：Rodney Cheung
"""

import time
from typing import Optional

from wisbec.console.shell import exec_cmd
from wisbec.logging.log import Log
from wisbec import system


class AdbException(Exception):
    def __init__(self, err_info):
        self.err_info = err_info

    def __str__(self):
        return repr(self.err_info)


class Adb(object):
    adb_path = None

    @classmethod
    def init(cls, adb_path):
        cls.adb_path = adb_path

    @staticmethod
    def devices(alive: bool = False) -> [str]:
        """
        获取所有设备列表
        :param alive: 只显示在线的设备
        :return: 设备号数组
        """
        devices = []
        ret_code, out, err = Adb.exec("devices")
        for line in out.split('\n')[1:]:
            splits = line.split()
            if len(splits) >= 2:
                device = splits[0]
                status = splits[1]
                if not alive or status == "device":
                    devices.append(device)
        return devices

    @staticmethod
    def wait_device(dev_id, timeout):
        s = time.time()
        while time.time() - s <= timeout:
            list_devs = Adb.devices(alive=True)
            if dev_id in list_devs:
                return True
            Log.warning('等待{}设备上线中...', dev_id)
            time.sleep(1)
        pass

    # return: code, out, err
    @classmethod
    def exec(cls, *args):
        """
        执行命令
        :param args: 命令
        :return: 输出结果
        """
        if cls.adb_path is not None:
            args = [cls.adb_path] + list(args)
        else:
            args = ['adb'] + list(args)
        code, out, err = exec_cmd(args)
        return code, out, err

    @staticmethod
    def shell(device_id, *args):
        code, out, err = Adb.exec('-s', device_id, 'shell', *args)
        return code, out, err

    @staticmethod
    def su_shell(device_id, *args):
        code, out, err = Adb.shell(device_id, 'su', '-c', 'id', '-Z')
        if code != 0:
            su_cmd = '0'
        else:
            if 'magisk' in out:
                su_cmd = '-c'
            else:
                su_cmd = '0'
        code, out, err = Adb.exec('-s', device_id, 'shell', 'su', su_cmd, *args)
        return code, out, err

    @staticmethod
    def top_app(device_id) -> str:
        code, out, err = Adb.shell(device_id,
                                   "dumpsys", "activity", "top", "|", "grep", "^TASK", "-A", "0")
        sdk_level = Adb.get_sdk_level(device_id)
        if sdk_level >= 26:
            current_app: str = out.strip().split(system.get_newline_ch())[-1].strip()
        else:
            current_app: str = out.strip().split(system.get_newline_ch())[0].strip()
        return current_app.split(' ')[1]

    @staticmethod
    def screen_cap(device_id, save_path):
        code, out, err = Adb.shell(device_id,
                                   "screencap", "-p", save_path)
        return out == '' and err == ''

    @staticmethod
    def push(device_id, src, dst):
        code, out, err = Adb.exec('-s', device_id, 'push', src, dst)
        return code == 0

    @staticmethod
    def pull(device_id, src, dst):
        code, out, err = Adb.exec('-s', device_id, 'pull', src, dst)
        return code == 0

    @staticmethod
    def install(device_id, apk_path):
        code, out, err = Adb.exec('-s', device_id, 'install', apk_path)
        return 'Success' in out

    @staticmethod
    def id(device_id):
        code, out, err = Adb.exec('-s', device_id, 'id')
        s = out.find('uid=')
        e = out.find('(')
        return int(out[s + 4:e])

    # is_suc, msg
    @staticmethod
    def disable_verify(device_id):
        code, out, err = Adb.exec('-s', device_id, 'disable-verity')
        if err != '':
            return False, err
        return True, ''

    @staticmethod
    def get_sdk_level(device_id: str) -> int:
        code, out, err = Adb.shell(device_id, 'getprop', 'ro.build.version.sdk')
        if code != 0:
            raise AdbException('get device sdk level exception:{0}'.format(err))
        else:
            return int(out.strip())
