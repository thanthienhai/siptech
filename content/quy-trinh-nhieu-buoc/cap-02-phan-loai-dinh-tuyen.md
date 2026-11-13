# Q2 — Phân loại và định tuyến: quy tắc trước, AI sau

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

## 1) Mục tiêu và người đọc

**Người đọc:** người đã có luồng Q1, còn một bước "đọc chữ tự do để biết chuyển cho ai": email chung `info@`, tin Zalo OA, yêu cầu nội bộ trong nhóm chat.

**Sau cấp này có:** bộ định tuyến 3 tầng: (1) luật bắt các trường hợp rõ (mã đơn, từ khóa); (2) AI phân loại phần còn lại, trả JSON có độ tin cậy; (3) "không chắc" hoặc "khác" vào hàng đợi người. Cộng một bộ ≥50 ca có đáp án để đo.

**Thứ chạy được độc lập:** bộ định tuyến chỉ **gắn nhãn và chuyển**, không trả lời khách, không ghi vào hệ thống nghiệp vụ. Sai thì hậu quả là chuyển nhầm người, người nhận chuyển lại.

Soạn câu trả lời cho khách là việc của nhóm `../xu-ly-yeu-cau-khach/00-README.md`. Ở đây chỉ phân loại và chuyển.

## 2) Câu hỏi cấp này trả lời / lỗi của Q1

**Câu hỏi:** "Làm sao chuyển yêu cầu viết tự do đến đúng người mà không cần ai ngồi đọc hết?"

**Lỗi của Q1:** luật từ khóa bắt được phần rõ ràng nhưng bỏ sót cách viết khác ("đơn hôm qua chưa thấy đâu", không có mã đơn), hoặc bắt nhầm ("CV" trong "CV xe tải").

## 3) Kiến thức nền

- **[Nguồn]** Mẫu "routing" trong Anthropic "Building effective agents" (định nghĩa ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.2): phân loại đầu vào rồi chuyển sang tác vụ chuyên biệt; phân loại có thể bằng LLM hoặc bộ phân loại truyền thống.
- **[Nguồn]** READY (arXiv 2609.02095): điều quyết định triển khai không phải độ chính xác của AI một mình, mà là chính sách giám sát: ca nào nhận tự động, ca nào chuyển người, để đạt độ tin cậy mục tiêu với chi phí thấp nhất. Ví dụ của bài: hai hệ có độ chính xác tự chạy 72,8% và 72,5% nhưng để cùng đạt độ tin cậy 76% cần chuyển người 39,2% và 29,6% số ca. Bài cũng nhấn mạnh phải chọn ngưỡng trên một bộ ca và kiểm lại trên bộ ca khác (held-out). Giới hạn: ví dụ thực nghiệm là kiểm toán lâm sàng, không phải định tuyến email.
- **[Nguồn]** τ-bench: khoảng 55% lỗi của gpt-4o là sai tham số hoặc sai thông tin; mô hình yếu hơn còn bịa mã không tồn tại nhiều hơn (gpt-3.5 khoảng 2,08 lần/việc so với 0,46 của gpt-4o). Hàm ý [Đề xuất]: mã đơn, mã nhân viên phải được kiểm bằng code, không tin chữ AI trả về.
- **[Nguồn]** Brynjolfsson và cs. (NBER 31161): công cụ AI giúp người mới nhiều hơn người giỏi. Hàm ý [Đề xuất]: đo định tuyến riêng cho các ca người mới hay chuyển nhầm.
- **[Đề xuất] Thiết kế 3 tầng:**
  1. **Luật trước:** biểu thức chính quy cho mã đơn (`DH\d{5}`), mã phiếu, địa chỉ email người gửi nội bộ, từ khóa chắc chắn. Rẻ, nhanh, giải thích được.
  2. **AI sau:** chỉ cho phần luật không bắt. Đầu ra JSON cố định `{loai, do_tin_cay, ly_do_ngan}`, `loai` thuộc danh sách đóng có "khac". Kiểm lược đồ bằng code; sai lược đồ coi như "không chắc".
  3. **Người cuối:** `khac`, độ tin cậy dưới ngưỡng, hoặc nhiều nhãn → hàng đợi người, kèm tin gốc.
- **[Đề xuất] Về "độ tin cậy" mô hình tự khai:** chưa chắc đã hiệu chuẩn. Đừng tin con số; chọn ngưỡng bằng cách đo trên bộ ca: với mỗi ngưỡng, bao nhiêu % ca tự động và bao nhiêu % trong số đó đúng. Đó là phiên bản thu nhỏ của READY.

## 4) Chuỗi bài nhỏ

### Bài Q2.1 — Danh sách nhãn đóng
- **Làm:** từ log 2 tuần ở Q0, liệt kê 4-7 loại yêu cầu và người nhận. Thêm `khac`. Viết định nghĩa một câu và 2 ví dụ cho mỗi loại.
- **Sản phẩm:** bảng nhãn. **Lỗi:** 20 nhãn chồng chéo; không có `khac`.

