#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 8/18/20 1:56 PM
@Author  : Rodney Cheung
@File    : log.py
"""

import io
import logging
import os
import time
import traceback

from colorlog import ColoredFormatter

from wisbec.file import filesystem


class MyLogger(logging.Logger):
    def findCaller(self, stack_info=False, stack_level=1):
        n_frames_upper = 2
        f = logging.currentframe()
        for _ in range(n_frames_upper):  # <-- correct frame
            if f is not None:
                f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv


class Log:
    logging.setLoggerClass(MyLogger)
    console_logger = None
    console_handler = None
    file_log_formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s %(funcName)s %(lineno)d: %(message)s")
    console_log_formatter = ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(asctime)s %(funcName)s %(lineno)d : %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%')
    is_log_to_file = False
    is_log_to_console = True
    file_loggers = {}

    log_dir = None
    log_debug_path = None
    log_info_path = None
    log_err_path = None
    log_warning_path = None
    log_critical_path = None
    log_path_dict = {}

    file_handler_created_flag = {
        logging.DEBUG: False,
        logging.WARNING: False,
        logging.ERROR: False,
        logging.CRITICAL: False,
        logging.INFO: False
    }

    @classmethod
    def __init_log_dir(cls, log_dir):
        filesystem.create_directories(log_dir)
        cls.log_dir = log_dir
        cls.log_debug_path = os.path.join(log_dir, "debug.log")
        cls.log_info_path = os.path.join(log_dir, "info.log")
        cls.log_err_path = os.path.join(log_dir, "error.log")
        cls.log_warning_path = os.path.join(log_dir, "warning.log")
        cls.log_critical_path = os.path.join(log_dir, "critical.log")
        cls.log_path_dict = {
            logging.DEBUG: cls.log_debug_path,
            logging.WARNING: cls.log_warning_path,
            logging.ERROR: cls.log_err_path,
            logging.CRITICAL: cls.log_critical_path,
            logging.INFO: cls.log_info_path
        }

    @classmethod
    def __init_log_handler(
            cls,
            is_log_to_file,
            is_log_to_console,
            console_log_name,
            console_log_level):
        cls.is_log_to_console = is_log_to_console
        if is_log_to_console:
            cls.console_handler = logging.StreamHandler()
            cls.console_handler.setFormatter(cls.console_log_formatter)
            cls.console_handler.setLevel(console_log_level)
            cls.console_logger = logging.getLogger(console_log_name)
            cls.console_logger.setLevel(logging.DEBUG)
            cls.console_logger.addHandler(cls.console_handler)
        cls.is_log_to_file = is_log_to_file

    @classmethod
    def init_logger(cls,
                    log_dir=os.path.join(os.getcwd(),
                                         "runtime", "log",
                                         time.strftime("%Y-%m-%d %H:%M:%S",
                                                       time.localtime())),
                    is_log_to_file=True,
                    is_log_to_console=True,
                    console_log_name='console_log',
                    console_log_level=logging.DEBUG,
                    ):
        """
        init logger
        Args:
            log_dir: log save path
            is_log_to_file:is output log to file
            is_log_to_console:is output log to console
            console_log_name: logger name
            console_log_level:minimum log level,if not set,all level logs will be recorded
        Returns:
            None
        """
        cls.__init_log_dir(log_dir)
        cls.__init_log_handler(
            is_log_to_file,
            is_log_to_console,
            console_log_name,
            console_log_level)

    @classmethod
    def __position_format(cls, msg: str, *args, **kwargs) -> str:
        # position_str = '{}'
        # position_str_list = list()
        # arg_len = len(args)
        # while arg_len > 0:
        #     position_str_list.append(position_str)
        #     arg_len -= 1
        # return "".join(position_str_list).format(*args)
        return msg.format(*args, **kwargs)

    @classmethod
    def debug(cls, msg: str, *args, **kwargs):
        data = cls.__position_format(msg, *args, **kwargs)
        if cls.is_log_to_console:
            cls.console_logger.debug(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.DEBUG]:
                cls.add_file_handler(cls.log_debug_path, logging.DEBUG)
                cls.file_handler_created_flag[logging.DEBUG] = True
            cls.file_loggers[logging.DEBUG].debug(data)

    @classmethod
    def info(cls, msg: str, *args, **kwargs):
        data = cls.__position_format(msg, *args, **kwargs)
        if cls.is_log_to_console:
            cls.console_logger.info(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.INFO]:
                cls.add_file_handler(cls.log_info_path, logging.INFO)
                cls.file_handler_created_flag[logging.INFO] = True
            cls.file_loggers[logging.INFO].info(data)

    @classmethod
    def warning(cls, msg: str, *args, **kwargs):
        data = cls.__position_format(msg, *args, **kwargs)
        if cls.is_log_to_console:
            cls.console_logger.warning(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.WARNING]:
                cls.add_file_handler(cls.log_warning_path, logging.WARNING)
                cls.file_handler_created_flag[logging.WARNING] = True
            cls.file_loggers[logging.WARNING].warning(data)

    @classmethod
    def error(cls, msg: str, *args, **kwargs):
        data = cls.__position_format(msg, *args, **kwargs)
        if cls.is_log_to_console:
            cls.console_logger.error(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.ERROR]:
                cls.add_file_handler(cls.log_err_path, logging.ERROR)
                cls.file_handler_created_flag[logging.ERROR] = True
            cls.file_loggers[logging.ERROR].error(data)

    @classmethod
    def critical(cls, msg: str, *args, **kwargs):
        data = cls.__position_format(msg, *args, **kwargs)
        if cls.is_log_to_console:
            cls.console_logger.critical(data)
        if cls.is_log_to_file:
            if not cls.file_handler_created_flag[logging.CRITICAL]:
                cls.add_file_handler(cls.log_critical_path, logging.CRITICAL)
                cls.file_handler_created_flag[logging.CRITICAL] = True
            cls.file_loggers[logging.CRITICAL].critical(data)

    @classmethod
    def add_file_handler(cls, log_file, log_level):
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(cls.file_log_formatter)
        file_handler.setLevel(log_level)
        file_logger = logging.getLogger(str(log_level))
        file_logger.setLevel(logging.DEBUG)
        file_logger.addHandler(file_handler)
        cls.file_loggers.update({log_level: file_logger})

    @classmethod
    def set_console_log_level(cls, log_level):
        cls.console_handler.setLevel(log_level)

    @classmethod
    def close(cls):
        cls.clear_file_handler()

    @classmethod
    def clear_file_handler(cls):
        for file_logger in cls.file_loggers:
            cls.file_loggers[file_logger].handlers[0].close()
            cls.file_handler_created_flag[file_logger] = False
        cls.file_loggers.clear()
