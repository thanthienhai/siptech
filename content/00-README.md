# Series: AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp

Tổng hợp ngày 2026-11-11. Đây là bộ tài liệu nghiên cứu làm nền cho series hướng dẫn, chưa phải nội dung series hoàn chỉnh.

## 1. Ý tưởng cốt lõi

Doanh nghiệp nhỏ ít tiền, chưa có quy trình, khó xây hệ thống riêng. Series đi theo **thang cấp độ**: mỗi cấp là một khối nhỏ chạy được độc lập, có sản phẩm cầm đi được, và có tiêu chí đo được để biết khi nào mới lên cấp. Mỗi cấp có hai đường: **không code** (Project, Gem, GPT tùy chỉnh) và **code nhẹ** (Python).

Ví dụ xuyên suốt là hệ thống tra cứu thông tin nội bộ: gọi AI thủ công → API → biến tài liệu thành text → chia khối → tìm kiếm → trả lời có trích dẫn → đánh giá → công cụ → quy trình nhiều bước → vận hành.

## 2. Mục lục

Cấu trúc thư mục: các file nền (bằng chứng, thực trạng, pháp lý) dùng chung nằm ở gốc. Mỗi bài toán là một thư mục riêng, có `00-README.md` và thang cấp độ riêng. Các nhóm sau tham chiếu lại khối chung của nhóm RAG (C0 dùng thủ công, C1 API, C2 tài liệu thành text, C6 đánh giá, C7 công cụ, C9 vận hành) thay vì viết lại.

| Thư mục | Bài toán | Thang cấp | Đầu ra |
|---|---|---|---|
| `rag-tra-cuu-tai-lieu/` | Tra cứu thông tin trên một tập tài liệu | C0-C9 | Câu trả lời có trích dẫn |
| `xu-ly-yeu-cau-khach/` | Xử lý yêu cầu khách theo SOP (Zalo, email, đổi trả, khiếu nại) | 7 cấp | Bản nháp trả lời, quyết định, hành động có duyệt |
| `kiem-tra-ho-so-theo-quy-tac/` | Chứng từ thành dữ liệu, kiểm theo quy tắc, đối chiếu ba bên, rà hợp đồng | K0-K7 | Danh sách lỗi có căn cứ |
| `tri-thuc-to-chuc/` | Biên bản họp, SOP từ người giỏi, bàn giao, giữ tài liệu cập nhật | 8 cấp | Tài liệu và SOP đã duyệt (đầu vào cho các nhóm khác) |
| `quy-trinh-nhieu-buoc/` | Vẽ quy trình, định tuyến, báo cáo định kỳ, chuỗi bước có duyệt | Q0-Q6 | Quy trình chạy tự động có điểm duyệt và số đo trước/sau |

Gợi ý thứ tự cho SME chưa có quy trình: `tri-thuc-to-chuc` (cấp đầu: viết SOP) → `xu-ly-yeu-cau-khach` hoặc `kiem-tra-ho-so-theo-quy-tac` → `rag-tra-cuu-tai-lieu` → `quy-trinh-nhieu-buoc`. Đây là [Đề xuất], không có nguồn đo.

Các file của nhóm RAG:

| File | Nội dung |
|---|---|
| `nen-tang-bang-chung.md` | Các bài báo đã đọc kỹ (MAP, Nubank, Airbnb, BMO, SAP) và các khảo sát ngành |
| `thuc-trang-sme-viet-nam.md` | Kiểm chứng giả thuyết "SME VN dùng AI vô tội vạ" |
| `an-toan-du-lieu-va-phap-ly-vn.md` | Dữ liệu nào được đưa vào AI; pháp luật VN (chưa xác minh toàn văn) |
| `rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` | Dùng chat/Project/Gem; prompt như bản giao việc; SOP thành prompt |
| `rag-tra-cuu-tai-lieu/cap-01-goi-api.md` | Gọi API, chi phí token, structured output, xử lý lỗi |
| `rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` | PDF/scan thành text có cấu trúc; OCR vs mô hình thị giác; kiểm chất lượng |
| `rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` | Chia khối theo tiêu đề; mã ổn định; lớp điều hướng; cập nhật khi tài liệu đổi |
| `rag-tra-cuu-tai-lieu/cap-04-tim-kiem.md` | BM25, vector, lai; tiếng Việt; tự đo chất lượng tìm kiếm |
| `rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md` | Trả lời từ nguồn; kiểm trích nguyên văn bằng code; từ chối khi thiếu căn cứ |
| `rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` | Bộ ca mẫu; LLM-as-judge và thiên lệch; khoảng tin cậy khi n nhỏ |
| `rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` | Function calling; hàm đọc/ghi; prompt injection; MCP |
| `rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` | Workflow vs agent; điểm duyệt của người; 3 tình huống SME |
| `rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` | Log; phiên bản prompt; kiểm tra trước khi phát hành; trôi dạt; khi nào nâng cấp |

