# Bài toán 07: Từ xuất-nhập-tồn 12 tháng đến đề xuất nhập hàng tháng tới

> **Dữ liệu trong bài toán này là GIẢ, sinh bằng code để học.** Tên hàng, giá vốn, nhà cung cấp, số lượng đều bịa; ngân sách 30.000.000 đ chỉ là tham số học tập. Không phải dữ liệu của doanh nghiệp thật.

Nhãn dùng trong bài: **[Đo được]** là kết quả chạy hoặc chấm của chúng tôi. **[Nguồn]** là thông tin có link. **[Đề xuất]** là ý kiến của người viết.

## Bạn làm được gì sau bài toán này

Bạn biết giao cho một coding agent (chương trình AI tự đọc file, viết và chạy code) việc **làm sạch nhật ký xuất nhập 12 tháng và tính đề xuất nhập hàng tháng tới** cho cửa hàng 60 mã: phân loại ABC, tồn an toàn, điểm đặt lại, cảnh báo hàng sắp hết, tổng tiền vốn so với ngân sách. Bạn biết **kiểm** kết quả (cộng tay bằng Excel, chấm bằng code), **giữ lại script** để chạy mỗi tháng, và nhờ agent giải thích, kiểm chéo, thử kịch bản.

Ba điều giữ nguyên xuyên suốt: **công thức do chủ cửa hàng đặt và do code tính; ngân sách là tham số của chủ cửa hàng, không phải con số agent biết; người chủ quyết số nhập cuối cùng**, báo cáo của agent chỉ là đề xuất.

## 4 bài

