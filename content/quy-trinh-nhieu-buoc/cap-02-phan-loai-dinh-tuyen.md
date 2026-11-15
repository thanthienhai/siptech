# Q2 — Phân loại và định tuyến: quy tắc trước, AI sau

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

!!! tip "Tóm tắt nhanh"
    Mỗi ngày có nhiều tin nhắn và email viết tự do đổ về hộp thư chung, và ai đó phải đọc để biết chuyển cho ai. Bài này dạy một bộ "người chia thư" gồm 3 tầng: **quy tắc** bắt các trường hợp rõ ràng, **AI** đọc phần còn lại, và **con người** nhận những ca AI không chắc. Sau bài, bạn có bộ định tuyến chạy thử được và một bộ ca có đáp án để đo xem nó chuyển đúng hay sai.

## 1) Mục tiêu và người đọc

**Bài này dành cho ai:** người đã có luồng Q1 (bài trước trong nhóm này), nhưng vẫn còn một bước phải đọc chữ viết tự do để biết chuyển cho ai. Ví dụ: email chung `info@`, tin nhắn Zalo OA (tài khoản Zalo chính thức của doanh nghiệp), hoặc yêu cầu nội bộ trong nhóm chat.

**Bạn cần chuẩn bị:**
- Luồng Q1 đã chạy được.
- Nhật ký (log, tức là bản ghi lại các yêu cầu đã đến) 2 tuần từ bài Q0, để biết các loại yêu cầu và người nhận.
- 50 tin nhắn thật đã che tên và số điện thoại, để làm bộ ca có đáp án.
- Một Project, Gem hoặc GPT tùy chỉnh (là các tính năng cho bạn lưu sẵn chỉ dẫn cho AI để dùng lại), và một bảng tính Sheet để chép kết quả.

**Sau bài này bạn sẽ có:** bộ định tuyến 3 tầng:
1. Luật bắt các trường hợp rõ (mã đơn, từ khóa).
2. AI phân loại phần còn lại, trả về JSON có độ tin cậy. (JSON là một cách viết dữ liệu có khung rõ ràng để máy đọc được.)
3. Ca "không chắc" hoặc "khác" thì vào hàng đợi cho người xử lý.

Cộng thêm một bộ ≥50 ca có đáp án để đo.

**Thứ bạn cầm đi được, chạy độc lập:** bộ định tuyến chỉ **gắn nhãn và chuyển**. Nó không trả lời khách và không ghi vào hệ thống nghiệp vụ. Nếu sai, hậu quả chỉ là chuyển nhầm người, và người nhận sẽ chuyển lại.

Soạn câu trả lời cho khách là việc của nhóm `../xu-ly-yeu-cau-khach/00-README.md`. Ở bài này, chúng ta chỉ phân loại và chuyển.

## 2) Câu hỏi cấp này trả lời / lỗi của Q1

**Câu hỏi:** "Làm sao chuyển yêu cầu viết tự do đến đúng người mà không cần ai ngồi đọc hết?"

**Lỗi của Q1:** luật từ khóa bắt được phần rõ ràng, nhưng có hai chỗ yếu:
- Bỏ sót khi khách viết theo cách khác, ví dụ "đơn hôm qua chưa thấy đâu" (không có mã đơn).
- Bắt nhầm, ví dụ "CV" trong "CV xe tải" bị hiểu là hồ sơ xin việc.

## 3) Kiến thức nền

Phần này gom lại vài nghiên cứu và một thiết kế để bạn hiểu **vì sao** chia làm 3 tầng. Bạn không cần nhớ chi tiết, chỉ cần nắm ý chính ở các hộp "Nói đơn giản".

- **[Nguồn]** Mẫu "routing" (định tuyến) trong bài "Building effective agents" của Anthropic (định nghĩa ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.2). Ý của mẫu này: phân loại đầu vào trước, rồi chuyển sang tác vụ chuyên biệt. Việc phân loại có thể làm bằng LLM (mô hình AI ngôn ngữ lớn, như ChatGPT hay Claude) hoặc bằng bộ phân loại truyền thống.
- **[Nguồn]** READY (arXiv 2609.02095): điều quyết định việc triển khai không phải độ chính xác của AI một mình, mà là **chính sách giám sát**: ca nào cho nhận tự động, ca nào chuyển cho người, để đạt độ tin cậy mục tiêu với chi phí thấp nhất. Ví dụ của bài: hai hệ có độ chính xác tự chạy 72,8% và 72,5%, nhưng để cùng đạt độ tin cậy 76% thì phải chuyển người lần lượt 39,2% và 29,6% số ca. Bài cũng nhấn mạnh: phải chọn ngưỡng trên một bộ ca, rồi kiểm lại trên một bộ ca khác (gọi là held-out, nghĩa là bộ ca "để riêng", chưa dùng khi chọn ngưỡng). Giới hạn: ví dụ thực nghiệm của bài là kiểm toán lâm sàng, không phải định tuyến email.

