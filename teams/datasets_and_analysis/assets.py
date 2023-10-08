from dagster import Definitions, asset, get_dagster_logger

logger = get_dagster_logger()


@asset(deps=[
    "predictions",
    "licences",
    "supply_chains",
], op_tags={
    'launcher/memory_in_mb': 10000,
    'launcher/disk_in_mb': 500,
})
def interactions() -> None:
    logger.info('Fetching interactions')


@asset(deps=[
    "interactions",
    "dbt__commodity_codes",
])
def report() -> None:
    logger.info('Fetching interactions')
