from pathlib import Path
from typing import Dict

from phidata.app.airflow import AirflowScheduler, AirflowWebserver, AirflowWorker
from phidata.app.postgres import PostgresDb
from phidata.app.redis import Redis

from workspace.dev.images import dev_airflow_image
from workspace.dev.pg_dbs import dev_pg_db_airflow_connections
from workspace.settings import (
    airflow_enabled,
    aws_region,
    use_cache,
    ws_dir_path,
    ws_name,
)

# -*- Docker resources

# Airflow db: A postgres instance to use as the database for airflow
dev_airflow_db = PostgresDb(
    name=f"airflow-db-{ws_name}",
    enabled=airflow_enabled,
    db_user="airflow",
    db_password="airflow",
    db_schema="airflow",
    # Connect to this db on port 8320
    container_host_port=8320,
)

# Airflow redis: A redis instance to use as the celery backend for airflow
dev_airflow_redis = Redis(
    name=f"airflow-redis-{ws_name}",
    enabled=airflow_enabled,
    command=["redis-server", "--save", "60", "1"],
    container_host_port=8321,
)

# Shared settings
# waits for airflow-db to be ready before starting app
wait_for_db: bool = True
# waits for airflow-redis to be ready before starting app
wait_for_redis: bool = True
# Airflow executor to use
executor: str = "CeleryExecutor"
# Mount the ws_repo using a docker volume
mount_workspace: bool = True
# Read env variables from env/dev_airflow_env.yml
dev_airflow_env_file: Path = ws_dir_path.joinpath("env/dev_airflow_env.yml")
# Read secrets from secrets/dev_airflow_secrets.yml
dev_airflow_secrets_file: Path = ws_dir_path.joinpath("secrets/dev_airflow_secrets.yml")
# Add airflow configuration using env variables
dev_airflow_env: Dict[str, str] = {
    "AIRFLOW__WEBSERVER__EXPOSE_CONFIG": "True",
    "AIRFLOW__WEBSERVER__EXPOSE_HOSTNAME": "True",
    "AIRFLOW__WEBSERVER__EXPOSE_STACKTRACE": "True",
    # Create aws_default connection_id
    "AWS_DEFAULT_REGION": aws_region,
    "AIRFLOW_CONN_AWS_DEFAULT": "aws://",
}

# Airflow webserver
dev_airflow_ws = AirflowWebserver(
    enabled=airflow_enabled,
    image_name=dev_airflow_image.name,
    image_tag=dev_airflow_image.tag,
    db_app=dev_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=dev_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    env=dev_airflow_env,
    env_file=dev_airflow_env_file,
    secrets_file=dev_airflow_secrets_file,
    use_cache=use_cache,
    db_connections=dev_pg_db_airflow_connections,
    # Access the airflow webserver on http://localhost:8310
    webserver_host_port=8310,
    # Settings to mark as false after first run
    # Wait for scheduler to initialize airflow db -- mark as false after first run
    wait_for_db_init=True,
    # Serve the airflow webserver on airflow.dp
    container_labels={
        "traefik.enable": "true",
        "traefik.http.routers.airflow-ws.entrypoints": "http",
        "traefik.http.routers.airflow-ws.rule": "Host(`airflow.dp`)",
        # point the traefik loadbalancer to the webserver_port on the container
        "traefik.http.services.airflow-ws.loadbalancer.server.port": "8080",
    },
)

# Airflow scheduler
dev_airflow_scheduler = AirflowScheduler(
    enabled=airflow_enabled,
    image_name=dev_airflow_image.name,
    image_tag=dev_airflow_image.tag,
    db_app=dev_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=dev_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    env=dev_airflow_env,
    env_file=dev_airflow_env_file,
    secrets_file=dev_airflow_secrets_file,
    use_cache=use_cache,
    db_connections=dev_pg_db_airflow_connections,
    # Settings to mark as false after first run
    # Init airflow db on container start -- mark as false after first run
    init_airflow_db=True,
    # Upgrade the airflow db on container start -- mark as false after first run
    upgrade_airflow_db=True,
    # Creates airflow user: admin, pass: admin -- mark as false after first run
    create_airflow_admin_user=True,
)

# Airflow worker serving the default & tier_1 queues
dev_airflow_worker = AirflowWorker(
    enabled=airflow_enabled,
    queue_name="default,tier_1",
    image_name=dev_airflow_image.name,
    image_tag=dev_airflow_image.tag,
    db_app=dev_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=dev_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    env=dev_airflow_env,
    env_file=dev_airflow_env_file,
    secrets_file=dev_airflow_secrets_file,
    use_cache=use_cache,
    db_connections=dev_pg_db_airflow_connections,
    # Settings to mark as false after first run
    # Wait for scheduler to initialize airflow db -- mark as false after first run
    wait_for_db_init=True,
)

dev_airflow_apps = [
    dev_airflow_db,
    dev_airflow_redis,
    dev_airflow_ws,
    dev_airflow_scheduler,
    dev_airflow_worker,
]
