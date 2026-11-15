# Cấp 1 (C1): Gọi AI qua API

> Ngày soạn: 2026-11-11. Nguyên tắc (bền) tách khỏi thao tác/tên tham số/model (hay đổi, có ghi ngày).
> **[Nguồn]** = đọc được trong tài liệu chính thức; **[Đề xuất]** = của chúng tôi.
> Không đưa giá cụ thể: chỉ nêu cách tính. Muốn con số, mở trang giá chính thức tại thời điểm dùng (mục 8).
> Không phải tư vấn pháp lý; xem `../an-toan-du-lieu-va-phap-ly-vn.md` trước khi gửi dữ liệu khách hàng qua API.

!!! tip "Tóm tắt nhanh"
    Ở cấp trước, bạn dán dữ liệu vào khung chat và chờ AI trả lời. Cách đó không chạy được 500 lần liên tiếp. Bài này dạy bạn nhờ một chương trình nhỏ (script) gọi AI thay bạn qua **API** (cổng để chương trình này nói chuyện với chương trình khác). Kết quả trả về có khung rõ ràng, mỗi lần chạy có ghi số token và chi phí ước tính, lỗi được xử lý gọn, và khóa truy cập được giữ an toàn. Bài này vẫn có phần viết code, nên nếu bạn không lập trình, hãy đọc để hiểu và giao việc cho người biết code.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người có thể viết hoặc đọc Python cơ bản trong doanh nghiệp nhỏ và vừa (SME), như IT kiêm nhiệm, kế toán biết Excel nâng cao, freelancer. Hoặc chủ SME muốn hiểu để giao việc cho người khác. (Python là một ngôn ngữ lập trình phổ biến, hay dùng để viết các chương trình nhỏ loại này.)

**Bạn cần chuẩn bị:**
- Một nghiệp vụ ở cấp C0 đã có sẵn **prompt** (đoạn chỉ dẫn bạn viết cho AI) và các **ca thử** (những mẫu đầu vào có đáp án để kiểm).
- Khả năng viết hoặc đọc Python cơ bản, hoặc một người biết code đi cùng bạn.
- Một tài khoản API của nhà cung cấp mô hình AI (Claude hoặc OpenAI trong bài này), kèm khóa API (sẽ giải thích ở mục 3.6).

**Mục tiêu:** sau cấp này, từ một nghiệp vụ C0 đã có prompt và ca thử, bạn chạy được nó bằng script. Cụ thể là:
- Một lệnh gọi duy nhất cho mỗi việc.
- Đầu ra có cấu trúc (JSON, tức là cách viết dữ liệu có khung rõ ràng để máy và bảng tính đọc được).
- Biết **mỗi lần chạy tốn bao nhiêu token và tiền**. (Token là đơn vị đếm lượng chữ mà AI đọc và viết; nhà cung cấp tính tiền theo đơn vị này.)
- Xử lý được lỗi và giới hạn tốc độ.
- Giữ khóa API an toàn.

**Sau bài này bạn sẽ có:** một nghiệp vụ chạy được hàng loạt bằng script, có nhật ký đầy đủ để biết nó chạy tốt hay hỏng, tốn bao nhiêu.

**Thứ bạn cầm đi được:** một script `run.py` + một file `prompts/<nghiep_vu>.md` + file CSV nhật ký (thời gian, mã yêu cầu, token vào/ra, chi phí ước tính, kết quả hợp lệ/không) + một khóa API riêng có hạn mức chi. (CSV là loại file bảng đơn giản, mở được bằng Excel.)

## 2. Câu hỏi cấp này trả lời / lỗi của C0

Cách làm ở C0 (dán vào khung chat) có những điểm yếu, và chính các điểm yếu này dẫn bạn tới C1:
- Không chạy hàng loạt được.
- Khó ghi nhật ký.
- Đầu ra là văn bản tự do nên khó đưa vào bảng tính.
- Không tính được chi phí theo từng việc.
- Mỗi người dán dữ liệu vào tài khoản cá nhân của mình.

Câu hỏi của cấp này: *"Làm sao chạy cùng một việc 500 lần, ra đúng cấu trúc, biết tốn bao nhiêu, và lỗi thì xử lý ra sao?"*

Hãy hình dung bạn mở một quán ăn. Ở C0, mỗi khách tự vào bếp nói với đầu bếp món mình muốn. Ở C1, bạn có một tờ phiếu gọi món in sẵn, một bàn giao phiếu cho bếp, và một cuốn sổ ghi mỗi phiếu tốn bao nhiêu nguyên liệu. API chính là cửa sổ nhận phiếu đó.

