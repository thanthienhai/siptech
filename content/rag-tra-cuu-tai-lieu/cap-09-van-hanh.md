# Cấp 9 — Vận hành (Operations) cho SME

Trạng thái: bản nháp nghiên cứu, soạn ngày 2026-11-11. Quy ước: **[Nguồn]** = kết quả có trong tài liệu đã đọc; **[Đề xuất]** = ý kiến của nhóm biên soạn, chưa được nguồn chứng minh; **[Tự chạy]** = mã đã chạy thử trong phiên soạn.

Cấp này dựa vào Cấp 6: không có bộ ca đáp án thì vận hành chỉ là "ghi log rồi hy vọng".

!!! tip "Tóm tắt nhanh"
    Một hệ thống AI chạy đúng hôm nay vẫn có thể sai dần vào tháng sau: nhà cung cấp đổi hoặc ngừng mô hình, tài liệu nội bộ đổi, hoặc ai đó lặng lẽ sửa chỉ dẫn "một chút". Bài này dạy cách **bảo dưỡng định kỳ** cho hệ thống AI: ghi nhật ký mỗi lần dùng, đánh số phiên bản cho chỉ dẫn, chỉ phát hành bản sửa khi chấm lại thấy không tệ đi, theo dõi chi phí và sự cố, và phân rõ ai chịu trách nhiệm. Sau bài, bạn có một bộ mẫu và một trang quy tắc để cả nhóm dùng AI an toàn, trong ngân sách. Đường không code luôn có; đường có code chỉ là phần thêm cho ai cần.

---

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** chủ SME (doanh nghiệp nhỏ và vừa), người được giao "phụ trách AI", và nhân viên IT kiêm nhiệm (nếu có). Công ty bạn cần đã có ít nhất một hệ thống AI được dùng hằng ngày, và đã có bộ ca đánh giá từ Cấp 6.

Hai cụm từ trên nghe kỹ thuật nhưng ý đơn giản:

- **Hệ thống AI** ở đây là Project (Claude), Gem (Gemini) hoặc GPT tùy chỉnh (ChatGPT), tức là các trợ lý đã được cài sẵn chỉ dẫn để cả nhóm dùng lại. Hoặc là một **bot gọi API**: một chương trình tự gửi câu hỏi tới AI qua một "cổng" kỹ thuật gọi là API.
- **Bộ ca đánh giá** là danh sách câu hỏi mẫu, mỗi câu kèm đáp án đúng, dùng để chấm xem AI trả lời đúng bao nhiêu. Bạn đã làm bộ này ở Cấp 6.

**Bạn cần chuẩn bị:**
- Ít nhất một hệ thống AI công ty đang dùng hằng ngày (Project, Gem, GPT tùy chỉnh hoặc bot gọi API).
- Bộ ca đánh giá đã làm ở Cấp 6.
- Một Google Sheet trống để làm sổ (nhật ký, nhật ký thay đổi, sổ sự cố đều làm được trên Sheet), và một Google Doc nếu muốn lưu chỉ dẫn có lịch sử phiên bản.

**Sau bài này bạn sẽ có:**
1. Một mẫu nhật ký (log) cho mỗi lần gọi AI, đã che dữ liệu nhạy cảm. Log là bản ghi lại "ai hỏi gì, AI đáp gì, lúc nào" để sau này còn xem lại được.
2. Một quy ước đặt tên và đánh số phiên bản cho prompt và skill (prompt là đoạn chỉ dẫn bạn đưa cho AI; skill là bộ chỉ dẫn đóng gói sẵn cho một loại việc), kèm nhật ký thay đổi.
3. Một quy trình phát hành: sửa, chạy lại bộ ca, so sánh, chỉ phát hành khi không xấu đi, và luôn có đường rút lại bản cũ.
4. Một "lịch kiểm tra trôi dạt" cho những lúc mô hình, tài liệu hoặc quy định đổi. "Trôi dạt" nghĩa là hệ thống lệch dần so với lúc bạn đo, dù bạn không chủ động đổi gì.
5. Cách giám sát chi phí và hạn mức, một sổ ghi sự cố, và một bảng phân vai cho biết ai chịu trách nhiệm.
6. Một trang quy tắc dùng AI cho cả nhóm, và các tiêu chí đo được để biết khi nào nên nâng cấp (tự động hóa, tích hợp, hoặc thuê làm).

**Thứ bạn cầm đi được sau bài:** mẫu nhật ký; thư mục chỉ dẫn kèm nhật ký thay đổi; phiếu thay đổi một trang; bảng kiểm kê hệ thống AI và lịch trôi dạt; bảng chi phí kèm ngân sách; sổ sự cố; bảng phân vai; quy tắc dùng AI một trang; và hồ sơ đề xuất nâng cấp một trang.

---

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

Sau Cấp 6, công ty đã biết hệ thống đúng bao nhiêu **tại một thời điểm**. Nhưng hệ thống không đứng yên. Những lỗi sau đây dẫn tới Cấp 9:

- Chất lượng tụt âm thầm: nhà cung cấp đổi hoặc ngừng mô hình (mô hình là "bộ não AI" đứng sau trợ lý), tài liệu nội bộ đổi, hoặc ai đó sửa prompt "một chút".
- Không ai biết bản prompt nào đang chạy, ai sửa, vì sao.
- Có lỗi nhưng không tái hiện được vì không có log.
- Hóa đơn API hoặc hạn mức bất ngờ.
- Một người nghỉ việc là cả hệ thống "mồ côi".
- Dữ liệu khách hoặc nhân viên đi vào log hoặc vào công cụ AI mà không ai kiểm soát.

**Câu hỏi của Cấp 9:** *Làm sao hệ thống tiếp tục đúng, an toàn, trong ngân sách, khi mọi thứ xung quanh nó đổi, và ai chịu trách nhiệm?*

!!! tip "Nói đơn giản"
    Hãy nghĩ đến chiếc xe máy của công ty. Mua về chạy tốt chưa đủ: phải ghi sổ bảo dưỡng, biết lần cuối thay nhớt là khi nào, có người giữ chìa khóa và người dự phòng. Hệ thống AI cũng vậy. Cấp 9 là "sổ bảo dưỡng" cho nó.

---

## 3. Kiến thức nền (ngắn, chính xác)

Phần này tóm tắt các bằng chứng làm cơ sở cho quy trình ở mục 4. Bạn không cần nhớ chi tiết từng nghiên cứu. Chỉ cần nắm ý chính: **đổi bất cứ thứ gì thì phải chấm lại**, và **mô hình sẽ bị nhà cung cấp ngừng theo lịch**.

