# Cấp 2 - Biến tài liệu thành text có cấu trúc

> Ngày soạn: 2026-11-11. Phần "nguyên tắc" bền theo thời gian; phần "thao tác / công cụ" hay đổi, mỗi chỗ có ghi ngày kiểm tra.
> Quy ước: **[Nguồn]** = kết quả có trong nguồn đã đọc (kèm mã tham chiếu ở mục 8). **[Đề xuất]** = ý kiến của nhóm soạn, chưa được nguồn nào kiểm chứng.
> Trạng thái code mẫu: ghi rõ "đã chạy thử" (chạy trong thư mục scratchpad, Python 3.13, `python -I`) hoặc "chưa chạy thử".

---

## 1. Mục tiêu và người đọc

**Người đọc:** chủ SME, kế toán, nhân sự, người phụ trách vận hành ở doanh nghiệp Việt Nam nhỏ; có thể có hoặc không có lập trình viên. Đã dùng AI thủ công (Cấp 0) hoặc gọi API (Cấp 1).

**Sau cấp này, doanh nghiệp có:**
1. Một thư mục `text/` chứa mỗi tài liệu gốc (PDF, Word, Excel, ảnh scan) đã thành một file Markdown (hoặc JSON) sạch, **giữ tiêu đề, danh sách, bảng**, và **mỗi đoạn đều biết đến từ file nào, trang nào**.
2. Một quy trình kiểm chất lượng bằng mẫu (đếm lỗi), không phải "nhìn thấy ổn là ổn".
3. Với hóa đơn/hợp đồng: bản trích trường theo lược đồ JSON, có kiểm tra bằng code (ví dụ tổng tiền khớp).
4. Một bảng chi phí tự tính và một quy tắc "tài liệu nào được phép gửi ra dịch vụ ngoài".

**Không thuộc cấp này:** chia khối, lập chỉ mục, tìm kiếm (Cấp 3 trở đi).

---

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

**Lỗi thường gặp ở Cấp 0-1 dẫn đến Cấp 2:**
- Người dùng kéo cả file PDF vào chat; AI trả lời sai số liệu trong bảng, hoặc bỏ sót trang, mà không ai biết vì không có bản text để đối chiếu.
- Mỗi lần hỏi lại phải tải lại file, tốn token, không tái dùng được; không có "bản chuẩn" của tài liệu.
- File scan/ảnh: AI "đọc" ra chữ nhưng sai dấu tiếng Việt hoặc nhầm số (0/O, 1/l, 5/6) và không báo là không chắc.
- Không biết câu trả lời lấy từ trang nào, nên không kiểm lại được.

**Câu hỏi cấp này trả lời:** "Tài liệu của tôi đã thành text đáng tin chưa, và tôi chứng minh điều đó bằng cách nào?"

**Quy tắc đầu vào [Đề xuất]:** chỉ lên Cấp 2 khi có ít nhất một nhóm tài liệu lặp lại (ví dụ 50 hóa đơn/tháng, một bộ chính sách bán hàng) mà người ta phải đọc lại nhiều lần. Một tài liệu dùng một lần: ở lại Cấp 0.

---

## 3. Kiến thức nền (ngắn)

### 3.1. Ba loại "PDF" và cách phân biệt
| Loại | Dấu hiệu | Cách lấy chữ |
|---|---|---|
| PDF có lớp chữ (born-digital), font Unicode | Bôi đen được chữ, copy ra tiếng Việt đúng | Trích trực tiếp từ lớp chữ (nhanh, gần như không lỗi) |
| PDF có lớp chữ nhưng font cũ (TCVN3, VNI...) | Bôi đen được nhưng copy ra ký tự rác | Xem 3.4; thường nên OCR/mô hình thị giác thay vì giải mã |
| PDF scan / ảnh chụp | Không bôi đen được chữ; mỗi trang là một ảnh | OCR hoặc mô hình thị giác |
| PDF lai | Một số trang có chữ, một số trang là ảnh scan (ví dụ hợp đồng có phụ lục scan) | Quyết định **theo từng trang** |

**[Đề xuất]** Kiểm tra tự động: đếm số ký tự trích được trên mỗi trang; trang gần 0 ký tự thì là ảnh. Mã này **chưa chạy thử** (cần thư viện đọc PDF như `pypdf`; chưa cài trong phiên soạn).

### 3.2. Ba cách biến trang thành chữ
1. **Trích trực tiếp lớp chữ.** Rẻ nhất, chính xác nhất khi có lớp chữ. Không biết gì về bố cục nếu chỉ lấy chuỗi thô.
2. **OCR truyền thống / dịch vụ OCR-bố cục** (ví dụ Tesseract, Azure Document Intelligence Read/Layout, Google Document AI OCR, Mistral OCR). Trả chữ + vị trí + (có dịch vụ) bảng và cấu trúc.
3. **Mô hình thị giác (LLM đọc ảnh).** Tổng quát, hiểu bố cục tốt, nhưng có thể "bịa" chữ trông hợp lý và không cho độ tin cậy từng ký tự. Chi phí theo token.

