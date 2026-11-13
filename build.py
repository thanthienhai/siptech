"""Dựng site SIPTech từ thư mục content/ (Markdown) sang site/ (HTML tĩnh).

Chạy: python build.py        (cần: pip install markdown)
Biến môi trường SITE_URL (tùy chọn) dùng cho canonical, ví dụ https://thanthienhai.github.io/siptech
"""
import html
import os
import re
import shutil
import sys
import unicodedata
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "assets"
OUT = ROOT / "site"
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")
BRAND = "SIPTech"
TAGLINE = "Tư vấn giải pháp AI trong doanh nghiệp"

GROUPS = [
    dict(slug="tri-thuc-to-chuc", name="Tri thức tổ chức", code="C0–C7", n=8,
         tag="Giữ quy trình không nằm trong đầu một người",
         desc="Biên bản họp, ghi âm tiếng Việt, SOP từ người làm giỏi, sổ đăng ký tài liệu, bàn giao khi nghỉ việc.",
         out="Tài liệu và SOP đã duyệt", step=1),
    dict(slug="xu-ly-yeu-cau-khach", name="Xử lý yêu cầu khách hàng", code="C0–C6", n=7,
         tag="Zalo, email, đổi trả, khiếu nại theo SOP",
         desc="Soạn trả lời có duyệt, phân loại và mức khẩn, tra đơn chỉ đọc, hành động ghi qua phiếu duyệt.",
         out="Bản nháp trả lời, quyết định, hành động có duyệt", step=2),
    dict(slug="kiem-tra-ho-so-theo-quy-tac", name="Kiểm tra hồ sơ, chứng từ", code="K0–K7", n=8,
         tag="Hóa đơn, hợp đồng, hồ sơ nhân sự",
         desc="Chứng từ thành dữ liệu có nguồn, quy tắc thành mã, quy tắc mờ có hàng rào, đối chiếu ba bên.",
         out="Danh sách lỗi có căn cứ", step=2),
    dict(slug="rag-tra-cuu-tai-lieu", name="Tra cứu tài liệu nội bộ", code="C0–C9", n=10,
         tag="Hỏi đáp trên bảng giá, chính sách, hợp đồng",
         desc="Từ dùng AI thủ công, gọi API, tách văn bản, chia khối, tìm kiếm, đến trả lời có trích dẫn và vận hành.",
         out="Câu trả lời có trích dẫn nguyên văn", step=3),
    dict(slug="quy-trinh-nhieu-buoc", name="Quy trình nhiều bước", code="Q0–Q6", n=7,
         tag="Một việc đi qua nhiều người, nhiều hệ thống",
         desc="Vẽ quy trình và đo nền, tự động hóa thường, định tuyến, báo cáo định kỳ, chuỗi bước có điểm duyệt.",
         out="Quy trình chạy tự động, có số đo trước/sau", step=4),
]
TOTAL = sum(g["n"] for g in GROUPS)
GROUP_BY_SLUG = {g["slug"]: g for g in GROUPS}

ROOT_DOCS = [
    ("tong-quan", "Tổng quan series", "Ý tưởng cốt lõi, mục lục, điều rút ra, giới hạn, việc phải kiểm trước khi xuất bản."),
    ("nen-tang-bang-chung", "Nền tảng bằng chứng", "Các bài báo đã đọc kỹ (MAP, Nubank, Airbnb, BMO, SAP) và khảo sát ngành."),
    ("thuc-trang-sme-viet-nam", "Thực trạng SME Việt Nam", "Kiểm chứng giả thuyết \"vô tội vạ\" bằng bằng chứng gián tiếp."),
    ("an-toan-du-lieu-va-phap-ly-vn", "An toàn dữ liệu và pháp lý", "Dữ liệu nào được đưa vào AI; pháp luật Việt Nam (chưa xác minh toàn văn)."),
]
ROOT_SRC = {"tong-quan": "00-README.md"}

# ---------- markdown ----------

def gh_slug(value, sep):
    value = unicodedata.normalize("NFC", value).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"\s", "-", value)


LIST_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")


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


