# Bài 3. Đưa vào dùng hằng ngày: lặp lại, tự kiểm, người duyệt

!!! info "Bài này"
    - **Bạn làm gì:** biến script agent đã viết thành quy trình hàng tháng: chạy script, tự kiểm bằng code, người duyệt, lưu hồ sơ. Và kiểm trước xem script có dùng lại được cho tháng sau không.
    - **Mất bao lâu:** khoảng 30 phút để dựng lần đầu. Mỗi tháng sau đó: chạy vài giây, duyệt khoảng 5 phút rồi xử từng ngoại lệ.
    - **Cần có:** Python 3, `openpyxl`, thư mục bài toán có `du-lieu/` và `ket-qua/` (script mẫu `ket-qua/claude-1/doi_soat.py`). Không cần mở agent cho các bước hằng tháng.
    - **Kết quả:** một thư mục theo tháng có đầu vào, đầu ra và quyết định của người duyệt; một checklist duyệt gọn.

> Dữ liệu là **dữ liệu giả để học**. Số liệu **[Đo được]** là kết quả ngày 2026-11-20 và 2026-11-21 trên bộ dữ liệu của bài 1 và hai bộ khác sinh bằng hạt giống khác (n nhỏ, xem từng mục). **[Đề xuất]** là ý kiến, chưa kiểm ở doanh nghiệp thật.

## Hai cách dùng agent hằng tháng

Ở bài 2, mỗi agent viết một script `doi_soat.py` rồi chạy. Câu hỏi hằng ngày không phải "agent làm được không" mà là: **tháng sau chúng ta làm gì?**

- **Cách 1: mỗi tháng gọi lại agent từ đầu.** Linh hơn, nhưng tốn thời gian và tiền mỗi lần, và kết quả dao động giữa các lần (bài 2, mục Đào sâu).
- **Cách 2: giữ script đã kiểm, mỗi tháng chỉ chạy script, chỉ gọi agent khi dữ liệu đổi dạng.** Rẻ và lặp lại được, nhưng chỉ đúng nếu script **thật sự tổng quát**. Bài 2 đã báo trước: một trong hai script viết cứng các ca cụ thể.

Bài này theo cách 2. Phần "Trước khi tin script" ở dưới đo xem điều đó nguy hiểm đến đâu.

## Quy trình mỗi tháng

Để luyện, chúng ta dùng một "tháng khác" do bộ sinh dữ liệu dựng (hạt giống 20261201). Dùng sao kê thật thì thay hai file dữ liệu bằng file của bạn, giữ nguyên tên file hoặc nhờ agent sửa tên trong script.

### Bước 1. Đặt dữ liệu tháng và script vào một thư mục riêng (người)

Windows PowerShell, chạy từ thư mục bài toán:

```lenh
cd du-lieu
python -X utf8 bai_tap.py thang-khac
cd ..\bai-tap\thang-khac-20261201
mkdir 2026-11
copy du-lieu\* 2026-11\
copy ..\..\ket-qua\claude-1\doi_soat.py 2026-11\
```

`bai_tap.py thang-khac` dựng dữ liệu mới vào `bai-tap/thang-khac-20261201/`. Hai lệnh `copy` đặt sao kê, sổ đơn và script vào thư mục tháng `2026-11`.

```ketqua
Đã dựng ../bai-tap/thang-khac-20261201
  144 dòng sao kê, 128 đơn, hạt giống 20261201
  tổng có 102,688,650  tổng nợ 70,234,000  dư cuối 72,454,650
  đơn CK chưa thu: 10
```

### Bước 2. Chạy script (máy)

```lenh
cd 2026-11
python -X utf8 doi_soat.py
```

`python` chạy Python, `-X utf8` để Windows in tiếng Việt không lỗi, `doi_soat.py` là script.

```ketqua
so_dong 144 | kiem_so_du_khop True | lech so du chay: []
loi so don: []
muc: {'CAO': 65, 'TRUNG BINH': 70, 'CAN NGUOI QUYET': 9}
loai: {'khop_du': 68, 'thieu': 4, 'thua': 4, 'trung': 3, 'nhieu_don': 6, 'hoan_tien': 3, 'cod_gop': 2, 'phi_lai_ngan_hang': 4, 'chi_khac': 41, 'khong_ro_nguon': 9}
tong_co_theo_loai: {'khop_du': 56400000, 'thieu': 1320000, 'thua': 2600000, 'trung': 6600000, 'nhieu_don': 13130000, 'hoan_tien': 0, 'cod_gop': 8430000, 'phi_lai_ngan_hang': 18650, 'chi_khac': 0, 'khong_ro_nguon': 14190000}
da ghep: 80050000 chua ghep/CNQ: 22638650
don chua thu: ['DH2610-036', 'DH2610-065', 'DH2610-069', 'DH2610-079', 'DH2610-101', 'DH2610-121', 'DH2610-122', 'DH2610-123', 'DH2610-124', 'DH2610-125', 'DH2610-126', 'DH2610-127', 'DH2610-128']
ngoai le: 40
```

