"""Biến các file Markdown "tài liệu nghiên cứu" thành bài giảng dễ đọc cho người mới.

Chạy trong build.py. Làm 5 việc:
1. Gọn phần đầu bài: bỏ "Ngày soạn", bảng quy ước [Nguồn]/[Đề xuất], gom ghi chú thành khung "Trước khi học".
2. Đổi tham chiếu file (`../x/cap-01.md` mục 3) thành liên kết có tên bài và tên phần.
3. Đổi nhãn [Nguồn] [Đề xuất] [Đã chạy thử]... thành thẻ nhỏ có giải thích; mã nguồn (B5, V1...) thành liên kết.
4. Gập phần "chưa kiểm chứng" (dành cho người soạn), biến địa chỉ web thành liên kết.
5. Giải nghĩa thuật ngữ khi rê chuột (từ điển).
"""
import html
import posixpath
import re
from pathlib import Path

SEP = "¦"  # ¦ ngăn các phần trong thẻ tạm

REG = {}          # đường dẫn md -> thông tin
GROUPS = {}       # slug -> tên nhóm
ROOT_TITLES = {}  # "nen-tang-bang-chung.md" -> tên hiển thị
WARN = []

TAG_WORDS = r"Nguồn|Đề xuất|Đã chạy thử|Chưa chạy thử|Tự tính|Tự chạy|Thao tác|Nguyên tắc"
TAG_RE = re.compile(r"\*\*\[(%s)([^\]\n]*)\]\*\*|\[(%s)([^\]\n]*)\]" % (TAG_WORDS, TAG_WORDS))
REFID = re.compile(r"[A-Z]{1,2}-?[A-Z]?\d+")

RENAMES = [
    (re.compile(r"^Chuỗi bài nhỏ$"), "Các bài thực hành"),
    (re.compile(r"^Tái dùng khối nào của .*$"), "Phần nào dùng lại từ nhóm bài Tra cứu tài liệu"),
    (re.compile(r"^Mục tiêu và người đọc$"), "Bài này dành cho ai và bạn sẽ làm được gì"),
    (re.compile(r"^Kiến thức nền.*$"), "Kiến thức nền"),
    (re.compile(r"^Câu hỏi cấp này trả lời.*$"), "Vấn đề bài này giải quyết"),
    (re.compile(r"^Đường không code vs.*khi nào buộc.*$"), "Hai cách làm: không cần code và có code (khi nào nên chuyển)"),
    (re.compile(r"^Đường không code vs.*$"), "Hai cách làm: không cần code và có code"),
    (re.compile(r"^Ví dụ cho SME Việt Nam.*$"), "Ví dụ cho doanh nghiệp nhỏ ở Việt Nam"),
    (re.compile(r"^Tiêu chí lên .*$"), "Khi nào bạn có thể lên cấp tiếp theo"),
    (re.compile(r"^Danh sách kiểm chứng trước khi xuất bản$"), "Việc cần kiểm trước khi xuất bản"),
    (re.compile(r"^Nguồn đã đọc và mức đọc$"), "Nguồn đã đọc và mức đọc"),
]
AUTH_RE = re.compile(r"chưa kiểm chứng|cần kiểm tra lại|cần kiểm chứng|việc cần kiểm trước|danh sách kiểm chứng", re.I)

TAG_DEFAULT = {
    "src": ("Có nguồn", "Điều này được nêu trong tài liệu nguồn mà SIPTech đã đọc."),
    "prop": ("Đề xuất", "Ý kiến hoặc thiết kế của SIPTech, chưa có nguồn nào kiểm chứng."),
    "ill": ("Minh họa", "Ví dụ giả định để dễ hình dung, không phải số liệu thật."),
    "obs": ("Quan sát", "Quan sát của người soạn, chưa có số đo."),
    "run": ("Mã đã chạy thử", "Đoạn mã đã được chạy thử trên máy người soạn, chưa chạy với dịch vụ thật."),
    "norun": ("Mã chưa chạy thử", "Đoạn mã này chưa được chạy thử."),
    "calc": ("Số tự tính", "Số do SIPTech tự tính bằng mã, chưa đối chiếu nguồn ngoài."),
    "op": ("Thao tác hay đổi", "Các bước trên giao diện thường thay đổi; mỗi chỗ có ghi ngày kiểm tra."),
    "prin": ("Nguyên tắc bền", "Nguyên tắc ít thay đổi theo thời gian."),
    "note": ("", ""),
}

# ----------------------------------------------------------------- tiện ích


