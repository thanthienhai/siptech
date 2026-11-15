# Cấp 5 (C5): Chuyển giao cho người, khiếu nại và khách bực

> Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** / **[Đề xuất]**.
> Dùng lại: gói chuyển giao tối thiểu và điểm duyệt ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4-3.5. File này viết phần riêng: **khi nào chuyển**, **chuyển quá nhiều cũng là lỗi**, **khiếu nại có hạn luật**, **tin chủ động qua Zalo**.

!!! tip "Tóm tắt nhanh"
    AI trả lời khách rất tốt ở các ca đơn giản, nhưng có những ca phải dừng lại và giao cho người: khách bực, khiếu nại, chuyện tiền bạc, chuyện an toàn. Bài này dạy bạn chia rõ **khi nào chuyển**, **chuyển thế nào để khách không phải kể lại từ đầu**, và **đo xem mình chuyển thừa hay chuyển thiếu**. Sau bài, bạn có bảng 10 lý do chuyển, mẫu gói chuyển giao, câu mẫu khi chuyển và quy trình khiếu nại có hạn báo "đã nhận". Làm được hoàn toàn bằng Google Sheet; phần code chỉ là lựa chọn thêm.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** trưởng nhóm CSKH (chăm sóc khách hàng), chủ shop, hoặc người rành kỹ thuật ở mức nhẹ. Bạn không cần biết lập trình để làm phần chính. Bạn nên đã học xong cấp C2. Cấp C3 và C4 giúp ích nhưng không bắt buộc.

**Bạn cần chuẩn bị:**
- Danh sách người, nhóm trong shop hoặc công ty có thể nhận ca khi AI chuyển (trưởng nhóm, quản lý, người trực).
- Một bảng tính Google Sheet làm hàng chuyển (mỗi ca là một dòng).
- Gói chuyển giao tối thiểu và điểm duyệt đã có ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4-3.5, để dùng lại.

**Sau bài này bạn sẽ có:**
1. Danh sách lý do chuyển cố định (10 lý do), mỗi ca chuyển ghi đúng một lý do chính.
2. Gói chuyển giao đủ để người nhận **không phải hỏi lại khách**.
3. Quy trình khiếu nại có hạn "báo đã nhận" tính bằng code (hoặc tính tay nếu bạn chưa dùng code).
4. Hai số đo: tỉ lệ chuyển người, và tỉ lệ **chuyển không cần thiết**.
5. Câu mẫu khi chuyển, trong đó AI không hứa thay người.

**Thứ bạn cầm đi được sau bài:** bảng 10 lý do chuyển kèm người nhận và hạn; mẫu gói chuyển giao trong Google Sheet; 3 đến 5 câu mẫu khi chuyển; hàng khiếu nại riêng có hạn báo đã nhận; và bảng đo chuyển thừa, chuyển thiếu hằng tuần.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

Câu hỏi: *"Khi nào AI dừng, và dừng thế nào để khách không phải kể lại từ đầu?"*

Lỗi thường gặp ở các cấp trước:
- Chuyển người bằng câu "chị chờ nhân viên nhé" rồi không ai nhận.
- Nhân viên hỏi lại mã đơn mà khách đã đưa.
- AI hứa "quản lý sẽ hoàn tiền cho chị" khi chưa ai quyết.
- Hoặc ngược lại, chuyển hết mọi ca nên AI không giảm được việc.

## 3. Kiến thức nền

Phần này tóm tắt các bằng chứng, hạn luật và danh sách lý do chuyển. Bạn không cần nhớ hết số liệu, chỉ cần nắm ý chính: chuyển người là việc cần thiết, nhưng chuyển thừa cũng là một lỗi đo được.

### 3.1 Bằng chứng

