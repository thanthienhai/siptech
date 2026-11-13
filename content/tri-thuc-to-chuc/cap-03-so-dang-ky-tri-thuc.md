# Cấp 3 (C3): Sổ đăng ký tri thức, mỗi tài liệu có chủ

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác.
> Dùng lại, không viết lại: mã ổn định, mã nội dung, phát hiện tài liệu đổi (`../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` Bài 3.5 và 3.8); phiên bản và nhật ký thay đổi (`../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` Bài 9.2). Cấp này thêm phần **con người**: ai chịu trách nhiệm, khi nào rà soát, bản nào là bản đúng.

## 1. Mục tiêu và người đọc

**Người đọc:** chủ doanh nghiệp, quản lý vận hành, người được giao "giữ tài liệu".

**Sau cấp này:**
1. Mọi tài liệu dùng để làm việc (SOP, bảng giá, chính sách, mẫu biểu) nằm trong **một sổ đăng ký**.
2. Mỗi dòng có: mã, chủ sở hữu, trạng thái (nháp / hiệu lực / hết hiệu lực), ngày rà soát gần nhất, chu kỳ rà soát, bản thay thế.
3. Quy định "chốt trong Zalo" được đưa vào tài liệu trong thời hạn đã định.
4. Các quy tắc quan trọng nhất được tách thành **thẻ quy tắc** nhỏ, có nguồn.

**Sản phẩm:** sổ đăng ký (Google Sheet/Excel/Lark Base); quy định "một nguồn sự thật" 1 trang; bộ thẻ quy tắc; script `so_dang_ky.py`.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Có nhiều tài liệu rồi. Bản nào đang đúng? Ai sửa? Bao lâu thì xem lại?"*

Lỗi của C0-C2: biên bản, SOP được tạo ra nhưng nằm rải ở Drive cá nhân, Zalo, máy tính từng người. Không ai biết bản nào mới. Nhóm RAG sẽ trả lời theo bản cũ nếu bản cũ còn trong kho (xem `../rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md` Bài 5.6).

## 3. Kiến thức nền

### 3.1 Bộ nhớ tổ chức có quản trị [Nguồn]

**SAP Signavio** (arXiv 2607.03228) đề xuất "bộ nhớ tổ chức" cho tác tử chạy quy trình:
- Tri thức từ chính sách, SOP, sơ đồ quy trình, kinh nghiệm cũ được tách thành **"process atom"**: mỗi mục đúng **một** quy tắc, gồm tên, nguồn, **phạm vi áp dụng**, **hành động**, **mục đích**; gắn thẻ (bộ phận, đối tượng, quy trình).
- Một bộ phận "Global Curator" kiểm mục mới: trùng, chồng chéo, mâu thuẫn với mục cũ. **Người** duyệt mọi thay đổi. Có chủ sở hữu theo bộ phận, quyền đọc/sửa tách nhau.
- Thử nghiệm: **10 tình huống mua hàng tổng hợp**. Tỷ lệ tuân thủ chính sách (GPT-4.1 / Claude Sonnet 4.5): không có gì 0,30 / 0,30; RAG 0,70 / 0,80; bộ nhớ 0,88 / 0,95. RAG trượt khi quy tắc **áp dụng chung** nhưng không giống câu hỏi (ví dụ "mọi đề nghị mua phải có trung tâm chi phí", nằm trong chính sách tài chính). Lỗi còn lại của bộ nhớ là do một mục có **phạm vi viết quá rộng**. Tác giả tự nói kết quả là sơ bộ.

**SAP** (arXiv 2608.00122, qua `../nen-tang-bang-chung.md`): bộ nhớ dùng chung cho tác tử lập trình hỏi xin phép người đóng góp, quét bảo mật, kiểm trùng; ~900 đóng góp thành 1.144 mục; **lợi ích chưa đo**; tác giả nêu nguy cơ nhiễm độc bộ nhớ.

