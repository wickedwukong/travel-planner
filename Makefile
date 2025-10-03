ifeq ($(OS),Windows_NT)
	VENV_BIN = .venv\Scripts
else
	VENV_BIN = .venv/bin
endif

.PHONY: test format lint typecheck run fix

$(VENV_BIN):
	python -m venv .venv

.PHONY: deps
deps: $(VENV_BIN)
	${VENV_BIN}/python -m pip install -e .[dev]

test: $(VENV_BIN)
	pytest -vv tests/

format: $(VENV_BIN)
	${VENV_BIN}/ruff format .

lint: $(VENV_BIN)
	${VENV_BIN}/ruff check . --fix

•PHONY: typecheck
typecheck:
	${VENV_BIN}/mypy ./src

## run just.typechecker
run: $(VENV_BIN)
	${VENV_BIN}/python src/journal/repository/migrate_db.py
	${VENV_BIN}/uvicorn journal.main:prod_app --reload --factory
