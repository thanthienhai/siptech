# Bài toán 07: Từ xuất-nhập-tồn 12 tháng đến đề xuất nhập hàng tháng tới

> **Dữ liệu trong bài này là GIẢ, sinh bằng code để học.** Tên hàng, giá vốn, nhà cung cấp, số lượng đều bịa. Không phải dữ liệu của doanh nghiệp thật. Mọi con số "đo được" là kết quả chạy của chúng tôi ngày 2026-11-20 trên bộ dữ liệu giả này, mỗi agent chỉ 1 lần chạy có đầy đủ log.

Nhãn dùng trong bài: **[Đo được]** là kết quả chạy/chấm của chúng tôi. **[Nguồn]** là thông tin có link. **[Đề xuất]** là ý kiến của người viết.

## 1. Bài toán và vì sao cửa hàng nhỏ ở Việt Nam hay gặp

Một cửa hàng tạp hóa, vật tư hoặc mỹ phẩm có vài chục đến vài trăm mã hàng. Cuối tháng chủ cửa hàng phải trả lời năm câu hỏi:

1. Mã nào đem lại phần lớn tiền, mã nào chỉ chiếm chỗ (phân loại **ABC**)?
2. Mỗi mã cần giữ bao nhiêu tồn **an toàn** và khi tồn tụt xuống mức nào thì phải **đặt lại**?
3. Mã nào **sắp hết**, mã nào **hết rồi**, mã nào **tồn lâu** bán không ra?
4. Tháng tới nên nhập bao nhiêu mỗi mã?
5. Tổng tiền vốn phải bỏ ra là bao nhiêu, có vượt tiền mặt mình đang có không (**cảnh báo dòng tiền**)?

Phần lớn cửa hàng nhỏ trả lời bằng trí nhớ hoặc một file Excel nhập tay. Dữ liệu nhập tay luôn có lỗi: gõ thừa số 0, số âm không rõ là trả hàng hay gõ nhầm, dòng bị nhập hai lần, ngày viết ba kiểu. Hơn nữa có một cái bẫy tinh vi: **mã hết hàng thì doanh số về 0**, nhưng 0 đó không có nghĩa là khách không mua. Nếu lấy trung bình "ngây thơ" thì mã vừa hết hàng sẽ bị đề xuất nhập ít đi, và vòng luẩn quẩn hết hàng tiếp diễn.

Bài này cho thấy cách giao việc làm sạch và tính toán cho coding agent (Claude Code, Antigravity `agy`), **với điều kiện công thức do code tất định tính, ghi rõ giả định, và người chủ quyết định số cuối**.

## 2. Dữ liệu mẫu (giả)

Thư mục `du-lieu/` (sinh bằng `sinh_du_lieu.py`, hạt giống cố định 20261120, chạy lại ra y hệt):

| File | Nội dung |
|---|---|
| `nhat-ky-xuat-nhap.csv` | 11.128 dòng xuất/nhập/điều chỉnh, 2025-11 đến 2026-10 (có bẫy, xem dưới) |
| `danh-muc-hang.csv` | 60 mã (24 tạp hóa, 20 vật tư, 16 mỹ phẩm): giá vốn, bội số đặt, thời gian giao (ngày), trạng thái |
| `ton-dau-ky-2025-11-01.csv`, `ton-kiem-ke-2026-10-31.csv` | tồn đầu kỳ và tồn kiểm kê thực tế cuối kỳ |
| `hang-dang-ve.csv` | 10 dòng đơn đang trên đường về |
| `tham-so.json` | mức phục vụ 95%, ngưỡng cảnh báo, **ngân sách nhập tháng 2026-11 = 30.000.000 đ** (tham số học tập) |
| `quy-uoc.md` | công thức và định nghĩa **cố định** (agent không được đổi) |
| `xuat_excel.py` | gom các CSV kết quả thành một file Excel cho chủ cửa hàng |

Bẫy đã cài (đáp án nằm ở `ket-qua/dap-an.json`, **không** đưa cho agent):

- Có **mùa vụ**: hàng Tết (mứt, hạt dưa), mùa nóng (nước ngọt, kem chống nắng), mùa mưa, mùa tựu trường.
- Có **hàng bán chậm** (1 đến 3 đơn vị/tháng), có **hàng ngừng nhập còn tồn** (tồn lâu), có **3 mặt hàng mới** chỉ có 2 đến 5 tháng dữ liệu.
- Có **hết hàng làm doanh số về 0 giả tạo**: 10 mã bị cắt nguồn cung vài tuần, tổng cộng 33 mã-tháng bị "cụt".
- **Lỗi nhập liệu cần phát hiện (28 dòng):** 11 dòng trùng, 6 số lượng âm không ghi chú, 6 số lượng gấp 10 lần (gõ thừa số 0), 3 dòng thiếu số lượng, 2 phiếu nhập có ngày tháng 12/2026 (sau ngày cuối dữ liệu).
- **Ca hợp lệ nhưng dễ nhầm:** 30 dòng số âm CÓ ghi chú "khách trả", 16 dòng hủy hàng hết hạn, 18 dòng xuất dùng tại quán, 55 dòng điều chỉnh kiểm kê (đều không phải bán hàng), 5 đơn sỉ một lần.
- **Định dạng lẫn lộn:** ngày viết `2026-03-13`, `13/03/2026`, `13/3/26`; mã hàng viết `th017`, `TH-017`, `TH017 ` (thừa khoảng trắng); 4 dòng thiếu mã hàng, chỉ có tên không dấu.
- **Bẫy MP002:** mã này hết hàng, đơn đang về nhưng ngày dự kiến là 2026-12-27, tức **sau** tháng đề xuất. Công thức vẫn trừ số hàng đang về nên cho ra 0, trong khi thực tế tháng 11 hết hàng. Người duyệt phải thấy.
- 5 dòng bị **xóa khỏi nhật ký** (lộ ra chỉ qua chênh lệch giữa tồn hệ thống và kiểm kê, không thể thấy trong nhật ký).

## 3. Công thức (cố định, ghi trong `du-lieu/quy-uoc.md`)

Trung bình trượt 3 tháng hợp lệ để dự báo F; độ lệch chuẩn σ của tối đa 6 tháng hợp lệ; **tồn an toàn SS = Z × σ × √(T/30)** (T là thời gian giao, Z = 1,645 cho mức phục vụ 95%); **điểm đặt lại = F/30 × T + SS**; số cần nhập = max(0, F + SS − tồn kiểm kê − hàng đang về) làm tròn lên theo bội số quy cách; ABC theo giá trị tiêu thụ 12 tháng (A: giá trị các mã đứng trước chưa tới 80%, B: chưa tới 95%, C: còn lại). Tháng có từ 7 ngày hết hàng trở lên bị **loại khỏi trung bình** (coi là thiếu số liệu, không phải 0).

Giả định ghi rõ: thời gian giao cố định, nhu cầu các tháng độc lập, không xét chi phí đặt hàng hay hạn sử dụng. **Dự báo ngây thơ làm mốc:** "bằng tháng liền trước". Mốc "cùng kỳ năm trước" **chỉ làm được cho tháng 2026-11** (lấy 2025-11); không làm được cho hai tháng giữ lại 2026-09 và 2026-10 vì dữ liệu chỉ có đúng 12 tháng.

## 4. Mục lục 3 bài

