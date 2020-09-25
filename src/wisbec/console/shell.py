# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : shell.py
# Time       ：2020/8/19 15:15
# Author     ：Rodney Cheung
"""
import os
import subprocess
from typing import AnyStr

from wisbec import path


def __decode(content):
    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        return content.decode('gb2312')


def exec_cmd(cmd, cwd=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False) -> (int, AnyStr, AnyStr):
    try:
        subp = subprocess.Popen(cmd, shell=shell, stdout=stdout, stderr=stderr, cwd=cwd)
    except Exception as e:
        print('exec cmd Exception: ' + str(e))
        return None, None, None
    out, err = subp.communicate()
    normal = None
    error = None
    if out is not None:
        normal = __decode(out)
    if err is not None:
        error = __decode(err)
    return subp.returncode, normal, error


def get_current_shell():
    current_shell = os.environ['SHELL']
    return current_shell.split('/')[-1]


def write_env(target_path):
    sh = get_current_shell()
    if sh == 'zsh':
        sh_rc_file = os.path.join(path.home_dir(), '.zshrc')
    else:
        sh_rc_file = os.path.join(path.home_dir(), '.bashrc')
    cmd = 'export PATH=$PATH:{}'.format(target_path)
    with open(sh_rc_file, 'a+') as f:
        f.write('\n')
        f.write(cmd)
