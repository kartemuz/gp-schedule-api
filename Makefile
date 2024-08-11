start:
	poetry run poetry run uvicorn src.main:app --host 0.0.0.0 --port 8123
setup_environment:
	poetry run python src/environment_setup.py
dev:
	poetry run fastapi dev --port 8213 src/main.py
test:
	poetry run pytest tests
test_controllers:
	poetry run pytest tests/controllers