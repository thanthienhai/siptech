date: 2026-11-11

# AI cho SME Việt Nam: từ khối nhỏ nhất đến nghiệp vụ phức tạp

Doanh nghiệp nhỏ thường ít tiền, chưa có quy trình và khó xây hệ thống riêng. Vì vậy series này không bắt đầu bằng "xây một hệ thống AI", mà đi theo **thang cấp độ**: mỗi cấp là một khối nhỏ chạy được độc lập, có sản phẩm cầm đi được, và có tiêu chí đo được để biết khi nào mới nên lên cấp. Trang này là cổng vào: ý tưởng chung, danh sách bài toán, điều rút ra từ bằng chứng và giới hạn của bộ tài liệu.

!!! note "Đây là tài liệu nghiên cứu nền"
    Bộ tài liệu tổng hợp ngày 11/11/2026, làm nền cho series hướng dẫn, chưa phải nội dung series hoàn chỉnh. Mỗi bài tách rõ điều **có nguồn** (nhãn [[S1]], bấm để mở nguồn) và điều **SIPTech đề xuất** (khung màu xanh).

## Ý tưởng cốt lõi: thang cấp độ

Mỗi cấp có hai đường đi:

- **Không code:** dùng công cụ có sẵn như Project, Gem hay GPT tùy chỉnh của Claude, ChatGPT, Gemini.
- **Code nhẹ:** vài chục dòng Python khi cần tự động hóa hoặc kiểm tra bằng máy.

Ví dụ xuyên suốt là hệ thống tra cứu thông tin nội bộ. Nó đi qua mười cấp: dùng AI thủ công, gọi API, biến tài liệu thành văn bản, chia khối, tìm kiếm, trả lời có trích dẫn, đánh giá, công cụ, quy trình nhiều bước, và vận hành. Các bài toán khác dùng lại những khối chung này (dùng AI thủ công, gọi API, tài liệu thành văn bản, đánh giá, công cụ, vận hành) thay vì viết lại.

## Các bài toán

| Bài toán | Việc cần giải | Thang cấp | Đầu ra |
|---|---|---|---|
| [Tra cứu tài liệu nội bộ](rag-tra-cuu-tai-lieu/00-README.md) | Hỏi đáp trên bảng giá, chính sách, hợp đồng | C0 đến C9 | Câu trả lời có trích dẫn |
| [Xử lý yêu cầu khách hàng](xu-ly-yeu-cau-khach/00-README.md) | Zalo, email, đổi trả, khiếu nại theo SOP | 7 cấp | Bản nháp trả lời, quyết định, hành động có duyệt |
| [Kiểm tra hồ sơ, chứng từ](kiem-tra-ho-so-theo-quy-tac/00-README.md) | Chứng từ thành dữ liệu, kiểm theo quy tắc, đối chiếu ba bên, rà hợp đồng | K0 đến K7 | Danh sách lỗi có căn cứ |
| [Tri thức tổ chức](tri-thuc-to-chuc/00-README.md) | Biên bản họp, SOP từ người giỏi, bàn giao, giữ tài liệu cập nhật | 8 cấp | Tài liệu và SOP đã duyệt (đầu vào cho các nhóm khác) |
| [Quy trình nhiều bước](quy-trinh-nhieu-buoc/00-README.md) | Vẽ quy trình, định tuyến, báo cáo định kỳ, chuỗi bước có duyệt | Q0 đến Q6 | Quy trình chạy tự động có điểm duyệt và số đo trước và sau |

Danh sách này tiếp tục được bổ sung. Xem [tất cả bài toán](bai-toan.html) để thấy bài mới và bài đang soạn.

!!! proposal "Nên bắt đầu từ đâu? (đề xuất của SIPTech, không có nguồn đo)"
    Với doanh nghiệp chưa có quy trình: **Tri thức tổ chức** (cấp đầu là viết SOP), rồi **Xử lý yêu cầu khách hàng** hoặc **Kiểm tra hồ sơ**, rồi **Tra cứu tài liệu**, cuối cùng **Quy trình nhiều bước**.

## Điều rút ra từ bằng chứng

### Từ các bài đã đọc kỹ

Nền tảng là năm bài báo về hệ thống chạy thật, chi tiết ở [Nền tảng bằng chứng](nen-tang-bang-chung.md).

