#!/bin/sh

if [ -d build ]; then
  rm -dr build
fi
if [ -d dist ]; then
  rm -dr dist
fi
if [ -d src/wisbec.egg-info ]; then
  rm -dr src/wisbec.egg-info
fi
