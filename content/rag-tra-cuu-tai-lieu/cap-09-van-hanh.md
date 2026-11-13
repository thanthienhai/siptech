# Cấp 9 — Vận hành (Operations) cho SME

Trạng thái: bản nháp nghiên cứu, soạn ngày 2026-11-11. Quy ước: **[Nguồn]** = kết quả có trong tài liệu đã đọc; **[Đề xuất]** = ý kiến của nhóm biên soạn, chưa được nguồn chứng minh; **[Tự chạy]** = mã đã chạy thử trong phiên soạn.

Cấp này dựa vào Cấp 6: không có bộ ca đáp án thì vận hành chỉ là "ghi log rồi hy vọng".

---

## 1. Mục tiêu và người đọc

**Người đọc:** chủ SME, người được giao "phụ trách AI", và nhân viên IT kiêm nhiệm (nếu có), ở công ty đã có ít nhất một hệ thống AI được dùng hằng ngày (Project/Gem/GPT tùy chỉnh hoặc bot gọi API) và đã có bộ ca đánh giá từ Cấp 6.

**Sau cấp này có trong tay:**
1. Một mẫu nhật ký (log) mỗi lần gọi AI, đã che dữ liệu nhạy cảm.
2. Một quy ước đặt tên/phiên bản cho prompt và skill, kèm nhật ký thay đổi.
3. Một quy trình phát hành: sửa → chạy lại bộ ca → so sánh → chỉ phát hành khi không xấu đi → có đường rút lại.
4. Một "lịch kiểm tra trôi dạt": khi mô hình, tài liệu, quy định đổi.
5. Giám sát chi phí/hạn mức, sổ ghi sự cố, bảng phân vai ai chịu trách nhiệm.
6. Quy tắc dùng AI cho cả nhóm (một trang) và tiêu chí đo được để biết khi nào nâng cấp (tự động hóa, tích hợp, thuê làm).

---

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

Sau Cấp 6 công ty đã biết hệ thống đúng bao nhiêu **tại một thời điểm**. Lỗi dẫn tới Cấp 9:

- Chất lượng tụt âm thầm: nhà cung cấp đổi/ngừng mô hình, tài liệu nội bộ đổi, ai đó sửa prompt "một chút".
- Không ai biết bản prompt nào đang chạy, ai sửa, vì sao.
- Có lỗi nhưng không tái hiện được vì không có log.
- Hóa đơn API/hạn mức bất ngờ.
- Một người nghỉ việc là cả hệ thống "mồ côi".
- Dữ liệu khách/nhân viên đi vào log hoặc vào công cụ AI không kiểm soát.

**Câu hỏi của Cấp 9:** *Làm sao hệ thống tiếp tục đúng, an toàn, trong ngân sách, khi mọi thứ xung quanh nó đổi, và ai chịu trách nhiệm?*

---

## 3. Kiến thức nền (ngắn, chính xác)

### 3.1 Bằng chứng về vận hành và đánh giá lặp lại

