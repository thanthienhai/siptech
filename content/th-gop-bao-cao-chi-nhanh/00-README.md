# Bài toán 08: Gộp báo cáo doanh thu từ nhiều file Excel của chi nhánh

> **Dữ liệu trong bài toán này là dữ liệu GIẢ để học.** Công ty "Mẫu An Phát", 6 chi nhánh, mã hàng, số chứng từ, số tiền đều do chương trình `du-lieu/sinh_du_lieu.py` bịa ra (hạt giống cố định). Không có dữ liệu của doanh nghiệp thật. Mọi con số gắn nhãn **[Đo được]** (kết quả chạy của chúng tôi, ngày 2026-11-20 và 2026-11-21, n nhỏ), **[Nguồn]** (có link) hoặc **[Đề xuất]** (ý kiến).

## Bạn làm được gì sau bài toán này

Công ty có vài chi nhánh hoặc đại lý. Cuối tháng, mỗi nơi gửi một file Excel doanh thu, mỗi nơi một kiểu: tiêu đề nằm dòng 7, ô ngày gộp, số tiền là chữ `1.250.000đ`, ngày `10/05/2026` mà không ai biết là mùng 5 tháng 10 hay mùng 10 tháng 5. Sau bốn bài bạn sẽ:

- giao việc gộp 6 file đó cho một coding agent (Claude Code hoặc Antigravity `agy`) theo hướng **"agent viết một script, script mới là thứ tính tiền"**;
- **chứng minh được file gốc không bị sửa** (so mã băm trước và sau) và kiểm kết quả bằng đáp án và bằng một lần kiểm chéo độc lập;
- hằng tháng chạy lại script bằng một lệnh, không gọi agent, và biết **gọi agent đúng lúc** khi một chi nhánh đổi định dạng;
- có bộ prompt dùng lại (giải thích script, soạn email hỏi chi nhánh, thêm chi nhánh mới...) và ba bài tập tự kiểm.

Ba nguyên tắc xuyên suốt:

1. **Không sửa file gốc.** File chi nhánh gửi là chứng cứ. Mọi thứ agent tạo ra nằm ở thư mục khác; ta so mã băm (SHA-256) trước và sau để chứng minh.
2. **Số do code tính.** Agent không "nhẩm" tổng: nó viết `gop.py`, chạy, và chỉ báo cáo con số script in ra.
3. **Không chắc thì ghi CẦN NGƯỜI QUYẾT.** Ngày `10/09/2026` có thể là mùng 10 tháng 9 hoặc mùng 9 tháng 10: không có căn cứ thì để người quyết, không đoán thầm.

## Bốn bài

