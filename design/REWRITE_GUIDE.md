# Hướng dẫn viết lại bài cấp độ thành bài giảng cho người mới

Mục tiêu: biến các file nghiên cứu trong `content/<nhóm>/cap-XX-*.md` thành **bài giảng** cho người **không biết lập trình, mới bắt đầu dùng AI** (chủ SME, kế toán, nhân sự, quản lý, nhân viên văn phòng ở Việt Nam).

Bài mẫu đã viết xong, đọc kỹ trước khi làm: `content/tri-thuc-to-chuc/cap-00-bien-ban-hop-co-khuon.md`.
Bản gốc để so sánh (đừng sửa): `C:\Users\PC\Coding\thienthan\MM\AI-Real\<nhóm>\<file>.md`.

## Việc phải làm với mỗi file

1. **Giữ nguyên khối đầu file** (dòng `# Tiêu đề` và các dòng `>` hoặc dòng "Ngày soạn/Quy ước" ngay sau đó). Bộ dựng site tự biến chúng thành khung "Trước khi học".
2. Ngay sau khối đầu, thêm hộp tóm tắt (đúng cú pháp, thụt 4 dấu cách):
   ```
   !!! tip "Tóm tắt nhanh"
       2 đến 4 câu: bài này giải quyết vấn đề gì, làm bằng cách nào, bạn có gì sau bài.
   ```
3. **Viết lại phần chữ** của các mục thành giọng giảng bài:
   - Xưng "bạn" và "chúng ta"; câu ngắn; một ý một câu; dùng lời thường.
   - **Giải thích thuật ngữ ngay lần đầu** gặp trong bài (API, prompt, token, JSON, chunk, OCR, log, agent...) bằng một vế ngắn trong ngoặc hoặc một câu sau đó. Không giả định người đọc biết gì.
   - Sau các đoạn kỹ thuật dày, thêm hộp giải thích đơn giản (1 đến 3 câu), cú pháp: `!!! tip "Nói đơn giản"` rồi nội dung thụt 4 dấu cách.
   - Mục 1 ("Mục tiêu và người đọc") thành: Bài này dành cho ai / Bạn cần chuẩn bị (tài khoản, tài liệu mẫu, công cụ, lấy từ nội dung gốc, không bịa thêm) / Sau bài này bạn sẽ có / Thứ bạn cầm đi được.
   - Các bài thực hành ("Bài X.Y"): giữ tên bài; viết thành các dòng **Việc cần làm**, **Bạn có sau bài**, **Lỗi hay gặp**, câu lệnh chia thành các bước rõ ràng khi nội dung gốc có thứ tự.
   - Trước mỗi khối mã, thêm 1 đến 3 câu "Đoạn mã dưới đây làm gì?" bằng lời thường, kèm câu nói người không code không cần đọc hiểu từng dòng, chỉ cần nhờ người biết code hoặc nhờ AI chạy giúp.
   - Giải thích tên viết tắt, chữ tiếng Anh khi xuất hiện (ví dụ "ablation" = thử bỏ từng phần để xem phần nào quan trọng).
4. **Tuyệt đối giữ nguyên và không thêm mới:**
   - mọi **con số, tỷ lệ, ngày, tên nguồn, mã arXiv, tên người, tên sản phẩm** của bản gốc; không thêm số liệu hay khẳng định mới;
   - mọi nhãn `[Nguồn]`, `[Nguồn: B5]`, `[Đề xuất]`, `[Đề xuất, minh họa]`, `[Đề xuất, quan sát]`, `[Đã chạy thử]`, `[Chưa chạy thử]`... (có thể đổi vị trí trong câu, không bỏ; nhãn ở tiêu đề `###` giữ ở tiêu đề);
   - **tiêu đề cấp 2 (`## ...`)**: đúng thứ tự và đúng chữ như bản gốc (bộ dựng nhận diện theo tên). Tiêu đề cấp 3 có thể sửa chữ cho dễ hiểu nhưng giữ số thứ tự (3.1, 3.2...) và tên bài "Bài X.Y";
   - **mọi khối mã** (```), chữ trong khối mã giữ y nguyên từng ký tự;
   - **mọi bảng** (cùng số bảng, cùng số liệu; được chỉnh chữ trong ô cho dễ hiểu);
   - **mọi URL** và các tham chiếu file dạng `../x/cap-01-....md` đặt trong dấu huyền (kèm "mục 3.2", "Bài 2.6" nếu có);
   - toàn bộ các mục **"Tài liệu tham khảo"** và **"Chưa kiểm chứng"** (chép lại gần như nguyên văn, chỉ sửa lỗi chữ);
   - các cảnh báo "không phải tư vấn pháp lý" và mọi chỗ ghi "chưa kiểm chứng", "chưa đo", "ngưỡng là đề xuất".
5. Không rút gọn bỏ ý. Mục tiêu là **dễ hiểu hơn**, không phải ngắn hơn (độ dài thường tăng 10 đến 40%).
6. Không dùng ký tự gạch dài "—" làm dấu ngắt câu thừa; không viết kiểu quảng cáo; không dùng icon/emoji.

## Cú pháp có thể dùng (bộ dựng site hỗ trợ)

- Hộp: `!!! tip "Nói đơn giản"`, `!!! note "Lưu ý"`, `!!! warning "Cẩn thận"`; nội dung thụt 4 dấu cách.
- Hộp `!!!` đặt ở lề trái, có một dòng trống ngay phía trước, không đặt bên trong mục danh sách.
- Bảng Markdown, danh sách, **đậm**, *nghiêng*.
- Không dùng HTML thô.

## Kiểm tra sau khi viết

Chạy từ thư mục `C:\Users\PC\Coding\thienthan\siptech`:

```
python -X utf8 design/check_rewrite.py <nhóm>/<file>.md
```

Lệnh in `OK` khi không mất số liệu, URL, khối mã, bảng, tiêu đề ##, nhãn nguồn. Nếu in `XEM`, sửa file cho tới khi `OK` (hoặc nếu chênh lệch là chủ ý hợp lý, ví dụ số thứ tự bị đổi cách viết, nói rõ trong báo cáo).

Đừng chạy `build.py`, đừng commit, đừng sửa file khác ngoài file được giao.

## Báo cáo cuối (ngắn)

Gồm: tên file; kết quả `check_rewrite`; 2 đến 3 điểm đã làm dễ hiểu hơn; những chỗ chưa chắc về nghĩa hoặc thuật ngữ cần người xem lại.
