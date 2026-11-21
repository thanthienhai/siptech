# Bài toán 05: Lập báo giá từ email và tin nhắn yêu cầu của khách

> **Dữ liệu giả để học.** Công ty "An Phát Demo", khách hàng, người, địa chỉ, số điện thoại (dãy 0900 000 xxx), email (@example.com) đều bịa. Bảng giá, chính sách, điều kiện giao hàng là do chúng tôi viết để làm bài, không phải của doanh nghiệp thật. Toàn bộ sinh bằng `du-lieu/sinh_du_lieu.py` (hạt giống cố định 20261120, chạy lại ra y hệt).

## Vì sao chủ doanh nghiệp nhỏ gặp bài này

Một công ty nhỏ bán thiết bị văn phòng, mực in, giấy, văn phòng phẩm nhận yêu cầu báo giá qua email, Zalo, điện thoại mỗi ngày. Người làm báo giá thường là nhân viên kinh doanh kiêm kế toán kiêm kho. Việc mất thời gian không nằm ở phép tính mà ở những thứ lộn xộn quanh nó:

- Khách viết "2 thùng giấy A4, 5 tá bút bi, 1 thùng mực": thùng giấy là bao nhiêu ram? thùng mực là bao nhiêu hộp?
- Khách ghi mã hàng sai một ký tự, hỏi cả hàng công ty không bán.
- Bảng giá có nhiều bậc theo số lượng, mỗi mã một mốc khác nhau; chiết khấu tính theo giá trị đơn nhưng chỉ cho một nhóm hàng; nhân viên chỉ được giảm đến một mức, vượt mức là phải hỏi sếp.
- Khách đòi "giao trước 10 giờ sáng thứ Sáu", đòi giữ giá cũ, đòi nợ 30 ngày: nhân viên không được hứa.

Bài này giao việc đó cho một coding agent (Claude Code, Antigravity `agy`): đọc 12 yêu cầu lộn xộn, lập 12 báo giá nháp theo mẫu của công ty, viết 12 email trả lời nháp, liệt kê câu hỏi cần hỏi lại khách, và **dừng ở chỗ phải có người quyết**. Phép tính tiền do code làm; người thật duyệt trước khi gửi.

## Dữ liệu mẫu (thư mục `du-lieu/`)

| File | Nội dung |
|---|---|
| `bang-gia.xlsx` | 29 mã hàng, 4 nhóm (Giấy & in ấn, Mực in, Thiết bị, VPP & vật liệu), 3 bậc giá theo số lượng (mốc bậc khác nhau theo từng mã), sheet `QuyDoi` có 13 dòng quy đổi đơn vị (thùng, hộp, tá, lốc, bó) |
| `chinh-sach-chiet-khau.docx` | Chính sách viết bằng chữ: chiết khấu theo giá trị đơn (2% từ 10 triệu, 4% từ 30 triệu, không tính cho nhóm Thiết bị), nhân viên được cấp thêm tối đa 2% với tổng không quá 5%, quà tặng/công nợ/giữ giá cũ do cấp trên quyết, hàng không có trong bảng giá, làm tròn |
| `dieu-kien-giao-hang.txt` | Danh sách quận nội thành, phí giao 40.000 đồng (miễn phí từ 3 triệu sau chiết khấu), ngoại tỉnh theo thỏa thuận, **không hứa ngày giờ giao**, thanh toán, hóa đơn |
| `mau-bao-gia.xlsx` | Mẫu báo giá của công ty (tiêu đề, khối khách hàng, bảng dòng hàng, các dòng tổng, điều kiện, chữ ký) và sheet `Tham số` (mức VAT là **tham số minh họa 10%, kiểm với kế toán**, ngày báo giá, hiệu lực) |
| `yeu-cau/R01.txt ... R12.txt` | 12 email/tin nhắn Zalo lộn xộn |

12 yêu cầu cài bẫy (đáp án nằm ở `ket-qua/dap-an.json`, **không** đưa cho agent):

| Mã | Bẫy chính |
|---|---|
| R01 | Email đủ thông tin; 3 hộp bút = 60 cây; xin giảm 2% (trong thẩm quyền); đơn dưới 3 triệu nên có phí giao 40.000 |
| R02 | Zalo cụt, không dấu: thiếu số lượng giấy, thiếu địa chỉ, "chiều anh cần" (đòi giao gấp) |
| R03 | Hai mã sai (`MUC-HP-12C`, `BUT-GEL-05-XANH`) và một dòng viết thường vẫn nhận ra được |
| R04 | Hỏi máy photocopy và máy chiếu 4K: không có trong bảng giá |
| R05 | Xin giảm 25% tổng đơn mới chốt |
| R06 | Đơn vị lẫn lộn: thùng, tá, lốc, hộp; "1 thùng mực" không có quy đổi |
| R07 | Số lượng sát mốc bậc giá (49, 50, 100); đòi giữ giá cũ 3.500 đồng |
| R08 | Giao Bắc Ninh (ngoại tỉnh) và đòi xác nhận giao trước 10 giờ sáng thứ Sáu; 72 cuộn đúng mốc bậc 3 |
| R09 | "Báo giá như đợt trước": không có danh sách hàng |
| R10 | Dòng trùng ("thêm 2 hộp nữa", "thêm 1 thùng nữa"), đơn trên 10 triệu: chiết khấu 2% theo đơn cộng 2% xin thêm |
| R11 | Đơn trên 50 triệu, xin giảm 10% và "mua 10 tặng 1", mực Canon đang tạm hết hàng |
| R12 | Không dấu, viết tắt, xin công nợ 30 ngày, xuất hóa đơn công ty |

