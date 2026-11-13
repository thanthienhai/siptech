# Q3 — Báo cáo định kỳ và phân tích số liệu: code tính, AI viết lời

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

## 1) Mục tiêu và người đọc

**Người đọc:** kế toán, quản lý bán hàng, chủ cửa hàng đang tự làm báo cáo tuần/tháng từ Sheets hoặc phần mềm bán hàng; người đang dán bảng số vào chatbot và hỏi "phân tích giúp".

**Sau cấp này có:** một báo cáo tuần tự sinh theo 4 bước: (1) lấy dữ liệu; (2) **kiểm dữ liệu bằng code** (trùng, thiếu, mâu thuẫn); (3) **tính số bằng code/công thức**; (4) AI chỉ viết phần nhận xét từ bảng số đã tính, và code kiểm mọi con số trong lời nhận xét phải có trong bảng. Người duyệt trước khi gửi.

**Thứ chạy được độc lập:** báo cáo này chỉ đọc dữ liệu, không ghi vào hệ thống nghiệp vụ. Nếu AI viết sai, người duyệt chặn lại trước khi gửi.

## 2) Câu hỏi cấp này trả lời / lỗi đang gặp

**Câu hỏi:** "Dùng AI làm báo cáo và phân tích bảng tính thế nào để không bị số sai?"

**Lỗi thường gặp [Đề xuất, quan sát]:** dán bảng 500 dòng vào chat, nhận về "doanh thu tăng 12%" mà không biết con số từ đâu; AI cộng cả đơn đã hủy; AI bỏ sót một kênh bán; mỗi lần hỏi lại ra số khác.

## 3) Kiến thức nền

### 3.1 Bằng chứng về AI và bảng tính [Nguồn]
- **SpreadsheetBench 2 (arXiv 2606.29955, NeurIPS 2026 Datasets track):** 321 việc từ dữ liệu doanh nghiệp thật, trung bình 11,8 sheet và 593,5 ô cần sửa mỗi việc. Mô hình tốt nhất (Claude Opus 4.6) đúng trọn việc 34,89%; việc sửa lỗi bảng tính chỉ 12%. Có hiện tượng sửa đúng phần lớn ô nhưng sai toàn việc (dựng mô hình tài chính: 89,69% ô đúng, 34% việc đúng). Lỗi chính của các lượt thất bại: xem bảng chưa đủ (42,3%), chọn sai ô để sửa (32,9%). Các sản phẩm AI gắn vào Excel thử trên 30 việc không vượt mô hình chạy qua khung agent của tác giả.
- **TrustDABench (arXiv 2608.24145):** 2.340 ca đã người kiểm. Khi dữ liệu bị làm cho không thể trả lời (thiếu cột, hai cột cùng tên, bản ghi trùng mâu thuẫn), điểm từ chối hợp lệ trung bình cao nhất chỉ 24,21%. Dữ liệu mâu thuẫn gần như không bị phát hiện (gộp các mô hình: 0,46% với nhóm toán tử mâu thuẫn, so với 16,49% với nhóm xóa thông tin). 74,8% ca lỗi là "trả lời im lặng không có căn cứ". Ví dụ trong bài: hai dòng cùng mã sản phẩm, cùng dải mã vạch, số lượng 43 và 25; mô hình cộng cả hai thành 1.176 thay vì hỏi lại.
- **Data referencing errors (arXiv 2606.32029, AWS AI Labs):** mô hình 1,7B-20B trích nhầm hoặc bỏ sót giá trị bảng ở 5,71% đến 46,48% câu trả lời (trên WTQ). Nhắc trong prompt "không bỏ sót, không trích sai" chỉ giảm từ 14,04% xuống 12,50% (Qwen3-8B). Có ca câu trả lời cuối đúng dù bước giữa trích sai. Giới hạn: mô hình nhỏ, bộ dữ liệu học thuật.
- **TheAgentCompany:** nhóm việc khoa học dữ liệu, tài chính có tỷ lệ hoàn thành thấp (14,29%, 8,33% với mô hình tốt nhất); tác giả nêu các việc này hay cần làm bảng tính và đọc ảnh scan.
- **τ-bench:** trong lỗi "sai thông tin" có ca tính sai tổng tiền.
- **[Nguồn, chỉ tóm tắt]** arXiv 2611.00163 (một tác giả, 5 bài toán) báo cáo Claude cho Excel hữu ích cho dựng mô hình cơ bản. Chưa đọc toàn văn; không dùng làm căn cứ.

