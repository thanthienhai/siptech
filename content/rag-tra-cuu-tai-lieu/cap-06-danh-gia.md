# Cấp 6 — Đánh giá (Evaluation) cho SME

Trạng thái: bản nháp nghiên cứu, soạn ngày 2026-11-11. Quy ước: **[Nguồn]** = kết quả có trong tài liệu đã đọc; **[Đề xuất]** = ý kiến của nhóm biên soạn, chưa được nguồn nào chứng minh; **[Tự tính]** = số do chúng tôi tính bằng mã trong mục 4, chưa đối chiếu nguồn ngoài.

---

## 1. Mục tiêu và người đọc

**Người đọc:** chủ SME, trưởng bộ phận, hoặc một nhân viên được giao "phụ trách AI" ở công ty 5–100 người, đang dùng Claude/ChatGPT/Gemini (C0) hoặc đã có Project/Gem/GPT tùy chỉnh, hoặc bot gọi API (C1–C5). Không cần biết thống kê. Đường code nhẹ cần biết chạy một file Python.

**Sau cấp này, người đọc có trong tay (sản phẩm cầm đi được):**
1. Một bảng tính "bộ ca vàng" (golden set) 20–30 ca có đáp án, chia theo loại việc.
2. Một quy tắc chấm (rubric) đúng/sai viết ra giấy.
3. Một con số "tỉ lệ đúng" kèm khoảng tin cậy, để biết con số đó đáng tin đến đâu.
4. (Tùy chọn) một bộ chấm tự động bằng AI đã được kiểm chứng với người chấm.
5. Một quy tắc quyết định "bản prompt/quy trình mới tốt hơn hay không" trước khi cả công ty dùng.

**Phạm vi:** đo chất lượng đầu ra của hệ thống AI trên công việc cụ thể của công ty. Không phải xếp hạng mô hình chung chung.

---

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

Cấp 5 (trả lời có trích dẫn) cho ra câu trả lời *trông* đáng tin vì có nguồn. Lỗi thường gặp dẫn tới Cấp 6:

- "Thấy ổn" sau khi thử 3–5 câu rồi triển khai (đánh giá bằng cảm giác).
- Sửa prompt để vá một lỗi, không biết đã làm hỏng ba việc khác.
- Chọn giữa hai prompt/hai mô hình theo ấn tượng hoặc theo câu dễ nhớ nhất.
- Có trích dẫn nhưng trích dẫn sai tài liệu, hoặc tìm đúng tài liệu mà trả lời sai (hai lỗi khác nhau, cần đo riêng).
- Báo cáo "AI tiết kiệm 50% thời gian" mà không có đối chứng.

**Câu hỏi của Cấp 6:** *Hệ thống này đúng bao nhiêu phần trăm trên việc thật của chúng ta, và mình có đủ bằng chứng để nói vậy chưa?*

---

## 3. Kiến thức nền (ngắn, chính xác)

### 3.1 Bằng chứng về cách đánh giá ngoài thực tế

- **[Nguồn, đã đối chiếu với toàn văn khi rà soát 2026-11-11]** MAP (arXiv 2512.04123): 74% hệ thống đánh giá có người, 52% dùng LLM-as-judge, 75% không dùng benchmark chính thức mà dùng A/B hoặc phản hồi chuyên gia. Mẫu chung: bộ câu hỏi–đáp "chuẩn vàng", thu tương tác thật, chuyên gia mở rộng dần; LLM judge cho điểm tin cậy, ca điểm thấp chuyển chuyên gia, ca điểm cao vẫn lấy mẫu ngẫu nhiên.
- **[Nguồn, đã đối chiếu với toàn văn khi rà soát 2026-11-11]** Nubank (arXiv 2606.08867): vài trăm nhãn nhị phân đủ dựng một bộ chấm; 3 chuyên viên gán nhãn, lấy đa số, giữ lời giải thích; tối ưu prompt bộ chấm làm độ chính xác bộ chấm ở một thí nghiệm tăng 58,07% → 73,01%; prompt viết tay ở thí nghiệm khác còn thua đoán lớp đa số (68,88% so với 77,78%). Bài học: *prompt chấm viết tay chưa kiểm chứng có thể tệ hơn đoán bừa theo lớp đông nhất.*
- **[Nguồn do chủ dự án cung cấp]** Airbnb (arXiv 2610.14428): chấm 3 lần lấy đa số vì một lần chấm có bất đồng khoảng 15%.
- **[Nguồn đã đọc]** Anthropic, "Demystifying evals for AI agents": "20-50 simple tasks drawn from real failures is a great start"; thay đổi ban đầu thường có hiệu ứng lớn nên mẫu nhỏ phát hiện được; ba loại grader (mã, mô hình, người); nên ưu tiên grader xác định (deterministic), thêm LLM grader khi cần, dùng người ít nhưng để hiệu chuẩn; "You won't know if your graders are working well unless you read the transcripts and grades from many trials."

### 3.2 Thống kê khi n nhỏ (phần then chốt của cấp này)

**Nguyên lý bền:** một tỉ lệ đúng đo trên n ca chỉ là *ước lượng*. Nhìn n nhỏ thì khoảng không chắc chắn rất rộng.

