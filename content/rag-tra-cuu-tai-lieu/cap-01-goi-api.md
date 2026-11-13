# Cấp 1 (C1): Gọi AI qua API

> Ngày soạn: 2026-11-11. Nguyên tắc (bền) tách khỏi thao tác/tên tham số/model (hay đổi, có ghi ngày).
> **[Nguồn]** = đọc được trong tài liệu chính thức; **[Đề xuất]** = của chúng tôi.
> Không đưa giá cụ thể: chỉ nêu cách tính. Muốn con số, mở trang giá chính thức tại thời điểm dùng (mục 8).
> Không phải tư vấn pháp lý; xem `../an-toan-du-lieu-va-phap-ly-vn.md` trước khi gửi dữ liệu khách hàng qua API.

## 1. Mục tiêu và người đọc

**Người đọc:** người có thể viết/đọc Python cơ bản trong SME (IT kiêm nhiệm, kế toán biết Excel nâng cao, freelancer), hoặc chủ SME muốn hiểu để giao việc.

**Mục tiêu:** sau cấp này, từ một nghiệp vụ C0 đã có prompt + ca thử, bạn chạy được nó bằng script: một lệnh gọi, đầu ra có cấu trúc (JSON), biết **mỗi lần chạy tốn bao nhiêu token và tiền**, xử lý lỗi/giới hạn tốc độ, và giữ khóa API an toàn.

**Sản phẩm cầm đi được:** một script `run.py` + một file `prompts/<nghiep_vu>.md` + file CSV nhật ký (thời gian, mã yêu cầu, token vào/ra, chi phí ước tính, kết quả hợp lệ/không) + một khóa API riêng có hạn mức chi.

## 2. Câu hỏi cấp này trả lời / lỗi của C0

Lỗi của C0 dẫn tới C1: không chạy hàng loạt được; khó ghi nhật ký; đầu ra văn bản tự do khó đưa vào bảng tính; không tính được chi phí theo việc; mỗi người dán dữ liệu vào tài khoản cá nhân. Câu hỏi: *"Làm sao chạy cùng một việc 500 lần, ra đúng cấu trúc, biết tốn bao nhiêu, và lỗi thì xử lý ra sao?"*

## 3. Kiến thức nền

### 3.1 Nguyên tắc (bền)

1. **Một lệnh gọi = (system prompt + messages) vào, (văn bản + thông tin sử dụng) ra.** Cả Anthropic và OpenAI đều tách chỉ dẫn cấp ứng dụng (system/developer) khỏi nội dung người dùng; OpenAI mô tả developer message là nơi "provide the system's rules and business logic" **[Nguồn: OpenAI prompt engineering guide]**.
2. **Chi phí tính theo token**, tách đầu vào và đầu ra, thường đơn giá đầu ra cao hơn; có đơn giá riêng cho phần đọc từ bộ nhớ đệm (cache) và có mức giá Batch cho việc không cần trả lời ngay. Cả hai trang giá đều ghi theo "1M tokens"/"MTok", đơn vị USD, có cột input, cached input, output **[Nguồn: trang giá OpenAI và Claude, truy cập 2026-11-11]**. Anthropic ghi Message Batches API giảm 50% chi phí **[Nguồn: Claude API overview]**.
3. **Token không phải từ.** Cùng một văn bản có thể ra số token khác nhau giữa các họ mô hình; Anthropic ghi các model từ Opus 4.7 trở đi dùng tokenizer mới, cùng văn bản ra khoảng 30% nhiều token hơn mô hình trước, và dặn đếm lại theo đúng model sẽ dùng **[Nguồn: Claude token counting]**. Tiếng Việt có dấu thường tốn nhiều token hơn tiếng Anh cùng nghĩa; **[Đề xuất]** đo trên chính dữ liệu của bạn, đừng suy từ tiếng Anh.
4. **Đầu ra cấu trúc không bảo đảm tuyệt đối.** Nhà cung cấp dùng giải mã ràng buộc để ra JSON đúng lược đồ, nhưng vẫn có ngoại lệ: từ chối (refusal), bị cắt do hết `max_tokens` **[Nguồn: Claude structured outputs; OpenAI structured outputs]**. Luôn kiểm bằng code và có nhánh xử lý.
5. **Giới hạn tốc độ và hạn mức chi là hai thứ khác nhau** (mục 3.4).
6. **Khóa API là mật khẩu trả tiền.** Ai có khóa là tiêu tiền của bạn.

### 3.2 Công thức tự tính chi phí

