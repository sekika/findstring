#!/bin/sh
# Change to this directory
cd `echo $0 | sed -e 's/[^/]*$//'`
echo '=== test'
findstring -d .. -l 35 関
./test.py
findstring -vd ~/git/work/draft/EJSS "biological clogging"
findstring -vtbd ~/git/work/.git "origin/master"

echo '=== autopep8'
autopep8 -i --aggressive ../src/findstring/*.py

echo '=== mypy'
mypy ../src/findstring/*.py

echo '=== flake8'
flake8 --ignore=E501,F401 ../src/findstring/*.py