1. **Hệ thống chạy thật đều hẹp và có kiểm soát:** 70% dùng prompt trên mô hình có sẵn, 68% chạy dưới 10 bước rồi chuyển cho người [[S1]]. Điều này làm cho hướng "khối nhỏ trước" hợp lý.
2. **Chất lượng nằm nhiều ở nội dung và quy trình hơn ở công nghệ truy xuất:** các biến thể tìm kiếm của Airbnb không khác nhau có ý nghĩa thống kê, còn phần thất bại còn lại chủ yếu do SOP thiếu bước [[S2]]. SME làm được việc này mà không cần nhiều tiền.
3. **Công thức chung ở các ca lớn:** SOP, quy trình từng bước, bộ ca mẫu có đáp án, triển khai nhỏ, sửa có kiểm soát [[S1]] [[S2]].
4. **Hàng rào bằng code đáng tin hơn hàng rào bằng prompt**, ví dụ kiểm trích dẫn nguyên văn bằng code [[S2]].

### Chung cho các nhóm bài

Các số dưới đây do SIPTech tổng hợp từ báo cáo của từng nhóm bài. Trong bước rà soát, chúng tôi chưa đối chiếu lại từng số với bài gốc.

- **Chính sách và SOP có chỗ trống thì AI tự điền, mỗi lần một kiểu** [[S3]]. Viết SOP là bước đầu ở cả nhóm khách hàng lẫn nhóm tri thức.
- **Một lần đúng chưa đủ:** gpt-4o có tỷ lệ đạt lần đầu trên 60% nhưng chỉ dưới 25% số việc đạt cả 8 lần liên tiếp [[S4]]; 14 triển khai LLM thương mại đều có lúc trả kết quả khác nhau cho cùng yêu cầu [[S5]]. Quy tắc tính được thì viết bằng code.
- **Số liệu và bảng tính phải do code tính:** mô hình tốt nhất trên SpreadsheetBench 2 đúng trọn việc 34,89% [[S6]]; nhắc "đừng trích sai" trong prompt gần như không giảm lỗi.
- **Độ tự tin mô hình tự báo không lọc được trường trích sai** (AUC 0,69 đến 0,74) [[S7]]. Kiểm "giá trị có xuất hiện nguyên văn trong chứng từ" bằng code rẻ và chắc hơn.
- **Agent tự làm trọn việc văn phòng còn yếu:** hành chính 13,33%, tài chính 8,33% [[S8]].
- **Tiếng Việt kém hơn tiếng Anh:** hội thoại khách hàng 0,52 so với 0,62 [[S9]]; chép lời cho kết quả dao động 6,7% đến 50,8% câu sai nghĩa giữa các dịch vụ [[S10]].
- **Năng suất tự ước cao hơn thực đo:** thí nghiệm Copilot ước 36 phút, đo được 12 phút [[S11]]. Nhóm Quy trình nhiều bước dạy đo trước và sau.

## Giới hạn của chính bộ tài liệu

- **Mọi bằng chứng định lượng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.** Không nguồn nào đo trực tiếp trên SME Việt Nam.
- **Giả thuyết "vô tội vạ" chỉ được ủng hộ gián tiếp**, xem [Thực trạng SME Việt Nam](thuc-trang-sme-viet-nam.md). SIPTech khuyến nghị trình bày đó là quan sát của người soạn, và dùng bộ câu hỏi khảo sát trong bài đó để thu dữ liệu gốc từ người học.
- **Ngưỡng và cỡ mẫu là đề xuất của SIPTech, không có nguồn.** Ví dụ bộ 20 đến 30 ca mẫu, ngưỡng recall, ngưỡng lên cấp. Với mẫu nhỏ như vậy, khoảng tin cậy rất rộng: chỉ phát hiện hỏng, không đo chính xác.
- **Mỗi bài cấp độ tách rõ phần có nguồn và phần đề xuất.**

## Việc cần kiểm trước khi xuất bản

Gom từ báo cáo của các nhóm bài; chi tiết nằm ở mục cuối của từng bài.

### Pháp lý (rủi ro cao nhất)

!!! warning "Chưa phải tư vấn pháp lý"
    Chưa đọc toàn văn Luật 91/2025/QH15, Nghị định 356/2025/NĐ-CP, Luật 71/2025/QH15 và Luật AI 134/2025/QH15: các trang thuvienphapluat trả lỗi 403, bản .doc của Nghị định 356 trên cổng văn bản của Bộ Tư pháp chưa tải. Cần luật sư hoặc đọc văn bản gốc trước khi dạy người khác. Chi tiết: [An toàn dữ liệu và pháp lý](an-toan-du-lieu-va-phap-ly-vn.md).

