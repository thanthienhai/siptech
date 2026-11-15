"""So bản viết lại (content/) với bản gốc (AI-Real) để chắc chắn không mất số liệu, nguồn, mã mẫu.

Dùng: python design/check_rewrite.py tri-thuc-to-chuc/cap-00-bien-ban-hop-co-khuon.md [...]
      python design/check_rewrite.py --group tri-thuc-to-chuc
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEW = ROOT / "content"
OLD = ROOT.parent / "MM" / "AI-Real"


def fences(t):
    return re.findall(r"```[^\n]*\n(.*?)```", t, re.S)


def nums(t):
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    return set(re.findall(r"\d+(?:[.,]\d+)*", t))


def urls(t):
    return set(re.findall(r"https?://[^\s)`|>\]]+", t))


def tags(t):
    return re.findall(r"\[(?:Nguồn|Đề xuất|Đã chạy thử|Chưa chạy thử|Tự tính|Tự chạy|Thao tác|Nguyên tắc)[^\]]*\]", t)


def h2(t):
    return [re.sub(r"^\d+[.)]?\s*", "", l[3:]).split("[")[0].strip() for l in t.split("\n") if l.startswith("## ")]


def refs(t):
    return set(re.findall(r"`[^`]*\.md`", t))


def check(rel):
    o, n = (OLD / rel).read_text(encoding="utf-8"), (NEW / rel).read_text(encoding="utf-8")
    probs = []
    miss = sorted(nums(o) - nums(n), key=lambda x: (len(x), x))
    if miss:
        probs.append(f"số có ở bản gốc nhưng mất: {miss[:25]}")
    if fences(o) != fences(n):
        probs.append(f"khối mã khác: gốc {len(fences(o))}, mới {len(fences(n))} hoặc nội dung khác")
    if urls(o) - urls(n):
        probs.append(f"mất URL: {sorted(urls(o) - urls(n))[:5]}")
    if len(tags(n)) < len(tags(o)) * 0.8:
        probs.append(f"nhãn [Nguồn]/[Đề xuất]: gốc {len(tags(o))}, mới {len(tags(n))}")
    if h2(o) != h2(n):
        probs.append(f"tiêu đề ## khác: {set(h2(o)) ^ set(h2(n))}")
    if refs(o) - refs(n):
        probs.append(f"mất tham chiếu file: {sorted(refs(o) - refs(n))[:4]}")
    tbl_o = len(re.findall(r"^\|[-| :]+\|$", o, re.M))
    tbl_n = len(re.findall(r"^\|[-| :]+\|$", n, re.M))
    if tbl_o != tbl_n:
        probs.append(f"số bảng: gốc {tbl_o}, mới {tbl_n}")
    print(("OK   " if not probs else "XEM  ") + rel, f"({len(o)//1000}KB -> {len(n)//1000}KB)")
    for p in probs:
        print("     -", p)
    return not probs


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--group":
        files = sorted(f"{args[1]}/{p.name}" for p in (NEW / args[1]).glob("cap-*.md"))
    else:
        files = args
    ok = [check(f) for f in files]
    sys.exit(0 if all(ok) else 1)
