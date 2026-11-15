# Cấp 0 (C0): Biên bản họp theo khuôn, có trích nguyên văn

> Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.
> Phần dùng chung đã có ở nhóm RAG, không viết lại: bản giao việc 6 phần, Sổ prompt (`../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`); quy trình biên bản nhiều bước có cổng kiểm (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 7.b).

!!! tip "Tóm tắt nhanh"
    Nhờ AI viết biên bản họp thì dễ, nhưng AI hay **bịa** hoặc **đoán** những chỗ nó không chắc. Bài này dạy một cách làm đơn giản, **không cần biết lập trình**: dùng một mẫu biên bản cố định, bắt AI **chép nguyên văn câu nói** làm bằng chứng cho từng việc, và để người chủ trì **duyệt bằng bảng kiểm** trước khi gửi đi.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** chủ doanh nghiệp, trưởng nhóm, hoặc bất kỳ ai hay được giao "ghi lại cuộc họp". Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Một tài khoản có thể tạo Project (Claude) hoặc Gem (Gemini). Đây là tính năng cho bạn lưu sẵn chỉ dẫn để dùng lại, khỏi phải gõ lại mỗi cuộc họp.
- Ghi chú tay (gõ lại thành chữ) của một vài cuộc họp gần đây để làm thử.
- Một bảng tính Google Sheet hoặc Excel để làm sổ việc.

**Sau bài này, bạn sẽ có:**
1. Mọi cuộc họp định kỳ có biên bản theo **một mẫu cố định**.
2. Mỗi việc cần làm ghi rõ: ai làm, làm gì, hạn khi nào, **trạng thái** (đã chốt hay mới đề xuất), và **một câu trích nguyên văn** để chứng minh việc đó có thật.
3. Người chủ trì duyệt biên bản trong vòng 24 giờ, trước khi gửi cho mọi người.
4. Một cách đo đơn giản để biết AI đang bịa, sót, hay làm sai bao nhiêu việc.

**Thứ bạn cầm đi được sau bài:** mẫu biên bản 1 trang; một Project (Claude) hoặc Gem (Gemini) tên "Thư ký họp"; bảng kiểm 8 lỗi; và sổ việc trên Google Sheet hoặc Excel.

## 2. Câu hỏi cấp này trả lời

*"Làm sao để mỗi cuộc họp để lại một danh sách việc đáng tin, không mất thêm nhiều thời gian?"*

Đây là bài đầu tiên của nhóm, vì ai cũng gặp: họp xong, mỗi người hiểu một kiểu, rồi việc rơi rụng.

Khi dùng AI một cách tùy tiện **[Đề xuất, quan sát]**, chuyện thường xảy ra như sau. Bạn dán ghi chú họp vào khung chat và nhận về một đoạn tóm tắt đọc rất trôi chảy. Vì đọc trôi chảy nên không ai kiểm. Nhưng bên trong có thể có những lỗi nhỏ mà hậu quả không nhỏ: một ý kiến kiểu "hay là mình thử..." bị ghi thành "Quyết định: ...", hoặc một việc không ai nhận lại được gán cho một người cụ thể.

## 3. Kiến thức nền

Trước khi làm, nên hiểu vì sao AI hay sai ở việc này. Phần dưới đây tóm tắt ba nghiên cứu và một thí nghiệm, đều giúp bạn đặt ra quy tắc làm việc.

!!! note "Lưu ý khi đọc các số liệu"
    Các nghiên cứu dưới đây làm trên bản ghi cuộc họp **tiếng Anh** hoặc dữ liệu **tổng hợp** (do máy tạo ra). Chưa có số đo nào trên cuộc họp tiếng Việt, nơi người ta hay dùng "anh/chị/em", tên tắt và tiếng lóng nghề. Hãy dùng chúng để biết **AI hay sai kiểu gì**, đừng dùng để suy ra tỷ lệ sai ở công ty bạn.

### 3.1 AI sai ở đâu khi đọc cuộc họp [Nguồn]

Nhóm nghiên cứu của Microsoft (arXiv 2608.20392) đã thử "bắt lỗi" một trợ lý AI trả lời câu hỏi về cuộc họp. Họ dùng 20 bản ghi tiếng Anh (cuộc họp trong bộ dữ liệu AMI, ICSI và các phiên họp nghị viện) và 3 mô hình AI. Kết quả có 1.049 lỗi, được chia thành 8 nhóm:

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

Ngay cả mô hình mạnh nhất trong thí nghiệm (GPT-5.2-chat) vẫn sai; lỗi đặc trưng của nó là **bịa việc cần làm** (15,8% số lỗi của nó).

