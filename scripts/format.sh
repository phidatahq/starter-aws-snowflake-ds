#!/bin/bash

############################################################################
#
# Format workspace using black and mypy
# Usage:
#   ./scripts/format.sh
#
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$( dirname $CURR_DIR )"
source ${CURR_DIR}/_utils.sh

main() {
  print_heading "Running: black ${REPO_ROOT}"
  black ${REPO_ROOT}
  print_heading "Running: mypy ${REPO_ROOT} --config-file ${REPO_ROOT}/pyproject.toml"
  mypy ${REPO_ROOT} --config-file ${REPO_ROOT}/pyproject.toml
}

main "$@"