!!! note "Lưu ý khi đọc các nguồn"
    Nhiều nguồn dưới đây là bài nghiên cứu đăng trên arXiv (kho đăng bản thảo nghiên cứu, thường chưa qua bình duyệt). Mỗi nguồn có giới hạn riêng, được nêu ngay trong mục. Các nhãn **[Nguồn]**, **[Đề xuất]** cho bạn biết đâu là điều tài liệu nói, đâu là ý kiến của nhóm soạn.

### 3.1 Bằng chứng về vận hành và đánh giá lặp lại

- **[Nguồn, đã đối chiếu với toàn văn khi rà soát 2026-11-11]** BMO ESCROW (arXiv 2608.01772): nhóm này chỉ sửa skill/prompt, không sửa thứ gì khác. Một bản sửa chỉ được nhận khi không nhóm nào xấu đi và các ca đã sửa trước đó vẫn đúng. Khi không có kho ca cũ, điểm trên các ca cũ tụt từ 0,857 xuống 0,7; khi có kho, điểm giữ ở khoảng 0,84. Mỗi thay đổi là một diff đọc được cho bộ phận tuân thủ (diff là bản so sánh cho thấy từng chỗ đã đổi). Chi phí chấm lại là nút thắt.
- **[Nguồn do chủ dự án cung cấp]** Nubank (arXiv 2606.08867): mỗi mô hình mới được coi như một thay đổi prompt, nên phải chạy lại bộ đánh giá. Họ phát hành theo kiểu rollout 1% rồi tăng dần (cho 1% người dùng dùng thử trước, êm thì tăng thêm). Họ theo dõi tNPS (chỉ số đo mức hài lòng của khách) và tỉ lệ tự phục vụ (khách tự giải quyết được, không cần người hỗ trợ), vì hai chỉ số này đánh đổi nhau. Điểm offline (chấm trên bộ ca) tương quan với kết quả online (khách dùng thật).
- **[Nguồn đã đọc qua alphaXiv]** She và Lin (arXiv 2609.21267, một đội ở Meta, agent phân tích dữ liệu phục vụ hàng chục nghìn người dùng hằng tháng; agent là AI tự làm nhiều bước để hoàn thành một việc): mỗi lần chạy trọn bộ 519 câu mất khoảng 3 giờ. Vì vậy họ so sánh các cách chạy *một phần* bộ ca. Cách được triển khai là tập con cố định phân tầng theo độ khó (difficulty-stratified fixed subset: chọn sẵn một nhóm câu hỏi cố định, lấy đủ cả câu dễ lẫn câu khó), vì đơn giản để vận hành. Ví dụ: chạy 200 trong 519 câu (38,5%) cho sai số tuyệt đối trung bình của tỉ lệ đạt chừng 1,4–1,5 điểm phần trăm với tập con cố định (bảng của tác giả), còn adaptive testing (chọn câu hỏi linh hoạt theo kết quả đã có) tốt nhất đạt 1,03 điểm phần trăm. Khuyến nghị của tác giả: **hiệu chuẩn lại sau khi có thay đổi đáng kể về mô hình, prompt, công cụ hay hệ thống thực thi, hoặc khi kết quả theo từng câu lệch kéo dài; và định kỳ chạy trọn bộ để so với ước lượng của tập con, đo sai số do chạy một phần.** Giới hạn do chính tác giả nêu: dữ liệu từ một tổ chức; không đo trực tiếp việc bắt được hay bỏ sót hồi quy (ca từng đúng nay hỏng lại) ở ngưỡng quyết định. *Áp dụng cho SME: khi bộ ca nhỏ (≤ 50) thì chạy trọn bộ mỗi lần, không cần tập con.*
- **[Nguồn đã đọc qua alphaXiv]** Phan và cs. (arXiv 2610.03315, Huawei, LiteTrajEval): họ chấm "quỹ đạo" (chuỗi các bước gọi công cụ của agent) bằng **một** lần gọi judge theo rubric. Judge là một AI đóng vai giám khảo; rubric là thang chấm viết sẵn. Trước đó, họ chuẩn hóa log về lược đồ tối thiểu (mỗi bước có `step_id`, `type`, `status`, `input`, `output`, nghĩa là mã bước, loại bước, trạng thái, đầu vào, đầu ra), đánh dấu bước cảnh báo hoặc lỗi bằng quy tắc xác định, rồi cắt gọn theo ngân sách ký tự cố định (50.000 ký tự). Kết quả trên bộ công khai nhỏ (44 và 29 mẫu thất bại): khớp vị trí lỗi với người cao hơn baseline AgentRx (cách làm dùng để so sánh) khoảng 20–35 điểm phần trăm (Magentic-One) và đến 23 điểm (τ-retail). Chi phí đánh giá toàn bộ mẫu giảm khoảng 6 lần cùng một judge (2,4628 USD xuống 0,4155 USD theo giá API công bố tháng 6/2026), thời gian giảm hơn 8 lần. Tác giả nói rõ: phương pháp **không thay thế** chỉ số thành công riêng cho từng tác vụ, kiểm tra ràng buộc, hay người duyệt; và việc hiệu chuẩn judge với người ở sản xuất "còn đang làm". Phân tích chỉ dùng log trạng thái cho thấy chỉ bắt được 56,8% và 31,0% ca thất bại, tức *quy tắc đơn giản trên log không đủ*. *Áp dụng cho SME:* thiết kế log có `step`, `status` ngay từ đầu để sau này chấm quỹ đạo được; chưa cần judge quỹ đạo ở quy mô SME nhỏ.
- **[Nguồn đã đọc, trang chính thức]** Anthropic, "Model deprecations" (trang thông báo ngừng mô hình): xem mục 3.2.
- **[Nguồn đã đọc qua công cụ tóm tắt]** Anthropic, "Demystifying evals for AI agents": eval hồi quy (regression) nên đạt gần 100%, vai trò là bắt việc lùi bước; eval khả năng (capability) bắt đầu ở tỉ lệ thấp. Có chỉ số pass^k (xác suất cả k lần thử đều đạt), dùng khi cần độ ổn định. Ví dụ trong bài: nếu mỗi lần đạt 75% thì pass^3 chỉ còn khoảng 42%. (Eval là bài kiểm tra chấm AI, như bộ ca của chúng ta.)
- **[Nguồn đã đọc qua công cụ tóm tắt]** Hamel Husain: ghi log vết (trace, tức bản ghi toàn bộ một lần tương tác) để xem được trọn vẹn cuộc tương tác; công cụ cần cho phép tìm, lọc, đọc. Lời khuyên nguyên văn: "Keep it simple. Don't buy fancy LLM tools. Use what you have first." (Giữ mọi thứ đơn giản, đừng mua công cụ LLM cầu kỳ, hãy dùng thứ bạn đang có trước; LLM là mô hình ngôn ngữ lớn, loại AI đứng sau các trợ lý chat.)

