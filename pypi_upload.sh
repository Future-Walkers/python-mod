#!/bin/sh

source clean_build.sh
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