**[Đề xuất]** Thứ tự ưu tiên: (1) nếu có lớp chữ đúng thì dùng; (2) nếu scan sạch và bảng đơn giản thì OCR/bố cục; (3) nếu bố cục phức tạp, chữ viết tay, bảng lồng thì mô hình thị giác hoặc dịch vụ tài liệu; **luôn** kiểm mẫu.

### 3.3. Định dạng đầu ra
- **Markdown:** đọc được bằng mắt, giữ tiêu đề (`#`), danh sách, bảng (`|`). Phù hợp làm đầu vào Cấp 3.
- **JSON có cấu trúc:** giữ cây khối, vị trí trang, phân cấp mục. Marker và Docling đều xuất JSON **[Nguồn: T2, T1]**. Phù hợp khi cần trỏ ngược về trang/vị trí.
- Bảng phức tạp (ô gộp) thường không biểu diễn tốt bằng Markdown; có thể giữ HTML hoặc JSON cho bảng đó **[Đề xuất]**.

### 3.4. Đặc thù tiếng Việt
- **Dấu:** ký tự có dấu có thể được mã hoá dạng dựng sẵn (NFC) hoặc tổ hợp (NFD). So sánh chuỗi cần chuẩn hoá Unicode trước, nếu không "đúng mà vẫn báo sai". Đã chạy thử: hàm `cer` chuẩn hoá NFC cho kết quả 0 khi so một câu với chính nó ở dạng NFD (mục 4, Bài 2.4).
- **Font cũ (TCVN3/ABC, VNI):** các nguồn cộng đồng cho biết font bắt đầu bằng `.Vn` (ví dụ `.VnTime`) thuộc nhóm TCVN3, font tên bắt đầu `VNI-` thuộc VNI, và copy chữ từ tài liệu dùng font này ra thường thành ký tự sai (mojibake) **[Nguồn: T12; mức tin cậy thấp-trung bình, là trang hướng dẫn cộng đồng, không phải đặc tả]**. Cùng nguồn nêu công cụ chuyển đổi (UniKey Toolkit, UnicodeConverter) và cảnh báo chuyển TCVN3 sang Unicode có thể sai một số chữ hoa. **[Đề xuất]** Với PDF (không phải Word), giải mã ký tự rác thường không đáng tin; coi như PDF scan và OCR lại, rồi kiểm mẫu.
- **Scan chất lượng thấp:** Tesseract có dữ liệu ngôn ngữ `vie`; một nguồn cộng đồng cũ ghi dữ liệu gốc được sinh cho vài font (Times New Roman, Arial, Verdana, Courier New) và các font khác "không tốt lắm" **[Nguồn: T11; cũ, hướng Tesseract 3.x, mức tin cậy thấp]**. Không có số liệu độ chính xác hiện hành trên tài liệu SME Việt Nam trong các nguồn đã đọc.
- **Dịch vụ thương mại:** Azure Document Intelligence (Read và Layout, bản v4.0) liệt kê tiếng Việt (`vi`) trong chữ in; **chữ viết tay** của bản này chỉ liệt kê 12 ngôn ngữ (Anh, Trung giản thể, Pháp, Đức, Ý, Nhật, Hàn, Bồ Đào Nha, Tây Ban Nha, Nga, Thái, Ả Rập), **không có tiếng Việt** **[Nguồn: T7, trang cập nhật 2026-10-19]**. Trang Google Document AI OCR tôi đọc **không nhắc tiếng Việt** (không kết luận được có hay không) **[Nguồn: T8]**.
- **Bảng, chữ ký, con dấu:** chưa có nguồn nào đã đọc đo mức lỗi riêng cho con dấu/chữ ký Việt Nam. **[Đề xuất]** coi chữ ký và con dấu là "vùng đánh dấu có/không", không tin OCR đọc chữ trong con dấu tròn; nếu cần, yêu cầu người xác nhận.

### 3.5. Mô hình thị giác đọc PDF: cách hoạt động và giới hạn (Claude)
Theo tài liệu Anthropic (2026-11-11): với PDF, hệ thống chuyển mỗi trang thành ảnh **và** trích text của từng trang, rồi đưa cả hai cho mô hình; ước lượng text khoảng 1.500-3.000 token mỗi trang tùy độ dày; chi phí ảnh tính như ảnh; giới hạn 128 MB mỗi request trên Claude API trực tiếp của Anthropic (nền tảng khác có thể khác), 600 trang mỗi request (100 trang nếu cửa sổ ngữ cảnh dưới 1M token); có thể tải lên bằng Files API và tham chiếu `file_id` **[Nguồn: T9]**. Tài liệu khuyến nghị đặt PDF trước câu hỏi, dùng font chuẩn, xoay trang cho thẳng, và dùng số trang logic của trình xem PDF khi nhắc tới trang trong prompt **[Nguồn: T9]**.

