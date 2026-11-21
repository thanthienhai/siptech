# Bài 1: Chuẩn bị dữ liệu và giao việc cho agent

> Mọi dữ liệu trong bài là **dữ liệu giả để học** (quán "Mây Lưng Chừng" hư cấu). Mọi con số gắn nhãn **[Đo được]** là kết quả chạy của chúng tôi ngày 2026-11-20; **[Nguồn]** có link; **[Đề xuất]** là ý kiến, không phải số đo.

## Mục tiêu đo được của bài này

Sau bài này bạn có: (1) thư mục làm việc sạch gồm đúng một file `danh-gia.csv` (250 dòng); (2) bản prompt 6 phần giao việc; (3) biết agent sẽ trả về bảy file nào và bạn sẽ kiểm từng file ra sao. Tiêu chí hoàn thành: chạy được `python -X utf8 -c "import csv;print(len(list(csv.DictReader(open('danh-gia.csv',encoding='utf-8')))))"` ra `250`, và thư mục agent **không** chứa file đáp án.

## 1. Vì sao không nên "đưa cả đống đánh giá cho chatbot rồi hỏi: tóm tắt giúp"

Cách phổ biến: dán 250 đánh giá vào khung chat, gõ "tóm tắt khách đang chê gì". Kết quả thường đọc trôi chảy nhưng bạn không kiểm được ba thứ: số đếm ("giá bị chê nhiều nhất" dựa trên số nào?), trích dẫn (có thật khách viết câu đó không?), và bài nào bị bỏ sót. Với coding agent bạn đổi cách làm: agent **đọc** từng bài để gán nhãn (việc cần hiểu tiếng Việt), còn **đếm** và **kiểm trích dẫn** là code (việc cần chính xác). Bài toán này chia việc đúng như vậy.

## 2. Dữ liệu: cái gì có trong `danh-gia.csv`

Tải thư mục `du-lieu/`: có `danh-gia.csv` (cho agent), `danh-gia.xlsx` (bản xem bằng Excel cho người), `sinh_du_lieu.py` (cách sinh, chạy lại ra đúng bộ cũ vì hạt giống cố định 20261120).

Cột: `ma` (R001...R250), `nen_tang` (Google Maps, Shopee Food, Facebook), `ngay`, `sao`, `noi_dung`.

![Trích 10 dòng của danh-gia.csv gồm bài không dấu, mỉa mai, bài nguy cấp, bài khen phóng đại](anh/d-du-lieu-dau-vao.webp)

*Ảnh 1: trích 10 trong 250 dòng của `danh-gia.csv`. Dữ liệu giả để học, do `sinh_du_lieu.py` sinh; ảnh dựng bằng cách vẽ bảng HTML từ file thật.*

Hãy nhìn kỹ ảnh: bài R001 có cả chữ kéo dài ("mêêêê"), R075 là câu mỉa mai ("Giá hợp lý lắm luôn, hợp lý với ví của chủ quán 🙃"), R077 viết không dấu, R050 là lời khen phóng đại nghe như chuyện nghiêm trọng ("ghiền như bị bỏ bùa"), R170 là bài nguy cấp thật (nôn mửa, đi cấp cứu). Cột `sao` trống ở bài Facebook, và ngày có hai kiểu (`24/08/2026` ở Google Maps, `2026-08-25` ở Shopee Food). Chính những chỗ này là bẫy.

### Các bẫy đã cài sẵn và đáp án

Mỗi bẫy có đáp án trong `ket-qua/dap-an.json` (đặt ngoài thư mục agent làm việc):

