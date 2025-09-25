.PHONY: test format lint typecheck run fix

test:
	pytest

format:
	ruff format .

lint:
	ruff check . --fix

typecheck:
	mypy src/

run:
	uvicorn src.main:app --reload
