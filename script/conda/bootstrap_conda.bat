@echo off
setlocal

set "Download_path=%USERPROFILE%\Downloads"
set "mini_conda=%USERPROFILE%\.miniconda"
set "mini_conda_path=%mini_conda%\Scripts"

call :install_conda

endlocal & ^
set "Path=%mini_conda_path%;%Path%"

goto :eof

:install_conda
	set "miniconda_app=Miniconda3-latest-Windows-x86_64.exe"
	set "miniconda_app_path=%Download_path%\Miniconda3-latest-Windows-x86_64.exe"	
	if not exist "%mini_conda%" ( 	
		if not exist "%miniconda_app_path%" (
			echo "downloading miniconda"
			powershell -Command "Invoke-WebRequest https://repo.continuum.io/miniconda/%miniconda_app% -OutFile %miniconda_app_path%"		
			echo "downloading miniconda completed"
		)
		if exist "%miniconda_app_path%" (
			echo "installing miniconda"
			start /wait "" %miniconda_app_path% /InstallationType=JustMe /RegisterPython=0 /S /D=%mini_conda%
			echo "installing miniconda completed"
		)
	)
goto :eof
