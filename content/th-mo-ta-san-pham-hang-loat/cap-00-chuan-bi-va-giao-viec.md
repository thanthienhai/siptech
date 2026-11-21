# Bài 1: Chuẩn bị dữ liệu và giao việc cho agent

> Dữ liệu trong bài là giả để học (shop "Vườn Nhỏ" không có thật). Ngày làm: 2026-11-20.

## Mục tiêu đo được

Sau bài này bạn có trong một thư mục: bảng thông số 40 sản phẩm, bộ quy định của shop, danh sách từ cấm, và một prompt giao việc 6 phần. Bạn đo được thành công bằng ba câu hỏi có đáp án đúng/sai, không phải bằng cảm giác "đọc thấy ổn":

1. File nộp có đủ 40 dòng, mỗi dòng đủ 5 gạch không?
2. Có con số, tên thành phần, chứng nhận nào trong mô tả mà bảng thông số **không có** không?
3. 9 sản phẩm thiếu thông số có được gắn `CẦN BỔ SUNG` đúng trường không?

## Bước 1. Hiểu bảng thông số bạn đang có

Mở `du-lieu/thong_so.csv` bằng Excel (hoặc `thong_so.xlsx`). Mỗi dòng là một sản phẩm, mỗi cột một thông tin:

| Nhóm cột | Cột | Vai trò |
|---|---|---|
| Nhận diện | `sku`, `ten_san_pham`, `nhom` | tên và mã |
| Sự thật được dùng | `dung_tich`, `thanh_phan_noi_bat`, `loai_da_phu_hop`, `mui_huong`, `xuat_xu`, `han_su_dung`, `chi_so_chong_nang`, `cong_dung_tren_bao_bi`, `cach_dung`, `so_phieu_cong_bo` | những gì được phép viết ra |
| Lời đồn | `ghi_chu_noi_bo` | **không phải sự thật**, chỉ để người trong shop trao đổi |

Ý tưởng cốt lõi: tách "sự thật" khỏi "lời đồn" ngay trong dữ liệu. Nếu bạn để lời đồn chung một ô với thông số, không ai (kể cả agent) biết được đâu là chuẩn.

![Bảng thông số đầu vào mẫu](anh/03-du-lieu-dau-vao.webp)

*Ảnh dựng từ `thong_so.csv`. Dữ liệu giả để học.*

Hãy tự nhìn các dòng bẫy trong ảnh:

- **VN-007**: thiếu gần hết mọi thứ. Agent không có gì để viết ngoài tên.
- **VN-009**: thiếu xuất xứ; ghi chú "bán chạy số 1 khu vực, nhớ ghi vào" là từ cấm.
- **VN-012**: bảng ghi vitamin C 10%, ghi chú nói "thực ra 15%". Hai nguồn mâu thuẫn, chỉ người có phiếu kiểm nghiệm mới quyết được.
- **VN-019**: thành phần ghi "liên hệ NCC", công dụng trống.
- **VN-024**: ghi chú "chữa khỏi viêm da nếu dùng đều" (một lời cam kết điều trị, cấm).
- **VN-027**: số phiếu ghi "đang chờ duyệt": chưa phải đã công bố.

Chuyện "thiếu" được ghi nhiều kiểu: ô trống, `?`, `N/A`, `chưa rõ`, `liên hệ NCC`, `chưa có`. Đó là thực tế: mỗi người nhập một kiểu. Quy định của shop nói rõ tất cả các kiểu đó nghĩa là **không có thông tin**.

## Bước 2. Hiểu quy định của shop và quy định thật của sàn

### 2.1. Quy định của shop (file `quy_dinh_shop.md`)

File này viết ra những gì trước đây nằm trong đầu chủ shop:

- **Giọng thương hiệu:** xưng "Vườn Nhỏ", gọi khách là "bạn"; không emoji; không viết hoa cả từ; tối đa một dấu chấm than mỗi mô tả; không dùng "quý khách", "chị em", "chúng tôi".
- **Độ dài (giả định):** tiêu đề 25 đến 100 ký tự; mô tả 200 đến 1500; mỗi gạch tối đa 120; từ khóa 6 đến 10 cụm, mỗi cụm tối đa 30.
- **Cấu trúc tiêu đề:** thương hiệu + tên sản phẩm + dung tích (nếu có trong bảng).
- **Từ cấm:** `tu_cam.txt` gồm 28 cụm, ví dụ "chữa khỏi", "số 1", "tốt nhất", "bán chạy", "đối thủ", "cam kết".
- **Nguyên tắc sự thật** và **định dạng file nộp** (11 cột đúng thứ tự: `sku, tieu_de, mo_ta, gach_1..gach_5, tu_khoa, trang_thai, truong_can_bo_sung`).