- **[Nguồn, đã đối chiếu với toàn văn khi rà soát 2026-11-11]** BMO ESCROW (arXiv 2608.01772): chỉ sửa skill/prompt; bản sửa chỉ được nhận khi không nhóm nào xấu đi và các ca đã sửa trước đó vẫn đúng; không có kho ca cũ thì điểm trên ca cũ tụt 0,857 → 0,7, có kho thì giữ ~0,84; mỗi thay đổi là một diff đọc được cho bộ phận tuân thủ; chi phí chấm lại là nút thắt.
- **[Nguồn do chủ dự án cung cấp]** Nubank (arXiv 2606.08867): mỗi mô hình mới coi như một thay đổi prompt, phải chạy lại bộ đánh giá; rollout 1% rồi tăng; theo dõi tNPS và tỉ lệ tự phục vụ vì chúng đánh đổi nhau; điểm offline tương quan với kết quả online.
- **[Nguồn đã đọc qua alphaXiv]** She và Lin (arXiv 2609.21267, một đội ở Meta, agent phân tích dữ liệu phục vụ hàng chục nghìn người dùng hàng tháng): mỗi lần chạy trọn bộ 519 câu mất ~3 giờ; họ so các cách chạy *một phần* bộ ca. Tập con cố định phân tầng theo độ khó (difficulty-stratified fixed subset) được triển khai vì đơn giản vận hành. Ví dụ: chạy 200 trong 519 câu (38,5%) cho sai số tuyệt đối trung bình của tỉ lệ đạt chừng 1,4–1,5 điểm phần trăm với tập con cố định (bảng tác giả), và adaptive testing tốt nhất đạt 1,03 điểm phần trăm. Khuyến nghị của tác giả: **hiệu chuẩn lại sau khi có thay đổi đáng kể về mô hình, prompt, công cụ hay hệ thống thực thi, hoặc khi kết quả theo từng câu lệch kéo dài; và định kỳ chạy trọn bộ để so với ước lượng của tập con, đo sai số do chạy một phần.** Giới hạn do chính tác giả nêu: dữ liệu từ một tổ chức; không đo trực tiếp việc bắt được hay bỏ sót hồi quy ở ngưỡng quyết định. *Áp dụng cho SME: khi bộ ca nhỏ (≤ 50) thì chạy trọn bộ mỗi lần, không cần tập con.*
- **[Nguồn đã đọc qua alphaXiv]** Phan và cs. (arXiv 2610.03315, Huawei, LiteTrajEval): chấm "quỹ đạo" (các bước gọi công cụ của agent) bằng **một** lần gọi judge theo rubric, sau khi chuẩn hóa log về lược đồ tối thiểu (mỗi bước có `step_id`, `type`, `status`, `input`, `output`), đánh dấu bước cảnh báo/lỗi bằng quy tắc xác định, rồi cắt gọn theo ngân sách ký tự cố định (50.000 ký tự). Kết quả trên bộ công khai nhỏ (44 và 29 mẫu thất bại): khớp vị trí lỗi với người cao hơn baseline AgentRx khoảng 20–35 điểm phần trăm (Magentic-One) và đến 23 điểm (τ-retail); chi phí đánh giá toàn bộ mẫu giảm ~6 lần cùng một judge (2,4628 USD → 0,4155 USD theo giá API công bố tháng 6/2026), thời gian giảm hơn 8 lần. Tác giả nói rõ: phương pháp **không thay thế** chỉ số thành công riêng cho từng tác vụ, kiểm tra ràng buộc, hay người duyệt; và việc hiệu chuẩn judge với người ở sản xuất "còn đang làm". Phân tích chỉ dùng log trạng thái cho thấy chỉ bắt được 56,8% và 31,0% ca thất bại, tức *quy tắc đơn giản trên log không đủ*. *Áp dụng cho SME:* thiết kế log có `step`, `status` ngay từ đầu để sau này chấm quỹ đạo được; chưa cần judge quỹ đạo ở quy mô SME nhỏ.
- **[Nguồn đã đọc, trang chính thức]** Anthropic, "Model deprecations": xem mục 3.2.
- **[Nguồn đã đọc qua công cụ tóm tắt]** Anthropic, "Demystifying evals for AI agents": eval hồi quy (regression) nên gần 100%, bắt lùi bước; eval khả năng (capability) bắt đầu ở tỉ lệ thấp; chỉ số pass^k (xác suất cả k lần thử đều đạt) dùng khi cần độ ổn định; ví dụ trong bài: 75% mỗi lần → khoảng 42% cho pass^3.
- **[Nguồn đã đọc qua công cụ tóm tắt]** Hamel Husain: ghi log vết (trace) để xem được toàn bộ tương tác; công cụ cần có tìm, lọc, đọc; "Keep it simple. Don't buy fancy LLM tools. Use what you have first."

### 3.2 Trôi dạt (drift): mô hình và tham số thay đổi, có ngày cụ thể

**Nguyên lý bền:** nhà cung cấp mô hình *sẽ* ngừng mô hình; nên coi "đổi mô hình" là sự kiện định kỳ, không phải bất thường.

**[Nguồn: trang "Model deprecations" của Anthropic, đã đọc 2026-11-11 — thao tác/dữ kiện hay đổi]:**
- Vòng đời: *Active, Legacy, Deprecated, Retired*; mô hình đã *Retired* thì yêu cầu gọi tới sẽ thất bại.
- Anthropic thông báo cho khách có triển khai đang chạy **ít nhất 60 ngày** trước khi ngừng mô hình đã phát hành công khai; thông báo qua email và tài liệu.
- Trang khuyên kiểm thử ứng dụng với mô hình mới "well before" ngày ngừng, và liệt kê mô hình thay thế đề xuất.
- Có cách kiểm kê: trang Usage trong Claude Console → Export → CSV, chia theo API key và mô hình, để biết còn dùng mô hình sắp ngừng không.
- Ví dụ trong bảng ngày truy cập: `claude-sonnet-4-5-20250929` ở trạng thái *Deprecated* (ngày thông báo 2026-09-30), **ngày ngừng 2026-11-30**, thay thế đề xuất `claude-sonnet-5-5`. (Chỉ minh họa; bảng này sẽ đổi, hãy mở trang gốc.)
- Nền tảng đối tác (Amazon Bedrock, Google Cloud do Google quản lý) có lịch ngừng riêng, có thể khác.
- **Trôi dạt tham số API:** trang ghi rằng `temperature`, `top_p`, `top_k` bị gỡ ở phiên bản API `2026-10-21` (gửi các tham số này sẽ trả về lỗi 400); khuyên bỏ chúng và dùng prompt để định hướng hành vi. Điều này quan trọng cho SME code nhẹ: mã cũ đặt `temperature=0` có thể **hỏng ngay khi nâng phiên bản API**. (Cũng do vậy, Miller khuyên *không* chỉnh temperature để giảm nhiễu đánh giá **[Nguồn arXiv 2411.00640]**; để giảm nhiễu hãy chấm lại nhiều lần.)
- Nhà cung cấp khác (OpenAI, Google...) có chính sách riêng; **chưa tra cứu** trong đợt này.

**Các nguồn trôi dạt khác [Đề xuất]:** tài liệu nội bộ cập nhật (bảng giá, chính sách), đổi phiên bản chính sách mà tài liệu cũ vẫn còn trong chỉ mục, thay đổi định dạng file đầu vào, mô hình đổi hành vi *không đổi tên* (một số nhà cung cấp dùng bí danh "latest"; hãy ghim phiên bản có ngày/ID cụ thể khi có thể, và ghi ID đó vào log).

---

