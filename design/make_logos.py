"""Sinh 5 phương án logo SIPTech (SVG) và trang xem thử design/logo-options/index.html.
Chạy: python design/make_logos.py
"""
from pathlib import Path

OUT = Path(__file__).parent / "logo-options"
OUT.mkdir(exist_ok=True)

BRAND, NAVY, ACC = "#1d4ed8", "#0b1f4d", "#ff7a3d"

# mode: "light" (trên nền sáng) hoặc "dark" (trên nền xanh đậm)


def icon_a(m):
    tile, fg = (BRAND, "#fff") if m == "light" else ("#fff", BRAND)
    return (f'<rect width="64" height="64" rx="16" fill="{tile}"/>'
            f'<path d="M13 47H26V36H39V25H51" fill="none" stroke="{fg}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="51" cy="14" r="5.5" fill="{ACC}"/>')


def icon_b(m):
    tile, fg = (NAVY, "#fff") if m == "light" else ("#fff", NAVY)
    return (f'<rect width="64" height="64" rx="16" fill="{tile}"/>'
            f'<path d="M44 20C44 12 33 11 27 14C20 18 21 26 30 30C39 34 44 38 41 45C38 52 27 52 20 46" fill="none" stroke="{fg}" stroke-width="5.5" stroke-linecap="round"/>'
            f'<circle cx="44" cy="20" r="5" fill="{ACC}"/><circle cx="20" cy="46" r="5" fill="{ACC}"/>')


def icon_c(m):
    ring = BRAND if m == "light" else "#fff"
    return (f'<circle cx="32" cy="32" r="24" fill="none" stroke="{ring}" stroke-width="7" stroke-dasharray="118 33" stroke-linecap="round" transform="rotate(-40 32 32)"/>'
            f'<path d="M20 33L29 42L48 20" fill="none" stroke="{ACC}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')


def icon_d(m):
    if m == "light":
        c1, c2, c3, dash = "#9db8ff", "#5b86f0", BRAND, "#aab6d3"
    else:
        c1, c2, c3, dash = "#6b8fe8", "#a9c1ff", "#ffffff", "#6c7fae"
    return (f'<rect x="5" y="35" width="24" height="24" rx="7" fill="{c1}"/>'
            f'<rect x="35" y="35" width="24" height="24" rx="7" fill="{c2}"/>'
            f'<rect x="35" y="5" width="24" height="24" rx="7" fill="{c3}"/>'
            f'<rect x="6.5" y="6.5" width="21" height="21" rx="6" fill="none" stroke="{dash}" stroke-width="3" stroke-dasharray="5 4"/>'
            f'<circle cx="47" cy="17" r="4" fill="{ACC}"/>')


def icon_e(m):
    tile, bar = (NAVY, "#fff") if m == "light" else ("#fff", NAVY)
    return (f'<circle cx="32" cy="32" r="32" fill="{tile}"/>'
            f'<rect x="15" y="36" width="9" height="13" rx="3" fill="{bar}"/>'
            f'<rect x="27.5" y="27" width="9" height="22" rx="3" fill="{bar}"/>'
            f'<rect x="40" y="16" width="9" height="33" rx="3" fill="{ACC}"/>')


LOGOS = [
    ("A", "Bậc thang", icon_a,
     "Đường đi lên theo từng bậc, điểm cam ở đỉnh là đích. Đúng nhất với thang cấp độ C0-C9 của series. Gần với logo đang dùng trên site nên ít thay đổi nhất."),
    ("B", "Chữ S nối nút", icon_b,
     "Chữ S viết bằng một nét có hai nút ở đầu và cuối, gợi mạng lưới kết nối, hệ thống và quy trình. Nền xanh đậm, nghiêm túc, hợp tư vấn."),
    ("C", "Dấu duyệt", icon_c,
     "Vòng tròn mở có dấu tích cam bung ra ngoài: AI đề xuất, người duyệt. Nhấn vào nguyên tắc cốt lõi của series, đơn giản, dễ nhận ở cỡ nhỏ."),
    ("D", "Khối nhỏ", icon_d,
     "Các khối xếp dần lên, một ô còn trống nét đứt: đi từ khối nhỏ nhất, làm xong cấp nào thì lấp ô đó. Có nét khác biệt nhất, cảm giác hiện đại, thân thiện."),
    ("E", "Cột đo", icon_e,
     "Ba cột tăng dần trong hình tròn, cột cao nhất màu cam: đo được, cải thiện được. Gợi báo cáo và số liệu, dễ làm dấu tròn cho mạng xã hội."),
]


