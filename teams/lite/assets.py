from dagster import asset, get_dagster_logger, AssetCheckSpec, AssetCheckResult, AssetCheckSeverity, Output

logger = get_dagster_logger()


@asset(check_specs=[
    AssetCheckSpec(name="has_no_nulls", asset="licences"),
    AssetCheckSpec(name="has_some_minor_issue", asset="licences"),
])
def licences() -> None:
    yield AssetCheckResult(
        check_name="has_no_nulls",
        passed=False
    )
    yield AssetCheckResult(
        check_name="has_some_minor_issue",
        severity=AssetCheckSeverity.WARN,
        passed=False,
        metadata={
            "number_of_rows_with_issue": int(10),
        },
    )

    logger.info('Fetching licences')
    yield Output(value=[])
