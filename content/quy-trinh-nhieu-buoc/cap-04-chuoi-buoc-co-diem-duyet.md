# Q4 — Chuỗi bước có trạng thái và điểm duyệt

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

!!! tip "Tóm tắt nhanh"
    Khi một việc đi qua nhiều bước và nhiều người duyệt, phiếu rất dễ lạc, người duyệt vượt quyền, hoặc không ai biết phiếu đang nằm ở đâu. Bài này dạy cách làm quy trình như một **máy trạng thái**: mỗi phiếu luôn ở đúng một trạng thái, chỉ được chuyển theo một bảng cho phép, và mỗi lần chuyển đều kiểm quyền và ghi nhật ký. AI, nếu dùng, chỉ làm một hai bước hẹp và kết quả của nó luôn qua cổng kiểm hoặc người duyệt. Sau bài, bạn có một quy trình chạy trên phiếu thật, có hàng đợi duyệt và nhật ký.

## 1) Mục tiêu và người đọc

**Bài này dành cho ai:** chủ SME (doanh nghiệp nhỏ và vừa), trưởng phòng kế toán, nhân sự, kinh doanh. Bạn đã làm xong luồng ở cấp Q1 và có thể đã có bộ định tuyến ở cấp Q2.

**Bạn cần chuẩn bị:**
- Luồng đã làm ở Q1 và bảng ở Q0 (bài Q4.1 sẽ lấy bảng Q0 làm đầu vào).
- Một quy trình thật của bạn để làm thử: đơn hàng, đề nghị thanh toán, hoặc tuyển dụng.
- Một nơi để lưu bảng phiếu: Google Sheets, Lark Base hoặc SQLite (SQLite là một cơ sở dữ liệu nhỏ nằm gọn trong một tệp).

**Sau bài này bạn sẽ có:** một quy trình nhiều bước (đơn hàng, đề nghị thanh toán, hoặc tuyển dụng) chạy như **máy trạng thái**. Nói cách khác:
- mỗi phiếu có một trạng thái;
- chỉ chuyển trạng thái qua bảng chuyển cho phép;
- mỗi lần chuyển, kiểm quyền bằng code (đoạn chương trình, không dựa vào lời dặn AI) và ghi nhật ký.

AI, nếu có, chỉ ở 1-2 bước hẹp (trích trường, phân loại) và kết quả của nó luôn qua cổng kiểm hoặc người duyệt. "Trích trường" là đọc một tài liệu rồi điền các thông tin cần thiết vào ô, ví dụ số tiền, ngày. "Cổng kiểm" là một bước kiểm tra tự động nằm giữa AI và người duyệt.

**Thứ bạn cầm đi được:** quy trình trên phiếu thật, có hàng đợi duyệt và nhật ký. Quy trình chạy được cả khi tắt hẳn bước AI (người làm thay bước đó).

## 2) Câu hỏi cấp này trả lời / lỗi của cấp trước

**Câu hỏi:** "Nối nhiều bước, nhiều người duyệt lại với nhau thế nào để không mất phiếu, không ai duyệt vượt quyền, và biết phiếu đang ở đâu?"

**Lỗi của Q1-Q3:** các luồng rời nhau. Trạng thái phiếu nằm trong đầu người hoặc trong tin nhắn. Duyệt qua Zalo không có dấu vết. Không ai chặn trường hợp "nhân viên tự duyệt phiếu của mình" hay "chi tiền khi chưa duyệt".

