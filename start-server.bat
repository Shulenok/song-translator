@echo off
chcp 65001 >nul
title Song Analyzer
cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
  echo Python not found. Install from https://python.org
  pause
  exit /b
)

REM Kill any existing server on port 8080
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1

REM Open browser after 2s
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8080/lyrics-translator.html"

REM Start server once
python server.py
pause