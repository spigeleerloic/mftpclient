##################################################
# Variables 
##################################################

PYTHON=python3

all : test

clean:
	rm -rf `find . -type d -name __pycache__ \
		-o -type f -name \*.bak \
		-o -type f -name \*.orig \
		-o -type f -name \*.pyc \
		-o -type f -name \*.pyd \
		-o -type f -name \*.pyo \
		-o -type f -name \*.rej \
		-o -type f -name \*.so`
	
	rm -rf \
		*.core \
		*.egg-info \
		.coverage \
		.tox \
		pyftpd-tmp-\* \
		build/ \
		dist/ \
		docs/_build/ \
		.pytest_cache/ \
		tmp/

##################################################
# Install 
##################################################

install:
	$(PYTHON) -m pip install -e . --user

uninstall:  ## Uninstall this package.
	cd ..; $(PYTHON) -m pip uninstall -y -v mftpclient || true
	$(PYTHON) scripts/internal/purge_installation.py

##################################################
# Testing 
##################################################

test:
	$(PYTHON) mftpclient/test/test_client.py -v

##################################################
# Distribution 
##################################################

pre-release:
	${MAKE} clean
	python3 -m pip install --upgrade twine
	$(PYTHON) -c \
		"from mftpclient import __ver__ as ver; \
		changes = open('CHANGES.md').read(); \
		pyproject = open('pyproject.toml').read(); \
		assert ver in changes, '%r not in CHANGES.md' % ver; \
		assert ver in pyproject, '%r not in pyproject.toml' % ver; \
		"
	$(PYTHON) -m build

release:
	${MAKE} pre-release
	twine check dist/*
	$(PYTHON) -m twine upload dist/*