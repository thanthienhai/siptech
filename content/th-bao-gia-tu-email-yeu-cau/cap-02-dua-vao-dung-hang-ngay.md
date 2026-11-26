# Bài 3. Đưa vào dùng hằng ngày

!!! info "Bài này"
    - **Bạn làm gì:** dựng quy trình lặp lại mỗi ngày: yêu cầu mới vào một thư mục, báo giá nháp ra thư mục khác, chương trình tự kiểm chạy trước, người duyệt mở hàng đợi theo thứ tự ưu tiên.
    - **Mất bao lâu:** khoảng 30 phút để dựng lần đầu; mỗi ngày sau đó vài phút cho phần máy, còn lại là thời gian người duyệt đọc.
    - **Cần có:** kết quả bài 2, Python 3 với `openpyxl`, một người duyệt có quyền quyết giá.
    - **Kết quả:** quy trình trong đó **không có gì tự gửi đi**, một bộ tự kiểm `kiem-tra-bao-gia.py` chạy được không cần đáp án, và một danh sách ngắn việc người duyệt phải nhìn kỹ.

> **Dữ liệu giả để học.** Số **[Đo được]** là từ các lần chạy ngày 2026-11-20 (n = 1 đến 2 lần mỗi agent hợp lệ). Mọi chính sách trong bài là chính sách bịa của công ty giả An Phát Demo.

!!! warning "Quy tắc an toàn"
    - **Agent soạn nháp, người duyệt và bấm gửi.** Không nối agent vào hộp thư để tự gửi.
    - **Dữ liệu khách hàng thật** (tên, số điện thoại, địa chỉ trong email và Zalo): chạy trên dịch vụ đám mây nghĩa là nội dung đó được gửi tới nhà cung cấp. **[Đề xuất]** Đọc điều khoản và cấu hình quyền riêng tư của gói bạn dùng, cân nhắc ẩn danh trước khi đưa vào, và hỏi người phụ trách bảo vệ dữ liệu hoặc luật sư nếu có khách yêu cầu bảo mật. Chúng tôi không đưa kết luận pháp lý.
    - **Đáp án và bộ chấm để ngoài tầm với của agent** (bài 1, Bước 4; bài 2, Bước 6). Hằng ngày bạn không có đáp án, nhưng bộ chấm mẫu 12 yêu cầu vẫn không được nằm cạnh thư mục chạy.
    - **VAT là tham số, hỏi kế toán.** Kế toán điền mức VAT vào sheet "Tham số" và quyết cách tính thuế cho dòng phí giao hàng. Con số 10 trong bài chỉ là minh họa.

## Quy trình mỗi ngày

```
sáng:   chép email/Zalo mới vào  yeu-cau/  (mỗi yêu cầu một file Rxx.txt)
        cập nhật bang-gia.xlsx và tham số VAT (nếu có đổi) -> chạy agent -> dau-ra/
        chạy kiem-tra-bao-gia.py trên dau-ra/
        người duyệt mở hàng đợi: CAN_NGUOI_QUYET, THIEU_THONG_TIN, rồi SAN_SANG
chiều:  người duyệt sửa, gửi từng cái (ngoài hệ thống này), ghi lại kết quả
```

Nguyên tắc: **agent đọc hiểu, code tính tiền, người quyết.**

| Việc | Ai làm | Vì sao |
|---|---|---|
| Hiểu email lộn xộn, tách dòng hàng, đổi đơn vị | Agent | Ngôn ngữ tự nhiên, việc agent giỏi |
| Tra bậc giá, chiết khấu, phí giao, VAT, tổng | **Code** (`tinh_bao_gia.py`) | Phải lặp lại y hệt; 35/35 dòng hàng đúng trong mọi lần chạy hợp lệ **[Đo được]** |
| Kiểm số học và quy tắc, không cần đáp án | Code (`kiem-tra-bao-gia.py`) | Bắt lỗi nhất quán |
| Quyết chiết khấu vượt mức, quà tặng, công nợ, giữ giá cũ, phí giao ngoại tỉnh, hàng không có | **Người** | Không phải việc của nhân viên, càng không phải của máy |
| Duyệt cuối, bấm gửi | **Người** | Người chịu trách nhiệm trước khách |

### Bước 1. Tách việc "đọc hiểu" khỏi việc "tính tiền"

