#!/usr/bin/env bash
set -eu

function CleanUp() {
    local exitCode=$?
    #echo "$(basename ${BASH_SOURCE})(${LINENO}): CleanUp, exitCode=${exitCode}"
}

trap CleanUp EXIT

function GetCurDir() {
    printf "%s" "$(realpath "$(dirname "${BASH_SOURCE}")")"
}

function GetPrjDir() {
    printf "%s" "$(realpath "$(GetCurDir)/..")"
}

. "$(GetCurDir)/version.sh"

function collectPackages() {
    local packages=()
    local packagesFile="${1}"
    while read -r package || [[ -n "${package}" ]]; do
        packages+=(${package})
    done < "${packagesFile}"

    echo "${packages[@]}"
}

function VcPkgInstall() {
    local packages=$(collectPackages "${1}")
    
    echo "$(basename ${BASH_SOURCE})(${LINENO}): "${VI_VcPkgDir}/vcpkg" install ${packages} --triplet ${VI_VcPkgTriplet} --overlay-triplets="$(GetPrjDir)/triplets""

    "${VI_VcPkgDir}/vcpkg" install ${packages} --triplet ${VI_VcPkgTriplet} --overlay-triplets="$(GetPrjDir)/triplets"
}

function VcPkgExport() {
    local packages=$(collectPackages "${1}")

    # Clean up all existing exports:
    rm -rf "${VI_VcPkgDir}"/vcpkg-export*.zip

    echo "$(basename ${BASH_SOURCE})(${LINENO}): "${VI_VcPkgDir}/vcpkg" export ${packages} --zip --triplet ${VI_VcPkgTriplet} --overlay-triplets="$(GetPrjDir)/triplets""

    "${VI_VcPkgDir}/vcpkg" export ${packages} --zip --triplet ${VI_VcPkgTriplet} --overlay-triplets="$(GetPrjDir)/triplets"
}

VcPkgInstall "$(GetCurDir)/packages.txt"

VcPkgExport "$(GetCurDir)/packages.txt"

