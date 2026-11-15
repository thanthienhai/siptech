# Cấp 4 (C4): Phát hiện mâu thuẫn và tài liệu lỗi thời

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác.
> Dùng lại: phát hiện tài liệu **đổi** theo mã khối (`../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` Bài 3.8); trả lời khi tài liệu mâu thuẫn hoặc hết hiệu lực (`../rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md` Bài 5.5, 5.6). Cấp này lo việc khác: **tìm** mâu thuẫn **giữa** các tài liệu và tài liệu **đã sai** dù không ai sửa nó.

!!! tip "Tóm tắt nhanh"
    Công ty nào cũng có cùng một thông tin nằm ở nhiều nơi (website, quy trình nội bộ, tin nhắn Zalo), và các nơi này dễ nói khác nhau. Bài này chỉ cách **lập một bảng nhỏ ghi các thông tin hay sai**, để máy (hoặc một bảng tính) tự **so con số giữa các tài liệu** và báo chỗ khác nhau. AI chỉ được **gợi ý**, còn người chủ tài liệu mới là người quyết. Sau bài, bạn có một danh sách mâu thuẫn cần xử lý và một kênh để nhân viên báo "tài liệu này sai rồi".

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người giữ sổ đăng ký tài liệu (đã làm ở C3), chủ của từng tài liệu, và người vận hành trợ lý AI nội bộ. Bạn **không cần biết lập trình** để làm phần chính. Phần có code ở mục 5 là để nhờ người biết code hoặc nhờ AI chạy giúp.

**Bạn cần chuẩn bị:**
- Sổ đăng ký tài liệu và các "thẻ quy tắc" từ C3.
- Các tài liệu đang có hiệu lực, kể cả FAQ trên website và tin nhắn ghim trên Zalo.
- Một tài khoản có thể tạo Project (Claude) hoặc Gem (Gemini), là tính năng cho bạn lưu sẵn chỉ dẫn để dùng lại nhiều lần.
- Một bảng tính Google Sheet hoặc Excel.

**Sau bài này bạn sẽ có:**
1. Một **bảng sự kiện có khóa**. "Khóa" là một cái tên chuẩn đặt cho một thông tin hay bị nói khác nhau (ví dụ `han_doi_hang_ngay = 7`, nghĩa là hạn đổi hàng là 7 ngày). Mỗi dòng trong bảng đều có **một câu trích nguyên văn** từ tài liệu gốc để chứng minh.
2. Một cách để **tự phát hiện con số khác nhau** cho cùng một khóa. Việc này do code (hoặc bảng tính) làm.
3. AI được dùng để **gợi ý** mâu thuẫn bằng lời. Mọi gợi ý đều vào một **hàng đợi** (danh sách chờ xử lý) để chủ tài liệu quyết.
4. Thêm các tín hiệu cho biết tài liệu đã lỗi thời, ngoài việc chờ đến hạn rà soát: câu hỏi mà trợ lý AI không trả lời được, hoặc nhân viên báo sai.

**Thứ bạn cầm đi được sau bài:** tệp `su_kien.csv` (bảng sự kiện, mở được bằng Excel); script `mau_thuan.py` (đoạn chương trình ngắn để so sánh); hàng đợi mâu thuẫn trên Google Sheet; và số đo tỷ lệ cảnh báo đúng.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Website ghi đổi hàng 15 ngày, SOP ghi 7 ngày, nhân viên nói 10 ngày. Làm sao phát hiện trước khi khách phát hiện?"*

(SOP là quy trình chuẩn của công ty, tức văn bản hướng dẫn cách làm một việc.)

Lỗi của C3: sổ đăng ký biết tài liệu **quá hạn rà soát**, nhưng không biết tài liệu **sai**. Hai tài liệu đều đang "hiệu lực" vẫn có thể nói ngược nhau. Khi đó, trợ lý RAG (trợ lý AI trả lời dựa trên kho tài liệu của công ty) sẽ trả lời theo khối nội dung nào nó tìm được trước, nên câu trả lời có thể đúng hôm nay và sai hôm sau.

## 3. Kiến thức nền

Phần này tóm tắt vài nghiên cứu cho thấy AI tìm mâu thuẫn được tới đâu, rồi đề xuất cách thiết kế để dùng AI mà không bị báo động giả làm phiền.

