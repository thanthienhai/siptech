# Làm sạch danh bạ khách hàng bằng coding agent (Claude Code, Antigravity)

> Ngày làm và đo: 2026-11-20 (bài 1-3), 2026-11-21 (bài 4). **Toàn bộ dữ liệu trong bài là GIẢ để học**: sinh bằng `du-lieu/sinh_du_lieu.py`, hạt giống cố định, không có khách hàng hay số điện thoại thật.
> Nhãn: **[Đo được]** = kết quả chạy và chấm của chúng tôi; **[Nguồn]** = có link; **[Đề xuất]** = ý kiến người soạn.

## Bạn làm được gì sau bài toán này

Bạn biết giao cho coding agent việc dọn một file danh bạ khoảng 400 dòng (cùng một khách nhiều dòng, SĐT và email viết lộn xộn, tên và địa chỉ viết tắt), và nhận lại ba thứ: **danh bạ sạch** mỗi khách một dòng, **nhật ký "đã gộp gì và vì sao"** để hoàn tác được, và **danh sách ca nghi trùng** để người quyết. Bạn cũng biết kiểm kết quả (cả khi không có đáp án), duyệt ca mơ hồ, chạy lại hằng tuần mà không tốn lượt gọi mô hình, và **giả danh danh bạ trước khi đưa cho agent đám mây**.

Nguyên tắc xuyên suốt: quy tắc gộp do **code tất định** làm; agent giúp viết code và gợi ý ở ca mơ hồ; ca mơ hồ chuyển cho người, không tự gộp.

Danh bạ thật là dữ liệu cá nhân. Agent đám mây gửi nội dung file nó đọc tới máy chủ nhà cung cấp, nên với dữ liệu thật hãy đọc [An toàn dữ liệu và pháp lý khi dùng AI](../an-toan-du-lieu-va-phap-ly-vn.md) và hỏi người phụ trách pháp lý trước. Chúng tôi chỉ nêu nguyên tắc, không viết điều luật.

## Bốn bài

| Bài | Mất bao lâu | Kết quả |
|---|---|---|
| [Bài 1. Chuẩn bị danh bạ và giao việc](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | khoảng 30 phút (agent chạy 9-17 phút) | Bản giả danh, thư mục riêng, prompt đã dán, agent tạo đủ 6 file |
| [Bài 2. Chạy thật và kiểm tra](cap-01-chay-that-va-kiem-tra.md) | khoảng 40 phút | Biết agent đúng bao nhiêu, sai ở đâu, 5 phép kiểm không cần đáp án |
| [Bài 3. Dùng hằng ngày](cap-02-dung-hang-ngay.md) | khoảng 30 phút, rồi 20-40 phút mỗi tuần | Quy trình 6 bước, hoàn tác một lệnh, hiểu vì sao phải thử script cũ trên dữ liệu mới |
| [Bài 4. Prompt mẫu và bài tập](cap-03-prompt-mau-va-bai-tap.md) | khoảng 2 giờ | 10 prompt dùng lại được, 3 bài tập có tiêu chí kiểm bằng lệnh, checklist dữ liệu thật |

## Kết quả đo tóm tắt **[Đo được]**

Cùng một prompt, cùng 400 dòng dữ liệu, mỗi agent chạy **2 lần** (một lần đủ log, một lần chỉ còn file kết quả vì mất log). n rất nhỏ: chỉ mô tả quan sát, **không kết luận agent nào tốt hơn**.

| | claude lần 1 | agy lần 1 | claude lần 0 (mất log) | agy lần 0 (mất log) |
|---|---|---|---|---|
| Nhóm gộp đúng trọn vẹn | 52/52 | 52/52 | 52/52 | **51/52** |
| Cặp bị gộp nhầm | 0 | 0 | 0 | 0 |
| Ca cần người quyết được báo đúng | 25/25 | 25/25 | 25/25 | **21/25** |
| SĐT đúng | 377/377 | **376/377** | 377/377 | 377/377 |
| Địa chỉ khớp | **259/261** | 261/261 | 261/261 | 262/262 |
| Chạy lại script ra file giống từng byte | đạt | đạt | đạt | đạt |
| Thời gian (giây) | 513,6 | 1.031,3 | không có log | không có log |

Quan sát chính:

- Với prompt **ghi rõ từng quy tắc**, cả hai agent viết được script làm đúng gần hết. Lỗi còn lại nhỏ nhưng thật: mất 1 SĐT, `DN` không thành Đà Nẵng, bỏ sót 4 ca cần quyết và 1 nhóm gộp (agy lần 0).
- Báo cáo bằng chữ của agent **không đáng tin tuyệt đối**: báo cáo agy lần 1 ghi "7 khách thiếu SĐT, 99 thiếu địa chỉ" trong khi file sạch của nó có 29 và 81.
- `tu_kiem.py` (không cần đáp án) bắt được lỗi bỏ sót ca nghi trùng, nhưng **đạt cả 5 phép** ở đợt dữ liệu mới dù có lỗi: phải đọc thêm cảnh báo và soi mẫu.
- **Chạy lại script cũ trên đợt dữ liệu mới** (bài 3, 1 lần mỗi script): không gộp nhầm ai, nhưng mất 6 (claude) và 10 (agy) SĐT. Kết quả tốt ở đợt 1 không cho phép suy ra độ chính xác trên dữ liệu mới.
- **Bài 4** (6 lần gọi Claude Code, mỗi prompt n = 1): agent tìm lại đúng hai lỗi bài 2 khi được gợi ý kiểm; thêm quy tắc `DN` chỉ đổi đúng 2 ô; thêm quy tắc email Q3 qua bộ chấm. Hai lần agent ghi script phụ ra ngoài thư mục dù được dặn không.

## Công cụ và phiên bản

Claude Code `2.1.329` và Antigravity (`agy`) `1.5.13` ở bài 1-3 (đọc từ `--version`); bài 4 chạy Claude Code `2.1.330`. Log không ghi tên mô hình nên chúng tôi không nêu. Python 3.13 với `openpyxl`, `pandas`.

## Chưa làm và giới hạn

- Dữ liệu giả, bẫy do chúng tôi nghĩ ra. Danh bạ thật lộn xộn hơn.
- n rất nhỏ ở mọi phép đo; không đo độ ổn định giữa các lần chạy.
- **Chưa thử** prompt mơ hồ (không ghi quy tắc): kết quả chỉ nói về prompt có quy tắc chi tiết.
- Chưa áp quyết định của người vào bản sạch; chưa cập nhật tăng dần khi có đợt mới (giữ mã `KH` cũ); chưa so khớp mờ.
- Quy tắc SĐT theo trang Wikipedia "Telephone numbers in Vietnam" (CC BY-SA 4.0, https://en.wikipedia.org/wiki/Telephone_numbers_in_Vietnam); trang này không có bảng đổi đầu số cũ 01x sang mới, nên số đó được coi là không hợp lệ chứ không tự đổi.
- Bản giả danh của bài 4 mới đo trên một script và một bộ dữ liệu.
- Lần phát lệnh đầu của bài 1-3 bị mất log (xem bài 2, phần Đào sâu); log đã che đường dẫn máy và tên tổ chức.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.
