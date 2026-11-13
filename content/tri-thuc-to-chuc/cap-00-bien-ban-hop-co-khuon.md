# Cấp 0 (C0): Biên bản họp theo khuôn, có trích nguyên văn

> Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.
> Phần dùng chung đã có ở nhóm RAG, không viết lại: bản giao việc 6 phần, Sổ prompt (`../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`); quy trình biên bản nhiều bước có cổng kiểm (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 7.b).

## 1. Mục tiêu và người đọc

**Người đọc:** chủ doanh nghiệp, trưởng nhóm, người hay phải "ghi lại cuộc họp". Không cần code.

**Sau cấp này:**
1. Mọi cuộc họp định kỳ có biên bản theo **một mẫu cố định**.
2. Mỗi việc cần làm có: ai, việc gì, hạn, **trạng thái** (đã chốt / mới đề xuất), và **câu trích nguyên văn** chứng minh.
3. Người chủ trì duyệt biên bản trong 24 giờ trước khi gửi.
4. Có số đo đơn giản: bao nhiêu việc bị sửa, bịa, sót.

**Sản phẩm cầm đi được:** mẫu biên bản 1 trang; một Project (Claude) hoặc Gem (Gemini) "Thư ký họp"; bảng kiểm 8 lỗi; sổ việc trên Google Sheet/Excel.

## 2. Câu hỏi cấp này trả lời

*"Làm sao để mỗi cuộc họp để lại một danh sách việc đáng tin, không mất thêm nhiều thời gian?"*

Đây là điểm xuất phát của nhóm. Lỗi thường thấy khi dùng AI "vô tội vạ" **[Đề xuất, quan sát]**: dán ghi chú vào chat, nhận về đoạn tóm tắt trôi chảy. Không ai kiểm. Ý kiến "hay là mình thử..." thành "Quyết định: ...". Việc không có người nhận vẫn được gán cho ai đó.

## 3. Kiến thức nền

### 3.1 AI sai ở đâu khi đọc cuộc họp [Nguồn]

Microsoft (arXiv 2608.20392) dò lỗi của trợ lý hỏi-đáp về cuộc họp trên 20 bản ghi tiếng Anh (AMI, ICSI, nghị viện), 3 mô hình. 1.049 lỗi được xếp thành 8 nhóm:

| Nhóm lỗi | Tỷ lệ | Ví dụ |
|---|---|---|
| Diễn giải quá tự tin từ câu mơ hồ | 27,3% | "cái này", "hơi quá" thành một khẳng định cụ thể |
| Bịa con số, danh sách "đủ" | 16,9% | "cả ba ràng buộc" khi chỉ nói hai |
| Gán sai người nói | 16,0% | Ý kiến của A ghi là của B |
| Biến thảo luận thành quyết định | 13,4% | Đang bàn, chưa chốt, ghi "đã thống nhất" |
| Bịa việc cần làm (người, hạn) | 10,4% | Suy ra người phụ trách, hạn từ thảo luận chung |
| Sai thứ tự thời gian | 8,6% | "Ai nói trước" bị đảo |
| Hiểu sai lý do | 4,0% | Gán lý do chi phí cho người nói vì thẩm mỹ |
| Liệt kê người tham gia không có căn cứ | 3,3% | "A, B, C cùng đồng ý" |

Mô hình mạnh nhất (GPT-5.2-chat) vẫn sai; lỗi đặc trưng của nó là **bịa việc cần làm** (15,8% số lỗi của nó). Đây là tỷ lệ lỗi khi **cố tình dò** (5,2% đến 15,3% câu hỏi dò ra lỗi, tùy mô hình), không phải tỷ lệ lỗi trung bình của một biên bản.

### 3.2 Tách bước tốt hơn một prompt [Nguồn]

FRAME (arXiv 2509.15901, 50 mẫu QMSum và 50 mẫu tổng hợp, GPT-4o): trích các sự kiện riêng lẻ, chọn cái quan trọng, lập dàn ý, rồi mới viết. Điểm bịa nội dung (thang 1-5, thấp là tốt) giảm từ 3 xuống 1 trên QMSum. Khi gộp mọi bước vào **một prompt**, điểm bỏ sót lên 4 (tệ hơn bản tách bước 3 điểm). Chấm bằng bộ chấm LLM (MESA), không phải người.

### 3.3 Danh sách người dự họp giúp gán đúng người [Nguồn]