## 4. Chuỗi bài nhỏ

Mỗi bài ≈ 30–120 phút. Bài 9.1–9.4 là cốt lõi.

### Bài 9.1 — Nhật ký (log) mỗi lần gọi
- **Mục tiêu:** mỗi lần AI chạy để lại một dòng đủ để tái hiện và đo lường.
- **Trường tối thiểu [Đề xuất]:** `ts` (thời điểm), `request_id`, `prompt_id` + `version`, `model` (đúng ID/phiên bản dùng), `input` (đã che), `output` (đã che), `tools` (tên công cụ + trạng thái từng bước), `retrieved_ids` (ID tài liệu/đoạn được đưa cho AI, để tách đo truy hồi như Cấp 6), `latency_ms`, `tokens_in`, `tokens_out`, `cost_est`, `error`, `user_group` (không phải tên người), `feedback` (nếu có: tốt/xấu/sửa). Với agent nhiều bước, mỗi bước một dòng với `step_id`, `type`, `status`, `input`, `output` (lược đồ gợi ý từ arXiv 2610.03315 **[Nguồn]**).
- **Che dữ liệu nhạy cảm [Đề xuất]:** che *trước khi ghi*, không sau; mặc định không ghi nội dung nếu việc không cần (chỉ ghi ID, độ dài, băm); giới hạn ai đọc được log; quy định thời hạn lưu và xóa; **không** ghi khóa API. Mẫu che dưới đây là *ví dụ tối thiểu* (email, điện thoại VN, dãy số 9–12 chữ số) và sẽ **bỏ sót** nhiều thứ (tên người, địa chỉ); cần mở rộng và kiểm với dữ liệu thật của bạn. Quy định pháp lý (Nghị định về bảo vệ dữ liệu cá nhân của Việt Nam) **chưa tra cứu trong đợt này**; nhờ người am hiểu pháp lý xem trước khi lưu dữ liệu khách.
- **Mã mẫu (Python chuẩn). Trạng thái: ĐÃ CHẠY THỬ 2026-11-11 (`python -I`), đầu ra: số điện thoại, email được thay bằng `[PHONE]`, `[EMAIL]`:**

```python
import json, re, time
PATTERNS = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL]"),
            (re.compile(r"(?<!\d)(?:\+?84|0)\d{9,10}(?!\d)"), "[PHONE]"),
            (re.compile(r"(?<!\d)\d{9,12}(?!\d)"), "[ID]")]
def redact(s):
    for p, r in PATTERNS: s = p.sub(r, s)
    return s

def log_call(path, **kw):
    kw["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    for f in ("input", "output"):
        if f in kw: kw[f] = redact(kw[f])
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(kw, ensure_ascii=False) + "\n")

log_call("calls.jsonl", prompt_id="tra-cuu@v3", model="<model-id>",
         input="KH 0912345678 a@b.vn hoi gia", output="...", tools=[],
         latency_ms=812, tokens_in=300, tokens_out=80, error=None)
```
  Mỗi dòng là một JSON (định dạng JSON Lines), mở được bằng Excel/Sheets sau khi nhập hoặc bằng vài dòng Python.
- **Đường không code:** Project/Gem/GPT thường không cho log cấu trúc đầy đủ. Dùng một Google Sheet "Sổ dùng AI" nhân viên tự ghi: ngày, việc, công cụ + phiên bản prompt, kết quả (dùng được/sửa nhẹ/sửa nặng/bỏ), thời gian sửa, ghi chú lỗi. Đây là log thô nhưng đủ để thấy xu hướng. (Khả năng xuất lịch sử hội thoại của từng công cụ khác nhau và đổi nhanh; **chưa kiểm** trong đợt này.)
- **Công cụ quan sát có sẵn:** chuẩn OpenTelemetry cho GenAI được chuyển sang kho riêng (trang cũ ghi "moved"; thuộc tính cụ thể **chưa đọc được** trong đợt này, xem mục 9). SME nhỏ không cần dùng ngay; log JSON Lines ở trên đủ.
- **Sản phẩm:** file `calls.jsonl` (hoặc Sheet) chạy thật 1 tuần; một người đọc thử 20 dòng ngẫu nhiên mỗi tuần.
- **Lỗi thường gặp:** ghi nguyên văn dữ liệu khách; log không có phiên bản prompt/mô hình nên không so sánh được; ghi log nhưng không ai đọc (Hamel: phải *bỏ ma sát* khi xem dữ liệu **[Nguồn]**).

### Bài 9.2 — Phiên bản hóa prompt/skill
- **Mục tiêu:** biết chính xác bản nào chạy, và có quay lui được.
- **Thực hành [Đề xuất]:**
  1. Mỗi prompt/skill có **ID + phiên bản**: `tra-cuu-bao-hanh@v3`. Thay đổi *bất kỳ chữ nào* là phiên bản mới (kể cả đổi tài liệu đính kèm hoặc mô hình, vì Nubank coi đổi mô hình như đổi prompt **[Nguồn do chủ dự án cung cấp]**).
  2. Lưu prompt dưới dạng file văn bản trong một thư mục chung (đường code: Git, mỗi lần sửa là một commit có lý do; ESCROW coi mỗi thay đổi là một diff đọc được **[Nguồn do chủ dự án cung cấp]**). Đường không code: Google Doc có lịch sử phiên bản + một Sheet "Nhật ký thay đổi".
  3. **Nhật ký thay đổi (changelog)** mỗi dòng: ngày, ID@phiên bản, người sửa, **vì sao**, thay đổi gì (diff ngắn), điểm bộ ca trước/sau (ghi k/n), người duyệt.
  4. Ghi trong cấu hình: bản nào là **đang chạy (production)**, bản nào **trước đó** (để rollback).
  5. Với Project/Gem/GPT tùy chỉnh: sao chép bản "đang chạy" thành bản "thử" để sửa; không sửa trực tiếp bản mọi người đang dùng.