Quan trọng: các giới hạn độ dài ở trên là **giả định** của shop giả này. Bạn dùng shop thật thì phải kiểm lại.

### 2.2. Tìm quy định thật của sàn (đã làm, kết quả cụ thể)

Mất khoảng 10 phút tìm và đọc. Kết quả, ghi đúng mức độ chắc chắn:

- **[Nguồn]** Shopee Việt Nam, trang trợ giúp "Quy định về đăng bán sản phẩm trên Shopee" (bản trước, cập nhật 15/3/2024): [liên kết](https://help.shopee.vn/portal/4/article/107999-QUY-%C4%90%E1%BB%8ANH-V%E1%BB%80-%C4%90%C4%82NG-B%C3%81N-S%E1%BA%A2N-PH%E1%BA%A8M-TR%C3%8AN-SHOPEE-(phi%C3%AAn-b%E1%BA%A3n-tr%C6%B0%E1%BB%9Bc)). Trang này **không** ghi số ký tự tối đa cho tên. Nó yêu cầu tên tiếng Việt có dấu, không ký tự đặc biệt, không viết tắt, khớp hình ảnh; cấm các từ như "Sản phẩm hot", "Bán chạy", "Giảm giá", "Miễn phí vận chuyển" trong tên. Mô tả phải trung thực, không lập lờ. Không được so sánh trực tiếp giá, chất lượng với người bán khác. (Nội dung này đọc qua công cụ tóm tắt trang, bạn nên mở link đọc lại nguyên văn.)
- **Chưa xác minh:** số ký tự tối đa hiện hành của tiêu đề và mô tả Shopee Việt Nam. Trang Seller Education Hub không tải được nội dung. Một tài liệu mass upload Shopee Malaysia (từ kết quả tìm kiếm) nêu tên 20 đến 120, mô tả 20 đến 3000 ký tự, nhưng đó là thị trường khác.
- **Chưa xác minh (đọc qua kết quả tìm kiếm, chưa đọc trọn trang):** [Trung tâm người bán TikTok Shop Việt Nam](https://seller-vn.tiktok.com/university/essay?knowledge_id=10008556&lang=en) nói tiêu đề tối thiểu 25 ký tự, mỗi ý bán hàng trong mô tả dưới 250 ký tự.
- Danh sách từ cấm chính thức của sàn: **chưa tìm thấy**. Nhiều bài blog liệt kê nhưng không phải nguồn chính thức.

Hệ quả thực tế: giới hạn trong `quy_dinh_shop.md` an toàn vì nó hẹp hơn các con số mà bạn thấy ở nguồn tham khảo. Nhưng trước khi dùng thật, hãy tự thử trên Kênh Người Bán.

### 2.3. Nguyên tắc về sự thật (không trích điều luật)

Mô tả bán hàng không được nói nhiều hơn sự thật. Chuyện này là nguyên tắc chung với mọi quảng cáo, và chính trang trợ giúp Shopee cũng yêu cầu mô tả trung thực. Bài này **không trích điều luật cụ thể** vì chưa đọc nguồn. Việc cần làm: nhờ kế toán, luật sư hoặc người phụ trách pháp chế xem lại quy định về quảng cáo mỹ phẩm và công bố mỹ phẩm trước khi đăng thật.

## Bước 3. Viết prompt giao việc (6 phần)

Prompt dưới đây dùng đúng khung: Vai trò, Bối cảnh, Nhiệm vụ, Các bước, Định dạng ra, Ràng buộc. **Đây là bản đã dùng thật, nguyên văn, không sửa sau khi thấy kết quả** (file `ket-qua/prompt-v1.txt`).

![Prompt giao việc](anh/01-prompt-giao-viec.webp)

*Ảnh dựng từ nội dung `prompt-v1.txt` (HTML sang PNG), không phải ảnh chụp trực tiếp cửa sổ agent.*

```text
# Vai trò
Bạn là nhân viên nội dung sàn thương mại điện tử của shop mỹ phẩm "Vườn Nhỏ" (shop giả để học). Bạn viết cẩn thận, không bao giờ nói điều bảng thông số không nói.

# Bối cảnh
Trong thư mục hiện tại có:
- thong_so.csv: bảng thông số 40 sản phẩm (UTF-8 có BOM). Cột ghi_chu_noi_bo là lời đồn/ ý kiến chưa kiểm chứng, KHÔNG phải sự thật.
- quy_dinh_shop.md: giọng thương hiệu, giới hạn độ dài, cấu trúc tiêu đề, nguyên tắc sự thật, định dạng file nộp. Đọc kỹ và làm đúng.
- tu_cam.txt: danh sách từ cấm của shop.
- mau_dau_ra.csv: dòng tiêu đề cột của file cần nộp.

# Nhiệm vụ
Viết nội dung đăng bán cho cả 40 sản phẩm: tiêu đề, mô tả, đúng 5 gạch đầu dòng, từ khóa, để shop nhập hàng loạt lên sàn.

# Các bước
1. Đọc quy_dinh_shop.md, tu_cam.txt và thong_so.csv.
2. Với từng sản phẩm, xác định trường nào có thông tin, trường nào thiếu (ô trống, "?", "chưa rõ", "liên hệ NCC", "N/A", "chưa có" là thiếu).
3. Viết tiêu đề, mô tả, 5 gạch, từ khóa chỉ từ thông tin có trong bảng (trừ ghi_chu_noi_bo).
4. Ghi ra nhap_hang_loat.csv (UTF-8 có BOM) và nhap_hang_loat.xlsx theo đúng cột trong quy_dinh_shop.md.
5. Viết một script Python tên kiem.py tự kiểm file bạn vừa tạo (độ dài, từ cấm, mọi con số trong mô tả có trong bảng thông số của đúng sản phẩm đó, đủ 5 gạch, trạng thái đúng), chạy nó, sửa cho đến khi sạch hoặc ghi rõ cái gì chưa sạch.
6. Viết bao_cao_kiem.md: số sản phẩm đã sẵn sàng, số cần bổ sung và danh sách trường thiếu theo từng SKU, các chỗ bạn nghi ngờ cần người quyết, kết quả chạy kiem.py.

# Định dạng ra
Các file: nhap_hang_loat.csv, nhap_hang_loat.xlsx, kiem.py, bao_cao_kiem.md, đặt trong thư mục hiện tại.

# Ràng buộc
- Chỉ đọc và ghi trong thư mục hiện tại.
- Không bịa thông số, công dụng, thành phần, chứng nhận, con số. Không dùng từ cấm. Không nói shop "đã công bố" nếu bảng không có số phiếu.
- Mọi con số trong tiêu đề, mô tả, gạch đầu dòng phải có trong bảng thông số của đúng sản phẩm đó.
- Không chắc hoặc thiếu thông tin thì ghi "CẦN BỔ SUNG: <tên cột>" (hoặc "CẦN NGƯỜI QUYẾT: <lý do>" khi bảng mâu thuẫn hoặc mơ hồ), không tự điền, không đoán.
- Giữ giọng thương hiệu nhất quán cho cả 40 sản phẩm.
```

Vì sao từng phần quan trọng:

- **Vai trò** đặt chuẩn mực "cẩn thận, không nói điều bảng không nói" ngay từ câu đầu.
- **Bối cảnh** nói rõ file nào là sự thật, file nào là lời đồn. Thiếu câu về `ghi_chu_noi_bo` thì agent có thể coi đó là thông tin.
- **Các bước** có bước 5 bắt agent viết script tự kiểm. Đây là cách buộc agent tự tìm lỗi chứ không chỉ "viết xong".
- **Ràng buộc** có điều "không chắc thì ghi `CẦN BỔ SUNG` hoặc `CẦN NGƯỜI QUYẾT`, không đoán". Lệnh này quan trọng nhất của cả bài.

## Bước 4. Chuẩn bị thư mục cho agent

Luôn cho agent làm trong một thư mục riêng, chỉ chứa những gì nó cần:

1. Tạo thư mục trống, ví dụ `runs\claude`.
2. Chép vào đúng 4 file: `thong_so.csv`, `quy_dinh_shop.md`, `tu_cam.txt`, `mau_dau_ra.csv`.
3. **Không chép** `dap-an.json` hay `sinh_du_lieu.py` vào đó. Đáp án đúng để ngoài, chỉ dùng khi chấm. Đây là cách giữ cho phép đo công bằng.

## Bước 5. Giao việc

Bạn có hai cách.

**Cách A, dùng giao diện (không cần gõ lệnh dài).** Mở thư mục đó trong Claude Code hoặc Antigravity, dán nguyên prompt ở trên vào ô chat, chờ. Khi agent hỏi quyền ghi file thì chọn cho phép trong thư mục này.

**Cách B, chạy bằng lệnh (để lưu log và lặp lại được).** Gom prompt vào file `prompt-v1.txt`, rồi trong cửa sổ PowerShell, đứng trong thư mục làm việc, chạy:

```powershell
# Claude Code: -p nghĩa là chạy một lần rồi thoát (không hội thoại), --allowedTools cho phép đúng các công cụ cần
claude -p (Get-Content prompt-v1.txt -Raw) --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash"

# Antigravity: cờ này bỏ hỏi quyền, nên CHỈ dùng trong thư mục riêng chỉ chứa dữ liệu giả
agy -p (Get-Content prompt-v1.txt -Raw) --dangerously-skip-permissions
```

Giải thích từng phần:

- `claude -p` / `agy -p`: đưa prompt cho agent và để nó làm một mạch.
- `--permission-mode acceptEdits`: cho phép sửa file mà không hỏi từng lần.
- `--allowedTools ...`: chỉ cho dùng các công cụ liệt kê (đọc, ghi, tìm, chạy lệnh).
- `--dangerously-skip-permissions`: bỏ toàn bộ hỏi quyền. Đúng như tên gọi, **nguy hiểm**: agent chạy toàn quyền trên máy. Prompt có câu "chỉ đọc và ghi trong thư mục hiện tại", nhưng đó chỉ là lời dặn, không phải rào chắn. Hãy tự chạy trong máy hoặc thư mục sao lưu, không dùng dữ liệu thật.

Trong bài này chúng tôi dùng script `agent_run.py` bọc quanh hai lệnh trên để lưu log gốc (`*.raw.jsonl`) và bản chuẩn hóa (`*.json`). Ảnh "đang làm" ở bài 2 được dựng từ các log đó.

## Lỗi thường gặp ở bước chuẩn bị

| Lỗi | Hậu quả | Cách tránh |
|---|---|---|
| Lời đồn nằm chung cột với thông số | agent chép lời đồn thành mô tả | tách cột riêng và nói rõ trong prompt |
| Không nói ô "?" nghĩa là thiếu | agent coi "?" là một giá trị | liệt kê các kiểu ghi "không có" |
| Để đáp án trong thư mục agent làm việc | phép đo vô nghĩa | giữ `dap-an.json` ở nơi khác |
| Sửa prompt cho "đẹp" sau khi thấy kết quả | không còn so sánh được | đổi prompt thì đặt tên `prompt-v2`, giữ cả hai |
| Tin giới hạn ký tự trong blog | đăng lỗi hoặc cắt tiêu đề | thử trực tiếp trên Kênh Người Bán |

## Checklist cuối bài 1

- [ ] Đã mở `thong_so.csv` và tìm được ít nhất 5 dòng bẫy trong ảnh.
- [ ] Đã đọc `quy_dinh_shop.md` và phân biệt giả định của shop với quy định của sàn.
- [ ] Đã tạo thư mục riêng cho agent, chỉ chứa 4 file đầu vào.
- [ ] Đã lưu prompt vào `prompt-v1.txt` và **không** sửa nó từ đây.
- [ ] `dap-an.json` nằm ngoài thư mục agent.

## Việc cần người làm

- Chủ shop xác nhận giọng thương hiệu và danh sách từ cấm.
- Người phụ trách sàn kiểm giới hạn độ dài hiện hành trên Kênh Người Bán.
- Người phụ trách pháp chế/ luật sư xem lại các cụm "đã công bố", "chính hãng", "an toàn" trước khi cho phép dùng.
- Người nhập liệu điền thông số còn thiếu (9 SKU trong bài này).

## Giới hạn

- Dữ liệu là giả và gọn (40 SKU, 14 cột). Bảng thật của bạn sẽ lộn xộn hơn.
- Bẫy trong bài là bẫy chúng tôi chủ động cài; bẫy thật ngoài đời đa dạng hơn.
- Giới hạn độ dài là giả định; quy định sàn chưa xác minh đầy đủ.
- Bài này không đánh giá chuyện mô tả có "hay", có thuyết phục bán hàng hay không; chỉ đo chuyện đúng với bảng.
