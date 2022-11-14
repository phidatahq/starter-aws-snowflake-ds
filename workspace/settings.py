from pathlib import Path
from typing import List
from typing_extensions import Literal

from phidata.utils.env_var import env_var_is_true

#
# -*- Workspace settings
#
# Workspace name: used for naming cloud resources
ws_name: str = "starter-aws-snowflake-ds"
# Workspace git repo url: used to git-sync DAGs and Charts
ws_repo: str = "https://github.com/phidatahq/starter-aws-snowflake-ds.git"
# Path to the workspace directory
ws_dir_path: Path = Path(__file__).parent.resolve()
# Path to the root i.e. data platform directory
data_platform_dir_path: Path = ws_dir_path.parent

#
# -*- Apps enabled in the workspace
#
pg_dbs_enabled: bool = True
superset_enabled: bool = True
jupyter_enabled: bool = True
airflow_enabled: bool = True
traefik_enabled: bool = True
whoami_enabled: bool = True

#
# -*- Dev settings
#
dev_env = "dev"
# Key for naming dev resources
dev_key = f"{ws_name}-{dev_env}"

#
# -*- Production settings
#
prd_env = "prd"
# Key for naming prd resources
prd_key = f"{ws_name}-{prd_env}"
# Tags for prd resources
prd_tags = {
    "Env": prd_env,
    "Project": ws_name,
}
# Domain for prd services like airflow and superset
prd_domain = "starter-aws-snowflake.com"

#
# -*- AWS settings
#
# Region to use for AWS resources
aws_region: str = "us-east-1"
# Availability Zone for EbsVolumes
aws_az: str = "us-east-1a"

#
# -*- EKS settings
#
# Production Subnets to use with the EKS cluster
prd_subnets: List[str] = ["subnet-005b6a764e3ab8a19", "subnet-0175392d110949300"]

# Node Group label for Services
services_ng_label = {
    "app_type": "service",
}
# Node Group label for Workers
workers_ng_label = {
    "app_type": "worker",
}

# How to distribute pods across EKS nodes
# "kubernetes.io/hostname" means spread across nodes
topology_spread_key: str = "kubernetes.io/hostname"
topology_spread_max_skew: int = 2
topology_spread_when_unsatisfiable: Literal[
    "DoNotSchedule", "ScheduleAnyway"
] = "DoNotSchedule"

#
# -*- Settings derived using environment variables
#
# When env var CACHE=True, phi will skip the create/delete of existing resources.
# So `CACHE=f phi [command]` can be used to recreate existing resources
# Example: `CACHE=f phi ws up --env dev --name airflow --type container`
#           will restart existing airflow containers.
use_cache: bool = env_var_is_true("CACHE", True)
