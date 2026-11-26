# Bài toán 05: Lập báo giá từ email và tin nhắn yêu cầu của khách

> **Dữ liệu giả để học.** Công ty "An Phát Demo", khách hàng, địa chỉ, số điện thoại (dãy 0900 000 xxx), email (@example.com) đều bịa. Bảng giá, chính sách, điều kiện giao hàng do chúng tôi viết để làm bài, không phải của doanh nghiệp thật. Toàn bộ sinh bằng `du-lieu/sinh_du_lieu.py` (hạt giống cố định 20261120, chạy lại ra y hệt).

## Bạn làm được gì sau bài toán này

Một công ty nhỏ bán thiết bị văn phòng, mực in, giấy và văn phòng phẩm nhận yêu cầu báo giá qua email và Zalo mỗi ngày. Việc mất thời gian không nằm ở phép tính mà ở những thứ lộn xộn quanh nó: đơn vị lẫn lộn, mã hàng sai, bậc giá theo số lượng, chiết khấu có thẩm quyền, khách đòi giao đúng giờ hay đòi nợ mà nhân viên không được hứa.

Sau bốn bài, bạn có thể:

- giao cho một coding agent (Claude Code, Antigravity) đọc 12 yêu cầu lộn xộn, lập 12 báo giá nháp theo mẫu, 12 email trả lời nháp và danh sách câu hỏi cần hỏi lại khách, rồi **dừng ở chỗ phải có người quyết**;
- chấm kết quả bằng code (có đáp án) và tự kiểm bằng code (không cần đáp án), thay vì tin vào lời "đã xong" của agent;
- đặt đúng hàng rào cho dữ liệu và đáp án, vì có một lần agent đã đi mở file đáp án ngoài thư mục làm việc;
- dùng bộ prompt mẫu và ba bài tập (thêm bậc giá, xin chiết khấu quá mức, đổi điều kiện miễn phí giao hàng) để áp vào công việc của bạn.

Phép tính tiền do code làm; người thật duyệt trước khi gửi. VAT là **tham số** để kế toán điền, bài không khẳng định thuế suất.

## Bốn bài