### 3.2 Tách theo tần suất thay đổi và chủ sở hữu [Nguồn]

**IBM Japan** (arXiv 2611.11348) tách 3 lớp theo **tần suất thay đổi và chủ sở hữu**: SOP lõi (logic nghiệp vụ, người làm nghiệp vụ giữ), tri thức ngữ cảnh (chi tiết thực thi, quy ước), hiện thực (prompt, công cụ). Khi gộp chung, sửa SOP làm mất các chỉnh sửa trước đó ("trôi SOP-kỹ năng").

### 3.3 Áp dụng cho SME [Đề xuất]

- Không cần hệ thống. Một Sheet là đủ cho vài chục đến vài trăm tài liệu.
- Thẻ quy tắc chỉ làm cho **quy tắc có con số hoặc điều kiện** (thời hạn đổi trả, mức chiết khấu, hạn mức duyệt chi). Đây là thứ hay mâu thuẫn (C4) và hay được AI trả lời sai.
- Mỗi tài liệu **một chủ**. Không có chủ thì không được dùng làm nguồn cho AI.

## 4. Chuỗi bài nhỏ

### Bài C3.1: Kiểm kê nơi tri thức đang nằm
- **Thực hành:** liệt kê theo nơi: nhóm Zalo (nhóm nào, ai quản trị), Google Drive/OneDrive (tài khoản cá nhân hay công ty), Notion/Lark, Excel trên máy, giấy dán tường, đầu người (C2). Đánh dấu chỗ thuộc **tài khoản cá nhân**: đây là thứ mất khi người nghỉ (C5).
- **Sản phẩm:** bản đồ tri thức 1 trang.
- **Lỗi thường gặp:** chỉ liệt kê Drive; quên Zalo và Excel cá nhân.

### Bài C3.2: Sổ đăng ký
- **Thực hành:** cột tối thiểu: `ma` (ổn định, ví dụ `SOP-BH-01`), `ten`, `loai`, `chu_so_huu`, `trang_thai` (nhap / hieu_luc / het_hieu_luc), `ngay_hieu_luc`, `ra_soat_lan_cuoi`, `chu_ky_ngay`, `thay_the_boi`, `link`, `muc_nhay_cam`, `duoc_dung_cho_AI` (có/không).
- **Sản phẩm:** sổ đăng ký với mọi tài liệu từ C0-C2.
- **Lỗi thường gặp:** dùng tên file làm mã (đổi tên là gãy); xóa tài liệu cũ thay vì đánh dấu hết hiệu lực.

### Bài C3.3: Chủ sở hữu và chu kỳ rà soát
- **Thực hành [Đề xuất]:** chủ = người có quyền quyết nội dung (không phải người gõ). Chu kỳ theo loại: bảng giá 30 ngày; chính sách khách 90 ngày; SOP nội bộ 180 ngày. Rà soát = mở ra, xác nhận còn đúng, ghi ngày (kể cả khi không sửa).
- **Sản phẩm:** cột chủ và chu kỳ đã điền đủ.
- **Lỗi thường gặp:** chủ là "phòng kinh doanh" (không phải một người); giám đốc làm chủ mọi thứ.

### Bài C3.4: Quy định "một nguồn sự thật"
- **Thực hành [Đề xuất]:** quy định 1 trang: (1) quyết định chốt ở Zalo/họp phải được chủ tài liệu cập nhật vào tài liệu trong 2 ngày làm việc; (2) tin nhắn Zalo không phải nguồn cho AI; (3) khi trả lời khách/nhân viên, dẫn link tài liệu trong sổ, không chuyển tiếp tin nhắn cũ.
- **Sản phẩm:** quy định; ghim trong các nhóm Zalo.
- **Lỗi thường gặp:** quy định không có người kiểm; chủ tài liệu không được báo khi có quyết định mới (gắn với sổ việc ở C0).