!!! tip "Nói đơn giản"
    Từ các nghiên cứu trên, có ba điều bạn mang đi. Một: mỗi lần đổi thứ gì (chỉ dẫn, mô hình, tài liệu, công cụ) là phải chấm lại bằng bộ ca. Hai: giữ lại các ca từng sai và đã sửa, để bản mới không làm chúng sai lại. Ba: ở quy mô công ty nhỏ, một cuốn sổ ghi chép đơn giản là đủ để bắt đầu, đừng vội mua công cụ đắt tiền.

### 3.2 Trôi dạt (drift): mô hình và tham số thay đổi, có ngày cụ thể

**Nguyên lý bền:** nhà cung cấp mô hình *sẽ* ngừng mô hình. Vì vậy hãy coi "đổi mô hình" là sự kiện định kỳ, không phải chuyện bất thường.

**[Nguồn: trang "Model deprecations" của Anthropic, đã đọc 2026-11-11 — thao tác/dữ kiện hay đổi]:**
- Vòng đời: *Active, Legacy, Deprecated, Retired* (tạm hiểu: đang dùng tốt, bản cũ, đã báo sắp ngừng, đã ngừng hẳn). Mô hình đã *Retired* thì yêu cầu gọi tới sẽ thất bại.
- Anthropic thông báo cho khách có triển khai đang chạy **ít nhất 60 ngày** trước khi ngừng mô hình đã phát hành công khai; thông báo qua email và tài liệu.
- Trang khuyên kiểm thử ứng dụng với mô hình mới "well before" ngày ngừng (tức từ rất sớm trước ngày ngừng), và liệt kê mô hình thay thế đề xuất.
- Có cách kiểm kê: vào trang Usage trong Claude Console, chọn Export, rồi lấy tệp CSV (bảng tính xuất ra), chia theo API key (khóa để chương trình được phép gọi AI) và theo mô hình, để biết còn dùng mô hình sắp ngừng hay không.
- Ví dụ trong bảng ngày truy cập: `claude-sonnet-4-5-20250929` ở trạng thái *Deprecated* (ngày thông báo 2026-09-30), **ngày ngừng 2026-11-30**, thay thế đề xuất `claude-sonnet-5-5`. (Chỉ minh họa; bảng này sẽ đổi, hãy mở trang gốc.)
- Nền tảng đối tác (Amazon Bedrock, Google Cloud do Google quản lý) có lịch ngừng riêng, có thể khác.
- **Trôi dạt tham số API:** trang ghi rằng `temperature`, `top_p`, `top_k` bị gỡ ở phiên bản API `2026-10-21` (gửi các tham số này sẽ trả về lỗi 400); trang khuyên bỏ chúng và dùng prompt để định hướng hành vi. Ba tham số này là các "nút chỉnh" mức ngẫu hứng khi AI chọn từ; lỗi 400 là mã báo "yêu cầu không hợp lệ". Điều này quan trọng cho SME dùng code nhẹ: mã cũ đặt `temperature=0` có thể **hỏng ngay khi nâng phiên bản API**. (Cũng do vậy, Miller khuyên *không* chỉnh temperature để giảm nhiễu đánh giá **[Nguồn arXiv 2411.00640]**; để giảm nhiễu hãy chấm lại nhiều lần.)
- Nhà cung cấp khác (OpenAI, Google...) có chính sách riêng; **chưa tra cứu** trong đợt này.

**Các nguồn trôi dạt khác [Đề xuất]:** tài liệu nội bộ cập nhật (bảng giá, chính sách); đổi phiên bản chính sách mà tài liệu cũ vẫn còn trong chỉ mục (chỉ mục là "kho mục lục" để AI tra tài liệu); thay đổi định dạng file đầu vào; và mô hình đổi hành vi mà *không đổi tên* (một số nhà cung cấp dùng bí danh "latest", luôn trỏ tới bản mới nhất; hãy ghim phiên bản có ngày hoặc ID cụ thể khi có thể, và ghi ID đó vào log).

!!! tip "Nói đơn giản"
    Mô hình AI giống một món hàng mà nhà cung cấp có thể ngừng bán theo lịch. Họ báo trước (với Anthropic là ít nhất 60 ngày), nhưng nếu không ai đọc thư, hệ thống của bạn sẽ ngừng chạy đúng ngày đó. Ngoài ra, những "nút chỉnh" nhỏ trong mã cũng có thể bị gỡ, khiến mã cũ báo lỗi. Cách phòng: biết công ty đang dùng mô hình nào ở đâu, và canh lịch ngừng đều đặn.

---

## 4. Chuỗi bài nhỏ

Mỗi bài mất khoảng 30–120 phút. Bài 9.1–9.4 là cốt lõi: nếu thời gian có hạn, hãy làm bốn bài này trước. Mỗi bài có phần mục tiêu, việc cần làm, thứ bạn có sau bài và lỗi hay gặp để tránh.

### Bài 9.1: Nhật ký (log) mỗi lần gọi
- **Mục tiêu:** mỗi lần AI chạy để lại một dòng ghi chép, đủ để tái hiện lại lần đó và đo lường sau này.
- **Trường tối thiểu [Đề xuất]:** "trường" là một cột thông tin trong dòng ghi chép. Nên có các trường sau:
  - `ts`: thời điểm gọi.
  - `request_id`: mã định danh của lần gọi, để tìm lại đúng lần đó.
  - `prompt_id` + `version`: chỉ dẫn nào, phiên bản nào đã được dùng.
  - `model`: đúng ID/phiên bản mô hình đã dùng.
  - `input`: câu hỏi đưa vào (đã che).
  - `output`: câu trả lời nhận về (đã che).
  - `tools`: tên công cụ AI đã dùng, kèm trạng thái từng bước.
  - `retrieved_ids`: ID tài liệu hoặc đoạn tài liệu được đưa cho AI, để tách riêng việc đo khâu tìm tài liệu (truy hồi) như ở Cấp 6.
  - `latency_ms`: độ trễ, tức AI mất bao nhiêu mili giây để đáp.
  - `tokens_in`, `tokens_out`: lượng chữ đi vào và đi ra, đếm bằng token (đơn vị đếm chữ mà AI dùng, nhà cung cấp tính tiền theo đó).
  - `cost_est`: chi phí ước tính của lần gọi.
  - `error`: lỗi nếu có.
  - `user_group`: nhóm người dùng (không phải tên người).
  - `feedback`: nếu có thì ghi tốt, xấu hoặc người dùng đã sửa.
  - Với agent nhiều bước, mỗi bước một dòng với `step_id`, `type`, `status`, `input`, `output` (lược đồ gợi ý từ arXiv 2610.03315 **[Nguồn]**).