```
chi_phi_1_lan = (token_vao x don_gia_vao + token_ra x don_gia_ra) / 1_000_000
chi_phi_thang = chi_phi_1_lan x so_lan_moi_ngay x so_ngay
```
Có cache: thêm `token_doc_cache x don_gia_cache_doc` và `token_ghi_cache x don_gia_ghi_cache` (Claude còn phân biệt ghi cache 5 phút và 1 giờ) **[Nguồn: trang giá Claude]**.

Cách làm:
1. Lấy `usage` từ phản hồi thật (token vào/ra) của 20-50 ca thử.
2. Lấy đơn giá từ trang giá chính thức **vào ngày chạy**, ghi ngày vào file cấu hình.
3. Nhân, lấy trung bình và mức xấu nhất (percentile 95).
4. Nhân hệ số dự phòng cho lần thử lại **[Đề xuất: bắt đầu từ 1,2]**.
5. Với Claude, có endpoint đếm token **miễn phí** trước khi gửi (`messages/count_tokens`, có rate limit riêng; con số là ước lượng, có thể lệch chút) **[Nguồn: Claude token counting]**.

### 3.3 Tham số hay gặp (thao tác; kiểm tra 2026-11-11)

- **Claude Messages API** `POST https://api.anthropic.com/v1/messages`, header `x-api-key` (hoặc `Authorization: Bearer`), `anthropic-version`, `content-type: application/json`; SDK tự gửi các header này **[Nguồn: Claude API overview]**. Trường chính: `model`, `max_tokens`, `system`, `messages`. Phản hồi có `usage` và header `request-id`.
- **Lưu ý đổi nhanh:** tài liệu lỗi Claude ghi một số model mới không còn hỗ trợ prefill tin nhắn assistant, hoặc không cho đặt `thinking` ở một số kiểu, trả 400 **[Nguồn: Claude errors, 2026-11-11]**. Nghĩa là mẹo prompt cũ có thể hỏng khi đổi model. **[Đề xuất]** Ghim (pin) tên model trong cấu hình và chạy lại ca thử khi đổi; OpenAI cũng khuyến nghị ghim snapshot **[Nguồn: OpenAI prompt guide]**.
- **OpenAI** (Responses API): structured output đặt ở `text.format` với `type: "json_schema"`, `name`, `schema`, `strict: true`; SDK Python có `client.responses.parse(..., text_format=<Pydantic>)` và trả `output_parsed` **[Nguồn: OpenAI structured outputs]**.
- **Claude structured outputs:** `output_config.format = {type: "json_schema", schema: {...}}` hoặc `client.messages.parse(..., output_format=<Pydantic>)`; lược đồ nên có `additionalProperties: false`; không hỗ trợ đệ quy, `minimum/maximum`, `minLength/maxLength`...; lần đầu với lược đồ mới chậm hơn **[Nguồn: Claude structured outputs]**. Tham số cũ `output_format` ở mức API thô đã bị đánh dấu deprecated **[Nguồn: cùng trang]**.

### 3.4 Rate limit và hạn mức chi

- Rate limit Claude đo bằng RPM, ITPM (token vào/phút), OTPM (token ra/phút) theo từng nhóm model; vượt thì trả 429 kèm header `retry-after`; thuật toán token bucket (dung lượng hồi liên tục, không reset theo giờ tròn). ITPM chỉ tính token đầu vào chưa cache, nên cache giúp tăng thông lượng **[Nguồn: Claude rate limits]**.
- Anthropic có **hạn mức chi theo tháng theo bậc (tier)** và bạn có thể tự đặt hạn mức thấp hơn trong Console; chạm hạn mức tự đặt thì trả 400, chạm trần của bậc thì trả 429 **không có** `retry-after` và thử lại vô ích tới khi sang tháng/nâng bậc **[Nguồn: Claude rate limits; errors]**. (Con số bậc có trong trang nguồn nhưng thay đổi, không chép vào đây.)
- OpenAI: giới hạn RPM, RPD, TPM, TPD...; cái nào chạm trước thì bị chặn; áp theo tổ chức và project; header `Retry-After`; mã 429 `slow_down` và 503 `server_is_overloaded` đều nên thử lại có lùi dần; **không** thử lại lỗi hạn mức/thanh toán; quy tắc ngón tay cái: khi đạt 1 triệu token vào/phút, tăng lưu lượng không quá 50% mỗi 15 phút **[Nguồn: OpenAI rate limits]**.

### 3.5 Xử lý lỗi (Claude, theo tài liệu)

