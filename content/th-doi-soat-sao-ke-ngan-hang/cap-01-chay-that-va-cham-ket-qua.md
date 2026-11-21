# Bài 2. Chạy thật và kiểm kết quả bằng đáp án

> Dữ liệu là **dữ liệu giả để học** (xem bài 1). Mọi con số dưới đây là **[Đo được]**: kết quả chạy ngày 2026-11-20 trên đúng bộ dữ liệu và prompt của bài 1. Mỗi agent chỉ có **một lần chạy có log đầy đủ** (n = 1), nên bài này chỉ mô tả quan sát, không kết luận agent nào tốt hơn và chưa đo được độ ổn định.

## Mục tiêu đo được

1. Chạy được cả hai agent (Claude Code và Antigravity `agy`) trên cùng dữ liệu, cùng prompt, trong thư mục riêng, và có log gốc để xem lại.
2. Chấm kết quả bằng **code** (`ket-qua/cham.py`) với đáp án, ra các chỉ số: ghép đúng bao nhiêu dòng "xác định", báo đúng bao nhiêu ca "mơ hồ", bỏ sót gì, bịa gì.
3. Nhận ra ba loại lỗi: lỗi của agent, lỗi do cách bạn giao việc, và lỗi do cách bạn chạy công cụ.

## 1. Chạy thật

### Bước 1. Thư mục riêng cho mỗi agent

Mỗi lần chạy một thư mục, chỉ có hai file dữ liệu (xem bài 1, mục 5). Tôi dùng `runs/claude-1` và `runs/agy-2`. Sau khi chạy, tôi so lại: file `sao-ke-t10-2026.csv` và `so-don-hang-t10-2026.xlsx` trong hai thư mục này **giống hệt** bản gốc (so mã băm với CSV, so từng ô với XLSX). Nghĩa là cả hai agent đều không sửa file đầu vào.

### Bước 2. Lệnh chạy

Cách tương tác: mở terminal trong thư mục, gõ `claude` (hoặc `agy`), dán prompt. Cách tôi dùng để lưu log là script `agent_run.py` bọc lệnh `-p` như bài 1, mỗi lần ra hai file: `*.raw.jsonl` (log gốc từng sự kiện) và `*.json` (bản chuẩn hóa để dựng ảnh).

```bash
python -X utf8 agent_run.py claude runs/claude-1 prompt.txt logs/claude-1 900
```

Giải thích: `python -X utf8` chạy Python ở chế độ UTF-8; `agent_run.py` là script bọc; `claude` là agent; `runs/claude-1` là thư mục làm việc; `prompt.txt` là file prompt; `logs/claude-1` là tiền tố file log; `900` là số giây tối đa.

### Bước 3. Thời gian và khối lượng

| | Claude Code (`claude-1`) | Antigravity `agy` (`agy-2`) |
|---|---|---|
| Thời gian chạy | 557 giây | 1.257 giây |
| Số lần gọi công cụ | 20 (10 lệnh shell, 9 sửa file, 1 ghi file) | 67 (34 lệnh, 28 ghi file, 4 đọc file, 1 sửa file) |
| File Python agent tự ghi | 1 script chính `doi_soat.py` (652 dòng) | 25 file Python (gồm cả script nháp), sau đó xóa bớt, còn `doi_soat.py` (570 dòng) |
| Token ghi trong log | output 80.370 (trong đó thinking 53.308) | input 270.441, output 130.911 |
| Chi phí log ghi | 1,51 USD (số của log Claude Code) | log `agy` không có số chi phí |

Hai số liệu không so trực tiếp được (hai công cụ tính token khác nhau). Chúng chỉ để bạn ước lượng tài nguyên.

![Claude Code đọc dữ liệu, viết script và chạy](anh/04-claude-lam-viec.webp)

*Dựng lại từ log thật của lần chạy `claude-1`, không phải ảnh chụp trực tiếp cửa sổ TUI. Đường dẫn máy đã được che (hiện là `~/bai-toan`).*

![Kết quả cuối Claude Code báo](anh/05-claude-ket-qua-cuoi.webp)

