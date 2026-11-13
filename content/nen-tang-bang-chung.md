# Nền tảng bằng chứng: AI/AI-Agent đang chạy thật trong doanh nghiệp

Ngày tổng hợp: 2026-11-11. Nguồn: alphaXiv (đọc nội dung chi tiết các bài đánh dấu "đã đọc"), một lượt tìm web cho khảo sát ngành.

Quy ước: **[Nguồn]** là kết quả trong bài báo. **[Đề xuất]** là suy luận của nhóm làm series, chưa được kiểm chứng.

## 1. Các bài đã đọc kỹ

### 1.1 Measuring Agents in Production (MAP) — arXiv 2512.04123
UC Berkeley, Intesa Sanpaolo, UIUC, Stanford, IBM Research. ICML 2026. https://www.alphaxiv.org/abs/2512.04123

- **[Nguồn] Phương pháp:** 20 ca phỏng vấn sâu; khảo sát 306 người làm agent (28/7-29/10/2025); lọc còn 86 hệ thống production/pilot, 26 lĩnh vực.
- **[Nguồn] Lý do triển khai:** năng suất 80%, giảm giờ công 72%, tăng hài lòng khách 38%, rủi ro/tuân thủ 12%.
- **[Nguồn] Người dùng:** 92,5% phục vụ con người; nhân viên nội bộ 52%, khách bên ngoài 40%. Triển khai nội bộ trước là chủ ý để giảm rủi ro.
- **[Nguồn] Kiến trúc:** 70% dùng mô hình có sẵn bằng prompt (không tinh chỉnh); 79% prompt viết tay hoặc tay + LLM; 68% chạy dưới 10 bước rồi chuyển cho người (47% dưới 5 bước); 16/20 ca dùng workflow cố định; 17/20 ca tự viết thay vì dùng framework.
- **[Nguồn] Độ trễ:** 66% chấp nhận phút trở lên; 15/20 ca chạy bất đồng bộ.
- **[Nguồn] Đánh giá:** 74% bằng người; 52% LLM-as-judge; 75% không dùng benchmark chính thức mà dùng A/B hoặc phản hồi chuyên gia. Mọi ca dùng LLM-as-judge đều kèm duyệt tay.
- **[Nguồn] Thách thức số 1:** độ tin cậy. Giảm rủi ro bằng chế độ chỉ-đọc, sandbox, bọc API, phân quyền như người dùng.
- **Hạn chế (tác giả nêu):** mẫu lệch Châu Mỹ và mạng lưới quen biết; thời điểm 4-11/2025.

### 1.2 Nubank — Building Customer Support AI Agents at 100M-User Scale — arXiv 2606.08867
KDD 2026. https://www.alphaxiv.org/abs/2606.08867

- **[Nguồn] Kết quả A/B test (điểm phần trăm):**

| Tác vụ | tNPS tăng | Tỷ lệ tự phục vụ | Chênh so với nhân viên giỏi |
|---|---|---|---|
| Giao thẻ | +37 | +29 | −10 |
| Quản lý nợ | +40 | +2,9 | −23,6 |
| Hạn mức tín dụng | +4,5 | +7,5 | −7,1 |
| Quản lý thẻ | +38,3 | +4,8 | −1,1 |
| Giải thích sản phẩm | +12,3 | −1,5 | −6,2 |