- **[Nguồn]** Nubank coi chuyển giao êm là yêu cầu riêng của agent chăm sóc khách (agent là trợ lý AI tự làm việc theo mục tiêu). Họ chuyển quyền điều khiển "với đầy đủ ngữ cảnh", vì sự hài lòng phản ánh cả hành trình chứ không chỉ đoạn tự động (2606.08867, mục 1.1). Chuyển khi ngoài routine (quy trình đã định sẵn), không lấy được dữ liệu, hoặc độ tin cậy thấp (mục 4.5.2). Một phiên bản thêm khả năng phát hiện khách bực và chủ động chuyển (mục 6.3).
- **[Nguồn]** Cùng bài: tNPS và tỉ lệ tự phục vụ (SSR) thường đánh đổi nhau. (tNPS là điểm đo mức hài lòng của khách sau một lần được hỗ trợ; SSR là tỉ lệ ca khách được giải quyết xong mà không cần người.) Ví dụ: chuyển ngay ca khó hoặc khách bực cho người làm tNPS đẹp nhưng giảm SSR (mục 3.4.3).
- **[Nguồn]** Nubank (arXiv 2609.30137): họ dùng một bộ chấm nhị phân (chỉ có hai đáp án: có hoặc không) cho câu hỏi "việc chuyển người có cần không". Phiên bản tốt nhất có tỉ lệ chuyển không cần thiết 16,0% so với 22,4% của bản gốc; các bản sửa tay khác lên tới 34,0%. Bản tốt nhất sau đó tăng SSR 4,90 điểm (khoảng tin cậy 95% 4,08-5,71) và tNPS 36,69 điểm trong A/B thật, so với agent cũ. (A/B thật là cho hai nhóm khách dùng hai bản khác nhau để so sánh. Khoảng tin cậy là khoảng mà con số thật nhiều khả năng nằm trong đó.) Tức là: chuyển thừa là lỗi đo được, không phải "an toàn miễn phí".
- **[Nguồn]** Nubank (2606.08867, Bảng 3): ca quản lý nợ, cần tính toán nhiều bước và giao tiếp đồng cảm, AI vẫn thấp hơn nhân viên giỏi 23,6 điểm tNPS, khoảng cách lớn nhất trong 5 ca. **[Đề xuất]** Ca có tiền, cảm xúc, thương lượng là ca nên để người làm chính.

!!! tip "Nói đơn giản"
    Chuyển cho người là cần thiết, nhưng không phải càng nhiều càng tốt. Chuyển thừa làm AI không giảm được việc cho bạn. Chuyển thiếu làm khách bực. Vì vậy phải **đo cả hai phía**, như Bài 5.5 dạy.

### 3.2 Khiếu nại: hạn luật [Nguồn: Luật 19/2023/QH15 Điều 31 qua caselaw.vn]

Tổ chức, cá nhân kinh doanh phải tổ chức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại; thông báo cho người tiêu dùng đã nhận trong 03 ngày làm việc kể từ ngày nhận. **[Đề xuất]** Với SME: khiếu nại luôn có người phụ trách đích danh. Câu "đã nhận" có thể gửi ngay (AI soạn từ mẫu, người duyệt), nhưng giải quyết là việc của người.

!!! note "Lưu ý"
    Đây là tóm tắt để bạn tổ chức quy trình, không phải tư vấn pháp lý. Cách đếm "03 ngày làm việc" còn chưa kiểm chứng, xem mục 9.

### 3.3 Mười lý do chuyển [Đề xuất]

Mười lý do dưới đây là mã dùng để ghi vào cột "lý do" (viết liền, không dấu, để máy và Sheet đọc dễ):

`ngoai_pham_vi`, `thieu_du_lieu`, `cong_kiem_loi` (cụm cấm, kiểm số), `khach_buc`, `khieu_nai`, `an_toan`, `phap_ly`, `vuot_han_muc`, `loi_he_thong`, `khach_xin_gap_nguoi`.

Khách xin gặp người thì chuyển, không thuyết phục ở lại. Dấu hiệu khách bực **[Đề xuất]**: nhắc lại cùng một câu, chữ in hoa, "lần thứ 2/3", "gặp quản lý", từ ngữ nặng, dọa đánh giá 1 sao hoặc đăng mạng.

