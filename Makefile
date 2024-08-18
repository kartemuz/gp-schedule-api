start:
	poetry run poetry run uvicorn src.main:app --host 0.0.0.0 --port 8123
setup_env:
	poetry run python src/setup_env.py
dev:
	poetry run fastapi dev --port 8213 src/main.py
test:
	poetry run pytest tests
