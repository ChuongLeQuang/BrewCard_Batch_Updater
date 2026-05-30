@echo off
:: Thiết lập bảng mã UTF-8 để hiển thị đúng tiếng Việt và Emoji trong CMD
chcp 65001 >nul

echo ===================================================
echo     🚀 TỰ ĐỘNG ĐẨY CODE LÊN GITHUB (AUTO PUSH)
echo ===================================================
echo.
echo 💡 MẸO: Chon dung loai de he thong tu dong tang Version tren GitHub!
echo   [1] fix  : Sua loi, cap nhat nho (Tang Patch: 1.0.4 -^> 1.0.5)
echo   [2] feat : Tinh nang moi         (Tang Minor: 1.0.4 -^> 1.1.0)
echo   [3] major: Dai tu / Tinh nang lon(Tang Major: 1.0.4 -^> 2.0.0)
echo   [4] Tu go toan bo commit (Tuy chinh)
echo.

set /p type_choice="👉 Chon loai cap nhat [1/2/3/4] (Enter mac dinh = 1): "

set PREFIX=fix(core): 
set BUMP_ARG=--patch
if "%type_choice%"=="2" set PREFIX=feat(core): 
if "%type_choice%"=="2" set BUMP_ARG=--minor
if "%type_choice%"=="3" set PREFIX=feat(core)!: BREAKING CHANGE - 
if "%type_choice%"=="3" set BUMP_ARG=--major
if "%type_choice%"=="4" set PREFIX=
if "%type_choice%"=="4" set BUMP_ARG=--patch

echo.
set PYTHON_CMD=python
if exist ".venv\Scripts\python.exe" set PYTHON_CMD=.venv\Scripts\python.exe

echo 🛡️ Dang chay kịch ban kiem tra tu dong (Auto Checks)...
"%PYTHON_CMD%" auto_checks.py
if %ERRORLEVEL% neq 0 (
    echo ❌ Phat hien loi trong ma nguon! Huy bo qua trinh dong bo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ⏳ Dang cap nhat Version (version.txt)...
"%PYTHON_CMD%" build.py --bump-only %BUMP_ARG%

echo.
set /p desc="👉 Nhap noi dung / mo ta (Enter mac dinh = 'Auto update'): "
if "%desc%"=="" set desc=Auto update

set msg=%PREFIX%%desc%

echo.
echo ===================================================
echo ⏳ Dang them cac thay doi (git add .)...
git add .

echo ⏳ Dang tao commit: "%msg%"
git commit -m "%msg%"

echo ⏳ Dang day len GitHub (git push origin main)...
git push origin main

echo ===================================================
echo ✅ DA DAY CODE THANH CONG!
pause