!!! see "Bạn sẽ thấy"
    Vài dòng tóm tắt, và thư mục có thêm `bang_ghep.csv`, `ngoai_le.csv`, `tong_kiem.json`, `bao_cao.md`. Không cần mở agent.

### Bước 3. Đọc tổng kiểm, dừng nếu sai (máy rồi người)

Mở `tong_kiem.json`. Nếu `kiem_so_du_khop` là `false`, **dừng**: sao kê đọc sai hoặc file thiếu dòng.

```lenh
Get-Content tong_kiem.json -Encoding UTF8 | Select-Object -First 7
```

macOS hoặc Linux: `head -7 tong_kiem.json`.

```ketqua
{
  "so_dong": 144,
  "so_du_dau": 40000000,
  "tong_ghi_co": 102688650,
  "tong_ghi_no": 70234000,
  "so_du_cuoi": 72454650,
  "kiem_so_du_khop": true,
```

### Bước 4. Tự kiểm bằng code, không dựa vào lời script (máy)

Script nói "đã khớp" chưa phải bằng chứng. `kiem_nhanh.py` (có sẵn trong `du-lieu/`) **tự cộng lại từ sao kê gốc** và kiểm ba điều: tổng khớp `tong_kiem.json`; `bang_ghep.csv` có đủ số CT, không trùng, cộng tiền đúng; không đơn nào ghép chắc chắn vào hai dòng `khop_du`.

```lenh
python -X utf8 ..\..\..\du-lieu\kiem_nhanh.py sao-ke-t10-2026.csv .
```

Đối số thứ nhất là sao kê gốc, thứ hai là thư mục có kết quả (`.` là thư mục hiện tại).

```ketqua
Tự cộng từ sao kê: 144 dòng, tổng có 102,688,650, tổng nợ 70,234,000, số dư cuối 72,454,650
bang_ghep.csv: 144 dòng
  cộng lại: có 102,688,650, nợ 70,234,000
  đơn nằm ở hơn một dòng khop_du: 0

KẾT QUẢ: ĐẠT (không có lỗi cộng trừ hay ghép trùng)
```

!!! stuck "Kiểm nhanh báo LỖI?"
    Đọc từng dòng `LỖI:`. "Thiếu số CT" hoặc "cộng ra khác": bảng bị mất hoặc nhân đôi dòng, chạy lại và xem script. "Đơn nằm ở hai dòng `khop_du`": xem hai dòng đó, có thể một dòng đúng ra là `trung` hoặc `thieu`. Dừng, chưa duyệt.

### Bước 5. Duyệt theo checklist (người)

Đọc theo thứ tự, khoảng 5 phút:

1. **`tong_kiem.json` và kết quả `kiem_nhanh.py`:** đều đạt. Số dòng bằng số dòng bạn đếm trong Excel.
2. **`ngoai_le.csv`:** xử từng dòng. Mỗi ngoại lệ có đề xuất, nhưng quyết định là của bạn.
3. **Mọi dòng `CAN NGUOI QUYET`:** người quyết, ghi lại lý do.
4. **Lấy mẫu dòng `CAO`:** mở ngẫu nhiên khoảng 10 dòng `CAO` trong `bang_ghep.csv`, đối chiếu tay với sao kê và sổ đơn. Sai một dòng nghĩa là `CAO` không đáng tin: dừng, xem lại script. **[Đề xuất]** con số 10 chỉ là ví dụ; shop tự chọn theo rủi ro.
5. **Đọc `ly_do` của dòng `TRUNG BINH`:** hầu hết ca đoán theo tên hoặc theo thứ tự ngày nằm ở đây.
6. **COD gộp, khách trùng tên, trả hai đơn không mã:** luôn đối chiếu thêm nguồn ngoài (bảng kê hãng vận chuyển, hỏi khách). **[Đề xuất]** viết thành quy ước: loại này luôn `CAN NGUOI QUYET`, không cho `CAO` (prompt ở dưới).
7. **Đơn chưa thu:** tách đơn đã giao lâu (cần đòi) và đơn mới đặt (chờ). Đừng nhắn khách đơn đã hủy.

