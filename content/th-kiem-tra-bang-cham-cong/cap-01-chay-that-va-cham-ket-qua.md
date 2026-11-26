# Bài 2. Chạy thật hai agent, rồi chấm bằng đáp án

!!! info "Bài này"
    - **Bạn làm gì:** mở kết quả thật của Claude Code và Antigravity (`agy`) trên cùng dữ liệu ẩn danh, chấm bằng bộ chấm có sẵn, đọc các ca agent làm khác đáp án, rồi rà xem agent có chạy lệnh ngoài thư mục không.
    - **Mất bao lâu:** khoảng 30 phút để làm theo. Đọc kỹ các ca khác đáp án thêm 15 phút.
    - **Cần có:** thư mục bài đã giải nén (có `ket-qua/` và `logs/`), Python 3, Excel hoặc Notepad. Không cần chạy lại agent.
    - **Kết quả:** bạn trả lời được bằng số: agent tìm đúng bao nhiêu trong 61 bất thường đã cài, báo oan bao nhiêu, bao nhiêu ô khớp đáp án, và chỗ nào khác là do lỗi tính hay do quy định chưa rõ.

> Dữ liệu giả (xem bài 1). Mọi số trong bài là kết quả chạy của chúng tôi ngày 2026-11-20, **n = 1 đến 2 lần mỗi cấu hình**: đây là quan sát, chưa đo được độ ổn định, không đủ để xếp hạng agent.

**[Đo được]** (cùng prompt nguyên văn của bài 1, cùng dữ liệu ẩn danh):

| Agent | Số lần chạy | Bất thường tìm đúng | Trạng thái ngày đúng | Người đúng cả 11 cột | Thời gian (lần có đo) |
|---|---|---|---|---|---|
| Claude Code | 3 | 61/61 cả 3 lần, bịa 0 | 750/750 cả 3 lần | 25/25 cả 3 lần | 247,8 và 326,1 giây |
| `agy` | 4 | 61/61 cả 4 lần, bịa 0 | 750, 750, 747, 747 | 25, 25, 23, 22 | 1.217,6 và 1.126,8 giây; một lần hết giờ 900 giây |

Chi tiết từng lần ở phần Đào sâu cuối bài.

## Các bước làm

### Bước 1. Xem agent đã làm gì

Cả hai agent làm đúng thứ tự mong muốn: đọc quy định, xem cấu trúc dữ liệu, viết `tinh_cong.py`, chạy, tự kiểm rồi viết báo cáo. Chạy lệnh thật trên Windows, mỗi lần chạy ở một thư mục riêng chỉ có 5 tệp ẩn danh của bài 1. Cách chạy không tương tác ở phần Đào sâu bài 1.

![Claude Code đọc quy định và xem dữ liệu](anh/04-claude-dang-lam.webp)

*Dựng lại từ log thật của lần chạy `claude-lan1`, không phải ảnh chụp trực tiếp cửa sổ TUI. Đường dẫn máy đã được thay bằng `<thu-muc-lam-viec>` hoặc `<user>`.*

Claude Code đếm các kiểu giờ trong dữ liệu trước khi viết code (máy A dạng `yyyy-mm-dd`, máy B dạng `dd/mm/yyyy`), tìm ra 2 dòng hỏng (giờ trống, ngày 31/09) và 1 mã lạ. Cuối ảnh là **lỗi thật đầu tiên**: chương trình in tiếng Việt ra màn hình Windows và gặp `UnicodeEncodeError`. Agent tự nhận ra, đặt đầu ra sang UTF-8, rồi kiểm tay 7 ngày đối chiếu với dữ liệu thô. Lỗi nằm ở khâu in, không phải ở số liệu (các CSV đã ghi đúng trước khi lỗi); nếu bạn dừng ở dòng "Exit code 1" thì sẽ tưởng cả chương trình hỏng.

![Claude Code, tóm tắt cuối](anh/06-claude-ket-qua-cuoi.webp)

*Dựng lại từ log thật của lần chạy `claude-lan1`.*

Tóm tắt cuối của Claude Code đưa số dòng từng tệp, số bất thường theo loại, và **các quyết định tự chọn ở chỗ quy định không nói rõ** (ví dụ mọi đơn "đã duyệt" đều ghi PHEP). Đây là phần có giá trị nhất với người duyệt.

`agy` làm lâu hơn nhiều và thăm dò nhiều hơn:

![agy thăm dò dữ liệu bằng nhiều script nhỏ](anh/07-agy-dang-lam.webp)

*Dựng lại từ log thật của lần chạy `agy-lan2`.*

