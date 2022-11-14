from typing import Dict
from pathlib import Path

from phidata.app.airflow import (
    AirflowWebserver,
    AirflowScheduler,
    AirflowWorker,
    AirflowFlower,
)
from phidata.app.postgres import PostgresDb, PostgresVolumeType
from phidata.app.redis import Redis, RedisVolumeType
from phidata.infra.aws.resource.group import AwsResourceGroup
from phidata.infra.aws.resource.ec2.volume import EbsVolume

from workspace.prd.aws_resources import prd_logs_s3_bucket
from workspace.prd.pg_dbs import prd_db_airflow_connections
from workspace.prd.images import prd_airflow_image
from workspace.settings import (
    airflow_enabled,
    aws_az,
    aws_region,
    prd_domain,
    prd_key,
    prd_tags,
    services_ng_label,
    topology_spread_key,
    topology_spread_max_skew,
    topology_spread_when_unsatisfiable,
    use_cache,
    workers_ng_label,
    ws_dir_path,
    ws_repo,
)

# -*- AWS resources

# Shared aws settings
aws_skip_delete: bool = False

# -*- EbsVolumes
# EbsVolume for airflow-db
prd_airflow_db_volume = EbsVolume(
    name=f"airflow-db-{prd_key}",
    size=32,
    availability_zone=aws_az,
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)
# EbsVolume for airflow-redis
prd_airflow_redis_volume = EbsVolume(
    name=f"airflow-redis-{prd_key}",
    size=16,
    availability_zone=aws_az,
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)

prd_airflow_aws_resources = AwsResourceGroup(
    name=f"airflow-{prd_key}",
    enabled=airflow_enabled,
    volumes=[prd_airflow_db_volume, prd_airflow_redis_volume],
)

# -*- Kubernetes resources

# Shared settings
# waits for airflow-db to be ready before starting app
wait_for_db: bool = True
# waits for airflow-redis to be ready before starting app
wait_for_redis: bool = True
# Airflow executor to use
executor: str = "CeleryExecutor"
# Mount the ws_repo using git-sync
mount_workspace: bool = True
# Mount the main branch of the ws_repo
git_sync_branch: str = "main"
# Read env variables from env/prd_airflow_env.yml
prd_airflow_env_file: Path = ws_dir_path.joinpath("env/prd_airflow_env.yml")
# Read secrets from secrets/prd_airflow_secrets.yml
prd_airflow_secrets_file: Path = ws_dir_path.joinpath("secrets/prd_airflow_secrets.yml")
# Add airflow configuration using env variables
prd_airflow_env: Dict[str, str] = {
    "AIRFLOW__WEBSERVER__BASE_URL": f"https://airflow.{prd_domain}",
    "AIRFLOW__WEBSERVER__EXPOSE_CONFIG": "True",
    "AIRFLOW__WEBSERVER__EXPOSE_HOSTNAME": "True",
    "AIRFLOW__WEBSERVER__EXPOSE_STACKTRACE": "True",
    "AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX": "True",
    # Create aws_default connection_id
    "AWS_DEFAULT_REGION": aws_region,
    "AIRFLOW_CONN_AWS_DEFAULT": "aws://",
    # Enable remote logging using s3
    "AIRFLOW__LOGGING__REMOTE_LOGGING": "True",
    "AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER": f"s3://{prd_logs_s3_bucket.name}/airflow",
    "AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID": "aws_default",
}

# Airflow db: A poprdres instance to use as the database for airflow
prd_airflow_db = PostgresDb(
    name="af-db",
    enabled=airflow_enabled,
    volume_type=PostgresVolumeType.AWS_EBS,
    ebs_volume=prd_airflow_db_volume,
    secrets_file=ws_dir_path.joinpath("secrets/prd_airflow_db_secrets.yml"),
    pod_node_selector=services_ng_label,
)

