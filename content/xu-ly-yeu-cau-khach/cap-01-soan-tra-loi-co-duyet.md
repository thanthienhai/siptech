# Cấp 1 (C1): Soạn trả lời theo SOP, người duyệt mọi tin

> Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** / **[Đề xuất]**.
> Nền tảng dùng lại: bản giao việc 6 phần, Sổ prompt, Project/Gem ở `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`; tra chính sách có trích dẫn ở `../rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md`. File này chỉ viết phần riêng của trả lời khách.

!!! tip "Tóm tắt nhanh"
    Dùng AI để soạn tin trả lời khách thì nhanh, nhưng AI có thể lỡ **hứa điều chính sách của shop không cho phép**, và lời hứa đó vẫn là lời của doanh nghiệp. Bài này dạy một cách làm **không cần biết lập trình**: AI chỉ soạn **phiếu nháp 5 phần** cho nhân viên, nhân viên **duyệt từng tin** rồi mới gửi, và mọi lần duyệt đều được ghi lại. Sau bài, bạn có một trợ lý soạn nháp dùng chung, bảng duyệt và danh sách cụm từ cấm.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** nhân viên chăm sóc khách hàng (CSKH) và chủ shop đã làm xong Cấp C0 (cấp trước đó của nhóm bài này). Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Kết quả của C0: chính sách (bản v2), bảng quyết định, danh mục ý định của khách, danh sách ca "chỉ người làm" và Sổ ca. (Ca "chỉ người làm" là loại ca AI không được tự quyết, chỉ nhân viên mới xử lý.)
- Một tài khoản có thể tạo Project (Claude), Gem (Gemini) hoặc GPT tùy chỉnh. Đây là các tính năng cho bạn lưu sẵn chỉ dẫn và tài liệu để dùng lại, khỏi phải gõ lại mỗi lần.
- Một bảng tính Google Sheet để làm bảng duyệt.

**Sau bài này bạn sẽ có:**
1. Một Project (Claude) hoặc Gem (Gemini) hoặc GPT tùy chỉnh "Soạn trả lời khách" chứa: chính sách v2, bảng quyết định, thư viện mẫu câu, danh sách "chỉ người làm".
2. Đầu ra mỗi lần là **một phiếu nháp 5 phần**, không chỉ là đoạn văn.
3. **Bảng duyệt:** mọi nháp được người duyệt trước khi gửi; ghi lại duyệt nguyên / sửa / bỏ và lý do.
4. Danh sách cụm cấm và quy tắc công khai đang dùng AI.

**Thứ bạn cầm đi được sau bài:** Project/Gem "Soạn trả lời khách" kèm trang hướng dẫn 5 dòng; thư viện mẫu câu `mau-cau-v1`; bảng duyệt Google Sheet; danh sách cụm cấm có lý do.

## 2. Câu hỏi cấp này trả lời / lỗi của C0

Câu hỏi: *"Làm sao để AI soạn nhanh mà không hứa điều chính sách không cho?"*

C0 có SOP (quy trình làm việc chuẩn, viết thành văn bản) nhưng người vẫn soạn tay. Cách dùng AI phổ biến hiện nay là dán tin của khách vào khung chat rồi chép kết quả gửi lại cho khách. Cách này có ba lỗi:
- AI không biết chính sách thật của shop;
- nó viết giọng chắc chắn kể cả khi chỉ đang đoán;
- không ai ghi lại AI đã nói gì.

**[Nguồn thứ cấp: CX Today, 19/2/2024]** Đây là vụ Moffatt v. Air Canada. Chatbot (chương trình trả lời khách tự động trên website) của hãng nói rằng khách có thể mua vé giá thường rồi xin hoàn phần chênh theo giá tang lễ. Chính sách thật của hãng không cho phép điều đó. Air Canada lập luận chatbot là "thực thể riêng". Trọng tài viên bác lập luận này: chatbot "vẫn chỉ là một phần của website"; Air Canada chịu trách nhiệm cho mọi thông tin trên website, "dù thông tin đến từ trang tĩnh hay chatbot". Tổng phải trả là 812,02 CAD, gồm bồi thường, lãi, phí.

**[Đề xuất]** Bài học: lời AI nói với khách là lời của doanh nghiệp. Ở Việt Nam, Luật 19/2023 Điều 10 khoản 1 điểm a cấm lừa dối khách bằng thông tin "sai lệch, không đầy đủ, không chính xác" **[Nguồn: caselaw.vn]**.