### 3.1 LLM tìm mâu thuẫn: tìm được, nhưng báo nhầm nhiều [Nguồn]

(LLM là mô hình ngôn ngữ lớn, loại AI đứng sau ChatGPT, Claude, Gemini. Ở đây ta gọi tắt là "AI".)

**American Express** (arXiv 2601.02627) làm bộ dữ liệu ContraDoc, gồm 449 văn bản có mâu thuẫn và 442 văn bản không có. Trung bình mỗi văn bản dài 37,5 câu. Có 8 loại mâu thuẫn: phủ định, con số, nội dung, quan điểm, cảm xúc, quan hệ, sự thật, nhân quả.
- GPT-4o, khi được hỏi trực tiếp, bắt được 76,3% văn bản có mâu thuẫn. Nhưng nó cũng **báo nhầm 39,9%** văn bản không có mâu thuẫn. Nghĩa là cứ khoảng 10 văn bản sạch thì có gần 4 văn bản bị báo oan.
- Độ chính xác của câu bằng chứng mà GPT-4o chỉ ra là thấp. Chỉ số EPR (đo xem câu AI chỉ ra có đúng là câu mâu thuẫn thật không) là 0,267 khi hỏi trực tiếp và 0,289 với cách "che bớt rồi hỏi lại" của bài báo. Nếu chỉ tính riêng những văn bản mà AI đã phân loại đúng thì là 0,349 và 0,383. Nói đơn giản: phần lớn câu được chỉ ra **không phải** câu mâu thuẫn thật.
- Mô hình yếu hơn (LLaMA 3.2 90B) bắt được ít hơn (61,6%).
- Cần nhớ: đây là mâu thuẫn **ngay trong một văn bản**, bằng tiếng Anh, trên bộ dữ liệu bán tổng hợp (một phần do máy tạo ra).

!!! tip "Nói đơn giản"
    AI giống một người soát lỗi rất hăng: bắt được nhiều lỗi thật, nhưng cũng hay chỉ nhầm chỗ không có lỗi, và hay chỉ sai câu. Vì vậy ta **không giao AI quyết**, chỉ dùng nó để **gợi ý** cho người xem.

**SAP Signavio** (arXiv 2607.03228) cho rằng việc kiểm trùng và kiểm mâu thuẫn mỗi khi thêm một quy tắc mới là yêu cầu bắt buộc của "bộ nhớ tổ chức" (kho tri thức dùng chung của công ty). Ví dụ trong bài: quy trình SOP cho phép lệch giá dưới 250 EUR, nhưng chính sách của một nhà máy lại đặt ngưỡng thấp hơn. Bài này không đo riêng độ chính xác của bước kiểm đó.

**Airbnb** (arXiv 2610.14428, qua `../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` Bài 3.7) cho biết: lớp tóm tắt do AI sinh ra sẽ "trôi" (dần lệch khỏi thực tế) khi kho tài liệu đổi. Việc bảo trì gồm kiểm cấu trúc, kiểm ngữ nghĩa bằng một mô hình độc lập, và sinh lại những trang bị đánh dấu.

### 3.2 Thiết kế 3 lớp [Đề xuất]

Vì AI báo nhầm nhiều (mục 3.1), ta chia việc thành ba lớp, từ chắc chắn nhất đến ít chắc chắn nhất:

1. **Lớp code (chắc chắn, rẻ):** con số, ngày, tên người phụ trách cho cùng một khóa phải giống nhau giữa các tài liệu "hiệu lực". Code không bao giờ tự chọn bản đúng.
2. **Lớp AI (gợi ý):** AI so từng cặp tài liệu cùng chủ đề. AI phải trích **nguyên văn** hai câu mâu thuẫn, rồi code kiểm xem hai câu đó có thật trong tài liệu không. Vì báo nhầm nhiều (3.1), mọi gợi ý đều vào hàng đợi.
3. **Lớp người:** chủ tài liệu quyết. Có ba lựa chọn: sửa tài liệu nào, đánh dấu hết hiệu lực tài liệu nào, hay "không mâu thuẫn" (ghi lý do để lần sau hệ thống không báo lại).

!!! tip "Nói đơn giản"
    Máy lo việc **so con số** vì việc đó chắc chắn. AI lo việc **đọc hiểu bằng lời** nhưng chỉ được gợi ý. Người luôn là người **chốt**.

