"""Dựng site SIPTech từ thư mục content/ (Markdown) sang site/ (HTML tĩnh).

Chạy: python build.py        (cần: pip install markdown)
Biến môi trường SITE_URL (tùy chọn) dùng cho canonical, ví dụ https://thanthienhai.github.io/siptech
"""
import html
import json
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path

import markdown

import lesson

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "assets"
OUT = ROOT / "site"
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")
BRAND = "SIPTech"
TAGLINE = "Tư vấn giải pháp AI trong doanh nghiệp"

STATUS = {"published": "Đã có", "draft": "Đang soạn", "planned": "Sắp ra"}


def load_groups():
    """Mỗi thư mục trong content/ có meta.json là một bài toán. Thêm bài toán = thêm thư mục."""
    groups = []
    for meta in sorted(CONTENT.glob("*/meta.json")):
        d = json.loads(meta.read_text(encoding="utf-8"))
        if d.get("hidden"):
            continue
        d["slug"] = meta.parent.name
        d["n"] = len(list(meta.parent.glob("cap-*.md")))
        d.setdefault("status", "published" if d["n"] else "planned")
        for k, v in (("order", 999), ("icon", "layers"), ("updated", ""), ("code", ""), ("out", ""), ("tags", []),
                     ("tag", ""), ("desc", ""), ("step", None), ("step_label", ""), ("step_note", "")):
            d.setdefault(k, v)
        d["has_pages"] = d["n"] > 0
        groups.append(d)
    groups.sort(key=lambda g: (g["order"], g["name"]))
    return groups


GROUPS = load_groups()
NUM = len(GROUPS)
TOTAL = sum(g["n"] for g in GROUPS)
GROUP_BY_SLUG = {g["slug"]: g for g in GROUPS}


def fmt_date(iso):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})$", iso or "")
    return f"{m.group(3)}/{m.group(2)}/{m.group(1)}" if m else ""


ROOT_DOCS = [
    ("tong-quan", "Tổng quan series", "Ý tưởng cốt lõi, mục lục, điều rút ra, giới hạn, việc phải kiểm trước khi xuất bản."),
    ("nen-tang-bang-chung", "Nền tảng bằng chứng", "Các bài báo đã đọc kỹ (MAP, Nubank, Airbnb, BMO, SAP) và khảo sát ngành."),
    ("thuc-trang-sme-viet-nam", "Thực trạng SME Việt Nam", "Kiểm chứng giả thuyết \"vô tội vạ\" bằng bằng chứng gián tiếp."),
    ("an-toan-du-lieu-va-phap-ly-vn", "An toàn dữ liệu và pháp lý", "Dữ liệu nào được đưa vào AI; pháp luật Việt Nam (chưa xác minh toàn văn)."),
]
ROOT_SRC = {}

# ---------- markdown ----------

def gh_slug(value, sep):
    value = unicodedata.normalize("NFC", value).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"\s", "-", value)


LIST_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")


def dedent_fences(text):
    """python-markdown không nhận khối mã thụt lề (trong danh sách): đưa về sát lề trái."""
    lines, out, i = text.split(chr(10)), [], 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r"^([ ]+)(```|~~~)", l)
        if not m:
            out.append(l)
            i += 1
            continue
        n = len(m.group(1))
        if out and out[-1].strip():
            out.append("")
        j = i
        while True:
            seg = lines[j]
            out.append(seg[n:] if seg.startswith(" " * n) else seg.lstrip())
            j += 1
            if j >= len(lines) or (j > i and lines[j - 1].strip().startswith(m.group(2)) and j - 1 > i):
                break
        out.append("")
        i = j
    return chr(10).join(out)


def blank_before_admonitions(text):
    """Hộp !!! phải bắt đầu ở lề trái và có dòng trống phía trước; đưa hộp thụt lề (trong danh sách) về lề trái."""
    lines, out, i = text.split(chr(10)), [], 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r"^( *)!!! ", l)
        if not m:
            out.append(l)
            i += 1
            continue
        n = len(m.group(1))
        if out and out[-1].strip():
            out.append("")
        out.append(l[n:])
        i += 1
        while i < len(lines):
            seg = lines[i]
            if seg.strip() == "":
                nxt = next((x for x in lines[i + 1:] if x.strip()), "")
                if nxt.startswith(" " * (n + 4)):
                    out.append("")
                    i += 1
                    continue
                break
            if seg.startswith(" " * (n + 4)):
                out.append(seg[n:])
                i += 1
            else:
                break
    return chr(10).join(out)


def prep(text):
    """GitHub cho phép danh sách ngay sau đoạn văn; python-markdown thì cần dòng trống."""
    out, fence, prev = [], False, ""
    for line in text.split(chr(10)):
        if line.lstrip().startswith("```"):
            fence = not fence
        elif (not fence and LIST_RE.match(line) and prev.strip() and not LIST_RE.match(prev)
              and not prev.startswith((" ", chr(9), "|", ">", "#"))):
            out.append("")
        out.append(line)
        prev = line
    return chr(10).join(out)


PAGE_FILES = {"tong-quan": "tong-quan.html", "nen-tang": "nen-tang-bang-chung.html",
              "thuc-trang": "thuc-trang-sme-viet-nam.html", "an-toan": "an-toan-du-lieu-va-phap-ly-vn.html"}
LEVELS = {"doc": ("Đọc trực tiếp", "ok"), "tom": ("Chỉ đọc tóm tắt", "mid"), "thu": ("Qua nguồn thứ cấp", "mid"),
          "chua": ("Chưa đọc được", "low"), "off": ("Nguồn chính thức", "ok")}
VERIFY = {"ok": "Đã xác minh", "part": "Xác minh một phần", "no": "Chưa xác minh"}
CONF = {"hi": "Tin cậy cao", "mid": "Tin cậy trung bình", "low": "Tin cậy thấp"}
SRC_RE = re.compile(r":::sources\n(.*?)\n:::", re.S)
CITE_RE = re.compile(r"\[\[((?:[a-z-]+:)?S\d+(?:\s*,\s*(?:[a-z-]+:)?S\d+)*)\]\]")
VER_RE = re.compile(r"\[\[v:(ok|part|no)\]\]")
CONF_RE = re.compile(r"\[\[c:(hi|mid|low)\]\]")


def extract_sources(text):
    """Khối :::sources: mỗi dòng 'S1 | Tiêu đề | Đơn vị, năm | URL (nhiều URL cách nhau dấu cách) | mức đọc | ghi chú'."""
    found = []

    def grab(m):
        for line in m.group(1).strip().split("\n"):
            parts = [x.strip() for x in line.split("|")]
            if len(parts) < 3:
                continue
            parts += [""] * (6 - len(parts))
            found.append(dict(id=parts[0], title=parts[1], meta=parts[2], urls=[u for u in parts[3].split() if u.startswith("http")],
                              level=parts[4], note=parts[5]))
        return "\n\nSIPSOURCES\n\n"

    return SRC_RE.sub(grab, text), found


def sources_html(sources):
    items = []
    for sc in sources:
        lv = LEVELS.get(sc["level"])
        badge = f'<em class="lvl lvl-{lv[1]}">{lv[0]}</em>' if lv else ""
        urls = sc["urls"]
        if urls:
            links = " ".join(
                f'<a href="{u}" target="_blank" rel="noopener">{"Mở nguồn" if len(urls) == 1 else "Nguồn " + str(i + 1)} ↗</a>'
                for i, u in enumerate(urls))
        else:
            links = '<span class="nolink">chưa có đường dẫn</span>'
        note = f'<p class="sn2">{html.escape(sc["note"])}</p>' if sc["note"] else ""
        items.append(
            f'<li class="src" id="{sc["id"].lower()}"><span class="sid">{sc["id"]}</span><div>'
            f'<b>{html.escape(sc["title"])}</b><small>{html.escape(sc["meta"])}</small>'
            f'<div class="srow">{badge}<span class="slinks">{links}</span></div>{note}</div></li>')
    return '<ol class="srcs">' + "".join(items) + "</ol>"


