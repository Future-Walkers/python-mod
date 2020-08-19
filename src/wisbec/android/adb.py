# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : adb.py
# Time       ：2020/8/19 15:09
# Author     ：Rodney Cheung
"""

import time

from wisbec.console.shell import exec_cmd
from wisbec.logging.log import Log


class Adb(object):

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
    @staticmethod
    def exec(*args):
        """
        执行命令
        :param args: 命令
        :return: 输出结果
        """
        args = ['adb'] + list(args)
        code, out, err = exec_cmd(args)
        return code, out, err

    @staticmethod
    def shell(device_id, *args):
        code, out, err = Adb.exec('-s', device_id, 'shell', *args)
        return code, out, err

    @staticmethod
    def top_app(device_id):
        code, out, err = Adb.shell(device_id,
                                   "dumpsys", "activity", "top", "|", "grep", "^TASK", "-A", "1")
        try:
            return out.split('\n')[1].strip().split(' ')[1].split('/')[0]
        except:
            return None

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
