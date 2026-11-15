# Q0 — Vẽ quy trình đang chạy và đo nền

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

!!! tip "Tóm tắt nhanh"
    Trước khi nhờ AI hay mua phần mềm tự động hóa, bạn cần biết việc của mình thật ra gồm những bước nào, mất bao lâu và sai ở đâu. Bài này dạy bạn **vẽ lại quy trình đang chạy** thành một bảng, gắn cho mỗi bước một nhãn (Người, Quy tắc, AI hoặc Bỏ), rồi **đo nền trong 2 tuần**. Bạn **không cần biết lập trình**. Sau bài, bạn có bảng quy trình, bảng đo nền và bản đồ dữ liệu để chọn bước nên tự động hóa đầu tiên.

## 1) Mục tiêu và người đọc

**Bài này dành cho ai:** chủ SME (doanh nghiệp nhỏ và vừa), trưởng bộ phận (bán hàng, kế toán, nhân sự, kho). Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Một danh sách khoảng 10 việc lặp lại trong bộ phận của bạn (bài Q0.1 sẽ giúp bạn lập danh sách này).
- Người làm giỏi nhất và người mới của việc bạn chọn, để ngồi cạnh quan sát (bài Q0.2).
- Một Google Sheet hoặc Lark Base (một công cụ bảng tính trực tuyến) để ghi bảng đo.
- Nếu muốn nhờ AI gợi ý: một tài khoản có Project (Claude) hoặc Gem (Gemini), tức là chỗ lưu sẵn chỉ dẫn để dùng lại.

**Sau bài này bạn sẽ có:**
- Bảng quy trình "như đang làm" cho 1-3 việc lặp lại, mỗi bước gắn một nhãn: **Người**, **Quy tắc** (máy làm chắc chắn), **AI** (cần hiểu ngôn ngữ), hoặc **Bỏ**.
- Bảng đo nền 2 tuần: số lượt, thời gian mỗi lượt, số lỗi, ai làm.
- Bản đồ dữ liệu: mỗi bước dữ liệu gì, nằm ở đâu, đi qua dịch vụ nào.

**Thứ bạn cầm đi được sau bài:** bảng quy trình và bảng đo nền. Chỉ riêng chúng đã giúp tìm bước thừa và giao việc rõ hơn, kể cả khi bạn không tự động hóa gì.

!!! tip "Nói đơn giản"
    "Đo nền" nghĩa là đo cách làm hiện tại **trước khi** thay đổi bất cứ thứ gì. Có số đo này, về sau bạn mới biết mình tiết kiệm thật hay chỉ tưởng là tiết kiệm.

## 2) Câu hỏi cấp này trả lời / lỗi đang gặp

**Câu hỏi:** "Việc này thật ra gồm những bước nào, mất bao lâu, sai ở đâu, và bước nào đáng tự động?"

**Lỗi thường gặp trước khi có cấp này [Đề xuất, quan sát]:**
- Dán cả việc vào chatbot ("xử lý đơn này giúp tôi") mà không biết bước nào AI làm, bước nào người kiểm.
- Mua công cụ tự động hóa trước khi biết quy trình. Tự động hóa một quy trình rối chỉ làm rối nhanh hơn.
- Không có số đo trước, nên sau này không biết có tiết kiệm thật không.

## 3) Kiến thức nền

Phần này gồm bốn ý từ các nguồn nghiên cứu và một bảng cách gán nhãn. Các ý nghiên cứu giúp bạn hiểu vì sao phải vẽ quy trình trước. Bảng gán nhãn là công cụ bạn sẽ dùng ở bài Q0.3.

