# Thực hành coding agent 01: Đối soát sao kê ngân hàng với sổ đơn hàng

> **Toàn bộ dữ liệu trong thư mục này là dữ liệu giả để học.** Tên người, số điện thoại (dãy `0900000xxx`), số tài khoản (`0000123456789`), công ty và nhà cung cấp (`CTY TNHH MOCHI DEMO`, `NCC DEMO 01`, `DV VAN CHUYEN XANH`) đều bịa. Không phải dữ liệu của doanh nghiệp nào.

## Bài toán

Shop hoặc công ty nhỏ nhận tiền bằng chuyển khoản. Cuối tháng, nhân viên kế toán ngồi ghép từng dòng của **sao kê ngân hàng** (CSV/Excel xuất từ internet banking, khoảng 150 dòng/tháng) với **sổ đơn hàng** (Excel, khoảng 120 đơn). Nội dung chuyển khoản do khách tự gõ nên lộn xộn: không dấu, viết tắt, sai mã đơn, chỉ ghi tên. Lại có chuyển thiếu, chuyển thừa, chuyển hai lần, một lần trả nhiều đơn, hoàn tiền, hãng vận chuyển trả gộp tiền COD, và tiền không rõ nguồn.

Việc làm bằng tay vừa chậm vừa dễ sót. Việc của coding agent trong bài này: **viết và chạy code Python** để ghép phần chắc chắn, và đẩy phần không chắc sang người với nhãn `CAN NGUOI QUYET`. Phép tính tiền do code làm, không để mô hình tính nhẩm.

## Vì sao SME Việt Nam gặp bài toán này

- Thu tiền chủ yếu bằng chuyển khoản (kể cả QR) mà không có hệ thống gắn tiền với đơn tự động.
- Khách ghi nội dung tự do trên điện thoại.
- Người làm kế toán thường kiêm nhiều việc; đối soát dồn vào cuối tháng.
- Sai sót ở đây dẫn tới đòi tiền sai khách, hoàn tiền nhầm, hoặc bỏ sót khoản chưa thu.

## Dữ liệu mẫu (sinh, hạt giống cố định)

| File | Nội dung |
|---|---|
| `du-lieu/sao-ke-t10-2026.csv` | 144 dòng giao dịch (97 ghi có, 47 ghi nợ), có dòng thông tin đầu file và dòng tổng cuối file |
| `du-lieu/so-don-hang-t10-2026.xlsx` | 128 đơn: 108 đơn chuyển khoản, 20 đơn COD; có ngày/tiền nhập dạng chữ |
| `du-lieu/sinh_du_lieu.py` | Script sinh lại dữ liệu và đáp án (`python -X utf8 sinh_du_lieu.py`); thêm tham số để sinh bộ khác |
| `ket-qua/dap-an.json` | **Đáp án** (không đưa vào thư mục agent làm việc) |

Bẫy cài vào: mã đơn viết lệch (khoảng trắng, chữ O thay số 0), chỉ ghi tên không dấu/viết tắt, chuyển thiếu/thừa/trùng, trả nhiều đơn, hoàn tiền (có một ca hoàn một phần), ghi mã của đơn khác, hai khách trùng tên cùng số tiền, COD gộp, tiền không rõ nguồn (có một dòng trùng đúng số tiền một đơn chưa thu), phí/lãi ngân hàng, và 41 dòng chi không liên quan đơn. Đáp án: **130 dòng xác định, 14 dòng mơ hồ (đúng ra phải để người quyết)**, 26 dòng cần đưa vào ngoại lệ, 10 đơn chuyển khoản chưa thu.

## Mẫu thật dùng làm tham chiếu định dạng

Chỉ dùng để mô phỏng cột, không chép nội dung hay dữ liệu cá nhân. **Không tìm được** file sao kê mẫu chính thức của một ngân hàng có tiêu đề cột chính xác, nên bộ cột dưới đây là bộ phổ biến chứ không phải bản sao của ngân hàng nào.

- **[Nguồn]** DNSE, "Cách đọc sao kê tài khoản VCB": mô tả các cột ngày giao dịch, số CT, ghi có, ghi nợ, số dư, nội dung chi tiết. https://www.dnse.com.vn/hoc/cach-doc-sao-ke-tai-khoan-vcb-chinh-xac-nhat
- **[Nguồn]** `ofxstatement-vn-vietcombank` (giấy phép MIT), công cụ chuyển sao kê Excel Vietcombank sang OFX; cho thấy sao kê Excel có cấu trúc bảng ổn định. https://github.com/darkms/ofxstatement-vn-vietcombank (tôi chỉ đọc trang mô tả, chưa đọc mã nguồn).
- **[Nguồn]** Trang hướng dẫn nhập sao kê ngân hàng từ Excel của MISA. https://helpact.misa.vn/?p=72941 (chỉ xem phần tóm tắt trong kết quả tìm kiếm).

## Mục lục 3 bài