| Bài | Nội dung | Mất bao lâu | Kết quả |
|---|---|---|---|
| [Bài 1](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | Xem 6 file lộn xộn, chụp mã băm, dựng thư mục an toàn, dán prompt giao việc | Khoảng 30 phút + agent chạy 12 đến 17 phút | `gop.py` và `ra/` gồm 7 file |
| [Bài 2](cap-01-chay-that-va-kiem-tra-ket-qua.md) | Chứng minh file gốc không đổi, chấm bằng đáp án, đọc bảng kiểm tra tổng và các ca agent làm sai | Khoảng 30 phút | Biết agent đúng bao nhiêu dòng, lệch ở đâu là hợp lý |
| [Bài 3](cap-02-dua-vao-dung-hang-thang.md) | Chạy lại script cho tháng mới (không gọi agent), quét "chữ của tháng cũ", agent sửa script khi định dạng đổi | Khoảng 30 phút mỗi tháng | Quy trình hằng tháng 5 bước và bộ hồi quy |
| [Bài 4](cap-03-prompt-mau-va-bai-tap.md) | 9 prompt dùng lại, 3 bài tập (thêm chi nhánh, đổi tên cột, báo cáo theo tuần), dùng với dữ liệu thật | Mỗi bài tập 20 đến 40 phút | Bộ prompt đã thử và tiêu chí đạt kiểm bằng lệnh |

## Kết quả đo, tóm tắt

Dữ liệu giả, mỗi tình huống chạy 1 lần hợp lệ (n=1). Không rút ra kết luận "agent nào tốt hơn".

| Tình huống | Claude Code | Antigravity (`agy`) |
|---|---|---|
| Bài 2: tháng 10, 6 file (đáp án 901 dòng + 3 dòng ngày mơ hồ) | 901/901 đúng, tổng 6/6 chi nhánh đúng, 718 giây, 37 lượt | 901/901, 6/6, 1.045 giây |
| Bài 2: 3 dòng ngày mơ hồ (HP `10/09/2026`) | Để trống ngày + CẦN NGƯỜI QUYẾT, 3/3 | 3/3 |
| Bài 2: file gốc | Nguyên vẹn (mã băm không đổi) | Nguyên vẹn |
| Bài 3: chạy lại script cũ cho tháng 11 (6 file cùng định dạng) | 877/877 đúng; chữ giải thích sạch | 877/877 đúng, **nhưng** in mã chứng từ và số tiền của tháng 10 trong `kiem_tra.csv` và `bao_cao.md`; nhãn khác cho 3 dòng ngày mơ hồ |
| Bài 3: tháng 11, NT đổi định dạng, chạy script cũ | Dừng, mã thoát 2, thông báo tiếng Việt | Dừng, mã thoát 1, `ValueError` |
| Bài 3: agent sửa script, rồi chạy lại 3 bộ (T11 mới, T11 cũ, T10) | 264 giây; 877/877, 877/877, 901/901 | 1.008 giây; 877/877, 877/877, 901/901 |
| Bài 4: 6 prompt chạy thật (Claude Code, n=1) | 33 đến 477 giây; thêm chi nhánh thứ bảy: 1025/1025 và 7/7, ĐẠT; đổi tên cột: 877/877, ĐẠT; kiểm chéo: 6/6 số khớp đáp án | Chưa chạy |

**Điều cần nhớ:** chấm đúng số tiền **chưa đủ**. Ở bài 3, script của `agy` ra số đúng mà chữ giải thích vẫn là của tháng cũ; chỉ đọc chữ hoặc quét mã tháng cũ mới thấy.

## Cấu trúc thư mục

```
08-gop-bao-cao-chi-nhanh/
  00-README.md, bai-1-..., bai-2-..., bai-3-..., bai-4-...
  du-lieu/
    sinh_du_lieu.py            sinh dữ liệu giả (seed cố định)
    sinh_bai_tap.py            sinh dữ liệu cho 3 bài tập ở bài 4 (seed cố định)
    prompt-giao-viec.txt       prompt bài 1-2 (dùng nguyên văn, giống hệt file prompt-gop.txt)
    prompt-gop.txt             bản gốc của prompt trên
    prompt-dinh-dang-moi.txt   prompt bài 3 (agent sửa script cho định dạng mới)
    prompt-bai4/               10 prompt của bài 4, dạng file
    thang-10/, thang-11/, thang-11-doi-dinh-dang/   mỗi thư mục: goc/ (6 file .xlsx) + 2 file danh mục
    bai-tap/bt1-chi-nhanh-thu-7/, bai-tap/bt2-doi-ten-cot/   dữ liệu bài tập 1, 2
  ket-qua/
    dap-an-*.json              đáp án (KHÔNG đưa cho agent)
    cham.py, chay_lai.py       bộ chấm gốc
    tom_tat_cham.py            in kết quả chấm ngắn cho bài 2, 3, 4
    quet_so_cu.py              tìm mã chứng từ của tháng trước còn sót (bài 3)
    kiem_tuan.py               chấm bài tập 3 (báo cáo theo tuần)
    tao_bao_cao_cham.py, bao-cao-cham.json   gom toàn bộ số chấm bài 1-3
    claude-bai1-2/, agy-bai1-2/        gop.py + ra/ do từng agent tạo (bài 1-2)
    claude-bai3-sua/, agy-bai3-sua/    gop.py đã sửa + ra/ (bài 3)
    bai4/                              file agent tạo ở 6 lần chạy bài 4 (Claude Code, rút gọn)
    dung_anh_*.py, chep_log_sach.py    dựng ảnh, chép log sạch
  logs/        log gốc *.raw.jsonl và transcript *.json (bài 1-3: 4 lần chạy; bài 4: 6 lần chạy, tiền tố bai4-), đã xử lý riêng tư
  anh/         ảnh PNG dùng trong bài
```

Chạy lại từ đầu (trong thư mục `du-lieu`): `python -X utf8 sinh_du_lieu.py` rồi `python -X utf8 sinh_bai_tap.py`.

## Giới hạn: chưa làm, cần biết trước khi dùng

- **n nhỏ.** Mỗi tình huống chạy 1 lần hợp lệ; chưa đo độ ổn định giữa các lần chạy. Bài 4 chỉ chạy với Claude Code.
- **"Đúng" nghĩa là khớp đáp án do chúng tôi đặt.** Đáp án theo quy tắc ghi trong prompt (dòng ngày mơ hồ không tính vào tổng; sản phẩm lạ vẫn tính vào doanh thu với mã `CHUA_XAC_DINH`; thành tiền lệch SL x giá thì giữ số chi nhánh ghi). Doanh nghiệp khác có thể chọn khác: **cần kiểm với kế toán trưởng**.
- **Dữ liệu giả sạch hơn thật.** Chưa thử công thức tham chiếu sheet khác, mật khẩu, nhiều sheet, file `.xls` cũ.
- **Chưa làm:** lập lịch tự chạy hằng tháng; chỗ nhập câu trả lời của chi nhánh vào script (`quyet-dinh.csv` mới là đề xuất); chạy trên dữ liệu doanh nghiệp thật; Prompt 1, 8, 9 và prompt bài tập 3 của bài 4 chưa chạy thử với agent.
- **Lỗi và sự cố khi chạy bài 2** (giữ lại vì có giá trị): lần chạy đầu mất log vì lệnh chạy nền bị dừng cùng phiên shell (bỏ lần đó; một quan sát không log: `agy` từng xếp 2 dòng "Combo quà Tết 2026" vào CẦN NGƯỜI QUYẾT và loại khỏi tổng, lệch 13.000.000 đ); `agy` hết giờ ở mốc 900 giây, chạy lại với giới hạn 2.100 giây xong sau 1.045 giây. Chi tiết ở bài 2.
- **Riêng tư trong log và ảnh.** Log công bố đã thay tiền tố đường dẫn máy bằng `<WORK>/`, `<HOME>`, `<user>` và bỏ các sự kiện `type="system"` khỏi `*.raw.jsonl`. Ảnh terminal được dựng lại từ log thật (không phải ảnh chụp cửa sổ TUI) đã che đường dẫn máy và tên tổ chức; ảnh bảng và ảnh file Excel dựng từ file thật bằng code (không phải ảnh chụp cửa sổ Excel).

## Đào sâu: tài liệu tham khảo

Không có bộ báo cáo chi nhánh Việt Nam công khai để tải; dữ liệu do chúng tôi sinh. Dạng lỗi được tham chiếu từ các bài hướng dẫn công khai (chúng tôi đọc phần tóm tắt trong kết quả tìm kiếm ngày 2026-11-20, chưa tải toàn văn từng trang; không chép nội dung nào vào bộ dữ liệu):

- **[Nguồn]** Ô gộp khi đọc bằng pandas thành ô trống, cách xử lý bằng điền xuống: <https://www.statology.org/pandas-read-excel-merged-cells/>
- **[Nguồn]** `pd.to_datetime` mặc định đọc tháng trước ngày, nên chuỗi ngày/tháng bị đảo: <https://towardsdatascience.com/clean-a-messy-date-column-with-mixed-formats-in-pandas-1a88808edbf7>
- **[Nguồn]** Khuyến nghị dùng ISO 8601 (`YYYY-MM-DD`) khi được chọn định dạng đầu ra: <https://data.europa.eu/apps/data-visualisation-guide/cleaning-data-dates>
- **[Nguồn]** Mẫu quy trình "đọc thô với `header=None`, tìm hàng tiêu đề bằng tên cột, rồi mới đọc lại": mô tả trong các kết quả tìm kiếm về pandas `read_excel` (ví dụ <https://tessl.io/registry/skills/github/HKUDS/OpenSpace/irregular-excel-parsing>); đây là bài viết cộng đồng, không phải tài liệu chính thức.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.
