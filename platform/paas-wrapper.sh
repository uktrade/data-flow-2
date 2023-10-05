#!/bin/sh

set -e

export POSTGRES_URL=$(echo $VCAP_SERVICES | jq -r '.postgres[] | select (.instance_name == "data-flow-2-db").credentials.uri' | sed "s/^postgres/postgresql/")
export REDIS_URL=$(echo $VCAP_SERVICES | jq -r '.redis[] | select (.instance_name == "data-flow-2-redis").credentials.uri')'?ssl_cert_reqs=CERT_REQUIRED&ssl_ca_certs=/etc/ssl/certs/ca-certificates.crt'
export DAGSTER_HOME=/home/vcap/app

# Would need to be different for prod
export CODE_SERVERS__DEET__HOST=data-flow-2-code-server-deet-staging.apps.internal

exec "$@"
