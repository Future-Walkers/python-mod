import sys

current_os = sys.platform


def get_newline_ch() -> str:
    if current_os == 'win32':
        return '\r\n'
    else:
        return '\n'
