# Cấp 8 — Quy trình nhiều bước (workflow, và khi nào mới là agent)

Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** = kết quả trong tài liệu đã đọc; **[Đề xuất]** = ý kiến của chúng tôi, chưa được nguồn nào kiểm chứng; **[Nguyên tắc]** bền, **[Thao tác]** hay đổi.

---

## 1) Mục tiêu và người đọc

**Người đọc:** chủ SME, trưởng bộ phận (CSKH, kế toán, hành chính), người "biết Python nhẹ" hoặc người dùng thành thạo công cụ kéo-thả. Đã qua C7 (có ≥2 công cụ an toàn).

**Sau Cấp 8, doanh nghiệp làm được:**
- Phân biệt *workflow* (code quyết định thứ tự bước) với *agent* (mô hình tự quyết thứ tự), và chọn đúng cái đơn giản nhất đủ dùng.
- Chuyển một SOP của con người thành chuỗi bước cố định, mỗi bước có đầu vào/đầu ra rõ, cổng kiểm, trần số bước.
- Đặt **điểm duyệt của người** đúng chỗ, có hàng đợi, có người chịu trách nhiệm, không thành điểm nghẽn.
- Xử lý ngoại lệ: chuyển cho người **kèm đủ ngữ cảnh**.
- Đo chi phí, độ trễ, tỷ lệ duyệt/sửa/từ chối.

**Sản phẩm cầm đi được:** 1–3 quy trình chạy được (xem mục 7), mỗi quy trình có SOP bản "agent-hóa", sơ đồ bước, bảng điểm duyệt, bộ ca thử, bảng số đo.

---

## 2) Câu hỏi cấp này trả lời / lỗi của cấp trước dẫn đến cấp này

**Câu hỏi:** "Việc thật gồm nhiều bước, nhiều nguồn dữ liệu, có người duyệt — làm sao để AI làm phần máy làm được mà vẫn kiểm soát được?"

**Lỗi của cấp trước dẫn đến C8:**
- C7: mỗi lần chỉ một lượt hỏi–gọi công cụ–trả lời; nhân viên vẫn phải tự nối các bước (phân loại → tra → soạn → kiểm → gửi), nên không tiết kiệm đáng kể.
- C0–C7 nếu nhét tất cả vào *một prompt khổng lồ*: khó biết bước nào sai, khó sửa, khó đo.
- Hoặc ngược lại: cho AI "tự lo hết" (agent tự do) → khó đoán, khó kiểm, tốn tiền, sai thì sai dây chuyền.

**Cái giá của C8:** nhiều bước = chi phí và độ trễ cộng dồn, lỗi cộng dồn, và có hàng đợi người duyệt phải quản lý.

---

## 3) Kiến thức nền

### 3.1 Workflow vs agent [Nguồn]
- Anthropic ("Building effective agents"): **Workflows** là "systems where LLMs and tools are orchestrated through predefined code paths"; **Agents** là "systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks". Khuyến nghị: "find the simplest solution possible, and only increasing complexity when needed"; nhiều ứng dụng chỉ cần một lời gọi LLM tối ưu với truy xuất và ví dụ; agent đổi độ trễ và chi phí lấy hiệu năng; autonomy làm tăng chi phí và rủi ro sai dây chuyền; nên có điểm dừng (ví dụ số vòng tối đa) và điểm kiểm tra của người.
- Nubank (arXiv 2606.08867, mục 3.1) dùng cùng cách phân biệt: workflow là đồ thị tính toán định sẵn do *lập trình viên* điều khiển luồng; agent theo ReAct do LLM điều khiển vòng lặp. Họ nói triển khai của họ bám sát ReAct nhưng thêm guardrail và kiểm tra tuân thủ bắt buộc, dùng 5–15 công cụ, và có chuyển giao cho người khi độ tin cậy thấp.
- **MAP (arXiv 2512.04123, ICML 2026) — bằng chứng thực tế:** 20 ca phỏng vấn và khảo sát 86 hệ thống đang chạy:
  - 68% chạy tối đa 10 bước trước khi cần người can thiệp (bản tóm tắt abstract nói "at most 10"; mục 5.4 nói "fewer than 10"); 47% dưới 5 bước.
  - 80% (16/20) ca phỏng vấn dùng workflow có cấu trúc thay vì lập kế hoạch tự do; chỉ 1 ca khám phá không ràng buộc và chỉ trong sandbox có CI/CD kiểm chứng nghiêm ngặt (C09). Ví dụ C01 (bảo hiểm): chuỗi cố định tra phạm vi bảo hiểm → rà soát sự cần thiết y tế → nhận diện rủi ro; agent tự làm từng việc con nhưng mục tiêu cấp cao cố định.
  - 85% (17/20) ca có triển khai thật tự viết thay vì dùng framework: lý do là linh hoạt, đơn giản, bảo mật (chính sách doanh nghiệp cấm một số thư viện). Ở khảo sát, 61% đang dùng framework (LangChain/LangGraph 25%).
  - 66% cho phép phản hồi cỡ phút trở lên (chịu được độ trễ); 74% dựa chủ yếu vào đánh giá có người; 75% ca không dùng benchmark chính thức.
  - Giới hạn của chính bài: mẫu chủ yếu tự chọn (tự báo cáo), khảo sát trả lời chỉ một phần; mô tả thực tế *hiện nay*, không chứng minh cách đó tối ưu.
