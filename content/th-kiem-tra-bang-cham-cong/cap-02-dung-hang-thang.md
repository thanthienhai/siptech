# Bài 3. Đưa vào dùng hằng tháng: lặp lại, tự kiểm, người duyệt

Hai bài trước cho thấy agent viết được chương trình tính công và báo bất thường khá sát đáp án trên dữ liệu giả. Bài này trả lời câu hỏi của người làm lương: **tháng sau làm thế nào, ai chịu trách nhiệm, và khi nào không nên tin?**

**Mục tiêu đo được:** có một quy trình hằng tháng 8 bước chạy trong dưới 10 phút (không tính thời gian người duyệt), có bộ tự kiểm bắt được lỗi hình thức mà không cần đáp án, và có danh sách rõ những việc chỉ người làm được.

> Dữ liệu và công ty trong bài là giả. Các ngưỡng là tham số giả định. Quy định pháp luật về giờ làm thêm, nghỉ lễ, nghỉ phép: cần kiểm với văn bản hiện hành hoặc chuyên gia nhân sự; bài này không trích điều luật.

## 1. Nguyên tắc: tách "phép tính" khỏi "lời giải thích"

Trong prompt ở bài 1 mình giao: phép tính giờ do code làm, mô hình chỉ giúp giải thích ngoại lệ. Sau hai bài chạy, có thể nói chính xác điều gì đã xảy ra:

- Agent viết `tinh_cong.py` (khoảng 420 đến 550 dòng, **[Đo được]**: 418 đến 550 dòng (đếm bằng `wc -l`) trên bảy bộ đầu ra) và chạy nó. Mọi con số trong ba CSV do chương trình này sinh.
- Các câu `giai_thich` **cũng nằm trong chương trình**, dưới dạng câu mẫu theo từng loại bất thường (mình mở hai tệp để kiểm: ví dụ câu "Nên hỏi quản lý trực tiếp xem là nghỉ chưa làm đơn hay chưa ghi nhận quẹt" nằm thẳng trong mã của Claude Code lần 1; câu về "kiểm tra camera" nằm trong mã của `agy` lần 2). Nghĩa là mô hình **viết lời giải thích một lần, khi viết code**; mỗi tháng chạy lại không cần gọi mô hình nữa.

Điều này có hai hệ quả. Một là tháng sau bạn chạy lại **không tốn token, không gửi dữ liệu lên đám mây**. Hai là nếu agent đã lỡ nhúng một câu bạn không muốn (ví dụ gợi ý "trích xuất camera"), câu đó sẽ lặp lại mọi tháng cho đến khi bạn sửa trong mã. Hãy đọc các câu mẫu một lần, trước khi chấp nhận chương trình.

## 2. Chạy lại không cần agent: đã thử thật

**[Đo được]** (2026-11-20): mình lấy `tinh_cong.py` do Claude Code (lần 1) và `agy` (lần 2) viết, chép vào một thư mục mới cùng bốn CSV, rồi chạy bằng Python thường, **không có agent**:

```
python -X utf8 tinh_cong.py
```

- Với Claude Code lần 1: chạy xong trong khoảng 0,3 giây trên máy này; nội dung ba CSV **giống hệt** bản agent sinh (so từng ô; các byte khác nhau chỉ ở ký tự xuống dòng khi mình chép tệp).
- Với `agy` lần 2: ba CSV **giống hệt từng byte**.
- Chạy `cham.py` lên bản chạy lại của Claude Code: 61/61 bất thường, 750/750 trạng thái, 25/25 người.

Hai điều kiện: máy phải có Python và (với bản của `agy`) thư viện `pandas`; bản của Claude Code chỉ dùng thư viện chuẩn của Python. Đây là một khác biệt thực tế khi bạn giao cho người kỹ thuật bảo trì.

### Đổi ngưỡng chỉ bằng một dòng, nếu code viết tốt

Quy định công ty đổi (ví dụ dung sai trễ từ 5 lên 10 phút) thì phải sửa ở đâu? **[Đo được]**: bản của Claude Code (cả ba lần chạy) có khối "THAM SỐ" ở đầu tệp (`DUNG_SAI = 5`, `TRUNG_PHUT = 3`, `QUET_HO_PHUT = 10`, ...). Mình sửa đúng một dòng `DUNG_SAI = 10` rồi chạy lại: số cảnh báo `DI_TRE` từ 12 xuống 10, `VE_SOM` từ 6 xuống 5, tổng bất thường từ 61 xuống 58. Ngược lại, trong bản `agy` lần 2 dung sai là số 5 viết thẳng ở nhiều dòng (dòng 358, 361, 400, 401 của `tinh_cong.py`), nên đổi ngưỡng đòi sửa nhiều chỗ và dễ sót. Mình chưa kiểm ba bản `agy` còn lại. Đây là lý do nên thêm vào prompt: "Gom mọi ngưỡng vào một khối tham số ở đầu tệp, ghi chú mục quy định tương ứng". (Mình **không** sửa prompt của hai bài trước; đây là gợi ý cho lần chạy sau.)

