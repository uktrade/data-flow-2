web: './platform/paas-wrapper.sh dagster-webserver --workspace workspace.yaml --port 8080 --host 0.0.0.0'
daemon: './platform/paas-wrapper.sh dagster-daemon run'
worker: 'dagster-celery worker start -A dagster_celery.app --config-yaml executor.yaml'
