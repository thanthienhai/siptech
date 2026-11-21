# Bài 3: Đưa vào dùng hằng ngày, có người duyệt, biết giới hạn

> Dữ liệu giả để học (shop "Vườn Nhỏ" không có thật). Số liệu **[Đo được]** là của các lần chạy ngày 2026-11-20, n=2 mỗi agent. Chỗ nào là ý kiến thì gắn **[Đề xuất]**.

## Mục tiêu đo được

Biến việc "viết mô tả cho một lô hàng mới" thành một quy trình lặp lại được, trong đó:

- agent làm phần việc nặng (viết 40 dòng);
- một thước kiểm bằng code, **do shop sở hữu**, chạy sau agent và trước người duyệt;
- người duyệt chỉ xem những dòng thật sự cần mắt người;
- không dòng nào còn chữ `CẦN BỔ SUNG` hay `CẦN NGƯỜI QUYẾT` được đăng lên sàn.

Đo được thành công bằng: "0 lỗi cứng từ thước kiểm, 0 dòng còn cờ, người duyệt đã ký tên từng dòng nhóm rủi ro".

## Quy trình một lô hàng mới (7 bước)

```
NCC gửi thông số ─▶ 1. Nhập vào thong_so.csv ─▶ 2. Chạy agent ─▶ 3. Chạy thước kiểm
                                                                       │
        6. Đăng lên sàn ◀─ 5. Người duyệt ký ◀─ 4. Sửa/ bổ sung ◀──────┘
                                         │
                                         ▼ 7. Ghi lại lỗi mới vào thước
```

### Bước 1. Nhập thông số, tách lời đồn

- Mỗi lô có một `thong_so.csv` mới, giữ nguyên cột như mẫu. Cột `ghi_chu_noi_bo` vẫn là lời đồn.
- Với ô chưa có thông tin, **để trống** hoặc ghi một kiểu thống nhất (ví dụ "chưa có"). Bài 2 cho thấy agent xử lý được nhiều kiểu, nhưng thống nhất thì người trong shop cũng đỡ nhầm.
- Cột `so_phieu_cong_bo`: chỉ điền khi đã **có giấy** trong tay. Đang chờ thì ghi "đang chờ duyệt". Chỗ này liên quan pháp lý nên tôi không nói thêm; hãy hỏi người phụ trách.

### Bước 2. Chạy agent