### 3.2 Hàm ý thiết kế [Đề xuất]
1. **Số do code hoặc công thức tính.** Pivot, SUMIFS, `QUERY` trong Sheets, hoặc script. AI không cộng, không trừ, không tính phần trăm trong đầu.
2. **Kiểm dữ liệu trước khi tính:** trùng mã, ô trống, dòng đã hủy, đơn vị lệch, cột trùng tên. TrustDABench cho thấy mô hình gần như không tự phát hiện mâu thuẫn, nên việc này phải là code.
3. **AI nhận bảng số đã tính (nhỏ), không nhận dữ liệu thô (lớn).** Ít dòng hơn thì ít chỗ để trích nhầm, và ít dữ liệu cá nhân đi ra ngoài.
4. **Code kiểm mọi con số trong lời AI phải có trong bảng đã tính.** Số lạ (ví dụ "dự báo 2,5 triệu") → chặn, chuyển người.
5. **Nếu cho AI viết code phân tích** (công cụ chạy code trong Claude/ChatGPT/Gemini), giữ lại code và chạy lại được; người kiểm logic lọc (đơn hủy có bị loại không?). Viết code đúng cú pháp vẫn có thể lọc sai.
6. **AI không sửa trực tiếp bảng tính thật.** Làm trên bản sao; người áp thay đổi.

## 4) Chuỗi bài nhỏ

### Bài Q3.1 — Định nghĩa báo cáo bằng chữ
- **Làm:** liệt kê 5-10 chỉ số (doanh thu hoàn thành theo kênh, số đơn hủy, top 10 sản phẩm, công nợ quá hạn). Mỗi chỉ số: công thức bằng lời, nguồn dữ liệu, loại trừ gì (đơn hủy, đơn thử).
- **Sản phẩm:** "từ điển chỉ số" 1 trang. Đây là phần quan trọng nhất; thiếu nó thì người và máy hiểu khác nhau.

### Bài Q3.2 — Lấy dữ liệu tự động
- **Làm:** xuất file theo lịch hoặc gọi API (KiotViet Public API có hóa đơn, đơn hàng; Haravan có API và webhook; MISA AMIS có đồng bộ qua API: xem `00-README.md` mục 5). Lưu bản thô theo ngày, không ghi đè.
- **Sản phẩm:** thư mục/tab dữ liệu thô theo ngày.

### Bài Q3.3 — Kiểm dữ liệu bằng code
- **Làm:** viết các kiểm tra: trùng `ma_don`; ô thiếu; trạng thái lạ; số âm; tổng số dòng so với hôm trước chênh bất thường. Kết quả kiểm in ở đầu báo cáo.
- **Sản phẩm:** phần "Chất lượng dữ liệu" trong báo cáo.

### Bài Q3.4 — Tính số
- **Làm:** **[Không code]** pivot/SUMIFS trên tab riêng, khóa công thức. **[Code]** script tính theo từ điển chỉ số. Đối chiếu một lần với báo cáo làm tay của tháng trước.
- **Sản phẩm:** bảng số tuần + biên bản đối chiếu (khớp/không khớp, vì sao).

### Bài Q3.5 — AI viết nhận xét, code kiểm số
- **Làm:** đưa AI bảng số (vài chục ô) + từ điển chỉ số + yêu cầu: chỉ dùng số trong bảng, nêu 3 điểm đáng chú ý, không dự báo. Code trích mọi con số trong lời và so với bảng.
- **Sản phẩm:** báo cáo hoàn chỉnh + dòng "kiểm số: đạt/không đạt".

