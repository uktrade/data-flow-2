from dagster import asset

@asset
def predictions() -> None:
    print('Predicting')
