# Cấp 5 — Trả lời có trích dẫn (Grounded answers with citations)

> Trạng thái: bản nháp nghiên cứu, ngày truy cập nguồn 2026-11-11.
> Quy ước: **[Nguồn]** = có trong nguồn đã đọc; **[Đề xuất]** = ý kiến nhóm biên soạn; **[Đã chạy thử]** / **[Chưa chạy thử]** cho code.

---

## 1) Mục tiêu và người đọc

**Người đọc:** chủ/quản lý SME và người làm IT kiêm nhiệm; đã qua C4 (có công cụ tìm và bộ câu hỏi vàng có số đo recall@k).

**Mục tiêu:** AI chỉ trả lời từ các khối tìm được, **ghi rõ nguồn** (mã tài liệu, mục, trích nguyên văn), **từ chối** khi không đủ căn cứ, và doanh nghiệp có cách **đo** tỷ lệ trả lời có căn cứ.

**Sản phẩm cầm đi được:** (a) một mẫu prompt "chỉ trả lời từ nguồn" đã thử; (b) định dạng câu trả lời chuẩn (câu trả lời + nguồn + trích nguyên văn hoặc "không đủ căn cứ"); (c) một script kiểm trích nguyên văn (đường code) hoặc quy trình kiểm tay (đường không code); (d) bảng điểm groundedness/từ chối đúng trên bộ câu hỏi vàng mở rộng.

---

## 2) Câu hỏi cấp này trả lời / lỗi của cấp trước dẫn đến cấp này

**Câu hỏi:** "AI nói thế, căn cứ ở đâu — và nếu tài liệu không nói thì AI có dám nói 'không biết' không?"

**Lỗi của C4 dẫn đến C5:**
- Tìm đúng khối nhưng AI vẫn "nói thêm" từ trí nhớ của nó (ví dụ bịa thời hạn bảo hành theo thông lệ).
- Nhân viên không có cách kiểm: đọc câu trả lời trôi chảy thì tin.
- Câu hỏi không có đáp án trong tài liệu vẫn nhận câu trả lời tự tin.
- Hai tài liệu mâu thuẫn hoặc bản cũ lẫn bản mới mà AI chọn bừa.

---

## 3) Kiến thức nền (ngắn, chính xác)

### 3.1 Bốn lớp bảo vệ, từ rẻ đến chặt
1. **Prompt:** nói rõ chỉ dùng tài liệu cho trước, được phép nói "không biết", và nếu cần thì rút trích dẫn nguyên văn trước rồi mới trả lời. Anthropic nêu các kỹ thuật cơ bản: cho phép Claude nói "I don't know"; với tài liệu dài (>20k token) yêu cầu trích nguyên văn trước khi làm việc; yêu cầu trích dẫn cho mỗi khẳng định và rút lại khẳng định nếu không tìm được trích dẫn; hạn chế dùng kiến thức bên ngoài. Cùng trang cảnh báo các kỹ thuật này giảm đáng kể nhưng **không loại bỏ hoàn toàn** hallucination. **[Nguồn: Anthropic, "Reduce hallucinations"]**
2. **Tính năng trích dẫn của nhà cung cấp (nếu có).** API Messages của Anthropic có tính năng Citations: bật trên tài liệu bạn đưa vào, phản hồi trả về trích đoạn kèm vị trí ký tự/trang; trường `cited_text` không tính vào token đầu ra; và nhà cung cấp nói trích dẫn "được đảm bảo có con trỏ hợp lệ" tới tài liệu đã cung cấp. Citations **không dùng chung** với structured outputs (API trả lỗi 400 nếu bật cả hai). **[Nguồn: Anthropic, tài liệu Citations, đọc 2026-11-11]** Đây là chi tiết sản phẩm, dễ đổi (xem mục 9).
3. **Kiểm bằng code (validator):** chỉ chấp nhận trích dẫn là **chuỗi con nguyên văn** của khối đã cấp. Mẫu của Airbnb: mỗi đoạn trích phải là substring của bài nguồn được cite, "chính xác sau khi chuẩn hóa dấu câu Unicode và khoảng trắng — đó là mức nới duy nhất", nếu một đoạn sai thì **từ chối ghi cả bản trả lời**; kết quả báo cáo: 99,7% đoạn trích khớp từng byte trước chuẩn hóa và 100% đạt ràng buộc sau chuẩn hóa (mẫu 1.769 đoạn trên 132 ca); số lần từ chối/thử lại không được ghi lại. Tác giả nhấn mạnh đây là "ranh giới tin cậy" do code ép, không phải do prompt. **[Nguồn: Airbnb arXiv 2610.14428, mục 3, 7, phụ lục D]**
4. **Đo và con người duyệt:** đo bằng bộ câu hỏi vàng + LLM judge (hoặc người), và để người duyệt các trường hợp rủi ro cao. Airbnb áp dụng người duyệt mọi ca và nói rõ kết luận chỉ áp dụng cho kho tài liệu đã biên tập kỹ và quy trình chấp nhận độ trễ. **[Nguồn: Airbnb, tóm tắt]**

