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

You can start writing assets in one of the directories in [teams/](./teams/). For Dagster to notice changes, you may have to "reload" the corresponding "code location" at http://localhost:8080/locations.


## Local development environment

To install production and development dependencies:

```shell
pip install -r requirements-dev.txt
```

### Linting

To configure linting to run before committing:

```shell
pre-commit install
```

To lint all files:

```shell
pre-commit run --all-files
```

### Tests

To run tests you need a PostgreSQL database running - some of the tests assert on how the pipelines ingest into a real PostgreSQL database. This can either be done with `docker compose up --build` as above to run all of Dagster including a database. Otherwise run the following to start only the database component.

```
cp sample.env .env
docker compose up --build -d db
```

To then run all the tests run:

```shell
pytest
```

To run all the tests in single file, for example `teams/deet/test_assets.py`, run:

```shell
pytest teams/deet/test_assets.py
```

To run a specific test in a file:

```shell
pytest teams/deet/test_assets.py::test_dynamic_asset_creation
```

See the [pytest documentation](https://docs.pytest.org/en/7.1.x/contents.html), or the [Dagster testing documentation](https://docs.dagster.io/concepts/testing) for more details.


## Deployment to staging

```shell
cf push data-flow-2-staging -f pipelines_platform/manifest.yaml
cf push data-flow-2-code-server-data-science-staging -f pipelines_platform/manifest-code-server.yaml
cf push data-flow-2-code-server-datasets-and-analysis-staging -f pipelines_platform/manifest-code-server.yaml
cf push data-flow-2-code-server-deet-staging -f pipelines_platform/manifest-code-server.yaml
cf push data-flow-2-code-server-gscip-staging -f pipelines_platform/manifest-code-server.yaml
cf push data-flow-2-code-server-lite-staging -f pipelines_platform/manifest-code-server.yaml
```