Cần hiểu đúng con số này: đó là tỷ lệ lỗi khi các nhà nghiên cứu **cố tình đặt câu hỏi để dò lỗi** (cứ 100 câu hỏi dò thì có khoảng 5,2 đến 15,3 câu làm lộ lỗi, tùy mô hình). Đó **không phải** tỷ lệ lỗi trung bình của một biên bản bạn nhờ AI viết.

!!! tip "Nói đơn giản"
    AI không nói dối cố ý, nhưng nó có thói quen "lấp chỗ trống" cho câu chuyện nghe trọn vẹn. Vì vậy ba chỗ cần canh nhất là: **quyết định** (đã chốt thật chưa), **người phụ trách** (có ai nhận thật không) và **con số**.

### 3.2 Tách bước tốt hơn một lệnh duy nhất [Nguồn]

Nghiên cứu FRAME (arXiv 2509.15901) dùng 50 mẫu từ bộ QMSum và 50 mẫu tổng hợp, với GPT-4o. Cách làm của họ là chia việc thành các bước: trích các sự kiện riêng lẻ, chọn cái quan trọng, lập dàn ý, rồi mới viết biên bản. Kết quả: điểm "bịa nội dung" (thang 1 đến 5, **điểm càng thấp càng tốt**) giảm từ 3 xuống 1 trên bộ QMSum. Ngược lại, khi gộp mọi bước vào **một lệnh duy nhất**, điểm "bỏ sót" lên 4 (tệ hơn bản tách bước 3 điểm). Việc chấm điểm do một AI chấm (bộ chấm MESA), không phải người chấm.

!!! tip "Nói đơn giản"
    Giống như nhờ một nhân viên: bảo họ "gạch chân những câu quan trọng trước, rồi mới viết" sẽ cho kết quả ít sai hơn là bảo "tóm tắt đi" ngay từ đầu. Bài thực hành C0.3 áp dụng đúng ý này.

### 3.3 Danh sách người dự họp giúp gán đúng người [Nguồn]

Nghiên cứu của Otter.ai (arXiv 2610.29319, dùng dữ liệu họp tổng hợp bằng tiếng Anh) cho thấy: độ đúng khi gán người phụ trách việc tăng từ 0,524 lên 0,752 khi cho AI thêm văn bản nền (danh sách thành viên, email, slide). Khi thêm cả mẫu giọng nói thì lên 0,792. Nếu không có danh sách tên, hệ thống tự "bịa" một cái tên nghe giống (ví dụ "Bevan" thay vì "Devon Ashby"). Tác giả nói rõ họ không khẳng định con số này đúng với ghi âm thật.

!!! tip "Nói đơn giản"
    Hãy đưa cho AI **danh sách người dự họp** trước khi nhờ nó viết biên bản. Việc này tốn một phút nhưng giảm đáng kể việc ghi nhầm tên.

### 3.4 Đừng tin cảm giác "tiết kiệm thời gian" [Nguồn]

Đây là slide của một thí nghiệm có nhóm đối chứng do Microsoft thực hiện (Edelman, 5/2024; 147 người làm tự do trên Upwork, làm 4 tác vụ). Với việc tóm tắt cuộc họp Teams bằng Copilot, người dùng làm nhanh hơn 19%, còn độ chính xác không thay đổi có ý nghĩa thống kê. Điều đáng chú ý: trên cả 4 tác vụ, người dùng **nói** Copilot tiết kiệm cho họ 36 phút, nhưng thí nghiệm **đo được** 12 phút. Lưu ý đây là tài liệu nội bộ dạng slide của nhà cung cấp, chưa qua bình duyệt.

!!! tip "Nói đơn giản"
    Cảm giác "AI giúp mình nhanh hơn nhiều" thường lớn hơn thực tế. Vì thế bài C0.6 dạy bạn **bấm giờ thật** thay vì ước chừng.

### 3.5 Ba quy tắc rút ra [Đề xuất]

1. **Không trích được nguyên văn thì không phải việc đã chốt.**
2. **Không ai nhận thì để trống**, không đoán.
3. **Phân biệt "đã chốt" và "đề xuất"** ngay trong mẫu biên bản.

## 4. Chuỗi bài nhỏ

Sáu bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và lỗi hay gặp để tránh.

### Bài C0.1: Mẫu biên bản 1 trang
- **Việc cần làm:** soạn một mẫu gồm 5 phần cố định: (1) Thông tin họp (ngày, người chủ trì, người dự); (2) Quyết định đã chốt; (3) Việc cần làm, dạng bảng `việc | người phụ trách | hạn | trạng thái | trích nguyên văn`; (4) Vấn đề còn treo; (5) Thông tin cần kiểm (con số, tên khách mà AI không chắc).
- **Bạn có sau bài:** mẫu trên Google Docs hoặc Word, ghim trong nhóm Zalo của phòng để ai cũng thấy.
- **Lỗi hay gặp:** mẫu có tới 15 mục nên không ai điền; hoặc thiếu cột "trạng thái".