**Đáp án** (`ket-qua/dap-an.json`) do chính `sinh_du_lieu.py` tính bằng code theo đúng chính sách: dòng hàng, bậc giá, chiết khấu, phí giao, VAT theo tham số, tổng cộng, trạng thái mong đợi và các nhãn "câu hỏi làm rõ / cần người quyết".

## Mục lục 3 bài

1. [Bài 1: Chuẩn bị dữ liệu và giao việc cho agent](cap-00-chuan-bi-du-lieu-va-giao-viec.md): mẫu báo giá, bảng giá, chính sách; prompt khung 6 phần; cách cho agent làm việc trong thư mục riêng.
2. [Bài 2: Chạy thật và chấm bằng đáp án](cap-01-chay-that-va-cham-bang-dap-an.md): hai agent, 5 lần chạy có kết quả, 1 lần bị loại vì đọc đáp án; chấm bằng `cham.py`.
3. [Bài 3: Đưa vào dùng hằng ngày](cap-02-dua-vao-dung-hang-ngay.md): quy trình hằng ngày, người duyệt, tự kiểm, giới hạn, mở rộng.

## Kết quả đo tóm tắt (ngày 2026-11-20)

**[Đo được]** 12 yêu cầu, 35 dòng hàng trong đáp án, mỗi lần chạy 36 file (12 báo giá + 12 email + 12 danh sách câu hỏi). n = 5 lần chạy hợp lệ (claude 3, agy 2), chưa đo được độ ổn định.

| Lần chạy | Log gốc | Dòng hàng đúng | Dòng bịa có giá | Yêu cầu đúng cả 6 dòng tổng | Trạng thái khớp đáp án |
|---|---|---|---|---|---|
| claude-1 | có | 35/35 | 0 | 12/12 | 10/12 |
| claude-2 (thư mục cô lập) | có | 35/35 | 0 | 12/12 | 12/12 |
| claude-0 | **mất** | 35/35 | 0 | 12/12 | 11/12 |
| agy-2 (thư mục cô lập) | có | 35/35 | 0 | 12/12 | 10/12 |
| agy-0 | **mất** | 35/35 | 0 | 8/12 | 8/12 |
| agy-1 | có | **loại**: agent đã mở file đáp án và file chấm ở ngoài thư mục làm việc | | | |

Điều rút ra (chỉ mô tả quan sát, không xếp hạng agent từ 1-2 lần chạy):

- Phép tính tiền đúng gần như tuyệt đối khi bắt buộc agent viết script tính (`tinh_bao_gia.py`): 35/35 dòng hàng trong mọi lần chạy hợp lệ. Lỗi tiền duy nhất đáng kể là agy-0 ở R10: bỏ phần chiết khấu thêm 2% do hiểu sai chính sách.
- Chỗ agent hay khác đáp án là **ranh giới "thiếu thông tin" và "cần người quyết"** (judgement), không phải số học. Ở ca R02 chúng tôi phải sửa đáp án vì hai lần chạy chạy trong thư mục cô lập (claude-2, agy-2) đều ghi nhận "chiều anh cần" là đòi giao gấp (claude-1 và claude-0 chỉ ghi THIEU_THONG_TIN) (chính sách giao hàng bắt buộc chuyển người quyết), còn đáp án gốc của chúng tôi bỏ sót (xem bài 2).
- Ba trong năm lần chạy hợp lệ (claude-1, agy-2, agy-0) viết trong email nháp những câu kiểu "đã chuyển lên trưởng phòng xem xét" trong khi việc đó chưa ai làm: người duyệt phải sửa hoặc làm cho câu đó đúng trước khi gửi.
- Một lần chạy (agy-1) đã đọc file đáp án và chạy chương trình chấm trên kết quả của agent khác dù prompt dặn "chỉ đọc và ghi trong thư mục hiện tại". Đây là bài học về cô lập môi trường làm việc, kể trong bài 2.

## Thư mục

