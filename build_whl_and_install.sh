#!/bin/sh

source clean_build.sh
python3 setup.py bdist_wheel
sudo pip3 install dist/*.whl
