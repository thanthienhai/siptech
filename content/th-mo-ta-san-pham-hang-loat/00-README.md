# Thực hành 03: Viết mô tả sản phẩm hàng loạt từ bảng thông số, không bịa

> Toàn bộ dữ liệu trong bài là **dữ liệu giả để học**. Shop "Vườn Nhỏ", tên sản phẩm, số phiếu công bố `DEMO-xxxx`, dung tích, xuất xứ đều do chương trình sinh ra với hạt giống cố định. Không có doanh nghiệp, sản phẩm hay giấy tờ thật nào ở đây.

## Bài toán

Chủ shop có một bảng thông số 40 sản phẩm (mỹ phẩm, chăm sóc cá nhân). Cần nhập lên sàn (Shopee, TikTok Shop, website) với mỗi sản phẩm gồm: tiêu đề, mô tả, đúng 5 gạch đầu dòng, từ khóa. Viết tay 40 sản phẩm mất cả buổi và dễ lệch giọng. Giao cho coding agent thì nhanh, nhưng có ba chỗ dễ hỏng:

1. **Bịa.** Agent (cũng như người viết vội) thích "làm cho đẹp": thêm "lành tính", "chính hãng", "an toàn cho da nhạy cảm", một con số nồng độ nghe hợp lý. Mô tả bán hàng không được vượt quá sự thật. Đó là nguyên tắc chung của quảng cáo và bán hàng; điều khoản cụ thể thì bài này **không trích**, cần hỏi luật sư hoặc người phụ trách pháp chế của shop.
2. **Thiếu thông số.** Có sản phẩm bảng để trống, ghi "?", "chưa rõ", "liên hệ NCC", "N/A". Người đang vội sẽ điền đại một con số. Agent phải ghi `CẦN BỔ SUNG`, không đoán.
3. **Lời đồn lẫn vào sự thật.** Cột ghi chú nội bộ có những câu như "bán chạy số 1", "nghe nói đạt chuẩn FDA", "chữa khỏi viêm da". Đó không phải thông số. Nếu chép sang mô tả, shop tự đưa mình vào rủi ro.

## Vì sao SME Việt Nam gặp bài toán này

Shop nhỏ nhập hàng từ nhà cung cấp (NCC) qua Zalo, bảng tính, ảnh chụp. Thông số lúc có lúc thiếu, ghi chú của kinh doanh và kỹ thuật lẫn vào nhau. Sàn có giới hạn độ dài và danh sách từ nhạy cảm. Việc thủ công nhất là viết lại cùng một thông tin ở 40 chỗ cho đúng giọng, và việc đó agent làm tốt nếu bạn **kiểm bằng code** chứ không đọc mắt.

## Dữ liệu mẫu (tải ở `du-lieu/`)

| File | Nội dung |
|---|---|
| `thong_so.csv` / `thong_so.xlsx` | 40 SKU, 14 cột, trong đó cột `ghi_chu_noi_bo` là lời đồn chưa kiểm chứng |
| `quy_dinh_shop.md` | giọng thương hiệu, giới hạn độ dài (giả định của shop), nguyên tắc sự thật, định dạng file nộp |
| `tu_cam.txt` | 28 cụm từ cấm do shop đặt |
| `mau_dau_ra.csv` | dòng tiêu đề của file cần nộp |
| `kiem_hang_ngay.py` | thước kiểm dùng hằng ngày, lấy `thong_so.csv` làm sự thật (bài 3) |
| `sinh_du_lieu.py` | sinh lại toàn bộ dữ liệu (seed 20261120); đồng thời sinh `ket-qua/dap-an.json` |

Bẫy cài sẵn, có đáp án:

- **9 SKU thiếu thông số** (VN-007 thiếu cả 6 trường bắt buộc; còn lại thiếu 1 đến 2 trường), mỗi nơi ghi "không có" một kiểu khác nhau.
- **14 SKU có ghi chú nội bộ chứa lời đồn** (số 1, FDA, bà bầu, không paraben, chữa khỏi, hết nám, rẻ hơn đối thủ 30%...).
- **1 SKU mâu thuẫn** (VN-012): bảng ghi vitamin C 10%, ghi chú nói "thực ra 15%".
- **10 SKU có số phiếu công bố giả** `DEMO-xxxx`, **4 SKU "đang chờ duyệt"** (không được nói là đã công bố).

![Bảng thông số đầu vào mẫu, 8 trong 40 dòng](anh/03-du-lieu-dau-vao.webp)

*Ảnh dựng từ `thong_so.csv` (HTML sang PNG). Dữ liệu giả để học. Ô đỏ là thông tin bắt buộc bị thiếu, cột vàng là lời đồn.*

## Mục lục 3 bài

1. [`cap-00-chuan-bi-va-giao-viec.md`](cap-00-chuan-bi-va-giao-viec.md): chuẩn bị dữ liệu, tìm quy định thật của sàn, viết prompt giao việc (nguyên văn, không sửa sau khi thấy kết quả).
2. [`cap-01-chay-that-va-kiem-tra.md`](cap-01-chay-that-va-kiem-tra.md): chạy Claude Code và Antigravity (`agy`), chấm bằng code, xem lỗi thật.
3. [`cap-02-dua-vao-dung-hang-ngay.md`](cap-02-dua-vao-dung-hang-ngay.md): quy trình lặp lại hằng ngày, người duyệt, giới hạn, mở rộng.

## Kết quả đo tóm tắt

**[Đo được]** ngày 2026-11-20, cùng prompt, cùng dữ liệu, 40 SKU. Mỗi agent chạy 2 lần (n=2, chỉ là quan sát, chưa đo được độ ổn định).

| Lần chạy | Thời gian | SKU sạch hoàn toàn (/40) | SKU thiếu thông số xử lý đúng (/9) | Ghi chú |
|---|---|---|---|---|
| Claude Code lần 1 | 241 s | 40 | 9 | không có lỗi trong phạm vi thước đo |
| Claude Code lần 2 | 298 s | 40 | 9 | không có lỗi trong phạm vi thước đo |
| Antigravity lần 1 | khoảng 11 đến 14 phút, **mất log** | 39 | 9 | 1 SKU có cụm "sản phẩm lành tính" không có trong bảng |
| Antigravity lần 2 | 756 s | 0 | 9 | cả 40 SKU có "chính hãng" (mô tả 40/40, từ khóa 37/40) không có trong bảng |

Cả hai agent đều: không dùng từ cấm, không bịa con số, không chép lời đồn có số, không nói "đã công bố" với SKU chỉ "đang chờ duyệt", gắn `CẦN BỔ SUNG` đúng 9 SKU, không báo động giả ở 31 SKU đủ thông tin. Cả hai đều tự viết `kiem.py` và tự báo "sạch 0 lỗi". Cái `kiem.py` của Antigravity lần 2 không bắt được "chính hãng". **Bài học chính: agent tự kiểm chỉ kiểm được những gì nó nghĩ ra để kiểm.**

![Bảng chấm 4 lần chạy](anh/07-bang-cham.webp)

*Bảng dựng từ `ket-qua/bao-cao-cham.json`.*

*Ảnh terminal dựng lại từ log đã che đường dẫn máy và tên tổ chức (script dựng: `ket-qua/dung_anh.py`).*

Chúng ta **không** kết luận agent nào tốt hơn từ 2 lần chạy mỗi bên. Chỉ mô tả quan sát.

## Giới hạn độ dài: giả định, và tìm được gì từ nguồn thật

Giới hạn trong `quy_dinh_shop.md` (tiêu đề 25 đến 100 ký tự, mô tả 200 đến 1500, mỗi gạch tối đa 120, từ khóa 6 đến 10 cụm) là **giả định của shop giả**, không phải quy định sàn. Đã thử đối chiếu với nguồn thật:

- **[Nguồn]** Shopee Việt Nam, trang trợ giúp "Quy định về đăng bán sản phẩm" (bản trước, cập nhật 15/3/2024): [help.shopee.vn](https://help.shopee.vn/portal/4/article/107999-QUY-%C4%90%E1%BB%8ANH-V%E1%BB%80-%C4%90%C4%82NG-B%C3%81N-S%E1%BA%A2N-PH%E1%BA%A8M-TR%C3%8AN-SHOPEE-(phi%C3%AAn-b%E1%BA%A3n-tr%C6%B0%E1%BB%9Bc)). Trang **không nêu số ký tự tối đa** cho tên sản phẩm. Có yêu cầu về nội dung: tên tiếng Việt có dấu, không ký tự đặc biệt, không viết tắt, không chứa từ như "Sản phẩm hot", "Bán chạy", "Giảm giá", "Miễn phí vận chuyển"; mô tả phải trung thực, không lập lờ. Bản này tự ghi là "phiên bản trước", có thể đã cũ.
- Giới hạn độ dài hiện hành của Shopee Việt Nam: **chưa xác minh**. Trang Seller Education Hub (`banhang.shopee.vn/edu/article/2100`) tải về không có nội dung đọc được. Một tài liệu mass upload của Shopee Malaysia (kết quả tìm kiếm, chưa mở file) nêu tên 20 đến 120 ký tự và mô tả 20 đến 3000 ký tự: đó là thị trường khác, không dùng làm căn cứ cho Việt Nam.
- TikTok Shop Việt Nam: kết quả tìm kiếm từ trung tâm người bán ([seller-vn.tiktok.com](https://seller-vn.tiktok.com/university/essay?knowledge_id=10008556&lang=en)) nói tiêu đề tối thiểu 25 ký tự và mỗi ý bán hàng trong mô tả dưới 250 ký tự. **Chưa đọc trọn trang**, chưa xác minh. Không tìm thấy mức tối đa chính thức.
- Danh sách từ cấm của sàn: Shopee không công khai đầy đủ; danh sách nhiều bài blog bên thứ ba đưa ra không phải nguồn chính thức. Danh sách trong bài là **của shop**, không phải của sàn.

Việc cần làm trước khi đăng thật: mở trang đăng sản phẩm trên Kênh Người Bán, thử dán một tiêu đề dài và một mô tả dài để biết giới hạn hiện hành, rồi sửa `quy_dinh_shop.md`.

## Cấu trúc thư mục

```
03-mo-ta-san-pham-hang-loat/
  00-README.md, bai-1-..., bai-2-..., bai-3-...
  du-lieu/    thong_so.csv/.xlsx, quy_dinh_shop.md, tu_cam.txt, mau_dau_ra.csv, kiem_hang_ngay.py, sinh_du_lieu.py
  ket-qua/    prompt-v1.txt, dap-an.json, cham.py, cham_kiem_thu.py, bao-cao-cham.json, cham-kiem-thu.json,
              và một thư mục cho mỗi lần chạy (đầu ra thật của agent, giữ cả bản có lỗi)
  logs/       claude-v1-lan1, claude-v1-lan2, agy-v1-lan2 (*.raw.jsonl và *.json)
  anh/        ảnh dùng trong bài
```

Thư mục làm việc tạm của agent (`runs/`) nằm ngoài bài, không đưa vào.

## Công cụ và phiên bản

Claude Code 2.1.329 (`claude --version`), Antigravity `agy` 1.5.13 (`agy --version`). Log của hai agent không ghi tên mô hình nên bài không nêu. Chi phí Claude Code do chính Claude Code báo: lần 1 khoảng 0,70 USD, lần 2 khoảng 0,86 USD. Antigravity không báo chi phí; lần 2 báo 166.211 token vào và 77.971 token ra.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây.