def apply_tokens(body, sources):
    titles = {x["id"]: x["title"] for x in sources}
    parts = re.split(r"(<pre.*?</pre>)", body, flags=re.S)

    def cite(m):
        out = []
        for ref in re.split(r"\s*,\s*", m.group(1)):
            page, _, sid = ref.rpartition(":")
            href = f"{PAGE_FILES[page]}#{sid.lower()}" if page else f"#{sid.lower()}"
            tip = titles.get(sid, "") if not page else ""
            out.append(f'<a class="cite" href="{href}" title="{html.escape(tip, quote=True)}">Nguồn {sid}</a>')
        return " ".join(out)

    for i in range(0, len(parts), 2):
        t = CITE_RE.sub(cite, parts[i])
        t = VER_RE.sub(lambda m: f'<span class="vb vb-{m.group(1)}">{VERIFY[m.group(1)]}</span>', t)
        t = CONF_RE.sub(lambda m: f'<span class="vb vb-c{m.group(1)}">{CONF[m.group(1)]}</span>', t)
        parts[i] = t
    return "".join(parts)


def label_tables(body):
    def one(m):
        tbl = m.group(0)
        heads = [re.sub(r"\[\[[^]]*\]\]", "", re.sub(r"<[^>]+>", "", h)).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", tbl, flags=re.S)]
        if not heads:
            return tbl

        def row(rm):
            idx = [0]

            def td(tm):
                lab = heads[idx[0]] if idx[0] < len(heads) else ""
                idx[0] += 1
                return f'<td data-label="{html.escape(lab, quote=True)}"{tm.group(1)}>'
            return re.sub(r"<td([^>]*)>", td, rm.group(0))
        return re.sub(r"<tr>.*?</tr>", row, tbl, flags=re.S).replace("<table>", '<table class="stack">', 1)
    return re.sub(r"<table>.*?</table>", one, body, flags=re.S)


def render_md(text):
    rel = getattr(render_md, "rel", "") or ""
    render_md.info = {"date": ""}
    if "/" in rel:
        text, render_md.info = lesson.preprocess(text, rel)
    text = prep(blank_before_admonitions(dedent_fences(text)))
    text, sources = extract_sources(text)
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list", "admonition", "meta"],
        extension_configs={"toc": {"slugify": gh_slug, "permalink": False, "toc_depth": "2-3"}},
    )
    body = md.convert(text)
    body = body.replace("<p>SIPSOURCES</p>", sources_html(sources))
    body = apply_tokens(body, sources)
    body = label_tables(body)
    body = lesson.post(body)
    render_md.meta = {k: " ".join(v) for k, v in getattr(md, "Meta", {}).items()}
    return body, md.toc_tokens


def fix_links(body):
    def repl(m):
        href = m.group(1)
        if re.match(r"^(https?:|mailto:|#)", href):
            return m.group(0)
        path, _, frag = href.partition("#")
        if path.endswith(".md"):
            path = path[:-3]
            if path.endswith("00-README"):
                path = path[: -len("00-README")]
                path = path + ("" if path.endswith("/") or path == "" else "/")
                path = path or "index"
                if path.endswith("/"):
                    path += "index"
            path += ".html"
        return 'href="%s"' % (path + ("#" + frag if frag else ""))
    body = re.sub(r'href="([^"]+)"', repl, body)
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
    body = re.sub(r"<table([^>]*)>", lambda m: '<div class="tw"><table' + m.group(1) + ">", body).replace("</table>", "</table></div>")
    return body


def title_of(text, fallback):
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def short_title(t):
    t = re.sub(r"^(Cấp\s+\w+\s*(\(\w+\))?\s*[:\-—]\s*|[CKQ]\d\s*[—:\-]\s*)", "", t)
    t = re.sub(r"\s*\([ -~]+\)", "", t)  # bỏ chú thích tiếng Anh trong ngoặc
    return t.strip()

# ---------- layout ----------

ICONS = {
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>',
    "flow": '<path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "user": '<path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><path d="M17 11l2 2 4-4"/>',
    "zap": '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "bars": '<path d="M18 20V10M12 20V4M6 20v-6"/>',
    "layers": '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "check": '<path d="M20 6L9 17l-5-5"/>',
    "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4M12 17h.01"/>',
}


def ic(name, size=22):
    return (f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS.get(name, ICONS['layers'])}</svg>')


S_D = "M44 20C44 12 33 11 27 14C20 18 21 26 30 30C39 34 44 38 41 45C38 52 27 52 20 46"


def _logo(tile, fg):
    return ('<svg class="logo" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="16" fill="%s"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="5.5" stroke-linecap="round"/>'
            '<circle cx="44" cy="20" r="5" fill="#ff7a3d"/><circle cx="20" cy="46" r="5" fill="#ff7a3d"/></svg>') % (tile, S_D, fg)


LOGO = _logo("#0b1f4d", "#fff")
LOGO_REV = _logo("#fff", "#0b1f4d")
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap">')


def page(title, body, depth, desc=None, active="", extra_head=""):
    r = "../" * depth
    d = html.escape(desc or f"{BRAND} - {TAGLINE}")
    nav = [("Bài toán", f"{r}bai-toan.html"), ("Cách làm", f"{r}index.html#cach-lam"),
           ("Tài liệu nền", f"{r}index.html#nen-tang"), ("Lưu ý", f"{r}index.html#gioi-han")]
    links = "".join(f'<a href="{h}">{t}</a>' for t, h in nav)
    full_title = title if title.startswith(BRAND) else f"{title} · {BRAND}"
    og_img = (f'<meta property="og:image" content="{SITE_URL}/assets/og-image.png"><meta name="twitter:card" content="summary_large_image">' if SITE_URL else "")
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#1d4ed8">
<meta name="color-scheme" content="light">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="website">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{r}assets/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
{og_img}
{FONTS}
<link rel="stylesheet" href="{r}assets/style.css">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Bỏ qua điều hướng</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{r}index.html">{LOGO}<span>SIP<b>Tech</b></span></a>
    <button class="menu" aria-label="Mở menu" aria-expanded="false" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">Menu</button>
    <nav id="nav">{links}<a class="cta" href="{r}tong-quan.html">Đọc tổng quan</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <div class="fcols">
      <div><div class="brand sm">{LOGO_REV}<span>SIP<b>Tech</b></span></div><p>{TAGLINE}.</p></div>
      <div><h4>Bài toán</h4>{''.join(f'<a href="{r}{g["slug"]}/index.html">{g["name"]}</a>' for g in [x for x in GROUPS if x["has_pages"]][:6])}<a href="{r}bai-toan.html"><b>Xem tất cả ({NUM})</b></a></div>
      <div><h4>Tài liệu nền</h4>{''.join(f'<a href="{r}{s}.html">{t}</a>' for s, t, _ in ROOT_DOCS)}<a href="{r}tu-dien.html">Từ điển thuật ngữ</a><a href="{r}bo-nhan-dien.html">Bộ nhận diện</a></div>
    </div>
    <p class="legal">Nội dung là tài liệu nghiên cứu và hướng dẫn kỹ thuật, không phải tư vấn pháp lý hay tư vấn thuế.
    Số liệu định lượng đến từ các nghiên cứu ở tổ chức lớn, chưa có nguồn nào đo trực tiếp trên SME Việt Nam.
    Các ngưỡng gắn nhãn Đề xuất là thiết kế của nhóm soạn.</p>
  </div>