!!! tip "Nói đơn giản"
    Hai hệ AI có độ chính xác gần bằng nhau, nhưng một hệ cần nhờ người nhiều hơn hẳn để đạt cùng mức tin cậy. Vì vậy điều đáng quan tâm là: **ca nào để máy tự chạy, ca nào trả về cho người**. Đó cũng là việc bạn sẽ làm ở bài Q2.5.

- **[Nguồn]** τ-bench (một bộ bài kiểm tra cho AI làm việc theo quy trình): khoảng 55% lỗi của gpt-4o là sai tham số hoặc sai thông tin. Mô hình yếu hơn còn bịa ra mã không tồn tại nhiều hơn (gpt-3.5 khoảng 2,08 lần mỗi việc, so với 0,46 của gpt-4o). Hàm ý **[Đề xuất]**: mã đơn, mã nhân viên phải được kiểm bằng code (tức là bằng chương trình máy tính), không tin chữ AI trả về.
- **[Nguồn]** Brynjolfsson và cs. (NBER 31161): công cụ AI giúp người mới nhiều hơn người giỏi. Hàm ý **[Đề xuất]**: đo định tuyến riêng cho các ca của người mới, vì họ hay chuyển nhầm.
- **[Đề xuất] Thiết kế 3 tầng:**
  1. **Luật trước:** dùng biểu thức chính quy (regex, là cách viết một "khuôn mẫu chữ" để máy tự tìm trong văn bản) cho mã đơn (`DH\d{5}`), mã phiếu, địa chỉ email người gửi nội bộ, và các từ khóa chắc chắn. Cách này rẻ, nhanh, và giải thích được vì sao ca đó đi về hướng đó.
  2. **AI sau:** chỉ dùng cho phần luật không bắt được. Đầu ra là JSON cố định `{loai, do_tin_cay, ly_do_ngan}`, trong đó `loai` phải thuộc một danh sách đóng (danh sách cố định, không được viết ngoài danh sách) và có sẵn mục "khac". Dùng code kiểm lược đồ (tức là kiểm xem JSON có đúng khuôn đã định không). Sai lược đồ thì coi như "không chắc".
  3. **Người cuối:** nhãn `khac`, độ tin cậy dưới ngưỡng, hoặc nhiều nhãn cùng lúc thì vào hàng đợi cho người xử lý, kèm tin nhắn gốc.

!!! tip "Nói đơn giản"
    Hình dung bàn tiếp nhận thư của công ty. Việc nào có dấu hiệu rõ (mã đơn, từ khóa chắc chắn) thì nhân viên mới cũng chia đúng chỗ. Thư viết lủng củng thì nhờ một trợ lý giỏi đọc giúp. Thư mà trợ lý cũng không chắc thì đưa cho người có kinh nghiệm. Càng ít thư phải đưa lên tầng trên càng đỡ tốn công.

- **[Đề xuất] Về "độ tin cậy" mà mô hình tự khai:** chưa chắc con số đó đã được hiệu chuẩn (nghĩa là chưa chắc "0,9" thật sự có nghĩa là đúng khoảng 9 lần trên 10). Đừng tin con số này. Hãy chọn ngưỡng bằng cách đo trên bộ ca: với mỗi ngưỡng, bao nhiêu % ca được xử lý tự động và bao nhiêu % trong số đó đúng. Đó là phiên bản thu nhỏ của READY.

## 4) Chuỗi bài nhỏ

Sáu bài dưới đây làm theo thứ tự. Mỗi bài nêu việc cần làm và thứ bạn có sau bài.

### Bài Q2.1 — Danh sách nhãn đóng
- **Việc cần làm:** từ log 2 tuần ở Q0, liệt kê 4 đến 7 loại yêu cầu và người nhận của từng loại. Thêm một nhãn `khac` cho những ca không thuộc loại nào. Với mỗi loại, viết định nghĩa một câu và 2 ví dụ.
- **Bạn có sau bài:** bảng nhãn.
- **Lỗi hay gặp:** có tới 20 nhãn chồng chéo nhau; không có nhãn `khac`.

