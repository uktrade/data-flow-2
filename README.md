# data-flow-2

[![Test suite](https://img.shields.io/github/actions/workflow/status/uktrade/data-flow-2/test.yml?label=Test%20suite)](https://github.com/uktrade/data-flow-2/actions/workflows/test.yml) [![Code coverage](https://img.shields.io/codecov/c/github/uktrade/data-flow-2?label=Code%20coverage)](https://app.codecov.io/gh/uktrade/data-flow-2)

data-flow-2 is an instance of Dagster together with the code of pipelines that transfer and transform data.

> This project is to evaluate Dagster in a non production environment


## Get started

To run Dagster locally, you need [Docker](https://www.docker.com/products/docker-desktop/) installed. Then run

```bash
cp sample.env .env
docker compose up --build
```

Then open http://localhost:8080 with your browser to see the Dagster interface.

You can start writing assets in one of the directories in [teams/](./teams/). The assets are automatically loaded into the corresponding Dagster code location as you define them.


## Local development environment

To install production and development dependencies:

```shell
pip install -r requirements-dev.txt
```

To configure linting to run before committing:

```shell
pre-commit install
```

To lint all files:

```shell
pre-commit run --all-files
```


## Deployment to staging

```shell
cf push data-flow-2-staging -f pipelines_platform/manifest.yaml
cf push data-flow-2-code-server-data-science-staging -f pipelines_platform/manifest-code-server.yaml
cf push data-flow-2-code-server-datasets-and-analysis-staging -f pipelines_platform/manifest-code-server.yaml
cf push data-flow-2-code-server-deet-staging -f pipelines_platform/manifest-code-server.yaml
cf push data-flow-2-code-server-gscip-staging -f pipelines_platform/manifest-code-server.yaml
cf push data-flow-2-code-server-lite-staging -f pipelines_platform/manifest-code-server.yaml
```