# Airflow redis: A redis instance to use as the celery backend for airflow
prd_airflow_redis = Redis(
    name="af-redis",
    enabled=airflow_enabled,
    volume_type=RedisVolumeType.AWS_EBS,
    ebs_volume=prd_airflow_redis_volume,
    command=["redis-server", "--save", "60", "1"],
    pod_node_selector=services_ng_label,
)

# Airflow webserver
prd_airflow_ws = AirflowWebserver(
    replicas=5,
    enabled=airflow_enabled,
    image_name=prd_airflow_image.name,
    image_tag=prd_airflow_image.tag,
    db_app=prd_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=prd_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    create_git_sync_sidecar=True,
    git_sync_repo=ws_repo,
    git_sync_branch=git_sync_branch,
    env=prd_airflow_env,
    env_file=prd_airflow_env_file,
    db_connections=prd_db_airflow_connections,
    secrets_file=prd_airflow_secrets_file,
    use_cache=use_cache,
    pod_node_selector=services_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
    # Settings to mark as false after first run
    # Wait for scheduler to initialize airflow db -- mark as false after first run
    wait_for_db_init=True,
)

# Airflow scheduler
prd_airflow_scheduler = AirflowScheduler(
    replicas=5,
    enabled=airflow_enabled,
    image_name=prd_airflow_image.name,
    image_tag=prd_airflow_image.tag,
    db_app=prd_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=prd_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    create_git_sync_sidecar=True,
    git_sync_repo=ws_repo,
    git_sync_branch=git_sync_branch,
    env=prd_airflow_env,
    env_file=prd_airflow_env_file,
    db_connections=prd_db_airflow_connections,
    secrets_file=prd_airflow_secrets_file,
    use_cache=use_cache,
    pod_node_selector=services_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
    # Settings to mark as false after first run
    # Init airflow db on container start -- mark as false after first run
    init_airflow_db=True,
    # Upgrade the airflow db on container start -- mark as false after first run
    upgrade_airflow_db=True,
    # Creates airflow user: admin, pass: admin -- mark as false after first run
    create_airflow_admin_user=True,
)

# Airflow worker queue
prd_airflow_worker = AirflowWorker(
    replicas=4,
    enabled=airflow_enabled,
    queue_name="default,tier_1",
    image_name=prd_airflow_image.name,
    image_tag=prd_airflow_image.tag,
    db_app=prd_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=prd_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    create_git_sync_sidecar=True,
    git_sync_repo=ws_repo,
    git_sync_branch=git_sync_branch,
    env=prd_airflow_env,
    env_file=prd_airflow_env_file,
    db_connections=prd_db_airflow_connections,
    secrets_file=prd_airflow_secrets_file,
    use_cache=use_cache,
    pod_node_selector=workers_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
    # Settings to mark as false after first run
    # Wait for scheduler to initialize airflow db -- mark as false after first run
    wait_for_db_init=True,
)


# Airflow flower
prd_airflow_flower = AirflowFlower(
    replicas=1,
    enabled=airflow_enabled,
    image_name=prd_airflow_image.name,
    image_tag=prd_airflow_image.tag,
    db_app=prd_airflow_db,
    wait_for_db=wait_for_db,
    redis_app=prd_airflow_redis,
    wait_for_redis=wait_for_redis,
    executor=executor,
    mount_workspace=mount_workspace,
    create_git_sync_sidecar=True,
    git_sync_repo=ws_repo,
    git_sync_branch=git_sync_branch,
    env=prd_airflow_env,
    env_file=prd_airflow_env_file,
    db_connections=prd_db_airflow_connections,
    secrets_file=prd_airflow_secrets_file,
    use_cache=use_cache,
    pod_node_selector=services_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
    # Settings to mark as false after first run
    # Wait for scheduler to initialize airflow db -- mark as false after first run
    wait_for_db_init=True,
)

prd_airflow_apps = [
    prd_airflow_db,
    prd_airflow_redis,
    prd_airflow_ws,
    prd_airflow_scheduler,
    prd_airflow_worker,
    prd_airflow_flower,
]
