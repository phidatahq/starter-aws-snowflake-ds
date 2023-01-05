from pathlib import Path
from typing import List, Optional

from phidata.utils.env_var import env_var_is_true

#
# -*- Workspace settings
#
# Workspace name: used for naming cloud resources
ws_name: str = "dp004"
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
aws_az_1a: str = "us-east-1a"
aws_az_1b: str = "us-east-1b"
# 2 public subnets. 1 in each AZ.
public_subnets: List[str] = ["subnet-0aebed09ea7c82a5f", "subnet-0d53d74c0bb98ac9d"]
# 2 private subnets. 1 in each AZ.
private_subnets: List[str] = ["subnet-0964a2e70b7289ee5", "subnet-0c2587701e140e69e"]
# Security Groups
security_groups: Optional[List[str]] = None

#
# -*- Settings from environment variables. Set these in .env file.
#
# By default use_cache=True and `phi` skips creation if a resource with the same name is found.
# Set use_cache=False to force recreate resources even if they exist.
use_cache: bool = env_var_is_true("USE_CACHE", True)
