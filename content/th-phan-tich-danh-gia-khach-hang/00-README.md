# Bài toán 04: Phân tích đánh giá của khách (quán cà phê, 250 đánh giá)

> Dữ liệu trong thư mục này là **dữ liệu giả để học**: quán "Mây Lưng Chừng" là hư cấu, 250 đánh giá do script sinh với hạt giống cố định. Không có tên người, số điện thoại hay doanh nghiệp thật. Không dùng làm kết luận về bất kỳ quán thật nào.

## Bạn làm được gì sau bài toán này

Quán nhận đánh giá từ Google Maps, Shopee Food và fanpage, mỗi nơi một kiểu. Sau bốn bài bạn biết cách giao cho một coding agent đọc cả 250 bài và trả về **năm thứ chủ quán dùng ngay**: ý kiến từng chủ đề kèm sắc thái, danh sách bài nguy cấp (nghi ngộ độc, nhân viên chửi khách, tính tiền gian), xu hướng theo tuần, và đúng 5 việc nên sửa trước với bằng chứng trích nguyên văn. Quan trọng hơn, bạn biết **kiểm** kết quả: mọi con số do code đếm, mọi trích dẫn do code kiểm là chép nguyên văn, bài mỉa mai hoặc không rõ nghĩa được chuyển cho người đọc thay vì bị đoán.

## Bốn bài

