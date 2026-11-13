date: 2026-11-11

# Nền tảng bằng chứng: AI-agent đang chạy thật trong doanh nghiệp

Trước khi hướng dẫn doanh nghiệp làm gì, SIPTech muốn biết các tổ chức đã đưa AI vào vận hành thật bằng cách nào, và chỗ nào họ gặp khó. Bài này tóm tắt năm bài báo đã đọc kỹ toàn văn, tám bài mới đọc tóm tắt và vài khảo sát ngành. Mỗi con số đi kèm một nhãn như [[S1]], bấm vào là nhảy tới nguồn ở cuối trang.

!!! note "Cách đọc bài này"
    Nhãn **Nguồn Sx** là kết quả nằm trong tài liệu gốc. Khung xanh **Đề xuất của SIPTech** là suy luận của nhóm soạn, chưa được kiểm chứng. Tổng hợp ngày 11/11/2026 từ alphaXiv (đọc nội dung chi tiết các bài đánh dấu "đọc kỹ") và một lượt tìm web cho khảo sát ngành.

## Đọc nhanh: bốn điều rút ra

!!! proposal "Đề xuất của SIPTech"
    1. **Hệ thống thành công đều hẹp:** có SOP, ít công cụ, có người duyệt. Điều này làm cho hướng "đi từ khối nhỏ" hợp lý với SME.
    2. **Công thức chung:** SOP, rồi quy trình từng bước, rồi bộ ca mẫu có đáp án, rồi triển khai nhỏ, rồi sửa có kiểm soát. Quy mô thu nhỏ được cho SME.
    3. **Chất lượng nằm nhiều ở nội dung và quy trình** (SOP đã đủ chưa, tài liệu đã sạch chưa) hơn là ở mô hình hay công nghệ truy xuất. SME làm được việc này mà không cần nhiều tiền.
    4. **Mọi bằng chứng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.** Chưa có nguồn nào đo trực tiếp trên SME Việt Nam, xem [Thực trạng SME Việt Nam](thuc-trang-sme-viet-nam.md).

## Năm bài đã đọc kỹ

### MAP: 86 hệ thống agent đang chạy thật

Nhóm UC Berkeley, Intesa Sanpaolo, UIUC, Stanford và IBM Research, ICML 2026 [[S1]]. Đây là khảo sát lớn nhất về agent đang vận hành, nên được dùng làm nền cho nhiều nhận định của series.

- **Phương pháp:** 20 ca phỏng vấn sâu; khảo sát 306 người làm agent (28/7 đến 29/10/2025); lọc còn 86 hệ thống đang chạy hoặc chạy thử, thuộc 26 lĩnh vực.
- **Vì sao triển khai:** năng suất 80%, giảm giờ công 72%, tăng hài lòng khách 38%, rủi ro và tuân thủ 12%.
- **Phục vụ ai:** 92,5% phục vụ con người; nhân viên nội bộ 52%, khách bên ngoài 40%. Triển khai nội bộ trước là chủ ý để giảm rủi ro.
- **Kiến trúc đơn giản đến bất ngờ:** 70% dùng mô hình có sẵn bằng prompt, không tinh chỉnh; 79% prompt viết tay hoặc tay kết hợp LLM; 68% chạy dưới 10 bước rồi chuyển cho người (47% dưới 5 bước); 16 trong 20 ca dùng workflow cố định; 17 trong 20 ca tự viết thay vì dùng framework.
- **Độ trễ:** 66% chấp nhận chờ từ vài phút; 15 trong 20 ca chạy bất đồng bộ.
- **Đánh giá chất lượng:** 74% bằng người; 52% dùng LLM làm giám khảo; 75% không dùng benchmark chính thức mà dùng A/B hoặc phản hồi chuyên gia. Mọi ca dùng LLM làm giám khảo đều kèm duyệt tay.
- **Thách thức số 1 là độ tin cậy.** Cách giảm rủi ro: chế độ chỉ đọc, sandbox, bọc API, phân quyền như người dùng.
- **Hạn chế tác giả nêu:** mẫu lệch về Châu Mỹ và mạng quen biết của nhóm; số liệu thu trong tháng 4 đến 11/2025.

