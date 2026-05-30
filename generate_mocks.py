"""
EN: Helper script to generate mock Excel files for E2E testing.
VI: Script hỗ trợ tạo các file Excel giả lập phục vụ kiểm thử E2E.
"""

import os
import openpyxl
from datetime import datetime


def generate_mocks():
    os.makedirs("tests/test_data", exist_ok=True)

    # 1. TẠO FILE TỔNG (MASTER)
    master_path = "tests/test_data/mock_master.xlsx"
    wb_master = openpyxl.Workbook()
    ws_master = wb_master.active
    ws_master.title = "BrewSync"
    ws_master.append(["Batch", "Grist/Water Ratio", "Mash-In Time"])
    ws_master.append(["B9999", 0.15, 60])  # Dòng dữ liệu cũ
    wb_master.save(master_path)
    print(f"✅ Đã tạo: {master_path}")

    # 2. TẠO FILE INPUT HOÀN HẢO (CLEAN)
    clean_path = "tests/test_data/mock_input_clean.xlsx"
    wb_clean = openpyxl.Workbook()
    ws_clean = wb_clean.active
    ws_clean.title = "Sheet1"

    # Vân tay và Số lô
    ws_clean["D3"] = "Order: 123"
    ws_clean["G3"] = "Batch: 10295"
    ws_clean["I3"] = "Date: 2024-03-20"
    ws_clean["H3"] = "10295"

    # Số liệu tính toán chuẩn xác
    ws_clean["E10"] = 100.0
    ws_clean["L15"] = 20.0
    ws_clean["L9"] = 50.0
    ws_clean["K10"] = 10.0
    ws_clean["F36"] = datetime(2024, 3, 20, 8, 0)
    ws_clean["F40"] = datetime(2024, 3, 20, 9, 30)

    # Bơm dữ liệu cho các ô đóng vai trò mẫu số (để tránh lỗi #DIV/0!)
    ws_clean["E9"] = 100.0
    ws_clean["E58"] = 100.0
    ws_clean["E78"] = 100.0
    ws_clean["E65"] = 100.0
    ws_clean["E97"] = 100.0

    # Bơm dữ liệu cho các ô đóng vai trò tử số (để số liệu đẹp)
    ws_clean["L8"] = 50.0
    ws_clean["E57"] = 50.0
    ws_clean["E83"] = 50.0
    ws_clean["D82"] = 50.0
    ws_clean["E99"] = 50.0

    wb_clean.save(clean_path)
    print(f"✅ Đã tạo: {clean_path}")

    # 3. TẠO FILE INPUT DỊ THƯỜNG (DIRTY)
    dirty_path = "tests/test_data/mock_input_dirty.xlsx"
    wb_dirty = openpyxl.Workbook()
    ws_dirty = wb_dirty.active
    ws_dirty.title = "Sheet1"

    ws_dirty["H3"] = "10296"  # Số lô mới
    ws_dirty["E10"] = 0.0  # Cố tình gán = 0 để gây lỗi #DIV/0!
    ws_dirty["L15"] = 20.0
    ws_dirty["L9"] = 50.0
    ws_dirty["F36"] = datetime(2024, 3, 21, 8, 0)
    ws_dirty["F40"] = "Not a time"  # Cố tình điền chữ để gây lỗi #VALUE! / TypeError
    wb_dirty.save(dirty_path)
    print(f"✅ Đã tạo: {dirty_path}")


if __name__ == "__main__":
    generate_mocks()
