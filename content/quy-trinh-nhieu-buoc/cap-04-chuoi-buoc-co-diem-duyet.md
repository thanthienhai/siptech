# Q4 — Chuỗi bước có trạng thái và điểm duyệt

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

## 1) Mục tiêu và người đọc

**Người đọc:** chủ SME, trưởng phòng kế toán/nhân sự/kinh doanh, người đã có luồng Q1 và có thể có bộ định tuyến Q2.

**Sau cấp này có:** một quy trình nhiều bước (đơn hàng, đề nghị thanh toán, hoặc tuyển dụng) chạy như **máy trạng thái**: mỗi phiếu có một trạng thái; chỉ chuyển trạng thái qua bảng chuyển cho phép; mỗi lần chuyển kiểm quyền bằng code và ghi nhật ký. AI, nếu có, chỉ ở 1-2 bước hẹp (trích trường, phân loại) và kết quả của nó luôn qua cổng kiểm hoặc người duyệt.

**Thứ chạy được độc lập:** quy trình trên phiếu thật, có hàng đợi duyệt và nhật ký. Chạy được cả khi tắt hẳn bước AI (người làm thay bước đó).

## 2) Câu hỏi cấp này trả lời / lỗi của cấp trước

**Câu hỏi:** "Nối nhiều bước, nhiều người duyệt lại với nhau thế nào để không mất phiếu, không ai duyệt vượt quyền, và biết phiếu đang ở đâu?"

**Lỗi của Q1-Q3:** các luồng rời nhau; trạng thái phiếu nằm trong đầu người hoặc trong tin nhắn; duyệt qua Zalo không có dấu vết; không ai chặn trường hợp "nhân viên tự duyệt phiếu của mình" hay "chi tiền khi chưa duyệt".

