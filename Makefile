ifeq ($(OS),Windows_NT)
	VENV_BIN = .venv\Scripts
else
	VENV_BIN = .venv/bin
endif

.PHONY: test format lint typecheck run fix

$(VENV_BIN):
	python -m venv .venv

#.PHONY: deps
#deps: $(VENV_BIN)
#      ${VENV_BIN}/python -m pip install -e .[dev]

test: $(VENV_BIN)
	pytest

format: $(VENV_BIN)
	ruff format .

lint: $(VENV_BIN)
	ruff check . --fix

typecheck: $(VENV_BIN)
	mypy src/

run: $(VENV_BIN)
	uvicorn src.main:app --reload
