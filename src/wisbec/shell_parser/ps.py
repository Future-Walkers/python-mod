# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : ps.py
# Time       ：12/11/20 11:16
# Author     ：Rodney Cheung
"""
import string
from typing import List

from wisbec.shell_parser.model.ps_info import PsInfo


class PsParser:
    @classmethod
    def __parse_ps_result_line(cls, line: str) -> list:
        res = list()
        word = ''
        last_word_index = 0
        for i in range(len(line)):
            if line[i] in string.whitespace:
                words_start = False
            else:
                if len(res) == 8:
                    last_word_index = i
                    break
                words_start = True
            if words_start:
                word += line[i]
            else:
                if word != '':
                    res.append(word)
                    word = ''
        res.append(line[last_word_index:])
        return res

    @classmethod
    def get_process(cls, ps_result: str) -> List[PsInfo]:
        process_list = list()
        for line in ps_result.strip().replace('\r\n', '\n').split('\n')[1:]:
            s = cls.__parse_ps_result_line(line)
            if len(s) == 9:
                process_list.append(PsInfo(user=s[0],
                                           pid=int(s[1]),
                                           ppid=int(s[2]),
                                           vsz=s[3],
                                           rss=s[4],
                                           wchan=s[5],
                                           addr=s[6],
                                           status=s[7],
                                           name=s[8]))
        return process_list
