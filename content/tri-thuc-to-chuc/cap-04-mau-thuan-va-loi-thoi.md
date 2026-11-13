# Cấp 4 (C4): Phát hiện mâu thuẫn và tài liệu lỗi thời

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác.
> Dùng lại: phát hiện tài liệu **đổi** theo mã khối (`../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` Bài 3.8); trả lời khi tài liệu mâu thuẫn hoặc hết hiệu lực (`../rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md` Bài 5.5, 5.6). Cấp này lo việc khác: **tìm** mâu thuẫn **giữa** các tài liệu và tài liệu **đã sai** dù không ai sửa nó.

## 1. Mục tiêu và người đọc

**Người đọc:** người giữ sổ đăng ký (C3), chủ tài liệu, người vận hành trợ lý AI nội bộ.

**Sau cấp này:**
1. Có **bảng sự kiện có khóa** (ví dụ `han_doi_hang_ngay = 7`) trích từ tài liệu, mỗi dòng có trích nguyên văn.
2. Code tự phát hiện **con số khác nhau** cho cùng một khóa.
3. AI được dùng để **gợi ý** mâu thuẫn bằng lời; mọi gợi ý vào **hàng đợi** cho chủ tài liệu quyết.
4. Có tín hiệu lỗi thời ngoài hạn rà soát: câu hỏi trợ lý không trả lời được, nhân viên báo sai.

**Sản phẩm:** `su_kien.csv`; script `mau_thuan.py`; hàng đợi mâu thuẫn trên Sheet; số đo tỷ lệ cảnh báo đúng.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Website ghi đổi hàng 15 ngày, SOP ghi 7 ngày, nhân viên nói 10 ngày. Làm sao phát hiện trước khi khách phát hiện?"*

Lỗi của C3: sổ đăng ký biết tài liệu **quá hạn rà soát**, nhưng không biết tài liệu **sai**. Hai tài liệu đều "hiệu lực" vẫn có thể nói ngược nhau. Trợ lý RAG khi đó trả lời theo khối nào tìm được trước.

## 3. Kiến thức nền

### 3.1 LLM tìm mâu thuẫn: tìm được, nhưng báo nhầm nhiều [Nguồn]

**American Express** (arXiv 2601.02627), bộ ContraDoc: 449 văn bản có mâu thuẫn, 442 không; trung bình 37,5 câu mỗi văn bản; 8 loại (phủ định, con số, nội dung, quan điểm, cảm xúc, quan hệ, sự thật, nhân quả).
- GPT-4o hỏi trực tiếp: bắt được 76,3% văn bản có mâu thuẫn, nhưng **báo nhầm 39,9%** văn bản không có mâu thuẫn.
- Độ chính xác của câu bằng chứng GPT-4o chỉ ra thấp: chỉ số EPR 0,267 (hỏi trực tiếp) và 0,289 (cách "che bớt rồi hỏi lại" của bài); tính riêng trên văn bản đã phân loại đúng là 0,349 và 0,383. Nghĩa là phần lớn câu được chỉ ra **không phải** câu mâu thuẫn thật.
- Mô hình yếu hơn (LLaMA 3.2 90B) bắt ít hơn (61,6%).
- Đây là mâu thuẫn **trong một văn bản**, tiếng Anh, bộ dữ liệu bán tổng hợp.

**SAP Signavio** (arXiv 2607.03228): kiểm trùng và mâu thuẫn khi thêm quy tắc mới là yêu cầu bắt buộc của bộ nhớ tổ chức; ví dụ SOP cho phép lệch giá dưới 250 EUR nhưng chính sách của một nhà máy đặt ngưỡng thấp hơn. Bài không đo riêng độ chính xác của bước này.

**Airbnb** (arXiv 2610.14428, qua `../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` Bài 3.7): lớp tóm tắt do AI sinh sẽ "trôi" khi kho tài liệu đổi; bảo trì gồm kiểm cấu trúc, kiểm ngữ nghĩa bằng mô hình độc lập, sinh lại trang bị đánh dấu.

### 3.2 Thiết kế 3 lớp [Đề xuất]

1. **Lớp code (chắc chắn, rẻ):** con số, ngày, tên người phụ trách cho cùng một khóa phải giống nhau giữa các tài liệu "hiệu lực". Code không bao giờ tự chọn bản đúng.
2. **Lớp AI (gợi ý):** so từng cặp tài liệu cùng chủ đề; AI phải trích **nguyên văn** hai câu mâu thuẫn; code kiểm trích; vì báo nhầm nhiều (3.1), mọi gợi ý vào hàng đợi.
3. **Lớp người:** chủ tài liệu quyết: sửa tài liệu nào, đánh dấu hết hiệu lực tài liệu nào, hay "không mâu thuẫn" (ghi lý do để lần sau không báo lại).

### 3.3 Dấu hiệu lỗi thời [Đề xuất]

- Quá hạn rà soát (C3).
- Tài liệu nhắc ngày, năm, giá, tên người đã qua hoặc đã nghỉ.
- Trợ lý AI (nhóm RAG) từ chối trả lời hoặc nhân viên sửa câu trả lời nhiều lần cho cùng một chủ đề (lấy từ nhật ký `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` Bài 9.1).
- Có quyết định mới trong sổ việc/biên bản (C0) mà tài liệu chưa cập nhật.

## 4. Chuỗi bài nhỏ

### Bài C4.1: Chọn khóa cần canh
- **Thực hành:** từ thẻ quy tắc (C3) chọn 20-50 khóa hay sai: thời hạn (đổi trả, bảo hành, thanh toán), mức (chiết khấu, phí, hạn mức duyệt), người (ai duyệt, ai nhận khiếu nại), địa chỉ/số hotline.
- **Sản phẩm:** danh sách khóa có tên chuẩn, ví dụ `han_doi_hang_ngay`.

