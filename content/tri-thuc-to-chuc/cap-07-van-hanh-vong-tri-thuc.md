# Cấp 7 (C7): Vận hành vòng tri thức

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác.
> Dùng lại, không viết lại: nhật ký, phiên bản prompt, quy trình sửa → chạy lại → phát hành, trôi dạt mô hình (`../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md`); bộ ca mẫu và thống kê n nhỏ (`../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`). Cấp này thêm **vòng đời của tài liệu**: tạo, duyệt, dùng, rà soát, hết hiệu lực, và cổng nối sang nhóm RAG, nhóm xử lý yêu cầu khách.

## 1. Mục tiêu và người đọc

**Người đọc:** người được giao "giữ tri thức" (thường là quản lý vận hành hoặc trợ lý giám đốc); chủ doanh nghiệp.

**Sau cấp này:**
1. Có **nhịp** cố định: việc hằng tuần, hằng tháng, hằng quý.
2. Có **5-8 chỉ số** về sức khỏe tri thức, xem mỗi tháng.
3. Có **cổng xuất**: chỉ tài liệu đạt điều kiện mới được đưa vào Project/Gem, kho RAG, trợ lý trả lời khách.
4. Mỗi lần tài liệu đổi, **ca thử** của các trợ lý dùng tài liệu đó được chạy lại.
5. Phân vai rõ, có người thay khi người giữ tri thức nghỉ.

**Sản phẩm:** lịch vận hành 1 trang; bảng chỉ số tháng; script `cong_xuat.py`; bảng phân vai.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Đã có biên bản, SOP, sổ đăng ký, bài học, báo cáo. Làm sao để 6 tháng sau nó vẫn đúng và vẫn được dùng?"*

Lỗi thường gặp sau C0-C6 **[Đề xuất, quan sát chung về quản trị tài liệu]**: hăng hái 2-3 tháng rồi bỏ; sổ không ai cập nhật; trợ lý AI vẫn trả lời theo tài liệu cũ vì không ai nối việc sửa tài liệu với việc cập nhật trợ lý.

## 3. Kiến thức nền

### 3.1 Bằng chứng về giữ chất lượng khi thay đổi [Nguồn]

- **BMO ESCROW** (arXiv 2608.01772, qua `../nen-tang-bang-chung.md`): qua 4 vòng sửa skill, không có kho ca cũ thì điểm trên ca cũ tụt 0,857 → 0,7; có kho ca cũ giữ khoảng 0,84. Ý: mỗi lần đổi tài liệu/quy tắc phải chạy lại ca cũ.
- **Airbnb** (arXiv 2610.14428): lớp tóm tắt do AI sinh trôi khi kho đổi; bảo trì là gánh nặng thật.
- **SAP** (arXiv 2608.00122): nguy cơ nhiễm độc bộ nhớ dùng chung; điểm tin cậy chưa hiệu chuẩn.
- **SAP Signavio** (arXiv 2607.03228): bộ nhớ cần chủ sở hữu, quyền đọc/sửa, quy trình duyệt, trách nhiệm giải trình; lỗi còn lại do mục quy tắc viết quá rộng, nghĩa là chất lượng biên soạn quyết định kết quả.
- **IBM Japan** (arXiv 2611.11348): khi SOP đổi mà tri thức bổ sung không được giữ riêng, các chỉnh sửa trước bị mất ("trôi SOP-kỹ năng").

### 3.2 Chỉ số sức khỏe tri thức [Đề xuất]

| Chỉ số | Cách tính | Nguồn |
|---|---|---|
| Độ phủ sổ | Tài liệu AI đang dùng có trong sổ / tổng tài liệu AI đang dùng | C3 |
| Quá hạn rà soát | Tài liệu "hiệu lực" quá hạn / tổng "hiệu lực" | C3 |
| Độ trễ quyết định → tài liệu | Trung vị số ngày từ quyết định chốt (C0) tới khi tài liệu cập nhật | C0, C3 |
| Mâu thuẫn mở | Số mâu thuẫn chưa quyết > 5 ngày | C4 |
| Bài học đã áp dụng | Bài học "đã áp dụng vào tài liệu" / bài học đã duyệt | C5 |
| Chất lượng biên bản | Việc bị sửa/bịa/sót khi duyệt, trên mẫu 5 cuộc họp/tháng | C0 |
| Dùng thật | Số lần tài liệu được trợ lý trích dẫn hoặc được mở | nhật ký RAG |
| Báo sai | Số "báo sai" mỗi tháng và thời gian xử lý | C4 |

Với SME nhỏ, các tỷ lệ này tính trên vài chục tài liệu: xem xu hướng, không kết luận từ một tháng (xem `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` mục 3.2).

### 3.3 Cổng xuất sang nhóm khác [Đề xuất]

Một tài liệu chỉ được đưa vào kho của trợ lý (RAG, Project/Gem chung, chatbot khách) khi: "hiệu lực"; có chủ đang làm việc; không quá hạn rà soát; đã đánh dấu được dùng cho AI; mức nhạy cảm cho phép; không có mâu thuẫn mở. Cổng này là **code hoặc bộ lọc Sheet**, không phải lời dặn.

