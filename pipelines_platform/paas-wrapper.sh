#!/bin/sh

set -e

sed -i 's/__RUN_LAUNCHER_MODULE__/cf_launcher/' ./pipelines_platform/dagster.yaml
sed -i 's/__RUN_LAUNCHER_CLASS__/CFLauncher/' ./pipelines_platform/dagster.yaml

export CF_LAUNCHER_CODE_LOCATION_TO_APP_MAPPING='{
    "Data Science": "data-flow-2-code-server-data-science-staging",
    "Datasets & Analysis": "data-flow-2-code-server-datasets-and-analysis-staging",
    "LITE": "data-flow-2-code-server-lite-staging",
    "GSCIP": "data-flow-2-code-server-gscip-staging",
    "DEET": "data-flow-2-code-server-deet-staging"
}'

export POSTGRES_URL=$(echo $VCAP_SERVICES | jq -r '.postgres[] | select (.instance_name == "data-flow-2-db").credentials.uri' | sed "s/^postgres/postgresql/")
export DAGSTER_HOME=/home/vcap/app/pipelines_platform

# Would need to be different for prod
export CODE_SERVERS__DEET__HOST=data-flow-2-code-server-deet-staging.apps.internal
export CODE_SERVERS__DATA_SCIENCE__HOST=data-flow-2-code-server-data-science-staging.apps.internal
export CODE_SERVERS__DATASETS_AND_ANALYSIS__HOST=data-flow-2-code-server-datasets-and-analysis-staging.apps.internal
export CODE_SERVERS__GSCIP__HOST=data-flow-2-code-server-gscip-staging.apps.internal
export CODE_SERVERS__LITE__HOST=data-flow-2-code-server-lite-staging.apps.internal

exec "$@"