| Bài | Nội dung | Kết quả |
|---|---|---|
| [Bài 1: Chuẩn bị dữ liệu và giao việc](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | Xem dữ liệu bằng Excel, tìm tài liệu tham chiếu, viết prompt 6 phần, lệnh chạy `claude` và `agy` | prompt nguyên văn + cách giao |
| [Bài 2: Chạy thật và kiểm tra kết quả](cap-01-chay-that-va-kiem-tra.md) | Agent làm gì, chấm bằng đáp án, lỗi gặp, công thức có hơn mốc ngây thơ không | bảng chấm và ảnh |
| [Bài 3: Dùng hằng ngày](cap-02-dung-hang-ngay.md) | Chu trình hàng tháng, chạy lại, đổi ngân sách, người duyệt, giới hạn | script chạy lại được |

## 5. Kết quả đo tóm tắt

**[Đo được]** ngày 2026-11-20, 60 mã, mỗi agent 1 lần chạy có log (Claude Code `claude-1`, Antigravity `agy-2`); chấm bằng `ket-qua/cham.py`.

| Chỉ tiêu | `claude-1` | `agy-2` |
|---|---|---|
| Phát hiện 28 lỗi nhập liệu cài sẵn, xử lý hợp lý | 28/28 | 28/28 |
| Phân loại ABC khớp đáp án | 60/60 | 60/60 |
| Dự báo F khớp tham chiếu (46 mã không mơ hồ, sai số ≤ 10% hoặc 1 đơn vị) | 46/46 | 44/46 |
| Nhãn cảnh báo khớp | 60/60 | 58/60 |
| Tháng cụt hàng: đúng / báo thừa / bỏ sót (trên 33) | 33 / 0 / 0 | 30 / 49 / 3 |
| Tổng tiền vốn đề xuất (ngân sách 30.000.000 đ) | 29.936.000 đ | 29.988.400 đ |
| Hàng hết/ sắp hết lớp A-B được đề xuất nhập | 2/2 | 2/2 |
| Báo người duyệt về MP002 (hàng về 27/12) | có | không (ghi "đầu tháng 11" ở bảng đề xuất) |
| Hold-out 2026-09, WAPE công thức / mốc tháng trước | 33,1% / 30,5% | 34,9% / 31,0% |
| Hold-out 2026-10, WAPE công thức / mốc tháng trước | 38,2% / 21,7% | 39,9% / 21,9% |
| Thời gian chạy | 660 giây | 1.525 giây |

**Điều quan trọng nhất:** công thức trung bình trượt do chủ cửa hàng đặt ra **thua mốc ngây thơ "bằng tháng trước"** ở cả hai tháng giữ lại, ở cả hai agent. Đây là kết quả thật và agent đã báo thẳng. Với n chỉ là hai tháng (khoảng 54 mã mỗi tháng, tập trung sai số ở vài mã mùa vụ lớn) thì **chưa đủ để kết luận công thức luôn kém**. Chi tiết ở bài 2.

Ảnh terminal dựng lại từ log đã che đường dẫn máy và tên tổ chức.

**Không** rút ra "agent nào tốt hơn" từ bảng này: mỗi bên chỉ 1 lần chạy, chưa đo được độ ổn định.

**Lỗi và sự cố trong quá trình làm (giữ lại cho trung thực):**

- Lượt chạy đầu của cả hai agent (`claude-0`, `agy-0`) **mất log** vì tôi khởi chạy sai cách (log chỉ ghi khi tiến trình kết thúc bình thường). Kết quả file của hai lượt đó vẫn còn trong `ket-qua/claude-0-mat-log/` và `ket-qua/agy-0-mat-log/`, được chấm và ghi vào `bao-cao-cham.json`, nhưng **không có ảnh dựng từ log** vì không có log. Hai lượt đó cho kết quả gần giống hai lượt có log, trừ việc `agy-0` sót 6 trong 28 lỗi (xem bài 2).
- Lượt `agy-1` chạy quá 900 giây (mức mặc định của brief) và bị cắt trước khi ghi log. Lượt `agy-2` chạy lại với giới hạn 1.800 giây và hoàn tất sau 1.525 giây.
- Prompt **không bị sửa** giữa các lần chạy (giữ nguyên bản ở `logs/prompt.txt`).
- Trong log Antigravity có dòng báo lỗi profile PowerShell của máy chạy ở mỗi lệnh; chúng tôi đã **che tên thư mục tổ chức** trong log (thay bằng `[đã che tên tổ chức]`) và lược các dòng này khỏi ảnh.

## 6. Tài liệu tham chiếu công khai

Chúng tôi dùng các nguồn dưới đây để chọn công thức và định dạng dữ liệu giả. Không chép nội dung có bản quyền.

- **Tồn kho an toàn, điểm đặt lại, z-score.** **[Nguồn]** NC State University, Supply Chain Resource Cooperative, "Safety Stock": <https://scm.ncsu.edu/scm-articles/article/safety-stock>. Trang này trả mã 403 khi tải trực tiếp nên chúng tôi **chỉ đọc qua tóm tắt tìm kiếm**: z = 1,29 / 1,65 / 2,33 cho mức phục vụ chu kỳ 90% / 95% / 99%; điểm đặt lại = nhu cầu trong thời gian giao + tồn an toàn.
- **[Nguồn]** Shopify, "Safety stock": <https://www.shopify.com/blog/safety-stock> (đã đọc): liệt kê các công thức "tối đa − trung bình", "số ngày cố định", Heizer và Render (SS = Z × σ thời gian giao), Greasley (SS = Z × σ thời gian giao × nhu cầu trung bình). Các công thức này nói về **biến động thời gian giao**, còn công thức của chúng tôi (Z × σ nhu cầu × √(T/30)) là bản **biến động nhu cầu**.
- **[Nguồn]** Zoho Inventory, "Safety stock formula": <https://zoho.com/inventory/tour/safety-stock-formula.pdf>. Chỉ đọc qua tóm tắt tìm kiếm: ví dụ dùng Z × √(thời gian giao trung bình) × σ nhu cầu. Đây là gần nhất với công thức của chúng tôi.
- **Phân loại ABC.** **[Nguồn]** Wikipedia, "ABC analysis": <https://en.wikipedia.org/wiki/ABC_analysis> (đã đọc): không có ngưỡng cố định; ví dụ 20%/30%/50% mặt hàng chiếm khoảng 70%/25%/5% giá trị, hoặc 10%/20%/70% mặt hàng chiếm 66,6%/23,3%/10,1%. **[Nguồn]** Sage, "ABC analysis": <https://www.sage.com/en-us/blog/abc-analysis/> (qua tóm tắt tìm kiếm): mô tả cách chia thường gặp 80/15/5. Ngưỡng 80% và 95% của chúng tôi là **[Đề xuất]**, không phải quy định.
- **Định dạng dữ liệu giao dịch bán lẻ.** **[Nguồn]** UCI Machine Learning Repository, "Online Retail", giấy phép CC BY 4.0, DOI 10.24432/C5BW33: <https://archive.ics.uci.edu/dataset/352/online+retail>. Chúng tôi chỉ tham chiếu **dạng lỗi** (hóa đơn hủy có số lượng âm, mã hàng, mô tả, ngày), không dùng dữ liệu của họ. Bộ dữ liệu này là của một nhà bán lẻ trực tuyến ở Anh, nên không dùng làm dữ liệu cửa hàng Việt Nam.
- **WAPE và hold-out.** Định nghĩa ghi trong `quy-uoc.md` (WAPE = Σ|dự báo − thực tế| / Σ thực tế). Đây là cách làm của chúng tôi, không trích nguồn.

## 7. Cấu trúc thư mục

```
07-ton-kho-va-de-xuat-nhap-hang/
  00-README.md  bai-1-...md  bai-2-...md  bai-3-...md
  du-lieu/      dữ liệu giả + sinh_du_lieu.py + xuat_excel.py
  ket-qua/      cham.py, bao-cao-cham.json, dap-an.json (ĐÁP ÁN, đừng đưa cho agent),
                claude-1/ agy-2/ (đầu ra thật), claude-0-mat-log/ agy-0-mat-log/ (đầu ra, không có log),
                thu-chay-lai.json, các script dựng ảnh
  logs/         prompt.txt, claude-1.raw.jsonl/.json, agy-2.raw.jsonl/.json
  anh/          12 ảnh dùng trong bài
```

**Việc cần người làm** (toàn bài): người chủ cửa hàng duyệt danh sách CẦN NGƯỜI QUYẾT, quyết số nhập cuối cùng, quyết ngân sách. **Giới hạn:** dữ liệu giả; 1 lần chạy mỗi agent; chưa đo độ ổn định; công thức chưa xét mùa vụ nên thua mốc ngây thơ ở hai tháng giữ lại.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây.
