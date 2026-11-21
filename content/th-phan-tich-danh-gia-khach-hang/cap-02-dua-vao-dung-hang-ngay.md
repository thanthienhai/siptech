# Bài 3: Đưa vào dùng hằng ngày: lặp lại, tự kiểm, người duyệt, giới hạn, mở rộng

> Ví dụ dùng **dữ liệu giả để học** (quán "Mây Lưng Chừng" hư cấu). Nhãn: **[Đo được]** = kết quả chạy của chúng tôi ngày 2026-11-20; **[Nguồn]** = có link; **[Đề xuất]** = ý kiến, chưa kiểm trên quán thật.

## Mục tiêu đo được

Biến thí nghiệm ở bài 2 thành một thói quen mỗi tuần mất không quá một buổi sáng, trong đó: (1) máy làm phần đọc, đếm, kiểm trích dẫn; (2) người làm phần quyết định: bài `CAN_NGUOI_DOC`, bài nguy cấp, 5 việc nên sửa; (3) có cách đo xem agent làm đúng đến đâu với **dữ liệu của quán bạn** chứ không phải dữ liệu giả này. Tiêu chí hoàn thành: bạn chạy được ba lệnh ở mục 2 liên tiếp trên một thư mục mới và đọc được báo cáo "QUA/CÓ LỖI" cuối cùng.

## 1. Nhìn lại: máy làm được gì, người phải làm gì

Từ bài 2 [Đo được]: trên bộ dữ liệu giả, cả hai agent đều xếp đủ 14/14 bài mỉa mai vào `CAN_NGUOI_DOC`, bắt 16/16 bài nguy cấp, và không có trích dẫn nào sai nguyên văn trong hơn 400 dòng. Nhưng cũng từ bài 2: một số ca "đúng hay sai" phụ thuộc người quyết (R191 spam hay ý kiến thật; "ổn" là tích cực hay trung tính), mỗi lần chạy có 15 đến 23 bài cần người đọc, và agent có thể bỏ một báo cáo khi hết giờ. Nên thói quen dùng hằng tuần phải có đủ ba lớp: **máy kiểm**, **người duyệt**, **lưu lại để so sánh**.

## 2. Quy trình hằng tuần (khoảng 5 bước)

Giả sử mỗi sáng thứ Hai bạn có file `danh-gia-tuan.csv` gồm các đánh giá mới và cũ trong 12 tuần gần nhất (đủ để thấy xu hướng). Cách xuất đánh giá từ Google Maps, Shopee Food, fanpage tùy từng nền tảng (chúng tôi chưa kiểm cách xuất của từng nơi, bạn có thể phải chép tay vào bảng tính). Cột bắt buộc: `ma, nen_tang, ngay, sao, noi_dung`.

### Bước 1. Che thông tin cá nhân

Đánh giá thật thường có số điện thoại, đôi khi có email hoặc link. Chạy script `ket-qua/che-thong-tin.py` (đã thử trên 250 dòng của bộ giả: che 2 chỗ là số điện thoại và link trong hai bài spam):

```bash
python -X utf8 che-thong-tin.py danh-gia-tuan.csv chay/danh-gia.csv
```

Giải thích: lệnh đọc file vào, thay số điện thoại bằng `[SĐT]`, email bằng `[EMAIL]`, link bằng `[LINK]`, rồi ghi file mới vào thư mục `chay/` (thư mục riêng cho lần chạy này). Script **không** che tên người hay địa chỉ viết tự do: bạn cần lướt qua cột `noi_dung`, hoặc xóa các cụm có tên. Còn việc đưa dữ liệu khách cho dịch vụ đám mây có phải xin phép hay thông báo không, **cần hỏi luật sư**; chúng tôi không viết điều khoản cụ thể ở đây.

### Bước 2. Giao việc cho agent

Dùng đúng prompt `ket-qua/prompt-giao-viec.txt` (giữ nguyên để so sánh tuần này với tuần trước). Trong PowerShell hoặc Git Bash, đứng trong thư mục `chay/`:

```bash
claude -p "$(cat ../prompt-giao-viec.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash"
```

