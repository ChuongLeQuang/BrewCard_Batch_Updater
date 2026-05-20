"""
EN: Script to automatically scan the project directory and generate an architecture report.
VI: Script tự động quét thư mục dự án và sinh báo cáo kiến trúc.
"""

import os
import ast
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")


def get_directory_tree(start_path: str, exclude_dirs: set = None) -> str:
    """Sinh cây thư mục (bỏ qua các thư mục không cần thiết)."""
    if exclude_dirs is None:
        exclude_dirs = {
            ".git",
            ".venv",
            "__pycache__",
            "build",
            "dist",
            "node_modules",
            ".vscode",
        }

    tree_str = f"📦 {os.path.basename(os.path.abspath(start_path))}\n"
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        if level > 0:
            tree_str += f"{indent}┣ 📂 {os.path.basename(root)}\n"
        subindent = " " * 4 * (level + 1)
        for f in files:
            tree_str += f"{subindent}┣ 📜 {f}\n"
    return tree_str


def parse_python_file(file_path: str) -> dict:
    """Phân tích file Python bằng AST để lấy thông tin Class, Function và Docstring."""
    info = {"classes": [], "functions": [], "docstring": ""}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            node = ast.parse(f.read(), filename=file_path)

        doc = ast.get_docstring(node)
        if doc:
            clean_lines = []
            for line in doc.split("\n"):
                line = line.strip()
                if line.startswith("EN:"):
                    continue
                if line.startswith("VI:"):
                    line = line[3:].strip()
                if line:
                    clean_lines.append(line)
            info["docstring"] = (
                clean_lines[0] if clean_lines else "Không có mô tả chi tiết."
            )
        else:
            info["docstring"] = "Chưa có mô tả chi tiết."

        info["docstring"] = info["docstring"].replace("<", "&lt;").replace(">", "&gt;")

        def get_returns(returns_node):
            if not returns_node:
                return "Any"
            if hasattr(ast, "unparse"):
                try:
                    return ast.unparse(returns_node)
                except (AttributeError, ValueError, TypeError):
                    pass
            if isinstance(returns_node, ast.Name):
                return returns_node.id
            return "Any"

        def get_arg_str(arg):
            annotation = ""
            if getattr(arg, "annotation", None):
                if hasattr(ast, "unparse"):
                    try:
                        annotation = f": {ast.unparse(arg.annotation)}"
                    except (AttributeError, ValueError, TypeError):
                        pass
                elif isinstance(arg.annotation, ast.Name):
                    annotation = f": {arg.annotation.id}"
            return f"{arg.arg}{annotation}"

        for item in node.body:
            if isinstance(item, ast.ClassDef):
                class_info = {
                    "name": item.name,
                    "docstring": (ast.get_docstring(item) or "Chưa có mô tả.")
                    .strip()
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"),
                    "methods": [
                        {
                            "name": m.name,
                            "args": [
                                get_arg_str(arg)
                                for arg in m.args.args
                                if arg.arg != "self"
                            ],
                            "returns": get_returns(m.returns),
                            "docstring": (ast.get_docstring(m) or "Chưa có mô tả.")
                            .strip()
                            .replace("<", "&lt;")
                            .replace(">", "&gt;"),
                        }
                        for m in item.body
                        if isinstance(m, ast.FunctionDef)
                    ],
                }
                info["classes"].append(class_info)
            elif isinstance(item, ast.FunctionDef):
                func_info = {
                    "name": item.name,
                    "args": [get_arg_str(arg) for arg in item.args.args],
                    "returns": get_returns(item.returns),
                    "docstring": (ast.get_docstring(item) or "Chưa có mô tả.")
                    .strip()
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"),
                }
                info["functions"].append(func_info)
    except (SyntaxError, OSError, UnicodeDecodeError) as e:
        info["docstring"] = f"Lỗi phân tích cú pháp: {e}"
    return info


def update_readme(target_dir: str = ".", readme_file: str = "README.md") -> None:
    """Quét kiến trúc và cập nhật thẳng vào file README.md."""
    if not os.path.exists(readme_file):
        logging.error(
            f"❌ Không tìm thấy file {readme_file}. Hãy chắc chắn bạn đang ở thư mục gốc."
        )
        return

    logging.info(f"🔍 Đang quét kiến trúc mã nguồn...")

    report = [
        "> Tài liệu này được cập nhật tự động bởi script `scan_architecture.py`.\n"
    ]
    report.append(
        f"### 🌳 Cây Thư Mục\n```text\n"
        + get_directory_tree(target_dir).strip()
        + "\n```\n### 🧩 Chi Tiết Modules (Tổng quan)\n"
    )
    report.append("| 📄 Tệp tin (File) | 📝 Chức năng / Mô tả |")
    report.append("| --- | --- |")

    exclude_dirs = {
        ".git",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        ".vscode",
    }

    py_files = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                py_files.append(Path(root) / file)

    for path in sorted(py_files):
        rel_path = path.relative_to(target_dir).as_posix()
        info = parse_python_file(str(path))
        desc = info["docstring"].replace("\n", " ").replace("|", "&#124;")
        report.append(f"| `{rel_path}` | {desc} |")

    report.append("\n### 📚 Tài liệu API & Logic chi tiết (Dành cho Dev/AI)")
    report.append(
        "Phần này trích xuất tự động thông tin về Đầu vào (Inputs) và Đầu ra (Outputs) của các hàm/lớp trong từng module để hỗ trợ tích hợp và phát triển."
    )

    for path in sorted(py_files):
        rel_path = path.relative_to(target_dir).as_posix()
        info = parse_python_file(str(path))

        if not info["classes"] and not info["functions"]:
            continue

        report.append(f"\n#### 📄 `{rel_path}`")
        if info["classes"]:
            report.append("**Classes:**")
            report.append("")
            for c in info["classes"]:
                report.append(f"- **`class {c['name']}`**")
                if c["docstring"]:
                    report.append(
                        "\n".join(
                            [f"  > {line}" for line in c["docstring"].split("\n")]
                        )
                    )
                for m in c["methods"]:
                    args_str = ", ".join(m["args"])
                    report.append(
                        f"  - **`def {m['name']}({args_str}) -> {m['returns']}`**"
                    )
                    if m["docstring"]:
                        report.append(
                            "\n".join(
                                [f"    > {line}" for line in m["docstring"].split("\n")]
                            )
                        )
                report.append("")
        if info["functions"]:
            report.append("**Functions:**")
            report.append("")
            for f in info["functions"]:
                args_str = ", ".join(f["args"])
                report.append(f"- **`def {f['name']}({args_str}) -> {f['returns']}`**")
                if f["docstring"]:
                    report.append(
                        "\n".join(
                            [f"  > {line}" for line in f["docstring"].split("\n")]
                        )
                    )
                report.append("")

    new_content = "\n".join(report)

    with open(readme_file, "r", encoding="utf-8") as f:
        readme_text = f.read()

    start_marker = "<!-- ARCHITECTURE_START -->"
    end_marker = "<!-- ARCHITECTURE_END -->"

    if start_marker in readme_text and end_marker in readme_text:
        pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
        new_readme_text = pattern.sub(
            lambda m: f"{start_marker}\n{new_content}\n{end_marker}", readme_text
        )
    else:
        new_readme_text = (
            readme_text
            + f"\n\n## 🏗️ Cấu trúc dự án (Architecture)\n{start_marker}\n{new_content}\n{end_marker}\n"
        )

    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(new_readme_text)

    logging.info(f"✅ Đã cập nhật thành công mục Kiến trúc vào: {readme_file}")


if __name__ == "__main__":
    update_readme(".", "README.md")
