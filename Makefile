##################################################
# Variables 
##################################################

PYTHON=python3
INSTALL_OPTS = `$(PYTHON) -c "import sys; print('' if hasattr(sys, 'real_prefix') else '--user')"`

all : test

##################################################
# Install 
##################################################

install:
	$(PYTHON) -c "import setuptools"
	$(PYTHON) setup.py develop $(INSTALL_OPTS)

uninstall:  ## Uninstall this package.
	cd ..; $(PYTHON) -m pip uninstall -y -v mftpclient || true
	$(PYTHON) scripts/internal/purge_installation.py

##################################################
# Testing 
##################################################

test:
	$(PYTHON) mftpclient/test/test_client.py -v