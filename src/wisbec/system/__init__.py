import sys

current_os = sys.platform

WINDOWS = 'win32'
MAC_OS = 'darwin'
LINUX = 'linux'


def get_newline_ch() -> str:
    if current_os == WINDOWS:
        return '\r\n'
    else:
        return '\n'


def is_windows() -> bool:
    return current_os == WINDOWS


def is_linux() -> bool:
    return current_os == LINUX


def is_mac_os() -> bool:
    return current_os == MAC_OS
