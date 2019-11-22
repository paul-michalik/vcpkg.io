#!/usr/bin/env bash
set -eu

function configure.GetCurDir() {
    printf "%s" "$(realpath "$(dirname "${BASH_SOURCE}")")"
}

function configure.GetPrjDir() {
    printf "%s" "$(realpath "$(configure.GetCurDir)/../..")"
}

function configure.ShowUsage() {
    cat <<EOF
Synopsis: 

    $(basename ${BASH_SOURCE}) [options] --url <url> --commit <tag|version> --triplet <triplet> <--> <package names>

Main options:
    --url|-u
        Url of the vcpkg repository 
        Default: ${VI_VcPkgUrls} or content of "VI_VcPkgUrl" shell variable
    --commit|-c
        Commit tag of the required version or version number of a release
        Default: "2019.10" or content of "VI_VcPkgCommit" shell variable
    --triplet|-t
        The vcpkg triplet. 
        Default: ${VI_VcPkgTriplet} or content of "VI_VcPkgTriplet" shell variable
    -- All positional arguments following "--" are interpreted as package names in vcpkg supported format including features
        Default: Empty or content "VI_VcPkgPackages" shell variable array
EOF
}

function configure.Defaults() {
    # Support grabbing values from environment or shell variables
    if [[ ! -v VI_VcPkgUrl ]]; then
        declare -g VI_VcPkgUrls=https://github.com/microsoft/vcpkg
    fi

    if [[ ! -v VI_VcPkgCommit ]]; then
        declare -g VI_VcPkgCommit=2019.10
    fi

    if [[ ! -v VI_VcPkgDir ]]; then
        declare -g VI_VcPkgDir="$(configure.GetPrjDir)/.vcpkg"
    fi

    if [[ ! -v VI_VcPkgTriplet ]]; then
        declare -g VI_VcPkgTriplet=x64-linux
    fi

    if [[ ! -v VI_VcPkgPackages ]]; then
        declare -g VI_VcPkgPackages=()
    fi

    if [[ ! -v VI_VcPkgPackagesHash ]]; then
        declare -g VI_VcPkgPackagesHash=""
    fi

    if [[ ! -v VI_VcPkgConfigDir ]]; then
        declare -g VI_VcPkgConfigDir="$(configure.GetPrjDir)/configurations"
    fi
}

function configure.ParseArgs() {
    echo "$(basename ${BASH_SOURCE})(${LINENO}): ${FUNCNAME[@]}, args="$@""

    # Parse arguments begin
    local actArgCount=0 expArgCount=0
    while [[ "$#" -gt 0 ]]; do 
        case "${1}" in
            --help|-h)
                configure.ShowUsage
                exit 0
                ;;
            --url|-u)
                VI_VcPkgUrls="${2}"
                ((actArgCount+=1))
                shift 2;;
            --commit|-c)
                VI_VcPkgCommit="${2}"
                ((actArgCount+=1))
                shift 2;;
            --triplet|-t)
                VI_VcPkgTriplet="${2}"
                ((actArgCount+=1))
                shift 2;;
            --) # package list
                VI_VcPkgPackages=(${@:2})
                ((actArgCount+=${#VI_VcPkgPackages[@]}))
                # consume all remaining arguments
                break;;
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

function configure.ProcessPackages() {
    if [[ 0 -lt ${#VI_VcPkgPackages[@]} ]]; then
        # Sort the package list
        IFS=$'\n' VI_VcPkgPackages=($(sort <<<"${VI_VcPkgPackages[*]}")); unset IFS

        # Calculate hash of the sorted package list
        local -r hashValue=($(echo -n "${VI_VcPkgPackages[@]}" | md5sum))
        VI_VcPkgPackagesHash=${hashValue[0]}
    fi
}

function configure.WriteConfiguration() {
    echo "$(basename ${BASH_SOURCE})(${LINENO}): ${FUNCNAME[@]}, args="$@""

    # directory for this configuration
    if [[ ! -e "${VI_VcPkgConfigDir}/${VI_VcPkgCommit}" ]]; then
        mkdir -p "${VI_VcPkgConfigDir}/${VI_VcPkgCommit}"
    fi


    configure.ProcessPackages

    if [[ 0 -lt ${#VI_VcPkgPackages[@]} ]]; then
        # add current packages to package list if combination does not already exist: 
        if [[ ! -e "${VI_VcPkgConfigDir}/${VI_VcPkgCommit}/packages.${VI_VcPkgPackagesHash}.txt" ]]; then
            printf " %s" ${VI_VcPkgPackages[@]} >> "${VI_VcPkgConfigDir}/${VI_VcPkgCommit}/packages.${VI_VcPkgPackagesHash}.txt"
        fi
    fi
}

function configure.Main() {
    echo "$(basename ${BASH_SOURCE})(${LINENO}): ${FUNCNAME[@]}, args="$@""
    configure.Defaults
    configure.ParseArgs "$@"
    configure.WriteConfiguration
}

# Invoke main if not explicitly disabled by passing first argument -noexec or --noexec  
if [[ 0 -eq "$#" || 0 -lt "$#" && ! "${1}" =~ ^[-]{1,2}noexec$ ]]; then
    $(basename "${BASH_SOURCE}" .sh).Main "$@"
fi