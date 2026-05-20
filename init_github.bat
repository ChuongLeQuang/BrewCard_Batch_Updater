@echo off
chcp 65001 >nul
echo ===================================================
echo     🚀 KHOI TAO VA DAY CODE LEN GITHUB LAN DAU
echo ===================================================
echo.

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
echo ✅ Cai dat Hook thanh cong! Tu gio moi thao tac commit se tu dong cap nhat README va format code.
echo.

echo ⏳ Dang them cac thay doi (git add .)...
git add .

set "default_commit_msg=🚀 Initial commit: Khoi tao du an BrewCard_Batch_Updater"
set /p commit_msg="👉 Nhap noi dung commit lan dau (Enter de dung mac dinh): "
if "%commit_msg%"=="" set "commit_msg=%default_commit_msg%"

git commit -m "%commit_msg%"
git branch -M main

echo.
echo 🔍 Kiem tra GitHub CLI (gh)...
where gh >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Da tim thay GitHub CLI!
    set /p repo_type="👉 Ban muon tao Repo [1] Public hay [2] Private? (1/2, mac dinh=2): "
    set visibility=--private
    if "%repo_type%"=="1" set visibility=--public
    
    echo ⏳ Dang tao repository tren GitHub...
    gh repo create BrewCard_Batch_Updater %visibility% --source=. --remote=origin --push
    echo ✅ Tao va day code len GitHub thanh cong!
    
    echo.
    echo ⏳ Dang tao Tag va GitHub Release v1.0.0...
    git tag v1.0.0
    git push origin v1.0.0
    gh release create v1.0.0 --title "Initial Release v1.0.0" --notes "🚀 Khoi tao du an BrewCard_Batch_Updater bang AI Project Generator"
    echo ✅ Tao GitHub Release v1.0.0 thanh cong!
) else (
    echo ⚠️ KHONG tim thay GitHub CLI (gh). Ban nen cai dat de tu dong hoa buoc nay.
    echo 👉 Hay tao Repository moi tren trang GitHub cua ban (https://github.com/new)
    set /p repo_url="👉 Dan duong dan (URL) GitHub Repository vao day (hoac nhan Enter de bo qua): "
    if not "%repo_url%"=="" (
        git remote add origin %repo_url%
        git push -u origin main
        echo ⏳ Dang tao Tag v1.0.0...
        git tag v1.0.0
        git push origin v1.0.0
        echo ✅ Day code va Tag thanh cong! Ban co the tao Release thu cong tren trang GitHub.
    ) else (
        echo ❌ Ban chua nhap URL. Xin huy thao tac day code lan dau.
    )
)
pause