- **Sản phẩm:** thư mục `prompts/` (hoặc Doc) + changelog.
- **Lỗi thường gặp:** "sửa nhanh cho gấp" ngay trên bản đang chạy; không ghi lý do; để prompt rải rác trong tin nhắn cá nhân.

### Bài 9.3 — Quy trình sửa → chạy lại → so sánh → phát hành (kiểu ESCROW/Nubank thu nhỏ)
- **Mục tiêu:** không bản nào lên production nếu làm xấu đi chất lượng đã đạt.
- **Thực hành [Đề xuất, dựa nguyên tắc của ESCROW/Nubank — nguồn do chủ dự án cung cấp]:**
  1. **Mở phiếu thay đổi** (1 dòng changelog trạng thái "đề xuất"): lỗi nào, bản sửa nào.
  2. **Sửa trên bản "thử"**, chỉ dùng bộ ca *dev* để nhìn lỗi.
  3. **Chạy lại toàn bộ bộ ca** (dev + các ca lỗi cũ đã sửa + held-out). Bộ ca là "kho ca cũ": ESCROW cho thấy thiếu kho này thì ca cũ tụt điểm **[Nguồn do chủ dự án cung cấp]**.
  4. **So sánh theo từng ca và theo nhóm** (Cấp 6, bài 6.8): ca nào tốt lên, ca nào hỏng, nhóm nào xấu đi.
  5. **Điều kiện phát hành:** (a) không nhóm/loại việc nào xấu đi; (b) mọi ca lỗi đã sửa trước đó vẫn đúng; (c) ca mới hỏng phải có giải thích và được người duyệt chấp nhận; (d) held-out không tụt. Với bộ ca nhỏ, các điều kiện này là "cổng chặn lỗi hiển nhiên", không phải chứng minh thống kê (Cấp 6 mục 3.2).
  6. **Rollout nhỏ** (một nhóm/10% trong 1–2 tuần), có nút quay lại bản trước.
  7. Ghi kết quả vào changelog và đóng phiếu.
  8. **Chi phí chấm lại** là nút thắt (ESCROW **[Nguồn do chủ dự án cung cấp]**; Meta: ba giờ mỗi lượt chạy bộ 519 câu **[Nguồn arXiv 2609.21267]**). Với SME: giữ bộ ca vừa phải (20–60), chạy bằng grader mã khi được; chỉ gọi judge AI cho ca cần. Chỉ cân nhắc "tập con" khi bộ ca đủ lớn để chạy trọn bộ trở thành nút thắt.
- **Chấm lại khi nào [Đề xuất tổng hợp]:** đổi prompt; đổi mô hình hoặc phiên bản API; đổi/nhập tài liệu mới vào chỉ mục; đổi công cụ; và định kỳ (ví dụ mỗi tháng) kể cả không đổi gì, để bắt trôi dạt do nhà cung cấp. Khuyến nghị của She & Lin: hiệu chuẩn lại sau thay đổi vật chất về mô hình/prompt/công cụ/hệ thống, hoặc khi kết quả theo câu lệch kéo dài **[Nguồn]**.
- **Sản phẩm:** một "phiếu thay đổi" một trang cho mỗi lần sửa; changelog cập nhật.
- **Lỗi thường gặp:** bỏ qua held-out vì "chỉ sửa chữ nhỏ"; chỉ chạy lại đúng ca vừa lỗi; đổi mô hình mà không chạy lại vì "mô hình mới chắc tốt hơn" (Nubank: coi là thay đổi phải chạy lại).

### Bài 9.4 — Xử lý trôi dạt: tài liệu đổi và mô hình đổi/ngừng
- **Mục tiêu:** không bị bất ngờ khi nhà cung cấp ngừng mô hình hay tài liệu đổi.
- **Thực hành:**
  1. **Kiểm kê:** lập bảng "Hệ thống AI của công ty": tên, chủ sở hữu, mô hình + phiên bản/ID, nhà cung cấp, nền tảng (trực tiếp hay qua Bedrock/Google Cloud), phiên bản prompt, nơi lưu log. Với Claude API có thể xuất CSV Usage theo API key và mô hình để tìm chỗ còn dùng mô hình sắp ngừng **[Nguồn: Model deprecations, ngày 2026-11-11]**.
  2. **Lịch xem thông báo:** mỗi tháng người phụ trách mở trang chính sách ngừng mô hình của từng nhà cung cấp đang dùng, và đọc email thông báo (Anthropic cam kết ≥ 60 ngày thông báo **[Nguồn]**). Đặt nhắc lịch.
  3. **Khi có thông báo:** (a) đọc hướng dẫn di chuyển và danh sách tham số bị gỡ/đổi; (b) tạo bản "thử" trỏ tới mô hình thay thế; (c) chạy bộ ca (bài 9.3); (d) so sánh; (e) rollout; (f) hoàn tất **trước** ngày ngừng, chừa biên an toàn (ví dụ ≥ 2 tuần) **[Đề xuất]**. Ví dụ thực tế của trang: một mô hình ngừng 2026-11-30 (xem mục 3.2): nếu thông báo ngày 2026-09-30 thì thời gian là đúng 61 ngày.
  4. **Đổi tài liệu:** mỗi lần tài liệu nguồn đổi (bảng giá, chính sách): ghi ngày hiệu lực; **gỡ bản cũ khỏi chỉ mục** hoặc đánh dấu hết hạn; cập nhật đáp án các ca bị ảnh hưởng; chạy lại các ca thuộc tài liệu đó.
  5. **Giám sát nhẹ giữa các lần đổi:** hằng tuần xem tỉ lệ lỗi, tỉ lệ "sửa nặng" từ sổ log/Sheet; hằng tháng chạy lại bộ ca với chính bản đang chạy (không đổi gì) để xem điểm có trôi không.
