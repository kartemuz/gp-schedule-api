start:
	poetry run poetry run uvicorn src.main:app --host 0.0.0.0 --port 8123
setup_environment:
	poetry run python src/environment_setup.py
