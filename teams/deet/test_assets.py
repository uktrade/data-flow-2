import os
from unittest import mock

from dagster import load_assets_from_modules
import sqlalchemy as sa
import pytest

from . import assets


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"POSTGRES_URL": "postgresql://postgres:postgres@127.0.0.1:5432/"}):
        yield


@pytest.fixture()
def conn():
    with sa.create_engine(os.environ['POSTGRES_URL'], future=True).connect() as conn:
        yield conn


def test_asset(conn):
    assets.dbt__commodity_codes()

    table = sa.Table("commodity_codes", sa.MetaData(), schema="dbt", autoload_with=conn)
    results = conn.execute(sa.select(table)).fetchall()

    assert results == [
        ('0100000000', '80', 'LIVE ANIMALS'),
        ('0101000000', '80', 'Live horses, asses, mules and hinnies'),
        ('0101210000', '10', 'Horses'),
        ('0101210000', '80', 'Pure-bred breeding animals'),
    ]
