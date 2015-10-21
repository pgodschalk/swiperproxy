streamhtmlparser.so: setup.py py-streamhtmlparser.pyx streamhtmlparser.pxd
	python setup.py build_ext 

install: streamhtmlparser.so
	python setup.py install

clean:
	rm -rf build
	rm -f py-streamhtmlparser.c
	rm -f streamhtmlparser.so

