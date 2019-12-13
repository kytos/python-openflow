build: clean prepare
	python3.6 setup.py sdist
	ls -l dist/

clean:
	rm -rf build/ dist/ *.egg-info/

prepare:
	pip3.6 install --upgrade pip setuptools wheel twine

testupload: build
	twine upload -r pypitest dist/*

upload: build
	twine upload dist/*
