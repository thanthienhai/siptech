# Cấp 0 (C0): Viết SOP tối thiểu từ các ca đã xảy ra

> Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** = tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.
> Cấp này gần như không cần AI. Nó là điều kiện để mọi cấp sau có nghĩa.

## 1. Mục tiêu và người đọc

**Người đọc:** chủ shop, trưởng nhóm bán hàng hoặc chăm sóc khách (CSKH) ở SME chưa có quy trình viết ra. Không cần biết code.

**Sau cấp này có:**
1. **Sổ ca:** 30 ca thật gần nhất, đã ẩn danh, mỗi ca ghi khách hỏi gì, đã xử lý thế nào, kết quả.
2. **Danh mục ý định:** 5-8 loại yêu cầu (hỏi đơn, đổi trả, hoàn tiền, khiếu nại, dời lịch, hỏi thông tin, khác).
3. **Chính sách 1 trang:** điều khoản đổi trả, hoàn tiền, dời lịch, phí, thời hạn, ai có quyền ngoại lệ.
4. **SOP dạng bảng quyết định** cho 3 loại yêu cầu nhiều nhất.
5. **Danh sách "chỉ người làm"**: việc không bao giờ giao cho AI.
6. **Bộ ca mẫu 20-30 ca** có đáp án là *quyết định* (được đổi / không được / chuyển người), không chỉ là câu trả lời.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

Câu hỏi: *"AI nên làm theo cái gì?"* Không có cấp trước. Lỗi đang gặp là: mỗi nhân viên xử lý một kiểu, chủ shop quyết theo cảm tính, rồi dán tin khách vào chat AI và gửi lại khách gần như nguyên văn.

Bằng chứng vì sao SOP đi trước:
- **[Nguồn]** Nubank dựng agent chăm sóc khách từ SOP của nhân viên, chuyển SOP thành "routine" có thứ tự bước. Ở ca giao thẻ, phiên bản đầu (V0) chỉ có công cụ tra kho kiến thức và công cụ chuyển người; các phiên bản sau lần lượt thêm routine từ SOP, công cụ tra dữ liệu, phát hiện khách bực, công cụ cấp lại thẻ (arXiv 2606.08867, mục 5.1 và 6.3).
- **[Nguồn]** Airbnb: phần thất bại còn lại chủ yếu do SOP thiếu bước mà nhân viên giỏi vẫn làm (xem `../nen-tang-bang-chung.md` mục 1.3).
- **[Nguồn]** Bài "Policy Loopholes" (arXiv 2609.14400) kiểm chính sách của τ²-bench: chính sách viết cho nhân viên đủ dùng ở ca thường nhưng mơ hồ ở ranh giới. Ở miền hàng không có 15 lỗ hổng; 7/50 tác vụ bị ảnh hưởng; trên các tác vụ này tỉ lệ thành công trung bình 37% so với 51% ở tác vụ còn lại; độ dao động giữa các lần chạy cao gấp 1,62 lần. Các mô hình khác nhau xử lý chỗ mơ hồ khác nhau: mô hình này chuyển người, mô hình kia tự tìm đường vòng.
- **[Đề xuất]** Hàm ý cho SME: nếu chính sách của bạn im lặng ở một chỗ, AI sẽ tự điền chỗ đó, và mỗi lần điền một kiểu. Sửa chính sách rẻ hơn sửa prompt.

## 3. Kiến thức nền

### 3.1 Bốn thứ hay bị trộn lẫn [Đề xuất]

| Thứ | Trả lời câu hỏi | Ví dụ |
|---|---|---|
| Chính sách | Được hay không được | "Đổi size trong 7 ngày kể từ khi nhận, hàng chưa giặt, còn tem" |
| SOP | Làm theo thứ tự nào | "B1 xin mã đơn; B2 tra ngày giao; B3 xét điều kiện; B4 tạo phiếu đổi" |
| Mẫu câu (macro) | Nói với khách thế nào | "Dạ shop đã nhận yêu cầu đổi size của anh/chị..." |
| Thẩm quyền | Ai được làm ngoại lệ | "Hoàn tiền từ 500.000đ phải chủ shop duyệt" |

