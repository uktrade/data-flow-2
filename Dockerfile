FROM python:3.11-buster
ENV PYTHONUNBUFFERED 1

RUN \
	mkdir -p /app

WORKDIR /app

COPY setup.py pyproject.toml .
RUN \
	pip install -e ".[dev]"

COPY dagster.yaml workspace.yaml .
