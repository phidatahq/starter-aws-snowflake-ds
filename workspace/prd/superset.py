from pathlib import Path

from phidata.app.postgres import PostgresDb, PostgresVolumeType
from phidata.app.redis import Redis, RedisVolumeType
from phidata.app.superset import (
    SupersetWebserver,
    SupersetInit,
    SupersetWorker,
    SupersetWorkerBeat,
)
from phidata.infra.aws.resource.group import AwsResourceGroup
from phidata.infra.aws.resource.ec2.volume import EbsVolume

from workspace.prd.images import prd_superset_image
from workspace.settings import (
    aws_az,
    prd_key,
    prd_tags,
    services_ng_label,
    superset_enabled,
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
# EbsVolume for superset-db
prd_superset_db_volume = EbsVolume(
    name=f"superset-db-{prd_key}",
    size=16,
    availability_zone=aws_az,
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)
# EbsVolume for superset-redis
prd_superset_redis_volume = EbsVolume(
    name=f"superset-redis-{prd_key}",
    size=8,
    availability_zone=aws_az,
    tags=prd_tags,
    skip_delete=aws_skip_delete,
)

prd_superset_aws_resources = AwsResourceGroup(
    name=f"superset-{prd_key}",
    enabled=superset_enabled,
    volumes=[prd_superset_db_volume, prd_superset_redis_volume],
)

# -*- Kubernetes resources

# Shared k8s settings
# waits for superset-db to be ready before starting app
wait_for_db: bool = True
# waits for superset-redis to be ready before starting app
wait_for_redis: bool = True
# Mount the ws_repo using git-sync
mount_workspace: bool = False
# Mount the main branch
git_sync_branch: str = "main"
# Read env variables from env/prd_superset_env.yml
prd_superset_env_file: Path = ws_dir_path.joinpath("env/prd_superset_env.yml")
# Read secrets from secrets/prd_superset_secrets.yml
prd_superset_secrets_file: Path = ws_dir_path.joinpath(
    "secrets/prd_superset_secrets.yml"
)

# Superset db: A postgres instance to use as the database for superset
prd_superset_db = PostgresDb(
    name=f"ss-db",
    enabled=superset_enabled,
    volume_type=PostgresVolumeType.AWS_EBS,
    ebs_volume=prd_superset_db_volume,
    secrets_file=ws_dir_path.joinpath("secrets/prd_superset_db_secrets.yml"),
    pod_node_selector=services_ng_label,
)

# Superset redis: A redis instance to use as the celery backend for superset
prd_superset_redis = Redis(
    name=f"ss-redis",
    enabled=superset_enabled,
    volume_type=RedisVolumeType.AWS_EBS,
    ebs_volume=prd_superset_redis_volume,
    command=["redis-server", "--save", "60", "1"],
    pod_node_selector=services_ng_label,
)

# Superset webserver
prd_superset_ws = SupersetWebserver(
    replicas=3,
    enabled=superset_enabled,
    image_name=prd_superset_image.name,
    image_tag=prd_superset_image.tag,
    db_app=prd_superset_db,
    wait_for_db=wait_for_db,
    redis_app=prd_superset_redis,
    wait_for_redis=wait_for_redis,
    mount_workspace=mount_workspace,
    create_git_sync_sidecar=True,
    git_sync_repo=ws_repo,
    git_sync_branch=git_sync_branch,
    env_file=prd_superset_env_file,
    secrets_file=prd_superset_secrets_file,
    use_cache=use_cache,
    pod_node_selector=services_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
)

# Superset init
superset_init_enabled = True  # Mark as False after first run
prd_superset_init = SupersetInit(
    enabled=(superset_enabled and superset_init_enabled),
    image_name=prd_superset_image.name,
    image_tag=prd_superset_image.tag,
    db_app=prd_superset_db,
    wait_for_db=wait_for_db,
    redis_app=prd_superset_redis,
    wait_for_redis=wait_for_redis,
    mount_workspace=mount_workspace,
    create_git_sync_sidecar=True,
    git_sync_repo=ws_repo,
    git_sync_branch=git_sync_branch,
    env_file=prd_superset_env_file,
    secrets_file=prd_superset_secrets_file,
    use_cache=use_cache,
    pod_node_selector=workers_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
)

# Superset worker
prd_superset_worker = SupersetWorker(
    replicas=2,
    enabled=superset_enabled,
    image_name=prd_superset_image.name,
    image_tag=prd_superset_image.tag,
    db_app=prd_superset_db,
    wait_for_db=wait_for_db,
    redis_app=prd_superset_redis,
    wait_for_redis=wait_for_redis,
    mount_workspace=mount_workspace,
    create_git_sync_sidecar=True,
    git_sync_repo=ws_repo,
    git_sync_branch=git_sync_branch,
    env_file=prd_superset_env_file,
    secrets_file=prd_superset_secrets_file,
    use_cache=use_cache,
    pod_node_selector=workers_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
)

# Superset worker beat
prd_superset_worker_beat = SupersetWorkerBeat(
    replicas=2,
    enabled=superset_enabled,
    image_name=prd_superset_image.name,
    image_tag=prd_superset_image.tag,
    db_app=prd_superset_db,
    wait_for_db=wait_for_db,
    redis_app=prd_superset_redis,
    wait_for_redis=wait_for_redis,
    mount_workspace=mount_workspace,
    create_git_sync_sidecar=True,
    git_sync_repo=ws_repo,
    git_sync_branch=git_sync_branch,
    env_file=prd_superset_env_file,
    secrets_file=prd_superset_secrets_file,
    use_cache=use_cache,
    pod_node_selector=workers_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
)

prd_superset_apps = [
    prd_superset_db,
    prd_superset_redis,
    prd_superset_ws,
    prd_superset_init,
    prd_superset_worker,
    prd_superset_worker_beat,
]
