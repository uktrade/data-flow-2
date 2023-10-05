from dagster import Definitions, load_assets_from_modules
from dagster_celery import celery_executor

from . import assets

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets, executor=celery_executor.configured({
        'broker': {
            'env': 'REDIS_URL',
        },
        'backend': {
            'env': 'REDIS_URL',
        },
    }),
)
