# Cấp 2 (C2): Phân loại ý định và mức khẩn, luật cứng đè lên AI

> Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** / **[Đề xuất]**.
> Dùng lại: gọi API, JSON có cấu trúc, chi phí ở `../rag-tra-cuu-tai-lieu/cap-01-goi-api.md`; mẫu routing ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.2 và bài 8.3.

!!! tip "Tóm tắt nhanh"
    Khi tin nhắn khách đổ về, tin "con tôi ăn bánh bị dị ứng" không thể xếp sau hàng chục tin hỏi size áo. Bài này dạy cách **tự động gắn nhãn** cho mỗi tin: khách muốn gì (ý định), gấp đến đâu (mức khẩn), AI chắc đến đâu (độ tin cậy). Điểm mấu chốt là **luật cứng**: một danh sách cụm từ nguy hiểm do con người đặt ra, chạy trước và có quyền hơn AI. Sau bài, bạn có hàng đợi xếp theo mức khẩn và biết đo xem việc phân loại có đáng tin không.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người phụ trách CSKH (chăm sóc khách hàng) hoặc người biết chút Python/Apps Script (hai ngôn ngữ lập trình thường dùng để viết các đoạn chương trình ngắn) trong SME (doanh nghiệp nhỏ và vừa). Bạn đã học xong cấp C1.

**Bạn cần chuẩn bị:**
- Kết quả của cấp C1 (bài này đi tiếp từ đó).
- Một hộp thư tin nhắn khách thật, để lấy ra 50-100 tin (đã ẩn danh) làm bộ tin thử.
- Một Google Sheet hoặc SQLite (một cơ sở dữ liệu nhỏ, gọn) để làm hàng đợi.
- Nếu muốn đi đường không code, một Project (Claude) hoặc Gem (Gemini); đây là tính năng để bạn lưu sẵn chỉ dẫn cho AI và dùng lại nhiều lần.

**Sau bài này bạn sẽ có:**
1. Mỗi tin khách đến được gắn tự động ba thông tin: `y_dinh` (ý định), `muc_khan` (mức khẩn), `tin_cay` (AI tự báo mình chắc đến đâu). Kết quả viết dưới dạng JSON (một cách ghi dữ liệu có khung rõ ràng để máy đọc được) và được **code kiểm lại**.
2. **Luật cứng** bằng code, chạy trước và đè lên AI cho các ca về an toàn, pháp lý, tiền.
3. Hàng đợi xếp theo mức khẩn; tin loại "khác/không chắc" và khiếu nại đều vào hàng cho người xử lý.
4. Bảng nhầm lẫn (confusion matrix: bảng đếm xem tin thật thuộc loại nào thì bị AI xếp vào loại nào) trên ≥50 tin thật có nhãn.

**Thứ bạn cầm đi được sau bài:** tệp nhãn `nhan-y-dinh-v1.csv`; một prompt phân loại ra JSON; danh sách luật cứng và hàm kiểm; bảng nhầm lẫn kèm ngưỡng tin cậy đã chọn; hàng đợi theo mức khẩn.

## 2. Câu hỏi cấp này trả lời / lỗi của C1

Câu hỏi: *"Tin nào cần người ngay, tin nào AI soạn nháp được?"*

Lỗi ở C1: mọi tin vào một hàng, xếp theo thứ tự đến. Tin "con tôi ăn bánh bị dị ứng" nằm sau 20 tin "còn size M không". Nhân viên cũng phải tự đọc từng tin để biết loại.

## 3. Kiến thức nền

### 3.1 Phân loại là bước routing

