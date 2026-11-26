# Bài 3. Dùng hằng tuần: máy kiểm, người duyệt, lưu lại

!!! info "Bài này"
    - **Bạn làm gì:** biến thí nghiệm ở bài 2 thành một quy trình mỗi tuần chạy trong khoảng một buổi sáng: che thông tin khách, giao việc cho agent, để máy tự kiểm, đọc cảnh báo tuần, rồi người duyệt.
    - **Mất bao lâu:** lần đầu khoảng 1 giờ; các tuần sau chủ yếu là thời gian agent chạy (**[Đo được]** 454,5 giây với `claude` và 957,9 giây với `agy` cho 250 bài) cộng thời gian người đọc.
    - **Cần có:** kết quả bài 1 và 2, thư mục `ket-qua/` (có `che-thong-tin.py`, `kiem-tra-dau-ra.py`, `canh-bao-tuan.py`, `cham-bo-vang.py`), file `danh-gia-tuan.csv` của bạn với cột `ma, nen_tang, ngay, sao, noi_dung`.
    - **Kết quả:** một thư mục lưu theo tuần có đủ kết quả, báo cáo "QUA" của bộ kiểm, và ghi chú quyết định của người duyệt.

> Ví dụ dùng **dữ liệu giả để học** (quán "Mây Lưng Chừng" hư cấu). Mọi số **[Đo được]** là kết quả chạy của chúng tôi ngày 2026-11-20 hoặc 2026-11-21; **[Đề xuất]** là ý kiến, chưa kiểm trên quán thật.

## Nhìn lại: máy làm gì, người làm gì

Từ bài 2 **[Đo được]**: trên bộ giả, cả hai agent xếp đủ 14/14 bài mỉa mai vào `CAN_NGUOI_DOC`, bắt 16/16 bài nguy cấp, không có trích dẫn nào sai nguyên văn. Nhưng cũng từ bài 2: một số ca "đúng hay sai" do người quyết (R191 spam hay ý kiến thật; "ổn" là tích cực hay trung tính), mỗi lần chạy có 15 đến 23 bài cần người đọc, và agent có thể bỏ báo cáo khi hết giờ. Nên thói quen hằng tuần cần ba lớp: **máy kiểm**, **người duyệt**, **lưu lại để so sánh**.

!!! warning "Quy tắc an toàn"
    - **Dữ liệu thật:** che số điện thoại, email, link trước khi đưa cho agent, và lướt cột `noi_dung` tìm tên người. Việc đưa dữ liệu khách cho dịch vụ đám mây có cần xin phép hay thông báo không, hỏi luật sư; xem [an toàn dữ liệu](../an-toan-du-lieu-va-phap-ly-vn.md). Chúng tôi không viết điều khoản cụ thể.
    - **Quyền:** mỗi tuần một thư mục riêng. Agent chạy với quyền rộng và có thể ghi file tạm ngoài thư mục (đã thấy ở bài 2); với dữ liệu thật, dùng máy hoặc tài khoản riêng.
    - **Đáp án:** `dap-an.json` chỉ dùng khi thử với bộ giả, không có ở dữ liệu thật và không bao giờ nằm trong thư mục agent.
    - **Đăng công khai:** agent soạn **nháp**, người đăng. Không để agent tự đăng phản hồi.

## Quy trình mỗi tuần

Giả sử sáng thứ Hai bạn có `danh-gia-tuan.csv` gồm các đánh giá trong 12 tuần gần nhất (đủ để thấy xu hướng), đặt cạnh thư mục `ket-qua/`. Cách xuất đánh giá từ Google Maps, Shopee Food, fanpage tùy nền tảng; chúng tôi chưa kiểm, bạn có thể phải chép tay vào bảng tính.

### Bước 1. Che thông tin cá nhân

Script che số điện thoại, email, link. Phải tạo thư mục `chay` trước, vì script không tự tạo.

Windows (PowerShell):

```lenh
mkdir chay
python -X utf8 ket-qua\che-thong-tin.py danh-gia-tuan.csv chay\danh-gia.csv
```

macOS hoặc Linux:

