# Cấp 0 (C0): Dùng AI thủ công một cách có kỷ luật

> Ngày soạn: 2026-11-11. Phần "nguyên tắc" là bền; phần "thao tác trên giao diện" hay đổi, mỗi chỗ có ghi ngày kiểm tra.
> Quy ước: **[Nguồn]** = kết quả đọc được trong nguồn; **[Đề xuất]** = đề xuất của chúng tôi, chưa có bằng chứng định lượng.
> Không phải tư vấn pháp lý. Phần dữ liệu và luật xem file `../an-toan-du-lieu-va-phap-ly-vn.md`.

## 1. Mục tiêu và người đọc

**Người đọc:** chủ SME, kế toán, nhân viên bán hàng/CSKH/vận hành ở Việt Nam, chưa có quy trình AI, đang dùng Claude/ChatGPT/Gemini "mỗi người một kiểu". Không cần biết code.

**Mục tiêu sau cấp này** (đo được):
1. Mỗi nghiệp vụ lặp lại có **một bản giao việc (prompt)** chuẩn lưu ở một chỗ chung, ai dùng cũng ra kết quả tương tự.
2. Mỗi bản giao việc có **5-10 ca thử** (đầu vào mẫu + đầu ra mong đợi) để kiểm tra khi đổi mô hình hay sửa prompt.
3. Mọi người biết **quy tắc dữ liệu**: cái gì không dán vào AI.
4. Có **người duyệt** (con người) cho mọi đầu ra đi ra ngoài công ty.

**Sản phẩm cầm đi được:** một "Sổ prompt" (bảng tính hoặc tài liệu) + một Project/Gem/GPT cho 1-3 nghiệp vụ + một trang quy tắc dữ liệu 1 tờ A4.

## 2. Câu hỏi cấp này trả lời / vì sao có cấp này

Cấp 0 là điểm xuất phát, không có "lỗi của cấp trước". Câu hỏi: *"Làm sao dùng công cụ AI có sẵn cho ổn định, an toàn, lặp lại được, trước khi bỏ tiền làm gì to hơn?"*

Bằng chứng về thực tế dùng agent/AI trong doanh nghiệp (**[Nguồn]**, bài MAP arXiv 2512.04123; các số này đã được đối chiếu với toàn văn bài ở bước rà soát ngày 2026-11-11): 70% dùng prompt trên mô hình có sẵn thay vì huấn luyện; 68% chạy dưới 10 bước rồi chuyển cho người; 74% đánh giá bằng người; 52% agent phục vụ nhân viên nội bộ. **[Đề xuất]** Ý nghĩa cho SME: bắt đầu bằng prompt + người duyệt là hợp với thực tế các tổ chức đã triển khai, không phải là "làm cho qua".

Dấu hiệu cần Cấp 0 có kỷ luật: nhân viên dùng tài khoản cá nhân; cùng một việc mỗi người hỏi một kiểu; không ai biết kết quả đúng hay sai; không rõ dữ liệu khách đã bị dán đi đâu (xem file an toàn dữ liệu).

## 3. Kiến thức nền (ngắn, chính xác)

### 3.1 Nguyên tắc (bền)

