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

LOGO = ('<svg class="logo" viewBox="0 0 24 24" aria-hidden="true"><rect x="0.75" y="0.75" width="22.5" height="22.5" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M5 19h5v-5h5V9h4" fill="none" stroke="var(--acc)" stroke-width="2.2" stroke-linecap="square"/></svg>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">')
LADDER = ["Dùng AI thủ công", "Gọi AI qua API", "Tài liệu thành text", "Chia khối và chỉ mục", "Tìm kiếm",
          "Trả lời có trích dẫn", "Đánh giá", "Công cụ (tool use)", "Quy trình nhiều bước", "Vận hành"]
LADDER_FILES = ["cap-00-dung-ai-thu-cong", "cap-01-goi-api", "cap-02-tai-lieu-thanh-text", "cap-03-chia-khoi-va-chi-muc",
                "cap-04-tim-kiem", "cap-05-tra-loi-co-trich-dan", "cap-06-danh-gia", "cap-07-cong-cu-tool",
                "cap-08-quy-trinh-nhieu-buoc", "cap-09-van-hanh"]


def page(title, body, depth, desc=None, active="", extra_head=""):
    r = "../" * depth
    d = html.escape(desc or f"{BRAND} - {TAGLINE}")
    nav = [("Bài toán", f"{r}index.html#bai-toan"), ("Cách làm", f"{r}index.html#cach-lam"),
           ("Tài liệu nền", f"{r}index.html#nen-tang"), ("Giới hạn", f"{r}index.html#gioi-han")]
    links = "".join(f'<a href="{h}">{t}</a>' for t, h in nav)
    full_title = title if title.startswith(BRAND) else f"{title} · {BRAND}"
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#0a0b0c">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="website">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{r}assets/style.css">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Bỏ qua điều hướng</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{r}index.html">{LOGO}<span>SIP<b>TECH</b></span></a>
    <button class="menu" aria-label="Mở menu" aria-expanded="false" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">MENU</button>
    <nav id="nav">{links}<a class="cta" href="{r}tong-quan.html">Tổng quan →</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <div class="fcols">
      <div><div class="brand sm">{LOGO}<span>SIP<b>TECH</b></span></div><p>{TAGLINE}.</p></div>
      <div><h4>Bài toán</h4>{''.join(f'<a href="{r}{g["slug"]}/index.html">{g["name"]}</a>' for g in GROUPS)}</div>
      <div><h4>Tài liệu nền</h4>{''.join(f'<a href="{r}{s}.html">{t}</a>' for s, t, _ in ROOT_DOCS)}</div>
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
            f'<a class="prev" href="{r}{p[0]}"><small>← CẤP TRƯỚC</small>{html.escape(p[1])}</a>' if p else "<span></span>") + (
            f'<a class="next" href="{r}{n[0]}"><small>CẤP TIẾP →</small>{html.escape(n[1])}</a>' if n else "<span></span>") + "</nav>"
    crumb_html = " / ".join(f'<a href="{r}{h}">{html.escape(t)}</a>' for t, h in crumbs)
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

def terminal():
    rows = ""
    for i, (name, f) in enumerate(zip(LADDER, LADDER_FILES)):
        meter = "".join('<i class="on"></i>' if k <= i else "<i></i>" for k in range(10))
        rows += f'<a class="trow" href="rag-tra-cuu-tai-lieu/{f}.html"><span class="tc">C{i}</span><span class="tn">{name}</span><span class="tm">{meter}</span></a>'
    return f"""<div class="term" aria-label="Thang cấp độ C0 đến C9 của nhóm tra cứu tài liệu">
  <div class="tbar"><span>siptech / ladder</span><span>rag-tra-cuu-tai-lieu</span></div>
  <div class="tbody"><div class="cmd"><span class="ps">$</span> siptech ladder --problem rag</div>{rows}<div class="cmd"><span class="ps">$</span> <span class="caret"></span></div></div>
</div>"""


def sh(idx, title, sub=""):
    s = f'<p class="sub">{sub}</p>' if sub else ""
    return f'<div class="sh"><span class="idx">{idx}</span><h2>{title}</h2>{s}</div>'


