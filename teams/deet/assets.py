from dagster import asset, define_asset_job, AssetsDefinition

import os

import sqlalchemy as sa
from pg_bulk_ingest import ingest


def sync(
    schema,
    table_name,
    high_watermark="",
    delete="",
):
    engine = sa.create_engine(os.environ['POSTGRES_URL'], future=True)

    # The SQLAlchemy definition of the table to ingest data into
    metadata = sa.MetaData()
    table = sa.Table(
        table_name,
        metadata,
        sa.Column("code", sa.VARCHAR(10), primary_key=True),
        sa.Column("suffix", sa.VARCHAR(2), primary_key=True),
        sa.Column("description", sa.VARCHAR(), nullable=False),
        sa.Index(None, "code"),
        schema=schema,
    )

    def batches(high_watermark):
        yield (None, None, (
            (table, ('0100000000', '80', 'LIVE ANIMALS')),
            (table, ('0101000000', '80', 'Live horses, asses, mules and hinnies')),
        ))
        yield (None, None, (
            (table, ('0101210000', '10', 'Horses')),
            (table, ('0101210000', '80', 'Pure-bred breeding animals')),
        ))

    def on_before_visible(
        conn, ingest_table, source_modified_date
    ):
        pass

    with engine.connect() as conn:
        ingest(
            conn,
            metadata,
            batches,
            on_before_visible=on_before_visible,
            high_watermark=high_watermark,
            delete=delete,
        )

specs = [
    {"name": "CommodityCodesPipeline1", "schema": "dbt", "table_name": "commodity_codes"},
    {"name": "CommodityCodesPipeline2", "schema": "dbt", "table_name": "commodity_codes2"},
]


def build_asset(spec) -> AssetsDefinition:
    @asset(name=spec["name"])
    def _asset():
        sync(table_name=spec["table_name"], schema=spec["schema"])

    return _asset


assets=[build_asset(spec) for spec in specs]