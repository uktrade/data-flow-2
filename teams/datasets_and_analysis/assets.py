from dagster import AssetKey, Definitions, SourceAsset, asset

predictions_asset = SourceAsset(key=AssetKey("predictions"))
licenses_asset = SourceAsset(key=AssetKey("licences"))
supply_chains_assets = SourceAsset(key=AssetKey("supply_chains"))

@asset(deps=[
    predictions_asset,
    licenses_asset,
    supply_chains_assets,
])
def interactions() -> None:
    print('Fetching interactions')
