from dagster import asset, get_dagster_logger

logger = get_dagster_logger()

@asset
def licences() -> None:
    logger.info('Fetching licences')