- **Prompt là bản giao việc.** Hướng dẫn của OpenAI mô tả cấu trúc điển hình của một prompt: Identity (vai trò, phong cách, mục tiêu), Instructions (quy tắc, điều không được làm), Examples (đầu vào mẫu và đầu ra mong muốn, nên đa dạng), Context (dữ liệu bổ sung, thường đặt gần cuối prompt) **[Nguồn: OpenAI Prompt engineering guide]**. Tài liệu Claude yêu cầu có trước: tiêu chí thành công rõ ràng, cách kiểm thử bằng thực nghiệm, và bản nháp đầu tiên **[Nguồn: Claude Prompt engineering overview]**.
- **Tách phần cố định và phần thay đổi.** Phần cố định (vai trò, quy tắc, định dạng) đặt vào chỉ dẫn của Project/Gem/GPT; phần thay đổi (tài liệu hôm nay) dán vào từng lần chạy. **[Đề xuất]**
- **Đo bằng ca thử.** Cả hai nhà cung cấp khuyến nghị có bộ đánh giá (evals) trước khi đổi prompt hay nâng cấp mô hình **[Nguồn: OpenAI; Claude]**. Ở C0, "bộ đánh giá" chỉ là bảng 5-10 dòng.
- **Con người chịu trách nhiệm.** Mô hình có thể bịa và tự tin sai (hallucination); không có công cụ C0 nào loại bỏ hoàn toàn điều này. **[Đề xuất]** Quy tắc: số liệu, trích dẫn luật, giá, tên người/công ty phải được người đối chiếu nguồn gốc trước khi dùng.

### 3.2 Cấu tạo một bản giao việc (khung 6 phần)

| Phần | Nội dung | Ví dụ ngắn (CSKH) |
|---|---|---|
| 1. Vai trò | Ai, cho ai, mục tiêu | "Bạn là nhân viên CSKH của cửa hàng X, trả lời khách bằng tiếng Việt lịch sự" |
| 2. Bối cảnh | Dữ kiện nền: chính sách, sản phẩm | "Chính sách đổi trả: ... (dán đoạn chính sách)" |
| 3. Nhiệm vụ | Việc cụ thể | "Soạn thư trả lời cho tin nhắn sau" |
| 4. Các bước | Trình tự từ SOP | "B1 xác định loại yêu cầu; B2 đối chiếu chính sách; B3 soạn thư" |
| 5. Định dạng ra | Cấu trúc đầu ra | "Gồm: Phân loại / Thư trả lời / Điều cần người duyệt" |
| 6. Ràng buộc | Điều không làm, khi nào dừng | "Nếu chính sách không nói, ghi 'CẦN NGƯỜI QUYẾT' và không tự suy đoán" |

### 3.3 Thao tác trên công cụ (hay đổi; kiểm tra 2026-11-11)

- **Claude Projects:** không gian riêng có lịch sử chat và kho kiến thức (tệp tải lên), có chỉ dẫn riêng cho từng Project. Mọi gói (kể cả miễn phí) đều tạo được; gói Free tối đa 5 Project; chỉ Team và Enterprise có chia sẻ. Ở gói trả phí, khi kiến thức gần đầy giới hạn ngữ cảnh, hệ thống chuyển sang RAG để tăng dung lượng tới 10 lần **[Nguồn: support.claude.com "What are projects", truy cập 2026-11-11]**.
- **Gemini Gems:** phiên bản Gemini được lưu sẵn cho một tác vụ: New Gem, đặt tên, viết chỉ dẫn, tùy chọn thêm tệp kiến thức (từ máy, Google Drive, NotebookLM), thử trong ô xem trước rồi lưu; có thể chia sẻ. **Lưu ý ngày:** trang trợ giúp ghi "từ tháng 11/2026 Gems sẽ bị gỡ khỏi tài khoản Google cá nhân và chuyển sang skills" **[Nguồn: support.google.com/gemini/answer/15146780, truy cập 2026-11-11]**. Cần kiểm tra lại trước khi hướng dẫn nhân viên dùng Gem trên tài khoản cá nhân.
- **ChatGPT custom GPT:** trang trợ giúp chính thức về tạo GPT trả lỗi 403 khi truy cập (không đọc được). Mọi chi tiết về GPT tùy chỉnh trong file này là **chưa kiểm chứng**; xem mục 9.

## 4. Chuỗi bài nhỏ

