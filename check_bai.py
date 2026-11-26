"""Kiểm cách viết bài thực hành theo MAU-BAI.md.

Dùng:  python -X utf8 check_bai.py <thư mục bài toán> [...]
In LỖI (phải sửa) và CẢNH BÁO (nên sửa). Thoát mã 1 nếu có lỗi.
"""
import re
import sys
from pathlib import Path

FENCE = re.compile(r"^(\s*)```(\w*)\s*$")
errors, warns = [], []


def split_blocks(text):
    """Trả (các dòng ngoài khối mã, các khối mã [(lang, nội dung)])."""
    out, blocks, cur, lang, inside = [], [], [], "", False
    for ln in text.split("\n"):
        m = FENCE.match(ln)
        if m:
            if not inside:
                inside, lang, cur = True, m.group(2), []
            else:
                blocks.append((lang, "\n".join(cur)))
                inside = False
            continue
        if inside:
            cur.append(ln)
        else:
            out.append(ln)
    if inside:
        errors.append("khối mã ``` không đóng")
    return out, blocks


def check_lesson(path, n, folder):
    where = path.name
    is0 = folder.name.startswith("00")
    text = path.read_text(encoding="utf-8")
    prose, blocks = split_blocks(text)
    E = lambda m: errors.append(f"{where}: {m}")
    W = lambda m: warns.append(f"{where}: {m}")

    first = text.split("\n", 1)[0]
    if not re.match(rf"^# Bài {n}\.\s+\S", first):
        E(f"dòng đầu phải là '# Bài {n}. Tên bài' (đang là: {first[:50]!r})")
    head = "\n".join(text.split("\n")[:10])
    if '!!! info "Bài này"' not in head:
        E('thiếu thẻ !!! info "Bài này" ngay sau tiêu đề')
    else:
        i = text.index('!!! info "Bài này"')
        block = text[i:i + 900]
        for lab in ("Bạn làm gì", "Mất bao lâu", "Cần có", "Kết quả"):
            if lab not in block:
                E(f'thẻ "Bài này" thiếu mục **{lab}**')

    body = "\n".join(prose)
    TOI = r"(?<!chúng )(?<!Chúng )\btôi\b"
    if re.search(TOI, body):
        c = len(re.findall(TOI, body))
        E(f'dùng "tôi" {c} lần (dùng "chúng tôi" hoặc "bạn")')
    if re.search(r"[A-Za-z]:[\\/]+Users[\\/]", text):
        E("có đường dẫn C:\\Users\\...")
    if re.search(r"OneDrive|Công nghiệp Hà Nội", text):
        E("có tên tổ chức/OneDrive")

    steps = re.findall(r"^### Bước \d+\.", body, re.M)
    need_steps = {1: 4, 2: 3, 3: 3, 4: 0}[n]
    if len(steps) < need_steps:
        E(f"cần ít nhất {need_steps} mục '### Bước N.' (đang có {len(steps)})")
    nums = [int(x) for x in re.findall(r"^### Bước (\d+)\.", body, re.M)]
    if nums and nums != list(range(1, len(nums) + 1)):
        E(f"số bước không liên tục: {nums}")

    kinds = [b[0] for b in blocks]
    np = kinds.count("prompt")
    if n == 1 and np < 1 and not is0:
        E("bài 1 phải có ít nhất một khung ```prompt")
    if n == 4 and np < 6 and not is0:
        E(f"bài 4 cần ít nhất 6 khung ```prompt (đang có {np})")
    if n in (1, 2, 3) and "lenh" not in kinds and n != 3:
        W("không có khung ```lenh nào (lệnh gõ vào Terminal nên dùng ```lenh)")
    for lang, content in blocks:
        if lang == "prompt" and len(content.strip()) < 40:
            E("có khung ```prompt quá ngắn/rỗng")
        if lang == "text":
            W("khối ```text: nếu là prompt dùng ```prompt, nếu là đầu ra dùng ```ketqua")

    for key, req in (("Checklist", True), ("Giới hạn", True), ("Lỗi thường gặp", n in (1, 2, 3)), ("Việc cần người làm", n in (1, 2, 3))):
        if req and not re.search(rf"^## .*{key}", body, re.M):
            E(f"thiếu mục '## ... {key}'")
    if n == 4 and not is0:
        for key in ("Bộ prompt", "bài tập", "dữ liệu thật", "Hỏi nhanh"):
            if not re.search(rf"^## .*{key}", body, re.I | re.M):
                E(f"bài 4 thiếu mục có chữ '{key}'")
        if len(re.findall(r"^### .*", body, re.M)) < 8:
            W("bài 4 nên có nhiều mục ### (mỗi prompt và mỗi bài tập một mục)")

    # !!! phải có nội dung thụt
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("!!!"):
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if not nxt.startswith("    "):
                E(f"dòng {i+1}: khối !!! phải có nội dung thụt 4 dấu cách ngay dưới")
            if i > 0 and lines[i - 1].strip():
                E(f"dòng {i+1}: !!! phải cách đoạn trên một dòng trống")

    # ảnh phải có chú thích và có file
    for m in re.finditer(r"^!\[[^\]]*\]\(([^)]+)\)\s*\n\s*\n(.*)$", text, re.M):
        cap = m.group(2).strip()
        if not (cap.startswith("*") and cap.endswith("*") and len(cap) > 6):
            E(f"ảnh {m.group(1)} thiếu dòng chú thích *...* ngay sau")
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        if not (folder / m.group(1)).exists():
            E(f"không thấy file ảnh {m.group(1)}")
    imgs = len(re.findall(r"!\[[^\]]*\]\(", text))
    if n in (1, 2) and imgs < 2:
        W("nên có ít nhất 2 ảnh")

    # độ dài: phần nhìn thấy (bỏ Đào sâu, bỏ khối mã)
    vis = re.split(r"^## Đào sâu.*$", body, flags=re.M)
    visible = " ".join(v if i == 0 else "\n".join(l for l in v.split("\n") if l.startswith("## ")) for i, v in enumerate(vis))
    words = len(re.findall(r"\w+", visible))
    lo, hi = (1000, 3300) if n != 4 else (1200, 3600)
    if words > hi:
        W(f"phần nhìn thấy khoảng {words} từ, dài (mục tiêu ≤ {hi - 300}); chuyển bớt vào '## Đào sâu'")
    if words < lo:
        W(f"phần nhìn thấy chỉ khoảng {words} từ, ngắn")
    return text, blocks