- **Đường code:** một script chạy bộ ca theo lịch (cron/Task Scheduler), ghi k/n vào một file theo ngày, gửi cảnh báo khi tụt quá ngưỡng đã đặt trước.
- **Sản phẩm:** bảng kiểm kê hệ thống AI; lịch trôi dạt; biểu đồ/bảng điểm theo ngày.
- **Lỗi thường gặp:** mã cứng ID mô hình rải khắp nơi; dùng bí danh "latest" rồi bị đổi hành vi; bỏ qua email thông báo (gửi vào hộp thư của người đã nghỉ); thấy "mô hình mới chạy được" là xong.

### Bài 9.5 — Giám sát chi phí và hạn mức
- **Mục tiêu:** biết tiền và hạn mức đi đâu, báo động trước khi vượt.
- **Thực hành:**
  1. Ghi `tokens_in`, `tokens_out`, `cost_est` mỗi lần gọi (bài 9.1). Giá theo bảng công bố của nhà cung cấp tại ngày (giá thay đổi; **không** ghi giá cố định trong tài liệu này).
  2. Tổng hợp theo tuần: theo hệ thống, theo nhóm dùng, theo loại việc. Tính **chi phí trên mỗi việc hoàn thành** và so với thời gian tiết kiệm (Cấp 6, bài 6.7).
  3. Đặt **ngân sách tháng** cho từng hệ thống; cảnh báo ở mốc ví dụ 50%/80%/100% **[Đề xuất]**. Công cụ cảnh báo của từng nền tảng khác nhau và đổi nhanh; **chưa kiểm** trong đợt này; nếu nền tảng không có, tự kiểm tra bảng tổng hợp hằng tuần.
  4. Tách API key theo hệ thống/nhóm để thấy từng phần (dựa trên việc Usage có chia theo API key **[Nguồn: Model deprecations]**); đặt giới hạn chi tiêu nếu nền tảng hỗ trợ (**chưa kiểm**).
  5. Giảm chi phí: ngắt vòng lặp (giới hạn số bước/lần thử), cắt ngữ cảnh thừa, dùng mô hình nhỏ cho việc dễ (phải chạy lại bộ ca khi đổi), giảm số lần chấm judge. Dữ liệu từ arXiv 2610.03315: chuẩn hóa/cắt gọn log và dùng một lần gọi judge giảm chi phí chấm khoảng 6 lần trong bộ thử của họ **[Nguồn]**; không suy ra tương tự cho việc của bạn.
  6. Với dùng gói thuê bao (Claude/ChatGPT/Gemini desktop): theo dõi số người dùng thật, ai bị giới hạn lượt, ai không dùng nữa (cắt gói thừa) **[Đề xuất]**.
- **Sản phẩm:** bảng chi phí tuần/tháng + ngân sách + cảnh báo.
- **Lỗi thường gặp:** vòng lặp agent không giới hạn; một key dùng chung cho mọi thứ; so chi phí mà quên chi phí nhân sự bảo trì.

### Bài 9.6 — Quản lý lỗi và nhật ký sự cố
- **Mục tiêu:** lỗi được xếp loại, sửa tận gốc, và để lại bài học.
- **Thực hành [Đề xuất]:**
  1. **Phân loại mức độ** (ví dụ): Sev1 = lộ dữ liệu/ gửi sai cho khách/ số tiền sai đã ra ngoài; Sev2 = trả lời sai ảnh hưởng quyết định nhưng chưa ra ngoài; Sev3 = chất lượng kém khó chịu. Sev1: **dừng hệ thống/rút bản mới ngay**, báo người chịu trách nhiệm.
  2. **Sổ sự cố** (Sheet): ngày, mức độ, mô tả, `request_id`, phát hiện thế nào, ảnh hưởng, nguyên nhân gốc (tài liệu? truy hồi? prompt? mô hình? người dùng sai cách?), cách xử lý tạm, sửa dứt điểm (link phiếu thay đổi), **ca mới đã thêm vào bộ ca chưa** (bắt buộc: mọi sự cố thật trở thành 1 ca hồi quy — như "lỗi thật → ca eval" của Anthropic **[Nguồn]**), người phụ trách, ngày đóng.
  3. **Lỗi kỹ thuật gọi API:** thử lại có giới hạn (số lần, thời gian chờ), ghi `error` vào log; không thử lại vô hạn (đốt tiền). Mã lỗi cụ thể theo nhà cung cấp, **chưa tra cứu** trong đợt này.
  4. **Họp rà ngắn** mỗi tháng 30 phút: xem sổ sự cố, xu hướng, 20 dòng log ngẫu nhiên.