## 3. Kiến thức nền

### 3.1 Nguyên tắc (bền)

1. **Một lệnh gọi = (system prompt + messages) vào, (văn bản + thông tin sử dụng) ra.** *System prompt* là phần chỉ dẫn cố định cho cả ứng dụng (ví dụ "bạn là trợ lý trích đơn hàng"). *Messages* là phần nội dung thay đổi theo từng lần (ví dụ một tin nhắn của khách). Cả Anthropic và OpenAI đều tách chỉ dẫn cấp ứng dụng (system/developer) khỏi nội dung người dùng; OpenAI mô tả developer message là nơi "provide the system's rules and business logic" **[Nguồn: OpenAI prompt engineering guide]**.
2. **Chi phí tính theo token**, tách đầu vào và đầu ra, thường đơn giá đầu ra cao hơn. Có đơn giá riêng cho phần đọc từ bộ nhớ đệm (cache, tức là phần AI đã đọc trước đó và được lưu tạm để đọc lại rẻ hơn). Có mức giá Batch cho việc không cần trả lời ngay (gửi cả mẻ rồi chờ kết quả sau). Cả hai trang giá đều ghi theo "1M tokens"/"MTok", đơn vị USD, có cột input, cached input, output **[Nguồn: trang giá OpenAI và Claude, truy cập 2026-11-11]**. Anthropic ghi Message Batches API giảm 50% chi phí **[Nguồn: Claude API overview]**.
3. **Token không phải từ.** Cùng một văn bản có thể ra số token khác nhau giữa các họ mô hình. Anthropic ghi các model từ Opus 4.7 trở đi dùng tokenizer mới (bộ cắt chữ thành token), cùng văn bản ra khoảng 30% nhiều token hơn mô hình trước, và dặn đếm lại theo đúng model sẽ dùng **[Nguồn: Claude token counting]**. Tiếng Việt có dấu thường tốn nhiều token hơn tiếng Anh cùng nghĩa; **[Đề xuất]** đo trên chính dữ liệu của bạn, đừng suy từ tiếng Anh.
4. **Đầu ra cấu trúc không bảo đảm tuyệt đối.** Nhà cung cấp dùng giải mã ràng buộc (ép AI chỉ được viết ra chuỗi đúng khuôn) để ra JSON đúng lược đồ (schema, tức là bản mô tả các ô dữ liệu mà bạn muốn), nhưng vẫn có ngoại lệ: AI từ chối trả lời (refusal), hoặc câu trả lời bị cắt giữa chừng do hết `max_tokens` (mức trần số token được phép viết ra) **[Nguồn: Claude structured outputs; OpenAI structured outputs]**. Luôn kiểm bằng code và có nhánh xử lý.
5. **Giới hạn tốc độ và hạn mức chi là hai thứ khác nhau** (mục 3.4).
6. **Khóa API là mật khẩu trả tiền.** Ai có khóa là tiêu tiền của bạn.

!!! tip "Nói đơn giản"
    Mỗi lần gọi AI giống như gửi một lá thư gồm hai phần: "quy định chung" (system prompt) và "nội dung lần này" (messages). Nhà cung cấp tính tiền theo số chữ gửi đi và số chữ nhận về, chứ không tính theo số lần gọi. Và chiếc khóa API chính là thẻ thanh toán gắn với tài khoản của bạn, nên phải cất kỹ như thẻ ngân hàng.

### 3.2 Công thức tự tính chi phí

Đoạn dưới đây không phải mã chạy thật, mà là hai công thức tính tiền viết theo kiểu chương trình. Dòng đầu tính tiền cho một lần gọi: lấy số token vào nhân đơn giá vào, cộng số token ra nhân đơn giá ra, rồi chia cho một triệu (vì nhà cung cấp báo giá theo mỗi triệu token). Dòng sau nhân ra tiền một tháng.

```
chi_phi_1_lan = (token_vao x don_gia_vao + token_ra x don_gia_ra) / 1_000_000
chi_phi_thang = chi_phi_1_lan x so_lan_moi_ngay x so_ngay
```
Có cache: thêm `token_doc_cache x don_gia_cache_doc` và `token_ghi_cache x don_gia_ghi_cache` (Claude còn phân biệt ghi cache 5 phút và 1 giờ) **[Nguồn: trang giá Claude]**.