Nubank tách "routine" (bước) và "macro" (mẫu câu viết sẵn để agent điều chỉnh) thành các thành phần có phiên bản riêng **[Nguồn: 2606.08867, mục 4.2, qua `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.3]**.

### 3.2 Bảng quyết định

Viết mỗi điểm quyết định thành một dòng: **điều kiện → quyết định → ai làm**. Cột cuối cùng luôn có dòng "không khớp dòng nào → chuyển người". Bảng này về sau thành code ở C4.

### 3.3 Bốn câu hỏi kiểm lỗ hổng chính sách [Nguồn: arXiv 2609.14400, mục 3 và phụ lục A.2]

Với mỗi điều khoản, hỏi:
1. **Phạm vi:** điều khoản có nói tới tình huống này không, hay im lặng?
2. **Ranh giới:** có nói tới ca biên không (đúng ngày thứ 7, khách từ chối phương án, chênh lệch 0đ)?
3. **Kết hợp:** khi hai điều khoản cùng áp dụng, cái nào thắng?
4. **Giả định ngầm:** có dựa vào khái niệm chưa định nghĩa không ("hàng lỗi" là lỗi gì? "7 ngày" tính từ ngày đặt hay ngày nhận?)?

Năm loại lỗ hổng bài báo đặt tên: thiếu phạm vi, im lặng ở ca biên, điều khoản mâu thuẫn, điều kiện tiên quyết ngầm, mơ hồ khi kết hợp. Phát hiện thêm của bài: miền bán lẻ cũng có 2 lỗ hổng nhưng **không** gây lỗi, vì công cụ đã chặn (đơn đổi trạng thái thì các lệnh ghi sau bị từ chối). Tức là: chỗ nào chặn được bằng hệ thống thì chặn, đừng chỉ viết thêm chữ.

### 3.4 Khiếu nại có yêu cầu pháp lý [Nguồn: Luật 19/2023/QH15 qua caselaw.vn; chưa đọc bản Công báo]

Điều 31: tổ chức, cá nhân kinh doanh có trách nhiệm tổ chức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại; thông báo đã nhận trong 03 ngày làm việc; nhà sản xuất, nhập khẩu, bán hàng trực tiếp phải công khai quy trình giải quyết. Theo tóm tắt, cá nhân kinh doanh không phải đăng ký và doanh nghiệp siêu nhỏ được loại khỏi yêu cầu công khai này. **[Đề xuất]** Dù được miễn, vẫn nên có quy trình khiếu nại 5 dòng trong SOP.

## 4. Chuỗi bài nhỏ

### Bài 0.1: Gom 30 ca thật
- **Làm:** lấy 30 hội thoại gần nhất từ Zalo OA, Messenger, email, sàn. Chép vào bảng tính, thay tên, SĐT, địa chỉ bằng mã (`KH_01`). Cột: kênh, tin gốc (đã ẩn danh), khách muốn gì, nhân viên đã làm gì, kết quả, mất bao lâu, có phải hỏi chủ không.
- **Sản phẩm:** Sổ ca 30 dòng.
- **Lỗi:** chỉ chọn ca đẹp; quên ca khách bực; dán tin có SĐT vào AI để "tóm tắt hộ".

### Bài 0.2: Đặt nhãn ý định và mức khẩn
- **Làm:** gán mỗi ca một ý định trong danh mục 5-8 loại. Thêm cột mức khẩn: *cao* (an toàn, pháp lý, tiền bị trừ sai, khách dọa đăng mạng), *vừa* (hôm nay phải xong), *thấp*. Đếm tần suất từng loại.
- **Sản phẩm:** danh mục ý định có định nghĩa 1 câu và 2 ví dụ mỗi loại; bảng tần suất.
- **Lỗi:** quá nhiều loại (trên 10) nên không ai gán giống ai. Hai người gán độc lập 30 ca, so số ca lệch; lệch nhiều thì định nghĩa chưa rõ.

### Bài 0.3: Chính sách 1 trang
- **Làm:** viết các điều khoản đang thực sự áp dụng (không phải điều mong muốn). Mỗi điều khoản có: điều kiện, thời hạn tính từ mốc nào, ngoại lệ, ai quyết ngoại lệ.
- **Sản phẩm:** `chinh-sach-v1.md` có ngày hiệu lực và người chủ.
- **Lỗi:** chép chính sách trên web không ai làm theo; không ghi mốc tính ngày.

### Bài 0.4: Bảng quyết định cho 3 loại nhiều nhất
- **Làm:** với từng loại, viết bảng điều kiện → quyết định → ai làm → mẫu câu. Đánh dấu bước *Code* (tính được: số ngày, số tiền), *AI* (hiểu tin, soạn câu), *Người* (ngoại lệ, tiền lớn, khiếu nại).
- **Sản phẩm:** 3 bảng quyết định. Mẫu ở mục 7.
- **Lỗi:** viết thành đoạn văn; thiếu dòng "không khớp → chuyển người".

### Bài 0.5: Kiểm lỗ hổng bằng 4 câu hỏi
- **Làm:** người làm trước bằng 4 câu hỏi ở mục 3.3. Sau đó có thể nhờ AI (Project/Gem, chính sách đã ẩn danh, không có dữ liệu khách) đóng vai "khách khó tính" liệt kê 10 tình huống chính sách không trả lời được. Người quyết từng tình huống: sửa chính sách, hay ghi "chuyển người".
- **Sản phẩm:** danh sách lỗ hổng và cách xử lý; `chinh-sach-v2.md`.
- **Lỗi:** để AI tự sửa chính sách; vá từng ca thay vì sửa câu chữ của điều khoản. Bài 2609.14400 cho thấy vá từng ca (sửa đáp án từng tác vụ) để lại điều khoản mơ hồ và có khi cho hai đáp án ngược nhau cho cùng một điều khoản.

### Bài 0.6: Bộ ca mẫu có đáp án quyết định
- **Làm:** từ Sổ ca chọn 20-30 ca: ca thường, ca biên (đúng ngày thứ 7), ca mâu thuẫn (hàng sale bị lỗi), ca phải chuyển người. Mỗi ca ghi: ý định đúng, mức khẩn đúng, quyết định đúng, hành động đúng, điều bắt buộc phải nói với khách.
- **Sản phẩm:** `bo-ca-mau-v1` (bảng tính). Dùng lại ở mọi cấp sau. Cách chấm và giới hạn của n nhỏ: `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`.
- **Lỗi:** đáp án chỉ là "câu trả lời hay"; không có ca chuyển người.

### Bài 0.7: Danh sách "chỉ người làm" và quy trình khiếu nại
- **Làm:** liệt kê việc AI không được tự quyết. Gợi ý **[Đề xuất]**: hoàn tiền; ngoại lệ chính sách; mọi khiếu nại; ca an toàn (dị ứng, ngộ độc, thương tích); khách nhắc luật sư, báo chí, cơ quan nhà nước; khách là trẻ em. Viết quy trình khiếu nại 5 dòng: ai nhận, báo đã nhận trong bao lâu (luật: 03 ngày làm việc), ai giải quyết, ghi vào đâu.
- **Sản phẩm:** 1 trang dán cạnh SOP.

## 5. Đường không code vs có code

| | Không code | Có code |
|---|---|---|
| Công cụ | Google Sheets/Docs; AI chỉ dùng để rà lỗ hổng trên chính sách đã ẩn danh | Không cần ở cấp này |
| Sản phẩm | Sổ ca, chính sách, bảng quyết định, bộ ca mẫu | — |

**Chuyển sang C1 khi:** đã có bảng quyết định cho ít nhất loại yêu cầu nhiều nhất và có người duyệt được chỉ định. Không cần code để lên C1.

## 6. Tiêu chí lên cấp (C0 → C1) [Đề xuất]

1. Sổ ca ≥30 ca thật, đã ẩn danh, phủ ≥80% số tin của một tuần điển hình theo ý định.
2. Hai người gán nhãn ý định độc lập trên 30 ca, lệch ≤5 ca. Lệch nhiều hơn thì sửa định nghĩa trước.
3. Có bảng quyết định cho ≥3 loại, mỗi bảng có dòng "không khớp → chuyển người".
4. Đã chạy 4 câu hỏi kiểm lỗ hổng; mọi lỗ hổng tìm được đều có cách xử lý ghi rõ.
5. Bộ ca mẫu ≥20 ca, trong đó ≥5 ca biên và ≥3 ca phải chuyển người.
6. Chủ shop ký chính sách v2 và danh sách "chỉ người làm".

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa; chính sách là giả định]

### 7.a Shop thời trang online (Zalo OA, Facebook, Shopee)

Bảng quyết định "đổi size":

| # | Điều kiện | Quyết định | Ai |
|---|---|---|---|
| 1 | Đơn chưa giao | Không đổi; hướng dẫn sửa đơn | AI soạn, NV duyệt |
| 2 | Lỗi do shop (sai size, lỗi may) | Đổi, shop chịu phí ship | AI đề xuất, trưởng ca duyệt |
| 3 | Hàng sale hoặc đồ lót, không lỗi | Không đổi | AI soạn, NV duyệt |
| 4 | Đã nhận ≤7 ngày, còn tem, chưa giặt | Đổi, khách chịu phí ship | AI đề xuất, NV duyệt |
| 5 | Đã nhận >7 ngày | Không đổi; ngoại lệ chỉ chủ shop | Chuyển người nếu khách xin |
| 6 | Không khớp dòng nào | Chuyển người | — |

Lỗ hổng tìm bằng 4 câu hỏi: "Hàng sale bị lỗi may thì sao?" (dòng 2 hay dòng 3 thắng? phải ghi rõ thứ tự); "7 ngày tính từ ngày giao theo hãng vận chuyển hay ngày khách báo đã nhận?"; "Khách đổi sang mẫu khác giá cao hơn?" (chính sách im lặng).

### 7.b Spa hoặc phòng khám nha (đặt lịch, đặt cọc)

Bảng "dời lịch": dời trước ≥24 giờ thì miễn phí, giữ cọc; dời trong 24 giờ thì mất cọc trừ lý do sức khỏe có giấy tờ (ngoại lệ, chỉ quản lý); dời lần thứ ba thì chuyển người. Lỗ hổng: "24 giờ tính tới giờ hẹn hay tới đầu ngày hẹn?"; "khách hủy hẳn thì cọc xử lý thế nào?" Ca *chỉ người làm*: mọi câu hỏi về triệu chứng, biến chứng sau điều trị.

### 7.c Tiệm bánh có giao hàng

Ý định đặc thù: "bánh hỏng khi nhận". Mức khẩn *cao* nếu có từ "đau bụng", "dị ứng": luôn chuyển chủ tiệm, không để AI soạn lời xin lỗi kèm cam kết.

## 8. Tài liệu tham khảo

| Nguồn | Loại | Đọc | Tin cậy |
|---|---|---|---|
| Nubank, *Building Customer Support AI Agents at 100M-User Scale*, arXiv 2606.08867 | Bài báo KDD 2026, triển khai thật | Phần lớn toàn văn (2026-11-11) | Cao, nhưng là ngân hàng lớn |
| Cao, *Policy Loopholes in Agent Evaluation*, arXiv 2609.14400 | Bài báo, 1 tác giả, trên benchmark | Phần chính và phụ lục A, C | Trung bình-Cao (2 miền, một benchmark) |
| Airbnb, arXiv 2610.14428 | Bài báo | Qua `../nen-tang-bang-chung.md` | Cao |
| Luật Bảo vệ quyền lợi người tiêu dùng 19/2023/QH15, Điều 31 | Văn bản luật, trang caselaw.vn | Qua công cụ tóm tắt, trích ≤125 ký tự | Trung bình (chưa đọc Công báo) |

## 9. Chưa kiểm chứng

- Ngoại lệ của Điều 31 khoản 3 (cá nhân không đăng ký kinh doanh, doanh nghiệp siêu nhỏ) và cách tính "doanh nghiệp siêu nhỏ": chỉ qua tóm tắt.
- NĐ 55/2024/NĐ-CP có quy định thời hạn giải quyết khiếu nại hay không: chưa đọc.
- Ngưỡng 30 ca, lệch ≤5 ca, 80% phủ: đề xuất, chưa thử trên SME thật.
- Chưa có nguồn đo xem SME Việt Nam có SOP chăm sóc khách viết ra hay không.
