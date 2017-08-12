PYTHON=./env/bin/python3
SRC=pma_api/
TEST=test/

.PHONY: lint tags ltags test all lint_all codestyle docstyle server serve lint_src lint_test doctest doc docs code linters_all code_src code_test doc_src doc_test shell initdb

# Batched Commands
all: linters_all test_all
lint: lint_src code_src doc_src
linters_all: doc code lint_all

# Pylint Only
lint_all: lint_src lint_test
lint_src:
	${PYTHON} -m pylint --output-format=colorized --reports=n ${SRC}
lint_test:
	${PYTHON} -m pylint --output-format=colorized --reports=n ${TEST}

# PyCodeStyle Only
codestyle: codestyle_src codestyle_test
code_src: codestyle_src
code_test: codestyle_test
code: codestyle
codestyle_src:
	${PYTHON} -m pycodestyle ${SRC}
codestyle_test:
	${PYTHON} -m pycodestyle ${TEST}

# PyDocStyle Only
docstyle: docstyle_src docstyle_test
doc_src: docstyle_src
doc_test: docstyle_test
doc: docstyle
docs: docstyle
docstyle_src:
	${PYTHON} -m pydocstyle ${SRC}
docstyle_test:
	${PYTHON} -m pydocstyle ${TEST}

# Text Editor Commands
tags:
	ctags -R --python-kinds=-i .
ltags:
	ctags -R --python-kinds=-i ./${SRC}

# Testing
test_all: unittest doctest
unittest: test
test:
	${PYTHON} -m unittest discover -v
doctest:
	${PYTHON} -m test --doctests-only

# Server Commands
serve:server
server:
	${PYTHON} manage.py runserver

shell:
	${PYTHON} manage.py shell

initdb:
	${PYTHON} manage.py initdb