---

## 4. Chuỗi bài nhỏ

> Mỗi bài chạy độc lập. Làm theo thứ tự lần đầu; về sau chọn bài cần.

### Bài 2.1 - Kiểm kê và phân loại tài liệu
- **Mục tiêu:** biết mình có những loại tài liệu nào, loại nào là "có lớp chữ", "scan", "font cũ".
- **Thực hành:**
  1. Lập bảng (Excel/Google Sheets) mỗi dòng một file: tên file, loại (hóa đơn/hợp đồng/bảng giá/chính sách), số trang, ngày, nhạy cảm? (có/không, xem 2.9).
  2. Mở 5 file mỗi loại, thử bôi đen chữ và copy sang Notepad. Ghi: "copy đúng", "copy ra ký tự rác", "không bôi đen được".
  3. Đánh dấu loại nào hỗn hợp (lai).
- **Sản phẩm:** bảng kiểm kê `kiem_ke.csv` với cột `loai_pdf` (text / scan / font_cu / lai).
- **Lỗi thường gặp:** chỉ thử một file rồi suy ra cả loại; không để ý phụ lục scan trong hợp đồng.

### Bài 2.2 - Chuyển một nhóm tài liệu sang Markdown (đường không code)
- **Mục tiêu:** có file `.md` cho mỗi tài liệu mà không viết code.
- **Thực hành (nguyên tắc, thao tác giao diện thay đổi nhanh, chưa kiểm chứng giao diện hiện tại):**
  1. Chọn một công cụ đọc file có sẵn (Claude / ChatGPT / Gemini bản desktop hoặc web). Tải một tài liệu.
  2. Dùng prompt cố định (ví dụ dưới) để yêu cầu xuất Markdown **nguyên văn**, đánh dấu số trang.
  3. Lưu kết quả vào `text/ten-file.md`.
  4. Với file dài, chia nhỏ theo khoảng trang (ví dụ 10 trang/lần) để không bị cắt cuối.
- **Prompt mẫu [Đề xuất, chưa đo]:**
  ```
  Chép lại toàn bộ trang <a> đến <b> của tài liệu thành Markdown.
  - Giữ NGUYÊN VĂN, không tóm tắt, không sửa lỗi chính tả, không dịch.
  - Tiêu đề dùng # ## ###; danh sách dùng - hoặc 1.; bảng dùng | |.
  - Trước mỗi trang chèn dòng: <!-- trang N -->
  - Chữ không đọc được ghi [không rõ]; KHÔNG đoán.
  ```
- **Sản phẩm:** thư mục `text/` với mỗi file có dòng `<!-- trang N -->`.
- **Lỗi thường gặp:** để AI "sửa chính tả" làm đổi số hoặc tên riêng; không có cờ `[không rõ]` nên AI đoán; mô hình bỏ qua trang giữa khi tài liệu dài (giảm bằng cách chia khoảng trang).

### Bài 2.3 - Chuyển hàng loạt bằng công cụ nguồn mở (đường code nhẹ)
- **Mục tiêu:** chạy một lệnh biến thư mục PDF/Word/Excel thành Markdown/JSON.
- **Công cụ đã xác minh tồn tại và có tài liệu (kiểm tra 2026-11-11):**

| Công cụ | Làm gì | Giấy phép | Lưu ý [Nguồn] |
|---|---|---|---|
| Docling | Đọc PDF, DOCX, PPTX, XLSX, HTML, ảnh...; xuất Markdown, HTML, JSON không mất thông tin; có OCR cho PDF scan/ảnh | MIT | `pip install docling`, Python >= 3.10 **[T1]**. Trang chủ không nêu engine OCR cụ thể và không liệt kê ngôn ngữ OCR **[T1]** |
| Marker | PDF, ảnh, PPTX, DOCX, XLSX, HTML, EPUB sang Markdown/JSON/HTML/chunks; chế độ `--use_llm` gọi dịch vụ LLM để cải thiện (ví dụ gộp bảng qua nhiều trang) | Code Apache 2.0; **trọng số mô hình theo giấy phép riêng**: nghiên cứu/cá nhân/startup dưới 5 triệu USD vốn hoặc doanh thu, ngoài ra phải trả phí | `marker_single file.pdf`; cần PyTorch **[T2]**. SME lớn hơn ngưỡng cần đọc kỹ giấy phép |
| MarkItDown (Microsoft) | Chuyển PDF, Word, Excel, PowerPoint, ảnh, HTML... sang Markdown cho pipeline LLM | MIT | Bản gốc **không mô tả OCR** cho PDF scan; OCR nhờ Azure Document Intelligence hoặc plugin `markitdown-ocr` (dùng mô hình thị giác); README cảnh báo "sanitize your inputs", ưu tiên `convert_local()`/`convert_stream()` hơn `convert()` **[T3]** |

