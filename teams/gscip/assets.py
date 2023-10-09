from dagster import asset, get_dagster_logger, AutoMaterializePolicy, AutoMaterializeRule, FreshnessPolicy

logger = get_dagster_logger()


@asset(
    auto_materialize_policy=AutoMaterializePolicy.eager().with_rules(
        AutoMaterializeRule.materialize_on_required_for_freshness(),
    ),
    freshness_policy=FreshnessPolicy(
        maximum_lag_minutes=2,
        cron_schedule='5/1 * * * *',
        cron_schedule_timezone='Europe/London',
    ),
)
def supply_chains() -> None:
    logger.info('Ingesting supply chains')