- **[Nguồn]** Anthropic (Miller, arXiv 2411.00640): coi các câu hỏi như mẫu rút từ một "tổng thể" vô hạn; với điểm 0/1, sai số chuẩn SE = √(p(1−p)/n); khoảng tin cậy 95% ≈ p ± 1,96·SE; khi so hai hệ thống trên **cùng** bộ câu hỏi, nên phân tích hiệu theo từng câu (paired) vì cho sai số nhỏ hơn; nên báo cả n và sai số chuẩn; chấm lại mỗi câu K lần giảm nhiễu do ngẫu nhiên của mô hình; khuyên không chỉnh temperature chỉ để giảm nhiễu. Ví dụ trong bài: phát hiện chênh 3 điểm phần trăm với độ tin 80% cần khoảng 969 câu độc lập (trong ví dụ giả định của bài: phân tích theo từng câu, không có nhiễu ngẫu nhiên khi lấy mẫu câu trả lời, alpha 0,05), và bài khuyên eval mới nên có ≥ ~1.000 câu để "signal" tốt. **Hệ quả cho SME: 20–30 ca KHÔNG đủ để phát hiện chênh vài điểm phần trăm. Nó chỉ đủ để phát hiện chênh rất lớn hoặc lỗi hàng loạt.**
- **[Nguồn]** Wikipedia (Binomial proportion confidence interval): xấp xỉ chuẩn (Wald) "becomes unreliable… as the sample size becomes small or the success probability grows close to either 0 or 1"; khi p̂ → 0 hoặc 1 khoảng Wald co về độ rộng 0, gây ảo giác chắc chắn; **quy tắc ba**: nếu 0 lần sai trên n ca, khoảng 95% xấp xỉ (0, 3/n) [tức nếu 20/20 đúng thì giới hạn trên của tỉ lệ sai ≈ 15%]. Công thức Wilson được dùng trong mã mẫu (mục 4, bài 6.2).
- **[Tự tính, đã chạy thử Python 2026-11-11]** Khoảng Wilson 95% của tỉ lệ đúng:

| Kết quả | Tỉ lệ | Khoảng 95% (Wilson) |
|---|---|---|
| 18/20 | 90% | 0,70 – 0,97 |
| 27/30 | 90% | 0,74 – 0,97 |
| 20/20 | 100% | 0,84 – 1,00 |
| 45/50 | 90% | 0,79 – 0,96 |
| 90/100 | 90% | 0,83 – 0,94 |
| 450/500 | 90% | 0,87 – 0,92 |

**Nói thẳng cho SME:** "18/20 đúng" nghĩa là tỉ lệ đúng thật có thể từ khoảng 70% đến 97%. Hai prompt đạt 18/20 và 20/20 **chưa** phân biệt được bằng thống kê (khoảng chồng nhau mạnh). Bộ 20–30 ca là bộ **phát hiện hỏng** (smoke/regression), không phải thước đo chính xác. Khi cần so hai phương án sát nhau, phải tăng ca (50–100+) hoặc chấm lại nhiều lần, hoặc dùng quyết định theo "ca nào đổi kết quả" (mục 4, bài 6.8) và chấp nhận kết luận yếu.

**Về cỡ mẫu "tối thiểu":** không có một con số tối thiểu chung; nó phụ thuộc mức chênh muốn phát hiện (công thức công suất ở Miller, phương trình 9 và 10). Con số 20–30 ca là **[Đề xuất]** theo logic "bắt đầu nhỏ" của Anthropic (20–50 ca từ lỗi thật), không phải ngưỡng thống kê.

### 3.3 LLM-as-a-judge: thiên lệch đã biết

**[Nguồn]** Zheng và cs., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (arXiv 2306.05685, NeurIPS 2023):
- **Thiên lệch vị trí (position bias):** khi đổi chỗ hai câu trả lời, phán quyết nhiều khi đảo. Độ nhất quán sau khi đổi chỗ (prompt mặc định): GPT-4 65,0%, GPT-3.5 46,2%, Claude-v1 23,8% (đây là các mô hình năm 2023; số hiện nay sẽ khác).
- **Thiên lệch độ dài (verbosity):** thí nghiệm "danh sách lặp" làm câu trả lời dài thêm mà không thêm nội dung; tỉ lệ judge bị lừa: Claude-v1 và GPT-3.5 đều 91,3%, GPT-4 8,7% (23 câu).
- **Tự ưu ái (self-enhancement):** GPT-4 tự chấm mình cao hơn người 10% (win rate), Claude-v1 25%, nhưng GPT-3.5 không; **chính tác giả nói dữ liệu ít, chưa kết luận được**.
- **Chấm sai câu có đáp án (toán/suy luận):** nếu không cho đáp án tham chiếu, judge hay bị câu trả lời sai làm lạc hướng; tỉ lệ thất bại 14/20 (prompt mặc định), 6/20 (chain-of-thought), 3/20 (có đáp án tham chiếu). Bài báo: **chấm có đáp án tham chiếu (reference-guided) giảm lỗi rõ rệt.**
- **Cách giảm:** đổi chỗ hai câu và chỉ coi là thắng khi thắng ở cả hai thứ tự (không thì hòa); ví dụ mẫu (few-shot) tăng độ nhất quán của GPT-4 từ 65,0% lên 77,5% nhưng làm chi phí gọi tăng khoảng 4 lần (theo bài).
- **Độ đồng thuận với người:** GPT-4 đạt 85% với chuyên gia người trong thiết lập không tính hòa, so với 81% giữa người với người (MT-bench). Đây là bộ câu hỏi mở, không phải nghiệp vụ SME, nên **không suy ra judge nào cũng đạt mức đó trên việc của bạn.**

**[Nguồn]** Panickssery và cs. (arXiv 2404.13076): các LLM có xu hướng tự ưu ái đầu ra của chính mình; độ mạnh của tự ưu ái tương quan tuyến tính với khả năng nhận ra đầu ra của mình (thí nghiệm tinh chỉnh, trên tóm tắt tin tức). Họ cũng báo tỉ lệ đảo phán quyết khi đổi thứ tự là 25% (GPT-4), 58% (GPT-3.5), 89% (Llama 2). Bằng chứng ở mức "ban đầu" theo chính tác giả.

