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

. "$(GetPrjDir)/scripts/internal/convert_path.sh"

docker run --rm -it --name $(GetImageName) -v "$(convert_path_ConvertPath "$(GetPrjDir)")":/wrk/vcpkg.io -w $(convert_path_ConvertPath /wrk/vcpkg.io) navvisgmbh/navvis.map.vcpkgio.$(GetImageName):latest