### Nubank: chăm sóc khách hàng ở quy mô 100 triệu người dùng

KDD 2026 [[S2]]. Bài mô tả cách xây agent hỗ trợ khách và đo bằng A/B test thật.

| Tác vụ | tNPS tăng | Tự phục vụ | Chênh so với nhân viên giỏi |
|---|---|---|---|
| Giao thẻ | +37 | +29 | −10 |
| Quản lý nợ | +40 | +2,9 | −23,6 |
| Hạn mức tín dụng | +4,5 | +7,5 | −7,1 |
| Quản lý thẻ | +38,3 | +4,8 | −1,1 |
| Giải thích sản phẩm | +12,3 | −1,5 | −6,2 |

*Đơn vị: điểm phần trăm* [[S2]]

- **Thiết kế:** ReAct với 5 đến 15 công cụ. Ngữ cảnh chia module có phiên bản (hướng dẫn, quy trình lấy từ SOP, macro, mô tả công cụ, bảng nháp). Hạ tầng đi trước prompt: danh tính, API hành động idempotent, nhật ký kiểm toán.
- **Công cụ:** mô tả công cụ được coi là prompt; chỉ trả về trường cần thiết; gộp luồng cố định thành một công cụ ghép bằng code.
- **Ca giao thẻ:** 3 công cụ, 5 bộ chấm (E1 đến E5); 3 chuyên viên gán nhãn rồi lấy đa số, giữ lời giải thích; "vài trăm nhãn nhị phân là đủ để dựng một bộ chấm".
- **Tối ưu bộ chấm bằng GEPA:** độ chính xác E3 tăng từ 58,07% lên 73,01%. Ở E2, prompt viết tay (68,88%) kém hơn cách đoán theo lớp đa số (77,78%). Độ đồng thuận kappa giữa các mô hình tăng rõ sau tối ưu (ví dụ GPT-5 và o3: 0,950).
- **Triển khai:** mỗi biến thể bắt đầu ở 1% lưu lượng; điểm đo offline tương quan dương với kết quả online. Tác giả ghi "10 biến thể" ở một chỗ và "11" ở chỗ khác.
- **Đánh đổi:** tNPS và tỷ lệ tự phục vụ kéo nhau xuống: chuyển ngay ca khó cho người làm tNPS đẹp nhưng giảm tự phục vụ.
- **Riêng tư:** ẩn danh dữ liệu; hợp đồng xử lý dữ liệu cấm bên thứ ba huấn luyện trên dữ liệu; agent không đưa ra quyết định tín dụng hay nợ không thể đảo ngược.

### Airbnb: tra cứu SOP bằng "kỹ năng" di động

Bài về agentic RAG [[S3]]. Đây là nguồn quan trọng nhất cho nhóm bài [Tra cứu tài liệu nội bộ](rag-tra-cuu-tai-lieu/index.md).

- **Bài toán:** từ một ca hỗ trợ đã ẩn danh, sinh hướng dẫn từng bước cho nhân viên, kèm trích dẫn nguyên văn từ 2.881 bài SOP.
- **Giải pháp:** "skill" gồm file hướng dẫn, vài script, cấu hình và kho tri thức. Lớp điều hướng khoảng 2.700 trang wiki do GPT-4.1 sinh trong một lượt: mỗi trang ghi việc nó giải quyết, liên kết có kiểu về bài gốc, gộp quy trình bị chia nhỏ. Công cụ tìm kiếm chỉ có BM25 cộng vector, không re-ranker, không tinh chỉnh.
- **Hàng rào bằng code:** trình kiểm tra từ chối cả lần ghi nếu một đoạn trích không phải chuỗi con nguyên văn của bài nguồn; kết quả là 100% đoạn trích hợp lệ.
- **Kết quả trên 132 ca thật:** tương đương quy trình chuẩn 99,2% (khoảng tin cậy 95,8 đến 99,9); đủ bằng chứng 83,3% (76,1 đến 88,7). Hệ thống RAG production hiện có đạt 59,8% ở chỉ số bằng chứng và 96,2% ở chỉ số quy trình.
- **Thử bỏ từng phần (ablation):** BM25 riêng, vector riêng, bỏ từng thuộc tính của lớp điều hướng: không cấu hình nào khác hệ thống đầy đủ ở mức p<0,05 (n=132); gần nhất là bỏ thực thể gộp (p=0,078). Tác giả chỉ kết luận "có tính định hướng".
- **Chi phí:** triển khai 1 đến 2 ngày công kỹ sư; chậm khoảng 90 giây so với 8 đến 9 giây của trợ lý production; chấm lấy đa số 3 lần vì một lần có bất đồng khoảng 15%.
- **Thất bại còn lại** chủ yếu do SOP thiếu bước mà nhân viên giỏi vẫn làm. Muốn tốt hơn cần viết thêm SOP, không phải sửa khâu truy xuất.
- **Hạn chế tác giả nêu:** một bộ tài liệu, một triển khai; con người xem lại mọi ca.

