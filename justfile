# https://github.com/casey/just

# For Windows - run from Git bash shell
set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"]

create-certs:
    mkdir -p certs
    openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -sha256 -days 365 -nodes -subj "//CN=localhost"

prepare-env:
    sed 's/=.*$/=/' .env.template > .senv

mypy:
    uv run mypy app

ruff:
    uv run ruff format app

test:
    uv run pytest tests

development:
    TEST_MODE=True uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

production:
    docker-compose up -d --build

all: mypy ruff test