| Bài | Mất bao lâu | Kết quả |
|---|---|---|
| [Bài 1. Chuẩn bị dữ liệu và giao việc](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | Khoảng 20 phút + thời gian agent chạy | Thư mục riêng có 250 đánh giá, prompt 6 phần đã dán, agent tạo 7 file trong `dau-ra/` |
| [Bài 2. Chạy thật và kiểm kết quả](cap-01-chay-that-va-kiem-tra-ket-qua.md) | Khoảng 40 phút | Bảng chấm bằng đáp án và bằng bộ kiểm không cần đáp án, các ca agent khác đáp án |
| [Bài 3. Dùng hằng tuần](cap-02-dua-vao-dung-hang-ngay.md) | Lần đầu khoảng 1 giờ | Quy trình che thông tin, kiểm, cảnh báo tuần, người duyệt, lưu trữ |
| [Bài 4. Prompt mẫu và bài tập](cap-03-prompt-mau-va-bai-tap.md) | 1 đến 2 giờ | 8 prompt dùng lại được, ba bài tập có bộ chấm, hướng dẫn dùng dữ liệu thật |

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

## Kết quả đo tóm tắt (ngày 2026-11-20)

Cùng một prompt (không sửa sau khi thấy kết quả), cùng dữ liệu. Claude Code 2.1.329 và Antigravity `agy` 1.5.13. **n nhỏ: claude 2 lần chạy hoàn chỉnh, agy 3 lần (1 lần bị dừng ở giới hạn 900 giây), chưa đo được độ ổn định.** Chấm bằng `ket-qua/cham.py`:

| Tiêu chí | claude lần 0 | claude lần 1 | agy lần 0 | agy lần 1 (hết giờ) | agy lần 2 |
|---|---|---|---|---|---|
| Loại bỏ đúng (trùng, spam, câu hỏi) | 8/8 | 8/8 | 7/8 | 7/8 | 7/8 |
| Chủ đề tìm đủ (bài x chủ đề) | 387/388 | 387/388 | 387/388 (thừa 3) | 386/388 | 385/388 (thừa 2) |
| Sắc thái đúng (trên ý đã gán) | 373/373 | 372/373 | 373/373 (hoãn 1) | 368/368 (hoãn 4) | 368/368 (hoãn 4) |
| Mỉa mai vào `CAN_NGUOI_DOC` | 14/14 | 14/14 | 14/14 | 14/14 | 14/14 |
| Nguy cấp bắt được / bắt thừa | 16/16, 0 | 16/16, 0 | 16/16, 0 | 16/16, 0 | 16/16, 0 |
| Trích dẫn không nguyên văn | 0 | 0 | 0 | 0 | 0 |
| Báo cáo 5 việc, phủ 5 vấn đề cài | có, 5/5 | có, 5/5 | có, 5/5 | **không có file** | có, 5/5 |

Thời gian: claude lần 1 mất 454,5 giây, agy lần 2 mất 957,9 giây. Hai lần "lần 0" chạy xong nhưng mất log (do chúng tôi chạy nền sai cách, xem bài 2); đầu ra còn và đã chấm.

**Đọc cho đúng.** Gần như tuyệt đối trên dữ liệu này, nhưng bộ dữ liệu **dễ hơn đánh giá thật**: khoảng 3/4 bài ghép từ ngân hàng câu có hạn, và log `agy-lan2` cho thấy agent đã đếm các cụm lặp rồi dựng bộ khớp mẫu. Đáp án có ca còn tranh cãi (R191 spam hay ý kiến thật; R105 "ổn" là tích cực hay trung tính), và **luật chấm đã được chúng tôi sửa một lần** sau khi xem kết quả lần 0 (không phạt `CAN_NGUOI_DOC` trên bài ranh giới), nên kết quả "đẹp hơn" một phần nhờ sửa luật. Muốn biết với quán của bạn, tự gán nhãn 50 bài rồi chấm (bài 3).

**Bài 4 (lần chạy 2026-11-21, n=1 mỗi prompt):** 5 trong 8 prompt đã chạy thật trên đầu ra có sẵn. Bộ kiểm chéo do một phiên mới tự viết bắt đủ 3 lỗi cố ý trong bản sao; báo cáo một trang có trích dẫn đúng nhưng con số "36 khách" không khớp bảng bài 2 (41 ý, agent tự bỏ 5 ý trùng với việc khác, không ghi vào báo cáo).

## Đào sâu: cấu trúc thư mục trong bản gốc của tác giả
```
04-phan-tich-danh-gia-khach-hang/
  00-README.md, bai-1 .. bai-4 (.md)
  du-lieu/    danh-gia.csv, danh-gia.xlsx, sinh_du_lieu.py, prompt-giao-viec.txt,
              them-dong-goi.csv, danh-gia-270.csv, sinh_them_dong_goi.py   (bài tập 1)
  ket-qua/    dap-an.json, cham.py, kiem-tra-dau-ra.py, canh-bao-tuan.py, cham-bo-vang.py,
              che-thong-tin.py, dem-nguy-cap.py, so-bao-cao.py, lam-hong-ban-sao.py, bo-vang-dong-goi.csv,
              claude-lan0, claude-lan1, agy-lan0, agy-lan1-het-gio, agy-lan2 (mỗi nơi có dau-ra/),
              bai4/ (prompt và đầu ra của các lần chạy bài 4)
  logs/       claude-lan1, agy-lan2, bai4-* (.raw.jsonl và .json)
  anh/        ảnh dùng trong bài
```

Ảnh terminal dựng lại từ log đã che đường dẫn máy và tên tổ chức, không phải ảnh chụp trực tiếp. Trong `logs/` chúng tôi đã che thông tin cá nhân của máy chạy (tên thư mục người dùng, tên tổ chức trong đường dẫn); ngoài chỗ đó không sửa gì.

## Việc cần người làm và giới hạn (tóm tắt)

- Người đọc: toàn bộ nhóm `CAN_NGUOI_DOC`, mọi dòng `nguy-cap.csv` (kể cả dòng "nghi"), và quyết định cuối về 5 việc.
- Dữ liệu giả, có cấu trúc lặp, **dễ hơn đánh giá thật**; chưa kiểm trên đánh giá thật.
- n=2 đến 3 lần chạy mỗi agent ở bài 1 đến 3, n=1 mỗi prompt ở bài 4; chưa đo độ ổn định.
- Đáp án một số ca còn tranh cãi (R191, R105); luật chấm sửa một lần.
- Agent làm việc trên máy với quyền rộng, nên dùng thư mục riêng (và máy hoặc tài khoản riêng với dữ liệu thật).
- Đánh giá thật có thể chứa tên, số điện thoại khách: che trước khi đưa cho dịch vụ đám mây, hỏi luật sư về quy định bảo vệ dữ liệu cá nhân; xem [an toàn dữ liệu](../an-toan-du-lieu-va-phap-ly-vn.md). Chúng tôi không viết điều khoản cụ thể.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.