- **Che dữ liệu nhạy cảm [Đề xuất]:** che *trước khi ghi*, không phải sau. Mặc định không ghi nội dung nếu việc không cần (chỉ ghi ID, độ dài, hoặc băm; băm là biến nội dung thành một dãy ký tự để đối chiếu mà không đọc ngược lại được). Giới hạn ai đọc được log. Quy định thời hạn lưu và thời điểm xóa. **Không** ghi khóa API. Mẫu che ở đoạn mã dưới đây chỉ là *ví dụ tối thiểu* (email, điện thoại VN, dãy số 9–12 chữ số) và sẽ **bỏ sót** nhiều thứ (tên người, địa chỉ); bạn cần mở rộng và kiểm với dữ liệu thật của mình. Quy định pháp lý (Nghị định về bảo vệ dữ liệu cá nhân của Việt Nam) **chưa tra cứu trong đợt này**; hãy nhờ người am hiểu pháp lý xem trước khi lưu dữ liệu khách.
- **Đoạn mã dưới đây làm gì?** Nó có hai phần. Phần một "che": tìm email, số điện thoại Việt Nam và các dãy 9 đến 12 chữ số trong câu hỏi hoặc câu trả lời, rồi thay bằng `[EMAIL]`, `[PHONE]`, `[ID]`. Phần hai "ghi sổ": thêm giờ gọi, che dữ liệu rồi ghi đúng một dòng vào tệp `calls.jsonl`. Dòng cuối là một lần gọi mẫu để thử. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ người biết lập trình (hoặc nhờ AI) chạy giúp khi cần đến mức này.
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
  Mỗi dòng là một JSON (định dạng JSON Lines). JSON là cách viết dữ liệu theo kiểu "tên: giá trị" có khung rõ ràng để máy đọc được. Tệp này mở được bằng Excel/Sheets sau khi nhập, hoặc bằng vài dòng Python.
- **Đường không code:** Project/Gem/GPT thường không cho log có cấu trúc đầy đủ. Hãy dùng một Google Sheet "Sổ dùng AI" để nhân viên tự ghi: ngày, việc, công cụ + phiên bản prompt, kết quả (dùng được/sửa nhẹ/sửa nặng/bỏ), thời gian sửa, ghi chú lỗi. Đây là log thô nhưng đủ để thấy xu hướng. (Khả năng xuất lịch sử hội thoại của từng công cụ khác nhau và đổi nhanh; **chưa kiểm** trong đợt này.)
- **Công cụ quan sát có sẵn:** chuẩn OpenTelemetry cho GenAI (một bộ quy ước chung về cách ghi dữ liệu theo dõi hệ thống AI) được chuyển sang kho riêng (trang cũ ghi "moved"; thuộc tính cụ thể **chưa đọc được** trong đợt này, xem mục 9). SME nhỏ chưa cần dùng ngay; log JSON Lines ở trên đã đủ.
- **Bạn có sau bài:** file `calls.jsonl` (hoặc Sheet) chạy thật 1 tuần; mỗi tuần có một người đọc thử 20 dòng ngẫu nhiên.
- **Lỗi hay gặp:** ghi nguyên văn dữ liệu khách; log không có phiên bản prompt hay mô hình nên không so sánh được; ghi log nhưng không ai đọc (Hamel: phải *bỏ ma sát* khi xem dữ liệu, tức làm cho việc xem log dễ nhất có thể **[Nguồn]**).

!!! tip "Nói đơn giản"
    Log giống cuốn sổ trực của bảo vệ: ai vào, lúc nào, làm gì. Không có sổ thì khi có chuyện, không ai chứng minh được điều gì đã xảy ra. Nhưng sổ này không được ghi số CCCD hay số điện thoại khách thật; phải che trước khi ghi.

### Bài 9.2: Phiên bản hóa prompt/skill
- **Mục tiêu:** biết chính xác bản nào đang chạy, và quay lui được khi cần.
- **Việc cần làm [Đề xuất]:**
  1. Mỗi prompt/skill có **ID + phiên bản**, ví dụ `tra-cuu-bao-hanh@v3`. Thay đổi *bất kỳ chữ nào* cũng là phiên bản mới (kể cả đổi tài liệu đính kèm hoặc đổi mô hình, vì Nubank coi đổi mô hình như đổi prompt **[Nguồn do chủ dự án cung cấp]**).
  2. Lưu prompt dưới dạng file văn bản trong một thư mục chung. Đường code: dùng Git (công cụ lưu lịch sử mọi lần sửa file), mỗi lần sửa là một commit (một lần lưu) có ghi lý do; ESCROW coi mỗi thay đổi là một diff đọc được **[Nguồn do chủ dự án cung cấp]**. Đường không code: Google Doc có lịch sử phiên bản, cộng một Sheet "Nhật ký thay đổi".
  3. **Nhật ký thay đổi (changelog)**, mỗi dòng gồm: ngày, ID@phiên bản, người sửa, **vì sao**, thay đổi gì (diff ngắn), điểm bộ ca trước/sau (ghi k/n, tức đúng k trên n ca), người duyệt.
  4. Ghi trong cấu hình: bản nào là **đang chạy (production)**, bản nào là **bản trước đó** (để rollback, tức quay lại bản cũ khi bản mới có vấn đề).
  5. Với Project/Gem/GPT tùy chỉnh: sao chép bản "đang chạy" thành bản "thử" để sửa; không sửa trực tiếp bản mà mọi người đang dùng.
- **Bạn có sau bài:** thư mục `prompts/` (hoặc Doc) cùng changelog.
- **Lỗi hay gặp:** "sửa nhanh cho gấp" ngay trên bản đang chạy; không ghi lý do; để prompt rải rác trong tin nhắn cá nhân.