### Bài C0.1: Kiểm kê cách đang dùng AI (shadow AI audit)
- **Mục tiêu:** biết ai đang dùng công cụ nào, cho việc gì, với dữ liệu gì.
- **Thực hành:** (1) Phát bảng khảo sát 6 cột: tên, công cụ, tài khoản cá nhân hay công ty, việc làm, loại dữ liệu đã dán, tần suất. (2) Cam kết không phạt lần này để nhận câu trả lời thật. (3) Gom thành 5-10 "nghiệp vụ ứng viên".
- **Sản phẩm:** bảng kiểm kê + danh sách nghiệp vụ xếp theo tần suất x rủi ro dữ liệu.
- **Lỗi thường gặp:** hỏi theo kiểu kiểm tra nên không ai khai; chỉ hỏi công cụ mà không hỏi loại dữ liệu.

### Bài C0.2: Viết bản giao việc 6 phần cho một nghiệp vụ
- **Mục tiêu:** một nghiệp vụ lặp lại có prompt chuẩn.
- **Thực hành:** chọn nghiệp vụ tần suất cao, rủi ro thấp (ví dụ soạn thư trả lời khách). Điền khung 3.2. Chạy 3 lần với cùng đầu vào, so sánh độ ổn định. Sửa phần mơ hồ.
- **Sản phẩm:** 1 dòng trong Sổ prompt (tên, phiên bản, người chủ, ngày, prompt, đầu vào mẫu).
- **Lỗi thường gặp:** prompt chỉ một câu; không nói định dạng ra; không có điều kiện dừng nên mô hình tự suy đoán.

### Bài C0.3: Chuyển SOP thành prompt
- **Mục tiêu:** biến quy trình viết tay thành các bước mô hình làm theo được.
- **Thực hành:** (1) Lấy SOP giấy. (2) Gạch dưới các **điểm quyết định** (nếu A thì B). (3) Mỗi điểm quyết định viết thành quy tắc rõ ràng, kèm "nếu thiếu thông tin thì dừng và hỏi". (4) Phần cần phán đoán của người thì đánh dấu "chuyển người". (5) Thử với 3 ca dễ, 2 ca khó, 2 ca ngoại lệ.
- **Sản phẩm:** prompt có các bước đánh số + bảng ca thử.
- **Lỗi thường gặp:** dán nguyên SOP dài mà không tách bước; SOP ngầm (chỉ nằm trong đầu nhân viên) chưa được viết ra.
- **Liên hệ bằng chứng:** nghiên cứu Nubank (arXiv 2606.08867) dựng "routine" từ SOP, dùng ba công cụ và bộ chấm vài trăm nhãn, rollout 1% **[Nguồn, theo tóm tắt người giao việc; chưa đọc lại]**. Đó là cấp cao hơn (C6-C8); ở C0 chỉ lấy ý: SOP là nguyên liệu tốt nhất cho prompt.

### Bài C0.4: Bộ ca thử và "bảng chấm tay"
- **Mục tiêu:** có cách biết một thay đổi làm tốt hay xấu hơn.
- **Thực hành:** lập bảng: đầu vào | đầu ra mong đợi | tiêu chí đạt (3-5 ý có/không) | kết quả lần chạy. Mỗi lần sửa prompt hoặc đổi mô hình, chạy lại toàn bộ và đếm số ca đạt.
- **Sản phẩm:** bảng ca thử gắn với từng prompt.
- **Lỗi thường gặp:** chỉ thử ca dễ; chỉ chạy một lần (đầu ra có tính ngẫu nhiên); không lưu kết quả cũ để so.

### Bài C0.5: Project / Gem / GPT tùy chỉnh cho một nghiệp vụ (đường không code)
- **Mục tiêu:** đóng gói prompt + tài liệu nền để đồng nghiệp dùng lại.
- **Thực hành:** tạo Project (Claude) hoặc Gem (Gemini) với chỉ dẫn = phần cố định của bản giao việc; tải 1-3 tài liệu nền (bảng giá, chính sách) đã **gỡ thông tin cá nhân**; chạy bộ ca thử; ghi phiên bản.
- **Sản phẩm:** một Project/Gem dùng được, kèm trang "cách dùng" 5 dòng.
- **Lỗi thường gặp:** tải cả thư mục tài liệu nội bộ lên; quên rằng chia sẻ Project chỉ có ở gói Team/Enterprise (Claude), nên người khác không thấy; tài khoản cá nhân của nhân viên nghỉ việc mang theo Project.

