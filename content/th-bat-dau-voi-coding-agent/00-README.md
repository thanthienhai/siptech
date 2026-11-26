# Bắt đầu với coding agent

## Bạn làm được gì sau nhóm bài này

Bạn cài được một **coding agent** (chương trình AI tự đọc file, viết file và chạy code trên máy bạn), mở nó đúng chỗ, giao một việc nhỏ bằng prompt 6 phần, đọc được câu xin quyền, và chấm kết quả bằng code. Bạn cũng biết các quy tắc an toàn cơ bản và biết khi nào phải dừng lại. Đây là nền cho 8 bài toán thực hành còn lại; mỗi bài toán đó đều bắt đầu bằng "mở agent trong một thư mục riêng" và dựa vào những gì có ở đây.

Không cần biết lập trình. Bạn chỉ cần gõ được vài lệnh trong cửa sổ dòng lệnh (bài 3 dạy từ đầu).

> Mọi dữ liệu trong nhóm bài này là **giả**. Phần cài đặt và đăng nhập lấy từ tài liệu chính thức (ngày đọc 2026-11-21), vì máy chúng tôi đã cài sẵn và đang đăng nhập. Kết quả chạy thật ghi nhãn **[Đo được]**.

## Bốn bài

| Bài | Nội dung | Mất bao lâu | Kết quả |
|---|---|---|---|
| [Bài 1. Cài đặt Claude Code](cap-00-cai-dat-claude-code.md) | Cài, đăng nhập, kiểm tra, thoát, câu xin quyền, thư mục tin cậy | khoảng 15 phút | `claude --version` in số phiên bản; mở được khung chat |
| [Bài 2. Cài đặt Antigravity CLI](cap-01-cai-dat-antigravity.md) | Cài, đăng nhập, kiểm tra, thoát, xin quyền, cảnh báo `--dangerously-skip-permissions` | khoảng 15 phút | `agy --version` in số phiên bản; mở được khung chat |
| [Bài 3. Làm quen với cửa sổ dòng lệnh](cap-02-lam-quen-cua-so-dong-lenh.md) | PowerShell: thư mục hiện tại, `cd`, `dir`, `mkdir`, `copy`, `python -X utf8`, đường dẫn có dấu cách, dán, `Ctrl + C` | khoảng 30 phút | thư mục `thu-agent` có 3 file; chạy Python không lỗi tiếng Việt |
| [Bài 4. Giao việc đầu tiên và an toàn](cap-03-giao-viec-dau-tien-va-an-toan.md) | Prompt 6 phần, đọc câu xin quyền, chấm bằng code, quy tắc an toàn, dữ liệu thật | khoảng 25 phút | `tong_theo_khach.csv` và `bao_cao.md` đạt 9/9 tiêu chí |

Chỉ cần cài **một** trong hai agent (bài 1 hoặc bài 2); bài 3 và bài 4 dùng được với cả hai.

## Kết quả đo

Việc đầu tiên ở bài 4: tổng hợp 20 dòng đơn hàng giả (12 đơn, 6 khách) thành số đơn và tổng tiền của mỗi khách. Bộ chấm `cham_bai_4.py` tự tính đáp án từ file gốc và kiểm 9 tiêu chí.

| Agent | Đúng/tổng tiêu chí | Số lần chạy | Thời gian |
|---|---|---|---|
| Claude Code | 9/9 | n=1 | 52,3 giây |
| Antigravity | 9/9 | n=1 | 116,1 giây |

**[Đo được]** ngày 2026-11-21, trên Windows 10. Chỉ một lần mỗi agent nên chưa đo được dao động. Việc rất nhỏ nên dễ đúng; đừng suy ra agent đúng với việc khó.

Chúng tôi cũng đã chạy thật trên máy này: `claude --version` (2.1.330), `claude doctor` (không có vấn đề cài đặt), `agy --version` (1.5.13), `agy --help`, và toàn bộ lệnh ở bài 3.

## Chưa làm và giới hạn

- **Cài đặt và đăng nhập chưa chạy lại từ đầu.** Lệnh cài, màn hình đăng nhập, hộp "tin thư mục", câu xin quyền và phím thoát lấy từ tài liệu chính thức; chúng tôi chưa chụp giao diện tương tác thật.
- **Chỉ chạy trên Windows 10.** Phần macOS và Linux lấy từ tài liệu, hoặc chỉ kiểm cú pháp bằng Git Bash.
- **Không nêu giá và hạn mức.** Chúng tôi không đọc được số liệu này từ nguồn chính thức khi soạn bài; xem trang chính thức của nhà cung cấp.
- **Yêu cầu hệ thống của Antigravity CLI:** không tìm thấy trong tài liệu chính thức.
- **Chưa kiểm** cờ `--dangerously-skip-permissions` có đè quy tắc cấm (deny) hay không; tài liệu không nói rõ.
- **Chưa kiểm** `Ctrl + C` trong cửa sổ dòng lệnh trên máy chúng tôi.
- Quy tắc từ chối ở bài 4 và các ước lượng thời gian là **[Đề xuất]**, không phải điều luật hay chính sách của nhà cung cấp.
- Về dữ liệu cá nhân và pháp luật Việt Nam, xem [An toàn dữ liệu và pháp lý Việt Nam](../an-toan-du-lieu-va-phap-ly-vn.md); chúng tôi không tự viết điều luật.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.

Log gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.