</footer>
</body>
</html>
"""


def sidebar(items, current, r):
    out = []
    for href, label, group_head in items:
        cls = ' class="cur" aria-current="page"' if href == current else ""
        out.append(f'<a{cls} href="{r}{href}">{html.escape(label)}</a>')
    return "".join(out)


LEGEND = ('<p class="legend">Cách đọc các nhãn nhỏ trong bài: <span class="tg tg-src">Có nguồn</span> điều được nêu trong tài liệu gốc; '
          '<span class="tg tg-prop">Đề xuất</span> ý kiến hoặc thiết kế của SIPTech; <span class="tg tg-ill">Minh họa</span> ví dụ giả định. '
          'Gặp từ lạ? Rê chuột lên từ có gạch chấm, hoặc mở <a href="{r}tu-dien.html">Từ điển thuật ngữ</a>.</p>')


def doc_page(kind, src_text, title, depth, side_items, current, crumbs, prev_next, extra_top="", pos=None):
    body, toc = render_md(src_text)
    meta = dict(getattr(render_md, "meta", {}))
    info = dict(getattr(render_md, "info", {}))
    body = fix_links(body)
    r = "../" * depth
    body = re.sub(r"^\s*<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    body = lesson.glossary_wrap(body, r)
    blog = kind == "root"
    blog_cls = " blog" if blog else ""
    if blog:
        mins = max(1, round(len(re.findall(r"\w+", src_text)) / 190))
        d = fmt_date(meta.get("date", ""))
        extra_top = (f'<div class="byline"><span>SIPTech</span>' + (f"<span>Cập nhật {d}</span>" if d else "") +
                     f"<span>{mins} phút đọc</span></div>" + extra_top)
    if kind == "level" and pos:
        mins = max(1, round(len(re.findall(r"\w+", src_text)) / 190))
        d = fmt_date(info.get("date", ""))
        extra_top = (f'<div class="byline"><span><a href="{r}{pos[3]}/index.html">{html.escape(pos[2])}</a></span>'
                     f"<span>Bài {pos[0] + 1} trong {pos[1]}</span><span>khoảng {mins} phút đọc</span>"
                     + (f"<span>Cập nhật {d}</span>" if d else "") + "</div>" + LEGEND.replace("{r}", r) + extra_top)
    toc_html = ""
    flat = []
    for h in toc[0]["children"] if toc and toc[0]["level"] == 1 else toc:
        if not lesson.AUTH_RE.search(h["name"]):
            flat.append(h)
    if len(flat) >= 3:
        toc_html = '<aside class="otp"><h4>Trong bài này</h4>' + "".join(
            f'<a href="#{t["id"]}">{html.escape(t["name"])}</a>' for t in flat) + "</aside>"
    pn = ""
    if prev_next:
        p, n = prev_next
        home = f"{r}{crumbs[-1][1]}"
        if p:
            prev_html = f'<a class="prev" href="{r}{p[0]}"><small>← Bài trước</small>{html.escape(p[1])}</a>'
        else:
            prev_html = f'<a class="prev" href="{home}"><small>← Quay lại</small>Tổng quan nhóm bài</a>'
        if n:
            q = f"<em>{html.escape(n[2])}</em>" if len(n) > 2 and n[2] else ""
            next_html = f'<a class="next" href="{r}{n[0]}"><small>Bài tiếp theo →</small>{html.escape(n[1])}{q}</a>'
        else:
            next_html = (f'<a class="next" href="{r}bai-toan.html"><small>Bạn đã học hết nhóm bài này →</small>'
                         f"Chọn bài toán tiếp theo<em>Xem danh sách các bài toán để học tiếp</em></a>")
        pn = '<nav class="pn">' + prev_html + next_html + "</nav>"
    crumb_html = " <i>/</i> ".join(f'<a href="{r}{h}">{html.escape(t)}</a>' for t, h in crumbs)
    main = f"""
<div class="wrap docgrid{blog_cls and " wide"}">
  <aside class="side"><div class="sidein">{sidebar(side_items, current, r)}</div></aside>
  <article class="doc{blog_cls}">
    <div class="crumb">{crumb_html}</div>
    <h1>{html.escape(title)}</h1>
    {extra_top}
    {body}
    {pn}
  </article>
  {toc_html}
</div>"""
    return page(title, main, depth, desc=None)

# ---------- home ----------

def pcard(g, compact=False):
    pages = g["has_pages"]
    tag = "a" if pages else "div"
    href = f' href="{g["slug"]}/index.html"' if pages else ""
    meta = " · ".join(x for x in (g["code"], f'{g["n"]} cấp' if g["n"] else "") if x)
    upd = f'<span class="upd">Cập nhật {fmt_date(g["updated"])}</span>' if g["updated"] else ""
    go = f'<span class="go">Xem lộ trình {ic("arrow", 16)}</span>' if pages else '<span class="go soon">Đang chuẩn bị nội dung</span>'
    out = f'<span class="pout">{ic("check", 16)}<span>{g["out"]}</span></span>' if g["out"] else ""
    hay = html.escape(" ".join([g["name"], g["tag"], g["desc"], g["out"]] + list(g["tags"])).lower(), quote=True)
    if compact:
        return f"""
<{tag} class="pcard pc-min st-{g['status']}"{href}>
  <span class="pmeta">{meta}</span>
  <h3>{g['name']}</h3>
  <p class="ptag">{g['tag']}</p>
  <span class="go">Xem lộ trình {ic("arrow", 16)}</span>
</{tag}>"""
    return f"""
<{tag} class="pcard st-{g['status']}"{href} data-status="{g['status']}" data-hay="{hay}">
  <div class="phead"><span class="pico">{ic(g['icon'], 26)}</span><span class="badge b-{g['status']}">{STATUS.get(g['status'], g['status'])}</span></div>
  <span class="pmeta">{meta}</span>
  <h3>{g['name']}</h3>
  <p class="ptag">{g['tag']}</p>
  <p>{g['desc']}</p>
  {out}
  {upd}
  {go}
</{tag}>"""



# ---------- hình minh họa trang chủ ----------

_B, _N, _A, _T, _L = "#1d4ed8", "#0b1f4d", "#ff7a3d", "#e8efff", "#cfd7e6"


def scene(n):
    """Ba cảnh minh họa cho ba vấn đề (SVG nhẹ, không chữ trừ chữ AI)."""
    head = '<svg class="scene" viewBox="0 0 320 160" role="img" aria-label="{}" xmlns="http://www.w3.org/2000/svg"><rect width="320" height="160" rx="14" fill="#f4f7fd"/>'
    if n == 1:
        return head.format("Quy trình nằm rải rác ở tin nhắn, bảng tính và trong đầu một người; AI trả về mỗi lần một kiểu") + f"""