- Lưu ý đọc: số liệu MAP cho thấy các đội thật *chọn* workflow + ít bước + có người; không chứng minh rằng agent tự do "không bao giờ" đáng dùng.

### 3.2 Năm mẫu workflow [Nguồn: Building effective agents; đã đối chiếu đúng định nghĩa]

| Mẫu | Là gì | Dùng khi (theo tài liệu) | Ví dụ gốc |
|---|---|---|---|
| Prompt chaining | Chia việc thành các bước LLM tuần tự, có thể có cổng kiểm bằng code giữa các bước | Việc chia được rõ thành việc con cố định; "trade off latency for higher accuracy, by making each LLM call an easier task" | Viết quảng cáo rồi dịch; dàn ý → kiểm theo tiêu chí → viết |
| Routing | Phân loại đầu vào rồi chuyển sang tác vụ chuyên biệt | Các nhóm khác nhau xử lý riêng tốt hơn và phân loại đáng tin (bằng LLM hoặc bộ phân loại truyền thống) | Hỏi chung/hoàn tiền/kỹ thuật; câu dễ cho mô hình nhỏ |
| Parallelization | Chạy song song, gộp bằng code. Hai biến thể: *sectioning* (việc con độc lập) và *voting* (cùng việc, nhiều lần) | Cần tốc độ, hoặc mỗi khía cạnh cần chú ý riêng; hoặc nhiều lần chạy tăng độ tin | Một mô hình trả lời, mô hình khác sàng lọc nội dung; nhiều prompt rà lỗ hổng |
| Orchestrator-workers | LLM trung tâm tự chia việc, giao cho worker, tổng hợp | Việc con **không đoán trước được** từ đầu | Sửa nhiều tệp mã; tìm kiếm nhiều nguồn |
| Evaluator-optimizer | Một LLM tạo, một LLM chấm và phản hồi, lặp | Có tiêu chí đánh giá rõ và vòng lặp cải thiện đo được | Dịch văn học; tìm kiếm nhiều vòng |

**[Đề xuất] Với SME:** 90% nhu cầu rơi vào *chaining + routing* (+ *sectioning* khi cần nhanh). Orchestrator-workers chỉ khi bước con thật sự không biết trước. Evaluator-optimizer chỉ khi viết được tiêu chí chấm mà người khác đồng ý; nếu không, vòng lặp chỉ đốt tiền. (Đây là phán đoán của chúng tôi, không phải kết quả từ nguồn.)

### 3.3 Chuyển SOP thành các bước cố định [Nguồn + Đề xuất]
- **[Nguồn]** Nubank: chuyển SOP của nhân viên thành **routine** — chuỗi bước có thứ tự, ví dụ SOP giao thẻ 8 bước (chào, kiểm hệ thống logistics, phân tích trạng thái, nếu không thấy → điều tra, nếu thấy → hướng dẫn kích hoạt, nếu mất → cấp lại thẻ, gửi mẫu trả lời, đóng) → routine: chào/đóng khung ca → lấy dữ liệu → phân tích → hỏi điều tra theo loại địa chỉ → đề nghị cấp lại. Thêm **macros** (mẫu câu trả lời viết sẵn để agent điều chỉnh, không soạn từ đầu) và **scratchpad** (trạng thái làm việc: tham số đã thu, kết quả công cụ trước, bước hiện tại, tránh gọi lặp). Ba công cụ ở ca giao thẻ: `get_customer_profile`, `check_card_delivery`, `reissue_card`. Mỗi thành phần có phiên bản độc lập.
- **[Nguồn]** Nubank: "Compose deterministic flows in code, not in prompts" — nối nhiều nguồn dữ liệu thành một công cụ ghép; giảm trễ và loại lỗi thứ tự gọi.
- **BMO (arXiv 2608.01772)**: theo mô tả trong hồ sơ dự án, agent chạy theo skill bằng ngôn ngữ tự nhiên với 15 công cụ, đầu ra JSON lược đồ cố định, bước kiểm tra cố định. **Chưa đọc lại bài này trong lần soạn này** (xem mục 9).
- **[Đề xuất] Công thức chuyển SOP:** (1) chép SOP *đúng như nhân viên đang làm*, không như sổ tay lý tưởng; (2) đánh dấu mỗi bước: *máy làm chắc chắn* (code), *LLM làm* (hiểu/soạn/phân loại), *người làm* (quyết định, tiền, ngoại lệ); (3) mỗi bước LLM ghi đầu vào, đầu ra theo lược đồ cố định (JSON), ví dụ đúng/sai; (4) thêm cổng kiểm bằng code ở mọi chỗ kiểm được (số tiền khớp bảng giá, đủ trường, ngày hợp lệ); (5) ghi điều kiện rẽ nhánh và điều kiện chuyển người; (6) đặt trần số bước.

