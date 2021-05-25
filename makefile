.PHONY: build

build:
	python /data/home/lixiangyong/project/python2so/setup.py build_ext

clean:
	find . -type f -name "*.c" -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name __pycache__ -delete
