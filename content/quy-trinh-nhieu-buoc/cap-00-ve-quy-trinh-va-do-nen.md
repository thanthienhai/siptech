# Q0 — Vẽ quy trình đang chạy và đo nền

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

## 1) Mục tiêu và người đọc

**Người đọc:** chủ SME, trưởng bộ phận (bán hàng, kế toán, nhân sự, kho). Không cần biết code.

**Sau cấp này có:**
- Bảng quy trình "như đang làm" cho 1-3 việc lặp lại, mỗi bước gắn một nhãn: **Người**, **Quy tắc** (máy làm chắc chắn), **AI** (cần hiểu ngôn ngữ), hoặc **Bỏ**.
- Bảng đo nền 2 tuần: số lượt, thời gian mỗi lượt, số lỗi, ai làm.
- Bản đồ dữ liệu: mỗi bước dữ liệu gì, nằm ở đâu, đi qua dịch vụ nào.

**Thứ chạy được độc lập:** bảng quy trình và bảng đo nền. Chỉ riêng chúng đã giúp tìm bước thừa và giao việc rõ hơn, kể cả khi không tự động hóa gì.

## 2) Câu hỏi cấp này trả lời / lỗi đang gặp

**Câu hỏi:** "Việc này thật ra gồm những bước nào, mất bao lâu, sai ở đâu, và bước nào đáng tự động?"

**Lỗi thường gặp trước khi có cấp này [Đề xuất, quan sát]:**
- Dán cả việc vào chatbot ("xử lý đơn này giúp tôi") mà không biết bước nào AI làm, bước nào người kiểm.
- Mua công cụ tự động hóa trước khi biết quy trình. Tự động hóa một quy trình rối chỉ làm rối nhanh hơn.
- Không có số đo trước, nên sau này không biết có tiết kiệm thật không.

## 3) Kiến thức nền

