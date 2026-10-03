@echo off
title Vyoma ^| AI With A Soul
cd /d "%~dp0"

if exist "venv\Scripts\streamlit.exe" (
    echo Starting Vyoma with the project environment...
    "venv\Scripts\streamlit.exe" run app.py
) else (
    echo Project venv not found - trying the system Python...
    python -m streamlit run app.py
)

echo.
echo Vyoma has stopped. Press any key to close this window.
pause >nul
