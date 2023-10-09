from dagster import asset, materialize_to_memory

from .assets import interactions, report


def test_report():
    # Will materialize the assets in the right order
    materialize_to_memory([report, interactions])
