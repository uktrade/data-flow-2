from dagster import Definitions, load_assets_from_modules

from . import assets

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    asset_checks=[
        assets.my_asset_has_something_1,
        assets.my_asset_has_something_2,
        assets.my_asset_has_something_3,
    ],
)