- **[Nguồn]** Nhóm RAG đã có công thức chuyển SOP thành bước, gán nhãn Code / LLM / Người (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md`, mục 3.3) và bài quan sát 5 ca thật (bài 8.1). Cấp này dùng lại, nhưng áp cho toàn bộ quy trình nghiệp vụ và thêm nhãn **Quy tắc** tách khỏi **AI**.
- **[Nguồn]** Airbnb (arXiv 2610.14428): thất bại còn lại chủ yếu do SOP thiếu bước mà nhân viên giỏi vẫn làm (`../nen-tang-bang-chung.md`). Nghĩa là chép quy trình từ người làm giỏi, không chép từ sổ tay.
- **[Nguồn]** TheAgentCompany (arXiv 2412.14161): agent tốt nhất chỉ hoàn thành 13,33% việc hành chính và 8,33% việc tài chính, thấp hơn nhiều so với việc lập trình (37,68%). Tác giả giải thích một phần bằng các việc cần thu thập thông tin từ nhiều người, đọc ảnh chụp, đi qua phần mềm phức tạp.
- **[Nguồn]** Dell'Acqua và cs. (HBS WP 24-013, chỉ đọc qua tóm tắt tìm kiếm): cùng một nhóm tư vấn viên dùng GPT-4 làm nhanh hơn ở việc "trong vùng" nhưng đúng ít hơn 19 điểm phần trăm ở việc "ngoài vùng". Nên phải tách quy trình thành từng bước nhỏ rồi xét riêng.
- **[Đề xuất] Cách gán nhãn mỗi bước:**

| Câu hỏi | Nếu "có" | Ví dụ |
|---|---|---|
| Bước có quyết định tiền, pháp lý, quyền lợi người? | **Người** (AI có thể chuẩn bị) | Duyệt chi, loại ứng viên, hoàn tiền |
| Viết được thành luật "nếu ... thì ..." mà người khác đồng ý? | **Quy tắc** | Đơn > 5 triệu chuyển trưởng phòng; cộng tổng; đổi định dạng ngày |
| Đầu vào là chữ tự do, ảnh, giọng nói, cần hiểu nghĩa? | **AI** (kèm cổng kiểm) | Đọc tin Zalo để biết khách muốn gì; trích trường từ ảnh hóa đơn |
| Bước không ai dùng kết quả? | **Bỏ** | Chép số liệu sang file "dự phòng" không ai mở |

Thứ tự ưu tiên khi phân vân: Bỏ → Quy tắc → Người → AI.

## 4) Chuỗi bài nhỏ

### Bài Q0.1 — Chọn việc
- **Làm:** liệt kê 10 việc lặp lại; chấm mỗi việc 1-5 theo tần suất, thời gian/lượt, mức đau (lỗi, chậm), rủi ro nếu sai. Chọn 1-3 việc tần suất cao, rủi ro vừa.
- **Sản phẩm:** bảng 10 việc có điểm.
- **Lỗi:** chọn việc hiếm nhưng "ấn tượng"; chọn ngay việc chi tiền.

### Bài Q0.2 — Quan sát và chép quy trình thật
- **Làm:** ngồi cạnh người làm giỏi nhất và người mới, mỗi người 3-5 lượt. Ghi từng thao tác: mở gì, chép gì, hỏi ai, chờ gì. Gộp thành 5-12 bước. Ghi điểm rẽ nhánh và ngoại lệ (đơn thiếu địa chỉ, CV gửi qua Zalo).
- **Sản phẩm:** bảng bước: #, việc, đầu vào, đầu ra, hệ thống, người làm, thời gian, ngoại lệ.
- **Lỗi:** chỉ phỏng vấn trưởng phòng; bỏ qua bước "hỏi lại khách".

### Bài Q0.3 — Gán nhãn Người / Quy tắc / AI / Bỏ
- **Làm:** dùng bảng mục 3. Với mỗi bước nhãn AI, viết một câu: "Nếu AI sai ở bước này thì ai phát hiện, khi nào?". Không trả lời được thì đổi sang Người.
- **Sản phẩm:** bảng có nhãn; đếm số bước theo nhãn.
- **Lỗi:** gắn AI cho bước chỉ cần công thức.

### Bài Q0.4 — Bản đồ dữ liệu
- **Làm:** mỗi bước ghi loại dữ liệu theo 5 mức của `../an-toan-du-lieu-va-phap-ly-vn.md` mục 3.1; nơi lưu (Zalo, Sheets, KiotViet, máy cá nhân); dịch vụ đi qua; ai xem được.
- **Sản phẩm:** bảng dữ liệu, đánh dấu chặng có dữ liệu cá nhân ra nước ngoài.
- **Lỗi:** quên ảnh chụp màn hình gửi qua nhóm Zalo.

### Bài Q0.5 — Đo nền 2 tuần
- **Làm:** một Google Sheet: ngày, mã lượt, người làm, giờ bắt đầu, giờ xong, kết quả (xong/trả lại/lỗi), ghi chú lỗi. Đo cả thời gian chờ (đơn nằm chờ duyệt bao lâu), không chỉ thời gian thao tác. Cách đo theo `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` bài 6.7.
- **Sản phẩm:** bảng đo nền: trung vị và khoảng (nhanh nhất-chậm nhất) thời gian, tỷ lệ lỗi, số lượt/tuần.
- **Lỗi:** chỉ đo người giỏi; đo một ngày rồi nhân lên.

### Bài Q0.6 — Chọn bước tự động hóa đầu tiên
- **Làm:** xếp các bước nhãn Quy tắc theo (thời gian tiết kiệm × tần suất). Chọn 1 bước cho Q1. Bước AI để sau, trừ khi nó chặn mọi thứ.
- **Sản phẩm:** một trang "kế hoạch Q1": bước nào, công cụ nào, ai phụ trách, đo gì.

## 5) Đường không code vs có code; khi nào buộc chuyển

| | Không code | Có code |
|---|---|---|
| Vẽ quy trình | Giấy, bảng tính, Lark Base, sơ đồ trong Docs | Không cần |
| Đo nền | Google Sheet / Lark Base tự ghi | Xuất nhật ký từ phần mềm (nếu có API) bằng script nhỏ |
| AI hỗ trợ | Dán ghi chép quan sát (đã che tên, SĐT) vào Project/Gem để gợi ý gộp bước, phát hiện bước trùng | — |

**Buộc chuyển sang code:** chỉ khi muốn lấy số lượt và thời gian thật từ phần mềm (ví dụ thời điểm tạo và hoàn tất đơn trên KiotViet/Haravan) thay vì tự ghi tay. Không bắt buộc ở cấp này.

## 6) Tiêu chí lên Q1 (đo được) [Đề xuất]

1. Có bảng quy trình cho ≥1 việc, người làm việc đó xác nhận "đúng như tôi làm".
2. Có đo nền ≥2 tuần hoặc ≥30 lượt, gồm trung vị thời gian và số lỗi.
3. Mỗi bước có nhãn; ≥1 bước nhãn Quy tắc được chọn cho Q1.
4. Có bản đồ dữ liệu; mọi chặng dữ liệu cá nhân ra ngoài được đánh dấu.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

**a) Cửa hàng mỹ phẩm online 6 người, bán qua Shopee, Facebook, Zalo; dùng phần mềm bán hàng.** Việc chọn: xử lý đơn từ Zalo.

| # | Bước | Nhãn | Lý do |
|---|---|---|---|
| 1 | Đọc tin Zalo, hiểu khách đặt gì | AI | Chữ tự do, viết tắt ("2 hộp kem 50ml ship q7") |
| 2 | Tra tồn kho | Quy tắc | Phần mềm đã có số |
| 3 | Tính tiền, phí ship theo bảng | Quy tắc | Công thức |
| 4 | Tạo đơn trên phần mềm | Quy tắc (sau khi người xác nhận bước 1) | Có API/nhập file |
| 5 | Nhắn khách xác nhận | Người (mẫu sẵn) | Ra ngoài, cần đúng |
| 6 | Chép đơn sang Sheet "theo dõi" | Bỏ | Phần mềm đã có báo cáo |

Đo nền giả định: 25 đơn Zalo/ngày, trung vị 6 phút/đơn, 3% đơn sai địa chỉ.

**b) Công ty xây lắp 30 người, đề nghị thanh toán bằng giấy + Zalo.** Việc chọn: đề nghị tạm ứng/thanh toán.

| # | Bước | Nhãn |
|---|---|---|
| 1 | Nhân viên điền đề nghị | Quy tắc (biểu mẫu có trường bắt buộc) |
| 2 | Chuyển trưởng công trình | Quy tắc (theo dự án) |
| 3 | Trưởng công trình duyệt | Người |
| 4 | Kế toán kiểm chứng từ kèm theo | Người, AI chỉ hỗ trợ trích trường (xem `../kiem-tra-ho-so-theo-quy-tac/00-README.md`) |
| 5 | Giám đốc duyệt nếu > hạn mức | Quy tắc chuyển + Người duyệt |
| 6 | Chi tiền | Người, ngoài hệ thống tự động |

Đo nền giả định: 60 đề nghị/tháng, thời gian từ nộp đến chi: trung vị 4 ngày, phần lớn là thời gian chờ ký, không phải thời gian thao tác. Bài học: AI không rút ngắn thời gian chờ ký; biểu mẫu + định tuyến + nhắc hạn (Q1) mới rút ngắn.

## 8) Tài liệu tham khảo

| Nguồn | Loại | Mức đọc | Tin cậy |
|---|---|---|---|
| TheAgentCompany, arXiv 2412.14161 | Benchmark (CMU) | Toàn văn các mục kết quả, Bảng 1, 5 | Cao cho môi trường giả lập; không phải doanh nghiệp thật |
| Airbnb, arXiv 2610.14428 (qua `../nen-tang-bang-chung.md`) | Bài công nghiệp | Nhóm trước đọc kỹ | Trung bình-cao |
| Dell'Acqua và cs., "Navigating the Jagged Technological Frontier", HBS WP 24-013 / SSRN 4573321 | Thử nghiệm ngẫu nhiên có đăng ký trước | **Chỉ qua tóm tắt tìm kiếm** | Cao về thiết kế; số liệu cần đối chiếu bản gốc |
| `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md`, `cap-06-danh-gia.md` | Tài liệu nội bộ | — | — |

## 9) Chưa kiểm chứng

- Không có nguồn đo nào về thời gian xử lý đơn/đề nghị thanh toán ở SME Việt Nam. Mọi số ở mục 7 là giả định.
- Thang chấm 1-5 ở bài Q0.1 và thứ tự ưu tiên "Bỏ → Quy tắc → Người → AI" là đề xuất, chưa kiểm chứng.
- Số Dell'Acqua chưa đối chiếu bản gốc.
