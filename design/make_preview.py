"""Tạo design/logo-kit/index.html (trang xem thử và hướng dẫn dùng) + README.md + file zip."""
import zipfile
from pathlib import Path

KIT = Path(__file__).parent / "logo-kit"


def size_kb(p):
    return f"{p.stat().st_size / 1024:.0f} KB"


def tile(src, label, bg="#fff", h=96, note=""):
    return (f'<figure class="t" style="background:{bg}"><img src="{src}" style="height:{h}px" alt="{label}">'
            f'<figcaption>{label}{(" · " + note) if note else ""}</figcaption></figure>')


def sec(title, sub, body):
    return f'<section><h2>{title}</h2><p class="sub">{sub}</p><div class="g">{body}</div></section>'


icons = "".join([
    tile("svg/icon-color.svg", "Màu (chính)", "#fff", 110),
    tile("svg/icon-reverse.svg", "Nền tối", "#0b1f4d", 110),
    tile("svg/icon-black.svg", "Một màu: đen", "#fff", 110),
    tile("svg/icon-white.svg", "Một màu: trắng", "#1d4ed8", 110),
])
avatars = "".join([
    tile("svg/avatar-circle.svg", "Tròn, nền xanh đậm", "#f4f7fd", 130, "Zalo, Facebook"),
    tile("svg/avatar-circle-blue.svg", "Tròn, nền xanh dương", "#f4f7fd", 130, "phương án phụ"),
    tile("svg/avatar-square.svg", "Vuông, tràn viền", "#f4f7fd", 130, "để nền tảng tự cắt"),
])
lock_h = "".join([
    tile("svg/lockup-horizontal-tagline-color.svg", "Ngang + giới thiệu (chính)", "#fff", 70),
    tile("svg/lockup-horizontal-color.svg", "Ngang", "#fff", 70),
    tile("svg/lockup-horizontal-tagline-reverse.svg", "Ngang + giới thiệu, nền tối", "#0b1f4d", 70),
    tile("svg/lockup-horizontal-reverse.svg", "Ngang, nền tối", "#0b1f4d", 70),
    tile("svg/lockup-horizontal-black.svg", "Một màu: đen", "#fff", 70),
    tile("svg/lockup-horizontal-white.svg", "Một màu: trắng", "#1d4ed8", 70),
])
lock_s = "".join([
    tile("svg/lockup-stacked-tagline-color.svg", "Dọc + giới thiệu", "#fff", 190),
    tile("svg/lockup-stacked-color.svg", "Dọc", "#fff", 160),
    tile("svg/lockup-stacked-tagline-reverse.svg", "Dọc + giới thiệu, nền tối", "#0b1f4d", 190),
    tile("svg/lockup-stacked-white.svg", "Một màu: trắng", "#1d4ed8", 160),
])
words = "".join([
    tile("svg/wordmark-color.svg", "Chỉ chữ", "#fff", 56),
    tile("svg/wordmark-reverse.svg", "Chỉ chữ, nền tối", "#0b1f4d", 56),
    tile("svg/wordmark-black.svg", "Một màu: đen", "#fff", 56),
])
soc = "".join(f'<figure class="w"><img src="social/{n}.png" alt="{n}"><figcaption>{n}</figcaption></figure>'
              for n in ("og-image-1200x630", "facebook-cover-1640x624", "linkedin-banner-1584x396"))

small = "".join(f'<span class="sm"><img src="png/icon-color-{s}.png" width="{s}" height="{s}" alt=""><small>{s}px</small></span>'
                for s in (16, 32, 48, 64))

rows = ""
for p in sorted((KIT / "png").glob("*.png")):
    rows += f'<tr><td><a href="png/{p.name}">png/{p.name}</a></td><td>{size_kb(p)}</td></tr>'
dl = f'<table><tr><th>Tệp PNG</th><th>Dung lượng</th></tr>{rows}</table>'

html = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bộ logo SIPTech</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap">
<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#f4f7fd;color:#14213d;font:16px/1.65 "Be Vietnam Pro",system-ui,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 24px}}
header{{padding:44px 0 8px}}
h1{{font-size:34px;font-weight:800;letter-spacing:-.02em;margin:0 0 6px;color:#0b1f4d}}
h2{{font-size:22px;font-weight:800;margin:0 0 4px;color:#0b1f4d}}
.sub{{margin:0 0 16px;color:#56627d}}
section{{margin:40px 0}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}}
.t{{margin:0;border:1px solid #dde3ef;border-radius:16px;padding:22px 16px 14px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;min-height:170px}}
.t img{{max-width:100%}}
figcaption{{font-size:12.5px;color:#7b86a1;text-align:center}}
.t[style*="0b1f4d"] figcaption,.t[style*="1d4ed8"] figcaption{{color:#b9c6e6}}
.w{{margin:0 0 14px}}.w img{{width:100%;border-radius:14px;border:1px solid #dde3ef;display:block}}.w figcaption{{margin-top:6px;text-align:left}}
.row{{display:flex;gap:28px;align-items:flex-end;background:#fff;border:1px solid #dde3ef;border-radius:16px;padding:22px}}
.sm{{display:flex;flex-direction:column;align-items:center;gap:8px}}.sm small{{color:#7b86a1;font-size:12px}}
.sw{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.sw div{{border-radius:14px;padding:16px;color:#fff;font-size:14px;min-height:96px;display:flex;flex-direction:column;justify-content:flex-end}}
.sw b{{font-size:15px}}
ul{{color:#14213d;padding-left:20px}}li{{margin-bottom:6px}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #dde3ef;border-radius:12px;font-size:14px}}
td,th{{text-align:left;padding:8px 14px;border-bottom:1px solid #eef1f7}}a{{color:#1d4ed8}}
.clr{{display:flex;gap:28px;flex-wrap:wrap;align-items:center;background:#fff;border:1px solid #dde3ef;border-radius:16px;padding:22px}}
.clr .box{{position:relative;padding:32px;border:1.5px dashed #ff7a3d;border-radius:6px}}
.clr .box img{{height:64px;display:block}}
.clr small{{color:#56627d;max-width:420px}}
</style></head><body><div class="wrap">
<header><h1>Bộ logo SIPTech</h1>
<p class="sub">Phương án B (chữ S nối nút). Chữ trong các file SVG đã chuyển thành đường nét nên không cần cài phông. Tải tệp ở thư mục <code>svg/</code> (in ấn, thiết kế) hoặc <code>png/</code> (đăng web, mạng xã hội).</p></header>

{sec("1. Biểu tượng", "Dùng khi không đủ chỗ cho chữ: favicon, avatar, con dấu, bìa slide.", icons)}
{sec("2. Ảnh đại diện", "Zalo, Facebook, LinkedIn tự cắt tròn, nên chữ S đã thu nhỏ để không bị mất nét.", avatars)}
{sec("3. Bản ngang", "Bản dùng nhiều nhất: đầu trang web, chữ ký email, tiêu đề tài liệu.", lock_h)}
{sec("4. Bản dọc", "Bìa tài liệu, bảng hiệu vuông, biểu ngữ dọc.", lock_s)}
{sec("5. Chỉ chữ", "Khi biểu tượng đã xuất hiện ngay bên cạnh.", words)}
<section><h2>6. Cỡ nhỏ</h2><p class="sub">Biểu tượng ở 16, 32, 48, 64px (PNG thật, đã thu nhỏ).</p><div class="row">{small}</div></section>
<section><h2>7. Ảnh cho mạng xã hội</h2><p class="sub">Ảnh chia sẻ link (1200×630), ảnh bìa Facebook, banner LinkedIn. Nội dung chữ sửa trong <code>make_kit.py</code>.</p>{soc}</section>

<section><h2>8. Màu sắc</h2><p class="sub">Màu chính và màu nhấn.</p><div class="sw">
<div style="background:#0b1f4d"><b>Xanh đậm</b>#0b1f4d · nền, chữ SIP</div>
<div style="background:#1d4ed8"><b>Xanh dương</b>#1d4ed8 · chữ Tech, nút</div>
<div style="background:#ff7a3d"><b>Cam</b>#ff7a3d · hai nút của chữ S</div>
<div style="background:#8fb0ff;color:#0b1f4d"><b>Xanh nhạt</b>#8fb0ff · chữ Tech trên nền tối</div>
</div></section>

<section><h2>9. Quy tắc dùng</h2><p class="sub">Vùng đệm và kích thước tối thiểu.</p>
<div class="clr"><div class="box"><img src="svg/lockup-horizontal-color.svg" alt=""></div>
<small>Chừa quanh logo một khoảng trống bằng nửa chiều cao biểu tượng (khung cam nét đứt là tham khảo).</small></div>
<ul>
<li>Cỡ nhỏ nhất: biểu tượng 16px; bản ngang không có dòng giới thiệu rộng 110px; có dòng giới thiệu rộng 220px (nhỏ hơn thì dùng bản không có giới thiệu).</li>
<li>Nền sáng dùng bản "Màu"; nền xanh đậm hoặc ảnh tối dùng bản "Nền tối"; in một màu dùng bản đen hoặc trắng.</li>
<li>Không đổi màu hai nút cam, không kéo giãn, không xoay, không thêm bóng đổ hay viền.</li>
<li>Chưa tra cứu nhãn hiệu: cần kiểm tra trùng lặp trước khi đăng ký hoặc in ấn hàng loạt.</li>
</ul></section>

<section><h2>10. Danh sách tệp PNG</h2><p class="sub">Tệp SVG nằm ở <code>svg/</code>; <code>favicon.ico</code> và <code>favicon.svg</code> ở thư mục gốc của bộ logo.</p>{dl}</section>
</div></body></html>"""
(KIT / "index.html").write_text(html, encoding="utf-8")

zp = KIT.parent / "siptech-logo-kit.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for f in KIT.rglob("*"):
        if f.is_file():
            z.write(f, f.relative_to(KIT.parent))
print("ok", zp, zp.stat().st_size // 1024, "KB")