- **Sản phẩm:** sổ sự cố; quy tắc mức độ; luồng "sự cố → ca hồi quy".
- **Lỗi thường gặp:** sửa prompt vá đúng lỗi mà không thêm ca (lỗi quay lại); đổ lỗi "AI ngu" thay vì tìm nguyên nhân gốc; giấu sự cố.

### Bài 9.7 — Ai chịu trách nhiệm (phân vai)
- **Mục tiêu:** mỗi hệ thống có chủ rõ ràng và người dự phòng.
- **Thực hành [Đề xuất]:** bảng RACI một trang, tối thiểu các vai:
  - **Chủ hệ thống (owner)**: một người tên cụ thể cho mỗi hệ thống AI; chịu trách nhiệm chất lượng, phiên bản, ngân sách.
  - **Người duyệt phát hành**: khác người sửa (nguyên tắc "hai người" cho thay đổi lên production; ESCROW dành diff đọc được cho bộ phận tuân thủ **[Nguồn do chủ dự án cung cấp]**).
  - **Người phụ trách dữ liệu/bảo mật**: quyết định dữ liệu nào được đưa vào công cụ AI nào, thời hạn lưu log.
  - **Người dự phòng** cho từng vai (tránh "một người nghỉ là mồ côi").
  - **Lãnh đạo**: quyết định ngân sách và rủi ro chấp nhận được.
  - Ghi rõ **người ra quyết định cuối** khi AI sai ảnh hưởng khách (con người chịu trách nhiệm, không phải "AI nói vậy").
- **Sản phẩm:** bảng RACI + danh bạ khẩn.
- **Lỗi thường gặp:** "ai cũng là chủ" nên không ai là chủ; chủ là người ngoài công ty mà không có quyền truy cập đầy đủ.

### Bài 9.8 — Đào tạo và quy tắc dùng cho cả nhóm
- **Mục tiêu:** cả nhóm dùng AI nhất quán, giảm dùng "vô tội vạ".
- **Thực hành [Đề xuất]:**
  1. **Quy tắc dùng một trang:** (a) dữ liệu *không bao giờ* dán vào công cụ AI công cộng (ví dụ CCCD, số tài khoản, hợp đồng khách, lương); (b) chỉ dùng hệ thống đã được duyệt cho việc đó; (c) *mọi* đầu ra gửi ra ngoài phải có người xem; (d) cách báo lỗi/sự cố (1 chạm vào Sheet); (e) ai xin thêm công cụ mới, theo quy trình nào.
  2. **Buổi đào tạo 60–90 phút**: ví dụ hệ thống đã duyệt; 5 lỗi AI hay mắc (bịa, sai số, theo mồi, lệ thuộc thứ tự/độ dài, lỗi do dữ liệu cũ); thực hành báo lỗi.
  3. **Kiểm tra định kỳ:** mỗi quý xem lại quy tắc; chọn ngẫu nhiên vài phiên dùng để rà (có thông báo trước, tránh giám sát lén).
  4. **Danh sách "dùng AI vô tội vạ" đang tồn tại** (kiểm kê "shadow AI"): hỏi nhân viên dùng công cụ nào cho việc gì; đưa vào hệ thống đã duyệt hoặc cấm.
- **Sản phẩm:** quy tắc một trang đã ký nhận; tài liệu đào tạo; sổ ghi người đã học.
- **Lỗi thường gặp:** quy tắc dài như luật; cấm hoàn toàn nên người dùng lén dùng; đào tạo một lần rồi quên.

### Bài 9.9 — Khi nào nâng cấp: tự động hóa, tích hợp, thuê làm
- **Mục tiêu:** quyết định dựa trên số đo, không cảm hứng.
- **Dấu hiệu nên nâng cấp [Đề xuất, ngưỡng là ví dụ, tự điều chỉnh theo công ty]:**

| Dấu hiệu đo được | Nâng cấp tới |
|---|---|
| Một việc lặp > ~50–100 lần/tháng, bước thủ công chiếm đa số thời gian, chấm bộ ca đã ổn (k/n ổn định ≥ 3 tháng) | Tự động hóa (code nhẹ/quy trình Cấp 8) |
| Người dùng phải sao chép dữ liệu qua lại giữa AI và phần mềm (CRM, kế toán, kho) > vài lần/ngày, tổng thời gian đáng kể | Tích hợp (Cấp 7 công cụ/API) |
| Chi phí sửa lỗi/ thời gian soát > thời gian tiết kiệm đo được (bài 6.7), hoặc sự cố Sev1/Sev2 lặp lại | Quay lại sửa Cấp 3–6, **chưa** nâng cấp |
| Cần xử lý dữ liệu nhạy cảm hoặc quy định đòi kiểm toán, nhưng không có người đủ năng lực | Thuê chuyên gia/đơn vị ngoài (kèm bộ ca và changelog của bạn làm "đặc tả nghiệm thu") |
| Chủ hệ thống nghỉ/quá tải, bảo trì ngốn nhiều thời gian hơn lợi ích | Thuê/hoặc đơn giản hóa |
| Nhu cầu vượt hạn mức hoặc độ trễ của công cụ desktop, cần SLA | Chuyển sang API/hạ tầng riêng |

