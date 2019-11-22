#!/usr/bin/env bash
set -eu

function docker.GetCurDir() {
    printf "%s" "$(realpath "$(dirname "${BASH_SOURCE}")")"
}

function docker.GetPrjDir() {
    printf "%s" "$(realpath "$(docker.GetCurDir)/../..")"
}

function docker.ShowUsage() {
    cat <<EOF
Synopsis: 

    $(basename ${BASH_SOURCE}) [options] --triplet <triplet> --commit <tag|version> <--> <package names>

Main options:
EOF
}

function docker.Defaults() {
    if [[ ! -v VI_VcPkgTriplet ]]; then
        declare -g VI_VcPkgTriplet=x64-linux-gcc
    fi
}