| Bẫy | Ví dụ thật trong dữ liệu | Đáp án đúng |
|---|---|---|
| Nhiều ý trong một bài | "đồ uống ngon, giá ok, nhưng nhân viên hơi chậm" (không dấu) | 3 ý: chat_luong tích cực, gia tích cực, phuc_vu tiêu cực |
| Mỉa mai | "Phục vụ nhanh ghê, chỉ đợi có 45 phút thôi à 👏👏" | phuc_vu, ý thật là chê, agent phải xếp `CAN_NGUOI_DOC` |
| Khen phóng đại như nguy cấp | "Cà phê muối ngon xỉu luôn 😍 uống xong tim đập loạn" | không phải nguy cấp |
| Nguy cấp thật | "...nôn mửa với tiêu chảy, phải đi cấp cứu..." | ngo_doc |
| Nguy cấp "nghi" | "tối đau bụng đi ngoài mấy lần. Không dám khẳng định do quán..." | ngo_doc, ghi chữ "nghi" |
| Bài trùng nguyên văn | 4 bài giống hệt một bài ở tuần trước | loại bỏ, ghi mã gốc |
| Spam / không phải đánh giá | link nhận quà, "Quán mở cửa tới mấy giờ ạ?" | loại bỏ |
| Sao lệch nội dung | "5 sao cho sự đều đặn: lần nào cũng quên order của mình" (5 sao) | tiêu cực/mỉa mai |
| Ngày hai kiểu | `24/08/2026` và `2026-08-25` | cùng tuần bắt đầu thứ Hai |
| Tiếng Anh | "Waited 30 minutes for a latte. Overpriced for the size." | phuc_vu tiêu cực, gia tiêu cực |
| Ca ranh giới | "Giá trên bill cao hơn menu 5k, chắc nhập sai thôi. Mình nhắc thì bạn sửa lại luôn" | báo hay không báo nguy cấp đều không bị phạt |

Con số tổng hợp xem ở `00-README.md`. Ngoài các bẫy, dữ liệu còn "cài" năm vấn đề thật theo thời gian (nghi ngộ độc, giao hàng xấu đi, tăng giá, thái độ nhân viên, tính tiền gian) để kiểm xem phần "5 việc nên sửa" có tìm ra không.

### Tại sao tự sinh mà không dùng bộ dữ liệu công khai

