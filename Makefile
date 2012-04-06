PYTHON = python
export PROTOC = protoc

EXPORT_DIR = svn_export
APP = $(shell cat NAME)
COPYRIGHT_OWNER = CRS4
NOTICE_TEMPLATE = notice_template.txt
COPYRIGHTER = copyrighter -p $(APP) -n $(NOTICE_TEMPLATE) $(COPYRIGHT_OWNER)
# install copyrighter >=0.4.0 from ac-dc/tools/copyrighter

GENERATED_FILES = AUTHORS MANIFEST README bl/core/version.py

PROTOBUF_SRC_DIRS := bl/core/messages bl/core/gt/messages


.PHONY: all build build_proto build_py install install_py install_user install_user_py docs docs_py docs_put docs_view dist clean distclean

all: build

build: build_proto
	$(PYTHON) setup.py build

build_proto:
	for d in $(PROTOBUF_SRC_DIRS); do make -e -C $${d}; done

build_py: build_proto
	$(PYTHON) setup.py build_py

install: build
	$(PYTHON) setup.py install --skip-build

install_py: build_py
	$(PYTHON) setup.py install --skip-build

install_user: build
	$(PYTHON) setup.py install --skip-build --user

install_user_py: build_py
	$(PYTHON) setup.py install --skip-build --user

docs: install_user
	make -C docs html

docs_py: install_user_py
	make -C docs html

docs_put: docs
	rsync -avz --delete -e ssh docs/_build/html/ ${USER},biodoop@web.sourceforge.net:/home/project-web/biodoop/htdocs/core/

docs_view: docs
	yelp docs/_build/html/index.html &

dist: docs
	rm -rf $(EXPORT_DIR) && svn export . $(EXPORT_DIR)
	$(COPYRIGHTER) -r $(EXPORT_DIR)
	rm -rf $(EXPORT_DIR)/docs/*
	mv docs/_build/html $(EXPORT_DIR)/docs/
	cd $(EXPORT_DIR) && $(PYTHON) setup.py sdist -k

clean:
	rm -rf build
	rm -f $(GENERATED_FILES)
	for d in $(PROTOBUF_SRC_DIRS); do make -C $${d} clean; done
	cd test && rm -fv *.{out,err,log}
	find . -regex '.*\(\.pyc\|\.pyo\|~\|\.so\)' -exec rm -fv {} \;
	rm -f test/*.{out,err,log}
	make -C docs clean
	make -C integration_test clean

distclean: clean
	rm -rf $(EXPORT_DIR) dist