- **Thực hành tối thiểu (Docling, đoạn mã theo README, chưa chạy thử):**
  ```python
  from docling.document_converter import DocumentConverter
  r = DocumentConverter().convert("hoa_don_001.pdf")
  open("text/hoa_don_001.md", "w", encoding="utf-8").write(r.document.export_to_markdown())
  ```
  (Mã trên lấy từ ví dụ trong README Docling **[T1]**; chưa chạy thử vì cần tải mô hình lớn. Cần thử trên 10 file thật của doanh nghiệp trước khi tin.)
- **Sản phẩm:** `text/*.md` (+ `text/*.json` nếu cần vị trí trang).
- **Lỗi thường gặp:** chạy công cụ trên file không tin cậy với quyền cao (xem T3 cảnh báo); không kiểm tra giấy phép trọng số (Marker); tin rằng "đã có OCR" khi công cụ im lặng bỏ qua (MarkItDown-OCR bỏ qua OCR **âm thầm** nếu không cấu hình `llm_client` **[T3]**).

### Bài 2.4 - Kiểm chất lượng trích xuất bằng mẫu (đếm lỗi)
- **Mục tiêu:** có một con số lỗi cho từng loại tài liệu, để quyết định dùng công cụ nào.
- **Thực hành [Đề xuất]:**
  1. Với mỗi loại tài liệu, chọn ngẫu nhiên 10 trang (gồm cả trang xấu nhất).
  2. Người gõ tay/hiệu đính "bản chuẩn" (ground truth) cho 10 trang đó. Đây là việc tốn công nhất, làm một lần và dùng lại.
  3. Tính **CER** (tỷ lệ lỗi ký tự = khoảng cách chỉnh sửa / số ký tự chuẩn) sau khi chuẩn hoá Unicode NFC và khoảng trắng. Tính riêng: (a) số liệu và tiền (b) tên riêng/mã số thuế (c) bảng (đúng/sai từng ô).
  4. Đặt ngưỡng chấp nhận theo rủi ro (ví dụ số tiền: 0 lỗi cho phép, sai thì chuyển người kiểm).
- **Mã mẫu - đã chạy thử** (scratchpad, `python -I`):
  ```python
  import unicodedata
  def lev(a, b):
      prev = list(range(len(b)+1))
      for i, ca in enumerate(a, 1):
          cur = [i]
          for j, cb in enumerate(b, 1):
              cur.append(min(prev[j]+1, cur[j-1]+1, prev[j-1]+(ca != cb)))
          prev = cur
      return prev[-1]
  def cer(truth, pred):
      n = lambda s: unicodedata.normalize("NFC", " ".join(s.split()))
      t, p = n(truth), n(pred)
      return lev(t, p) / max(len(t), 1)
  ```
  Kết quả thử: câu "Hàng đổi trả trong 7 ngày, còn nguyên tem." đối chiếu với bản mất hai dấu ("Hang ... ngay") cho CER = 0,048; đối chiếu với chính nó ở dạng NFD cho CER = 0.
- **Sản phẩm:** bảng `chat_luong.csv`: loại tài liệu | công cụ | số trang mẫu | CER chữ | lỗi số/tiền | lỗi ô bảng | kết luận.
- **Lỗi thường gặp:** so sánh khi chưa chuẩn hoá Unicode; chỉ kiểm trang đẹp; coi CER thấp là đủ trong khi một chữ số sai trong số tiền là lỗi nghiêm trọng (CER không phân biệt).

### Bài 2.5 - Ghi nguồn (tên file, trang) cho mỗi đoạn
- **Mục tiêu:** mỗi đoạn text biết mình thuộc `file` nào, `trang` nào, để Cấp 5 trích dẫn được.
- **Thực hành [Đề xuất]:**
  1. Chuyển từng trang riêng (hoặc dùng chế độ xuất theo trang của công cụ) rồi ghép; hoặc chèn dấu `<!-- trang N -->` như Bài 2.2.
  2. Giữ file nguồn gốc bất biến, đặt tên theo quy ước `LOAI_YYYYMMDD_tenngan.pdf` và tính hash (SHA-256) lưu cạnh bản text. Bài báo đánh giá RAG trên văn bản quy phạm Ấn Độ cũng ghi hash SHA-256 của chính các byte PDF đã dùng trong bản kê corpus **[Nguồn: P5]**; đó là thực hành tốt, nhưng bài báo không đo tác dụng của nó.
  3. Lưu tệp phụ `ten-file.meta.json` gồm `source_file`, `sha256`, `ngay_chuyen`, `cong_cu_va_phien_ban`, `so_trang`.