Chúng tôi có tìm: **[Nguồn]** UIT-ViSFD (<https://arxiv.org/abs/2105.15079>, bản Hugging Face <https://huggingface.co/datasets/visolex/ViSFD>) và UIT-ViSD4SA (<https://arxiv.org/abs/2110.07833>) là 11.122 bình luận tiếng Việt về điện thoại, gán nhãn khía cạnh và sắc thái. Giấy phép: thẻ dữ liệu bản Hugging Face ghi "xem LICENSE kho gốc, nếu không nêu thì coi là CC BY 4.0" và đề nghị liên hệ tác giả nếu dùng thương mại; bản SEACrowd ghi "không rõ". Vì không chắc chắn, chúng tôi chỉ dùng chúng để hiểu cách người viết (lẫn khía cạnh, nhãn ba mức) và **không chép câu nào**. Đây là bình luận về điện thoại chứ không phải quán cà phê, và bộ đó không có phần "nguy cấp" hay "xu hướng theo tuần", nên tự sinh mới cài được đáp án cho những yêu cầu này.

**Tự sinh hoạt động thế nào** (đọc `sinh_du_lieu.py` nếu muốn): có ngân hàng mệnh đề cho 6 chủ đề x 3 sắc thái, mỗi mệnh đề gán sẵn nhãn. Một bài = 1 đến 3 mệnh đề ghép bằng ", " hoặc "nhưng", sau đó thêm nhiễu (bỏ dấu 22%, teen code 35%, kéo dài chữ, emoji, câu đuôi kiểu "Hôm đó trời mưa"). Xu hướng theo tuần được cài bằng xác suất đổi theo tuần (ví dụ giá bị chê nhiều hẳn từ tuần thứ 6). 60 bài khó viết tay. Vì sinh từ mệnh đề lặp, đây là điểm yếu: bộ dữ liệu này **dễ hơn đánh giá thật** (xem bài 2).

## 3. Cách mở agent: từ đơn giản đến đúng cách chúng tôi chạy

Bạn không cần biết lập trình để dùng agent, nhưng cần biết ba thứ: thư mục làm việc, lệnh mở agent, và dán prompt.

**Bước 1. Tạo thư mục riêng cho một lần chạy.** Mỗi lần chạy một thư mục, vì agent sẽ tạo thêm file. Trên Windows mở Git Bash hoặc PowerShell:

```bash
mkdir chay-1
cp du-lieu/danh-gia.csv chay-1/
cd chay-1
```

Giải thích: `mkdir` tạo thư mục mới tên `chay-1`; `cp` chép đúng một file dữ liệu vào; `cd` đi vào thư mục đó. **Không chép `dap-an.json` vào**, nếu không agent có thể đọc thấy đáp án và kết quả chấm mất ý nghĩa.

**Bước 2. Mở agent.** Gõ `claude` (Claude Code) hoặc `agy` (Antigravity) rồi Enter. Cửa sổ trò chuyện hiện ra. Dán toàn bộ prompt ở mục 4 vào và Enter. Agent sẽ hỏi quyền đọc/ghi file; trong thư mục `chay-1` bạn có thể cho phép.

**Bước 3 (cách chúng tôi dùng, chạy một lệnh không cần ngồi canh).** Cả hai agent có chế độ `-p` (print): nhận prompt, tự làm, in kết quả rồi thoát. Chúng tôi bọc lệnh này trong `agent_run.py` để lưu log gốc. Tương đương lệnh tay:

```bash
claude -p "$(cat prompt-giao-viec.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash"
agy -p "$(cat prompt-giao-viec.txt)" --dangerously-skip-permissions
```

Giải thích từng phần: `-p` là chế độ một lần; `$(cat ...)` đọc file prompt ra thành chuỗi; `--permission-mode acceptEdits --allowedTools ...` cho phép Claude Code ghi file và chạy lệnh trong các công cụ liệt kê; `--dangerously-skip-permissions` của `agy` bỏ qua mọi câu hỏi xin phép, nghĩa là agent có **toàn quyền trên máy**. Vì vậy: chỉ chạy trong thư mục riêng, không để file quan trọng gần đó, và không chạy với dữ liệu thật chưa được che thông tin khách. Phiên bản chúng tôi dùng: Claude Code 2.1.329, `agy` 1.5.13 [Đo được: lấy từ `claude --version` và `agy --version`].

## 4. Prompt giao việc (bản dùng thật, không sửa sau khi thấy kết quả)

Prompt dùng khung 6 phần: Vai trò, Bối cảnh, Nhiệm vụ, Các bước, Định dạng ra, Ràng buộc. Toàn văn nằm ở `ket-qua/prompt-giao-viec.txt`; ảnh dưới là bản hiển thị đúng file đó.

![Prompt giao việc 6 phần gồm vai trò, bối cảnh, nhiệm vụ, tám bước, định dạng ra, ràng buộc](anh/a-prompt-giao-viec.webp)

*Ảnh 2: prompt giao việc (hiển thị lại nội dung `ket-qua/prompt-giao-viec.txt`).*

Vì sao viết như vậy (đây là phần dùng được cho mọi bài toán tương tự):

- **Bước 2 (loại bỏ) đặt trước bước 3 (gán nhãn).** Nếu không, bài trùng và spam bị đếm vào xu hướng. Hãy nhớ: đếm sai từ gốc thì mọi bảng sau đều sai.
- **Chỉ định cột và giá trị cho phép** (`chu_de`, `sac_thai`, `loai`). Không có điều này mỗi lần chạy agent sẽ đặt tên khác nhau và bạn không so sánh được. Đã có chủ đề `khac` để agent không phải ép ý lạc đề vào chủ đề sai.
- **"Sắc thái tính cho từng ý, không tính cho cả bài"**: câu này là cốt lõi của bài toán. Bỏ nó, agent sẽ gán một nhãn cho cả bài.
- **Bước 4 và ràng buộc cuối ("không chắc thì ghi `CAN_NGUOI_DOC`")**: cho agent một lối thoát hợp lệ. Nếu không có lối này, agent bị buộc phải đoán và mỉa mai sẽ bị gán thành "tích cực".
- **Bước 5 nêu cả ví dụ không phải nguy cấp** ("ngon xỉu", "ghiền như bị bỏ bùa"). Đây là hướng dẫn thật mà người dùng nên viết; nó cũng làm bẫy từ khóa dễ hơn thực tế. [Đề xuất] khi đo độ khó thật, thử bỏ câu này và xem agent báo thừa bao nhiêu.
- **Bước 6 buộc đếm bằng file `tong-hop.py`** đọc từ `y-kien.csv`. Cùng một file ý kiến, chạy lại luôn ra cùng bảng. Con số do code, không do trí nhớ của mô hình.
- **Bước 8 buộc viết và chạy bộ kiểm trích dẫn.** Mô hình ngôn ngữ có thể "sửa" câu của khách cho đẹp hơn; kiểm bằng `in` (chuỗi con) bắt được ngay.
- **"Chỉ đọc và ghi trong thư mục hiện tại"**: giới hạn phạm vi. (Bài 2 sẽ cho thấy một agent vẫn ghi file tạm ra ngoài.)

## 5. Chạy thử kiểm cấu trúc trước khi giao việc

Trước khi giao cho agent, tự kiểm dữ liệu bằng ba lệnh (đều chạy được trên máy có Python):

```bash
python -X utf8 -c "import csv;r=list(csv.DictReader(open('danh-gia.csv',encoding='utf-8')));print(len(r), r[0].keys())"
python -X utf8 -c "import csv,collections as c;r=list(csv.DictReader(open('danh-gia.csv',encoding='utf-8')));print(c.Counter(x['nen_tang'] for x in r))"
python -X utf8 -c "import csv;r=list(csv.DictReader(open('danh-gia.csv',encoding='utf-8')));print(sum(1 for x in r if x['sao']==''),'bài trống sao')"
```

Giải thích: dòng 1 đếm số dòng và in tên cột (phải ra 250 và `ma, nen_tang, ngay, sao, noi_dung`); dòng 2 đếm theo nền tảng [Đo được: 124, 73, 53]; dòng 3 đếm bài trống cột `sao` [Đo được: 32]. Cờ `-X utf8` bắt buộc trên Windows để in được tiếng Việt.

## 6. Lỗi thường gặp ở bước chuẩn bị

1. **Excel mở file CSV bị vỡ dấu tiếng Việt.** Dùng `danh-gia.xlsx` để xem; hoặc trong Excel chọn Data > From Text/CSV và chọn UTF-8. Đừng lưu lại đè lên `danh-gia.csv` từ Excel.
2. **Chép nhầm cả đáp án vào thư mục agent.** Kiểm bằng `ls`, trong thư mục chạy chỉ có `danh-gia.csv`.
3. **Dùng chung một thư mục cho hai lần chạy.** File lần trước còn đó, agent có thể đọc và "chép" kết quả, hoặc trộn lẫn.
4. **Prompt quá ngắn** ("phân tích đánh giá giúp tôi"). Agent sẽ chọn định dạng ra tùy ý; so sánh lần này với lần khác là không thể.
5. **Gửi dữ liệu thật có tên, số điện thoại khách cho dịch vụ đám mây.** Che trước (xem bài 3).

## Checklist trước khi giao việc

- [ ] Thư mục riêng, chỉ có `danh-gia.csv`.
- [ ] `dap-an.json` nằm ngoài thư mục agent.
- [ ] Prompt đủ 6 phần, có giá trị cho phép của từng cột, có lối thoát `CAN_NGUOI_DOC`.
- [ ] Biết lệnh chạy và nơi ghi log.
- [ ] Đã quyết định giới hạn thời gian (chúng tôi dùng 900 giây; bài 2 cho thấy `agy` có thể cần hơn).

## Việc cần người làm

- Chọn đúng bộ giá trị `chu_de` hợp với quán của bạn (quán cơm có thể cần "phần ăn", "chỗ để xe").
- Với dữ liệu thật: che tên, số điện thoại, địa chỉ khách trong nội dung đánh giá trước khi đưa cho agent.
- Quyết định ai nhận bài `CAN_NGUOI_DOC` và `nguy-cap.csv` mỗi tuần (bài 3).

## Giới hạn

- Dữ liệu là giả và có cấu trúc lặp, dễ hơn đánh giá thật. Mọi số đo ở bài 2 chỉ nói về bộ dữ liệu này.
- Chúng tôi chỉ dùng hai agent, mỗi agent một prompt. Đổi prompt có thể đổi kết quả; chúng tôi chưa thử các biến thể.
- Cấu hình `--dangerously-skip-permissions` của `agy` rủi ro; chỉ nên dùng trong thư mục thử nghiệm.
