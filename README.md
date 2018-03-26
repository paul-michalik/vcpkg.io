# vcpkg.io
Manage vcpkg artifacts

## Run

**using conda**
cd script/conda
`vcpkg.io.bat execute <yml file path>`
**using pip**
cd script/pip
`vcpkg.io.bat execute <yml file path>`
**example**
for downloading
`vcpkg.io.bat execute ..\..\vcpkg_download_bin.yml`
for uploading
`vcpkg.io.bat execute ..\..\vcpkg_upload_bin.yml`

## Scope
1. The intention is not create very neat design for vcpkg binary artifacts management.
2. The end user can upload and download vcpkg binaries for their application.
3. it should support continuous integration. 
4. It was designed so that producer of vcpkg binaries and consumer of vcpkg binaries can work independently.
5. It was also designed so that any remote client can be plug-in for uploading and downloading vcpkg binaries.
6. currently remote client conan is provided.

## Feature
1. it support uploading/download vcpkg binaries to/from bintray through conan
2. it provides setting file which can be customized based on specific requirement.
3. it is also not specific to conan , anybody can use different remote client e.g nuget for uploading and downloading binaries.
4. it supports bundle based artifacts which means a bundle can comprise of many vcpkg packages.
6. it also support merging downloaded bundles to single bundle.
6. it also support importing downloaded bundles to the existing vcpkg.
7. unique_id should be define to make sure of bundle compatibility. currently commit_id is provided as unique_id
8. vcpkg.io has 3 main tools: git_tools,vcpkg_tools and remote_tools which can be used independently.

## Settings
The Setting file can be provided to configure remote server and vcpkg.
sample `vcpkg_download_bin.yml` and `vcpkg_upload_bin.yml` is provided in the root which can be used as reference for downloading and uploading bundles.
- vcpkg_download_bin.yml can be used for downloading a bundle
- vcpkg_upload_bin.yml can be used for uploading a bundle
