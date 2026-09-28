# Error action handling.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

# 0. Init constants.
. "${PSScriptRoot}/Util-Constants.ps1"

# 1. Clean up previous initialization.
$paths = ${MODULE_DIR}, ${VIRTUAL_ENV_DIR}

foreach ($path in ${paths}) {
    if (Test-Path -LiteralPath ${path}) {
        Remove-Item -Force -Recurse ${path}
    }
}

# 1. Clone testing system repository.
git clone ${MODULE_URL} ${MODULE_DIR}

# 2. Create Python virtual environment.
python -m venv ${VIRTUAL_ENV_DIR}

# 3. Install and upgrade pip and setuptools module.
."${VIRTUAL_ENV_DIR}\Scripts\python.exe" -m pip install --upgrade pip setuptools

# 4. Install testbuild module.
."${VIRTUAL_ENV_DIR}\Scripts\python.exe" -m pip install --no-deps ${MODULE_DIR}
