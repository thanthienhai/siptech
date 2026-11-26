# Thực hành coding agent 01: Đối soát sao kê ngân hàng với sổ đơn hàng

> **Toàn bộ dữ liệu trong thư mục này là dữ liệu giả để học.** Tên người, số điện thoại (dãy `0900000xxx`), số tài khoản (`0000123456789`), công ty và nhà cung cấp (`CTY TNHH MOCHI DEMO`, `NCC DEMO 01`, `DV VAN CHUYEN XANH`) đều bịa. Không phải dữ liệu của doanh nghiệp nào.

## Bạn làm được gì sau bài toán này

Giao cho một coding agent (chương trình AI tự đọc file, viết và chạy code) việc ghép từng dòng **sao kê ngân hàng** với **sổ đơn hàng**; chấm kết quả bằng code có đáp án thay vì tin lời agent; biến script agent viết thành quy trình hàng tháng có người duyệt; và biết ca nào agent phải đẩy sang người quyết. Phép tính tiền luôn do code làm, không để mô hình tính nhẩm.

Việc này hay gặp ở shop và công ty nhỏ thu tiền bằng chuyển khoản (kể cả QR): khoảng 150 dòng sao kê và 120 đơn mỗi tháng, nội dung chuyển khoản do khách tự gõ nên lộn xộn (không dấu, viết tắt, sai mã đơn, chỉ ghi tên), lại có chuyển thiếu, chuyển thừa, chuyển hai lần, trả nhiều đơn một lần, hoàn tiền, hãng vận chuyển trả gộp tiền COD và tiền không rõ nguồn. Làm tay mất vài giờ và dễ sót; sai sót dẫn tới đòi tiền nhầm khách, hoàn tiền nhầm hoặc bỏ sót khoản chưa thu.

## Bốn bài

