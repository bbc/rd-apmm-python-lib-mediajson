PYTHON=`which python3`
PY2DSC=`which py2dsc`

topdir := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
topbuilddir := $(realpath .)

DESTDIR=/
PROJECT=$(shell python $(topdir)/setup.py --name)
VERSION=$(shell python $(topdir)/setup.py --version)
MODNAME=$(PROJECT)

# The rules for names and versions in python and deb are different
# and not entirely compatible. As such py2dsc will automatically convert
# your package name into a suitable deb name and version number, and this
# code replicates that.
DEBNAME=$(shell echo $(MODNAME) | tr '[:upper:]_' '[:lower:]-')
DEBVERSION=$(shell echo $(VERSION) | sed 's/\.dev/~dev/')

DEBIANDIR=$(topbuilddir)/deb_dist/$(DEBNAME)-$(DEBVERSION)/debian
DEBIANOVERRIDES=$(patsubst $(topdir)/debian/%,$(DEBIANDIR)/%,$(wildcard $(topdir)/debian/*))

TOX_WORK_DIR?=$(topbuilddir)
TOXDIR=$(TOX_WORK_DIR)/$(MODNAME)/.tox/
TOXENV?=py310
TOX_ACTIVATE=$(TOXDIR)/$(TOXENV)/bin/activate

all:
	@echo "$(PROJECT)-$(VERSION)"
	@echo "make source  - Create source package"
	@echo "make install - Install on local system (only during development)"
	@echo "make clean   - Get rid of scratch and byte files"
	@echo "make test    - Test using tox and nose2"
	@echo "make deb     - Create deb package"
	@echo "make dsc     - Create debian source package"
	@echo "make wheel   - Create whl package"
	@echo "make egg     - Create egg package"

$(topbuilddir)/dist:
	mkdir -p $@

source: $(topbuilddir)/dist
	$(PYTHON) $(topdir)/setup.py sdist $(COMPILE) --dist-dir=$(topbuilddir)/dist

$(topbuilddir)/dist/$(MODNAME)-$(VERSION).tar.gz: source

install:
	$(PYTHON) $(topdir)/setup.py install --root $(DESTDIR) $(COMPILE)

clean:
	$(PYTHON) $(topdir)/setup.py clean || true
	rm -rf $(TOXDIR)
	rm -rf $(topbuilddir)/build/ MANIFEST
	rm -rf $(topbuilddir)/dist
	rm -rf $(topbuilddir)/deb_dist
	rm -rf $(topbuilddir)/*.egg-info
	find $(topdir) -name '*.pyc' -delete
	find $(topdir) -name '*.py,cover' -delete

test:
	tox -c tox.ini -e $(TOXENV)

testenv: $(TOX_ACTIVATE)

$(TOX_ACTIVATE): tox.ini setup.py
	tox -r -c tox.ini -e $(TOXENV) --notest

lint: $(TOX_ACTIVATE)
	. $(TOX_ACTIVATE) && python -m flake8 $(MODNAME) tests

mypy: $(TOX_ACTIVATE)
	. $(TOX_ACTIVATE) && python -m mypy -p $(MODNAME)

deb_dist: $(topbuilddir)/dist/$(MODNAME)-$(VERSION).tar.gz
	$(PY2DSC) --with-python2=false --with-python3=true $(topbuilddir)/dist/$(MODNAME)-$(VERSION).tar.gz

$(DEBIANDIR)/%: $(topdir)/debian/% deb_dist
	cp $< $@

dsc: deb_dist $(DEBIANOVERRIDES)
	cp $(topbuilddir)/deb_dist/$(DEBNAME)_$(DEBVERSION)-1.dsc $(topbuilddir)/dist

deb: source deb_dist $(DEBIANOVERRIDES)
	cd $(DEBIANDIR)/..;debuild -uc -us
	cp $(topbuilddir)/deb_dist/python*$(DEBNAME)_$(DEBVERSION)-1*.deb $(topbuilddir)/dist

wheel:
	$(PYTHON) $(topdir)/setup.py bdist_wheel

egg:
	$(PYTHON) $(topdir)/setup.py bdist_egg

.PHONY: test clean install source deb dsc wheel egg all docs