!!! tip "Nói đơn giản"
    Mỗi ca chuyển chỉ ghi **một** lý do chính, chọn từ danh sách 10 mã này. Danh sách cố định giúp bạn đếm được sau này: tuần này lý do nào chiếm nhiều nhất.

### 3.4 Tin chủ động qua Zalo

**[Nguồn: zalo.solutions/zns, đọc 2026-11-11]** Trang Zalo hiện gọi dịch vụ là "ZBS Template Message" (đường dẫn vẫn là ZNS). Đây là tin gửi theo mẫu, có loại giao dịch và loại khuyến mãi. Doanh nghiệp phải tạo và gửi duyệt mẫu tin. Tin gửi được tới số điện thoại đang dùng Zalo, không cần người nhận đã quan tâm OA (OA là tài khoản Zalo chính thức của doanh nghiệp). Phí tính theo tin gửi thành công, trang ghi "từ 200đ".

**[Đề xuất]** Dùng cho báo "đã nhận khiếu nại", "phiếu đổi đã duyệt", "đã hoàn tiền". AI không soạn tự do tin ZNS: chỉ điền tham số vào mẫu đã duyệt. (Tham số là chỗ trống trong mẫu, ví dụ tên khách hay mã đơn.)

## 4. Chuỗi bài nhỏ

Sáu bài thực hành dưới đây làm theo thứ tự. Mỗi bài ghi việc cần làm và thứ bạn có sau bài. Một số bài có thêm lỗi hay gặp để tránh.

### Bài 5.1: Danh sách lý do chuyển và người nhận
- **Việc cần làm:** gán mỗi lý do một người hoặc nhóm nhận và hạn nhận. Có người thay khi vắng. Ngoài giờ: soạn câu báo giờ làm việc kèm hạn sẽ trả lời.
- **Bạn có sau bài:** bảng 10 lý do × người nhận × hạn.

### Bài 5.2: Gói chuyển giao
- **Việc cần làm:** dùng khung ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.5, thêm 3 trường riêng của CSKH:
  1. **đã nói gì với khách** (chép nguyên văn);
  2. **đã hứa gì** (nếu có, đây là lỗi cần ghi lại);
  3. **hạn luật** (với khiếu nại).

  Code chặn gói thiếu tin gốc hoặc thiếu "đã nói gì".
- **Không code:** dùng mẫu ghi chú cố định trong Sheet hàng đợi; nhân viên điền đủ cột mới được đổi trạng thái.

### Bài 5.3: Câu mẫu khi chuyển
- **Việc cần làm:** soạn 3-5 câu: trong giờ, ngoài giờ, khiếu nại, ca an toàn. Không có câu nào hứa kết quả. Ví dụ: "Dạ shop đã chuyển trường hợp của anh cho quản lý. Quản lý sẽ liên hệ anh trước 17 giờ hôm nay ạ." Giờ hẹn lấy từ bảng hạn, không để AI tự đặt.

### Bài 5.4: Quy trình khiếu nại
- **Việc cần làm:** cho khiếu nại vào hàng riêng; code tính hạn báo đã nhận (3 ngày làm việc, mục 5); quá hạn thì báo chủ shop; ghi kết quả giải quyết.
- **Lỗi hay gặp:** coi khiếu nại trên Facebook công khai khác khiếu nại qua inbox.

### Bài 5.5: Đo chuyển thừa và chuyển thiếu
- **Việc cần làm:** mỗi tuần lấy ngẫu nhiên 20 ca đã chuyển và 20 ca AI tự xử lý. Người chấm hai câu hỏi: ca chuyển có cần không; ca tự xử lý có lẽ ra phải chuyển không. Ghi lý do.
- **Bạn có sau bài:** hai tỉ lệ theo tuần, kèm khoảng tin cậy (C6).
- **Lỗi hay gặp:** chỉ giảm chuyển người để "AI làm được nhiều hơn", bỏ qua tỉ lệ chuyển thiếu.

