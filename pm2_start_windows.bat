@echo off
setlocal
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual ausente. Execute source_start_windows.bat uma vez.
    pause
    exit /b 1
)

"venv\Scripts\python.exe" -c "import aiofiles, disnake, dotenv; from utils.client import BotPool" >nul 2>nul
if errorlevel 1 (
    echo [ERRO] O ambiente Python precisa ser reparado. Execute source_start_windows.bat uma vez.
    pause
    exit /b 1
)

call pm2 start ecosystem.config.cjs --only lukes-saber
if errorlevel 1 goto :failure

call pm2 save
if errorlevel 1 goto :failure

call pm2 status lukes-saber
echo.
echo Luke's Saber foi iniciado e salvo no PM2.
pause
exit /b 0

:failure
echo.
echo [ERRO] O PM2 nao conseguiu iniciar ou salvar o processo.
pause
exit /b 1
