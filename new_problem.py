"""Tạo khung cho một bài toán mới trong content/.

Dùng:  python new_problem.py ten-thu-muc "Tên hiển thị" [--status draft|planned|published]
Ví dụ: python new_problem.py quan-ly-ton-kho "Quản lý tồn kho" --status planned

Sau khi tạo: sửa meta.json, viết 00-README.md và các file cap-00-*.md, cap-01-*.md...
Chỉ có meta.json (không có file cap-*) thì bài toán hiện là thẻ "Sắp ra", chưa có trang.
Push lên nhánh main là site tự dựng lại.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("slug")
ap.add_argument("name")
ap.add_argument("--status", default="planned", choices=["published", "draft", "planned"])
a = ap.parse_args()
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a.slug):
    sys.exit("slug chỉ gồm chữ thường không dấu, số và dấu gạch ngang")
d = Path(__file__).parent / "content" / a.slug
if d.exists():
    sys.exit(f"Đã tồn tại: {d}")
d.mkdir(parents=True)
meta = dict(name=a.name, code="", icon="layers", order=100, status=a.status, updated=datetime.date.today().isoformat(),
            tag="Một câu mô tả việc doanh nghiệp cần làm", desc="Hai câu mô tả các cấp độ sẽ đi qua.", out="Sản phẩm cầm đi được ở cuối bài toán",
            tags=[], step=None, step_label="")
(d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if a.status != "planned":
    (d / "00-README.md").write_text(f"# Nhóm bài: {a.name}\n\n> Quy ước: **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.\n\n## 1. Bài toán\n\n...\n", encoding="utf-8")
    (d / "cap-00-mo-dau.md").write_text("# Cấp 0: ...\n\n## 1. Mục tiêu\n\n...\n", encoding="utf-8")
print("Đã tạo", d, "\nIcon có sẵn: chat, file, search, flow, book, shield, user, zap, lock, bars, layers")
