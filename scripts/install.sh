#!/bin/bash

############################################################################
#
# Install python dependencies. Please run this inside a virtual env
# Usage:
# 1. Create + activate virtual env using:
#     python3 -m venv ~/.venvs/dpenv
#     source ~/.venvs/dpenv/bin/activate
# 2. Install workspace and dependencies:
#     ./scripts/install.sh
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$( dirname $CURR_DIR )"
source ${CURR_DIR}/_utils.sh

main() {
  print_heading "Installing workspace: ${ROOT_DIR}"

  pip install --upgrade wheel

  print_heading "Installing requirements.txt"
  pip install --no-deps \
    -r ${ROOT_DIR}/requirements.txt

  print_heading "Installing workspace ${ROOT_DIR} with [dev] extras"
  pip install --editable "${ROOT_DIR}[dev]"

  # print_heading "Installing airflow requirements without dependencies for code completion"
  # pip install --no-deps \
  #   -r ${ROOT_DIR}/workspace/dev/airflow_resources/requirements-airflow.txt
}

main "$@"
