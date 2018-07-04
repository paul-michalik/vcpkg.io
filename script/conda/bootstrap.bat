@echo off
setlocal
set "Platform=x64"
set "Toolset=v141"
set "BuildType=Release"

if NOT "%~1"=="" set "Platform=%~1"
if NOT "%~2"=="" set "Toolset=%~2"
if NOT "%~3"=="" set "BuildType=%~3"

rem ----------------------------------
rem Locate vcpkg using environment variables
rem ----------------------------------
set "VcPkgDir=%USERPROFILE%\.vcpkg\vcpkg"
set "VcPkgTriplet=%Platform%-windows"
if defined VCPKG_ROOT_DIR if /i not "%VCPKG_ROOT_DIR%"=="" set "VcPkgDir=%VCPKG_ROOT_DIR%"
if defined VCPKG_DEFAULT_TRIPLET if /i not "%VCPKG_DEFAULT_TRIPLET%"=="" set "VcPkgTriplet=%VCPKG_DEFAULT_TRIPLET%"

rem ----------------------------------
rem Try to look for vcpkg at default locations
rem ----------------------------------
if not exist "%VcPkgDir%" set "VcPkgDir=%~d0\Software\vcpkg\vcpkg"
if not exist "%VcPkgDir%" set "VcPkgDir=%~d0\.vcpkg\vcpkg"
if not exist "%VcPkgDir%" set "VcPkgDir=C:\Software\vcpkg\vcpkg"
if not exist "%VcPkgDir%" set "VcPkgDir=C:\.vcpkg\vcpkg"
if not exist "%VcPkgDir%" set "VcPkgDir=%USERPROFILE%\.vcpkg\vcpkg"
if not exist "%VcPkgDir%" (
    echo vcpkg not found, installing at %VcPkgDir%...
    git clone --recursive https://github.com/Microsoft/vcpkg.git "%VcPkgDir%"
) 
    
echo vcpkg at %VcPkgDir%...

rem
rem Check whether we have a difference in the toolsrc folder. If non empty, %errorlevel% should be 0  
rem git --no-pager diff --name-only origin/HEAD remotes/origin/HEAD | find "toolsrc/" > NUL & echo %errorlevel%
rem Check whether changes was made between local commit an remotes/origin/HEAD in toolsrc\VERSION.txt
rem 
rem git --no-pager diff --name-only 15e4f46b45c432a41ee6a962609039bc2497ec19 remotes/origin/HEAD -- toolsrc\VERSION.txt

rem ----------------------------------
rem Using version 0.0.108 (toolsrc/VERSION.txt)
rem ----------------------------------
set "VcPkgCommit=15e4f46b45c432a41ee6a962609039bc2497ec19"
set "VcPkgCommitLock=bootstrap-vcpkg-%VcPkgCommit%"
call
pushd "%VcPkgDir%"
git fetch origin %VcPkgCommit%
git checkout FETCH_HEAD
popd

rem ==============================
rem Upgrade and Install packages.
rem ==============================
set "VcPkgDeps=opencv[ffmpeg] boost-filesystem boost-property-tree"
call :BootstrapVcPkgExe
call "%VcPkgDir%\vcpkg.exe" upgrade %VcPkgDeps% --no-dry-run --triplet %VcPkgTriplet%
call "%VcPkgDir%\vcpkg.exe" install %VcPkgDeps% --triplet %VcPkgTriplet%

rem ==============================
rem temporary hack to copy opencv_ffmpeg dlls until this is solved in vcpkg
rem ==============================
if not exist "%~dp0..\..\products" mkdir "%~dp0..\..\products"
echo xcopy "%VcPkgDir%\installed\%VcPkgTriplet%\bin\opencv_ffmpeg*.dll" "%%~1/" /y /f > "%~dp0..\..\products\copy_ffmpeg.bat"
echo xcopy "%VcPkgDir%\installed\%VcPkgTriplet%\debug\bin\opencv_ffmpeg*.dll" "%%~1/" /y /f > "%~dp0..\..\products\copy_ffmpegd.bat"

endlocal & ^
set "VcPkgDir=%VcPkgDir%" & ^
set "VcPkgTriplet=%VcPkgTriplet%" & ^
set "Platform=%Platform%" & ^
set "Toolset=%Toolset%" & ^
set "Platform=%Platform%" & ^
set "BuildType=%BuildType%"

goto :eof

:BootstrapVcPkgExe
    call :RemoveBootstrappingLocks
    if not exist "%VcPkgDir%\%VcPkgCommitLock%.lock" (
        call "%VcPkgDir%\bootstrap-vcpkg.bat" & echo %VcPkgCommit% > "%VcPkgDir%\%VcPkgCommitLock%.lock"
    )

goto :eof

rem ---------------------------------- 
rem Remove all bootstrap lock files NOT matching current commit tag:
rem ----------------------------------
:RemoveBootstrappingLocks
    rem powershell.exe -NoProfile -ExecutionPolicy Bypass -command "Remove-Item ^"%VcPkgDir%^" -Include *.tag.txt -Exclude *%VcPkgCommit%.tag.txt"
    for /f "tokens=*" %%F in ('dir /b /s ^"%VcPkgDir%\*.lock^"') do (
        if /i not "%%~nF%%~xF"=="%VcPkgCommitLock%.lock" (
            del /q "%%F"
        )
    )

goto :eof
