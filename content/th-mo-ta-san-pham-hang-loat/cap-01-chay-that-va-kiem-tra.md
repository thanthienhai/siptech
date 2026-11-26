# Bài 2. Chạy thật, chấm bằng code, xem agent sai ở đâu

!!! info "Bài này"
    - **Bạn làm gì:** mở kết quả của hai agent, chạy bộ chấm so với đáp án, đọc các ca agent làm sai.
    - **Mất bao lâu:** khoảng 30 phút. Chạy bộ chấm mất vài giây mỗi lần.
    - **Cần có:** bộ bài đã giải nén (thư mục `du-lieu/` và `ket-qua/` cạnh nhau), Python 3. Kết quả mẫu của chúng tôi đã có sẵn trong `ket-qua/`. Tải [bo-cham.zip](bo-cham.zip) và giải nén ở **ngoài** thư mục chạy của agent (đừng để đáp án cạnh agent). Cách sắp xếp thư mục: xem mục "Sắp xếp thư mục" ở [trang tổng quan nhóm bài](00-README.md).
    - **Kết quả:** một bảng đúng/sai theo từng chỉ tiêu, và hiểu vì sao "agent tự báo sạch" không đủ.

Kết quả đo của chúng tôi, ngày 2026-11-20, cùng prompt (bài 1), cùng dữ liệu, 40 sản phẩm, mỗi agent chạy 2 lần (**n=2**, chỉ là quan sát, chưa đo được độ ổn định):

| Lần chạy | Thời gian | SKU sạch hoàn toàn (/40) | SKU thiếu thông số xử lý đúng (/9) | Ghi chú |
|---|---|---|---|---|
| Claude Code lần 1 | 241 giây, 12 lượt | 40 | 9 | không lỗi trong phạm vi thước đo |
| Claude Code lần 2 | 298 giây, 15 lượt | 40 | 9 | không lỗi trong phạm vi thước đo |
| Antigravity lần 1 | khoảng 11 đến 14 phút, **mất log** | 39 | 9 | 1 SKU có cụm "sản phẩm lành tính" không có trong bảng |
| Antigravity lần 2 | 756 giây | 0 | 9 | cả 40 SKU có "chính hãng" không có trong bảng |

> Dữ liệu giả để học. Chúng tôi **không** kết luận agent nào tốt hơn từ 2 lần chạy mỗi bên.

## Các bước làm

### Bước 1. Mở kết quả của agent

Trong `ket-qua/` mỗi lần chạy có một thư mục: `claude-v1-lan1`, `claude-v1-lan2`, `agy-v1-lan1-mat-log`, `agy-v1-lan2`. Mỗi thư mục có đầu ra thật của agent: `nhap_hang_loat.csv`, `nhap_hang_loat.xlsx`, `kiem.py` (script kiểm do chính agent viết), `bao_cao_kiem.md`. Chúng tôi giữ cả bản có lỗi.

Mở `claude-v1-lan1/bao_cao_kiem.md` và `agy-v1-lan2/bao_cao_kiem.md`. Cả hai tự kết luận "sạch, 0 lỗi".

!!! see "Bạn sẽ thấy"
    Hai báo cáo nghe rất tự tin và giống nhau. Bước sau sẽ cho thấy một trong hai có lỗi ở 40 sản phẩm.

### Bước 2. Chạy bộ chấm

`cham.py` đọc file CSV của agent, so với `dap-an.json` và bảng thông số, rồi chấm từng sản phẩm. Trong thư mục `ket-qua`, PowerShell:

```lenh
cd ket-qua
python -X utf8 cham.py claude-v1-lan1\nhap_hang_loat.csv claude-v1-lan1
python -X utf8 cham.py agy-v1-lan2\nhap_hang_loat.csv agy-v1-lan2
```

