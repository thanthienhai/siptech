# Bài 3. Đưa vào dùng hằng tháng

!!! info "Bài này"
    - **Bạn làm gì:** giữ script mà agent đã viết, chạy lại bằng một lệnh, đổi ngân sách, xuất ra Excel, rồi lập quy trình hằng tháng có người duyệt ở đúng chỗ.
    - **Mất bao lâu:** khoảng 30 phút để thử lần đầu. Mỗi tháng sau đó chủ yếu là thời gian người duyệt (script chạy dưới 1 giây).
    - **Cần có:** kết quả bài 1 và 2 (thư mục `kho-lan-1` có `tinh_ton_kho.py`), Python 3, `pip install openpyxl` nếu muốn xuất Excel.
    - **Kết quả:** một quy trình 6 bước, trong đó phần tính chạy bằng một lệnh và ra kết quả giống hệt nhau mỗi lần với cùng dữ liệu; tiền kiểm lại được trong 5 phút; người quyết số cuối.

> Dữ liệu GIẢ để học. Nhãn: **[Đo được]** là kết quả chạy hoặc thử của chúng tôi ngày 2026-11-20, **[Đề xuất]** là ý kiến của chúng tôi, chưa kiểm với cửa hàng thật.

## Quy trình mỗi tháng

### Bước 1. Giữ script, chạy lại bằng một lệnh

Ở bài 2 agent không chỉ trả lời, nó **viết ra một chương trình** `tinh_ton_kho.py`. Đó là thứ đáng giữ nhất: lần sau bạn không nhờ agent làm lại từ đầu, chỉ chạy chương trình. Đúng nguyên tắc ở bài 1: **công thức do code tính**, agent giúp làm sạch và giải thích.

Thử chạy lại trên một bản sao. Windows (PowerShell), trong thư mục chứa `kho-lan-1`:

```lenh
mkdir kho-thu-lai
copy kho-lan-1\*.csv kho-thu-lai\
copy kho-lan-1\tham-so.json, kho-lan-1\quy-uoc.md, kho-lan-1\tinh_ton_kho.py kho-thu-lai\
cd kho-thu-lai
python -X utf8 tinh_ton_kho.py
```

macOS hoặc Linux:

```lenh
mkdir kho-thu-lai
cp kho-lan-1/*.csv kho-lan-1/tham-so.json kho-lan-1/quy-uoc.md kho-lan-1/tinh_ton_kho.py kho-thu-lai/
cd kho-thu-lai
python3 -X utf8 tinh_ton_kho.py
```

`python` chạy chương trình, `-X utf8` để tiếng Việt không vỡ. Chương trình đọc các CSV trong thư mục hiện tại và ghi lại bốn file CSV cùng `bao-cao.md`.

!!! see "Bạn sẽ thấy"
    Vài dòng tóm tắt hiện ra. Với script của `claude-1` trên dữ liệu bài 1 **[Đo được]**:

    ```ketqua
    So ma: 60 | dong nhat ky: 11128 | dong loi ghi nhan: 133
    Tong can chua xet ngan sach: 41.104.400 VND | de xuat: 29.936.000 VND | ngan sach: 30.000.000
    Khong vuot ngan sach: True | boi so dung: True
    ABC: {'A': 13, 'B': 24, 'C': 23} | canh bao: {'OK': 43, 'SAP_HET': 9, 'TON_LAU': 5, 'HET_HANG': 2, 'BAN_CHAM': 1}
    ```

    Chạy lại với dữ liệu không đổi cho kết quả **giống từng byte** ở cả 5 file (đã so bằng lệnh so sánh file) và mất dưới 1 giây. Agent tự chạy lại mỗi lần thì **không** bảo đảm được điều này (hai lượt `agy` cho hai kết quả khác nhau ở khâu phát hiện lỗi, bài 2). Khi tính bằng script, chỗ còn dao động là **lúc viết script**.

### Bước 2. Đổi ngân sách, xem tác động lên dòng tiền

Ngân sách nằm trong `tham-so.json`, trường `ngan_sach_nhap_vnd`. Sửa số đó (bằng Notepad), chạy lại script. **[Đo được]** với script `claude-1`, cùng dữ liệu:

![Đổi ngân sách và thử dòng lạ vào nhật ký](anh/10-thu-chay-lai.webp)

*Ảnh dựng từ `ket-qua/thu-chay-lai.json`, kết quả thử của chúng tôi. Dữ liệu giả để học.*

