# Cấp 5 (C5): Gom bài học sau sự cố và bàn giao khi nghỉ việc

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác. Không phải tư vấn pháp lý.
> Dùng lại: phỏng vấn rút tri thức (C2 của nhóm này); sổ đăng ký và chủ sở hữu (C3); quy trình sự cố dữ liệu (`../an-toan-du-lieu-va-phap-ly-vn.md` Bài A6).

## 1. Mục tiêu và người đọc

**Người đọc:** quản lý vận hành, trưởng dự án, nhân sự.

**Sau cấp này:**
1. Mỗi sự cố đáng kể và mỗi dự án kết thúc để lại **một bài học** theo mẫu, có hành động sửa tài liệu cụ thể.
2. Bài học đi qua **lọc bằng code** (dữ liệu nhạy cảm, trùng) và **người duyệt** trước khi vào kho.
3. Khi nhân viên nghỉ: có **gói bàn giao** lấy từ sổ đăng ký, sổ việc, danh sách tài khoản; có buổi phỏng vấn bàn giao.
4. Dữ liệu cá nhân của người nghỉ được xử lý theo quy định (xóa phần phải xóa).

**Sản phẩm:** mẫu bài học; kho bài học (Sheet/Notion/Lark); script `bai_hoc.py`; danh sách kiểm bàn giao; quy trình bàn giao 1 trang.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Lỗi này năm ngoái đã xảy ra rồi, sao lại xảy ra? Chị Hoa nghỉ, ai biết mật khẩu web và cách làm hồ sơ thầu?"*

C0-C4 tạo và giữ tài liệu cho việc **đang** làm. Còn hai dòng tri thức hay mất: **kinh nghiệm từ sai lầm** (nằm trong tin nhắn khi xử lý sự cố) và **mọi thứ một người biết** khi họ rời đi.

## 3. Kiến thức nền

### 3.1 Bộ nhớ từ đóng góp: gom được, chưa chứng minh có ích [Nguồn]

**SAP** (arXiv 2608.00122, qua `../nen-tang-bang-chung.md`): khi một người làm thay đổi tệp tri thức, hệ thống **hỏi xin phép** người đó; một chuỗi xử lý soạn cặp hỏi-đáp, gắn nhãn, **quét bảo mật**, **kiểm trùng**. 900 đóng góp tạo 1.144 mục; chỉ 53,7% đóng góp tạo ra ít nhất một mục. Tác giả thừa nhận **chưa đo** hiệu quả với chất lượng công việc, điểm tin cậy chưa hiệu chuẩn, và có nguy cơ **nhiễm độc bộ nhớ dùng chung**.

**[Đề xuất] Ý nghĩa:** gom bài học là việc làm được, nhưng hãy đo nó có được dùng không (C7), và chặn rác trước khi vào kho.

### 3.2 AI giúp tóm tắt sự cố [Nguồn]

Slide thí nghiệm của Microsoft (Edelman, 5/2024): 149 người mới về bảo mật (Upwork) làm tóm tắt sự cố, báo cáo sự cố, phân tích script. Nhóm có Copilot đạt điểm nội dung tóm tắt sự cố cao hơn 151%, chất lượng tóm tắt cao hơn 32%; giữ nguyên chất lượng thì nhanh hơn 26%. Người dùng nói tiết kiệm 38 phút; thí nghiệm đo được 5 phút. Đây là slide nhà cung cấp, công cụ chuyên dụng, không phải SME.

### 3.3 Pháp lý khi nhân viên nghỉ [Nguồn, xác minh một phần]

Điều 25 Luật 91/2025/QH15 (qua hethongphapluat.com, chưa đối chiếu Công báo):
- Khoản 2: dữ liệu cá nhân người lao động phải lưu trong thời hạn theo luật hoặc thỏa thuận; **khi chấm dứt hợp đồng phải xóa, hủy**, trừ khi có thỏa thuận hoặc luật quy định khác.
- Khoản 1: ứng viên không được tuyển thì phải xóa, hủy thông tin đã cung cấp, trừ khi có thỏa thuận khác.

**[Đề xuất]** Tách hai thứ: (a) **tri thức công việc** (SOP, ghi chú quy trình, bài học đã bỏ tên người) là tài sản công ty, giữ lại; (b) **dữ liệu cá nhân** của người nghỉ (bản ghi giọng nói phỏng vấn, đánh giá cá nhân, thông tin liên lạc riêng) xử lý theo Điều 25. Thời hạn lưu hồ sơ lao động, BHXH, thuế theo luật khác: hỏi kế toán/luật sư.

### 3.4 Rủi ro riêng của bàn giao [Đề xuất, dựa `../an-toan-du-lieu-va-phap-ly-vn.md` mục 3.3]

- Project/Gem/GPT, lịch sử chat, tệp tải lên nằm trong **tài khoản AI cá nhân** của người nghỉ.
- Người nghỉ là quản trị viên duy nhất của nhóm Zalo khách hàng, trang Facebook, tài khoản sàn.
- Mật khẩu ghi trong ghi chú, tin nhắn; vô tình chép vào bài học.

## 4. Chuỗi bài nhỏ

### Bài C5.1: Mẫu bài học 1 trang
- **Thực hành [Đề xuất]:** 6 mục: (1) Chuyện gì xảy ra (thời gian, ảnh hưởng: tiền, khách, giờ công); (2) Phát hiện thế nào; (3) Vì sao (nguyên nhân quy trình, **không** đổ lỗi cá nhân); (4) Đã xử lý gì; (5) **Thay đổi tài liệu**: mã tài liệu trong sổ C3 + bước cần thêm/sửa; (6) Nguồn (link biên bản, ngày tin nhắn).
- **Sản phẩm:** mẫu.
- **Lỗi thường gặp:** bài học chỉ là "cần cẩn thận hơn"; không gắn với tài liệu nào.

### Bài C5.2: AI nháp bài học từ tin nhắn và biên bản
- **Thực hành:** dán chuỗi tin nhắn xử lý sự cố (đã che tên khách, số điện thoại) và biên bản họp rút kinh nghiệm (C0) vào Project "Bài học". Chỉ dẫn: điền mẫu 6 mục; mục 3 và 5 phải trích nguyên văn câu trong nguồn; không có thì để `??`.
- **Sản phẩm:** bản nháp.
- **Lỗi thường gặp:** AI tự viết nguyên nhân "hợp lý" mà không ai nói.

### Bài C5.3: Lọc bằng code
- **Thực hành:** chạy `bai_hoc.py` (mục 5): chặn bài có số điện thoại, email, số CCCD, chuỗi giống mật khẩu; đánh dấu bài gần giống bài cũ để người duyệt gộp. Bổ sung mẫu nhạy cảm riêng của công ty (mã số thuế khách, số tài khoản).
- **Sản phẩm:** danh sách chặn / nghi trùng / chờ duyệt.
- **Lỗi thường gặp:** chỉ dựa vào AI "nhớ che thông tin" (hàng rào bằng prompt).

### Bài C5.4: Duyệt và biến thành thay đổi tài liệu
- **Thực hành:** chủ tài liệu (theo sổ C3) duyệt bài học. Mục 5 tạo một việc trong sổ việc (C0): "sửa SOP-X bước B4, hạn ...". Bài học chỉ "đóng" khi tài liệu đã sửa. Gắn bài học vào tài liệu liên quan để người đọc tài liệu thấy.
- **Sản phẩm:** kho bài học có trạng thái (nháp / đã duyệt / đã áp dụng vào tài liệu).

### Bài C5.5: Ôn cuối dự án
- **Thực hành:** họp 30 phút cuối mỗi dự án/mùa vụ: 3 câu (giữ gì, bỏ gì, đổi gì). Làm biên bản theo C0, rồi tách thành bài học theo C5.1.

### Bài C5.6: Danh sách kiểm bàn giao
- **Thực hành [Đề xuất]:** khi có đơn nghỉ việc, chạy:
  1. Lọc sổ đăng ký (C3): mọi tài liệu có `chu_so_huu` = người nghỉ → chọn chủ mới.
  2. Lọc sổ việc (C0): việc đang mở của người nghỉ → giao lại.
  3. Danh sách tài khoản: email, Drive, Zalo OA/nhóm (quyền quản trị), sàn TMĐT, tài khoản AI (Project/Gem/GPT có dùng cho công việc không) → chuyển quyền hoặc xuất nội dung.
  4. Tài liệu chỉ nằm trên máy/tài khoản cá nhân (bản đồ C3.1) → chuyển vào kho công ty.
- **Sản phẩm:** biểu mẫu bàn giao có chữ ký hai bên.

### Bài C5.7: Phỏng vấn bàn giao
- **Thực hành:** dùng bộ câu hỏi C2 cho 2-3 việc chỉ người nghỉ biết; thêm: "ai là đầu mối bên khách/nhà cung cấp?", "việc gì hay bị quên vào cuối tháng/quý?". Thông báo mục đích; chỉ giữ SOP và trích đoạn, xóa âm thanh theo quy tắc C1.
- **Sản phẩm:** SOP nháp, đi tiếp theo C2.4-C2.7 với người kế nhiệm làm thử.

### Bài C5.8: Xử lý dữ liệu cá nhân của người nghỉ
- **Thực hành:** theo 3.3: liệt kê dữ liệu cá nhân của người nghỉ mà quy trình AI đã tạo ra (bản ghi phỏng vấn, mẫu giọng nếu có, ghi chú đánh giá); xóa phần không có căn cứ giữ; ghi ngày xóa.
- **Sản phẩm:** dòng nhật ký xóa.

## 5. Đường không code vs có code

| | Không code | Có code nhẹ |
|---|---|---|
| Nháp bài học | Project "Bài học" | API + mẫu JSON |
| Lọc | Người duyệt đọc kỹ | `bai_hoc.py` chặn trước |
| Bàn giao | Lọc Sheet bằng tay | Script lọc sổ C3 và sổ việc theo tên người nghỉ |

**Mã mẫu (đã chạy thử, `python -I -X utf8`):**

```python
import re, unicodedata
MAU_NHAY_CAM = {
    "SDT": re.compile(r"\b0\d{9}\b"),
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "CCCD": re.compile(r"\b\d{12}\b"),
    "MAT_KHAU": re.compile(r"(mật khẩu|password|pass)\s*[:=]\s*\S+", re.I),
}

def tu(s):
    return set(re.findall(r"\w+", unicodedata.normalize("NFC", s.lower())))

def jaccard(a, b):
    a, b = tu(a), tu(b)
    return len(a & b) / max(len(a | b), 1)

def loc(moi, kho, nguong_trung=0.6):
    ket_qua = []
    for bh in moi:
        nhan = [k for k, p in MAU_NHAY_CAM.items() if p.search(bh["noi_dung"])]
        if nhan:
            ket_qua.append((bh["ma"], "CHAN_NHAY_CAM", nhan)); continue
        diem, ma = max(((jaccard(bh["noi_dung"], k["noi_dung"]), k["ma"]) for k in kho), default=(0, None))
        ket_qua.append((bh["ma"], "NGHI_TRUNG", ma, round(diem, 2)) if diem >= nguong_trung
                       else (bh["ma"], "CHO_NGUOI_DUYET"))
    return ket_qua
```

Chạy thử với 3 bài giả và kho 1 bài: bài về "độ ẩm gỗ trên 12% phải sấy lại" bị đánh dấu `NGHI_TRUNG` với bài cũ; bài có "0912345678" và "mật khẩu: abc123" bị `CHAN_NHAY_CAM` (SDT, MAT_KHAU); bài về chụp ảnh kiện hàng xuất khẩu đi tiếp tới người duyệt.

**Giới hạn:** biểu thức chính quy bỏ sót tên người, địa chỉ, số viết có dấu cách ("0912 345 678"). Code là lớp chặn đầu, người duyệt vẫn phải đọc. Ngưỡng trùng 0,6 là đề xuất; so trùng theo từ không bắt được hai bài cùng ý khác chữ.

**Khi nào buộc chuyển sang code [Đề xuất]:** > 10 bài học/tháng; có > 1 người nghỉ mỗi quý; muốn bài học tự hiện ra khi ai đó mở tài liệu liên quan.

