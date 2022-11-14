from phidata.app.traefik import IngressRoute, ServiceType

from workspace.prd.aws_resources import prd_aws_dp_certificate
from workspace.prd.airflow import prd_airflow_ws, prd_airflow_flower
from workspace.prd.superset import prd_superset_ws
from workspace.prd.jupyter import prd_jupyter
from workspace.k8s.whoami import whoami_service, whoami_port
from workspace.settings import (
    airflow_enabled,
    jupyter_enabled,
    prd_domain,
    services_ng_label,
    superset_enabled,
    topology_spread_key,
    topology_spread_max_skew,
    topology_spread_when_unsatisfiable,
    traefik_enabled,
    use_cache,
    ws_dir_path,
)

# -*- Kubernetes resources

# Traefik Ingress: For routing web requests within the EKS cluster
routes = [
    {
        "match": f"Host(`whoami.{prd_domain}`)",
        "kind": "Rule",
        "services": [
            {
                "name": whoami_service.service_name,
                "port": whoami_port.service_port,
            }
        ],
    },
]

if airflow_enabled:
    routes.append(
        {
            "match": f"Host(`airflow.{prd_domain}`)",
            "kind": "Rule",
            "services": [
                {
                    "name": prd_airflow_ws.get_ws_service_name(),
                    "port": prd_airflow_ws.get_ws_service_port(),
                }
            ],
        }
    )
    routes.append(
        {
            "match": f"Host(`flower.{prd_domain}`)",
            "kind": "Rule",
            "services": [
                {
                    "name": prd_airflow_flower.get_flower_service_name(),
                    "port": prd_airflow_flower.get_flower_service_port(),
                }
            ],
        }
    )

if superset_enabled:
    routes.append(
        {
            "match": f"Host(`superset.{prd_domain}`)",
            "kind": "Rule",
            "services": [
                {
                    "name": prd_superset_ws.get_app_service_name(),
                    "port": prd_superset_ws.get_app_service_port(),
                }
            ],
        }
    )

if jupyter_enabled:
    routes.append(
        {
            "match": f"Host(`jupyter.{prd_domain}`)",
            "kind": "Rule",
            "services": [
                {
                    "name": prd_jupyter.get_app_service_name(),
                    "port": prd_jupyter.get_app_service_port(),
                }
            ],
        }
    )

traefik_name = "traefik"
traefik_ingress_route = IngressRoute(
    replicas=3,
    name=traefik_name,
    enabled=traefik_enabled,
    web_enabled=True,
    web_routes=routes,
    # Use ACM certificate to enable HTTPS
    # websecure_enabled=True,
    # websecure_routes=routes,
    # forward_web_to_websecure=True,
    # Read ACM certificate from a summary file and add the certificate ARN to the service_annotations
    # acm_certificate_summary_file=prd_aws_dp_certificate.certificate_summary_file,
    # Use a LoadBalancer service
    service_type=ServiceType.LOAD_BALANCER,
    # Configure the LoadBalancer using annotations:
    service_annotations={
        # Use a Network LoadBalancer
        # reference: https://kubernetes.io/docs/concepts/services-networking/service/#aws-nlb-support
        "service.beta.kubernetes.io/aws-load-balancer-type": "nlb",
        "service.beta.kubernetes.io/aws-load-balancer-nlb-target-type": "ip",
        # To make the load balancer internal. Set internal = "true"
        # reference: https://kubernetes.io/docs/concepts/services-networking/service/#internal-load-balancer
        # "service.beta.kubernetes.io/aws-load-balancer-internal": "true",
        # Other annotations: https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/guide/service/annotations/#annotations
    },
    # Enable traefik dashboard
    dashboard_enabled=True,
    # Serve traefik dashboard at traefik.prd_domain
    domain_name=prd_domain,
    # The dashboard is gated behind a user:password, which is generated using the cmd:
    #   htpasswd -nb user password
    # You can provide the "users:password" list as DASHBOARD_AUTH_USERS in the secrets_file
    secrets_file=ws_dir_path.joinpath("secrets/prd_traefik_secrets.yml"),
    use_cache=use_cache,
    pod_node_selector=services_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
)

prd_traefik_apps = [traefik_ingress_route]