| Bài | Nội dung | Mất bao lâu | Kết quả |
|---|---|---|---|
| [Bài 1. Chuẩn bị dữ liệu và giao việc](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | Xem dữ liệu bằng Excel, hiểu công thức, tạo thư mục riêng, dán prompt 6 phần | khoảng 30 phút | thư mục chạy xong với 5 file kết quả và script |
| [Bài 2. Chạy thật và kiểm tra](cap-01-chay-that-va-kiem-tra.md) | Cộng tay, chấm bằng `cham.py`, đọc các ca agent sai, công thức có hơn mốc ngây thơ không | khoảng 40 phút | bảng chấm và kết luận có ghi n |
| [Bài 3. Dùng hằng tháng](cap-02-dung-hang-ngay.md) | Chạy lại script, đổi ngân sách, xuất Excel, quy trình 6 bước có người duyệt | khoảng 30 phút | script chạy lại bằng một lệnh |
| [Bài 4. Prompt mẫu và bài tập](cap-03-prompt-mau-va-bai-tap.md) | 8 prompt dùng lại (5 đã chạy thật), 3 bài tập có bộ kiểm, dùng với dữ liệu thật | 1 đến 2 giờ | bộ prompt và ba bài tập tự đo |

## Sắp xếp thư mục trước khi làm

Tạo một thư mục trống làm nơi làm bài (ví dụ `bai-toan`) và sắp như sau:

```file
bai-toan/
  du-lieu/      giải nén du-lieu.zip vào đây (dữ liệu giả và bản giao việc)
  lan-chay-1/   thư mục RIÊNG của agent: bạn tạo ở Bài 1, chỉ chép file dữ liệu vào
  ket-qua/      giải nén bo-cham.zip vào đây (đáp án và bộ chấm), SAU KHI agent chạy xong
```

- Trong từng bài, lệnh chấm cho biết bạn đứng ở thư mục nào. Phần lớn bộ chấm cần `du-lieu/` và `ket-qua/` nằm **cạnh nhau**.
- **Để đáp án ngoài tầm agent.** Đừng giải nén `bo-cham.zip` trước khi agent chạy xong. Agent có thể đi lên thư mục cha để tìm file; việc này đã xảy ra trong các lần chạy của chúng tôi (xem bài 2).
- **Cần Python 3** (cách kiểm và cài: [Bài 1 của nhóm Bắt đầu](../th-bat-dau-voi-coding-agent/cap-00-lam-quen-cua-so-dong-lenh.md)). Một số bộ chấm đọc file Excel nên cần thư viện `openpyxl`: nếu thấy `ModuleNotFoundError`, gõ `pip install openpyxl`. **Chưa kiểm** trên máy sạch.

## Khi dùng dữ liệu thật (không có đáp án)

Đáp án và bộ chấm trong bài chỉ có cho dữ liệu giả. Với dữ liệu thật bạn không có "đáp án đúng", nên kiểm theo các bước sau **[Đề xuất]**:

1. Làm trên **bản sao**, đã ẩn danh nếu có thông tin cá nhân (xem [An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md)).
2. Thử trên **20 đến 30 dòng** trước, rồi mới chạy cả file.
3. Tự làm lại bằng tay **10 dòng ngẫu nhiên** và **mọi dòng agent đánh dấu cần người quyết**: mở dữ liệu gốc, tự tính, so với kết quả của agent.
4. Đối chiếu **tổng** bằng Excel (cộng cột tiền hoặc đếm dòng ở file gốc và file kết quả). Tổng khớp chưa chứng minh từng dòng đúng, nhưng tổng lệch là dấu hiệu chắc chắn có lỗi.
5. Chạy lại lần hai trên cùng dữ liệu và so hai kết quả: chỗ khác nhau là chỗ chưa đáng tin.
6. Người có trách nhiệm (kế toán trưởng, quản lý) duyệt trước khi dùng cho tiền, lương hay khách hàng. Đừng để agent tự gửi hay tự sửa dữ liệu gốc.

## Kết quả đo tóm tắt

**[Đo được]** ngày 2026-11-20, 60 mã, mỗi agent 1 lần chạy có log (Claude Code `claude-1`, Antigravity `agy-2`), chấm bằng `ket-qua/cham.py`.

| Chỉ tiêu | `claude-1` | `agy-2` |
|---|---|---|
| Phát hiện 28 lỗi nhập liệu cài sẵn, xử lý hợp lý | 28/28 | 28/28 |
| ABC khớp đáp án | 60/60 | 60/60 |
| Dự báo khớp tham chiếu (46 mã không mơ hồ) | 46/46 | 44/46 |
| Nhãn cảnh báo khớp | 60/60 | 58/60 |
| Tháng cụt hàng: đúng / báo thừa / bỏ sót (trên 33) | 33 / 0 / 0 | 30 / 49 / 3 |
| Tổng tiền đề xuất (ngân sách 30.000.000 đ; công thức cần 41,1 và 41,9 triệu) | 29.936.000 đ | 29.988.400 đ |
| Báo người duyệt về MP002 (hàng về **27/12**, sau tháng đề xuất) | có | không |
| Hold-out 2026-09, WAPE công thức / mốc tháng trước | 33,1% / 30,5% | 34,9% / 31,0% |
| Hold-out 2026-10, WAPE công thức / mốc tháng trước | 38,2% / 21,7% | 39,9% / 21,9% |
| Thời gian chạy | 660 giây | 1.525 giây |

**Điều quan trọng nhất:** công thức trung bình trượt của chủ cửa hàng **thua mốc ngây thơ "bằng tháng trước" ở cả hai tháng giữ lại, ở cả hai agent**, và agent đã báo thẳng. Nhưng n chỉ là hai tháng (khoảng 54 mã mỗi tháng, sai số dồn vào vài mã mùa vụ lớn). **[Đo được]** Khi đo lại trên 8 tháng (bài 4, bài tập 3), công thức thắng 4 tháng (03, 04, 05, 08) và thua 4 tháng (06, 07, 09, 10): thắng thua lẫn lộn, **chưa kết luận được**.

**Không** rút ra "agent nào tốt hơn" từ bảng này: mỗi bên chỉ 1 lần chạy.

**Bài 4 [Đo được]:** 8 prompt, 5 prompt chạy thật ngày 2026-11-21 (n = 1 mỗi prompt), thêm 1 lần chạy để thử bài tập 2: tổng 6 lần gọi agent. Ba kết quả đáng nhớ: agent giải thích script nói một chi tiết sai (mã hàng lạ không "bị bỏ qua" mà làm script dừng); kiểm chéo ABC độc lập ra 56/60 khớp, lệch do hai đơn lớn cần người quyết; thêm một mã bán theo mùa vào thì công thức đề xuất nhập 114 hộp (10,26 triệu đồng) cho mã mà cùng kỳ năm trước chỉ bán 1 hộp.

## Sự cố trong quá trình làm (giữ lại cho trung thực)

- Lượt chạy đầu của cả hai agent (`claude-0`, `agy-0`) **mất log** vì chúng tôi khởi chạy sai cách. File kết quả vẫn được chấm (`ket-qua/claude-0-mat-log/`, `ket-qua/agy-0-mat-log/`), nhưng không có ảnh dựng từ log. `agy-0` sót 6 trong 28 lỗi (bài 2).
- Lượt `agy-1` chạy quá 900 giây và bị cắt trước khi ghi log; `agy-2` chạy lại với giới hạn 1.800 giây.
- Prompt **không bị sửa** giữa các lần chạy (bản gốc ở `logs/prompt.txt` và `du-lieu/prompt-giao-viec.txt`).
- Log Antigravity có dòng báo lỗi profile PowerShell của máy chạy; chúng tôi đã che tên thư mục tổ chức và đường dẫn máy trong mọi log và ảnh.

## Đào sâu: cấu trúc thư mục trong bản gốc của tác giả
```
07-ton-kho-va-de-xuat-nhap-hang/
  00-README.md  bai-1-...md  bai-2-...md  bai-3-...md  bai-4-...md
  du-lieu/      7 file đầu vào cho agent, sinh_du_lieu.py, xuat_excel.py, prompt-giao-viec.txt,
                kiem_ngan_sach.py, do_giu_lai.py, them_hang_mua_vu.py (cho bài 3 và bài 4)
  ket-qua/      cham.py, bao-cao-cham.json, dap-an.json (ĐÁP ÁN, đừng đưa cho agent),
                claude-1/ agy-2/ (đầu ra thật), claude-0-mat-log/ agy-0-mat-log/, thu-chay-lai.json
  logs/         prompt.txt, log lần chạy bài 2 (claude-1, agy-2) và bài 4 (bai4-*)
  anh/          ảnh dùng trong bài
```

Nguồn tham chiếu của công thức (tồn an toàn, ABC, định dạng dữ liệu) nằm trong mục Đào sâu của bài 1.

## Việc cần người làm

Người chủ cửa hàng duyệt danh sách CẦN NGƯỜI QUYẾT, **quyết số nhập cuối cùng** và **quyết ngân sách** (tham số `ngan_sach_nhap_vnd`).

## Giới hạn

- Dữ liệu giả; mùa vụ và nhu cầu do chúng tôi đặt.
- Bài 2: mỗi agent 1 lần chạy có log; chưa đo độ ổn định. Bài 4: mỗi prompt chạy 1 lần, chỉ bằng Claude Code.
- Công thức chưa xét mùa vụ, hạn dùng, chi phí đặt hàng, thời gian giao thay đổi.
- Mốc "cùng kỳ năm trước" chỉ làm được cho tháng 2026-11, không làm được cho các tháng giữ lại.
- Chưa mở file Excel xuất ra bằng Excel thật; chưa thử cập nhật script sang tháng 12.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.