**[Nguồn]** Dubois và cs. (arXiv 2404.04475, Length-Controlled AlpacaEval): tỉ lệ thắng của một mô hình chỉ đổi do yêu cầu "trả lời chi tiết/ngắn gọn" từ 22,9% đến 64,3% khi chấm thô; sau hiệu chỉnh độ dài còn 41,9% đến 51,6%. Tức *độ dài câu trả lời có thể làm lệch điểm LLM chấm rất mạnh.* Cách họ sửa là hồi quy thống kê, SME không cần làm; SME chỉ cần biết để **chấm theo tiêu chí, không chấm "câu nào hay hơn"** và để ý độ dài.

### 3.4 Kappa — giải thích dễ hiểu

Giả sử người và AI cùng chấm 10 ca đúng/sai. Họ trùng nhau 8/10 = 80%. Nhưng nếu cả hai đều hay nói "đúng" thì trùng ngẫu nhiên cũng cao. **Cohen's kappa** trừ đi phần trùng "do may rủi":

κ = (p_o − p_e) / (1 − p_e), với p_o là tỉ lệ trùng quan sát, p_e là tỉ lệ trùng kỳ vọng nếu hai bên chấm độc lập theo tần suất của mình. **[Nguồn: Wikipedia, Cohen's kappa]**

- κ = 0: không hơn đoán ngẫu nhiên; κ = 1: trùng hoàn toàn.
- Bảng Landis–Koch: 0,41–0,60 trung bình; 0,61–0,80 đáng kể; 0,81–1,00 gần hoàn hảo. **[Nguồn]** Nhưng Wikipedia ghi rõ các ngưỡng này "by no means universally accepted" và kappa phụ thuộc tỉ lệ các lớp (prevalence) và số lớp. Vậy: **dùng ngưỡng như hướng dẫn thô, không phải luật.**
- **[Tự tính, đã chạy thử]** Ví dụ 10 ca: người [1,1,0,1,0,1,1,0,1,1], AI [1,1,0,1,1,1,1,0,1,0] → trùng 80% nhưng κ ≈ 0,52 (trung bình). Một "judge" luôn nói "đúng" khi người chấm 8/10 đúng sẽ trùng 80% mà κ = 0.
- **[Nguồn: Hamel Husain, "Your AI Product Needs Evals"]** Khi các lớp mất cân bằng đừng chỉ nhìn % trùng khớp; đo riêng precision và recall.
- Với n = 20–30 ca, bản thân kappa cũng rất nhiễu **[Đề xuất/nhận xét thống kê chung, chưa có nguồn đã đọc]**. Vì vậy, mục tiêu thực tế: xem *những ca nào* AI và người bất đồng và vì sao, hơn là tin vào một con số κ.

### 3.5 Tách "tìm đúng tài liệu" khỏi "trả lời đúng"

**[Đề xuất, logic đo lường]** Với hệ thống Cấp 4–5 (tìm kiếm + trả lời), mỗi ca nên có hai nhãn độc lập:
- **Truy hồi (retrieval) đúng?** Tài liệu/đoạn có chứa đáp án có nằm trong các đoạn được đưa cho AI không? (đo bằng người xem log, hoặc tự động nếu ghi sẵn ID tài liệu đúng).
- **Trả lời đúng?** Với đoạn đã đưa, câu trả lời có đúng và trích dẫn có khớp không?

Bảng chẩn đoán 2×2: truy hồi sai + trả lời sai → sửa Cấp 3–4 (chia khối, tìm kiếm); truy hồi đúng + trả lời sai → sửa prompt/mô hình; truy hồi sai + trả lời "đúng" → nghi ngờ đoán mò hoặc rò rỉ (AI biết sẵn từ dữ liệu huấn luyện), không nên tin.

---

## 4. Chuỗi bài nhỏ

Mỗi bài ≈ 30–90 phút. Làm theo thứ tự. Bài 6.1–6.5 đủ cho đường không code.

### Bài 6.1 — Chọn loại việc và định nghĩa "đúng"
- **Mục tiêu:** viết ra một câu "việc này đúng khi…" cho từng loại việc.
- **Thực hành:** (1) Liệt kê 1–3 việc AI đang làm cho công ty (ví dụ: tra cứu quy định nội bộ, soạn email báo giá, trích số liệu từ hóa đơn, phân loại ticket). (2) Xếp mỗi việc vào một trong 4 loại và dùng metric tương ứng (bảng dưới). (3) Với mỗi việc, viết tiêu chí đúng/sai 3–5 gạch đầu dòng, người ngoài đọc cũng chấm giống nhau được.

| Loại việc | Metric gợi ý **[Đề xuất]** | Cách chấm |
|---|---|---|
| Tra cứu / hỏi đáp | Đúng sự thật so với tài liệu; trích dẫn khớp; "từ chối đúng" khi không có thông tin | Người hoặc judge có đáp án tham chiếu |
| Trích xuất (hóa đơn, hợp đồng) | Đúng từng trường (khớp chính xác), tỉ lệ ca đúng toàn bộ trường | Mã so sánh tự động (grader mã) |
| Phân loại | Độ chính xác, và precision/recall từng lớp nếu lớp mất cân bằng | Mã so sánh nhãn |
| Soạn thảo (email, bài đăng) | Danh sách kiểm (đủ ý bắt buộc, đúng giọng, không bịa số liệu, độ dài), dùng nhị phân từng mục | Người; judge theo từng mục nhị phân |

- **Sản phẩm:** một trang "định nghĩa đúng" cho mỗi loại việc.
- **Lỗi thường gặp:** tiêu chí mơ hồ ("hay", "tự nhiên"); trộn nhiều tiêu chí vào một điểm 1–10. Hamel Husain khuyên bắt đầu bằng nhãn nhị phân tốt/xấu vì dễ quản lý hơn thang điểm chi tiết **[Nguồn]**.

### Bài 6.2 — Dựng bộ 20–30 ca có đáp án
- **Mục tiêu:** bảng tính "bộ ca vàng" đầu tiên.
- **Thực hành:**
  1. Tạo bảng (Google Sheets/Excel) với cột: `id`, `loai_viec`, `muc_do` (de/trung_binh/kho), `dau_vao`, `dap_an_chuan` (hoặc tiêu chí bắt buộc), `tai_lieu_dung` (ID tài liệu chứa đáp án, nếu có), `nguon_ca` (thật/giả lập/ngoại lệ), `nguoi_viet`, `ngay`.
  2. **Chọn ca [Đề xuất]:**
     - Ưu tiên ca **lấy từ thực tế**: câu khách/nhân viên đã hỏi, lỗi AI đã từng mắc (cùng tinh thần "tasks drawn from real failures" của Anthropic **[Nguồn]**).
     - **Phân tầng:** chia theo loại việc, theo độ khó, theo nhóm khách/sản phẩm; mỗi tầng ít nhất vài ca, đừng để 25/30 ca là loại dễ.
     - **Ca khó:** câu nhiều điều kiện, tài liệu mâu thuẫn, số liệu phải tính.
     - **Ca ngoại lệ:** câu không có đáp án trong tài liệu (AI phải nói "không có thông tin"), câu ngoài phạm vi, câu mơ hồ cần hỏi lại, câu nhạy cảm, dữ liệu sai chính tả/tiếng Việt không dấu, viết tắt.
  3. Hai người độc lập viết hoặc kiểm đáp án; ca bất đồng thì họp thống nhất rồi ghi lý do.
  4. Che dữ liệu nhạy cảm (tên, số điện thoại, CMND/CCCD, số tài khoản) trước khi đưa vào bảng, đặc biệt nếu bảng lưu ở nơi nhiều người xem.
  5. **Chia held-out:** tách ngay từ đầu khoảng 1/3 số ca làm bộ **giữ kín (held-out)**; bộ còn lại là bộ **phát triển (dev)**. Chỉ dùng dev để chỉnh prompt. Held-out chỉ chạy khi chốt phiên bản. **[Đề xuất]** Lý do: nếu bạn nhìn kết quả từng ca rồi sửa prompt cho đúng các ca đó, điểm trên chúng không còn phản ánh chất lượng thật (học vẹt trên ca dev). Với n = 25 thì 8 ca held-out là *rất* ít; xem mục thống kê 3.2 và coi held-out như "kiểm tra nhanh có bị overfit không", không phải phép đo chính xác. Anthropic nói về "saturation" (khi đạt hết ca giải được thì phải thêm ca khó) nhưng bài đó **không** bàn held-out **[Nguồn]**; khái niệm held-out ở đây là thông lệ chung của học máy, chúng tôi đề xuất áp dụng.
  6. Hàng tháng thêm 3–5 ca từ lỗi mới thực tế (bộ ca "lớn dần", giống mẫu "chuyên gia mở rộng dần" trong MAP **[Nguồn do chủ dự án cung cấp]**). Ca đã đổi thì ghi phiên bản, không sửa đè.
- **Sản phẩm:** file bảng tính `bo_ca_vang_v1`.
- **Lỗi thường gặp:** chỉ toàn ca dễ; đáp án chuẩn do chính AI viết rồi dùng AI chấm (vòng tròn); ca chứa dữ liệu khách thật rò ra ngoài; quên cập nhật đáp án khi chính sách/giá đổi.

### Bài 6.3 — Chấm tay có kỷ luật
- **Mục tiêu:** có điểm "chuẩn vàng" từ người, kèm lý do.
- **Thực hành:**
  1. Chạy hệ thống trên toàn bộ ca, lưu đầu ra vào cột mới (một cột cho mỗi phiên bản prompt).
  2. Người chấm **không biết** đầu ra nào của phiên bản nào (xáo trộn/ẩn nhãn) khi so hai phiên bản **[Đề xuất]**.
  3. Chấm đúng/sai theo tiêu chí Bài 6.1; ghi 1 dòng lý do khi sai (loại lỗi: bịa, thiếu ý, sai số, sai giọng, lẽ ra phải từ chối...). Phân loại lỗi này quan trọng hơn con số.
  4. Nếu có thể, hai người cùng chấm ít nhất 10 ca; tính tỉ lệ trùng và kappa (mã dưới) để biết chính *tiêu chí* có rõ không. Hai người mà còn bất đồng nhiều thì sửa tiêu chí trước, đừng đổ lỗi cho AI. (Nubank dùng 3 chuyên viên và lấy đa số, giữ lời giải thích **[Nguồn do chủ dự án cung cấp]**.)
  5. Đọc đầu ra thật, không chỉ nhìn điểm **[Nguồn: Anthropic; Hamel Husain "You can never stop looking at data"]**.
- **Sản phẩm:** cột `diem_nguoi` (0/1) và `loai_loi` cho mỗi ca.
- **Lỗi thường gặp:** chấm khi đã biết đây là bản "mới" (thiên vị xác nhận); chấm theo cảm giác từng hôm; sửa đáp án chuẩn cho khớp AI.

### Bài 6.4 — Tách đo "tìm đúng tài liệu" và "trả lời đúng" (cho hệ thống Cấp 4–5)
- **Mục tiêu:** biết lỗi nằm ở tìm kiếm hay ở trả lời.
- **Thực hành:** thêm hai cột `truy_hoi_dung` (0/1: tài liệu đúng có trong đoạn đưa cho AI không) và `tra_loi_dung` (0/1). Lấy ID tài liệu từ log (xem Cấp 9). Lập bảng 2×2 theo mục 3.5. Báo hai tỉ lệ riêng, kèm khoảng Wilson.
- **Sản phẩm:** bảng 2×2 và ưu tiên sửa (truy hồi hay prompt).
- **Lỗi thường gặp:** chỉ báo "độ chính xác chung"; dùng AI chấm "tài liệu có liên quan không" mà không kiểm với người.

### Bài 6.5 — Tính tỉ lệ đúng kèm khoảng tin cậy (mã mẫu)
- **Mục tiêu:** luôn báo "k/n (khoảng)" thay vì một con số trần.
- **Đường không code:** dùng Google Sheets; p = k/n; dùng công thức Wilson (Wikipedia, mục 3.2) hoặc tra bảng ở mục 3.2. Cách thô nhưng trung thực: ghi "18/20, rất rộng, khoảng 70–97%".
- **Đường code (Python 3, chỉ thư viện chuẩn). Trạng thái: ĐÃ CHẠY THỬ 2026-11-11, kết quả khớp bảng mục 3.2:**

```python
import math
from collections import Counter

def wilson(k, n, z=1.96):          # khoảng tin cậy ~95% cho tỉ lệ đúng
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return max(0, c-h), min(1, c+h)

def kappa(a, b):                   # a, b: hai danh sách nhãn cùng độ dài
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k]*cb[k] for k in set(a)|set(b)) / n**2
    return (po-pe)/(1-pe) if pe < 1 else float("nan")

def majority(votes):               # chấm nhiều lần lấy đa số
    return Counter(votes).most_common(1)[0][0]

print(wilson(18, 20))              # (0.70, 0.97)
```
- **Sản phẩm:** báo cáo một dòng: "Bản X: 24/30 đúng (80%, khoảng 62–90%); held-out 6/8".
- **Lỗi thường gặp:** dùng công thức Wald khi p gần 0/1 hoặc n nhỏ (khoảng sai); báo "tăng 10%" từ 8/10 lên 9/10.

### Bài 6.6 — Chấm bằng AI (LLM-as-judge) có kiểm chứng
- **Mục tiêu:** thay phần lớn việc chấm tay bằng AI *chỉ khi* đã chứng minh nó trùng với người.
- **Thực hành:**
  1. **Ưu tiên grader mã** nếu đáp án so khớp được (trích xuất, phân loại) **[Nguồn: Anthropic]**. LLM judge chỉ cho việc cần đọc hiểu (tra cứu, soạn thảo).
  2. Viết prompt chấm: nhãn nhị phân theo từng tiêu chí; **kèm đáp án tham chiếu/ tài liệu nguồn** (giảm chấm sai, Zheng và cs. **[Nguồn]**); yêu cầu giải thích ngắn rồi mới kết luận (giữ lời giải thích như Nubank **[Nguồn do chủ dự án cung cấp]**).
  3. Giảm thiên lệch **[Nguồn Zheng và cs.; phần áp dụng là Đề xuất]**: nếu so hai câu trả lời thì đổi chỗ và chỉ tính thắng khi thắng cả hai chiều; ưu tiên chấm từng câu theo tiêu chí hơn là hỏi "câu nào hay hơn"; nêu rõ trong prompt rằng độ dài không phải điểm cộng; không dùng chính mô hình đã sinh câu trả lời làm judge nếu có lựa chọn khác (tự ưu ái, nhưng bằng chứng còn sơ bộ).
  4. **Kiểm chứng với người:** cho judge chấm đúng các ca người đã chấm (Bài 6.3). Tính: tỉ lệ trùng, kappa, và hai con số theo lớp (judge bắt được bao nhiêu % ca sai thật: recall của "sai"; trong số ca judge bảo sai, bao nhiêu % thật sự sai: precision). Đọc từng ca bất đồng.
  5. **Chấm nhiều lần lấy đa số:** chấm mỗi ca 3 lần, lấy đa số (Airbnb dùng cách này vì bất đồng một-lần ~15% **[Nguồn do chủ dự án cung cấp]**; Miller cũng nêu chấm lại K lần làm giảm nhiễu **[Nguồn]**). Chi phí tăng ~3 lần.
  6. Quy tắc dùng judge **[Đề xuất theo mẫu MAP]**: judge cho "tin cậy"; ca điểm thấp/không chắc chuyển cho người; ca điểm cao vẫn lấy mẫu ngẫu nhiên (ví dụ 5–10 ca mỗi đợt) cho người kiểm.
  7. Mỗi khi đổi mô hình judge hoặc prompt judge, kiểm chứng lại (Nubank: mỗi mô hình mới coi như thay đổi prompt **[Nguồn do chủ dự án cung cấp]**).
  8. **Tiêu chí tin judge [Đề xuất, ngưỡng do chúng tôi đặt, chưa có nguồn]:** recall của nhãn "sai" ≥ 80% *và* không có ca sai nghiêm trọng bị judge cho qua *và* đã đọc toàn bộ ca bất đồng. Nếu không đạt, dùng người chấm.
- **Đường không code:** dán đầu ra và tiêu chí vào Claude/ChatGPT/Gemini (Project/Gem/GPT tùy chỉnh làm "người chấm"), lưu kết quả vào bảng. Làm tay 25 ca vẫn khả thi. **Nhớ:** nếu bản chấm và bản sinh cùng một dịch vụ, bạn dính nguy cơ tự ưu ái.
- **Đường code:** gọi API chấm theo vòng lặp, lưu JSON có lý do và nhãn; dùng `majority()` ở trên.
- **Sản phẩm:** bảng "judge vs người": trùng %, kappa, precision/recall của nhãn sai, danh sách ca bất đồng và nguyên nhân; quyết định "tin/không tin judge cho loại việc này".
- **Lỗi thường gặp:** tin judge vì nó "nghe hợp lý"; tối ưu prompt chấm trên chính bộ ca định đo (rò rỉ); tăng điểm bằng cách làm câu trả lời dài hơn.

### Bài 6.7 — Đo thời gian tiết kiệm (và cách khỏi tự lừa mình)
- **Mục tiêu:** có một con số "tiết kiệm" đáng tin hơn lời khen.
- **Thực hành [Đề xuất toàn bộ]:**
  1. Chọn 1 việc lặp lại; ghi **trước khi dùng AI** thời gian trung bình một đơn vị việc (ví dụ soạn một báo giá) trên 10–20 lần.
  2. Sau khi dùng AI: đo cùng cách, **bao gồm** thời gian đọc lại, sửa, tra cứu xác minh, và sửa lỗi phát sinh sau đó. Không chỉ đo "thời gian AI trả lời".
  3. Đo thêm chất lượng (số lần bị trả lại, lỗi khách phát hiện) vì nhanh mà sai là mất.
  4. Tránh tự lừa: (a) so cùng loại việc, cùng độ khó; (b) người đo không phải người muốn AI thành công nếu có thể; (c) không chọn riêng ca đẹp; (d) tính cả thời gian đào tạo/dựng ban đầu và chi phí API/gói thuê khi tính hoàn vốn; (e) báo khoảng/dải (nhanh nhất–chậm nhất), không chỉ trung bình; (f) nếu có thể, làm xen kẽ (tuần có AI/tuần không) hoặc chia ngẫu nhiên việc cho hai cách.
  5. Với n nhỏ, coi con số là ước lượng thô, chỉ ra quyết định khi chênh rất lớn.
- **Sản phẩm:** bảng "trước/sau" gồm thời gian, chất lượng, chi phí.
- **Lỗi thường gặp:** chỉ tính thời gian sinh; quên thời gian soát lỗi; so người giỏi nhất với AI trung bình hoặc ngược lại.

### Bài 6.8 — So hai phiên bản (A/B) và rollout nhỏ
- **Mục tiêu:** quyết định có đổi sang bản mới không.
- **Thực hành:**
  1. **Offline trước (cùng bộ ca):** chạy bản A và B trên cùng ca. Lập bảng "ca nào đổi": B đúng–A sai (B thắng), A đúng–B sai (B hỏng), còn lại giống nhau. Đây là so sánh theo từng ca (paired), cùng tinh thần Miller **[Nguồn]**.
  2. **Quy tắc phát hành [Đề xuất, theo tinh thần BMO ESCROW & Nubank, thu nhỏ]:** chỉ chấp nhận B khi (a) không có nhóm/loại việc nào xấu đi, (b) các ca đã sửa trước đây vẫn đúng, (c) số ca B hỏng bằng 0 hoặc đã giải thích được. **[Nguồn do chủ dự án cung cấp]** ESCROW: bản sửa chỉ nhận khi không nhóm nào xấu đi và ca đã sửa trước đó vẫn đúng; không giữ kho ca cũ thì điểm trên ca cũ tụt từ 0,857 xuống 0,7, có giữ thì ~0,84.
  3. **Đọc bằng số, thật thà:** **[Tự tính]** với test dấu (sign test, hai phía) trên các ca khác nhau: 5 ca B thắng và 1 ca B hỏng cho p ≈ 0,22 (không đủ kết luận); 8 thắng và 0 hỏng cho p ≈ 0,008. Tức là với 25–30 ca chỉ phát hiện được cải thiện *rất rõ*, đúng như mục 3.2.
  4. **Rollout nhỏ:** cho bản mới chạy với 1 người hoặc 1 nhóm nhỏ hoặc 10% lượt dùng trong 1–2 tuần, giữ cách rút lại (rollback) một nút bấm. Nubank rollout 1% rồi tăng dần và theo dõi tNPS và tỉ lệ tự phục vụ vì hai chỉ số đánh đổi nhau **[Nguồn do chủ dự án cung cấp]**. Điểm offline tương quan với kết quả online trong nghiên cứu đó, nhưng với SME hãy tự kiểm tra: bản thắng offline có được người dùng ưa không.
  5. Chỉ số online cho SME **[Đề xuất]**: tỉ lệ người dùng phải sửa nặng; số lần "không dùng được"; số ticket/khiếu nại; thời gian xử lý.
- **Sản phẩm:** biên bản "phát hành/không phát hành" 1 trang: bảng ca đổi, nhóm xấu đi, kết luận, người duyệt.
- **Lỗi thường gặp:** đổi nhiều thứ cùng lúc (mô hình + prompt + tài liệu) nên không biết cái nào gây ra; so trên bộ ca đã dùng để chỉnh (không held-out); chỉ nhìn điểm trung bình.

### Bài 6.9 — Chốt bộ đánh giá thành thủ tục
- **Mục tiêu:** đánh giá thành thói quen, không phải việc một lần.
- **Thực hành:** viết "Thủ tục đánh giá 1 trang": khi nào chạy (đổi prompt, đổi mô hình, đổi tài liệu, hàng tháng); ai chạy; ngưỡng; lưu kết quả ở đâu (bảng có cột ngày + phiên bản prompt); khi nào thêm ca. Phần vận hành chi tiết nằm ở Cấp 9.
- **Sản phẩm:** thủ tục và một bảng kết quả theo thời gian.

---

## 5. Đường không code vs đường có code; khi nào buộc phải chuyển

| Việc | Không code (Project/Gem/GPT + Sheets) | Có code (Python nhẹ) |
|---|---|---|
| Lưu bộ ca | Google Sheets/Excel | CSV/JSON trong thư mục có theo dõi phiên bản |
| Chạy hệ thống trên ca | Dán từng ca, hoặc chia người chạy | Vòng lặp gọi API |
| Chấm | Người; hoặc dán vào AI từng ca | `majority()`, lưu lý do |
| Thống kê | Công thức Sheets/bảng mục 3.2 | `wilson()`, `kappa()` |
| Chấm lại 3 lần | Tốn công, thường bỏ | Dễ, tăng chi phí gọi ~3 lần |

**Khi nên chuyển sang code [Đề xuất, ngưỡng tham khảo, tự điều chỉnh]:** (1) chạy bộ ca thủ công mất hơn khoảng 1–2 giờ mỗi lần và bạn né không chạy; (2) cần chạy lại sau mỗi lần đổi (đa phiên bản); (3) bộ ca > ~50; (4) cần chấm nhiều lần lấy đa số hoặc dùng judge; (5) cần log cấu trúc để tách truy hồi/trả lời tự động (Cấp 9).

---

## 6. Tiêu chí lên cấp tiếp theo (Cấp 7 công cụ / Cấp 8 quy trình / Cấp 9 vận hành)

Chỉ lên cấp khi **cả bốn** điều sau đúng **[Đề xuất]**:
1. Có bộ ≥ 20 ca có đáp án, đã chia dev/held-out, hai người đồng ý đáp án.
2. Mỗi kết quả được báo dạng "k/n (khoảng tin cậy)", không là con số trần.
3. Có quy tắc phát hành bằng văn bản (không bản mới nào lên khi có nhóm xấu đi).
4. Nếu dùng judge: đã so với người trên ít nhất 20 ca, đã đọc ca bất đồng, có tiêu chí tin/không tin ghi ra.

Trước **Cấp 7/8** (công cụ, nhiều bước): bộ ca phải mở rộng để có ca cho cả bước trung gian và dùng công cụ (xem bài báo arXiv 2610.03315 ở mục 8 về chấm quỹ đạo nhẹ). Trước **Cấp 9**: cần thủ tục ở Bài 6.9 đang chạy ổn.

---

## 7. Ví dụ cho SME Việt Nam (minh họa, **không** phải số liệu thật)

**Công ty phân phối vật liệu xây dựng ~30 người, bot hỏi đáp chính sách bảo hành/giá cho nhân viên kinh doanh (Project có tài liệu nội bộ):**
- Bộ ca 28 ca: 10 tra cứu bảo hành, 6 điều kiện giá sỉ/lẻ (khó: nhiều điều kiện), 5 câu ngoài tài liệu (đáp án đúng: "chưa có thông tin, hỏi phòng X"), 4 câu viết tắt/không dấu, 3 câu mâu thuẫn giữa bản chính sách cũ và mới. Giữ 9 ca làm held-out.
- Chấm tay: 2 người, trùng 26/28; 2 ca bất đồng do tiêu chí "có nêu thời hạn bảo hành không" mơ hồ → sửa tiêu chí.
- Kết quả bản 1: 20/28 (71%; khoảng Wilson ≈ 53–85%). Lỗi chia nhóm: 4 lỗi bịa số, 3 lỗi chọn nhầm phiên bản chính sách, 1 lỗi giọng.
- Sửa: thêm quy tắc "trích rõ ngày hiệu lực" và loại bản cũ. Bản 2: 24/28; ca đổi: 5 ca tốt lên, 1 ca hỏng. Quyết định: **không đủ để kết luận bằng thống kê**, nhưng không nhóm nào xấu đi ngoài 1 ca hỏng đã giải thích được → rollout cho 3 nhân viên trong 2 tuần, theo dõi số lần phải sửa tay.
- (Các con số 20/28, 24/28 là giả định minh họa; khoảng tin cậy thật của 20/28 cần tính bằng `wilson(20, 28)`.)

**Công ty kế toán dịch vụ 12 người, trích xuất trường từ hóa đơn:** grader mã so khớp từng trường (số hóa đơn, MST, ngày, tổng tiền); không cần judge AI. Báo "tỉ lệ ca đúng toàn bộ trường" và "đúng từng trường"; ca ngoại lệ: hóa đơn chụp mờ, hóa đơn song ngữ. Số tiền sai là lỗi nghiêm trọng, chặn phát hành dù điểm trung bình cao.

**Cửa hàng 5 người, soạn bài đăng:** metric là danh sách kiểm nhị phân (đúng giá, đúng khuyến mãi, không hứa quá, độ dài), người chủ chấm 20 bài/tuần trong 10 phút; không cần judge.

---

## 8. Tài liệu tham khảo

Ngày truy cập tất cả: 2026-11-11. "Mức tin cậy" là nhận định của người soạn về độ bền và độ phù hợp với SME, không phải xếp hạng chính thức.

| # | Tiêu đề | URL | Loại | Mức tin cậy |
|---|---|---|---|---|
| 1 | Miller, "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations" (arXiv 2411.00640) | https://arxiv.org/abs/2411.00640 | Bài báo (preprint), tác giả Anthropic; **đã đọc toàn văn qua alphaXiv** | Cao cho phương pháp thống kê; ví dụ số là giả định |
| 2 | Zheng và cs., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (arXiv 2306.05685, NeurIPS 2023) | https://arxiv.org/abs/2306.05685 | Bài báo hội nghị; **đã đọc** | Cao về hiện tượng thiên lệch; số liệu theo mô hình 2023 đã cũ |
| 3 | Panickssery, Bowman, Feng, "LLM Evaluators Recognize and Favor Their Own Generations" (arXiv 2404.13076) | https://arxiv.org/abs/2404.13076 | Preprint; **đã đọc** | Trung bình (tác giả nói bằng chứng nhân quả chưa đầy đủ; chỉ thử trên tác vụ tóm tắt tin) |
| 4 | Dubois và cs., "Length-Controlled AlpacaEval" (arXiv 2404.04475) | https://arxiv.org/abs/2404.04475 | Preprint; **đã đọc** | Cao cho việc chứng minh thiên lệch độ dài; phương pháp sửa không dành cho SME |
| 5 | Anthropic, "Demystifying evals for AI agents" | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Blog kỹ thuật chính thức; **đã đọc qua công cụ tóm tắt trang** (không đọc nguyên văn) | Trung bình–cao; trích dẫn nên kiểm lại trên trang gốc |
| 6 | Wikipedia, "Binomial proportion confidence interval" | https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval | Bách khoa mở; **đã đọc qua công cụ tóm tắt** | Trung bình (đủ cho công thức Wilson/quy tắc ba; nên đối chiếu Brown–Cai–DasGupta 2001, chưa đọc) |
| 7 | Wikipedia, "Cohen's kappa" | https://en.wikipedia.org/wiki/Cohen%27s_kappa | Bách khoa mở; **đã đọc qua công cụ tóm tắt** | Trung bình |
| 8 | Hamel Husain, "Your AI Product Needs Evals" | https://hamel.dev/blog/posts/evals/ | Blog cá nhân của kỹ sư thực hành; **đã đọc qua công cụ tóm tắt** | Trung bình (kinh nghiệm thực hành, không phải nghiên cứu có đối chứng) |
| 9 | She, Lin, "Efficient Benchmarking in Production: A Study of an Evolving LLM Agent" (arXiv 2609.21267) | https://arxiv.org/abs/2609.21267 | Preprint; **đã đọc nội dung chính qua alphaXiv** | Trung bình (một tổ chức, một benchmark; tác giả tự nêu giới hạn); dùng ở Cấp 9 |
| 10 | Phan và cs., "Lightweight, Rubric-Guided Trajectory Evaluation for Production AI Agents" (arXiv 2610.03315) | https://arxiv.org/abs/2610.03315 | Preprint; **đã đọc nội dung chính qua alphaXiv** | Trung bình (dữ liệu nhỏ: 44 và 29 mẫu; tự nêu hiệu chuẩn judge còn là việc đang làm) |
| 11 | MAP, arXiv 2512.04123; Nubank, arXiv 2606.08867; BMO ESCROW, arXiv 2608.01772; Airbnb, arXiv 2610.14428 | https://arxiv.org/abs/2512.04123 ; https://arxiv.org/abs/2606.08867 ; https://arxiv.org/abs/2608.01772 ; https://arxiv.org/abs/2610.14428 | Preprint; **chủ dự án cung cấp số liệu và cho biết đã đọc kỹ; người soạn file này không đọc lại** | Số liệu lấy nguyên từ bản tóm tắt của chủ dự án; cần kiểm lại trước khi xuất bản |

---

## 9. Chưa kiểm chứng / cần kiểm tra lại

1. Số liệu MAP, Nubank, ESCROW, Airbnb: chưa đọc lại trong phiên này; chỉ chép đúng như chủ dự án cung cấp.
2. Các bài đọc qua công cụ tóm tắt trang (Anthropic blog, Wikipedia, Hamel Husain) chưa đọc nguyên văn: trích dẫn trực tiếp cần đối chiếu.
3. Số liệu thiên lệch vị trí/độ dài (Zheng và cs.) từ mô hình 2023; chưa có số cho mô hình hiện nay; nên tự đo trên judge bạn dùng (bài 6.6).
4. **Không tìm thấy nguồn** nêu "cỡ mẫu tối thiểu" riêng cho SME; các con số 20–30 ca, 1/3 held-out, ngưỡng recall ≥ 80% của judge, ngưỡng chuyển sang code là **đề xuất** của người soạn.
5. Ý kiến "kappa rất nhiễu khi n nhỏ" là nhận xét thống kê chung, chưa gắn với nguồn đã đọc.
6. Công thức khoảng Wilson trong mã đã chạy thử và khớp bảng, nhưng chưa đối chiếu với thư viện thống kê độc lập (ví dụ statsmodels).
7. Giá trị p của test dấu (0,22 và 0,008) tính tay từ phân phối nhị thức, chưa chạy bằng mã.
8. Kiểm tra held-out cho ca nhỏ (8–10 ca) có ý nghĩa thống kê rất thấp; chưa tìm nguồn nói về cách thức tốt nhất cho bộ nhỏ như vậy.
9. Công cụ cụ thể (Project, Gem, GPT tùy chỉnh, giao diện Sheets) thay đổi nhanh; bài viết giữ ở mức nguyên tắc, thao tác cụ thể cần kiểm lại ngày dùng.