400 `invalid_request_error` (cũng dùng khi chạm hạn mức tự đặt); 401 xác thực; 402 thanh toán; 403 quyền; 404; 413 quá lớn; 429 rate limit; 500 lỗi nội bộ (thử lại, lùi dần); 504 timeout; 529 quá tải. SDK chính thức tự thử lại lỗi tạm thời 2 lần mặc định, tôn trọng `retry-after` **[Nguồn: Claude errors]**. Mỗi phản hồi có `request-id`: ghi vào nhật ký để hỏi hỗ trợ. Việc dài (hơn 10 phút) nên dùng streaming hoặc Batch.

OpenAI khuyến cáo: giới hạn số lần thử và tổng thời gian; nếu tự thử lại thì tắt thử lại của SDK hoặc tính vào hạn mức để khỏi nhân đôi số yêu cầu; thất bại vẫn tính vào giới hạn theo phút **[Nguồn: OpenAI rate limits]**.

### 3.6 Giữ khóa API an toàn

OpenAI khuyến nghị: dùng khóa theo project/service account chứ không dùng khóa cá nhân; không để khóa trong mã hoặc kho công khai, dùng biến môi trường hoặc dịch vụ quản lý bí mật; đặt hạn dùng và xoay khóa; tách project staging/production; đặt cảnh báo và hạn mức chi **[Nguồn: OpenAI production best practices]**. Claude: tài liệu cho tạo khóa theo workspace và đặt hạn dùng khi tạo; workspace để tách môi trường và kiểm soát chi **[Nguồn: Claude API overview]**; yêu cầu từ trình duyệt có thể bị từ chối với một số tổ chức, hãy gọi từ máy chủ của bạn **[Nguồn: Claude errors]**.

## 4. Chuỗi bài nhỏ

### Bài C1.1: Tạo tài khoản API và khóa an toàn
- **Mục tiêu:** có khóa riêng, hạn mức thấp, không lộ.
- **Thực hành:** (1) Tạo tổ chức/project bằng email công ty, không dùng tài khoản cá nhân của nhân viên. (2) Nạp số tiền nhỏ; đặt hạn mức chi tháng thấp (ví dụ vài chục USD **[Đề xuất]**) và cảnh báo. (3) Tạo khóa riêng cho từng ứng dụng; đặt hạn dùng nếu có. (4) Lưu khóa trong biến môi trường (`ANTHROPIC_API_KEY`/`OPENAI_API_KEY`) hoặc file `.env`; thêm `.env` vào `.gitignore`. (5) Cài trình quét bí mật trước khi commit **[Đề xuất]**.
- **Sản phẩm:** khóa + `.env` + file `.gitignore` + ghi chú ai giữ khóa, xoay khi nào.
- **Lỗi thường gặp:** dán khóa vào Zalo/email; commit lên GitHub; một khóa dùng chung cho mọi người; không đặt hạn mức nên vòng lặp lỗi đốt tiền.

### Bài C1.2: Một lệnh gọi đầu tiên và đọc `usage`
- **Mục tiêu:** gửi prompt C0 qua API, in token vào/ra.
- **Thực hành:** xem mẫu 6.1. Chạy cùng đầu vào 3 lần; so sánh đầu ra và `usage`.
- **Sản phẩm:** script 20 dòng + file prompt tách riêng.
- **Lỗi thường gặp:** `max_tokens` quá thấp nên cắt giữa câu (`stop_reason` khác kết thúc bình thường); nhồi dữ liệu vào chuỗi code thay vì file.

### Bài C1.3: System prompt và ghép dữ liệu đầu vào
- **Mục tiêu:** phần cố định vào `system`, phần đổi vào `messages`.
- **Thực hành:** chuyển 3 phần đầu của khung 6 phần (vai trò, bối cảnh, ràng buộc) vào system; tài liệu cần xử lý đặt trong thẻ rõ ràng (ví dụ `<tai_lieu>...</tai_lieu>`); dữ liệu dài đặt gần cuối prompt (OpenAI khuyên đặt context ở cuối **[Nguồn]**). Chống "tiêm lệnh": dặn rằng nội dung trong thẻ là dữ liệu, không phải chỉ thị **[Đề xuất]**.
- **Sản phẩm:** file prompt có phiên bản.
- **Lỗi thường gặp:** để người dùng cuối sửa trực tiếp system prompt; tài liệu chứa lệnh ("bỏ qua hướng dẫn trên") làm lệch hành vi.

