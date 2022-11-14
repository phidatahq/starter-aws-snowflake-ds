#!/bin/bash

############################################################################
#
# Format workspace using black and mypy
# Usage:
#   ./scripts/format.sh
#
############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$( dirname $CURR_DIR )"
source ${CURR_DIR}/_utils.sh

main() {
  print_heading "Running: black ${ROOT_DIR}"
  black ${ROOT_DIR}
  print_heading "Running: mypy ${ROOT_DIR} --config-file ${ROOT_DIR}/pyproject.toml"
  mypy ${ROOT_DIR} --config-file ${ROOT_DIR}/pyproject.toml
}

main "$@"