- **Sản phẩm:** `text/*.md` + `text/*.meta.json`.
- **Lỗi thường gặp:** số trang trong ảnh (số in ở chân trang) khác số trang PDF; thống nhất dùng chỉ số trang của PDF (Anthropic cũng khuyên dùng số trang logic của trình xem PDF khi nhắc trang **[Nguồn: T9]**).

### Bài 2.6 - Trích trường theo lược đồ JSON (hóa đơn, hợp đồng) và kiểm bằng code
- **Mục tiêu:** từ hóa đơn sang JSON cố định, và tự động phát hiện bản trích sai.
- **Thực hành [Đề xuất]:**
  1. Định nghĩa lược đồ trường (ví dụ hóa đơn): `so_hoa_don`, `ngay`, `ma_so_thue_nguoi_ban`, `dong_hang[] {ten, so_luong, don_gia}`, `tong_truoc_thue`, `thue_suat`, `tien_thue`, `tong_thanh_toan`.
  2. Dặn mô hình (hoặc dịch vụ trích hóa đơn) chỉ trả JSON đúng lược đồ; trường không thấy thì `null`.
  3. Chạy **kiểm tra bằng code**, không dùng mô hình để tự kiểm: (a) tổng `so_luong × don_gia` = `tong_truoc_thue`; (b) `tong_truoc_thue × thue_suat` ≈ `tien_thue` (cho phép lệch làm tròn 1 đồng); (c) `tong_truoc_thue + tien_thue = tong_thanh_toan`; (d) mã số thuế có 10 hoặc 13 chữ số. Hóa đơn nào không qua thì vào hàng đợi người kiểm.
  4. Dịch vụ lớn có mô hình hóa đơn dựng sẵn (ví dụ Azure có mô hình Invoice; một ghi chú phát hành cũ cho biết đã thêm locale `vi` và mã VND cho mô hình này **[Nguồn: T6, thứ cấp qua kết quả tìm kiếm, chưa đọc trang gốc; cần xác minh]**).
- **Mã mẫu kiểm - đã chạy thử** (scratchpad, `python -I`):
  ```python
  from decimal import Decimal as D
  def check(inv):
      e = []
      s = sum(D(str(l["so_luong"])) * D(str(l["don_gia"])) for l in inv["dong_hang"])
      if s != D(str(inv["tong_truoc_thue"])): e.append("tong dong != tong_truoc_thue")
      vat = (D(str(inv["tong_truoc_thue"])) * D(str(inv["thue_suat"])) / 100).quantize(D(1))
      if abs(vat - D(str(inv["tien_thue"]))) > 1: e.append("VAT lech")
      if D(str(inv["tong_truoc_thue"])) + D(str(inv["tien_thue"])) != D(str(inv["tong_thanh_toan"])):
          e.append("tong thanh toan lech")
      if len(str(inv.get("ma_so_thue", "")).replace("-", "")) not in (10, 13): e.append("MST la")
      return e
  ```
  Thử với hóa đơn đúng (10×150.000 + 2×500.000 = 2.500.000; VAT 8% = 200.000; tổng 2.700.000) trả `[]`; với bản cố ý sai tổng trả ba lỗi: tổng dòng, VAT, tổng thanh toán. **Lưu ý:** thuế suất và quy định hóa đơn điện tử Việt Nam thay đổi; con số 8% chỉ là ví dụ minh hoạ, chưa đối chiếu quy định hiện hành.
- **Sản phẩm:** `hoa_don_json/*.json`, `hang_doi_kiem.csv`, tỷ lệ qua kiểm tự động.
- **Lỗi thường gặp:** mô hình tự "sửa" cho tổng khớp; quên hóa đơn nhiều thuế suất; làm tròn từng dòng khác làm tròn tổng (cần quy ước và kiểm theo quy ước đó); dấu `.` và `,` trong số Việt Nam (1.500.000 vs 1,5) bị đọc sai thành số thập phân.

