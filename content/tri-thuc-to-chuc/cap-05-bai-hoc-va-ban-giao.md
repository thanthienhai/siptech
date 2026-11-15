# Cấp 5 (C5): Gom bài học sau sự cố và bàn giao khi nghỉ việc

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác. Không phải tư vấn pháp lý.
> Dùng lại: phỏng vấn rút tri thức (C2 của nhóm này); sổ đăng ký và chủ sở hữu (C3); quy trình sự cố dữ liệu (`../an-toan-du-lieu-va-phap-ly-vn.md` Bài A6).

!!! tip "Tóm tắt nhanh"
    Có hai thứ rất dễ mất trong một doanh nghiệp: **kinh nghiệm rút ra từ sai lầm** (sự cố xong là quên) và **mọi điều một người biết** khi họ nghỉ việc. Bài này hướng dẫn bạn gom mỗi sự cố thành một "bài học" theo mẫu, cho máy lọc bớt dữ liệu nhạy cảm rồi người duyệt, và làm một gói bàn giao khi có nhân viên nghỉ. Sau bài, bạn có kho bài học, danh sách kiểm bàn giao và cách xử lý dữ liệu cá nhân của người nghỉ. Bạn **không cần biết lập trình** để làm cách đầu tiên.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** quản lý vận hành, trưởng dự án, nhân sự. Bạn không cần biết code.

**Bạn cần chuẩn bị:**
- Các tài liệu mà bài này dùng lại: kết quả phỏng vấn rút tri thức (Cấp C2 của nhóm này), sổ đăng ký và chủ sở hữu tài liệu (Cấp C3), sổ việc và biên bản họp (Cấp C0).
- Một nơi để làm kho bài học: Google Sheet, Notion hoặc Lark (đều là công cụ bảng/ghi chú trên mạng, ai cũng dùng được).
- Một tài khoản AI có thể tạo Project (gói chỉ dẫn lưu sẵn để dùng lại nhiều lần).
- Một vài chuỗi tin nhắn xử lý sự cố hoặc biên bản họp rút kinh nghiệm gần đây để làm thử.

**Sau bài này bạn sẽ có:**
1. Mỗi sự cố đáng kể và mỗi dự án kết thúc để lại **một bài học** theo mẫu, có hành động sửa tài liệu cụ thể.
2. Bài học đi qua **lọc bằng code** (chặn dữ liệu nhạy cảm, phát hiện bài trùng) và **người duyệt** trước khi vào kho.
3. Khi nhân viên nghỉ: có **gói bàn giao** lấy từ sổ đăng ký, sổ việc, danh sách tài khoản; có buổi phỏng vấn bàn giao.
4. Dữ liệu cá nhân của người nghỉ được xử lý theo quy định (xóa phần phải xóa).

**Thứ bạn cầm đi được sau bài:** mẫu bài học; kho bài học (Sheet/Notion/Lark); script `bai_hoc.py` (script là một đoạn chương trình ngắn, ở đây dùng để lọc bài học); danh sách kiểm bàn giao; quy trình bàn giao 1 trang.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Lỗi này năm ngoái đã xảy ra rồi, sao lại xảy ra? Chị Hoa nghỉ, ai biết mật khẩu web và cách làm hồ sơ thầu?"*

Các cấp C0 đến C4 giúp bạn tạo và giữ tài liệu cho việc **đang** làm. Còn hai dòng tri thức hay mất nhất:
- **Kinh nghiệm từ sai lầm.** Nó nằm lẫn trong tin nhắn lúc xử lý sự cố, xong việc là trôi mất.
- **Mọi thứ một người biết** khi họ rời đi.

## 3. Kiến thức nền

### 3.1 Bộ nhớ từ đóng góp: gom được, chưa chứng minh có ích [Nguồn]

Nghiên cứu **SAP** (arXiv 2608.00122, qua `../nen-tang-bang-chung.md`) làm một hệ thống như sau. Khi một người làm thay đổi tệp tri thức, hệ thống **hỏi xin phép** người đó. Sau đó một chuỗi xử lý tự soạn cặp hỏi-đáp, gắn nhãn, **quét bảo mật** (tìm dữ liệu không được để lọt), và **kiểm trùng** (xem có mục giống sẵn có chưa). Kết quả: 900 đóng góp tạo ra 1.144 mục; chỉ 53,7% đóng góp tạo ra ít nhất một mục. Tác giả thừa nhận ba điều. Một là họ **chưa đo** hiệu quả đối với chất lượng công việc. Hai là điểm tin cậy chưa hiệu chuẩn (tức chưa kiểm xem điểm đó có phản ánh đúng độ tin cậy thật hay không). Ba là có nguy cơ **nhiễm độc bộ nhớ dùng chung**, nghĩa là một mục sai hoặc xấu lọt vào kho thì cả nhóm cùng dùng phải nó.