Thứ tự đọc cho người làm series: `nen-tang-bang-chung` → `thuc-trang-sme-viet-nam` → `an-toan-du-lieu-va-phap-ly-vn` → các cấp 00 đến 09.

## 3. Điều rút ra từ bằng chứng

### Chung cho 5 nhóm (từ báo cáo của 4 nhóm mới; chi tiết và nguồn ở README từng thư mục)

- **Chính sách và SOP có chỗ trống thì AI tự điền, mỗi lần một kiểu** (Policy Loopholes 2609.14400). Viết SOP là bước đầu ở cả nhóm khách hàng lẫn nhóm tri thức.
- **Một lần đúng chưa đủ:** τ-bench gpt-4o pass^1 trên 60% nhưng pass^8 dưới 25%; 14 triển khai LLM thương mại đều trả kết quả khác nhau cho cùng yêu cầu. Quy tắc tính được thì viết bằng code.
- **Số liệu và bảng tính phải do code tính:** SpreadsheetBench 2 tốt nhất 34,89%; nhắc "đừng trích sai" trong prompt gần như không giảm lỗi.
- **Độ tự tin mô hình tự báo không lọc được trường trích sai** (AUC 0,69-0,74); kiểm "giá trị có xuất hiện nguyên văn trong chứng từ" bằng code rẻ và chắc hơn.
- **Agent tự làm trọn việc văn phòng còn yếu** (TheAgentCompany: hành chính 13,33%, tài chính 8,33%).
- **Tiếng Việt kém hơn tiếng Anh** ở cả hội thoại khách hàng (SEATauBench 0,52 so với 0,62) lẫn chép lời (dịch vụ dao động 6,7%-50,8% câu sai nghĩa).
- **Năng suất tự ước cao hơn thực đo** (thí nghiệm Copilot: ước 36 phút, đo 12 phút). Nhóm quy trình dạy đo trước/sau.

Các số trên do agent đọc và báo lại; trong bước rà soát tôi chưa đối chiếu lại từng số với bài gốc.

### Từ các bài đã đọc kỹ

Mỗi nhận định có nguồn trong `nen-tang-bang-chung.md`.

1. Hệ thống chạy thật đều hẹp và có kiểm soát: 70% dùng prompt trên mô hình có sẵn, 68% chạy dưới 10 bước rồi chuyển cho người (MAP). Điều này làm cho hướng "khối nhỏ trước" hợp lý.
2. Chất lượng nằm nhiều ở nội dung và quy trình hơn ở công nghệ truy xuất: các biến thể tìm kiếm của Airbnb không khác nhau có ý nghĩa thống kê, còn phần thất bại còn lại chủ yếu do SOP thiếu bước. Đây là việc SME làm được mà không cần nhiều tiền.
3. Công thức chung ở các ca lớn: SOP → quy trình từng bước → bộ ca mẫu có đáp án → rollout nhỏ → sửa có kiểm soát.
4. Hàng rào bằng code (ví dụ kiểm trích nguyên văn) đáng tin hơn hàng rào bằng prompt.

## 4. Giới hạn của chính bộ tài liệu

- **Mọi bằng chứng định lượng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.** Không có nguồn nào đo trực tiếp trên SME Việt Nam.
- **Giả thuyết "vô tội vạ" chỉ được ủng hộ gián tiếp** (xem `thuc-trang-sme-viet-nam.md`). Khuyến nghị: trình bày là quan sát của tác giả, và dùng bộ câu hỏi khảo sát gợi ý trong file đó để thu dữ liệu gốc từ người học.
- **Các ngưỡng và cỡ mẫu** (ví dụ bộ 20-30 ca, ngưỡng recall, ngưỡng lên cấp) là đề xuất của nhóm, không có nguồn. Với n nhỏ như vậy khoảng tin cậy rất rộng: bộ 20-30 ca chỉ phát hiện hỏng, không đo chính xác (xem `cap-06`).
- Mỗi file cấp tách rõ **[Nguồn]** (kết quả trong tài liệu) và **[Đề xuất]** (suy luận của nhóm).

## 5. Việc phải kiểm tra trước khi xuất bản

Gom từ báo cáo của 6 agent; chi tiết nằm ở mục 9 của từng file.

**Pháp lý (rủi ro cao nhất):**
- Chưa đọc toàn văn Luật 91/2025/QH15, Nghị định 356/2025/NĐ-CP, Luật 71/2025/QH15, Luật AI 134/2025/QH15. Các trang `thuvienphapluat` trả lỗi 403; bản .doc của NĐ 356 trên `vbpl.moj.gov.vn` chưa tải.
- Số điều về chuyển dữ liệu ra nước ngoài còn lệch giữa các nguồn thứ cấp (Điều 20 của Luật, hay Điều 18 của NĐ 356).
- Chưa xác minh: mức phạt, Nghị định 142/2026/NĐ-CP, thời hạn chuyển tiếp 12/18 tháng của Luật AI, Luật Dữ liệu 2024.
- File chỉ là tổng hợp thứ cấp, **không phải tư vấn pháp lý**. Cần luật sư hoặc đọc văn bản gốc trước khi dạy người khác.

