# For Windows - run from Git bash shell
set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"]

mypy:
    uv run mypy app

ruff:
    uv run ruff format app

test:
    uv run pytest tests

all: mypy ruff test