**[Đề xuất] Ý nghĩa:** gom bài học là việc làm được, nhưng hãy đo xem nó có được dùng không (C7), và chặn rác trước khi vào kho.

!!! tip "Nói đơn giản"
    Gom bài học vào một kho chung thì làm được. Nhưng chưa ai chứng minh kho đó giúp làm việc tốt hơn, và nếu để lọt thứ sai hay thứ nhạy cảm vào thì cả nhóm cùng bị ảnh hưởng. Vì vậy phải có bước lọc và người duyệt, rồi theo dõi xem bài học có được đọc thật không.

### 3.2 AI giúp tóm tắt sự cố [Nguồn]

Đây là một thí nghiệm do Microsoft thực hiện (slide của Edelman, 5/2024). Họ cho 149 người mới về bảo mật (tuyển trên Upwork) làm ba việc: tóm tắt sự cố, viết báo cáo sự cố, phân tích script. Nhóm có Copilot đạt điểm nội dung tóm tắt sự cố cao hơn 151%, chất lượng tóm tắt cao hơn 32%; giữ nguyên chất lượng thì nhanh hơn 26%. Người dùng **nói** là tiết kiệm 38 phút, còn thí nghiệm **đo được** 5 phút. Lưu ý đây là slide của nhà cung cấp, dùng công cụ chuyên dụng, không phải bối cảnh doanh nghiệp vừa và nhỏ (SME).

!!! tip "Nói đơn giản"
    AI giúp tóm tắt sự cố tốt hơn và nhanh hơn trong thí nghiệm này. Nhưng cảm giác "tiết kiệm được nhiều" của người dùng vẫn lớn hơn số đo thật. Đừng dùng con số này để hứa hẹn kết quả cho công ty bạn.

### 3.3 Pháp lý khi nhân viên nghỉ [Nguồn, xác minh một phần]

Nội dung dưới đây **không phải tư vấn pháp lý**. Nó dựa trên Điều 25 Luật 91/2025/QH15 (qua hethongphapluat.com, chưa đối chiếu Công báo):
- Khoản 2: dữ liệu cá nhân người lao động phải lưu trong thời hạn theo luật hoặc thỏa thuận; **khi chấm dứt hợp đồng phải xóa, hủy**, trừ khi có thỏa thuận hoặc luật quy định khác.
- Khoản 1: ứng viên không được tuyển thì phải xóa, hủy thông tin đã cung cấp, trừ khi có thỏa thuận khác.

**[Đề xuất]** Hãy tách hai thứ:
- (a) **Tri thức công việc** (SOP, ghi chú quy trình, bài học đã bỏ tên người) là tài sản công ty, giữ lại. SOP là "quy trình làm việc chuẩn", tức tài liệu viết các bước làm một việc.
- (b) **Dữ liệu cá nhân** của người nghỉ (bản ghi giọng nói phỏng vấn, đánh giá cá nhân, thông tin liên lạc riêng) xử lý theo Điều 25.

Thời hạn lưu hồ sơ lao động, BHXH (bảo hiểm xã hội), thuế theo luật khác: hãy hỏi kế toán hoặc luật sư.

!!! tip "Nói đơn giản"
    Cái người nghỉ **biết về công việc** thì công ty giữ. Cái thuộc về **riêng người đó** (giọng nói, đánh giá, liên lạc riêng) thì phần lớn phải xóa khi họ nghỉ. Xóa hay giữ đến bao lâu thì hỏi kế toán hoặc luật sư.

### 3.4 Rủi ro riêng của bàn giao [Đề xuất, dựa `../an-toan-du-lieu-va-phap-ly-vn.md` mục 3.3]

Có ba chỗ hay bị bỏ sót:
- Project/Gem/GPT (các gói chỉ dẫn AI lưu sẵn), lịch sử chat và tệp tải lên nằm trong **tài khoản AI cá nhân** của người nghỉ. Họ đi thì công ty không còn truy cập được.
- Người nghỉ là quản trị viên duy nhất của nhóm Zalo khách hàng, trang Facebook, tài khoản trên sàn thương mại điện tử.
- Mật khẩu bị ghi trong ghi chú hoặc tin nhắn, rồi vô tình bị chép vào bài học.

## 4. Chuỗi bài nhỏ

Tám bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và lỗi hay gặp để tránh.

### Bài C5.1: Mẫu bài học 1 trang
- **Việc cần làm [Đề xuất]:** soạn một mẫu gồm 6 mục:
  1. Chuyện gì xảy ra (thời gian, ảnh hưởng: tiền, khách, giờ công).
  2. Phát hiện thế nào.
  3. Vì sao (nguyên nhân do quy trình, **không** đổ lỗi cá nhân).
  4. Đã xử lý gì.
  5. **Thay đổi tài liệu:** mã tài liệu trong sổ C3 và bước cần thêm hoặc sửa.
  6. Nguồn (link biên bản, ngày tin nhắn).
