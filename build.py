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

LOGO = ('<svg class="logo" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="var(--ink)"/>'
        '<path d="M8 22h5v-4h5v-4h5v-4" fill="none" stroke="var(--amber)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="23" cy="10" r="2.4" fill="var(--amber)"/></svg>')


def page(title, body, depth, desc=None, active="", extra_head=""):
    r = "../" * depth
    d = html.escape(desc or f"{BRAND} - {TAGLINE}")
    nav = [("bai-toan", "Bài toán", f"{r}index.html#bai-toan"), ("cach-lam", "Cách làm", f"{r}index.html#cach-lam"),
           ("nen-tang", "Tài liệu nền", f"{r}index.html#nen-tang"), ("gioi-han", "Giới hạn", f"{r}index.html#gioi-han")]
    links = "".join(f'<a href="{h}">{t}</a>' for _, t, h in nav)
    full_title = title if title.startswith(BRAND) else f"{title} · {BRAND}"
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#0e3b3f">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="website">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{r}assets/style.css">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Bỏ qua điều hướng</a>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="{r}index.html">{LOGO}<span><b>SIP</b>Tech</span></a>
    <button class="menu" aria-label="Mở menu" aria-expanded="false" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">☰</button>
    <nav id="nav">{links}<a class="cta" href="{r}tong-quan.html">Đọc tổng quan</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <div class="fcols">
      <div><div class="brand sm">{LOGO}<span><b>SIP</b>Tech</span></div><p>{TAGLINE}.</p></div>
      <div><h4>5 bài toán</h4>{''.join(f'<a href="{r}{g["slug"]}/index.html">{g["name"]}</a>' for g in GROUPS)}</div>
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
    # bỏ H1 đầu (đã in ở đầu bài)
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

def ladder_svg():
    steps = []
    for i in range(10):
        h = 24 + i * 22
        x = 10 + i * 40
        y = 270 - h
        op = 0.35 + i * 0.065
        steps.append(f'<rect x="{x}" y="{y}" width="34" height="{h}" rx="5" fill="var(--sage)" opacity="{op:.2f}"/>'
                     f'<text x="{x + 17}" y="{y + 20}" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">{i}</text>')
    return ('<svg viewBox="0 0 420 290" role="img" aria-label="Thang cấp độ từ 0 đến 9: mỗi cấp là một khối chạy được độc lập">'
            + "".join(steps) +
            '<path d="M20 240 L120 200 L220 150 L320 90 L400 30" fill="none" stroke="var(--amber)" stroke-width="3" stroke-linecap="round" stroke-dasharray="1 8"/>'
            '<circle cx="400" cy="30" r="9" fill="var(--amber)"/>'
            '<text x="10" y="284" font-size="12" fill="var(--hero-mute)">Dùng thủ công</text>'
            '<text x="410" y="284" text-anchor="end" font-size="12" fill="var(--hero-mute)">Vận hành</text></svg>')