Lưu ý nhỏ: sau khi đổi `5` thành `10`, dòng chú thích bên cạnh vẫn ghi "<= 5 phút" nếu không sửa. Chú thích cũ là lỗi hay gặp.

## 3. Quy trình hằng tháng (8 bước)

1. **Xuất dữ liệu** từ máy chấm công hoặc phần mềm (CSV/Excel). Giữ nguyên, không mở bằng Excel rồi lưu lại (Excel hay đổi định dạng ngày).
2. **Ẩn danh** bằng `an_danh.py` (bài 1). Script tự kiểm rò rỉ và dừng nếu còn họ tên. Chỉ khi báo "Rò rỉ phát hiện: KHÔNG" mới sang bước sau.
3. **Cập nhật tệp tham số của tháng**: kỳ công (đầu tháng, cuối tháng), danh sách ngày lễ (công ty khai báo), lịch ca xoay, đơn nghỉ phép đã duyệt, danh sách nhân viên. Đây là phần **người** làm; chương trình hiện tại ghi cứng kỳ 09/2026 và hai ngày lễ, nên mỗi tháng phải sửa khối tham số.
4. **Chạy `tinh_cong.py`** (bản đã được người kỹ thuật đọc và duyệt). Không cần agent.
5. **Tự kiểm** bằng `kiem_tra_dau_ra.py` (mục 4). Chỉ đi tiếp khi tất cả mục đạt.
6. **Người duyệt** mở `bat_thuong.csv` và xử lý từng dòng, ghi quyết định (mục 5).
7. **Gắn tên lại trên máy bạn**: `python -X utf8 an_danh.py --giai-ma bat_thuong.csv bat_thuong_co_ten.csv`. Chỉ lúc này mới đưa cho quản lý trực tiếp xem.
8. **Lưu hồ sơ**: ba CSV, `tinh_cong.py` (kèm phiên bản và tham số), quyết định của người duyệt, theo chính sách lưu trữ của công ty. Khi có khiếu nại, bạn truy ra được vì sao một ngày bị tính như vậy.

Giải thích lệnh bước 7: `--giai-ma` đọc bảng mã hóa ở máy bạn, thêm cột `ho_ten` và thay mọi `NV-xxx` trong câu giải thích bằng họ tên.

## 4. Tự kiểm: bắt lỗi hình thức, không cần đáp án

Ở bài 2 mình chấm bằng đáp án, nhưng ngoài đời **không có đáp án**. Tệp `ket-qua/kiem_tra_dau_ra.py` kiểm những thứ không cần đáp án:

| Mục | Kiểm gì |
|-----|---------|
| 1 | Đủ dòng: số nhân viên x số ngày, không trùng khóa |
| 2 | Trạng thái hợp lệ; ngày OK có đủ giờ vào, ra, giờ công trong khoảng 0 đến 8 |
| 3 | Mỗi ngày CHO_XAC_NHAN có ít nhất một dòng giải thích trong danh sách bất thường |
| 4 | Mã loại hợp lệ; không trùng khóa; giải thích không trống; `can_nguoi_quyet` đúng quy ước |
| 5 | Nhất quán chéo: có phút trễ thì phải có DI_TRE và ngược lại; tương tự về sớm |
| 6 | Tổng hợp theo người khớp với tổng từ bảng ngày |
| 7 | Không có họ tên (từ bảng mã hóa) nào lọt vào đầu ra |

Chạy:

```
python -X utf8 kiem_tra_dau_ra.py ket-qua/claude-lan1 du-lieu/an-danh --ten ket-qua/bang-ma-hoa.csv
```

![Kết quả chạy bộ tự kiểm](anh/12-tu-kiem-dau-ra.webp)

*Chạy `kiem_tra_dau_ra.py` ngày 2026-11-20 trên bảy bộ đầu ra thật và một bản cố ý làm hỏng. Dữ liệu giả.*

