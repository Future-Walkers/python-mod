# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : shell.py
# Time       ：2020/8/19 15:15
# Author     ：Rodney Cheung
"""
import subprocess


def exec_cmd(cmd, cwd=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False):
    try:
        subp = subprocess.Popen(cmd, shell=shell, stdout=stdout, stderr=stderr, cwd=cwd)
    except Exception as e:
        print('exec cmd Exception: ' + str(e))
        return None, None, None
    out, err = subp.communicate()
    normal = None
    error = None
    if out is not None:
        normal = out.decode(errors='ignore')
    if err is not None:
        error = err.decode()
    return subp.returncode, normal, error
