@echo off
setlocal
cd /d "%~dp0"

set "VENV_PY=venv\Scripts\python.exe"

if exist "%VENV_PY%" (
    "%VENV_PY%" --version >nul 2>nul
    if errorlevel 1 (
        echo [Luke's Saber] O ambiente virtual aponta para um Python removido.
        echo [Luke's Saber] Reconstruindo o ambiente...
        ren venv venv_broken_%RANDOM%
    )
)

if not exist "%VENV_PY%" (
    py -3 --version >nul 2>nul
    if errorlevel 1 (
        echo.
        echo [ERRO] Python 3 nao foi encontrado.
        echo Instale Python 3.11 ou mais recente e execute este arquivo novamente.
        echo https://www.python.org/downloads/windows/
        pause
        exit /b 1
    )
    py -3 -m venv venv
    if errorlevel 1 goto :failure
    "%VENV_PY%" -m ensurepip --upgrade
    if errorlevel 1 goto :failure
    "%VENV_PY%" -m pip install --upgrade pip
    "%VENV_PY%" -m pip install -r requirements.txt
    if errorlevel 1 goto :failure
)

"%VENV_PY%" -c "import aiofiles, disnake, dotenv; from utils.client import BotPool" >nul 2>nul
if errorlevel 1 (
    echo [Luke's Saber] Dependencias ausentes. Reparando a instalacao...
    "%VENV_PY%" -m pip --version >nul 2>nul
    if errorlevel 1 (
        echo [Luke's Saber] Pip ausente. Restaurando o instalador de pacotes...
        "%VENV_PY%" -m ensurepip --upgrade
        if errorlevel 1 goto :failure
    )
    "%VENV_PY%" -m pip install --force-reinstall -r requirements.txt
    if errorlevel 1 goto :failure
)

"%VENV_PY%" main.py
pause
exit /b %errorlevel%

:failure
echo.
echo [ERRO] Nao foi possivel preparar o ambiente do Luke's Saber.
pause
exit /b 1
