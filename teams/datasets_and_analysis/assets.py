import random

from dagster import Output, Definitions, AssetCheckResult, AssetCheckSpec, AssetCheckSeverity, asset, asset_check, get_dagster_logger

logger = get_dagster_logger()


@asset(deps=[
    "predictions",
    "licences",
    "supply_chains",
], op_tags={
    'launcher/memory_in_mb': 10000,
    'launcher/disk_in_mb': 500,
}, description='''
Initial description of the asset. Markdown is supported

---

With multiple lines **bold**, ~strike~, [link](https://www.github.com/)_

### Header

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc tincidunt nec arcu eget sodales.

- List item
- Second list item

---

### Another header

 Nunc vitae maximus elit, et feugiat nulla. Etiam posuere nibh sapien, vitae cursus mi gravida non. Duis rhoncus at orci et luctus. Nam nibh nisi, commodo ac rutrum id, pellentesque quis tortor. Vivamus ipsum lorem, porttitor quis nunc quis, venenatis egestas ligula. Aenean rutrum magna ut luctus finibus. Fusce suscipit mattis tempus. Aenean ullamcorper ipsum et augue lobortis, ut fermentum velit interdum.

''')
def interactions() -> None:
    logger.info('Fetching interactions')


@asset(deps=[
    "interactions",
    "dbt__commodity_codes",
], check_specs=[
    AssetCheckSpec(name="has_no_nulls", asset="report"),
    AssetCheckSpec(name="has_some_minor_issue", asset="report"),
])
def report():
    logger.info('Fetching report')

    yield Output(None, metadata={
        "num_rows": 35 + random.randrange(-10, 10),
        "maximum_widgets_per_foo": 10 + random.randrange(-10, 10),
        "something_custom": "custom-data-value",
    })

    yield AssetCheckResult(
        check_name="has_no_nulls",
        passed=True
    )

    yield AssetCheckResult(
        check_name="has_some_minor_issue",
        severity=AssetCheckSeverity.WARN,
        passed=False,
        metadata={
            "number_of_rows_with_issue": int(10),
        },
    )
