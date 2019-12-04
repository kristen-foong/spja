#!/bin/bash

git clone --recursive https://github.com/Fredrik00/pyyolo
cd pyyolo || exit
make -f Makefile_CPU -j
python setup.py build
pip install -e .
