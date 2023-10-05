from dagster import asset

@asset
def supply_chains() -> None:
    print('Ingesting supply chains')
