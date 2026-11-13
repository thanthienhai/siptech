"""Bộ nhận diện SIPTech (phương án B: chữ S nối nút).
Sinh SVG (chữ đã chuyển thành đường nét), PNG, favicon, ảnh mạng xã hội và trang xem thử.
Chạy: python design/make_kit.py        (cần: fonttools, uharfbuzz, pillow; Edge để xuất PNG)
Phông Be Vietnam Pro (giấy phép OFL) nằm ở design/fonts/.
"""
import io
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

HERE = Path(__file__).parent
KIT = HERE / "logo-kit"
SVG = KIT / "svg"
PNG = KIT / "png"
SOCIAL = KIT / "social"
FONTS = HERE / "fonts"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

BRAND, NAVY, ACC, SOFT = "#1d4ed8", "#0b1f4d", "#ff7a3d", "#8fb0ff"
GREY, GREY_D = "#56627d", "#b9c6e6"
S_PATH = "M44 20C44 12 33 11 27 14C20 18 21 26 30 30C39 34 44 38 41 45C38 52 27 52 20 46"
NODES = [(44, 20), (20, 46)]
TAGLINE = "Tư vấn giải pháp AI trong doanh nghiệp"

# ---------------- chữ thành đường nét ----------------
_fonts = {}


def _font(name):
    if name not in _fonts:
        p = FONTS / f"BeVietnamPro-{name}.ttf"
        tt = TTFont(p)
        hbf = hb.Font(hb.Face(hb.Blob.from_file_path(str(p))))
        _fonts[name] = (tt, tt.getGlyphSet(), hbf, tt["head"].unitsPerEm, tt["OS/2"].sCapHeight)
    return _fonts[name]


def text_path(text, weight, size, x, y, track=0.0, anchor="start"):
    """Trả về (d, rộng). y là đường cơ sở. track tính theo em."""
    tt, gs, hbf, upm, cap = _font(weight)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbf, buf, {"kern": True, "liga": True})
    k = size / upm
    pen_x = 0.0
    glyphs = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        glyphs.append((hbf.glyph_to_string(info.codepoint), pen_x + pos.x_offset * k, pos.y_offset * k))
        pen_x += pos.x_advance * k + track * size
    width = pen_x - track * size
    ox = x if anchor == "start" else (x - width / 2 if anchor == "middle" else x - width)
    parts = []
    for name, gx, gy in glyphs:
        sp = SVGPathPen(gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
        gs[name].draw(TransformPen(sp, (k, 0, 0, -k, ox + gx, y - gy)))
        d = sp.getCommands()
        if d:
            parts.append(d)
    return " ".join(parts), width


def cap_height(weight, size):
    return _font(weight)[4] * size / _font(weight)[3]


# ---------------- biểu tượng ----------------
_mid = [0]


def icon_inner(mode, shape="tile", scale_s=1.0):
    """Biểu tượng trong khung 64x64. mode: color | reverse | black | white."""
    s_tf = "" if scale_s == 1 else f' transform="translate(32 32) scale({scale_s}) translate(-32 -32)"'
    s_el = f'<path d="{S_PATH}" fill="none" stroke="{{c}}" stroke-width="5.5" stroke-linecap="round"/>'
    n_el = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="{{n}}"/>' for x, y in NODES)
    base = (lambda: '<rect width="64" height="64" rx="16" fill="{t}"/>') if shape == "tile" else \
        (lambda: '<circle cx="32" cy="32" r="32" fill="{t}"/>') if shape == "circle" else \
        (lambda: '<rect width="64" height="64" fill="{t}"/>')
    if mode in ("color", "reverse"):
        tile, sc = (NAVY, "#fff") if mode == "color" else ("#fff", NAVY)
        return (base().format(t=tile) + f"<g{s_tf}>" + s_el.format(c=sc) + n_el.format(n=ACC) + "</g>")
    col = "#111111" if mode == "black" else "#ffffff"
    _mid[0] += 1
    mid = f"m{_mid[0]}"
    cut = (f'<mask id="{mid}"><rect width="64" height="64" fill="#fff"/><g{s_tf}>' + s_el.format(c="#000") +
           n_el.format(n="#000") + "</g></mask>")
    return cut + f'<g mask="url(#{mid})">' + base().format(t=col) + "</g>"


def svg_doc(w, h, body, title, bg=None):
    r = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">'
            f"<title>{title}</title>{r}{body}</svg>")