- **Cách đo:** dùng số từ log (số lượt, độ trễ, chi phí) và sổ thời gian (Cấp 6, bài 6.7), tính **hoàn vốn** = chi phí dựng + chi phí vận hành/tháng so với thời gian tiết kiệm × giá trị giờ công; đòi bộ ca là tiêu chí nghiệm thu khi thuê làm.
- **Sản phẩm:** một "hồ sơ đề xuất nâng cấp" 1 trang: số đo hiện tại, ngưỡng, ước tính hoàn vốn, rủi ro.
- **Lỗi thường gặp:** nâng cấp để "theo kịp xu hướng"; tự động hóa một quy trình chưa có đáp án đúng để đo; thuê làm mà không có bộ ca nghiệm thu.

---

## 5. Đường không code vs đường có code; khi nào buộc phải chuyển

| Việc | Không code | Có code (Python nhẹ) |
|---|---|---|
| Log mỗi lần gọi | Sổ Sheet nhân viên tự ghi; ghi nhận thủ công | JSON Lines tự động (bài 9.1) |
| Phiên bản prompt | Doc có lịch sử + Sheet changelog | Git, diff đọc được |
| Chạy lại bộ ca | Người chạy tay theo danh sách | Script chạy theo lịch, lưu điểm theo ngày |
| Giám sát chi phí | Xem trang sử dụng/hóa đơn tay mỗi tuần | Tổng hợp từ log, cảnh báo |
| Kiểm kê mô hình | Bảng kiểm kê tay + nhắc lịch | Xuất CSV usage, script đối chiếu |

**Buộc phải chuyển sang code khi [Đề xuất]:** (1) hệ thống gọi API (không còn là Project/Gem/GPT), vì khi đó log phải tự động; (2) có công cụ/nhiều bước (Cấp 7–8) cần log từng bước; (3) bộ ca > ~50 hoặc chạy lại thủ công bị bỏ qua; (4) cần rollback nhanh, tách môi trường thử/chạy; (5) cần cảnh báo chi phí theo thời gian thực.

---

## 6. Tiêu chí lên cấp tiếp theo (đo được)

Cấp 9 là cấp cuối của khung này; tiêu chí "xong cấp 9" **[Đề xuất]**:
1. Mỗi hệ thống AI trong công ty có trong bảng kiểm kê, có chủ + người dự phòng.
2. Có log (Sheet hoặc JSONL) ≥ 4 tuần liên tục; đã đọc rà ≥ 20 dòng ngẫu nhiên mỗi tuần.
3. Có changelog; mọi thay đổi trong 3 tháng gần nhất đều có k/n trước–sau và người duyệt.
4. Đã từng chạy lại bộ ca ít nhất một lần do sự kiện bên ngoài (đổi mô hình/tài liệu) hoặc theo lịch tháng.
5. Có sổ sự cố; mỗi sự cố Sev1/Sev2 đã thành ca hồi quy.
6. Có ngân sách + cảnh báo chi phí; không vượt ngân sách bất ngờ 3 tháng liền.
7. Quy tắc dùng AI một trang đã được cả nhóm học và ký nhận.
Chỉ khi đủ mới xét nâng cấp tự động hóa/tích hợp/thuê làm theo bảng bài 9.9.

---

## 7. Ví dụ cho SME Việt Nam (minh họa, **không** phải số liệu thật)

**Công ty du lịch ~20 người, bot gọi API trả lời lịch tour và giá cho nhân viên tư vấn:**
- Log JSONL: mỗi lượt có `prompt_id=tour-gia@v5`, `model=<id>`, `retrieved_ids`, `latency_ms`, `cost_est`, `feedback` (nhân viên bấm tốt/xấu); số điện thoại khách bị che trước khi ghi.
- Tháng 10: bảng giá tour đổi → người phụ trách đánh dấu hết hạn bản cũ, cập nhật 6 ca, chạy lại 30 ca: 26/30 → 28/30; ca hỏng 0.
- Nhận email thông báo mô hình đang dùng sắp ngừng (ví dụ 60 ngày trước hạn): tạo bản thử trỏ mô hình thay thế; chạy bộ ca; thấy 2 ca nhóm "giá có điều kiện" xấu đi → sửa prompt (v6), chạy lại, phát hành cho 3 nhân viên trong 2 tuần rồi cho cả nhóm; ghi vào changelog.
- Sự cố Sev2: bot báo sai giá khuyến mãi hết hạn. Nguyên nhân gốc: tài liệu cũ còn trong chỉ mục. Xử lý: gỡ tài liệu; thêm 2 ca hồi quy; thêm bước "ngày hiệu lực" vào quy trình cập nhật tài liệu.
- Chi phí: API ~theo bảng tổng hợp tuần; một nhân viên phụ trách (có người dự phòng); họp rà 30 phút mỗi tháng.

**Văn phòng luật/kế toán 8 người, chỉ dùng gói desktop:** không log tự động; "Sổ dùng AI" Sheet (ngày, việc, công cụ+phiên bản prompt, kết quả, thời gian sửa); quy tắc cấm dán hồ sơ khách; kiểm kê ba người đang dùng ba công cụ khác nhau và thống nhất một; bộ 20 ca chạy lại tay mỗi quý và khi đổi công cụ.