def render_md(text):
    text = prep(text)
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
        extension_configs={"toc": {"slugify": gh_slug, "permalink": False, "toc_depth": "2-3"}},
    )
    body = md.convert(text)
    toc = md.toc_tokens
    return body, toc


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
                path = path or "tong-quan"
                if path.endswith("/"):
                    path += "index"
            path += ".html"
        return 'href="%s"' % (path + ("#" + frag if frag else ""))
    body = re.sub(r'href="([^"]+)"', repl, body)
    body = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    return body


def title_of(text, fallback):
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def short_title(t):
    t = re.sub(r"^(Cấp\s+\w+\s*(\(\w+\))?\s*[:\-—]\s*|[CKQ]\d\s*[—:\-]\s*)", "", t)
    return t

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
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


GROUP_ICON = {"tri-thuc-to-chuc": "book", "xu-ly-yeu-cau-khach": "chat", "kiem-tra-ho-so-theo-quy-tac": "file",
              "rag-tra-cuu-tai-lieu": "search", "quy-trinh-nhieu-buoc": "flow"}

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
    nav = [("Bài toán", f"{r}index.html#bai-toan"), ("Cách làm", f"{r}index.html#cach-lam"),
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
      <div><h4>Bài toán</h4>{''.join(f'<a href="{r}{g["slug"]}/index.html">{g["name"]}</a>' for g in GROUPS)}</div>
      <div><h4>Tài liệu nền</h4>{''.join(f'<a href="{r}{s}.html">{t}</a>' for s, t, _ in ROOT_DOCS)}<a href="{r}bo-nhan-dien.html">Bộ nhận diện</a></div>
    </div>
    <p class="legal">Nội dung là tài liệu nghiên cứu và hướng dẫn kỹ thuật, không phải tư vấn pháp lý hay tư vấn thuế.
    Số liệu định lượng đến từ các nghiên cứu ở tổ chức lớn, chưa có nguồn nào đo trực tiếp trên SME Việt Nam.
    Các ngưỡng gắn nhãn [Đề xuất] là thiết kế của nhóm soạn.</p>
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


def doc_page(kind, src_text, title, depth, side_items, current, crumbs, prev_next, extra_top=""):
    body, toc = render_md(src_text)
    body = fix_links(body)
    r = "../" * depth
    body = re.sub(r"^\s*<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    toc_html = ""
    flat = []
    for h in toc[0]["children"] if toc and toc[0]["level"] == 1 else toc:
        flat.append(h)
    if len(flat) >= 3:
        toc_html = '<aside class="otp"><h4>Trong bài này</h4>' + "".join(
            f'<a href="#{t["id"]}">{html.escape(t["name"])}</a>' for t in flat) + "</aside>"
    pn = ""
    if prev_next:
        p, n = prev_next
        pn = '<nav class="pn">' + (
            f'<a class="prev" href="{r}{p[0]}"><small>← Cấp trước</small>{html.escape(p[1])}</a>' if p else "<span></span>") + (
            f'<a class="next" href="{r}{n[0]}"><small>Cấp tiếp →</small>{html.escape(n[1])}</a>' if n else "<span></span>") + "</nav>"
    crumb_html = " <i>/</i> ".join(f'<a href="{r}{h}">{html.escape(t)}</a>' for t, h in crumbs)
    main = f"""
<div class="wrap docgrid">
  <aside class="side"><div class="sidein">{sidebar(side_items, current, r)}</div></aside>
  <article class="doc">
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

def flow_card():
    steps = [
        ("chat", "Khách nhắn Zalo", "“Đơn của tôi đã giao chưa?”", "Khách", ""),
        ("search", "Tra đơn trong phần mềm bán hàng", "Chỉ đọc, không sửa được dữ liệu", "Công cụ", ""),
        ("zap", "AI soạn bản nháp theo quy trình", "Có trích dẫn đúng điều khoản", "AI", ""),
        ("user", "Nhân viên duyệt rồi mới gửi", "Tiền và cam kết luôn qua người", "Người", "hot"),
    ]
    items = "".join(
        f'<li class="{hot}"><span class="fi">{ic(i, 20)}</span><div><b>{t}</b><small>{s}</small></div><em>{tag}</em></li>'
        for i, t, s, tag, hot in steps)
    return f"""<div class="flowcard" aria-label="Ví dụ quy trình xử lý tin nhắn của khách có điểm duyệt của người">
  <div class="fhead"><span class="dot"></span>Ví dụ minh họa: xử lý tin nhắn khách hàng</div>
  <ol>{items}</ol>
</div>"""


def sh(eyebrow, title, sub=""):
    s = f'<p class="sub">{sub}</p>' if sub else ""
    return f'<div class="sh"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{s}</div>'


def home():
    cards = ""
    for g in GROUPS:
        cards += f"""
<a class="pcard" href="{g['slug']}/index.html">
  <span class="pico">{ic(GROUP_ICON[g['slug']], 26)}</span>
  <span class="pmeta">{g['code']} · {g['n']} cấp</span>
  <h3>{g['name']}</h3>
  <p class="ptag">{g['tag']}</p>
  <p>{g['desc']}</p>
  <span class="pout">{ic('check', 16)}<span>{g['out']}</span></span>
  <span class="go">Xem lộ trình {ic('arrow', 16)}</span>
</a>"""
    cards += f"""
<a class="pcard ctacard" href="#cach-lam">
  <h3>Chưa biết bắt đầu từ đâu?</h3>
  <p>Doanh nghiệp chưa có quy trình nên bắt đầu bằng việc viết SOP. Xem thứ tự gợi ý cho từng giai đoạn.</p>
  <span class="go">Xem thứ tự gợi ý {ic('arrow', 16)}</span>
</a>"""
    order = {1: "Viết SOP", 2: "Khách hàng hoặc hồ sơ", 3: "Tra cứu tài liệu", 4: "Quy trình nhiều bước"}
    path = ""
    for s, label in order.items():
        gs = [g for g in GROUPS if g["step"] == s]
        path += f'<li><span class="sn">{s}</span><b>{label}</b><span>{" · ".join(g["name"] for g in gs)}</span></li>'
    stats = [
        ("70%", "hệ thống AI trong doanh nghiệp chạy thật dùng prompt trên mô hình có sẵn, không huấn luyện lại", "Nghiên cứu MAP · arXiv 2512.04123"),
        ("68%", "chạy tối đa 10 bước rồi chuyển cho người", "Nghiên cứu MAP · arXiv 2512.04123"),
        ("&lt;25%", "tỉ lệ đạt khi cùng một việc phải đúng 8 lần liên tiếp, ở mô hình mà lần đầu đúng trên 60%", "τ-bench"),
        ("36→12", "phút tiết kiệm: người dùng tự ước 36, thực đo 12 trong thí nghiệm Copilot", "Thí nghiệm có đối chứng"),
    ]
    stat_html = "".join(f'<div class="stat"><b>{a}</b><p>{b}</p><small>{c}</small></div>' for a, b, c in stats)
    principles = [
        ("layers", "Bắt đầu từ việc nhỏ", "Mỗi cấp chạy được độc lập, có sản phẩm cầm đi được và tiêu chí đo để biết khi nào mới lên cấp."),
        ("chat", "Dùng công cụ sẵn có trước", "Claude, ChatGPT, Gemini cho người không code; Python nhẹ khi cần. Không phải xây sản phẩm riêng."),
        ("lock", "Quy tắc quan trọng do code giữ", "Phép tính, kiểm trích dẫn, giới hạn quyền viết bằng code, không chỉ nhắc AI trong prompt."),
        ("user", "Người duyệt điểm quan trọng", "Tiền, cam kết với khách và dữ liệu cá nhân đi qua điểm duyệt của người. AI đề xuất, người quyết định."),
        ("bars", "Đo trước khi tin", "Bộ ca mẫu có đáp án, đo trước và sau. Năng suất tự ước thường cao hơn thực đo."),
    ]
    pr_html = "".join(f'<div class="pr"><span class="pico sm">{ic(i, 20)}</span><div><h3>{b}</h3><p>{c}</p></div></div>' for i, b, c in principles)
    base = "".join(
        f'<a class="base" href="{s}.html"><h3>{t}</h3><p>{d}</p><span class="go">Đọc {ic("arrow", 16)}</span></a>' for s, t, d in ROOT_DOCS)
    problems = [
        ("flow", "Chưa có quy trình", "Quy trình nằm trong đầu vài người làm giỏi và trong tin nhắn Zalo. AI không làm theo được thứ chưa viết ra, và sẽ tự điền chỗ trống mỗi lần một kiểu."),
        ("zap", "Ít tiền, ít người kỹ thuật", "Không đủ ngân sách xây hệ thống từ đầu thành một sản phẩm độc lập. Cần đi bằng công cụ có sẵn và thêm code nhẹ đúng chỗ."),
        ("shield", "Dùng AI chưa có kỷ luật", "Dán dữ liệu khách vào chat công khai, tin câu trả lời không kiểm, không đo hiệu quả. Đây là quan sát của SIPTech, có bằng chứng gián tiếp, chưa có số đo trên SME Việt Nam."),
    ]
    pb = "".join(f'<div class="issue"><span class="pico">{ic(i, 24)}</span><h3>{a}</h3><p>{b}</p></div>' for i, a, b in problems)
    body = f"""
<section class="hero">
  <div class="wrap herogrid">
    <div class="herotext">
      <span class="pill">{TAGLINE}</span>
      <h1>Đưa AI vào doanh nghiệp <span class="hl">đúng cách</span>: từng bước, đo được, an toàn</h1>
      <p class="lead">Nhiều doanh nghiệp vừa và nhỏ đang dùng AI mỗi nơi một kiểu, chưa có quy trình và không đủ ngân sách xây hệ thống riêng.
      {BRAND} đi từ việc nhỏ nhất với công cụ có sẵn như Claude, ChatGPT, Gemini, rồi mới đến API và code, kèm cách đo để biết khi nào nên đi tiếp.</p>
      <div class="btns"><a class="btn pri" href="#bai-toan">Xem 5 bài toán</a><a class="btn ghost" href="tong-quan.html">Đọc tổng quan</a></div>
      <ul class="checks">
        <li>{ic('check', 18)}Mỗi cấp có sản phẩm cầm đi được</li>
        <li>{ic('check', 18)}Có đường không cần code</li>
        <li>{ic('check', 18)}Nguồn và số đo rõ ràng</li>
      </ul>
    </div>
    <div>{flow_card()}</div>
  </div>
  <div class="wrap"><div class="facts">
    <div><b>5</b><span>bài toán doanh nghiệp</span></div>
    <div><b>{TOTAL}</b><span>cấp độ từ dễ đến khó</span></div>
    <div><b>2</b><span>đường: không code và code nhẹ</span></div>
    <div><b>A–D</b><span>4 hạng quyền cho công cụ, từ chỉ đọc đến có hậu quả</span></div>
  </div></div>
</section>

<section class="sec" id="van-de">
  <div class="wrap">
    {sh("Vấn đề", "Doanh nghiệp đang vướng ở đâu khi dùng AI?")}
    <div class="grid3">{pb}</div>
  </div>
</section>

<section class="band" id="bang-chung">
  <div class="wrap">
    <div class="sh light"><span class="eyebrow">Bằng chứng</span><h2>Những hệ thống AI chạy thật trông như thế nào</h2>
    <p class="sub">Đều từ tổ chức lớn hoặc nhóm kỹ thuật mạnh. Cách đọc chi tiết trong <a href="nen-tang-bang-chung.html">Nền tảng bằng chứng</a>.</p></div>
    <div class="stats">{stat_html}</div>
  </div>
</section>

<section class="sec" id="bai-toan">
  <div class="wrap">
    {sh("Bài toán", "5 bài toán doanh nghiệp, mỗi bài một lộ trình", "Mỗi cấp có sản phẩm cầm đi được, đường không code, đường code nhẹ, tiêu chí lên cấp và rủi ro cần tránh.")}
    <div class="pgrid">{cards}</div>
  </div>
</section>

<section class="sec tint" id="cach-lam">
  <div class="wrap">
    {sh("Cách làm", "Năm nguyên tắc xuyên suốt")}
    <div class="prs">{pr_html}</div>
    <h3 class="subh">Thứ tự gợi ý cho doanh nghiệp chưa có quy trình</h3>
    <ol class="order">{path}</ol>
    <p class="fine">Đây là đề xuất của SIPTech, chưa có nguồn đo.</p>
  </div>
</section>

<section class="sec" id="nen-tang">
  <div class="wrap">
    {sh("Tài liệu nền", "Đọc trước khi bắt đầu")}
    <div class="bases">{base}</div>
    <p class="fine">Có bộ slide 33 trang cho nhóm tra cứu tài liệu:
    <a href="rag-tra-cuu-tai-lieu/RAG-tra-cuu-tai-lieu-C0-C9.pptx">tải file PowerPoint</a>.</p>
  </div>
</section>

<section class="sec tint" id="gioi-han">
  <div class="wrap narrow">
    {sh("Lưu ý", "Điều cần biết trước khi áp dụng")}
    <ul class="limits">
      <li><span class="lic">{ic('alert', 20)}</span><div><b>Chưa có số đo trên SME Việt Nam.</b> Mọi bằng chứng định lượng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.</div></li>
      <li><span class="lic">{ic('alert', 20)}</span><div><b>Pháp lý chưa xác minh toàn văn.</b> Luật, nghị định được tổng hợp từ nguồn thứ cấp. Đây không phải tư vấn pháp lý; cần luật sư hoặc đọc văn bản gốc trước khi áp dụng.</div></li>
      <li><span class="lic">{ic('alert', 20)}</span><div><b>Ngưỡng và cỡ mẫu là đề xuất.</b> Ví dụ bộ 20-30 ca chỉ phát hiện hỏng, không đo chính xác. Mỗi bài tách rõ [Nguồn] và [Đề xuất].</div></li>
      <li><span class="lic">{ic('alert', 20)}</span><div><b>Công cụ thay đổi nhanh.</b> Tính năng, giá và điều khoản của Claude, ChatGPT, Gemini, Zalo và các phần mềm bán hàng cần kiểm lại trước khi dùng.</div></li>
    </ul>
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
                desc="Series hướng dẫn doanh nghiệp vừa và nhỏ ứng dụng AI từ công cụ có sẵn đến quy trình nhiều bước: 5 bài toán, 40 cấp độ, có nguồn và cách đo.")

# ---------- group landing ----------

def group_page(g, levels, readme_text):
    slug = g["slug"]
    r = "../"
    body, _ = render_md(readme_text)
    body = fix_links(body)
    body = re.sub(r"^\s*<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    steps = ""
    for i, (fname, t, _) in enumerate(levels):
        steps += f'<a class="lv" href="{fname}.html"><span class="n">{i}</span><span class="t">{html.escape(short_title(t))}</span><span class="a">{ic("arrow", 18)}</span></a>'
    extra = ""
    if slug == "rag-tra-cuu-tai-lieu":
        extra = '<a class="btn pri dl" href="RAG-tra-cuu-tai-lieu-C0-C9.pptx">Tải bộ slide PowerPoint (33 slide)</a>'
    main = f"""
<section class="ghero"><div class="wrap">
  <div class="crumb"><a href="{r}index.html">Trang chủ</a> <i>/</i> <a href="{r}index.html#bai-toan">Bài toán</a></div>
  <div class="gtop"><span class="pico big">{ic(GROUP_ICON[slug], 32)}</span><span class="pill">{g['code']} · {g['n']} cấp</span></div>
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
        gdir = CONTENT / g["slug"]
        levels = []
        for f in sorted(gdir.glob("cap-*.md")):
            text = f.read_text(encoding="utf-8")
            levels.append((f.stem, title_of(text, f.stem), text))
        assert len(levels) == g["n"], (g["slug"], len(levels), g["n"])
        readme = (gdir / "00-README.md").read_text(encoding="utf-8")
        write(OUT / g["slug"] / "index.html", group_page(g, levels, readme))
        side = [("%s/index.html" % g["slug"], "Tổng quan nhóm bài", None)] + [
            (f"{g['slug']}/{fn}.html", f"{i}. {short_title(t)}", None) for i, (fn, t, _) in enumerate(levels)]
        for i, (fn, t, text) in enumerate(levels):
            prev = (f"{g['slug']}/{levels[i-1][0]}.html", short_title(levels[i-1][1])) if i > 0 else None
            nxt = (f"{g['slug']}/{levels[i+1][0]}.html", short_title(levels[i+1][1])) if i < len(levels) - 1 else None
            crumbs = [("Trang chủ", "index.html"), (g["name"], f"{g['slug']}/index.html")]
            write(OUT / g["slug"] / f"{fn}.html",
                  doc_page("level", text, t, 1, side, f"{g['slug']}/{fn}.html", crumbs, (prev, nxt)))
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
