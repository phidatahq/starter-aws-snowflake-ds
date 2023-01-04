#!/bin/bash

set -e

CURR_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCKER_FILE="${CURR_SCRIPT_DIR}/jupyter.Dockerfile"
REPO="repo"
NAME="jupyter"
TAG="prd"

echo "Running: docker build -t $REPO/$NAME:$TAG -f $DOCKER_FILE ."
docker build -t $REPO/$NAME:$TAG -f $DOCKER_FILE .
docker push $REPO/$NAME:$TAG
