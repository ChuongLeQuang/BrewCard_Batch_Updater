@echo off
:: Thiết lập bảng mã UTF-8 để hiển thị đúng tiếng Việt trong CMD
chcp 65001 >nul

echo ===================================================
echo       📦 TỰ ĐỘNG ĐÓNG GÓI ỨNG DỤNG (BUILD .EXE)
echo ===================================================
echo.
echo Chon loai cap nhat phien ban truoc khi build:
echo   [0] Khong cap nhat (Giu nguyen hien tai)
echo   [1] Patch (Sua loi nho)
echo   [2] Minor (Tinh nang moi)
echo   [3] Major (Dai tu lon)
echo.

set /p choice="👉 Nhap lua chon (0/1/2/3) hoac nhan Enter de Giu nguyen: "

set BUMP_FLAG=--current
if "%choice%"=="1" set BUMP_FLAG=--patch
if "%choice%"=="2" set BUMP_FLAG=--minor
if "%choice%"=="3" set BUMP_FLAG=--major

echo.
set PYTHON_CMD=python
if exist ".venv\Scripts\python.exe" set PYTHON_CMD=.venv\Scripts\python.exe

echo ⏳ Dang khoi dong kien truc PyInstaller...
"%PYTHON_CMD%" build.py %BUMP_FLAG%

echo.
pause