Cách làm:
1. Lấy `usage` (bảng thống kê token mà AI trả về kèm câu trả lời) từ phản hồi thật (token vào/ra) của 20-50 ca thử.
2. Lấy đơn giá từ trang giá chính thức **vào ngày chạy**, ghi ngày vào file cấu hình.
3. Nhân, lấy trung bình và mức xấu nhất (percentile 95, tức là mức mà 95 lần trên 100 lần chạy không vượt quá).
4. Nhân hệ số dự phòng cho lần thử lại **[Đề xuất: bắt đầu từ 1,2]**.
5. Với Claude, có endpoint (một địa chỉ nhận yêu cầu trên máy chủ của nhà cung cấp) đếm token **miễn phí** trước khi gửi (`messages/count_tokens`, có rate limit riêng; con số là ước lượng, có thể lệch chút) **[Nguồn: Claude token counting]**.

!!! tip "Nói đơn giản"
    Muốn biết một tháng tốn bao nhiêu, bạn không cần đoán. Chạy thử 20 đến 50 mẫu thật, đọc số token trong kết quả, nhân với đơn giá trên trang giá hôm nay, rồi nhân với số lần chạy mỗi ngày. Cộng thêm một khoản dự phòng vì có lúc phải chạy lại.

### 3.3 Tham số hay gặp (thao tác; kiểm tra 2026-11-11)

Mục này liệt kê những "ô điền" mà chương trình phải gửi cho AI. Bạn không cần nhớ tên từng ô. Chỉ cần biết mỗi nhà cung cấp có cách đặt tên riêng, và nhờ người biết code đối chiếu với tài liệu chính thức.

- **Claude Messages API** `POST https://api.anthropic.com/v1/messages`, header `x-api-key` (hoặc `Authorization: Bearer`), `anthropic-version`, `content-type: application/json`; SDK tự gửi các header này **[Nguồn: Claude API overview]**. Trường chính: `model`, `max_tokens`, `system`, `messages`. Phản hồi có `usage` và header `request-id`. (Header là phần "phong bì" của yêu cầu, chứa thông tin như khóa và phiên bản. SDK là bộ thư viện do nhà cung cấp viết sẵn để gọi API đỡ phải làm thủ công. `request-id` là mã số của từng lần gọi, giống số vận đơn.)
- **Lưu ý đổi nhanh:** tài liệu lỗi Claude ghi một số model mới không còn hỗ trợ prefill tin nhắn assistant (viết sẵn phần mở đầu câu trả lời cho AI viết tiếp), hoặc không cho đặt `thinking` ở một số kiểu (chế độ cho AI "suy nghĩ" trước khi trả lời), trả 400 **[Nguồn: Claude errors, 2026-11-11]**. Nghĩa là mẹo prompt cũ có thể hỏng khi đổi model. **[Đề xuất]** Ghim (pin) tên model trong cấu hình (tức là ghi cố định một tên model, không để tự đổi) và chạy lại ca thử khi đổi; OpenAI cũng khuyến nghị ghim snapshot **[Nguồn: OpenAI prompt guide]**.
- **OpenAI** (Responses API): structured output đặt ở `text.format` với `type: "json_schema"`, `name`, `schema`, `strict: true`; SDK Python có `client.responses.parse(..., text_format=<Pydantic>)` và trả `output_parsed` **[Nguồn: OpenAI structured outputs]**. (Pydantic là thư viện Python dùng để khai báo khung dữ liệu và kiểm dữ liệu có đúng khung hay không.)
- **Claude structured outputs:** `output_config.format = {type: "json_schema", schema: {...}}` hoặc `client.messages.parse(..., output_format=<Pydantic>)`; lược đồ nên có `additionalProperties: false`; không hỗ trợ đệ quy, `minimum/maximum`, `minLength/maxLength`...; lần đầu với lược đồ mới chậm hơn **[Nguồn: Claude structured outputs]**. Tham số cũ `output_format` ở mức API thô đã bị đánh dấu deprecated (nghĩa là sắp bỏ, không nên dùng nữa) **[Nguồn: cùng trang]**.

!!! tip "Nói đơn giản"
    Tên các "ô điền" và model đổi thường xuyên. Vì vậy hãy ghi rõ ngày kiểm tra, ghim tên model trong file cấu hình, và mỗi lần đổi model thì chạy lại bộ ca thử. Đừng tin rằng cách làm hôm nay vẫn chạy được sau vài tháng.

### 3.4 Rate limit và hạn mức chi

