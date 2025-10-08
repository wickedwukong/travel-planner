
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

migrate_db:
	PYTHONPATH=src python -m journal.repository.migrate_db
## run just.typechecker
run:
	PYTHONPATH=src python -m journal.repository.migrate_db
	PYTHONPATH=src uvicorn journal.main:prod_app --reload --factory