### BMO ESCROW: sửa "kỹ năng" mà không làm hỏng ca cũ

NeurIPS 2026 [[S4]].

- **Hệ thống:** FinDAS kiểm toán tài liệu tài chính nộp kèm hồ sơ vay thế chấp; 78 tài liệu chính sách, 23 loại tài liệu; bộ 15 công cụ.
- **Ý tưởng:** giữ nguyên mô hình, chỉ sửa skill (viết bằng ngôn ngữ tự nhiên). Bản sửa chỉ được nhận khi không nhóm ca nào xấu đi và các ca đã sửa trước đó vẫn đúng; mỗi thay đổi là một diff đọc được cho bộ phận tuân thủ.
- **Bằng chứng:** qua 4 vòng cập nhật, nếu không có kho ca cũ thì điểm trên ca cũ tụt từ 0,857 xuống 0,7; có kho này thì giữ khoảng 0,84 (chênh +0,138, khoảng tin cậy +0,10 đến +0,18).
- **Hạn chế:** chấm lại toàn bộ ca tốn kém nên vòng lặp chỉ xử lý được vài trăm ca; không phát hành mã hay dữ liệu.

### SAP: bộ nhớ chung cho tổ chức

Bài về agent lập trình trong doanh nghiệp [[S5]].

- **Hệ thống:** hook phát hiện thay đổi file tri thức rồi xin phép người đóng góp; chuỗi nhiều agent soạn cặp hỏi đáp, gắn nhãn, quét bảo mật, kiểm tra trùng; truy xuất qua MCP ba mức.
- **Số liệu (một vài nhóm nội bộ, ngày 22/7/2026):** 900 đóng góp cho ra 1.144 bộ nhớ (53,7% đóng góp tạo ít nhất một bộ nhớ).
- **Tác giả thừa nhận:** hiệu quả đối với chất lượng lập trình chưa được đo; điểm tin cậy chưa được hiệu chuẩn; có nguy cơ nhiễm độc bộ nhớ dùng chung.

## Tám bài mới đọc tóm tắt

Cần đọc kỹ trước khi trích số liệu.

- Making Sense of AI Agents Hype: 138 bài nói của người làm thực tế [[S6]]
- How Do Practitioners Build SE Agents? [[S7]]
- Governed Agentic Workflows in Regulated Finance (Zafin) [[S8]]
- Reference Architecture for Agentic AI in Enterprise Software [[S9]]
- READY or Not (Scale AI) [[S10]]
- Is Bash All You Need? (Microsoft, CMU) [[S11]]
- EAIR: rủi ro khi nhiều agent tương tác [[S12]]
- Skill LLMs cho chăm sóc khách hàng (Dialpad) [[S13]]

!!! warning "Không dùng làm bằng chứng"
    Bài Agents in the Wild [[S14]] chỉ là mô tả dạng hướng dẫn, không có dữ liệu triển khai.

## Khảo sát ngành: chỉ để tham khảo

Các số dưới đây thu được qua một lượt tìm web, chưa đọc nguồn gốc, và các nguồn mâu thuẫn nhau. Số liệu từ nhà cung cấp công cụ AI có lợi ích liên quan.

