# Cấp 0 (C0): Dùng AI thủ công một cách có kỷ luật

> Ngày soạn: 2026-11-11. Phần "nguyên tắc" là bền; phần "thao tác trên giao diện" hay đổi, mỗi chỗ có ghi ngày kiểm tra.
> Quy ước: **[Nguồn]** = kết quả đọc được trong nguồn; **[Đề xuất]** = đề xuất của chúng tôi, chưa có bằng chứng định lượng.
> Không phải tư vấn pháp lý. Phần dữ liệu và luật xem file `../an-toan-du-lieu-va-phap-ly-vn.md`.

!!! tip "Tóm tắt nhanh"
    Ở nhiều công ty nhỏ, mỗi người dùng AI một kiểu: hỏi một việc mỗi lần một cách, không ai biết kết quả đúng hay sai, dữ liệu khách có thể đã bị dán đi đâu không rõ. Bài này dạy cách dùng AI **có kỷ luật mà không cần biết lập trình**: viết một "bản giao việc" chuẩn cho mỗi nghiệp vụ, lập bảng ca thử để kiểm tra, đặt quy tắc dữ liệu và có người duyệt. Sau bài, bạn có một "Sổ prompt" dùng chung, một Project hoặc Gem cho vài nghiệp vụ, và một trang quy tắc dữ liệu.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** chủ doanh nghiệp nhỏ và vừa (SME), kế toán, nhân viên bán hàng, chăm sóc khách hàng (CSKH), vận hành ở Việt Nam. Công ty bạn chưa có quy trình dùng AI, mọi người đang dùng Claude, ChatGPT hay Gemini "mỗi người một kiểu". Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Một tài khoản công cụ AI đang dùng (Claude, ChatGPT hoặc Gemini).
- Một bảng tính hoặc một tài liệu chung để làm "Sổ prompt".
- Một vài nghiệp vụ lặp đi lặp lại trong công ty (ví dụ soạn thư trả lời khách) và 1 đến 3 tài liệu nền như bảng giá, chính sách.

**Sau bài này, bạn sẽ có** (đo được):
1. Mỗi nghiệp vụ lặp lại có **một bản giao việc (prompt)** chuẩn, lưu ở một chỗ chung, ai dùng cũng ra kết quả tương tự. ("Prompt" là đoạn chữ bạn gõ để ra lệnh cho AI. Trong bài này ta coi nó như một bản giao việc cho nhân viên.)
2. Mỗi bản giao việc có **5-10 ca thử** (đầu vào mẫu cùng đầu ra mong đợi) để kiểm tra mỗi khi đổi mô hình AI hay sửa prompt.
3. Mọi người biết **quy tắc dữ liệu**: cái gì không được dán vào AI.
4. Có **người duyệt** (con người) cho mọi kết quả đi ra ngoài công ty.

**Thứ bạn cầm đi được sau bài:** một "Sổ prompt" (bảng tính hoặc tài liệu); một Project, Gem hoặc GPT cho 1-3 nghiệp vụ (đây là những tính năng cho phép bạn lưu sẵn chỉ dẫn để dùng lại, sẽ giải thích ở mục 3.3); và một trang quy tắc dữ liệu 1 tờ A4.

## 2. Câu hỏi cấp này trả lời / vì sao có cấp này

Cấp 0 là điểm xuất phát, nên không có "lỗi của cấp trước" để sửa. Câu hỏi của cấp này là: *"Làm sao dùng công cụ AI có sẵn cho ổn định, an toàn, lặp lại được, trước khi bỏ tiền làm gì to hơn?"*

Bằng chứng về thực tế dùng agent (AI tự làm nhiều bước) và AI trong doanh nghiệp (**[Nguồn]**, bài MAP arXiv 2512.04123; các số này đã được đối chiếu với toàn văn bài ở bước rà soát ngày 2026-11-11):
- 70% dùng prompt trên mô hình có sẵn thay vì huấn luyện mô hình riêng;
- 68% chạy dưới 10 bước rồi chuyển cho người;
- 74% đánh giá kết quả bằng người;
- 52% agent phục vụ nhân viên nội bộ.