- **Bạn có sau bài:** mẫu bài học.
- **Lỗi hay gặp:** bài học chỉ là "cần cẩn thận hơn"; không gắn với tài liệu nào. Một bài học tốt phải dẫn tới việc sửa một tài liệu cụ thể (mục 5 của mẫu).

### Bài C5.2: AI nháp bài học từ tin nhắn và biên bản
- **Việc cần làm:** dán chuỗi tin nhắn xử lý sự cố (đã che tên khách, số điện thoại) và biên bản họp rút kinh nghiệm (C0) vào Project "Bài học". Chỉ dẫn cho AI gồm ba ý: điền mẫu 6 mục; mục 3 và mục 5 phải trích nguyên văn câu trong nguồn; chỗ nào không có thì để `??`. (Dấu `??` nghĩa là "chưa biết, để người điền sau".)
- **Bạn có sau bài:** bản nháp bài học.
- **Lỗi hay gặp:** AI tự viết một nguyên nhân "nghe hợp lý" mà không ai nói. Quy tắc trích nguyên văn ở mục 3 và mục 5 là để chặn lỗi này.

### Bài C5.3: Lọc bằng code
- **Việc cần làm:** chạy `bai_hoc.py` (mã mẫu ở mục 5). Đoạn chương trình này làm ba việc: chặn bài có số điện thoại, email, số CCCD (căn cước công dân), chuỗi giống mật khẩu; đánh dấu bài gần giống bài cũ để người duyệt gộp lại; chuyển các bài còn lại cho người duyệt. Bạn nên bổ sung các mẫu nhạy cảm riêng của công ty (ví dụ mã số thuế của khách, số tài khoản). Nếu bạn không biết lập trình, hãy nhờ người biết code hoặc nhờ AI chạy giúp.
- **Bạn có sau bài:** danh sách chia ba nhóm: bị chặn / nghi trùng / chờ duyệt.
- **Lỗi hay gặp:** chỉ dựa vào việc AI "nhớ che thông tin" (hàng rào bằng prompt, tức bằng lời dặn). Lời dặn có thể bị quên, còn bước lọc bằng code thì luôn chạy.

### Bài C5.4: Duyệt và biến thành thay đổi tài liệu
- **Việc cần làm:** chủ tài liệu (theo sổ C3) duyệt bài học. Mục 5 của bài học tạo ra một việc trong sổ việc (C0), ví dụ "sửa SOP-X bước B4, hạn ...". Bài học chỉ "đóng" khi tài liệu đã được sửa. Đồng thời gắn bài học vào tài liệu liên quan, để người đọc tài liệu cũng thấy bài học đó.
- **Bạn có sau bài:** kho bài học có trạng thái: nháp / đã duyệt / đã áp dụng vào tài liệu.
- **Lỗi hay gặp:** duyệt xong rồi để đó, không có ai sửa tài liệu, nên lỗi cũ lại lặp lại.

### Bài C5.5: Ôn cuối dự án
- **Việc cần làm:** họp 30 phút cuối mỗi dự án hoặc mùa vụ, chỉ trả lời 3 câu: giữ gì, bỏ gì, đổi gì. Làm biên bản theo C0, rồi tách thành bài học theo C5.1.
- **Bạn có sau bài:** một biên bản ôn cuối dự án và các bài học tách ra từ đó.

### Bài C5.6: Danh sách kiểm bàn giao
- **Việc cần làm [Đề xuất]:** khi có đơn nghỉ việc, chạy bốn bước sau:
  1. Lọc sổ đăng ký (C3): mọi tài liệu có `chu_so_huu` (cột ghi chủ sở hữu) bằng tên người nghỉ thì chọn chủ mới.
  2. Lọc sổ việc (C0): việc đang mở của người nghỉ thì giao lại cho người khác.
  3. Lập danh sách tài khoản: email, Drive, Zalo OA/nhóm (quyền quản trị), sàn TMĐT (thương mại điện tử), tài khoản AI (Project/Gem/GPT có dùng cho công việc không). Với mỗi thứ, chuyển quyền hoặc xuất nội dung ra.
  4. Tài liệu chỉ nằm trên máy hoặc tài khoản cá nhân (xem bản đồ ở C3.1) thì chuyển vào kho công ty.
- **Bạn có sau bài:** biểu mẫu bàn giao có chữ ký hai bên.
- **Lỗi hay gặp:** chỉ bàn giao tài liệu mà quên quyền quản trị tài khoản (nhóm Zalo, trang Facebook, sàn).

