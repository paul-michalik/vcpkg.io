#!/usr/bin/env bash
set -eu

function bootstrap.GetCurDir() {
    printf "%s" "$(realpath "$(dirname "${BASH_SOURCE}")")"
}

function bootstrap.DownloadVcPkg() {
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

function bootstrap.Main() {
    source "${bootstrap.GetCurDir}/configure.sh" "$@"
    ($(basename "${BASH_SOURCE}").DownloadVcPkg
    ($(basename "${BASH_SOURCE}").BootstrapVcPkg "$@"
}

# Invoke main if not explicitly disabled by passing first argument -noexec or --noexec  
if [[ 0 -eq "$#" || 0 -lt "$#" && ! "${1}" =~ ^[-]{1,2}noexec$ ]]; then
    $(basename "${BASH_SOURCE}" .sh).Main "$@"
fi