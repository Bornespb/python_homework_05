.PHONY: lint run test coverage

lint:
	pylint domain infrastructure tests main.py

run:
	python main.py

test:
	pytest

coverage:
	pytest --cov=domain --cov=infrastructure