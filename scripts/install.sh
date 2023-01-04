#!/bin/bash

############################################################################
#
# Install python dependencies. Run this inside a virtual env.
# Usage:
# 1. Create + activate virtual env using:
#     python3 -m venv ~/.venvs/dpenv
#     source ~/.venvs/dpenv/bin/activate
# 2. Install workspace and dependencies:
#     ./scripts/install.sh
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$( dirname $CURR_DIR )"
source ${CURR_DIR}/_utils.sh

main() {
  print_heading "Installing workspace: ${REPO_ROOT}"

  pip install --upgrade wheel

  print_heading "Installing requirements.txt"
  pip install --no-deps \
    -r ${REPO_ROOT}/requirements.txt

  print_heading "Installing workspace ${REPO_ROOT}"
  pip install --editable "${REPO_ROOT}"

  print_heading "Installing airflow requirements without dependencies for code completion"
  pip install --no-deps \
    -r ${REPO_ROOT}/workspace/dev/airflow_resources/requirements-airflow.txt
}

main "$@"
