from phidata.infra.aws.config import AwsConfig

from workspace.settings import prd_env
from workspace.prd.aws_resources import prd_aws_resources
from workspace.prd.airflow import prd_airflow_aws_resources
from workspace.prd.superset import prd_superset_aws_resources
from workspace.prd.pg_dbs import prd_pg_db_aws_resources
from workspace.prd.jupyter import prd_jupyter_aws_resources


# -*- Define prd aws resources using the AwsConfig
prd_aws_config = AwsConfig(
    env=prd_env,
    resources=[
        prd_aws_resources,
        prd_airflow_aws_resources,
        prd_pg_db_aws_resources,
        prd_superset_aws_resources,
        prd_jupyter_aws_resources,
    ],
)
