@echo off
chcp 65001 >nul
echo ===================================================
echo       🛡️ CHẠY KIỂM TRA TỰ ĐỘNG (AUTO CHECKS)
echo ===================================================
echo.
set PYTHON_CMD=python
if exist ".venv\Scripts\python.exe" set PYTHON_CMD=.venv\Scripts\python.exe

"%PYTHON_CMD%" auto_checks.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ KIEM TRA THAT BAI! Vui long sua loi trong ma nguon.
) else (
    echo.
    echo ✅ KIEM TRA HOAN TAT. Ma nguon an toan va sach se!
)
pause