**Phần đã có ở nhóm RAG, không lặp lại:** phân biệt workflow/agent, 5 mẫu workflow, thiết kế điểm duyệt (khi nào, ai, duyệt gì, hàng đợi, chống duyệt cho xong), gói chuyển giao, trần bước, lỗi cộng dồn pⁿ: `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.1-3.7. Phân hạng công cụ đọc/ghi A-D và idempotent: `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` mục 3.4-3.5. Cấp này chỉ thêm phần riêng của quy trình nghiệp vụ: **trạng thái, quyền, hạn mức, và chỗ đặt AI trong ba nghiệp vụ cụ thể**.

Một vài từ ở đoạn trên, giải thích ngắn:
- **Workflow** là quy trình có các bước định sẵn, chạy theo đường đã vẽ. **Agent** là AI tự quyết định bước tiếp theo.
- **Điểm duyệt** là chỗ quy trình dừng lại chờ một người xem và bấm đồng ý hoặc từ chối.
- **Idempotent** nghĩa là làm một thao tác hai lần thì kết quả vẫn như làm một lần (ví dụ bấm "chi tiền" hai lần mà chỉ chi một lần).
- **Lỗi cộng dồn pⁿ**: nếu mỗi bước đúng với xác suất p thì n bước nối nhau đúng với xác suất p nhân với chính nó n lần, nên càng nhiều bước càng dễ sai.

## 3) Kiến thức nền

### 3.1 Bằng chứng [Nguồn]

Các nghiên cứu dưới đây cho thấy vì sao nên để AI làm ít bước, còn người và quy tắc giữ các bước quan trọng.

- **MAP (arXiv 2512.04123):** 16/20 ca dùng workflow có cấu trúc; 68% hệ thống chạy ≤10 bước rồi chuyển người; 15/20 ca chạy bất đồng bộ (không bắt người dùng ngồi chờ, kết quả trả về sau); 66% chấp nhận độ trễ cỡ phút trở lên. "Agents suggest actions, experts approve execution" (tạm dịch: agent đề xuất hành động, chuyên gia duyệt việc thực thi).
- **TheAgentCompany:** khi để agent tự làm trọn việc nhiều bước (trung bình 27,2 bước), mô hình tốt nhất hoàn thành 30,3%. Ví dụ việc "hoàn tiền công tác" trong hình minh họa của bài gồm truy cập hóa đơn, kiểm tiêu chí, hỏi người phụ trách, xác nhận số tiền; agent được chấm theo từng mốc. Bài nêu agent yếu nhất ở giao tiếp với đồng nghiệp và phần mềm văn phòng web.
- **τ-bench:** việc càng nhiều hành động ghi càng khó (hình 6 của bài); 25% lỗi là quyết định sai do không theo quy định nghiệp vụ, ví dụ đổi từng món một trong khi quy định chỉ cho gọi lệnh đổi một lần.
- **Samsung SDS (arXiv 2505.20733):** quy trình chi phí 4 bước: OCR/IDP trích trường (OCR là đọc chữ từ ảnh; IDP là xử lý tài liệu thông minh) → phân loại theo cơ sở dữ liệu chính sách → LLM hỗ trợ ngoại lệ (LLM là mô hình ngôn ngữ lớn, tức loại AI đứng sau các chatbot) → người quyết định cuối, hệ thống học từ quyết định đó. Trên 1.448 hóa đơn giấy: độ chính xác 0,83, precision 1, recall 0,82. (Precision 1 nghĩa là hóa đơn hệ thống cho qua đều hợp lệ; recall 0,82 nghĩa là trong số hóa đơn hợp lệ, hệ thống nhận ra khoảng 82%.) Nghĩa là 242 hóa đơn hợp lệ bị hệ thống đánh dấu, phải qua người. Tác giả là nhóm của nhà cung cấp; con số "giảm 80-90% thời gian" nằm trong phần "hiệu quả kỳ vọng" chứ không phải phép đo có đối chứng.
- **READY:** cùng một agent, lượng người duyệt cần thiết phụ thuộc chính sách chuyển người; nên quyết định "bao nhiêu % phiếu qua người" bằng số đo, không bằng cảm giác.

!!! tip "Nói đơn giản"
    Đừng để AI tự chạy trọn một quy trình dài. Để AI làm phần nhỏ, rồi cho người duyệt những chỗ có tiền hoặc quyền lợi. Và hãy đo xem bao nhiêu phiếu cần người xem, đừng đoán.

### 3.2 Máy trạng thái thay cho "chuỗi prompt" [Đề xuất]

"Prompt" là câu lệnh bạn gõ cho AI. Cách làm dưới đây thay vì dặn AI từng bước, ta đặt luật vào một bảng và để code kiểm.

- Mỗi phiếu có `trang_thai` thuộc danh sách đóng (chỉ gồm các giá trị bạn đã liệt kê trước, không có giá trị lạ).
- Bảng `CHUYEN[(trạng thái, hành động)] → trạng thái mới`. Hành động không có trong bảng thì code từ chối.
- Mỗi trạng thái chờ duyệt gắn **tập người có quyền**. Code kiểm, không phải prompt.
- **Hạn mức** (ví dụ trưởng phòng duyệt ≤ 20 triệu) nằm trong một bảng cấu hình, không nằm trong lời dặn AI.
- **Tách người:** người tạo phiếu không được duyệt phiếu của mình; người duyệt không được là người chi.
- Bước AI là một hành động như mọi hành động khác (`trich_truong`), kết quả đi vào trạng thái "chờ kiểm", không nhảy thẳng sang "đã duyệt".
- Trạng thái lưu ở **một nơi** (một bảng Sheets/Lark Base/SQLite), không lưu trong lịch sử chat.

!!! tip "Nói đơn giản"
    Hãy hình dung phiếu như một con tốt trên bàn cờ: mỗi lúc chỉ đứng ở một ô, và chỉ đi theo các nước đã ghi trong luật. Ai được đi nước nào, đi tới mức tiền nào, đều ghi trong bảng. Người nào đi sai luật thì máy từ chối, không cần nhờ AI nhớ luật.

### 3.3 Đặt AI ở đâu trong ba nghiệp vụ [Đề xuất]

Bảng dưới cho thấy ở mỗi nghiệp vụ, bước nào có thể dùng AI và bước nào không.

| Nghiệp vụ | Bước có thể dùng AI | Bước không dùng AI | Ghi chú |
|---|---|---|---|
| Đơn hàng từ tin nhắn | Đọc tin tự do thành đơn nháp (sản phẩm, số lượng, địa chỉ) | Giá, tồn kho, phí ship, khuyến mãi (quy tắc); xác nhận với khách (người, mẫu sẵn); tạo đơn chính thức (code sau khi người xác nhận) | Soạn trả lời khách: nhóm `xu-ly-yeu-cau-khach` |
| Đề nghị thanh toán | Trích trường từ ảnh hóa đơn/chứng từ | Định tuyến theo dự án và hạn mức (quy tắc); duyệt (người); chi (người, ngoài hệ thống) | Kiểm chứng từ theo quy tắc: nhóm `kiem-tra-ho-so-theo-quy-tac` |
| Tuyển dụng | Trích trường CV (vị trí, kinh nghiệm năm, khu vực) vào bảng | Loại/nhận ứng viên (người); hẹn lịch (quy tắc + lịch); gửi thư mời (người bấm) | Không cho AI chấm điểm/xếp hạng ứng viên ở cấp này |

## 4) Chuỗi bài nhỏ

Sáu bài dưới đây làm theo thứ tự, từ vẽ sơ đồ đến chạy thật. Mỗi bài ghi việc cần làm và thứ bạn có sau bài.

### Bài Q4.1 — Vẽ máy trạng thái
- **Việc cần làm:** từ bảng Q0, liệt kê trạng thái (5-9) và hành động. Vẽ ô và mũi tên (mỗi ô là một trạng thái, mỗi mũi tên là một hành động đưa phiếu sang ô khác). Mỗi trạng thái chờ ghi: ai có quyền, hạn xử lý.
- **Bạn có sau bài:** sơ đồ + bảng chuyển + bảng quyền.
- **Lỗi hay gặp:** trạng thái "đang xử lý" chung chung; quên trạng thái "trả lại" và "hủy".

### Bài Q4.2 — Bảng phiếu là nguồn sự thật
- **Việc cần làm:** lập một bảng phiếu (Sheets/Lark Base/SQLite) với `ma_phieu`, `trang_thai`, `nguoi_tao`, `nguoi_xu_ly`, `han`, `so_tien`, link chứng từ. Mọi luồng đọc/ghi qua bảng này. Khóa sửa tay cột `trang_thai`.
- **Bạn có sau bài:** bảng phiếu + quyền truy cập.

### Bài Q4.3 — Kiểm chuyển trạng thái bằng code
- **Việc cần làm:** viết hàm `chuyen(phieu, hanh_dong, nguoi)` (hàm là một đoạn code làm một việc cố định) để kiểm bảng chuyển, quyền, hạn mức; ghi nhật ký. Thử các ca sai có chủ đích:
  - người không có quyền duyệt;
  - duyệt vượt hạn mức;
  - chi khi chưa duyệt;
  - người tạo tự duyệt.
- **Bạn có sau bài:** hàm + bảng ca sai và kết quả "đã chặn".

### Bài Q4.4 — Gắn bước AI hẹp
- **Việc cần làm:** chỉ một bước (ví dụ trích trường hóa đơn). Đầu ra là JSON (một cách viết thông tin thành các cặp "tên trường: giá trị" để máy đọc được), có trường `null` (nghĩa là "để trống") khi không chắc. Kết quả vào `cho_kiem`; cổng kiểm bằng code (số tiền là số dương, ngày hợp lệ, mã số thuế đúng độ dài) rồi mới sang người duyệt. Người duyệt thấy ảnh gốc cạnh trường đã trích.
- **Bạn có sau bài:** bước AI + tỷ lệ trường bị người sửa trên 30 phiếu.

### Bài Q4.5 — Hàng đợi duyệt và nhắc hạn
- **Việc cần làm:** dùng thiết kế hàng đợi ở `cap-08-quy-trinh-nhieu-buoc.md` bài 8.4 (hàng đợi là danh sách phiếu đang chờ người duyệt); nhắc hạn bằng luồng Q1. Với Lark: Lark Approval có API tạo phiếu và sự kiện thay đổi trạng thái (theo tài liệu thứ cấp, cần kiểm); với Google: Forms + Apps Script + email có link duyệt. (API là cổng để một phần mềm nói chuyện với phần mềm khác; Apps Script là công cụ viết đoạn lệnh nhỏ chạy trong Google Sheets và Forms.)
- **Bạn có sau bài:** hàng đợi chạy 2 tuần; tỷ lệ phiếu quá hạn.

### Bài Q4.6 — Chạy song song với cách cũ
- **Việc cần làm:** 2 tuần đầu chạy song song: phiếu vẫn làm cách cũ, hệ thống mới chạy "bóng" (không ghi ra ngoài). So kết quả từng phiếu.
- **Bạn có sau bài:** bảng chênh lệch; quyết định bật thật.

## 5) Đường không code vs có code; khi nào buộc chuyển

Bài này có hai đường. Đường không code dùng công cụ có sẵn và đủ để bắt đầu. Đường có code dùng một đoạn chương trình ngắn để kiểm thay con người.

| | Không code | Có code |
|---|---|---|
| Trạng thái + duyệt | Lark Approval; Lark Base với trường trạng thái + automation; Google Forms + Sheets + AppSheet (chưa kiểm AppSheet) | Bảng SQLite/Sheets + hàm chuyển trạng thái (mẫu dưới) |
| Quyền | Phân quyền của nền tảng (ai sửa cột nào) | Kiểm trong hàm `chuyen` |
| Bước AI | Bước gọi AI trong Make/n8n; hoặc người dán vào Gem/Project | Gọi API, kiểm JSON, cổng kiểm |

(Make và n8n là các công cụ kéo thả để nối các bước lại với nhau. Gem và Project là tính năng của Gemini và Claude cho phép lưu sẵn chỉ dẫn để dùng lại.)

**Buộc chuyển sang code [Đề xuất] khi:** quy định hạn mức nhiều tầng mà nền tảng không biểu diễn được; cần chặn "tự duyệt phiếu của mình"; cần nhật ký kiểm toán đầy đủ; cần chạy lại bộ ca sai sau mỗi lần sửa quy trình.

**Đoạn mã dưới đây làm gì?** Nó là phiên bản rút gọn của hàm `chuyen`. Trước khi cho phiếu đổi trạng thái, nó hỏi lần lượt: hành động này có nằm trong bảng cho phép không, người này có quyền ở trạng thái hiện tại không, số tiền có vượt hạn mức trưởng phòng không. Nếu qua hết thì nó đổi trạng thái và ghi một dòng nhật ký. Nếu sai thì nó dừng và báo lỗi. Bạn **không cần đọc hiểu từng dòng**; chỉ cần nắm ý này, và nhờ người biết lập trình (hoặc nhờ AI) chạy thử giúp khi cần.

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

!!! tip "Nói đơn giản"
    Đoạn mã trên giống một bảo vệ đứng cửa với một cuốn sổ luật. Ai muốn đưa phiếu sang bước tiếp theo đều phải qua bảo vệ. Bảo vệ kiểm luật, kiểm quyền, kiểm tiền, rồi mới mở cửa và ghi tên người đi qua vào sổ.

## 6) Tiêu chí lên Q5 (đo được) [Đề xuất]

Bạn có thể sang Q5 khi đạt đủ các điều sau:

1. Một quy trình chạy thật ≥4 tuần hoặc ≥100 phiếu; mọi phiếu truy được trạng thái và nhật ký.
2. 0 lần chuyển trạng thái trái bảng chuyển hoặc vượt quyền (kiểm bằng nhật ký); bộ ca sai có chủ đích chạy lại sau mỗi lần sửa quy trình.
3. Tỷ lệ phiếu quá hạn duyệt giảm so với đo nền (số đo lấy trước khi áp dụng quy trình mới), hoặc ghi rõ vì sao không.
4. Bước AI (nếu có): tỷ lệ trường bị người sửa được đo; tắt bước AI thì quy trình vẫn chạy.
5. Đã gặp ít nhất một lỗi kỹ thuật (mạng, API, nộp trùng) trong thực tế hoặc khi chạy bóng. Đó là đầu vào cho Q5.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

Ba tình huống dưới đây là giả định, để bạn dễ hình dung cách áp dụng.

**a) Công ty xây lắp 30 người: đề nghị thanh toán (tiếp Q1).** Trạng thái: mới → chờ kiểm → chờ trưởng công trình → (nếu > 20 triệu) chờ giám đốc → chờ chi → đóng; nhánh trả lại. AI chỉ trích số hóa đơn, ngày, mã số thuế, tổng tiền từ ảnh; kế toán thấy ảnh cạnh trường. Kế toán chi trên ngân hàng điện tử bằng tay, rồi bấm "đã chi" kèm số giao dịch. Không có hàm chi tiền.

**b) Nhà phân phối nông sản 15 người nhận đơn sỉ qua Zalo.** Trạng thái: tin mới → đơn nháp (AI đọc tin) → chờ sale xác nhận → chờ kho (tồn kho, quy tắc) → chờ giao → đã giao → đã thu tiền. Khách sỉ hay viết "như tuần trước, thêm 2 thùng cam": AI không biết "tuần trước", nên bước nháp phải tra đơn gần nhất bằng code và đưa vào ngữ cảnh (phần thông tin đưa kèm cho AI đọc), sale xác nhận. Giá sỉ theo bảng giá khách, quy tắc, không AI.

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

(Benchmark là bộ bài kiểm chuẩn để so các hệ thống AI với nhau. Ma trận nhầm lẫn là bảng đếm xem hệ thống đoán đúng và đoán sai ở mỗi loại ra sao.)

## 9) Chưa kiểm chứng

- Lark Approval: endpoint tạo phiếu, sự kiện, hạn mức sự kiện mỗi tháng (tài liệu thứ cấp có nhắc quota): chưa đọc trang chính thức.
- AppSheet, Google Forms phê duyệt: chưa đọc tài liệu.
- Không có nguồn đo tỷ lệ trích trường đúng từ hóa đơn/CV tiếng Việt. Phần đó thuộc nhóm `kiem-tra-ho-so-theo-quy-tac` và người học tự đo.
- Pháp lý tuyển dụng (lưu CV, thời hạn xóa, đồng ý của ứng viên): chưa tra văn bản gốc.
- Hạn mức 20 triệu, ≥100 phiếu, 4 tuần, 2 tuần chạy bóng là đề xuất/giả định.