!!! tip "Nói đơn giản"
    Giống một công thức nấu ăn của quán: mỗi lần chỉnh gia vị phải ghi "ngày nào, ai chỉnh, vì sao, ngon hơn hay dở hơn". Khi khách chê, bạn quay lại được công thức cũ ngay, thay vì ngồi đoán xem hôm qua ai đã thêm gì.

### Bài 9.3: Quy trình sửa, chạy lại, so sánh, phát hành (kiểu ESCROW/Nubank thu nhỏ)
- **Mục tiêu:** không bản nào lên production (bản đang chạy thật) nếu làm xấu đi chất lượng đã đạt.
- **Việc cần làm [Đề xuất, dựa nguyên tắc của ESCROW/Nubank — nguồn do chủ dự án cung cấp]:**
  1. **Mở phiếu thay đổi** (1 dòng changelog trạng thái "đề xuất"): ghi lỗi nào, bản sửa nào.
  2. **Sửa trên bản "thử"**, và chỉ dùng bộ ca *dev* (nhóm ca dùng để nhìn lỗi và sửa) để nhìn lỗi.
  3. **Chạy lại toàn bộ bộ ca**: dev, các ca lỗi cũ đã sửa, và held-out (nhóm ca giữ kín, không dùng khi sửa, để kiểm tra xem bản sửa có thật sự tốt hơn không). Bộ ca là "kho ca cũ": ESCROW cho thấy thiếu kho này thì ca cũ tụt điểm **[Nguồn do chủ dự án cung cấp]**.
  4. **So sánh theo từng ca và theo nhóm** (Cấp 6, bài 6.8): ca nào tốt lên, ca nào hỏng, nhóm nào xấu đi.
  5. **Điều kiện phát hành:** (a) không nhóm hay loại việc nào xấu đi; (b) mọi ca lỗi đã sửa trước đó vẫn đúng; (c) ca mới hỏng phải có giải thích và được người duyệt chấp nhận; (d) held-out không tụt. Với bộ ca nhỏ, các điều kiện này là "cổng chặn lỗi hiển nhiên", không phải chứng minh thống kê (Cấp 6 mục 3.2).
  6. **Rollout nhỏ** (một nhóm hoặc 10% người dùng trong 1–2 tuần), có nút quay lại bản trước.
  7. Ghi kết quả vào changelog và đóng phiếu.
  8. **Chi phí chấm lại** là nút thắt (ESCROW **[Nguồn do chủ dự án cung cấp]**; Meta: ba giờ mỗi lượt chạy bộ 519 câu **[Nguồn arXiv 2609.21267]**). Với SME: giữ bộ ca vừa phải (20–60), chạy bằng grader mã khi được (grader mã là chương trình chấm đơn giản, ví dụ so khớp đáp án, không cần nhờ AI chấm); chỉ gọi judge AI cho ca cần. Chỉ cân nhắc "tập con" khi bộ ca đủ lớn để việc chạy trọn bộ trở thành nút thắt.
- **Chấm lại khi nào [Đề xuất tổng hợp]:** khi đổi prompt; đổi mô hình hoặc phiên bản API; đổi hoặc nhập tài liệu mới vào chỉ mục; đổi công cụ; và định kỳ (ví dụ mỗi tháng) kể cả khi không đổi gì, để bắt trôi dạt do nhà cung cấp. Khuyến nghị của She & Lin: hiệu chuẩn lại sau thay đổi vật chất về mô hình/prompt/công cụ/hệ thống, hoặc khi kết quả theo câu lệch kéo dài **[Nguồn]**.
- **Bạn có sau bài:** một "phiếu thay đổi" một trang cho mỗi lần sửa; changelog được cập nhật.
- **Lỗi hay gặp:** bỏ qua held-out vì "chỉ sửa chữ nhỏ"; chỉ chạy lại đúng ca vừa lỗi; đổi mô hình mà không chạy lại vì "mô hình mới chắc tốt hơn" (Nubank: coi là thay đổi phải chạy lại).

!!! tip "Nói đơn giản"
    Hãy xem bộ ca như đề thi lại. Mỗi lần sửa chỉ dẫn là cho AI "thi lại" toàn bộ đề, không chỉ câu vừa sai. Bản sửa chỉ được đưa vào dùng thật khi điểm không giảm ở chỗ nào, và vẫn có đường quay lại bản cũ.

### Bài 9.4: Xử lý trôi dạt, khi tài liệu đổi và khi mô hình đổi hoặc ngừng
- **Mục tiêu:** không bị bất ngờ khi nhà cung cấp ngừng mô hình hay khi tài liệu đổi.
- **Việc cần làm:**
  1. **Kiểm kê:** lập bảng "Hệ thống AI của công ty" gồm: tên, chủ sở hữu, mô hình + phiên bản/ID, nhà cung cấp, nền tảng (trực tiếp hay qua Bedrock/Google Cloud), phiên bản prompt, nơi lưu log. Với Claude API, có thể xuất CSV Usage theo API key và mô hình để tìm chỗ còn dùng mô hình sắp ngừng **[Nguồn: Model deprecations, ngày 2026-11-11]**.
  2. **Lịch xem thông báo:** mỗi tháng người phụ trách mở trang chính sách ngừng mô hình của từng nhà cung cấp đang dùng, và đọc email thông báo (Anthropic cam kết ≥ 60 ngày thông báo **[Nguồn]**). Đặt nhắc lịch.
  3. **Khi có thông báo:** (a) đọc hướng dẫn di chuyển và danh sách tham số bị gỡ hoặc đổi; (b) tạo bản "thử" trỏ tới mô hình thay thế; (c) chạy bộ ca (bài 9.3); (d) so sánh; (e) rollout; (f) hoàn tất **trước** ngày ngừng, chừa biên an toàn (ví dụ ≥ 2 tuần) **[Đề xuất]**. Ví dụ thực tế của trang: một mô hình ngừng 2026-11-30 (xem mục 3.2); nếu thông báo ngày 2026-09-30 thì thời gian là đúng 61 ngày.
  4. **Đổi tài liệu:** mỗi lần tài liệu nguồn đổi (bảng giá, chính sách): ghi ngày hiệu lực; **gỡ bản cũ khỏi chỉ mục** hoặc đánh dấu hết hạn; cập nhật đáp án các ca bị ảnh hưởng; chạy lại các ca thuộc tài liệu đó.
  5. **Giám sát nhẹ giữa các lần đổi:** hằng tuần xem tỉ lệ lỗi và tỉ lệ "sửa nặng" từ sổ log/Sheet; hằng tháng chạy lại bộ ca với chính bản đang chạy (không đổi gì) để xem điểm có trôi không.