def strip_md(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[*_`]", "", t)
    return t.strip()


def gh_slug(value):
    import unicodedata
    value = unicodedata.normalize("NFC", value).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"\s", "-", value)


def tok(kind, label="", tip=""):
    clean = lambda s: re.sub(r"[`\]\[|%s\n]" % SEP, " ", re.sub(r"(?:\.\./)*[\w./-]+\.md", "bài khác", s)).strip()
    return f"[[t:{kind}{SEP}{clean(label)}{SEP}{clean(tip)}]]"


def tag_to_tokens(word, rest):
    rest = rest.strip()
    if word == "Nguồn":
        if rest.startswith(":"):
            items = [x.strip() for x in re.split(r"[,;]", rest[1:]) if x.strip()]
            refs = [x for x in items if REFID.fullmatch(x)]
            other = [x for x in items if not REFID.fullmatch(x)]
            out = " ".join(f"[[r:{x}]]" for x in refs)
            if other:
                out += (" " if out else "") + (tok("note", ", ".join(other)) if refs else tok("src", "Nguồn: " + ", ".join(other)))
            return out or tok("src")
        return tok("src", "", rest.lstrip(",; ").strip())
    if word == "Đề xuất":
        r = rest.lstrip(",; ").strip()
        low = r.lower()
        if low.startswith("minh họa"):
            return tok("ill", "", r[len("minh họa"):].lstrip(",; "))
        if low.startswith("quan sát"):
            return tok("obs", "", r[len("quan sát"):].lstrip(",; "))
        return tok("prop", "", r)
    return {"Đã chạy thử": tok("run"), "Tự chạy": tok("run"), "Chưa chạy thử": tok("norun"), "Tự tính": tok("calc"),
            "Thao tác": tok("op"), "Nguyên tắc": tok("prin")}[word]


def replace_tags(line):
    def f(m):
        word = m.group(1) or m.group(3)
        rest = m.group(2) if m.group(1) else m.group(4)
        return tag_to_tokens(word, rest)
    return TAG_RE.sub(f, line)


def norm_heading(raw):
    """Trả về (số thứ tự hoặc '', chữ tiêu đề đã làm sạch, [thẻ])."""
    tags = [tag_to_tokens(m.group(1) or m.group(3), m.group(2) if m.group(1) else m.group(4)) for m in TAG_RE.finditer(raw)]
    text = TAG_RE.sub("", raw).strip()
    text = text.replace("nhóm RAG", "nhóm bài Tra cứu tài liệu").replace("Nhóm RAG", "Nhóm bài Tra cứu tài liệu")
    m = re.match(r"^(\d+[a-z]?(?:\.[A-Za-z0-9]+)*[.)]?)\s+(.*)$", text)
    num, body = (m.group(1), m.group(2)) if m else ("", text)
    body = body.strip(" :")
    for pat, new in RENAMES:
        if pat.match(strip_md(body)):
            body = new
            break
    return num, body, tags


def heading_key(text):
    m = re.match(r"^(?:Bài\s+)?([A-Z]?\d+[a-z]?(?:\.[A-Za-z0-9]+)*)\s*[.:)\s]", text + " ")
    return m.group(1) if m else ""

# ----------------------------------------------------------------- đăng ký trang


def init(content_dir, groups, root_docs):
    REG.clear()
    for g in groups:
        GROUPS[g["slug"]] = g["name"]
    for slug, title, _ in root_docs:
        ROOT_TITLES[slug + ".md"] = title
    for f in sorted(Path(content_dir).glob("*/*.md")) + sorted(Path(content_dir).glob("*.md")):
        rel = f.relative_to(content_dir).as_posix()
        lines = f.read_text(encoding="utf-8").split("\n")
        h1 = next((l[2:].strip() for l in lines if l.startswith("# ")), rel)
        heads, fence = [], False
        for l in lines:
            if l.lstrip().startswith("```"):
                fence = not fence
            m = None if fence else re.match(r"^(#{2,4})\s+(.*)$", l)
            if m:
                num, body, _ = norm_heading(m.group(2))
                full = (num + " " + body).strip()
                heads.append((heading_key(full + " "), body, gh_slug(strip_md(full)), body.startswith("Bài ")))
        grp = rel.split("/")[0] if "/" in rel else ""
        REG[rel] = dict(h1=strip_md(h1), group=grp, heads=heads)


def short_h1(h1):
    t = re.sub(r"\s*\([^)]*\)", "", h1).strip()
    return t


def short_head(t, limit=56):
    t = re.sub(r"\s*\([^)]*\)", "", t).strip(" :—-")
    return t if len(t) <= limit else t[: limit - 1].rsplit(" ", 1)[0] + "…"


def label_for(target, cur_group):
    info = REG[target]
    if "/" not in target:
        return ROOT_TITLES.get(target, info["h1"])
    g = info["group"]
    gname = GROUPS.get(g, g)
    if target.endswith("00-README.md"):
        return f"Nhóm bài {gname}"
    h = short_h1(info["h1"])
    return h if g == cur_group else f"{gname} · {h}"


def question_of(text):
    """Câu hỏi mà bài trả lời (dòng in nghiêng trong mục 'Câu hỏi cấp này trả lời')."""
    m = re.search(r"Câu hỏi cấp này trả lời[^\n]*\n+\*[\"“]([^\n]+?)[\"”]\*", text)
    return m.group(1).strip() if m else ""


# ----------------------------------------------------------------- tiền xử lý markdown


ID_ = r"[A-Z]?\d+(?:\.[A-Za-z0-9]+)?(?:\s*(?:-|–|và|,)\s*[A-Z]?\d+(?:\.[A-Za-z0-9]+)?)*"
REF_RE = re.compile(
    r"`((?:\.\./|\./)*[A-Za-z0-9_./-]*?\.md)`"
    r"(?:\s*\(\s*(mục|Mục|bài|Bài)\s+(" + ID_ + r")\s*\)|\s+(mục|Mục|bài|Bài)\s+(" + ID_ + r"))?")
DIR_RE = re.compile(r"`(?:\.\./)?([a-z0-9-]+)/`")


def resolve(raw, cur_dir):
    target = posixpath.normpath(posixpath.join(cur_dir, raw))
    if target in REG:
        return target
    base = posixpath.basename(raw)
    hits = [k for k in REG if posixpath.basename(k) == base]
    return hits[0] if len(hits) == 1 and base != "00-README.md" else None


BARE_RE = re.compile(r"(?<![\w/\[(.`-])((?:\.\./)*[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9-]+)*\.md)(?![\w(])")


def convert_refs(line, rel):
    cur_dir = posixpath.dirname(rel)
    cur_group = rel.split("/")[0] if "/" in rel else ""

    def fix(m):
        raw = m.group(1)
        kw, loc = (m.group(2), m.group(3)) if m.group(2) else (m.group(4), m.group(5))
        target = resolve(raw, cur_dir)
        if target is None:
            WARN.append((rel, raw))
            return m.group(0)
        label = label_for(target, cur_group)
        anchor = ""
        if loc:
            first = re.match(r"[A-Z]?\d+[a-z]?(?:\.[A-Za-z0-9]+)?", loc).group(0)
            cands = [h for h in REG[target]["heads"] if h[0] == first]
            want_bai = (kw or "").lower() == "bài"
            hit = next((h for h in cands if h[3] == want_bai), cands[0] if cands else None)
            if hit:
                anchor = "#" + hit[2]
                label += f" › {short_head(hit[1])}"
            else:
                label += f" ({(kw or 'mục').lower()} {loc})"
        path = posixpath.relpath(target, cur_dir or ".")
        return f"[{label}]({path}{anchor})"

    line = REF_RE.sub(fix, line)

    def fixbare(m):
        target = resolve(m.group(1), cur_dir)
        if target is None:
            return m.group(0)
        return f"[{label_for(target, cur_group)}]({posixpath.relpath(target, cur_dir or '.')})"
    line = BARE_RE.sub(fixbare, line)

    def fixdir(m):
        slug = m.group(1)
        if slug not in GROUPS:
            return m.group(0)
        target = f"{slug}/00-README.md"
        before = re.sub(r"[\s(*]+$", "", line[:m.start()]).lower()
        name = GROUPS[slug] if before.endswith("nhóm") or before.endswith("nhóm bài") else f"Nhóm bài {GROUPS[slug]}"
        return f"[{name}]({posixpath.relpath(target, cur_dir or '.')})"
    return DIR_RE.sub(fixdir, line)


PHRASES = [
    (re.compile(r"^(?:Phần dùng chung đã có ở nhóm RAG, không viết lại|Đã có ở nhóm RAG, không viết lại|Đã có, không viết lại|Dùng lại, không viết lại|Nền tảng dùng lại|Dùng lại|Liên quan)\s*:\s*"), "Nên xem trước: "),
    (re.compile(r"^Nền chung về ([^:]+):"), r"Nên xem trước, phần nền về \1:"),
    (re.compile(r"^Đã có ở nhóm RAG, không viết lại:"), "Nên xem trước:"),
    (re.compile(r"File này chỉ viết phần riêng của ([^.]*)\."), r"Bài này chỉ nói phần riêng của \1."),
    (re.compile(r"File này (?:chỉ )?viết phần (?:riêng|khác)\s*:"), "Riêng bài này tập trung vào:"),
    (re.compile(r"File này viết cách áp"), "Bài này nói cách áp"),
    (re.compile(r"File này viết phần \*\*"), "Bài này tập trung vào phần **"),
    (re.compile(r"[Ff]ile này mở rộng"), "bài này mở rộng"),
    (re.compile(r"File này"), "Bài này"),
    (re.compile(r"file này"), "bài này"),
]
LOCAL = [
    (re.compile(r"Không lặp lại nội dung các file trên\."), "Không nhắc lại nội dung các bài trên."),
    (re.compile(r"xem file nền mục 4"), "xem [An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md)"),
    (re.compile(r"\(qua file nền\)"), "(qua [Thực trạng SME Việt Nam](../thuc-trang-sme-viet-nam.md))"),
    (re.compile(r"Qua file nền của series"), "Qua bài [Nền tảng bằng chứng](../nen-tang-bang-chung.md) của series"),
    (re.compile(r"\*\*\[xem file pháp lý chung, mục 4\.4\]\*\*"), "([xem bài An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md))"),
    (re.compile(r"nhóm RAG(\*{0,2}) \((`(?:\.\./)?[a-z0-9-]+/`)\)"), r"nhóm bài\1 (\2)"),
    (re.compile(r"Phần đã có ở nhóm RAG, không lặp lại:"), "Đã học ở nhóm bài Tra cứu tài liệu (xem lại nếu cần):"),
    (re.compile(r"→ file này →"), "→ phần giới thiệu này →"),
    (re.compile(r"nhóm RAG"), "nhóm bài Tra cứu tài liệu"),
    (re.compile(r"Nhóm RAG"), "Nhóm bài Tra cứu tài liệu"),
    (re.compile(r"\(scratchpad, `python -I`, "), "(chạy thử trên máy người soạn, "),
    (re.compile(r"\(scratchpad, `python -I`\)"), "(chạy thử trên máy người soạn)"),
    (re.compile(r"\(scratchpad[,)]"), "(chạy thử trên máy người soạn)"),
    (re.compile(r"(?:trong|ở) scratchpad"), "trên máy người soạn"),
]


def split_header(lines):
    """Trả về (chỉ số bắt đầu thân bài, ngày, các dòng ghi chú còn giữ)."""
    i = 1
    hdr = []
    while i < len(lines):
        l = lines[i]
        if l.startswith("## ") or l.startswith("# ") or l.startswith("!!!") or l.strip() == "---":
            break
        if l.strip():
            hdr.append(re.sub(r"^>\s?", "", l).strip())
        i += 1
    if i < len(lines) and lines[i].strip() == "---":
        i += 1
    date, keep, law = "", [], False
    for l in hdr:
        if not l:
            continue
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", l)
        if m and not date:
            date = m.group(0)
        if "Không phải tư vấn" in l:
            law = True
        if re.match(r"^(Thuộc series|Trạng thái|Code mẫu|Quy ước|\*\*\[Nguồn\]\*\*)", l):
            continue
        if l.startswith("Ngày soạn"):
            rest = re.sub(r"^Ngày soạn[^.]*?\d{4}-\d{2}-\d{2}\.?\s*", "", l)
            if "[Nguồn]" in rest or "Quy ước" in rest or "như quy ước" in rest or "như các file khác" in rest:
                rest = " ".join(s for s in re.split(r"(?<=\.)\s+", rest) if "[Nguồn]" not in s and "quy ước" not in s.lower()
                                and "như các file khác" not in s)
            rest = re.sub(r"Thuộc series[^.]*\.\s*", "", rest)
            l = rest.strip()
            if not l:
                continue
        for pat, new in PHRASES + LOCAL:
            l = pat.sub(new, l)
        # câu pháp lý lặp: chỉ giữ một lần ở cuối
        l = re.sub(r"\s*Không phải tư vấn pháp lý( hay tư vấn thuế)?\.?\s*", " ", l).strip(" ;")
        if l and l not in ("Nên xem trước:",):
            keep.append(l[0].upper() + l[1:])
    if law:
        keep.append("Nội dung này không phải tư vấn pháp lý.")
    return i, date, keep


TIDY = [
    (re.compile(r"([Nn]hóm) \[Nhóm bài "), r"\1 [bài "),
    (re.compile(r"xem file an toàn dữ liệu"), "xem [An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md)"),
    (re.compile(r"\(file (?=\[)"), "("),
    (re.compile(r"\b([Xx])em file (?=\[)"), r"\1em "),
    (re.compile(r"\bfile (?=\[)"), ""),
]


def tidy(line):
    for pat, new in TIDY:
        line = pat.sub(new, line)
    return line


def preprocess(text, rel):
    lines = text.split("\n")
    info = {"date": ""}
    if not lines or not lines[0].startswith("# "):
        return text, info
    start, date, keep = split_header(lines)
    info["date"] = date
    out = [lines[0], ""]
    if keep:
        title = "Lưu ý khi đọc" if rel.endswith("00-README.md") else "Trước khi học"
        out.append(f'!!! note "{title}"')
        for k in keep:
            out.append("    " + tidy(convert_refs(replace_tags(k), rel)))
            out.append("")
    fence = False
    for l in lines[start:]:
        if l.lstrip().startswith("```"):
            fence = not fence
            out.append(l)
            continue
        if fence:
            out.append(l)
            continue
        for pat, new in LOCAL:
            l = pat.sub(new, l)
        for pat, new in PHRASES[-2:]:
            l = pat.sub(new, l)
        m = re.match(r"^(#{2,4})\s+(.*)$", l)
        if m:
            num, body, tags = norm_heading(m.group(2))
            out.append(f"{m.group(1)} {(num + ' ' + body).strip()}")
            if tags:
                out.append("")
                out.append(" ".join(tags))
            continue
        l = replace_tags(l)
        l = tidy(convert_refs(l, rel))
        out.append(l)
    return chr(10).join(out), info

# ----------------------------------------------------------------- hậu xử lý HTML


URL_RE = re.compile(r"(https?://[^\s<>\")]+[^\s<>\").,;:])")


def autolink(body):
    parts = re.split(r"(<[^>]+>)", body)
    skip = 0
    for i, p in enumerate(parts):
        if p.startswith("<"):
            low = p.lower()
            if re.match(r"<(a|code|pre)\b", low):
                skip += 1
            elif re.match(r"</(a|code|pre)>", low):
                skip = max(0, skip - 1)
        elif not skip:
            parts[i] = URL_RE.sub(lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1) if len(m.group(1)) < 46 else m.group(1)[:44] + "…"} ↗</a>', p)
    return "".join(parts)