### Bài C3.5: Thẻ quy tắc
- **Thực hành:** với 10-30 quy tắc quan trọng, viết thẻ theo khuôn SAP Signavio: `ma_the`, `ten`, `pham_vi` (áp dụng cho ai, khi nào), `hanh_dong` (một quy tắc), `muc_dich`, `nguon` (mã tài liệu + trích nguyên văn), `chu_so_huu`, `hieu_luc`. Có thể nhờ AI nháp thẻ từ tài liệu; người chủ duyệt từng thẻ. Kiểm bằng code: trích nguyên văn phải có trong tài liệu nguồn (logic của `../rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md` Bài 5.2).
- **Sản phẩm:** `the_quy_tac.csv`.
- **Lỗi thường gặp:** một thẻ chứa nhiều quy tắc; phạm vi viết quá rộng (lỗi SAP Signavio gặp); thẻ được trích như nguồn thay vì tài liệu gốc.

### Bài C3.6: Tách lõi và ghi chú ngữ cảnh
- **Thực hành:** với mỗi SOP từ C2, tách phần "chi tiết thực thi" (đường dẫn file, tên menu phần mềm, mẹo) sang trang "Ghi chú thực hiện" riêng, chủ có thể khác. SOP lõi ngắn, ít đổi; ghi chú đổi thường xuyên.
- **Sản phẩm:** SOP lõi + ghi chú, cả hai trong sổ.

### Bài C3.7: Kiểm sổ hằng tuần bằng code
- **Thực hành:** chạy `so_dang_ky.py` (mục 5) mỗi thứ Hai; gửi danh sách cảnh báo cho từng chủ.
- **Sản phẩm:** báo cáo tuần: không có chủ, chủ đã nghỉ, quá hạn rà soát, "hiệu lực" nhưng đã có bản thay, "hết hiệu lực" mà không chỉ bản mới.

## 5. Đường không code vs có code

| | Không code | Có code nhẹ |
|---|---|---|
| Sổ | Google Sheet/Excel/Lark Base, tô màu theo hạn | Sheet + script đọc CSV xuất ra |
| Cảnh báo | Công thức `=TODAY()-E2>F2` trong Sheet | `so_dang_ky.py` chạy theo lịch, gửi email |
| Thẻ quy tắc | Bảng tay | AI nháp thẻ, code kiểm trích nguyên văn |

**Mã mẫu (đã chạy thử, `python -I -X utf8`):**

```python
import csv, io
from datetime import date

def kiem_so(csv_text, hom_nay, nhan_vien_dang_lam):
    canh_bao = []
    for d in csv.DictReader(io.StringIO(csv_text)):
        ma = d["ma"]
        if not d["chu_so_huu"]:
            canh_bao.append((ma, "KHONG_CO_CHU"))
        elif d["chu_so_huu"] not in nhan_vien_dang_lam:
            canh_bao.append((ma, "CHU_DA_NGHI:" + d["chu_so_huu"]))
        if d["trang_thai"] == "hieu_luc":
            qua = (hom_nay - date.fromisoformat(d["ra_soat_lan_cuoi"])).days - int(d["chu_ky_ngay"])
            if qua > 0:
                canh_bao.append((ma, "QUA_HAN_RA_SOAT_%d_NGAY" % qua))
            if d["thay_the_boi"]:
                canh_bao.append((ma, "HIEU_LUC_NHUNG_DA_CO_BAN_THAY"))
        if d["trang_thai"] == "het_hieu_luc" and not d["thay_the_boi"]:
            canh_bao.append((ma, "HET_HIEU_LUC_KHONG_CHI_BAN_MOI"))
    return canh_bao
```

Chạy thử với 4 dòng giả, ngày 2026-11-11: `SOP-KHO-02` chủ "Nam" đã nghỉ và quá hạn rà soát 151 ngày; `BG-2026Q3` hết hiệu lực nhưng không chỉ bản mới; `CS-GH-01` không có chủ và còn "hiệu lực" dù đã có `CS-GH-02` thay.