### Bài C5.7: Phỏng vấn bàn giao
- **Việc cần làm:** dùng bộ câu hỏi của C2 cho 2-3 việc chỉ người nghỉ biết. Hỏi thêm hai câu: "ai là đầu mối bên khách/nhà cung cấp?" và "việc gì hay bị quên vào cuối tháng/quý?". Hãy thông báo mục đích buổi phỏng vấn cho người nghỉ. Chỉ giữ SOP và các trích đoạn cần thiết, xóa âm thanh theo quy tắc C1.
- **Bạn có sau bài:** SOP nháp. Sau đó đi tiếp theo C2.4-C2.7, với người kế nhiệm làm thử theo SOP.

### Bài C5.8: Xử lý dữ liệu cá nhân của người nghỉ
- **Việc cần làm:** làm theo mục 3.3. Liệt kê dữ liệu cá nhân của người nghỉ mà quy trình dùng AI đã tạo ra (bản ghi phỏng vấn, mẫu giọng nếu có, ghi chú đánh giá). Xóa phần không có căn cứ để giữ. Ghi lại ngày xóa.
- **Bạn có sau bài:** dòng nhật ký xóa.

## 5. Đường không code vs có code

Bài này có hai cách làm. Cách 1 không cần code, đủ dùng khi mới bắt đầu. Cách 2 cần một chút lập trình, để máy làm thay những việc lặp lại.

| | Không code | Có code nhẹ |
|---|---|---|
| Nháp bài học | Project "Bài học" | API + mẫu JSON |
| Lọc | Người duyệt đọc kỹ | `bai_hoc.py` chặn trước |
| Bàn giao | Lọc Sheet bằng tay | Script lọc sổ C3 và sổ việc theo tên người nghỉ |

(API là cách một chương trình "gọi" AI để nhờ làm việc, không qua khung chat. JSON là một cách viết dữ liệu có khung rõ ràng để máy đọc được. Script là một đoạn chương trình ngắn.)

**Đoạn mã dưới đây làm gì?** Nó nhận danh sách bài học mới và kho bài học cũ. Với mỗi bài mới, nó tìm trong nội dung các mẫu nhạy cảm: số điện thoại (10 chữ số bắt đầu bằng 0), email, số CCCD (12 chữ số), và chuỗi có dạng "mật khẩu: ...". Bài nào dính thì bị chặn. Bài còn lại được so với các bài cũ theo số từ giống nhau (cách so này gọi là Jaccard); nếu giống từ 0,6 trở lên thì đánh dấu nghi trùng, nếu không thì chuyển cho người duyệt. Các "biểu thức chính quy" (`re.compile`) là cách viết mẫu để máy tìm ra chuỗi có hình dạng nhất định, ví dụ một dãy 10 chữ số. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

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

**Kết quả chạy thử** với 3 bài giả và kho 1 bài: bài về "độ ẩm gỗ trên 12% phải sấy lại" bị đánh dấu `NGHI_TRUNG` với bài cũ; bài có "0912345678" và "mật khẩu: abc123" bị `CHAN_NHAY_CAM` (SDT, MAT_KHAU); bài về chụp ảnh kiện hàng xuất khẩu đi tiếp tới người duyệt.

!!! tip "Nói đơn giản"
    Đoạn mã này chỉ là "chốt chặn đầu tiên": thấy số điện thoại, email, số căn cước, mật khẩu thì không cho vào kho, thấy bài giống bài cũ thì báo người duyệt gộp. Người duyệt vẫn phải đọc từng bài.

**Giới hạn:** biểu thức chính quy bỏ sót tên người, địa chỉ, và số viết có dấu cách (ví dụ "0912 345 678"). Code là lớp chặn đầu, người duyệt vẫn phải đọc. Ngưỡng trùng 0,6 là đề xuất; so trùng theo từ không bắt được hai bài cùng ý nhưng khác chữ.

**Khi nào buộc chuyển sang code [Đề xuất]:** > 10 bài học/tháng; có > 1 người nghỉ mỗi quý; muốn bài học tự hiện ra khi ai đó mở tài liệu liên quan.

## 6. Tiêu chí lên cấp [Đề xuất]

Bạn có thể sang cấp tiếp theo khi đạt đủ các điều sau:
1. 3 tháng liên tục: mọi sự cố được phân loại "đáng kể" có bài học; ≥ 80% bài học đã áp dụng vào tài liệu.
2. Không bài học nào trong kho chứa dữ liệu bị chặn (kiểm ngẫu nhiên 20 bài).
3. Lần nghỉ việc gần nhất: 100% tài liệu và việc của người nghỉ có chủ mới trước ngày nghỉ; người kế nhiệm làm được việc chính theo SOP.
4. Có nhật ký xử lý dữ liệu cá nhân của người nghỉ.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung:

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