**Giới hạn cần nhớ của lớp 3:** validator chứng minh "câu trích có thật trong khối đó"; **không** chứng minh "câu trích thật sự ủng hộ câu trả lời" và không chứng minh "khối đó còn hiệu lực". Hai việc sau cần lớp 4 và metadata (mục 4, bài 5.6, 5.7).

### 3.2 Đo hallucination / groundedness
- **RAGAS** (Es và cộng sự, arXiv 2309.15217) — khung đánh giá RAG không cần đáp án tham chiếu, ba chiều: **Faithfulness** (các phát biểu trong câu trả lời có suy ra được từ ngữ cảnh không), **Answer relevance** (câu trả lời có đúng câu hỏi không), **Context relevance** (ngữ cảnh có gọn không). **[Nguồn: RAGAS mục 3]**
  - Cách tính Faithfulness: LLM tách câu trả lời thành các phát biểu ngắn; LLM kiểm từng phát biểu có được ngữ cảnh ủng hộ không; điểm = số phát biểu được ủng hộ / tổng số phát biểu. **[Nguồn: RAGAS mục 3]**
  - Độ khớp với người trên bộ WikiEval (do tác giả tạo, 50 trang Wikipedia, tiếng Anh, dùng gpt-3.5-turbo-16k làm LLM chấm): Faithfulness 0,95; Answer relevance 0,78; Context relevance 0,70 (độ chính xác khi so cặp). **[Nguồn: RAGAS bảng 1]** Hạn chế: dữ liệu tiếng Anh, phiên bản tác giả dùng mô hình cũ, bộ nhỏ; **chưa có bằng chứng tôi đã đọc về độ tin cậy trên tiếng Việt**. Ở các mục sau của bài, tác giả cũng nói context relevance khó chấm nhất.
  - Tên hàm/thư viện `ragas` hiện hành có thể khác bài báo: **[Chưa kiểm chứng]** (chưa đọc tài liệu thư viện). Dùng ý tưởng, đừng chép tên API từ đây.
- **Cách tự làm, rẻ, không cần thư viện [Đề xuất, theo ý tưởng của RAGAS và Airbnb]:** với mỗi câu trả lời, chấm hai lỗi riêng:
  1. *Trích sai*: validator bắt được (nhị phân, chạy bằng code, 100% lặp lại).
  2. *Phát biểu không có căn cứ*: LLM judge hoặc người đọc từng phát biểu đối chiếu khối. Để giảm dao động của judge, Airbnb dùng **đa số 3 lần chấm** (mỗi metric là nhị phân, chạy 3 lần lấy đa số). **[Nguồn: Airbnb phụ lục A, D]**
- **Hai số cần tách, vì chỉ ra nơi cần sửa:** Airbnb dùng cặp (đúng quy trình) và (đủ bằng chứng nguyên văn): khoảng cách giữa hai số cho biết việc tiếp theo thuộc về tác tử hay kho tài liệu; phần thất bại còn lại **chủ yếu do tài liệu thiếu nội dung** chứ không do tìm/sinh (phân tích định tính của tác giả, chưa có thống kê từng loại). **[Nguồn: Airbnb mục 1, 7]**

### 3.3 Ngữ cảnh nhiều khối và vị trí
- Đưa quá nhiều khối không giúp mãi: hiệu năng bão hòa trước recall của bộ tìm (50 tài liệu thay 20 chỉ tăng ~1–1,5%), và thông tin ở giữa ngữ cảnh dài bị dùng kém hơn thông tin ở đầu/cuối (mô hình 2023). **[Nguồn: arXiv 2307.03172]** **[Đề xuất]** giữ 3–8 khối, đặt khối xếp hạng cao ở đầu; đo lại trên mô hình đang dùng.
- Cùng bài đó: đặt câu hỏi cả trước và sau tài liệu (query-aware) cải thiện mạnh tác vụ khóa-giá trị tổng hợp nhưng thay đổi rất ít ở QA nhiều tài liệu. **[Nguồn: arXiv 2307.03172 mục 4.2]** — không nên kỳ vọng mẹo này sửa được lỗi RAG.