- **[Nguồn] Thiết kế:** ReAct với 5-15 công cụ; context chia module có phiên bản (instructions, routines từ SOP, macros, mô tả công cụ, scratchpad); hạ tầng trước prompt (danh tính, API hành động idempotent, nhật ký kiểm toán).
- **[Nguồn] Công cụ:** mô tả công cụ được coi là prompt; chỉ trả về trường cần thiết; gộp luồng cố định thành một công cụ ghép bằng code.
- **[Nguồn] Ca giao thẻ:** 3 công cụ (`get_customer_profile`, `check_card_delivery`, `reissue_card`); 5 bộ chấm (E1-E5); 3 chuyên viên gán nhãn, lấy đa số, giữ lời giải thích; "vài trăm nhãn nhị phân là đủ để dựng một bộ chấm".
- **[Nguồn] Tối ưu bộ chấm bằng GEPA:** độ chính xác E3 từ 58,07% lên 73,01%. Ở E2, prompt viết tay (68,88%) kém hơn đoán lớp đa số (77,78%). Độ đồng thuận kappa giữa các mô hình tăng rõ sau tối ưu (ví dụ GPT-5 và o3: 0,950).
- **[Nguồn] Rollout:** mỗi biến thể bắt đầu ở 1% lưu lượng; điểm offline tương quan dương với kết quả online. Tác giả ghi "10 biến thể" ở một chỗ và "11" ở chỗ khác.
- **[Nguồn] Đánh đổi:** tNPS và tỷ lệ tự phục vụ đánh đổi nhau (chuyển ngay ca khó cho người làm tNPS đẹp nhưng giảm tự phục vụ).
- **[Nguồn] Riêng tư:** ẩn danh dữ liệu; hợp đồng xử lý dữ liệu cấm bên thứ ba huấn luyện trên dữ liệu; agent không đưa quyết định tín dụng/nợ không thể đảo ngược.

### 1.3 Airbnb — Agentic RAG via Portable Skills — arXiv 2610.14428
https://www.alphaxiv.org/abs/2610.14428

- **[Nguồn] Bài toán:** từ một ca hỗ trợ đã ẩn danh, sinh hướng dẫn từng bước cho nhân viên kèm trích dẫn nguyên văn từ 2.881 bài SOP.
- **[Nguồn] Giải pháp:** "skill" gồm file hướng dẫn, vài script, cấu hình, kho tri thức. Lớp điều hướng ~2.700 trang wiki do GPT-4.1 sinh trong một lượt: mỗi trang ghi việc nó giải quyết, liên kết có kiểu về bài gốc, gộp quy trình bị chia nhỏ. Công cụ tìm kiếm duy nhất là BM25 + vector, không re-ranker, không fine-tune.
- **[Nguồn] Hàng rào bằng code:** trình kiểm tra từ chối cả lần ghi nếu một đoạn trích không phải chuỗi con nguyên văn của bài nguồn; 100% đoạn trích hợp lệ.
- **[Nguồn] Kết quả (132 ca thật):** tương đương quy trình chuẩn 99,2% (CI 95,8-99,9); đủ bằng chứng 83,3% (CI 76,1-88,7); RAG production hiện có 59,8% ở chỉ số bằng chứng, 96,2% ở chỉ số quy trình.
- **[Nguồn] Ablation:** BM25 riêng, vector riêng, bỏ từng thuộc tính của lớp điều hướng: không cấu hình nào khác biệt với hệ thống đầy đủ ở p<0,05 (n=132); gần nhất là bỏ thực thể gộp (p=0,078). Tác giả chỉ kết luận "có tính định hướng".
- **[Nguồn] Chi phí:** triển khai 1-2 ngày công kỹ sư; chậm ~90 giây so với ~8-9 giây của trợ lý production; chấm lấy đa số 3 lần vì một lần có bất đồng ~15%.
- **[Nguồn] Thất bại còn lại:** chủ yếu do SOP thiếu bước mà nhân viên giỏi vẫn làm. Cải thiện cần viết thêm SOP, không phải sửa truy xuất.
- **Hạn chế (tác giả nêu):** một corpus, một triển khai; con người xem lại mọi ca.

### 1.4 BMO — ESCROW — arXiv 2608.01772
NeurIPS 2026. https://www.alphaxiv.org/abs/2608.01772

- **[Nguồn] Hệ thống:** FinDAS kiểm toán tài liệu tài chính nộp kèm hồ sơ vay thế chấp; 78 tài liệu chính sách, 23 loại tài liệu; bộ 15 công cụ.
- **[Nguồn] Ý tưởng:** mô hình giữ nguyên, chỉ sửa skill (ngôn ngữ tự nhiên). Bản sửa chỉ được nhận khi không nhóm ca nào xấu đi và các ca đã sửa trước đó vẫn đúng; mỗi thay đổi là một diff đọc được cho bộ phận tuân thủ.
- **[Nguồn] Bằng chứng:** qua 4 vòng cập nhật, không có kho ca cũ thì điểm trên ca cũ tụt 0,857 → 0,7; có kho này giữ ~0,84 (chênh +0,138, CI [+0,10, +0,18]).
- **[Nguồn] Hạn chế:** chi phí chấm lại toàn bộ ca làm vòng lặp chỉ xử lý được vài trăm ca; không phát hành mã hay dữ liệu.

