from setuptools import find_packages, setup

setup(
    name="data_flow_2",
    packages=find_packages(exclude=["data_flow_2_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-webserver",
        "dagster-postgres",
        "pg-bulk-ingest",
        "psycopg==3.1.10",
    ],
    extras_require={"dev": ["pytest"]},
)
