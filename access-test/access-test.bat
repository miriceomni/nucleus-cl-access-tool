@echo off

setlocal

pushd "%~dp0"

::
::  Change this line to point to the downloaded (and built)
::  Client library root dir. 
::
set CLIENT_LIB_SDK_DIR=C:\omniverse\nucleus-cl-access-tool\connect-sdk\connect-samples-205.0.0\

set USD_LIB_DIR=%CLIENT_LIB_SDK_DIR%\_build\windows-x86_64\release
set PYTHON=%CLIENT_LIB_SDK_DIR%\_build\target-deps\python\python.exe

set PATH=%PATH%;%USD_LIB_DIR%
set PYTHONPATH=%USD_LIB_DIR%\python;%USD_LIB_DIR%\bindings-python

if not exist "%PYTHON%" (
    echo Python, USD, and Omniverse Client libraries are missing.  Run "repo.bat build --stage" to retrieve them.
    popd
    exit /b
)

"%PYTHON%" --version
"%PYTHON%" access-test.py %*

popd

EXIT /B %ERRORLEVEL%