def add_ref_ids(body):
    body = re.sub(r"<li><strong>([A-Z]{1,2}-?[A-Z]?\d+)\.?</strong>",
                  lambda m: f'<li id="ref-{m.group(1).lower()}"><strong>{m.group(1)}.</strong>', body)
    body = re.sub(r"<tr>\s*<td([^>]*)>([A-Z]{1,2}-?[A-Z]?\d+)</td>",
                  lambda m: f'<tr id="ref-{m.group(2).lower()}"><td{m.group(1)}>{m.group(2)}</td>', body)
    return body


def tokens_to_html(body):
    ids = set(re.findall(r'id="(ref-[a-z0-9-]+)"', body))

    def t(m):
        kind, label, tip = m.group(1), m.group(2), m.group(3)
        dl, dt = TAG_DEFAULT.get(kind, ("", ""))
        label = label or dl
        if kind == "note":
            return f'<span class="tg tg-note">{html.escape(label)}</span>'
        tip = tip or dt
        cls = "src" if kind == "src" else kind
        return f'<span class="tg tg-{cls}" title="{html.escape(tip, quote=True)}">{html.escape(label)}</span>'

    body = re.sub(r"\[\[t:(\w+)%s([^%s\]]*)%s([^\]]*)\]\]" % (SEP, SEP, SEP), t, body)

    def r(m):
        rid = m.group(1)
        if f"ref-{rid.lower()}" in ids:
            return f'<a class="cite" href="#ref-{rid.lower()}">Nguồn {rid}</a>'
        return f'<span class="cite nolink">Nguồn {rid}</span>'
    return re.sub(r"\[\[r:([A-Za-z0-9-]+)\]\]", r, body)