### 1.5 SAP — Shared Organizational Memory for Enterprise Coding Agents — arXiv 2608.00122
https://www.alphaxiv.org/abs/2608.00122

- **[Nguồn] Hệ thống:** hook `PostToolUse`/`Stop` phát hiện thay đổi file tri thức, hỏi xin phép người đóng góp; chuỗi xử lý nhiều agent (soạn cặp hỏi-đáp, gắn nhãn, quét bảo mật, kiểm tra trùng); truy xuất qua MCP 3 mức.
- **[Nguồn] Số liệu (một vài nhóm nội bộ, 22/7/2026):** 900 đóng góp → 1.144 bộ nhớ (53,7% cho ra ít nhất một bộ nhớ).
- **[Nguồn] Tác giả thừa nhận:** hiệu quả đối với chất lượng lập trình chưa được đo; điểm tin cậy chưa được hiệu chuẩn; nguy cơ nhiễm độc bộ nhớ dùng chung.

## 2. Bài chỉ mới đọc tóm tắt (cần đọc kỹ trước khi trích)

- arXiv 2604.00189 — Making Sense of AI Agents Hype (138 bài nói của người làm thực tế).
- arXiv 2607.10856 — How Do Practitioners Build SE Agents?
- arXiv 2610.33253 — Governed Agentic Workflows in Regulated Finance (Zafin).
- arXiv 2610.14818 — Reference Architecture for Agentic AI in Enterprise Software.
- arXiv 2609.02095 — READY or Not (Scale AI).
- arXiv 2609.11999 — Is Bash All You Need? (Microsoft, CMU).
- arXiv 2610.14800 — EAIR, rủi ro tương tác multi-agent.
- arXiv 2610.14346 — Skill LLMs cho CSKH (Dialpad).

Bài arXiv 2607.19336 (Agents in the Wild) chỉ là mô tả tutorial, không có dữ liệu triển khai: **không dùng làm bằng chứng**.

## 3. Khảo sát ngành (thứ cấp, chưa đọc nguồn gốc)

Thu được qua một lượt tìm web, các nguồn mâu thuẫn nhau; chỉ để tham khảo. Số liệu từ nhà cung cấp công cụ AI có lợi ích liên quan.

- Anthropic "State of AI Agents 2026" (500+ lãnh đạo kỹ thuật): ứng dụng phi lập trình hiệu quả nhất là phân tích dữ liệu/báo cáo (60%) và tự động hóa quy trình nội bộ (48%).
- Snowflake: 40% số đơn vị đo được ROI báo thu về $1,49 cho mỗi $1.
- WRITER: 79% gặp khó khăn đáng kể; 23% thấy ROI rõ rệt.
- Tỷ lệ dùng agent trong production: khoảng 40% đến 80% tùy định nghĩa "production".
- **Không dùng:** "ROI 171%", "hoàn vốn 5,1 tháng", "3,4 lần ROI từ 517 công ty" (chỉ gặp ở blog, không tìm được nguồn gốc).

## 4. Điều rút ra cho series [Đề xuất]

1. Hệ thống thành công trong các nguồn đều hẹp, có SOP, ít công cụ, có người duyệt. Điều này làm cho hướng "đi từ khối nhỏ" hợp lý với SME.
2. Phương tiện chung là: SOP → quy trình từng bước → bộ ca mẫu có đáp án → rollout nhỏ → sửa có kiểm soát. Quy mô có thể thu nhỏ cho SME.
3. Phần lớn chất lượng nằm ở nội dung và quy trình (SOP đủ chưa, tài liệu sạch chưa), không nằm ở mô hình hay truy xuất. Đây là điểm SME làm được mà không cần nhiều tiền.
4. Mọi bằng chứng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh. **Chưa có nguồn nào đo trực tiếp trên SME Việt Nam**: xem `thuc-trang-sme-viet-nam.md`.