### 3.4 Đánh đổi độ trễ / chi phí
- **[Nguồn: Airbnb]** Cách đọc-nhiều-lần của họ mất ~90 giây mỗi ca so với ~8–9 giây của trợ lý sản xuất; tác giả nói rõ không tuyên bố lợi thế độ trễ, và ca dùng là quy trình chịu được độ trễ, có người duyệt. Mỗi ca trung vị ~5 truy vấn + 6 lần lấy bài.
- **[Nguồn: Anthropic Contextual Retrieval]** Prompt caching giảm độ trễ >2 lần và chi phí tới 90% khi một ngữ cảnh lớn được dùng lại.
- **[Đề xuất]** Mỗi bước thêm (viết lại câu hỏi, tìm nhiều vòng, judge kiểm lại, trích rồi trả lời hai lượt) cộng thêm độ trễ và token; áp dụng theo mức rủi ro (xem bảng ở bài 5.8).
- Truy xuất nhiều mức (nhanh/thường/sâu) theo kiểu SAP: **[Chưa kiểm chứng trong tài liệu này]** — tôi chưa đọc bài SAP arXiv 2608.00122; chỉ ghi nhận theo bối cảnh dự án.

---

## 4) Chuỗi bài nhỏ

### Bài 5.1 — Mẫu prompt "chỉ từ nguồn" + quyền từ chối
- **Mục tiêu:** AI chỉ trả lời từ các khối được cấp, và nói "không đủ căn cứ" khi cần.
- **Thực hành:** (1) lấy 5 câu hỏi từ bộ vàng C4 có đáp án và 5 câu không đáp án; (2) cấp khối bằng cách dán (đường không code) hoặc từ C4 (đường code); (3) dùng mẫu sau, chạy 10 câu, chép kết quả vào bảng:

```text
Bạn là trợ lý tra cứu nội bộ. CHỈ dùng các khối <nguon> bên dưới. Không dùng kiến thức bên ngoài.
Quy tắc:
1. Mỗi ý trong câu trả lời phải kèm [mã khối] và một trích dẫn NGUYÊN VĂN từ khối đó (không diễn đạt lại trong phần trích dẫn).
2. Nếu các khối không đủ để trả lời, chỉ trả lời đúng một câu: "Không đủ căn cứ trong tài liệu." và nêu thiếu thông tin gì.
3. Nếu các khối mâu thuẫn, nêu cả hai kèm [mã khối] và ngày hiệu lực, không tự chọn.
4. Nếu khối đã hết hiệu lực (ngày hết hiệu lực < hôm nay), nói rõ.
Hôm nay: {ngay}
<nguon>
[BH-01 | hiệu lực đến: không | cập nhật: 2026-09-01]
...văn bản khối...
</nguon>
Câu hỏi: {cau_hoi}
Trả lời theo mẫu: TRẢ LỜI: ... / NGUỒN: [mã khối] "trích nguyên văn" ...
```
- **Sản phẩm:** prompt chuẩn + bảng 10 câu (trả lời đúng / sai / từ chối đúng / từ chối thừa / bịa).
- **Lỗi thường gặp:** chỉ nói "hãy trả lời chính xác" mà không cấp lối thoát "không đủ căn cứ" (Anthropic: cho phép nói không biết là một trong những kỹ thuật cơ bản **[Nguồn]**); nhồi 20 khối; không ghi ngày hôm nay (để xử lý hết hiệu lực); để AI "tóm tắt" trong phần trích dẫn.

### Bài 5.2 — Trích dẫn nguyên văn: tự kiểm bằng code (validator)
- **Mục tiêu:** từ chối tự động mọi câu trả lời có trích dẫn không có trong khối đã cấp.
- **Thực hành:** yêu cầu AI trả JSON `{status, answer, citations:[{chunk_id, quote}]}`; chạy validator; nếu lỗi → gửi lại cho AI kèm danh sách lỗi (tối đa 2 lần), sau đó ghi "không đủ căn cứ" hoặc đẩy cho người. Validator dưới đây theo ý tưởng của Airbnb (substring sau chuẩn hóa Unicode/khoảng trắng), thêm hai kiểm tra do chúng tôi đề xuất: nhánh từ chối hợp lệ và ngày hết hiệu lực của khối.

