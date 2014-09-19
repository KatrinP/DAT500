@echo off
setlocal enabledelayedexpansion

set VENDOR_DIR=.\vendor
set GITHUB=github.com
set HTTP=https
set GIT=git

MKDIR "%VENDOR_DIR%" 2>&1 > NUL
::if [ $? -ne 0 ]
::xthen
::	# directory exists, we don't care
::fi

set PACKAGES=( KatrinP/Language-recognition )

for %%i in %PACKAGES% do (
	for /F "delims=/= tokens=1" %%j in ('echo %%i') do (
		set USERNAME = %%j
	)
	for /F "delims=/= tokens=2" %%j in ('echo %%i') do (
		set PACKAGE = %%j
	)

	echo Installing package %PACKAGE% from %USERNAME%
	MKDIR "%VENDOR_DIR%"\\"%USERNAME%"\\"%PACKAGE%" 2>&1 > NUL
	"%GIT%" clone "%HTTP%"://"%GITHUB%"/"%USERNAME%"/"%PACKAGE%" "%VENDOR_DIR%"\\"%USERNAME%"\\"%PACKAGE%"

	SET _PYTHON_PATH = %_PYTHON_PATH%:"%VENDOR_DIR%"\\"%USERNAME%"\\"%PACKAGE%" > NUL
	SETX _PYTHON_PATH %_PYTHON_PATH%:"%VENDOR_DIR%"\\"%USERNAME%"\\"%PACKAGE%" > NUL
	echo Autoload generated
)





::if [ $? -ne 0 ]
::then
::	echo "Fatal error."
::	exit 1
::fi