*Dựng lại từ log thật của lần chạy `claude-1`, không phải ảnh chụp trực tiếp cửa sổ TUI.*

![agy chạy script và tự kiểm đầu ra](anh/06-agy-lam-viec.webp)

*Dựng lại từ log thật của lần chạy `agy-2`, không phải ảnh chụp trực tiếp cửa sổ TUI. Tôi lược các dòng lỗi nhiễu của profile PowerShell trên máy chạy (xem mục lỗi).*

![Kết quả cuối agy báo](anh/07-agy-ket-qua-cuoi.webp)

*Dựng lại từ log thật của lần chạy `agy-2`, không phải ảnh chụp trực tiếp cửa sổ TUI.*

## 2. Các sự cố khi chạy (giữ nguyên, vì đây là phần giá trị)

1. **`agy` hết giờ ở lần chạy đầu (900 giây).** Hạn 900 giây trong quy ước của tôi không đủ: `agy` còn đang trong giai đoạn khám phá dữ liệu, chưa ghi được `bang_ghep.csv`. Script bọc ban đầu **không lưu log khi hết giờ**, nên lần đó không có log. Tôi giữ các file script nháp nó để lại ở `ket-qua/agy-lan1-timeout900/` và chạy lần hai (`agy-2`) với hạn 1.800 giây, có bọc lại để nếu hết giờ vẫn lưu log. Lần hai xong sau 1.257 giây. **Kết luận thực tế:** nếu bạn dùng chế độ `-p`, đặt giới hạn thời gian rộng hơn với dữ liệu cỡ này.
2. **Lần "lần 0" mất log do tôi.** Lần đầu tôi khởi chạy cả hai agent từ một lệnh nền mà tôi đóng ngay sau đó; nhiều khả năng vì vậy script bọc bị dừng trước khi ghi log (ngoài ra `agy` cũng vượt hạn 900 giây ở lần đó), dù agent vẫn chạy xong và để lại file kết quả. Tôi **không dùng** lần này làm kết quả chính vì không có log. Các file kết quả vẫn giữ ở `ket-qua/lan0-khong-co-log/` và vẫn được chấm để bạn thấy mức dao động giữa các lần chạy (mục 4).
3. **Claude Code gặp lỗi mã hóa Windows (cp1252) hai lần** khi in tiếng Việt từ một lệnh Python nhanh, rồi tự thêm `-X utf8`.
4. **Claude Code thử vá script bằng một lệnh dài, lệnh dừng giữa chừng vì không tìm thấy đúng đoạn cần thay.** Nó nhận ra chưa có thay đổi nào được ghi (log ghi rõ), rồi sửa từng chỗ bằng 9 lần Edit. Đây là hành vi mong muốn: kiểm lại trước khi tin.
5. **Dòng lỗi lạ trong log của `agy`**: mỗi lệnh đều kèm một đoạn lỗi về file profile PowerShell của máy chạy. Đó là nhiễu của máy, không liên quan bài toán. Nếu bạn gặp, bỏ qua.

## 3. Chấm bằng code

Agent tự báo cáo "đã đối soát xong" không đủ. Cần chấm bằng một thứ độc lập: **đáp án** sinh cùng dữ liệu.

```bash
cd ket-qua
python -X utf8 cham.py claude-1=claude-1 agy-2=agy-2
```

`cham.py` đọc `bang_ghep.csv`, `ngoai_le.csv`, `tong_kiem.json` trong mỗi thư mục và so với `dap-an.json`. Quy tắc:

