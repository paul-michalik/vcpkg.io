#!/usr/bin/env bash
set -e

function CleanUp() {
    local exitCode=$?
    #echo "$(basename ${BASH_SOURCE})(${LINENO}): CleanUp, exitCode=${exitCode}"
}

trap CleanUp EXIT

function GetCurDir() {
    printf "%s" "$(realpath "$(dirname "${BASH_SOURCE}")")"
}

. "$(GetCurDir)/version.sh"

function DownloadVcPkg() {
    [[ ! -d "${VI_VcPkgDir}" ]] && mkdir -p "${VI_VcPkgDir}"

    [[ ! -e "${VI_VcPkgDir}/vcpkg.zip" ]] && curl -L "http://github.com/microsoft/vcpkg/archive/${VI_VcPkgCommitHash}.zip" -o "${VI_VcPkgDir}/vcpkg.zip"
    
    if [[ ! -e "${VI_VcPkgDir}/.vcpkg-root" ]]; then
        [[ ! -d "${VI_VcPkgDir}/vcpkg-${VI_VcPkgCommitHash}" ]] && unzip -o "${VI_VcPkgDir}/vcpkg.zip" -d "${VI_VcPkgDir}"
        mv "${VI_VcPkgDir}/vcpkg-${VI_VcPkgCommitHash}"/{,.[^.]}* "${VI_VcPkgDir}"
        rm -rf "${VI_VcPkgDir}/vcpkg-${VI_VcPkgCommitHash}"
    else
        echo "Nothing to do, everything up to date. vcpkg in ${VI_VcPkgDir}"
    fi
}

function BootstrapVcPkg() {
    local osName=$(uname)
    if [[ "${osName,,}" =~ mingw64_nt ]]; then
        [[ ! -e "${VI_VcPkgDir}/vcpkg.exe" ]] && "${VI_VcPkgDir}/bootstrap-vcpkg.bat"
    else
        [[ ! -e "${VI_VcPkgDir}/vcpkg" ]] && "${VI_VcPkgDir}/bootstrap-vcpkg.sh"
    fi
}

DownloadVcPkg
BootstrapVcPkg