### 3.4 Điểm duyệt của người [Nguồn + Đề xuất]
- **[Nguồn]** MAP: người là kiểm chứng cuối ("agents suggest actions, experts approve execution"); ca bán ra ngoài dùng quy trình hạn chế: truy xuất cấu hình sẵn, "mandatory human approval at critical steps", chuỗi hành động cố định; các đội coi human-in-the-loop như nguyên tắc thiết kế có thể kéo dài, không chỉ là tạm thời. Nhóm dùng LLM-as-a-judge đều kết hợp duyệt người: điểm tin cậy thấp chuyển cho chuyên gia, lấy mẫu ngẫu nhiên phần tin cậy cao để kiểm tiếp (C01, C15).
- **[Nguồn]** OWASP LLM06: yêu cầu người duyệt hành động tác động cao trước khi thực hiện; kiểm soát quyền ở hệ thống hạ nguồn.
- **[Nguồn, công cụ]** n8n cho phép tạm dừng workflow chờ người duyệt qua Slack/Gmail/Teams..., người duyệt thấy tên công cụ và tham số; từ chối thì hủy và báo AI (docs.n8n.io, 2026-11-11).
- **[Đề xuất] Thiết kế điểm duyệt:**
  - *Khi nào:* trước mọi hành động ra ngoài (gửi khách, ghi vào sổ, chi tiền) và khi độ tin cậy thấp / dữ liệu thiếu / khách có dấu hiệu bực. Nubank có phát hiện khách bực và chuyển người sớm (đã thấy ở danh sách cải tiến; chi tiết chưa đọc kỹ).
  - *Ai:* người có thẩm quyền với *chính hậu quả đó*; không giao người duyệt thứ mình không hiểu. Có người thay thế khi vắng.
  - *Duyệt gì:* người duyệt phải thấy **bản sẽ gửi/chạy thật**, nguồn dữ liệu đã dùng (dòng bảng giá, điều khoản), kết quả cổng kiểm, và tham số chính xác; không chỉ "bản tóm tắt của AI".
  - *Hàng đợi:* mỗi mục có mã, hạn xử lý (SLA), trạng thái (chờ/đã duyệt/sửa/từ chối), người nhận; mục quá hạn leo thang; cảnh báo khi hàng đợi vượt ngưỡng. Nhiều ca vào cùng lúc → xếp theo mức khẩn.
  - *Chống "duyệt cho xong" (rubber-stamping):* nếu tỷ lệ duyệt không sửa >95% kéo dài, vẫn chọn ngẫu nhiên một phần để duyệt kỹ và đo lại; đừng bỏ duyệt chỉ vì tỷ lệ cao.
  - *Từ chối/sửa phải ghi lý do* — đây là dữ liệu để cải tiến prompt và bộ ca thử.

### 3.5 Ngoại lệ và chuyển giao đủ ngữ cảnh [Nguồn + Đề xuất]
- **[Nguồn]** Nubank: graceful handoff — "transfer control with full context preserved"; chuyển người khi ngoài routine, không lấy được dữ liệu, hoặc độ tin cậy thấp; hàm hành động idempotent; không quyết định không thể đảo ngược; xác thực và đồng ý của khách.
- **[Đề xuất] Gói chuyển giao tối thiểu:** mã phiếu; nội dung gốc của khách; các bước đã chạy và kết quả (từ scratchpad); dữ liệu đã tra; bản nháp (nếu có); **lý do chuyển** (ngoài phạm vi / thiếu dữ liệu / cổng kiểm lỗi / khách bực / lỗi hệ thống); đề xuất bước tiếp. Người nhận không phải hỏi lại khách điều khách đã nói.

### 3.6 Giới hạn bước, bất đồng bộ, trạng thái, chi phí, độ trễ [Nguồn + Đề xuất]
- **Giới hạn bước [Nguồn]:** Anthropic nêu điểm dừng như số vòng tối đa; MAP: 68% ≤10 bước. **[Đề xuất]** SME đặt trần *cứng* trong code (ví dụ 6–10 bước cho một phiếu) và trần ngân sách token/phiếu; vượt trần → chuyển người, không "thử thêm".
- **Bất đồng bộ [Nguồn]:** MAP ghi 66% chấp nhận độ trễ cỡ phút trở lên, nên agent chạy nền, người duyệt sau. (Con số "15/20 ca có thể chạy bất đồng bộ" đã được đối chiếu với toàn văn MAP mục 4.4 khi rà soát 2026-11-11.) **[Đề xuất]** thiết kế "nộp phiếu → hàng đợi → xử lý nền → thông báo người duyệt", không bắt người ngồi chờ.
- **Trạng thái/bộ nhớ làm việc [Nguồn]:** scratchpad của Nubank. **[Đề xuất]** lưu trạng thái theo mã phiếu trong một bảng/DB đơn giản; mỗi bước đọc và ghi; có thể chạy lại từ bước lỗi (kết hợp hàm idempotent từ C7). Không dùng bộ nhớ *dùng chung* cho nhiều người/khách mà chưa phân tách (hồ sơ dự án ghi bài SAP arXiv 2608.00122 cảnh báo nhiễm độc bộ nhớ dùng chung; chưa đọc lại bài).
- **Chi phí/độ trễ [Nguồn]:** Anthropic: agent đổi độ trễ và chi phí lấy hiệu năng; prompt chaining đổi độ trễ lấy độ chính xác; số token công cụ cũng tính phí (tài liệu tool use). **[Đề xuất]** đo từng bước: số token vào/ra, thời gian, tiền; nhìn chi phí *trên mỗi phiếu hoàn thành* và so với thời gian người làm tay; dùng mô hình nhỏ cho bước phân loại (routing) nếu đo thấy không giảm chất lượng.
- **Lỗi cộng dồn [Nguồn: Anthropic "compounding errors"] [Đề xuất]:** n bước, mỗi bước xác suất đúng p → đúng cả chuỗi ≈ pⁿ (phép tính đơn giản, giả định các bước độc lập; chỉ để minh họa: p=0,95, n=6 ⇒ ≈0,74). Vì vậy chuỗi ngắn + cổng kiểm + người duyệt tốt hơn chuỗi dài.