Giải thích: `-p` chạy một lần rồi thoát; hai cờ cuối cho phép agent ghi file và chạy lệnh Python trong thư mục này. Đây là lệnh tương đương với lệnh `agent_run.py` bọc mà chúng tôi dùng (chúng tôi chạy qua `agent_run.py` để có log). Với `agy` thay bằng `agy -p "$(cat ../prompt-giao-viec.txt)" --dangerously-skip-permissions`, nhớ rằng cờ này cho agent toàn quyền trên máy. Dự trù thời gian: trong bài 2, `claude` mất 454,5 giây và `agy` mất 957,9 giây cho 250 bài [Đo được, một lần chạy mỗi loại có log]. Nếu bạn đặt giới hạn thời gian, đặt dư (chúng tôi mất báo cáo ở lần `agy` bị dừng ở 900 giây).

**Chi phí**: log `claude-lan1` ghi chi phí do công cụ báo là 1,35 USD cho một lần chạy 250 bài [Đo được, n=1]; log `agy-lan2` chỉ ghi lượng token (231.920 vào, 95.014 ra), không có giá tiền. Giá thay đổi theo gói và thời điểm, hãy tự xem trên tài khoản của bạn.

### Bước 3. Máy tự kiểm (không cần đáp án)

```bash
python -X utf8 kiem-tra-dau-ra.py chay chay/dau-ra
```

Giải thích: đối chiếu `chay/dau-ra/*` với `chay/danh-gia.csv` và in "QUA" hoặc "CÓ n LỖI". Nó kiểm file và cột, giá trị `chu_de`/`sac_thai`/`loai` hợp lệ, mọi trích dẫn nguyên văn, mọi bài chưa loại bỏ đều có ý kiến, bảng tuần khớp đếm lại, báo cáo đúng 5 mục mỗi mục 2 đến 3 trích dẫn. Cuối cùng in danh sách bài `CAN_NGUOI_DOC` kèm nội dung để người đọc. Kết quả [Đo được] ở bài 2: 4 trong 5 lần chạy "QUA", lần thiếu báo cáo bị báo "CÓ 1 LỖI"; khi chúng tôi cố ý sửa hỏng một trích dẫn và một số trong bảng tuần, bộ kiểm báo đúng hai lỗi. Nếu báo lỗi, **không dùng kết quả**: chạy lại hoặc mở file ra sửa tay.

### Bước 4. Cảnh báo tuần (đếm bằng code)

```bash
python -X utf8 canh-bao-tuan.py chay/dau-ra/xu-huong-tuan.csv
```

Giải thích: so số ý tiêu cực của tuần mới nhất với trung bình 4 tuần trước theo từng chủ đề; chủ đề nào từ 3 ý trở lên và gấp 2 lần trở lên thì in "CẢNH BÁO". Ngưỡng 2 lần và 3 ý là **[Đề xuất]** tùy ý, bạn chỉnh theo lượng đánh giá của quán. Trên dữ liệu giả, xét tuần 05/10 (so với 4 tuần trước) script cảnh báo 3 chủ đề [Đo được]: giá (8 ý so với trung bình 2,2), giao hàng (5 so với 0,8), vệ sinh (3 so với 0,8), đúng ba xu hướng đã cài. Mỗi tuần chỉ có vài ý đến vài chục ý, nên đây là dấu hiệu để theo dõi, chưa phải kết luận.

### Bước 5. Người duyệt, rồi mới hành động

Người duyệt đọc theo thứ tự: (a) `nguy-cap.csv` từng dòng, kể cả dòng "nghi"; (b) danh sách `CAN_NGUOI_DOC`; (c) 5 việc trong `bao-cao.md`. Cụ thể:

- **Nguy cấp (ngộ độc, thái độ, lừa đảo):** [Đề xuất] một người cụ thể đọc trong ngày làm việc, và quyết định có liên hệ khách hay kiểm tra thực phẩm/ca làm việc hay không. Agent chỉ nói "bài này nghi ngộ độc", không biết sự thật. Báo cáo của `claude` cũng tự ghi: "Không kết luận được nguyên nhân các ca đau bụng, nôn. File chỉ có lời kể của khách".
- **`CAN_NGUOI_DOC`:** người đọc gán nhãn thật cho từng bài (thường 15 đến 23 bài trên 250, [Đo được] ở bài 2). Với bài mỉa mai, gán `tieu_cuc` cho đúng chủ đề.
- **5 việc nên sửa:** người quyết định việc nào làm, ai làm, hạn nào. Kiểm lại từng trích dẫn: bấm tìm mã `R..` trong file gốc. Bộ kiểm đã bảo đảm trích dẫn có thật; **chưa** bảo đảm nó chọn đúng bằng chứng quan trọng.
- Nếu muốn trả lời công khai trên Google Maps/Shopee, nhờ agent soạn **nháp** nhưng **người đăng**, không để agent tự đăng.

