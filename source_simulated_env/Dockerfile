FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONPATH=/app:/app/project:/app/project/cli:/app/project/resources

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.in-project true

RUN poetry install --no-interaction

