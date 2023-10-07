FROM python:3.11-buster
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
COPY pipelines_platform ./pipelines_platform
RUN \
	sed -i 's/__RUN_LAUNCHER_MODULE__/dagster/' ./pipelines_platform/dagster.yaml && \
	sed -i 's/__RUN_LAUNCHER_CLASS__/DefaultRunLauncher/' ./pipelines_platform/dagster.yaml

RUN pip install -r requirements.txt
