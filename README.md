## AWS Data Platform

This repo contains the code for building a data platform with 2 data environments:

1. dev: A development env running on docker
2. prd: A production env running on aws + k8s

## Setup

1. Create + activate a virtual env:

```sh
python3 -m venv ~/.venvs/dpenv
source ~/.venvs/dpenv/bin/activate
```

2. Install + init `phidata`:

```sh
pip install phidata
phi init
```

> from the `data-platform` dir:

3. Setup workspace:

```sh
phi ws setup
```

4. Copy `workspace/example_secrets` to `workspace/secrets`:

```sh
cp -r workspace/example_secrets workspace/secrets
```

5. Deploy dev containers to docker using:

```sh
phi ws up
```

If something fails, try running again with debug logs:

```sh
phi ws up -d
```

Optional: Create `.env` file:

```sh
cp example.env .env
```

## Using the dev environment

The [workspace/dev](workspace/dev) directory contains the code for the dev resources. The [workspace/settings.py](workspace/settings.py) file can be used to enable other apps like:

1. Postgres App: for storing dev data (runs 1 container)
2. Airflow App: for running workflows (runs 5 containers)
3. Superset App: for visualizing dev data (runs 4 containers)

Update the [workspace/settings.py](workspace/settings.py) file and run:

```sh
phi ws up
```

TIP: The `phi ws ...` commands use `--env dev` and `--config docker` by default. Set in the `workspace/config.py` file.

Running `phi ws up` is equivalent to running `phi ws up --env dev --config docker`

### Run Airflow

1. Set `airflow_enabled = True` in [workspace/settings.py](workspace/settings.py) and run `phi ws up`
2. Check out the airflow webserver running in the `airflow-ws-container`:

- url: `http://localhost:8310/`
- user: `admin`
- pass: `admin`

### Superset webserver

1. Set `superset_enabled = True` in [workspace/settings.py](workspace/settings.py) and run `phi ws up`
2. Check out the superset webserver running in the `superset-ws-container`:

- url: `http://localhost:8410/`
- user: `admin`
- pass: `admin`

### Format + lint workspace

Format with `black` & lint with `mypy` using:

```sh
./scripts/format.sh
```

If you need to install packages, run:

```sh
pip install black mypy
```

### Upgrading phidata version

> activate virtualenv: `source ~/.venvs/dpenv/bin/activate`

1. Upgrade phidata:

```sh
pip install phidata --upgrade
```

2. Rebuild local images & recreate containers:

```sh
CACHE=f phi ws up --env dev --config docker
```

### Optional: Install workspace locally

Install the workspace & python packages locally in your virtual env using:

```sh
./scripts/install.sh
```

This will:

1. Install python packages from `requirements.txt`
2. Install python project in `--editable` mode
3. Install `requirements-airflow.txt` without dependencies for code completion

This enables:

1. Running `black` & `mypy` locally
2. Running workflows locally
3. Editor auto-completion

### Add python packages

Following [PEP-631](https://peps.python.org/pep-0631/), we should add dependencies to the [pyproject.toml](pyproject.toml) file.

To add a new package:

1. Add the module to the [pyproject.toml](pyproject.toml) file.
2. Run: `./scripts/upgrade.sh`. This script updates the `requirements.txt` file.
3. _Optional: Run: `./scripts/install.sh` to install the new dependencies in a local virtual env._
4. Run `CACHE=f phi ws up` to recreate images + containers

### Adding airflow providers

Airflow requirements are stored in the [workspace/dev/airflow_resources/requirements-airflow.txt](/workspace/dev//airflow_resources/requirements-airflow.txt) file.

To add new airflow providers:

1. Add the module to the [workspace/dev/airflow_resources/requirements-airflow.txt](/workspace/dev/airflow_resources/requirements-airflow.txt) file.
2. _Optional: Run: `./scripts/install.sh` to install the new dependencies in a local virtual env._
3. Run `CACHE=f phi ws up --name airflow` to recreate images + containers

### To force recreate all images & containers, use the `CACHE` env variable

```sh
CACHE=false phi ws up \
  --env dev \
  --config docker \
  --type image|container \
  --name airflow|superset|pg \
  --app airflow|superset
```

### Shut down workspace

```sh
phi ws down
```

### Restart all resources

```sh
phi ws restart
```

### Restart all containers

```sh
phi ws restart --type container
```

### Restart traefik app

```sh
phi ws restart --app traefik
```

### Restart airflow app

```sh
phi ws restart --app airflow
```

### Add environment/secret variables to your apps

The containers read env using the `env_file` and secrets using the `secrets_file` params.
These files are stored in the [workspace/env](workspace/env) or [workspace/secrets](workspace/secrets) directories.

#### Airflow

To add env variables to your airflow containers:

1. Update the [workspace/env/dev_airflow_env.yml](workspace/env/dev_airflow_env.yml) file.
2. Restart all airflow containers using: `phi ws restart --name airflow --type container`

To add secret variables to your airflow containers:

1. Update the [workspace/secrets/dev_airflow_secrets.yml](workspace/secrets/dev_airflow_secrets.yml) file.
2. Restart all airflow containers using: `phi ws restart --name airflow --type container`

### Test a DAG

```sh
# ssh into airflow-worker | airflow-ws
docker exec -it airflow-ws-container zsh
docker exec -it airflow-worker-container zsh

# Test run the DAGs using module name
python -m workflow.dir.file

# Test run the DAG file
python /mnt/workspaces/data-platform/workflow/dir/file.py

# List DAGs
airflow dags list

# List tasks in DAG
airflow tasks list \
  -S /mnt/workspaces/data-platform/workflow/dir/file.py \
  -t dag_name

# Test airflow task
airflow tasks test dag_name task_name 2022-07-01
```

### Recreate everything

Notes:

- Use `data-platform` as the working directory
- Deactivate existing venv using `deactivate` if needed

```sh
echo "*- Deleting venv"
rm -rf ~/.venvs/dpenv

echo "*- Recreating venv"
python3 -m venv ~/.venvs/dpenv
source ~/.venvs/dpenv/bin/activate

echo "*- Install phi"
pip install phidata
phi init -r

echo "*- Setup + deploying workspace"
phi ws setup
CACHE=f phi ws up
```