### 3.3 Dấu hiệu lỗi thời [Đề xuất]

Một tài liệu có thể đã sai dù chưa tới hạn rà soát. Hãy để ý các dấu hiệu sau:
- Quá hạn rà soát (C3).
- Tài liệu nhắc ngày, năm, giá, hoặc tên người đã qua hoặc đã nghỉ việc.
- Trợ lý AI (nhóm RAG) từ chối trả lời, hoặc nhân viên phải sửa câu trả lời nhiều lần cho cùng một chủ đề. Các dấu hiệu này lấy từ nhật ký (bản ghi lại các lần hỏi đáp) ở `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` Bài 9.1.
- Có quyết định mới trong sổ việc hoặc biên bản họp (C0) mà tài liệu chưa được cập nhật.

## 4. Chuỗi bài nhỏ

Bảy bài dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và (nếu có) lỗi hay gặp để tránh.

### Bài C4.1: Chọn khóa cần canh
- **Việc cần làm:** từ thẻ quy tắc (C3), chọn 20-50 khóa hay bị sai. Gợi ý các nhóm: thời hạn (đổi trả, bảo hành, thanh toán); mức (chiết khấu, phí, hạn mức duyệt); người (ai duyệt, ai nhận khiếu nại); địa chỉ hoặc số hotline. Mỗi khóa đặt một tên chuẩn, viết liền, không dấu, nối bằng dấu gạch dưới.
- **Bạn có sau bài:** danh sách khóa có tên chuẩn, ví dụ `han_doi_hang_ngay`.

### Bài C4.2: Trích sự kiện có khóa
- **Việc cần làm:** với mỗi tài liệu "hiệu lực" (và cả FAQ website, tin ghim Zalo), nhờ AI trích ra các trường sau: `khoa, gia_tri, trich_nguyen_van, nguon, hieu_luc` (tức: khóa, giá trị, câu trích nguyên văn, nguồn tài liệu, ngày có hiệu lực). Chỉ cho AI chọn khóa trong danh sách đã có. Không tìm thấy thì không ghi gì.
- **Đường không code:** làm trong Project hoặc Gem, rồi chép kết quả ra Sheet.
- **Bạn có sau bài:** `su_kien.csv`.
- **Lỗi hay gặp:** để AI tự đặt tên khóa (mỗi tài liệu ra một tên khác nhau, nên sau đó không so được); hoặc AI "chuẩn hóa" con số khi trích (ví dụ sửa "15 ngày" thành "30 ngày" cho khớp với chỗ khác).

### Bài C4.3: Code so sánh
- **Việc cần làm:** chạy `mau_thuan.py` (mã ở mục 5). Đoạn chương trình này làm hai việc: bỏ những dòng có câu trích không khớp với tài liệu nguồn; rồi với mỗi khóa có nhiều giá trị khác nhau, báo bản có ngày hiệu lực mới nhất và các nguồn cần xem lại.
- **Bạn có sau bài:** danh sách mâu thuẫn chắc chắn (về con số).

### Bài C4.4: AI gợi ý mâu thuẫn bằng lời
- **Việc cần làm:** chỉ so các cặp tài liệu **cùng thẻ chủ đề** (không so tất cả với tất cả, vì sẽ quá nhiều và báo nhầm nhiều). Chỉ dẫn cho AI: "Liệt kê cặp câu mâu thuẫn. Mỗi cặp chép nguyên văn hai câu. Nếu không chắc, không liệt kê." Sau đó code kiểm hai câu có thật trong hai tài liệu hay không.
- **Bạn có sau bài:** các gợi ý đã qua kiểm trích, đưa vào hàng đợi.
- **Lỗi hay gặp:** coi gợi ý là kết luận; hoặc bắt chủ tài liệu đọc 50 gợi ý mỗi tuần (họ sẽ bỏ qua).

### Bài C4.5: Hàng đợi cho chủ tài liệu
- **Việc cần làm:** lập một Sheet với các cột: mã mâu thuẫn, khóa/chủ đề, trích A, trích B, chủ tài liệu, quyết định (sửa A / sửa B / hết hiệu lực A / không mâu thuẫn), lý do, ngày. Những cặp được quyết định "không mâu thuẫn" phải được ghi nhớ để lần sau bỏ qua cặp đó.
- **Bạn có sau bài:** hàng đợi có hạn xử lý (ví dụ 5 ngày làm việc).

