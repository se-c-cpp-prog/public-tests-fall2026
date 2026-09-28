#!/usr/bin/env bash

set -euo pipefail

# 0. Init constants.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/util-constants.sh"

# 1. Update repository.
git -C ${MODULE_DIR} pull --ff-only

# 2. Re-install testbuild module.
${VIRTUAL_ENV_DIR}/bin/python3 -m pip install --no-deps --upgrade --force-reinstall ${MODULE_DIR}