<g stroke="{_L}" stroke-width="2" stroke-dasharray="4 4" fill="none"><path d="M92 34 C120 34 124 70 150 76"/><path d="M92 80 L150 80"/><path d="M92 124 C120 124 124 92 150 86"/></g>
<rect x="16" y="14" width="76" height="40" rx="12" fill="{_T}" stroke="{_B}" stroke-width="2"/><path d="M30 54 L28 66 L42 54Z" fill="{_T}" stroke="{_B}" stroke-width="2" stroke-linejoin="round"/>
<rect x="27" y="26" width="42" height="4" rx="2" fill="{_B}"/><rect x="27" y="36" width="28" height="4" rx="2" fill="{_B}" opacity=".5"/>
<rect x="16" y="62" width="76" height="38" rx="8" fill="#fff" stroke="{_B}" stroke-width="2"/><path d="M16 74 H92 M16 87 H92 M42 62 V100 M67 62 V100" stroke="{_B}" stroke-width="1.5" opacity=".5"/><rect x="16" y="62" width="76" height="12" rx="6" fill="{_B}" opacity=".15"/>
<circle cx="54" cy="116" r="9" fill="{_N}"/><path d="M34 148 C34 130 74 130 74 148Z" fill="{_N}"/>
<rect x="150" y="50" width="62" height="60" rx="16" fill="{_B}"/><text x="181" y="88" text-anchor="middle" font-size="24" font-weight="800" fill="#fff" font-family="inherit">AI</text>
<path d="M214 80 H232" stroke="{_B}" stroke-width="2.5" stroke-linecap="round"/><path d="M228 74 L236 80 L228 86" fill="none" stroke="{_B}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
<g fill="#fff" stroke="{_B}" stroke-width="2"><rect x="240" y="18" width="64" height="38" rx="8" transform="rotate(-4 272 37)"/><rect x="240" y="62" width="64" height="38" rx="8"/><rect x="240" y="106" width="64" height="38" rx="8" transform="rotate(4 272 125)" stroke="{_A}"/></g>
<g fill="{_B}" opacity=".55"><rect x="250" y="30" width="40" height="4" rx="2" transform="rotate(-4 272 37)"/><rect x="250" y="40" width="26" height="4" rx="2" transform="rotate(-4 272 37)"/><rect x="250" y="74" width="30" height="4" rx="2"/><rect x="250" y="84" width="42" height="4" rx="2"/><rect x="250" y="118" width="44" height="4" rx="2" transform="rotate(4 272 125)"/><rect x="250" y="128" width="20" height="4" rx="2" transform="rotate(4 272 125)"/></g>
<text x="289" y="148" font-size="22" font-weight="800" fill="{_A}" font-family="inherit">?</text></svg>"""
    if n == 2:
        return head.format("Ngân sách nhỏ không đủ xây hệ thống riêng; dùng công cụ có sẵn và thêm code nhẹ") + f"""
<g fill="#ffd2b8" stroke="{_A}" stroke-width="2"><ellipse cx="50" cy="128" rx="26" ry="9"/><ellipse cx="50" cy="116" rx="26" ry="9"/><ellipse cx="50" cy="104" rx="26" ry="9"/></g>
<rect x="116" y="22" width="76" height="116" rx="8" fill="none" stroke="{_L}" stroke-width="2.5" stroke-dasharray="6 5"/>
<g fill="{_L}"><rect x="128" y="36" width="14" height="14" rx="3"/><rect x="150" y="36" width="14" height="14" rx="3"/><rect x="172" y="36" width="10" height="14" rx="3"/><rect x="128" y="62" width="14" height="14" rx="3"/><rect x="150" y="62" width="14" height="14" rx="3"/><rect x="172" y="62" width="10" height="14" rx="3"/><rect x="128" y="88" width="14" height="14" rx="3"/><rect x="150" y="88" width="14" height="14" rx="3"/></g>
<circle cx="192" cy="24" r="14" fill="{_A}"/><path d="M186 18 L198 30 M198 18 L186 30" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
<rect x="232" y="112" width="68" height="26" rx="8" fill="{_B}"/><rect x="240" y="82" width="68" height="26" rx="8" fill="{_B}" opacity=".75"/><rect x="236" y="52" width="40" height="26" rx="8" fill="{_B}" opacity=".5"/>
<circle cx="290" cy="50" r="13" fill="#0f9d6b"/><path d="M283 50 L288 55 L297 45" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
    return head.format("Dán dữ liệu khách vào chat công khai, tin câu trả lời không kiểm và không đo hiệu quả") + f"""
<rect x="20" y="16" width="186" height="128" rx="12" fill="#fff" stroke="{_B}" stroke-width="2"/><path d="M20 40 H206" stroke="{_B}" stroke-width="2"/>
<g fill="{_B}"><circle cx="34" cy="28" r="3.5"/><circle cx="46" cy="28" r="3.5" opacity=".6"/><circle cx="58" cy="28" r="3.5" opacity=".3"/></g>
<rect x="64" y="50" width="130" height="50" rx="10" fill="{_T}" stroke="{_A}" stroke-width="2"/>
<rect x="76" y="60" width="52" height="5" rx="2.5" fill="{_N}"/><rect x="76" y="71" width="94" height="5" rx="2.5" fill="{_N}" opacity=".5"/><rect x="76" y="82" width="74" height="5" rx="2.5" fill="{_N}" opacity=".5"/>
<rect x="32" y="112" width="162" height="22" rx="11" fill="#f4f7fd" stroke="{_L}" stroke-width="2"/><rect x="44" y="121" width="46" height="4" rx="2" fill="{_L}"/>
<path d="M262 30 L296 90 H228Z" fill="#fff6ec" stroke="{_A}" stroke-width="3" stroke-linejoin="round"/><rect x="260" y="48" width="4" height="22" rx="2" fill="{_A}"/><circle cx="262" cy="79" r="2.8" fill="{_A}"/>
<path d="M232 142 A32 32 0 0 1 292 142" fill="none" stroke="{_L}" stroke-width="6" stroke-linecap="round" stroke-dasharray="3 9"/><text x="262" y="140" text-anchor="middle" font-size="18" font-weight="800" fill="{_L}" font-family="inherit">?</text></svg>"""


def dots_svg(n, total=100):
    cells = "".join(
        f'<circle cx="{(i % 10) * 10 + 5}" cy="{(i // 10) * 10 + 5}" r="3.6" class="{"on" if i < n else ""}"/>' for i in range(total))
    return f'<svg class="dots" viewBox="0 0 100 100" role="img" aria-label="{n} trên {total}">{cells}</svg>'


def bars_html(rows):
    return '<div class="bars">' + "".join(
        f'<div class="br"><span>{lab}</span><div class="bt"><i style="width:{w}%" class="{cls}"></i></div></div>'
        for lab, w, cls in rows) + "</div>"



HERO_START = "tri-thuc-to-chuc/cap-00-bien-ban-hop-co-khuon.html"


def brand_chip(file, name):
    if file == "zalo":  # logo Zalo là chữ (wordmark): hiển thị lớn hơn, không lặp tên
        return f'<span class="bchip word"><img src="assets/brands/{file}.svg" alt="{name}" width="38" height="38" loading="lazy"></span>'
    return (f'<span class="bchip"><img src="assets/brands/{file}.svg" alt="" width="18" height="18" loading="lazy">{name}</span>')


