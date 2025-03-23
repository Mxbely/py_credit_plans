ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/home/appuser" \
#     --shell "/sbin/nologin" \
#     --uid "${UID}" \
#     appuser

# RUN mkdir -p /app/alembic/versions && \
#     chown -R appuser:appuser /app/alembic && \
#     chmod -R 755 /app/alembic

RUN python -m pip install --upgrade pip && \
    pip install poetry

COPY ./poetry.lock ./poetry.lock
COPY ./pyproject.toml ./pyproject.toml
COPY ./alembic.ini ./alembic.ini

RUN poetry config virtualenvs.create false

RUN poetry lock
RUN poetry install --no-root --only main

# USER appuser

COPY . .

EXPOSE 8000
