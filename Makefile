
.PHONY: test format lint typecheck run fix


.PHONY: deps
deps:
	python -m pip install -e .[dev]

test:
	pytest -vv tests/

format:
	ruff format .

lint:
	ruff check . --fix

•PHONY: typecheck
typecheck:
	mypy ./src

## run just.typechecker
run:
	python src/journal/repository/migrate_db.py
	uvicorn journal.main:prod_app --reload --factory