### 3.7 Khi nào KHÔNG nên làm agent (hoặc không nên nhiều bước) [Đề xuất, có dẫn nguồn ở các ý nền]
1. **Một lời gọi + truy xuất là đủ** (Anthropic: nhiều ứng dụng chỉ cần vậy) → ở C5/C7.
2. **Quy trình ổn định, biết trước các bước** → workflow cố định, không agent (MAP 80%).
3. **Hành động ghi tiền/không đảo ngược** mà chưa có người duyệt và hàm idempotent (Nubank, OWASP).
4. **Không có tiêu chí đúng/sai hay bộ ca thử** → không biết cải thiện hay hỏng; chưa nên tự động hóa.
5. **Không có người duyệt đủ nhân lực** → hàng đợi ứ, quy trình hỏng; làm nhỏ lại.
6. **Dữ liệu đầu vào chưa sạch** (bảng giá lỗi thời, chính sách mâu thuẫn) → sửa dữ liệu trước (cấp C2–C4).
7. **Việc xảy ra quá hiếm** (vài lần/tháng): chi phí xây + duy trì lớn hơn lợi.
8. **Cần quyết định có hậu quả pháp lý/tài chính lớn** mà người không thể kiểm lại độc lập.
9. **Agent đọc nội dung ngoài *và* có quyền ghi/gửi** mà chưa có cổng duyệt (xem C7, injection).
10. **Chưa đo được chi phí/phiếu** hoặc ngân sách không chịu được dao động chi phí.

---

## 4) Chuỗi bài nhỏ

`[NC]` = đường không code, `[PY]` = code nhẹ.

### Bài 8.1 — Chép SOP thật và chấm từng bước
- **Mục tiêu:** SOP "như đang làm" → bảng bước có nhãn *Code / LLM / Người*.
- **Làm:** (1) quan sát 5 ca thật, ghi từng thao tác; (2) gộp thành 5–10 bước; (3) mỗi bước ghi đầu vào/đầu ra, nhãn, điều kiện rẽ nhánh, điều kiện chuyển người; (4) gạch bước nào làm *tay* mất nhiều thời gian nhất.
- **Sản phẩm:** bảng SOP agent-hóa (mẫu ở mục 7).
- **Lỗi:** chép SOP trên giấy chứ không phải thực tế; gom mọi thứ vào một bước "AI xử lý".

### Bài 8.2 — Chuỗi hai bước đầu tiên (prompt chaining tối thiểu)
- **Mục tiêu:** tách "soạn" khỏi "kiểm" và đo cải thiện.
- **Làm:** **[NC]** hai prompt/hai Gem-Project: bước 1 soạn theo mẫu, bước 2 đối chiếu bản soạn với bảng giá và liệt kê sai lệch (người dán kết quả sang). **[PY]** hai hàm, giữa chúng là cổng kiểm bằng code. So sánh với "một prompt làm cả hai" trên 20 ca.
- **Sản phẩm:** bảng 20 ca × (đúng/sai, thời gian, token).
- **Lỗi:** không có ca thử nên cảm tính; để bước kiểm tự do thay vì tiêu chí cụ thể.

### Bài 8.3 — Routing và ngoại lệ
- **Mục tiêu:** phân loại đầu vào, ngoại lệ → người, có ngữ cảnh.
- **Làm:** nhóm đầu vào 3–5 loại + "khác/không chắc"; mọi thứ "khác/không chắc" vào hàng đợi người kèm gói chuyển giao (mục 3.5); đo tỷ lệ phân loại đúng trên ≥30 ca.
- **Sản phẩm:** bảng phân loại + mẫu gói chuyển giao.
- **Lỗi:** ép mọi thứ vào một loại; chuyển giao chỉ có câu "xử lý giúp".

### Bài 8.4 — Hàng đợi duyệt
- **Mục tiêu:** điểm duyệt vận hành được.
- **Làm:** **[NC]** một bảng tính/Notion/Trello làm hàng đợi (cột: mã, bản nháp, nguồn, trạng thái, người duyệt, hạn); hoặc n8n Human review (xem C7). **[PY]** bảng SQLite hoặc CSV. Đặt SLA, người thay thế, quy tắc leo thang.
- **Sản phẩm:** hàng đợi chạy được + quy tắc 1 trang.
- **Lỗi:** duyệt qua chat rời rạc, không dấu vết; người duyệt không thấy bản sẽ gửi thật.

### Bài 8.5 — Trần bước, trạng thái, chạy lại
- **Mục tiêu:** không chạy vô hạn, không mất việc khi lỗi giữa chừng.
- **Làm:** thêm đếm bước và trần; lưu trạng thái theo mã phiếu; chạy lại từ bước lỗi (không gọi lại bước ghi đã thành công, dựa idempotent); thử cố ý làm hỏng bước 3.
- **Sản phẩm:** log trạng thái + bài thử "bước 3 lỗi".
- **Lỗi:** thử lại vô hạn; chạy lại từ đầu làm gửi trùng.

### Bài 8.6 — Đo và quyết định
- **Mục tiêu:** có số để quyết định tiếp tục, thu hẹp, hay dừng.
- **Làm:** theo dõi 2–4 tuần: số phiếu, % tự động tới điểm duyệt, % duyệt không sửa, % sửa, % từ chối (kèm lý do), % chuyển người, thời gian từ nhận đến gửi, tiền/phiếu, lỗi lọt (khách báo sau gửi). So với làm tay.
- **Sản phẩm:** bảng số đo tuần + quyết định.
- **Lỗi:** chỉ đo tốc độ, bỏ qua lỗi lọt; không so với làm tay.