### Bài Q3.6 — Hỏi đáp số liệu có kiểm soát
- **Làm:** khi quản lý hỏi câu ngoài báo cáo ("tháng này khách mới mua bao nhiêu?"), dùng công cụ chạy code của AI trên bản sao dữ liệu đã che; yêu cầu hiện code; người đọc phần lọc. Ghi câu hỏi hay gặp thành chỉ số mới trong từ điển (Q3.1).
- **Sản phẩm:** sổ "câu hỏi số liệu" + chỉ số được bổ sung.

### Bài Q3.7 — Người duyệt và gửi
- **Làm:** người duyệt xem phần chất lượng dữ liệu, bảng số, lời nhận xét; bấm gửi. Nếu kiểm số không đạt, không gửi.
- **Sản phẩm:** báo cáo gửi đúng hạn 4 tuần liên tục.

## 5) Đường không code vs có code; khi nào buộc chuyển

| | Không code | Có code |
|---|---|---|
| Tính số | Pivot, SUMIFS, QUERY trong Sheets; báo cáo có sẵn của phần mềm bán hàng | Script Python/Apps Script theo từ điển chỉ số |
| Viết nhận xét | Dán bảng số (không dán dữ liệu thô) vào Project/Gem có hướng dẫn cố định | Gọi API với bảng số, kiểm số tự động |
| Kiểm số | Người đối chiếu từng số với bảng | Code (mẫu dưới) |

**Buộc chuyển sang code [Đề xuất] khi:** dữ liệu từ ≥2 nguồn phải ghép; cần kiểm trùng/thiếu tự động; báo cáo chạy hằng ngày; cần lưu lịch sử để so sánh tuần.

**Code mẫu (đã chạy thử 2026-11-11 bằng `python -I`, hàm giả thay mô hình).** Kết quả: phát hiện 1 dòng trùng `DH00003` và 1 dòng thiếu doanh thu `DH00005`; tính tổng hoàn thành 2.450.000 đồng (không cộng đơn hủy); lời AI có con số bịa "2,500,000" bị chặn.

```python
import csv, io, re
from collections import defaultdict

def doc_va_kiem(text):                      # kiểm dữ liệu TRƯỚC khi tính
    rows, loi, thay = [], [], set()
    for i, r in enumerate(csv.DictReader(io.StringIO(text)), start=2):
        if r["ma_don"] in thay: loi.append(f"dong {i}: trung ma {r['ma_don']}"); continue
        thay.add(r["ma_don"])
        if not r["doanh_thu"].strip(): loi.append(f"dong {i}: thieu doanh_thu {r['ma_don']}"); continue
        r["doanh_thu"] = int(r["doanh_thu"]); rows.append(r)
    return rows, loi

def tong_hop(rows):                         # code tính, theo từ điển chỉ số
    theo_kenh = defaultdict(int)
    for r in rows:
        if r["trang_thai"] == "hoan_thanh": theo_kenh[r["kenh"]] += r["doanh_thu"]
    return {"tong": sum(theo_kenh.values()), **{f"kenh_{k}": v for k, v in theo_kenh.items()}}

def kiem_so_trong_loi(text, so):            # mọi số trong lời AI phải có trong bảng
    cho_phep = {f"{v:,}" for v in so.values()}
    return [x for x in re.findall(r"\d{1,3}(?:,\d{3})+", text) if x not in cho_phep]
```

Giới hạn của bộ kiểm số: chỉ bắt số có dấu phân cách hàng nghìn; không bắt phần trăm, "2,5 triệu", hay số viết bằng chữ. Cần mở rộng theo cách viết của công ty. Nó cũng không bắt lỗi diễn giải ("tăng" khi thật ra giảm); phần đó người duyệt xem.

## 6) Tiêu chí lên Q4 (đo được) [Đề xuất]

1. Báo cáo tự sinh đúng hạn ≥4 tuần liên tục; mỗi tuần có phần chất lượng dữ liệu.
2. Đối chiếu với báo cáo làm tay ≥1 kỳ: mọi chỉ số khớp hoặc chênh đã giải thích.
3. 0 con số không có nguồn lọt qua người duyệt trong 4 tuần (đo bằng bộ kiểm số + người duyệt ghi lại).
4. Thời gian làm báo cáo (kể cả duyệt) thấp hơn đo nền.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