Otter.ai (arXiv 2610.29319, dữ liệu họp tổng hợp tiếng Anh): độ đúng khi gán người phụ trách việc tăng từ 0,524 lên 0,752 khi thêm văn bản nền (danh sách thành viên, email, slide); lên 0,792 khi thêm cả mẫu giọng. Không có danh sách tên, hệ thống tự "bịa" một cái tên nghe giống (ví dụ "Bevan" thay vì "Devon Ashby"). Tác giả nói rõ không khẳng định con số này chuyển được sang ghi âm thật.

### 3.4 Đừng tin cảm giác "tiết kiệm thời gian" [Nguồn]

Slide thí nghiệm có đối chứng của Microsoft (Edelman, 5/2024; 147 người làm tự do trên Upwork, 4 tác vụ): tóm tắt cuộc họp Teams với Copilot nhanh hơn 19%, độ chính xác không thay đổi có ý nghĩa thống kê. Trên cả 4 tác vụ, người dùng nói Copilot tiết kiệm 36 phút; thí nghiệm đo được 12 phút. Đây là tài liệu nội bộ dạng slide của nhà cung cấp, không qua bình duyệt.

### 3.5 Ba quy tắc rút ra [Đề xuất]

1. **Không trích được nguyên văn thì không phải việc đã chốt.**
2. **Không ai nhận thì để trống**, không đoán.
3. **Phân biệt "đã chốt" và "đề xuất"** ngay trong mẫu.

## 4. Chuỗi bài nhỏ

### Bài C0.1: Mẫu biên bản 1 trang
- **Thực hành:** dùng 5 phần cố định: (1) Thông tin họp (ngày, người chủ trì, người dự); (2) Quyết định đã chốt; (3) Việc cần làm: bảng `việc | người phụ trách | hạn | trạng thái | trích nguyên văn`; (4) Vấn đề còn treo; (5) Thông tin cần kiểm (con số, tên khách AI không chắc).
- **Sản phẩm:** mẫu trên Google Docs/Word, ghim trong nhóm Zalo của phòng.
- **Lỗi thường gặp:** mẫu có 15 mục, không ai điền; thiếu cột "trạng thái".

### Bài C0.2: Chuẩn bị đầu vào
- **Thực hành:** trước họp, ghi sẵn danh sách người dự (tên gọi trong họp: "chị Lan", "anh Tuấn kho") và chương trình 3-5 mục. Đầu vào cho AI là: ghi chú tay gõ lại, hoặc bản chép lời có sẵn (C1 nói cách làm ra bản chép lời).
- **Sản phẩm:** khối "Bối cảnh họp" dán đầu mỗi lần chạy.
- **Lỗi thường gặp:** chỉ dán bản ghi, không có danh sách tên (xem 3.3).

### Bài C0.3: Project/Gem "Thư ký họp" chạy 3 lượt
- **Thực hành [Đề xuất, dựa trên 3.2]:** trong cùng một cuộc chat, làm ba lượt thay vì một lệnh "tóm tắt cuộc họp":
  1. *Lượt 1:* "Liệt kê mọi câu có nội dung giao việc, chốt, hoặc con số. Mỗi dòng chép **nguyên văn** câu đó và tên người nói. Không diễn giải."
  2. *Lượt 2:* "Với từng dòng, gán nhãn: QUYẾT_ĐỊNH_ĐÃ_CHỐT / ĐỀ_XUẤT / VIỆC / THÔNG_TIN. Chỉ gán ĐÃ_CHỐT nếu có câu đồng ý rõ. Người phụ trách và hạn: chỉ ghi nếu có trong câu trích; không có thì ghi `null`."
  3. *Lượt 3:* "Điền mẫu biên bản. Không thêm gì không có ở lượt 2."
- Đặt ba lượt này vào chỉ dẫn của Project/Gem. Tải mẫu biên bản làm tệp kiến thức.
- **Sản phẩm:** Project/Gem dùng chung; trang hướng dẫn 5 dòng.
- **Lỗi thường gặp:** để AI "tóm tắt cho gọn" trước khi trích, mất nguyên văn.

### Bài C0.4: Bảng kiểm 8 lỗi khi duyệt
- **Thực hành:** người chủ trì duyệt bằng bảng kiểm lấy từ 3.1: câu trích có đúng trong bản ghi? đúng người nói? con số đúng? "đã chốt" có thật chốt? người phụ trách có thật nhận việc? hạn có ai nói? thứ tự đúng? có ai bị liệt kê thừa?
- **Sản phẩm:** bảng kiểm dán cạnh Project.
- **Lỗi thường gặp:** đọc lướt bản tóm tắt vì "đọc trôi chảy"; không mở bản ghi gốc.