### Bài C4.6: Tín hiệu lỗi thời từ người dùng
- **Việc cần làm:** thêm vào trợ lý nội bộ một nút hoặc một câu lệnh "báo sai". Mỗi lần có người báo sai, hệ thống tạo một dòng trong hàng đợi, kèm tài liệu nguồn của câu trả lời bị báo.
- **Bạn có sau bài:** kênh báo sai.

### Bài C4.7: Đo độ chính xác của cảnh báo
- **Việc cần làm:** mỗi tháng đếm hai số: số gợi ý của AI, và số gợi ý được chủ tài liệu xác nhận là mâu thuẫn thật. Nếu tỷ lệ đúng thấp (bài của AmEx gợi ý đây là chuyện bình thường), hãy **thu hẹp phạm vi so** (ít cặp hơn, chủ đề hẹp hơn) thay vì bỏ hàng đợi.
- **Bạn có sau bài:** một dòng số đo mỗi tháng.

## 5. Đường không code vs có code

Cách không code đủ dùng khi bạn mới bắt đầu và có ít tài liệu. Cách có code nhẹ giúp máy làm thay những việc lặp lại.

| | Không code | Có code nhẹ |
|---|---|---|
| Trích sự kiện | Project/Gem, chép ra Sheet | API trả JSON theo lược đồ |
| So con số | Pivot table trong Sheet, lọc khóa có > 1 giá trị | `mau_thuan.py` |
| Gợi ý bằng lời | Dán 2 tài liệu vào chat, hỏi | Script so cặp theo thẻ, kiểm trích |

(API là cổng để một chương trình gọi AI tự động thay vì gõ vào khung chat. JSON là cách viết danh sách có khung rõ ràng để máy đọc được. Lược đồ là bản quy định "mỗi dòng phải có những trường nào". Pivot table là công cụ của Excel và Google Sheet để gom và đếm dữ liệu theo nhóm. Script là một đoạn chương trình ngắn.)

**Đoạn mã dưới đây làm gì?** Nó nhận bảng sự kiện (mỗi dòng gồm khóa, giá trị, câu trích, nguồn, ngày hiệu lực) và nguyên văn các tài liệu nguồn. Bước 1: nó kiểm câu trích có thật sự nằm trong tài liệu nguồn không; dòng nào trích sai thì bị loại và báo `TRICH_SAI`. Bước 2: với các dòng còn lại, nó gom theo khóa, và nếu một khóa có từ hai giá trị khác nhau trở lên thì báo `MAU_THUAN`, kèm bản mới nhất và các nguồn cần xem lại. Bạn **không cần đọc hiểu từng dòng**; chỉ cần nắm ý nghĩa của nó, và nhờ người biết lập trình hoặc nhờ AI chạy giúp.

**Mã mẫu (đã chạy thử, `python -I -X utf8`):**

```python
from collections import defaultdict

def tim_mau_thuan(su_kien, van_ban_nguon):
    loi, theo_khoa = [], defaultdict(list)
    for s in su_kien:
        if s["trich"] not in van_ban_nguon.get(s["nguon"], ""):   # hang rao trich nguyen van
            loi.append(("TRICH_SAI", s["nguon"], s["khoa"]))
            continue
        theo_khoa[s["khoa"]].append(s)
    for khoa, ds in theo_khoa.items():
        if len({s["gia_tri"] for s in ds}) > 1:
            ds = sorted(ds, key=lambda s: s["hieu_luc"], reverse=True)
            moi = ds[0]
            cu = [s["nguon"] for s in ds[1:] if s["gia_tri"] != moi["gia_tri"]]
            loi.append(("MAU_THUAN", khoa,
                        "moi nhat: %s=%s (%s)" % (moi["nguon"], moi["gia_tri"], moi["hieu_luc"]),
                        "can xem: " + ", ".join(cu)))
    return loi
```

**Kết quả chạy thử** với 3 nguồn giả (SOP 7 ngày, FAQ website 15 ngày, tin Zalo "đổi trong 15 ngày"): dòng trích từ Zalo bị AI ghi sai thành "đổi trong 30 ngày" nên bị loại (`TRICH_SAI`). Code báo `MAU_THUAN` cho `han_doi_hang_ngay`: bản mới nhất là FAQ (15 ngày, 2026-10-01), cần xem SOP-BH-01. Code **không** sửa SOP; chủ tài liệu quyết.

