# Web API для программы составления расписания занятий

## Запуск

### Разработка
```bash
fastapi dev src/main.py
```
### Тестирование
```bash
pytest tests
```
### Сервер
```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 80
```