## 4. Chuỗi bài nhỏ

### Bài C7.1: Lịch vận hành
- **Thực hành [Đề xuất]:**
  - *Hằng tuần (30 phút):* chạy kiểm sổ (C3), xem hàng đợi mâu thuẫn và báo sai (C4), nhắc chủ tài liệu quá hạn.
  - *Hằng tháng (1-2 giờ):* tính bảng chỉ số; lấy mẫu 5 biên bản kiểm chất lượng; xem bài học chưa áp dụng; chạy lại ca thử của các trợ lý.
  - *Hằng quý:* rà quy tắc ghi âm và dữ liệu (C1, C5); kiểm điều khoản công cụ AI (theo `../an-toan-du-lieu-va-phap-ly-vn.md` mục 5); chọn 1-2 quy trình mới để làm SOP (C2).
- **Sản phẩm:** lịch trên Google Calendar/Lark, có người nhận.

### Bài C7.2: Phân vai
- **Thực hành:** ba vai tối thiểu: *chủ tài liệu* (quyết nội dung); *người giữ sổ* (chạy kiểm, nhắc, cổng xuất); *người duyệt AI* (duyệt biên bản, bài học, báo cáo). Một người có thể giữ nhiều vai, nhưng chủ tài liệu không tự duyệt thay đổi do AI đề xuất cho tài liệu quan trọng của chính mình nếu có người khác làm được **[Đề xuất]**. Mỗi vai có người dự phòng.
- **Sản phẩm:** bảng phân vai trong sổ C3.

### Bài C7.3: Cổng xuất bằng code
- **Thực hành:** chạy `cong_xuat.py` (mục 5) trước mỗi lần cập nhật kho của trợ lý. Tài liệu bị chặn kèm lý do được gửi cho chủ.
- **Sản phẩm:** danh sách được xuất / bị chặn mỗi lần cập nhật.

### Bài C7.4: Tài liệu đổi → chạy lại ca thử
- **Thực hành:** mỗi trợ lý (nhóm RAG, nhóm xử lý yêu cầu khách) có bảng ca thử gắn với mã tài liệu. Khi tài liệu đổi (phát hiện bằng `../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` Bài 3.8): cập nhật đáp án ca bị ảnh hưởng; chạy lại toàn bộ ca, không chỉ ca liên quan (bài học ESCROW); chỉ phát hành khi không ca cũ nào hỏng (quy trình ở `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` Bài 9.3).
- **Sản phẩm:** dòng nhật ký: tài liệu đổi, ca chạy lại, kết quả.

### Bài C7.5: Chống nhiễm độc kho
- **Thực hành:** chỉ người có quyền mới nhập vào kho; mọi mục có nguồn; mục do AI sinh (thẻ quy tắc, bài học, tóm tắt) được đánh dấu và **không được trích làm nguồn** thay tài liệu gốc (giống quy tắc của Airbnb ở nhóm RAG); tài liệu từ bên ngoài (email khách, file nhà cung cấp) không vào kho tri thức nội bộ khi chưa qua chủ.
- **Sản phẩm:** quy tắc nhập kho 5 dòng.

### Bài C7.6: Đo chi phí và giá trị
- **Thực hành:** mỗi quý ghi giờ công cho vận hành (lịch C7.1) và các số đo trước-sau có đồng hồ (thời gian làm biên bản, báo cáo; thời gian người mới làm được việc). Quyết định giữ, thu hẹp, hay mở rộng dựa trên số này.
- **Sản phẩm:** bảng quý.

## 5. Đường không code vs có code

| | Không code | Có code nhẹ |
|---|---|---|
| Chỉ số | Tab "Chỉ số" trong Sheet sổ đăng ký | Script đọc các sổ, xuất bảng |
| Cổng xuất | Bộ lọc Sheet (lọc theo các cột điều kiện) | `cong_xuat.py` chạy trước khi cập nhật kho |
| Nhắc việc | Lịch, nhắc thủ công | Script gửi email theo lịch (Task Scheduler/cron) |

**Mã mẫu (đã chạy thử, `python -I -X utf8`):**

```python
import csv, io
from datetime import date
MUC_CHO_PHEP = {"cong_khai", "noi_bo"}

def cong_xuat(csv_text, hom_nay, nhan_vien_dang_lam, mau_thuan_mo):
    duoc, bi_chan = [], []
    for d in csv.DictReader(io.StringIO(csv_text)):
        ly_do = []
        if d["trang_thai"] != "hieu_luc": ly_do.append("khong_hieu_luc")
        if d["chu_so_huu"] not in nhan_vien_dang_lam: ly_do.append("khong_co_chu")
        if (hom_nay - date.fromisoformat(d["ra_soat_lan_cuoi"])).days > int(d["chu_ky_ngay"]):
            ly_do.append("qua_han_ra_soat")
        if d["duoc_dung_cho_AI"] != "co": ly_do.append("chua_duoc_phep_AI")
        if d["muc_nhay_cam"] not in MUC_CHO_PHEP: ly_do.append("nhay_cam:" + d["muc_nhay_cam"])
        if d["ma"] in mau_thuan_mo: ly_do.append("co_mau_thuan_chua_xu_ly")
        (bi_chan if ly_do else duoc).append((d["ma"], ly_do))
    return duoc, bi_chan
```

