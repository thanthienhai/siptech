# Bài toán 04: Phân tích đánh giá của khách (quán cà phê, 250 đánh giá)

> Dữ liệu trong thư mục này là **dữ liệu giả để học**: quán "Mây Lưng Chừng" là hư cấu, 250 đánh giá do `du-lieu/sinh_du_lieu.py` sinh (hạt giống cố định). Không có tên người, số điện thoại hay doanh nghiệp thật. Không dùng làm kết luận về bất kỳ quán thật nào.

## 1. Bài toán và vì sao chủ quán gặp

Quán nhỏ nhận đánh giá từ nhiều nơi cùng lúc: Google Maps, Shopee Food, fanpage Facebook. Mỗi nơi một kiểu: có nơi có sao, có nơi không; ngày viết kiểu `2026-10-04` hoặc `04/10/2026`; khách viết không dấu, viết tắt (`ko`, `dc`, `nv`, `vs`), thêm emoji, đôi khi mỉa mai ("Phục vụ nhanh ghê, chỉ đợi có 45 phút thôi à 👏"), và một bài thường nhắc nhiều chuyện cùng lúc ("đồ uống ngon, giá ok, nhưng nhân viên hơi chậm").

Chủ quán thường chỉ làm được một trong hai việc: chỉ nhìn điểm sao trung bình (không biết vì sao), hoặc đọc vài bài mới nhất rồi sửa theo cảm tính. Cả hai đều bỏ sót ba thứ quan trọng: (1) sắc thái **từng ý** chứ không phải cả bài (khen món, chê phục vụ trong cùng một bài), (2) bài **nguy cấp** (nghi ngộ độc, nhân viên chửi khách, tính tiền gian) bị chìm giữa hàng chục bài khen/chê thường, (3) **xu hướng theo tuần** (chê giao hàng có thật sự tăng từ tuần nào?).

Bài toán giao cho coding agent: đọc cả 250 bài, trả về năm thứ chủ quán dùng được ngay, và **mọi con số do code đếm, mọi trích dẫn kiểm bằng code là chép nguyên văn**. Bài mỉa mai hoặc không rõ nghĩa thì không đoán, đưa vào nhóm `CAN_NGUOI_DOC`.

## 2. Dữ liệu mẫu

| Mục | Giá trị [Đo được] (đếm từ `ket-qua/dap-an.json`) |
|---|---|
| Số bài | 250 (Google Maps 124, Shopee Food 73, Facebook 53), 12 tuần từ 24/08 đến 15/11/2026 |
| Số ý kiến cài đáp án (sau khi trừ bài loại bỏ) | 391 ý kiến trên 242 bài |
| Bài mỉa mai | 14 (đáp án: ý thật là chê, agent phải xếp `CAN_NGUOI_DOC`) |
| Bài nguy cấp | 16 bắt buộc (ngộ độc 6 trong đó 2 ở dạng "nghi", thái độ 5, lừa đảo 5) + 4 ca ranh giới không phạt dù báo hay không |
| Bẫy từ khóa | 6 bài khen phóng đại ("ngon xỉu", "ghiền như bị bỏ bùa", "đau bụng cười") không phải nguy cấp |
| Bài đáng loại bỏ | 8: 4 bài trùng nguyên văn bài trước, 3 spam/quảng cáo, 1 câu hỏi |
| Bài mơ hồ | 6 ("Được. Như mọi khi.", "Ok nha 👌"): không bị phạt dù gán gì |
| Sao trống | 32 bài; 28 bài viết không dấu; 96 bài có emoji; 43 bài có teen code kiểu `ko`, `dc`, `nv` |
| Việc "cài" vào dữ liệu | 5 vấn đề có thật để agent tìm: I1 nghi ngộ độc (từ 19/10 đến 01/11), I2 giao hàng xấu đi từ tuần 05/10, I3 tăng giá từ tuần 28/09, I4 thái độ nhân viên (từ 07/09 đến 27/09), I5 tính tiền sai/khuyến mãi ảo/nhận tiền không giao (từ 12/10 đến 08/11) |