Đọc bảng: ngân sách 20 và 30 triệu đều chỉ nhập được 9 mã; phải có ít nhất **41.104.400 đ** mới nhập đủ 24 mã công thức yêu cầu, từ đó trở lên tổng tiền không đổi. Con số 41,1 triệu là câu trả lời cho "tháng này cần tối đa bao nhiêu vốn nhập hàng theo công thức". Nếu tiền mặt thấp hơn, phần cắt là **quyết định của chủ cửa hàng**, không phải của agent. Bạn tự thử và xem mã nào bị cắt ở **bài tập 1, bài 4**.

**[Đề xuất]** Khi đọc phần bị cắt, nhìn **số ngày tồn còn lại** của từng mã: nhóm tồn chỉ đủ bán dưới 30 ngày phải quyết trước, vì sau 30 ngày chúng hết.

### Bước 3. Cho Excel đọc kết quả

Chủ cửa hàng quen Excel hơn CSV. `du-lieu/xuat_excel.py` (cần `pip install openpyxl`) gom 4 file CSV thành một file `.xlsx`. Trong thư mục `kho-thu-lai` (macOS, Linux dùng `python3` và dấu `/`):

```lenh
python -X utf8 ..\du-lieu\xuat_excel.py . bao-cao-nhap-hang.xlsx
```

Dấu `.` là thư mục hiện tại chứa các CSV; tham số sau là tên file Excel.

!!! see "Bạn sẽ thấy"
    Dòng `da ghi bao-cao-nhap-hang.xlsx`. File có 4 trang: đề xuất nhập (dòng cần người quyết tô vàng, cuối trang có ô tổng bằng công thức SUM, ngân sách và số còn lại), ABC và cảnh báo (hết hàng và sắp hết tô đỏ), giữ lại 2 tháng, lỗi dữ liệu. **[Đo được]** Chúng tôi **chưa mở bằng Excel thật để xác nhận ô SUM tính ra đúng**, chỉ kiểm bằng code rằng công thức ghi đúng ô. Hãy mở và xem ô đó.

### Bước 4. Người duyệt đọc đề xuất bằng ba câu hỏi

Mở `loi-du-lieu.csv` trước. Dòng `CAN_NGUOI_QUYET` phải do **người** trả lời (số âm là trả hàng hay gõ nhầm, số gấp 10 là bao nhiêu, đơn sỉ có lặp lại không). Sửa dòng sai **trong nhật ký gốc**, đừng sửa kết quả, rồi chạy lại. Sau đó đọc `de-xuat-nhap.csv` với ba câu hỏi:

1. Tổng tiền có vượt ngân sách không?
2. Mã hết hoặc sắp hết: **hàng đang về có kịp không?** Nhìn **ngày về**, không chỉ số lượng. Ví dụ MP002 có 12 cái "đang về" nhưng dự kiến 2026-12-27, sau tháng đề xuất: công thức vẫn trừ 12 cái đó nên đề xuất 0, trong khi tháng 11 mã này hết hàng.
3. Mã bị cắt vì ngân sách còn đủ bán bao nhiêu ngày?

### Bước 5. Đặt hàng và ghi lại chỗ bạn sửa

**Người quyết số cuối cùng.** Đề xuất của agent hoặc script chỉ là tham khảo. Ghi lại chỗ bạn sửa so với đề xuất và lý do (ví dụ "tăng gạo vì khách quen đặt trước", "hỏi nhà cung cấp giao sớm MP002"). **[Đề xuất]** lưu cùng thư mục của tháng đó.

### Bước 6. Cuối tháng sau: đo lại

Ghi lại thực tế bán và so với dự báo, để biết công thức đúng tới đâu với cửa hàng của bạn. Trong dữ liệu giả, công thức thua mốc "bằng tháng trước" ở hai tháng giữ lại (bài 2); với dữ liệu thật bạn phải tự đo, không dựa vào bài này.

!!! warning "Quy tắc an toàn khi dùng dữ liệu thật"
    - **Quyền.** `agy` với `--dangerously-skip-permissions` là toàn quyền; Claude Code với `acceptEdits` tự chấp nhận sửa file. Cả hai chạy được lệnh trên máy bạn. Ở bài 2, chúng tôi thấy `claude-1` ghi một file tạm ra ngoài thư mục làm việc dù prompt dặn "chỉ ghi trong thư mục hiện tại". **Lời dặn trong prompt không phải rào chắn.** Dùng thư mục riêng, sao lưu, nếu được thì máy hoặc tài khoản riêng.
    - **Dữ liệu cá nhân.** Nhật ký thật thường có tên khách, số điện thoại trong cột ghi chú. Xóa hoặc thay bằng mã **trước** khi giao agent. Log của agent có thể chứa đường dẫn thư mục máy bạn: kiểm trước khi chia sẻ.
    - **Đáp án để ngoài tầm agent.** Trong cửa hàng thật, "đáp án" là kiểm kê thực tế và quyết định cuối của bạn.