def hero_card():
    """Sơ đồ minh họa: khách nhắn, AI soạn nháp, người duyệt, ghi vào sổ (logo là nhãn hiệu của chủ sở hữu)."""
    steps = [
        ("Khách nhắn tin", "", [("zalo", "Zalo"), ("messenger", "Messenger"), ("gmail", "Gmail")]),
        ("AI soạn bản nháp", "", [("claude", "Claude"), ("chatgpt", "ChatGPT"), ("gemini", "Gemini")]),
        ("Người duyệt rồi mới gửi", "hot", []),
        ("Ghi vào sổ theo dõi", "", [("sheets", "Google Sheets"), ("excel", "Excel")]),
    ]
    person = ('<svg class="avatar" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="20" fill="#ffe3cf"/>'
              '<circle cx="20" cy="15" r="6.5" fill="#0b1f4d"/><path d="M7 35c1-8 7-11 13-11s12 3 13 11a20 20 0 0 1-26 0z" fill="#0b1f4d"/>'
              '<circle cx="31" cy="30" r="7" fill="#0f9d6b" stroke="#fff" stroke-width="2"/>'
              '<path d="M27.8 30l2.2 2.2 3.6-4" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    rows = ""
    for i, (title, hot, chips) in enumerate(steps, 1):
        inner = "".join(brand_chip(f, n) for f, n in chips) if chips else f'<span class="who">{person}<span>Nhân viên</span></span>'
        rows += f'<li class="{hot}"><span class="sn">{i}</span><div><b>{title}</b><div class="bchips">{inner}</div></div></li>'
    return f"""<div class="stage" role="group" aria-label="Ví dụ minh họa: xử lý tin nhắn khách hàng bằng AI có người duyệt">
  <div class="st-head"><span class="dot"></span>Ví dụ minh họa: xử lý tin nhắn khách hàng</div>
  <ol class="pipe">{rows}</ol>
</div>"""


def sh(eyebrow, title, sub=""):
    s = f'<p class="sub">{sub}</p>' if sub else ""
    return f'<div class="sh"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{s}</div>'


def home():
    shown = sorted([g for g in GROUPS if g["has_pages"]], key=lambda g: g["order"])
    shown = sorted(shown, key=lambda g: g["updated"], reverse=True)[:5]
    cards = "".join(pcard(g, True) for g in sorted(shown, key=lambda g: g["order"]))
    cards += f"""
<a class="pcard ctacard" href="#cach-lam">
  <h3>Chưa biết bắt đầu từ đâu?</h3>
  <p>Xem thứ tự gợi ý cho doanh nghiệp chưa có quy trình.</p>
  <span class="go">Xem thứ tự gợi ý {ic('arrow', 16)}</span>
</a>"""
    steps = {}
    for g in GROUPS:
        if g["step"] is not None and g["has_pages"]:
            st = steps.setdefault(g["step"], {"label": g["step_label"] or g["name"], "note": "", "chips": []})
            st["note"] = st["note"] or g["step_note"]
            st["chips"].append(f'<a class="rchip" href="{g["slug"]}/index.html">{g["name"]}<small>{g["n"]} cấp</small></a>')
    path = "".join(
        f'<li class="rs"><span class="rn">{i + 1}</span><div class="rc"><b>{v["label"]}</b>'
        + (f'<p>{v["note"]}</p>' if v["note"] else "") + f'<div class="rchips">{"".join(v["chips"])}</div></div></li>'
        for i, (k, v) in enumerate(sorted(steps.items())))
    charts = [
        (dots_svg(70), "70%", "hệ thống AI chạy thật dùng mô hình có sẵn, không huấn luyện lại", "Nghiên cứu MAP · arXiv 2512.04123"),
        (dots_svg(68), "68%", "chạy tối đa 10 bước rồi chuyển cho người", "Nghiên cứu MAP · arXiv 2512.04123"),
        (bars_html([("Đúng lần đầu: trên 60%", 60, ""), ("Đúng 8 lần liên tiếp: dưới 25%", 25, "hot")]),
         "&lt;25%", "tỉ lệ đạt giảm mạnh khi cùng một việc phải đúng 8 lần liên tiếp", "τ-bench"),
        (bars_html([("Tự ước: 36 phút", 100, ""), ("Thực đo: 12 phút", 33, "hot")]),
         "36→12", "phút tiết kiệm, tự ước so với thực đo trong thí nghiệm Copilot", "Thí nghiệm có đối chứng"),
    ]
    stat_html = "".join(f'<div class="stat"><div class="sviz">{v}</div><b>{a}</b><p>{b}</p><small>{c}</small></div>'
                        for v, a, b, c in charts)
    principles = [
        ("Bắt đầu từ việc nhỏ", "Mỗi cấp chạy được độc lập và có tiêu chí đo để lên cấp.", "bai-toan.html"),
        ("Dùng công cụ sẵn có trước", "Claude, ChatGPT, Gemini cho người không code; Python nhẹ khi cần.",
         "rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.html"),
        ("Quy tắc quan trọng do code giữ", "Phép tính, kiểm trích dẫn, giới hạn quyền viết bằng code.",
         "rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.html"),
        ("Người duyệt điểm quan trọng", "Tiền, cam kết và dữ liệu cá nhân luôn qua người duyệt.",
         "rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.html"),
        ("Đo trước khi tin", "Bộ ca mẫu có đáp án, đo trước và sau.", "rag-tra-cuu-tai-lieu/cap-06-danh-gia.html"),
    ]
    pr_html = "".join(
        f'<li><a class="prow" href="{href}"><span class="pnum">0{n}</span><span class="ptxt"><b>{b}</b><span>{c}</span></span>'
        f'<span class="parr">{ic("arrow", 18)}</span></a></li>'
        for n, (b, c, href) in enumerate(principles, 1))
    base = "".join(
        f'<a class="base" href="{s}.html" title="{html.escape(d, quote=True)}"><h3>{t.replace("dữ liệu", "dữ&nbsp;liệu").replace("pháp lý", "pháp&nbsp;lý").replace("Việt Nam", "Việt&nbsp;Nam")}</h3><span class="go">Đọc {ic("arrow", 16)}</span></a>' for s, t, d in ROOT_DOCS)
    problems = [
        (1, "Chưa có quy trình", "Quy trình nằm trong đầu vài người và trong tin nhắn Zalo. AI không làm theo được thứ chưa viết ra, nên tự điền chỗ trống, mỗi lần một kiểu."),
        (2, "Ít tiền, ít người kỹ thuật", "Không đủ ngân sách xây hệ thống riêng. Đi bằng công cụ có sẵn và thêm code nhẹ đúng chỗ."),
        (3, "Dùng AI chưa có kỷ luật", "Dán dữ liệu khách vào chat công khai, tin câu trả lời không kiểm, không đo hiệu quả."),
    ]
    pb = "".join(f'<div class="issue">{scene(i)}<h3>{a}</h3><p>{b}</p></div>' for i, a, b in problems)
    body = f"""
<section class="hero">
  <div class="wrap herogrid">
    <div class="herotext">
      <h1><span class="nw">Đưa AI vào</span> <span class="nw">doanh nghiệp,</span><br><span class="hl"><span class="nw">từng bước</span> <span class="nw">và đo được</span></span></h1>
      <p class="lead">Lộ trình cho doanh nghiệp vừa và nhỏ ở Việt Nam. Bắt đầu bằng công cụ có sẵn như Claude, ChatGPT, Gemini, không cần biết code.</p>
      <div class="btns heroact"><a class="btn pri big" href="{HERO_START}">Bắt đầu với bài toán đầu tiên {ic('arrow', 18)}</a><a class="textlink" href="bai-toan.html">Xem tất cả bài toán</a></div>
      <p class="micro">Miễn phí · Không cần biết lập trình · Có đường không cần code</p>
      <div class="proof" aria-label="Bằng chứng từ nghiên cứu">
        <div><b>70%</b><span>hệ thống AI trong doanh nghiệp chạy thật dùng mô hình có sẵn, không huấn luyện lại</span><small>Nghiên cứu MAP · arXiv 2512.04123</small></div>
        <div><b>36→12</b><span>phút tiết kiệm: người dùng tự ước 36, thực đo 12</span><small>Thí nghiệm Copilot có đối chứng</small></div>
      </div>
      <a class="proofmore" href="nen-tang-bang-chung.html">Xem các nguồn và cách đọc số liệu →</a>
    </div>
    <div>{hero_card()}</div>
  </div>
</section>

<section class="factstrip"><div class="wrap"><div class="facts">
  <div><b>{NUM}</b><span>bài toán, thêm mới liên tục</span></div>
  <div><b>{TOTAL}</b><span>cấp độ từ dễ đến khó</span></div>
  <div><b>2</b><span>đường: không code và code nhẹ</span></div>
  <div><b>4</b><span>hạng quyền cho công cụ AI, từ chỉ đọc đến có hậu quả</span></div>
</div></div></section>

<section class="sec" id="van-de">
  <div class="wrap">
    {sh("Vấn đề", "Doanh nghiệp đang vướng ở đâu khi dùng AI?")}
    <div class="grid3">{pb}</div>
    <p class="fine">Ba điều trên là quan sát của SIPTech, có bằng chứng gián tiếp, chưa có số đo trên SME Việt Nam.</p>
  </div>
</section>

<section class="band" id="bang-chung">
  <div class="wrap">
    <div class="sh light"><span class="eyebrow">Bằng chứng</span><h2>Những hệ thống AI chạy thật trông như thế nào</h2>
    <p class="sub">Đều từ tổ chức lớn hoặc nhóm kỹ thuật mạnh. <a href="nen-tang-bang-chung.html">Xem nguồn và cách đọc số liệu</a>.</p></div>
    <div class="stats">{stat_html}</div>
  </div>
</section>

<section class="sec" id="bai-toan">
  <div class="wrap">
    {sh("Bài toán", "Các bài toán doanh nghiệp, mỗi bài một lộ trình", f"Hiện có {NUM} bài toán, bổ sung liên tục. Mỗi cấp có sản phẩm cầm đi được và tiêu chí lên cấp.")}
    <div class="pgrid">{cards}</div>
    <p class="allp"><a class="btn ghost" href="bai-toan.html">Xem tất cả {NUM} bài toán {ic('arrow', 16)}</a></p>
  </div>
</section>

<section class="sec tint" id="cach-lam">
  <div class="wrap">
    {sh("Bắt đầu từ đâu", "Thứ tự gợi ý cho doanh nghiệp chưa có quy trình")}
    <ol class="road">{path}</ol>
    <p class="fine">Đây là đề xuất của SIPTech, chưa có nguồn đo.</p>
  </div>
</section>

<section class="sec" id="nguyen-tac">
  <div class="wrap prsplit">
    <div class="sh"><span class="eyebrow">Cách làm</span><h2>Năm nguyên tắc<br>xuyên suốt</h2>
      <p class="sub">Rút ra từ các hệ thống AI đã chạy thật. <a href="nen-tang-bang-chung.html">Vì sao là năm nguyên tắc này?</a></p></div>
    <ol class="prlist">{pr_html}</ol>
  </div>
</section>

<section class="sec tint" id="nen-tang">
  <div class="wrap">
    {sh("Tài liệu nền", "Đọc trước khi bắt đầu")}
    <div class="bases">{base}</div>
    <p class="fine">Có bộ slide 33 trang cho nhóm tra cứu tài liệu:
    <a href="rag-tra-cuu-tai-lieu/RAG-tra-cuu-tai-lieu-C0-C9.pptx">tải file PowerPoint</a>.</p>
  </div>
</section>

<section class="sec" id="gioi-han">
  <div class="wrap narrow">
    <details class="limitbox">
      <summary><span class="lic">{ic('alert', 20)}</span><span><b>Điều cần biết trước khi áp dụng</b><small>4 lưu ý về số liệu, pháp lý, ngưỡng và công cụ</small></span></summary>
      <ul class="limits">
        <li><span class="lic">{ic('alert', 20)}</span><div><b>Chưa có số đo trên SME Việt Nam.</b> Mọi bằng chứng định lượng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.</div></li>
        <li><span class="lic">{ic('alert', 20)}</span><div><b>Pháp lý chưa xác minh toàn văn.</b> Luật, nghị định được tổng hợp từ nguồn thứ cấp. Đây không phải tư vấn pháp lý; cần luật sư hoặc đọc văn bản gốc trước khi áp dụng.</div></li>
        <li><span class="lic">{ic('alert', 20)}</span><div><b>Ngưỡng và cỡ mẫu là đề xuất.</b> Ví dụ bộ 20-30 ca chỉ phát hiện hỏng, không đo chính xác. Mỗi bài tách rõ [Nguồn] và [Đề xuất].</div></li>
        <li><span class="lic">{ic('alert', 20)}</span><div><b>Công cụ thay đổi nhanh.</b> Tính năng, giá và điều khoản của Claude, ChatGPT, Gemini, Zalo và các phần mềm bán hàng cần kiểm lại trước khi dùng.</div></li>
      </ul>
    </details>
  </div>
</section>

<section class="cta">
  <div class="wrap">
    <h2>Bắt đầu từ bài toán đang làm bạn tốn thời gian nhất</h2>
    <p>Chọn một nhóm, đọc cấp đầu tiên và thử với dữ liệu của chính doanh nghiệp bạn.</p>
    <div class="btns c"><a class="btn pri light" href="#bai-toan">Chọn bài toán</a><a class="btn ghost light" href="tong-quan.html">Đọc tổng quan series</a></div>
  </div>
</section>
"""
    return page(f"{BRAND} - {TAGLINE}", body, 0,
                desc="Series hướng dẫn doanh nghiệp vừa và nhỏ ứng dụng AI từ công cụ có sẵn đến quy trình nhiều bước: nhiều bài toán, cập nhật liên tục, có nguồn và cách đo.")

# ---------- group landing ----------

def group_page(g, levels, readme_text):
    slug = g["slug"]
    r = "../"
    render_md.rel = f"{slug}/00-README.md"
    body, _ = render_md(readme_text or "")
    render_md.rel = ""
    body = fix_links(body)
    body = re.sub(r"^\s*<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    body = lesson.glossary_wrap(body, r)
    steps = ""
    for i, (fname, t, _) in enumerate(levels):
        steps += f'<a class="lv" href="{fname}.html"><span class="n">{i}</span><span class="t">{html.escape(short_title(t))}</span><span class="a">{ic("arrow", 18)}</span></a>'
    extra = ""
    if slug == "rag-tra-cuu-tai-lieu":
        extra = '<a class="btn pri dl" href="RAG-tra-cuu-tai-lieu-C0-C9.pptx">Tải bộ slide PowerPoint (33 slide)</a>'
    main = f"""
<section class="ghero"><div class="wrap">
  <div class="crumb"><a href="{r}index.html">Trang chủ</a> <i>/</i> <a href="{r}bai-toan.html">Bài toán</a></div>
  <div class="gtop"><span class="pico big">{ic(g['icon'], 32)}</span><span class="pill">{g['code']} · {g['n']} cấp</span>{('<span class="upd2">Cập nhật ' + fmt_date(g['updated']) + '</span>') if g['updated'] else ''}</div>
  <h1>{html.escape(g['name'])}</h1>
  <p class="lead">{g['tag']}. {g['desc']}</p>
  <p class="outline">{ic('check', 18)}<span><b>Đầu ra:</b> {g['out']}</span></p>
  {extra}
</div></section>
<div class="wrap">
  <h2 class="lvh">Lộ trình theo cấp</h2>
  <div class="lvs">{steps}</div>
  <h2 class="lvh">Giới thiệu nhóm bài</h2>
  <article class="doc inline">{body}</article>
</div>"""
    return page(g["name"], main, 1, desc=g["tag"] + ". " + g["desc"])


# ---------- trang bộ nhận diện ----------

KIT = ROOT / "design" / "logo-kit"
BRAND_PAGE = "bo-nhan-dien"


def brand_page():
    def tile(name, label, bg="", h=80, note=""):
        png = ""
        for cand in (f"{name}-1600.png", f"{name}-512.png", f"{name}-800.png"):
            if (KIT / "png" / cand).exists():
                png = f' · <a href="brand/png/{cand}" download>PNG</a>'
                break
        cls = {"dark": " dk", "blue": " bl"}.get(bg, "")
        n = f"<small>{note}</small>" if note else ""
        return (f'<figure class="bt{cls}"><div class="bi"><img src="brand/svg/{name}.svg" style="height:{h}px" alt="{html.escape(label)}"></div>'
                f'<figcaption><b>{label}</b>{n}<span><a href="brand/svg/{name}.svg" download>SVG</a>{png}</span></figcaption></figure>')

    def grp(eyebrow, title, sub, items):
        return f'<section class="sec"><div class="wrap">{sh(eyebrow, title, sub)}<div class="bgrid">{"".join(items)}</div></div></section>'

    icons = [tile("icon-color", "Màu (chính)", h=96), tile("icon-reverse", "Nền tối", "dark", 96),
             tile("icon-black", "Một màu: đen", h=96), tile("icon-white", "Một màu: trắng", "blue", 96)]
    avatars = [tile("avatar-circle", "Tròn, nền xanh đậm", h=110, note="Zalo, Facebook"),
               tile("avatar-circle-blue", "Tròn, nền xanh dương", h=110, note="phương án phụ"),
               tile("avatar-square", "Vuông, tràn viền", h=110, note="để nền tảng tự cắt")]
    hz = [tile("lockup-horizontal-tagline-color", "Ngang + giới thiệu (chính)", h=64),
          tile("lockup-horizontal-color", "Ngang", h=64),
          tile("lockup-horizontal-tagline-reverse", "Ngang + giới thiệu, nền tối", "dark", 64),
          tile("lockup-horizontal-reverse", "Ngang, nền tối", "dark", 64),
          tile("lockup-horizontal-black", "Một màu: đen", h=64),
          tile("lockup-horizontal-white", "Một màu: trắng", "blue", 64)]
    st = [tile("lockup-stacked-tagline-color", "Dọc + giới thiệu", h=170), tile("lockup-stacked-color", "Dọc", h=140),
          tile("lockup-stacked-tagline-reverse", "Dọc + giới thiệu, nền tối", "dark", 170),
          tile("lockup-stacked-white", "Một màu: trắng", "blue", 140)]
    wm = [tile("wordmark-color", "Chỉ chữ", h=52), tile("wordmark-reverse", "Chỉ chữ, nền tối", "dark", 52),
          tile("wordmark-black", "Một màu: đen", h=52)]
    soc = "".join(
        f'<figure class="sw2"><img src="brand/social/{n}.png" alt="{n}" loading="lazy"><figcaption><b>{n}</b>'
        f'<span><a href="brand/social/{n}.png" download>PNG</a> · <a href="brand/social/{n}.svg" download>SVG</a></span></figcaption></figure>'
        for n in ("og-image-1200x630", "facebook-cover-1640x624", "linkedin-banner-1584x396"))
    colors = [("#0b1f4d", "Xanh đậm", "nền, chữ SIP", "#fff"), ("#1d4ed8", "Xanh dương", "chữ Tech, nút bấm", "#fff"),
              ("#ff7a3d", "Cam", "hai nút của chữ S", "#fff"), ("#8fb0ff", "Xanh nhạt", "chữ Tech trên nền tối", "#0b1f4d")]
    cs = "".join(f'<div class="cw" style="background:{c};color:{t}"><b>{n}</b><span>{c} · {d}</span></div>' for c, n, d, t in colors)
    body = f"""
<section class="ghero"><div class="wrap">
  <div class="crumb"><a href="index.html">Trang chủ</a> <i>/</i> Bộ nhận diện</div>
  <span class="pill">Thương hiệu</span>
  <h1>Bộ nhận diện SIPTech</h1>
  <p class="lead">Logo, ảnh đại diện, ảnh cho mạng xã hội và màu sắc. Chữ trong các tệp SVG đã chuyển thành đường nét nên không cần cài phông.</p>
  <div class="btns"><a class="btn pri" href="brand/siptech-logo-kit.zip" download>Tải toàn bộ (.zip, 1,7 MB)</a></div>
</div></section>
{grp("Biểu tượng", "Khi không đủ chỗ cho chữ", "Favicon, bìa slide, con dấu.", icons)}
{grp("Ảnh đại diện", "Zalo, Facebook, LinkedIn", "Nền tảng tự cắt tròn nên chữ S đã thu nhỏ để không bị mất nét.", avatars)}
{grp("Bản ngang", "Bản dùng nhiều nhất", "Đầu trang web, chữ ký email, tiêu đề tài liệu.", hz)}
{grp("Bản dọc", "Bìa tài liệu, bảng hiệu vuông", "", st)}
{grp("Chỉ chữ", "Khi biểu tượng đã có bên cạnh", "", wm)}
<section class="sec"><div class="wrap">{sh("Mạng xã hội", "Ảnh chia sẻ và ảnh bìa", "Ảnh chia sẻ link, ảnh bìa Facebook, banner LinkedIn.")}<div class="swgrid">{soc}</div></div></section>
<section class="sec tint"><div class="wrap">{sh("Màu sắc và quy tắc", "Dùng cho nhất quán")}
  <div class="cwgrid">{cs}</div>
  <ul class="rules">
    <li>Chừa quanh logo một khoảng trống bằng nửa chiều cao biểu tượng.</li>
    <li>Cỡ nhỏ nhất: biểu tượng 16px; bản ngang không có dòng giới thiệu rộng 110px, có dòng giới thiệu rộng 220px.</li>
    <li>Nền sáng dùng bản "Màu"; nền xanh đậm hoặc ảnh tối dùng bản "Nền tối"; in một màu dùng bản đen hoặc trắng.</li>
    <li>Không đổi màu hai nút cam, không kéo giãn, không xoay, không thêm bóng đổ hay viền.</li>
    <li>Chưa tra cứu nhãn hiệu: cần kiểm tra trùng lặp trước khi đăng ký hoặc in ấn hàng loạt.</li>
  </ul></div></section>
"""
    return page("Bộ nhận diện", body, 0, desc="Logo, ảnh đại diện, ảnh mạng xã hội và màu sắc của SIPTech. Tải SVG, PNG hoặc cả bộ.")


# ---------- trang tất cả bài toán ----------

def all_page():
    cnt = {k: sum(1 for g in GROUPS if g["status"] == k) for k in STATUS}
    chips = f'<button class="chip on" data-f="all">Tất cả <b>{NUM}</b></button>' + "".join(
        f'<button class="chip" data-f="{k}">{v} <b>{cnt[k]}</b></button>' for k, v in STATUS.items() if cnt[k])
    ordered = sorted(GROUPS, key=lambda g: (g["updated"] or ""), reverse=True)
    cards = "".join(pcard(g) for g in ordered)
    body = f"""
<section class="ghero"><div class="wrap">
  <div class="crumb"><a href="index.html">Trang chủ</a> <i>/</i> Bài toán</div>
  <span class="pill">Danh sách cập nhật liên tục</span>
  <h1>Tất cả bài toán</h1>
  <p class="lead">Hiện có {NUM} bài toán, {TOTAL} cấp độ. Bài toán mới được thêm theo thời gian; thẻ nào đang soạn hoặc sắp ra sẽ ghi rõ trạng thái.</p>
</div></section>
<section class="sec"><div class="wrap">
  <div class="tools">
    <label class="srch">{ic('search', 18)}<input id="q" type="search" placeholder="Tìm theo tên, việc cần làm, từ khóa..." autocomplete="off"></label>
    <div class="chips2" role="group" aria-label="Lọc theo trạng thái">{chips}</div>
  </div>
  <p class="count" id="count" aria-live="polite"></p>
  <div class="pgrid" id="plist">{cards}</div>
  <p class="empty" id="empty" hidden>Không có bài toán khớp. Thử từ khóa khác hoặc chọn "Tất cả".</p>
</div></section>
<script>
(function(){{
  var q=document.getElementById('q'),list=document.getElementById('plist'),cards=[].slice.call(list.children),
      chips=[].slice.call(document.querySelectorAll('.chip')),empty=document.getElementById('empty'),count=document.getElementById('count'),f='all';
  function norm(t){{return t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d');}}
  function run(){{
    var t=norm(q.value.trim()),n=0;
    cards.forEach(function(c){{
      var ok=(f==='all'||c.dataset.status===f)&&(!t||norm(c.dataset.hay).indexOf(t)>-1);
      c.hidden=!ok; if(ok)n++;
    }});
    empty.hidden=n>0; count.textContent='Đang hiển thị '+n+' / '+cards.length+' bài toán';
  }}
  q.addEventListener('input',run);
  chips.forEach(function(b){{b.addEventListener('click',function(){{
    chips.forEach(function(x){{x.classList.remove('on')}}); b.classList.add('on'); f=b.dataset.f; run();
  }})}});
  run();
}})();
</script>
"""
    return page("Tất cả bài toán", body, 0, desc=f"{NUM} bài toán doanh nghiệp ứng dụng AI, cập nhật liên tục: lộ trình theo cấp, đường không code và code nhẹ.")


# ---------- từ điển ----------

def glossary_page():
    body = f"""
<section class="ghero"><div class="wrap">
  <div class="crumb"><a href="index.html">Trang chủ</a> <i>/</i> Từ điển thuật ngữ</div>
  <span class="pill">Dành cho người mới</span>
  <h1>Từ điển thuật ngữ</h1>
  <p class="lead">Giải thích bằng lời thường những từ hay gặp trong các bài giảng. Trong bài, từ nào có gạch chấm bên dưới thì rê chuột lên để xem nghĩa ngắn.</p>
</div></section>
<section class="sec"><div class="wrap"><div class="gloss" style="max-width:860px">{lesson.glossary_html()}</div></div></section>
"""
    return page("Từ điển thuật ngữ", body, 0, desc="Giải thích bằng lời thường các thuật ngữ AI trong bài giảng của SIPTech: prompt, API, token, RAG, agent...")

# ---------- build ----------

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ASSETS, OUT / "assets")

    write(OUT / "index.html", home())
    write(OUT / "bai-toan.html", all_page())
    write(OUT / "tu-dien.html", glossary_page())
    lesson.init(CONTENT, GROUPS, ROOT_DOCS)
    if KIT.exists():
        shutil.copytree(KIT / "svg", OUT / "brand" / "svg")
        shutil.copytree(KIT / "social", OUT / "brand" / "social")
        (OUT / "brand" / "png").mkdir(parents=True)
        for f in (KIT / "png").glob("*.png"):
            if re.search(r"-(1600|512|800|1000)\.png$", f.name):
                shutil.copy2(f, OUT / "brand" / "png" / f.name)
        for f in ("favicon.svg", "favicon.ico"):
            shutil.copy2(KIT / f, OUT / "brand" / f)
        zp = ROOT / "design" / "siptech-logo-kit.zip"
        if zp.exists():
            shutil.copy2(zp, OUT / "brand" / zp.name)
        write(OUT / f"{BRAND_PAGE}.html", brand_page())
    write(OUT / ".nojekyll", "")
    if (ROOT / "CNAME").exists():
        shutil.copy2(ROOT / "CNAME", OUT / "CNAME")

    # tài liệu gốc
    root_side = [(f"{s}.html", t, None) for s, t, _ in ROOT_DOCS]
    for s, t, _ in ROOT_DOCS:
        src = CONTENT / ROOT_SRC.get(s, s + ".md")
        text = src.read_text(encoding="utf-8")
        title = title_of(text, t)
        write(OUT / f"{s}.html", doc_page("root", text, title, 0, root_side, f"{s}.html",
                                          [("Trang chủ", "index.html")], None))

    # các nhóm
    for g in GROUPS:
        if not g["has_pages"]:
            continue
        gdir = CONTENT / g["slug"]
        levels = []
        for f in sorted(gdir.glob("cap-*.md")):
            text = f.read_text(encoding="utf-8")
            levels.append((f.stem, title_of(text, f.stem), text))
        assert len(levels) == g["n"], (g["slug"], len(levels), g["n"])
        readme = (gdir / "00-README.md").read_text(encoding="utf-8") if (gdir / "00-README.md").exists() else ""
        write(OUT / g["slug"] / "index.html", group_page(g, levels, readme))
        side = [("%s/index.html" % g["slug"], "Tổng quan nhóm bài", None)] + [
            (f"{g['slug']}/{fn}.html", f"{i}. {short_title(t)}", None) for i, (fn, t, _) in enumerate(levels)]
        for i, (fn, t, text) in enumerate(levels):
            prev = (f"{g['slug']}/{levels[i-1][0]}.html", short_title(levels[i-1][1])) if i > 0 else None
            nxt = (f"{g['slug']}/{levels[i+1][0]}.html", short_title(levels[i+1][1]),
                   lesson.question_of(levels[i+1][2])) if i < len(levels) - 1 else None
            crumbs = [("Trang chủ", "index.html"), (g["name"], f"{g['slug']}/index.html")]
            render_md.rel = f"{g['slug']}/{fn}.md"
            write(OUT / g["slug"] / f"{fn}.html",
                  doc_page("level", text, t, 1, side, f"{g['slug']}/{fn}.html", crumbs, (prev, nxt),
                           pos=(i, len(levels), g["name"], g["slug"])))
            render_md.rel = ""
        for extra in gdir.iterdir():
            if extra.suffix.lower() in (".pptx", ".pdf", ".xlsx", ".docx", ".zip"):
                shutil.copy2(extra, OUT / g["slug"] / extra.name)

    # sitemap + 404
    pages = [p.relative_to(OUT).as_posix() for p in OUT.rglob("*.html")]
    if SITE_URL:
        urls = "".join(f"<url><loc>{SITE_URL}/{p}</loc></url>" for p in sorted(pages))
        write(OUT / "sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
        write(OUT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    nf = '<section class="sec"><div class="wrap narrow"><h1>Không tìm thấy trang</h1><p>Trang bạn mở không tồn tại hoặc đã đổi địa chỉ.</p><p><a class="btn pri" href="index.html">Về trang chủ</a></p></div></section>'
    base = f'<base href="{SITE_URL}/">' if SITE_URL else ""
    write(OUT / "404.html", page("Không tìm thấy", nf, 0, extra_head=base))
    print(f"OK: {len(pages)} trang -> {OUT}")


if __name__ == "__main__":
    sys.exit(main())