!!! tip "Nói đơn giản"
    Khách không phân biệt "AI nói" hay "shop nói". Cái gì đến tay khách thì shop chịu trách nhiệm. Vì vậy ở cấp này, AI chỉ soạn nháp, còn **người** mới là người gửi.

## 3. Kiến thức nền

### 3.1 Phiếu nháp 5 phần [Đề xuất]

Thay vì chỉ nhờ AI "viết giúp câu trả lời", ta bắt AI điền một phiếu gồm 5 phần cố định. Nhờ vậy người duyệt nhìn thấy cả lý do phía sau câu chữ, không chỉ thấy đoạn văn nghe có vẻ hợp lý.

| Phần | Nội dung | Vì sao |
|---|---|---|
| 1. Ý định | Một nhãn trong danh mục C0 (nhãn cho biết khách đang muốn gì, ví dụ đổi trả) | Người duyệt thấy ngay AI hiểu đúng chưa |
| 2. Căn cứ | Dòng nào của bảng quyết định, điều khoản nào (trích nguyên văn) | Kiểm được; xem cách kiểm trích ở `../rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md` |
| 3. Đề xuất xử lý | "Đủ điều kiện đổi" / "Không đủ" / "CẦN NGƯỜI QUYẾT" | Tách quyết định khỏi câu chữ |
| 4. Nháp gửi khách | Theo mẫu câu, xưng hô của shop | |
| 5. Cần người kiểm | Thông tin còn thiếu, điểm AI không chắc | Chống "duyệt cho xong" |

!!! tip "Nói đơn giản"
    Phiếu này giống một phiếu trình sếp: ghi rõ "em hiểu khách muốn gì", "em dựa vào điều nào", "em đề xuất xử lý thế nào", "đây là câu em định gửi", và "chỗ này em chưa chắc, anh/chị xem giúp". Người duyệt chỉ cần đối chiếu từng phần.

### 3.2 Mẫu câu (macro) thay vì soạn từ đầu

**[Nguồn]** Nubank (một ngân hàng số) dùng macro: mẫu trả lời viết sẵn để nhân viên điều chỉnh, không soạn từ đầu (2606.08867, mục 4.2).

**[Đề xuất]** Với SME (doanh nghiệp vừa và nhỏ): chuẩn bị 10-20 mẫu câu cho các tình huống thường gặp, viết bằng giọng của shop. AI chỉ điền chỗ trống và chỉnh cho khớp tin khách. Câu nào ngoài mẫu thì người duyệt soi kỹ hơn.

**Tiếng Việt cần ghi rõ trong mẫu:** cách xưng hô (shop/em - anh/chị), có dùng "dạ, ạ" không, có emoji không, độ dài tối đa trên Zalo/Messenger.

### 3.3 Người duyệt mọi tin ở cấp này

**[Nguồn]** MAP (arXiv 2512.04123): 68% hệ thống production (hệ thống đang chạy thật cho người dùng, không phải bản thử nghiệm) chạy dưới 10 bước rồi chuyển cho người; mẫu chung là "agent đề xuất, chuyên gia duyệt" (xem `../nen-tang-bang-chung.md`). Ở đây "agent" là chương trình AI tự làm một chuỗi việc.

**[Nguồn]** Brynjolfsson, Li, Raymond (NBER, 5.179 nhân viên hỗ trợ khách): trợ lý AI tăng năng suất khoảng 14%, người mới khoảng 34% (qua `../thuc-trang-sme-viet-nam.md`). NBER là một viện nghiên cứu kinh tế của Mỹ.

**[Đề xuất]** Ở C1, AI là trợ lý cho nhân viên, không nói thẳng với khách.

### 3.4 Công khai đang dùng AI

