PYTHON ?= python3
VENV ?= .venv
BIN := $(VENV)/bin

.PHONY: setup test lint dev tdd clean

setup:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e .[dev]

test:
	$(BIN)/pytest -q

tdd:
	$(BIN)/pytest -q --maxfail=1

lint:
	$(BIN)/ruff check src tests
	$(BIN)/ruff format --check src tests

dev:
	$(BIN)/python -m fingertips_consol.cli --help

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache
