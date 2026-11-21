# Bài toán 08: Gộp báo cáo doanh thu từ nhiều file Excel của chi nhánh

> **Dữ liệu trong bài này là dữ liệu GIẢ để học.** Công ty "Mẫu An Phát", 6 chi nhánh, mã hàng, số chứng từ, số tiền đều do chương trình `du-lieu/sinh_du_lieu.py` bịa ra (hạt giống cố định). Không có dữ liệu của doanh nghiệp thật. Mọi con số trong bài gắn nhãn **[Đo được]** (kết quả chạy của chúng tôi, ngày 2026-11-20, n nhỏ), **[Nguồn]** (có link) hoặc **[Đề xuất]** (ý kiến).

## Vì sao doanh nghiệp nhỏ ở Việt Nam hay gặp bài toán này

Công ty có vài chi nhánh hoặc vài đại lý. Cuối tháng, mỗi nơi gửi về một file Excel doanh thu. Không ai thống nhất mẫu: nơi thì tiêu đề nằm dòng 7 vì phía trên có dòng giới thiệu, nơi thì ô ngày gộp theo ngày, nơi thì số tiền là chữ `1.250.000đ` (Excel không cộng được), nơi thì máy cài tiếng Anh nên ngày thành `10/05/2026` mà chẳng ai biết là mùng 5 tháng 10 hay mùng 10 tháng 5. Kế toán trung tâm mất một hai ngày chép tay vào một file tổng, rồi vẫn không chắc tổng có khớp với tổng của từng chi nhánh.

Bài này cho thấy cách giao việc đó cho một coding agent (Claude Code, Antigravity `agy`) theo hướng **"agent viết một script, script mới là thứ tính tiền"**, và cách kiểm lại bằng đáp án. Ba nguyên tắc xuyên suốt:

1. **Không sửa file gốc.** File chi nhánh gửi là chứng cứ. Mọi thứ agent tạo ra nằm ở thư mục khác; ta so mã băm (SHA-256) trước và sau để chứng minh.
2. **Số do code tính.** Agent không "nhẩm" tổng. Nó viết `gop.py`, chạy, và chỉ báo cáo con số script in ra.
3. **Không chắc thì ghi CẦN NGƯỜI QUYẾT.** Ngày `10/09/2026` có thể là mùng 10 tháng 9 hoặc mùng 9 tháng 10: không có căn cứ thì để người quyết, không đoán thầm.

## Mục lục 3 bài