**[Đo được]** (2026-11-20): bộ kiểm này **đạt cả 7 mục trên cả bảy bộ đầu ra**. Mình cũng thử cố ý làm hỏng một bản (xóa một dòng bảng công, sửa tổng phút trễ thành 999, xóa một câu giải thích) và nó báo đúng ba chỗ (mục 1, 4, 6).

Điều cần nhớ, **và là điều quan trọng nhất của bài**: hai bộ đầu ra ở bài 2 có khác biệt so với đáp án (ngày nghỉ trong đơn phép bị ghi PHEP; ngày làm thêm quá 3 giờ bị bỏ trống giờ công) nhưng **vẫn đạt cả 7 mục tự kiểm**, vì chúng nhất quán nội bộ. Tự kiểm bắt được lỗi hình thức và mâu thuẫn, **không bắt được cách hiểu quy định khác ý bạn**. Chỗ đó chỉ phát hiện được bằng hai cách: người đọc mục "giả định" trong `bao_cao.md`, và quy định viết đủ rõ để không còn chỗ hiểu khác.

## 5. Người duyệt: ai quyết cái gì

Chương trình không có thẩm quyền quyết lương hay kỷ luật. Gợi ý phân việc (**[Đề xuất]**, chỉnh theo công ty):

| Loại bất thường | Ai xem | Câu hỏi cần trả lời |
|-----------------|--------|---------------------|
| THIEU_RA, THIEU_VAO, THIEU_KHONG_RO | Quản lý trực tiếp | Giờ vào/ ra thực tế là mấy giờ, có nhân chứng/ lịch làm việc không |
| VANG_CHUA_GHI | Quản lý trực tiếp, nhân sự | Nghỉ có phép chưa ghi, hay vắng không phép |
| CO_PHEP_NHUNG_QUET | Nhân sự | Đơn nghỉ còn hiệu lực không, người đó có đi làm không |
| LAM_NGAY_LE, LAM_NGAY_NGHI, OT_VUOT_NGUONG, OT_THANG_VUOT | Quản lý và nhân sự | Có được giao làm không; cách tính lương làm thêm: **cần kiểm với văn bản hiện hành hoặc chuyên gia nhân sự** |
| NGHI_QUET_HO | Quản lý chi nhánh, nhân sự | Chỉ là dấu hiệu từ dữ liệu; xác minh theo quy trình của công ty, **không kết luận từ bảng này** |
| DU_LIEU_LOI | Người kỹ thuật | Thẻ không có trong danh sách (nhân viên mới chưa nhập?), giờ máy lỗi |
| QUET_TRUNG, DI_TRE, VE_SOM | Nhân sự (xem lướt) | Đã tính tự động theo quy định; xem có ngoại lệ miễn trừ không |

Mỗi quyết định ghi lại: ai, ngày, quyết gì, vì sao. Một cột `quyet_dinh` trong bản sao của `bat_thuong.csv` là đủ.

Một ca cần chú ý riêng: ngày `CHO_XAC_NHAN` **chưa được tính giờ**. Người làm lương không được lấy bảng công ngày đưa thẳng vào tính lương khi còn ngày chờ. Đây không phải vấn đề kỹ thuật mà là quy trình: tên cột `so_ngay_cho_xac_nhan` trong `tong_hop_nguoi.csv` phải bằng 0 trước khi chốt.

## 6. Khi nào dùng mô hình cho phần giải thích

Nếu bạn muốn lời giải thích tự nhiên hơn các câu mẫu cho **ca ngoại lệ lạ** (ví dụ chuỗi quẹt rất bất thường), có thể gọi mô hình chỉ trên dòng bất thường đã ẩn danh. Một prompt ngắn đủ dùng:

```
Dưới đây là một dòng bất thường đã được chương trình phát hiện (mã NV ẩn danh, số liệu do chương trình tính).
Viết 1-2 câu tiếng Việt cho quản lý: chuyện gì xảy ra và nên hỏi/ kiểm gì.
Không đoán nguyên nhân, không kết luận gian lận, không nêu điều luật, không thêm số liệu ngoài dòng này.
```

Quy tắc: mô hình **không được tính lại số liệu**, chỉ diễn đạt số đã có; và vẫn chỉ nhận bản ẩn danh.

## 7. Giới hạn của cách làm này (nói thẳng)

