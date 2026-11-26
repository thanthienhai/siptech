"""Nhập chuỗi "Thực hành với coding agent" từ AI-Real/thuc-hanh-coding-agent vào content/.

Dùng:  python import_thuc_hanh.py <thư mục thuc-hanh-coding-agent>
Mỗi bài toán thành một thư mục content/th-<tên>/ gồm:
  meta.json, 00-README.md, cap-00..03-*.md (từ bai-1..4), anh/*.webp, du-lieu.zip, bo-cham.zip (nếu có)
KHÔNG đưa lên site: logs/ (log gốc của agent), runs/, bất cứ file nào ngoài du-lieu/, ket-qua/, anh/.
Chạy lại được: xóa và ghi đè content/th-*.
"""
import json, re, shutil, sys, zipfile
from pathlib import Path
from PIL import Image

SRC = Path(sys.argv[1])
DST = Path(__file__).parent / "content"
UPDATED = "2026-11-21"

META = {
    "00-bat-dau-voi-coding-agent": dict(name="Bắt đầu với coding agent", icon="zap", order=59, code="4 bài",
        tag="Cài và dùng Claude Code hoặc Antigravity khi chưa biết code",
        desc="Cài một coding agent, làm quen cửa sổ dòng lệnh, giao việc đầu tiên trong thư mục riêng và các quy tắc an toàn trước khi làm các bài toán thực hành.",
        out="Một agent chạy được trên máy bạn, một thư mục thử an toàn, một prompt giao việc đầu tiên",
        tags=["cài đặt", "claude code", "antigravity", "dòng lệnh", "người mới"]),
    "01-doi-soat-sao-ke-ngan-hang": dict(name="Đối soát sao kê ngân hàng", icon="bars", order=60,
        tag="Ghép từng dòng sao kê với sổ đơn hàng, tìm tiền thiếu, thừa, trùng",
        desc="Dùng coding agent viết script đối soát; số tiền do code tính, ca mơ hồ chuyển người quyết. Có dữ liệu giả, lần chạy thật và bảng chấm.",
        out="Bảng ghép dòng sao kê với đơn, danh sách ngoại lệ, tổng kiểm",
        tags=["kế toán", "sao kê", "đối soát", "ngân hàng", "excel"]),
    "02-lam-sach-danh-ba-khach-hang": dict(name="Làm sạch danh bạ khách hàng", icon="user", order=61,
        tag="Gộp khách trùng, chuẩn hóa số điện thoại, không xóa dữ liệu",
        desc="Dùng coding agent làm sạch 400 dòng danh bạ gom từ nhiều nguồn; mọi gộp ghi lại và hoàn tác được; ca nghi trùng chuyển người quyết.",
        out="Danh bạ sạch, nhật ký gộp, danh sách ca nghi trùng cần người quyết",
        tags=["crm", "danh bạ", "trùng", "số điện thoại", "dữ liệu cá nhân"]),
    "03-mo-ta-san-pham-hang-loat": dict(name="Mô tả sản phẩm hàng loạt", icon="file", order=62,
        tag="Viết mô tả cho sàn từ bảng thông số mà không bịa thông số",
        desc="Dùng coding agent viết mô tả 40 sản phẩm; kiểm bằng code mọi con số có trong bảng; sản phẩm thiếu thông số phải ghi CẦN BỔ SUNG.",
        out="File nhập hàng loạt (tiêu đề, mô tả, gạch đầu dòng, từ khóa) và báo cáo kiểm",
        tags=["shopee", "tiktok shop", "mô tả sản phẩm", "thương mại điện tử"]),
    "04-phan-tich-danh-gia-khach-hang": dict(name="Phân tích đánh giá của khách", icon="chat", order=63,
        tag="Từ hàng trăm review đời thường ra chủ đề, ca nguy cấp và việc nên sửa trước",
        desc="Dùng coding agent phân tích 250 đánh giá; số đếm do code, mọi trích dẫn kiểm nguyên văn, mỉa mai chuyển người đọc.",
        out="Chủ đề và sắc thái theo ý, ca nguy cấp, xu hướng theo tuần, 5 việc nên sửa có trích dẫn",
        tags=["đánh giá", "review", "cskh", "phân tích", "sắc thái"]),
    "05-bao-gia-tu-email-yeu-cau": dict(name="Lập báo giá từ email yêu cầu", icon="file", order=64,
        tag="Từ email khách lộn xộn và bảng giá ra báo giá, thư trả lời nháp và câu hỏi làm rõ",
        desc="Dùng coding agent lập báo giá cho 12 yêu cầu; tiền do code tính, chiết khấu vượt thẩm quyền chuyển người quyết, không tự hứa ngày giao.",
        out="File báo giá, email trả lời nháp, danh sách câu hỏi làm rõ",
        tags=["báo giá", "email", "chiết khấu", "bán hàng"]),
    "06-kiem-tra-bang-cham-cong": dict(name="Kiểm tra bảng chấm công", icon="shield", order=65,
        tag="Tìm bất thường trong dữ liệu chấm công trước khi tính lương",
        desc="Dùng coding agent kiểm bảng công 25 nhân viên trên dữ liệu đã ẩn danh; giờ do code tính, ngưỡng là tham số của công ty, quản lý xác nhận ngoại lệ.",
        out="Bảng công ngày và tháng, danh sách bất thường để quản lý xác nhận",
        tags=["chấm công", "nhân sự", "lương", "ẩn danh"]),
    "07-ton-kho-va-de-xuat-nhap-hang": dict(name="Tồn kho và đề xuất nhập hàng", icon="bars", order=66,
        tag="Phân loại ABC, tồn kho an toàn và số lượng nên nhập, đo trên tháng giữ lại",
        desc="Dùng coding agent tính từ xuất nhập tồn 12 tháng; công thức tất định, có mốc so sánh đơn giản và đo trên hai tháng giữ lại; người quyết số cuối.",
        out="Phân loại ABC, cảnh báo sắp hết hoặc tồn lâu, đề xuất nhập kèm tiền vốn",
        tags=["tồn kho", "nhập hàng", "abc", "dự báo"]),
    "08-gop-bao-cao-chi-nhanh": dict(name="Gộp báo cáo từ nhiều chi nhánh", icon="layers", order=67,
        tag="Gộp sáu file Excel mỗi nơi một kiểu thành một báo cáo chuẩn, có kiểm tổng",
        desc="Dùng coding agent gộp 6 file chi nhánh; tổng từng file phải khớp tổng hợp, không sửa file gốc, và cách chạy lại khi một chi nhánh đổi định dạng.",
        out="Bảng hợp nhất, báo cáo tháng, danh sách việc phải hỏi lại chi nhánh",
        tags=["excel", "báo cáo", "chi nhánh", "gộp dữ liệu"]),
}