**Phần đã có ở nhóm RAG, không lặp lại:** phân biệt workflow/agent, 5 mẫu workflow, thiết kế điểm duyệt (khi nào, ai, duyệt gì, hàng đợi, chống duyệt cho xong), gói chuyển giao, trần bước, lỗi cộng dồn pⁿ: `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.1-3.7. Phân hạng công cụ đọc/ghi A-D và idempotent: `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` mục 3.4-3.5. Cấp này chỉ thêm phần riêng của quy trình nghiệp vụ: **trạng thái, quyền, hạn mức, và chỗ đặt AI trong ba nghiệp vụ cụ thể**.

## 3) Kiến thức nền

### 3.1 Bằng chứng [Nguồn]
- **MAP (arXiv 2512.04123):** 16/20 ca dùng workflow có cấu trúc; 68% hệ thống chạy ≤10 bước rồi chuyển người; 15/20 ca chạy bất đồng bộ; 66% chấp nhận độ trễ cỡ phút trở lên. "Agents suggest actions, experts approve execution".
- **TheAgentCompany:** khi để agent tự làm trọn việc nhiều bước (trung bình 27,2 bước), mô hình tốt nhất hoàn thành 30,3%. Ví dụ việc "hoàn tiền công tác" trong hình minh họa của bài gồm truy cập hóa đơn, kiểm tiêu chí, hỏi người phụ trách, xác nhận số tiền; agent được chấm theo từng mốc. Bài nêu agent yếu nhất ở giao tiếp với đồng nghiệp và phần mềm văn phòng web.
- **τ-bench:** việc càng nhiều hành động ghi càng khó (hình 6 của bài); 25% lỗi là quyết định sai do không theo quy định nghiệp vụ, ví dụ đổi từng món một trong khi quy định chỉ cho gọi lệnh đổi một lần.
- **Samsung SDS (arXiv 2505.20733):** quy trình chi phí 4 bước (OCR/IDP trích trường → phân loại theo cơ sở dữ liệu chính sách → LLM hỗ trợ ngoại lệ → người quyết định cuối, hệ thống học từ quyết định đó). Trên 1.448 hóa đơn giấy: độ chính xác 0,83, precision 1, recall 0,82. Nghĩa là 242 hóa đơn hợp lệ bị hệ thống đánh dấu, phải qua người. Tác giả là nhóm của nhà cung cấp; con số "giảm 80-90% thời gian" nằm trong phần "hiệu quả kỳ vọng" chứ không phải phép đo có đối chứng.
- **READY:** cùng một agent, lượng người duyệt cần thiết phụ thuộc chính sách chuyển người; nên quyết định "bao nhiêu % phiếu qua người" bằng số đo, không bằng cảm giác.

### 3.2 Máy trạng thái thay cho "chuỗi prompt" [Đề xuất]
- Mỗi phiếu có `trang_thai` thuộc danh sách đóng. Bảng `CHUYEN[(trạng thái, hành động)] → trạng thái mới`. Hành động không có trong bảng thì code từ chối.
- Mỗi trạng thái chờ duyệt gắn **tập người có quyền**. Code kiểm, không phải prompt.
- **Hạn mức** (ví dụ trưởng phòng duyệt ≤ 20 triệu) nằm trong một bảng cấu hình, không nằm trong lời dặn AI.
- **Tách người:** người tạo phiếu không được duyệt phiếu của mình; người duyệt không được là người chi.
- Bước AI là một hành động như mọi hành động khác (`trich_truong`), kết quả đi vào trạng thái "chờ kiểm", không nhảy thẳng sang "đã duyệt".
- Trạng thái lưu ở **một nơi** (một bảng Sheets/Lark Base/SQLite), không lưu trong lịch sử chat.

### 3.3 Đặt AI ở đâu trong ba nghiệp vụ [Đề xuất]

| Nghiệp vụ | Bước có thể dùng AI | Bước không dùng AI | Ghi chú |
|---|---|---|---|
| Đơn hàng từ tin nhắn | Đọc tin tự do thành đơn nháp (sản phẩm, số lượng, địa chỉ) | Giá, tồn kho, phí ship, khuyến mãi (quy tắc); xác nhận với khách (người, mẫu sẵn); tạo đơn chính thức (code sau khi người xác nhận) | Soạn trả lời khách: nhóm `xu-ly-yeu-cau-khach` |
| Đề nghị thanh toán | Trích trường từ ảnh hóa đơn/chứng từ | Định tuyến theo dự án và hạn mức (quy tắc); duyệt (người); chi (người, ngoài hệ thống) | Kiểm chứng từ theo quy tắc: nhóm `kiem-tra-ho-so-theo-quy-tac` |
| Tuyển dụng | Trích trường CV (vị trí, kinh nghiệm năm, khu vực) vào bảng | Loại/nhận ứng viên (người); hẹn lịch (quy tắc + lịch); gửi thư mời (người bấm) | Không cho AI chấm điểm/xếp hạng ứng viên ở cấp này |

## 4) Chuỗi bài nhỏ

### Bài Q4.1 — Vẽ máy trạng thái
- **Làm:** từ bảng Q0, liệt kê trạng thái (5-9) và hành động. Vẽ ô và mũi tên. Mỗi trạng thái chờ ghi: ai có quyền, hạn xử lý.
- **Sản phẩm:** sơ đồ + bảng chuyển + bảng quyền. **Lỗi:** trạng thái "đang xử lý" chung chung; quên trạng thái "trả lại" và "hủy".

### Bài Q4.2 — Bảng phiếu là nguồn sự thật
- **Làm:** một bảng phiếu (Sheets/Lark Base/SQLite) với `ma_phieu`, `trang_thai`, `nguoi_tao`, `nguoi_xu_ly`, `han`, `so_tien`, link chứng từ. Mọi luồng đọc/ghi qua bảng này. Khóa sửa tay cột `trang_thai`.
- **Sản phẩm:** bảng phiếu + quyền truy cập.

### Bài Q4.3 — Kiểm chuyển trạng thái bằng code
- **Làm:** hàm `chuyen(phieu, hanh_dong, nguoi)` kiểm bảng chuyển, quyền, hạn mức; ghi nhật ký. Thử các ca sai có chủ đích: người không có quyền duyệt; duyệt vượt hạn mức; chi khi chưa duyệt; người tạo tự duyệt.
- **Sản phẩm:** hàm + bảng ca sai và kết quả "đã chặn".

### Bài Q4.4 — Gắn bước AI hẹp
- **Làm:** chỉ một bước (ví dụ trích trường hóa đơn). Đầu ra JSON có trường `null` khi không chắc. Kết quả vào `cho_kiem`; cổng kiểm bằng code (số tiền là số dương, ngày hợp lệ, mã số thuế đúng độ dài) rồi mới sang người duyệt. Người duyệt thấy ảnh gốc cạnh trường đã trích.
- **Sản phẩm:** bước AI + tỷ lệ trường bị người sửa trên 30 phiếu.

### Bài Q4.5 — Hàng đợi duyệt và nhắc hạn
- **Làm:** dùng thiết kế hàng đợi ở `cap-08-quy-trinh-nhieu-buoc.md` bài 8.4; nhắc hạn bằng luồng Q1. Với Lark: Lark Approval có API tạo phiếu và sự kiện thay đổi trạng thái (theo tài liệu thứ cấp, cần kiểm); với Google: Forms + Apps Script + email có link duyệt.
- **Sản phẩm:** hàng đợi chạy 2 tuần; tỷ lệ phiếu quá hạn.

### Bài Q4.6 — Chạy song song với cách cũ
- **Làm:** 2 tuần đầu chạy song song: phiếu vẫn làm cách cũ, hệ thống mới chạy "bóng" (không ghi ra ngoài). So kết quả từng phiếu.
- **Sản phẩm:** bảng chênh lệch; quyết định bật thật.

## 5) Đường không code vs có code; khi nào buộc chuyển

| | Không code | Có code |
|---|---|---|
| Trạng thái + duyệt | Lark Approval; Lark Base với trường trạng thái + automation; Google Forms + Sheets + AppSheet (chưa kiểm AppSheet) | Bảng SQLite/Sheets + hàm chuyển trạng thái (mẫu dưới) |
| Quyền | Phân quyền của nền tảng (ai sửa cột nào) | Kiểm trong hàm `chuyen` |
| Bước AI | Bước gọi AI trong Make/n8n; hoặc người dán vào Gem/Project | Gọi API, kiểm JSON, cổng kiểm |

**Buộc chuyển sang code [Đề xuất] khi:** quy định hạn mức nhiều tầng mà nền tảng không biểu diễn được; cần chặn "tự duyệt phiếu của mình"; cần nhật ký kiểm toán đầy đủ; cần chạy lại bộ ca sai sau mỗi lần sửa quy trình.

**Code mẫu (đã chạy thử 2026-11-11 bằng `python -I`, không có AI thật).** Kết quả: 3 thao tác sai bị chặn (người không có quyền duyệt; trưởng phòng duyệt trong hạn mức cho phiếu 35 triệu; chi khi chưa duyệt); phiếu đi đúng đường trưởng phòng → giám đốc → kế toán; 5 dòng nhật ký.

```python
CHUYEN = {("moi", "trich_truong"): "cho_kiem", ("cho_kiem", "kiem_dat"): "cho_duyet_tp",
          ("cho_kiem", "kiem_loi"): "tra_lai",
          ("cho_duyet_tp", "duyet"): "cho_duyet_gd", ("cho_duyet_tp", "duyet_trong_han_muc"): "cho_chi",
          ("cho_duyet_tp", "tu_choi"): "tra_lai", ("cho_duyet_gd", "duyet"): "cho_chi",
          ("cho_duyet_gd", "tu_choi"): "tra_lai", ("cho_chi", "da_chi"): "dong"}
