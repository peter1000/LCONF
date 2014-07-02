#!/bin/bash

PYTHON=/usr/bin/env python3

.PHONY: help cleanall clean tests tests_cover build dist install docs info check_setup pypiupload pypiregister checksoftware


help:
	@echo 'Please use: `make <target>` where <target> is one of'
	@echo '  cleanall       to clean inclusive generated documentation: docs.'
	@echo '  clean          to clean but keep any generated documentation: docs.'
	@echo '  tests          to test the project'
	@echo '  tests_cover    to test the project and produce a coverage report: dir cover'
	@echo '  build          to build the project'
	@echo '  install        to install the package'
	@echo '  dist           to build a source distribution tar file'
	@echo '  docs           to build the docs for the project'
	@echo '  info           to build the general info'
	@echo '  check_setup    checks the setup.py file'   
	@echo '  pypiupload     builds a release and uploads it to pypi'
	@echo '  pypiregister   register/submit your distribution’s meta-data to the pypi index'
	@echo '  checksoftware  checks for the projects required/installed software'

cleanall: clean
	@rm -rf build dist cover
	@rm -rf docs/LCONF-DOCUMENTATION
	@rm -rf info/GENERAL-INFO

clean: 
	@find . -iname '__pycache__' |xargs rm -rf
	@find . -iname '*.egg-info' |xargs rm -rf
	@find . -iname '*.pyc' |xargs rm -rf
	@rm -rf MANIFEST MANIFEST.in .coverage

tests: clean
	${PYTHON} setup.py nosetests
	$(MAKE) clean
	@echo -e '\n=== finished tests'

tests_cover: clean
	@rm -rf cover
	${PYTHON} setup.py nosetests --cover-branches --with-coverage --cover-html --cover-erase --cover-package=LCONF
	$(MAKE) clean
	@echo -e '\n=== finished tests_cover'
   
build: clean 
	rm -rf build
	${PYTHON} setup.py build
	$(MAKE) clean
	@echo -e '\n=== finished build'

dist: cleanall
	${PYTHON} setup.py sdist 
	$(MAKE) clean
	@echo -e '\n=== finished dist'

install: clean 
	rm -rf build
	${PYTHON} setup.py install
	$(MAKE) clean
	@echo -e '\n=== finished install'

docs: 
	rm -rf docs/LCONF-DOCUMENTATION
	sphinx-apidoc --force --output-dir=docs/source LCONF
	cd docs && make html
	cd ..
	$(MAKE) clean
	@echo -e '\n=== finished docs'

info: 
	rm -rf info/GENERAL-INFO
	cd info && make html
	cd ..
	$(MAKE) clean
	@echo -e '\n=== finished info'
   
check_setup: clean
	${PYTHON} setup.py check
	$(MAKE) clean
	@echo -e '\n=== finished check_setup'
   
pypiupload: cleanall
	${PYTHON} setup.py check
	${PYTHON} setup.py sdist upload
	$(MAKE) clean
	@echo -e '\n=== finished pypiupload'

pypiregister: cleanall
	${PYTHON} setup.py check
	${PYTHON} setup.py register
	$(MAKE) clean
	@echo -e '\n=== finished pypiregister'

checksoftware: clean
	${PYTHON} LCONF/RequiredSoftware.py
	@echo -e '\n=== finished checksoftware'