def main():
    for arg in sys.argv[1:]:
        folder = Path(arg)
        start_e, start_w = len(errors), len(warns)
        files = sorted(folder.glob("bai-*.md"))
        nums = [int(re.match(r"bai-(\d)", f.name).group(1)) for f in files]
        if nums != [1, 2, 3, 4] and folder.name[:2] != "00":
            errors.append(f"{folder.name}: cần đúng 4 bài bai-1..bai-4 (đang có {nums})")
        texts = {}
        for f, n in zip(files, nums):
            if n in (1, 2, 3, 4):
                texts[n] = check_lesson(f, n, folder)
        pf = folder / "du-lieu" / "prompt-giao-viec.txt"
        if 1 in texts and not folder.name.startswith("00"):
            if not pf.exists():
                errors.append(f"{folder.name}: thiếu du-lieu/prompt-giao-viec.txt")
            else:
                want = pf.read_text(encoding="utf-8").strip()
                have = [c.strip() for l, c in texts[1][1] if l == "prompt"]
                if want not in have:
                    errors.append(f"{folder.name}: không có khung ```prompt nào GIỐNG HỆT du-lieu/prompt-giao-viec.txt")
        rd = folder / "00-README.md"
        if not rd.exists():
            errors.append(f"{folder.name}: thiếu 00-README.md")
        else:
            t = rd.read_text(encoding="utf-8")
            if "Tải về" in t:
                warns.append(f"{folder.name}/00-README.md: bỏ mục '## Tải về' (bộ nhập tự thêm)")
            if not re.search(r"Bài 4|bài 4", t) and not folder.name.startswith("00"):
                warns.append(f"{folder.name}/00-README.md: chưa nhắc bài 4")
        print(f"[{folder.name}] lỗi mới: {len(errors) - start_e}, cảnh báo mới: {len(warns) - start_w}")
    print()
    for e in errors:
        print("LỖI    ", e)
    for w in warns:
        print("CẢNH BÁO", w)
    print(f"\nTổng: {len(errors)} lỗi, {len(warns)} cảnh báo")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
