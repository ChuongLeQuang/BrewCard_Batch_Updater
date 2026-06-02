import json
import glob
import os


def guess_format(name: str) -> str:
    nl = name.lower()
    if "%" in nl or "ratio" in nl or "evap" in nl:
        return "📊 Phần trăm (0.00%)"
    if "°c" in nl or "temp" in nl:
        return "🧮 Số thập phân (1)"
    if (
        "hl" in nl
        or "plato" in nl
        or "kg" in nl
        or "ebc" in nl
        or "ph" in nl
        or "index" in nl
        or "bar" in nl
    ):
        return "🧮 Số thập phân (2)"
    if "min" in nl:
        return "🔢 Số nguyên"
    if "time in" in nl or "time out" in nl or "start of" in nl or "end of" in nl:
        return "⏰ Ngày & Giờ (dd/mm/yyyy hh:mm)"
    if "day" in nl or "date" in nl:
        return "📅 Ngày (dd/mm/yyyy)"
    return "📝 Mặc định"


def run_migration():
    profiles = glob.glob("data/profiles/*.json")
    for path in profiles:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for mapping in data.get("mappings", []):
            t_name = mapping.get("target_col", "")
            fmt = guess_format(t_name)
            mapping["format_type"] = fmt

            # Xóa các đuôi *100 hoặc /100 dư thừa cho cột Phần trăm
            if fmt == "📊 Phần trăm (0.00%)":
                src = mapping.get("source_mapping", "")
                mapping["source_mapping"] = src.replace("*100", "").replace("/100", "")

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Đã cập nhật thành công: {path}")


if __name__ == "__main__":
    run_migration()