!!! tip "Nói đơn giản"
    Code ở đây chỉ làm hai việc: loại những dòng mà AI trích sai so với tài liệu thật, rồi chỉ ra "cùng một thông tin nhưng hai nơi ghi hai số khác nhau". Nó không tự quyết số nào đúng.

**Giới hạn:** code chỉ bắt được mâu thuẫn trên khóa đã chọn và con số trích đúng. Mâu thuẫn về điều kiện (ví dụ "áp dụng cho khách lẻ" và "áp dụng cho mọi khách") cần lớp AI và người.

**Khi nào buộc chuyển sang code [Đề xuất]:** có hơn 30 tài liệu hiệu lực; thẻ quy tắc nhiều hơn 50; hoặc muốn chạy lại mỗi khi tài liệu đổi (dùng cách phát hiện thay đổi ở Bài 3.8 của nhóm RAG).

## 6. Tiêu chí lên cấp [Đề xuất]

Bạn có thể sang cấp tiếp theo khi đạt đủ các điều sau:
1. Bảng sự kiện phủ mọi khóa đã chọn trên mọi tài liệu "hiệu lực", kể cả FAQ website và tin ghim.
2. Không còn mâu thuẫn con số nào chưa có quyết định quá 5 ngày làm việc.
3. Có số đo tỷ lệ gợi ý AI được xác nhận đúng trong ≥ 2 tháng.
4. Có kênh "báo sai" và ít nhất một vòng: báo sai, rồi sửa tài liệu, rồi chạy lại ca thử của trợ lý.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung:

- **Cửa hàng nội thất online (Shopee + website + Zalo OA):** khóa `phi_giao_noi_thanh`, `han_doi_tra`, `bao_hanh_thang`. Mâu thuẫn thường gặp: mô tả sản phẩm trên sàn chưa được cập nhật sau khi đổi chính sách. Chủ tài liệu: trưởng bán hàng online.
- **Công ty phân phối dược phẩm/thực phẩm chức năng 30 người:** khóa `chiet_khau_nha_thuoc_cap_1`, `han_thanh_toan_ngay`, `nguoi_duyet_cong_no_vuot`. Mâu thuẫn giữa bảng chính sách đại lý (PDF gửi khách) và file Excel nội bộ. Chỉ dùng tài liệu đã bỏ tên khách.
- **Trường mầm non tư thục 2 cơ sở:** khóa `hoc_phi_thang`, `han_nop_hoc_phi`, `chinh_sach_hoan_phi_nghi_om`. Mâu thuẫn giữa sổ tay phụ huynh và thông báo Zalo nhóm lớp. Không đưa thông tin trẻ vào AI.

## 8. Tài liệu tham khảo

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| Improved Evidence Extraction and Metrics for Document Inconsistency Detection (American Express) | https://arxiv.org/abs/2601.02627 | Gần toàn văn, bảng phụ lục | Trung bình-Cao (mâu thuẫn trong một văn bản, tiếng Anh) |
| Organizational Memory for Agentic Business Process Execution (SAP Signavio) | https://arxiv.org/abs/2607.03228 | Phần lớn | Trung bình |
| ContraDoc (Li và cộng sự 2024, bộ dữ liệu gốc) | (qua bài AmEx) | Không đọc | Thấp |
| Nhóm RAG cap-03, cap-05, cap-09 | `../rag-tra-cuu-tai-lieu/` | Đã đọc phần liên quan | Nội bộ |

## 9. Chưa kiểm chứng

- Chưa có nguồn đo LLM phát hiện mâu thuẫn **giữa** các tài liệu doanh nghiệp, hay trên tiếng Việt.
- Các bài có tiêu đề hứa hẹn nhưng **chưa đọc**: "Towards Reversible Forgetting: Managing Obsolete Knowledge in Continual Enterprise AI Agents" (arXiv 2608.18177), "LLMs in Resolving Contextual Knowledge Conflicts" (arXiv 2609.03148), "CorporateBench" (arXiv 2608.27391). Nên đọc trước khi xuất bản.
- Hạn 5 ngày làm việc, 20-50 khóa là đề xuất.
- Tỷ lệ báo nhầm trên tài liệu SME tiếng Việt có thể khác hẳn số của AmEx.