### Bài 2.7 - Chi phí và cách tự tính
- **Mục tiêu:** biết trước chi phí chuyển đổi một kho tài liệu.
- **Công thức [Đề xuất]:** `chi_phi = so_trang × (chi phí_mỗi_trang)` + công người kiểm. Chi phí mỗi trang:
  - Trích trực tiếp / công cụ nguồn mở chạy máy mình: 0 tiền dịch vụ; tốn thời gian máy và công cài.
  - Dịch vụ OCR theo trang: giá niêm yết/1.000 trang. Ví dụ đã đọc: Mistral OCR 4.1 là 4 USD/1.000 trang, OCR 3 là 2 USD/1.000 trang (trang giá docs.mistral.ai, **2026-11-11**) **[Nguồn: T10]**. Giá thay đổi (một nguồn thứ cấp báo giá OCR tăng từ 2 lên 4 USD vào tháng 7/2026, chưa xác minh **[T10b]**).
  - Mô hình thị giác theo token: tài liệu Anthropic ước 1.500-3.000 token text mỗi trang cộng chi phí ảnh theo token; dùng công cụ đếm token để đo trên mẫu **[Nguồn: T9]**. Nhân với giá token hiện hành trên trang giá của nhà cung cấp (giá không được đọc trong phiên này).
- **Cách làm:** chạy thử 20 trang đại diện, đo chi phí thật, nhân lên. Tính cả **công người kiểm** vì thường lớn hơn tiền dịch vụ.
- **Sản phẩm:** bảng `chi_phi.xlsx` có ô giả định (giá, số trang, tỷ lệ phải kiểm lại).
- **Lỗi thường gặp:** quên rằng PDF dày đặc có thể làm tràn ngữ cảnh trước khi đủ số trang cho phép (Anthropic khuyên chia nhỏ **[T9]**); quên chạy lại khi tài liệu đổi.

### Bài 2.8 - Chọn công cụ bằng thử đối chiếu (bake-off nhỏ)
- **Mục tiêu:** chọn công cụ cho từng loại tài liệu bằng số đo, không bằng quảng cáo.
- **Thực hành [Đề xuất]:** lấy 10 trang mẫu của Bài 2.4; chạy 2-3 công cụ (ví dụ Docling, một dịch vụ OCR, một mô hình thị giác); điền cùng một bảng `chat_luong.csv`; chọn công cụ rẻ nhất thỏa ngưỡng. Một nghiên cứu khác cho biết khi ghép parser với chunker thì "parser tốt nhất" không dự đoán được từ xếp hạng riêng từng thành phần **[Nguồn: P5, một corpus, bốn văn bản quy phạm tiếng Anh]**, nên đừng chọn parser chỉ theo bảng xếp hạng chung.
- **Sản phẩm:** một dòng quyết định cho mỗi loại tài liệu: "Hóa đơn scan: công cụ X; Hợp đồng text: trích trực tiếp; Bảng giá Excel: đọc trực tiếp".
- **Lỗi thường gặp:** chọn theo một trang đẹp; không ghi phiên bản công cụ (công cụ đổi, kết quả đổi).

### Bài 2.9 - Bảo mật khi gửi tài liệu lên dịch vụ ngoài
- **Mục tiêu:** có quy tắc rõ "loại nào được gửi, loại nào không".
- **Thực hành [Đề xuất]:**
  1. Phân hạng: (A) công khai (bảng giá công bố, catalogue) - được gửi; (B) nội bộ thường (chính sách bán hàng, SOP) - gửi được qua tài khoản doanh nghiệp đã đọc điều khoản dữ liệu; (C) nhạy cảm (hợp đồng có giá, lương, hồ sơ cá nhân, CCCD, tài khoản ngân hàng) - chỉ chạy công cụ **chạy trên máy mình** (Docling/Marker mô hình cục bộ) hoặc che thông tin trước.
  2. Với mỗi dịch vụ, đọc và ghi lại: dữ liệu có dùng để huấn luyện không, lưu bao lâu, vùng lưu. Các điều khoản này **không được đọc trong phiên soạn**; ghi vào mục 9.
  3. Che (mask) trước khi gửi: thay số tài khoản, CCCD, tên bằng mã giữ riêng bảng đối chiếu.
  4. Nhắc trong tài liệu Anthropic: HIPAA chỉ áp dụng cho PDF gửi inline qua Messages API, không qua Files API **[Nguồn: T9]**; ví dụ cho thấy điều kiện tuân thủ phụ thuộc kênh gửi, nên đọc điều khoản đúng kênh dùng.
  5. Quy định pháp lý về dữ liệu cá nhân ở Việt Nam: **chưa kiểm chứng trong phiên này**, xem mục 9.
- **Sản phẩm:** `chinh_sach_gui_tai_lieu.md` một trang + cột "hạng" trong bảng kiểm kê.
- **Lỗi thường gặp:** nhân viên dùng tài khoản cá nhân miễn phí cho tài liệu hạng C; không ghi lại ai gửi gì lên đâu.

---

## 5. Đường không code vs đường có code; khi nào buộc phải chuyển