## Prompt khi có thay đổi

Hai prompt dưới đây là prompt mới. Prompt thứ nhất **chưa chạy thử**; prompt thứ hai chúng tôi chạy một lần (xem kết quả bên dưới nó). Bài 4 có thêm các prompt đã chạy thật. Dán vào agent đang mở trong thư mục chứa script.

**Khi sang tháng mới.** **[Đo được]** từ mã nguồn script `claude-1`: nó gắn cứng cửa sổ 12 tháng 2025-11 đến 2026-10 và tên hai file tồn. Sang tháng 12 bạn không chỉ thay dữ liệu.

```prompt
Dữ liệu đã thêm tháng 2026-11. Hãy sửa tinh_ton_kho.py để cửa sổ 12 tháng và tên file tồn đầu kỳ, kiểm kê lấy từ tham-so.json thay vì viết cứng. Sau khi sửa, chạy lại trên dữ liệu CŨ (12 tháng 2025-11 đến 2026-10) và chứng minh bằng so sánh file rằng de-xuat-nhap.csv và phan-loai-tinh-toan.csv giống hệt bản trước khi sửa. Ghi những gì đã đổi vào nhat-ky-sua-script.md. Không đổi công thức trong quy-uoc.md.
```

**Khi thêm một quy tắc.** Ví dụ: mã có dự báo cao gấp nhiều lần cùng kỳ năm trước thì không tự động nhập mà đẩy sang người quyết (xem bài tập 2, bài 4).

```prompt
Thêm một quy tắc vào tinh_ton_kho.py: với mỗi mã mà dự báo tháng tới cao gấp 3 lần trở lên so với cùng kỳ năm trước (cột cung_ky_nam_truoc_2025_11), đặt can_nguoi_quyet = CO và ghi vào ly_do câu "dự báo cao gấp N lần cùng kỳ năm trước, có thể là hàng theo mùa". Không đổi số lượng đề xuất. Chạy lại và liệt kê những mã bị gắn cờ mới so với bản trước. Công thức trong quy-uoc.md giữ nguyên.
```

**[Đo được]** Chạy thử ngày 2026-11-21, n=1, 71 giây, trên dữ liệu có thêm mã bánh trung thu TH025 của bài tập 2 (bài 4). Agent thêm quy tắc với ngưỡng đặt ở một hằng số, chạy lại, và báo 3 mã bị gắn cờ: TH025 (dự báo 107,3 so với cùng kỳ 1, nhưng đã `CO` từ trước), VT020 (11,0 so với 2, đã `CO` từ trước) và **VT010 (5,67 so với 1, mới bị gắn cờ)**. Số lượng đề xuất của mọi mã không đổi, `phan-loai-tinh-toan.csv` giống hệt bản trước. Chúng tôi kiểm lại: bộ kiểm của bài tập 2 báo `DAT` và trong `de-xuat-nhap.csv`, ngoài cột lý do, chỉ một ô đổi: `can_nguoi_quyet` của VT010 từ `KHONG` thành `CO`. Agent tự cảnh báo: cùng kỳ chỉ 1 đến 2 đơn vị nên tỉ lệ "gấp N lần" có thể là do mẫu số quá nhỏ chứ chưa chắc là mùa vụ; 4 mã không xét được vì cột cùng kỳ trống. Bài học: quy tắc dùng tỉ lệ bắt được mã bánh, nhưng cũng gắn cờ cả mã không phải hàng mùa. Người duyệt vẫn phải nhìn.

## Lỗi thường gặp khi dùng hằng tháng

| Triệu chứng | Cách xử lý |
|---|---|
| Script dừng với `ngay khong doc duoc: 30-10-2026` | Kiểu ngày mới mà script chưa biết. **[Đo được]** (dòng thử `PX99003`). Gửi agent đúng thông báo lỗi và dòng làm lỗi (prompt ở bài 4), rồi so kết quả bản cũ và bản mới |
| Script dừng với `KeyError: 'ZZ999'` | Mã hàng không có trong danh mục. **[Đo được]** (dòng thử `PX99004`). Nhờ agent ghi mã lạ vào `loi-du-lieu.csv` thay vì dừng |
| Số âm không ghi chú, thiếu số lượng | Script chạy tiếp, ghi `CAN_NGUOI_QUYET`, tạm tính 0 **[Đo được]**. Người phải trả lời |
| Tổng tiền đề xuất ra gần đúng ngân sách nhưng thiếu nhiều mã sắp hết | Đó là hệ quả của thứ tự ưu tiên agent chọn. Xem lại phần bị cắt (Bước 4) |
| Bạn sửa kết quả thay vì sửa nhật ký gốc | Lần chạy sau lỗi quay lại. Sửa ở nhật ký gốc |