def wrap_author_notes(body):
    pat = re.compile(r'<h2 id="([^"]*)">([^<]*)</h2>(.*?)(?=<h2 id=|\Z)', re.S)

    def f(m):
        if not AUTH_RE.search(m.group(2)):
            return m.group(0)
        return ('<details class="authnote" id="' + m.group(1) + '"><summary><b>Ghi chú kiểm chứng</b> · những điều chưa chắc chắn, '
                'dành cho người soạn tài liệu (người học có thể bỏ qua)</summary>' + m.group(3) + "</details>")
    return pat.sub(f, body)


def post(body):
    body = add_ref_ids(body)
    body = tokens_to_html(body)
    body = autolink(body)
    return wrap_author_notes(body)

# ----------------------------------------------------------------- từ điển

GLOSSARY = [
    ("llm", "Mô hình ngôn ngữ lớn (LLM)", r"LLM|mô hình ngôn ngữ lớn", "Loại AI đọc và viết chữ như ChatGPT, Claude, Gemini.",
     "Loại AI đọc và viết chữ như ChatGPT, Claude, Gemini. Nó học từ lượng chữ khổng lồ rồi đoán chữ tiếp theo, nên viết rất trôi chảy nhưng vẫn có thể sai."),
    ("prompt", "Prompt (câu lệnh)", r"prompt", "Đoạn chữ bạn gõ để giao việc cho AI.",
     "Đoạn chữ bạn gõ để giao việc cho AI. Prompt càng rõ việc, đầu vào, cách trình bày thì kết quả càng ổn định."),
    ("api", "API", r"API", "Cổng để phần mềm này nói chuyện với phần mềm khác.",
     "Cổng để phần mềm này gọi phần mềm khác. Dùng API, chương trình của bạn gửi yêu cầu cho AI và nhận kết quả, thay vì bạn gõ vào khung chat."),
    ("api-key", "Khóa API (API key)", r"khóa API|API key", "Chuỗi ký tự như mật khẩu để chương trình dùng dịch vụ AI.",
     "Chuỗi ký tự như mật khẩu, cho phép chương trình của bạn dùng dịch vụ AI và bị tính tiền vào tài khoản của bạn. Không được để lộ ra ngoài."),
    ("token", "Token", r"token", "Đơn vị đếm chữ của AI; tiền dùng API tính theo token.",
     "Đơn vị đếm chữ của AI, khoảng một âm tiết hoặc một phần của từ. Tiền dùng API tính theo số token gửi vào và nhận về."),
    ("rag", "RAG (hỏi đáp dựa trên tài liệu)", r"RAG", "AI trả lời dựa trên tài liệu của bạn: tìm đoạn liên quan trước, rồi mới đọc và trả lời.",
     "Cách cho AI trả lời dựa trên tài liệu của riêng bạn: trước tiên tìm các đoạn liên quan, rồi đưa những đoạn đó cho AI đọc và trả lời, kèm trích dẫn."),
    ("chunk", "Khối (chunk)", r"chunk", "Đoạn tài liệu được cắt nhỏ để tìm kiếm và đưa cho AI đọc.",
     "Đoạn tài liệu được cắt nhỏ (ví dụ theo từng mục) để tìm kiếm và đưa cho AI đọc."),
    ("vector", "Vector, embedding", r"embedding|vector", "Cách biến một đoạn chữ thành dãy số để máy so độ giống nhau về nghĩa.",
     "Cách biến một đoạn chữ thành dãy số để máy so sánh xem hai đoạn có giống nhau về nghĩa hay không, kể cả khi dùng từ khác nhau."),
    ("bm25", "BM25", r"BM25", "Cách tìm kiếm theo từ khóa, giống ô tìm kiếm thông thường.",
     "Cách tìm kiếm cổ điển: chấm điểm đoạn văn theo số từ khóa trùng với câu hỏi. Nhanh, rẻ, hiểu từ khóa nhưng không hiểu nghĩa."),
    ("ocr", "OCR", r"OCR", "Công nghệ đọc chữ từ ảnh hoặc bản scan.",
     "Công nghệ đọc chữ từ ảnh chụp hoặc bản scan để biến thành văn bản máy tính xử lý được."),
    ("json", "JSON", r"JSON", "Cách viết dữ liệu có khung rõ ràng để máy đọc được.",
     "Cách viết dữ liệu theo khung rõ ràng (tên trường và giá trị) để máy đọc chính xác, ví dụ {\"so_hoa_don\": \"0012\", \"tong_tien\": 1500000}."),
    ("agent", "Agent (AI tự hành)", r"agent|Agent", "AI tự chọn bước làm và tự gọi công cụ để hoàn thành việc.",
     "Chương trình AI tự quyết định làm bước nào tiếp theo và tự gọi công cụ để hoàn thành việc, thay vì làm theo kịch bản cố định."),
    ("workflow", "Workflow (quy trình tự động)", r"workflow", "Chuỗi bước cố định đã thiết kế sẵn; AI chỉ làm một số bước.",
     "Chuỗi bước cố định đã được thiết kế sẵn, có chỗ nào dùng AI, chỗ nào dùng quy tắc, chỗ nào người duyệt. Dễ kiểm soát hơn agent."),
    ("tool-use", "Công cụ cho AI (function calling, tool use)", r"function calling|tool use", "Cách để AI nhờ chương trình chạy một chức năng như tra đơn hàng.",
     "Cách để AI yêu cầu chương trình chạy một chức năng (tra đơn hàng, gửi email...) rồi nhận kết quả để trả lời tiếp."),
    ("mcp", "MCP", r"MCP", "Chuẩn chung để nối AI với công cụ và dữ liệu bên ngoài.",
     "Chuẩn chung để nối AI với các công cụ và nguồn dữ liệu bên ngoài, giống ổ cắm chuẩn dùng được cho nhiều thiết bị."),
    ("prompt-injection", "Prompt injection (lệnh ẩn)", r"prompt injection", "Tài liệu hoặc tin nhắn giấu lệnh để AI làm sai ý chủ.",
     "Kẻ xấu, hoặc chính một tài liệu lạ, giấu lệnh trong nội dung (ví dụ \"bỏ qua mọi hướng dẫn trước\") để AI làm theo. Nguy hiểm khi AI có quyền gọi công cụ."),
    ("hallucination", "Hallucination (AI bịa)", r"hallucination|ảo giác", "AI nói điều sai nhưng nghe rất thuyết phục.",
     "Hiện tượng AI bịa ra thông tin sai nhưng trình bày rất tự tin và trôi chảy."),
    ("sop", "SOP (quy trình chuẩn)", r"SOP", "Quy trình làm việc chuẩn viết thành văn bản.",
     "Quy trình làm việc chuẩn bằng văn bản: ai làm gì, theo thứ tự nào, khi nào chuyển cho người khác."),
    ("project-gem", "Project, Gem, GPT tùy chỉnh", r"Project|Gem|GPT tùy chỉnh", "Tính năng cho bạn lưu sẵn chỉ dẫn và tài liệu để dùng lại nhiều lần.",
     "Tính năng của Claude (Project), Gemini (Gem), ChatGPT (GPT tùy chỉnh) cho bạn lưu sẵn chỉ dẫn và tài liệu để dùng lại, không phải dán lại mỗi lần."),
    ("roi", "ROI", r"ROI", "Lợi ích thu về so với chi phí bỏ ra.", "Lợi ích thu về so với chi phí bỏ ra."),
    ("ab-test", "A/B test", r"A/B", "So sánh hai cách làm trên hai nhóm để xem cách nào tốt hơn.",
     "So sánh hai cách làm trên hai nhóm khách hoặc nhóm việc để xem cách nào cho kết quả tốt hơn."),
    ("recall", "Recall@k", r"recall@k|recall", "Trong k kết quả đầu, tìm thấy đúng đoạn cần bao nhiêu phần trăm câu hỏi.",
     "Trong k kết quả tìm kiếm đầu tiên, có bao nhiêu phần trăm câu hỏi tìm thấy đúng đoạn cần."),
    ("mrr", "MRR", r"MRR", "Điểm đo đoạn đúng nằm cao hay thấp trong danh sách kết quả.",
     "Điểm đo đoạn đúng nằm ở vị trí cao hay thấp trong danh sách kết quả tìm kiếm. Càng gần 1 càng tốt."),
    ("ci", "Khoảng tin cậy", r"khoảng tin cậy", "Khoảng giá trị mà con số thật nhiều khả năng nằm trong đó.",
     "Khoảng giá trị mà con số thật nhiều khả năng nằm trong đó. Mẫu càng ít, khoảng càng rộng, nên con số đo trên ít ca chưa chắc chắn."),
    ("llm-judge", "LLM-as-judge (AI chấm điểm)", r"LLM-as-judge|LLM làm giám khảo|LLM judge", "Dùng một AI để chấm câu trả lời của AI khác.",
     "Dùng một AI để chấm câu trả lời của AI khác. Rẻ và nhanh nhưng có thiên lệch, nên cần người kiểm lại một phần."),
    ("benchmark", "Benchmark", r"benchmark", "Bộ bài kiểm tra chuẩn để so sánh các hệ thống.", "Bộ bài kiểm tra chuẩn dùng để so sánh các hệ thống với nhau."),
    ("idempotent", "Idempotent", r"idempotent", "Chạy một yêu cầu nhiều lần chỉ gây hiệu ứng một lần.",
     "Tính chất khi chạy cùng một yêu cầu nhiều lần chỉ gây hiệu ứng một lần, ví dụ không hoàn tiền hai lần dù bấm hai lần."),
    ("webhook", "Webhook", r"webhook", "Phần mềm tự báo tin cho phần mềm khác ngay khi có sự kiện.",
     "Cách một phần mềm tự báo tin cho phần mềm khác ngay khi có sự kiện, ví dụ vừa có đơn hàng mới."),
    ("regex", "Biểu thức chính quy (regex)", r"biểu thức chính quy|regex", "Mẫu ký tự để máy tìm chuỗi theo quy tắc, ví dụ số điện thoại.",
     "Mẫu ký tự để máy tìm chuỗi theo quy tắc, ví dụ tìm mọi số điện thoại hay email trong một đoạn văn."),
    ("dpa", "DPA", r"DPA", "Hợp đồng xử lý dữ liệu giữa doanh nghiệp và nhà cung cấp dịch vụ.",
     "Thỏa thuận xử lý dữ liệu (Data Processing Addendum) giữa doanh nghiệp và nhà cung cấp dịch vụ."),
    ("shadow-ai", "Shadow AI", r"shadow AI|Shadow AI", "Nhân viên tự dùng công cụ AI ngoài tầm kiểm soát của công ty.",
     "Việc nhân viên tự dùng công cụ AI (thường bằng tài khoản cá nhân) mà công ty không biết hoặc không quản lý."),
    ("kappa", "Kappa", r"kappa", "Điểm đo hai người chấm đồng ý với nhau đến đâu, đã trừ phần trùng hợp ngẫu nhiên.",
     "Điểm đo mức đồng ý giữa hai người chấm (hoặc người và AI), đã trừ phần trùng hợp ngẫu nhiên."),
    ("cer", "CER", r"CER", "Tỷ lệ ký tự đọc sai khi chuyển ảnh hoặc âm thanh thành chữ.",
     "Tỷ lệ ký tự bị đọc sai khi chuyển ảnh hoặc âm thanh thành chữ. Càng thấp càng tốt."),
    ("passk", "pass^k", r"pass\^k|pass\^\d+", "Tỷ lệ việc AI làm đúng cả k lần liên tiếp; đo độ ổn định.",
     "Tỷ lệ việc mà AI làm đúng cả k lần liên tiếp. Đo độ ổn định, vì AI làm đúng một lần chưa chắc lần sau cũng đúng."),
    ("sandbox", "Sandbox", r"sandbox", "Môi trường cách ly để thử, lỗi cũng không ảnh hưởng dữ liệu thật.",
     "Môi trường cách ly để thử nghiệm, nếu có lỗi cũng không ảnh hưởng dữ liệu thật."),
    ("fine-tune", "Tinh chỉnh (fine-tune)", r"fine-tun\w*|tinh chỉnh", "Huấn luyện thêm một mô hình có sẵn bằng dữ liệu riêng.",
     "Huấn luyện thêm một mô hình có sẵn bằng dữ liệu riêng. Tốn công và tiền hơn nhiều so với viết prompt tốt."),
    ("context-window", "Cửa sổ ngữ cảnh", r"cửa sổ ngữ cảnh|context window", "Lượng chữ tối đa AI đọc được trong một lần.",
     "Lượng chữ tối đa mà AI đọc được trong một lần hỏi, gồm cả câu hỏi, tài liệu đính kèm và câu trả lời."),
    ("csv", "CSV", r"CSV", "Tệp bảng dạng chữ thuần, mở được bằng Excel.", "Tệp bảng dạng chữ thuần, các cột ngăn bằng dấu phẩy, mở được bằng Excel hoặc Google Sheets."),
    ("sla", "SLA", r"SLA", "Cam kết thời hạn xử lý.", "Cam kết về thời hạn xử lý, ví dụ trả lời khách trong 2 giờ."),
    ("log", "Log (nhật ký)", r"log", "Bản ghi lại mỗi lần hệ thống chạy: ai hỏi gì, AI trả lời gì.",
     "Bản ghi lại mỗi lần hệ thống chạy: ai hỏi gì, AI trả lời gì, tốn bao nhiêu. Có log mới biết chuyện gì đã xảy ra khi có sai sót."),
    ("coding-agent", "Coding agent", r"coding agent", "Chương trình AI tự đọc file, viết và chạy code trên máy bạn để làm việc bạn giao.",
     "Chương trình AI chạy trong cửa sổ dòng lệnh: nó đọc file trong thư mục bạn mở, viết script, chạy lệnh và báo kết quả. Vì chạy được lệnh trên máy bạn nên cần thư mục riêng và dữ liệu thử trước (ví dụ Claude Code, Antigravity)."),
    ("script", "Script", r"script", "Một file chứa các lệnh để máy chạy lại nhiều lần.",
     "Một file chứa các lệnh (ở đây thường là Python) để máy làm lại cùng một việc mỗi lần bạn chạy. Script chạy lại cho kết quả giống nhau, khác với nhờ AI làm lại từ đầu."),
    ("csv", "CSV", r"CSV", "File bảng dạng chữ, mỗi dòng một hàng, các ô cách nhau bằng dấu phẩy.",
     "File bảng dạng chữ thuần: mỗi dòng là một hàng, các ô cách nhau bằng dấu phẩy hoặc chấm phẩy. Mở được bằng Excel hoặc Notepad. Nếu chữ tiếng Việt bị vỡ, mở bằng Notepad hoặc nhập qua Data > From Text/CSV và chọn UTF-8."),
    ("log", "Log (nhật ký chạy)", r"log", "Bản ghi lại từng việc agent đã làm, để xem lại sau.",
     "Bản ghi theo thứ tự thời gian mọi việc agent đã làm (đọc file nào, chạy lệnh gì, kết quả ra sao). Nhờ log mới kiểm được agent làm đúng hay tự báo đúng."),
    ("hat-giong", "Hạt giống (seed)", r"hạt giống", "Một con số cố định để máy sinh ra cùng một bộ dữ liệu ngẫu nhiên mỗi lần.",
     "Máy sinh dữ liệu giả bằng cách bốc ngẫu nhiên. Đặt cùng một hạt giống thì lần nào cũng ra đúng bộ dữ liệu cũ, nên người khác chạy lại được và so sánh được."),
    ("ma-bam", "Mã băm (hash)", r"mã băm", "Dấu vân tay của một file: đổi một ký tự thì mã đổi hoàn toàn.",
     "Một chuỗi ký tự được tính từ nội dung file. Hai file giống từng byte thì mã băm giống nhau; sửa dù một ký tự thì mã khác hẳn. Dùng để kiểm agent có sửa file gốc hay không."),
    ("n-1", "n = 1 (cỡ mẫu)", r"n ?= ?1", "Chỉ có một lần chạy: đủ để thấy kiểu sai, chưa đủ để nói chắc.",
     "n là số lần chạy hoặc số mẫu đã đo. n = 1 nghĩa là mới chạy một lần: cho thấy agent làm được gì và sai ở kiểu nào, nhưng không đo được độ ổn định và không đủ để so sánh hai công cụ."),
    ("terminal", "Dòng lệnh (Terminal, PowerShell)", r"cửa sổ dòng lệnh|PowerShell", "Cửa sổ để gõ lệnh cho máy thay vì bấm chuột.",
     "Cửa sổ chữ nơi bạn gõ lệnh và máy trả lời bằng chữ. Trên Windows thường dùng PowerShell. Coding agent chạy trong cửa sổ này."),
    ("abc", "Phân loại ABC", r"phân loại ABC|ABC", "Chia mặt hàng thành nhóm A, B, C theo mức đóng góp doanh thu để biết nên chú ý hàng nào trước.",
     "Cách xếp mặt hàng theo đóng góp: nhóm A là số ít mặt hàng tạo phần lớn doanh thu (cần canh tồn kho sát), nhóm C là nhiều mặt hàng đóng góp ít. Ngưỡng chia (ví dụ 80% và 95% doanh thu cộng dồn) là do người dùng đặt."),
    ("wape", "WAPE", r"WAPE", "Sai số dự báo tính bằng tỉ lệ: càng thấp càng sát thực tế.",
     "Tổng sai lệch tuyệt đối giữa số dự báo và số bán thật, chia cho tổng số bán thật. WAPE 20% nghĩa là dự báo lệch trung bình khoảng một phần năm so với thực tế. Chỉ có ý nghĩa khi so với một mốc đơn giản."),
    ("holdout", "Hold-out (tháng giữ lại)", r"hold-out|giữ lại để đo", "Giấu vài tháng cuối khi dự báo, rồi so với số thật của chính những tháng đó.",
     "Cách kiểm công thức dự báo trung thực: không cho công thức nhìn thấy vài tháng cuối, bảo nó dự báo, rồi đối chiếu với số bán thật của các tháng đó."),
    ("sku", "SKU", r"SKU", "Mã định danh của một mặt hàng cụ thể (một loại, một cỡ, một màu).",
     "Mã quản lý riêng cho từng biến thể hàng hóa, ví dụ cùng một loại áo nhưng khác cỡ thì khác SKU."),
    ("bom", "BOM (dấu đầu file)", r"BOM", "Ba byte đầu file giúp Excel nhận ra chữ tiếng Việt.",
     "Ba byte ở đầu file văn bản cho biết file lưu bằng UTF-8. Nó giúp Excel mở đúng chữ có dấu, nhưng một số script đọc file có thể thấy nó như một ký tự lạ dính vào tên cột đầu."),
    ("utf8", "UTF-8", r"UTF-8", "Cách lưu chữ cho phép viết đủ tiếng Việt có dấu.",
     "Bảng mã phổ biến cho văn bản. Nếu chữ tiếng Việt hiện thành ký tự lạ, thường là mở file bằng bảng mã khác UTF-8."),
    ("pip", "pip", r"pip install", "Lệnh cài thêm thư viện cho Python.",
     "Công cụ đi kèm Python để tải và cài thêm thư viện, ví dụ `pip install openpyxl` để Python đọc được file Excel."),
]