**[Đề xuất]** Ý nghĩa cho SME: bắt đầu bằng prompt cộng người duyệt là hợp với thực tế các tổ chức đã triển khai, không phải là "làm cho qua".

!!! tip "Nói đơn giản"
    Đa số tổ chức thật sự đang làm đúng những thứ đơn giản này: dùng AI có sẵn, ra lệnh bằng prompt, và để người kiểm tra. Bạn không phải làm điều gì cao siêu mới bắt đầu được.

Dấu hiệu cho thấy bạn cần Cấp 0 có kỷ luật:
- nhân viên dùng tài khoản cá nhân;
- cùng một việc mà mỗi người hỏi một kiểu;
- không ai biết kết quả đúng hay sai;
- không rõ dữ liệu khách đã bị dán đi đâu (xem file an toàn dữ liệu).

## 3. Kiến thức nền (ngắn, chính xác)

### 3.1 Nguyên tắc (bền)

- **Prompt là bản giao việc.** Hướng dẫn của OpenAI (công ty làm ChatGPT) mô tả cấu trúc điển hình của một prompt gồm bốn phần: Identity (vai trò, phong cách, mục tiêu), Instructions (quy tắc, điều không được làm), Examples (đầu vào mẫu và đầu ra mong muốn, nên đa dạng), Context (dữ liệu bổ sung, thường đặt gần cuối prompt) **[Nguồn: OpenAI Prompt engineering guide]**. Tài liệu của Claude thì yêu cầu phải có trước ba thứ: tiêu chí thành công rõ ràng, cách kiểm thử bằng thực nghiệm, và bản nháp đầu tiên **[Nguồn: Claude Prompt engineering overview]**.
- **Tách phần cố định và phần thay đổi.** Phần cố định (vai trò, quy tắc, định dạng) đặt vào chỉ dẫn của Project/Gem/GPT. Phần thay đổi (tài liệu của hôm nay) dán vào từng lần chạy. **[Đề xuất]**
- **Đo bằng ca thử.** Cả hai nhà cung cấp khuyến nghị có bộ đánh giá (evals, tức là một bộ bài kiểm tra để chấm AI làm tốt hay không) trước khi đổi prompt hay nâng cấp mô hình **[Nguồn: OpenAI; Claude]**. Ở C0, "bộ đánh giá" chỉ là một bảng 5-10 dòng.
- **Con người chịu trách nhiệm.** Mô hình có thể bịa và tự tin nói sai (người ta gọi là hallucination, nghĩa là "ảo giác"); không có công cụ C0 nào loại bỏ hoàn toàn điều này. **[Đề xuất]** Quy tắc: số liệu, trích dẫn luật, giá, tên người hay tên công ty phải được người đối chiếu nguồn gốc trước khi dùng.

!!! tip "Nói đơn giản"
    Hãy xem AI như một nhân viên mới rất nhanh nhưng đôi khi nói chắc nịch điều sai. Muốn nhân viên đó làm ổn định thì phải giao việc rõ ràng bằng văn bản, có bài kiểm tra, và có người chịu trách nhiệm xem lại kết quả.

### 3.2 Cấu tạo một bản giao việc (khung 6 phần)

Bảng dưới đây chia một bản giao việc thành 6 phần. Cột cuối là ví dụ ngắn cho việc chăm sóc khách hàng (CSKH).

| Phần | Nội dung | Ví dụ ngắn (CSKH) |
|---|---|---|
| 1. Vai trò | Ai, cho ai, mục tiêu | "Bạn là nhân viên CSKH của cửa hàng X, trả lời khách bằng tiếng Việt lịch sự" |
| 2. Bối cảnh | Dữ kiện nền: chính sách, sản phẩm | "Chính sách đổi trả: ... (dán đoạn chính sách)" |
| 3. Nhiệm vụ | Việc cụ thể | "Soạn thư trả lời cho tin nhắn sau" |
| 4. Các bước | Trình tự từ SOP | "B1 xác định loại yêu cầu; B2 đối chiếu chính sách; B3 soạn thư" |
| 5. Định dạng ra | Cấu trúc đầu ra | "Gồm: Phân loại / Thư trả lời / Điều cần người duyệt" |
| 6. Ràng buộc | Điều không làm, khi nào dừng | "Nếu chính sách không nói, ghi 'CẦN NGƯỜI QUYẾT' và không tự suy đoán" |