*Rate limit* (giới hạn tốc độ) là mức trần số yêu cầu hoặc số token mà bạn được gửi trong mỗi phút. *Hạn mức chi* là số tiền tối đa bạn được tiêu. Hai thứ này khác nhau.

- Rate limit Claude đo bằng RPM (số yêu cầu mỗi phút), ITPM (token vào mỗi phút), OTPM (token ra mỗi phút) theo từng nhóm model. Vượt thì trả 429 (mã lỗi nghĩa là "bạn gọi quá nhiều, chờ chút") kèm header `retry-after` (cho biết nên chờ bao lâu). Thuật toán là token bucket (dung lượng hồi liên tục, không reset theo giờ tròn; có thể hình dung như một cái xô được rót đầy dần, mỗi lần gọi là múc bớt ra). ITPM chỉ tính token đầu vào chưa cache, nên cache giúp tăng thông lượng **[Nguồn: Claude rate limits]**.
- Anthropic có **hạn mức chi theo tháng theo bậc (tier)** và bạn có thể tự đặt hạn mức thấp hơn trong Console (trang quản trị trên web của nhà cung cấp). Chạm hạn mức tự đặt thì trả 400. Chạm trần của bậc thì trả 429 **không có** `retry-after` và thử lại vô ích tới khi sang tháng hoặc nâng bậc **[Nguồn: Claude rate limits; errors]**. (Con số bậc có trong trang nguồn nhưng thay đổi, không chép vào đây.)
- OpenAI: giới hạn RPM, RPD, TPM, TPD...; cái nào chạm trước thì bị chặn; áp theo tổ chức và project; header `Retry-After`; mã 429 `slow_down` và 503 `server_is_overloaded` đều nên thử lại có lùi dần (chờ lâu hơn sau mỗi lần thất bại); **không** thử lại lỗi hạn mức/thanh toán; quy tắc ngón tay cái: khi đạt 1 triệu token vào/phút, tăng lưu lượng không quá 50% mỗi 15 phút **[Nguồn: OpenAI rate limits]**.

!!! tip "Nói đơn giản"
    Hãy nghĩ tới đường cao tốc. Giới hạn tốc độ là biển báo "chạy chậm lại, đợi một lát rồi đi tiếp", nên chờ là xong. Hạn mức chi là hết tiền trong ví, và chờ đợi cũng vô ích cho đến khi bạn nạp thêm hoặc sang tháng mới. Phải biết phân biệt hai loại lỗi này, vì cách xử lý ngược nhau.

### 3.5 Xử lý lỗi (Claude, theo tài liệu)

Khi gọi API, mỗi kết quả kèm một mã số cho biết thành công hay thất bại. Danh sách dưới đây chỉ để bạn biết mã nào là lỗi do mình (không thử lại được), mã nào là lỗi tạm thời (thử lại được).

400 `invalid_request_error` (cũng dùng khi chạm hạn mức tự đặt); 401 xác thực; 402 thanh toán; 403 quyền; 404; 413 quá lớn; 429 rate limit; 500 lỗi nội bộ (thử lại, lùi dần); 504 timeout; 529 quá tải. SDK chính thức tự thử lại lỗi tạm thời 2 lần mặc định, tôn trọng `retry-after` **[Nguồn: Claude errors]**. Mỗi phản hồi có `request-id`: ghi vào nhật ký để hỏi hỗ trợ. Việc dài (hơn 10 phút) nên dùng streaming (nhận câu trả lời từng đoạn một khi AI đang viết, thay vì chờ xong hết) hoặc Batch.

OpenAI khuyến cáo: giới hạn số lần thử và tổng thời gian; nếu tự thử lại thì tắt thử lại của SDK hoặc tính vào hạn mức để khỏi nhân đôi số yêu cầu; thất bại vẫn tính vào giới hạn theo phút **[Nguồn: OpenAI rate limits]**.

!!! tip "Nói đơn giản"
    Lỗi chia làm hai nhóm. Nhóm "lỗi của mình" (sai khóa, sai yêu cầu, hết tiền) thì thử lại bao nhiêu lần cũng vô ích, phải sửa. Nhóm "lỗi tạm thời" (máy chủ bận, gọi quá nhanh) thì chờ một lát rồi thử lại, và mỗi lần chờ lâu hơn một chút.

### 3.6 Giữ khóa API an toàn