1. [Bài 1. Chuẩn bị dữ liệu và giao việc cho agent](cap-00-chuan-bi-du-lieu-va-giao-viec.md): dữ liệu mẫu, các bẫy, prompt 6 phần nguyên văn, cách chạy.
2. [Bài 2. Chạy thật và kiểm kết quả bằng đáp án](cap-01-chay-that-va-cham-ket-qua.md): Claude Code và `agy` chạy trên cùng dữ liệu, chấm bằng code, các sự cố gặp.
3. [Bài 3. Đưa vào dùng hằng ngày](cap-02-dung-hang-ngay.md): quy trình hàng tháng, kiểm tái lập script, checklist người duyệt, giới hạn.

## Kết quả đo tóm tắt **[Đo được]** (ngày 2026-11-20, n = 1 lần chạy có log mỗi agent)

| Chỉ số | Claude Code | Antigravity (`agy`) |
|---|---|---|
| Thời gian một lần chạy | 557 giây | 1.257 giây (hạn nới lên 1.800 giây) |
| Dòng xác định ghép đúng | 130/130 | 130/130 |
| Dòng mơ hồ được báo cho người quyết | 13/14 | 9/14 |
| Dòng mơ hồ ghép sai mà không báo | 0 | 0 |
| Ngoại lệ thật bắt được | 25/26 | 21/26 |
| Tổng kiểm (6 số) đúng | 6/6 | 6/6 |
| Mã đơn bịa (không có trong sổ) | 0 | 0 |

Quan sát khác, đáng đọc hơn các con số trên:

- Cả hai đều không tự chốt ba dòng ghi sai mã đơn và sáu dòng tiền không rõ nguồn, đưa sang `CAN NGUOI QUYET`.
- `agy` ghi mức `CAO` cho hai dòng COD gộp và không báo ngoại lệ, dù nội dung sao kê không có mã đơn nào; lần này tập đơn đoán đúng.
- Script cuối của `agy` viết cứng 38 nhánh theo số CT và mã đơn của bộ dữ liệu này. Chạy lại trên một bộ dữ liệu khác (hạt giống khác, chưa gọi agent lại), script đó ghép đúng 97/130 dòng xác định và có 5 dòng sai ở mức `CAO`; script của Claude Code vẫn 130/130. **Tổng kiểm vẫn 6/6 ở cả hai**, nghĩa là tổng kiểm đúng không chứng minh bảng ghép đúng.
- Đây là một đến hai lần chạy mỗi bên. **Không kết luận agent nào tốt hơn, chưa đo được độ ổn định.**

## Cấu trúc thư mục

```
01-doi-soat-sao-ke-ngan-hang/
  00-README.md
  cap-00-chuan-bi-du-lieu-va-giao-viec.md
  cap-01-chay-that-va-cham-ket-qua.md
  cap-02-dung-hang-ngay.md
  du-lieu/            sao kê, sổ đơn, sinh_du_lieu.py
  ket-qua/
    prompt-giao-viec.txt       prompt đã dùng (không đổi sau khi thấy kết quả)
    dap-an.json                đáp án
    cham.py, bao-cao-cham.json chấm bằng code và điểm
    dung_anh.py                dựng lại 10 ảnh trong anh/
    claude-1/, agy-2/          đầu ra thật của hai lần chạy có log
    agy-lan1-timeout900/       script nháp của lần `agy` hết giờ 900 giây (không có log)
    lan0-khong-co-log/         lần chạy đầu của cả hai agent, mất log do cách tôi khởi chạy; vẫn được chấm
    tai-lap-seed-khac/         dữ liệu thứ hai, đầu ra của hai script chạy lại, điểm chấm
  logs/               log gốc *.raw.jsonl và transcript *.json (claude-1, agy-2)
  anh/                10 ảnh dùng trong bài
```

## Lưu ý về log và ảnh

- Log trong `logs/` là log gốc của hai lần chạy, **đã thay tên người dùng và đường dẫn máy trong log bằng `user`/`<org>`** để không lộ thông tin cá nhân; nội dung sự kiện không bị sửa. Mỗi lệnh của `agy` kèm một đoạn lỗi về file profile PowerShell của máy chạy; đó là nhiễu của máy, không liên quan bài toán.
- Ảnh terminal dựng lại từ log đã che đường dẫn máy và tên tổ chức; script dựng lại là `ket-qua/dung_anh.py`.
- Ảnh terminal là **dựng lại từ log thật** bằng `term.py`, không phải ảnh chụp trực tiếp cửa sổ TUI. Ảnh bảng (dữ liệu, kết quả, điểm) dựng từ file thật trong thư mục này.
- Không dùng OpenCode (khóa hết hạn). Phiên bản công cụ: Claude Code 2.1.329, Antigravity `agy` 1.5.13 (từ lệnh `--version`).

## Lỗi và hạn chế của cả bài toán

- Tiêu đề cột sao kê là mô phỏng, không phải bản sao sao kê một ngân hàng cụ thể.
- Đáp án và nhãn "mơ hồ" do người sinh dữ liệu gán; một kế toán khác có thể gán khác.
- Dữ liệu thật sẽ có kiểu lộn xộn khác (nội dung bị cắt ngắn, tiền tố mã ngân hàng, nhiều sheet). Chưa thử.
- Mọi quy định kế toán, chứng từ, bảo vệ dữ liệu cá nhân: cần kiểm với kế toán/luật sư; bài không viết điều khoản.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây.