- Số điều về chuyển dữ liệu ra nước ngoài còn lệch giữa các nguồn thứ cấp (Điều 20 của Luật hay Điều 18 của Nghị định 356).
- Chưa xác minh: mức phạt, Nghị định 142/2026/NĐ-CP, thời hạn chuyển tiếp 12 hoặc 18 tháng của Luật AI, Luật Dữ liệu 2024.
- **Hóa đơn điện tử:** Nghị định 123/2020/NĐ-CP và Nghị định 70/2025/NĐ-CP đã được thay bằng Nghị định 254/2026/NĐ-CP (hiệu lực 01/7/2026, hướng dẫn Luật Quản lý thuế 108/2025/QH15) cùng Thông tư 91/2026/TT-BTC. Đã kiểm qua tìm kiếm (thuvienphapluat, Công văn 4831/CT-CS của Cục Thuế qua luatvietnam), chưa đọc văn bản gốc. Tên thẻ XML hóa đơn chưa xác minh.
- **Luật Bảo vệ quyền lợi người tiêu dùng 19/2023/QH15** (Điều 10, Điều 31), Nghị định 55/2024 và **Luật 91/2025** Điều 25, 32 (dữ liệu nhân viên, ghi âm): mới đọc qua nguồn thứ cấp.

### Công cụ và điều khoản (thay đổi nhanh)

- API và webhook của KiotViet, Sapo, MISA; giá và tiêu chí duyệt Zalo ZNS/ZBS; Lark Approval; Meet, Teams, Zoom, Lark có chép lời tiếng Việt hay không: chưa xác minh.
- Điều khoản dữ liệu và tính năng của Claude, ChatGPT, Gemini: một số trang (OpenAI cá nhân, hướng dẫn GPT tùy chỉnh) trả lỗi 403, chỉ có tóm tắt tìm kiếm. Trang Google nêu Gemini Gems sẽ chuyển sang skills từ 11/2026.
- Chưa đọc cách gọi Gemini API, function calling của Gemini, Make; Zapier chỉ qua blog.
- Chưa xác minh Google Document AI hỗ trợ tiếng Việt, Azure Invoice có locale `vi`.
- Chính sách ngừng mô hình của OpenAI và Google chưa tra (của Anthropic đã đọc ngày 11/11/2026).
- Giá API không ghi số, chỉ ghi cách tự tính.

### Tiếng Việt (không có nguồn đo)

- Không nguồn nào đo OCR hay trích xuất trên tài liệu SME Việt Nam.
- Số MIRACL của M3 và mE5 không gồm tiếng Việt; số tiếng Việt chỉ có ở VN-MTEB (dịch máy) và MKQA (chéo ngôn ngữ).
- Chưa có nguồn cho việc tách từ hoặc bỏ dấu có giúp BM25 tiếng Việt hay không: người học phải tự thử bằng bộ câu hỏi riêng.
- Độ tin cậy của RAGAS và LLM judge trên tiếng Việt chưa có dữ liệu.

### Kỹ thuật

- Công thức RRF và k=60 chỉ có từ bài thứ cấp.
- Docling, Marker, MarkItDown chưa chạy thử; HybridChunker của Docling chỉ qua tóm tắt.
- Mã mẫu đã chạy thử cục bộ (BM25, FTS5, kiểm trích dẫn, chia khối, CER, kiểm tổng hóa đơn, khoảng Wilson, kappa, ghi log, tính chi phí, hàm công cụ giả), chưa chạy với API thật. Đoạn RRF chưa chạy thử; mã nhúng vector chưa viết.
- Hai p-value của kiểm định dấu ở Cấp C6 (0,22 và 0,008) mới tính tay.

### Đã kiểm trong bước rà soát (11/11/2026)

- Số liệu MAP, Nubank, Airbnb, BMO trong các bài cấp độ khớp với toàn văn các bài báo đã đọc; các số ablation của Airbnb khớp Bảng 5 của bài.
- Khoảng Wilson cho 18/20 (khoảng 70% đến 97%) và pass^3 = 0,75³ (khoảng 42%) đúng.
- Chưa kiểm: từng đường dẫn trong mục tài liệu tham khảo của các bài (mỗi bài đã ghi mức tin cậy cho từng mục), và các trích dẫn từ trang web đọc qua công cụ tóm tắt.