QUYEN = {"cho_duyet_tp": {"tp_duan_A"}, "cho_duyet_gd": {"giam_doc"}, "cho_chi": {"ke_toan"}}
HAN_MUC_TP = 20_000_000          # giả định
NHAT_KY = []

def chuyen(phieu, hanh_dong, nguoi):
    k = (phieu["trang_thai"], hanh_dong)
    if k not in CHUYEN: raise ValueError(f"khong cho phep {k}")
    can = QUYEN.get(phieu["trang_thai"])
    if can and nguoi not in can: raise PermissionError(f"{nguoi} khong co quyen")
    if hanh_dong == "duyet_trong_han_muc" and phieu["so_tien"] > HAN_MUC_TP:
        raise ValueError("vuot han muc")
    if hanh_dong == "duyet" and phieu["trang_thai"] == "cho_duyet_tp" and phieu["so_tien"] <= HAN_MUC_TP:
        hanh_dong = "duyet_trong_han_muc"; k = (phieu["trang_thai"], hanh_dong)
    cu, phieu["trang_thai"] = phieu["trang_thai"], CHUYEN[k]
    NHAT_KY.append({"ma": phieu["ma"], "tu": cu, "den": phieu["trang_thai"],
                    "hanh_dong": hanh_dong, "nguoi": nguoi})
