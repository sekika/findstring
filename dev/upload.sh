#!/bin/sh
# Change to this directory
cd `echo $0 | sed -e 's/[^/]*$//'`

# test
./test.sh

# Make package
echo "Making packages."
cd ..
python3 -m build

# Token required. Check ~/.pypirc
twine upload --skip-existing dist/*

# Uninstall unsatfit
python3 -m pip uninstall findstring
echo "Upload completed. Installed version uninstalled. Wait for a while and run"
echo "python3 -m pip install findstring"
