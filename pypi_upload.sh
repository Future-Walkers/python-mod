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

echo "$1" | sudo -S python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