| Bài | Mất bao lâu | Kết quả |
|---|---|---|
| [Bài 1. Chuẩn bị dữ liệu và giao việc cho agent](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | khoảng 20 phút, agent chạy thêm vài phút đến vài chục phút | Thư mục có bảng ghép, danh sách ngoại lệ, tổng kiểm |
| [Bài 2. Chạy thật và kiểm kết quả bằng đáp án](cap-01-chay-that-va-cham-ket-qua.md) | chấm vài giây, đọc kỹ khoảng 30 phút | Bảng điểm và hiểu agent sai ở đâu |
| [Bài 3. Đưa vào dùng hằng ngày](cap-02-dung-hang-ngay.md) | khoảng 30 phút dựng lần đầu | Quy trình hàng tháng, kiểm tái lập, checklist người duyệt |
| [Bài 4. Prompt mẫu và bài tập tự làm](cap-03-prompt-mau-va-bai-tap.md) | mỗi prompt vài phút, mỗi bài tập 20 đến 40 phút | 9 prompt dùng lại được, 3 bài tập có tiêu chí chấm bằng code |

## Sắp xếp thư mục trước khi làm

Tạo một thư mục trống làm nơi làm bài (ví dụ `bai-toan`) và sắp như sau:

```file
bai-toan/
  du-lieu/      giải nén du-lieu.zip vào đây (dữ liệu giả và bản giao việc)
  lan-chay-1/   thư mục RIÊNG của agent: bạn tạo ở Bài 1, chỉ chép file dữ liệu vào
  ket-qua/      giải nén bo-cham.zip vào đây (đáp án và bộ chấm), SAU KHI agent chạy xong
```

- Trong từng bài, lệnh chấm cho biết bạn đứng ở thư mục nào. Phần lớn bộ chấm cần `du-lieu/` và `ket-qua/` nằm **cạnh nhau**.
- **Để đáp án ngoài tầm agent.** Đừng giải nén `bo-cham.zip` trước khi agent chạy xong. Agent có thể đi lên thư mục cha để tìm file; việc này đã xảy ra trong các lần chạy của chúng tôi (xem bài 2).
- **Cần Python 3** (cách kiểm và cài: [Bài 1 của nhóm Bắt đầu](../th-bat-dau-voi-coding-agent/cap-00-lam-quen-cua-so-dong-lenh.md)). Một số bộ chấm đọc file Excel nên cần thư viện `openpyxl`: nếu thấy `ModuleNotFoundError`, gõ `pip install openpyxl`. **Chưa kiểm** trên máy sạch.

## Dữ liệu mẫu (sinh, hạt giống cố định)

| File | Nội dung |
|---|---|
| `du-lieu/sao-ke-t10-2026.csv` | 144 dòng giao dịch (97 ghi có, 47 ghi nợ), có dòng thông tin đầu file và dòng tổng cuối file |
| `du-lieu/so-don-hang-t10-2026.xlsx` | 128 đơn: 108 đơn chuyển khoản, 20 đơn COD; có ngày và tiền nhập dạng chữ |
| `du-lieu/sinh_du_lieu.py` | Sinh lại dữ liệu và đáp án (`python -X utf8 sinh_du_lieu.py`); thêm tham số để sinh bộ khác |
| `du-lieu/bai_tap.py`, `doi_cot_sao_ke.py`, `kiem_nhanh.py`, `sao-ke-moi.csv` | Dùng ở bài 3 và bài 4: dựng bộ dữ liệu bài tập, giả lập sao kê đổi định dạng, tự kiểm kết quả |
| `ket-qua/dap-an.json` | **Đáp án** (không đưa vào thư mục agent làm việc) |

Bẫy cài vào: mã đơn viết lệch (khoảng trắng, chữ O thay số 0), chỉ ghi tên không dấu hoặc viết tắt, chuyển thiếu/thừa/trùng, trả nhiều đơn, hoàn tiền (một ca hoàn một phần), ghi mã của đơn khác, hai khách trùng tên cùng số tiền, COD gộp, tiền không rõ nguồn (một dòng trùng đúng số tiền một đơn chưa thu), phí và lãi ngân hàng, 41 dòng chi không liên quan đơn. Đáp án: **130 dòng xác định, 14 dòng mơ hồ (đúng ra phải để người quyết)**, 26 dòng cần đưa vào ngoại lệ, 10 đơn chuyển khoản chưa thu.

## Kết quả đo tóm tắt **[Đo được]**

Ngày 2026-11-20, n = 1 lần chạy có log mỗi agent:

| Chỉ số | Claude Code | Antigravity (`agy`) |
|---|---|---|
| Thời gian một lần chạy | 557 giây | 1.257 giây (hạn nới lên 1.800 giây) |
| Dòng xác định ghép đúng | 130/130 | 130/130 |
| Dòng mơ hồ được báo cho người quyết | 13/14 | 9/14 |
| Dòng mơ hồ ghép sai mà không báo | 0 | 0 |
| Ngoại lệ thật bắt được | 25/26 | 21/26 |
| Tổng kiểm (6 số) đúng | 6/6 | 6/6 |
| Mã đơn bịa (không có trong sổ) | 0 | 0 |

Chạy lại script đã có trên dữ liệu khác (hạt giống khác, không gọi agent lại): script của Claude Code vẫn 130/130; script của `agy` còn 97/130 và 100/130 trên hai bộ, kèm 5 dòng sai mà mức `CAO`. **Tổng kiểm vẫn 6/6 ở cả hai**, nghĩa là tổng kiểm đúng không chứng minh bảng ghép đúng.

Sáu prompt ở bài 4 chạy thật một lần mỗi prompt (ngày 2026-11-21): 60 đến 197 giây, 0,31 đến 0,64 USD theo log Claude Code. Chúng nêu đúng rủi ro lớn nhất của script, bắt được cả ba lỗi chúng tôi cài vào kết quả, và sửa được script khi sao kê đổi định dạng.

## Chưa làm và giới hạn

- Mỗi agent chỉ một lần chạy có log. **Không kết luận agent nào tốt hơn, chưa đo được độ ổn định.**
- Tiêu đề cột sao kê là mô phỏng, không phải bản sao của ngân hàng nào; chúng tôi không tìm được file sao kê mẫu chính thức kèm tiêu đề cột chính xác.
- Đáp án và nhãn "mơ hồ" do người sinh dữ liệu gán; một kế toán khác có thể gán khác.
- Dữ liệu thật có kiểu lộn xộn khác (nội dung bị cắt ngắn, tiền tố mã ngân hàng, nhiều sheet). Chưa thử.
- Bài tập 2 và 3 ở bài 4 chưa có lần chạy agent; tiêu chí được kiểm bằng bộ chấm và script nhỏ.
- Chưa dùng OpenCode (khóa hết hạn). Phiên bản công cụ: Claude Code 2.1.329 (bài 1, 2) và 2.1.330 (bài 4), Antigravity `agy` 1.5.13 (từ lệnh `--version`).
- Mọi quy định kế toán, chứng từ, bảo vệ dữ liệu cá nhân: cần kiểm với kế toán hoặc luật sư; bài không viết điều khoản.

## Nguồn tham chiếu định dạng sao kê

Chỉ dùng để mô phỏng cột, không chép nội dung. Chi tiết ở phần Đào sâu của bài 1.

- **[Nguồn]** DNSE, "Cách đọc sao kê tài khoản VCB": https://www.dnse.com.vn/hoc/cach-doc-sao-ke-tai-khoan-vcb-chinh-xac-nhat
- **[Nguồn]** `ofxstatement-vn-vietcombank` (giấy phép MIT): https://github.com/darkms/ofxstatement-vn-vietcombank (chúng tôi chỉ đọc trang mô tả).
- **[Nguồn]** Hướng dẫn nhập sao kê từ Excel của MISA: https://helpact.misa.vn/?p=72941 (chỉ xem phần tóm tắt trong kết quả tìm kiếm).

## Lưu ý về log và ảnh

- Log trong `logs/` là log gốc các lần chạy (`claude-1`, `agy-2` ở bài 2; `bai4-*` ở bài 4), **đã thay tên người dùng và đường dẫn máy bằng `user`/`<org>`**; nội dung sự kiện không bị sửa. Mỗi lệnh của `agy` kèm một đoạn lỗi về file profile PowerShell của máy chạy; đó là nhiễu của máy.
- Ảnh terminal là **dựng lại từ log thật** bằng `term.py`, không phải ảnh chụp trực tiếp cửa sổ TUI, đã che đường dẫn máy. Ảnh bảng (dữ liệu, kết quả, điểm) dựng từ file thật trong thư mục này.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.
