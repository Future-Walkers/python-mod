#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
@Author: Sphantix Hang
@Date: 2020-04-22 15:50:16
@LastEditors: Sphantix Hang
@LastEditTime: 2020-04-24 21:36:53
@FilePath: /urldownload/helper.py
'''

import os
import time
import socket
import shutil
import random
import hashlib
import datetime
import urllib.request
from constant import const
from urllib.parse import urlparse
from zipfile import ZipFile


def is_directory_exist(dir_full_path):
    return (os.path.exists(dir_full_path) and os.path.isdir(dir_full_path))


def create_directory(dir_full_path):
    if not is_directory_exist(dir_full_path):
        os.makedirs(dir_full_path)


def is_file_exist(file_full_path):
    return (os.path.exists(file_full_path) and os.path.isfile(file_full_path))


def remove(full_path):
    if not os.path.exists(full_path):
        return
    else:
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path, ignore_errors=True)


def create_file(full_path):
    if os.path.exists(full_path):
        print("{0} already existed.".format(full_path))
        return

    f = open(full_path, 'w')
    f.close()


def copy_file(src_full_path, dst_full_path):
    shutil.copy2(src_full_path, dst_full_path)


def format_time_use(time):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return ("Cost: %dh%02dm%02ds" % (h, m, s))
    elif m > 0:
        return ("Cost: %02dm%02ds" % (m, s))
    else:
        return ("Cost: %02ds" % (s))


def get_current_timestamp():
    return time.mktime(
        time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      "%Y-%m-%d %H:%M:%S"))


def check_url_access(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent',
                          const.USER_AGENT["Android"][random.randint(0, len(const.USER_AGENT["Android"])-1)])]
    try:
        opener.open(url)
        return True
    except Exception as e:
        print("Current URL[{0}] connect failed!".format(url), e)
        return False


def get_IP_from_URL(url):
    netloc = urlparse(url).netloc
    domain = netloc.split(":")[0]
    addr = socket.getaddrinfo(domain, 'http')
    return (addr[0][4][0])


def get_file_md5(file_full_path):
    if not os.path.isfile(file_full_path):
        return
    md5hash = hashlib.md5()
    with open(file_full_path, 'rb') as f:
        while True:
            b = f.read(8096)
            if not b:
                break
            md5hash.update(b)

    return md5hash.hexdigest()


def create_zip_file(output_full_path, input_dir):
    shutil.make_archive(output_full_path, 'zip', input_dir)