### Bước 6. Xử lý ngoại lệ và lưu hồ sơ (người)

Hỏi khách, hoàn tiền, ghi sổ. Ghi lại quyết định (ai quyết, ngày nào, vì sao). Lưu **cả thư mục tháng** (đầu vào, đầu ra, quyết định) để sau này truy lại.

**[Đề xuất]** chạy hằng tuần thay vì cuối tháng: chuyển thiếu, chuyển hai lần xử lý sớm dễ hơn khi khách đã quên.

!!! warning "Quy tắc an toàn"
    - **Dữ liệu thật** (tên khách, số tài khoản) chỉ để trong thư mục tháng trên máy bạn. Đừng dán lên dịch vụ web hay thư mục chung khi chưa được phép. Xem [An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md); bài này không viết điều khoản.
    - **Đáp án** (nếu bạn có, như ở bài tập) để ngoài thư mục agent làm việc.
    - **Không** dùng cách 2 khi chưa chạy "Trước khi tin script" ở dưới.
    - Xóa file tạm sau khi xong; đừng để thư mục chạy chứa sao kê thật trên ổ chung.

## Trước khi tin script: kiểm tái lập

Chạy script của agent trên một bộ dữ liệu khác từ cùng bộ sinh (đổi hạt giống), **không gọi agent lại**, rồi chấm. Bộ mới có cùng loại bẫy, cùng cột, cùng tiền tố `DH2610`, chỉ khác tên khách, số tiền, ngày, số CT và ca nào là ca nào. Đây là phép thử "script có viết cứng không", không phải thử trên tháng thật.

Lệnh dựng bộ mới và chấm (thư mục `thang-khac-20261201` đã dựng ở Bước 1; mỗi agent một thư mục chạy):

```lenh
cd ..
mkdir chay-agy
copy du-lieu\* chay-agy\
copy ..\..\ket-qua\agy-2\doi_soat.py chay-agy\
cd chay-agy
python -X utf8 doi_soat.py
cd ..\ket-qua
python -X utf8 cham.py agy=..\chay-agy
```

Lệnh `cd ..` đưa bạn từ `2026-11` về `bai-tap/thang-khac-20261201`. Thư mục `ket-qua/` ở đó do `bai_tap.py` dựng sẵn: có `cham.py` và đáp án của bộ mới.

### Kết quả **[Đo được]** (mỗi script chạy 1 lần trên mỗi bộ mới)

| Chỉ số | Claude Code, bộ 20261121 | `agy`, bộ 20261121 | Claude Code, bộ 20261201 | `agy`, bộ 20261201 |
|---|---|---|---|---|
| Dòng xác định ghép đúng | 130/130 | **97/130** | 130/130 | **100/130** |
| Dòng mơ hồ báo cho người quyết | 13/14 | 9/14 | 13/14 | 9/14 |
| Dòng mơ hồ ghép sai không báo | 0 | **5** | 0 | **5** |
| Ngoại lệ thật bắt được | 25/26 | **9/26** | 25/26 | **9/26** |
| Báo ngoại lệ thừa | 5 | 14 | 1 | 11 |
| Đơn chưa thu: đủ 10 / liệt kê thừa | đủ, thừa 5 | đủ, thừa 30 | đủ, thừa 3 | đủ, thừa 27 |
| Tổng kiểm (6 số) đúng | 6/6 | 6/6 | 6/6 | 6/6 |
| `kiem_nhanh.py` | chưa chạy | chưa chạy | đạt | 6 đơn ở hai dòng `khop_du` |

Cách đọc:

