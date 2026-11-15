# Cấp 0 (C0): Viết SOP tối thiểu từ các ca đã xảy ra

> Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** = tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.
> Cấp này gần như không cần AI. Nó là điều kiện để mọi cấp sau có nghĩa.

!!! tip "Tóm tắt nhanh"
    Trước khi nhờ AI trả lời khách, bạn phải có thứ để AI **làm theo**. Bài này giúp bạn viết ra quy trình xử lý (gọi là SOP, tức là các bước làm việc chuẩn) bắt đầu từ chính những ca khách đã xảy ra ở shop của bạn. Bạn **không cần biết lập trình** và gần như không cần AI. Sau bài, bạn có sổ ca, chính sách 1 trang, bảng quyết định và danh sách việc chỉ người mới được làm.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** chủ shop, trưởng nhóm bán hàng hoặc chăm sóc khách (CSKH) ở doanh nghiệp vừa và nhỏ (SME) chưa có quy trình viết ra. Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Các hội thoại thật gần nhất với khách, lấy từ Zalo OA (tài khoản Zalo dành cho doanh nghiệp), Messenger, email hoặc sàn thương mại điện tử.
- Một bảng tính (Google Sheets hoặc Excel) để ghi sổ ca.
- Một công cụ soạn văn bản (Google Docs hoặc Word) để viết chính sách.

**Sau bài này bạn sẽ có:**
1. **Sổ ca:** 30 ca thật gần nhất, đã ẩn danh (thay thông tin cá nhân bằng mã), mỗi ca ghi khách hỏi gì, đã xử lý thế nào, kết quả.
2. **Danh mục ý định:** 5-8 loại yêu cầu (hỏi đơn, đổi trả, hoàn tiền, khiếu nại, dời lịch, hỏi thông tin, khác). "Ý định" nghĩa là khách đang muốn gì.
3. **Chính sách 1 trang:** điều khoản đổi trả, hoàn tiền, dời lịch, phí, thời hạn, ai có quyền ngoại lệ.
4. **SOP dạng bảng quyết định** cho 3 loại yêu cầu nhiều nhất.
5. **Danh sách "chỉ người làm"**: việc không bao giờ giao cho AI.
6. **Bộ ca mẫu 20-30 ca** có đáp án là *quyết định* (được đổi / không được / chuyển người), không chỉ là câu trả lời.

**Thứ bạn cầm đi được sau bài:** sổ ca 30 dòng, một trang chính sách, ba bảng quyết định, một trang "chỉ người làm" kèm quy trình khiếu nại, và bộ ca mẫu để dùng lại ở các cấp sau.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

Câu hỏi: *"AI nên làm theo cái gì?"* Cấp này là cấp đầu tiên nên không có cấp trước. Lỗi chúng ta đang gặp là: mỗi nhân viên xử lý một kiểu, chủ shop quyết theo cảm tính, rồi dán tin khách vào khung chat AI và gửi lại cho khách gần như nguyên văn.

Dưới đây là bằng chứng vì sao SOP phải đi trước:
- **[Nguồn]** Nubank dựng agent chăm sóc khách từ SOP của nhân viên. (Agent ở đây là một chương trình AI tự làm từng bước để xử lý yêu cầu, có thể gọi thêm công cụ.) Họ chuyển SOP thành "routine", tức là các bước có thứ tự. Ở ca giao thẻ, phiên bản đầu (V0) chỉ có công cụ tra kho kiến thức và công cụ chuyển người; các phiên bản sau lần lượt thêm routine từ SOP, công cụ tra dữ liệu, phát hiện khách bực, công cụ cấp lại thẻ (arXiv 2606.08867, mục 5.1 và 6.3).
- **[Nguồn]** Airbnb: phần thất bại còn lại chủ yếu do SOP thiếu bước mà nhân viên giỏi vẫn làm (xem `../nen-tang-bang-chung.md` mục 1.3).
- **[Nguồn]** Bài "Policy Loopholes" (arXiv 2609.14400) kiểm chính sách của τ²-bench. (τ²-bench là một bộ bài kiểm dùng để thử xem AI xử lý các tác vụ chăm sóc khách tốt đến đâu.) Kết quả: chính sách viết cho nhân viên đủ dùng ở ca thường nhưng mơ hồ ở ranh giới. Ở miền hàng không có 15 lỗ hổng; 7/50 tác vụ bị ảnh hưởng; trên các tác vụ này tỉ lệ thành công trung bình 37% so với 51% ở tác vụ còn lại; độ dao động giữa các lần chạy cao gấp 1,62 lần. Các mô hình AI khác nhau xử lý chỗ mơ hồ khác nhau: mô hình này chuyển người, mô hình kia tự tìm đường vòng.
- **[Đề xuất]** Hàm ý cho SME: nếu chính sách của bạn im lặng ở một chỗ, AI sẽ tự điền chỗ đó, và mỗi lần điền một kiểu. Sửa chính sách rẻ hơn sửa prompt. (Prompt là đoạn chỉ dẫn bạn viết cho AI.)