## Đọc tiếp

Thứ tự gợi ý cho người làm series:

1. [Nền tảng bằng chứng](nen-tang-bang-chung.md): các bài báo đã đọc kỹ.
2. [Thực trạng SME Việt Nam](thuc-trang-sme-viet-nam.md): kiểm chứng giả thuyết "vô tội vạ".
3. [An toàn dữ liệu và pháp lý](an-toan-du-lieu-va-phap-ly-vn.md): dữ liệu nào được đưa vào AI.
4. Các bài cấp độ của từng bài toán, bắt đầu từ cấp 0.

Việc tiếp theo cho người soạn: chọn một ngành và một bộ tài liệu thật (bảng giá, chính sách, hợp đồng) làm ví dụ xuyên suốt; biến từng cấp thành bài có kịch bản, tài liệu mẫu, mã mẫu và bộ ca mẫu có đáp án; trước khi xuất bản thì kiểm pháp lý bằng văn bản gốc, kiểm lại tính năng công cụ và đo thử trên tài liệu tiếng Việt thật.

## Nguồn

Các bài báo và benchmark được trích ở trang này. Bấm tên nguồn để mở bài gốc.

:::sources
S1 | Measuring Agents in Production (MAP) | UC Berkeley, IBM Research và nhóm tác giả · ICML 2026 · arXiv 2512.04123 | https://www.alphaxiv.org/abs/2512.04123 | doc | Chi tiết ở trang Nền tảng bằng chứng.
S2 | Agentic RAG via Portable Skills | Airbnb · arXiv 2610.14428 | https://www.alphaxiv.org/abs/2610.14428 | doc | Chi tiết ở trang Nền tảng bằng chứng.
S3 | Policy Loopholes | arXiv 2609.14400 | https://www.alphaxiv.org/abs/2609.14400 | doc | Kiểm chính sách của τ²-bench: chính sách có chỗ im lặng hoặc mâu thuẫn làm agent xử lý không nhất quán.
S4 | τ-bench | Sierra · arXiv 2406.12045 | https://www.alphaxiv.org/abs/2406.12045 | doc | Mô hình năm 2024 (gpt-4o): tỷ lệ đạt lần đầu khoảng 61% (bán lẻ), đạt cả 8 lần liên tiếp dưới 25%.
S5 | Nghiên cứu 14 triển khai LLM thương mại (tính không lặp lại của kết quả) | arXiv 2610.21300 | https://www.alphaxiv.org/abs/2610.21300 | tom | Cùng yêu cầu gửi lặp lại ở chế độ "xác định": cả 14 đều có lúc trả khác nhau, 12 có lúc đổi nhãn kết luận.
S6 | SpreadsheetBench 2 | NeurIPS 2026 Datasets track · arXiv 2606.29955 | https://www.alphaxiv.org/abs/2606.29955 | doc | 321 việc từ dữ liệu doanh nghiệp thật; bảng tính tài chính lớn hơn bảng SME thường gặp.
S7 | Beyond Logprobs (ExtractConf) | arXiv 2606.24420 | https://www.alphaxiv.org/abs/2606.24420 | doc | Một tác giả, một mô hình, tiếng Anh; trên 55 trường hóa đơn DocILE, GPT-4o sai 26,6%.
S8 | TheAgentCompany | CMU · arXiv 2412.14161 | https://www.alphaxiv.org/abs/2412.14161 | doc | Môi trường giả lập 175 việc văn phòng, không phải doanh nghiệp thật.
S9 | SEATauBench | arXiv 2606.28715 | https://www.alphaxiv.org/abs/2606.28715 | doc | Benchmark đa ngôn ngữ có tiếng Việt; bản dịch có kiểm bởi người bản ngữ, không phải tin nhắn SME thật.
S10 | mu-bench | Sierra AI · arXiv 2609.32082 | https://www.alphaxiv.org/abs/2609.32082 | doc | 975 câu tiếng Việt qua điện thoại 8 kHz, khách đóng vai gọi tổng đài ngân hàng.
S11 | Selected Copilot Experiments | Edelman, Microsoft · 5/2024 | https://www.microsoft.com/en-us/research/wp-content/uploads/2024/05/Edelman_Copilot-Experiments-Merged-2024-05-AICE-Shareable.pdf | doc | Chỉ đọc 12 trang slide đầu; slide nội bộ của nhà cung cấp.
:::