### Bài C0.2: Chuẩn bị đầu vào
- **Việc cần làm:** trước buổi họp, ghi sẵn danh sách người dự theo đúng cách gọi trong họp (ví dụ "chị Lan", "anh Tuấn kho") và chương trình họp 3 đến 5 mục. Thứ bạn đưa cho AI là ghi chú tay đã gõ lại, hoặc bản chép lời có sẵn (Cấp C1 sẽ chỉ cách tạo bản chép lời từ ghi âm).
- **Bạn có sau bài:** một khối "Bối cảnh họp" để dán vào đầu mỗi lần nhờ AI viết biên bản.
- **Lỗi hay gặp:** chỉ dán bản ghi mà không có danh sách tên (xem mục 3.3).

### Bài C0.3: Project/Gem "Thư ký họp" chạy 3 lượt
- **Việc cần làm [Đề xuất, dựa trên 3.2]:** trong cùng một cuộc trò chuyện với AI, làm **ba lượt** thay vì một lệnh "tóm tắt cuộc họp":
  1. *Lượt 1:* "Liệt kê mọi câu có nội dung giao việc, chốt, hoặc con số. Mỗi dòng chép **nguyên văn** câu đó và tên người nói. Không diễn giải."
  2. *Lượt 2:* "Với từng dòng, gán nhãn: QUYẾT_ĐỊNH_ĐÃ_CHỐT / ĐỀ_XUẤT / VIỆC / THÔNG_TIN. Chỉ gán ĐÃ_CHỐT nếu có câu đồng ý rõ. Người phụ trách và hạn: chỉ ghi nếu có trong câu trích; không có thì ghi `null`."
  3. *Lượt 3:* "Điền mẫu biên bản. Không thêm gì không có ở lượt 2."
- Cách đặt: chép ba lượt này vào phần chỉ dẫn của Project hoặc Gem, và tải mẫu biên bản lên làm tệp kiến thức. (Chữ `null` ở lượt 2 chỉ có nghĩa là "để trống".)
- **Bạn có sau bài:** một Project hoặc Gem dùng chung cho cả nhóm, kèm trang hướng dẫn 5 dòng.
- **Lỗi hay gặp:** để AI "tóm tắt cho gọn" trước khi trích, làm mất câu nguyên văn.

### Bài C0.4: Bảng kiểm 8 lỗi khi duyệt
- **Việc cần làm:** người chủ trì duyệt biên bản bằng bảng kiểm lấy từ 8 nhóm lỗi ở mục 3.1. Tám câu hỏi cần trả lời: câu trích có đúng nằm trong bản ghi không? Đúng người nói không? Con số đúng không? "Đã chốt" có thật sự chốt không? Người phụ trách có thật nhận việc không? Hạn có ai nói ra không? Thứ tự đúng không? Có ai bị liệt kê thừa không?
- **Bạn có sau bài:** bảng kiểm dán cạnh Project để dùng mỗi lần duyệt.
- **Lỗi hay gặp:** đọc lướt bản tóm tắt vì "đọc trôi chảy"; không mở bản ghi gốc ra đối chiếu.

### Bài C0.5: Sổ việc và nhắc việc
- **Việc cần làm:** chép bảng việc đã duyệt vào một Google Sheet chung với các cột: mã việc, ngày họp, người, hạn, trạng thái, link biên bản. Đầu buổi họp sau, mở sổ trước và cập nhật trạng thái từng việc.
- **Bạn có sau bài:** sổ việc. Đây là "bộ nhớ" đầu tiên của cả tổ chức.
- **Lỗi hay gặp:** để việc chỉ nằm trong tin nhắn Zalo.

### Bài C0.6: Đo trên 5 cuộc họp
- **Việc cần làm:** với 5 cuộc họp đầu tiên, người chủ trì tự liệt kê các việc **trước** khi đọc bản AI viết (đó là "đáp án" của bạn). Sau đó đếm: việc AI bịa, việc AI bỏ sót, việc phải sửa người hoặc hạn. Bấm giờ thời gian làm biên bản bằng tay và thời gian làm bằng AI cộng với thời gian duyệt.
- **Bạn có sau bài:** bảng đo 5 dòng. Với chỉ 5 cuộc họp, bảng này chỉ dùng để **phát hiện hỏng**, không dùng để kết luận tỷ lệ (xem `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` mục 3.2).
- **Lỗi hay gặp:** đọc bản AI trước rồi mới làm đáp án, nên bị dẫn dắt theo AI.