## 6. Tiêu chí lên cấp [Đề xuất]

1. 3 tháng liên tục: mọi sự cố được phân loại "đáng kể" có bài học; ≥ 80% bài học đã áp dụng vào tài liệu.
2. Không bài học nào trong kho chứa dữ liệu bị chặn (kiểm ngẫu nhiên 20 bài).
3. Lần nghỉ việc gần nhất: 100% tài liệu và việc của người nghỉ có chủ mới trước ngày nghỉ; người kế nhiệm làm được việc chính theo SOP.
4. Có nhật ký xử lý dữ liệu cá nhân của người nghỉ.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

- **Xưởng cơ khí gia công 35 người (Bắc Ninh):** sự cố "lô 500 chi tiết sai dung sai vì dùng bản vẽ cũ". Bài học: mục 5 gắn với SOP nhận bản vẽ (thêm bước "kiểm số phiên bản bản vẽ với kỹ thuật"); liên quan C4 (bản vẽ cũ vẫn "hiệu lực"). Nguồn: biên bản họp chất lượng.
- **Đại lý du lịch 10 người (Đà Nẵng):** nhân viên điều hành tour nghỉ; chỉ chị ấy biết đầu mối nhà xe, khách sạn ở Hội An, cách xử lý khi khách đổi ngày. Gói bàn giao: lọc sổ C3, chuyển quyền nhóm Zalo nhà cung cấp, phỏng vấn bàn giao 2 buổi; người mới chạy thử 2 tour có người cũ dự phòng qua điện thoại trong tháng đầu (nếu thỏa thuận được).
- **Shop thời trang online 8 người:** sự cố "đăng nhầm giá flash sale". Bài học dẫn tới thẻ quy tắc mới ở C3: "giá flash sale phải có người thứ hai kiểm trước khi bật". Tin nhắn nguồn có số điện thoại khách khiếu nại: bị code chặn, phải che trước khi nhập.

## 8. Tài liệu tham khảo

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| Shared Organizational Memory for Enterprise Coding Agents (SAP) | https://arxiv.org/abs/2608.00122 | Qua `../nen-tang-bang-chung.md` | Cao về mô tả; lợi ích chưa đo |
| Selected Copilot Experiments (Edelman, Microsoft) | https://www.microsoft.com/en-us/research/wp-content/uploads/2024/05/Edelman_Copilot-Experiments-Merged-2024-05-AICE-Shareable.pdf | 12 trang slide đầu | Trung bình (nhà cung cấp) |
| Điều 25 Luật BVDLCN 2025 (hethongphapluat.com) | https://hethongphapluat.com/luat-bao-ve-du-lieu-ca-nhan-2025/dieu-25 | Đọc qua công cụ tóm tắt | Trung bình (chưa đối chiếu Công báo) |
| lsvn.vn: Doanh nghiệp phải xóa dữ liệu cá nhân của NLĐ khi nghỉ việc | https://lsvn.vn/tu-nam-2026-doanh-nghiep-phai-xoa-du-lieu-ca-nhan-cua-nguoi-lao-dong-khi-nghi-viec-a167358.html | Đọc qua công cụ tóm tắt | Trung bình |

## 9. Chưa kiểm chứng

- Chưa có nguồn đo hiệu quả của kho bài học (bài học có được đọc và tránh lặp lỗi không). SAP cũng chưa đo.
- Bài "Expert Mind: Retrieval-Augmented Architecture for Expert Knowledge Preservation in the Energy Sector" (arXiv 2603.14541) có vẻ liên quan đến bàn giao chuyên gia nghỉ hưu; **chưa đọc**.
- Thời hạn lưu hồ sơ người lao động theo luật lao động, BHXH, thuế; phạm vi "thỏa thuận khác" ở Điều 25: cần luật sư.
- Cách chuyển quyền quản trị nhóm Zalo, Zalo OA; cách xuất Project/Gem khỏi tài khoản cá nhân: chưa kiểm trong phiên này.
- Mẫu 6 mục, ngưỡng 80%, 20 bài, 0,6 là đề xuất.
