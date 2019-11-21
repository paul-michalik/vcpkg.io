# vcpkg.io
Manage bundles created by https://github.com/Microsoft/vcpkg the GitOps way. With GitOps your Git repository is the single source of truth. 
* [vcpkg.io](https://github.com/paul-michalik/vcpkg.io) repository is the single source of truth for *your* bundle created from *their* commit of vcpkg
* All changes to the desired state are Git commits. This applies to *your* packages and *their* vcpkg

## Quick start

1. Clone the project 
2. Create and switch to a new branch.
3. Create a configuration: 
   1) Choose your vcpkg version. NOTE: This creates a unique bundle which is guaranteed to contain mutually and transitively consistent set of packages 
   2) Choose the list of packages. NOTE: You can later add packages to the list without braking the compatibility of the bundle
4. Commit current changes
5. Build and export packages
6. Go back to 3.

## Supported commands

```
vcpkg.io configure --commit 2019.10 -- aws-sdk-cpp[batch,s3,sts] 
```

After these steps you have created a configuration which fixes the `vcpkg` commit tag. The set of packages is variable and can be modified in the scope of this specific `vcpkg` commit. The command above will create a new folder in `configurations/2019.10`. The folder contains `configurations/2019.10/invocation.sh` with initial list of packages you have passed via command line or an empty `packages.txt`. You may also create the folder structure manually - in this case running the corresponding statement will only add new packages passed from command line to `packages.txt`.


```
vcpkg.io bootstrap --commit 2019.09 -- aws-sdk-cpp[batch,s3,sts]
```

```
vcpkg.io build --commit 2019.09 -- aws-sdk-cpp[batch,s3,sts]
```

```
vcpkg.io export --commit 2019.09 -- aws-sdk-cpp[batch,s3,sts] protobuf[zlib] boost[MPI]
```

## Environment variables and defaults

* Required:
```
VI_Platform=x64
VI_SystemName=windows
```
* Inferred: 
```
VI_VcPkgDir=~/vcpkg.io/.vcpkg/2019.7.31
VI_Toolset=msvc
VI_VcPkgTriplet=x64-windows
VI_VcPkgCommitHash=3dda86bd2785933485225202a710cde22c3b1ae1
VI_VcPkgVersion=2019.7.31
```