### Bài C0.5: Sổ việc và nhắc việc
- **Thực hành:** chép bảng việc đã duyệt vào một Google Sheet chung: mã việc, ngày họp, người, hạn, trạng thái, link biên bản. Họp sau mở sổ trước, cập nhật trạng thái.
- **Sản phẩm:** sổ việc. Đây là "bộ nhớ" đầu tiên của tổ chức.
- **Lỗi thường gặp:** để việc chỉ nằm trong tin nhắn Zalo.

### Bài C0.6: Đo trên 5 cuộc họp
- **Thực hành:** với 5 cuộc họp đầu, người chủ trì tự liệt kê việc **trước** khi đọc bản AI (làm đáp án). Đếm: việc AI bịa, việc AI bỏ sót, việc phải sửa người/hạn. Bấm giờ thời gian làm biên bản tay và bản AI + duyệt.
- **Sản phẩm:** bảng đo 5 dòng. Với n=5, chỉ dùng để phát hiện hỏng, không để kết luận tỷ lệ (xem `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` mục 3.2).
- **Lỗi thường gặp:** đọc bản AI trước rồi mới làm đáp án (bị dẫn dắt).

## 5. Đường không code vs có code

| | Không code | Có code nhẹ |
|---|---|---|
| Làm gì | Project/Gem 3 lượt; người duyệt bằng bảng kiểm | AI trả JSON danh sách việc; script kiểm trích dẫn, tên, hạn |
| Hàng rào | Bảng kiểm do người làm | Code chặn: trích không có trong bản ghi, tên không có trong danh sách, hạn sai |

**Mã mẫu (đã chạy thử, Python 3, `python -I -X utf8`, dữ liệu giả):**

```python
import re, unicodedata
from datetime import date

def chuan(s):
    s = unicodedata.normalize("NFC", s).lower()
    return re.sub(r"\s+", " ", s).strip()

def kiem_viec(viec_list, ban_ghi, nguoi_du, ngay_hop):
    bg, ds, loi = chuan(ban_ghi), {chuan(n) for n in nguoi_du}, []
    for i, v in enumerate(viec_list, 1):
        trich = v.get("trich_nguyen_van") or ""
        if not trich or chuan(trich) not in bg:
            loi.append((i, "TRICH_KHONG_CO_TRONG_BAN_GHI"))
        ai = v.get("nguoi_phu_trach")
        if ai is None:
            loi.append((i, "THIEU_NGUOI_PHU_TRACH"))
        elif chuan(ai) not in ds:
            loi.append((i, "NGUOI_KHONG_CO_TRONG_DANH_SACH"))
        han = v.get("han")
        if han is None:
            loi.append((i, "THIEU_HAN"))
        else:
            try:
                if date.fromisoformat(han) < ngay_hop:
                    loi.append((i, "HAN_TRUOC_NGAY_HOP"))
            except ValueError:
                loi.append((i, "HAN_SAI_DINH_DANG"))
        if v.get("trang_thai") not in ("da_chot", "de_xuat"):
            loi.append((i, "THIEU_TRANG_THAI_CHOT"))
    return loi
```

Kết quả chạy thử với 3 việc giả: việc 2 ("Anh Tuấn sẽ đổi nhà cung cấp bao bì", trong khi bản ghi nói "để tháng sau bàn tiếp") bị bắt `TRICH_KHONG_CO_TRONG_BAN_GHI`; việc 3 gán cho "Hùng" không dự họp bị bắt `NGUOI_KHONG_CO_TRONG_DANH_SACH` và `THIEU_HAN`. Đây đúng là hai lỗi "biến thảo luận thành quyết định" và "bịa việc" ở 3.1.

**Giới hạn:** so chuỗi con đòi hỏi AI chép đúng từng chữ. Bản ghi do máy chép (C1) có lỗi chính tả thì AI có thể "sửa" khi trích, làm kiểm thất bại oan. Khi đó, báo cho người duyệt xem, không tự bỏ qua.

**Khi nào buộc chuyển sang code [Đề xuất]:** (a) hơn khoảng 5 cuộc họp/tuần cần biên bản; (b) muốn tự đổ việc vào Sheet/phần mềm quản lý việc; (c) người duyệt bắt đầu bỏ qua bảng kiểm.

