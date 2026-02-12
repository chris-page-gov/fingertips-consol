PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin

.PHONY: setup test lint dev clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e .[dev]

test:
	$(BIN)/pytest -q

lint:
	$(BIN)/ruff check src tests
	$(BIN)/ruff format --check src tests

dev:
	$(BIN)/python -m fingertips_consol.cli --help

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache
