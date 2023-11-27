FROM python:3.11-alpine

WORKDIR /app

RUN apk --no-cache add gcc musl-dev python3-dev libffi-dev

ENV PYTHONPATH=/app:/app/project:/app/project/cli:/app/project/resources

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.in-project true

RUN poetry install --no-interaction