- Khảo sát State of AI Agents 2026 của Anthropic (hơn 500 lãnh đạo kỹ thuật): ứng dụng ngoài lập trình hiệu quả nhất là phân tích dữ liệu và báo cáo (60%) và tự động hóa quy trình nội bộ (48%) [[S15]].
- Snowflake: 40% đơn vị đo được ROI báo thu về 1,49 đô la cho mỗi 1 đô la [[S16]].
- WRITER: 79% gặp khó khăn đáng kể; 23% thấy ROI rõ rệt [[S17]].
- Tỷ lệ dùng agent trong production dao động khoảng 40% đến 80% tùy cách định nghĩa "production".

!!! warning "Không dùng các con số này"
    "ROI 171%", "hoàn vốn 5,1 tháng", "3,4 lần ROI từ 517 công ty": chỉ gặp ở blog, không tìm được nguồn gốc.

## Nguồn

Bấm tên nguồn để mở bài gốc. Nhãn màu cho biết SIPTech đã đọc tới đâu.

:::sources
S1 | Measuring Agents in Production (MAP) | UC Berkeley, Intesa Sanpaolo, UIUC, Stanford, IBM Research · ICML 2026 · arXiv 2512.04123 | https://www.alphaxiv.org/abs/2512.04123 | doc
S2 | Building Customer Support AI Agents at 100M-User Scale | Nubank · KDD 2026 · arXiv 2606.08867 | https://www.alphaxiv.org/abs/2606.08867 | doc
S3 | Agentic RAG via Portable Skills | Airbnb · arXiv 2610.14428 | https://www.alphaxiv.org/abs/2610.14428 | doc
S4 | ESCROW | BMO · NeurIPS 2026 · arXiv 2608.01772 | https://www.alphaxiv.org/abs/2608.01772 | doc
S5 | Shared Organizational Memory for Enterprise Coding Agents | SAP · arXiv 2608.00122 | https://www.alphaxiv.org/abs/2608.00122 | doc
S6 | Making Sense of AI Agents Hype | arXiv 2604.00189 | https://www.alphaxiv.org/abs/2604.00189 | tom
S7 | How Do Practitioners Build SE Agents? | arXiv 2607.10856 | https://www.alphaxiv.org/abs/2607.10856 | tom
S8 | Governed Agentic Workflows in Regulated Finance | Zafin · arXiv 2610.33253 | https://www.alphaxiv.org/abs/2610.33253 | tom
S9 | Reference Architecture for Agentic AI in Enterprise Software | arXiv 2610.14818 | https://www.alphaxiv.org/abs/2610.14818 | tom
S10 | READY or Not | Scale AI · arXiv 2609.02095 | https://www.alphaxiv.org/abs/2609.02095 | tom
S11 | Is Bash All You Need? | Microsoft, CMU · arXiv 2609.11999 | https://www.alphaxiv.org/abs/2609.11999 | tom
S12 | EAIR: rủi ro tương tác multi-agent | arXiv 2610.14800 | https://www.alphaxiv.org/abs/2610.14800 | tom
S13 | Skill LLMs cho chăm sóc khách hàng | Dialpad · arXiv 2610.14346 | https://www.alphaxiv.org/abs/2610.14346 | tom
S14 | Agents in the Wild | arXiv 2607.19336 | https://www.alphaxiv.org/abs/2607.19336 | tom | Chỉ là mô tả dạng hướng dẫn, không dùng làm bằng chứng
S15 | State of AI Agents 2026 | Anthropic · hơn 500 lãnh đạo kỹ thuật | | thu | Nhà cung cấp có lợi ích liên quan; chưa đọc báo cáo gốc
S16 | Khảo sát ROI của Snowflake | Snowflake | | thu | Nhà cung cấp có lợi ích liên quan; chưa đọc báo cáo gốc
S17 | Khảo sát của WRITER | WRITER | | thu | Nhà cung cấp có lợi ích liên quan; chưa đọc báo cáo gốc
:::