Lệnh chạy `cham.py` cho từng file. `-X utf8` để Windows đọc tiếng Việt đúng. Lệnh in số liệu và ghi thêm một mục vào `bao-cao-cham.json`. macOS hoặc Linux: đổi `\` thành `/` và `python -X utf8` thành `python3 -X utf8`.

Đầu ra mẫu của lệnh thứ hai (rút gọn, bỏ các chỉ tiêu bằng 0 không đáng xem):

```ketqua
{
 "dung_5_gach": 40,
 "tu_cam": 0,
 "so_bia": 0,
 "lexicon_bia": 40,
 "ro_ghi_chu": 0,
 "cong_bo_sai": 0,
 …
 "miss_sku_total": 9,
 "miss_fields_exact": 9,
 "false_alarm": 0,
 "sku_sach_hoan_toan": 0
}
```

`lexicon_bia` là số SKU có "cụm ngoài bảng". Ở lần chạy của Claude, các dòng cùng tên là 0 và `sku_sach_hoan_toan` là 40.

!!! stuck "Gặp lỗi?"
    - **`FileNotFoundError` về `dap-an.json`:** bạn đang đứng sai thư mục. Phải ở trong `ket-qua`, nơi có `cham.py` và `dap-an.json`.
    - **`UnicodeDecodeError` hoặc chữ vỡ:** thiếu `-X utf8`.
    - **Kết quả khác bảng dưới đây:** bạn đã sửa file của agent hoặc chạy trên đầu ra khác. Chạy lại trên bản gốc.

### Bước 3. Đọc bảng kết quả

`cham.py` làm 10 việc cho từng sản phẩm: đủ 5 gạch, độ dài, từ cấm (cả có dấu và không dấu), con số ngoài bảng, cụm ngoài bảng, rò ghi chú, "đã công bố" sai, 9 sản phẩm thiếu có gắn `CẦN BỔ SUNG` đúng trường, báo động giả ở 31 sản phẩm đủ thông tin, giọng thương hiệu. Kết quả bốn lần chạy:

| Chỉ tiêu (40 sản phẩm) | Claude 1 | Claude 2 | Antigravity 1 (mất log) | Antigravity 2 |
|---|---|---|---|---|
| Đủ 5 gạch | 40 | 40 | 40 | 40 |
| Vi phạm độ dài, từ cấm, số ngoài bảng | 0 | 0 | 0 | 0 |
| Cụm ngoài bảng | 0 | 0 | 1 | **40** |
| Rò ghi chú, "đã công bố" sai, giọng sai | 0 | 0 | 0 | 0 |
| 9 SKU thiếu: gắn cờ và trường thiếu đúng hệt | 9 | 9 | 9 | 9 |
| 31 SKU đủ: báo động giả | 0 | 0 | 0 | 0 |
| **SKU sạch hoàn toàn** | **40** | **40** | **39** | **0** |

![Bảng chấm 4 lần chạy](anh/07-bang-cham.webp)

*Bảng dựng từ `ket-qua/bao-cao-cham.json`. Dữ liệu giả để học.*

Tất cả nằm trong giới hạn độ dài giả định: tiêu đề 34 đến 85 ký tự, mô tả 361 đến 761, gạch dài nhất 103.

### Bước 4. Đọc các ca agent sai

Đừng chỉ nhìn tổng. Hai ca đáng xem:

| Agent làm gì | Đúng ra | Vì sao đáng chú ý |
|---|---|---|
| Antigravity lần 2 viết "Sản phẩm được phân phối chính hãng tại Vườn Nhỏ" vào mô tả của **cả 40** sản phẩm, và từ khóa "chính hãng + nước" ở 37 sản phẩm | Bảng không có thông tin nào nói hàng chính hãng, nên không được viết | Bịa **nhẹ, lịch sự, nghe vô hại**: không có số liệu, không có từ cấm nên dễ lọt. `kiem.py` của chính nó báo "sạch, tuân thủ 100%" |
| Antigravity lần 1 thêm từ khóa "sản phẩm lành tính" ở **VN-007** (dòng gần như trống) | Bảng không nói gì về độ lành | Chỉ 1 trong 40 dòng, nhưng trúng đúng chỗ thông tin trống nhất, nơi áp lực "phải có gì đó để viết" lớn nhất |

![Cụm ngoài bảng](anh/06-loi-cum-ngoai-bang.webp)

*Trích từ `ket-qua/agy-v1-lan2/nhap_hang_loat.csv`, `agy-v1-lan1-mat-log` và `claude-v1-lan2`. Dữ liệu giả để học.*

Muốn biết chính xác SKU nào lỗi, chạy máy kiểm hằng ngày (giới thiệu ở bài 3) trong thư mục `du-lieu`:

```lenh
cd ..\du-lieu
python -X utf8 kiem_hang_ngay.py ..\ket-qua\agy-v1-lan1-mat-log\nhap_hang_loat.csv
```

Đầu ra mẫu:

```ketqua
LỖI CỨNG VN-007 {'cum_ngoai_bang': ['lành tính']}