```lenh
mkdir chay
python3 -X utf8 ket-qua/che-thong-tin.py danh-gia-tuan.csv chay/danh-gia.csv
```

Lệnh thay số điện thoại bằng `[SĐT]`, email bằng `[EMAIL]`, link bằng `[LINK]`, ghi file mới vào `chay/`.

```ketqua
đã che 2 chỗ trong 250 dòng
```

!!! see "Bạn sẽ thấy"
    Trên bộ giả: "đã che 2 chỗ trong 250 dòng" (số điện thoại và link trong hai bài spam). Script **không** che tên người hay địa chỉ viết tự do: bạn lướt cột `noi_dung`, xóa cụm có tên. Chưa thử `python3` trên macOS/Linux.

### Bước 2. Giao việc cho agent

Mở agent trong thư mục `chay` (cách mở: [Bắt đầu với coding agent](../th-bat-dau-voi-coding-agent/00-README.md)) và dán đúng prompt ở bài 1 (`du-lieu/prompt-giao-viec.txt`). **Giữ nguyên prompt** để so tuần này với tuần trước. Cách chạy một lệnh không cần ngồi canh nằm ở mục Đào sâu của bài 1.

**Chi phí và thời gian:** log `claude-lan1` ghi chi phí do công cụ báo 1,35 USD cho một lần chạy 250 bài **[Đo được, n=1]**; log `agy-lan2` chỉ có lượng token (231.920 vào, 95.014 ra), không có giá tiền. Giá thay đổi theo gói và thời điểm, hãy xem trên tài khoản của bạn. Nếu đặt giới hạn thời gian, đặt dư: chúng tôi mất báo cáo ở lần `agy` bị dừng ở 900 giây.

### Bước 3. Máy tự kiểm (không cần đáp án)

```lenh
python -X utf8 ket-qua\kiem-tra-dau-ra.py chay chay\dau-ra
```

(macOS, Linux: `python3 -X utf8 ket-qua/kiem-tra-dau-ra.py chay chay/dau-ra`.) Lệnh đối chiếu `chay/dau-ra/*` với `chay/danh-gia.csv` và in "QUA" hoặc "CÓ n LỖI". Nó kiểm file và cột, giá trị hợp lệ, trích dẫn nguyên văn, bài chưa loại đều có ý kiến, bảng tuần khớp đếm lại, báo cáo đúng 5 mục. Cuối cùng in danh sách bài `CAN_NGUOI_DOC` để người đọc.

!!! see "Bạn sẽ thấy"
    Dòng cuối "KẾT QUẢ: QUA". Chúng tôi chạy lệnh này trên bản sao có `chay/danh-gia.csv` đã che và `dau-ra` của `claude-lan1`: ra "QUA", 16 bài cần người đọc **[Đo được]**. Báo "CÓ n LỖI" thì **không dùng kết quả**: chạy lại hoặc sửa tay. Ở bài 2, lần thiếu báo cáo bị báo đúng "CÓ 1 LỖI".

### Bước 4. Cảnh báo tuần (đếm bằng code)

```lenh
python -X utf8 ket-qua\canh-bao-tuan.py chay\dau-ra\xu-huong-tuan.csv 2026-10-05
```

Lệnh so số ý tiêu cực của tuần được chọn (bỏ trống thì lấy tuần mới nhất) với trung bình 4 tuần trước, theo từng chủ đề. Chủ đề nào từ 3 ý trở lên và gấp 2 lần trở lên thì in "CẢNH BÁO". Ngưỡng 2 lần và 3 ý là **[Đề xuất]** tùy ý, chỉnh theo lượng đánh giá của quán.

```ketqua
Tuần xét: 2026-10-05 | so với 4 tuần trước: 2026-09-07 .. 2026-09-28
  chat_luong  tiêu cực tuần này  4 | TB các tuần trước  2.2 
  gia         tiêu cực tuần này  8 | TB các tuần trước  2.2 <-- CẢNH BÁO
  giao_hang   tiêu cực tuần này  5 | TB các tuần trước  0.8 <-- CẢNH BÁO
  khong_gian  tiêu cực tuần này  2 | TB các tuần trước  1.8 
  phuc_vu     tiêu cực tuần này  2 | TB các tuần trước  4.2 
  ve_sinh     tiêu cực tuần này  3 | TB các tuần trước  0.8 <-- CẢNH BÁO
Số cảnh báo: 3
```