### Bài Q2.2 — Bộ 50 ca có đáp án
- **Làm:** lấy 50 tin thật (che tên, SĐT bằng script ở `../an-toan-du-lieu-va-phap-ly-vn.md` bài A3), hai người gán nhãn độc lập, bàn lại chỗ lệch. Gồm ≥10 ca khó (viết tắt, không dấu, nhiều ý). Cách làm bộ ca: `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` bài 6.2.
- **Sản phẩm:** file 50 ca. Ghi tỷ lệ hai người đồng ý ngay từ đầu: nếu người với người còn lệch nhiều, nhãn chưa rõ, sửa Q2.1 trước.

### Bài Q2.3 — Tầng luật
- **Làm:** viết luật; chạy trên 50 ca; ghi ca nào luật bắt, bắt đúng bao nhiêu.
- **Sản phẩm:** bảng "luật bắt X/50, đúng Y/X". Luật bắt sai nào phải sửa hoặc bỏ.

### Bài Q2.4 — Tầng AI
- **Làm:** **[Không code]** một Project/Gem/GPT tùy chỉnh với bảng nhãn, ví dụ, yêu cầu trả JSON; dán từng ca chưa được luật bắt, chép kết quả vào Sheet. **[Code]** gọi API với đầu ra có cấu trúc (`../rag-tra-cuu-tai-lieu/cap-01-goi-api.md` bài C1.4), kiểm lược đồ bằng code.
- **Sản phẩm:** kết quả AI trên phần còn lại của 50 ca.

### Bài Q2.5 — Chọn ngưỡng chuyển người
- **Làm:** với các ngưỡng 0,5 / 0,7 / 0,9: tính % ca tự động và % đúng trong số tự động. Chọn ngưỡng sao cho số ca chuyển nhầm chấp nhận được. Kiểm lại trên 20 ca mới chưa dùng để chọn.
- **Sản phẩm:** bảng ngưỡng + ngưỡng đã chọn + kết quả trên 20 ca mới. Với n nhỏ, báo khoảng tin cậy Wilson (`cap-06-danh-gia.md` bài 6.5).

### Bài Q2.6 — Nối vào luồng Q1
- **Làm:** bộ định tuyến ghi `loai`, `nguon` (luat/ai/nguoi), `do_tin_cay` vào bảng phiếu; người nhận có nút "chuyển nhầm" ghi lại nhãn đúng. Nhãn đúng này thành ca mới cho bộ test.
- **Sản phẩm:** luồng chạy thật 2 tuần + tỷ lệ "chuyển nhầm".

## 5) Đường không code vs có code; khi nào buộc chuyển

| | Không code | Có code |
|---|---|---|
| Cách | Make/Zapier/n8n có bước gọi mô hình AI; hoặc người dán vào Gem/Project rồi chọn nhãn | Script gọi API, luật bằng regex, kiểm JSON |
| Hàng rào | Bộ lọc của nền tảng (điều kiện trên trường) | Kiểm lược đồ, danh sách nhãn đóng, kiểm mã đơn tồn tại bằng tra cứu thật |

**Buộc chuyển sang code [Đề xuất] khi:** lượng tin > vài chục/ngày mà vẫn dán tay; cần kiểm mã đơn có thật (tra KiotViet/Haravan); cần chạy lại 50 ca mỗi khi đổi prompt hoặc mô hình.

**Code mẫu (đã chạy thử 2026-11-11 bằng `python -I`, hàm giả thay mô hình; chưa chạy với API thật).** Kết quả: 3 ca bắt bằng luật, ca "rất bực" AI gắn `khieu_nai` với độ tin cậy 0,9, ca "giờ mở cửa" vào hàng đợi người; JSON hỏng bị coi là "không chắc".

```python
import json, re
LOAI = {"don_hang", "thanh_toan", "tuyen_dung", "khieu_nai", "khac"}
NGUOI_NHAN = {"don_hang": "kho@", "thanh_toan": "ketoan@", "tuyen_dung": "nhansu@",
              "khieu_nai": "truongca@", "khac": "hang_doi_nguoi"}
QUY_TAC = [(re.compile(r"\b(DH|ĐH)\d{5}\b", re.I), "don_hang"),
           (re.compile(r"(đề nghị thanh toán|de nghi thanh toan|ĐNTT)", re.I), "thanh_toan"),
           (re.compile(r"(ứng tuyển|ung tuyen|\bCV\b)", re.I), "tuyen_dung")]
NGUONG = 0.8   # [Đề xuất] chọn lại bằng bài Q2.5

def llm_phan_loai(text):                       # HÀM GIẢ thay API
    if "bực" in text: return json.dumps({"loai": "khieu_nai", "do_tin_cay": 0.9})
    return json.dumps({"loai": "khac", "do_tin_cay": 0.4})

def kiem_json(raw):                            # hàng rào bằng code
    try:
        d = json.loads(raw)
        if d.get("loai") in LOAI and 0 <= float(d.get("do_tin_cay", -1)) <= 1: return d
    except (ValueError, TypeError): pass
    return {"loai": "khac", "do_tin_cay": 0.0}

def dinh_tuyen(text):
    for bt, loai in QUY_TAC:                   # tầng 1: luật
        if bt.search(text): return {"loai": loai, "nguon": "quy_tac", "den": NGUOI_NHAN[loai]}
    d = kiem_json(llm_phan_loai(text))         # tầng 2: AI
    if d["do_tin_cay"] < NGUONG or d["loai"] == "khac":   # tầng 3: người
        return {"loai": d["loai"], "nguon": "ai_khong_chac", "den": "hang_doi_nguoi"}
    return {"loai": d["loai"], "nguon": "ai", "den": NGUOI_NHAN[d["loai"]]}
```