```python
# validate2.py — [Đã chạy thử] Python 3.13, `python -I -X utf8`; 5 ca thử: đúng, trích sai, khối hết hạn, từ chối, thiếu trích dẫn
import re, unicodedata
from datetime import date

def _n(s):
    s = unicodedata.normalize("NFC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()

def validate(out, chunks, today=None, min_len=15):
    """chunks = {id: {"text": str, "valid_to": "YYYY-MM-DD" | None}}"""
    errs, today = [], today or date.today().isoformat()
    if out.get("status") == "refused":
        return errs if not out.get("citations") else ["tu choi nhung van co trich dan"]
    if out.get("status") != "answered" or not out.get("answer", "").strip():
        return ["status/answer khong hop le"]
    cites = out.get("citations") or []
    if not cites:
        errs.append("tra loi nhung khong co trich dan")
    for i, c in enumerate(cites):
        ch, q = chunks.get(c.get("chunk_id")), c.get("quote", "")
        if ch is None:            errs.append(f"[{i}] chunk_id khong ton tai"); continue
        if len(q.strip()) < min_len: errs.append(f"[{i}] quote qua ngan"); continue
        if _n(q) not in _n(ch["text"]): errs.append(f"[{i}] quote KHONG nguyen van")
        if ch.get("valid_to") and ch["valid_to"] < today: errs.append(f"[{i}] chunk het hieu luc {ch['valid_to']}")
    return errs
```
  Kết quả chạy thử: câu trả lời với trích dẫn khớp → `[]`; trích dẫn bị đổi "24"→"36" → báo "KHONG nguyen van"; khối có `valid_to` trước ngày hôm nay → báo hết hiệu lực; từ chối không trích dẫn → `[]`; trả lời không trích dẫn → báo lỗi.
- **Điểm quan trọng:** validator nên **kiểm cả trường hợp bị cắt chữ**: dấu "…" trong trích dẫn sẽ làm trượt substring; yêu cầu AI không dùng "…" (Airbnb không nêu quy tắc này — đây là đề xuất của chúng tôi). Cũng đừng nới lỏng ngoài chuẩn hóa dấu câu/khoảng trắng; nếu nới (bỏ dấu, bỏ hoa thường) thì chấp nhận được cả câu bịa na ná.
- **Đường không code:** làm tay bằng Ctrl+F: chép từng trích dẫn vào tài liệu gốc, đánh dấu "có / không". Vài chục câu/lần thì chấp nhận được, hơn thế thì chuyển sang code.
- **Sản phẩm:** `validate.py` + tỷ lệ trích dẫn hợp lệ trên 30 câu (mục tiêu: 100% sau tối đa 2 lần thử lại).
- **Lỗi thường gặp:** PDF/Word có ký tự xuống dòng giữa câu (đã xử lý bằng chuẩn hóa khoảng trắng); số "8.500.000" vs "8,500,000" (chuẩn hóa ở C2); trích cả đoạn quá dài để "chắc ăn" → nên ràng buộc độ dài tối đa của mỗi trích dẫn **[Đề xuất]** (Airbnb giới hạn số đoạn trích k=15 và độ dài tối thiểu 15 ký tự **[Nguồn: phụ lục E]**).

### Bài 5.3 — Hiển thị nguồn cho người dùng
- **Mục tiêu:** nhân viên kiểm được trong 10 giây.
- **Thực hành:** mỗi câu trả lời hiển thị: *tên tài liệu + mục/trang + ngày cập nhật + trích dẫn nguyên văn* (và liên kết mở đúng tài liệu nếu có). Khối nên mang metadata từ C3 (`doc_id`, `section`, `page`, `updated`, `valid_from`, `valid_to`). Nếu dùng API Citations của nhà cung cấp, vị trí ký tự/trang có sẵn trong phản hồi **[Nguồn: tài liệu Citations]**; nếu tự làm, dùng `chunk_id` → bảng metadata.
- **Sản phẩm:** mẫu hiển thị (bảng/Word/Zalo) và một câu trả lời mẫu.
- **Lỗi thường gặp:** hiển thị tên tệp nội bộ vô nghĩa (`final_v3_new.pdf`); không có ngày cập nhật; nguồn là bản tóm tắt thay vì bản gốc (Airbnb chỉ cho trích từ bài gốc, không từ trang tóm tắt/điều hướng **[Nguồn: mục 4.1]**).

### Bài 5.4 — Câu hỏi ngoài phạm vi và từ chối đúng
- **Mục tiêu:** đo được AI từ chối đúng/thừa.
- **Thực hành:** mở rộng bộ câu hỏi vàng C4 thành 4 nhóm: (a) có đáp án rõ; (b) không có trong tài liệu nhưng cùng chủ đề ("bảo hành máy giặt Hãng Z" khi tài liệu chỉ có Hãng X); (c) hoàn toàn ngoài phạm vi ("thời tiết mai"); (d) câu hỏi mơ hồ. Chạy, chấm: nhóm (b), (c) phải ra "không đủ căn cứ"; nhóm (d) phải hỏi lại.
- **Cách chấm 2 số:** *Từ chối đúng* = (số câu nhóm b+c bị từ chối) / (số câu nhóm b+c); *Từ chối thừa* = (số câu nhóm a bị từ chối) / (số câu nhóm a). Giảm một số thường làm tăng số kia; ghi cả hai.
- **Sản phẩm:** bảng 2 số trên ≥ 30 câu (≥ 10 câu b/c).
- **Lỗi thường gặp:** bộ câu hỏi toàn câu có đáp án → từ chối đúng không đo được; từ chối khi khối đúng không tìm được do lỗi tìm (C4) bị gán nhầm cho C5 — đối chiếu với recall@k.
- **[Đề xuất]** Nếu từ chối là kết quả đúng nhưng người dùng cần một lối đi, thêm "liên hệ ai" (trưởng bộ phận) vào mẫu từ chối.

