PYTHON ?= python3
export PYTHONDONTWRITEBYTECODE := 1

.PHONY: help test build check verify example

help:
	@printf '%s\n' 'make test' 'make build' 'make check' 'make verify' 'make example NAME=portable-worker|image-pipeline|knowledge-context-check|integration-check'

test:
	@PYTHONPATH=reference $(PYTHON) -B -m unittest discover -s tests -v
	@PYTHONPATH=examples/image-pipeline/src $(PYTHON) -B -m unittest discover -s examples/image-pipeline/tests -v
	@PYTHONPATH=examples/knowledge-context-check/src $(PYTHON) -B -m unittest discover -s examples/knowledge-context-check/tests -v
	@PYTHONPATH=examples/integration-check/src $(PYTHON) -B -m unittest discover -s examples/integration-check/tests -v

build:
	@$(PYTHON) -B tools/build_site.py

check:
	@$(PYTHON) -B tools/check_site.py

verify: test build check
	@git diff --check

example:
	@if test "$(NAME)" = portable-worker; then PYTHONPATH=reference $(PYTHON) -B -m unittest discover -s tests -v; \
	elif test "$(NAME)" = image-pipeline; then PYTHONPATH=examples/image-pipeline/src $(PYTHON) -B -m unittest discover -s examples/image-pipeline/tests -v; \
	elif test "$(NAME)" = knowledge-context-check; then PYTHONPATH=examples/knowledge-context-check/src $(PYTHON) -B -m unittest discover -s examples/knowledge-context-check/tests -v; \
	elif test "$(NAME)" = integration-check; then PYTHONPATH=examples/integration-check/src $(PYTHON) -B -m unittest discover -s examples/integration-check/tests -v; \
	else echo '지원 예제: portable-worker, image-pipeline, knowledge-context-check, integration-check' >&2; exit 2; fi