### Bài 8.7 (tùy chọn) — Song song và vòng chấm
- **Mục tiêu:** chỉ thêm khi bài 8.6 chỉ ra lý do (chậm hoặc lỗi cụ thể).
- **Làm:** sectioning (kiểm giá, kiểm chính sách chạy song song); hoặc evaluator-optimizer có trần 2 vòng và tiêu chí chấm bằng văn bản; nếu dùng LLM chấm, kiểm độ đồng thuận với người (Nubank dùng Cohen's kappa và yêu cầu ngưỡng đồng thuận người–máy tối thiểu trước khi tin; MAP nêu mọi ca dùng LLM-as-judge đều kèm duyệt người).
- **Sản phẩm:** so sánh trước/sau với số liệu.
- **Lỗi:** thêm vòng lặp vì "nghe hay"; không có tiêu chí chấm.

---

## 5) Đường không code vs đường có code; khi nào buộc phải chuyển

| | Không code `[NC]` | Code nhẹ `[PY]` |
|---|---|---|
| Cách làm | Chuỗi Project/Gem/GPT thủ công + người chuyển kết quả giữa các bước; hoặc công cụ kéo-thả (ví dụ n8n) | Script Python: các hàm bước + trạng thái + hàng đợi |
| Ưu | Bắt đầu ngay, học quy trình trước | Cổng kiểm bằng code, trần bước, trạng thái, nhật ký, ca thử tự động |
| Nhược | Tay nhiều, khó đo; dễ sai thứ tự; không chạy nền | Cần người bảo trì |

- **n8n [Nguồn, Thao tác]:** có bước Human review cho lời gọi công cụ của AI Agent (xem C7, mục 5). Chưa kiểm chứng gì về Make; Zapier chỉ qua một bài blog (xem mục 9).
- **Rủi ro công cụ kéo-thả [Đề xuất]:** quyền OAuth rộng, workflow chạy ngầm, chi phí tăng theo số lần chạy, dữ liệu khách qua bên thứ ba.
- **Buộc chuyển sang code [Đề xuất] khi:** cần cổng kiểm số tiền/ngày bằng code; cần trần bước/ngân sách cứng; >~50 phiếu/ngày làm tay chuyển kết quả trở thành nút thắt; cần chạy lại từ bước lỗi; cần bộ ca thử chạy mỗi khi đổi mô hình hay prompt; cần nhật ký kiểm toán. (Các con số là phán đoán của chúng tôi.)
- **Tự viết vs framework [Nguồn]:** MAP: 85% (17/20) tự viết với lời gọi API trực tiếp; Anthropic: bắt đầu bằng API trực tiếp, framework có thể che prompt/phản hồi và khó debug, nếu dùng phải hiểu mã bên dưới. **[Đề xuất]** SME nên bắt đầu bằng script ngắn của mình.

---

## 6) Tiêu chí lên Cấp 9 (vận hành) [Đề xuất]

Lên C9 khi **đủ**:
1. ≥1 quy trình chạy trên phiếu thật ≥4 tuần, ≥100 phiếu (hoặc đủ lượng cho thống kê hợp lý với quy mô doanh nghiệp).
2. Có bộ ≥30–50 ca thử (gồm ca ngoại lệ và ca injection) chạy được mỗi khi đổi prompt/mô hình, kết quả so được với lần trước.
3. Tỷ lệ lỗi lọt sau duyệt (khách/đối tác báo) thấp hơn hoặc bằng làm tay — đo được và có người ký nhận ngưỡng.
4. Hàng đợi duyệt đạt SLA ≥90% thời gian; có người thay thế.
5. Chi phí/phiếu và thời gian/phiếu thấp hơn làm tay, có số.
6. 0 hành động ghi chạy không qua duyệt; mọi phiếu truy vết được bước-nhật ký.
7. Có kế hoạch khi nhà cung cấp mô hình đổi/ngừng (chạy lại bộ ca thử trên mô hình mới trước khi chuyển — Nubank coi nâng cấp mô hình như thay đổi prompt, phải chạy đủ bộ đánh giá).

(Ngưỡng cụ thể là đề xuất, tự điều chỉnh theo rủi ro.)

**Không lên C9 nếu:** chỉ chạy được "khi người xây còn ngồi cạnh", hoặc không có số đo.

---

## 7) Ví dụ cho SME Việt Nam (ba tình huống chi tiết)

Tất cả số liệu dưới đây là **giả định minh họa**, không phải kết quả đo. Tên sản phẩm/công ty là hư cấu.

### 7.a Soạn trả lời khách Zalo/email từ bảng giá và chính sách, nhân viên duyệt trước khi gửi

**SOP mẫu (như nhân viên đang làm):**
1. Đọc tin khách. 2. Xác định khách hỏi gì (giá / còn hàng / giao hàng / đổi trả / khiếu nại / khác). 3. Tra bảng giá hoặc tồn kho. 4. Kiểm chính sách (đổi trả 7 ngày... là ví dụ giả định). 5. Soạn trả lời theo giọng cửa hàng. 6. Gửi. 7. Ghi chú khách vào sổ.

**Quy trình agent-hóa (workflow cố định, mẫu routing + chaining):**

| # | Bước | Ai làm | Công cụ / cổng kiểm |
|---|---|---|---|
| 1 | Nhận tin, tạo mã phiếu | Code | Lưu nguyên văn tin |
| 2 | Phân loại (hỏi giá / còn hàng / giao / đổi trả / khiếu nại / khác) | LLM (routing) | Đầu ra JSON `{loai, do_tin_cay}` |
| 3 | Nếu `khieu_nai` hoặc `khac` hoặc tin cậy thấp → hàng đợi người, kèm gói chuyển giao | Code | — |
| 4 | Lấy dữ liệu: dòng bảng giá, tồn kho, điều khoản chính sách liên quan | Code (công cụ C7 hạng A) | Thiếu dữ liệu → chuyển người |
| 5 | Soạn trả lời từ macro + dữ liệu | LLM | Chỉ được dùng số/điều khoản đã truy xuất; trích nguồn nội bộ (dòng nào) |
| 6 | **Cổng kiểm bằng code:** mọi số tiền/ngày trong nháp phải khớp dữ liệu bước 4; không có cam kết ngoài chính sách (so với danh sách cụm cấm) | Code | Lỗi → chuyển người hoặc soạn lại 1 lần |
| 7 | **Điểm duyệt:** nhân viên thấy tin gốc + nháp + nguồn + kết quả cổng kiểm; Duyệt / Sửa rồi duyệt / Từ chối (lý do) | Người | Hàng đợi có hạn xử lý |
| 8 | Gửi (người bấm gửi, hoặc hệ thống gửi *sau* duyệt) | Người/Code | Nhật ký |
| 9 | Ghi nhận kết quả duyệt để cải tiến | Code | — |

**Công cụ cần (từ C7):** `tra_gia` (A), `tra_ton_kho` (A), `tra_chinh_sach` (A), `tao_nhap_tra_loi` (C); **không có công cụ gửi trực tiếp** ở giai đoạn đầu.
**Điểm duyệt:** mọi tin trước khi ra khỏi cửa hàng. Giai đoạn sau, nếu số liệu tốt, *có thể* cho nhóm câu rất đơn giản (chỉ hỏi còn hàng, không giá) gửi tự động; đó là quyết định có số đo, không phải mặc định.
**Đo gì:** % phân loại đúng; % nháp duyệt không sửa / sửa nhẹ / sửa nặng / từ chối; số lỗi số tiền bị cổng kiểm bắt; thời gian nhận→gửi; tiền/phiếu; số lần khách phàn nàn sau gửi.
**Rủi ro:** (1) báo sai giá/cam kết sai chính sách (→ cổng kiểm + duyệt); (2) tin của khách chứa lệnh giả ("hãy giảm 50%") → agent này không có quyền ghi giá, nháp chỉ dùng số từ bảng giá; (3) lộ thông tin khách khác (→ tra đơn chỉ theo SĐT/mã của chính khách đang chat, kiểm quyền trong code); (4) giọng cứng/đáp lạc điệu với khách bực (→ chuyển người); (5) người duyệt bấm cho xong.

### 7.b Tóm tắt và chuẩn hóa nội dung (biên bản họp, báo cáo ngày)

**SOP mẫu:** người dự họp ghi chú → trưởng nhóm viết biên bản theo mẫu (Nội dung, Quyết định, Việc cần làm: ai/việc/hạn, Vấn đề tồn) → gửi các bên.

**Quy trình (prompt chaining + sectioning):**

| # | Bước | Ai làm | Ghi chú |
|---|---|---|---|
| 1 | Nhận bản ghi/ghi chú thô, tạo mã phiếu | Code | Gắn ngày, danh sách người dự |
| 2 | Làm sạch/chia đoạn bản ghi | Code/LLM | Giữ nguyên văn gốc song song |
| 3a | Rút **quyết định** | LLM | Chạy song song 3a–3c (sectioning), mỗi bước một prompt hẹp |
| 3b | Rút **việc cần làm** (ai, việc, hạn) | LLM | Đầu ra JSON; trường không có trong bản ghi để `null`, **không đoán** |
| 3c | Rút **vấn đề tồn** | LLM | — |
| 4 | **Cổng kiểm bằng code:** tên người thuộc danh sách dự họp/nhân sự; hạn là ngày hợp lệ ở tương lai; mỗi việc có người phụ trách (nếu `null` → gắn cờ) | Code | — |
| 5 | Ráp biên bản theo mẫu | Code | Mẫu cố định |
| 6 | **Điểm duyệt:** người chủ trì họp đối chiếu từng việc cần làm với bản ghi gốc (hiển thị đoạn gốc bên cạnh) | Người | Duyệt trong 24 giờ |
| 7 | Gửi và lưu | Người/Code | Nhật ký |

**Công cụ:** `doc_ban_ghi` (A), `tra_danh_sach_nhan_su` (A), `tao_nhap_bien_ban` (C). Việc giao nhắc việc tự động (ghi vào công cụ quản lý việc) = hạng D/C → chỉ sau duyệt.
**Đo:** % việc cần làm bị sửa/thêm/xóa khi duyệt; số việc bị **bỏ sót** (đối chiếu ngẫu nhiên với bản ghi); số việc **bịa** (không có trong bản ghi); thời gian viết biên bản; mức hài lòng người chủ trì.
**Rủi ro:** gán sai người/hạn (→ `null` thay vì đoán, cổng kiểm); mất ngữ cảnh trong họp dài (→ chia đoạn, kiểm bỏ sót); nội dung nhạy cảm (nhân sự, lương) đi qua dịch vụ ngoài (→ kiểm chính sách dữ liệu, loại nội dung nhạy cảm); lẫn tiếng Việt/tiếng Anh/tên riêng (→ danh sách tên chuẩn); injection thấp nhưng có (bản ghi có thể chứa câu lệnh).

### 7.c Đối chiếu và kiểm tra tài liệu theo danh sách quy tắc (hợp đồng, hóa đơn, đề nghị thanh toán)

**SOP mẫu (đề nghị thanh toán, giả định):** kế toán nhận đề nghị + hóa đơn + hợp đồng/đơn đặt hàng → kiểm: (1) hóa đơn đủ trường bắt buộc (số, ngày, MST bên bán...), (2) MST/tên bên bán khớp hợp đồng, (3) số tiền hóa đơn khớp đề nghị, (4) khớp đơn giá/số lượng trong đơn đặt hàng, (5) nằm trong hạn mức người đề nghị, (6) không trùng hóa đơn đã thanh toán → duyệt/trả lại.

**Quy trình (chaining + sectioning; nghiêng về code):**

| # | Bước | Ai làm | Ghi chú |
|---|---|---|---|
| 1 | Nhận bộ hồ sơ, tạo mã phiếu | Code | — |
| 2 | Trích trường từ tài liệu (văn bản/PDF) thành JSON (C2) | LLM | Mỗi trường kèm *đoạn nguồn*; không chắc → `null` + cờ |
| 3 | **Kiểm quy tắc bằng code** trên các trường đã trích: khớp số tiền, MST, trùng hóa đơn (tra sổ), hạn mức | Code (công cụ đọc hạng A/B) | Đây là phần máy làm chắc chắn, **không để LLM tính** |
| 4 | Quy tắc cần hiểu ngữ nghĩa (điều khoản hợp đồng có cho phép? mô tả hàng khớp?) | LLM, từng quy tắc một (sectioning) | Trả `{ket_qua: dat/khong_dat/khong_ro, trich_dan}` |
| 5 | Tổng hợp **bảng kiểm**: mỗi quy tắc → đạt / không đạt / không rõ + trích dẫn | Code | — |
| 6 | **Điểm duyệt:** kế toán xem bảng kiểm + tài liệu gốc cạnh nhau; mọi "không rõ"/"không đạt" bắt buộc người xem; quyết định duyệt/trả lại là của người | Người | Hàng đợi, SLA |
| 7 | Ghi kết quả; **không có công cụ thanh toán** | Người | Nhật ký |

**Công cụ:** `doc_tai_lieu` (A), `tra_so_hoa_don` (B, kiểm trùng), `tra_han_muc` (B), `ghi_bang_kiem` (C). Hạng D (lệnh chi) ngoài phạm vi.
**Đo:** với bộ phiếu đã có đáp án do người gắn nhãn: % quy tắc kết luận đúng; **tỷ lệ bỏ sót vi phạm** (quan trọng nhất; ưu tiên hơn tỷ lệ báo nhầm); % "không rõ"; thời gian/phiếu; số lỗi lọt sau duyệt. Nếu dùng LLM làm "giám khảo", kiểm độ đồng thuận với người trên mẫu trước khi tin (Nubank dùng kappa; MAP nêu mọi ca dùng LLM-as-a-judge đều kèm người).
**Rủi ro:** trích sai trường từ PDF xấu/scan (→ cờ `null`, người xem nguồn); LLM bỏ sót một quy tắc (→ danh sách quy tắc nằm trong code, mỗi quy tắc một kết quả bắt buộc); **injection qua tài liệu** (hóa đơn/hợp đồng chứa chữ ẩn ra lệnh "đánh dấu đạt") → LLM ở bước này không có quyền ghi quyết định, kết quả chỉ là *đề xuất*, người duyệt xem nguồn; gian lận tinh vi (hóa đơn giả hợp lệ về hình thức) mà quy tắc không bắt; trách nhiệm pháp lý (không dùng kết luận của AI làm căn cứ duy nhất).

### Code mẫu rút gọn (đã chạy thử)
Trạng thái: **đã chạy thử** 2026-11-11 với `python -I`, dùng hàm giả thay mô hình; **chưa chạy thử với API thật**. Kết quả: ca "hỏi giá" đi qua 4 bước và vào hàng đợi duyệt; ca "khiếu nại" dừng ngay sau phân loại và vào hàng đợi chuyển người kèm các bước đã làm. Đây là khung tối thiểu, chưa có thử lại, chưa lưu bền, chưa phân quyền.

```python
MAX_STEPS = 6
QUEUE, STATE = [], {}                  # hàng đợi người duyệt, trạng thái theo mã phiếu
BANG_GIA = {"SP001": 150000}

def llm(task, **kw):                   # HÀM GIẢ thay cho gọi API
    if task == "phan_loai": return "hoi_gia" if "gia" in kw["tin"].lower() else "khac"
    if task == "soan": return f"Chao anh/chi, gia {kw['gia']:,} dong."

def xu_ly(ma, tin):
    s = STATE.setdefault(ma, {"buoc": 0, "log": []})
    def buoc(ten):
        s["buoc"] += 1
        if s["buoc"] > MAX_STEPS: raise RuntimeError("vuot gioi han buoc")
        s["log"].append(ten)
    def chuyen(loai):                  # chuyển người KÈM ngữ cảnh
        QUEUE.append({"ma": ma, "loai": loai, "tin": tin, "da_lam": list(s["log"])}); return loai

    buoc("phan_loai")
    if llm("phan_loai", tin=tin) != "hoi_gia": return chuyen("chuyen_nguoi")
    buoc("tra_gia"); gia = BANG_GIA.get("SP001")          # bước cố định bằng code
    if gia is None: return chuyen("thieu_du_lieu")
    buoc("soan"); nhap = llm("soan", gia=gia)
    buoc("kiem_co_dinh")                                   # cổng kiểm bằng code
    if f"{gia:,}" not in nhap: return chuyen("kiem_loi")
    QUEUE.append({"ma": ma, "loai": "duyet_truoc_khi_gui", "nhap": nhap, "tin": tin, "da_lam": s["log"]})
    return "cho_duyet"                                      # KHÔNG tự gửi
```

---

## 8) Tài liệu tham khảo

Ngày truy cập tất cả: 2026-11-11.

| # | Tiêu đề | URL | Loại | Mức tin cậy |
|---|---|---|---|---|
| 1 | Building effective agents (Anthropic) | https://www.anthropic.com/engineering/building-effective-agents | Blog kỹ thuật chính thức | Cao (qua tóm tắt WebFetch; định nghĩa 2 loại và 5 mẫu đã đối chiếu) |
| 2 | Measuring Agents in Production (MAP), arXiv 2512.04123v4 (ICML 2026) | https://arxiv.org/abs/2512.04123 | Bài báo | Cao; đã đọc lại bằng công cụ trích PDF: các số 68%, 47%, 16/20, 17/20, 74%, 75%, 66% |
| 3 | Building Customer Support AI Agents at 100M-User Scale (Nubank), arXiv 2606.08867 (KDD'26) | https://arxiv.org/abs/2606.08867 | Bài báo công nghiệp | Trung bình–cao; một công ty, số tNPS/SSR tự báo cáo (+37 điểm % tNPS, +29 điểm % self-service ở ca giao thẻ) |
| 4 | Tool use with Claude / Handle tool calls / Define tools | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Tài liệu nhà cung cấp | Cao; hay đổi |
| 5 | Function calling (OpenAI) | https://developers.openai.com/api/docs/guides/function-calling | Tài liệu nhà cung cấp | Cao; hay đổi |
| 6 | OWASP Top 10 for LLM Applications 2025 (LLM01, LLM06) | https://genai.owasp.org/llm-top-10/ | Tiêu chuẩn cộng đồng | Cao |
| 7 | Human-in-the-loop for AI tool calls (n8n) | https://docs.n8n.io/advanced-ai/human-in-the-loop-tools | Tài liệu nhà cung cấp | Cao; hay đổi |
| 8 | AI security risks (Zapier blog) | https://zapier.com/blog/ai-security-risks | Blog nhà cung cấp | Trung bình |
| 9 | Cấp 7 của series này | cap-07-cong-cu-tool.md | Tài liệu nội bộ | — |

---

## 9) Chưa kiểm chứng / cần kiểm tra lại

- **MAP "15/20 ca chạy bất đồng bộ":** đã được xác minh khi rà soát 2026-11-11 (toàn văn MAP mục 4.4). Mục này giữ lại chỉ để ghi nhận lịch sử kiểm tra.
- **BMO (arXiv 2608.01772)** và **SAP (arXiv 2608.00122):** các mô tả ở mục 3.3 và 3.6 lấy từ hồ sơ dự án, **chưa đọc lại**. Bài 2609.11999, 2610.14818, 2610.14800: chưa dùng.
- **Nubank:** đã đọc lại mục kiến trúc/thiết kế công cụ/ca giao thẻ/kết quả; "phát hiện khách bực, chuyển người sớm" chỉ thấy ở danh sách biến thể (mục 6.3), chưa đọc phương pháp chi tiết. Không có số liệu chi phí/độ trễ trong phần đã đọc.
- Các **ví dụ SOP, số liệu, ngưỡng** (SLA 24 giờ, 95%, ≥30–50 ca, ≥100 phiếu, 4 tuần, ~50 phiếu/ngày, p=0,95 và n=6) là **đề xuất/giả định minh họa của chúng tôi**, chưa có nguồn.
- Công thức pⁿ giả định các bước độc lập; thực tế lỗi có thể tương quan.
- **Claude/ChatGPT/Gemini desktop** (Project, Gem, GPT tùy chỉnh, connector): chưa đọc tài liệu chính thức → các bài [NC] mô tả nguyên tắc, **không** hướng dẫn thao tác cụ thể; cần kiểm tra tên tính năng, giới hạn gói, chính sách dữ liệu tại thời điểm làm.
- **Make:** chưa kiểm chứng. **Zapier:** chỉ một blog. **n8n:** đã đọc trang docs về HITL qua WebFetch tóm tắt; các kênh liệt kê có thể đổi.
- Chưa chạy thử với API thật; chưa thử trên dữ liệu SME thật; chưa đo chất lượng LLM ở bất kỳ tình huống nào ở mục 7.
- Chưa có nguồn đo lường chi phí/độ trễ riêng cho mẫu orchestrator-workers hoặc evaluator-optimizer trong bối cảnh SME.
- Pháp lý (hóa đơn điện tử, lưu trữ chứng từ, bảo vệ dữ liệu cá nhân ở Việt Nam): **chưa tra cứu**; cần chuyên gia kiểm trước khi đưa tình huống 7.c vào vận hành.