- Script của Claude Code cho kết quả gần như lần đầu trên cả hai bộ mới. Nó là bộ quy tắc, không phải bộ nhớ. **[Đo được]** chạy lại trên dữ liệu gốc cho file giống hệt lần đầu (so từng byte).
- Script của `agy` viết cứng theo số CT và mã đơn của bộ cũ. Trên bộ mới nó gán sai loại cho ca chuyển thiếu, thừa, trùng (ghi `khop_du`, mức `CAO`), gán hai đợt COD với tập đơn cũ và đẩy các dòng đáng ra ghép được sang "không rõ nguồn". Đáng nói nhất: **5 dòng ghi sai mà mức `CAO`, không báo người**, đúng loại lỗi nguy hiểm nhất ("sai mà tự tin").
- **Tổng kiểm vẫn 6/6 ở cả hai.** Tổng kiểm chỉ cộng tiền và so số dư, nó không biết ghép đúng hay sai. **Tổng kiểm đúng không chứng minh bảng ghép đúng.** Đây là bài học lớn nhất của bài này.
- `kiem_nhanh.py` bắt được dấu hiệu của script hỏng (6 đơn bị ghép vào hai dòng) mà tổng kiểm bỏ qua, nhưng chúng tôi chưa kiểm 6 đơn đó có trùng với 5 dòng sai mức `CAO` hay không. Nó **không thay** việc lấy mẫu dòng `CAO` ở Bước 5.
- Đây là hai bộ dữ liệu mới. Chúng nói "script này viết cứng, script kia thì không", không nói "agent nào tốt hơn".

![Ca hai agent xử lý khác nhau ở bài 2](anh/10-ca-khac-nhau.webp)

*Nhắc lại ảnh từ bài 2: dòng nào để người quyết, dòng nào tự tin. Dựng từ `ket-qua/claude-1`, `ket-qua/agy-2` và đáp án; dữ liệu giả để học.*

## Prompt dùng khi có thay đổi

Khi ngân hàng đổi định dạng sao kê: dùng prompt "sửa khi sao kê đổi cột" ở [bài 4](cap-03-prompt-mau-va-bai-tap.md) (đã chạy thật). Hai prompt dưới đây là **đề xuất, chưa chạy lại bằng agent**.

Thêm vào prompt giao việc để giảm viết cứng:

```prompt
doi_soat.py phải chạy lại được trên sao kê và sổ đơn của tháng khác có cùng định dạng. Không viết cứng số CT, mã đơn hay số tiền của từng dòng cụ thể vào script. Quy tắc phải tổng quát (biểu thức chính quy, so tên, so tiền).
```

Thêm quy ước cho ca nên luôn để người quyết:

```prompt
Quy ước thêm: các dòng sau luôn ghi CAN NGUOI QUYET, không bao giờ ghi CAO hay TRUNG BINH: (1) tiền hãng vận chuyển trả gộp COD mà nội dung không có mã đơn; (2) hai khách trùng tên và hai đơn cùng số tiền; (3) một lần chuyển trả nhiều đơn mà nội dung không ghi mã đơn. Với các dòng này vẫn nêu đơn ứng viên và lý do.
```

Kiểm tay: tìm trong script các dãy 8 chữ số (số CT) và các chuỗi `DH2610-0xx`. Nhiều thì script viết cứng.

## Lỗi thường gặp

| Triệu chứng | Nguyên nhân | Cách xử |
|---|---|---|
| Tháng sau script chạy được nhưng toàn `CAN NGUOI QUYET` | Script viết cứng theo tháng cũ, hoặc tiền tố mã đơn đổi (`DH2611`) | Chạy kiểm tái lập; đổi tiền tố hoặc nhờ agent làm thành biến cấu hình |
| Tổng kiểm 6/6 nhưng người duyệt thấy sai | Tổng kiểm chỉ kiểm tiền, không kiểm ghép | Lấy mẫu dòng `CAO` (Bước 5) |
| Số "đã ghép" của hai tháng khác quy ước | Quy ước xếp ca mơ hồ khác nhau | Ghi quy ước một lần, dùng mãi |
| Khách bực vì nhắn nhầm đơn đã hủy | Danh sách đơn chưa thu không loại đơn hủy | Kiểm cột `Trạng thái` trước khi nhắn |
| `kiem_nhanh.py` báo không đọc được sao kê | Sao kê đổi định dạng (đổi tên cột, dấu phân cách) | `kiem_nhanh.py` đọc đúng định dạng bài 1; đổi định dạng thì nhờ agent sửa cả hai |
| Excel mở CSV bị vỡ chữ | Mã hóa | *Data > From Text/CSV*, chọn UTF-8 |

## Checklist cuối bài 3

- [ ] Đã chốt người duyệt và ngưỡng xử lý lệch tiền.
- [ ] Đã chạy kiểm tái lập trên một bộ dữ liệu khác; script nào viết cứng thì sửa trước khi dùng.
- [ ] Đã viết quy ước: COD gộp, khách trùng tên, trả hai đơn không mã luôn là `CAN NGUOI QUYET`.
- [ ] Mỗi tháng chạy `kiem_nhanh.py` và lấy mẫu dòng `CAO`.
- [ ] Đã quyết định chạy hằng tuần hay hằng tháng.

