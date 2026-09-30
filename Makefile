PYTHON ?= python3

.PHONY: help test example

help:
	@printf '%s\n' 'make test' 'make example NAME=workflow-contract-check|image-pipeline'

test:
	@$(PYTHON) -m unittest discover -s examples/workflow-contract-check/tests -v
	@PYTHONPATH=examples/image-pipeline/src $(PYTHON) -m unittest discover -s examples/image-pipeline/tests -v

example:
	@if test "$(NAME)" = workflow-contract-check; then \
	  $(PYTHON) -m unittest discover -s examples/workflow-contract-check/tests -v; \
	elif test "$(NAME)" = image-pipeline; then \
	  PYTHONPATH=examples/image-pipeline/src $(PYTHON) -m unittest discover -s examples/image-pipeline/tests -v && \
	  PYTHONPATH=examples/image-pipeline/src $(PYTHON) -m image_pipeline_demo; \
	else echo '지원 예제: workflow-contract-check, image-pipeline' >&2; exit 2; fi
