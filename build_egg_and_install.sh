#!/bin/zsh

if [ -d build ]; then
  echo "$1" | sudo -S rm -dr build
fi
if [ -d dist ]; then
  sudo rm -dr dist
fi
if [ -d src/wisbec.egg-info ]; then
  sudo rm -dr src/wisbec.egg-info
fi
sudo python3 setup.py bdist_egg
sudo easy_install dist/*.egg
