FROM python:3.11-buster
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pipelines_platform ./pipelines_platform
