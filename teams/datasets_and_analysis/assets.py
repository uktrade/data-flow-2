from dagster import AssetKey, Definitions, SourceAsset, asset, get_dagster_logger

logger = get_dagster_logger()

predictions_asset = SourceAsset(key=AssetKey("predictions"))
licenses_asset = SourceAsset(key=AssetKey("licences"))
supply_chains_assets = SourceAsset(key=AssetKey("supply_chains"))


@asset(deps=[
    predictions_asset,
    licenses_asset,
    supply_chains_assets,
], op_tags={
    'launcher/memory_in_mb': 10000,
    'launcher/disk_in_mb': 500,
})
def interactions() -> None:
    logger.info('Fetching interactions')
