from phidata.app.jupyter import JupyterLab

from workspace.dev.images import dev_jupyter_image
from workspace.settings import jupyter_enabled, use_cache, ws_dir_path

# -*- Docker resources

# JupyterLab: Run dev notebooks
dev_jupyter = JupyterLab(
    enabled=jupyter_enabled,
    image_name=dev_jupyter_image.name,
    image_tag=dev_jupyter_image.tag,
    mount_workspace=True,
    # mounted when creating the image
    jupyter_config_file="/usr/local/jupyter/jupyter_lab_config.py",
    # Read env variables from env/dev_jupyter_env.yml
    env_file=ws_dir_path.joinpath("env/dev_jupyter_env.yml"),
    # Read secrets from secrets/dev_jupyter_secrets.yml
    secrets_file=ws_dir_path.joinpath("secrets/dev_jupyter_secrets.yml"),
    use_cache=use_cache,
    # Serve the notebook server on jupyter.dp
    container_labels={
        "traefik.enable": "true",
        "traefik.http.routers.jupyter.entrypoints": "http",
        "traefik.http.routers.jupyter.rule": "Host(`jupyter.dp`)",
        "traefik.http.services.jupyter.loadbalancer.server.port": "8888",
    },
)

dev_jupyter_apps = [dev_jupyter]
