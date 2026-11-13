# Cấp 5 (C5): Chuyển giao cho người, khiếu nại và khách bực

> Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** / **[Đề xuất]**.
> Dùng lại: gói chuyển giao tối thiểu và điểm duyệt ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4-3.5. File này viết phần riêng: **khi nào chuyển**, **chuyển quá nhiều cũng là lỗi**, **khiếu nại có hạn luật**, **tin chủ động qua Zalo**.

## 1. Mục tiêu và người đọc

**Người đọc:** trưởng nhóm CSKH, chủ shop, người kỹ thuật nhẹ. Đã xong C2 (C3-C4 giúp ích nhưng không bắt buộc).

**Sau cấp này có:**
1. Danh sách lý do chuyển cố định (10 lý do), mỗi ca chuyển ghi đúng một lý do chính.
2. Gói chuyển giao đủ để người nhận **không phải hỏi lại khách**.
3. Quy trình khiếu nại có hạn "báo đã nhận" tính bằng code.
4. Hai số đo: tỉ lệ chuyển người, tỉ lệ **chuyển không cần thiết**.
5. Câu mẫu khi chuyển, không hứa thay người.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

Câu hỏi: *"Khi nào AI dừng, và dừng thế nào để khách không phải kể lại từ đầu?"*

Lỗi thường gặp ở các cấp trước: chuyển người bằng câu "chị chờ nhân viên nhé" rồi không ai nhận; nhân viên hỏi lại mã đơn khách đã đưa; AI hứa "quản lý sẽ hoàn tiền cho chị" khi chưa ai quyết; hoặc ngược lại, chuyển hết mọi ca nên AI không giảm được việc.

## 3. Kiến thức nền

### 3.1 Bằng chứng

- **[Nguồn]** Nubank coi chuyển giao êm là yêu cầu riêng của agent chăm sóc khách: chuyển quyền điều khiển "với đầy đủ ngữ cảnh", vì sự hài lòng phản ánh cả hành trình chứ không chỉ đoạn tự động (2606.08867, mục 1.1). Chuyển khi ngoài routine, không lấy được dữ liệu, hoặc tin cậy thấp (mục 4.5.2). Một phiên bản thêm phát hiện khách bực và chủ động chuyển (mục 6.3).
- **[Nguồn]** Cùng bài: tNPS và tỉ lệ tự phục vụ (SSR) thường đánh đổi nhau; ví dụ chuyển ngay ca khó hoặc khách bực cho người làm tNPS đẹp nhưng giảm SSR (mục 3.4.3).
- **[Nguồn]** Nubank (arXiv 2609.30137): họ dùng một bộ chấm nhị phân "việc chuyển người có cần không". Phiên bản tốt nhất có tỉ lệ chuyển không cần thiết 16,0% so với 22,4% của bản gốc; các bản sửa tay khác lên tới 34,0%. Bản tốt nhất sau đó tăng SSR 4,90 điểm (khoảng tin cậy 95% 4,08-5,71) và tNPS 36,69 điểm trong A/B thật, so với agent cũ. Tức là: chuyển thừa là lỗi đo được, không phải "an toàn miễn phí".
- **[Nguồn]** Nubank (2606.08867, Bảng 3): ca quản lý nợ, cần tính toán nhiều bước và giao tiếp đồng cảm, AI vẫn thấp hơn nhân viên giỏi 23,6 điểm tNPS, khoảng cách lớn nhất trong 5 ca. **[Đề xuất]** Ca có tiền, cảm xúc, thương lượng là ca nên để người làm chính.

### 3.2 Khiếu nại: hạn luật [Nguồn: Luật 19/2023/QH15 Điều 31 qua caselaw.vn]

Tổ chức, cá nhân kinh doanh phải tổ chức tiếp nhận và giải quyết phản ánh, yêu cầu, khiếu nại; thông báo cho người tiêu dùng đã nhận trong 03 ngày làm việc kể từ ngày nhận. **[Đề xuất]** Với SME: khiếu nại luôn có người phụ trách đích danh; câu "đã nhận" có thể gửi ngay (AI soạn từ mẫu, người duyệt), nhưng giải quyết là việc của người.

### 3.3 Mười lý do chuyển [Đề xuất]

`ngoai_pham_vi`, `thieu_du_lieu`, `cong_kiem_loi` (cụm cấm, kiểm số), `khach_buc`, `khieu_nai`, `an_toan`, `phap_ly`, `vuot_han_muc`, `loi_he_thong`, `khach_xin_gap_nguoi`.

Khách xin gặp người thì chuyển, không thuyết phục ở lại. Dấu hiệu khách bực **[Đề xuất]**: nhắc lại cùng một câu, chữ in hoa, "lần thứ 2/3", "gặp quản lý", từ ngữ nặng, dọa đánh giá 1 sao hoặc đăng mạng.

### 3.4 Tin chủ động qua Zalo

**[Nguồn: zalo.solutions/zns, đọc 2026-11-11]** Trang Zalo hiện gọi dịch vụ là "ZBS Template Message" (đường dẫn vẫn là ZNS): tin theo mẫu, có loại giao dịch và loại khuyến mãi; doanh nghiệp phải tạo và gửi duyệt mẫu tin; gửi được tới số điện thoại đang dùng Zalo, không cần người nhận đã quan tâm OA; tính phí theo tin gửi thành công, trang ghi "từ 200đ". **[Đề xuất]** Dùng cho báo "đã nhận khiếu nại", "phiếu đổi đã duyệt", "đã hoàn tiền". AI không soạn tự do tin ZNS: chỉ điền tham số vào mẫu đã duyệt.