!!! see "Bạn sẽ thấy"
    Ba cảnh báo: giá, giao hàng, vệ sinh, đúng ba xu hướng đã cài **[Đo được]**. Mỗi tuần chỉ có vài ý đến vài chục ý, nên đây là dấu hiệu để theo dõi, chưa phải kết luận. Chạy không đối số (tuần mới nhất 09/11) ra 2 cảnh báo là phục vụ và vệ sinh, với 3 và 4 ý.

### Bước 5. Người duyệt, rồi mới hành động

Đọc theo thứ tự: (a) `nguy-cap.csv` từng dòng, kể cả dòng "nghi"; (b) danh sách `CAN_NGUOI_DOC`; (c) 5 việc trong `bao-cao.md`.

- **Nguy cấp (ngộ độc, thái độ, lừa đảo):** **[Đề xuất]** một người cụ thể đọc trong ngày làm việc, và quyết định có liên hệ khách hay kiểm tra thực phẩm/ca làm việc không. Agent chỉ nói "bài này nghi ngộ độc", không biết sự thật. Báo cáo `claude` cũng tự ghi: "Không kết luận được nguyên nhân các ca đau bụng, nôn. File chỉ có lời kể của khách".
- **`CAN_NGUOI_DOC`:** người đọc gán nhãn thật cho từng bài (thường 15 đến 23 bài trên 250). Bài mỉa mai gán `tieu_cuc` cho đúng chủ đề.
- **5 việc nên sửa:** chủ quán quyết việc nào làm, ai làm, hạn nào. Kiểm lại từng trích dẫn bằng cách tìm mã `R..` trong file gốc. Bộ kiểm bảo đảm trích dẫn có thật; **chưa** bảo đảm nó chọn đúng bằng chứng quan trọng.
- **Nhân sự:** các bài kể thái độ nhân viên có thể nhắc người cụ thể. Agent không xác minh được. Đừng xử lý kỷ luật chỉ từ đánh giá; cần xem ca làm việc, camera (nếu có), nghe nhân viên. Quy định lao động cụ thể hỏi chuyên gia.

### Bước 6. Lưu lại

Lưu cả thư mục `chay` theo tuần, kèm prompt đã dùng và phiên bản agent, để lần sau mở lại so sánh.

```lenh
Copy-Item chay luu-tru\2026-11-16 -Recurse
```

(macOS, Linux: `mkdir -p luu-tru && cp -r chay luu-tru/2026-11-16`.) Lệnh chép `chay` sang `luu-tru\2026-11-16` (tự tạo `luu-tru` nếu chưa có). Mỗi tuần dùng một thư mục `chay` mới: file cũ lẫn vào kết quả mới là lỗi hay gặp.

## Prompt dùng khi có thay đổi

Cả hai prompt dưới đây là **mới, chưa chạy lại** cho bài này. Thay phần trong dấu `<...>`. Prompt thêm chủ đề mới đã chạy thử ở bài 4.

Khi định dạng file thay đổi (ví dụ thêm cột, đổi kiểu ngày):

```prompt
Tuần này file danh-gia.csv có thay đổi so với các tuần trước: <mô tả, ví dụ: thêm cột chi_nhanh; ngày đổi sang dạng DD-MM-YYYY>.
Giữ nguyên mọi quy tắc, tên cột và định dạng ra như prompt gốc. Chỉ sửa phần đọc dữ liệu cho đúng định dạng mới.
Trước khi xử lý cả file, in ra 5 dòng đầu sau khi chuẩn hóa (mã, ngày, sao) để kiểm. Nếu có ngày nào không đọc được, liệt kê mã của các dòng đó và dừng, không đoán.
Mọi con số vẫn do code đếm. Chỉ đọc và ghi trong thư mục hiện tại.
```

Khi thêm quy tắc mới cho nguy cấp (ví dụ một loại mới):

