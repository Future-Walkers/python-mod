# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : adb.py
# Time       ：2020/8/19 15:09
# Author     ：Rodney Cheung
"""
import os
import re
import time
from typing import List, AnyStr, Set

from wisbec.console.shell import exec_cmd
from wisbec.logging.log import Log
from wisbec.parser.parse import Parser, InterfaceInfo
from wisbec.resource.resource import PackageResource
from wisbec.shell_parser.ps import PsParser


class AdbException(Exception):
    def __init__(self, err_info):
        self.err_info = err_info

    def __str__(self):
        return repr(self.err_info)


class Adb(object):
    adb_path: str = ''

    @classmethod
    def __get_su_cmd(cls, device_id: str) -> str:
        code, out, err = Adb.shell(device_id, 'su', '-c', 'id', '-Z')
        if code != 0:
            su_cmd = '0'
        else:
            if 'magisk' in out:
                su_cmd = '-c'
            else:
                su_cmd = '0'
        return su_cmd

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

    @classmethod
    def emulators(cls) -> List[str]:
        device_list = cls.devices(True)
        emulator_list = list()
        for device in device_list:
            if device.startswith('emulator'):
                emulator_list.append(device)
        return emulator_list

    @classmethod
    def real_devices(cls) -> List[str]:
        device_list = cls.devices(True)
        real_device_list = list()
        for device in device_list:
            if not device.startswith('emulator'):
                real_device_list.append(device)
        return real_device_list

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

    @classmethod
    def su_shell(cls, device_id: str, *args) -> (int, AnyStr, AnyStr):
        code, out, err = cls.shell(device_id, 'id')
        if code != 0:
            raise AdbException('check device is rooted exception:{0}'.format(err))
        else:
            if '(root)' in out:
                return cls.shell(device_id, *args)
            else:
                su_cmd = cls.__get_su_cmd(device_id)
                return Adb.shell(device_id, 'su', su_cmd, *args)

    @staticmethod
    def top_app(device_id: str, sdk_level: int) -> str:
        code, out, err = Adb.shell(device_id,
                                   "dumpsys", "activity", "top", "|", "grep", "^TASK", "-A", "1")
        if sdk_level >= 26:
            current_app: str = out.strip().split(os.linesep)[-1].strip()
        else:
            current_app: str = out.strip().split(os.linesep)[1].strip()
        return current_app.split(' ')[1].split('/')[0]

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
        if 'Success' in out:
            return True
        else:
            raise AdbException(out + err)

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

    @classmethod
    def get_installed_packages(cls, device_id: str) -> Set[str]:
        code, out, err = Adb.shell(device_id, 'pm', 'list', 'packages')
        if code != 0:
            raise AdbException('get system packages exception:{0}'.format(err))
        else:
            packages: List[str] = out.strip().split(os.linesep)
            installed_packages = set()
            for package in packages:
                installed_packages.add(package.split(':')[-1])
            return installed_packages

    @classmethod
    def get_user_installed_packages(cls, device_id: str) -> Set[str]:
        code, out, err = Adb.shell(device_id, 'pm', 'list', 'packages', '-3')
        if code != 0:
            raise AdbException('get system packages exception:{0}'.format(err))
        else:
            packages: List[str] = out.strip().split(os.linesep)
            user_installed_packages = set()
            for package in packages:
                user_installed_packages.add(package.split(':')[-1].strip())
            return user_installed_packages

    @staticmethod
    def get_system_packages(device_id: str) -> Set[str]:
        code, out, err = Adb.shell(device_id, 'pm', 'list', 'packages', '-s')
        if code != 0:
            raise AdbException('get system packages exception:{0}'.format(err))
        else:
            packages: List[str] = out.strip().split(os.linesep)
            system_packages = set()
            for package in packages:
                system_packages.add(package.split(':')[-1])
            return system_packages

    @classmethod
    def is_rooted(cls, device_id: str) -> bool:
        code, out, err = cls.shell(device_id, 'id')
        if code != 0:
            raise AdbException('check device is rooted exception:{0}'.format(err))
        else:
            if '(root)' in out:
                return True
            else:
                code, out, err = cls.su_shell(device_id, 'id')
                if code != 0:
                    raise AdbException('check device is rooted exception:{0}'.format(err))
                else:
                    return '(root)' in out

    @classmethod
    def is_system_partition_rw(cls, device_id: str) -> bool:
        code, out, err = cls.shell(device_id, 'mount')
        if code != 0:
            raise AdbException('get device mount info failed:{}'.format(err))
        else:
            mount_info_list = out.strip().split(os.linesep)
            for mount_info in mount_info_list:
                components = mount_info.split(' ')
                partition = components[2]
                fs_type = components[4]
                fs_auth = components[5]
                if partition == '/system' or partition == '/':
                    if fs_type == 'ext4':
                        if 'rw' in fs_auth:
                            return True
            return False

    @classmethod
    def get_device_model(cls, device_id: str) -> str:
        code, out, err = cls.shell(device_id, 'getprop', 'ro.product.model')
        if code != 0:
            raise AdbException('get device model failed:{}'.format(err))
        else:
            return out.strip()

    @classmethod
    def get_base_apk_path(cls, device_id: str, pkg_name: str):
        code, out, err = cls.shell(device_id, 'pm', 'path', pkg_name)
        if code != 0:
            raise AdbException('get base apk failed:{}'.format(err))
        else:
            return out[8:]

    @classmethod
    def get_app_name(cls, device_id: str, pkg_name: str):
        if not cls.is_path_exists(device_id, '/sdcard/android-tool.apk'):
            cls.push(device_id, PackageResource.get_android_tool_path(), '/sdcard')
        code, out, err = cls.shell(device_id,
                                   'CLASSPATH=/sdcard/android-tool.apk',
                                   'app_process', '/', 'android.tools.Main',
                                   'debug', '--app-name', pkg_name)
        if code != 0:
            raise AdbException('get app name failed:{}'.format(err))
        else:
            return out.strip()

    @classmethod
    def get_prop(cls, device_id: str, property_name: str, default=None):
        code, out, err = cls.shell(device_id, 'getprop ' + property_name)
        if code != 0:
            raise AdbException('get prop failed:{}'.format(err))
        else:
            out = out.strip()
            if out is None or out == '':
                return default
            return out

    @classmethod
    def forward(cls, device_id: str, dev: str, host: str):
        code, out, err = cls.exec('-s', device_id, 'forward', dev, host)
        if code != 0:
            raise AdbException('forward failed:{}'.format(err))

    @classmethod
    def is_path_exists(cls, device_id: str, path: str) -> bool:
        code, out, err = cls.shell(device_id, 'ls', path)
        return 'No such file or director' not in out + err

    @staticmethod
    def grant_permission(device_id, pkg_name, permission):
        code, out, err = Adb.shell(device_id, 'pm', 'grant', pkg_name, permission)
        if out + err != '':
            code, out, err = Adb.su_shell(device_id, 'pm', 'grant', pkg_name, permission)
            if out + err != '':
                return False, out + err
        return True, None

    @staticmethod
    def is_installed(device_id, pkg_name):
        code, out, err = Adb.shell(device_id, 'pm', 'path', pkg_name)
        return out + err != ''

    # return: is_succ, err_reason
    @staticmethod
    def start_service(device_id, *args):
        """
        [success]
        Starting service: Intent { cmp=com.pkiller.mocklocation/.MockLocationService (has extras) }

        [fail]
        # 8.0及以上系统，未申请android.permission.FOREGROUND_SERVIC权限，报如下错误：
        Starting service: Intent { cmp=com.pkiller.mocklocation/.MockLocationService (has extras) }
        Error: app is in background uid UidRecord{bcb15bb u0a120 CEM  idle change:cached procs:1 seq(0,0,0)}

        [fail]
        # 8.0及以上系统，未申请android.permission.FOREGROUND_SERVIC权限，报如下错误：
        Starting service: Intent { cmp=com.pkiller.mocklocation/.MockLocationService (has extras) }
        Error: app is in background uid null
        """
        code, out, err = Adb.shell(device_id, 'am', 'startservice', *args)
        out = out.strip()
        if (out + err).startswith('Starting service:') and ('\n' not in (out + err)):
            return True, None
        elif 'Error: app is in background uid' in (out + err):
            # v8.0及以后，后台服务需要通过 am start-foreground-service 启动，否则报如上错误
            code, out, err = Adb.shell(device_id, 'am', 'start-foreground-service', *args)
            out = out.strip()
            if out.startswith('Starting service:') and ('\n' not in (out + err)):
                return True, None
            return False, (out + err)
        else:
            return False, (out + err)

    # return: is_succ, err_reason
    @staticmethod
    def stop_service(device_id, *args):
        """
        [success]
        Stopping service: Intent { cmp=com.pkiller.mocklocation/.MockLocationService }
        Service stopped

        [fail]
        Stopping service: Intent { cmp=com.pkiller.mocklocation/.MockLocationServiced }
        Service not stopped: was not running.
        """
        code, out, err = Adb.shell(device_id, 'am', 'stopservice', *args)
        out = out.strip()
        if 'Service stopped' in (out + err):
            return True, None
        else:
            return False, (out + err)

    @staticmethod
    def get_app_permission(device_id, pkg_name):
        code, out, err = Adb.shell(device_id, 'pm', 'dump', pkg_name)
        if pkg_name not in out:
            return None

        dict_permissions = {}

        ST_NONE = 0
        ST_REQUESTED = 1
        ST_INSTALL = 2
        ST_RUNTIME = 3

        status = ST_NONE

        lines = out.split('\n')
        for line in lines:
            if line.strip() == 'requested permissions:':
                status = ST_REQUESTED
                continue
            elif line.strip() == 'install permissions:':
                status = ST_INSTALL
                continue
            elif line.strip() == 'runtime permissions:':
                status = ST_RUNTIME
                continue
            elif not line.strip().startswith('android.permission'):
                status = ST_NONE
                continue

            if status == ST_REQUESTED:
                line = line.strip()
                name = line if (':' not in line) else line[:line.find(':')]
                if name not in dict_permissions:
                    dict_permissions[name] = 'deny'
            elif status == ST_RUNTIME or status == ST_INSTALL:
                line = line.strip()
                name = line[:line.find(':')]
                mode = 'allow' if ('granted=true' in line) else 'deny'
                dict_permissions[name] = mode

        # 位置模拟权限特殊, 用其他方式获取
        if 'android.permission.ACCESS_MOCK_LOCATION' in dict_permissions:
            is_succ, mode = Adb.appops_get(device_id, pkg_name, 58)
            if is_succ is False:
                return None
            dict_permissions['android.permission.ACCESS_MOCK_LOCATION'] = mode

        return dict_permissions

    # return: is_success, mode
    # mode: allow|ignore|deny|default
    @staticmethod
    def appops_get(device_id, pkg_name, operation):
        code, out, err = Adb.shell(device_id, 'appops', 'get', pkg_name, str(operation))
        if code != 0:
            return False, None

        if 'No operations.' in out.strip():
            return True, 'deny'

        """
        > adb shell appops get com.pkiller.mocklocation MOCK_LOCATION
        MOCK_LOCATION: deny; rejectTime=+4m51s587ms ago
        """
        expected_modes = ['allow', 'ignore', 'deny', 'default']
        try:
            mode = out.strip().split(' ')[1].replace(';', '')
            if mode not in expected_modes:
                return False, None
            return True, mode
        except Exception as e:
            return False, None

    # return: is_success
    # mode: allow|ignore|deny|default
    @staticmethod
    def appops_set(device_id, pkg_name, operation, mode):

        """ @hide No operation specified. """
        OP_NONE = -1
        """ @hide Access to coarse location information. """
        OP_COARSE_LOCATION = 0
        """ @hide Access to fine location information. """
        OP_FINE_LOCATION = 1
        """ @hide Causing GPS to run. """
        OP_GPS = 2
        """ @hide """
        OP_VIBRATE = 3
        """ @hide """
        OP_READ_CONTACTS = 4
        """ @hide """
        OP_WRITE_CONTACTS = 5
        """ @hide """
        OP_READ_CALL_LOG = 6
        """ @hide """
        OP_WRITE_CALL_LOG = 7
        """ @hide """
        OP_READ_CALENDAR = 8
        """ @hide """
        OP_WRITE_CALENDAR = 9
        """ @hide """
        OP_WIFI_SCAN = 10
        """ @hide """
        OP_POST_NOTIFICATION = 11
        """ @hide """
        OP_NEIGHBORING_CELLS = 12
        """ @hide """
        OP_CALL_PHONE = 13
        """ @hide """
        OP_READ_SMS = 14
        """ @hide """
        OP_WRITE_SMS = 15
        """ @hide """
        OP_RECEIVE_SMS = 16
        """ @hide """
        OP_RECEIVE_EMERGECY_SMS = 17
        """ @hide """
        OP_RECEIVE_MMS = 18
        """ @hide """
        OP_RECEIVE_WAP_PUSH = 19
        """ @hide """
        OP_SEND_SMS = 20
        """ @hide """
        OP_READ_ICC_SMS = 21
        """ @hide """
        OP_WRITE_ICC_SMS = 22
        """ @hide """
        OP_WRITE_SETTINGS = 23
        """ @hide """
        OP_SYSTEM_ALERT_WINDOW = 24
        """ @hide """
        OP_ACCESS_NOTIFICATIONS = 25
        """ @hide """
        OP_CAMERA = 26
        """ @hide """
        OP_RECORD_AUDIO = 27
        """ @hide """
        OP_PLAY_AUDIO = 28
        """ @hide """
        OP_READ_CLIPBOARD = 29
        """ @hide """
        OP_WRITE_CLIPBOARD = 30
        """ @hide """
        OP_TAKE_MEDIA_BUTTONS = 31
        """ @hide """
        OP_TAKE_AUDIO_FOCUS = 32
        """ @hide """
        OP_AUDIO_MASTER_VOLUME = 33
        """ @hide """
        OP_AUDIO_VOICE_VOLUME = 34
        """ @hide """
        OP_AUDIO_RING_VOLUME = 35
        """ @hide """
        OP_AUDIO_MEDIA_VOLUME = 36
        """ @hide """
        OP_AUDIO_ALARM_VOLUME = 37
        """ @hide """
        OP_AUDIO_NOTIFICATION_VOLUME = 38
        """ @hide """
        OP_AUDIO_BLUETOOTH_VOLUME = 39
        """ @hide """
        OP_WAKE_LOCK = 40
        """ @hide Continually monitoring location data. """
        OP_MONITOR_LOCATION = 41
        """ @hide Continually monitoring location data with a relatively high power request. """
        OP_MONITOR_HIGH_POWER_LOCATION = 42
        """ @hide Retrieve current usage stats via {@link UsageStatsManager}. """
        OP_GET_USAGE_STATS = 43
        """ @hide """
        OP_MUTE_MICROPHONE = 44
        """ @hide """
        OP_TOAST_WINDOW = 45
        """ @hide Capture the device's display contents and/or audio """
        OP_PROJECT_MEDIA = 46
        """ @hide Activate a VPN connection without user intervention. """
        OP_ACTIVATE_VPN = 47
        """ @hide Access the WallpaperManagerAPI to write wallpapers. """
        OP_WRITE_WALLPAPER = 48
        """ @hide Received the assist structure from an app. """
        OP_ASSIST_STRUCTURE = 49
        """ @hide Received a screenshot from assist. """
        OP_ASSIST_SCREENSHOT = 50
        """ @hide Read the phone state. """
        OP_READ_PHONE_STATE = 51
        """ @hide Add voicemail messages to the voicemail content provider. """
        OP_ADD_VOICEMAIL = 52
        """ @hide Access APIs for SIP calling over VOIP or WiFi. """
        OP_USE_SIP = 53
        """ @hide Intercept outgoing calls. """
        OP_PROCESS_OUTGOING_CALLS = 54
        """ @hide User the fingerprint API. """
        OP_USE_FINGERPRINT = 55
        """ @hide Access to body sensors such as heart rate, etc. """
        OP_BODY_SENSORS = 56
        """ @hide Read previously received cell broadcast messages. """
        OP_READ_CELL_BROADCASTS = 57
        """ @hide Inject mock location into the system. """
        OP_MOCK_LOCATION = 58
        """ @hide Read external storage. """
        OP_READ_EXTERNAL_STORAGE = 59
        """ @hide Write external storage. """
        OP_WRITE_EXTERNAL_STORAGE = 60
        """ @hide Turned on the screen. """
        OP_TURN_SCREEN_ON = 61
        """ @hide Get device accounts. """
        OP_GET_ACCOUNTS = 62
        """ @hide Control whether an application is allowed to run in the background. """
        OP_RUN_IN_BACKGROUND = 63
        """ @hide """
        _NUM_OP = 64

        code, out, err = Adb.shell(device_id, 'appops', 'set', pkg_name, str(operation), mode)
        return out + err == ''

    @classmethod
    def get_app_version(cls, device_id: str, pkg_name: str) -> str:
        code, out, err = cls.shell(device_id, 'dumpsys', 'package', pkg_name)
        if code != 0:
            raise AdbException('get app version failed:{}'.format(err))
        else:
            version_pattern: re.Pattern = re.compile(r'versionName=\S+')
            matched: re.Match = version_pattern.search(out)
            if matched is None:
                return ''
        return out[matched.span()[0] + 12: matched.span()[1]]

    @classmethod
    def kill_server(cls) -> bool:
        code, out, err = cls.exec('kill-server')
        return code == 0

    @classmethod
    def connect(cls, host: str, port: int) -> bool:
        code, out, err = cls.exec('connect', host + ':' + str(port))
        return code == 0

    @classmethod
    def set_proxy(cls, device_id: str, host: str, port: int) -> bool:
        code, out, err = cls.shell(device_id, 'settings', 'put', 'global', 'http_proxy', host + ':' + str(port))
        if code != 0:
            raise AdbException('set proxy failed:{}'.format(err))
        return True

    @classmethod
    def rm_proxy(cls, device_id: str) -> bool:
        code, out, err = cls.shell(device_id, 'settings', 'put', 'global', 'http_proxy', ':0')
        if code != 0:
            raise AdbException('rm proxy failed:{}'.format(err))
        return True

    @classmethod
    def get_process(cls, device_id: str):
        code, res1, err = Adb.su_shell(device_id, 'ps -A')
        code, res2, err = Adb.su_shell(device_id, 'ps')
        res = res1 if len(res1) > len(res2) else res2
        return PsParser.get_process(res)

    @classmethod
    def start_app(cls, device_id: str, package_name: str):
        code, out, err = cls.shell(device_id, 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER',
                                   '1')
        return 'No activities found to run, monkey aborted' not in out

    @classmethod
    def get_ifaces(cls, device_id: str) -> List[InterfaceInfo]:
        code, out, err = cls.shell(device_id, 'ifconfig')
        return Parser.parse_ifconfig(out)