PAL = {
    "color": dict(sip=NAVY, tech=BRAND, tag=GREY),
    "reverse": dict(sip="#fff", tech=SOFT, tag=GREY_D),
    "black": dict(sip="#111111", tech="#111111", tag="#111111"),
    "white": dict(sip="#fff", tech="#fff", tag="#fff"),
}
MODE_NAME = {"color": "Màu", "reverse": "Nền tối", "black": "Đen", "white": "Trắng"}


def wordmark_parts(mode, size, x, y, anchor="start"):
    p = PAL[mode]
    d1, w1 = text_path("SIP", "ExtraBold", size, 0, 0, track=-0.02)
    d2, w2 = text_path("Tech", "ExtraBold", size, 0, 0, track=-0.02)
    gap = -0.02 * size
    total = w1 + gap + w2
    ox = x if anchor == "start" else x - total / 2
    return (f'<path transform="translate({ox:.2f} {y:.2f})" d="{d1}" fill="{p["sip"]}"/>'
            f'<path transform="translate({ox + w1 + gap:.2f} {y:.2f})" d="{d2}" fill="{p["tech"]}"/>'), total


def horizontal(mode, tagline):
    wm = 40
    cap = cap_height("ExtraBold", wm)
    x0 = 64 + 16
    if tagline:
        y_wm, y_tag = 33.5, 54
        td, tw = text_path(TAGLINE, "Medium", 11.2, x0, y_tag, track=0.005)
        tag = f'<path d="{td}" fill="{PAL[mode]["tag"]}"/>'
    else:
        y_wm = 32 + cap / 2
        tag, tw = "", 0
    wmsvg, ww = wordmark_parts(mode, wm, x0, y_wm)
    w = x0 + max(ww, tw) + 2
    body = icon_inner(mode) + wmsvg + tag
    return svg_doc(w, 64, body, "SIPTech" + (" - " + TAGLINE if tagline else "")), w, 64


def stacked(mode, tagline):
    wm = 44
    cap = cap_height("ExtraBold", wm)
    y_wm = 64 + 20 + cap
    wmsvg, ww = wordmark_parts(mode, wm, 0, y_wm, anchor="middle")
    td, tw = text_path(TAGLINE, "Medium", 12.5, 0, y_wm + 26, track=0.005, anchor="middle") if tagline else ("", 0)
    W = max(ww, tw) + 4
    cx = W / 2
    # dịch tâm về giữa khung
    body = (f'<g transform="translate({cx - 32:.2f} 0)">{icon_inner(mode)}</g>'
            f'<g transform="translate({cx:.2f} 0)">{wmsvg}'
            + (f'<path transform="translate({cx:.2f} 0)" d="{td}" fill="{PAL[mode]["tag"]}"/>' if tagline else "") + "</g>")
    # tagline đã căn giữa quanh 0 nên chỉ cần tịnh tiến một lần
    body = (f'<g transform="translate({cx - 32:.2f} 0)">{icon_inner(mode)}</g>'
            f'<g transform="translate({cx:.2f} 0)">{wmsvg}'
            + (f'<path d="{td}" fill="{PAL[mode]["tag"]}"/>' if tagline else "") + "</g>")
    H = y_wm + (34 if tagline else 12)
    return svg_doc(W, H, body, "SIPTech"), W, H


