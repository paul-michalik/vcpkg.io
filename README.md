# vcpkg.io

Manage bundles created by https://github.com/Microsoft/vcpkg 

The [vcpkg](https://github.com/Microsoft/vcpkg) community is doing a great job to provide a brewing package manager for the Windows platform. However, vcpkg does not directly cover the distribution of compatible bundles of binaries and other artifacts. This is where `vcpkg.io` jumps in. It helps to maintain and to consume pre-built vcpkg artifacts. vcpkg.io consists of one front-end script `vcpkgi.io` which supports few commands to accomplish this task. 

`vcpkg.io pull [url] [--into <name>]`

Pulls (or clones) the master from `[url]` into a folder `vcpkg.io/<name>`. Default is to pull the latest master from https://github.com/Microsoft/vcpkg.git into `vcpkg.io/vcpkg`. Examples:
* `vcpkg.io pull`
* `vcpkg.io pull https://github.com/paul-michalik/vcpkg.git --into vcpkg-paul-michalik`

`vcpkg.io download <revision> [url]` 

Downloads the `[revision]` given by Git commit hash from `[url]` into a folder `vcpkg.io/[revision]`. Default `[url]` is `https://github.com/Microsoft/vcpkg`. Examples:
* `vcpkg.io download f279e9f5e3a569b237dbaca44bbc7225f1d7e27d`
* `vcpkg.io download 240d1d2facc5407fbd002b678f561bfacaccdee7 https://github.com/paul-michalik/vcpkg`  