### Bài 5.5 — Câu hỏi nhiều bước và mâu thuẫn giữa tài liệu
- **Mục tiêu:** xử lý câu cần ≥ 2 khối và câu có khối mâu thuẫn.
- **Thực hành, nhiều bước:** ví dụ "máy giặt 9kg đang khuyến mãi, hỏng motor sau 3 năm thì khách được gì?" cần giá/khuyến mãi (GIA), bảo hành (BH), đổi trả (DT). Hai cách: (1) tìm một lượt lấy k lớn hơn một chút; (2) tách câu hỏi thành các câu con, tìm riêng từng câu rồi tổng hợp (Airbnb: tác tử chạy ~5 truy vấn và đọc ~6 bài mỗi ca, và nhận xét ca có truy vấn tinh chỉnh bổ sung có xu hướng bao phủ trích dẫn cao hơn — đây là quan sát không kiểm soát, tác giả gọi là giả thuyết **[Nguồn: Airbnb phụ lục C]**). Với mỗi câu con, validator bài 5.2 chạy riêng.
- **Thực hành, mâu thuẫn:** tạo cố ý 5 cặp khối mâu thuẫn (thông báo cũ vs mới; chính sách chung vs ngoại lệ hãng). Yêu cầu trong prompt (quy tắc 3, bài 5.1): nêu cả hai kèm mã khối và ngày; **không** tự chọn khi không có quy tắc ưu tiên. **[Đề xuất]** quy tắc ưu tiên tường minh đặt trong prompt hoặc metadata: "văn bản mới hơn thay thế văn bản cũ cùng chủ đề; văn bản của phòng pháp chế ưu tiên hơn thông báo nội bộ".
- **Sản phẩm:** 10 câu nhiều bước + 5 cặp mâu thuẫn, bảng điểm đúng/sai/nêu mâu thuẫn.
- **Lỗi thường gặp:** AI "trộn" hai khối thành một câu mượt nhưng không có trích dẫn nào ủng hộ toàn câu (validator không bắt được, cần judge hoặc người đọc từng phát biểu — xem 3.2); một khối phụ thiếu trong tìm kiếm (recall) → câu trả lời thiếu nhưng "có vẻ đầy đủ".
- **Lưu ý nguồn:** Airbnb giải quyết một phần "quy trình bị chia ở nhiều bài" bằng cách gộp thực thể thành một trang ngay lúc tạo chỉ mục (merged entities), thay vì tìm nhiều bước lúc truy vấn; xóa lớp này khiến kết quả tụt gần nhất nhưng p=0,078, chưa đạt p<0,05. **[Nguồn: Airbnb bảng 5]** Với SME: **[Đề xuất]** nếu một quy trình luôn nằm rải rác ở 3 tài liệu, hãy viết một khối tổng hợp có tham chiếu về tài liệu gốc, thay vì bắt AI ráp mỗi lần — nhưng trích dẫn vẫn phải lấy từ tài liệu gốc.

### Bài 5.6 — Tài liệu cũ, hết hiệu lực
- **Mục tiêu:** AI không dùng bảng giá/chính sách đã hết hạn.
- **Thực hành:** mỗi khối có `valid_from`, `valid_to` (hoặc `updated`); (1) **lọc trước khi đưa cho AI** (chỉ khối còn hiệu lực theo ngày hỏi, hoặc theo ngày giao dịch nếu câu hỏi nói rõ); (2) nếu cần trả lời lịch sử ("giá tháng 9?") thì cho phép khối cũ nhưng prompt phải nhận ra; (3) validator kiểm `valid_to` (code ở bài 5.2) làm lớp phòng thủ thứ hai; (4) khi cập nhật bảng giá, **thay hoặc đánh dấu hết hạn** khối cũ và nhúng lại chỉ mục (C4).
- **Sản phẩm:** bảng metadata + 5 câu thử "giá hiện tại" vs "giá tháng trước".
- **Lỗi thường gặp:** để cả hai bản trong chỉ mục không có ngày; người cập nhật quên đổi mã khối; hết hiệu lực nhưng không ai ghi.
- **[Chưa kiểm chứng]** Không có nguồn đã đọc đo mức độ mô hình xử lý tốt/kém tài liệu cũ-mới lẫn lộn; đây là quy trình quản trị, không phải kết quả thực nghiệm. Airbnb nhắc việc duy trì lớp điều hướng khi nguồn đổi cần kiểm tra cấu trúc và kiểm tra ngữ nghĩa định kỳ: "gánh nặng chuyển sang quản trị văn bản và dữ liệu — là gánh nặng thật". **[Nguồn: Airbnb mục 8]**

