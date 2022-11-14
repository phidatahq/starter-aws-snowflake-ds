#!/bin/bash

set -e

CURR_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCKER_FILE="${CURR_SCRIPT_DIR}/airflow.Dockerfile"
REPO="repo"
NAME="airflow-dp"
TAG="prd"

echo "Running: docker build -t $REPO/$NAME:$TAG -f $DOCKER_FILE ."
docker build -t $REPO/$NAME:$TAG -f $DOCKER_FILE .
docker push $REPO/$NAME:$TAG