- **Hóa đơn điện tử:** NĐ 123/2020/NĐ-CP và NĐ 70/2025/NĐ-CP đã được thay bằng NĐ 254/2026/NĐ-CP (hiệu lực 01/7/2026, hướng dẫn Luật Quản lý thuế 108/2025/QH15), kèm TT 91/2026/TT-BTC. Đã kiểm qua tìm kiếm (thuvienphapluat, Công văn 4831/CT-CS của Cục Thuế qua luatvietnam), chưa đọc văn bản gốc. Tên thẻ XML hóa đơn chưa xác minh.
- **Luật Bảo vệ quyền lợi người tiêu dùng 19/2023/QH15** (Điều 10, Điều 31) và NĐ 55/2024; **Luật 91/2025** Điều 25, 32 (dữ liệu nhân viên, ghi âm): mới đọc qua nguồn thứ cấp.
- Mỗi thư mục bài toán có danh sách kiểm chứng riêng trong `00-README.md` và mục 9 của từng cấp.

**Công cụ và điều khoản (thay đổi nhanh):**
- API và webhook của KiotViet, Sapo, MISA; giá và tiêu chí duyệt Zalo ZNS/ZBS; Lark Approval; Meet/Teams/Zoom/Lark có chép lời tiếng Việt hay không: chưa xác minh.
- Điều khoản dữ liệu và tính năng của Claude, ChatGPT, Gemini: một số trang (OpenAI consumer, hướng dẫn GPT tùy chỉnh) trả lỗi 403, chỉ có tóm tắt tìm kiếm. Trang Google nêu Gemini Gems sẽ chuyển sang skills từ 11/2026.
- Chưa đọc cách gọi Gemini API, function calling của Gemini, Make; Zapier chỉ qua blog.
- Chưa xác minh Google Document AI hỗ trợ tiếng Việt, Azure Invoice có locale `vi`.
- Chính sách ngừng mô hình của OpenAI và Google chưa tra (của Anthropic đã đọc ngày 2026-11-11).
- Giá API không ghi số, chỉ ghi cách tự tính.

**Tiếng Việt (không có nguồn đo):**
- Không có nguồn nào đo OCR/trích xuất trên tài liệu SME Việt Nam.
- Số MIRACL của M3 và mE5 không gồm tiếng Việt; số tiếng Việt chỉ có ở VN-MTEB (dịch máy) và MKQA (chéo ngôn ngữ).
- Chưa có nguồn cho việc tách từ hoặc bỏ dấu có giúp BM25 tiếng Việt hay không. Người học phải tự thử bằng bộ câu hỏi riêng.
- Độ tin cậy của RAGAS và LLM judge trên tiếng Việt chưa có dữ liệu.

**Kỹ thuật:**
- Công thức RRF và k=60 chỉ có từ bài thứ cấp.
- Docling, Marker, MarkItDown chưa chạy thử; HybridChunker của Docling chỉ qua tóm tắt.
- Code mẫu đã chạy thử với `python -I` ở scratchpad (BM25, FTS5, validator trích dẫn, chia khối, CER, kiểm tổng hóa đơn, Wilson, kappa, ghi log, tính chi phí, hàm công cụ giả). Chưa chạy với API thật. Đoạn RRF chưa chạy thử; code nhúng vector chưa viết.
- Hai p-value của test dấu trong `cap-06` (0,22 và 0,008) mới tính tay.

**Đã kiểm trong bước rà soát (2026-11-11):**
- Số liệu MAP, Nubank, Airbnb, BMO trong các file cấp khớp với toàn văn các bài đã đọc.
- Các số ablation Airbnb trong `cap-03` khớp Bảng 5 của bài.
- Khoảng Wilson 18/20 ≈ 70-97% và pass^3 = 0,75³ ≈ 42% đúng.
- Chưa kiểm: từng URL trong mục tài liệu tham khảo (các agent ghi mức tin cậy cho mỗi mục), và các trích dẫn từ trang web đọc qua công cụ tóm tắt.

## 6. Bước tiếp theo đề xuất

1. Đọc `thuc-trang-sme-viet-nam.md` và quyết định cách trình bày vấn đề trong series.
2. Chọn một ngành và một bộ tài liệu thật (bảng giá, chính sách, hợp đồng) để làm ví dụ xuyên suốt.
3. Biến từng cấp thành bài: kịch bản, bộ tài liệu mẫu, mã mẫu, bộ ca mẫu có đáp án.
4. Trước khi xuất bản: kiểm pháp lý bằng văn bản gốc, kiểm lại tính năng công cụ, và đo thử chất lượng trên tài liệu tiếng Việt thật.