- **[Nguồn, theo tóm tắt]** Luật 71/2025/QH15 Điều 44: hệ thống AI tương tác trực tiếp với người phải thông báo cho người dùng biết, trừ khi hiển nhiên (xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 4.4; chưa đọc toàn văn).
- **[Nguồn, chỉ đọc tóm tắt]** Luo, Tong, Fang, Qu (Marketing Science, 2019): thí nghiệm thực địa hơn 6.200 khách nhận cuộc gọi bán hàng từ chatbot hoặc người; khi công khai là máy trước cuộc gọi, tỉ lệ mua giảm hơn 79,7%; chatbot không công khai bán tốt ngang nhân viên giỏi. Đây là cuộc gọi bán hàng chủ động năm 2019, không phải trả lời yêu cầu khách bằng chat. Không nên khái quát.
- **[Đề xuất]** Ở C1 người duyệt rồi người gửi, nên tin là của nhân viên. Từ C2 trở đi, nếu có tin gửi thẳng không qua người, phải ghi rõ "trả lời tự động" hoặc "trợ lý AI". Đánh đổi doanh thu không phải lý do để giấu.

!!! warning "Cẩn thận"
    Các điều luật nêu ở trên chỉ để bạn biết hướng đi, **không phải tư vấn pháp lý**. Hai điều luật này mới đọc qua tóm tắt, chưa đọc toàn văn. Khi cần áp dụng cho doanh nghiệp của bạn, hãy hỏi người có chuyên môn pháp lý.

### 3.5 Cụm cấm: hàng rào bằng code, không bằng prompt

Prompt (chỉ dẫn bạn viết cho AI) nói "đừng hứa hoàn tiền" thì vẫn có lúc AI bỏ qua. Một hàm kiểm (đoạn code ngắn tự động rà văn bản) chạy trên mọi nháp trước khi người duyệt thấy thì không bao giờ quên (xem mục 5). "Cụm cấm" là những cụm từ mà nháp gửi khách không được chứa, ví dụ lời hứa hoàn tiền ngay.

!!! tip "Nói đơn giản"
    Dặn AI bằng lời giống như nhắc nhân viên miệng: có khi quên. Dùng danh sách cụm cấm giống như dán một tờ giấy cạnh màn hình và có người soát từng tin: chắc chắn hơn.

## 4. Chuỗi bài nhỏ

Sáu bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và (nếu có) lỗi hay gặp để tránh.

### Bài 1.1: Thư viện mẫu câu
- **Việc cần làm:** từ Sổ ca C0, lấy câu trả lời tốt nhất cho mỗi tình huống, sửa thành mẫu có chỗ trống `{ten_khach}`, `{ma_don}`, `{han_doi}`. Làm 10-20 mẫu.
- **Bạn có sau bài:** `mau-cau-v1` (bảng: mã mẫu, tình huống, câu, ghi chú giọng).
- **Lỗi hay gặp:** mẫu quá dài cho Zalo; mẫu có câu hứa ("shop sẽ hoàn ngay").

### Bài 1.2: Project/Gem "Soạn trả lời khách"
- **Việc cần làm:** phần chỉ dẫn của Project/Gem gồm bản giao việc 6 phần (`../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` mục 3.2) và yêu cầu xuất phiếu 5 phần. Tải lên: chính sách v2, bảng quyết định, mẫu câu, danh sách "chỉ người làm". **Không tải** Sổ ca có dữ liệu khách.
- **Ràng buộc bắt buộc trong chỉ dẫn:** không tự suy ra điều chính sách không nói; ca thuộc "chỉ người làm" thì phần 3 ghi "CẦN NGƯỜI QUYẾT" và phần 4 chỉ là câu báo đã nhận.
- **Bạn có sau bài:** Project/Gem dùng được và trang hướng dẫn 5 dòng.

### Bài 1.3: Ẩn danh tin khách trước khi dán
- **Việc cần làm:** nhân viên thay tên, SĐT, địa chỉ, mã đơn bằng mã trước khi dán vào AI. Nếu dùng gói doanh nghiệp có điều khoản không huấn luyện (nhà cung cấp cam kết không dùng dữ liệu của bạn để dạy AI), vẫn nên làm. Xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 3.2.
- **Lỗi hay gặp:** dán ảnh chụp màn hình Zalo có SĐT và ảnh đại diện khách.

### Bài 1.4: Chạy bộ ca mẫu
- **Việc cần làm:** chạy 20-30 ca của C0 qua Project/Gem, mỗi ca 3 lần. Chấm 4 tiêu chí có/không: ý định đúng; đề xuất xử lý đúng; không có câu trái chính sách; ca "chỉ người làm" được đánh dấu.
- **Bạn có sau bài:** bảng chấm. Cách đọc kết quả khi số ca còn ít (n nhỏ): `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` mục 3.2.
- **Lỗi hay gặp:** chỉ chấm câu văn có hay không.