### Bài C0.6: Nhận diện lỗi điển hình và quy tắc duyệt
- **Mục tiêu:** biết khi nào không tin đầu ra.
- **Thực hành:** chạy "bài thử bẫy": hỏi một sự kiện không có thật, một điều khoản không có trong tài liệu, một phép tính nhiều bước. Ghi lại cách mô hình phản ứng. Lập danh sách kiểm 5 điểm: số liệu đã đối chiếu? trích dẫn có trong tài liệu gốc? tên riêng đúng? có chỗ mô hình tự suy đoán? định dạng đúng?
- **Sản phẩm:** danh sách kiểm duyệt dán cạnh mỗi prompt; quy tắc "ai duyệt cái gì".
- **Lỗi thường gặp:** coi giọng văn tự tin là bằng chứng đúng; để AI tự kiểm lại chính nó rồi coi như đã duyệt.

### Bài C0.7: Sổ prompt và quy tắc chung
- **Mục tiêu:** chấm dứt "mỗi người một kiểu".
- **Thực hành:** một bảng chung: tên, mục đích, chủ sở hữu, phiên bản, ngày sửa, loại dữ liệu cho phép, công cụ/mô hình dùng, link ca thử. Quy tắc: sửa prompt phải tăng phiên bản và chạy lại ca thử.
- **Sản phẩm:** Sổ prompt + quy tắc 1 trang.
- **Lỗi thường gặp:** sổ không ai cập nhật; không có chủ sở hữu.

## 5. Đường không code vs đường có code

| | Không code (C0) | Có code nhẹ |
|---|---|---|
| Công cụ | Chat, Project, Gem, GPT tùy chỉnh | Gọi API bằng Python (xem `cap-01-goi-api.md`) |
| Mạnh | Khởi động trong ngày; không cần IT | Lặp lại tự động, hàng loạt; có nhật ký; kiểm soát tham số |
| Yếu | Khó chạy hàng loạt; khó ghi nhật ký; phụ thuộc giao diện đổi; dữ liệu đi qua tài khoản người dùng | Cần người viết/bảo trì mã; phải giữ khóa API an toàn |

**Khi buộc phải chuyển sang code (C1)** **[Đề xuất, ngưỡng cần chỉnh theo thực tế]**: (a) cần xử lý hơn khoảng 50-100 tài liệu mỗi lần; (b) cần đầu ra JSON để đưa vào bảng tính/phần mềm khác; (c) cần nhật ký ai-chạy-gì-lúc-nào; (d) cần tự động theo lịch; (e) cần tính chi phí chính xác theo từng việc.

## 6. Tiêu chí lên cấp tiếp theo (C0 -> C1) [Đề xuất]

Lên C1 khi **đủ cả** 4 điều kiện đo được:
1. Có >= 3 nghiệp vụ trong Sổ prompt, mỗi nghiệp vụ có >= 5 ca thử.
2. Mỗi prompt đạt >= 80% ca thử trong 3 lần chạy liên tiếp (ngưỡng đề xuất, chỉnh theo rủi ro nghiệp vụ).
3. Có trang quy tắc dữ liệu và >= 90% nhân viên liên quan đã đọc/ký xác nhận.
4. Có ít nhất một nghiệp vụ gặp ngưỡng chuyển ở mục 5 (nếu không gặp, chưa cần lên C1).

Không lên C1 nếu chưa có quy tắc dữ liệu: gọi API chỉ làm lỗi dữ liệu lan nhanh hơn.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

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