### Bài 5.6: Tin thông báo theo mẫu
- **Việc cần làm:** đăng ký 2-3 mẫu tin Zalo (đã nhận khiếu nại; phiếu đổi đã duyệt; đã hoàn tiền). Code chỉ điền tham số từ phiếu C4.

## 5. Đường không code vs có code

Cách không code đủ dùng khi mới bắt đầu: mọi thứ nằm trong Google Sheet và người làm tay. Cách code nhẹ giúp máy tự tính hạn và tự kiểm gói chuyển giao, để không ca nào bị bỏ sót.

| | Không code | Code nhẹ |
|---|---|---|
| Hàng chuyển | Sheet có cột lý do, người nhận, hạn | Bảng + hàm tạo gói, kiểm đủ trường |
| Hạn khiếu nại | Người tính tay | Hàm cộng ngày làm việc |
| Thông báo | Nhân viên nhắn tay | Mẫu tin Zalo + tham số từ phiếu |

(Hàm là một đoạn code nhỏ làm đúng một việc, ví dụ "cộng thêm 3 ngày làm việc".)

**Đoạn mã dưới đây làm gì?** Nó làm hai việc. Việc thứ nhất: tính ngày hết hạn báo "đã nhận" bằng cách cộng 3 ngày làm việc (bỏ qua thứ Bảy, Chủ nhật và các ngày nghỉ bạn tự điền). Việc thứ hai: lập gói chuyển giao cho một ca, kiểm lý do chuyển có nằm trong danh sách 10 lý do không, và chặn gói nếu thiếu tin gốc của khách hoặc thiếu "đã nói gì với khách", vì khi đó người nhận sẽ phải hỏi lại khách. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

Mã mẫu (đã chạy thử bằng `python -I -X utf8`, 2026-11-11):

```python
from datetime import date, timedelta
NGAY_NGHI = set()   # tự điền ngày lễ; để trống trong ví dụ

def cong_ngay_lam_viec(tu_ngay, so_ngay):
    d, dem = tu_ngay, 0
    while dem < so_ngay:
        d += timedelta(days=1)
        if d.weekday() < 5 and d not in NGAY_NGHI:   # giả định làm việc T2-T6
            dem += 1
    return d

LY_DO = {"ngoai_pham_vi", "thieu_du_lieu", "cong_kiem_loi", "khach_buc", "khieu_nai",
         "an_toan", "phap_ly", "vuot_han_muc", "loi_he_thong", "khach_xin_gap_nguoi"}

def goi_chuyen_giao(ca, ly_do, ngay_nhan):
    if ly_do not in LY_DO:
        raise ValueError(f"ly do chuyen khong hop le: {ly_do}")
    g = {"ma_ca": ca["ma_ca"], "ly_do": ly_do, "tin_goc": ca["tin_goc"],
         "y_dinh": ca.get("y_dinh"), "da_tra": ca.get("da_tra", {}),
         "da_noi_voi_khach": ca.get("da_noi", []), "nhap_dang_do": ca.get("nhap"),
         "de_xuat_buoc_tiep": ca.get("de_xuat")}
    if ly_do == "khieu_nai":
        g["han_bao_da_nhan"] = cong_ngay_lam_viec(ngay_nhan, 3).isoformat()
    thieu = [k for k in ("tin_goc", "da_noi_voi_khach") if not g[k]]
    if thieu:
        raise ValueError(f"goi chuyen giao thieu {thieu}: nguoi nhan se phai hoi lai khach")
    return g
```

**Kết quả chạy thử:** khiếu nại nhận thứ Năm 13/11/2026 → hạn báo đã nhận 18/11/2026 (thứ Ba) theo cách đếm "ngày nhận không tính, thứ Bảy và Chủ nhật không tính". Gói thiếu "đã nói gì với khách" → bị chặn. Cách đếm ngày là giả định; xem mục 9.

!!! tip "Nói đơn giản"
    Đoạn mã chỉ làm hai việc mà bạn cũng làm được bằng tay: đếm đúng ngày hạn, và không cho phép chuyển ca khi hồ sơ còn thiếu. Code chỉ giúp không ai quên.

