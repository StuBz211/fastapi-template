FROM python:3.10.14-alpine

ARG POETRY_VERSION=1.8.2

WORKDIR /code

RUN apk add --no-cache \
        curl gcc &&  \
    curl -sSL https://install.python-poetry.org | \
            POETRY_VERSION=${POETRY_VERSION} \
            POETRY_HOME=/opt/poetry \
            python3 - && cd /usr/local/bin && ln -s /opt/poetry/bin/poetry && \
            poetry config virtualenvs.create false && \
    apk del \
        curl gcc


COPY pyproject.toml poetry.lock* /code/

RUN poetry install

COPY . .