- **Đường code:** một script (đoạn chương trình ngắn) chạy bộ ca theo lịch (cron hoặc Task Scheduler, tức công cụ hẹn giờ tự chạy), ghi k/n vào một file theo ngày, và gửi cảnh báo khi điểm tụt quá ngưỡng đã đặt trước.
- **Bạn có sau bài:** bảng kiểm kê hệ thống AI; lịch trôi dạt; biểu đồ hoặc bảng điểm theo ngày.
- **Lỗi hay gặp:** mã cứng ID mô hình rải khắp nơi (đổi mô hình phải sửa nhiều chỗ); dùng bí danh "latest" rồi bị đổi hành vi; bỏ qua email thông báo (gửi vào hộp thư của người đã nghỉ); thấy "mô hình mới chạy được" là xong.

!!! tip "Nói đơn giản"
    Giống việc giấy phép hay hợp đồng thuê có ngày hết hạn: bạn cần một bảng ghi rõ cái nào hết hạn khi nào, và một người được giao mở bảng đó mỗi tháng. Thư báo gửi vào hộp thư người đã nghỉ việc thì coi như chưa ai nhận được.

### Bài 9.5: Giám sát chi phí và hạn mức
- **Mục tiêu:** biết tiền và hạn mức đi đâu, và báo động trước khi vượt.
- **Việc cần làm:**
  1. Ghi `tokens_in`, `tokens_out`, `cost_est` mỗi lần gọi (bài 9.1). Giá theo bảng công bố của nhà cung cấp tại ngày bạn tính (giá thay đổi; **không** ghi giá cố định trong tài liệu này).
  2. Tổng hợp theo tuần: theo hệ thống, theo nhóm dùng, theo loại việc. Tính **chi phí trên mỗi việc hoàn thành** và so với thời gian tiết kiệm (Cấp 6, bài 6.7).
  3. Đặt **ngân sách tháng** cho từng hệ thống; cảnh báo ở mốc ví dụ 50%/80%/100% **[Đề xuất]**. Công cụ cảnh báo của từng nền tảng khác nhau và đổi nhanh; **chưa kiểm** trong đợt này; nếu nền tảng không có, hãy tự kiểm tra bảng tổng hợp hằng tuần.
  4. Tách API key theo hệ thống hoặc theo nhóm để thấy từng phần (dựa trên việc Usage có chia theo API key **[Nguồn: Model deprecations]**); đặt giới hạn chi tiêu nếu nền tảng hỗ trợ (**chưa kiểm**).
  5. Giảm chi phí: ngắt vòng lặp (giới hạn số bước hoặc số lần thử); cắt ngữ cảnh thừa (bớt phần chữ đưa vào AI mà không cần); dùng mô hình nhỏ cho việc dễ (phải chạy lại bộ ca khi đổi); giảm số lần chấm bằng judge. Dữ liệu từ arXiv 2610.03315: chuẩn hóa và cắt gọn log rồi dùng một lần gọi judge giảm chi phí chấm khoảng 6 lần trong bộ thử của họ **[Nguồn]**; đừng suy ra tương tự cho việc của bạn.
  6. Với dùng gói thuê bao (Claude/ChatGPT/Gemini desktop): theo dõi số người dùng thật, ai bị giới hạn lượt, ai không dùng nữa (cắt gói thừa) **[Đề xuất]**.
- **Bạn có sau bài:** bảng chi phí tuần/tháng + ngân sách + cảnh báo.
- **Lỗi hay gặp:** vòng lặp agent không giới hạn; một key dùng chung cho mọi thứ; so chi phí mà quên chi phí nhân sự bảo trì.

!!! tip "Nói đơn giản"
    Giống hóa đơn điện: nếu cả công ty dùng chung một công tơ thì không ai biết phòng nào tốn điện. Tách key (mỗi hệ thống một "công tơ") và đặt mốc cảnh báo để biết trước khi hóa đơn lớn lên, chứ không phải sau khi nhận.

### Bài 9.6: Quản lý lỗi và nhật ký sự cố
- **Mục tiêu:** lỗi được xếp loại, sửa tận gốc, và để lại bài học.
- **Việc cần làm [Đề xuất]:**
  1. **Phân loại mức độ** (ví dụ): Sev1 = lộ dữ liệu / gửi sai cho khách / số tiền sai đã ra ngoài; Sev2 = trả lời sai ảnh hưởng quyết định nhưng chưa ra ngoài; Sev3 = chất lượng kém, khó chịu. ("Sev" là viết tắt của severity, nghĩa là mức nghiêm trọng.) Với Sev1: **dừng hệ thống hoặc rút bản mới ngay**, và báo người chịu trách nhiệm.
  2. **Sổ sự cố** (làm trên Sheet): ngày, mức độ, mô tả, `request_id`, phát hiện thế nào, ảnh hưởng, nguyên nhân gốc (tài liệu? truy hồi? prompt? mô hình? người dùng sai cách?), cách xử lý tạm, sửa dứt điểm (link phiếu thay đổi), **ca mới đã thêm vào bộ ca chưa** (bắt buộc: mọi sự cố thật trở thành 1 ca hồi quy, như "lỗi thật → ca eval" của Anthropic **[Nguồn]**), người phụ trách, ngày đóng.
  3. **Lỗi kỹ thuật khi gọi API:** thử lại có giới hạn (số lần, thời gian chờ), ghi `error` vào log; không thử lại vô hạn (đốt tiền). Mã lỗi cụ thể theo nhà cung cấp, **chưa tra cứu** trong đợt này.
  4. **Họp rà ngắn** mỗi tháng 30 phút: xem sổ sự cố, xu hướng, và 20 dòng log ngẫu nhiên.
- **Bạn có sau bài:** sổ sự cố; quy tắc mức độ; luồng "sự cố → ca hồi quy". (Ca hồi quy là ca kiểm tra được thêm vào bộ ca để lỗi cũ không quay lại lần nữa.)
- **Lỗi hay gặp:** sửa prompt vá đúng lỗi mà không thêm ca (lỗi quay lại); đổ lỗi "AI ngu" thay vì tìm nguyên nhân gốc; giấu sự cố.

!!! tip "Nói đơn giản"
    Mỗi lần AI sai thật là một bài học miễn phí, nhưng chỉ khi bạn ghi lại và biến nó thành một câu hỏi trong bộ ca. Nếu chỉ "vá cho qua", lần sau lỗi đó sẽ quay lại mà không ai nhớ đã từng gặp.

