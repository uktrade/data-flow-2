from dagster import asset, get_dagster_logger

logger = get_dagster_logger()

@asset
def supply_chains() -> None:
    logger.info('Ingesting supply chains')
