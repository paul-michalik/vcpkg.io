@echo off
python -c "import conans"
if %errorlevel% neq 0 (
	echo installing conan,please wait..
	pip install -r vcpkg.io\requirement.txt
	echo conan is installed...
)

call python vcpkg.io\vcpkg.io.py %*