def wordmark_only(mode):
    wm = 48
    cap = cap_height("ExtraBold", wm)
    wmsvg, ww = wordmark_parts(mode, wm, 2, cap + 2)
    return svg_doc(ww + 4, cap + 14, wmsvg, "SIPTech"), ww + 4, cap + 14


# ---------------- ảnh mạng xã hội ----------------

def social(w, h, kind):
    big = Path
    body = []
    # chữ S trang trí lớn bên phải
    k = h * 1.15 / 64
    body.append(f'<g opacity=".09" transform="translate({w - 64 * k * 0.80:.1f} {h * 0.5 - 32 * k:.1f}) scale({k:.3f})">'
                f'<path d="{S_PATH}" fill="none" stroke="#fff" stroke-width="5.5" stroke-linecap="round"/></g>')
    unit = h / 630
    pad = 84 * unit if kind != "linkedin" else 70
    # logo ngang bản nền tối (không tagline), cao 64*s
    s = (1.25 if kind != "linkedin" else 1.0) * unit if kind != "linkedin" else 1.0
    lh, lw = 64, 0
    lock_svg, lw, lh = horizontal("reverse", False)
    inner = lock_svg[lock_svg.index(">") + 1: lock_svg.rindex("</svg>")]
    inner = inner.replace(f"<title>SIPTech</title>", "")
    body.append(f'<g transform="translate({pad:.1f} {pad * 0.9:.1f}) scale({s:.3f})">{inner}</g>')
    if kind == "linkedin":
        d, _ = text_path("Đưa AI vào doanh nghiệp đúng cách", "ExtraBold", 40, pad, h - 120, track=-0.02)
        body.append(f'<path d="{d}" fill="#fff"/>')
        d, _ = text_path(TAGLINE, "Medium", 22, pad, h - 78, track=0.003)
        body.append(f'<path d="{d}" fill="{GREY_D}"/>')
    else:
        fs = 66 * unit
        y1 = h * 0.54
        d, _ = text_path("Đưa AI vào doanh nghiệp", "ExtraBold", fs, pad, y1, track=-0.025)
        body.append(f'<path d="{d}" fill="#fff"/>')
        d1, w1 = text_path("đúng cách", "ExtraBold", fs, pad, y1 + fs * 1.18, track=-0.025)
        body.append(f'<path d="{d1}" fill="{SOFT}"/>')
        d2, _ = text_path(": từng bước, đo được", "ExtraBold", fs, pad + w1, y1 + fs * 1.18, track=-0.025)
        body.append(f'<path d="{d2}" fill="#fff"/>')
        d, _ = text_path(TAGLINE, "Medium", 27 * unit, pad, y1 + fs * 1.18 + 56 * unit, track=0.003)
        body.append(f'<path d="{d}" fill="{GREY_D}"/>')
        d, _ = text_path("5 bài toán  ·  40 cấp độ  ·  có nguồn, có đo", "SemiBold", 22 * unit, pad, h - pad * 0.7, track=0.01)
        body.append(f'<path d="{d}" fill="{SOFT}"/>')
    return svg_doc(w, h, "".join(body), "SIPTech", bg=NAVY)


# ---------------- xuất PNG qua Edge ----------------

def render_png(svg_text, out_png, width, height=None, transparent=True, tmp=None):
    """Vẽ SVG ở độ phân giải lớn rồi thu nhỏ bằng Lanczos để giữ nét."""
    import re
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
    vw, vh = float(m.group(1)), float(m.group(2))
    if height is None:
        height = round(width * vh / vw)
    big_w = max(width, 1400) if vw >= vh else max(width, 1400)
    big_h = round(big_w * vh / vw)
    tmp = tmp or (KIT / "_tmp")
    tmp.mkdir(exist_ok=True)
    s = svg_text.replace(f'width="{vw:.0f}" height="{vh:.0f}"', f'width="{big_w}" height="{big_h}"', 1)
    page = tmp / "r.html"
    page.write_text(f'<!doctype html><meta charset="utf-8"><style>html,body{{margin:0;background:transparent}}svg{{display:block}}</style>{s}', encoding="utf-8")
    shot = tmp / "shot.png"
    args = [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={big_w},{big_h + 120}",
            f"--screenshot={shot}", "--default-background-color=00000000" if transparent else "--default-background-color=ffffffff",
            page.as_uri()]
    subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=60)
    im = Image.open(shot).convert("RGBA").crop((0, 0, big_w, big_h))
    im = im.resize((width, height), Image.LANCZOS)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_png)
    return im