Trong `agy-lan2`, agent viết khoảng 14 script thăm dò (`inspect_*.py`, `check_*.py`, `verify_*.py`) trước khi viết `tinh_cong.py`, rồi xóa chúng ở cuối. Thời gian chênh nhau rõ nhưng **không kết luận gì về chất lượng**: lúc chạy máy còn nhiều tiến trình `agy` khác, nên thời gian bị nhiễu.

### Bước 2. Mở kết quả của agent

Mở thư mục `ket-qua/claude-lan1/`. Mỗi lần chạy để lại ba CSV, một `bao_cao.md` và `tinh_cong.py`. Mở `bat_thuong.csv` bằng Excel: cột `chi_tiet` do **code tính**, cột `giai_thich` do mô hình viết (một lần, khi viết code).

![Dòng bảng công ngày và bất thường trích từ đầu ra](anh/10-ket-qua-bang-cong-bat-thuong.webp)

*Trích đầu ra thật của `claude-lan1` (dữ liệu giả, mã ẩn danh).*

!!! see "Bạn sẽ thấy"
    `bang_cong_ngay.csv` 750 dòng (25 người x 30 ngày), `bat_thuong.csv` 61 dòng, `tong_hop_nguoi.csv` 25 dòng. Nhưng **đừng tin vì "trông đủ"**: sang bước 3.

### Bước 3. Chấm bằng bộ chấm

`ket-qua/cham.py` so ba tệp của agent với `ket-qua/dap-an.json` (đáp án do bộ tính tham chiếu tính ra, mã đã ẩn danh). Cách chấm: (1) bất thường khớp theo bộ ba (mã NV, ngày, loại): *đúng*, *bỏ sót*, hoặc *bịa* (agent báo mà đáp án không có); (2) `can_nguoi_quyet` đúng quy ước; (3) bảng công ngày: 750 trạng thái, và với 501 ngày OK so từng cột; (4) tổng hợp 25 người, 11 cột; (5) "đoán số": ngày lẽ ra để trống mà agent vẫn điền giờ công.