### Bài 5.7 — Đo hallucination/groundedness trên bộ vàng (đường không code → có code)
- **Mục tiêu:** có hai số: *tỷ lệ trích dẫn hợp lệ* (validator) và *tỷ lệ phát biểu có căn cứ* (judge/người).
- **Thực hành (không code):** với 30 câu, người chấm đọc từng câu trả lời: ghi phát biểu nào không có trong nguồn. Dùng bảng: `câu | số phát biểu | số có căn cứ | trích dẫn có thật? | từ chối đúng?`. Tính groundedness = Σ có căn cứ / Σ phát biểu (cùng ý với Faithfulness của RAGAS **[Nguồn]**).
- **Thực hành (code):** (1) validator chạy toàn bộ; (2) judge LLM: prompt hai bước theo RAGAS (tách phát biểu → kiểm từng phát biểu có trong ngữ cảnh) — mô phỏng ý tưởng, tự viết prompt; chạy 3 lần lấy đa số như Airbnb; (3) **hiệu chỉnh judge bằng người trên 20–30 câu** trước khi tin điểm của nó. Dùng một mô hình khác hoặc ít nhất khác phiên với mô hình sinh để tránh tự chấm mình (vấn đề này là cảnh báo chung; Airbnb dùng "mô hình mạnh hơn, độc lập" để audit liên kết điều hướng **[Nguồn: mục 4.1]**).
- **Sản phẩm:** bảng điểm theo từng cấu hình (ví dụ k=3 vs k=8; prompt A vs B; có/không validator-retry) kèm số câu.
- **Lỗi thường gặp:** chạy judge một lần rồi tin con số; n nhỏ kết luận mạnh (Airbnb n=132 mà các cấu hình vẫn không tách được ở p<0,05); judge và sinh dùng cùng prompt/mô hình; đo "độ lưu loát" thay vì độ có căn cứ.

### Bài 5.8 — Chọn mức kiểm theo rủi ro (độ trễ, chi phí)
- **Mục tiêu:** không dùng "súng cao xạ bắn muỗi" và không bỏ qua câu rủi ro cao.
- **Bảng đề xuất [Đề xuất của nhóm; ngưỡng chưa được nguồn nào chứng minh]:**

| Mức | Loại câu hỏi | Kiểm tối thiểu | Độ trễ/chi phí thêm |
|---|---|---|---|
| Thấp | FAQ nội bộ, hỏi nhanh | Prompt "chỉ từ nguồn" + hiển thị nguồn | gần 0 |
| Vừa | Chính sách bảo hành, đổi trả cho khách | + validator trích nguyên văn (retry ≤ 2) | cộng 0–2 lần gọi mô hình |
| Cao | Bảng giá báo khách, cam kết hợp đồng, quy định pháp lý | + người duyệt bắt buộc; + judge đa số 3 lần khi chạy đo; ghi log nguồn | chấp nhận chậm hơn nhiều lần (tham chiếu: ~90 s so với ~8–9 s của Airbnb **[Nguồn]**) |

- **Sản phẩm:** một trang "quy tắc mức kiểm" gắn với từng nhóm câu hỏi.
- **Lỗi thường gặp:** để mọi câu đi qua đường nặng nhất rồi nhân viên bỏ dùng; hoặc bỏ validator vì "đã dặn trong prompt" (Airbnb: ràng buộc do code ép, không phải do prompt **[Nguồn]**).

---

## 5) Đường không code vs đường có code; khi nào buộc phải chuyển

| | Không code | Có code nhẹ |
|---|---|---|
| Cách làm | Project/Gem/GPT với tệp tải lên + prompt mẫu bài 5.1; yêu cầu nêu tên tệp + trích nguyên văn; kiểm trích dẫn bằng Ctrl+F | Pipeline: C4 tìm → prompt → JSON → validator → retry → hiển thị nguồn → log |
| Mạnh | Nhanh; đủ cho quy mô nhỏ, rủi ro thấp | Kiểm tự động 100% trích dẫn; log; đo lặp lại |
| Yếu | Khó đo, khó ép; không có cơ chế "từ chối cả bản trả lời" | Cần bảo trì; chi phí gọi nhiều lượt |