| Việc | Không code | Có code |
|---|---|---|
| Vài chục tài liệu, dùng định kỳ | Bài 2.2 (dán/tải lên, prompt cố định) | Không cần |
| Hàng trăm đến hàng nghìn trang, lặp lại | Rất tốn công và dễ sót trang | Bài 2.3 (Docling/Marker/MarkItDown) |
| Kiểm chất lượng | Chấm tay bằng bảng tính | Bài 2.4 (CER bằng code) |
| Trích hóa đơn/hợp đồng | Dán vào chat, copy kết quả vào bảng tính; kiểm tổng bằng công thức Excel | Bài 2.6 (lược đồ JSON + kiểm bằng code) |

**Buộc chuyển sang code khi [Đề xuất]:** (a) hơn khoảng 200 trang cần chuyển mỗi tháng, hoặc (b) cần chạy lại hằng tuần, hoặc (c) cần kiểm tự động tổng tiền cho hơn khoảng 50 hóa đơn mỗi tháng, hoặc (d) cần giữ tài liệu hạng C ở trong máy. Các ngưỡng là ước lượng của nhóm soạn, **chưa có nguồn**; điều chỉnh theo thời gian người kiểm thực tế.

---

## 6. Tiêu chí lên Cấp 3 (đo được)

Chỉ lên Cấp 3 (chia khối, lập chỉ mục) khi **tất cả** thỏa trên bộ mẫu của doanh nghiệp **[Đề xuất; các ngưỡng là gợi ý, điều chỉnh theo rủi ro]**:
1. 100% tài liệu mục tiêu có file `.md` và file `.meta.json` (nguồn, hash, phiên bản công cụ).
2. Trên mẫu 10 trang mỗi loại: CER chữ không quá ngưỡng bạn đặt (ví dụ 2%); **0 lỗi** số tiền/mã số/ngày trong mẫu; bảng đúng từng ô trên mẫu.
3. Mỗi đoạn truy ngược được về (file, trang); kiểm bằng cách bốc ngẫu nhiên 20 đoạn và mở đúng trang gốc, đúng 20/20.
4. Với hóa đơn/hợp đồng cần trích: tỷ lệ qua kiểm bằng code và tỷ lệ phải chuyển người kiểm đã được đo; không có trường nào "tự sửa cho khớp".
5. Có bảng chi phí và chính sách gửi tài liệu được người có thẩm quyền duyệt.

Nếu chưa đạt: ở lại Cấp 2, đổi công cụ (Bài 2.8) hoặc cải thiện nguồn (xin file gốc Word/Excel thay vì scan).

---

## 7. Ví dụ cho SME Việt Nam

| Tài liệu | Dạng thường gặp | Cách xử lý đề xuất [Đề xuất] | Kiểm |
|---|---|---|---|
| Hóa đơn đầu vào | PDF/XML từ nhà cung cấp; ảnh chụp | Nếu có file XML/PDF text thì trích trực tiếp; ảnh chụp thì OCR/thị giác; trích JSON | Tổng tiền, VAT, MST (Bài 2.6) |
| Hợp đồng | PDF text + phụ lục scan, có chữ ký/con dấu | Quyết định theo từng trang; chữ ký/con dấu chỉ đánh dấu có/không | Mẫu điều khoản chính: giá, thời hạn, phạt |
| Bảng giá | Excel/PDF xuất từ Excel; bảng nhiều ô | Ưu tiên đọc Excel gốc; nếu PDF thì giữ Markdown/HTML cho bảng | Đối chiếu 20 dòng ngẫu nhiên với Excel |
| Chính sách bán hàng | Word/PDF văn bản nhiều cấp tiêu đề | Chuyển Markdown giữ cấp tiêu đề (đầu vào quan trọng cho Cấp 3) | Đếm tiêu đề và số mục so với bản gốc |
| Báo cáo/đơn từ cũ | Font TCVN3/VNI | Coi như scan; OCR lại; kiểm mẫu | CER mẫu |

---

## 8. Tài liệu tham khảo

Ngày truy cập tất cả: **2026-11-11**. "Mức tin cậy" là đánh giá của nhóm soạn về độ ổn định/độ kiểm chứng của nguồn.