def home():
    rows = ""
    for g in GROUPS:
        rows += f"""
<a class="prow" href="{g['slug']}/index.html">
  <span class="pcode">{g['code']}</span>
  <span class="pmain"><b>{g['name']}</b><em>{g['tag']}</em></span>
  <span class="pdesc">{g['desc']}</span>
  <span class="pout"><small>ĐẦU RA</small>{g['out']}</span>
  <span class="parrow">→</span>
</a>"""
    order = {1: "Viết SOP", 2: "Khách hàng hoặc hồ sơ", 3: "Tra cứu tài liệu", 4: "Quy trình nhiều bước"}
    path = ""
    for s, label in order.items():
        gs = [g for g in GROUPS if g["step"] == s]
        path += f'<li><small>BƯỚC {s}</small><b>{label}</b><span>{" · ".join(g["name"] for g in gs)}</span></li>'
    stats = [
        ("70%", "hệ thống AI trong doanh nghiệp chạy thật dùng prompt trên mô hình có sẵn, không huấn luyện lại", "MAP · arXiv 2512.04123"),
        ("68%", "chạy tối đa 10 bước rồi chuyển cho người", "MAP · arXiv 2512.04123"),
        ("&lt;25%", "tỉ lệ đạt khi cùng một việc phải đúng 8 lần liên tiếp (pass^8) ở mô hình có pass^1 trên 60%", "τ-bench"),
        ("36→12", "phút tiết kiệm người dùng tự ước so với thực đo trong thí nghiệm Copilot", "thí nghiệm có đối chứng"),
    ]
    stat_html = "".join(f'<div class="stat"><b>{a}</b><p>{b}</p><small>{c}</small></div>' for a, b, c in stats)
    principles = [
        ("P1", "Khối nhỏ trước", "Mỗi cấp chạy được độc lập, có sản phẩm cầm đi được và tiêu chí đo được để biết khi nào mới lên cấp."),
        ("P2", "Hai đường", "Không code (Project, Gem, GPT tùy chỉnh) và code nhẹ (Python). Bắt đầu bằng công cụ đã có, không xây sản phẩm riêng."),
        ("P3", "Code giữ hàng rào", "Quy tắc tính được thì viết bằng code. Số liệu do code tính. Trích dẫn kiểm nguyên văn bằng code, không chỉ nhắc trong prompt."),
        ("P4", "Người duyệt điểm quan trọng", "Tiền, cam kết với khách và dữ liệu cá nhân đi qua điểm duyệt của người. AI đề xuất, người quyết định."),
        ("P5", "Đo trước khi tin", "Bộ ca mẫu có đáp án, đo trước và sau, khoảng tin cậy khi mẫu nhỏ. Năng suất tự ước thường cao hơn thực đo."),
    ]
    pr_html = "".join(f'<div class="pr"><span>{a}</span><div><h3>{b}</h3><p>{c}</p></div></div>' for a, b, c in principles)
    base = "".join(
        f'<a class="base" href="{s}.html"><code>{s}.md</code><h3>{t}</h3><p>{d}</p><span class="go">ĐỌC →</span></a>' for s, t, d in ROOT_DOCS)
    problems = [
        ("Chưa có quy trình", "Quy trình nằm trong đầu vài người làm giỏi và trong tin nhắn Zalo. AI không thể làm theo thứ chưa được viết ra, và sẽ tự điền chỗ trống mỗi lần một kiểu."),
        ("Ít tiền, ít người kỹ thuật", "Không đủ ngân sách xây hệ thống từ đầu thành một sản phẩm độc lập. Cần đi bằng công cụ có sẵn và thêm code nhẹ ở đúng chỗ."),
        ("Dùng AI chưa có kỷ luật", "Dán dữ liệu khách vào chat công khai, tin câu trả lời không kiểm, không đo hiệu quả. Đây là quan sát của nhóm soạn, được ủng hộ gián tiếp, chưa có số đo trên SME Việt Nam."),
    ]
    pb = "".join(f'<div class="cell"><span class="n">0{i+1}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(problems))
    body = f"""
<section class="hero">
  <div class="wrap herogrid">
    <div>
      <p class="kicker">// {TAGLINE.upper()}</p>
      <h1>Ứng dụng AI đúng cách, từ việc nhỏ nhất đến <span class="hl">nghiệp vụ phức tạp</span></h1>
      <p class="lead">Nhiều doanh nghiệp vừa và nhỏ đang dùng AI mỗi nơi một kiểu, chưa có quy trình và không đủ tiền xây hệ thống riêng.
      {BRAND} dẫn từng bước: dùng công cụ có sẵn như Claude, ChatGPT, Gemini trước, rồi mới đến API và code, kèm cách đo để biết khi nào nên đi tiếp.</p>
      <div class="btns"><a class="btn pri" href="#bai-toan">XEM 5 BÀI TOÁN →</a><a class="btn ghost" href="tong-quan.html">ĐỌC TỔNG QUAN</a></div>
    </div>
    <div>{terminal()}</div>
  </div>
  <div class="wrap"><div class="strip">
    <div><small>BÀI TOÁN</small><b>5</b></div>
    <div><small>CẤP ĐỘ</small><b>{TOTAL}</b></div>
    <div><small>HAI ĐƯỜNG</small><b>không code / code nhẹ</b></div>
    <div><small>QUY ƯỚC</small><b>[Nguồn] ≠ [Đề xuất]</b></div>
  </div></div>
</section>

<section class="sec" id="van-de">
  <div class="wrap">
    {sh("01", "Vấn đề doanh nghiệp đang gặp")}
    <div class="cells c3">{pb}</div>
  </div>
</section>

<section class="sec" id="bang-chung">
  <div class="wrap">
    {sh("02", "Bằng chứng từ nơi đã làm thật", "Đều từ tổ chức lớn hoặc nhóm kỹ thuật mạnh. Chi tiết trong <a href='nen-tang-bang-chung.html'>Nền tảng bằng chứng</a>.")}
    <div class="stats">{stat_html}</div>
  </div>
</section>

<section class="sec" id="bai-toan">
  <div class="wrap">
    {sh("03", "5 bài toán, mỗi bài một thang cấp độ", "Mỗi cấp có sản phẩm cầm đi được, đường không code, đường code nhẹ, tiêu chí lên cấp và rủi ro.")}
    <div class="probs">{rows}</div>
  </div>
</section>

<section class="sec" id="cach-lam">
  <div class="wrap">
    {sh("04", "Cách làm")}
    <div class="prs">{pr_html}</div>
    <h3 class="subh">Thứ tự gợi ý cho doanh nghiệp chưa có quy trình</h3>
    <ol class="order">{path}</ol>
    <p class="fine">[Đề xuất] của nhóm soạn, không có nguồn đo.</p>
  </div>
</section>

<section class="sec" id="nen-tang">
  <div class="wrap">
    {sh("05", "Tài liệu nền")}
    <div class="bases">{base}</div>
    <p class="fine">Bộ slide cho nhóm tra cứu tài liệu (33 slide, có hình minh họa):
    <a href="rag-tra-cuu-tai-lieu/RAG-tra-cuu-tai-lieu-C0-C9.pptx">tải file PowerPoint</a>.</p>
  </div>
</section>

<section class="sec" id="gioi-han">
  <div class="wrap">
    {sh("06", "Giới hạn của bộ tài liệu")}
    <ul class="limits">
      <li><span>CHƯA ĐO</span><div><b>Chưa có số đo trên SME Việt Nam.</b> Mọi bằng chứng định lượng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.</div></li>
      <li><span>PHÁP LÝ</span><div><b>Chưa xác minh toàn văn.</b> Luật, nghị định được tổng hợp từ nguồn thứ cấp. Đây không phải tư vấn pháp lý; cần luật sư hoặc đọc văn bản gốc trước khi áp dụng.</div></li>
      <li><span>NGƯỠNG</span><div><b>Ngưỡng và cỡ mẫu là đề xuất.</b> Ví dụ bộ 20-30 ca chỉ phát hiện hỏng, không đo chính xác. Mỗi file cấp tách rõ [Nguồn] và [Đề xuất].</div></li>
      <li><span>CÔNG CỤ</span><div><b>Thay đổi nhanh.</b> Tính năng, giá và điều khoản của Claude, ChatGPT, Gemini, Zalo, các phần mềm bán hàng cần kiểm lại trước khi dùng.</div></li>
    </ul>
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
        steps += f'<a class="lv" href="{fname}.html"><span class="n">{g["code"][0]}{i}</span><span class="t">{html.escape(short_title(t))}</span><span class="a">→</span></a>'
    extra = ""
    if slug == "rag-tra-cuu-tai-lieu":
        extra = '<a class="btn pri dl" href="RAG-tra-cuu-tai-lieu-C0-C9.pptx">TẢI SLIDE POWERPOINT (33) ↓</a>'
    main = f"""
<section class="ghero"><div class="wrap">
  <div class="crumb"><a href="{r}index.html">~/siptech</a> / <a href="{r}index.html#bai-toan">bai-toan</a> / {slug}</div>
  <p class="kicker">// {g['code']} · {g['n']} CẤP</p>
  <h1>{html.escape(g['name'])}</h1>
  <p class="lead">{g['tag']}. {g['desc']}</p>
  <p class="outline"><small>ĐẦU RA</small> {g['out']}</p>
  {extra}
</div></section>
<div class="wrap">
  <div class="sh"><span class="idx">//</span><h2>Thang cấp độ</h2></div>
  <div class="lvs">{steps}</div>
  <div class="sh"><span class="idx">//</span><h2>Giới thiệu nhóm bài</h2></div>
  <article class="doc inline">{body}</article>
</div>"""
    return page(g["name"], main, 1, desc=g["tag"] + ". " + g["desc"])

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
