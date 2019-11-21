#!/usr/bin/env bash
set -eu

function vcpkg.io.GetCurDir() {
    printf "%s" "$(realpath "$(dirname "${BASH_SOURCE}")")"
}

function vcpkg.io.GetPrjDir() {
    printf "%s" "$(vcpkg.io.GetCurDir)/.."
}

function vcpkg.io.ShowUsage() {
    cat <<EOF
Synopsis: 

    $(basename ${BASH_SOURCE}) [command] [options]

Supported commands:
    help
        Show this text and exit
    configure
        Configure the vcpkg source and version. Use "configure --help" for more information
    docker
        Build the docker image with required build tools. Use "docker --help" for more information 
    bootstrap
        Bootstrap the selected vcpkg source and version. Use "bootstrap --help" for more information
    install
        Install selected packages. Use "install --help" for more information
    export
        Export selected packages in specified format. Use "export --help" for more information
EOF
}

function vcpkg.io.DispatchCommand() {
    echo "$(basename ${BASH_SOURCE})(${LINENO}): ${FUNCNAME}, args="$@""

    if [[ "$#" -lt 1 ]]; then
        local -r command="help"
    elif [[ "$#" -lt 2 ]]; then
        local -r command="${1}"
        local -r commandArgs=()
    else
        local -r command="${1}"
        local -r commandArgs="${@:2}"
    fi
    
    case "${command}" in
        configure)
            echo "$(basename ${BASH_SOURCE})(${LINENO}): \
                "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]} "
            source "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]}
            ;;
        docker)
            echo "$(basename ${BASH_SOURCE})(${LINENO}): \
                "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]} "
            source "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]}
            ;;
        bootstrap)
            echo "$(basename ${BASH_SOURCE})(${LINENO}): \
                "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]} "
            source "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]}
            ;;
        install)
            echo "$(basename ${BASH_SOURCE})(${LINENO}): \
                "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]} "
            source "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]}
            ;;
        export)
            echo "$(basename ${BASH_SOURCE})(${LINENO}): \
                "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]} "
            source "$(vcpkg.io.GetCurDir)/commands/${command}.sh" ${commandArgs[@]}
            ;;
        *)
            vcpkg.io.ShowUsage
            exit 0
            ;;
    esac
}

function vcpkg.io.Main() {
    echo "$(basename ${BASH_SOURCE})(${LINENO}): ${FUNCNAME[@]}"
    vcpkg.io.DispatchCommand "$@"
}

# Invoke main if not explicitly disabled by passing first argument -noexec or --noexec  
if [[ 0 -eq "$#" || 0 -lt "$#" && ! "${1}" =~ ^[-]{1,2}noexec$ ]]; then
    $(basename "${BASH_SOURCE}" .sh).Main "$@"
fi