**a) Cửa hàng thời trang 2 chi nhánh dùng KiotViet, bán thêm Shopee.** Báo cáo tuần: doanh thu hoàn thành theo chi nhánh và kênh, đơn hủy/trả, top 10 mã hàng, hàng tồn > 60 ngày. Dữ liệu: xuất hóa đơn KiotViet (API hoặc file), file đối soát Shopee. Kiểm: mã đơn trùng giữa hai nguồn, đơn trả hàng có âm không. AI viết 3 điểm đáng chú ý. Không đưa tên, SĐT khách vào AI: bảng số không cần chúng.

**b) Công ty dịch vụ kế toán 10 người làm báo cáo công nợ cho 40 khách hàng doanh nghiệp từ MISA.** Mỗi khách: tổng phải thu, quá hạn theo nhóm tuổi nợ. Tuổi nợ tính bằng code từ ngày hóa đơn và ngày đến hạn. AI chỉ soạn đoạn nhắc nợ chung theo mẫu, người kiểm từng khách. Rủi ro: số liệu tài chính của khách là bí mật kinh doanh; dùng gói AI có điều khoản không huấn luyện (`../an-toan-du-lieu-va-phap-ly-vn.md` mục 5).

**c) Xưởng mộc 25 người, sản lượng ghi trong Sheets do tổ trưởng nhập.** Kiểm dữ liệu phát hiện cùng một ngày một tổ nhập hai lần (hai tổ trưởng cùng nhập). Đây đúng loại "bản ghi mâu thuẫn" mà TrustDABench cho thấy AI hay cộng dồn. Code đánh dấu, tổ trưởng xác nhận; báo cáo chỉ chạy sau khi hết cờ.

## 8) Tài liệu tham khảo

| Nguồn | Loại | Mức đọc | Tin cậy |
|---|---|---|---|
| SpreadsheetBench 2, arXiv 2606.29955 | Benchmark, NeurIPS 2026 D&B | Toàn văn các mục kết quả, phụ lục lỗi | Cao cho benchmark; bảng tính tài chính lớn hơn bảng SME thường gặp |
| TrustDABench, arXiv 2608.24145 | Benchmark (China Mobile Jiutian) | Toàn văn các mục kết quả | Trung bình-cao; chấm từ chối bằng LLM judge |
| When LLMs Read Tables Carelessly, arXiv 2606.32029 | Nghiên cứu (USC, AWS AI Labs) | Toàn văn | Trung bình-cao; mô hình ≤20B |
| TheAgentCompany, arXiv 2412.14161 | Benchmark | Toàn văn các mục kết quả | Cao cho môi trường giả lập |
| τ-bench, arXiv 2406.12045 | Benchmark | Toàn văn | Cao; mô hình 2024 |
| Claude for Excel is Transformative..., arXiv 2611.00163 | Báo cáo một tác giả | Chỉ tiêu đề và tóm tắt | Thấp; không dùng |

## 9) Chưa kiểm chứng

- Không có nguồn đo AI làm báo cáo trên dữ liệu bán hàng tiếng Việt, số có dấu chấm phân cách hàng nghìn kiểu Việt Nam ("2.450.000"). Bộ kiểm số mẫu dùng dấu phẩy; cần chỉnh.
- Mô hình trong các benchmark (2024-2026) khác mô hình người học dùng; tỷ lệ lỗi sẽ khác. Người học phải tự đo trên báo cáo của mình.
- Công cụ chạy code trong Claude/ChatGPT/Gemini (tên, giới hạn file, nơi lưu file tải lên): chưa đọc tài liệu chính thức trong phiên này.
- Cách lấy dữ liệu từ KiotViet/MISA qua API (xác thực, giới hạn): chưa đọc tài liệu kỹ thuật.
- Ngưỡng 4 tuần, "60 ngày tồn" là đề xuất/giả định.