---

## 8. Tài liệu tham khảo

Ngày truy cập tất cả: 2026-11-11. "Mức tin cậy" là nhận định của người soạn.

| # | Tiêu đề | URL | Loại | Mức tin cậy |
|---|---|---|---|---|
| 1 | Anthropic, "Model deprecations" (Claude Docs) | https://platform.claude.com/docs/en/about-claude/model-deprecations (URL cũ docs.anthropic.com chuyển hướng 301 sang đây) | Tài liệu chính thức của nhà cung cấp; **đã đọc** | Cao; **thao tác/ngày thay đổi nhanh**, luôn mở bản gốc |
| 2 | She, Lin, "Efficient Benchmarking in Production: A Study of an Evolving LLM Agent" (arXiv 2609.21267) | https://arxiv.org/abs/2609.21267 | Preprint; **đã đọc nội dung chính qua alphaXiv** | Trung bình (một tổ chức; giới hạn do tác giả nêu) |
| 3 | Phan và cs., "Lightweight, Rubric-Guided Trajectory Evaluation for Production AI Agents" (arXiv 2610.03315) | https://arxiv.org/abs/2610.03315 | Preprint; **đã đọc nội dung chính qua alphaXiv** | Trung bình (mẫu nhỏ, judge chưa hiệu chuẩn ở sản xuất theo tác giả) |
| 4 | Miller, "Adding Error Bars to Evals" (arXiv 2411.00640) | https://arxiv.org/abs/2411.00640 | Preprint (Anthropic); **đã đọc** | Cao cho thống kê; dùng ở đây để giải thích vì sao chấm lại K lần và không chỉnh temperature |
| 5 | Anthropic, "Demystifying evals for AI agents" | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Blog kỹ thuật chính thức; **đọc qua công cụ tóm tắt trang** | Trung bình–cao |
| 6 | Hamel Husain, "Your AI Product Needs Evals" | https://hamel.dev/blog/posts/evals/ | Blog cá nhân thực hành; **đọc qua công cụ tóm tắt trang** | Trung bình |
| 7 | OpenTelemetry, Semantic conventions cho GenAI (trang cũ ghi đã chuyển) | https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ ; kho mới: https://github.com/open-telemetry/semantic-conventions-genai | Tài liệu chuẩn mở; **chỉ đọc được thông báo chuyển kho, chưa đọc nội dung thuộc tính** | Chưa đánh giá (chưa đọc nội dung) |
| 8 | BMO ESCROW arXiv 2608.01772; Nubank arXiv 2606.08867 | https://arxiv.org/abs/2608.01772 ; https://arxiv.org/abs/2606.08867 | Preprint; **chủ dự án cung cấp số liệu và cho biết đã đọc kỹ; người soạn không đọc lại** | Lấy nguyên từ chủ dự án; cần kiểm lại trước khi xuất bản |

---

## 9. Chưa kiểm chứng / cần kiểm tra lại

1. Số liệu ESCROW và Nubank: chưa đọc lại trong phiên này.
2. Chính sách ngừng mô hình của OpenAI, Google và các nền tảng khác (Bedrock, Google Cloud do Google quản lý): chưa tra cứu; chỉ đọc trang của Anthropic. Bảng ngày ngừng sẽ đổi; ví dụ `claude-sonnet-4-5-20250929` chỉ là minh họa theo trang đã đọc ngày 2026-11-11.
3. Lỗi 400 khi gửi `temperature/top_p/top_k` ở API version `2026-10-21`: lấy từ trang Anthropic; chưa tự thử gọi API.
4. Tính năng cảnh báo ngân sách, giới hạn chi tiêu theo key, xuất lịch sử hội thoại ở từng công cụ (Claude, ChatGPT, Gemini, Project/Gem/GPT): chưa kiểm; thao tác đổi nhanh.
5. Thuộc tính OpenTelemetry GenAI: chưa đọc được; chưa nên đưa vào hướng dẫn cho đến khi đọc kho mới.
6. Yêu cầu pháp lý Việt Nam về dữ liệu cá nhân khi ghi log và đưa dữ liệu vào công cụ AI nước ngoài: chưa tra cứu; cần người am hiểu.
7. Mẫu che dữ liệu bằng biểu thức chính quy chỉ là ví dụ tối thiểu, không bắt tên, địa chỉ; chưa kiểm trên dữ liệu thật tiếng Việt.
8. Mọi ngưỡng trong bài 9.9 và mục 6 (số lượt/tháng, mốc ngân sách, 2 tuần dự phòng, 3 tháng ổn định) là đề xuất của người soạn, chưa có nguồn thực nghiệm.
9. Con số "1,4–1,5 điểm phần trăm" cho tập con cố định 200/519 lấy từ các bảng của arXiv 2609.21267 (1,40–1,49 tùy đối tượng chạy), không phải con số tóm tắt trong phần tóm lược của tác giả; nên đối chiếu bản gốc trước khi trích.
10. Hiệu quả thực tế của việc áp quy trình kiểu ESCROW/Nubank vào bộ ca 20–50 ca của SME chưa được nghiên cứu nào ta biết kiểm chứng.