OpenAI khuyến nghị: dùng khóa theo project hoặc service account (tài khoản dành riêng cho chương trình) chứ không dùng khóa cá nhân; không để khóa trong mã hoặc kho công khai, dùng biến môi trường (một chỗ trên máy để cất giá trị bí mật, tách khỏi mã) hoặc dịch vụ quản lý bí mật; đặt hạn dùng và xoay khóa (đổi khóa mới định kỳ); tách project staging (chạy thử) và production (chạy thật); đặt cảnh báo và hạn mức chi **[Nguồn: OpenAI production best practices]**. Claude: tài liệu cho tạo khóa theo workspace và đặt hạn dùng khi tạo; workspace để tách môi trường và kiểm soát chi **[Nguồn: Claude API overview]**. Yêu cầu từ trình duyệt có thể bị từ chối với một số tổ chức, hãy gọi từ máy chủ của bạn **[Nguồn: Claude errors]**.

!!! tip "Nói đơn giản"
    Đừng bao giờ gửi khóa qua Zalo hay email, và đừng dán nó vào file mã. Mỗi ứng dụng một khóa riêng, mỗi khóa có hạn mức chi riêng. Nhờ vậy nếu khóa bị lộ, thiệt hại có trần và bạn biết ngay khóa nào cần thay.

## 4. Chuỗi bài nhỏ

### Bài C1.1: Tạo tài khoản API và khóa an toàn
- **Mục tiêu:** có khóa riêng, hạn mức thấp, không lộ.
- **Việc cần làm:**
  1. Tạo tổ chức/project bằng email công ty, không dùng tài khoản cá nhân của nhân viên.
  2. Nạp số tiền nhỏ; đặt hạn mức chi tháng thấp (ví dụ vài chục USD **[Đề xuất]**) và cảnh báo.
  3. Tạo khóa riêng cho từng ứng dụng; đặt hạn dùng nếu có.
  4. Lưu khóa trong biến môi trường (`ANTHROPIC_API_KEY`/`OPENAI_API_KEY`) hoặc file `.env`; thêm `.env` vào `.gitignore`. (`.env` là file văn bản nhỏ chứa các giá trị bí mật. `.gitignore` là danh sách file mà công cụ quản lý mã nguồn Git sẽ bỏ qua, để file đó không bị đưa lên kho mã.)
  5. Cài trình quét bí mật trước khi commit **[Đề xuất]** (commit là bước lưu một phiên bản mã vào Git; trình quét bí mật sẽ báo nếu bạn lỡ để khóa trong mã).
- **Bạn có sau bài:** khóa + `.env` + file `.gitignore` + ghi chú ai giữ khóa, xoay khi nào.
- **Lỗi thường gặp:** dán khóa vào Zalo/email; commit lên GitHub; một khóa dùng chung cho mọi người; không đặt hạn mức nên vòng lặp lỗi đốt tiền.

### Bài C1.2: Một lệnh gọi đầu tiên và đọc `usage`
- **Mục tiêu:** gửi prompt C0 qua API, in token vào/ra.
- **Việc cần làm:** xem mẫu 6.1. Chạy cùng đầu vào 3 lần; so sánh đầu ra và `usage`.
- **Bạn có sau bài:** script 20 dòng + file prompt tách riêng.
- **Lỗi thường gặp:** `max_tokens` quá thấp nên cắt giữa câu (`stop_reason`, tức là lý do AI dừng viết, khác kết thúc bình thường); nhồi dữ liệu vào chuỗi code thay vì file.

### Bài C1.3: System prompt và ghép dữ liệu đầu vào
- **Mục tiêu:** phần cố định vào `system`, phần đổi vào `messages`.
- **Việc cần làm:** chuyển 3 phần đầu của khung 6 phần (vai trò, bối cảnh, ràng buộc) vào system; tài liệu cần xử lý đặt trong thẻ rõ ràng (ví dụ `<tai_lieu>...</tai_lieu>`); dữ liệu dài đặt gần cuối prompt (OpenAI khuyên đặt context ở cuối **[Nguồn]**). Chống "tiêm lệnh" (prompt injection: kẻ xấu nhét câu lệnh vào tài liệu để AI làm theo): dặn rằng nội dung trong thẻ là dữ liệu, không phải chỉ thị **[Đề xuất]**.
- **Bạn có sau bài:** file prompt có phiên bản.
- **Lỗi thường gặp:** để người dùng cuối sửa trực tiếp system prompt; tài liệu chứa lệnh ("bỏ qua hướng dẫn trên") làm lệch hành vi.