| Bài | Nội dung | Mất bao lâu | Kết quả |
|---|---|---|---|
| [Bài 1](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | Chuẩn bị dữ liệu, thư mục riêng, dán prompt giao việc | khoảng 25 phút (+ agent chạy 6 đến 16 phút) | 12 báo giá nháp, 12 email nháp, 12 danh sách câu hỏi, script tính tiền |
| [Bài 2](cap-01-chay-that-va-cham-bang-dap-an.md) | Chấm bằng `cham.py`, đọc ca sai, sửa đáp án, tìm dấu vết agent ra ngoài thư mục | khoảng 40 phút | Bảng điểm 6 lần chạy, hiểu "tính đúng" chưa chắc "đúng chính sách" |
| [Bài 3](cap-02-dua-vao-dung-hang-ngay.md) | Quy trình mỗi ngày, tự kiểm không cần đáp án, checklist người duyệt | khoảng 30 phút | Quy trình không có gì tự gửi, hàng đợi duyệt theo trạng thái |
| [Bài 4](cap-03-prompt-mau-va-bai-tap.md) | 9 prompt dùng lại (5 đã chạy thật), 3 bài tập có bộ chấm, dùng dữ liệu thật | khoảng 1,5 đến 3 giờ | Bộ prompt của riêng bạn, ba bài tập chấm bằng code |

## Kết quả đo tóm tắt

**[Đo được]** Ngày 2026-11-20. 12 yêu cầu, 35 dòng hàng trong đáp án, mỗi lần chạy 36 file. n = 5 lần chạy hợp lệ (claude 3, agy 2), chưa đo được độ ổn định, không xếp hạng agent.

| Lần chạy | Log gốc | Dòng hàng đúng | Dòng bịa có giá | Đúng cả 6 dòng tổng | Trạng thái khớp đáp án |
|---|---|---|---|---|---|
| claude-1 | có | 35/35 | 0 | 12/12 | 10/12 |
| claude-2 (thư mục cô lập) | có | 35/35 | 0 | 12/12 | 12/12 |
| claude-0 | **mất** | 35/35 | 0 | 12/12 | 11/12 |
| agy-2 (thư mục cô lập) | có | 35/35 | 0 | 12/12 | 10/12 |
| agy-0 | **mất** | 35/35 | 0 | 8/12 | 8/12 |
| agy-1 | có | **loại**: agent đã mở file đáp án và file chấm ngoài thư mục | | | |

Điều rút ra (chỉ mô tả quan sát):

- Phép tính tiền đúng gần như tuyệt đối khi bắt buộc agent viết script tính: 35/35 dòng hàng trong mọi lần chạy hợp lệ. Lỗi tiền duy nhất đáng kể là agy-0 ở R10: bỏ phần chiết khấu thêm 2% do hiểu sai chính sách.
- Chỗ agent hay khác đáp án là ranh giới "thiếu thông tin" và "cần người quyết", không phải số học. Ở ca R02 chúng tôi **phải sửa đáp án** sau khi thấy kết quả (bài 2).
- Ba trong năm lần chạy hợp lệ (claude-1, agy-2, agy-0) viết trong email nháp những câu kiểu "đã chuyển lên trưởng phòng xem xét" trong khi chưa ai làm.
- Một lần chạy (agy-1) đã đọc file đáp án và chạy chương trình chấm trên kết quả của agent khác dù prompt dặn "chỉ đọc và ghi trong thư mục hiện tại": bài học về hàng rào thật.
- Bài 4 **[Đo được]**, ngày 2026-11-21, n = 1 mỗi prompt, Claude Code: 5 prompt (giải thích script, kiểm chéo, email không hứa ngày giao, câu hỏi làm rõ, báo cáo cho sếp) đã chạy thật, 54 đến 197 giây, 0,20 đến 0,64 USD theo giá niêm yết. Kiểm bằng code: email không hứa giờ giao; báo cáo cho sếp khớp 12/12 tổng cộng với đáp án; kiểm chéo ra 7 khớp, 0 lệch, 5 "không kết luận được" (quá thận trọng).

## Thư mục

```
00-README.md
bai-1-...md  bai-2-...md  bai-3-...md  bai-4-...md
du-lieu/        dữ liệu giao cho agent + prompt-giao-viec.txt + sinh_du_lieu.py (chứa đáp án: đừng chép vào thư mục agent)
                bai-tap/bt1, bt2, bt3: đầu vào ba bài tập (không có đáp án)
ket-qua/        dap-an.json, cham.py, kiem-tra-bao-gia.py, bao-cao-cham.json, prompt-giao-viec.txt,
                claude-1, claude-2, claude-0, agy-2, agy-0 (mỗi thư mục có dau-ra/ và tinh_bao_gia.py),
                agy-1-NHIEM-DAP-AN (giữ để minh bạch, không tính điểm),
                dap-an-v1-chua-sua.json và bao-cao-cham-v1-dap-an-chua-sua.json (bản chấm trước khi sửa đáp án),
                bai-tap/  sinh_bai_tap.py, cham_bai_tap.py, dap-an-bt1..bt3.json (đáp án bài tập, để ngoài tầm agent)
logs/           *.raw.jsonl (log gốc) và *.json (transcript chuẩn hóa): claude-1, claude-2, agy-1, agy-2, bai4-*
anh/            ảnh dùng trong bài (ảnh terminal dựng lại từ log, đã che đường dẫn máy và tên tổ chức)
```

## Việc cần người làm

- Người duyệt (chủ doanh nghiệp, kế toán, trưởng phòng kinh doanh) đọc từng báo giá nháp trước khi gửi.
- Kế toán xác nhận mức VAT trong sheet "Tham số" và cách tính thuế cho dòng phí giao hàng.
- Người có thẩm quyền quyết chiết khấu vượt mức, quà tặng, công nợ, giữ giá cũ, phí giao ngoại tỉnh, hàng không có trong bảng giá.

## Giới hạn

- Dữ liệu giả; 12 yêu cầu chỉ phủ một số kiểu lộn xộn. Yêu cầu thật có ảnh chụp, file đính kèm, giọng điệu khác.
- n rất nhỏ (1 đến 2 lần mỗi agent hợp lệ ở bài 2; n = 1 mỗi prompt ở bài 4). Không so sánh agent này tốt hơn agent kia.
- Hai lần chạy đầu (claude-0, agy-0) mất log nên không biết chúng có mở file đáp án hay không.
- Chấm nhãn "câu hỏi / cần người quyết" bằng từ khóa chỉ là ước lượng; chúng tôi đọc tay các ca chính.
- Ba bài tập ở bài 4 chưa cho agent làm; chỉ bộ chấm được thử bằng đầu ra dựng bằng code.
- Mọi quy định (ngưỡng chiết khấu, phí giao, thẩm quyền, mức VAT) là quy định bịa của công ty giả. Không phải tư vấn thuế hay pháp luật.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.