(SOP là quy trình làm việc chuẩn của công ty, thường viết thành các bước.)

!!! tip "Nói đơn giản"
    Một bản giao việc tốt trả lời đủ sáu câu hỏi: bạn là ai, bạn biết gì, làm việc gì, làm theo thứ tự nào, trả kết quả dạng nào, và khi nào thì dừng lại hỏi người. Phần 6 là phần hay bị quên nhất, nhưng lại là phần giúp AI không tự đoán bừa.

### 3.3 Thao tác trên công cụ (hay đổi; kiểm tra 2026-11-11)

Phần này nói về ba tính năng cho phép bạn "đóng gói" chỉ dẫn và tài liệu nền để dùng lại. Chúng thay đổi nhanh nên mỗi chỗ có ghi ngày kiểm tra.

- **Claude Projects:** không gian riêng có lịch sử chat và kho kiến thức (các tệp tải lên), có chỉ dẫn riêng cho từng Project. Mọi gói (kể cả miễn phí) đều tạo được; gói Free tối đa 5 Project; chỉ Team và Enterprise có chia sẻ. Ở gói trả phí, khi kiến thức gần đầy giới hạn ngữ cảnh (lượng chữ AI đọc được trong một lần), hệ thống chuyển sang RAG (một kỹ thuật cho AI tìm đúng đoạn cần trong tài liệu thay vì đọc hết) để tăng dung lượng tới 10 lần **[Nguồn: support.claude.com "What are projects", truy cập 2026-11-11]**.
- **Gemini Gems:** phiên bản Gemini được lưu sẵn cho một tác vụ. Cách làm: New Gem, đặt tên, viết chỉ dẫn, tùy chọn thêm tệp kiến thức (từ máy, Google Drive, NotebookLM), thử trong ô xem trước rồi lưu; có thể chia sẻ. **Lưu ý ngày:** trang trợ giúp ghi "từ tháng 11/2026 Gems sẽ bị gỡ khỏi tài khoản Google cá nhân và chuyển sang skills" **[Nguồn: support.google.com/gemini/answer/15146780, truy cập 2026-11-11]**. Cần kiểm tra lại trước khi hướng dẫn nhân viên dùng Gem trên tài khoản cá nhân.
- **ChatGPT custom GPT** (phiên bản ChatGPT do bạn tự cấu hình): trang trợ giúp chính thức về tạo GPT trả lỗi 403 khi truy cập (không đọc được). Mọi chi tiết về GPT tùy chỉnh trong file này là **chưa kiểm chứng**; xem mục 9.

!!! tip "Nói đơn giản"
    Project, Gem và GPT tùy chỉnh đều là một "trợ lý đã được dặn sẵn". Bạn viết chỉ dẫn và đưa tài liệu nền một lần, sau đó đồng nghiệp chỉ việc dùng. Giao diện của các công cụ này hay đổi, nên đừng học thuộc từng nút bấm, hãy nhớ nguyên tắc.

## 4. Chuỗi bài nhỏ

Bảy bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: mục tiêu, việc cần làm, thứ bạn có sau bài, và lỗi hay gặp để tránh.

### Bài C0.1: Kiểm kê cách đang dùng AI (shadow AI audit, nghĩa là rà xem nhân viên đang tự dùng AI "ngầm" như thế nào)
- **Mục tiêu:** biết ai đang dùng công cụ nào, cho việc gì, với dữ liệu gì.
- **Việc cần làm:** (1) Phát bảng khảo sát 6 cột: tên, công cụ, tài khoản cá nhân hay công ty, việc làm, loại dữ liệu đã dán, tần suất. (2) Cam kết không phạt lần này để nhận câu trả lời thật. (3) Gom thành 5-10 "nghiệp vụ ứng viên".
- **Bạn có sau bài:** bảng kiểm kê cùng danh sách nghiệp vụ xếp theo tần suất x rủi ro dữ liệu.
- **Lỗi hay gặp:** hỏi theo kiểu kiểm tra nên không ai khai; chỉ hỏi công cụ mà không hỏi loại dữ liệu.

