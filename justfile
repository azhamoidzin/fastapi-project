# https://github.com/casey/just

# For Windows - run from Git bash shell
set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"]

mypy:
    uv run mypy app

ruff:
    uv run ruff format app

test:
    uv run pytest tests

development:
    TEST_MODE=True uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

all: mypy ruff test