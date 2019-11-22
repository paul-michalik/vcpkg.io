#!/usr/bin/env bash
set -e

function GetCurDir() {
    printf "%s" "$(realpath "$(dirname "${BASH_SOURCE}")")"
}

function GetImageName() {
    printf "%s" "$(basename "$(dirname "${BASH_SOURCE}")")"
}

docker build -t navvisgmbh/navvis.map.vcpkgio.$(GetImageName):latest --file="$(GetCurDir)/Dockerfile" .
