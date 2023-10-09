import pytest
from unittest import mock
import os
import sqlalchemy as sa

from dagster import load_assets_from_modules

from . import assets

all_assets = load_assets_from_modules([assets])


def test_dynamic_asset_creation():
    assert len(all_assets) == len(assets.specs)


def test_asset():
    with mock.patch.dict(os.environ, {'POSTGRES_URL': 'postgresql://postgres:postgres@127.0.0.1:5432/'}):
        for asset in all_assets:
            asset()

        engine = sa.create_engine(os.environ['POSTGRES_URL'], future=True)
        with engine.connect() as conn:
            table_1 = sa.Table("commodity_codes", sa.MetaData(), schema="dbt", autoload_with=conn)
            results_1 = conn.execute(sa.select(table_1)).fetchall()
            table_2 = sa.Table("commodity_codes2", sa.MetaData(), schema="dbt", autoload_with=conn)
            results_2 = conn.execute(sa.select(table_2)).fetchall()

        assert results_1, results_2 == (
            ('0100000000', '80', 'LIVE ANIMALS'),
            ('0101000000', '80', 'Live horses, asses, mules and hinnies'),
            ('0101210000', '10', 'Horses'),
            ('0101210000', '80', 'Pure-bred breeding animals'),
        )
