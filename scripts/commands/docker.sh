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

    $(basename ${BASH_SOURCE}) [options] --triplet <triplet>

Main options:
    --triplet|-t
        The vcpkg triplet. 
        Default: ${VI_VcPkgTriplet} or content of "VI_VcPkgTriplet" shell variable
EOF
}

function docker.Defaults() {
    if [[ ! -v VI_VcPkgTriplet ]]; then
        declare -g VI_VcPkgTriplet=x64-linux-gcc
    fi
}

function docker.ParseArgs() {
    echo "$(basename ${BASH_SOURCE})(${LINENO}): ${FUNCNAME[@]}, args="$@""

    # Parse arguments begin
    local actArgCount=0 expArgCount=0
    while [[ "$#" -gt 0 ]]; do 
        case "${1}" in
            --help|-h)
                docker.ShowUsage
                exit 0
                ;;
            --triplet|-t)
                VI_VcPkgTriplet="${2}"
                ((actArgCount+=1))
                shift 2;;
            *) # positional arguments
                # ignored
                shift;;
        esac
    done

    if [[ ${actArgCount} -lt ${expArgCount} ]]; then 
        echo "$(basename ${BASH_SOURCE})(${LINENO}): Wrong number of arguments! expected=${expArgCount}, actual=${actArgCount}" >&2
        return 1
    fi
    # Parse arguments end
}

function docker.Build() {
    echo "$(basename ${BASH_SOURCE})(${LINENO}): ${FUNCNAME[@]}, args="$@""
}

function docker.Main() {
    echo "$(basename ${BASH_SOURCE})(${LINENO}): ${FUNCNAME[@]}, args="$@""
    docker.Defaults
    docker.ParseArgs "$@"
    docker.Build "$@"
}

# Invoke main if not explicitly disabled by passing first argument -noexec or --noexec  
if [[ 0 -eq "$#" || 0 -lt "$#" && ! "${1}" =~ ^[-]{1,2}noexec$ ]]; then
    $(basename "${BASH_SOURCE}" .sh).Main "$@"
fi
