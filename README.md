# Pet project

## Description
Simple pet-project with following features:
- `FastAPI` as backend.
- Everything is containerized via `Docker`.
- `Nginx` as reverse proxy to run in front of backend.
- Async `SQLAlchmy` for ORM models. **PostgreSQL** is used as main database.
- `Alembic` for migrations.
- `Pytest` for testing. Mocks, fixtures, patches.
- Other tools used: `mypy`, `ruff`, `uv`, `just`.

## Project requirements

- [Docker](https://www.docker.com/)
- [uv package manager](https://github.com/astral-sh/uv)

## Setup

### 0. Setup .env file

Some config variables have default values (`app/config.py`), but some of them
require respective value in `.env` file. You may use following command
```
just prepare-env
```
which creates .env file with empty variables

### 1. Install project dependencies

```
uv sync --frozen
```

### 2. Create self-signed certificates (skip if you have certificates)

```
just create-certs
```

## Running application

### Development mode

In this mode *docs* are included as endpoints for convenient testing.

To run in development mode simply run following command

 ```
 just development
 ```

This will run FastAPI application in console, with in-memory sqlite databse

### Production mode

*docs* are excluded for this mode to prevent API exposure.

To run in production mode simply run following command

 ```
 just production
 ```

This will run FastAPI application in docker container, with nginx container as reverse proxy, running on HTTPS on 443 port.
Containerized PostgreSQL will be used as database.

## Useful development tools

### Formatting, type checking, tests

For type checking simply use
```
just mypy
```

For formatting simply use
```
just ruff
```

For tests simply use
```
just test
```

To run everything at once use
```
just all
```