Cách sinh: khoảng 190 bài ghép từ ngân hàng mệnh đề (mỗi mệnh đề đã gán sẵn chủ đề và sắc thái) rồi thêm nhiễu: bỏ dấu, teen code, kéo dài chữ, emoji, đuôi câu vô nghĩa; 60 bài còn lại **viết tay** cho các tình huống khó (nguy cấp, mỉa mai, bẫy từ khóa, tiếng Anh, nhiều ý trái chiều). Xem rõ hơn ở bài 1.

### Tài liệu tham chiếu thật (chỉ để học giọng văn, không chép nội dung)

- UIT-ViSFD: bộ 11.122 bình luận tiếng Việt về điện thoại trên sàn thương mại điện tử, gán nhãn khía cạnh và sắc thái. **[Nguồn]** bài báo: <https://arxiv.org/abs/2105.15079>; bản trên Hugging Face: <https://huggingface.co/datasets/visolex/ViSFD>. Thẻ dữ liệu ghi: xem LICENSE của kho gốc, nếu không nêu thì coi như CC BY 4.0; dùng thương mại thì liên hệ nhóm tác giả. Nơi khác (SEACrowd) ghi giấy phép "không rõ", tác giả nói cho phép dùng cho nghiên cứu.
- UIT-ViSD4SA: cùng 11.122 bình luận, gán thêm đoạn (span) cho từng khía cạnh. **[Nguồn]** <https://arxiv.org/abs/2110.07833>. Giấy phép cũng ghi "không rõ" trên SEACrowd.
- Vì giấy phép không rõ ràng, chúng tôi **không chép câu nào** vào bộ dữ liệu. Các tài liệu này chỉ gợi ý hai điều: người Việt thật sự viết lẫn nhiều khía cạnh trong một bình luận, và nhãn nên là ba mức (tích cực, trung tính, tiêu cực) theo từng khía cạnh.
- Đây là bình luận điện thoại, không phải quán cà phê. Giọng văn quán cà phê ở đây là do chúng tôi bịa theo cách viết đời thường, nên độ khó có thể khác dữ liệu thật (xem phần Giới hạn).

## 3. Mục lục 3 bài

1. [`cap-00-chuan-bi-du-lieu-va-giao-viec.md`](cap-00-chuan-bi-du-lieu-va-giao-viec.md): dữ liệu, các bẫy cài sẵn, cách mở agent bằng giao diện/lệnh đơn giản, prompt giao việc 6 phần.
2. [`cap-01-chay-that-va-kiem-tra-ket-qua.md`](cap-01-chay-that-va-kiem-tra-ket-qua.md): chạy `claude` và `agy` thật, chấm bằng đáp án và bằng code, lỗi đã gặp (cả lỗi của chúng tôi).
3. [`cap-02-dua-vao-dung-hang-ngay.md`](cap-02-dua-vao-dung-hang-ngay.md): quy trình hằng tuần, tự kiểm không cần đáp án, người duyệt, giới hạn, mở rộng.

## 4. Kết quả đo tóm tắt (ngày 2026-11-20)

Cùng một prompt (`ket-qua/prompt-giao-viec.txt`, không sửa sau khi thấy kết quả), cùng dữ liệu. Claude Code 2.1.329 và Antigravity `agy` 1.5.13. **n nhỏ: claude 2 lần chạy hoàn chỉnh, agy 3 lần chạy (1 lần bị dừng ở giới hạn 900 giây), chưa đo được độ ổn định.**