Sau khi duyệt, lưu cả thư mục `chay/` vào kho theo tuần (ví dụ `luu-tru/2026-11-16/`) cùng prompt dùng và phiên bản agent. Lần sau mở lại để so sánh.

## 3. Đo agent với dữ liệu của quán bạn (đừng tin bảng ở bài 2)

Điểm cần nhớ từ bài 2: dữ liệu giả có cấu trúc lặp, nên kết quả gần tuyệt đối. Trên đánh giá thật, nơi khách viết dài, lẫn tên món, lẫn chuyện cá nhân, kết quả có thể kém hơn nhiều; chúng tôi chưa đo.

Cách đo đơn giản [Đề xuất]:

1. Chọn 50 bài ngẫu nhiên từ dữ liệu thật của bạn (để nhiều loại: dài, ngắn, không dấu, có chê, có khen).
2. Tự gán nhãn tay vào `bo-vang.csv` với cột `ma, chu_de, sac_thai` (mỗi ý một dòng; bài bạn thấy mỉa mai ghi `CAN_NGUOI_DOC`). Mất khoảng một buổi chiều.
3. Chạy:

```bash
python -X utf8 cham-bo-vang.py chay/dau-ra/y-kien.csv bo-vang.csv
```

Script in số cặp (bài, chủ đề) agent tìm đủ, sót, thừa, độ khớp sắc thái và danh sách bài lệch. Chúng tôi đã thử script này bằng cách dựng một "bộ vàng" từ đáp án của bộ giả cho 50 bài đầu: với `claude-lan1` ra tìm đủ 84/85, sót 1 (R050), khớp sắc thái 84/84; với `agy-lan2` tìm đủ 85/85, khớp 85/85 [Đo được]. Lưu ý đây chỉ là thử script chạy được, vì bộ vàng lấy từ đáp án nên không phải đo trên dữ liệu thật.

4. Đặt ngưỡng chấp nhận trước khi nhìn kết quả (ví dụ: dưới 90% khớp sắc thái thì mọi con số chỉ để tham khảo và phải duyệt toàn bộ bằng tay). Ngưỡng này là **[Đề xuất]**, chọn theo mức rủi ro của bạn.
5. Làm lại với 50 bài mới mỗi vài tháng, hoặc khi bạn đổi prompt, đổi agent, đổi loại quán.

Vì số lần chạy ít, nếu bạn chạy cùng dữ liệu hai lần mà số lệch nhau đáng kể thì đó là một dấu hiệu quan trọng: ở bài 2 hai lần chạy `claude` cho tổng số ý kiến 400 và 404, các lần `agy` cho 413, 399 và 402 [Đo được]. Cách tách ý khác nhau làm số tuyệt đối khác nhau.

## 4. Người duyệt và phân vai

| Việc | Ai | Khi nào ([Đề xuất]) |
|---|---|---|
| Chạy quy trình, lưu thư mục tuần | Nhân viên văn phòng / chủ quán | Sáng thứ Hai |
| Đọc `nguy-cap.csv` | Chủ quán hoặc quản lý ca | Cùng ngày |
| Đọc `CAN_NGUOI_DOC` | Người biết giọng khách quen (thu ngân lâu năm cũng được) | Trong tuần |
| Chốt 5 việc | Chủ quán | Họp 15 phút |
| Kiểm đo agent bằng 50 bài vàng | Người thạo nghiệp vụ | Mỗi quý, hoặc khi đổi prompt |

Lưu ý nhạy cảm về nhân sự: các bài kể thái độ nhân viên có thể nhắc người cụ thể (trong dữ liệu giả, ví dụ "bạn thu ngân", "quản lý đứng quầy"). Agent không xác minh được. Đừng xử lý kỷ luật chỉ từ đánh giá; cần xem ca làm việc, camera (nếu có), nghe nhân viên. Quy định lao động cụ thể cần hỏi chuyên gia.

## 5. Lỗi thường gặp khi dùng hằng tuần