- **Dòng "xác định" (130 dòng):** đúng khi tập mã đơn khớp **và** loại khớp (với ca trả nhiều đơn còn phải đúng phần phân bổ). Gồm cả 41 dòng chi, 4 dòng phí/lãi, ghép đủ, thiếu, thừa, trùng, hoàn tiền.
- **Dòng "mơ hồ" (14 dòng):** đạt khi agent ghi `CAN NGUOI QUYET` hoặc đưa dòng đó vào `ngoai_le.csv`. Không đạt mà ghép sai là "chắc sai"; không đạt mà ghép đúng là "đúng nhưng không báo".
- **Ngoại lệ:** so với 26 dòng đáp án coi là cần người xử lý; đếm bỏ sót và báo thừa.
- **Đơn chưa thu:** so tập mã đơn với 10 đơn đáp án.
- **Tổng kiểm:** so từng con số (số dòng, dư đầu, tổng có, tổng nợ, dư cuối, `kiem_so_du_khop`) với đáp án, kiểm thêm tổng theo loại cộng lại có bằng tổng ghi có không.
- **Mã đơn bịa:** mã không có trong sổ.

![Bảng điểm chấm](anh/09-bang-cham.webp)

*Dựng từ `ket-qua/bao-cao-cham.json`. Dữ liệu giả để học. n = 1 lần có log mỗi agent.*

### Kết quả tóm tắt **[Đo được]**

| Chỉ số | Claude Code (`claude-1`) | `agy` (`agy-2`) |
|---|---|---|
| Dòng xác định ghép đúng | 130/130 | 130/130 |
| Dòng mơ hồ được báo cho người quyết | 13/14 | 9/14 |
| Dòng mơ hồ ghép sai mà không báo | 0 | 0 |
| Ngoại lệ thật bắt được | 25/26 | 21/26 |
| Báo ngoại lệ thừa | 1 dòng | 0 |
| Đơn CK chưa thu: bắt đủ 10 đơn | có, liệt kê thừa 3 đơn | có, không thừa |
| Tổng kiểm (6 số) đúng | 6/6 | 6/6 |
| Mã đơn không có trong sổ | 0 | 0 |
| Tổng ghi có / ghi nợ / dư cuối | đúng cả ba | đúng cả ba |

Ghi chú để đọc đúng bảng:

- "130/130" hơi dễ nghe: 41 dòng là chi không liên quan đơn, và 24 dòng ghép bằng mã viết lệch hoặc tên. Cả hai agent đều xử lý được chữ O thay số 0, thiếu số 0, khoảng trắng, "don hang so 33".
- Cả hai agent đọc đúng **mọi** số tiền và chiều (có/nợ) của 144 dòng. Không dòng nào lệch.
- Con số "bao nhiêu tiền đã ghép đơn" **khác nhau giữa hai agent** (112.810.000 đ so với 113.720.000 đ), chênh đúng 910.000 đ. Nguyên nhân: ba dòng "sai mã đơn" (120.000 + 380.000 + 410.000 đ). Claude Code xếp ba dòng này vào "không rõ nguồn, cần người quyết" và không tính vào "đã ghép"; `agy` vẫn tính vào "khớp đủ" (nhưng đưa sang ngoại lệ). Cả hai đều hợp lý, nhưng **con số tổng phụ thuộc quy ước**. Hệ quả: nếu bạn so hai báo cáo, hãy so theo quy ước chứ đừng so mỗi con số.

![Ca hai agent xử lý khác nhau](anh/10-ca-khac-nhau.webp)

*Dựng từ `ket-qua/claude-1`, `ket-qua/agy-2` và đáp án `ket-qua/dap-an.json`. Dữ liệu giả để học.*

## 4. Các ca đáng xem

**Ba dòng ghi sai mã đơn (đúng ra phải để người quyết).** Ví dụ `DANG KIM MAI CK DH2610-054`, 120.000 đ: mã chỉ tới đơn của khách khác (khác số tiền), còn tên và số tiền lại khớp đúng đơn khác. **Cả hai agent đều không tự chốt, đều ghi `CAN NGUOI QUYET` và nêu đơn ứng viên.** Đây là đúng điều bài toán muốn.

**Sáu dòng không rõ nguồn.** Cả hai đều ghi `CAN NGUOI QUYET`, kể cả dòng `MUA HANG ZALO` 560.000 đ (ghi ngày 27/10) trùng đúng tổng đơn `DH2610-121` chưa thu (đặt ngày 30/10, tức sau ngày dòng tiền vào). `agy` nêu `DH2610-121` làm ứng viên nhưng không ghép; Claude Code không nêu đơn nào, vì nhận ra dòng tiền vào trước ngày đặt đơn. Cả hai cách đều không ghép bừa.