## Việc cần người làm

- Duyệt kết quả, quyết từng ngoại lệ, giữ hồ sơ quyết định.
- Làm việc với khách: hỏi lại, hoàn tiền, nhắc thanh toán.
- Chọn cách xử lý chuyển thiếu, thừa, trùng theo chính sách shop. Hạch toán và chứng từ: **cần kiểm với kế toán hoặc luật sư**.
- Đọc script (hoặc nhờ người biết Python đọc) trước khi dùng thật.

## Giới hạn

- Kiểm tái lập dùng hai bộ dữ liệu từ cùng một bộ sinh, nên bẫy giống nhau. Dữ liệu thật có kiểu lộn xộn khác và có thể làm cả script "tổng quát" của Claude Code hỏng ở chỗ khác. Con số 130/130 trên bộ mới không dự báo kết quả trên dữ liệu thật.
- n nhỏ: mỗi agent một lần chạy có log, mỗi script chạy lại một lần trên mỗi bộ. Không đo được độ ổn định, không kết luận agent nào tốt hơn. Phần "viết cứng" là quan sát về một script cụ thể.
- `kiem_nhanh.py` chỉ phát hiện lỗi cộng trừ và ghép trùng, không biết ghép đúng hay sai đơn.
- Hai prompt ở mục trên chưa được chạy lại bằng agent.
- Không có phép đo thời gian tiết kiệm so với làm tay: chúng tôi không có số liệu đó và không ước lượng.

## Đào sâu: chi phí, thay đổi và mở rộng

### Chi phí và tài nguyên **[Đo được]**

Chỉ có hai điểm số, đừng suy rộng:

- Một lần Claude Code tạo script: 557 giây, log ghi 1,51 USD (số do log Claude Code ghi, theo cấu hình lúc chạy).
- Một lần `agy`: 1.257 giây; log `agy` không ghi chi phí.
- Chạy lại script đã có: vài giây, không tốn lần gọi agent.

Dùng cách 2 thì chỉ tốn tiền gọi agent khi cần sửa script. **[Đề xuất]** ghi lại mỗi lần sửa: ai, ngày nào, vì sao, và kết quả kiểm tái lập sau sửa.

### Quản lý thay đổi

- **Đổi định dạng sao kê** (đổi cột, thêm dòng đầu file): script lỗi hoặc đọc sai. Dấu hiệu: `kiem_so_du_khop` thành `false`, hoặc số dòng lệch. Gọi lại agent, đưa **một** sao kê mới, nhờ sửa script, rồi chạy lại kiểm tái lập.
- **Sang tháng mới:** tiền tố mã đơn đổi theo tháng. Script của Claude Code viết cứng `DH2610` ở vài chỗ; sang tháng 11 phải đổi thành `DH2611`. **[Đề xuất]** đưa tiền tố vào một biến ở đầu file (prompt đề xuất chưa chạy):

```prompt
Trong doi_soat.py, tiền tố mã đơn (DH2610) đang viết cứng ở vài chỗ. Đưa nó thành một biến cấu hình ở đầu file và dùng biến đó ở mọi chỗ. Sau khi sửa, chạy lại trên dữ liệu hiện có và so bang_ghep.csv mới với bản cũ bằng code: hai bản phải giống nhau. Không đổi quy tắc ghép nào khác.
```

- **Thêm ngân hàng thứ hai:** mỗi ngân hàng một hàm đọc sao kê, phần ghép dùng chung.

### Mở rộng

- **Sổ Excel nhiều sheet, nhiều kho:** thêm bước ghép sheet trước khi đối soát.
- **Đối soát hai chiều:** ngoài "dòng sao kê chưa khớp đơn", thêm báo cáo "đơn đã giao quá N ngày mà chưa thu" cho đội bán hàng.
- **Ghi vào phần mềm kế toán:** xuất `bang_ghep.csv` sang định dạng nhập của phần mềm (xem tài liệu phần mềm bạn dùng; ví dụ MISA có hướng dẫn nhập sao kê, https://helpact.misa.vn/?p=72941). **[Đề xuất]** chỉ nhập các dòng `CAO` đã duyệt, các dòng khác nhập tay sau khi quyết.
- **Mã chuyển khoản riêng cho từng đơn:** giảm lộn xộn từ gốc bằng cách yêu cầu khách ghi mã đơn theo mẫu cố định, hoặc dùng mã QR có sẵn nội dung. **[Đề xuất]**; chúng tôi chưa kiểm tính năng này ở ngân hàng nào.