IGNORE_TAGS = re.compile(r"^<(a|code|pre|h[1-6]|summary|abbr|button|script|style)\b", re.I)
CLOSE_TAGS = re.compile(r"^</(a|code|pre|h[1-6]|summary|abbr|button|script|style)>", re.I)


def glossary_wrap(body, root):
    used = set()
    compiled = [(gid, re.compile(r"(?<![\w@./-])(?:%s)(?![\w@-])" % pat)) for gid, _, pat, _, _ in GLOSSARY]
    short = {g[0]: g[3] for g in GLOSSARY}
    parts = re.split(r"(<[^>]+>)", body)
    skip = 0
    for i, p in enumerate(parts):
        if p.startswith("<"):
            if IGNORE_TAGS.match(p):
                skip += 1
            elif CLOSE_TAGS.match(p):
                skip = max(0, skip - 1)
            continue
        if skip or not p.strip():
            continue
        for gid, rx in compiled:
            if gid in used:
                continue
            m = rx.search(p)
            if m:
                used.add(gid)
                rep = f'<a class="gl" href="{root}tu-dien.html#{gid}" title="{html.escape(short[gid], quote=True)}">{m.group(0)}</a>'
                p = p[:m.start()] + rep + p[m.end():]
        parts[i] = p
    return "".join(parts)


def glossary_html():
    items = sorted(GLOSSARY, key=lambda g: g[1].lower())
    out = []
    for gid, name, _, short, long_ in items:
        out.append(f'<div class="gterm" id="{gid}"><h2>{html.escape(name)}</h2><p>{html.escape(long_)}</p></div>')
    return "".join(out)