### Bài C0.2: Viết bản giao việc 6 phần cho một nghiệp vụ
- **Mục tiêu:** một nghiệp vụ lặp lại có prompt chuẩn.
- **Việc cần làm:** chọn nghiệp vụ tần suất cao, rủi ro thấp (ví dụ soạn thư trả lời khách). Điền khung ở mục 3.2. Chạy 3 lần với cùng đầu vào, so sánh độ ổn định. Sửa phần mơ hồ.
- **Bạn có sau bài:** 1 dòng trong Sổ prompt (tên, phiên bản, người chủ, ngày, prompt, đầu vào mẫu).
- **Lỗi hay gặp:** prompt chỉ một câu; không nói định dạng ra; không có điều kiện dừng nên mô hình tự suy đoán.

### Bài C0.3: Chuyển SOP thành prompt
- **Mục tiêu:** biến quy trình viết tay thành các bước mô hình làm theo được.
- **Việc cần làm:** (1) Lấy SOP giấy. (2) Gạch dưới các **điểm quyết định** (nếu A thì B). (3) Mỗi điểm quyết định viết thành quy tắc rõ ràng, kèm "nếu thiếu thông tin thì dừng và hỏi". (4) Phần cần phán đoán của người thì đánh dấu "chuyển người". (5) Thử với 3 ca dễ, 2 ca khó, 2 ca ngoại lệ.
- **Bạn có sau bài:** prompt có các bước đánh số cùng bảng ca thử.
- **Lỗi hay gặp:** dán nguyên SOP dài mà không tách bước; SOP ngầm (chỉ nằm trong đầu nhân viên) chưa được viết ra.
- **Liên hệ bằng chứng:** nghiên cứu Nubank (arXiv 2606.08867) dựng "routine" (một quy trình mẫu cho AI làm theo) từ SOP, dùng ba công cụ và bộ chấm vài trăm nhãn, rollout 1% (tức là mới cho chạy thật ở 1% trường hợp) **[Nguồn, theo tóm tắt người giao việc; chưa đọc lại]**. Đó là cấp cao hơn (C6-C8); ở C0 chỉ lấy ý: SOP là nguyên liệu tốt nhất cho prompt.

### Bài C0.4: Bộ ca thử và "bảng chấm tay"
- **Mục tiêu:** có cách biết một thay đổi làm tốt hay xấu hơn.
- **Việc cần làm:** lập bảng: đầu vào | đầu ra mong đợi | tiêu chí đạt (3-5 ý có/không) | kết quả lần chạy. Mỗi lần sửa prompt hoặc đổi mô hình, chạy lại toàn bộ và đếm số ca đạt.
- **Bạn có sau bài:** bảng ca thử gắn với từng prompt.
- **Lỗi hay gặp:** chỉ thử ca dễ; chỉ chạy một lần (đầu ra có tính ngẫu nhiên, nghĩa là cùng một câu hỏi, mỗi lần AI có thể trả lời khác nhau); không lưu kết quả cũ để so.

### Bài C0.5: Project / Gem / GPT tùy chỉnh cho một nghiệp vụ (đường không code)
- **Mục tiêu:** đóng gói prompt và tài liệu nền để đồng nghiệp dùng lại.
- **Việc cần làm:** tạo Project (Claude) hoặc Gem (Gemini) với chỉ dẫn = phần cố định của bản giao việc; tải 1-3 tài liệu nền (bảng giá, chính sách) đã **gỡ thông tin cá nhân**; chạy bộ ca thử; ghi phiên bản.
- **Bạn có sau bài:** một Project/Gem dùng được, kèm trang "cách dùng" 5 dòng.
- **Lỗi hay gặp:** tải cả thư mục tài liệu nội bộ lên; quên rằng chia sẻ Project chỉ có ở gói Team/Enterprise (Claude), nên người khác không thấy; tài khoản cá nhân của nhân viên nghỉ việc mang theo Project.

