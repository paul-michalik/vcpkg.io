#!/usr/bin/env bash
set -exv

function GetCurDir() {
    realpath "$(dirname "${BASH_SOURCE}")"
}

function GetImageName() {
    basename "$(dirname "${BASH_SOURCE}")"
}

function GetPrjDir() {
    realpath "$(GetCurDir)/../.."
}

docker run --rm -it --name $(GetImageName) -v "$(GetPrjDir)":/wrk/vcpkg.io -w //wrk/vcpkg.io navvisgmbh/navvis.map.vcpkgio.$(GetImageName):latest