# Error action handling.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

# 0. Init constants.
. "${PSScriptRoot}/Util-Constants.ps1"

# 1. Update repository.
git -C ${MODULE_DIR} pull --ff-only

# 2. Re-install testbuild module.
."${VIRTUAL_ENV_DIR}\Scripts\python.exe" -m pip install --no-deps --upgrade --force-reinstall ${MODULE_DIR}