**Buộc phải chuyển sang code khi (đề xuất):**
1. Hơn ~50 câu/tuần cần kiểm trích dẫn → kiểm tay không bền.
2. Câu trả lời được gửi ra ngoài (cho khách) hoặc ràng buộc hợp đồng.
3. Cần chứng minh được "đã kiểm" (log nguồn + kết quả validator) cho kiểm toán nội bộ.
4. Cần lọc theo hiệu lực/quyền truy cập trước khi đưa AI (bài 5.6).
5. Điểm groundedness hoặc từ chối đúng không đạt ngưỡng ở mục 6 sau khi đã chỉnh prompt.

Lưu ý: tính năng Citations của nhà cung cấp là "đường giữa" cho người dùng API, nhưng nhà cung cấp mô tả nó là cung cấp con trỏ hợp lệ tới tài liệu bạn đưa vào; việc **kiểm câu trích nguyên văn bằng code của bạn** vẫn là lớp độc lập, đặc biệt nếu chuyển nhà cung cấp hoặc dùng đầu ra có cấu trúc (không dùng chung với Citations ở API Anthropic theo tài liệu tại thời điểm đọc). **[Nguồn: tài liệu Citations]**

---

## 6) Tiêu chí lên cấp tiếp theo (C6 — đánh giá) — đo được

**[Đề xuất]** — các ngưỡng là điểm xuất phát; hạ/tăng theo rủi ro (mục 4, bài 5.8):
- ≥ 99% trích dẫn trong câu trả lời có đáp án qua validator ở lần cuối (sau tối đa 2 lần thử lại); mọi lỗi còn lại đều bị chặn (không hiển thị cho người dùng).
- Tỷ lệ phát biểu có căn cứ (bài 5.7) ≥ 95% trên bộ ≥ 30 câu có đáp án (≥ 98% cho mức Cao), judge đã hiệu chỉnh với người.
- Từ chối đúng ≥ 90% trên câu ngoài tài liệu/ngoài phạm vi (≥ 10 câu); từ chối thừa ≤ 10% trên câu có đáp án.
- Xử lý đúng ≥ 4/5 cặp mâu thuẫn (nêu cả hai kèm ngày) và 5/5 câu "tài liệu hết hiệu lực".
- Có log mỗi câu hỏi: câu hỏi, các khối đã cấp, câu trả lời, kết quả validator, người duyệt (nếu có), phiên bản mô hình + prompt.
- Biết độ trễ trung bình/p95 và chi phí mỗi câu hỏi theo từng mức.
- Phân tích lỗi còn lại và gán nguyên nhân: *tài liệu thiếu* (sửa C2/C3), *tìm sai* (C4), *sinh sai* (C5). Airbnb ghi nhận phần còn lại của họ chủ yếu là nội dung thiếu — **[Nguồn]** — nhưng đây là một kho tài liệu khác; hãy tự phân loại.

---

## 7) Ví dụ cho SME Việt Nam

**Chính sách bảo hành (khách hỏi qua Zalo, nhân viên tra cứu):**

Khối cấp cho AI:
```
[BH-01 | hiệu lực: 2026-01-01 → không | cập nhật 2026-09-01]
Máy giặt được bảo hành 24 tháng kể từ ngày mua, động cơ bảo hành 10 năm.
```
Câu hỏi: "Máy giặt hỏng động cơ năm thứ 5 có được bảo hành không?"
Câu trả lời mong muốn (có validator):
```
TRẢ LỜI: Có. Động cơ được bảo hành 10 năm, nên năm thứ 5 vẫn trong thời hạn. Các bộ phận khác chỉ 24 tháng.
NGUỒN: [BH-01] "động cơ bảo hành 10 năm" ; [BH-01] "bảo hành 24 tháng kể từ ngày mua"
```
(Ví dụ minh hoạ do chúng tôi soạn, không phải dữ liệu thật.)

**Bảng giá hết hiệu lực:** `GIA-2026-10` có `valid_to = 2026-10-31`; hôm nay 2026-11-11 hỏi "giá máy giặt 9kg" → bộ lọc loại khối cũ; nếu chỉ còn khối cũ → AI trả "Không đủ căn cứ: bảng giá hiện hành chưa được cập nhật; liên hệ phòng kinh doanh."

**Quy định nội bộ — mâu thuẫn:** thông báo cũ "xin nghỉ phép trước 3 ngày", thông báo mới "trước 5 ngày" → AI nêu cả hai kèm ngày, kèm gợi ý "áp dụng văn bản ban hành sau nếu phòng nhân sự xác nhận" (quy tắc ưu tiên do doanh nghiệp đặt).

**Câu ngoài phạm vi:** "Có bán máy lạnh Hãng X không?" khi tài liệu không đề cập → "Không đủ căn cứ trong tài liệu."

---

## 8) Tài liệu tham khảo