1. **Agent đổi định dạng cột giữa các tuần** nếu bạn sửa prompt. Giữ prompt cố định và đưa vào kho cùng kết quả.
2. **Quên che số điện thoại** trước khi chạy. Chạy `che-thong-tin.py` mỗi tuần và lướt cột nội dung tìm tên người.
3. **Tin số đếm một tuần quá ít ý.** Nhìn xu hướng 4 tuần trở lên, và xem trích dẫn cụ thể.
4. **Báo cáo bị cụt khi hết giờ.** Bộ kiểm phát hiện "thiếu bao-cao.md"; chạy lại với giới hạn dài hơn.
5. **Cho agent tự đăng phản hồi công khai.** Đừng; người duyệt và đăng.
6. **Dùng cùng một thư mục cho nhiều tuần.** File cũ lẫn vào kết quả mới. Mỗi tuần một thư mục.
7. **Tin vào mỗi con số sao.** Bài viết mỉa mai thường kèm 4 đến 5 sao; trong dữ liệu giả có bài "5 sao cho sự đều đặn: lần nào cũng quên order của mình" mang 5 sao nhưng là chê.

## 6. Mở rộng

- **Nhiều chi nhánh:** thêm cột `chi_nhanh` vào CSV và vào bảng đếm; chia xu hướng theo chi nhánh. Cần sửa prompt và `tong-hop.py`, chưa thử.
- **Thêm chủ đề riêng của quán** (ví dụ "chỗ để xe", "trẻ em"): thêm vào danh sách `chu_de` trong prompt và cập nhật `kiem-tra-dau-ra.py` (biến `TOPICS`).
- **Soạn nháp phản hồi cho khách:** thêm bước 9 vào prompt, nhưng nhãn đầu ra phải ghi "NHÁP, chờ người duyệt".
- **Chạy theo lịch** (Task Scheduler của Windows, cron): có thể, nhưng khi đó không có người canh nên bước 3 (bộ kiểm) và gửi báo cáo cho người đọc là bắt buộc. Chúng tôi chưa thử chạy lịch.
- **Thử agent khác hoặc bản mới:** chạy lại 50 bài vàng trước khi tin; không suy từ bài này.

## Checklist

- [ ] Che số điện thoại/email/link; lướt tên người.
- [ ] Mỗi tuần một thư mục `chay/`, lưu cả prompt và phiên bản agent.
- [ ] `kiem-tra-dau-ra.py` báo "QUA" mới được dùng.
- [ ] `canh-bao-tuan.py` chạy xong, xem trích dẫn của chủ đề bị cảnh báo.
- [ ] Người đọc `nguy-cap.csv` và `CAN_NGUOI_DOC`; ghi lại quyết định.
- [ ] Mỗi quý đo lại bằng 50 bài vàng.

## Việc cần người làm

- Chọn người chịu trách nhiệm đọc nguy cấp mỗi tuần và có thẩm quyền liên hệ khách/kiểm tra bếp.
- Tự gán nhãn 50 bài vàng cho quán bạn.
- Quyết định đăng/phản hồi công khai; quyết định xử lý nhân sự sau khi xác minh.
- Hỏi luật sư về việc xử lý dữ liệu khách trong đánh giá (che thông tin, lưu trữ, dùng dịch vụ đám mây).

## Giới hạn

- **Chưa kiểm trên dữ liệu thật.** Tất cả số đo là trên 250 đánh giá giả, phần lớn ghép từ mệnh đề lặp; agent có thể làm kém hơn trên đánh giá thật.
- **n nhỏ:** claude 2 lần hoàn chỉnh, agy 2 lần hoàn chỉnh; chi phí 1,35 USD chỉ là một lần chạy.
- **Ngưỡng cảnh báo, thời hạn người duyệt, ngưỡng 90% đều là [Đề xuất]**, không có số liệu nền.
- **`che-thong-tin.py` chỉ che mẫu có hình dạng rõ**, không che được tên, địa chỉ viết tự do.
- **Agent chạy với quyền rộng** (đặc biệt `agy` với `--dangerously-skip-permissions`) và có thể ghi ra ngoài thư mục (đã thấy `claude` tạo file tạm ở thư mục của công cụ). Dùng máy hoặc tài khoản riêng khi có dữ liệu thật.
- Chúng tôi không kết luận agent nào tốt hơn.