Giữ nguyên prompt (`prompt-v1.txt`), đặt trong thư mục riêng cho từng lô, ví dụ `lo-2026-12\`. Chép 4 file vào rồi chạy như bài 1. Với 40 SKU, **[Đo được]** Claude Code mất 241 s và 298 s (chi phí do chính nó báo khoảng 0,70 và 0,86 USD); Antigravity lần 2 mất 756 s. Con số này là của dữ liệu này, đừng tự nhân lên cho lô 400 SKU: chưa đo.

Nên đưa vào lô nhỏ trước (5 đến 10 SKU) khi đổi prompt, đổi dữ liệu hay đổi agent. **[Đề xuất]**

### Bước 3. Chạy thước kiểm của shop

Agent tự viết `kiem.py` và tự báo "sạch". Bài 2 cho thấy một lần như vậy bỏ lọt "chính hãng" ở 40 SKU. Vì thế shop cần một thước **riêng**, không do agent viết. Bộ bài này có sẵn một cái:

```powershell
cd du-lieu
python -X utf8 kiem_hang_ngay.py ..\ket-qua\agy-v1-lan2\nhap_hang_loat.csv
```

`kiem_hang_ngay.py` lấy chính `thong_so.csv` làm sự thật (không cần file đáp án riêng như `dap-an.json`), đọc `tu_cam.txt`, dùng lại logic của `cham.py`, và in ra từng SKU có lỗi:

- `LỖI CỨNG`: từ cấm, số ngoài bảng, cụm ngoài bảng, rò ghi chú, nói "đã công bố" sai, trạng thái sai, độ dài, giọng sai.
- `XEM LẠI`: ứng viên tên riêng hoặc chữ hoa lạ (cần mắt người, không chắc là lỗi).

Thoát mã 1 nếu còn lỗi cứng, nên có thể gắn vào một tệp `.bat` hay lịch chạy. **[Đo được]** trên bốn file đầu ra ở bài 2, nó cho đúng số SKU sạch như `cham.py`: 40, 40, 39 và 0.

### Bước 4. Sửa hoặc bổ sung

- Dòng `CAN_BO_SUNG`: nhờ người nhập liệu hỏi NCC, điền vào `thong_so.csv`, chạy lại **chỉ các dòng đó** (đưa agent bảng gồm đúng các SKU này). Bài này chưa thử chạy lại từng phần; nên thử trên lô nhỏ trước.
- Dòng lỗi từ thước kiểm: **đừng sửa tay trong file đầu ra** mà không ghi lại. Nên sửa nguyên nhân (thêm câu vào quy định, hoặc sửa bảng) rồi chạy lại. Sửa tay thì lô sau lỗi lại.
- Lỗi lặp ở cả lô (như "chính hãng"): thêm một dòng vào mục "nguyên tắc sự thật" của `quy_dinh_shop.md`, ví dụ "không dùng các từ chính hãng, lành tính, an toàn trừ khi bảng ghi đúng cụm đó" và lưu thành `prompt-v2` hoặc `quy_dinh_shop` bản v2. **[Đề xuất]** Chưa chạy thử câu này, nên chưa biết nó có hiệu quả không; hãy đo bằng cách chạy lại và chấm.

### Bước 5. Người duyệt xem gì, ký gì

Không ai đọc kỹ 40 dòng 3 lần. Người duyệt xem theo nhóm rủi ro:

| Nhóm | Vì sao | Ví dụ trong bài |
|---|---|---|
| Mọi dòng `CAN_BO_SUNG` | còn chữ thô tên cột trong mô tả | VN-007, VN-019 |
| Dòng có `ghi_chu_noi_bo` | nơi lời đồn dễ rò | 14 SKU |
| Dòng có số phiếu hoặc "đang chờ duyệt" | liên quan tuyên bố pháp lý | 10 + 4 SKU |
| Dòng bảng mâu thuẫn | chỉ người mới quyết được | VN-012 (10% hay 15%) |
| 5 dòng ngẫu nhiên khác | bắt lỗi mà thước không biết | tự chọn |

**[Đề xuất]**: người duyệt ghi tên và ngày vào cột phụ cho mỗi dòng đã xem; không ghi thì không đăng.

Với VN-012: cả bốn lần chạy dùng 10%, đưa mâu thuẫn vào báo cáo kiểm, nhưng vẫn xếp `SAN_SANG`. Nếu dữ liệu giả này là thật, tôi sẽ giữ dòng này lại tới khi có phiếu kiểm nghiệm. **[Đề xuất]**

### Bước 6. Chặn đăng nhầm cờ

Trước khi tải file lên sàn, kiểm không còn dòng nào mang cờ:

```powershell
# Liệt kê mọi dòng còn chữ CẦN BỔ SUNG hoặc CẦN NGƯỜI QUYẾT
Select-String -Path nhap_hang_loat.csv -Pattern "CẦN BỔ SUNG|CẦN NGƯỜI QUYẾT" -Encoding utf8 | ForEach-Object { $_.LineNumber }
```

Nếu in ra số dòng nào, sản phẩm đó chưa được đăng. (Đây là số dòng vật lý trong file; mô tả có xuống dòng nên số này không trùng số hàng trong Excel. Mở Excel, lọc cột `trang_thai` khác `SAN_SANG` cho dễ thấy.) Ở bài 2, cả hai agent chép nguyên tên cột kỹ thuật (`dung_tich`...) vào chỗ cần bổ sung ngay trong mô tả: đăng nhầm sẽ để khách thấy chữ đó.

Một điều khác: file CSV này theo định dạng **của shop** (11 cột). Mẫu nhập hàng loạt thật của Shopee hay TikTok Shop có cột và quy tắc riêng, **chưa xác minh trong bài này** (chưa tải mẫu về). Bạn cần một bước ánh xạ cột sang mẫu sàn, và nên thử nhập 2 đến 3 dòng trước.

### Bước 7. Ghi lại lỗi mới vào thước

Mỗi lần thấy lỗi lạ, thêm vào thước. Ví dụ trong bài này:

- Thấy "chính hãng" lọt: thêm vào danh sách cụm của `cham.py` (đã có).
- Thấy thước bắt nhầm "mỹ phẩm" vì có chữ "mỹ": sửa (đã sửa, ghi ở bài 2).

Danh sách cụm là tài sản của shop và lớn dần theo thời gian. Người nào nghi ngờ một cụm mới ("an toàn cho bà bầu", "đã kiểm nghiệm") thì thêm cụm đó, rồi chạy `cham_kiem_thu.py` để chắc thước vẫn bắt đúng.

## Những điểm bạn nên biết về agent khi dùng hằng ngày

1. **Kết quả dao động giữa các lần chạy.** Antigravity lần 1 có 1 SKU lỗi, lần 2 có 40. Cùng prompt, cùng dữ liệu. Vì vậy thước kiểm là bắt buộc **mỗi lần**, không chỉ lần thử đầu.
2. **Agent tự khen.** Cả bốn báo cáo kiểm đều tự kết luận "sạch". Thước độc lập mới cho biết lỗi.
3. **Agent làm tốt việc thiếu thông số** khi bạn nói rõ trong prompt (9/9 SKU, 17/17 trường). Đáng lưu ý: điều này đến từ chỉ dẫn rõ trong cả prompt và `quy_dinh_shop.md`, không phải "bản năng" của agent. Chưa thử khi chỉ dẫn mơ hồ hơn.
4. **Văn bản viết ra khô.** Cả hai agent chuyển bảng thành câu, chưa viết thành lời bán hàng. Nếu bạn muốn văn thuyết phục hơn, đó là bước viết thêm và **tăng rủi ro vượt sự thật**: cần chạy lại cả thước kiểm lẫn người duyệt. Bài này không đo phần đó.

## Bảo mật và dữ liệu

- Đưa agent chỉ những gì cần: bảng thông số, quy định, từ cấm. Không đưa giá nhập, giá NCC, hợp đồng.
- Agent chạy với `--dangerously-skip-permissions` hay `--permission-mode acceptEdits` có quyền rộng. Dùng thư mục riêng và dữ liệu đã lọc. Đọc lại bài 1 về cờ này.
- Lưu `prompt-v1.txt`, bảng thông số và file đầu ra theo từng lô. Khi sàn hỏi "sao ghi vậy", bạn truy được nguồn của từng câu.

## Mở rộng

- **Thêm cột `cong_dung_duoc_phep`** gồm các câu công dụng đã được người có thẩm quyền duyệt. Agent chỉ được chọn trong danh sách này. **[Đề xuất]**
- **Nhiều sàn, nhiều giới hạn:** thêm bảng giới hạn riêng cho từng sàn (sau khi xác minh trên Kênh Người Bán), chạy thước kiểm theo từng sàn.
- **Ảnh và alt text:** chưa làm trong bài này.
- **Đa ngôn ngữ:** nếu dịch sang tiếng Anh, phải chạy lại cả thước kiểm (từ cấm tiếng Anh, "natural", "organic"...). Chưa thử.
- **Kiểm chéo bằng agent khác:** có thể nhờ agent thứ hai đọc đầu ra và tìm cụm không có trong bảng. Chưa thử; nếu thử thì chấm nó bằng cùng cách tiêm lỗi, vì một agent đọc lướt có thể lướt qua những cụm "dễ thương".

## Lỗi thường gặp khi dùng hằng ngày

| Lỗi | Hậu quả | Cách xử lý |
|---|---|---|
| Sửa tay file đầu ra, quên ghi | lô sau lỗi lại | sửa nguồn (bảng/ quy định), chạy lại |
| Tin báo cáo "sạch" của agent | lọt cụm bịa | chạy thước độc lập |
| Điền `so_phieu_cong_bo` khi chưa có giấy | nội dung nói sai sự thật | chỉ điền khi đã có giấy |
| Đăng khi còn dòng cờ | khách thấy tên cột kỹ thuật | chặn bằng bước 6 |
| Không cập nhật danh sách cụm | lỗi cũ quay lại | ghi vào thước mỗi lần thấy lỗi mới |
| Dùng quy định sàn từ blog | sai giới hạn | đối chiếu Kênh Người Bán, ghi nguồn |

## Checklist hằng ngày

- [ ] `thong_so.csv` mới: lời đồn ở cột ghi chú, ô thiếu để trống hoặc ghi thống nhất.
- [ ] Chạy agent trong thư mục riêng, lưu log.
- [ ] Chạy `kiem_hang_ngay.py`, không còn "LỖI CỨNG".
- [ ] Xem hết mục `XEM LẠI`.
- [ ] Người duyệt xem đủ các nhóm rủi ro và ký.
- [ ] Không còn dòng nào có `CẦN BỔ SUNG` / `CẦN NGƯỜI QUYẾT`.
- [ ] Ánh xạ sang mẫu của sàn, thử 2 đến 3 dòng.
- [ ] Ghi lỗi mới vào danh sách cụm của thước.

## Việc cần người làm

- **Chủ shop:** quyết giọng thương hiệu, từ cấm, và những dòng mâu thuẫn.
- **Người phụ trách sàn:** kiểm giới hạn độ dài hiện hành, tải mẫu nhập hàng loạt, đăng thử.
- **Người nhập liệu:** điền thông số thiếu; chỉ điền số phiếu khi có giấy.
- **Người phụ trách pháp chế hoặc luật sư:** xem các cụm "chính hãng", "đã công bố", "an toàn", "lành tính" và quy định quảng cáo mỹ phẩm. Bài này không trích điều luật.
- **Người duyệt:** ký từng dòng nhóm rủi ro.

## Giới hạn

- Chỉ 40 SKU giả, 1 prompt, 2 lần chạy mỗi agent. Chưa đo ổn định, chưa đo lô lớn.
- Thước kiểm bắt được cái nó biết tìm (danh sách cụm tay, so khớp số). Nó không đọc hiểu nghĩa câu, không biết một cụm mới là bịa nếu chưa có trong danh sách.
- Chưa thử chạy lại từng phần cho SKU được bổ sung.
- Chưa thử "prompt-v2" chặn các cụm kiểu "chính hãng": đó chỉ là đề xuất.
- Giới hạn độ dài và mẫu nhập hàng loạt của sàn chưa xác minh đầy đủ (xem README).
- Đây không phải tư vấn pháp lý.
