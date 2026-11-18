.PHONY: run gui test lint fmt setup check
PY := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
export PYTHONPATH := src

setup:   ## a venv with the test and lint tools (GTK comes from the system)
	python3 -m venv --system-site-packages .venv
	.venv/bin/python -m pip install -q pytest ruff

run:     ## the command: make run ARGS="add buy milk"
	$(PY) -m kiwi_template $(ARGS)

gui:     ## the window, from the checkout
	$(PY) -m kiwi_template.ui

test:
	$(PY) -m pytest tests/unit -q

lint:
	.venv/bin/ruff check src tests
	.venv/bin/ruff format --check src tests

fmt:
	.venv/bin/ruff format src tests
	.venv/bin/ruff check --fix src tests

check:   ## what CI runs
	bash tools/kit-check.sh
	bash tools/check-version.sh
	bash -n install.sh scripts/*.sh tools/*.sh
	$(MAKE) test