def convert_images(src_dir, dst_dir):
    dst_dir.mkdir(parents=True, exist_ok=True)
    for f in sorted(src_dir.glob("*.png")):
        im = Image.open(f).convert("RGB")
        if im.width > 1700:
            im = im.resize((1700, round(im.height * 1700 / im.width)), Image.LANCZOS)
        im.save(dst_dir / (f.stem + ".webp"), "WEBP", quality=88, method=6)


def zip_dir(src_dir, out_zip, skip=()):
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src_dir.rglob("*")):
            if f.is_file() and not any(p in f.parts for p in skip) and f.suffix != ".pyc" and "__pycache__" not in f.parts:
                z.write(f, f.relative_to(src_dir.parent).as_posix())


DOWNLOAD_TAIL = "\nLog gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.\n"

for old in DST.glob("th-*"):
    shutil.rmtree(old)

for folder, m in META.items():
    sdir = SRC / folder
    if not sdir.exists():
        print("bỏ qua (chưa có thư mục nguồn):", folder)
        continue
    slug = "th-" + re.sub(r"^\d+-", "", folder)
    d = DST / slug
    d.mkdir(parents=True)
    has_data = (sdir / "du-lieu").is_dir()
    has_grader = (sdir / "ket-qua").is_dir()
    # đặt tên file mới: bai-N-x.md -> cap-0(N-1)-x.md
    lessons = sorted(sdir.glob("bai-*.md"))
    rename = {}
    for f in lessons:
        n = int(re.match(r"bai-(\d)", f.name).group(1))
        rename[f.name] = f"cap-{n-1:02d}-" + re.sub(r"^bai-\d-", "", f.name)
    for f in [sdir / "00-README.md"] + lessons:
        text = f.read_text(encoding="utf-8")
        for a, b in rename.items():
            text = text.replace(a, b)
        text = re.sub(r"(anh/[\w.\-]+)\.png", r"\1.webp", text)
        text = text.replace("../../an-toan-du-lieu-va-phap-ly-vn.md", "../an-toan-du-lieu-va-phap-ly-vn.md")
        if f.name == "00-README.md":
            if has_data or has_grader:
                dl = "\n\n## Tải về\n\n"
                if has_data:
                    dl += "- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.\n"
                if has_grader:
                    dl += ("- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. "
                           "Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.\n")
                text = text.rstrip() + dl + DOWNLOAD_TAIL
            (d / "00-README.md").write_text(text, encoding="utf-8")
        else:
            (d / rename[f.name]).write_text(text, encoding="utf-8")
    if (sdir / "anh").is_dir():
        convert_images(sdir / "anh", d / "anh")
    if has_data:
        zip_dir(sdir / "du-lieu", d / "du-lieu.zip")
    if has_grader:
        zip_dir(sdir / "ket-qua", d / "bo-cham.zip", skip=("runs",))
    meta = dict(name=m["name"], code=m.get("code", "4 bài"), icon=m["icon"], order=m["order"], status="draft", kind="thuc-hanh", updated=UPDATED,
                tag=m["tag"], desc=m["desc"], out=m["out"], tags=m["tags"], step=None, step_label="")
    (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n_img = len(list((d / "anh").glob("*.webp"))) if (d / "anh").exists() else 0
    print(slug, len(rename), "bài,", n_img, "ảnh")
