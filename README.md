# data-flow-2

data-flow-2 is an instance of Dagster together with the code of pipelines that transfer and transform data.

> This project is to evaluate Dagster in a non production environment


## Get started

To run Dagster locally, you need [Docker](https://www.docker.com/products/docker-desktop/) installed. Then run

```bash
docker compose up --build
```

Then open http://localhost:8080 with your browser to see the Dagster interface.

You can start writing assets in one of the directories in [teams/](./teams/). The assets are automatically loaded into the corresponding Dagster code location as you define them.