```prompt
Thêm một loại nguy cấp mới vào nguy-cap.csv: di_ung, khi khách nói bị dị ứng, nổi mẩn, khó thở sau khi dùng món của quán.
Giữ nguyên ba loại cũ (ngo_doc, thai_do, lua_dao) và quy tắc "nghi ở đầu ly_do nếu chưa chắc".
Chạy lại toàn bộ và báo: bao nhiêu dòng nguy cấp mới thuộc loại di_ung, bao nhiêu dòng cũ đổi loại sang di_ung. Dòng nào đổi loại phải nêu lý do một câu.
Cập nhật bộ kiểm trích dẫn cho đủ file. Chỉ đọc và ghi trong thư mục hiện tại.
```

## Đo agent với dữ liệu của quán bạn

Dữ liệu giả có cấu trúc lặp nên kết quả gần tuyệt đối. Trên đánh giá thật, khách viết dài, lẫn tên món, lẫn chuyện cá nhân, kết quả có thể kém hơn nhiều; chúng tôi chưa đo. Cách đo **[Đề xuất]**:

1. Chọn 50 bài ngẫu nhiên từ dữ liệu thật (đủ loại: dài, ngắn, không dấu, chê, khen).
2. Tự gán nhãn tay vào `bo-vang.csv`, cột `ma, chu_de, sac_thai` (mỗi ý một dòng; bài bạn thấy mỉa mai ghi `CAN_NGUOI_DOC`). Mất khoảng một buổi chiều.
3. Chấm:

```lenh
python -X utf8 ket-qua\cham-bo-vang.py chay\dau-ra\y-kien.csv bo-vang.csv
```

Script in số cặp (bài, chủ đề) agent tìm đủ, sót, thừa, độ khớp sắc thái, và danh sách bài lệch. Chúng tôi từng thử script bằng "bộ vàng" dựng từ đáp án của 50 bài đầu bộ giả: `claude-lan1` tìm đủ 84/85, sót 1 (R050), khớp sắc thái 84/84; `agy-lan2` tìm đủ 85/85, khớp 85/85 **[Đo được]**. Đó chỉ là thử script chạy được, vì bộ vàng lấy từ đáp án nên không phải đo trên dữ liệu thật.

4. Đặt ngưỡng chấp nhận **trước khi** nhìn kết quả (ví dụ dưới 90% khớp sắc thái thì mọi con số chỉ để tham khảo và phải duyệt toàn bộ bằng tay). Ngưỡng này là **[Đề xuất]**.
5. Làm lại với 50 bài mới mỗi vài tháng, hoặc khi đổi prompt, đổi agent, đổi loại quán.

Nếu chạy cùng dữ liệu hai lần mà số lệch nhau đáng kể thì đó là dấu hiệu quan trọng: ở bài 2 hai lần chạy `claude` cho tổng số ý kiến 400 và 404, các lần `agy` cho 413, 399 và 402 **[Đo được]**. Cách tách ý khác nhau làm số tuyệt đối khác nhau.

## Đào sâu: phân vai, lỗi hằng tuần và mở rộng

### Phân vai

| Việc | Ai | Khi nào **[Đề xuất]** |
|---|---|---|
| Chạy quy trình, lưu thư mục tuần | Nhân viên văn phòng hoặc chủ quán | Sáng thứ Hai |
| Đọc `nguy-cap.csv` | Chủ quán hoặc quản lý ca | Cùng ngày |
| Đọc `CAN_NGUOI_DOC` | Người biết giọng khách quen (thu ngân lâu năm cũng được) | Trong tuần |
| Chốt 5 việc | Chủ quán | Họp 15 phút |
| Đo agent bằng 50 bài vàng | Người thạo nghiệp vụ | Mỗi quý, hoặc khi đổi prompt |

### Mở rộng (chưa thử)