### Bài C1.4: Đầu ra JSON có cấu trúc + kiểm tra
- **Mục tiêu:** đầu ra đưa thẳng vào Excel/CSV.
- **Việc cần làm:** định nghĩa lược đồ (Pydantic hoặc JSON Schema) với ít trường, kiểu rõ, `enum` cho trường phân loại (enum là danh sách đáp án cố định, ví dụ chỉ được chọn "khen", "chê" hoặc "hỏi giá"); gọi với structured output; kiểm `stop_reason`/trạng thái (từ chối, cắt); kiểm lại bằng code (kiểu, miền giá trị, khớp danh mục); ca không đạt thì ghi vào hàng "cần người xem".
- **Bạn có sau bài:** `schema.py` + CSV đầu ra + cột `hop_le`.
- **Lỗi thường gặp:** lược đồ dùng tính năng không hỗ trợ (ví dụ giới hạn độ dài/giá trị) nên bị 400; tin JSON "đúng cú pháp" là "đúng nội dung" (đúng cấu trúc không có nghĩa đúng sự thật).

### Bài C1.5: Ước tính và theo dõi chi phí
- **Mục tiêu:** biết giá một lần chạy, một tháng.
- **Việc cần làm:** dùng công thức 3.2; ghi mỗi lần gọi: thời gian, `request-id`, token vào/ra, chi phí ước tính; cuối ngày cộng và so với trang Usage của nhà cung cấp; sai lệch lớn thì tìm nguyên nhân (cache, thử lại, tokenizer).
- **Bạn có sau bài:** `cost.py` + bảng chi phí theo nghiệp vụ.
- **Lỗi thường gặp:** quên token đầu ra; quên tính lần thử lại; dùng đơn giá cũ; đếm token bằng model khác.

### Bài C1.6: Xử lý lỗi, thử lại, giới hạn tốc độ
- **Mục tiêu:** 500 yêu cầu chạy xong dù có 429/5xx. (5xx là cách gọi chung các mã lỗi bắt đầu bằng số 5, tức lỗi từ phía máy chủ.)
- **Việc cần làm:** dùng thử lại có lùi dần + ngẫu nhiên (mỗi lần chờ lâu hơn và lệch nhau một chút, để các yêu cầu không dồn cùng lúc), tôn trọng `retry-after`; giới hạn số lần và tổng thời gian; phân biệt lỗi **không** thử lại (400, 401, 402, 403, trần chi 429 không có `retry-after`); chạy tuần tự hoặc song song nhỏ; ghi mã yêu cầu thất bại để chạy lại phần thiếu; việc không gấp thì dùng Batch (giảm 50% theo Claude) **[Nguồn]**.
- **Bạn có sau bài:** hàm `goi_co_thu_lai()`; file `that_bai.csv`.
- **Lỗi thường gặp:** vòng lặp thử lại vô hạn; thử lại cả lỗi 400 (tốn tiền, không bao giờ qua); song song quá nhiều khiến 429 dày hơn.

### Bài C1.7: Đưa vào nhịp làm việc (đóng gói tối thiểu)
- **Mục tiêu:** người không phải tác giả chạy được.
- **Việc cần làm:** `README` 10 dòng (file hướng dẫn ngắn nằm cạnh mã); một lệnh chạy; chạy bộ ca thử tự động trước mỗi lần đổi prompt/model; người duyệt xem CSV.
- **Bạn có sau bài:** thư mục dự án + README + lịch duyệt.
- **Lỗi thường gặp:** chỉ một người hiểu script; đổi model mà không chạy lại ca thử.

## 5. Đường không code vs đường có code, khi nào buộc phải chuyển

- **Vẫn ở không code nếu:** khối lượng nhỏ (vài việc/ngày), đầu ra do người đọc và dùng ngay, không cần nhật ký.
- **Buộc sang code (C1) khi:** hàng loạt; cần JSON/CSV; cần nhật ký và chi phí theo việc; cần chạy theo lịch **[Đề xuất]**.
- **Có đường trung gian ít code (chưa kiểm chứng):** công cụ tự động hóa nối bảng tính với API (kiểu no-code, tức là kéo thả cấu hình, không viết code). Chưa đọc tài liệu nào nên không khuyến nghị cụ thể; xem mục 9.
- **Không nên chuyển nếu** chưa có quy tắc dữ liệu và chưa có người duyệt.

## 6. Mã mẫu ngắn

Hai đoạn mã dưới đây là ví dụ cho người biết lập trình. Nếu bạn không viết code, bạn **không cần đọc hiểu từng dòng**. Chỉ cần biết mỗi đoạn làm gì, rồi nhờ người biết code (hoặc nhờ AI) chạy giúp và điều chỉnh cho đúng nghiệp vụ của bạn.