Ở bài 2, mỗi script `tinh_bao_gia.py` do agent viết có **12 yêu cầu gõ cứng trong một biến `YEU_CAU`** (ví dụ `ket-qua/claude-2/tinh_bao_gia.py`, từ dòng 232). Phần tính tiền và điền mẫu dùng lại được; phần dữ liệu yêu cầu chỉ đúng cho 12 yêu cầu này. Muốn dùng hằng ngày, tách làm hai:

1. Agent đọc yêu cầu mới và ghi một file nhỏ cho mỗi yêu cầu, ví dụ `cau-truc/R13.json`:

```json
{
  "id": "R13",
  "khach": "tên người/đơn vị",
  "dia_chi": "địa chỉ giao hoặc null nếu chưa biết",
  "dong": [{"ma": "GIAY-A4-80", "so_luong": 25, "dvt": "ram"}],
  "xin_giam_pct": 2,
  "van_de": ["đòi giao trước 10h sáng thứ Sáu"]
}
```

2. Một script cố định (người đã xem và duyệt) đọc `cau-truc/*.json`, tính tiền, điền mẫu. Script **không đổi** mỗi ngày, chỉ dữ liệu đổi. Mỗi khi chính sách đổi, bạn sửa script một lần, chạy lại trên 12 yêu cầu mẫu và so với kết quả cũ.

Người duyệt còn mở được file JSON để xem agent đọc hiểu yêu cầu thế nào trước khi nhìn tới số tiền. Prompt cho phần (1), **chưa chạy thử**:

```prompt
Trong thư mục hiện tại có yeu-cau/ (các email và tin nhắn khách mới), bang-gia.xlsx (có sheet QuyDoi) và dieu-kien-giao-hang.txt. Với MỖI yêu cầu Rxx, đọc rồi ghi cau-truc/Rxx.json gồm: id, khach, dia_chi (null nếu khách chưa nói), dong (mỗi dòng: ma theo bang-gia.xlsx, so_luong theo đơn vị khách ghi, dvt theo đơn vị khách ghi), xin_giam_pct (0 nếu không xin), van_de (danh sách việc khách đòi mà nhân viên không được tự quyết hoặc hứa). Quy tắc: chỉ ghi mã có trong bảng giá; mã sai hoặc hàng không có thì ghi vào van_de, không tự đoán mã; không đổi đơn vị, không tính tiền. Chỉ đọc và ghi trong thư mục hiện tại.
```

!!! see "Bạn sẽ thấy"
    Một thư mục `cau-truc/` có mỗi yêu cầu một file JSON ngắn, đọc được bằng mắt. Chưa có số tiền nào ở bước này.

### Bước 2. Tự kiểm bằng code, không cần đáp án

Hằng ngày bạn không có `dap-an.json`. Dùng `ket-qua/kiem-tra-bao-gia.py`. Tham số thứ nhất là thư mục chứa `Rxx-bao-gia.xlsx`, `Rxx-email.txt`, `Rxx-cau-hoi.txt`; tham số thứ hai là thư mục có `bang-gia.xlsx` và `mau-bao-gia.xlsx` (lấy mức VAT từ sheet "Tham số"):

```lenh
python -X utf8 ket-qua/kiem-tra-bao-gia.py ket-qua/claude-2/dau-ra du-lieu
```

Chương trình phân biệt **LỖI** (số học, mã không có trong bảng giá, đơn giá sai bậc, VAT khác tham số, chiết khấu quá mức, trạng thái trống) và **CẢNH BÁO** (phí giao ghi 0 khi chưa biết địa chỉ, email nói "đã chuyển", email thiếu chữ "kế toán", câu giống lời hứa giao hàng, dòng không có giá). **[Đo được]** Đầu ra thật:

```ketqua
R01 OK
R02 OK
...
R12 OK
Tổng: 0 lỗi, 0 cảnh báo
```

(Chúng tôi lược R03 đến R11.) Kết quả chạy trên 6 thư mục đầu ra **[Đo được]**:

| Lần chạy | Lỗi | Cảnh báo | Cảnh báo là gì |
|---|---|---|---|
| claude-1 | 0 | 6 | 6 email viết "đã chuyển ..." |
| claude-2 | 0 | 0 | |
| claude-0 | 0 | 0 | |
| agy-2 | 0 | 8 | 8 email viết "đã chuyển ..." |
| agy-0 | 0 | 12 | email "đã chuyển", 4 dòng không giá (ghi chú), 1 cờ giả hứa giờ giao ở R08 (một tiêu đề), phí giao ghi 0 ở R02 |
| agy-1 (bị loại) | 0 | 5 | |

