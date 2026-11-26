# Bài 3. Dùng hằng ngày: có thước kiểm riêng, có người duyệt

!!! info "Bài này"
    - **Bạn làm gì:** biến việc "viết mô tả cho một lô hàng mới" thành quy trình lặp lại: agent viết, thước kiểm của shop chạy, người duyệt ký, rồi mới đăng.
    - **Mất bao lâu:** thiết lập lần đầu khoảng 30 phút. Mỗi lô sau: agent vài phút **[Đo được]** (40 sản phẩm: Claude Code 241 và 298 giây, Antigravity 756 giây) cộng thời gian người duyệt.
    - **Cần có:** kết quả bài 1 và 2, Python 3, một người duyệt có quyền quyết.
    - **Kết quả:** 0 lỗi cứng từ thước kiểm, 0 dòng còn cờ `CẦN BỔ SUNG` hay `CẦN NGƯỜI QUYẾT`, người duyệt đã ký từng dòng nhóm rủi ro.

> Dữ liệu giả để học (shop "Vườn Nhỏ" không có thật). Số liệu **[Đo được]** là của các lần chạy ngày 2026-11-20, n=2 mỗi agent. Chỗ nào là ý kiến thì gắn **[Đề xuất]**. Chạy các lệnh trong thư mục `du-lieu/`, thư mục `ket-qua/` nằm cạnh.

## Quy trình mỗi lô hàng mới

```
NCC gửi thông số ─▶ 1. Nhập thong_so.csv ─▶ 2. Chạy agent ─▶ 3. Chạy thước kiểm của shop
                                                                       │
          6. Đăng lên sàn ◀─ 5. Người duyệt ký ◀─ 4. Sửa / bổ sung ◀──┘
```

### Bước 1. Nhập thông số, tách lời đồn

- Mỗi lô có một `thong_so.csv` mới, giữ nguyên cột như mẫu. Cột `ghi_chu_noi_bo` vẫn là lời đồn.
- Ô chưa có thông tin: **để trống** hoặc ghi một kiểu thống nhất (ví dụ "chưa có"). Bài 2 cho thấy agent xử lý được nhiều kiểu, nhưng thống nhất thì người trong shop cũng đỡ nhầm.
- Cột `so_phieu_cong_bo`: chỉ điền khi đã **có giấy** trong tay. Đang chờ thì ghi "đang chờ duyệt". Chỗ này liên quan pháp lý nên bài không nói thêm; hãy hỏi người phụ trách.

!!! warning "Quy tắc an toàn"
    - Đưa agent chỉ những gì cần: bảng thông số, quy định, từ cấm. **Không đưa** giá nhập, giá NCC, hợp đồng.
    - Mỗi lô một thư mục riêng (ví dụ `lo-2026-12`). Máy kiểm và `dap-an.json` **ở ngoài** thư mục agent.
    - `--dangerously-skip-permissions` hay `--permission-mode acceptEdits` cho agent quyền rộng. Chỉ dùng trong thư mục riêng, với dữ liệu đã lọc (đọc lại bài 1).
    - Lưu `prompt-giao-viec.txt`, bảng thông số và file đầu ra theo từng lô. Khi sàn hỏi "sao ghi vậy", bạn truy được nguồn từng câu.

### Bước 2. Chạy agent

Giữ nguyên prompt ở bài 1 (`du-lieu/prompt-giao-viec.txt`), chép vào thư mục lô, bốn file đầu vào như bài 1, rồi chạy. Con số tham khảo **[Đo được]** cho 40 sản phẩm: Claude Code 241 và 298 giây (chi phí do chính nó báo khoảng 0,70 và 0,86 USD), Antigravity lần 2 mất 756 giây. Đừng tự nhân lên cho lô 400 sản phẩm: chưa đo.

Khi đổi prompt, đổi dữ liệu hay đổi agent, chạy lô nhỏ trước (5 đến 10 sản phẩm). **[Đề xuất]**

### Bước 3. Chạy thước kiểm của shop