**Công cụ và tài liệu**
- **T1.** Docling (docling-project) - README. https://github.com/docling-project/docling . Loại: tài liệu/repo. Tin cậy: cao cho tính năng nêu trong README; chưa chạy thử.
- **T2.** Marker (datalab-to) - README. https://github.com/datalab-to/marker . Loại: tài liệu/repo. Tin cậy: cao cho tính năng; giấy phép trọng số cần đọc bản gốc.
- **T3.** MarkItDown (Microsoft) - README. https://github.com/microsoft/markitdown . Loại: tài liệu/repo. Tin cậy: cao.
- **T6.** Ghi chú phát hành Azure Document Intelligence (what's new). https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/whats-new . Loại: tài liệu. Tin cậy: trung bình (chỉ thấy qua tóm tắt tìm kiếm, chưa đọc trang gốc).
- **T7.** Azure Document Intelligence - ngôn ngữ cho Read và Layout (v4.0). https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/language-support/ocr . Loại: tài liệu. Tin cậy: cao (đọc trực tiếp, trang cập nhật 2026-10-19).
- **T8.** Google Document AI - Enterprise Document OCR. https://docs.cloud.google.com/document-ai/docs/process-documents-ocr . Loại: tài liệu. Tin cậy: cao cho phần đã đọc; trang không nêu danh sách ngôn ngữ.
- **T9.** Anthropic - PDF support. https://platform.claude.com/docs/en/build-with-claude/pdf-support . Loại: tài liệu. Tin cậy: cao; thay đổi nhanh.
- **T10.** Mistral - bảng giá API (OCR). https://docs.mistral.ai/inference/pricing . Loại: tài liệu giá. Tin cậy: cao tại ngày đọc; giá đổi nhanh.
- **T10b.** Theo dõi giá bên thứ ba về việc tăng giá OCR tháng 7/2026 (qua tìm kiếm). https://www.usagepricing.com/blueprint/activity/mistral-ai-2026-07-06-api-rate-increase . Loại: nguồn thứ cấp. Tin cậy: thấp, chưa xác minh.
- **T11.** Nhóm VietOCR / Tesseract tiếng Việt (hướng dẫn cộng đồng, cũ). https://vietunicode.sourceforge.net/howto/tesseract-ocr.html . Loại: hướng dẫn cộng đồng. Tin cậy: thấp (cũ, Tesseract 3.x).
- **T12.** Hướng dẫn chuyển font cũ TCVN3/VNI sang Unicode (UniKey/UnicodeConverter). https://vietunicode.sourceforge.net/howto/unicodeconversion.html và https://search.r-project.org/CRAN/refmans/vietnameseConverter/html/decodeVN.html . Loại: hướng dẫn/tài liệu gói R. Tin cậy: thấp-trung bình.

**Bài báo**
- **P5.** Singh, S. K. "Parser, Chunking, and Embedding Interactions in RAG over Indian Government Regulatory Documents", arXiv:2609.31660 (09/2026). https://www.alphaxiv.org/abs/2609.31660 . Loại: bài báo (chưa phản biện, một tác giả). Tin cậy: trung bình; bốn văn bản tiếng Anh, câu hỏi do LLM sinh.

---

## 9. Chưa kiểm chứng / cần kiểm tra lại

1. **Độ chính xác OCR/thị giác trên tài liệu SME Việt Nam** (hóa đơn chụp điện thoại, scan mờ, con dấu, chữ ký, chữ viết tay tiếng Việt): không có số liệu từ nguồn đã đọc. Cần tự đo (Bài 2.4, 2.8).
2. **Google Document AI có hỗ trợ tiếng Việt hay không:** trang đã đọc không nhắc; cần xem danh sách ngôn ngữ riêng của dịch vụ.
3. **Azure mô hình Invoice hỗ trợ locale `vi`/VND:** chỉ từ ghi chú phát hành cũ qua tìm kiếm; cần đọc trang mô hình Invoice hiện hành.
4. **Docling và Marker chạy với tiếng Việt scan:** README Marker nói OCR đa ngôn ngữ, README Docling không nêu ngôn ngữ; chưa chạy thử. Cần thử trên mẫu thật.
5. **Giá và điều khoản dữ liệu của các dịch vụ** (lưu bao lâu, có huấn luyện không, vùng lưu): chưa đọc điều khoản của bất kỳ nhà cung cấp nào. Phải đọc trước khi gửi tài liệu hạng B/C.
6. **Pháp lý Việt Nam về dữ liệu cá nhân và hóa đơn điện tử:** chưa kiểm chứng; cần hỏi luật sư/kế toán trưởng, không dùng mục này làm căn cứ.
7. **Thao tác giao diện** của Claude/ChatGPT/Gemini (tải file, giới hạn số trang): chưa kiểm chứng; chỉ phần API/Claude PDF đã đọc ở T9.
8. **Ngưỡng ở mục 5 và mục 6** (số trang/tháng, CER 2%): ước lượng của nhóm soạn, chưa có nguồn.
9. **Mã mẫu PDF có/không lớp chữ** (Bài 2.1) và **Docling/MarkItDown/Marker** trong Bài 2.3: **chưa chạy thử**. Chỉ `cer` và `check_invoice` đã chạy thử.
10. **Chi phí token mô hình thị giác theo trang cho tiếng Việt:** nguồn chỉ cho khoảng 1.500-3.000 token text/trang chung; chưa đo cho tiếng Việt (tiếng Việt thường tốn token hơn tiếng Anh là giả thuyết, chưa kiểm).