Bài học: script **dừng ồn ào** khi gặp dạng dữ liệu chưa biết còn hơn im lặng chạy sai, nhưng người không rành code sẽ không biết làm gì khi thấy chữ `KeyError`. **[Đề xuất]** Khi gặp lỗi, quay lại agent với đúng thông báo lỗi.

## Đào sâu: khi nào KHÔNG nên tin đề xuất, và hướng mở rộng

- **Công thức thua mốc "bằng tháng trước" ở hai tháng giữ lại** (bài 2: WAPE 2026-09 là 33,1% so với 30,5%; 2026-10 là 38,2% so với 21,7%, `claude-1`). Với mã mùa vụ (nước giải khát, hàng Tết, đồ mùa mưa) hãy so với **cùng kỳ năm trước** khi có đủ 24 tháng; trong bài này chỉ làm được cho tháng 2026-11. Người duyệt nên nhìn cột `cung_ky_nam_truoc_2025_11`; báo cáo `claude-0` chỉ ra mã nước ngọt có dự báo cao hơn hẳn năm trước.
- **Mã mới ít tháng dữ liệu:** độ lệch chuẩn chỉ là giả định (0,5 × dự báo), kém chắc chắn (MP010 chỉ có 2 tháng).
- **Thời gian giao cố định** là giả định. Nhà cung cấp trễ thì tồn an toàn thật không đủ. Công thức có xét độ lệch thời gian giao tồn tại (Shopify <https://www.shopify.com/blog/safety-stock>), bài này không dùng.
- **Hạn sử dụng, chi phí đặt hàng, ưu đãi theo số lượng** chưa được xét.
- Ngưỡng ABC 80/95, mức phục vụ 95%, ngưỡng tồn lâu 120 ngày là **tham số đề xuất** của chúng tôi, không phải quy định; cần kiểm với kế toán nếu liên quan sổ sách.

**Hướng mở rộng [Đề xuất]** (phải đo lại bằng hold-out, không thêm khi chưa đo): hệ số mùa vụ khi có 24 tháng dữ liệu; thêm độ lệch chuẩn thời gian giao vào tồn an toàn; gộp đơn theo nhà cung cấp để đạt mức giao tối thiểu; cột ngày hết hạn cho hàng cận hạn; đặt lịch chạy script cuối tháng và gửi Excel cho chủ cửa hàng (vẫn phải có người duyệt trước khi đặt).

## Checklist

- [ ] Có script chạy lại bằng một lệnh và đã thử chạy lần hai (kết quả giống nhau).
- [ ] Biết tổng tiền cần theo công thức, ngân sách của mình và phần bị cắt là mã nào.
- [ ] Đã nhìn ngày về của hàng đang về, nhất là mã đang hết hàng.
- [ ] Mọi dòng `CAN_NGUOI_QUYET` đã được người trả lời và sửa ở nhật ký gốc.
- [ ] Đã so với cùng kỳ năm trước cho mã có mùa vụ (khi có dữ liệu).
- [ ] Đã che dữ liệu cá nhân trước khi giao agent và kiểm log trước khi chia sẻ.

## Việc cần người làm

- Duyệt số cuối cùng và chịu trách nhiệm đặt hàng.
- Quyết ngân sách, thứ tự ưu tiên khi bị cắt, mức phục vụ.
- Xác nhận ngày về của hàng đang về với nhà cung cấp.
- Ghi lại thực tế bán để lần sau đo lại công thức.

## Giới hạn

- Dữ liệu giả; một cửa hàng giả với mùa vụ do chúng tôi đặt; mỗi agent 1 lần chạy có log; chưa đo độ ổn định giữa các lần viết script.
- Prompt "Khi sang tháng mới" **chưa chạy thử**; việc cập nhật script sang tháng mới chúng tôi chưa làm. Prompt "Khi thêm một quy tắc" mới chạy 1 lần.
- Chưa mở file Excel xuất ra bằng Excel thật.
- Không có đánh giá nào về việc agent này hay agent kia "tốt hơn".