### 6.1 Một lệnh gọi + JSON có cấu trúc (Claude, Python)
**Trạng thái: CHƯA chạy thử với API thật** (không có khóa trong phiên soạn). Tên tham số lấy từ tài liệu chính thức đã đọc 2026-11-11; tên model để biến cấu hình (đừng chép cứng), hãy lấy từ trang models của nhà cung cấp.

**Đoạn mã dưới đây làm gì?** Nó gửi cho Claude một tin nhắn đặt hàng ("Chị Lan lấy 3 hộp trà nhé") kèm chỉ dẫn "hãy trích tên khách, sản phẩm, số lượng". Claude trả về đúng bốn ô: tên khách, sản phẩm, số lượng, và một ô đánh dấu "cần người xem" (bật lên nếu thông tin thiếu hoặc mơ hồ). Cuối cùng chương trình in ra kết quả cùng số token đã dùng. Lưu ý đoạn mã này chưa được chạy thử với API thật.

```python
import os
from anthropic import Anthropic          # pip install anthropic pydantic
from pydantic import BaseModel

class DonHang(BaseModel):
    ten_khach: str
    san_pham: str
    so_luong: int
    can_nguoi_xem: bool                  # True nếu thiếu/mơ hồ

client = Anthropic()                     # đọc ANTHROPIC_API_KEY từ môi trường
MODEL = os.environ["MODEL_ID"]           # ghim trong cấu hình, ghi ngày kiểm tra

resp = client.messages.parse(
    model=MODEL,
    max_tokens=1024,
    system="Bạn trích thông tin đơn hàng từ tin nhắn. Nếu thiếu thông tin thì đặt can_nguoi_xem=true, không tự đoán.",
    messages=[{"role": "user", "content": "<tin_nhan>Chị Lan lấy 3 hộp trà nhé</tin_nhan>"}],
    output_format=DonHang,
)
print(resp.parsed_output)
u = resp.usage                           # token vào/ra để tính chi phí
print(u.input_tokens, u.output_tokens, resp._request_id)
```

!!! tip "Nói đơn giản"
    Ví dụ này giống việc nhờ một nhân viên đọc tin nhắn của khách và điền vào một phiếu có bốn ô cố định, kèm dặn "ô nào không chắc thì đánh dấu để người khác xem, đừng tự đoán".
### 6.2 Tính chi phí và thử lại (đã chạy thử logic, không gọi mạng)
**Trạng thái: ĐÃ chạy thử** phần tính chi phí và vòng thử lại bằng lỗi giả (Python, kiểm tra bằng `assert`, 2026-11-11). Đơn giá trong mã là số giả định để kiểm thử; hãy thay bằng đơn giá đọc từ trang giá.

**Đoạn mã dưới đây làm gì?** Hàm đầu tiên tính tiền một lần gọi từ số token vào và ra (dùng đơn giá giả định để thử). Hàm thứ hai là cơ chế thử lại: nếu gọi thất bại thì chờ một lúc rồi gọi lại, mỗi lần chờ lâu hơn, và dừng sau tối đa 5 lần. Bạn không cần đọc từng dòng; hãy nhờ người biết code ghép nó vào script của bạn.

```python
import time, random
P_IN, P_OUT = 1.0, 5.0   # USD / 1M token: GIẢ ĐỊNH, thay bằng giá chính thức + ghi ngày

def cost_usd(tok_in, tok_out, p_in=P_IN, p_out=P_OUT):
    return tok_in / 1e6 * p_in + tok_out / 1e6 * p_out

def call_with_retry(fn, max_tries=5, base=1.0, cap=30.0):
    for i in range(max_tries):
        try:
            return fn()
        except RuntimeError:                     # thay bằng lỗi 429/5xx của SDK
            if i == max_tries - 1:
                raise
            time.sleep(min(cap, base * 2 ** i) * random.uniform(0.5, 1.0))
```
Lưu ý: SDK chính thức đã tự thử lại; chỉ tự viết thêm khi cần kiểm soát và khi đó nên tắt hoặc tính cả thử lại của SDK (xem mục 3.5).

## 7. Tiêu chí lên cấp tiếp theo (C1 -> C2) [Đề xuất]

