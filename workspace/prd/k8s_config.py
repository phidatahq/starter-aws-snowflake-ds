from phidata.infra.k8s.config import K8sConfig

from workspace.settings import prd_env
from workspace.prd.airflow import prd_airflow_apps
from workspace.prd.aws_resources import prd_eks_cluster
from workspace.prd.superset import prd_superset_apps
from workspace.prd.traefik import prd_traefik_apps
from workspace.prd.jupyter import prd_jupyter_apps
from workspace.prd.pg_dbs import prd_pg_db_apps
from workspace.k8s.whoami import whoami_k8s_rg


# -*- Define prd k8s resources using the K8sConfig
prd_k8s_config = K8sConfig(
    env=prd_env,
    apps=prd_airflow_apps
    + prd_superset_apps
    + prd_pg_db_apps
    + prd_traefik_apps
    + prd_jupyter_apps,
    create_resources=[whoami_k8s_rg],
    eks_cluster=prd_eks_cluster,
)