**Buộc chuyển sang code khi [Đề xuất]:** có ca chuyển bị quên quá hạn; có nhiều người nhận theo ca làm; cần đo chuyển thừa/thiếu hằng tuần.

## 6. Tiêu chí lên cấp (C5 → C6) [Đề xuất]

Bạn có thể sang cấp C6 khi đạt đủ các điều sau:
1. 100% ca chuyển có đúng một lý do chính và gói đủ trường (rà 20 ca ngẫu nhiên).
2. Trong 20 ca chuyển rà ngẫu nhiên, ≤2 ca người nhận phải hỏi lại khách điều khách đã nói.
3. 100% khiếu nại được báo đã nhận trong hạn luật trong 4 tuần.
4. Có số tuần của tỉ lệ chuyển thừa và chuyển thiếu, đo ≥4 tuần.
5. 0 câu hứa kết quả trong tin chuyển giao (kiểm bằng cụm cấm C1, tức danh sách cụm từ không được phép xuất hiện, đã làm ở cấp C1).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung cách áp dụng.

### 7.a Shop thời trang, khách nhận sai màu lần hai
Khách nhắn: "Áo giao sai màu lần 2 rồi, tôi muốn gặp quản lý." Luật: `khach_xin_gap_nguoi` + `khieu_nai`. AI gửi câu mẫu khiếu nại. Gói chuyển có trạng thái đơn, lịch sử lần sai trước, câu đã gửi. Đề xuất bước tiếp do AI ghi chỉ là gợi ý; quản lý quyết đổi và miễn phí ship.

### 7.b Phòng khám thú y, chủ nuôi báo thú cưng nôn sau khi dùng thuốc
Luật cứng `an_toan` → chuyển người ngay, gọi điện. AI không soạn lời khuyên y tế. Tin chủ động sau đó (lịch tái khám) dùng mẫu tin Zalo đã duyệt.

### 7.c Công ty du lịch nhỏ, khách đòi hoàn tiền tour bị hủy do thời tiết
`vuot_han_muc` (số tiền lớn) + có thể là `khieu_nai`. Gói chuyển gồm mã booking, điều khoản hủy đã trích, số tiền đã thanh toán (từ công cụ đọc). Người quyết; AI soạn câu báo đã nhận.

## 8. Tài liệu tham khảo

| Nguồn | Loại | Đọc | Tin cậy |
|---|---|---|---|
| Nubank, arXiv 2606.08867 | Bài báo, triển khai thật | Phần lớn toàn văn | Cao |
| Nubank, arXiv 2609.30137 | Bài báo, triển khai thật | Phần lớn toàn văn | Cao (một tổ chức; bộ chấm "chuyển không cần thiết" chưa báo hiệu chuẩn riêng) |
| Luật 19/2023/QH15 Điều 31, caselaw.vn | Văn bản luật | Qua công cụ tóm tắt | Trung bình |
| Zalo, trang ZBS Template Message, https://zalo.solutions/zns | Trang sản phẩm | Đọc 2026-11-11 qua công cụ tóm tắt | Trung bình-Cao (trang chính thức, nhưng không có tiêu chí duyệt) |

## 9. Chưa kiểm chứng

- Cách đếm "03 ngày làm việc kể từ ngày nhận" (có tính ngày nhận không, thứ Bảy có là ngày làm việc của doanh nghiệp không): chưa đọc hướng dẫn; NĐ 55/2024 chưa đọc.
- Tiêu chí duyệt mẫu tin Zalo, giá cụ thể, phân loại tag: chỉ có blog bên thứ ba, mô tả không thống nhất. Trang chính thức không nêu tiêu chí.
- Quy tắc cửa sổ trả lời của Messenger cho doanh nghiệp: chưa tra.
- Dấu hiệu khách bực và 10 lý do chuyển: đề xuất, chưa có nguồn đo trên tiếng Việt.
- Ngưỡng ≤2/20 hỏi lại, 4 tuần: đề xuất.
