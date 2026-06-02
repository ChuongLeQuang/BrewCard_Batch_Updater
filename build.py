"""
EN: Build script to automate PyInstaller packaging.
VI: Kịch bản tự động hóa quá trình đóng gói ứng dụng bằng PyInstaller.
"""

import os
import sys
import subprocess
import platform
import shutil
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_next_version(file_path: str = "version.txt", bump_type: str = "current") -> str:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            current_version = f.read().strip()
    else:
        current_version = "1.0.0"

    if bump_type == "current":
        return current_version

    parts = current_version.split(".")
    if len(parts) >= 3:
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        if bump_type == "major":
            return f"{major + 1}.0.0"
        elif bump_type == "minor":
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"
    return "1.0.1"


def create_version_file(version: str) -> str:
    parts = version.split(".")
    while len(parts) < 4:
        parts.append("0")
    vers_tuple = f"({parts[0]}, {parts[1]}, {parts[2]}, {parts[3]})"

    content = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(filevers={vers_tuple}, prodvers={vers_tuple}, mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[StringFileInfo([StringTable('040904B0', [
    StringStruct('CompanyName', 'Le Quang Chuong'),
    StringStruct('FileDescription', 'BrewCard_Batch_Updater Tool'),
    StringStruct('FileVersion', '{version}'),
    StringStruct('InternalName', 'BrewCard_Batch_Updater'),
    StringStruct('LegalCopyright', 'Copyright (c) 2026 Le Quang Chuong'),
    StringStruct('OriginalFilename', 'BrewCard_Batch_Updater.exe'),
    StringStruct('ProductName', 'BrewCard_Batch_Updater'),
    StringStruct('ProductVersion', '{version}')])]), 
  VarFileInfo([VarStruct('Translation', [1033, 1200])])]
)"""
    file_path = "version_info.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


def clean_pycache(start_path: str = ".") -> None:
    logging.info("🧹 Đang dọn dẹp các thư mục __pycache__...")
    count = 0
    for root, dirs, files in os.walk(start_path, topdown=False):
        for name in dirs:
            if name == "__pycache__":
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path)
                    count += 1
                except OSError:
                    pass  # Bỏ qua nếu file đang bị khóa
    if count > 0:
        logging.info(f"✨ Đã xóa thành công {count} thư mục __pycache__.")


def clean_logs(start_path: str = ".") -> None:
    logs_dir = os.path.join(start_path, "logs")
    if os.path.exists(logs_dir):
        logging.info("🧹 Đang dọn dẹp các file log cũ...")
        count = 0
        for f in os.listdir(logs_dir):
            if f.endswith(".log"):
                try:
                    os.remove(os.path.join(logs_dir, f))
                    count += 1
                except OSError:
                    pass  # Bỏ qua nếu file đang bị khóa
        if count > 0:
            logging.info(f"✨ Đã xóa thành công {count} file log.")


def clean_temp_files(start_path: str = ".") -> None:
    logging.info("🧹 Đang dọn dẹp các file tạm (.env, .sqlite)...")
    count = 0
    for root, dirs, files in os.walk(start_path):
        if ".venv" in root or ".git" in root:
            continue
        for f in files:
            if f == ".env" or f.endswith(".sqlite") or f.endswith(".sqlite3"):
                try:
                    os.remove(os.path.join(root, f))
                    count += 1
                except OSError:
                    pass  # Bỏ qua nếu bị khóa
    if count > 0:
        logging.info(f"✨ Đã xóa thành công {count} file tạm.")


def ensure_init_files() -> None:
    for base_dir in ["src", "apps", "shared", "core"]:
        if os.path.exists(base_dir):
            for root, dirs, files in os.walk(base_dir):
                init_file = os.path.join(root, "__init__.py")
                if not os.path.exists(init_file):
                    with open(init_file, "w", encoding="utf-8") as f:
                        pass


def build_app() -> None:
    if "--bump-only" in sys.argv:
        bump_type = "patch"
        if "--major" in sys.argv:
            bump_type = "major"
        elif "--minor" in sys.argv:
            bump_type = "minor"
        new_version = get_next_version(bump_type=bump_type)
        with open("version.txt", "w", encoding="utf-8") as f:
            f.write(new_version)
        logging.info(f"✅ Đã cập nhật version.txt lên: {new_version}")
        sys.exit(0)

    logging.info("🚀 Khởi động quá trình đóng gói ứng dụng...")
    try:
        import PyInstaller
    except ImportError:
        logging.error(
            "\n❌ Không tìm thấy thư viện 'pyinstaller'. Vui lòng chạy pip install pyinstaller"
        )
        sys.exit(1)

    for old_dir in ["build", "dist"]:
        if os.path.exists(old_dir):
            shutil.rmtree(old_dir, ignore_errors=True)

    clean_pycache()
    clean_logs()
    clean_temp_files()
    ensure_init_files()

    if os.path.exists("auto_checks.py"):
        logging.info("🔍 Đang chạy các kịch bản kiểm tra tự động (Auto Checks)...")
        try:
            subprocess.run([sys.executable, "auto_checks.py"], check=True)
        except subprocess.CalledProcessError:
            logging.error(
                "❌ LỖI: Auto Checks thất bại. Vui lòng sửa mã nguồn trước khi đóng gói."
            )
            sys.exit(1)

    bump_type = "current"
    if "--major" in sys.argv:
        bump_type = "major"
    elif "--minor" in sys.argv:
        bump_type = "minor"
    elif "--patch" in sys.argv:
        bump_type = "patch"

    new_version = get_next_version(bump_type=bump_type)
    logging.info(f"📌 Phiên bản chuẩn bị build: {new_version}")

    app_name = "BrewCard_Batch_Updater"
    entry_point = "main.py"
    icon_path_ico = os.path.join("assets", "icon.ico")
    icon_path_png = os.path.join("assets", "icon.png")
    separator = os.pathsep

    pyinstaller_args = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        f"--name={app_name}",
        "--paths=.",
    ]

    if (
        not os.path.exists(icon_path_ico)
        and os.path.exists(icon_path_png)
        and platform.system() == "Windows"
    ):
        try:
            from PIL import Image

            img = Image.open(icon_path_png)
            # Tạo file .ico chứa nhiều độ phân giải để Windows hiển thị sắc nét ở mọi kích cỡ
            img.save(
                icon_path_ico,
                format="ICO",
                sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
            )
            logging.info("🎨 Đã tự động chuyển đổi icon.png sang icon.ico thành công!")
        except ImportError:
            logging.warning(
                "⚠️ Thư viện 'Pillow' chưa cài đặt, phần mềm sẽ dùng icon mặc định của Windows cho file exe."
            )
        except OSError as e:
            logging.warning(f"⚠️ Không thể chuyển đổi icon: {e}")

    if os.path.exists(icon_path_ico):
        pyinstaller_args.append(f"--icon={icon_path_ico}")
    elif os.path.exists(icon_path_png) and platform.system() != "Windows":
        pyinstaller_args.append(f"--icon={icon_path_png}")

    for extra in ["assets", "templates", "static"]:
        if os.path.exists(extra):
            pyinstaller_args.append(f"--add-data={extra}{separator}{extra}")

    old_version = "1.0.0"
    if os.path.exists("version.txt"):
        with open("version.txt", "r", encoding="utf-8") as f:
            old_version = f.read().strip()

    with open("version.txt", "w", encoding="utf-8") as f:
        f.write(new_version)

    if os.path.exists("version.txt"):
        pyinstaller_args.append(f"--add-data=version.txt{separator}.")

    if platform.system() == "Windows":
        version_file = create_version_file(new_version)
        pyinstaller_args.append(f"--version-file={version_file}")

    pyinstaller_args.append(entry_point)

    try:
        subprocess.run(pyinstaller_args, check=True)
        logging.info(f"\n✅ Đóng gói thành công '{app_name}'!")
        if platform.system() == "Windows" and os.path.exists("version_info.txt"):
            os.remove("version_info.txt")
        if os.path.exists(f"{app_name}.spec"):
            os.remove(f"{app_name}.spec")
        if os.path.exists("build"):
            shutil.rmtree("build")
    except subprocess.CalledProcessError as e:
        with open("version.txt", "w", encoding="utf-8") as f:
            f.write(old_version)
        logging.error(f"\n❌ Có lỗi xảy ra: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_app()