### Bài 1.5: Bảng duyệt và lý do sửa
- **Việc cần làm:** lập một Google Sheet với các cột: thời điểm, kênh, mã ca, ý định AI, đề xuất AI, nháp AI, bản đã gửi, kết quả duyệt (nguyên/sửa nhẹ/sửa nặng/bỏ), lý do (sai ý định / sai chính sách / sai giọng / thiếu thông tin / khác), người duyệt.
- **Bạn có sau bài:** bảng duyệt chạy 2 tuần.
- **Lỗi hay gặp:** chỉ ghi khi sửa; không ghi ai duyệt.

### Bài 1.6: Cụm cấm và kiểm công khai AI
- **Việc cần làm (không code):** lập danh sách 10-20 cụm cấm, dán cạnh bảng duyệt; người duyệt soát bằng mắt.
- **Việc cần làm (có code):** chạy hàm `kiem()` ở mục 5 trên mỗi nháp.
- **Bạn có sau bài:** danh sách cụm cấm có lý do.

## 5. Đường không code vs có code

Bài này có hai cách làm. Cách không code đủ dùng khi mới bắt đầu. Cách code nhẹ chỉ thêm một hàm kiểm tự động để rà cụm cấm.

| | Không code | Code nhẹ |
|---|---|---|
| Soạn | Project/Gem/GPT, nhân viên dán tin đã ẩn danh | Như bên trái; code chỉ để kiểm |
| Kiểm | Người soát danh sách cụm cấm | Hàm kiểm cụm cấm chạy trên mọi nháp |
| Ghi lại | Bảng duyệt Google Sheet | Như bên trái |

**Đoạn mã dưới đây làm gì?** Nó nhận một bản nháp trả lời khách, bỏ dấu tiếng Việt để dễ so khớp, rồi tìm xem nháp có chứa cụm cấm nào không (ví dụ hứa hoàn tiền ngay, hứa thời gian giao chắc chắn, đổ lỗi cho bên vận chuyển) và có dòng công khai đang dùng AI hay không. Kết quả là danh sách các lỗi tìm thấy. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

Mã mẫu (đã chạy thử bằng `python -I -X utf8`, 2026-11-11; không gọi API, tức là không kết nối đến dịch vụ AI nào):

```python
import re, unicodedata
def bo_dau(s):
    s = unicodedata.normalize("NFD", s.lower()).replace("đ", "d")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

CUM_CAM = {
    r"hoan tien (ngay|lien|100|toan bo)": "hua hoan tien",
    r"cam ket|dam bao 100": "cam ket",
    r"mien phi (doi|ship|van chuyen)": "hua mien phi",
    r"boi thuong": "boi thuong",
    r"chac chan (se )?(giao|nhan|toi)": "hua thoi gian",
    r"(do|loi) (ben )?(van chuyen|shipper)": "do loi cho ben thu ba",
}
BAT_BUOC = [r"\[ai\]|tro ly ai|tra loi tu dong"]

def kiem(nhap):
    t = bo_dau(nhap)
    loi = [ly for mau, ly in CUM_CAM.items() if re.search(mau, t)]
    loi += ["thieu cong khai AI" for m in BAT_BUOC if not re.search(m, t)]
    return loi
# kiem("[AI] Dạ shop sẽ hoàn tiền ngay cho chị ạ, chắc chắn giao trong hôm nay.")
#   -> ['hua hoan tien', 'hua thoi gian']
# kiem("Dạ lỗi do bên vận chuyển chị ơi.") -> ['do loi cho ben thu ba', 'thieu cong khai AI']
```

Hàm này chỉ bắt cụm đã biết. Nó không thay người duyệt.

!!! tip "Nói đơn giản"
    Hàm kiểm giống một chiếc rây: nó giữ lại những câu có từ khóa nguy hiểm đã được liệt kê. Câu nguy hiểm nhưng dùng từ khác thì rây không bắt được, nên người duyệt vẫn là chốt chặn cuối cùng.

**Buộc chuyển sang C2 (code) khi [Đề xuất]:** trên khoảng 50 tin mỗi ngày làm nhân viên mất thời gian dán qua lại; cần phân loại để xếp hàng đợi theo mức khẩn; cần nhật ký tự động thay vì chép tay.

## 6. Tiêu chí lên cấp (C1 → C2) [Đề xuất]

