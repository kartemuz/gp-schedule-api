start:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000
setup_env:
	poetry run python src/setup_env.py
dev:
	poetry run fastapi dev --port 8000 src/main.py
test:
	poetry run pytest tests
ssl_start:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=./certs/key.pem --ssl-certfile=./certs/cert.pem