### Bài Q2.2 — Bộ 50 ca có đáp án
- **Việc cần làm:** lấy 50 tin nhắn thật. Che tên và số điện thoại (SĐT) bằng script (đoạn chương trình ngắn) ở `../an-toan-du-lieu-va-phap-ly-vn.md` bài A3. Sau đó hai người gán nhãn **độc lập** (mỗi người làm riêng, không nhìn bài nhau), rồi ngồi bàn lại những chỗ lệch nhau. Bộ ca phải có ≥10 ca khó (viết tắt, không dấu, nhiều ý trong một tin). Cách làm bộ ca xem ở `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` bài 6.2.
- **Bạn có sau bài:** file 50 ca. Ghi lại tỷ lệ hai người đồng ý ngay từ đầu. Nếu người với người còn lệch nhiều, nghĩa là nhãn chưa rõ, hãy quay lại sửa Q2.1 trước.

### Bài Q2.3 — Tầng luật
- **Việc cần làm:** viết luật, chạy trên 50 ca, rồi ghi lại ca nào luật bắt và bắt đúng bao nhiêu.
- **Bạn có sau bài:** bảng "luật bắt X/50, đúng Y/X". Luật nào bắt sai thì phải sửa hoặc bỏ.

### Bài Q2.4 — Tầng AI
- **Việc cần làm:**
  - **[Không code]** Tạo một Project, Gem hoặc GPT tùy chỉnh, nạp vào bảng nhãn, các ví dụ và yêu cầu trả về JSON. Sau đó dán từng ca chưa được luật bắt vào, rồi chép kết quả vào Sheet.
  - **[Code]** Gọi API (cổng để chương trình của bạn nói chuyện trực tiếp với dịch vụ AI) với đầu ra có cấu trúc (xem `../rag-tra-cuu-tai-lieu/cap-01-goi-api.md` bài C1.4), và kiểm lược đồ bằng code.
- **Bạn có sau bài:** kết quả AI trên phần còn lại của 50 ca (phần luật không bắt được).

### Bài Q2.5 — Chọn ngưỡng chuyển người
- **Việc cần làm:** với các ngưỡng 0,5 / 0,7 / 0,9, tính hai con số: % ca được xử lý tự động, và % đúng trong số ca tự động đó. Chọn ngưỡng sao cho số ca chuyển nhầm ở mức chấp nhận được. Cuối cùng kiểm lại trên 20 ca mới, chưa dùng để chọn ngưỡng.
- **Bạn có sau bài:** bảng ngưỡng, ngưỡng đã chọn, và kết quả trên 20 ca mới. Khi số ca nhỏ (n nhỏ), hãy báo khoảng tin cậy Wilson (một cách tính cho biết "con số đo được có thể lệch trong khoảng nào"; xem `cap-06-danh-gia.md` bài 6.5).

### Bài Q2.6 — Nối vào luồng Q1
- **Việc cần làm:** bộ định tuyến ghi `loai`, `nguon` (luat/ai/nguoi) và `do_tin_cay` vào bảng phiếu. Người nhận có nút "chuyển nhầm" để ghi lại nhãn đúng. Nhãn đúng này trở thành ca mới cho bộ test.
- **Bạn có sau bài:** luồng chạy thật 2 tuần và tỷ lệ "chuyển nhầm".

## 5) Đường không code vs có code; khi nào buộc chuyển

Bài này có hai cách làm. Cách không code đủ dùng khi mới bắt đầu. Cách có code cần người biết lập trình, nhưng cho phép máy tự kiểm và chạy lại nhanh.

| | Không code | Có code |
|---|---|---|
| Cách | Make/Zapier/n8n (các nền tảng kéo thả để nối các ứng dụng với nhau) có bước gọi mô hình AI; hoặc người dán vào Gem/Project rồi chọn nhãn | Script gọi API, luật bằng regex, kiểm JSON |
| Hàng rào | Bộ lọc của nền tảng (điều kiện trên trường) | Kiểm lược đồ, danh sách nhãn đóng, kiểm mã đơn tồn tại bằng tra cứu thật |