**[Nguồn]** Mẫu routing (routing = "định tuyến", tức phân loại đầu vào rồi chuyển tới nơi xử lý phù hợp): phân loại đầu vào rồi chuyển tới xử lý chuyên biệt (Anthropic, "Building effective agents", qua `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.2). **[Nguồn]** Nubank chuyển người khi gặp tình huống ngoài routine, không lấy được dữ liệu, hoặc độ tin cậy thấp (2606.08867, mục 4.5.2); một phiên bản về sau thêm "phát hiện khách bực và chủ động chuyển người" (mục 6.3).

!!! tip "Nói đơn giản"
    Giống người trực tổng đài: nghe vài câu đầu rồi quyết định "chuyển cho bộ phận nào" hoặc "chuyển ngay cho sếp". Phân loại chính là bước nghe vài câu đầu đó.

### 3.2 Sai có giá khác nhau [Đề xuất]

Không phải lỗi nào cũng tốn như nhau. Bảng dưới đây cho thấy từng kiểu nhầm gây hậu quả gì và nên xử lý ra sao.

| Nhầm | Hậu quả | Cách xử lý |
|---|---|---|
| Ca khẩn bị coi là thường | Khách bị bỏ rơi trong ca an toàn/pháp lý | Luật cứng bằng code; đo **recall** của lớp `cao` |
| Ca thường bị coi là khẩn | Người phải xem thêm vài tin | Chấp nhận được |
| Khiếu nại bị coi là hỏi thông tin | AI soạn lời nhẹ nhàng cho khách đang bực | Khiếu nại luôn vào hàng người |
| Ý định đúng nhưng AI không chắc | (để trống) | `tin_cay` dưới ngưỡng → người |

Recall (độ phủ) nghĩa là: trong tất cả các ca khẩn **thật**, hệ thống bắt được bao nhiêu phần. Lớp `cao` là nhóm tin có `muc_khan` ở mức cao. Vì vậy đừng chỉ nhìn độ chính xác chung. Một bộ phân loại "đúng 95%" vẫn có thể bỏ sót phần lớn ca khẩn nếu ca khẩn hiếm.

!!! tip "Nói đơn giản"
    Bỏ sót một ca khẩn tệ hơn nhiều so với báo động nhầm một ca thường. Vì thế ta đo riêng việc "ca khẩn có bị lọt không", thay vì chỉ hỏi "tổng thể đúng bao nhiêu phần".

### 3.3 Tiếng Việt chat: không dấu, viết tắt

- **[Nguồn]** SEATauBench (arXiv 2606.28715; benchmark = bộ bài kiểm tra chuẩn để so sánh các mô hình): khi bản địa hóa toàn bộ sang tiếng Việt (hội thoại, công cụ, chính sách, dữ liệu), pass@1 (tỷ lệ làm đúng ngay lần thử đầu) trung bình là 0,52, so với 0,62 ở bản tiếng Anh (3 mô hình, 3 miền). Khi chỉ đổi ngôn ngữ hội thoại, mức giảm nhỏ hơn. Hiệu năng tiếng Anh dự báo khá tốt chất lượng trung bình nhưng dự báo kém độ ổn định qua nhiều lần chạy. Đây là benchmark dịch từ tiếng Anh, không phải tin nhắn thật của khách Việt.
- **[Đề xuất]** Bộ ca thử phải có tin không dấu, viết tắt ("sp", "e", "ib", "ship cod"), tin nhiều ý trong một câu, và tin chỉ có ảnh.
- **[Đã chạy thử]** Bỏ dấu để so từ khóa giúp bắt tin không dấu, nhưng gây trùng nghĩa: "bong" khớp cả "bỏng" lẫn "bóng đèn", "bông tai". Từ khóa ngắn sau khi bỏ dấu phải thử với câu thật trước khi đưa vào luật cứng.

!!! tip "Nói đơn giản"
    Khách nhắn tin thường không gõ dấu và hay viết tắt. Khi ta bỏ dấu để dò từ khóa, nhiều từ khác nghĩa bỗng giống hệt nhau. Nên mỗi từ khóa ngắn phải được thử trên câu thật trước khi tin dùng.

### 3.4 Luật cứng trước, AI sau

Luật cứng (từ khóa, mẫu) chạy **trước** AI và **thắng** AI. Đầu ra AI sai lược đồ (tức không đúng khung đã quy định, ví dụ thiếu trường hoặc nhãn lạ) thì coi là "không chắc". Đây là hàng rào bằng code: không phụ thuộc mô hình có nghe lời hay không.

!!! tip "Nói đơn giản"
    Bạn có thể dặn AI "gặp ca nguy hiểm thì báo ngay", nhưng AI vẫn có lúc quên. Luật cứng thì không quên, vì nó là một đoạn chương trình chạy trước AI. Nếu luật cứng thấy cụm từ nguy hiểm, kết quả của AI không còn được tính.

## 4. Chuỗi bài nhỏ

### Bài 2.1: Gán nhãn 50-100 tin thật
- **Việc cần làm:** từ hộp thư, lấy 50-100 tin (ẩn danh). Hai người gán `y_dinh`, `muc_khan` độc lập theo định nghĩa C0 (nghĩa là mỗi người tự gán, chưa nhìn kết quả của người kia). Ca lệch thì bàn và ghi lý do.
- **Bạn có sau bài:** `nhan-y-dinh-v1.csv` (tệp bảng tính lưu dạng chữ). Đồng thuận giữa người với người là trần hợp lý cho AI. Xem kappa (một chỉ số đo mức hai người chấm có đồng ý với nhau hay không) ở `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` mục 3.4.

### Bài 2.2: Prompt phân loại ra JSON
- **Việc cần làm:** viết prompt (lời chỉ dẫn gửi cho AI) có định nghĩa từng nhãn, 2 ví dụ mỗi nhãn (lấy từ C0), và yêu cầu chỉ xuất `{"y_dinh":..., "muc_khan":..., "tin_cay":...}`. Dùng structured output (tính năng ép AI trả lời đúng khung) nếu API hỗ trợ (API là cổng để chương trình của bạn nói chuyện với AI; xem `../rag-tra-cuu-tai-lieu/cap-01-goi-api.md` bài C1.4).
- **Không code:** dán 20 tin vào Project/Gem, yêu cầu trả bảng; chép vào Sheet và so với nhãn.

### Bài 2.3: Luật cứng và hàm kiểm
- **Việc cần làm:** viết danh sách cụm buộc chuyển người (an toàn, pháp lý, tiền). Viết hàm kiểm JSON (hàm = một đoạn code làm một việc cụ thể; ở đây là kiểm xem đầu ra của AI có đúng khung không). Ghép thành `dinh_tuyen()` (mục 5).
- **Thử:** 10 tin cố tình viết không dấu, viết tắt, sai chính tả cho từng cụm.

### Bài 2.4: Bảng nhầm lẫn và ngưỡng tin cậy
- **Việc cần làm:** chạy 50-100 tin có nhãn. Lập bảng nhầm lẫn. Tính riêng recall của `muc_khan = cao`. Thử 2-3 ngưỡng `tin_cay` (0,6 / 0,7 / 0,8): đếm số tin chuyển người và số tin sai lọt. (Ngưỡng là mức cắt: tin nào có `tin_cay` thấp hơn mức đó thì chuyển người.)
- **Bạn có sau bài:** bảng nhầm lẫn + ngưỡng đã chọn, kèm lý do.
- **Lỗi hay gặp:** tin `tin_cay` của mô hình như xác suất thật. Nó là số tự khai; chỉ dùng sau khi đã đo trên tin có nhãn.

### Bài 2.5: Hàng đợi theo mức khẩn
- **Việc cần làm:** lập Google Sheet hoặc SQLite với các cột: mã, thời điểm, kênh, ý định, mức khẩn, tuyến (đi về người hay AI soạn nháp), hạn xử lý, người nhận, trạng thái. Sắp theo mức khẩn rồi thời gian. Hạn gợi ý **[Đề xuất]**: cao 30 phút trong giờ làm, vừa trong ngày, thấp 24 giờ. Thiết kế hàng đợi chung: `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` bài 8.4.

### Bài 2.6: Tin nhiều ý
- **Việc cần làm:** khách viết "đơn em tới đâu rồi, mà cho em đổi màu luôn nha". Cho phép trả **danh sách** ý định, hoặc quy tắc "nhiều ý → lấy ý có quyền cao nhất và ghi chú". **[Nguồn]** τ-bench: 19% lỗi của gpt-4o ở miền bán lẻ là giải quyết thiếu yêu cầu ghép (arXiv 2406.12045, mục 5.2).

!!! tip "Nói đơn giản"
    Một tin nhắn có thể chứa hai việc khác nhau. Nếu AI chỉ trả lời việc đầu, khách sẽ thấy bị bỏ sót việc sau. Vì vậy ta cho phép gắn nhiều ý định, hoặc chọn ý quan trọng nhất làm đầu và ghi chú các ý còn lại.

## 5. Đường không code vs có code

Bài này có hai cách làm. Cách không code đủ để bắt đầu với số tin ít. Cách code nhẹ cần một người biết lập trình, để máy tự kiểm và tự sắp xếp.

| | Không code | Code nhẹ |
|---|---|---|
| Phân loại | Project/Gem trả bảng cho lô tin; người chép vào Sheet | Gọi API mỗi tin, JSON, kiểm lược đồ |
| Luật cứng | Người đọc danh sách cụm khẩn | Hàm `luat_cung()` chạy trước |
| Hàng đợi | Sheet lọc tay | Sheet/SQLite tự sắp |

**Đoạn mã dưới đây làm gì?** Nó gồm bốn phần. Phần một đặt danh sách nhãn hợp lệ. Phần hai là luật cứng: tìm các cụm từ về pháp lý, an toàn, tiền trong tin khách (đã bỏ dấu để bắt cả tin không dấu). Phần ba kiểm xem câu trả lời của AI có đúng khung JSON không. Phần bốn (`dinh_tuyen`) quyết định tin này đi về đâu: người xử lý ngay, người xử lý thường, hay AI soạn nháp. Bạn **không cần đọc hiểu từng dòng**; chỉ cần nắm ý nghĩa, và nhờ người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

Mã mẫu (đã chạy thử bằng `python -I -X utf8`, 2026-11-11; đầu ra LLM là chuỗi giả; LLM là mô hình ngôn ngữ lớn, tức "bộ não" của AI trò chuyện):

```python
import json, re, unicodedata
Y_DINH = {"hoi_tinh_trang_don","doi_tra","hoan_tien","khieu_nai","doi_lich","hoi_thong_tin","khac"}
MUC_KHAN = {"thap","vua","cao"}

def bo_dau(s):
    s = unicodedata.normalize("NFD", s.lower()).replace("đ", "d")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

LUAT_CUNG = [  # viết không dấu để bắt cả tin không dấu
    (r"luat su|kien|toa an|cong an|bao chi|quan ly thi truong|so cong thuong", "phap_ly"),
    (r"ngo doc|di ung|cap cuu|chay no|nhap vien", "an_toan"),
    (r"lua dao|tru tien 2 lan|bi tru tien|mat tien", "tien"),
]

def luat_cung(tin):
    t = bo_dau(tin)
    return next((ly for mau, ly in LUAT_CUNG if re.search(mau, t)), None)

def kiem_json_llm(raw):
    try: d = json.loads(raw)
    except json.JSONDecodeError: return None
    if d.get("y_dinh") not in Y_DINH or d.get("muc_khan") not in MUC_KHAN: return None
    if not isinstance(d.get("tin_cay"), (int, float)) or not 0 <= d["tin_cay"] <= 1: return None
    return d

def dinh_tuyen(tin, raw_llm, nguong=0.7):
    ly = luat_cung(tin)
    if ly: return {"tuyen": "nguoi_ngay", "muc_khan": "cao", "ly_do": ly}
    d = kiem_json_llm(raw_llm)
    if d is None: return {"tuyen": "nguoi", "ly_do": "dau_ra_llm_khong_hop_le"}
    if d["y_dinh"] in {"khieu_nai", "khac"} or d["tin_cay"] < nguong:
        return {"tuyen": "nguoi", "muc_khan": d["muc_khan"], "ly_do": "ngoai_pham_vi_hoac_tin_cay_thap"}
    return {"tuyen": "ai_soan_nhap", "y_dinh": d["y_dinh"], "muc_khan": d["muc_khan"]}
```

Kết quả chạy thử:
- "Ăn bánh xong con tôi bị dị ứng, nổi mẩn" + AI nói `hoi_thong_tin, thap` → `nguoi_ngay, an_toan` (luật cứng thắng).
- "Tôi sẽ báo Sở Công Thương nếu không hoàn tiền" → `nguoi_ngay, phap_ly`.
- "Cho em doi size ao nhe" với `tin_cay 0,55` → `nguoi`.
- Đầu ra AI không phải JSON → `nguoi, dau_ra_llm_khong_hop_le`.

!!! tip "Nói đơn giản"
    Hãy nhìn bốn kết quả trên như bốn tình huống thật. Ca dị ứng và ca dọa báo cơ quan chức năng đều đi thẳng tới người, dù AI có nói gì. Ca đổi size mà AI không chắc thì chuyển người. Và nếu AI trả lời lung tung, không đúng khung, hệ thống cũng chuyển người thay vì tin nó.

**Buộc chuyển sang code khi [Đề xuất]:** trên khoảng 50 tin mỗi ngày; cần hạn xử lý theo mức khẩn chạy tự động; cần đo bảng nhầm lẫn mỗi khi đổi prompt hay mô hình.

**Lưu ý chi phí:** bước phân loại có thể dùng mô hình nhỏ, rẻ nếu đo trên tin có nhãn thấy không kém hơn (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.6).

## 6. Tiêu chí lên cấp (C2 → C3) [Đề xuất]

Bạn sang cấp C3 khi đạt đủ các điều sau:

1. Trên ≥50 tin có nhãn: độ đúng ý định không thấp hơn mức hai người đồng thuận với nhau quá 10 điểm.
2. Recall lớp `muc_khan = cao` = 100% trên bộ thử, gồm ≥10 ca khẩn viết không dấu hoặc viết tắt. Với n nhỏ (n là số mẫu), 10/10 vẫn cho giới hạn trên của tỉ lệ sót khoảng 28% (Wilson; đây là công thức thống kê tính khoảng dao động của một tỉ lệ khi có ít mẫu); vì vậy luật cứng là bắt buộc, không phải tùy chọn.
3. 100% đầu ra sai lược đồ bị chặn và chuyển người (thử bằng ≥5 đầu ra hỏng cố ý).
4. Hàng đợi chạy 2 tuần; ca khẩn được xử lý trong hạn ≥90% thời gian.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung.

### 7.a Cửa hàng điện máy nhỏ
Ý định thêm: `bao_hanh`, `lap_dat`. Luật cứng: "chập điện", "khét", "bốc khói", "giật" → `nguoi_ngay, an_toan`. Không dùng từ ngắn "chay" (khớp cả "cháy" và "chạy"); dùng cụm "bi chay", "chay no".

### 7.b Phòng khám nha
Ý định: `dat_lich`, `doi_lich`, `hoi_gia`, `sau_dieu_tri`. Mọi tin `sau_dieu_tri` (sưng, chảy máu, đau) → người ngay, AI không soạn. Lịch hẹn đọc từ phần mềm lịch ở C3.

### 7.c Shop thời trang
Tin chỉ có ảnh (ảnh áo bị rách) → `khac`, người. Ở cấp sau có thể thêm mô hình thị giác (AI biết "nhìn" ảnh), nhưng chỉ sau khi đo.

## 8. Tài liệu tham khảo

| Nguồn | Loại | Đọc | Tin cậy |
|---|---|---|---|
| Nubank, arXiv 2606.08867 | Bài báo, triển khai thật | Phần lớn toàn văn | Cao |
| SEATauBench, arXiv 2606.28715 | Benchmark đa ngôn ngữ có tiếng Việt | Phần chính và phụ lục C-F | Trung bình-Cao (dịch từ tiếng Anh, có kiểm bởi người bản ngữ) |
| τ-bench, arXiv 2406.12045 | Benchmark | Toàn văn phần chính | Cao về phương pháp; số mô hình năm 2024 đã cũ |
| Anthropic, "Building effective agents" | Blog kỹ thuật | Qua `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` | Cao |

## 9. Chưa kiểm chứng

- Không có nguồn đo phân loại ý định trên tin nhắn tiếng Việt thật của SME. Số SEATauBench là benchmark dịch.
- Ngưỡng `tin_cay` 0,7, hạn 30 phút, 50 tin/ngày: đề xuất.
- Danh sách luật cứng là ví dụ; chưa thử trên dữ liệu thật.
- Khoảng Wilson cho 10/10 (giới hạn dưới ≈ 0,72) tính bằng công thức ở `cap-06`; đã kiểm bằng hàm `wilson()` trong mã mẫu C6.
