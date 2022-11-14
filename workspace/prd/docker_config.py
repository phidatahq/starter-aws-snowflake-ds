from phidata.infra.docker.config import DockerConfig

from workspace.settings import ws_name, prd_env
from workspace.prd.images import prd_images


# -*- Define prd docker resources using the DockerConfig
prd_docker_config = DockerConfig(
    env=prd_env,
    network=ws_name,
    # uncomment the following line to build local images
    images=prd_images,
)