### Bài C4.2: Trích sự kiện có khóa
- **Thực hành:** với mỗi tài liệu "hiệu lực" (và FAQ website, tin ghim Zalo), nhờ AI trích: `khoa, gia_tri, trich_nguyen_van, nguon, hieu_luc`. Chỉ cho chọn khóa trong danh sách. Không tìm thấy thì không ghi. Đường không code: làm trong Project, chép ra Sheet.
- **Sản phẩm:** `su_kien.csv`.
- **Lỗi thường gặp:** để AI tự đặt tên khóa (mỗi tài liệu một tên khác); AI "chuẩn hóa" con số khi trích.

### Bài C4.3: Code so sánh
- **Thực hành:** chạy `mau_thuan.py` (mục 5): bỏ dòng có trích không khớp nguồn; với mỗi khóa có nhiều giá trị, báo bản có ngày hiệu lực mới nhất và các nguồn cần xem.
- **Sản phẩm:** danh sách mâu thuẫn chắc chắn (về con số).

### Bài C4.4: AI gợi ý mâu thuẫn bằng lời
- **Thực hành:** chỉ so các cặp tài liệu cùng thẻ chủ đề (không so tất cả với tất cả). Chỉ dẫn: "Liệt kê cặp câu mâu thuẫn. Mỗi cặp chép nguyên văn hai câu. Nếu không chắc, không liệt kê." Code kiểm hai câu có thật trong hai tài liệu.
- **Sản phẩm:** gợi ý đã qua kiểm trích, vào hàng đợi.
- **Lỗi thường gặp:** coi gợi ý là kết luận; bắt chủ tài liệu đọc 50 gợi ý mỗi tuần (họ sẽ bỏ).

### Bài C4.5: Hàng đợi cho chủ tài liệu
- **Thực hành:** Sheet cột: mã mâu thuẫn, khóa/chủ đề, trích A, trích B, chủ tài liệu, quyết định (sửa A / sửa B / hết hiệu lực A / không mâu thuẫn), lý do, ngày. "Không mâu thuẫn" được ghi nhớ để lần sau bỏ qua cặp đó.
- **Sản phẩm:** hàng đợi có hạn xử lý (ví dụ 5 ngày làm việc).

### Bài C4.6: Tín hiệu lỗi thời từ người dùng
- **Thực hành:** thêm vào trợ lý nội bộ một nút hoặc câu lệnh "báo sai"; mỗi báo sai tạo một dòng trong hàng đợi, gắn tài liệu nguồn của câu trả lời.
- **Sản phẩm:** kênh báo sai.

### Bài C4.7: Đo độ chính xác của cảnh báo
- **Thực hành:** mỗi tháng đếm: số gợi ý của AI, số được chủ xác nhận là mâu thuẫn thật. Nếu tỷ lệ đúng thấp (bài AmEx gợi ý điều này là bình thường), thu hẹp phạm vi so (ít cặp hơn, chủ đề hẹp hơn) thay vì bỏ hàng đợi.
- **Sản phẩm:** dòng số đo hằng tháng.

## 5. Đường không code vs có code

| | Không code | Có code nhẹ |
|---|---|---|
| Trích sự kiện | Project/Gem, chép ra Sheet | API trả JSON theo lược đồ |
| So con số | Pivot table trong Sheet, lọc khóa có > 1 giá trị | `mau_thuan.py` |
| Gợi ý bằng lời | Dán 2 tài liệu vào chat, hỏi | Script so cặp theo thẻ, kiểm trích |

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

Chạy thử với 3 nguồn giả (SOP 7 ngày, FAQ website 15 ngày, tin Zalo "đổi trong 15 ngày"): dòng trích từ Zalo bị AI ghi sai thành "đổi trong 30 ngày" nên bị loại (`TRICH_SAI`); code báo `MAU_THUAN` cho `han_doi_hang_ngay`, bản mới nhất là FAQ (15 ngày, 2026-10-01), cần xem SOP-BH-01. Code **không** sửa SOP; chủ tài liệu quyết.

**Giới hạn:** chỉ bắt mâu thuẫn trên khóa đã chọn và con số trích đúng. Mâu thuẫn về điều kiện ("áp dụng cho khách lẻ" và "áp dụng cho mọi khách") cần lớp AI và người.

**Khi nào buộc chuyển sang code [Đề xuất]:** > 30 tài liệu hiệu lực; thẻ quy tắc > 50; muốn chạy lại mỗi khi tài liệu đổi (dùng phát hiện thay đổi ở Bài 3.8 của nhóm RAG).

## 6. Tiêu chí lên cấp [Đề xuất]

1. Bảng sự kiện phủ mọi khóa đã chọn trên mọi tài liệu "hiệu lực", kể cả FAQ website và tin ghim.
2. Không còn mâu thuẫn con số nào chưa có quyết định quá 5 ngày làm việc.
3. Có số đo tỷ lệ gợi ý AI được xác nhận đúng trong ≥ 2 tháng.
4. Có kênh "báo sai" và ít nhất một vòng: báo sai → sửa tài liệu → chạy lại ca thử của trợ lý.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

- **Cửa hàng nội thất online (Shopee + website + Zalo OA):** khóa `phi_giao_noi_thanh`, `han_doi_tra`, `bao_hanh_thang`. Mâu thuẫn thường gặp: mô tả sản phẩm trên sàn chưa cập nhật sau đổi chính sách. Chủ: trưởng bán hàng online.
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