## 6. Tiêu chí lên cấp [Đề xuất]

Lên C1 (hoặc C2) khi đủ:
1. ≥ 4 tuần liên tục, mọi cuộc họp định kỳ có biên bản theo mẫu, được duyệt trong 24 giờ.
2. Trên ≥ 10 cuộc họp có đáp án: không còn việc "đã chốt" nào bị bịa lọt qua người duyệt.
3. Sổ việc được cập nhật ở đầu mỗi cuộc họp sau.
4. Có lý do cần ghi âm (ghi chú tay sót nhiều; họp dài; người ghi chú cũng phải phát biểu).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa, không phải số đo]

- **Xưởng nội thất gỗ 40 người (Bình Dương), họp sản xuất sáng thứ Hai, 30 phút:** người dự: quản đốc, tổ trưởng sơn, tổ trưởng mộc, kho, kinh doanh. Việc điển hình: "lô bàn ăn đơn A giao trước ngày 20", "kiểm độ ẩm gỗ lô mới". Lỗi hay gặp: kinh doanh nói "khách muốn giao sớm", AI ghi thành "Quyết định: giao sớm". Bảng kiểm bắt được nhờ cột trạng thái.
- **Chuỗi 3 phòng khám nha khoa, họp chuyên môn tháng:** việc điển hình: cập nhật quy trình vô trùng, lịch đào tạo. **Không** đưa tên bệnh nhân hay tình trạng sức khỏe vào bản ghi gửi AI (dữ liệu nhạy cảm, xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 3.1). Thay bằng mã ca trước khi dán.
- **Công ty phân phối thiết bị điện 15 người, họp kinh doanh tuần:** nhiều con số (doanh số, công nợ). Quy tắc: mọi con số trong biên bản đánh dấu "cần kiểm" và đối chiếu với file Excel trước khi gửi (con số bịa là nhóm lỗi lớn thứ hai ở 3.1).

## 8. Tài liệu tham khảo

Truy cập 2026-11-11. Tin cậy: Cao = bài báo/tài liệu gốc đã đọc phần chính; Trung bình = tài liệu nhà cung cấp hoặc đọc một phần; Thấp = chỉ đọc tóm tắt.

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| Evaluation-as-Search: Grounding Failures in Meeting Assistants (Microsoft) | https://arxiv.org/abs/2608.20392 | Các trang chính và phụ lục phân loại lỗi | Cao cho bản ghi tiếng Anh; chưa có tiếng Việt |
| Re-FRAME the Meeting Summarization SCOPE (FRAME) | https://arxiv.org/abs/2509.15901 | Các trang chính, bảng kết quả, phụ lục ablation | Trung bình-Cao (n=50, chấm bằng LLM) |
| OSynth (Otter.ai) | https://arxiv.org/abs/2610.29319 | Các trang chính, phụ lục ablation | Trung bình (dữ liệu tổng hợp) |
| Selected Copilot Experiments (Edelman, Microsoft, 5/2024) | https://www.microsoft.com/en-us/research/wp-content/uploads/2024/05/Edelman_Copilot-Experiments-Merged-2024-05-AICE-Shareable.pdf | 12 trang slide đầu | Trung bình (slide nội bộ nhà cung cấp) |
| QMSum benchmark | https://arxiv.org/abs/2104.05938 | Chỉ tóm tắt | Thấp (chỉ dùng để nêu tên bộ dữ liệu) |
| Nhóm RAG cap-08 mục 7.b | `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` | Đã đọc | Nội bộ |

## 9. Chưa kiểm chứng

- Mọi số đo về họp ở mục 3 là trên bản ghi tiếng Anh hoặc dữ liệu tổng hợp. Chưa có số cho họp tiếng Việt, nơi hay dùng cách gọi "anh/chị/em", tên tắt, tiếng lóng nghề.
- Cách 3 lượt ở Bài C0.3 là chuyển thể từ FRAME; chưa đo trên Project/Gem hay tiếng Việt.
- Copilot Teams, Google Meet, Zoom có tóm tắt tiếng Việt hay không: chưa xác minh (xem C1 mục 9).
- Ngưỡng 24 giờ, 4 tuần, 10 cuộc họp, 5 cuộc họp/tuần là đề xuất.
- Slide Edelman: không rõ cỡ mẫu riêng cho tác vụ tóm tắt họp, không rõ cách chấm "độ chính xác".
