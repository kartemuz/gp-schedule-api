# Web API для программы составления расписания занятий

## Running

### Using bash

#### Development
```bash
fastapi dev --port 8213 src/main.py
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

## Generating secret keys
### Creating `certs` directory
```
mkdir certs
```
### Private key
```bash
openssl genrsa -out certs/jwt-private.pem 2048
```
### Public key
```bash
openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```