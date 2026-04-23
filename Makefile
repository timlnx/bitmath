########################################################

# Makefile for bitmath
#
# useful targets:
#   make build ---------------- build sdist + wheel (output in dist/)
#   make pypitest ------------- upload to TestPyPI (requires: pip install twine)
#   make pypi ----------------- upload to PyPI     (requires: pip install twine)
#   make rpm  ----------------- produce RPMs
#   make docs ----------------- rebuild the docs
#   make ci   ----------------- run full test suite in virtualenv

########################################################

# > VARIABLE = value
#
# Normal setting of a variable - values within it are recursively
# expanded when the variable is USED, not when it's declared.
#
# > VARIABLE := value
#
# Setting of a variable with simple expansion of the values inside -
# values within it are expanded at DECLARATION time.

########################################################


NAME := bitmath
PKGNAME := python-$(NAME)

# VERSION file provides one place to update the software version.
VERSION := $(shell cat VERSION)
RPMRELEASE := 1

RPMSPECDIR := .
RPMSPEC := $(RPMSPECDIR)/$(PKGNAME).spec

# This doesn't evaluate until it's called. The -D argument is the
# directory of the target file ($@), kinda like `dirname`.
ASCII2MAN = a2x -D $(dir $@) -d manpage -f manpage $<
ASCII2HTMLMAN = a2x -D docs/html/man/ -d manpage -f xhtml
MANPAGES := bitmath.1

######################################################################
# Begin make targets
######################################################################

# Documentation. YAY!!!!
DOCSVENV := bitmath2

docs-venv:
	@if [ ! -d "$(DOCSVENV)" ]; then \
		echo "Creating docs virtualenv '$(DOCSVENV)' with Python 3.12..."; \
		python3.12 -m venv $(DOCSVENV); \
	fi
	. $(DOCSVENV)/bin/activate && pip install -q -r doc-requirements.txt

docs: docs-venv $(MANPAGES) docsite/source/index.rst
	. $(DOCSVENV)/bin/activate && cd docsite && make html

# Add examples to the RTD docs by taking it from the README
docsite/source/index.rst: docsite/source/index.rst.in README.rst VERSION
	@echo "#############################################"
	@echo "# Building $@ Now"
	@echo "#############################################"
	awk 'BEGIN{P=0} /^Examples/ { P=1} { if (P == 1) print $$0 }' README.rst | cat $< - > $@

# Regenerate %.1.asciidoc if %.1.asciidoc.in has been modified more
# recently than %.1.asciidoc.
%.1.asciidoc: %.1.asciidoc.in VERSION
	sed "s/%VERSION%/$(VERSION)/" $< > $@

# Regenerate %.1 if %.1.asciidoc or VERSION has been modified more
# recently than %.1. (Implicitly runs the %.1.asciidoc recipe)
%.1: %.1.asciidoc
	@echo "#############################################"
	@echo "# Building $@ NOW"
	@echo "#############################################"
	$(ASCII2MAN)

viewdocs: docs
	@if [ "$$(uname)" = "Darwin" ]; then \
		open docsite/build/html/index.html; \
	elif echo "$$(uname)" | grep -qi "mingw\|cygwin\|msys"; then \
		start docsite/build/html/index.html; \
	else \
		xdg-open docsite/build/html/index.html; \
	fi

viewcover: ci-unittests
	@if [ "$$(uname)" = "Darwin" ]; then \
		open htmlcov/index.html; \
	else \
		xdg-open htmlcov/index.html; \
	fi

build: clean
	@echo "#############################################"
	@echo "# Building sdist + wheel"
	@echo "#############################################"
	. $(NAME)env3/bin/activate && python -m build