| Tiêu chí (chấm bằng `ket-qua/cham.py`) | claude lần 0 | claude lần 1 | agy lần 0 | agy lần 1 (hết giờ) | agy lần 2 |
|---|---|---|---|---|---|
| Loại bỏ đúng (trùng, spam, câu hỏi) | 8/8 | 8/8 | 7/8 | 7/8 | 7/8 |
| Chủ đề tìm đủ (bài x chủ đề) | 387/388 | 387/388 | 387/388 (thừa 3) | 386/388 | 385/388 (thừa 2) |
| Sắc thái đúng (trên ý đã gán) | 373/373 | 372/373 | 373/373 (hoãn 1) | 368/368 (hoãn 4) | 368/368 (hoãn 4) |
| Mỉa mai vào `CAN_NGUOI_DOC` | 14/14 | 14/14 | 14/14 | 14/14 | 14/14 |
| Nguy cấp bắt được / bắt thừa | 16/16, 0 | 16/16, 0 | 16/16, 0 | 16/16, 0 | 16/16, 0 |
| Trích dẫn không nguyên văn | 0 | 0 | 0 | 0 | 0 |
| Báo cáo 5 việc, phủ 5 vấn đề cài | có, 5/5 | có, 5/5 | có, 5/5 | **không có file** | có, 5/5 |
| Có log gốc trong `logs/` | không | có | không | không | có |

Thời gian: claude lần 1 mất 454,5 giây, agy lần 2 mất 957,9 giây (đặt giới hạn 1500 giây vì lần 1 bị dừng ở 900 giây). Hai lần "lần 0" chạy xong nhưng log bị mất (lỗi do chúng tôi chạy nền sai cách, xem bài 2); kết quả đầu ra vẫn còn và đã được chấm.

**Đọc kết quả thế nào cho đúng.** Gần như tuyệt đối trên dữ liệu này, nhưng đừng suy ra "agent làm được 99% trên đánh giá thật". Khoảng 3/4 bài trong bộ này ghép từ ngân hàng câu có hạn, và ở lần chạy `agy-lan2` log cho thấy agent đã đếm các cụm lặp rồi dựng bộ khớp mẫu. Phần khó thật sự là 60 bài viết tay, trong đó cả hai agent làm đúng gần hết (xem bài 2). Muốn biết với dữ liệu của quán bạn, hãy tự gán nhãn 50 bài rồi chấm (bài 3).

## 5. Cấu trúc thư mục

```
04-phan-tich-danh-gia-khach-hang/
  00-README.md
  cap-00-chuan-bi-du-lieu-va-giao-viec.md
  cap-01-chay-that-va-kiem-tra-ket-qua.md
  cap-02-dua-vao-dung-hang-ngay.md
  du-lieu/    danh-gia.csv, danh-gia.xlsx, sinh_du_lieu.py     (cho người học tải về)
  ket-qua/    prompt-giao-viec.txt, dap-an.json, cham.py, bao-cao-cham.json,
              dung_anh.py, kiem-tra-dau-ra.py, canh-bao-tuan.py, cham-bo-vang.py, che-thong-tin.py   (công cụ dùng hằng tuần, bài 3)
              claude-lan0/, claude-lan1/, agy-lan0/, agy-lan1-het-gio/, agy-lan2/   (mỗi nơi có dau-ra/ của agent)
  logs/       claude-lan1.raw.jsonl + .json, agy-lan2.raw.jsonl + .json
  anh/        10 ảnh dùng trong bài (a, b x2, c x2, d, e, e2, f, g)
```

Ảnh terminal dựng lại từ log đã che đường dẫn máy và tên tổ chức (script dựng: `ket-qua/dung_anh.py`, chạy lại được).

Ghi chú về log: trong `logs/` chúng tôi đã che thông tin cá nhân của máy chạy (tên thư mục người dùng, tên tổ chức trong đường dẫn). Ngoài chỗ đó không sửa gì.

## 6. Việc cần người làm / Giới hạn (tóm tắt)

- Người đọc: toàn bộ nhóm `CAN_NGUOI_DOC`, mọi dòng `nguy-cap.csv` (kể cả dòng "nghi"), và quyết định cuối về 5 việc.
- Giới hạn chính: dữ liệu giả và có cấu trúc lặp; n=2-3 lần chạy mỗi agent; đáp án một số ca còn tranh cãi; agent làm việc trên máy với toàn quyền nên phải dùng thư mục riêng; đánh giá thật có thể chứa tên, số điện thoại khách (cần che trước khi gửi cho dịch vụ đám mây, cần hỏi luật sư về quy định bảo vệ dữ liệu cá nhân, không viết điều khoản cụ thể ở đây).

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây.