def svg(inner, vb="0 0 64 64", size=None, extra=""):
    wh = f' width="{size}" height="{size}"' if size else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{wh}{extra}>{inner}</svg>'


def lockup_html(fn, mode):
    txt, tech, sub = (NAVY, BRAND, "#56627d") if mode == "light" else ("#fff", "#8fb0ff", "#b9c6e6")
    return (f'<div class="lock {mode}">{svg(fn(mode), size=56)}'
            f'<div><div class="wm" style="color:{txt}">SIP<b style="color:{tech}">Tech</b></div>'
            f'<div class="tg" style="color:{sub}">Tư vấn giải pháp AI trong doanh nghiệp</div></div></div>')


cards = ""
for key, name, fn, desc in LOGOS:
    for mode in ("light", "dark"):
        (OUT / f"logo-{key}-{mode}.svg").write_text(svg(fn(mode)), encoding="utf-8")
    smalls = "".join(f'<span class="sm">{svg(fn("light"), size=s)}<small>{s}px</small></span>' for s in (16, 24, 32, 48))
    cards += f"""
<section class="card">
  <div class="top"><span class="key">{key}</span><h2>{name}</h2></div>
  <div class="big">{svg(fn('light'), size=132)}</div>
  <div class="rows">
    <div class="row l">{lockup_html(fn, 'light')}</div>
    <div class="row d">{lockup_html(fn, 'dark')}</div>
    <div class="row s">{smalls}</div>
  </div>
  <p>{desc}</p>
</section>"""

html = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SIPTech: 5 phương án logo</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f4f7fd;color:#14213d;font:16px/1.65 "Be Vietnam Pro",system-ui,sans-serif}}
header{{max-width:1180px;margin:0 auto;padding:40px 24px 8px}}
h1{{font-size:32px;font-weight:800;letter-spacing:-.02em;margin:0 0 6px;color:#0b1f4d}}
header p{{margin:0;color:#56627d}}
.grid{{max-width:1180px;margin:0 auto;padding:24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px}}
.card{{background:#fff;border:1px solid #e3e8f2;border-radius:20px;padding:24px;display:flex;flex-direction:column}}
.top{{display:flex;align-items:center;gap:12px}}
.key{{width:34px;height:34px;border-radius:10px;background:#e8efff;color:#1239a8;display:grid;place-items:center;font-weight:800}}
h2{{font-size:20px;margin:0;color:#0b1f4d}}
.big{{display:grid;place-items:center;background:#f4f7fd;border-radius:16px;padding:28px;margin:18px 0 12px}}
.row{{border-radius:14px;padding:14px 16px;margin-bottom:10px}}
.row.l{{border:1px solid #e3e8f2}}.row.d{{background:#0b1f4d}}
.row.s{{display:flex;align-items:flex-end;gap:18px;border:1px solid #e3e8f2}}
.sm{{display:flex;flex-direction:column;align-items:center;gap:6px}}.sm small{{color:#56627d;font-size:11px}}
.lock{{display:flex;align-items:center;gap:12px}}
.wm{{font-weight:800;font-size:30px;letter-spacing:-.03em;line-height:1.1}}
.tg{{font-size:11.5px;line-height:1.3;margin-top:3px}}
.card p{{margin:8px 0 0;color:#56627d;font-size:14.5px}}
</style></head><body>
<header><h1>SIPTech: 5 phương án logo</h1>
<p>Mỗi phương án gồm biểu tượng, bản ngang trên nền sáng và nền tối, và các cỡ nhỏ (16-48px) để xem có còn rõ không. Màu: xanh #1d4ed8, xanh đậm #0b1f4d, cam #ff7a3d.</p></header>
<div class="grid">{cards}</div>
</body></html>"""
(OUT / "index.html").write_text(html, encoding="utf-8")
print("OK", OUT)
