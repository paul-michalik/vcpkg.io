@echo off
call conda --version 2> nul
if %errorlevel% neq 0 (
	echo installing conda
	call "%~dp0bootstrap_conda.bat"
)

call conda env create -f conan_dep.yml
call activate conan_dep || echo Activation vcpkg_io Failed

call python ..\..\vcpkg.io\vcpkg.io.py %*
call deactivate