## 4. Chuỗi bài nhỏ

### Bài 5.1: Danh sách lý do chuyển và người nhận
- **Làm:** gán mỗi lý do một người/nhóm nhận và hạn nhận. Có người thay khi vắng. Ngoài giờ: câu báo giờ làm việc + hạn sẽ trả lời.
- **Sản phẩm:** bảng 10 lý do × người nhận × hạn.

### Bài 5.2: Gói chuyển giao
- **Làm:** dùng khung ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.5, thêm 3 trường riêng của CSKH: **đã nói gì với khách** (nguyên văn), **đã hứa gì** (nếu có, là lỗi cần ghi), **hạn luật** (khiếu nại). Code chặn gói thiếu tin gốc hoặc thiếu "đã nói gì".
- **Không code:** mẫu ghi chú cố định trong Sheet hàng đợi; nhân viên điền đủ cột mới được đổi trạng thái.

### Bài 5.3: Câu mẫu khi chuyển
- **Làm:** 3-5 câu: trong giờ, ngoài giờ, khiếu nại, ca an toàn. Không có câu nào hứa kết quả. Ví dụ: "Dạ shop đã chuyển trường hợp của anh cho quản lý. Quản lý sẽ liên hệ anh trước 17 giờ hôm nay ạ." Giờ hẹn lấy từ bảng hạn, không để AI tự đặt.

### Bài 5.4: Quy trình khiếu nại
- **Làm:** khiếu nại vào hàng riêng; code tính hạn báo đã nhận (3 ngày làm việc, mục 5); quá hạn thì báo chủ shop; ghi kết quả giải quyết.
- **Lỗi:** coi khiếu nại trên Facebook công khai khác khiếu nại qua inbox.

### Bài 5.5: Đo chuyển thừa và chuyển thiếu
- **Làm:** mỗi tuần lấy ngẫu nhiên 20 ca đã chuyển và 20 ca AI tự xử lý. Người chấm: ca chuyển có cần không; ca tự xử lý có lẽ ra phải chuyển không. Ghi lý do.
- **Sản phẩm:** hai tỉ lệ tuần, kèm khoảng tin cậy (C6).
- **Lỗi:** chỉ giảm chuyển người để "AI làm được nhiều hơn", bỏ qua tỉ lệ chuyển thiếu.

### Bài 5.6: Tin thông báo theo mẫu
- **Làm:** đăng ký 2-3 mẫu tin Zalo (đã nhận khiếu nại; phiếu đổi đã duyệt; đã hoàn tiền). Code chỉ điền tham số từ phiếu C4.

## 5. Đường không code vs có code

| | Không code | Code nhẹ |
|---|---|---|
| Hàng chuyển | Sheet có cột lý do, người nhận, hạn | Bảng + hàm tạo gói, kiểm đủ trường |
| Hạn khiếu nại | Người tính tay | Hàm cộng ngày làm việc |
| Thông báo | Nhân viên nhắn tay | Mẫu tin Zalo + tham số từ phiếu |

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

Chạy thử: khiếu nại nhận thứ Năm 13/11/2026 → hạn báo đã nhận 18/11/2026 (thứ Ba) theo cách đếm "ngày nhận không tính, thứ Bảy và Chủ nhật không tính". Gói thiếu "đã nói gì với khách" → bị chặn. Cách đếm ngày là giả định; xem mục 9.

**Buộc chuyển sang code khi [Đề xuất]:** có ca chuyển bị quên quá hạn; có nhiều người nhận theo ca làm; cần đo chuyển thừa/thiếu hằng tuần.

## 6. Tiêu chí lên cấp (C5 → C6) [Đề xuất]

1. 100% ca chuyển có đúng một lý do chính và gói đủ trường (rà 20 ca ngẫu nhiên).
2. Trong 20 ca chuyển rà ngẫu nhiên, ≤2 ca người nhận phải hỏi lại khách điều khách đã nói.
3. 100% khiếu nại được báo đã nhận trong hạn luật trong 4 tuần.
4. Có số tuần của tỉ lệ chuyển thừa và chuyển thiếu, đo ≥4 tuần.
5. 0 câu hứa kết quả trong tin chuyển giao (kiểm bằng cụm cấm C1).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

### 7.a Shop thời trang, khách nhận sai màu lần hai
"Áo giao sai màu lần 2 rồi, tôi muốn gặp quản lý." Luật: `khach_xin_gap_nguoi` + `khieu_nai`. AI gửi câu mẫu khiếu nại; gói chuyển có trạng thái đơn, lịch sử lần sai trước, câu đã gửi. Đề xuất bước tiếp do AI ghi chỉ là gợi ý; quản lý quyết đổi và miễn phí ship.

### 7.b Phòng khám thú y, chủ nuôi báo thú cưng nôn sau khi dùng thuốc
Luật cứng `an_toan` → người ngay, gọi điện. AI không soạn lời khuyên y tế. Tin chủ động sau đó (lịch tái khám) dùng mẫu tin Zalo đã duyệt.

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