| # | Tiêu đề | URL | Loại | Truy cập | Tin cậy |
|---|---|---|---|---|---|
| 1 | Bako et al., Airbnb, *Frustratingly Easy Agentic RAG via Portable Skills* | https://arxiv.org/abs/2610.14428 | Bài báo/ca triển khai (arXiv, 10/2026) | 2026-11-11 | Trung bình–cao; n=132, một bối cảnh, người duyệt mọi ca |
| 2 | Es et al., *Ragas: Automated Evaluation of Retrieval Augmented Generation* | https://arxiv.org/abs/2309.15217 | Bài báo (khung đánh giá; v2 04/2025) | 2026-11-11 | Trung bình–cao; WikiEval nhỏ, tiếng Anh, mô hình chấm cũ |
| 3 | Anthropic, *Reduce hallucinations* | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | Tài liệu chính thức | 2026-11-11 | Trung bình–cao; khuyến nghị thực hành, không phải thực nghiệm |
| 4 | Anthropic, *Citations* | https://platform.claude.com/docs/en/build-with-claude/citations | Tài liệu chính thức (API) | 2026-11-11 | Cao về mô tả tính năng; **dễ đổi theo thời gian** |
| 5 | Liu et al., *Lost in the Middle* | https://arxiv.org/abs/2307.03172 | Bài báo (TACL) | 2026-11-11 | Cao; mô hình 2023 |
| 6 | Anthropic, *Introducing Contextual Retrieval* | https://www.anthropic.com/news/contextual-retrieval | Blog kỹ thuật chính thức | 2026-11-11 | Trung bình (đọc qua công cụ tóm tắt trang) |
| 7 | Cấp 4 của series (file `cap-04-tim-kiem.md`) | (cùng thư mục) | Tài liệu nội bộ | 2026-11-11 | — |

(Ghi chú: các URL `docs.anthropic.com/...` cũ chuyển hướng 301 sang `platform.claude.com/docs/...`.)

---

## 9) Chưa kiểm chứng / cần kiểm tra lại

1. **Tính năng Citations** (danh sách mô hình hỗ trợ, ràng buộc với structured outputs, định dạng khối) là chi tiết sản phẩm đã đọc tại 2026-11-11; cần kiểm lại khi triển khai. Chưa chạy thử API.
2. **RAGAS:** chỉ đọc bài gốc (2023, bản v2 2025). API/tên hàm thư viện hiện hành, các metric mới thêm sau bài, và độ tin cậy trên tiếng Việt: chưa kiểm chứng.
3. **Độ tin cậy của LLM judge trên tiếng Việt:** không có nguồn đã đọc. Phải tự hiệu chỉnh bằng người (bài 5.7). Việc dùng đa số 3 lần chấm là cách của Airbnb; không có bằng chứng ở đây rằng nó đủ cho dữ liệu tiếng Việt.
4. **Validator chỉ chứng minh trích nguyên văn, không chứng minh trích ủng hộ đúng câu trả lời.** Phần kiểm "ủng hộ" cần judge/người; chưa có số liệu về tỷ lệ bỏ sót.
5. **Hiệu lực/mâu thuẫn tài liệu:** quy trình và quy tắc ưu tiên là đề xuất của nhóm; chưa có nguồn đo mức độ mô hình xử lý tài liệu mâu thuẫn.
6. **SAP arXiv 2608.00122 (truy xuất 3 mức):** chưa đọc trong phạm vi này; chỉ nhắc theo bối cảnh dự án, không dùng số liệu.
7. **Nubank arXiv 2606.08867** (mô tả công cụ là prompt): chưa đọc trong phạm vi này; chủ yếu liên quan cấp 7.
8. **Phân tích lỗi của Airbnb** ("tài liệu thiếu nội dung") là kiểm tra định tính của tác giả, không có số theo loại; không nên coi là tỷ lệ chắc chắn.
9. **Độ trễ/chi phí:** số 90 giây vs 8–9 giây là của Airbnb (khác kho, khác mô hình); chưa có số đo trên bối cảnh SME hoặc tiếng Việt.
10. **Các ngưỡng** (≥99% trích hợp lệ, ≥95% có căn cứ, ≥90% từ chối đúng, 50 câu/tuần, retry ≤ 2) là đề xuất, chưa được nguồn nào xác nhận.
11. **Code:** validator (`validate2.py`) **đã chạy thử** trong scratchpad với 5 ca; chưa thử trên dữ liệu thật hay đầu ra mô hình thật; prompt mẫu bài 5.1 **chưa chạy thử** với mô hình cụ thể.
12. Sản phẩm Project/Gem/GPT tùy chỉnh: khả năng trích nguyên văn, giới hạn tệp và hành vi tìm bên trong thay đổi nhanh; phần này là "thao tác" cần rà lại mỗi quý, còn nguyên tắc (ép nguồn, từ chối khi thiếu, kiểm bằng code, đo bằng bộ câu hỏi riêng) bền hơn.