### Bài 9.7: Ai chịu trách nhiệm (phân vai)
- **Mục tiêu:** mỗi hệ thống có chủ rõ ràng và có người dự phòng.
- **Việc cần làm [Đề xuất]:** lập bảng RACI một trang (bảng cho biết với mỗi việc thì ai làm, ai chịu trách nhiệm cuối, ai được hỏi ý kiến, ai chỉ cần biết), tối thiểu có các vai sau:
  - **Chủ hệ thống (owner)**: một người tên cụ thể cho mỗi hệ thống AI; chịu trách nhiệm chất lượng, phiên bản, ngân sách.
  - **Người duyệt phát hành**: khác người sửa (nguyên tắc "hai người" cho thay đổi lên production; ESCROW dành diff đọc được cho bộ phận tuân thủ **[Nguồn do chủ dự án cung cấp]**).
  - **Người phụ trách dữ liệu/bảo mật**: quyết định dữ liệu nào được đưa vào công cụ AI nào, và thời hạn lưu log.
  - **Người dự phòng** cho từng vai (tránh "một người nghỉ là mồ côi").
  - **Lãnh đạo**: quyết định ngân sách và mức rủi ro chấp nhận được.
  - Ghi rõ **người ra quyết định cuối** khi AI sai ảnh hưởng tới khách (con người chịu trách nhiệm, không phải "AI nói vậy").
- **Bạn có sau bài:** bảng RACI + danh bạ khẩn.
- **Lỗi hay gặp:** "ai cũng là chủ" nên không ai là chủ; chủ là người ngoài công ty mà không có quyền truy cập đầy đủ.

!!! tip "Nói đơn giản"
    Một hệ thống mà "ai cũng có thể sửa, không ai phải chịu trách nhiệm" sớm muộn sẽ hỏng. Hãy ghi tên cụ thể: ai là chủ, ai duyệt, ai thay khi người đó vắng. Khi AI sai với khách, người chịu trách nhiệm vẫn là một con người trong công ty.

### Bài 9.8: Đào tạo và quy tắc dùng cho cả nhóm
- **Mục tiêu:** cả nhóm dùng AI nhất quán, và giảm việc dùng "vô tội vạ".
- **Việc cần làm [Đề xuất]:**
  1. **Quy tắc dùng một trang:** (a) dữ liệu *không bao giờ* được dán vào công cụ AI công cộng (ví dụ CCCD, số tài khoản, hợp đồng khách, lương); (b) chỉ dùng hệ thống đã được duyệt cho việc đó; (c) *mọi* đầu ra gửi ra ngoài phải có người xem; (d) cách báo lỗi/sự cố (1 chạm vào Sheet); (e) ai xin thêm công cụ mới, theo quy trình nào.
  2. **Buổi đào tạo 60–90 phút:** ví dụ hệ thống đã duyệt; 5 lỗi AI hay mắc (bịa, sai số, theo mồi, lệ thuộc thứ tự/độ dài, lỗi do dữ liệu cũ); thực hành báo lỗi.
  3. **Kiểm tra định kỳ:** mỗi quý xem lại quy tắc; chọn ngẫu nhiên vài phiên dùng để rà (có thông báo trước, tránh giám sát lén).
  4. **Danh sách "dùng AI vô tội vạ" đang tồn tại** (kiểm kê "shadow AI", tức việc nhân viên tự dùng công cụ AI ngoài tầm kiểm soát của công ty): hỏi nhân viên đang dùng công cụ nào cho việc gì; đưa vào hệ thống đã duyệt hoặc cấm.
- **Bạn có sau bài:** quy tắc một trang đã ký nhận; tài liệu đào tạo; sổ ghi người đã học.
- **Lỗi hay gặp:** quy tắc dài như luật; cấm hoàn toàn nên người dùng lén dùng; đào tạo một lần rồi quên.

!!! tip "Nói đơn giản"
    Quy tắc tốt giống biển báo giao thông: ngắn, rõ, ai cũng đọc được trong vài giây. Nếu cấm tuyệt đối mọi thứ, nhân viên sẽ dùng AI lén bằng tài khoản cá nhân, và công ty còn kém kiểm soát hơn. Cách khôn hơn là hỏi họ đang dùng gì rồi đưa vào danh sách đã duyệt.

### Bài 9.9: Khi nào nâng cấp, từ dùng tay sang tự động hóa, tích hợp, hoặc thuê làm
- **Mục tiêu:** quyết định dựa trên số đo, không dựa trên cảm hứng.
- **Dấu hiệu nên nâng cấp [Đề xuất, ngưỡng là ví dụ, tự điều chỉnh theo công ty]:**

| Dấu hiệu đo được | Nâng cấp tới |
|---|---|
| Một việc lặp > ~50–100 lần/tháng, bước thủ công chiếm đa số thời gian, chấm bộ ca đã ổn (k/n ổn định ≥ 3 tháng) | Tự động hóa (code nhẹ/quy trình Cấp 8) |
| Người dùng phải sao chép dữ liệu qua lại giữa AI và phần mềm (CRM, kế toán, kho) > vài lần/ngày, tổng thời gian đáng kể | Tích hợp (Cấp 7 công cụ/API) |
| Chi phí sửa lỗi/ thời gian soát > thời gian tiết kiệm đo được (bài 6.7), hoặc sự cố Sev1/Sev2 lặp lại | Quay lại sửa Cấp 3–6, **chưa** nâng cấp |
| Cần xử lý dữ liệu nhạy cảm hoặc quy định đòi kiểm toán, nhưng không có người đủ năng lực | Thuê chuyên gia/đơn vị ngoài (kèm bộ ca và changelog của bạn làm "đặc tả nghiệm thu") |
| Chủ hệ thống nghỉ/quá tải, bảo trì ngốn nhiều thời gian hơn lợi ích | Thuê/hoặc đơn giản hóa |
| Nhu cầu vượt hạn mức hoặc độ trễ của công cụ desktop, cần SLA | Chuyển sang API/hạ tầng riêng |