## 6) Tiêu chí lên Q3 (đo được) [Đề xuất]

1. Bộ ≥50 ca có đáp án, hai người gán nhãn, có ca khó.
2. Trên 20 ca kiểm lại (không dùng để chọn ngưỡng): chuyển nhầm trong số ca tự động ≤ mức công ty chấp nhận (ví dụ ≤ 1/20) và ghi khoảng tin cậy.
3. Chạy thật 2 tuần, có số "chuyển nhầm" do người nhận báo; số này không cao hơn khi người phân loại tay (từ đo nền Q0).
4. Tỷ lệ vào hàng đợi người được ghi lại; hàng đợi có người trực.

Nếu luật đã bắt ≥90% ca và phần còn lại ít, **có thể bỏ tầng AI**: người xử lý phần còn lại rẻ hơn duy trì AI.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

**a) Công ty phân phối thiết bị điện 40 người, email chung `kinhdoanh@` nhận 80 email/ngày.** Nhãn: báo giá, đơn đặt hàng, khiếu nại/bảo hành, công nợ, hồ sơ thầu, nhà cung cấp chào hàng, khác. Luật: email từ tên miền của 30 khách lớn → nhân viên phụ trách khách đó; tiêu đề có "PO" + số → đơn hàng. AI cho phần còn lại. Hồ sơ thầu và khiếu nại luôn có người xem trong ngày, kể cả AI chắc chắn. Rủi ro: email chứa câu lệnh ẩn; bộ định tuyến không có quyền gửi/ghi nên tác động chỉ là chuyển nhầm (xem `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` mục 3.6).

**b) Chuỗi 3 quán cà phê, nhóm Zalo nội bộ "Yêu cầu" 20 tin/ngày.** Nhãn: hỏng thiết bị, thiếu nguyên liệu, đổi ca, tạm ứng, khác. Phần lớn tin ngắn, có từ khóa rõ ("máy xay", "hết sữa", "đổi ca"): luật bắt gần hết. Kết luận có thể là: không cần AI; chuyển sang biểu mẫu Lark có danh sách chọn (Q1) là đủ.

**c) Công ty tuyển dụng thời vụ, nhận CV qua email và Zalo.** Định tuyến theo vị trí ứng tuyển (kho, bán hàng, giao hàng). AI chỉ đọc vị trí và khu vực, không chấm điểm ứng viên. CV là dữ liệu cá nhân; nếu gửi qua API nước ngoài phải xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 6. Phương án an toàn hơn: biểu mẫu ứng tuyển có ô chọn vị trí (Q1), AI chỉ dùng cho CV gửi lẻ.

## 8) Tài liệu tham khảo

| Nguồn | Loại | Mức đọc | Tin cậy |
|---|---|---|---|
| READY, arXiv 2609.02095 (Scale AI) | Khung đánh giá + nghiên cứu ca | Tóm tắt, mục 1-2, 6-7 | Trung bình-cao; một workflow lâm sàng |
| τ-bench, arXiv 2406.12045 | Benchmark | Toàn văn | Cao; mô hình 2024 |
| Anthropic, "Building effective agents" (qua `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md`) | Blog kỹ thuật | Nhóm RAG đọc qua tóm tắt | Cao |
| Brynjolfsson, Li, Raymond, NBER WP 31161 (qua `../thuc-trang-sme-viet-nam.md`) | Nghiên cứu có đối chứng | Trang tóm tắt | Cao cho bối cảnh đó |

## 9) Chưa kiểm chứng

- Không có nguồn đo độ chính xác phân loại tin nhắn/email tiếng Việt có viết tắt, không dấu. Người học phải tự đo bằng bộ 50 ca.
- Độ tin cậy mô hình tự khai có hiệu chuẩn hay không trên tiếng Việt: chưa có dữ liệu.
- Ngưỡng 0,8, bộ 50 + 20 ca, "1/20 chuyển nhầm", "luật bắt ≥90%" là đề xuất.
- Tính năng gọi mô hình AI trong Make/Zapier/n8n (tên node, chi phí operation của bước AI): chưa đọc tài liệu chính thức.
