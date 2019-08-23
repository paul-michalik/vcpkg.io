#!/usr/bin/env bash
set -e

function convert_path_ConvertPath() {
    local pathToConvert="${1}"
    local osName=$(uname)
    if [[ "${osName,,}" =~ mingw64_nt && -x "$(command -v cygpath)" ]]; then
        printf "/%s" $(cygpath --unix "${pathToConvert}")
    else
        # OK, we're on some sort of native UNIXoid, just a unit transform
        printf "%s" "${pathToConvert}"
    fi
}