- **Nhiều chi nhánh:** thêm cột `chi_nhanh` vào CSV và bảng đếm, chia xu hướng theo chi nhánh. Cần sửa prompt và `tong-hop.py`.
- **Thêm chủ đề riêng của quán** (ví dụ "chỗ để xe", "đóng gói"): thêm vào danh sách `chu_de` trong prompt và cập nhật biến `TOPICS` trong `kiem-tra-dau-ra.py`. Bài 4 có bài tập về việc này.
- **Soạn nháp phản hồi cho khách:** thêm bước 9 vào prompt, đầu ra phải ghi "NHÁP, chờ người duyệt".
- **Chạy theo lịch** (Task Scheduler, cron): khi không có người canh, bộ kiểm và việc gửi báo cáo cho người đọc là bắt buộc. Chúng tôi chưa thử chạy lịch.
- **Thử agent khác hoặc bản mới:** chạy lại 50 bài vàng trước khi tin.

## Lỗi thường gặp khi dùng hằng tuần

| Triệu chứng | Cách xử lý |
|---|---|
| `che-thong-tin.py` báo `FileNotFoundError` | Chưa tạo thư mục `chay`: chạy `mkdir chay` trước |
| Agent đổi định dạng cột giữa các tuần | Giữ prompt cố định, lưu vào kho cùng kết quả |
| Quên che số điện thoại | Chạy `che-thong-tin.py` mỗi tuần và lướt cột nội dung tìm tên người |
| Tin số đếm của một tuần quá ít ý | Nhìn xu hướng 4 tuần trở lên, xem trích dẫn cụ thể |
| Báo cáo bị cụt khi hết giờ | Bộ kiểm báo "thiếu bao-cao.md"; chạy lại với giới hạn dài hơn |
| Cho agent tự đăng phản hồi công khai | Đừng; người duyệt và đăng |
| Dùng một thư mục cho nhiều tuần | Mỗi tuần một thư mục |
| Tin vào mỗi con số sao | Bài mỉa mai thường kèm 4 đến 5 sao. Trong bộ giả, "5 sao cho sự đều đặn: lần nào cũng quên order của mình" mang 5 sao nhưng là chê |

## Checklist cuối bài 3

- [ ] Che số điện thoại, email, link; lướt tìm tên người.
- [ ] Mỗi tuần một thư mục `chay`, lưu cả prompt và phiên bản agent.
- [ ] `kiem-tra-dau-ra.py` báo "QUA" mới được dùng.
- [ ] `canh-bao-tuan.py` chạy xong, xem trích dẫn của chủ đề bị cảnh báo.
- [ ] Người đọc `nguy-cap.csv` và `CAN_NGUOI_DOC`, ghi lại quyết định.
- [ ] Mỗi quý đo lại bằng 50 bài vàng.

## Việc cần người làm

- Chọn người chịu trách nhiệm đọc nguy cấp mỗi tuần, có thẩm quyền liên hệ khách và kiểm tra bếp.
- Tự gán nhãn 50 bài vàng cho quán của bạn.
- Quyết định đăng và phản hồi công khai; quyết định xử lý nhân sự sau khi xác minh.
- Hỏi luật sư về việc xử lý dữ liệu khách trong đánh giá (che thông tin, lưu trữ, dùng dịch vụ đám mây).

## Giới hạn

- **Chưa kiểm trên dữ liệu thật.** Mọi số đo là trên 250 đánh giá giả, phần lớn ghép từ mệnh đề lặp, **dễ hơn đánh giá thật**; agent có thể làm kém hơn trên đánh giá thật.
- **n nhỏ:** claude 2 lần hoàn chỉnh, agy 2 lần hoàn chỉnh; chi phí 1,35 USD chỉ là một lần chạy.
- **Ngưỡng cảnh báo, thời hạn người duyệt, ngưỡng 90% đều là [Đề xuất]**, không có số liệu nền.
- **`che-thong-tin.py` chỉ che mẫu có hình dạng rõ**, không che được tên, địa chỉ viết tự do.
- **Agent chạy với quyền rộng** (đặc biệt `agy` với `--dangerously-skip-permissions`) và có thể ghi ra ngoài thư mục. Dùng máy hoặc tài khoản riêng khi có dữ liệu thật.
- Chưa thử các lệnh macOS, Linux trong bài này; chưa thử chạy theo lịch. Chúng tôi không kết luận agent nào tốt hơn.