- **Kết quả đẹp vì dữ liệu giả và quy định rõ.** Bảy lần chạy đều 61/61 bất thường, 0 báo oan; điều đó không bảo đảm gì với dữ liệu thật của bạn, nơi lỗi lạ hơn, quy định mơ hồ hơn và đáp án không có sẵn.
- **Các lỗi chưa cài:** ca qua đêm (quẹt vào 22:00, ra 06:00 hôm sau), giờ máy chấm bị lệch, nhân viên đổi mã thẻ giữa tháng, hai người dùng chung một thẻ, nghỉ nửa ngày, đi công tác, làm việc từ xa, ngày lễ rơi vào cuối tuần và nghỉ bù. Với các tình huống này chương trình hiện tại **chưa được thử**.
- **Kỳ và ngày lễ ghi cứng** trong chương trình; mình chưa chạy thử tháng khác.
- **n nhỏ:** hai agent, mỗi cấu hình 1 đến 2 lần; chưa đo được độ ổn định giữa các lần chạy; không kết luận agent nào tốt hơn.
- **Ẩn danh bằng mã không phải ẩn danh tuyệt đối:** lịch làm việc đặc thù vẫn có thể lộ danh tính; việc đưa dữ liệu nhân sự ra dịch vụ bên ngoài cần xem quy định nội bộ và pháp lý.
- **Agent có toàn quyền trên máy** khi chạy với `--dangerously-skip-permissions` (bài 2: một lần `agy` chạy lệnh ngoài thư mục làm việc dù prompt dặn không). Chạy trong thư mục/ tài khoản riêng.

## 8. Mở rộng (đề xuất, chưa thử)

- Xuất bảng công ra Excel có định dạng (tô màu ngày chờ xác nhận) bằng một bước sau `tinh_cong.py`. **[Đề xuất]**
- Thêm bộ test cố định: giữ lại bộ dữ liệu giả và đáp án của bài, mỗi lần đổi `tinh_cong.py` thì chạy lại `cham.py`; nếu số đúng giảm là có hồi quy. **[Đề xuất]** (bộ này đã có trong thư mục bài).
- Hỏi lại agent về các ca ngoài danh sách bẫy: cho nó thêm dữ liệu ca qua đêm và xem nó phản ứng thế nào, rồi **viết thêm bẫy vào đáp án** để lần sau chấm được. **[Đề xuất]**
- Nối với phần mềm tính lương: chỉ khi `so_ngay_cho_xac_nhan` bằng 0 và người duyệt đã ký. **[Đề xuất]**

## Lỗi thường gặp

- **Tưởng agent là "người tính lương".** Nó là công cụ chuẩn bị số liệu; ký duyệt là việc của người.
- **Quên cập nhật kỳ/ ngày lễ** khi chạy tháng sau, ra bảng công toàn ngày nghỉ.
- **Chấp nhận chương trình mà không đọc câu giải thích nhúng sẵn** (mục 1).
- **Đưa bảng đã gắn tên vào hộp thư chung.** Bảng có tên chỉ ở máy người có quyền.
- **Chỉ chạy tự kiểm rồi tin hết:** tự kiểm đạt không có nghĩa là cách hiểu quy định đúng ý (mục 4).

## Checklist hằng tháng

- [ ] Bản ẩn danh báo "Rò rỉ phát hiện: KHÔNG".
- [ ] Đã cập nhật kỳ công, ngày lễ, lịch ca, đơn nghỉ phép trong tháng.
- [ ] `tinh_cong.py` là bản đã duyệt, chạy không lỗi.
- [ ] `kiem_tra_dau_ra.py` đạt cả 7 mục.
- [ ] Đã đọc mục "giả định" và "điều chưa chắc" trong `bao_cao.md`.
- [ ] Mọi dòng `can_nguoi_quyet = CO` có quyết định của người, `so_ngay_cho_xac_nhan` bằng 0.
- [ ] Bản có họ tên chỉ nằm ở nơi được phép; hồ sơ tháng đã lưu.

## Việc cần người làm

- Người kỹ thuật (hoặc đối tác): đọc và duyệt `tinh_cong.py` một lần; giữ khối tham số; chạy thử với dữ liệu tháng cũ đã biết kết quả.
- Nhân sự: giữ danh sách nhân viên, đơn nghỉ phép, lịch ca; quyết các dòng bất thường; kiểm quy định pháp luật về giờ làm thêm, ngày lễ, nghỉ phép với văn bản hiện hành hoặc chuyên gia nhân sự.
- Chủ doanh nghiệp: ký duyệt trước khi chốt lương; quyết chính sách đưa dữ liệu nhân sự (dù đã ẩn danh) lên dịch vụ đám mây.

## Giới hạn

Xem mục 7. Tóm lại: bài chỉ chứng minh rằng với dữ liệu giả, quy định rõ và người duyệt, quy trình này chạy được và lặp lại được; chưa chứng minh gì về dữ liệu thật.
