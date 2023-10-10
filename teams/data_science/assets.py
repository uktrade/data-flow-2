from dagster import asset, asset_check, get_dagster_logger, AssetCheckResult, AssetCheckSeverity

logger = get_dagster_logger()


@asset
def predictions() -> None:
    logger.info('Predicting')


@asset_check(asset=predictions, description="Check that the predictions make sense")
def my_asset_has_something_1() -> AssetCheckResult:
    return AssetCheckResult(passed=True, metadata={"num_rows": 1253}, severity=AssetCheckSeverity.ERROR)


@asset_check(asset=predictions, description="Check that the predictions make sense")
def my_asset_has_something_2() -> AssetCheckResult:
    return AssetCheckResult(passed=False, metadata={"num_rows": 21}, severity=AssetCheckSeverity.ERROR)


@asset_check(asset=predictions, description="Check that the predictions make sense")
def my_asset_has_something_3() -> AssetCheckResult:
    return AssetCheckResult(passed=False, metadata={"num_rows": 42}, severity=AssetCheckSeverity.WARN)