- **[Nguồn]** Nhóm RAG đã có công thức chuyển SOP thành bước, gán nhãn Code / LLM / Người (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md`, mục 3.3) và bài quan sát 5 ca thật (bài 8.1). Cấp này dùng lại, nhưng áp cho toàn bộ quy trình nghiệp vụ và thêm nhãn **Quy tắc** tách khỏi **AI**. (SOP là quy trình làm việc chuẩn được viết thành văn bản. RAG là cách cho AI tra cứu tài liệu của bạn trước khi trả lời. LLM là mô hình ngôn ngữ lớn, tức là loại AI đứng sau các chatbot.)
- **[Nguồn]** Airbnb (arXiv 2610.14428): thất bại còn lại chủ yếu do SOP thiếu bước mà nhân viên giỏi vẫn làm (`../nen-tang-bang-chung.md`). Nghĩa là chép quy trình từ người làm giỏi, không chép từ sổ tay.
- **[Nguồn]** TheAgentCompany (arXiv 2412.14161): agent tốt nhất chỉ hoàn thành 13,33% việc hành chính và 8,33% việc tài chính, thấp hơn nhiều so với việc lập trình (37,68%). Tác giả giải thích một phần bằng các việc cần thu thập thông tin từ nhiều người, đọc ảnh chụp, đi qua phần mềm phức tạp. (Agent là chương trình AI tự thực hiện nhiều bước để hoàn thành một việc.)
- **[Nguồn]** Dell'Acqua và cs. (HBS WP 24-013, chỉ đọc qua tóm tắt tìm kiếm): cùng một nhóm tư vấn viên dùng GPT-4 làm nhanh hơn ở việc "trong vùng" nhưng đúng ít hơn 19 điểm phần trăm ở việc "ngoài vùng". Nên phải tách quy trình thành từng bước nhỏ rồi xét riêng.

!!! tip "Nói đơn giản"
    Hai nghiên cứu cuối cho thấy AI không giỏi đều mọi việc: có việc nó làm nhanh, có việc nó làm sai nhiều hơn. Vì vậy chúng ta không giao cả quy trình cho AI. Chúng ta tách từng bước ra, rồi mới quyết định bước nào giao cho ai.

- **[Đề xuất] Cách gán nhãn mỗi bước:** với mỗi bước, bạn trả lời lần lượt các câu hỏi trong bảng dưới đây. Câu nào trả lời "có" thì dùng nhãn tương ứng.

| Câu hỏi | Nếu "có" | Ví dụ |
|---|---|---|
| Bước có quyết định tiền, pháp lý, quyền lợi người? | **Người** (AI có thể chuẩn bị) | Duyệt chi, loại ứng viên, hoàn tiền |
| Viết được thành luật "nếu ... thì ..." mà người khác đồng ý? | **Quy tắc** | Đơn > 5 triệu chuyển trưởng phòng; cộng tổng; đổi định dạng ngày |
| Đầu vào là chữ tự do, ảnh, giọng nói, cần hiểu nghĩa? | **AI** (kèm cổng kiểm) | Đọc tin Zalo để biết khách muốn gì; trích trường từ ảnh hóa đơn |
| Bước không ai dùng kết quả? | **Bỏ** | Chép số liệu sang file "dự phòng" không ai mở |

(Cổng kiểm là một chỗ dừng để người hoặc quy tắc kiểm lại kết quả của AI trước khi đi tiếp.)

Thứ tự ưu tiên khi phân vân: Bỏ → Quy tắc → Người → AI.

!!! tip "Nói đơn giản"
    Khi chưa biết gán nhãn nào, hãy thử theo thứ tự này: bước này có bỏ được không? Nếu không, có viết thành luật rõ ràng được không? Nếu không, có cần người quyết định không? Chỉ khi cả ba câu trên đều không, mới nghĩ tới AI.

## 4) Chuỗi bài nhỏ

Sáu bài dưới đây làm theo thứ tự. Mỗi bài có việc cần làm và thứ bạn có sau bài. Hầu hết các bài còn có "lỗi hay gặp" để bạn tránh.

### Bài Q0.1: Chọn việc
- **Việc cần làm:** liệt kê 10 việc lặp lại; chấm mỗi việc 1-5 theo tần suất, thời gian/lượt, mức đau (lỗi, chậm), rủi ro nếu sai. Chọn 1-3 việc tần suất cao, rủi ro vừa.
- **Bạn có sau bài:** bảng 10 việc có điểm.
- **Lỗi hay gặp:** chọn việc hiếm nhưng "ấn tượng"; chọn ngay việc chi tiền.

### Bài Q0.2: Quan sát và chép quy trình thật
- **Việc cần làm:** ngồi cạnh người làm giỏi nhất và người mới, mỗi người 3-5 lượt. Ghi từng thao tác: mở gì, chép gì, hỏi ai, chờ gì. Gộp thành 5-12 bước. Ghi điểm rẽ nhánh và ngoại lệ (đơn thiếu địa chỉ, CV gửi qua Zalo).
- **Bạn có sau bài:** bảng bước: #, việc, đầu vào, đầu ra, hệ thống, người làm, thời gian, ngoại lệ.
- **Lỗi hay gặp:** chỉ phỏng vấn trưởng phòng; bỏ qua bước "hỏi lại khách".

### Bài Q0.3: Gán nhãn Người / Quy tắc / AI / Bỏ
- **Việc cần làm:** dùng bảng ở mục 3. Với mỗi bước nhãn AI, viết một câu: "Nếu AI sai ở bước này thì ai phát hiện, khi nào?". Không trả lời được thì đổi sang Người.
- **Bạn có sau bài:** bảng có nhãn; đếm số bước theo nhãn.
- **Lỗi hay gặp:** gắn AI cho bước chỉ cần công thức.

### Bài Q0.4: Bản đồ dữ liệu
- **Việc cần làm:** mỗi bước ghi loại dữ liệu theo 5 mức của `../an-toan-du-lieu-va-phap-ly-vn.md` mục 3.1; nơi lưu (Zalo, Sheets, KiotViet, máy cá nhân); dịch vụ đi qua; ai xem được.
- **Bạn có sau bài:** bảng dữ liệu, đánh dấu chặng có dữ liệu cá nhân ra nước ngoài.
- **Lỗi hay gặp:** quên ảnh chụp màn hình gửi qua nhóm Zalo.

### Bài Q0.5: Đo nền 2 tuần
- **Việc cần làm:** một Google Sheet: ngày, mã lượt, người làm, giờ bắt đầu, giờ xong, kết quả (xong/trả lại/lỗi), ghi chú lỗi. Đo cả thời gian chờ (đơn nằm chờ duyệt bao lâu), không chỉ thời gian thao tác. Cách đo theo `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` bài 6.7.
- **Bạn có sau bài:** bảng đo nền: trung vị và khoảng (nhanh nhất-chậm nhất) thời gian, tỷ lệ lỗi, số lượt/tuần. (Trung vị là con số nằm giữa khi bạn xếp các lần đo từ nhỏ đến lớn. Nó ít bị kéo lệch bởi vài lần đo quá nhanh hoặc quá chậm.)
- **Lỗi hay gặp:** chỉ đo người giỏi; đo một ngày rồi nhân lên.

### Bài Q0.6: Chọn bước tự động hóa đầu tiên
- **Việc cần làm:** xếp các bước nhãn Quy tắc theo (thời gian tiết kiệm × tần suất). Chọn 1 bước cho Q1. Bước AI để sau, trừ khi nó chặn mọi thứ.
- **Bạn có sau bài:** một trang "kế hoạch Q1": bước nào, công cụ nào, ai phụ trách, đo gì.

## 5) Đường không code vs có code; khi nào buộc chuyển

Ở cấp này, bạn có thể làm hoàn toàn không cần code. Cột "Có code" chỉ dành cho trường hợp bạn muốn máy tự ghi số liệu thay cho người.

| | Không code | Có code |
|---|---|---|
| Vẽ quy trình | Giấy, bảng tính, Lark Base, sơ đồ trong Docs | Không cần |
| Đo nền | Google Sheet / Lark Base tự ghi | Xuất nhật ký từ phần mềm (nếu có API) bằng script nhỏ |
| AI hỗ trợ | Dán ghi chép quan sát (đã che tên, SĐT) vào Project/Gem để gợi ý gộp bước, phát hiện bước trùng | — |

(Nhật ký là bản ghi tự động mà phần mềm lưu lại mỗi khi có việc xảy ra. API là "cổng" để một chương trình khác lấy dữ liệu từ phần mềm. Script là một đoạn chương trình ngắn. SĐT là số điện thoại.)

**Buộc chuyển sang code:** chỉ khi muốn lấy số lượt và thời gian thật từ phần mềm (ví dụ thời điểm tạo và hoàn tất đơn trên KiotViet/Haravan) thay vì tự ghi tay. Không bắt buộc ở cấp này.

!!! tip "Nói đơn giản"
    Nếu bạn chưa muốn nhờ lập trình viên, cứ tự ghi tay vào Google Sheet. Cách này đủ dùng ở cấp này.

## 6) Tiêu chí lên Q1 (đo được) [Đề xuất]

Bạn có thể sang cấp Q1 khi đạt đủ các điều sau:

1. Có bảng quy trình cho ≥1 việc, người làm việc đó xác nhận "đúng như tôi làm".
2. Có đo nền ≥2 tuần hoặc ≥30 lượt, gồm trung vị thời gian và số lỗi.
3. Mỗi bước có nhãn; ≥1 bước nhãn Quy tắc được chọn cho Q1.
4. Có bản đồ dữ liệu; mọi chặng dữ liệu cá nhân ra ngoài được đánh dấu.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

Hai ví dụ dưới đây là tình huống giả định để bạn dễ hình dung cách gán nhãn. Chúng không phải số đo thật.

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

!!! tip "Nói đơn giản"
    Ví dụ b cho thấy vì sao phải đo cả thời gian chờ. Nếu việc chậm chủ yếu vì chờ người ký, thì dùng AI ở bước khác cũng không làm nó nhanh hơn.

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