### Bài C1.4: Đầu ra JSON có cấu trúc + kiểm tra
- **Mục tiêu:** đầu ra đưa thẳng vào Excel/CSV.
- **Thực hành:** định nghĩa lược đồ (Pydantic hoặc JSON Schema) với ít trường, kiểu rõ, `enum` cho trường phân loại; gọi với structured output; kiểm `stop_reason`/trạng thái (từ chối, cắt); kiểm lại bằng code (kiểu, miền giá trị, khớp danh mục); ca không đạt thì ghi vào hàng "cần người xem".
- **Sản phẩm:** `schema.py` + CSV đầu ra + cột `hop_le`.
- **Lỗi thường gặp:** lược đồ dùng tính năng không hỗ trợ (ví dụ giới hạn độ dài/giá trị) nên bị 400; tin JSON "đúng cú pháp" là "đúng nội dung" (đúng cấu trúc không có nghĩa đúng sự thật).

### Bài C1.5: Ước tính và theo dõi chi phí
- **Mục tiêu:** biết giá một lần chạy, một tháng.
- **Thực hành:** dùng công thức 3.2; ghi mỗi lần gọi: thời gian, `request-id`, token vào/ra, chi phí ước tính; cuối ngày cộng và so với trang Usage của nhà cung cấp; sai lệch lớn thì tìm nguyên nhân (cache, thử lại, tokenizer).
- **Sản phẩm:** `cost.py` + bảng chi phí theo nghiệp vụ.
- **Lỗi thường gặp:** quên token đầu ra; quên tính lần thử lại; dùng đơn giá cũ; đếm token bằng model khác.

### Bài C1.6: Xử lý lỗi, thử lại, giới hạn tốc độ
- **Mục tiêu:** 500 yêu cầu chạy xong dù có 429/5xx.
- **Thực hành:** dùng thử lại có lùi dần + ngẫu nhiên, tôn trọng `retry-after`; giới hạn số lần và tổng thời gian; phân biệt lỗi **không** thử lại (400, 401, 402, 403, trần chi 429 không có `retry-after`); chạy tuần tự hoặc song song nhỏ; ghi mã yêu cầu thất bại để chạy lại phần thiếu; việc không gấp thì dùng Batch (giảm 50% theo Claude) **[Nguồn]**.
- **Sản phẩm:** hàm `goi_co_thu_lai()`; file `that_bai.csv`.
- **Lỗi thường gặp:** vòng lặp thử lại vô hạn; thử lại cả lỗi 400 (tốn tiền, không bao giờ qua); song song quá nhiều khiến 429 dày hơn.

### Bài C1.7: Đưa vào nhịp làm việc (đóng gói tối thiểu)
- **Mục tiêu:** người không phải tác giả chạy được.
- **Thực hành:** `README` 10 dòng; một lệnh chạy; chạy bộ ca thử tự động trước mỗi lần đổi prompt/model; người duyệt xem CSV.
- **Sản phẩm:** thư mục dự án + README + lịch duyệt.
- **Lỗi thường gặp:** chỉ một người hiểu script; đổi model mà không chạy lại ca thử.

## 5. Đường không code vs đường có code, khi nào buộc phải chuyển

- **Vẫn ở không code nếu:** khối lượng nhỏ (vài việc/ngày), đầu ra do người đọc và dùng ngay, không cần nhật ký.
- **Buộc sang code (C1) khi:** hàng loạt; cần JSON/CSV; cần nhật ký và chi phí theo việc; cần chạy theo lịch **[Đề xuất]**.
- **Có đường trung gian ít code (chưa kiểm chứng):** công cụ tự động hóa nối bảng tính với API (kiểu no-code). Chưa đọc tài liệu nào nên không khuyến nghị cụ thể; xem mục 9.
- **Không nên chuyển nếu** chưa có quy tắc dữ liệu và chưa có người duyệt.

## 6. Mã mẫu ngắn

### 6.1 Một lệnh gọi + JSON có cấu trúc (Claude, Python)
**Trạng thái: CHƯA chạy thử với API thật** (không có khóa trong phiên soạn). Tên tham số lấy từ tài liệu chính thức đã đọc 2026-11-11; tên model để biến cấu hình (đừng chép cứng), hãy lấy từ trang models của nhà cung cấp.

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

### 6.2 Tính chi phí và thử lại (đã chạy thử logic, không gọi mạng)
**Trạng thái: ĐÃ chạy thử** phần tính chi phí và vòng thử lại bằng lỗi giả (Python, kiểm tra bằng `assert`, 2026-11-11). Đơn giá trong mã là số giả định để kiểm thử; hãy thay bằng đơn giá đọc từ trang giá.

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