| Bài | Nội dung | Kết quả chính |
|---|---|---|
| [Bài 1](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | Xem 6 file lộn xộn, hiểu bẫy cài sẵn, viết prompt giao việc (khung 6 phần), dựng thư mục làm việc an toàn | Prompt thật `du-lieu/prompt-gop.txt`, 6 file mẫu, đáp án để chấm |
| [Bài 2](cap-01-chay-that-va-kiem-tra-ket-qua.md) | Chạy thật Claude Code và Antigravity, chấm bằng code, đọc bảng kiểm tra tổng | Cả hai: 901/901 dòng đúng, 3/3 ca ngày mơ hồ chuyển cho người; tổng từng file lệch ở đâu đã được giải thích |
| [Bài 3](cap-02-dua-vao-dung-hang-thang.md) | Chạy lại hằng tháng bằng script (không gọi agent); gọi agent chỉ khi có định dạng mới | Tháng mới cùng định dạng: script chạy lại đúng; chi nhánh đổi định dạng: script dừng, agent sửa trong 264 s / 1008 s, hồi quy sạch |

## Đo được, tóm tắt (ngày 2026-11-20, dữ liệu giả, mỗi tình huống chạy 1 lần hợp lệ)

- **Tháng 10/2026, 6 file, đáp án 901 dòng bán hàng + 3 dòng ngày mơ hồ.** Claude Code: 901/901 dòng đúng cả 5 trường, tổng 6/6 chi nhánh đúng, 718 s, 37 lượt. Antigravity (`agy`): 901/901, 6/6, 1045 s. Cả hai để trống ngày + CẦN NGƯỜI QUYẾT cho đúng 3 dòng HP `10/09/2026`. Cả hai không đụng file gốc (mã băm không đổi).
- **Chạy lại script của bài 1-2 cho tháng 11 (6 file cùng định dạng, không gọi agent):** cả hai script ra 877/877 dòng đúng. Nhưng script của `agy` còn in **mã chứng từ và số tiền của tháng 10** trong cột giải thích `kiem_tra.csv` và `bao_cao.md` (số tháng cũ bị gõ cứng trong code), và gắn nhãn khác cho 3 dòng ngày mơ hồ của tháng 11. Chấm số tiền không bắt được lỗi này; phải đọc chữ.
- **Tháng 11, chi nhánh NT đổi định dạng:** cả hai script dừng, không đoán thầm (`claude`: mã thoát 2 kèm thông báo tiếng Việt; `agy`: mã thoát 1 kèm lỗi `ValueError`). Cho agent sửa: Claude Code 264 s, `agy` 1008 s; sau sửa cả hai chạy đúng 877/877 trên tháng 11 định dạng mới, tháng 11 định dạng cũ và tháng 10.

## Cấu trúc thư mục

```
08-gop-bao-cao-chi-nhanh/
  00-README.md, bai-1-..., bai-2-..., bai-3-...
  du-lieu/
    sinh_du_lieu.py            sinh dữ liệu giả (seed cố định)
    prompt-gop.txt             prompt bài 1-2 (dùng nguyên văn, không sửa sau khi thấy kết quả)
    prompt-dinh-dang-moi.txt   prompt bài 3 (agent sửa script cho định dạng mới)
    thang-10/                  goc/ (6 file .xlsx) + danh_muc_san_pham.csv + danh_muc_chi_nhanh.csv
    thang-11/                  tháng 11, cùng định dạng
    thang-11-doi-dinh-dang/    tháng 11, chi nhánh NT đổi định dạng
  ket-qua/
    dap-an-T10.json, dap-an-T11.json, dap-an-T11-doi-dinh-dang.json   đáp án (KHÔNG đưa cho agent)
    cham.py                    chấm một lần chạy bằng đáp án
    chay_lai.py                chạy lại gop.py cho tháng mới rồi chấm (bài 3)
    tao_bao_cao_cham.py, bao-cao-cham.json   gom toàn bộ số chấm
    claude-bai1-2/, agy-bai1-2/     gop.py + ra/ do từng agent tạo (bài 1-2)
    claude-bai3-sua/, agy-bai3-sua/ gop.py đã sửa + ra/ (bài 3)
    dung_anh_*.py, chep_log_sach.py  dựng ảnh, chép log sạch
  logs/        log gốc *.raw.jsonl và transcript *.json của 4 lần chạy hợp lệ (đã xử lý riêng tư, xem dưới)
  anh/         20 ảnh PNG dùng trong bài
```

## Cách tự chạy lại

```powershell
cd du-lieu
python -X utf8 sinh_du_lieu.py        # sinh lại dữ liệu + đáp án (ra du-lieu/thang-XX và ket-qua/dap-an-*.json)
```
Chấm một lần chạy: `python -X utf8 ket-qua\cham.py <thư_mục_agent_đã_làm> ket-qua\dap-an-T10.json du-lieu\thang-10\goc`.

## Tài liệu tham khảo (tìm trước khi làm, 2026-11-20)

Không có bộ báo cáo chi nhánh Việt Nam công khai để tải; dữ liệu do chúng tôi sinh. Dạng lỗi được tham chiếu từ các bài hướng dẫn công khai (chúng tôi đọc phần tóm tắt trong kết quả tìm kiếm, chưa tải toàn văn từng trang; không chép nội dung nào vào bộ dữ liệu):

- [Nguồn] Ô gộp khi đọc bằng pandas thành ô trống, cách xử lý bằng điền xuống: <https://www.statology.org/pandas-read-excel-merged-cells/>
- [Nguồn] `pd.to_datetime` mặc định đọc tháng trước ngày, nên chuỗi ngày/tháng bị đảo: <https://towardsdatascience.com/clean-a-messy-date-column-with-mixed-formats-in-pandas-1a88808edbf7>
- [Nguồn] Khuyến nghị dùng ISO 8601 (`YYYY-MM-DD`) khi được chọn định dạng đầu ra: <https://data.europa.eu/apps/data-visualisation-guide/cleaning-data-dates>
- [Nguồn] Mẫu quy trình "đọc thô với `header=None`, tìm hàng tiêu đề bằng tên cột, rồi mới đọc lại": mô tả trong các kết quả tìm kiếm về pandas `read_excel` (ví dụ <https://tessl.io/registry/skills/github/HKUDS/OpenSpace/irregular-excel-parsing>); đây là bài viết cộng đồng, không phải tài liệu chính thức.

## Điều cần biết trước khi dùng kết quả

- **n nhỏ.** Mỗi tình huống chạy 1 lần hợp lệ. Chưa đo được độ ổn định giữa các lần chạy. Không rút ra kết luận "agent nào tốt hơn" từ đây; chỉ mô tả quan sát.
- **"Đúng" nghĩa là khớp đáp án do chúng tôi đặt.** Đáp án dựa trên các quy tắc ghi trong prompt (ví dụ: dòng ngày mơ hồ không tính vào tổng; sản phẩm lạ vẫn tính vào doanh thu với mã `CHUA_XAC_DINH`; thành tiền lệch SL x giá thì giữ số chi nhánh ghi). Doanh nghiệp khác có thể chọn khác.
- **Dữ liệu giả sạch hơn dữ liệu thật.** Thật có thể còn công thức tham chiếu sheet khác, mật khẩu, nhiều sheet, file `.xls` cũ... Bài này không thử các trường hợp đó.
- **Lỗi và sự cố khi chạy** (giữ lại vì có giá trị):
  - Lần chạy đầu mất log: lệnh chạy nền bị dừng cùng phiên shell nên `agent_run.py` không kịp ghi log (kết quả của các agent vẫn nằm trong thư mục làm việc). Chúng tôi bỏ lần đó, không dùng số. Một quan sát không có log: lần ấy `agy` từng xếp 2 dòng "Combo quà Tết 2026" vào CẦN NGƯỜI QUYẾT và loại khỏi tổng (lệch 13.000.000 đ so với đáp án); lần chạy hợp lệ không lặp lại điều này. Đây là một lần, không có log, chỉ để thấy kết quả có thể khác giữa các lần.
  - `agy` hết giờ ở mốc 900 s (agent_run ném `TimeoutExpired`, mất log). Chạy lại với giới hạn 2100 s (khác khuyến nghị 900 s trong brief): hoàn thành sau 1045 s. Vậy `agy` có 3 lần khởi chạy, 1 lần hợp lệ có log; `claude` có 2 lần khởi chạy, 1 lần hợp lệ có log.
- **Riêng tư trong log.** Log công bố đã thay các tiền tố đường dẫn máy (ví dụ `C:\Users\...`) bằng `<WORK>/`, `<HOME>`, `<user>`, và bỏ các sự kiện `type="system"` (liệt kê cấu hình máy người chạy) khỏi `*.raw.jsonl`. Nội dung lời agent, lệnh, kết quả lệnh, số token giữ nguyên.
- **Ảnh terminal dựng lại từ log đã che đường dẫn máy và tên tổ chức** (`logs/*.json` đã che, cộng thêm bước che `scrub_text` của công cụ dựng ảnh khi vẽ); cả 20 ảnh đã được dựng lại và xem từng ảnh sau bước che này.
- **Ảnh terminal** được dựng lại từ log thật của lần chạy ghi dưới mỗi ảnh, không phải ảnh chụp trực tiếp cửa sổ TUI. Ảnh bảng/ file Excel được dựng từ file thật bằng code, không phải ảnh chụp cửa sổ Excel.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây.