def main():
    if KIT.exists():
        shutil.rmtree(KIT)
    for d in (SVG, PNG, SOCIAL):
        d.mkdir(parents=True)
    files = {}

    # --- SVG ---
    for mode in ("color", "reverse", "black", "white"):
        files[f"icon-{mode}"] = svg_doc(64, 64, icon_inner(mode), "SIPTech")
        for tg, tn in ((False, ""), (True, "-tagline")):
            files[f"lockup-horizontal{tn}-{mode}"] = horizontal(mode, tg)[0]
            files[f"lockup-stacked{tn}-{mode}"] = stacked(mode, tg)[0]
        files[f"wordmark-{mode}"] = wordmark_only(mode)[0]
    files["avatar-square"] = svg_doc(64, 64, icon_inner("color", "square", 0.82), "SIPTech")
    files["avatar-circle"] = svg_doc(64, 64, icon_inner("color", "circle", 0.8), "SIPTech")
    files["avatar-circle-blue"] = svg_doc(64, 64, icon_inner("color", "circle", 0.8).replace(NAVY, BRAND, 1), "SIPTech")
    for name, svg in files.items():
        (SVG / f"{name}.svg").write_text(svg, encoding="utf-8")
    # favicon.svg: khung bo nhỏ hơn để rõ ở 16px
    (KIT / "favicon.svg").write_text(files["icon-color"], encoding="utf-8")

    # --- ảnh mạng xã hội (SVG + PNG) ---
    socials = {"og-image-1200x630": (1200, 630, "og"), "facebook-cover-1640x624": (1640, 624, "fb"),
               "linkedin-banner-1584x396": (1584, 396, "linkedin")}
    for name, (w, h, kind) in socials.items():
        sv = social(w, h, kind)
        (SOCIAL / f"{name}.svg").write_text(sv, encoding="utf-8")
        render_png(sv, SOCIAL / f"{name}.png", w, h, transparent=False)

    # --- PNG ---
    for sz in (16, 32, 48, 64, 128, 180, 192, 256, 512, 1024):
        render_png(files["icon-color"], PNG / f"icon-color-{sz}.png", sz, sz)
    for sz in (512,):
        render_png(files["icon-reverse"], PNG / f"icon-reverse-{sz}.png", sz, sz)
        render_png(files["icon-black"], PNG / f"icon-black-{sz}.png", sz, sz)
        render_png(files["icon-white"], PNG / f"icon-white-{sz}.png", sz, sz)
    render_png(files["avatar-square"], PNG / "avatar-square-800.png", 800, 800)
    render_png(files["avatar-circle"], PNG / "avatar-circle-800.png", 800, 800)
    render_png(files["avatar-circle-blue"], PNG / "avatar-circle-blue-800.png", 800, 800)
    for name in files:
        if name.startswith(("lockup-", "wordmark-")):
            render_png(files[name], PNG / f"{name}-1600.png", 1600 if "horizontal" in name or "wordmark" in name else 1000)

    # favicon.ico
    ims = [Image.open(PNG / f"icon-color-{s}.png") for s in (16, 32, 48)]
    ims[2].save(KIT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[])
    shutil.rmtree(KIT / "_tmp", ignore_errors=True)
    print("files:", len(files), "->", KIT)


if __name__ == "__main__":
    sys.exit(main())