Agent tự viết `kiem.py` và tự báo "sạch". Bài 2 cho thấy một lần như vậy bỏ lọt "chính hãng" ở 40 sản phẩm. Vì thế shop cần một thước **riêng, không do agent viết**. Bộ bài có sẵn `kiem_hang_ngay.py`:

```lenh
python -X utf8 kiem_hang_ngay.py ..\ket-qua\agy-v1-lan2\nhap_hang_loat.csv
```

Lệnh lấy chính `thong_so.csv` làm sự thật (không cần file đáp án riêng), đọc `tu_cam.txt`, dùng lại logic của `cham.py`, in từng sản phẩm có lỗi. macOS hoặc Linux: đổi `\` thành `/`, `python` thành `python3`. Đầu ra mẫu (rút gọn: 40 dòng lỗi, ở đây chỉ trích một dòng):

```ketqua
LỖI CỨNG VN-040 {'cum_ngoai_bang': ['chính hãng']}
…
40 SKU: 0 sạch, 40 có lỗi cứng; thiếu thông số 9 (gắn cờ đúng 9), báo động giả 0.
```

- `LỖI CỨNG`: từ cấm, số ngoài bảng, cụm ngoài bảng, rò ghi chú, nói "đã công bố" sai, trạng thái sai, độ dài, giọng sai.
- `XEM LẠI`: ứng viên tên riêng hoặc chữ hoa lạ (cần mắt người, chưa chắc là lỗi).
- Thoát mã 1 nếu còn lỗi cứng, nên có thể gắn vào một tệp `.bat` hay lịch chạy.

**[Đo được]** trên bốn file đầu ra ở bài 2, nó cho đúng số sản phẩm sạch như `cham.py`: 40, 40, 39 và 0.

!!! stuck "Gặp lỗi?"
    - **Chữ tiếng Việt hiện vỡ trong cửa sổ dòng lệnh:** có thể chỉ là chuyện hiển thị. Thêm `--ghi ketqua.txt` vào cuối lệnh để ghi kết quả ra file UTF-8 rồi mở bằng Notepad.
    - **`ModuleNotFoundError` nhắc tới `cham`, hoặc không thấy `dap-an.json`:** `kiem_hang_ngay.py` cần `ket-qua/cham.py` và `ket-qua/dap-an.json` nằm cạnh thư mục `du-lieu`. Chạy lệnh trong `du-lieu`.

### Bước 4. Sửa hoặc bổ sung

- **Dòng `CAN_BO_SUNG`:** nhờ người nhập liệu hỏi NCC, điền vào `thong_so.csv`, chạy lại **chỉ các dòng đó**. Bài 4 (prompt 9) có prompt soạn danh sách câu hỏi gửi NCC. Chúng tôi chưa thử chạy lại từng phần; thử trên lô nhỏ trước.
- **Dòng lỗi từ thước kiểm:** đừng sửa tay trong file đầu ra mà không ghi lại. Sửa nguyên nhân (thêm câu vào quy định, hoặc sửa bảng) rồi chạy lại. Sửa tay thì lô sau lỗi lại.
- **Lỗi lặp ở cả lô** (như "chính hãng"): thêm một dòng vào mục "nguyên tắc sự thật" của `quy_dinh_shop.md`. Prompt dưới đây nhờ agent làm việc đó. **Chưa chạy thử**, nên chưa biết nó có hiệu quả không; hãy đo bằng cách chạy lại và chấm.

```prompt
Trong quy_dinh_shop.md, mục 5 (Nguyên tắc sự thật), hãy thêm một dòng: không dùng các từ "chính hãng", "lành tính", "an toàn" trừ khi bảng thông số của đúng sản phẩm đó ghi đúng cụm này. Chỉ thêm đúng dòng đó, không sửa chỗ nào khác, rồi cho tôi xem phần đã thêm.
```

### Bước 5. Người duyệt xem gì, ký gì

Không ai đọc kỹ 40 dòng ba lần. Người duyệt xem theo nhóm rủi ro:

| Nhóm | Vì sao | Ví dụ trong bài |
|---|---|---|
| Mọi dòng `CAN_BO_SUNG` | còn chữ thô tên cột trong mô tả | VN-007, VN-019 |
| Dòng có `ghi_chu_noi_bo` | nơi lời đồn dễ rò | 14 sản phẩm |
| Dòng có số phiếu hoặc "đang chờ duyệt" | liên quan tuyên bố pháp lý | 10 và 4 sản phẩm |
| Dòng bảng mâu thuẫn | chỉ người mới quyết được | VN-012 (10% hay 15%) |
| 5 dòng ngẫu nhiên khác | bắt lỗi mà thước không biết | tự chọn |

**[Đề xuất]** Người duyệt ghi tên và ngày vào cột phụ cho mỗi dòng đã xem; không ghi thì không đăng.

Với VN-012: cả bốn lần chạy dùng 10%, đưa mâu thuẫn vào báo cáo kiểm, nhưng vẫn xếp `SAN_SANG`. Nếu dữ liệu giả này là thật, chúng tôi sẽ giữ dòng này lại tới khi có phiếu kiểm nghiệm. **[Đề xuất]**

### Bước 6. Chặn đăng nhầm cờ, rồi ghi lỗi mới vào thước

Trước khi tải file lên sàn, kiểm không còn dòng nào mang cờ. Lệnh sau liệt kê số dòng còn chữ `CẦN BỔ SUNG` hoặc `CẦN NGƯỜI QUYẾT` (chạy từ thư mục `du-lieu`):

```lenh
Select-String -Path ..\ket-qua\claude-v1-lan1\nhap_hang_loat.csv -Pattern "CẦN BỔ SUNG|CẦN NGƯỜI QUYẾT" -Encoding utf8 | ForEach-Object { $_.LineNumber }
```

Ở đây lệnh chạy trên file của Claude lần 1; với lô của bạn, thay đường dẫn sau `-Path`. Chúng tôi thấy in ra 8, 10, 15, 20, 26, 28, 30, 35, 39 (chín dòng vật lý). Đây là số dòng trong file, mô tả có xuống dòng nên số này **không trùng** số hàng trong Excel. Mở Excel, lọc cột `trang_thai` khác `SAN_SANG` cho dễ thấy. Nếu in ra số dòng nào, sản phẩm đó chưa được đăng; không in gì thì qua.

Sau đó, mỗi lần thấy lỗi lạ, thêm vào thước. Ví dụ: thấy "chính hãng" lọt thì thêm vào danh sách cụm của `cham.py` (đã có); thấy thước bắt nhầm "mỹ phẩm" thì sửa (đã sửa, ghi ở bài 2). Danh sách cụm là tài sản của shop và lớn dần. Thêm cụm mới rồi chạy `cham_kiem_thu.py` để chắc thước vẫn bắt đúng.

Một điều nữa: file CSV này theo định dạng **của shop** (11 cột). Mẫu nhập hàng loạt thật của Shopee hay TikTok Shop có cột và quy tắc riêng, **chưa xác minh** (chưa tải mẫu về). Cần một bước ánh xạ cột sang mẫu sàn, và thử nhập 2 đến 3 dòng trước.

## Điều nên biết về agent khi dùng hằng ngày

1. **Kết quả dao động giữa các lần chạy.** Antigravity lần 1 có 1 sản phẩm lỗi, lần 2 có 40, cùng prompt, cùng dữ liệu. Thước kiểm là bắt buộc **mỗi lần**, không chỉ lần thử đầu.
2. **Agent tự khen.** Cả bốn báo cáo kiểm đều tự kết luận "sạch". Thước độc lập mới cho biết lỗi.
3. **Agent làm tốt việc thiếu thông số** khi bạn nói rõ (9/9 sản phẩm, 17/17 trường). Điều này đến từ chỉ dẫn rõ trong prompt và `quy_dinh_shop.md`, không phải "bản năng". Chưa thử khi chỉ dẫn mơ hồ hơn.
4. **Văn viết khô.** Cả hai agent chuyển bảng thành câu, chưa viết thành lời bán hàng. Muốn thuyết phục hơn là thêm một bước viết, **tăng rủi ro vượt sự thật**: phải chạy lại cả thước kiểm lẫn người duyệt. Bài 4 có prompt đổi giọng và bài tập đo bằng code.

## Mở rộng

- **Cột `cong_dung_duoc_phep`:** các câu công dụng đã được người có thẩm quyền duyệt; agent chỉ được chọn trong danh sách này. **[Đề xuất]**
- **Nhiều sàn, nhiều giới hạn:** thêm bảng giới hạn riêng cho từng sàn (sau khi xác minh trên Kênh Người Bán), chạy thước kiểm theo từng sàn.
- **Kiểm chéo bằng agent thứ hai:** đã thử ở bài 4 (prompt 3), n=1, kết quả tốt trên dữ liệu này nhưng chưa đủ để kết luận.
- **Ảnh và alt text, đa ngôn ngữ:** chưa làm. Nếu dịch sang tiếng Anh phải chạy lại cả thước kiểm (từ cấm tiếng Anh, "natural", "organic"...).

## Lỗi thường gặp khi dùng hằng ngày

| Triệu chứng | Cách xử lý |
|---|---|
| Sửa tay file đầu ra, quên ghi, lô sau lỗi lại | Sửa nguồn (bảng, quy định), chạy lại |
| Tin báo cáo "sạch" của agent | Chạy thước độc lập |
| Điền `so_phieu_cong_bo` khi chưa có giấy | Chỉ điền khi đã có giấy |
| Đăng khi còn dòng cờ, khách thấy tên cột kỹ thuật | Chặn bằng Bước 6 |
| Không cập nhật danh sách cụm, lỗi cũ quay lại | Ghi vào thước mỗi lần thấy lỗi mới |
| Dùng quy định sàn từ blog | Đối chiếu Kênh Người Bán, ghi nguồn |

## Checklist hằng ngày

- [ ] `thong_so.csv` mới: lời đồn ở cột ghi chú, ô thiếu để trống hoặc ghi thống nhất.
- [ ] Chạy agent trong thư mục riêng, lưu log.
- [ ] Chạy `kiem_hang_ngay.py`, không còn "LỖI CỨNG".
- [ ] Xem hết mục `XEM LẠI`.
- [ ] Người duyệt xem đủ các nhóm rủi ro và ký.
- [ ] Không còn dòng nào có `CẦN BỔ SUNG` hay `CẦN NGƯỜI QUYẾT`.
- [ ] Ánh xạ sang mẫu của sàn, thử 2 đến 3 dòng.
- [ ] Ghi lỗi mới vào danh sách cụm của thước.

## Việc cần người làm

- **Chủ shop:** quyết giọng thương hiệu, từ cấm, và những dòng mâu thuẫn.
- **Người phụ trách sàn:** kiểm giới hạn độ dài hiện hành, tải mẫu nhập hàng loạt, đăng thử.
- **Người nhập liệu:** điền thông số thiếu; chỉ điền số phiếu khi có giấy.
- **Pháp chế hoặc luật sư:** xem các cụm "chính hãng", "đã công bố", "an toàn", "lành tính" và quy định quảng cáo mỹ phẩm. Bài này không trích điều luật.
- **Người duyệt:** ký từng dòng nhóm rủi ro.

## Giới hạn

- Chỉ 40 sản phẩm giả, 1 prompt, 2 lần chạy mỗi agent. Chưa đo ổn định, chưa đo lô lớn.
- Thước kiểm bắt được cái nó biết tìm (danh sách cụm tay, so khớp số). Nó không đọc hiểu nghĩa câu, không biết một cụm mới là bịa nếu chưa có trong danh sách.
- Chưa thử chạy lại từng phần cho sản phẩm được bổ sung. Chưa thử câu dặn ở Bước 4 (chưa đo).
- Giới hạn độ dài và mẫu nhập hàng loạt của sàn chưa xác minh đầy đủ (xem bài 1, phần Đào sâu).
- Đây không phải tư vấn pháp lý. Tiếp theo: bộ prompt dùng lại và bài tập ở **bài 4** ([cap-03-prompt-mau-va-bai-tap.md](cap-03-prompt-mau-va-bai-tap.md)).