## 5. Đường không code vs có code

Bài này có hai cách làm. Cách 1 không cần code, đủ dùng khi mới bắt đầu. Cách 2 cần một chút lập trình, để máy tự kiểm thay cho người.

| | Không code | Có code nhẹ |
|---|---|---|
| Làm gì | Project/Gem 3 lượt; người duyệt bằng bảng kiểm | AI trả JSON danh sách việc; script kiểm trích dẫn, tên, hạn |
| Hàng rào | Bảng kiểm do người làm | Code chặn: trích không có trong bản ghi, tên không có trong danh sách, hạn sai |

(JSON là một cách viết danh sách có khung rõ ràng để máy đọc được. Script là một đoạn chương trình ngắn.)

**Đoạn mã dưới đây làm gì?** Nó nhận danh sách việc mà AI đã soạn, rồi tự kiểm từng việc: câu trích có thật sự nằm trong bản ghi cuộc họp không, người phụ trách có trong danh sách người dự không, hạn có bị ghi trước ngày họp không, trạng thái đã ghi rõ chưa. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

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

**Kết quả chạy thử** với 3 việc giả: việc 2 ("Anh Tuấn sẽ đổi nhà cung cấp bao bì", trong khi bản ghi nói "để tháng sau bàn tiếp") bị bắt lỗi `TRICH_KHONG_CO_TRONG_BAN_GHI`; việc 3 gán cho "Hùng" (người không dự họp) bị bắt `NGUOI_KHONG_CO_TRONG_DANH_SACH` và `THIEU_HAN`. Đây đúng là hai lỗi "biến thảo luận thành quyết định" và "bịa việc" đã nói ở mục 3.1.

**Giới hạn:** cách kiểm này đòi hỏi AI chép đúng **từng chữ** câu trích. Nếu bản ghi do máy chép lời (Cấp C1) có lỗi chính tả, AI có thể tự "sửa" khi trích, làm phép kiểm báo lỗi oan. Khi đó hãy báo cho người duyệt xem, đừng tự bỏ qua.

**Khi nào nên chuyển sang code [Đề xuất]:** (a) có hơn khoảng 5 cuộc họp mỗi tuần cần biên bản; (b) muốn tự đổ việc vào Google Sheet hoặc phần mềm quản lý việc; (c) người duyệt bắt đầu bỏ qua bảng kiểm.

## 6. Tiêu chí lên cấp [Đề xuất]

Bạn có thể sang cấp tiếp theo (C1, hoặc C2) khi đạt đủ các điều sau:
1. Liên tục ≥ 4 tuần, mọi cuộc họp định kỳ đều có biên bản theo mẫu và được duyệt trong 24 giờ.
2. Trên ≥ 10 cuộc họp có đáp án để so: không còn việc "đã chốt" nào bị bịa mà lọt qua người duyệt.
3. Sổ việc được cập nhật ở đầu mỗi cuộc họp sau.
4. Có lý do cần ghi âm: ghi chú tay sót nhiều, họp dài, hoặc người ghi chú cũng phải phát biểu.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa, không phải số đo]

Ba tình huống giả định để bạn dễ hình dung:

- **Xưởng nội thất gỗ 40 người (Bình Dương), họp sản xuất sáng thứ Hai, 30 phút.** Người dự: quản đốc, tổ trưởng sơn, tổ trưởng mộc, kho, kinh doanh. Việc điển hình: "lô bàn ăn đơn A giao trước ngày 20", "kiểm độ ẩm gỗ lô mới". Lỗi hay gặp: bên kinh doanh nói "khách muốn giao sớm", AI lại ghi thành "Quyết định: giao sớm". Bảng kiểm bắt được lỗi này nhờ cột trạng thái.
- **Chuỗi 3 phòng khám nha khoa, họp chuyên môn hằng tháng.** Việc điển hình: cập nhật quy trình vô trùng, lịch đào tạo. **Không** đưa tên bệnh nhân hay tình trạng sức khỏe vào bản ghi gửi AI (đây là dữ liệu nhạy cảm, xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 3.1). Hãy thay bằng mã ca trước khi dán.
- **Công ty phân phối thiết bị điện 15 người, họp kinh doanh hằng tuần.** Có nhiều con số (doanh số, công nợ). Quy tắc: mọi con số trong biên bản đều đánh dấu "cần kiểm" và đối chiếu với file Excel trước khi gửi (con số bịa là nhóm lỗi lớn thứ hai ở mục 3.1).

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
