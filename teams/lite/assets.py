from dagster import asset

@asset
def my_asset() -> None:
    print('Ingesting!')