def home():
    cards = ""
    for g in GROUPS:
        cards += f"""
<a class="card prob" href="{g['slug']}/index.html">
  <div class="pbadge"><span>{g['code']}</span><em>{g['n']} cấp</em></div>
  <h3>{g['name']}</h3>
  <p class="ptag">{g['tag']}</p>
  <p>{g['desc']}</p>
  <div class="pout"><small>Đầu ra</small>{g['out']}</div>
  <span class="go">Xem thang cấp →</span>
</a>"""
    order = {1: "Viết SOP", 2: "Khách hàng hoặc hồ sơ", 3: "Tra cứu tài liệu", 4: "Quy trình nhiều bước"}
    path = ""
    for s, label in order.items():
        gs = [g for g in GROUPS if g["step"] == s]
        path += f'<li><b>{label}</b><span>{" · ".join(g["name"] for g in gs)}</span></li>'
    stats = [
        ("70%", "hệ thống AI trong doanh nghiệp chạy thật dùng prompt trên mô hình có sẵn, không huấn luyện lại", "MAP, arXiv 2512.04123"),
        ("68%", "chạy tối đa 10 bước rồi chuyển cho người", "MAP, arXiv 2512.04123"),
        ("<25%", "tỉ lệ đạt khi cùng một việc phải đúng 8 lần liên tiếp (pass^8) ở mô hình có pass^1 trên 60%", "τ-bench"),
        ("36 → 12", "phút tiết kiệm người dùng tự ước so với thực đo trong thí nghiệm Copilot", "thí nghiệm có đối chứng"),
    ]
    stat_html = "".join(f'<div class="stat"><b>{a}</b><p>{b}</p><small>{c}</small></div>' for a, b, c in stats)
    principles = [
        ("1", "Khối nhỏ trước", "Mỗi cấp chạy được độc lập, có sản phẩm cầm đi được và tiêu chí đo được để biết khi nào mới lên cấp."),
        ("2", "Hai đường", "Không code (Project, Gem, GPT tùy chỉnh) và code nhẹ (Python). Bắt đầu bằng công cụ đã có, không xây sản phẩm riêng."),
        ("3", "Code giữ hàng rào", "Quy tắc tính được thì viết bằng code. Số liệu do code tính. Trích dẫn kiểm nguyên văn bằng code, không chỉ nhắc trong prompt."),
        ("4", "Người duyệt điểm quan trọng", "Tiền, cam kết với khách và dữ liệu cá nhân đi qua điểm duyệt của người. AI đề xuất, người quyết định."),
        ("5", "Đo trước khi tin", "Bộ ca mẫu có đáp án, đo trước và sau, khoảng tin cậy khi mẫu nhỏ. Năng suất tự ước thường cao hơn thực đo."),
    ]
    pr_html = "".join(f'<div class="pr"><span>{a}</span><h3>{b}</h3><p>{c}</p></div>' for a, b, c in principles)
    base = "".join(
        f'<a class="card base" href="{s}.html"><h3>{t}</h3><p>{d}</p><span class="go">Đọc →</span></a>' for s, t, d in ROOT_DOCS)
    body = f"""
<section class="hero">
  <div class="wrap herogrid">
    <div>
      <p class="eyebrow">{TAGLINE}</p>
      <h1>Ứng dụng AI đúng cách, từ việc nhỏ nhất đến nghiệp vụ phức tạp</h1>
      <p class="lead">Nhiều doanh nghiệp vừa và nhỏ đang dùng AI mỗi nơi một kiểu, chưa có quy trình và không đủ tiền xây hệ thống riêng.
      {BRAND} dẫn từng bước: dùng công cụ có sẵn như Claude, ChatGPT, Gemini trước, rồi mới đến API và code, kèm cách đo để biết khi nào nên đi tiếp.</p>
      <div class="btns"><a class="btn pri" href="#bai-toan">Xem 5 bài toán</a><a class="btn ghost" href="tong-quan.html">Đọc tổng quan series</a></div>
      <ul class="chips"><li>5 bài toán</li><li>{TOTAL} cấp độ</li><li>Có nguồn, có đo</li><li>Bối cảnh Việt Nam</li></ul>
    </div>
    <div class="heroviz">{ladder_svg()}</div>
  </div>
</section>

<section class="sec" id="van-de">
  <div class="wrap">
    <h2>Vấn đề doanh nghiệp đang gặp</h2>
    <div class="grid3">
      <div class="card"><h3>Chưa có quy trình</h3><p>Quy trình nằm trong đầu vài người làm giỏi và trong tin nhắn Zalo. AI không thể làm theo thứ chưa được viết ra, và sẽ tự điền chỗ trống mỗi lần một kiểu.</p></div>
      <div class="card"><h3>Ít tiền, ít người kỹ thuật</h3><p>Không đủ ngân sách xây hệ thống từ đầu thành một sản phẩm độc lập. Cần đi bằng công cụ có sẵn và thêm code nhẹ ở đúng chỗ.</p></div>
      <div class="card"><h3>Dùng AI chưa có kỷ luật</h3><p>Dán dữ liệu khách vào chat công khai, tin câu trả lời không kiểm, không đo hiệu quả. Đây là quan sát của nhóm soạn, được ủng hộ gián tiếp, chưa có số đo trên SME Việt Nam.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Bằng chứng từ nơi đã làm thật</h2>
    <div class="stats">{stat_html}</div>
    <p class="fine">Đều từ tổ chức lớn hoặc nhóm kỹ thuật mạnh. Chi tiết và cách đọc kết quả trong <a href="nen-tang-bang-chung.html">Nền tảng bằng chứng</a>.</p>
  </div>
</section>

<section class="sec" id="bai-toan">
  <div class="wrap">
    <h2>5 bài toán, mỗi bài một thang cấp độ</h2>
    <p class="sub">Mỗi bài toán đi từ dùng thủ công đến vận hành, mỗi cấp có sản phẩm, đường không code, đường code nhẹ, tiêu chí lên cấp và rủi ro.</p>
    <div class="probs">{cards}</div>
  </div>
</section>

<section class="sec alt" id="cach-lam">
  <div class="wrap">
    <h2>Cách làm</h2>
    <div class="prs">{pr_html}</div>
    <div class="order">
      <h3>Thứ tự gợi ý cho doanh nghiệp chưa có quy trình</h3>
      <ol>{path}</ol>
      <p class="fine">Đây là [Đề xuất] của nhóm soạn, không có nguồn đo.</p>
    </div>
  </div>
</section>

<section class="sec" id="nen-tang">
  <div class="wrap">
    <h2>Tài liệu nền</h2>
    <div class="bases">{base}</div>
    <p class="fine">Bộ slide cho nhóm tra cứu tài liệu (33 slide, có hình minh họa):
    <a href="rag-tra-cuu-tai-lieu/RAG-tra-cuu-tai-lieu-C0-C9.pptx">tải file PowerPoint</a>.</p>
  </div>
</section>

<section class="sec alt" id="gioi-han">
  <div class="wrap narrow">
    <h2>Giới hạn của bộ tài liệu</h2>
    <ul class="limits">
      <li><b>Chưa có số đo trên SME Việt Nam.</b> Mọi bằng chứng định lượng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.</li>
      <li><b>Pháp lý chưa xác minh toàn văn.</b> Luật, nghị định được tổng hợp từ nguồn thứ cấp. Đây không phải tư vấn pháp lý; cần luật sư hoặc đọc văn bản gốc trước khi áp dụng.</li>
      <li><b>Ngưỡng và cỡ mẫu là đề xuất.</b> Ví dụ bộ 20-30 ca chỉ phát hiện hỏng, không đo chính xác. Mỗi file cấp tách rõ <b>[Nguồn]</b> và <b>[Đề xuất]</b>.</li>
      <li><b>Công cụ thay đổi nhanh.</b> Tính năng, giá và điều khoản của Claude, ChatGPT, Gemini, Zalo, các phần mềm bán hàng cần kiểm lại trước khi dùng.</li>
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
    title = title_of(readme_text, g["name"])
    steps = ""
    for i, (fname, t, _) in enumerate(levels):
        steps += (f'<a class="lv" href="{fname}.html"><span class="n">{i}</span><span class="t">{html.escape(short_title(t))}</span></a>')
    extra = ""
    if slug == "rag-tra-cuu-tai-lieu":
        extra = '<a class="btn pri dl" href="RAG-tra-cuu-tai-lieu-C0-C9.pptx">Tải bộ slide PowerPoint (33 slide)</a>'
    main = f"""
<section class="ghero"><div class="wrap">
  <div class="crumb dark"><a href="{r}index.html">Trang chủ</a> / <a href="{r}index.html#bai-toan">Bài toán</a></div>
  <p class="eyebrow">{g['code']} · {g['n']} cấp</p>
  <h1>{html.escape(g['name'])}</h1>
  <p class="lead">{g['tag']}. {g['desc']}</p>
  <p class="outline"><small>Đầu ra</small> {g['out']}</p>
  {extra}
</div></section>
<div class="wrap">
  <h2 class="lvh">Thang cấp độ</h2>
  <div class="lvs">{steps}</div>
  <div class="hr"></div>
  <article class="doc inline"><div class="srcnote">Phần giới thiệu nhóm bài, nguyên văn từ <code>00-README.md</code>.</div>{body}</article>
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