```

Mẫu chưa có: chặn người tạo tự duyệt (thêm kiểm `nguoi != phieu["nguoi_tao"]`), lưu bền, khóa chống hai người bấm cùng lúc (Q5).

## 6) Tiêu chí lên Q5 (đo được) [Đề xuất]

1. Một quy trình chạy thật ≥4 tuần hoặc ≥100 phiếu; mọi phiếu truy được trạng thái và nhật ký.
2. 0 lần chuyển trạng thái trái bảng chuyển hoặc vượt quyền (kiểm bằng nhật ký); bộ ca sai có chủ đích chạy lại sau mỗi lần sửa.
3. Tỷ lệ phiếu quá hạn duyệt giảm so với đo nền, hoặc ghi rõ vì sao không.
4. Bước AI (nếu có): tỷ lệ trường bị người sửa được đo; tắt bước AI thì quy trình vẫn chạy.
5. Đã gặp ít nhất một lỗi kỹ thuật (mạng, API, nộp trùng) trong thực tế hoặc khi chạy bóng. Đó là đầu vào cho Q5.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

**a) Công ty xây lắp 30 người: đề nghị thanh toán (tiếp Q1).** Trạng thái: mới → chờ kiểm → chờ trưởng công trình → (nếu > 20 triệu) chờ giám đốc → chờ chi → đóng; nhánh trả lại. AI chỉ trích số hóa đơn, ngày, mã số thuế, tổng tiền từ ảnh; kế toán thấy ảnh cạnh trường. Kế toán chi trên ngân hàng điện tử bằng tay, rồi bấm "đã chi" kèm số giao dịch. Không có hàm chi tiền.

**b) Nhà phân phối nông sản 15 người nhận đơn sỉ qua Zalo.** Trạng thái: tin mới → đơn nháp (AI đọc tin) → chờ sale xác nhận → chờ kho (tồn kho, quy tắc) → chờ giao → đã giao → đã thu tiền. Khách sỉ hay viết "như tuần trước, thêm 2 thùng cam": AI không biết "tuần trước", nên bước nháp phải tra đơn gần nhất bằng code và đưa vào ngữ cảnh, sale xác nhận. Giá sỉ theo bảng giá khách, quy tắc, không AI.

**c) Chuỗi bán lẻ 5 cửa hàng tuyển nhân viên thời vụ dịp Tết.** Trạng thái: CV mới → đã trích trường → chờ cửa hàng trưởng xem → hẹn phỏng vấn → kết quả → gửi thư. AI chỉ trích vị trí, khu vực, có thể làm ca tối không. Cửa hàng trưởng quyết định. Lý do: quyết định tuyển dụng ảnh hưởng quyền lợi người lao động; Luật AI 134/2025 theo báo chí xếp lao động vào lĩnh vực có yêu cầu chặt hơn (chưa đọc toàn văn). CV xóa sau thời hạn công ty quy định.

## 8) Tài liệu tham khảo

| Nguồn | Loại | Mức đọc | Tin cậy |
|---|---|---|---|
| MAP, arXiv 2512.04123 (qua `../nen-tang-bang-chung.md` và `cap-08`) | Khảo sát + phỏng vấn | Nhóm trước đọc toàn văn | Cao, có thiên lệch mẫu |
| TheAgentCompany, arXiv 2412.14161 | Benchmark | Toàn văn mục kết quả | Cao cho giả lập |
| τ-bench, arXiv 2406.12045 | Benchmark | Toàn văn | Cao; mô hình 2024 |
| Samsung SDS, arXiv 2505.20733 | Nghiên cứu ca của nhà cung cấp | Toàn văn mục 3-5 | Trung bình-thấp cho số hiệu quả (tự báo, kỳ vọng); trung bình cho ma trận nhầm lẫn |
| READY, arXiv 2609.02095 | Khung đánh giá | Tóm tắt + mục chính | Trung bình-cao |
| Lark Approval v4 (qua tài liệu thứ cấp: Alibaba Cloud, BytePlus, Zadig) | Tài liệu tích hợp | Qua tóm tắt tìm kiếm | Thấp-trung bình |

## 9) Chưa kiểm chứng

- Lark Approval: endpoint tạo phiếu, sự kiện, hạn mức sự kiện mỗi tháng (tài liệu thứ cấp có nhắc quota): chưa đọc trang chính thức.
- AppSheet, Google Forms phê duyệt: chưa đọc tài liệu.
- Không có nguồn đo tỷ lệ trích trường đúng từ hóa đơn/CV tiếng Việt. Phần đó thuộc nhóm `kiem-tra-ho-so-theo-quy-tac` và người học tự đo.
- Pháp lý tuyển dụng (lưu CV, thời hạn xóa, đồng ý của ứng viên): chưa tra văn bản gốc.
- Hạn mức 20 triệu, ≥100 phiếu, 4 tuần, 2 tuần chạy bóng là đề xuất/giả định.
