ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m pip install --upgrade pip && \
    pip install poetry

COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
COPY ./alembic.ini ./alembic.ini

RUN poetry config virtualenvs.create false

RUN poetry lock
RUN poetry install --no-root --only main

COPY . .

EXPOSE 8000
