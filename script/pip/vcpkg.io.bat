@echo off
python -c "import conans"
if %errorlevel% neq 0 (
	echo installing conan,please wait..
	pip install -r vcpkg.io\requirement.txt
	echo conan is installed...
)

set "VCPKG_USERNAME=NOT_YET_SET" 
set "VCPKG_API_KEY=NOT_YET_SET"

if /i "%VCPKG_USERNAME%"=="NOT_YET_SET" (
	echo "uploading/downloading will be failed as VCPKG_USERNAME is not set !!!"
)

if /i "%VCPKG_API_KEY%"=="NOT_YET_SET" (
	echo "uploading/downloading will be failed as VCPKG_API_KEY is not set !!!"
)

call python ..\..\vcpkg.io\vcpkg.io.py %*