### Bài C0.6: Nhận diện lỗi điển hình và quy tắc duyệt
- **Mục tiêu:** biết khi nào không tin đầu ra.
- **Việc cần làm:** chạy "bài thử bẫy": hỏi một sự kiện không có thật, một điều khoản không có trong tài liệu, một phép tính nhiều bước. Ghi lại cách mô hình phản ứng. Lập danh sách kiểm 5 điểm: số liệu đã đối chiếu? trích dẫn có trong tài liệu gốc? tên riêng đúng? có chỗ mô hình tự suy đoán? định dạng đúng?
- **Bạn có sau bài:** danh sách kiểm duyệt dán cạnh mỗi prompt; quy tắc "ai duyệt cái gì".
- **Lỗi hay gặp:** coi giọng văn tự tin là bằng chứng đúng; để AI tự kiểm lại chính nó rồi coi như đã duyệt.

### Bài C0.7: Sổ prompt và quy tắc chung
- **Mục tiêu:** chấm dứt "mỗi người một kiểu".
- **Việc cần làm:** lập một bảng chung với các cột: tên, mục đích, chủ sở hữu, phiên bản, ngày sửa, loại dữ liệu cho phép, công cụ/mô hình dùng, link ca thử. Quy tắc: sửa prompt phải tăng phiên bản và chạy lại ca thử.
- **Bạn có sau bài:** Sổ prompt cùng quy tắc 1 trang.
- **Lỗi hay gặp:** sổ không ai cập nhật; không có chủ sở hữu.

## 5. Đường không code vs đường có code

Bài này có hai đường. Đường không code đủ để bắt đầu. Đường có code nhẹ dành cho lúc khối lượng việc lớn lên.

| | Không code (C0) | Có code nhẹ |
|---|---|---|
| Công cụ | Chat, Project, Gem, GPT tùy chỉnh | Gọi API bằng Python (xem `cap-01-goi-api.md`) |
| Mạnh | Khởi động trong ngày; không cần IT | Lặp lại tự động, hàng loạt; có nhật ký; kiểm soát tham số |
| Yếu | Khó chạy hàng loạt; khó ghi nhật ký; phụ thuộc giao diện đổi; dữ liệu đi qua tài khoản người dùng | Cần người viết/bảo trì mã; phải giữ khóa API an toàn |

(API là "cổng" để một chương trình máy tính gọi AI thay cho người gõ tay. Python là một ngôn ngữ lập trình. Khóa API là chuỗi bí mật như mật khẩu, ai có khóa thì dùng được tài khoản của bạn.)

**Khi buộc phải chuyển sang code (C1)** **[Đề xuất, ngưỡng cần chỉnh theo thực tế]**: (a) cần xử lý hơn khoảng 50-100 tài liệu mỗi lần; (b) cần đầu ra JSON (một cách viết dữ liệu có khung rõ ràng để máy khác đọc được) để đưa vào bảng tính hoặc phần mềm khác; (c) cần nhật ký ai-chạy-gì-lúc-nào; (d) cần tự động theo lịch; (e) cần tính chi phí chính xác theo từng việc.

!!! tip "Nói đơn giản"
    Nếu bạn chỉ làm vài việc mỗi ngày, cứ dùng chat và Project là đủ. Khi phải làm hàng chục tài liệu một lần, cần máy tự chạy theo lịch hoặc cần đếm chi phí từng việc, lúc đó mới nên nhờ người biết lập trình.

## 6. Tiêu chí lên cấp tiếp theo (C0 -> C1) [Đề xuất]