**Buộc chuyển sang code [Đề xuất] khi:**
- Lượng tin > vài chục/ngày mà vẫn dán tay.
- Cần kiểm mã đơn có thật (tra KiotViet/Haravan, các phần mềm quản lý bán hàng).
- Cần chạy lại 50 ca mỗi khi đổi prompt (câu chỉ dẫn gửi cho AI) hoặc đổi mô hình.

**Đoạn mã dưới đây làm gì?** Nó mô phỏng đúng bộ định tuyến 3 tầng ở mục 3. Một tin nhắn đi vào sẽ được thử qua luật trước (có mã đơn, có từ "đề nghị thanh toán", có từ "ứng tuyển" hay không). Nếu luật không bắt, tin được đưa cho AI phân loại. Phần trả lời của AI luôn bị kiểm lại: nếu không đúng khuôn thì coi như "không chắc". Cuối cùng, ca nào AI không chắc hoặc thuộc nhóm "khác" thì được đưa vào hàng đợi cho người. Trong mã này, phần "AI" chỉ là một hàm giả để minh họa. Bạn **không cần đọc hiểu từng dòng**. Chỉ cần nắm ý chính, rồi nhờ người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

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

!!! tip "Nói đơn giản"
    Đoạn mã này chỉ làm đúng ba việc theo thứ tự: thử luật trước, hỏi AI sau, và đưa cho người nếu AI không chắc. Con số 0,8 trong mã là ngưỡng tạm; bạn sẽ chọn lại con số của riêng mình bằng bài Q2.5.

## 6) Tiêu chí lên Q3 (đo được) [Đề xuất]

Bạn có thể sang Q3 khi đạt đủ các điều sau:
1. Có bộ ≥50 ca có đáp án, do hai người gán nhãn, và có ca khó.
2. Trên 20 ca kiểm lại (không dùng để chọn ngưỡng): số ca chuyển nhầm trong số ca tự động ≤ mức công ty chấp nhận (ví dụ ≤ 1/20), và có ghi khoảng tin cậy.
3. Chạy thật 2 tuần, có số "chuyển nhầm" do người nhận báo. Số này không cao hơn khi người phân loại tay (lấy từ đo nền ở Q0).
4. Tỷ lệ ca vào hàng đợi người được ghi lại, và hàng đợi có người trực.

Nếu luật đã bắt ≥90% ca và phần còn lại ít, bạn **có thể bỏ tầng AI**: để người xử lý phần còn lại sẽ rẻ hơn duy trì AI.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

Ba tình huống giả định để bạn dễ hình dung:

**a) Công ty phân phối thiết bị điện 40 người, email chung `kinhdoanh@` nhận 80 email/ngày.**
- Nhãn: báo giá, đơn đặt hàng, khiếu nại/bảo hành, công nợ, hồ sơ thầu, nhà cung cấp chào hàng, khác.
- Luật: email từ tên miền của 30 khách lớn thì chuyển nhân viên phụ trách khách đó; tiêu đề có "PO" kèm số thì là đơn hàng. AI xử lý phần còn lại.
- Hồ sơ thầu và khiếu nại luôn có người xem trong ngày, kể cả khi AI chắc chắn.
- Rủi ro: email có thể chứa câu lệnh ẩn nhằm đánh lừa AI. Vì bộ định tuyến không có quyền gửi hay ghi, tác động nếu bị lừa chỉ là chuyển nhầm (xem `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` mục 3.6).

**b) Chuỗi 3 quán cà phê, nhóm Zalo nội bộ "Yêu cầu" 20 tin/ngày.**
- Nhãn: hỏng thiết bị, thiếu nguyên liệu, đổi ca, tạm ứng, khác.
- Phần lớn tin ngắn và có từ khóa rõ ("máy xay", "hết sữa", "đổi ca"), nên luật bắt gần hết.
- Kết luận có thể là: không cần AI. Chuyển sang biểu mẫu Lark có danh sách chọn (Q1) là đủ.

**c) Công ty tuyển dụng thời vụ, nhận CV qua email và Zalo.**
- Định tuyến theo vị trí ứng tuyển (kho, bán hàng, giao hàng). AI chỉ đọc vị trí và khu vực, không chấm điểm ứng viên.
- CV là dữ liệu cá nhân. Nếu gửi qua API của nước ngoài thì phải xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 6.
- Phương án an toàn hơn: dùng biểu mẫu ứng tuyển có ô chọn vị trí (Q1), và chỉ dùng AI cho CV gửi lẻ.

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
