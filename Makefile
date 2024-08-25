all:

install:
	- python3 -m pip uninstall findstring
	python3 -m pip install -e .

test:
	@ cd dev; ./test.sh

upload:
	@ cd dev; ./upload.sh