Chấm một lần chạy. Windows (PowerShell) và macOS, Linux dùng cùng lệnh, đổi `\` thành `/` nếu cần:

```lenh
python -X utf8 ket-qua\tom_tat_cham.py ket-qua\claude-lan1
```

`tom_tat_cham.py` gọi `cham.py` rồi in một dòng tóm tắt.

```ketqua
claude-lan1            bất thường 61/61 (bịa 0) | trạng thái ngày 750/750 | người đúng hết cột 25/25
```

Xem bảng cả bảy lần chạy:

```lenh
python -X utf8 ket-qua\tom_tat_cham.py
```

```ketqua
claude-lan0-mat-log    bất thường 61/61 (bịa 0) | trạng thái ngày 750/750 | người đúng hết cột 25/25
claude-lan1            bất thường 61/61 (bịa 0) | trạng thái ngày 750/750 | người đúng hết cột 25/25
claude-rutgon          bất thường 61/61 (bịa 0) | trạng thái ngày 750/750 | người đúng hết cột 25/25
agy-lan0-mat-log       bất thường 61/61 (bịa 0) | trạng thái ngày 750/750 | người đúng hết cột 25/25
agy-lan1-het-gio       bất thường 61/61 (bịa 0) | trạng thái ngày 750/750 | người đúng hết cột 25/25
agy-lan2               bất thường 61/61 (bịa 0) | trạng thái ngày 747/750 | người đúng hết cột 23/25
agy-rutgon             bất thường 61/61 (bịa 0) | trạng thái ngày 747/750 | người đúng hết cột 22/25
```

![Bảng chấm điểm các lần chạy](anh/11-cham-diem-cac-lan-chay.webp)

*Kết quả chạy `cham.py` trên bảy bộ đầu ra, ngày 2026-11-20 (n = 1 mỗi dòng).*

!!! see "Bạn sẽ thấy"
    - Cả bảy lần: **61/61 bất thường, 0 bỏ sót, 0 bịa**, `can_nguoi_quyet` đúng 61/61. Các "bẫy giống lỗi mà không phải lỗi" (quẹt cách 4 phút, trễ đúng 5 phút, làm thêm 29 phút, người làm thêm 36,18 giờ sát ngưỡng, quẹt 4 lần vì nghỉ trưa) **không bị báo oan**.
    - Ba ca một quẹt giữa ca đều được gắn `THIEU_KHONG_RO` và đưa cho người quyết, không đoán vào hay ra.
    - Bảng ngày và bảng người: 5 trong 7 lần khớp tuyệt đối; hai lần của `agy` lệch (bước 4). Chưa lần nào có lỗi cộng trừ giờ phút.

!!! stuck "Gặp lỗi?"
    - **"Không thấy tệp" (`FileNotFoundError`):** chạy lệnh từ thư mục bài (nơi có `ket-qua/`), không phải từ bên trong `ket-qua/`.
    - **Chữ tiếng Việt vỡ khi in:** quên `-X utf8`.
    - **Muốn chấm kết quả của chính bạn:** chép ba CSV vào một thư mục mới, chạy `tom_tat_cham.py <thư mục đó>`. Đáp án chỉ đúng với bộ dữ liệu của bài.

### Bước 4. Đọc các ca khác đáp án

Hai lần của `agy` lệch đáp án. Lệch không phải do cộng trừ sai mà do **cách hiểu quy định**. Mở `bang_cong_ngay.csv` của `agy-lan2` và `agy-rutgon`, lọc `ma_nv`, và so với `claude-lan1`:

| Agent làm gì | Đúng ra | Vì sao đáng chú ý |
|---|---|---|
| `agy-lan2`: ghi thứ Bảy 05/09 và Chủ nhật 06/09 nằm giữa đơn nghỉ ốm của NV-009 là `PHEP` (cũng một ngày OFF nằm trong đơn khác): 3 ô trạng thái và 2 ô `so_ngay_phep` lệch (3 so với 5; 1 so với 2) | `NGHI` (ngày nghỉ sẵn) | Câu 5.7 do chúng tôi viết ("ngày nằm trong đơn nghỉ phép đã duyệt và không có quẹt: PHEP") không nói rõ có tính ngày nghỉ hay không. Agent đọc theo nghĩa đen và còn ghi vào báo cáo là chỗ cần chuyên gia nhân sự xem. **Chỗ mơ hồ nằm ở quy định, không ở agent** |
| `agy-rutgon`: ngày làm thêm quá 3 giờ (NV-010 ngày 28/09, NV-013 ngày 26/09, NV-025 ngày 10/09) để `CHO_XAC_NHAN` và **bỏ trống giờ công cả ngày** | Trạng thái OK, 8 giờ công thường, phần làm thêm ghi riêng | Khi bỏ phần "cách tính" khỏi quy định, agent tự suy ra. Hậu quả: NV-010 chỉ 17 ngày công thay vì 18, tổng giờ công 136 thay vì 144, làm thêm 0 thay vì 3,78 giờ. Dùng thẳng bảng này mà không đọc danh sách bất thường thì người lao động **thiếu công**. Agent có ghi quy ước này trong báo cáo, nên không phải bịa |
| `claude-rutgon`: trả đúng cả 750 ô | | Nó **liệt kê giả định** mà quy định bỏ ngỏ (cách tính giờ công, trễ) và đánh dấu hai điều chưa chắc. Quy định chặt thì các lần chạy giống nhau; quy định thiếu thì ba cách xử lý khác nhau lộ ra: **người duyệt phải đọc mục "giả định"** |

Xem nhanh ba ngày làm thêm của `agy-rutgon` so với `claude-lan1` (cột `gio_cong` trống so với 8.00):

```ketqua
claude-lan1  :  NV-010,2026-09-28,HC,07:59,20:47,8.00,0,0,227,OK
agy-rutgon   :  NV-010,2026-09-28,HC,07:59,20:47,,0,0,227,CHO_XAC_NHAN
```

### Bước 5. Rà xem agent có chạy lệnh ngoài thư mục không

Prompt ghi "Chỉ đọc và ghi trong thư mục hiện tại". Trong lần `agy-lan2`, agent chạy hai lệnh ngoài thư mục: `git log -n 5` (báo "not a git repository") và `dir ..\..` (liệt kê thư mục cha của thư mục cha). Hai lệnh chỉ đọc, không sửa gì, nhưng **trái ràng buộc trong prompt**.

![agy chạy git log và dir ..\..](anh/08-agy-ra-ngoai-thu-muc.webp)

*Dựng lại từ log thật của lần chạy `agy-lan2`. Hai dòng đầu mỗi khối là lỗi hồ sơ PowerShell trên máy chạy, không liên quan tới bài.*

Tự rà log bằng một lệnh. Windows (PowerShell), chạy trong thư mục bài:

```lenh
Select-String -Path logs\*.json -Pattern "git log" -SimpleMatch
```

macOS hoặc Linux: `grep -n "git log" logs/*.json`.

```ketqua
logs\agy-lan2.json:294:    "CommandLine": "git log -n 5"
```

!!! warning "Câu dặn trong prompt không phải hàng rào"
    `agy` chạy với `--dangerously-skip-permissions` là **toàn quyền trên máy**. Trong log của Claude Code và `agy-rutgon` chúng tôi không thấy lệnh tương tự (hai lần `lan0` và `agy-lan1` không có log nên không kiểm được). Với dữ liệu nhân sự, cách an toàn là chạy agent trong thư mục tách biệt (hoặc máy ảo, tài khoản riêng), chỉ để dữ liệu đã ẩn danh ở đó, và rà log sau mỗi lần chạy.

## Lỗi thường gặp khi chạy và chấm

| Triệu chứng | Cách xử lý |
|---|---|
| Chạy trên thư mục có cả đáp án hoặc bảng mã hóa | Agent đọc được là chấm vô nghĩa. Mỗi lần chạy một thư mục riêng, chỉ có 5 tệp ẩn danh |
| Chỉ đọc "tóm tắt cuối" mà không mở `bat_thuong.csv` | Tóm tắt của cả hai agent khớp số liệu, nhưng đó là điều phải kiểm bằng bộ chấm |
| Chạy lại prompt đã chỉnh cho "đẹp hơn" và chỉ giữ lần cuối | Giữ nguyên prompt cho mọi lần, hoặc giữ cả hai bản và ghi đã sửa gì |
| Không có log để rà | Ghi log ra tệp **ngay khi chạy**, kể cả khi hết giờ |
| Tin bộ chấm chưa thử | Thử bộ chấm bằng "đầu ra hoàn hảo" (phải 100%) và "đầu ra sửa tay" (phải bắt được) trước khi tin |
| Đọc log không ra vì đường dẫn máy | Xem `logs/*.json` (đã che đường dẫn) |

## Checklist

- [ ] Mỗi lần chạy ở thư mục riêng, không có đáp án.
- [ ] Đã chạy `tom_tat_cham.py` và đọc đúng 3 con số: bất thường đúng, ngày đúng, người đúng.
- [ ] Đã đọc mục "giả định" và "điều chưa chắc" trong `bao_cao.md`.
- [ ] Đã rà log tìm lệnh ngoài thư mục (`..`, `git`, đường dẫn tuyệt đối).
- [ ] Không có ngày `CHO_XAC_NHAN` nào bị dùng làm công 0 giờ khi chưa được người xác nhận.

## Việc cần người làm

- Người làm lương: mở `bat_thuong.csv`, xử lý từng dòng `can_nguoi_quyet = CO`; ngày `CHO_XAC_NHAN` chưa tính giờ nên phải xác nhận trước khi tính lương.
- Quản lý trực tiếp: xác minh các ca `NGHI_QUET_HO` (chỉ là dấu hiệu, không phải kết luận), ca vắng chưa ghi, làm ngày lễ hay ngày nghỉ.
- Chủ doanh nghiệp: quyết cách hiểu cho chỗ quy định chưa rõ (ngày nghỉ nằm trong đơn phép; ngày làm thêm quá ngưỡng có tính giờ thường không) rồi **viết vào quy định**.

## Giới hạn

- n rất nhỏ: mỗi cấu hình 1 đến 2 lần (hai cấu hình có thêm lần mất log). Chưa đo được độ ổn định; không có cơ sở nói agent nào tốt hơn.
- Dữ liệu sạch hơn thực tế; đáp án và quy định do cùng người viết nên có thể đã ngầm làm đề dễ hơn.
- Bảy lần đều sát đáp án vì quy định có ngưỡng và cách tính cụ thể; thất bại có nhiều khả năng hơn khi quy định mơ hồ hoặc dữ liệu có lỗi lạ chưa cài (giờ máy lệch, ca qua đêm).
- Bộ chấm và đáp án do chúng tôi viết; chúng đã được thử bằng đầu ra hoàn hảo và đầu ra sửa tay, nhưng chưa được ai ngoài nhóm kiểm.

## Đào sâu: chi tiết từng lần chạy, mất log và những điều bất ngờ

### Cách chạy và bảy lần chạy

Phiên bản đọc từ log: Claude Code 2.1.329, mô hình `claude-sonnet-5-5`; Antigravity CLI `agy` 1.5.13 (log `agy` không ghi tên mô hình nên bài không nêu). Lệnh dùng:

```lenh
claude -p "<nội dung prompt>" --output-format stream-json --verbose --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash"
agy -p "<nội dung prompt>" --output-format stream-json --dangerously-skip-permissions
```

`--output-format stream-json` in từng sự kiện thành một dòng JSON (để lưu log gốc); `--allowedTools` giới hạn công cụ của Claude Code; `--dangerously-skip-permissions` của `agy` là **không hỏi xin phép** khi chạy lệnh.

| Lần | Agent | Quy định đưa cho agent | Thời gian | Log |
|---|---|---|---|---|
| claude-lan0 | Claude Code | đầy đủ | không đo (khoảng 6 phút theo giờ tệp) | **mất** |
| claude-lan1 | Claude Code | đầy đủ | 247,8 giây, 16 lượt | có |
| claude-rutgon | Claude Code | rút gọn (bỏ mục 5 "cách tính") | 326,1 giây, 20 lượt | có |
| agy-lan0 | `agy` | đầy đủ | không đo (khoảng 16 phút theo giờ tệp) | **mất** |
| agy-lan1 | `agy` | đầy đủ | **hết giờ 900 giây** (đã ghi xong 3 CSV, chưa ghi báo cáo) | **mất** |
| agy-lan2 | `agy` | đầy đủ | 1.217,6 giây | có (giới hạn 1.800 giây) |
| agy-rutgon | `agy` | rút gọn | 1.126,8 giây | có (giới hạn 1.800 giây) |

Hai cấu hình "rút gọn" là thử thêm: chúng tôi bỏ phần hướng dẫn cách tính chi tiết khỏi `quy_dinh_cong_ty.md` (vẫn giữ bảng ngưỡng ở mục 4 và danh sách mã), **prompt không đổi**, để xem điều gì xảy ra khi quy định viết thiếu.

![Claude Code tự kiểm và sửa lỗi in tiếng Việt](anh/05-claude-tu-kiem.webp)

*Dựng lại từ log thật của lần chạy `claude-lan1`.*

![agy, tóm tắt cuối](anh/09-agy-ket-qua-cuoi.webp)

*Dựng lại từ log thật của lần chạy `agy-lan2`.*

### Mất log, hết giờ

Hai lần đầu chúng tôi gọi lệnh chạy bằng cách làm tiến trình bị cắt khi lệnh gọi kết thúc, nên log gốc của `claude-lan0` và `agy-lan0` không được ghi; `agy-lan1` chạm giới hạn 900 giây và công cụ `agent_run.py` khi hết giờ không lưu phần đã chạy. Chúng tôi **giữ nguyên các tệp kết quả** của ba lần này và chấm chúng, nhưng không có log để dựng ảnh. Đây là lỗi của người chạy: luôn ghi log ra tệp ngay khi chạy. Với `agy` nên đặt giới hạn 1.800 giây cho bài này, hoặc yêu cầu agent ghi báo cáo trước khi tinh chỉnh.

### Báo cáo dài hơn yêu cầu, và chi tiết agent tự thêm

- **[Đo được]** Số từ `bao_cao.md` (prompt ghi "tối đa một trang"): Claude Code 616 và 644 (hai lần có log), `agy` 1.322 và 1.332. Dài hơn gần gấp đôi; muốn đúng một trang thì phải đo số từ ngay trong bước tự kiểm.
- Trong tóm tắt cuối của `agy-lan2`, agent gọi ngày 01 và 02/09 là "ngày Quốc khánh" (quy định chỉ nói "ngày lễ do công ty khai báo"), đề nghị "trích xuất camera" để xác minh quẹt hộ và nhắc trợ cấp ốm đau BHXH. Không phải điều luật, nhưng là chi tiết agent **tự thêm**: người duyệt cần biết để không tin như thể nằm trong dữ liệu. Prompt dặn "không kết luận quẹt hộ": cả hai agent giữ đúng (chỉ nêu dấu hiệu).
- Mã lạ được cả hai gắn `DU_LIEU_LOI` đúng: không ai cố gán nó cho một nhân viên.

### Bộ chấm đã được thử trước

Đưa thẳng đáp án vào làm "đầu ra giả" thì `cham.py` chấm ra đúng tuyệt đối; sửa tay vài ô thì bắt được (59/61 khi xóa 2 dòng bất thường, 498/501 khi sửa 3 ô phút trễ). Hãy làm bước này với bộ chấm của bạn trước khi tin nó.

### Chi phí và token

Giá trị `cost_usd` trong log Claude Code (0,746 và 0,976 USD cho hai lần có log) là con số công cụ báo, không phải hóa đơn. `agy` báo số token (khoảng 238 nghìn vào, 118 nghìn ra ở lần 2; 230 nghìn và 116 nghìn ở lần rút gọn), không báo tiền.