```
00-README.md
bai-1-...md  bai-2-...md  bai-3-...md
du-lieu/        dữ liệu cho người học tải về + sinh_du_lieu.py
ket-qua/        dap-an.json, cham.py, dung_anh.py, kiem-tra-bao-gia.py (+ kiem-tra-bao-cao.txt), bao-cao-cham.json, prompt-giao-viec.txt,
                claude-1, claude-2, claude-0, agy-2, agy-0 (mỗi thư mục có dau-ra/ và tinh_bao_gia.py),
                agy-1-NHIEM-DAP-AN (giữ để minh bạch, không tính điểm),
                dap-an-v1-chua-sua.json và bao-cao-cham-v1-dap-an-chua-sua.json (bản chấm trước khi sửa đáp án)
logs/           *.raw.jsonl (log gốc) và *.json (transcript chuẩn hóa) của claude-1, claude-2, agy-1, agy-2
anh/            12 ảnh dùng trong bài (dựng lại bằng ket-qua/dung_anh.py)
```

Hai lần chạy đầu (claude-0, agy-0) chạy bằng `nohup` trong một phiên làm việc, tiến trình bị dừng trước khi ghi log (chúng tôi không biết nguyên nhân chính xác). Các file `dau-ra/` của chúng đã được tạo xong nên vẫn được giữ và chấm, nhưng **không có log nên không dựng ảnh từ chúng và không biết chúng có mở file đáp án hay không** (file đáp án lúc đó đã nằm trong máy, ở một thư mục khác). Các lần chạy sau (claude-1, agy-1, claude-2, agy-2) chạy bằng PowerShell `Start-Process` và log đầy đủ.

Ảnh terminal dựng lại từ log đã che đường dẫn máy và tên tổ chức.

## Tài liệu tham chiếu công khai về bố cục báo giá (không chép nội dung)

Chúng tôi tìm mẫu báo giá công khai để tham chiếu **bố cục**, không sao chép file hay nội dung có bản quyền. Chúng tôi chỉ đọc mô tả trang, không tải file mẫu về dùng.

- **[Nguồn]** MISA AMIS, "Cách tạo báo giá bằng Excel chi tiết": https://amis.misa.vn/74600/cach-lam-bang-bao-gia-tren-excel/ . Bố cục tham chiếu: khối công ty, tiêu đề BẢNG BÁO GIÁ, lời chào khách, bảng STT / tên / mô tả / ĐVT / số lượng / đơn giá / thành tiền, hiệu lực báo giá, chiết khấu ghi rõ % hay số tiền, điều kiện giao hàng - thanh toán - bảo hành, người liên hệ, chữ ký. Trang có dòng "Copyright 1994-2026 MISA JSC. All rights reserved" nên chúng tôi không chép chữ.
- **[Nguồn]** Spreadsheet123, Price Quote Template: https://www.spreadsheet123.com/ExcelTemplates/quote-template . Bố cục tham chiếu: sheet Settings chứa VAT/tiền tệ tách khỏi sheet báo giá, ô Quote Date / Valid Until / Quote #, tổng phụ - chiết khấu - thuế - tổng. Trang ghi giấy phép "company use", không được phân phối lại, nên chúng tôi không dùng file.
- **[Nguồn]** Vertex42 (https://www.vertex42.com/ExcelTemplates/quote-template.html, "private use, không phân phối lại") và IONOS (cột description / quantity / unit / price per unit / VAT % / VAT / total): chỉ để đối chiếu tên cột.
- Mẫu `mau-bao-gia.xlsx` là do chúng tôi tự dựng theo các bố cục trên, bằng tiếng Việt, kèm sheet "Tham số" để mức VAT là tham số chứ không gõ cứng.

## Việc cần người làm

- Người duyệt (chủ doanh nghiệp, kế toán, trưởng phòng kinh doanh) đọc từng báo giá nháp trước khi gửi.
- Kế toán xác nhận mức VAT đưa vào sheet "Tham số" và cách tính thuế cho dòng phí giao hàng.
- Người có thẩm quyền quyết chiết khấu vượt mức, quà tặng, công nợ, giữ giá cũ, phí giao ngoại tỉnh, hàng không có trong bảng giá.

## Giới hạn

- Dữ liệu giả; 12 yêu cầu chỉ phủ một số kiểu lộn xộn. Yêu cầu thật có ảnh chụp, file đính kèm, giọng điệu khác.
- n rất nhỏ (1-2 lần mỗi agent hợp lệ). Không so sánh agent này tốt hơn agent kia.
- Chấm nhãn "câu hỏi / cần người quyết" bằng so khớp từ khóa, chỉ là ước lượng; chúng tôi đọc tay các ca chính.
- Mọi quy định (ngưỡng chiết khấu, phí giao, thẩm quyền) là quy định bịa của công ty giả. Không phải tư vấn thuế hay pháp luật.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây.