**Khi nào buộc chuyển sang code [Đề xuất]:** > 50 tài liệu; nhiều chủ cần nhắc riêng; muốn chặn tự động tài liệu "không có chủ" hoặc "hết hiệu lực" khỏi kho của nhóm RAG.

## 6. Tiêu chí lên cấp [Đề xuất]

1. 100% tài liệu đang dùng cho AI (Project/Gem, kho RAG) có trong sổ, có chủ, có trạng thái.
2. ≥ 90% tài liệu "hiệu lực" không quá hạn rà soát.
3. Lấy ngẫu nhiên 5 quyết định chốt ở Zalo/họp trong tháng: ≥ 4 đã có trong tài liệu đúng hạn.
4. Có ≥ 10 thẻ quy tắc có nguồn kiểm được bằng code.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

- **Chuỗi 4 cửa hàng điện thoại (Hải Phòng):** chính sách bảo hành, đổi trả, giá thu cũ đổi mới thay đổi hằng tháng; trước đây gửi qua nhóm Zalo "Quản lý cửa hàng". Sổ đăng ký: bảng giá thu cũ (chủ: trưởng thu mua, chu kỳ 7 ngày), chính sách bảo hành (chủ: giám đốc, 90 ngày). Thẻ quy tắc: "máy vỡ màn hình không thu cũ", "đổi mới trong 7 ngày nếu lỗi nhà sản xuất".
- **Công ty xây dựng nhỏ 50 người (Nghệ An):** quy trình nghiệm thu, an toàn lao động, mẫu hồ sơ thanh toán. Chủ sở hữu: chỉ huy trưởng (quy trình hiện trường), kế toán trưởng (hồ sơ thanh toán). Ghi chú thực hiện (mẫu Excel nào, gửi cho ai ở chủ đầu tư) tách khỏi SOP lõi vì mỗi công trình khác nhau.
- **Spa 2 cơ sở (TP.HCM):** quy trình liệu trình, chính sách hoàn tiền gói. Thẻ quy tắc "hoàn tiền gói chưa dùng trong 30 ngày, trừ 10% phí" (số giả định) là nguồn duy nhất cho chatbot trả lời khách ở nhóm `../xu-ly-yeu-cau-khach/`.

## 8. Tài liệu tham khảo

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| Organizational Memory for Agentic Business Process Execution (SAP Signavio) | https://arxiv.org/abs/2607.03228 | Phần lớn (mục 1-5, kết quả mục 6, kết luận) | Trung bình (10 tình huống tổng hợp, tác giả nói sơ bộ) |
| Shared Organizational Memory for Enterprise Coding Agents (SAP) | https://arxiv.org/abs/2608.00122 | Qua `../nen-tang-bang-chung.md` | Cao về mô tả; chưa đo lợi ích |
| Separation of Skilling Context for SOP-based Agents (IBM Japan) | https://arxiv.org/abs/2611.11348 | Gần toàn văn | Trung bình (dùng ý tách lớp, không dùng số) |
| Nhóm RAG cap-03, cap-09 | `../rag-tra-cuu-tai-lieu/` | Đã đọc phần liên quan | Nội bộ |

## 9. Chưa kiểm chứng

- Không có nguồn nào đo hiệu quả của "sổ đăng ký + chủ sở hữu" ở SME. Đây là thực hành quản trị tài liệu thông thường, nhóm soạn đề xuất.
- Chu kỳ rà soát 7/30/90/180 ngày, hạn cập nhật 2 ngày làm việc, ngưỡng 90% là đề xuất.
- Tính năng của Lark Base, Notion database (nhắc hạn, phân quyền theo cột) chưa kiểm trong phiên này.
- Kết quả SAP Signavio có thể không lặp lại khi quy tắc nhiều, chồng chéo, viết tay như ở SME.
