##################################################
# Variables 
##################################################

PYTHON=python3
INSTALL_OPTS = `$(PYTHON) -c "import sys; print('' if hasattr(sys, 'real_prefix') else '--user')"`

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
		tmp/

##################################################
# Install 
##################################################

install:
	pip install -e

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
		history = open('CHANGES.md').read(); \
		pyproject = open('pyproject.toml').read(); \
		setup = open('setup.py').read(); \
		assert ver in history, '%r not in CHANGES.md' % ver; \
		assert ver in pyproject, '%r not in pyproject.toml' % ver; \
		assert ver in setup, '%r not in setup.py' % ver; \
		"
	$(PYTHON) -m build

release:
	${MAKE} pre-release
	twine check dist/*
	$(PYTHON) -m twine upload dist/*