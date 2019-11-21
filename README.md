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
5. Build packages
6. Commit current changes 


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