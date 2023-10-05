from dagster import asset

@asset
def licences() -> None:
    print('Fetching licences')