**Hai dòng COD gộp (4.220.000 và 3.530.000 đ).** Cả hai agent tìm ra đúng tập 5 và 6 đơn COD có tổng bằng số tiền (tìm bằng code). Tập tìm được **trùng đáp án**. Nhưng:
- Claude Code ghi `TRUNG BINH`, đưa vào ngoại lệ, và nói trong báo cáo cần đối chiếu bảng kê của hãng vận chuyển.
- `agy` ghi `CAO` và **không** đưa vào ngoại lệ. Nội dung sao kê không có mã đơn nào; căn cứ chỉ là "tổng bằng nhau và các đơn liên tiếp". Dữ liệu thật có thể có nhiều tổ hợp đơn cho cùng một tổng, nên "CAO" ở đây là tự tin hơn mức bằng chứng cho phép. Lần này nó đoán đúng, nhưng prompt đã dặn "chỉ dùng CAO khi mã đơn và số tiền đều khớp rõ ràng".

**Hai khách cùng tên Trần Văn Bình, hai đơn cùng 920.000 đ.** Nội dung chỉ có tên. Cả hai agent đều ghép dòng đến trước vào đơn đặt trước (`DH2610-066`) và dòng sau vào đơn sau (`DH2610-101`), ghi `TRUNG BINH`. Claude Code đưa hai dòng vào ngoại lệ; `agy` không. Đáp án sinh dữ liệu cho biết cách ghép của cả hai **trùng với đáp án thật**, nhưng bạn không thể biết điều đó nếu chỉ có sao kê và sổ đơn. **[Đo được]** chỉ một mẫu; đừng coi "đoán theo thứ tự ngày" là quy tắc an toàn.

**Một dòng trả hai đơn không ghi mã (`TRAN HUU DAT CK 2 don`).** Tổng bằng hai đơn của cùng một khách, cả hai ghép đúng cặp đơn, ghi `TRUNG BINH`, không báo ngoại lệ. Đáp án muốn người xác nhận.

**Báo thừa của Claude Code.** Dòng `don 003 HOANG KIM VY` có đúng mã và đúng tiền, nhưng người chuyển tên khác khách trên đơn. Claude Code ghi `TRUNG BINH` và đưa vào ngoại lệ để hỏi lại khách. Đó là thận trọng quá mức so với đáp án, nhưng chi phí chỉ là một câu hỏi. Tốt hơn là thừa một dòng hơn là thiếu một dòng.

**Liệt kê thừa 3 đơn chưa thu của Claude Code.** Ba đơn này là ứng viên của ba dòng "sai mã". Claude Code liệt kê chúng là "đơn chưa có tiền" kèm ghi chú. Về logic là đúng (chúng thật sự chưa có dòng nào được ghép chắc chắn), nhưng đáp án chỉ tính 10 đơn.

## 5. Một điều quan trọng về script (không thấy trong điểm số)

Điểm chấm đo **kết quả**. Nhưng bạn dùng lại **script** mỗi tháng, nên phải đọc script.

- Script của Claude Code (`ket-qua/claude-1/doi_soat.py`) là quy tắc tổng quát: biểu thức chính quy rút mã đơn, so tên, so tiền. Tiền tố tháng `DH2610` được viết cứng ở vài chỗ (biểu thức rút mã và hàm tạo mã; sang tháng 11 phải đổi thành `DH2611`).
- Script cuối của `agy` (`ket-qua/agy-2/doi_soat.py`) có **38 nhánh `so_ct == "..."` viết cứng**, cùng mã đơn và các chuỗi phân bổ tiền gõ sẵn (ví dụ danh sách mã và số tiền của hai đợt COD). Tức là agent khám phá kết quả bằng nhiều script nháp, rồi **dán kết quả vào script cuối** thay vì để script tự suy ra. Số tiền ở các dòng đó đúng (chấm cho thấy phân bổ cộng đúng bằng số tiền), nhưng:
  - Chạy lại với sao kê tháng sau sẽ **không** cho kết quả đúng.
  - Các con số phân bổ này không còn do code tính ở lần chạy cuối. Đây là điểm sát với nguyên tắc "tiền do code làm, không do mô hình ghi" nhất trong cả bài.
  Phần tổng kiểm (cộng tổng, so số dư) vẫn do code tính.