!!! warning "Giới hạn của bộ tự kiểm"
    Nó **không bắt** được lỗi của agy-0 ở R10 (bỏ phần chiết khấu thêm 2% được phép): báo giá đó đúng số học và không vượt 5%, chỉ **thiếu** một khoản chính sách cho phép. Tự kiểm chỉ chứng minh "nhất quán", không chứng minh "đúng chính sách". Vì vậy bản gốc của chúng tôi còn `cham.py` (cần đáp án) để đo định kỳ trên 12 yêu cầu mẫu mỗi khi đổi prompt, đổi agent hay đổi phiên bản.

### Bước 3. Người duyệt đọc gì trước

Sắp hàng đợi theo ô "Trạng thái" trong mỗi báo giá:

1. **CAN_NGUOI_QUYET:** đọc ghi chú ở dòng chiết khấu, phí giao và mục "Nội dung đang chờ" trong email. Quyết rồi mới tiếp.
2. **THIEU_THONG_TIN:** đọc `Rxx-cau-hoi.txt`, gửi câu hỏi cho khách; báo giá nháp chỉ có phần đã chắc.
3. **SAN_SANG:** vẫn nhìn dòng chiết khấu, dòng phí giao và câu VAT.

![Báo giá R10 do claude-2 lập: ghi chú giải thích quy đổi và chiết khấu ngay trong file.](anh/05-claude-bao-gia-R10.webp)

*Kết quả thật, dựng lại từ `ket-qua/claude-2/dau-ra/R10-bao-gia.xlsx`. Dữ liệu giả để học.*

Checklist cho người duyệt mỗi báo giá (nên in dán cạnh máy):

- [ ] Số lượng và đơn vị khớp ý khách (2 thùng = bao nhiêu)?
- [ ] Đơn giá đúng bậc? Dòng sát mốc bậc (49/50) có đúng?
- [ ] **Dòng chiết khấu:** đúng %, đúng nhóm hàng? Có khoản được phép mà bị bỏ không (như agy-0 ở R10)?
- [ ] Phí giao: nội thành hay ngoại tỉnh? Chưa rõ thì ghi "theo thỏa thuận", không ghi 0.
- [ ] Mức VAT khớp tham số kế toán đã xác nhận?
- [ ] Email có câu "đã chuyển ..." mà chưa ai chuyển? Có câu nào giống lời hứa ngày giờ giao?
- [ ] Câu hỏi làm rõ đủ, không hỏi lặp, không quá nhiều?
- [ ] Việc cần người quyết đã có người nhận chưa?

### Bước 4. Khi chính sách hoặc bảng giá đổi

Sửa script một lần, chạy lại 12 yêu cầu mẫu, so với kết quả cũ để thấy đúng những yêu cầu bị ảnh hưởng. Prompt nhờ agent sửa và liệt kê tác động có ở bài 4 (mục "Đổi bảng giá hoặc chiết khấu"), **chưa chạy thử**.

### Bước 5. Giữ log và bằng chứng

Mỗi lần chạy giữ lại: (a) log gốc `*.raw.jsonl`, (b) thư mục `dau-ra/`, (c) bản `tinh_bao_gia.py` đã dùng, (d) phiên bản bảng giá và tham số VAT, (e) tên người duyệt và quyết định. Khi khách hoặc kế toán hỏi "vì sao giá này", bạn có thứ để trả lời. Tìm trong log các tên file lạ là cách kiểm nhanh agent có ra ngoài thư mục (bài 2, Bước 6).

## Đào sâu: chi phí, thời gian và việc chưa làm

**[Đo được]** Với lô 12 yêu cầu, Claude Code báo chi phí theo giá niêm yết 1,04 USD (claude-1) và 1,19 USD (claude-2), mất 378 s và 432 s. Antigravity (agy-2) mất 962,5 s, log không báo chi phí (173.743 token vào, 110.581 token ra). Chia ra khoảng 0,09 đến 0,10 USD cho một yêu cầu theo giá niêm yết của Claude Code. Đây là hai điểm đo, máy lúc đó chạy nhiều việc song song, gói thuê bao của bạn có thể tính khác. **[Đề xuất]** Đo lại trên máy và gói của bạn trước khi hứa với ai về chi phí. So với thời gian nhân viên lập 12 báo giá bằng tay, bạn tự đo bằng cách bấm giờ một buổi: chúng tôi **không có số này**.

Chưa làm trong bài này:

- **Mẫu DOCX/PDF:** điền vào `.docx` bằng thư viện `python-docx`, chúng tôi chưa thử nên không có số liệu.
- **Ảnh và PDF đính kèm:** cần đọc chữ trong ảnh (OCR); độ chính xác phải đo riêng.
- **Bảng giá lớn:** cần tìm kiếm theo mã hoặc tên thay vì đưa cả bảng vào prompt.
- **Nối với email, Zalo, phần mềm kế toán:** làm khi quy trình ở thư mục đã ổn và có người chịu trách nhiệm; khâu gửi vẫn nên do người bấm.
- **Chạy lặp để đo độ ổn định:** muốn nói gì về độ ổn định cần chạy mỗi cấu hình ít nhất vài chục lần.
- **Lấy câu hỏi từ khách hàng thật** (có đồng ý) để mở rộng bộ 12 yêu cầu.

## Lỗi thường gặp khi dùng thật

| Tình huống | Gặp ở đâu trong bài này | Cách đối phó |
|---|---|---|
| Agent hiểu sai chính sách rồi tính "đúng" theo hiểu sai | agy-0 R10: bỏ 2% chiết khấu thêm | Người duyệt đọc dòng chiết khấu; chạy `cham.py` trên 12 yêu cầu mẫu mỗi khi đổi prompt hay agent |
| Email nói việc chưa xảy ra ("đã chuyển lên trưởng phòng") | 6/12, 8/12, 6/12 email ở claude-1, agy-2, agy-0 | Người duyệt sửa; **[Đề xuất]** sửa prompt thành "sẽ chuyển" |
| Chính sách mơ hồ, agent hiểu khác nhau | R02 ("chiều anh cần" = giao gấp?), R09 ("như đợt trước" = giữ giá cũ?) | Chủ doanh nghiệp quyết một cách hiểu và viết vào chính sách |
| Agent đi ra ngoài thư mục, đọc file không được đọc | agy-1 đọc đáp án | Chạy ở thư mục hoặc tài khoản cô lập; kiểm log |
| Bảng giá đổi mà quên cập nhật | không xảy ra trong bài, nhưng là rủi ro số một | Ghi ngày hiệu lực bảng giá ở mỗi báo giá (mẫu đã có "Ngày báo giá"), bắt buộc cập nhật trước khi chạy |
| Tiến trình chạy nền bị dừng mất log | claude-0, agy-0 | Dùng `Start-Process` và đặt thời gian tối đa dư (1500 giây) |
| Khách gửi ảnh chụp, PDF, báo giá đối thủ | không có trong bài | Bài này chỉ xử lý văn bản |

## Checklist cuối bài 3

- [ ] Có thư mục `yeu-cau/` (vào) tách khỏi `dau-ra/` (ra), không có gì tự gửi.
- [ ] `kiem-tra-bao-gia.py` chạy được trên `dau-ra/` và bạn hiểu từng cảnh báo.
- [ ] Người duyệt có checklist 8 mục ở Bước 3 và biết thứ tự đọc hàng đợi.
- [ ] Kế toán đã xác nhận mức VAT trong sheet "Tham số".
- [ ] Log và bản script của mỗi lần chạy được giữ lại.

## Việc cần người làm

- Chủ doanh nghiệp: viết chính sách giá, chiết khấu, thẩm quyền, giao hàng thành văn bản rõ; quyết những chỗ mơ hồ.
- Người duyệt: dùng checklist cho từng báo giá và chịu trách nhiệm trước khi gửi.
- Kế toán: xác nhận mức VAT trong "Tham số", cách tính thuế cho phí giao hàng, mẫu hóa đơn.
- Người quản trị máy: cô lập thư mục hoặc tài khoản chạy agent, giữ log, đặt quyền truy cập.

## Giới hạn

- Dữ liệu và chính sách giả; 12 yêu cầu; n = 1 đến 2 lần mỗi agent hợp lệ; không xếp hạng agent.
- Bộ tự kiểm không bắt được lỗi hiểu sai chính sách. Người duyệt không thể bỏ.
- Chi phí và thời gian chỉ là vài điểm đo trong một ngày, máy đang bận.
- Chưa thử mẫu DOCX/PDF, ảnh đính kèm, bảng giá lớn, dữ liệu khách hàng thật.
- Không phải tư vấn thuế hay pháp luật: mức VAT, hóa đơn, bảo vệ dữ liệu cần kế toán hoặc luật sư xác nhận.