Lên C1 khi **đủ cả** 4 điều kiện đo được:
1. Có >= 3 nghiệp vụ trong Sổ prompt, mỗi nghiệp vụ có >= 5 ca thử.
2. Mỗi prompt đạt >= 80% ca thử trong 3 lần chạy liên tiếp (ngưỡng đề xuất, chỉnh theo rủi ro nghiệp vụ).
3. Có trang quy tắc dữ liệu và >= 90% nhân viên liên quan đã đọc/ký xác nhận.
4. Có ít nhất một nghiệp vụ gặp ngưỡng chuyển ở mục 5 (nếu không gặp, chưa cần lên C1).

Không lên C1 nếu chưa có quy tắc dữ liệu: gọi API chỉ làm lỗi dữ liệu lan nhanh hơn.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Bốn tình huống để bạn dễ hình dung việc áp dụng ở công ty mình:

- **Bán lẻ:** soạn trả lời bình luận/tin nhắn khách theo chính sách đổi trả; viết mô tả sản phẩm từ bảng thông số. Duyệt: nhân viên phụ trách trước khi đăng. Dữ liệu cấm: số điện thoại, địa chỉ khách.
- **Dịch vụ (spa, giáo dục, du lịch):** soạn email báo giá từ bảng giá; tóm tắt cuộc gọi tư vấn đã ẩn danh thành việc cần làm.
- **Kế toán:** giải thích thuật ngữ, soạn mẫu thư nhắc công nợ, lập danh sách kiểm hồ sơ cuối kỳ. Không dùng AI làm nguồn duy nhất cho số liệu thuế/luật: mô hình có thể bịa điều khoản; luôn đối chiếu văn bản gốc. Không dán sao kê, hóa đơn có mã số thuế cá nhân vào tài khoản cá nhân.
- **Nhân sự:** soạn mô tả công việc, câu hỏi phỏng vấn; không dán CV có thông tin cá nhân khi chưa có quy tắc.

## 8. Tài liệu tham khảo

Ngày truy cập tất cả: 2026-11-11 (trừ ghi chú). Mức tin cậy: Cao = tài liệu chính thức của nhà cung cấp/bài báo; Trung bình = bài báo chí/tổng hợp.

| Tiêu đề | URL | Loại | Truy cập | Tin cậy |
|---|---|---|---|---|
| Prompt engineering (OpenAI) | https://developers.openai.com/api/docs/guides/prompt-engineering | Tài liệu nhà cung cấp | 2026-11-11 | Cao |
| Prompt engineering overview (Claude) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Tài liệu nhà cung cấp | 2026-11-11 | Cao |
| What are projects? (Claude) | https://support.claude.com/en/articles/9517075-what-are-projects | Trợ giúp nhà cung cấp | 2026-11-11 | Cao |
| Gems (Gemini Apps Help) | https://support.google.com/gemini/answer/15146780 | Trợ giúp nhà cung cấp | 2026-11-11 | Cao |
| MAP, arXiv 2512.04123 | https://arxiv.org/abs/2512.04123 | Bài báo | đã đọc trước (theo người giao việc); không đọc lại | Cao (chưa xác minh lại trong phiên này) |
| Nubank, arXiv 2606.08867 | https://arxiv.org/abs/2606.08867 | Bài báo | như trên | Cao (chưa xác minh lại) |

## 9. Chưa kiểm chứng / cần kiểm tra lại

- Chi tiết tạo/chia sẻ **custom GPT** của ChatGPT: trang trợ giúp OpenAI trả 403, chưa đọc được. Cần mở bằng trình duyệt và ghi lại gói nào có, cách chia sẻ.
- Dung lượng tệp và số tệp tối đa của Project/Gem: chưa đọc.
- Việc Gems chuyển thành skills từ 11/2026: mới đọc một dòng thông báo, chưa rõ phạm vi (tài khoản Workspace có bị ảnh hưởng không).
- Các số liệu MAP/Nubank trong file này lấy từ tóm tắt đầu bài, chưa đọc lại bản gốc trong phiên này.
- Ngưỡng 80%, 90%, 50-100 tài liệu là **đề xuất của chúng tôi**, chưa có thực nghiệm.
- Tỷ lệ bịa/sai của từng mô hình: chưa tìm nguồn định lượng đáng tin cho nghiệp vụ SME; đừng trích số nào khi chưa có nguồn.
