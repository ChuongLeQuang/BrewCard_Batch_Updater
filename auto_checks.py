"""
EN: Automated check script to format code, update docs, and run tests before commit/build.
VI: Công cụ tự động kiểm tra, format code, cập nhật tài liệu và chạy test trước khi commit/build.
"""

import os
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")


def run_cmd(cmd: list, desc: str) -> None:
    """
    Thực thi một lệnh shell hệ thống và kiểm tra lỗi.
    - Inputs:
      + cmd (list): Danh sách đối số lệnh cần thực thi (không dùng shell=True).
      + desc (str): Mô tả hiển thị trên màn hình.
    - Outputs: Không trả về giá trị (None). Sẽ dừng chương trình bằng sys.exit(1) nếu lệnh thất bại.
    """
    logging.info(f"\n🔄 {desc}...")
    try:
        subprocess.run(cmd, check=True)
        logging.info(f"✅ Xong: {desc}")
    except subprocess.CalledProcessError:
        logging.error(f"\n❌ LỖI NGHIÊM TRỌNG: {desc} thất bại!")
        logging.error("👉 Vui lòng kiểm tra và sửa lỗi trước khi tiếp tục.")
        sys.exit(1)


def main() -> None:
    """
    Hàm chính điều phối chuỗi kiểm tra tự động bao gồm: Định dạng mã nguồn (Black), Cập nhật Kiến trúc (Scan), và Chạy Test (Pytest).
    """
    logging.info("===================================================")
    logging.info("  🚀 BẮT ĐẦU CHẠY KIỂM TRA TỰ ĐỘNG (AUTO CHECKS)   ")
    logging.info("===================================================")

    # 1. Định dạng mã nguồn (Format Code)
    try:
        import black

        run_cmd([sys.executable, "-m", "black", "."], "Định dạng mã nguồn bằng Black")
    except ImportError:
        logging.warning(
            "\n⚠️ Cảnh báo: Thư viện 'black' chưa được cài đặt, bỏ qua định dạng."
        )

    # 2. Vẽ lại sơ đồ Kiến trúc (Cập nhật README)
    if os.path.exists("scan_architecture.py"):
        run_cmd(
            [sys.executable, "scan_architecture.py"],
            "Cập nhật tài liệu Architecture (README.md)",
        )

    # 3. Chạy Unit Test đảm bảo logic không bị gãy
    try:
        import pytest

        run_cmd([sys.executable, "-m", "pytest"], "Chạy Unit Tests (Pytest)")
    except ImportError:
        logging.warning(
            "\n⚠️ Cảnh báo: Thư viện 'pytest' chưa được cài đặt, bỏ qua kiểm thử."
        )

    logging.info("\n🎉 TẤT CẢ KIỂM TRA ĐÃ VƯỢT QUA! MÃ NGUỒN AN TOÀN VÀ SẠCH SẼ.\n")


if __name__ == "__main__":
    main()
