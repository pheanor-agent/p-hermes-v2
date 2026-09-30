PYTHON ?= python3

.PHONY: test example

test:
	@$(PYTHON) -m unittest discover -s examples/workflow-contract-check/tests -v

example:
	@test "$(NAME)" = workflow-contract-check || (echo '지원 예제: workflow-contract-check' >&2; exit 2)
	@$(PYTHON) -m unittest discover -s examples/workflow-contract-check/tests -v
