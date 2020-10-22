default:
	python setup.py sdist bdist_wheel --universal

clean:
	rm -rf __pycache__ *.py[oc] build *.egg-info dist MANIFEST

test:
	python2.5 test.py
	python2.7 test.py
	python3.6 test.py