!!! tip "Nói đơn giản"
    AI giống một nhân viên mới rất chăm nhưng không dám hỏi. Chỗ nào bạn chưa viết rõ, nó sẽ tự đoán, và mỗi lần đoán một kiểu. Vì vậy việc đầu tiên là viết rõ luật chơi, rồi mới tính chuyện giao việc cho AI.

## 3. Kiến thức nền

### 3.1 Bốn thứ hay bị trộn lẫn [Đề xuất]

Khi nói "quy trình", nhiều người gộp bốn thứ khác nhau vào một. Hãy tách chúng ra:

| Thứ | Trả lời câu hỏi | Ví dụ |
|---|---|---|
| Chính sách | Được hay không được | "Đổi size trong 7 ngày kể từ khi nhận, hàng chưa giặt, còn tem" |
| SOP | Làm theo thứ tự nào | "B1 xin mã đơn; B2 tra ngày giao; B3 xét điều kiện; B4 tạo phiếu đổi" |
| Mẫu câu (macro) | Nói với khách thế nào | "Dạ shop đã nhận yêu cầu đổi size của anh/chị..." |
| Thẩm quyền | Ai được làm ngoại lệ | "Hoàn tiền từ 500.000đ phải chủ shop duyệt" |

Nubank tách "routine" (bước) và "macro" (mẫu câu viết sẵn để agent điều chỉnh) thành các thành phần có phiên bản riêng **[Nguồn: 2606.08867, mục 4.2, qua `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.3]**.

!!! tip "Nói đơn giản"
    Chính sách là "luật", SOP là "các bước làm", mẫu câu là "lời nói với khách", thẩm quyền là "ai được phá lệ". Viết riêng từng thứ thì sau này dễ sửa: đổi luật không bắt bạn viết lại lời nói.

### 3.2 Bảng quyết định

Chúng ta viết mỗi điểm quyết định thành một dòng theo dạng: **điều kiện → quyết định → ai làm**. Cột cuối cùng luôn có dòng "không khớp dòng nào → chuyển người". Bảng này về sau thành code ở C4. (Code là chương trình máy tính tự chạy theo luật bạn đã viết.)

### 3.3 Bốn câu hỏi kiểm lỗ hổng chính sách [Nguồn: arXiv 2609.14400, mục 3 và phụ lục A.2]

Lỗ hổng chính sách là chỗ điều khoản viết thiếu hoặc mơ hồ, khiến hai người đọc ra hai cách làm khác nhau. Với mỗi điều khoản, bạn hỏi bốn câu:
1. **Phạm vi:** điều khoản có nói tới tình huống này không, hay im lặng?
2. **Ranh giới:** có nói tới ca biên không (đúng ngày thứ 7, khách từ chối phương án, chênh lệch 0đ)? Ca biên là ca nằm sát mép của điều kiện.
3. **Kết hợp:** khi hai điều khoản cùng áp dụng, cái nào thắng?
4. **Giả định ngầm:** có dựa vào khái niệm chưa định nghĩa không ("hàng lỗi" là lỗi gì? "7 ngày" tính từ ngày đặt hay ngày nhận?)?

Năm loại lỗ hổng bài báo đặt tên: thiếu phạm vi, im lặng ở ca biên, điều khoản mâu thuẫn, điều kiện tiên quyết ngầm, mơ hồ khi kết hợp. Phát hiện thêm của bài: miền bán lẻ cũng có 2 lỗ hổng nhưng **không** gây lỗi, vì công cụ đã chặn (đơn đổi trạng thái thì các lệnh ghi sau bị từ chối). Tức là: chỗ nào chặn được bằng hệ thống thì chặn, đừng chỉ viết thêm chữ.

!!! tip "Nói đơn giản"
    Bốn câu hỏi này là cách "đọc chính sách bằng mắt của khách khó tính". Chỗ nào bạn không trả lời được ngay thì đó là lỗ hổng. Nếu phần mềm có thể tự chặn (ví dụ đơn đã giao thì không cho sửa), hãy để phần mềm chặn, đừng chỉ dặn bằng chữ.

### 3.4 Khiếu nại có yêu cầu pháp lý [Nguồn: Luật 19/2023/QH15 qua caselaw.vn; chưa đọc bản Công báo]

Điều 31: tổ chức, cá nhân kinh doanh có trách nhiệm tổ chức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại; thông báo đã nhận trong 03 ngày làm việc; nhà sản xuất, nhập khẩu, bán hàng trực tiếp phải công khai quy trình giải quyết. Theo tóm tắt, cá nhân kinh doanh không phải đăng ký và doanh nghiệp siêu nhỏ được loại khỏi yêu cầu công khai này. **[Đề xuất]** Dù được miễn, vẫn nên có quy trình khiếu nại 5 dòng trong SOP.

!!! warning "Cẩn thận"
    Đây là phần tóm tắt từ một trang tổng hợp luật, chúng tôi chưa đọc bản Công báo (bản chính thức của nhà nước). Nội dung này **không phải tư vấn pháp lý**. Nếu cần chắc chắn, hãy hỏi luật sư hoặc cơ quan có thẩm quyền.

## 4. Chuỗi bài nhỏ

Bảy bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và lỗi hay gặp để tránh (nếu có).

### Bài 0.1: Gom 30 ca thật
- **Việc cần làm:** lấy 30 hội thoại gần nhất từ Zalo OA, Messenger, email, sàn. Chép vào bảng tính, thay tên, SĐT (số điện thoại), địa chỉ bằng mã (`KH_01`). Cột: kênh, tin gốc (đã ẩn danh), khách muốn gì, nhân viên đã làm gì, kết quả, mất bao lâu, có phải hỏi chủ không.
- **Bạn có sau bài:** Sổ ca 30 dòng.
- **Lỗi hay gặp:** chỉ chọn ca đẹp; quên ca khách bực; dán tin có SĐT vào AI để "tóm tắt hộ".

### Bài 0.2: Đặt nhãn ý định và mức khẩn
- **Việc cần làm:** gán mỗi ca một ý định trong danh mục 5-8 loại. Thêm cột mức khẩn: *cao* (an toàn, pháp lý, tiền bị trừ sai, khách dọa đăng mạng), *vừa* (hôm nay phải xong), *thấp*. Đếm tần suất từng loại, tức là mỗi loại xuất hiện bao nhiêu lần.
- **Bạn có sau bài:** danh mục ý định có định nghĩa 1 câu và 2 ví dụ mỗi loại; bảng tần suất.
- **Lỗi hay gặp:** quá nhiều loại (trên 10) nên không ai gán giống ai. Cách thử: hai người gán độc lập 30 ca, rồi so số ca lệch; lệch nhiều thì định nghĩa chưa rõ.

### Bài 0.3: Chính sách 1 trang
- **Việc cần làm:** viết các điều khoản đang thực sự áp dụng (không phải điều mong muốn). Mỗi điều khoản có: điều kiện, thời hạn tính từ mốc nào, ngoại lệ, ai quyết ngoại lệ.
- **Bạn có sau bài:** `chinh-sach-v1.md` có ngày hiệu lực và người chủ. (Tên tệp chỉ là ví dụ; bạn có thể lưu bằng Google Docs hay Word.)
- **Lỗi hay gặp:** chép chính sách trên web không ai làm theo; không ghi mốc tính ngày.

### Bài 0.4: Bảng quyết định cho 3 loại nhiều nhất
- **Việc cần làm:** với từng loại, viết bảng điều kiện → quyết định → ai làm → mẫu câu. Đánh dấu bước *Code* (tính được: số ngày, số tiền), *AI* (hiểu tin, soạn câu), *Người* (ngoại lệ, tiền lớn, khiếu nại).
- **Bạn có sau bài:** 3 bảng quyết định. Mẫu ở mục 7.
- **Lỗi hay gặp:** viết thành đoạn văn; thiếu dòng "không khớp → chuyển người".

### Bài 0.5: Kiểm lỗ hổng bằng 4 câu hỏi
- **Việc cần làm:** người làm trước, bằng 4 câu hỏi ở mục 3.3. Sau đó có thể nhờ AI (trong Project của Claude hoặc Gem của Gemini, là nơi bạn lưu sẵn chỉ dẫn để dùng lại; đưa vào chính sách đã ẩn danh, không có dữ liệu khách) đóng vai "khách khó tính" liệt kê 10 tình huống chính sách không trả lời được. Người quyết từng tình huống: sửa chính sách, hay ghi "chuyển người".
- **Bạn có sau bài:** danh sách lỗ hổng và cách xử lý; `chinh-sach-v2.md`.
- **Lỗi hay gặp:** để AI tự sửa chính sách; vá từng ca thay vì sửa câu chữ của điều khoản. Bài 2609.14400 cho thấy vá từng ca (sửa đáp án từng tác vụ) để lại điều khoản mơ hồ và có khi cho hai đáp án ngược nhau cho cùng một điều khoản.

### Bài 0.6: Bộ ca mẫu có đáp án quyết định
- **Việc cần làm:** từ Sổ ca chọn 20-30 ca: ca thường, ca biên (đúng ngày thứ 7), ca mâu thuẫn (hàng sale bị lỗi), ca phải chuyển người. Mỗi ca ghi: ý định đúng, mức khẩn đúng, quyết định đúng, hành động đúng, điều bắt buộc phải nói với khách.
- **Bạn có sau bài:** `bo-ca-mau-v1` (bảng tính). Dùng lại ở mọi cấp sau. Cách chấm và giới hạn của n nhỏ (n là số ca bạn có; ít ca thì kết quả chưa đáng tin): `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`.
- **Lỗi hay gặp:** đáp án chỉ là "câu trả lời hay"; không có ca chuyển người.

### Bài 0.7: Danh sách "chỉ người làm" và quy trình khiếu nại
- **Việc cần làm:** liệt kê việc AI không được tự quyết. Gợi ý **[Đề xuất]**: hoàn tiền; ngoại lệ chính sách; mọi khiếu nại; ca an toàn (dị ứng, ngộ độc, thương tích); khách nhắc luật sư, báo chí, cơ quan nhà nước; khách là trẻ em. Viết quy trình khiếu nại 5 dòng: ai nhận, báo đã nhận trong bao lâu (luật: 03 ngày làm việc), ai giải quyết, ghi vào đâu.
- **Bạn có sau bài:** 1 trang dán cạnh SOP.

## 5. Đường không code vs có code

Ở cấp này, đường không code là đủ. Bảng dưới cho thấy bạn dùng gì và nhận được gì.

| | Không code | Có code |
|---|---|---|
| Công cụ | Google Sheets/Docs; AI chỉ dùng để rà lỗ hổng trên chính sách đã ẩn danh | Không cần ở cấp này |
| Sản phẩm | Sổ ca, chính sách, bảng quyết định, bộ ca mẫu | — |

**Chuyển sang C1 khi:** đã có bảng quyết định cho ít nhất loại yêu cầu nhiều nhất và có người duyệt được chỉ định. Không cần code để lên C1.

## 6. Tiêu chí lên cấp (C0 → C1) [Đề xuất]

Bạn có thể sang cấp C1 khi đạt đủ các điều sau:
1. Sổ ca ≥30 ca thật, đã ẩn danh, phủ ≥80% số tin của một tuần điển hình theo ý định.
2. Hai người gán nhãn ý định độc lập trên 30 ca, lệch ≤5 ca. Lệch nhiều hơn thì sửa định nghĩa trước.
3. Có bảng quyết định cho ≥3 loại, mỗi bảng có dòng "không khớp → chuyển người".
4. Đã chạy 4 câu hỏi kiểm lỗ hổng; mọi lỗ hổng tìm được đều có cách xử lý ghi rõ.
5. Bộ ca mẫu ≥20 ca, trong đó ≥5 ca biên và ≥3 ca phải chuyển người.
6. Chủ shop ký chính sách v2 và danh sách "chỉ người làm".

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa; chính sách là giả định]

Các ví dụ dưới đây là tình huống giả định để bạn dễ hình dung. Chính sách trong ví dụ là do chúng tôi đặt ra, không phải chuẩn chung.

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

(NV là nhân viên.)

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
