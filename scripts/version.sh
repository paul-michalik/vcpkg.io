#!/usr/bin/env bash

set -e

function GetCurDir() {
    printf "%s" "$(realpath "$(dirname "${BASH_SOURCE}")")"
}

function GetPrjDir() {
    printf "%s" "$(realpath "$(GetCurDir)/..")"
}

[[ ! -v VI_Platform || -z "${VI_Platform}" ]] && export VI_Platform=x64
[[ ! -v VI_Toolset || -z "${VI_Toolset}" ]] && export VI_Toolset=gcc

# ==============================
# VcPkg version 2019.7.31 (in toolsrc/VERSION.txt) 
# ==============================
[[ ! -v VI_VcPkgVersion || -z "${VI_VcPkgVersion}" ]] && export VI_VcPkgVersion=2019.7.31
[[ ! -v VI_VcPkgCommitHash || -z "${VI_VcPkgCommitHash}" ]] && export VI_VcPkgCommitHash=3dda86bd2785933485225202a710cde22c3b1ae1
[[ ! -v VI_VcPkgDir || -z "${VI_VcPkgDir}" ]] && export VI_VcPkgDir="$(GetPrjDir)/.vcpkg/${VI_VcPkgVersion}"
[[ ! -v VI_VcPkgTriplet || -z "${VI_VcPkgTriplet}" ]] && export VI_VcPkgTriplet=${VI_Platform}-linux

echo "Your vcpkg environment:" 
printenv | grep "^VI_*"