Chạy thử với 4 tài liệu giả: chỉ `BG-2026Q4` được xuất; `SOP-BH-01` bị chặn vì còn mâu thuẫn mở (ví dụ của C4); hợp đồng khách `HD-KH-ABC` bị chặn vì mức "bí mật"; `SOP-KHO-02` bị chặn vì chủ đã nghỉ và quá hạn rà soát.

**Khi nào buộc chuyển sang code [Đề xuất]:** có ≥ 2 trợ lý dùng chung kho; cập nhật kho hơn 1 lần/tuần; > 100 tài liệu.

## 6. Tiêu chí "đang vận hành" [Đề xuất]

Đây là cấp cuối của nhóm. Coi là đang vận hành khi đủ 6 tháng liên tục:
1. Lịch tuần và tháng được làm ≥ 90% số lần.
2. Mọi lần cập nhật kho trợ lý đi qua cổng xuất; không tài liệu bị chặn nào lọt vào kho (kiểm ngẫu nhiên).
3. Mỗi lần tài liệu đổi có dòng nhật ký chạy lại ca thử.
4. Bảng chỉ số tháng có đủ 6 tháng; xu hướng quá hạn rà soát và mâu thuẫn mở không tăng.
5. Đã qua ít nhất một lần nghỉ việc hoặc đổi người giữ sổ mà hệ thống vẫn chạy.

**Khi nào nâng cấp lên công cụ chuyên dụng [Đề xuất]:** Sheet chậm hoặc hay bị sửa nhầm; > 300 tài liệu; cần phân quyền theo từng tài liệu; cần nhiều trợ lý dùng chung một bộ nhớ quy tắc (hướng SAP Signavio). Lúc đó cân nhắc phần mềm quản lý tài liệu có phân quyền và lịch sử, hoặc thuê làm (xem `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` Bài 9.9).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

- **Công ty logistics nội địa 60 người (Hà Nội):** trợ lý nội bộ trả lời tài xế và điều phối về quy trình giao hàng, đối soát COD. Người giữ sổ: trợ lý giám đốc vận hành. Mỗi khi bảng phí đổi, cổng xuất chặn bảng cũ, ca thử "phí giao nội thành dưới 3 kg" chạy lại trước khi trợ lý dùng bảng mới.
- **Phòng khám đa khoa tư nhân:** chỉ SOP hành chính (đặt lịch, thu phí, xuất hóa đơn) qua cổng xuất sang trợ lý lễ tân; mọi tài liệu chuyên môn y khoa mức "nhạy cảm" bị chặn khỏi trợ lý dùng dịch vụ AI bên ngoài.
- **Công ty phần mềm gia công 20 người (Đà Nẵng):** bài học sau sự cố triển khai (C5) và SOP phát hành (C2) là kho chung cho trợ lý lập trình; theo đúng cảnh báo của SAP, mỗi mục nhập kho phải có người duyệt và nguồn, chống ghi chú sai lan sang mọi người.

## 8. Tài liệu tham khảo

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| BMO ESCROW | https://arxiv.org/abs/2608.01772 | Qua `../nen-tang-bang-chung.md` | Cao |
| Airbnb Agentic RAG via Portable Skills | https://arxiv.org/abs/2610.14428 | Qua `../nen-tang-bang-chung.md` | Cao |
| SAP Shared Organizational Memory | https://arxiv.org/abs/2608.00122 | Qua `../nen-tang-bang-chung.md` | Cao về mô tả |
| SAP Signavio Organizational Memory | https://arxiv.org/abs/2607.03228 | Phần lớn | Trung bình |
| IBM Japan, Separation of Skilling Context | https://arxiv.org/abs/2611.11348 | Gần toàn văn | Trung bình |
| Nhóm RAG cap-03, cap-06, cap-09 | `../rag-tra-cuu-tai-lieu/` | Đã đọc phần liên quan | Nội bộ |

## 9. Chưa kiểm chứng

- Không có nguồn đo hiệu quả của "vận hành vòng tri thức" ở SME. Bảng chỉ số, lịch, ngưỡng 90%, 6 tháng, 300 tài liệu đều là đề xuất.
- Chưa so sánh công cụ quản lý tài liệu (Notion, Lark, Google Drive có nhãn, phần mềm trong nước) về phân quyền, lịch sử, nhắc hạn.
- Quy tắc "chủ tài liệu không tự duyệt" có thể không khả thi ở doanh nghiệp rất nhỏ; cần thử với người học.
