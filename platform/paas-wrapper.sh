#!/bin/sh

export POSTGRES_URL=$(echo $VCAP_SERVICES | jq -r '.postgres[] | select (.instance_name == "data-flow-2-db").credentials.uri'| sed "s/^postgres/postgresql/")

exec "$@"
