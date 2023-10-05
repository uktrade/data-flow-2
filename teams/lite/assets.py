from dagster import asset

@asset
def licenses() -> None:
    print('Fetching licenses')