Bạn có thể sang cấp tiếp theo (C2) khi đạt đủ các điều sau:

1. Bảng duyệt chạy ≥2 tuần, ≥100 tin.
2. Tỉ lệ "bỏ" (nháp không dùng được) ≤20%; lý do sửa đã phân loại.
3. **0 tin gửi khách chứa câu trái chính sách** sau duyệt trong 2 tuần đó (đo bằng rà ngẫu nhiên 20 tin đã gửi).
4. Trên bộ ca mẫu, mọi ca "chỉ người làm" đều được đánh dấu CẦN NGƯỜI QUYẾT ở cả 3 lần chạy.
5. Nhân viên đã quen ẩn danh: rà ngẫu nhiên 20 lần dán, 0 lần còn SĐT.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung.

### 7.a Shop mỹ phẩm online
Tin khách: "sp em nhận bị móp hộp, e muốn trả". Phiếu nháp được điền như sau:
1. Ý định: `doi_tra`.
2. Căn cứ: dòng 2 bảng quyết định "lỗi do shop hoặc vận chuyển" + điều khoản "báo trong 48 giờ kèm ảnh".
3. Đề xuất: CẦN THÔNG TIN (thiếu ảnh, thiếu ngày nhận).
4. Nháp: "Dạ shop xin lỗi chị vì hộp bị móp ạ. Chị gửi giúp shop ảnh hộp và mã đơn để shop kiểm tra nhé."
5. Cần người kiểm: hàng mỹ phẩm đã mở có đổi được không, chính sách im lặng → bổ sung vào C0.

### 7.b Trung tâm tiếng Anh
Phụ huynh nhắn xin học bù và hỏi bảo lưu học phí. Bảo lưu có tiền nên thuộc "chỉ người làm": nháp chỉ báo đã nhận và hẹn giờ tư vấn viên gọi lại. Học bù theo lịch có sẵn: AI soạn từ mẫu, nhân viên duyệt.

### 7.c Nhà xe khách liên tỉnh
Khách hỏi đổi giờ đi. Mẫu câu có chỗ trống giờ và phí đổi. Phí lấy từ bảng giá, người duyệt đối chiếu. Khách nói "xe đến trễ làm lỡ việc": khiếu nại, chuyển người.

## 8. Tài liệu tham khảo

| Nguồn | Loại | Đọc | Tin cậy |
|---|---|---|---|
| Nubank, arXiv 2606.08867 | Bài báo, triển khai thật | Phần lớn toàn văn | Cao |
| MAP, arXiv 2512.04123 | Bài báo khảo sát | Qua `../nen-tang-bang-chung.md` | Cao |
| Brynjolfsson, Li, Raymond, NBER WP 31161 | Nghiên cứu có đối chứng | Qua `../thuc-trang-sme-viet-nam.md` | Cao cho bối cảnh đó |
| CX Today, "Court orders Air Canada to pay out for chatbot's bad advice", https://www.cxtoday.com/contact-center/court-orders-air-canada-to-pay-out-for-chatbots-bad-advice/ | Báo ngành | Đọc qua công cụ tóm tắt | Trung bình (bản án CanLII trả 403) |
| Luo, Tong, Fang, Qu, *Machines vs. Humans*, Marketing Science 38(6):937-947, 2019, doi 10.1287/mksc.2019.1192 | Bài báo có thí nghiệm thực địa | **Chỉ tóm tắt** (RePEc, thông cáo báo chí) | Trung bình cho con số; chưa đọc bài |
| Luật 19/2023/QH15 Điều 10, caselaw.vn | Văn bản luật | Qua công cụ tóm tắt | Trung bình |

## 9. Chưa kiểm chứng

- Số tiền và lập luận trong bản án Moffatt v. Air Canada (2024 BCCRT 149): chỉ qua báo. Một nguồn khác ghi phần bồi thường 650,88; cần đọc bản án.
- Con số 79,7% của Luo và cs.: chỉ qua tóm tắt; chưa rõ bối cảnh ngành và nước.
- Điều 44 Luật 71/2025: chỉ qua tóm tắt; chưa rõ "hiển nhiên" nghĩa là gì và có áp dụng khi người duyệt trước khi gửi không.
- Ngưỡng 20% bỏ, 100 tin, 2 tuần: đề xuất.
- Danh sách cụm cấm là ví dụ; mỗi shop phải tự lập.