40 SKU: 39 sạch, 1 có lỗi cứng; thiếu thông số 9 (gắn cờ đúng 9), báo động giả 0.
```

!!! see "Bạn sẽ thấy"
    Chỉ một dòng lỗi, đúng SKU VN-007, đúng cụm "lành tính". Chạy tương tự với `agy-v1-lan2` sẽ ra 40 dòng "chính hãng".

### Bước 5. Xem điều cả bốn lần chạy làm đúng, và điều chưa ổn

Làm đúng ở cả bốn lần (theo thước đo của chúng tôi):

- Không dùng từ cấm nào, không chép "bán chạy", "số 1", "tốt nhất", "chữa khỏi" từ ghi chú.
- Không có con số nào ngoài bảng. Ở **VN-012** cả bốn lần dùng **10%** theo bảng, không dùng 15% của ghi chú.
- 4 sản phẩm "đang chờ duyệt" không bị nói là đã công bố; 10 sản phẩm có số phiếu `DEMO-xxxx` được ghi đúng số.
- 9 sản phẩm thiếu thông số được gắn `CAN_BO_SUNG`, `truong_can_bo_sung` đúng hệt (17 trường thiếu, 17 đúng).

Chưa ổn, và **không đo bằng code được**:

- **VN-012 (10% hay 15%):** cả bốn lần đều ghi mâu thuẫn vào báo cáo kiểm nhưng vẫn xếp `SAN_SANG`, không lần nào đặt `CẦN NGƯỜI QUYẾT` trong ô mô tả dù prompt có nhắc. Shop thật nên giữ VN-012 lại tới khi có phiếu kiểm nghiệm **[Đề xuất]**. Bài 4 có bài tập thử xem agent xử lý ra sao khi mâu thuẫn nhiều hơn.
- **Văn viết khô.** Đầu ra của cả hai agent đọc như bảng thông số chuyển thành câu, chưa phải mô tả bán hàng. Claude viết một đoạn dày đặc, mọi sản phẩm cùng khuôn "Dung tích: ... Thành phần nổi bật: ...". Antigravity có xuống dòng nên dễ đọc hơn nhưng cả 40 mô tả cùng mở đầu "Chào bạn, Vườn Nhỏ xin gửi đến bạn thông tin chi tiết về sản phẩm ...".
- **Chép tên cột kỹ thuật vào mô tả.** Cả hai chép nguyên `dung_tich`, `thanh_phan_noi_bat` vào chỗ `CẦN BỔ SUNG`. Với người nhập liệu đó là chỉ dẫn hay; nếu quên điền rồi đăng, khách sẽ thấy chữ này trên trang. Cách chặn ở bài 3.

![Đầu ra thật của Claude Code](anh/05-ket-qua-dau-ra-claude.webp)

*Trích từ `ket-qua/claude-v1-lan1/nhap_hang_loat.csv`. Dữ liệu giả để học. Ô vàng là chỗ `CẦN BỔ SUNG`.*

## Đào sâu: chi tiết từng lần chạy và chuyện mất log

**Chi phí và thời gian [Đo được].** Claude Code lần 1: 241 giây, 12 lượt, khoảng 0,70 USD (do Claude Code tự báo). Lần 2: 298 giây, 15 lượt, khoảng 0,86 USD. Antigravity lần 2: 756 giây, 166.211 token vào, 77.971 token ra (do agy báo). Antigravity không báo chi phí. Log của hai agent không ghi tên mô hình nên bài không nêu. Phiên bản: Claude Code 2.1.329, Antigravity `agy` 1.5.13.

**Chuyện đã xảy ra với Antigravity lần 1.** Chúng tôi chạy hai agent song song, đặt timeout 900 giây. Claude xong sau 4 phút. Với Antigravity, các file đầu ra xuất hiện (`nhap_hang_loat.csv` lúc 22:53, `bao_cao_kiem.md` lúc 22:56) nhưng **tiến trình bọc ngoài biến mất mà không ghi `*.raw.jsonl` hay `*.json`**, và tệp thông báo rỗng. Chúng tôi không biết chắc nguyên nhân (nghi chạm 900 giây hoặc tiến trình nền bị dừng); chưa kiểm chứng. Hệ quả: lần 1 còn **đầu ra** để chấm nhưng **không có log**. Chúng tôi chạy lại lần 2 với timeout 1500 giây và giữ cả hai. Nếu bạn tự chạy `agy` theo cách này, hãy đặt timeout rộng và lưu log từ đầu.

**Dao động giữa các lần chạy.** Antigravity lần 1 có 1 sản phẩm lỗi, lần 2 có 40, cùng prompt, cùng dữ liệu. Vì vậy mỗi lần chạy đều cần thước kiểm.

**Agent làm gì khi chạy.** Claude Code lần 1 đọc quy định, đọc bảng, sinh 40 dòng bằng một script, rồi viết `kiem.py`. Chạy xong thấy sạch ngay, nó **không tin** và tự **tiêm lỗi** vào bản sao trong bộ nhớ (từ cấm "số 1", số 15% sai, "đã công bố" khi chỉ đang chờ duyệt, "bà bầu", xuất xứ sai...) để xem `kiem.py` có bắt không. Nó bắt được cả 12. Lần 2 tiêm 21 lỗi. Đó là cách làm đúng: kiểm cái thước trước khi tin cái thước. Antigravity lần 2 viết nhiều script kiểm nhỏ, rồi bộ sinh, rồi `kiem.py`, rồi xóa script tạm; đây chỉ là quan sát về cách làm, không phải đánh giá.

![Claude Code đang làm](anh/02-claude-dang-lam.webp)

*Dựng lại từ log thật của lần chạy `claude-v1-lan1`, không phải ảnh chụp trực tiếp cửa sổ terminal.*

![Antigravity đang làm](anh/03-agy-dang-lam.webp)

*Dựng lại từ log thật của lần chạy `agy-v1-lan2`. Chỉ trích 13 bước đầu trong 43 khối.*

![Báo cáo cuối của Claude Code](anh/04-claude-ket-qua-cuoi.webp)

*Dựng lại từ log thật của lần chạy `claude-v1-lan1`.*

![Báo cáo cuối của Antigravity](anh/04b-agy-ket-qua-cuoi.webp)

*Dựng lại từ log thật của lần chạy `agy-v1-lan2`.*

## Đào sâu: thử chính cái thước, và lỗi trong thước của chúng tôi

**Thử thước bằng cách tiêm lỗi.** Một cái thước chưa thử thì chưa đáng tin. `cham_kiem_thu.py` lấy file sạch của Claude lần 1, tiêm 16 lỗi biết trước (từ cấm có dấu và không dấu, đổi 150 ml thành 250 ml, số 15% từ ghi chú, FDA, "lành tính", "chính hãng", "đã công bố" ở sản phẩm đang chờ duyệt, tự điền dung tích cho sản phẩm thiếu, trạng thái sai, tiêu đề quá ngắn, mô tả quá dài, emoji, "quý khách", báo động giả, chép "bán chạy"). **[Đo được]** `cham.py` bắt **16/16**. Chạy lại: `python -X utf8 cham_kiem_thu.py` trong `ket-qua`.

**Lỗi trong chính cái thước của chúng tôi.** Lần chấm đầu, `cham.py` báo "cụm ngoài bảng" ở 38 sản phẩm của Antigravity lần 1. Xem ra: danh sách có chữ "mỹ" (để bắt "xuất xứ Mỹ") nên bắt nhầm "**mỹ** phẩm", cụm bình thường của shop mỹ phẩm. Chúng tôi đổi thành "hoa kỳ", "nước mỹ", chạy lại cho **cả bốn** lần chạy. Bài học: báo 38 lỗi chưa chắc là agent sai; xem vài mẫu trước khi tin.

**Thước vẫn chỉ bắt cái nó biết tìm.** Danh sách "cụm ngoài bảng" (hơn 100 cụm dễ bịa) là danh sách tay do chúng tôi viết. Nếu chúng tôi quên một cụm thì cụm đó lọt. Ở bài 4, một agent đọc độc lập đã chỉ ra thêm một cụm mà `cham.py` không bắt (xem bài 4, prompt 3).

## Lỗi thường gặp khi kiểm tra

| Triệu chứng | Cách xử lý |
|---|---|
| Tin lời agent "đã sạch 100%" | Chạy thước độc lập của bạn |
| Thước báo hàng chục lỗi cùng một cụm | Xem vài mẫu: có thể thước sai (như cụm "mỹ" ở trên) |
| Chấm chung ghi chú và bảng, số từ ghi chú lọt | Chấm số theo ô thông số, bỏ cột ghi chú |
| Đọc 40 dòng bằng mắt, bỏ qua "chính hãng" lặp 40 lần | Để code quét, mắt chỉ xem mẫu |
| Chỉ chạy một lần, kết quả may rủi | Chạy ít nhất hai lần, ghi rõ n |

## Checklist cuối bài 2

- [ ] Chạy ít nhất hai lần, lưu log gốc.
- [ ] Chạy `cham.py` cho từng lần và đọc từng sản phẩm có lỗi, không chỉ nhìn tổng.
- [ ] Thử thước bằng cách tiêm lỗi (như `cham_kiem_thu.py`).
- [ ] Mở ít nhất 5 dòng đầu ra, trong đó có dòng thiếu thông số và dòng mâu thuẫn (VN-012).
- [ ] Giữ cả bản có lỗi.

## Việc cần người làm

- Xem VN-012 (10% hay 15%) và quyết đăng hay giữ.
- Điền thông số cho 9 sản phẩm thiếu rồi chạy lại.
- Bổ sung vào danh sách "cụm ngoài bảng" những cụm bạn thấy ở các lần chạy sau.
- Hỏi pháp chế về các cụm kiểu "chính hãng", "lành tính", "an toàn" trước khi cho phép dùng.

## Giới hạn

- **n=2** mỗi agent, một prompt, một bộ dữ liệu: chưa đo được độ ổn định, chưa nên suy ra agent nào tốt hơn. Cùng Antigravity mà 1 sản phẩm lỗi so với 40 sản phẩm lỗi cho thấy kết quả dao động.
- Antigravity lần 1 không có log gốc; kết quả chấm dựa vào file đầu ra còn lại trong thư mục.
- `cham.py` không đọc hiểu nghĩa câu: tên riêng lạ và cụm bịa chưa có trong danh sách của chúng tôi có thể lọt.
- Chưa đo chất lượng bán hàng, SEO, hay việc sàn có chấp nhận nội dung không.
- Bước tiếp theo: dùng hằng ngày với người duyệt ở **bài 3** ([cap-02-dua-vao-dung-hang-ngay.md](cap-02-dua-vao-dung-hang-ngay.md)).
