# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : adb.py
# Time       ：2020/8/19 15:09
# Author     ：Rodney Cheung
"""
import os
import time
from typing import List, AnyStr

from wisbec.console.shell import exec_cmd
from wisbec.logging.log import Log


class AdbException(Exception):
    def __init__(self, err_info):
        self.err_info = err_info

    def __str__(self):
        return repr(self.err_info)


class Adb(object):
    adb_path: str = ''

    @classmethod
    def init(cls, adb_path: str):
        cls.adb_path = adb_path

    @staticmethod
    def devices(alive: bool = False) -> List[str]:
        """
        获取所有设备列表
        :param alive: 只显示在线的设备
        :return: 设备号数组
        """
        devices = list()
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
    def wait_device(device_id: str, timeout):
        s = time.time()
        while time.time() - s <= timeout:
            list_devs = Adb.devices(alive=True)
            if device_id in list_devs:
                return True
            Log.warning('等待{}设备上线中...', device_id)
            time.sleep(1)
        pass

    # return: code, out, err
    @classmethod
    def exec(cls, *args) -> (int, AnyStr, AnyStr):
        """
        执行命令
        :param args: 命令
        :return: 输出结果
        """
        if cls.adb_path != '':
            args = [cls.adb_path] + list(args)
        else:
            args = ['adb'] + list(args)
        return exec_cmd(args)

    @staticmethod
    def shell(device_id: str, *args) -> (int, AnyStr, AnyStr):
        return Adb.exec('-s', device_id, 'shell', *args)

    @staticmethod
    def su_shell(device_id: str, *args) -> (int, AnyStr, AnyStr):
        code, out, err = Adb.shell(device_id, 'su', '-c', 'id', '-Z')
        if code != 0:
            su_cmd = '0'
        else:
            if 'magisk' in out:
                su_cmd = '-c'
            else:
                su_cmd = '0'
        return Adb.exec('-s', device_id, 'shell', 'su', su_cmd, *args)

    @staticmethod
    def top_app(device_id: str, sdk_level: int) -> str:
        code, out, err = Adb.shell(device_id,
                                   "dumpsys", "activity", "top", "|", "grep", "^TASK", "-A", "0")
        if sdk_level >= 26:
            current_app: str = out.strip().split(os.linesep)[-1].strip()
        else:
            current_app: str = out.strip().split(os.linesep)[0].strip()
        return current_app.split(' ')[1]

    @staticmethod
    def screen_cap(device_id: str, save_path: str) -> bool:
        code, out, err = Adb.shell(device_id,
                                   "screencap", "-p", save_path)
        return out == '' and err == ''

    @staticmethod
    def push(device_id: str, src: str, dst: str) -> bool:
        code, out, err = Adb.exec('-s', device_id, 'push', src, dst)
        return code == 0

    @staticmethod
    def pull(device_id: str, src: str, dst: str) -> bool:
        code, out, err = Adb.exec('-s', device_id, 'pull', src, dst)
        return code == 0

    @staticmethod
    def install(device_id: str, apk_path: str) -> bool:
        code, out, err = Adb.exec('-s', device_id, 'install', apk_path)
        return 'Success' in out

    @staticmethod
    def id(device_id: str) -> int:
        code, out, err = Adb.exec('-s', device_id, 'id')
        s = out.find('uid=')
        e = out.find('(')
        return int(out[s + 4:e])

    # is_suc, msg
    @staticmethod
    def disable_verify(device_id: str) -> (bool, AnyStr):
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
