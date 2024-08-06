# Web API для программы составления расписания занятий

## Running

### Using bash

#### Development
```bash
fastapi dev src/main.py
```
#### Testing
```bash
pytest tests
```
#### Server
```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8123
```
### Using make

#### Server
```bash
make start
```
