@echo off
chcp 65001 >nul
echo ===================================================
echo     🚀 KET NOI LAI VOI GITHUB REPO CO SAN
echo ===================================================
echo.

echo ⏳ Dang cap quyen thu muc an toan cho Git...
git config --global --add safe.directory "*"

if not exist ".git" (
    echo ⏳ Dang khoi tao Git repository...
    git init
)

echo ⏳ Dang cai dat Git Pre-commit Hook...
if not exist ".git\hooks" mkdir ".git\hooks"
(
echo #!/bin/sh
echo echo "🛡️ Dang chay Git Pre-commit Hook..."
echo PYTHON_CMD="python"
echo if [ -f ".venv/Scripts/python.exe" ]; then PYTHON_CMD=".venv/Scripts/python.exe"; elif [ -f ".venv/bin/python" ]; then PYTHON_CMD=".venv/bin/python"; fi
echo $PYTHON_CMD auto_checks.py
echo if [ $? -ne 0 ]; then echo "❌ Phat hien loi! Huy bo commit."; exit 1; fi
echo git add README.md
echo git add -u
echo exit 0
) > ".git\hooks\pre-commit"

echo ⏳ Dang them cac thay doi...
git add .
git commit -m "🚀 Phuc hoi va hoan thien toan dien du an"
git branch -M main

echo.
set /p repo_url="👉 Dan duong dan (URL) GitHub Repository CU cua ban vao day (VD: https://github.com/user/BrewCard...): "
if not "%repo_url%"=="" (
    git remote remove origin 2>nul
    git remote add origin %repo_url%
    echo ⏳ Dang day code len GitHub - Ghi de / Force Push de cap nhat...
    git push -u origin main --force
    echo ✅ Ket noi va day code thanh cong! Tu gio ban co the dung chuc nang Sync nhu binh thuong.
) else (
    echo ❌ Ban chua nhap URL.
)
pause