Vì vậy, **chấm kết quả chưa đủ để tin script**. Cách kiểm đơn giản: tìm trong script các chuỗi như `so_ct ==` hoặc các dãy số 8 chữ số.

## 6. Mức dao động giữa các lần chạy

Tôi còn hai lần chạy "lần 0" không có log (xem mục 2). Chúng được chấm bằng cùng `cham.py`. **[Đo được, không log]** Claude Code: dòng mơ hồ báo 10/14, ngoại lệ 22/26 (lần có log là 13/14 và 25/26); `agy`: 9/14 và 21/26 (trùng lần có log). Dòng xác định đều 130/130, tổng kiểm đều 6/6. Điều này chỉ cho thấy phần "xác định" ổn trong hai lần mỗi agent, còn phần "mơ hồ" thì mức thận trọng thay đổi giữa các lần. Với 2 lần chạy mỗi bên, **không đủ để nói gì về độ ổn định**.

## Lỗi thường gặp (và cách xử)

| Triệu chứng | Nguyên nhân thường gặp | Cách xử |
|---|---|---|
| Agent báo "xong" nhưng thiếu file | Hết giờ giữa chừng | Tăng giới hạn thời gian; kiểm danh sách file ra |
| Dòng tổng bị tính như giao dịch | Prompt không nói file có dòng tổng | Giữ câu này ở bước 1 |
| Tổng "đã ghép" của hai lần không khớp nhau | Quy ước xếp ca mơ hồ khác nhau | Ghi quy ước vào prompt |
| `UnicodeEncodeError` | Windows dùng cp1252 | Thêm `-X utf8` |
| Kết quả đúng nhưng chạy lại tháng sau sai | Script viết cứng ca cụ thể | Đọc script; yêu cầu "không viết cứng số CT hay mã đơn" |

## Checklist cuối bài 2

- [ ] Mỗi agent chạy trong thư mục riêng, file đầu vào không bị sửa (so mã băm).
- [ ] Có log gốc `*.raw.jsonl` của mỗi lần chạy.
- [ ] Đã chạy `cham.py` và đọc cả phần "mơ hồ", không chỉ phần tổng.
- [ ] Đã mở script cuối, tìm các chuỗi viết cứng.
- [ ] Đã ghi quy ước xếp ca mơ hồ trước khi so hai báo cáo.

## Việc cần người làm

- Quyết định từng dòng `CAN NGUOI QUYET` (hỏi khách, xem bảng kê hãng vận chuyển).
- Xác nhận với kế toán trưởng cách xử lý chuyển thiếu, chuyển thừa, chuyển hai lần: hoàn tiền, trừ vào đơn sau, hay giữ chờ. Đó là quy trình của công ty, không phải việc của agent. Quy định về chứng từ, hóa đơn và kỳ hạch toán: cần kiểm với kế toán/luật sư, bài này không viết điều khoản.
- Đọc script ít nhất một lần trước khi dùng cho tháng sau.

## Giới hạn

- n = 1 lần chạy có log mỗi agent (cộng 1 lần không log). Không so được độ ổn định, và không kết luận agent nào tốt hơn.
- Đáp án là của chính dữ liệu tôi sinh; các quyết định "mơ hồ" do tôi gán nhãn. Một kế toán khác có thể gán khác (ví dụ chấp nhận ghép theo thứ tự ngày với hai khách trùng tên).
- Hạn `agy` bị tôi nới từ 900 giây lên 1.800 giây ở lần có log; kết quả `agy` thuộc về cấu hình này.
- Chưa thử dữ liệu có nội dung bị ngân hàng cắt ngắn, thêm tiền tố mã của ngân hàng, hoặc sao kê Excel nhiều sheet.
