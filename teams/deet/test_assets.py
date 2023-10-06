import pytest

from dagster import load_assets_from_modules

from . import assets

all_assets = load_assets_from_modules([assets])

def test_dynamic_asset_creation():
    assert len(all_assets) == len(assets.specs)

