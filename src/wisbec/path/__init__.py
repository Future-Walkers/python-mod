import os

from wisbec import system


def home_dir() -> str:
    current_os = system.current_os
    if current_os == 'darwin' or current_os == 'linux':
        return os.environ['HOME']
    elif current_os == 'win32':
        return os.environ['USERPROFILE']
    else:
        return ''
