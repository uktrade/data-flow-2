from dagster import asset

@asset
def interactions() -> None:
    print('Fetching interactions')
