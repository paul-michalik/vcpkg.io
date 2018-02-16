# vcpkg.io

Manage bundles created by https://github.com/Microsoft/vcpkg 

The [vcpkg](https://github.com/Microsoft/vcpkg) community is doing a great job to provide a brewing package manager for the Windows platform. However, vcpkg does not directly cover the distribution of compatible bundles of binaries and other artifacts. This is where `vcpkg.io` jumps in. It helps to maintain, deploy and consume pre-built vcpkg artifacts. vcpkg.io consists of one front-end script `vcpkgi.io` which supports few commands to accomplish this task. 

## clone

`vcpkg.io clone [[options] <repository> <directory>]`

Clones from `<repository>` into a folder `<directory>`. Default is to clone from https://github.com/Microsoft/vcpkg.git into `vcpkg.io/vcpkg`. 

Examples:
* `vcpkg.io clone`
* `vcpkg.io clone https://github.com/paul-michalik/vcpkg.git vcpkg-paul-michalik`

Synopsis:

* `git clone https://github.com/paul-michalik/vcpkg.git`



## pull

`vcpkg.io pull <directory>`

Pulls changes from configured upstream into a folder `vcpkg.io/<directory>`. Default `<directory>` is `vcpkg.io/vcpkg`. The export associated with this repository are invalidated.

Examples:
* `vcpkg.io pull`
* `vcpkg.io pull vcpkg-paul-michalik`

Synopsis: 

```
pushd vcpkg
git pull
vcpkg upgrade --no-dry-run
popd
```


## download

`vcpkg.io download <revision> [url]` 

Downloads the `[revision]` given by Git commit hash from `[url]` into a folder `vcpkg.io/[revision]`. Default `[url]` is https://github.com/Microsoft/vcpkg. 

Examples:

* `vcpkg.io download f279e9f5e3a569b237dbaca44bbc7225f1d7e27d`
* `vcpkg.io download 240d1d2facc5407fbd002b678f561bfacaccdee7 https://github.com/paul-michalik/vcpkg`  

Synopsis:
```
Invoke-WebRequest "https://github.com/Microsoft/vcpkg/archive/$CommitTag.zip" -OutFile "$CommitTag.zip"
Expand-Archive "$CommitTag.zip" -DestinationPath "$CommitTag"
```