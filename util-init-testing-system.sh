#!/usr/bin/env bash

set -euo pipefail

# 0. Init constants.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/util-constants.sh"

# 1. Clean up previous initialization.
rm -rf ${MODULE_DIR} ${VIRTUAL_ENV_DIR}

# 2. Clone testing system repository.
git clone ${MODULE_URL} ${MODULE_DIR}

# 3. Create Python virtual environment.
python3 -m venv ${VIRTUAL_ENV_DIR}

# 4. Install and upgrade pip and setuptools module.
${VIRTUAL_ENV_DIR}/bin/python3 -m pip install --upgrade pip setuptools

# 5. Install testbuild module.
${VIRTUAL_ENV_DIR}/bin/python3 -m pip install --no-deps ${MODULE_DIR}

# 6. Install requirements.
${VIRTUAL_ENV_DIR}/bin/python3 -m pip install -r requirements.txt
