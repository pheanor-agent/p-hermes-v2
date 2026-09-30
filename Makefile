PYTHON ?= python3
export PYTHONDONTWRITEBYTECODE := 1

.PHONY: help test example

help:
	@printf '%s\n' 'make test' 'make example NAME=workflow-contract-check|image-pipeline|knowledge-context-check'

test:
	@$(PYTHON) -m unittest discover -s examples/workflow-contract-check/tests -v
	@PYTHONPATH=preview/examples/image-pipeline/src $(PYTHON) -m unittest discover -s preview/examples/image-pipeline/tests -v
	@PYTHONPATH=examples/knowledge-context-check/src $(PYTHON) -m unittest discover -s examples/knowledge-context-check/tests -v

example:
	@if test "$(NAME)" = workflow-contract-check; then \
	  $(PYTHON) -m unittest discover -s examples/workflow-contract-check/tests -v; \
	elif test "$(NAME)" = image-pipeline; then \
	  PYTHONPATH=preview/examples/image-pipeline/src $(PYTHON) -m unittest discover -s preview/examples/image-pipeline/tests -v && \
	  PYTHONPATH=preview/examples/image-pipeline/src $(PYTHON) -m image_pipeline_demo; \
	elif test "$(NAME)" = knowledge-context-check; then \
	  PYTHONPATH=examples/knowledge-context-check/src $(PYTHON) -m unittest discover -s examples/knowledge-context-check/tests -v; \
	else echo '지원 예제: workflow-contract-check, image-pipeline, knowledge-context-check' >&2; exit 2; fi