pypi: build
	@echo "#############################################"
	@echo "# Uploading to PyPI"
	@echo "#############################################"
	. $(NAME)env3/bin/activate && pip install twine && twine upload dist/*

pypitest: build
	@echo "#############################################"
	@echo "# Uploading to TestPyPI"
	@echo "#############################################"
	. $(NAME)env3/bin/activate && pip install twine && twine upload --repository testpypi dist/*

# usage example: make tag TAG=1.1.0-1
tag:
	git tag -s -m $(TAG) $(TAG)

clean:
	@find . -type f -regex ".*\.py[co]$$" -delete
	@find . -type f \( -name "*~" -or -name "#*" \) -delete
	@rm -fR build cover dist rpm-build MANIFEST htmlcov .coverage bitmathenv3 docsite/build/html/ docsite/build/doctrees/ bitmath.egg-info

uniquetestnames:
	@echo "#############################################"
	@echo "# Running Unique TestCase checker"
	@echo "#############################################"
	./tests/test_unique_testcase_names.sh

install:
	pip install .
	mkdir -p /usr/share/man/man1/
	gzip -9 -c bitmath.1 > /usr/share/man/man1/bitmath.1.gz

sdist: clean virtualenv
	@echo "#############################################"
	@echo "# Creating SDIST"
	@echo "#############################################"
	. $(NAME)env3/bin/activate && pip install build && python -m build --sdist

rpmcommon: sdist
	@echo "#############################################"
	@echo "# Building (S)RPM Now"
	@echo "#############################################"
	@mkdir -p rpm-build
	@cp dist/$(NAME)-$(VERSION).tar.gz rpm-build/$(VERSION).tar.gz

srpm: rpmcommon
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir $(RPMSPECDIR)" \
	--define "_sourcedir %{_topdir}" \
	--define "_pkgversion $(VERSION)" \
	--define "_pkgrelease $(RPMRELEASE)" \
	-bs $(RPMSPEC)
	@echo "#############################################"
	@echo "$(PKGNAME) SRPM is built:"
	@find rpm-build -maxdepth 2 -name '$(PKGNAME)*src.rpm' | awk '{print "    " $$1}'
	@echo "#############################################"

rpm: rpmcommon
	rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir $(RPMSPECDIR)" \
	--define "_sourcedir %{_topdir}" \
	--define "_pkgversion $(VERSION)" \
	--define "_pkgrelease $(RPMRELEASE)" \
	-ba $(RPMSPEC)
	@echo "#############################################"
	@echo "$(PKGNAME) RPMs are built:"
	@find rpm-build -maxdepth 2 -name '$(PKGNAME)*.rpm' | awk '{print "    " $$1}'
	@echo "#############################################"

virtualenv:
	@echo ""
	@echo "#############################################"
	@echo "# Creating a virtualenv"
	@echo "#############################################"
	@if [ ! -d "$(NAME)env3" ]; then \
		python3 -m venv $(NAME)env3; \
	fi
	. $(NAME)env3/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt

ci-unittests: virtualenv
	@echo ""
	@echo "#############################################"
	@echo "# Running Unit Tests in virtualenv"
	@echo "# Using python: $(shell ./$(NAME)env3/bin/python --version 2>&1)"
	@echo "#############################################"
	. $(NAME)env3/bin/activate && pytest -v --cov=bitmath --cov-report term-missing --cov-report term:skip-covered --cov-report xml:coverage.xml --cov-report html:htmlcov tests

ci-list-deps:
	@echo ""
	@echo "#############################################"
	@echo "# Listing all pip deps"
	@echo "#############################################"
	. $(NAME)env3/bin/activate && pip freeze

ci-pycodestyle:
	@echo ""
	@echo "#############################################"
	@echo "# Running PEP8 Compliance Tests in virtualenv"
	@echo "#############################################"
	. $(NAME)env3/bin/activate && pycodestyle -v --ignore=E501,E722 bitmath/__init__.py tests/*.py

ci-flake8:
	@echo ""
	@echo "#################################################"
	@echo "# Running Flake8 Compliance Tests in virtualenv"
	@echo "#################################################"
	. $(NAME)env3/bin/activate && flake8 --select=F bitmath/__init__.py tests/*.py

ci: clean uniquetestnames virtualenv ci-list-deps ci-pycodestyle ci-flake8 ci-unittests
	:
