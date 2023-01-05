from pathlib import Path
from typing import Dict

from phidata.app.superset import (
    SupersetInit,
    SupersetWebserver,
    SupersetWorker,
    SupersetWorkerBeat,
)
from phidata.app.group import AppGroup
from phidata.app.postgres import PostgresDb, PostgresVolumeType
from phidata.app.redis import Redis, RedisVolumeType

from workspace.prd.superset.aws_resources import (
    prd_superset_db_volume,
    prd_superset_redis_volume,
)
from workspace.prd.aws_resources import (
    services_ng_label,
    topology_spread_key,
    topology_spread_max_skew,
    topology_spread_when_unsatisfiable,
    workers_ng_label,
)
from workspace.prd.images import prd_superset_image
from workspace.settings import (
    superset_enabled,
    use_cache,
    ws_dir_path,
    ws_repo,
)

#
# -*- Kubernetes resources
#

# -*- Settings
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
    name="ss-db",
    volume_type=PostgresVolumeType.AWS_EBS,
    ebs_volume=prd_superset_db_volume,
    secrets_file=ws_dir_path.joinpath("secrets/prd_superset_db_secrets.yml"),
    pod_node_selector=services_ng_label,
)

# Superset redis: A redis instance to use as the celery backend for superset
prd_superset_redis = Redis(
    name="ss-redis",
    volume_type=RedisVolumeType.AWS_EBS,
    ebs_volume=prd_superset_redis_volume,
    command=["redis-server", "--save", "60", "1"],
    pod_node_selector=services_ng_label,
)

# Superset webserver
prd_superset_ws = SupersetWebserver(
    replicas=2,
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
    replicas=1,
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
    replicas=1,
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

prd_superset_apps = AppGroup(
    name="superset",
    enabled=superset_enabled,
    apps=[
        prd_superset_db,
        prd_superset_redis,
        prd_superset_ws,
        prd_superset_init,
        prd_superset_worker,
        prd_superset_worker_beat,
    ],
)