- **Cách đo:** dùng số từ log (số lượt, độ trễ, chi phí) và sổ thời gian (Cấp 6, bài 6.7). Tính **hoàn vốn** = chi phí dựng + chi phí vận hành/tháng, so với thời gian tiết kiệm × giá trị giờ công. Khi thuê làm, hãy đòi bộ ca làm tiêu chí nghiệm thu.
- **Bạn có sau bài:** một "hồ sơ đề xuất nâng cấp" 1 trang: số đo hiện tại, ngưỡng, ước tính hoàn vốn, rủi ro.
- **Lỗi hay gặp:** nâng cấp để "theo kịp xu hướng"; tự động hóa một quy trình chưa có đáp án đúng để đo; thuê làm mà không có bộ ca nghiệm thu.

!!! tip "Nói đơn giản"
    Trong bảng trên, CRM là phần mềm quản lý khách hàng; SLA là cam kết về mức dịch vụ (độ ổn định, tốc độ). Ý chính của cả bảng: chỉ nâng cấp khi con số cho thấy đáng, và nếu hệ thống hiện tại còn hay sai thì sửa nó trước, đừng chất thêm tự động hóa lên một nền chưa vững.

---

## 5. Đường không code vs đường có code; khi nào buộc phải chuyển

Mọi việc ở mục 4 đều làm được bằng Sheet và Doc. Bảng dưới cho thấy mỗi việc ở hai đường. "Code nhẹ" nghĩa là một vài đoạn chương trình Python ngắn, thường nhờ người biết lập trình hoặc nhờ AI viết giúp.

| Việc | Không code | Có code (Python nhẹ) |
|---|---|---|
| Log mỗi lần gọi | Sổ Sheet nhân viên tự ghi; ghi nhận thủ công | JSON Lines tự động (bài 9.1) |
| Phiên bản prompt | Doc có lịch sử + Sheet changelog | Git, diff đọc được |
| Chạy lại bộ ca | Người chạy tay theo danh sách | Script chạy theo lịch, lưu điểm theo ngày |
| Giám sát chi phí | Xem trang sử dụng/hóa đơn tay mỗi tuần | Tổng hợp từ log, cảnh báo |
| Kiểm kê mô hình | Bảng kiểm kê tay + nhắc lịch | Xuất CSV usage, script đối chiếu |

**Buộc phải chuyển sang code khi [Đề xuất]:** (1) hệ thống gọi API (không còn là Project/Gem/GPT), vì khi đó log phải tự động; (2) có công cụ hoặc nhiều bước (Cấp 7–8) cần log từng bước; (3) bộ ca > ~50 hoặc việc chạy lại thủ công bị bỏ qua; (4) cần rollback nhanh, và cần tách môi trường thử với môi trường chạy thật; (5) cần cảnh báo chi phí theo thời gian thực.

!!! tip "Nói đơn giản"
    Bắt đầu bằng sổ tay và bảng tính là hoàn toàn bình thường. Chỉ khi việc ghi chép bằng tay bắt đầu bị bỏ qua, hoặc hệ thống đã tự chạy mà không có người ngồi trước màn hình, thì mới cần đến code để ghi và canh thay cho người.

---

## 6. Tiêu chí lên cấp tiếp theo (đo được)

Cấp 9 là cấp cuối của khung này. Tiêu chí "xong cấp 9" **[Đề xuất]**:
1. Mỗi hệ thống AI trong công ty có trong bảng kiểm kê, có chủ + người dự phòng.
2. Có log (Sheet hoặc JSONL) ≥ 4 tuần liên tục; đã đọc rà ≥ 20 dòng ngẫu nhiên mỗi tuần.
3. Có changelog; mọi thay đổi trong 3 tháng gần nhất đều có k/n trước–sau và người duyệt.
4. Đã từng chạy lại bộ ca ít nhất một lần do sự kiện bên ngoài (đổi mô hình/tài liệu) hoặc theo lịch tháng.
5. Có sổ sự cố; mỗi sự cố Sev1/Sev2 đã thành ca hồi quy.
6. Có ngân sách + cảnh báo chi phí; không vượt ngân sách bất ngờ 3 tháng liền.
7. Quy tắc dùng AI một trang đã được cả nhóm học và ký nhận.

Chỉ khi đủ các điều trên mới xét nâng cấp tự động hóa, tích hợp hoặc thuê làm theo bảng ở bài 9.9.

---

## 7. Ví dụ cho SME Việt Nam (minh họa, **không** phải số liệu thật)

Hai tình huống giả định dưới đây giúp bạn hình dung các bài ở mục 4 chạy cùng nhau ra sao.

**Công ty du lịch ~20 người, bot gọi API trả lời lịch tour và giá cho nhân viên tư vấn:**
- Log JSONL: mỗi lượt có `prompt_id=tour-gia@v5`, `model=<id>`, `retrieved_ids`, `latency_ms`, `cost_est`, `feedback` (nhân viên bấm tốt/xấu); số điện thoại khách bị che trước khi ghi.
- Tháng 10: bảng giá tour đổi, người phụ trách đánh dấu hết hạn bản cũ, cập nhật 6 ca, chạy lại 30 ca: 26/30 → 28/30; ca hỏng 0.
- Nhận email thông báo mô hình đang dùng sắp ngừng (ví dụ 60 ngày trước hạn): tạo bản thử trỏ mô hình thay thế; chạy bộ ca; thấy 2 ca nhóm "giá có điều kiện" xấu đi, nên sửa prompt (v6), chạy lại, phát hành cho 3 nhân viên trong 2 tuần rồi cho cả nhóm; ghi vào changelog.
- Sự cố Sev2: bot báo sai giá khuyến mãi hết hạn. Nguyên nhân gốc: tài liệu cũ còn trong chỉ mục. Xử lý: gỡ tài liệu; thêm 2 ca hồi quy; thêm bước "ngày hiệu lực" vào quy trình cập nhật tài liệu.
- Chi phí: API ~theo bảng tổng hợp tuần; một nhân viên phụ trách (có người dự phòng); họp rà 30 phút mỗi tháng.

**Văn phòng luật/kế toán 8 người, chỉ dùng gói desktop:** không có log tự động; dùng "Sổ dùng AI" trên Sheet (ngày, việc, công cụ + phiên bản prompt, kết quả, thời gian sửa); quy tắc cấm dán hồ sơ khách; kiểm kê thấy ba người đang dùng ba công cụ khác nhau và thống nhất chọn một; bộ 20 ca được chạy lại tay mỗi quý và mỗi khi đổi công cụ.

---

## 8. Tài liệu tham khảo

Ngày truy cập tất cả: 2026-11-11. "Mức tin cậy" là nhận định của người soạn. ("Preprint" là bản thảo nghiên cứu đăng công khai trước khi được bình duyệt.)

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