Lên C2 (tài liệu thành text có cấu trúc) khi:
1. >= 1 nghiệp vụ chạy bằng script >= 4 tuần liên tục, có nhật ký đủ token, chi phí, `request-id`.
2. Tỷ lệ đầu ra JSON hợp lệ >= 98% sau kiểm bằng code (ngưỡng đề xuất).
3. Chi phí thực tế lệch dự báo không quá 20%.
4. Sai sót lớn nhất đến từ **đầu vào** (PDF/ảnh/Word lộn xộn, bảng vỡ), không phải từ prompt. Đây là dấu hiệu cần C2.
5. Có người sở hữu khóa, đã thử xoay khóa ít nhất một lần.

## 8. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống dưới đây là ví dụ minh họa để bạn dễ hình dung, không phải số đo thật.

- **Bán lẻ:** từ 300 tin nhắn đặt hàng Zalo/Facebook đã ẩn danh, trích (sản phẩm, số lượng, địa chỉ rút gọn đến cấp quận) vào CSV; dòng `can_nguoi_xem=true` chuyển người.
- **Kế toán:** phân loại diễn giải sao kê vào danh mục chi phí theo `enum` cố định; mọi dòng độ tin thấp chuyển kế toán duyệt; không gửi số tài khoản/tên chủ tài khoản (ẩn danh bằng mã).
- **Dịch vụ:** gán nhãn (khen/chê/hỏi giá) cho đánh giá khách; báo cáo đếm nhãn theo tuần.
- Chi phí: dùng công thức 3.2 trên 50 mẫu thật rồi nhân ra tháng.

## 9. Tài liệu tham khảo

Truy cập tất cả: 2026-11-11. Tin cậy: Cao = tài liệu chính thức của nhà cung cấp.

| Tiêu đề | URL | Loại | Tin cậy |
|---|---|---|---|
| Claude API overview | https://platform.claude.com/docs/en/api/overview | Tài liệu nhà cung cấp | Cao |
| Claude API errors | https://platform.claude.com/docs/en/api/errors | Tài liệu nhà cung cấp | Cao |
| Claude rate limits | https://platform.claude.com/docs/en/api/rate-limits | Tài liệu nhà cung cấp | Cao |
| Claude structured outputs | https://platform.claude.com/docs/en/build-with-claude/structured-outputs | Tài liệu nhà cung cấp | Cao (phần cuối trang chưa đọc, xem mục 10) |
| Claude token counting | https://platform.claude.com/docs/en/build-with-claude/token-counting | Tài liệu nhà cung cấp | Cao |
| Claude pricing (xem để lấy giá, không chép số) | https://platform.claude.com/docs/en/about-claude/pricing | Trang giá chính thức | Cao |
| OpenAI pricing (xem để lấy giá, không chép số) | https://developers.openai.com/api/docs/pricing | Trang giá chính thức | Cao |
| OpenAI structured outputs | https://developers.openai.com/api/docs/guides/structured-outputs | Tài liệu nhà cung cấp | Cao (đọc tối đa 100.000 ký tự đầu) |
| OpenAI rate limits | https://developers.openai.com/api/docs/guides/rate-limits | Tài liệu nhà cung cấp | Cao |
| OpenAI production best practices | https://developers.openai.com/api/docs/guides/production-best-practices | Tài liệu nhà cung cấp | Cao |
| OpenAI prompt engineering | https://developers.openai.com/api/docs/guides/prompt-engineering | Tài liệu nhà cung cấp | Cao |
| Gemini API pricing | https://ai.google.dev/gemini-api/docs/pricing (chuyển hướng sang aistudio.google.com/docs/pricing) | Trang giá chính thức | Chưa đọc nội dung, chỉ thấy chuyển hướng |

## 10. Chưa kiểm chứng / cần kiểm tra lại

- Mã mẫu 6.1 **chưa chạy với API thật**; tên model, kiểu `usage` và `_request_id` cần thử khi có khóa.
- Cách gọi Gemini API (tham số, structured output, rate limit): **chưa đọc**; file này chỉ nói sâu Claude và OpenAI.
- Phần cuối trang structured outputs của Claude và OpenAI (danh sách đầy đủ giới hạn lược đồ) chưa đọc hết.
- Giá cụ thể: cố ý không ghi. Trang giá hiện có nhiều tầng (Standard/Batch/Flex, khuyến mãi theo ngày, phụ phí vùng) nên phải đọc lại ngày chạy.
- Chi phí token của tiếng Việt so với tiếng Anh: chưa có nguồn, hãy tự đo.
- Ngưỡng 98%, 20%, 4 tuần, hệ số 1,2, mức hạn mức vài chục USD: đề xuất của chúng tôi.
- Công cụ no-code nối API: chưa tìm hiểu.
