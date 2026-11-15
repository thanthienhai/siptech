# Q5 — Lỗi, thử lại, chống chạy trùng

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

!!! tip "Tóm tắt nhanh"
    Một luồng làm việc tự động chạy thật sẽ gặp lỗi: mạng chập chờn, phần mềm bán hàng gửi lại cùng một đơn, hai người bấm cùng lúc. Nếu không chuẩn bị, bạn sẽ có phiếu kho trùng, email gửi hai lần, hoặc phiếu nằm im cả tuần mà không ai biết. Bài này dạy cách chặn việc **làm hai lần**, cách **thử lại có giới hạn**, cách gom việc hỏng vào một **hàng lỗi** để người xem mỗi sáng, và cách **phát hiện luồng ngừng chạy im lặng**. Sau bài, bạn có một bộ test 6 ca hỏng để chạy lại mỗi lần sửa luồng.

## 1) Mục tiêu và người đọc

**Bài này dành cho ai:** người dựng và bảo trì luồng tự động: nhân viên IT kiêm nhiệm, người làm Make/n8n/Apps Script (các công cụ nối phần mềm với nhau), người viết Python nhẹ. Bạn đã có quy trình Q4 hoặc luồng Q1 đang chạy thật. Nếu bạn chưa biết lập trình, vẫn đọc được phần giải thích; phần mã chỉ cần nhờ người biết code hoặc nhờ AI chạy giúp.

**Bạn cần chuẩn bị:**
- Một quy trình Q4 hoặc một luồng Q1 đang chạy thật, để có cái mà thử cho hỏng.
- Một nơi lưu bảng (Google Sheet, một tab, hoặc cơ sở dữ liệu nhỏ) để làm bảng `da_xu_ly` (bảng ghi những việc đã làm xong) và hàng lỗi.
- Một người được giao xem hàng lỗi mỗi sáng.

**Sau bài này bạn sẽ có:** bộ xử lý sự kiện chịu được 6 ca hỏng có chủ đích:
1. Nền tảng gửi lại cùng một sự kiện.
2. Hai lần chạy chồng nhau.
3. Lỗi mạng tạm thời.
4. Dữ liệu sai nghiệp vụ.
5. Chữ ký không hợp lệ.
6. Luồng ngừng chạy im lặng.

Kèm theo là **hàng lỗi** (dead-letter: nơi gom những việc không xử lý được để người xem lại) có người xem hằng ngày.

**Thứ bạn cầm đi được sau bài:** bộ test 6 ca hỏng, chạy lại được mỗi lần sửa luồng. Không cần AI. Cấp này áp dụng cả cho luồng không có bước AI.

## 2) Câu hỏi cấp này trả lời / lỗi của Q4

**Câu hỏi:** "Khi mạng chập chờn, nền tảng gửi lại, hai người bấm cùng lúc, hay AI trả kết quả lỗi, thì làm sao không tạo đơn trùng, không chi trùng, không mất phiếu?"

**Lỗi của Q4 [Đề xuất, quan sát]:** ba chuyện đã gặp. Một là phiếu kho tạo hai lần vì webhook được gửi lại (webhook là tin nhắn tự động mà phần mềm bán hàng gửi sang hệ thống của bạn mỗi khi có sự kiện, ví dụ có đơn mới). Hai là script (đoạn chương trình ngắn) chạy nửa chừng thì hết giờ, bị chạy lại từ đầu, nên gửi email hai lần. Ba là lỗi API (cổng để chương trình này gọi chương trình khác) bị nuốt mất, nên phiếu nằm im ở "chờ kiểm" một tuần.

**Phần đã có ở nhóm RAG, không lặp lại:** bài này không viết lại những điều sau, bạn xem ở bài tương ứng.
- Idempotent (làm một lần hay làm nhiều lần thì kết quả vẫn như nhau) bằng `idem_key` cho hàm ghi, thử lại chỉ cho hàm đọc và hàm idempotent: `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` mục 3.4.
- Lưu trạng thái theo mã phiếu, chạy lại từ bước lỗi: `cap-08-quy-trinh-nhieu-buoc.md` bài 8.5.
- Thử lại lỗi API có giới hạn: `cap-01-goi-api.md` bài C1.6.
- Log (nhật ký ghi lại những gì chương trình đã làm) và sổ sự cố: `cap-09-van-hanh.md` bài 9.1, 9.6.

Cấp này thêm phần riêng của luồng nghiệp vụ: **webhook gửi lại, khóa chống chạy đồng thời, phân loại lỗi, hàng lỗi, giám sát "im lặng"**.

## 3) Kiến thức nền

### 3.1 Nền tảng sẽ gửi lại [Nguồn]
- **Haravan (tài liệu webhook chính thức):** chờ phản hồi 5 giây; không phản hồi hoặc lỗi thì gửi lại 19 lần trong 48 giờ; không theo chuyển hướng (3xx tính là lỗi); 19 lần lỗi liên tiếp thì tự xóa đăng ký webhook. Mỗi lần gửi có chữ ký HMAC-SHA256 ở header `X-Haravan-Hmacsha256`; tài liệu khuyên trả 200 trước rồi mới xử lý.
- Hàm ý [Đề xuất]: (a) cùng một đơn có thể đến nhiều lần, nên bên nhận phải tự chống trùng; (b) xử lý lâu hơn 5 giây thì bị coi là lỗi và bị gửi lại, nên nhận nhanh, ghi vào hàng, xử lý sau; (c) luồng hỏng 2 ngày là mất đăng ký im lặng, nên cần giám sát "không có sự kiện".
- Các nền tảng khác (KiotViet, Sapo, Lark, Zalo): cơ chế gửi lại **chưa kiểm**. Mặc định coi là "có thể gửi lại".

!!! note "Từ khó trong mục này"
    **Haravan** là một phần mềm bán hàng của Việt Nam. **Phản hồi** là câu trả lời "đã nhận" mà bên nhận gửi ngược lại. **Mã 200** là mã nghĩa là "ổn", **mã 3xx** là mã nghĩa là "chuyển sang địa chỉ khác". **Header** là phần thông tin đi kèm tin nhắn, giống phong bì bên ngoài lá thư. **Chữ ký HMAC-SHA256** là một dãy ký tự tính ra từ nội dung tin và một khóa bí mật, để bên nhận biết tin này đúng là của Haravan gửi, không bị giả mạo.

!!! tip "Nói đơn giản"
    Phần mềm bán hàng giống người giao thư: nếu bạn không ra nhận trong 5 giây, họ quay lại gõ cửa tiếp, nhiều lần. Vì vậy cùng một đơn có thể đến tay bạn nhiều lần. Việc của bạn là ra nhận thật nhanh, ghi lại "đơn này đã nhận", và không làm lại nếu đơn đó đến lần nữa.

### 3.2 Chạy đồng thời [Nguồn]
- Google Apps Script có `LockService` để "ngăn truy cập đồng thời vào một đoạn code": khóa theo script (`getScriptLock`), theo tài liệu (`getDocumentLock`), theo người dùng (`getUserLock`); khóa chỉ có hiệu lực sau khi gọi `tryLock`/`waitLock`.
- Apps Script giới hạn 6 phút mỗi lần chạy và 30 lần chạy đồng thời mỗi người dùng. Hàm ý [Đề xuất]: việc dài phải chia lô, lưu "đã làm đến đâu", lần sau chạy tiếp.

!!! tip "Nói đơn giản"
    Khóa giống biển "đang có người dùng" trên cửa phòng họp: người thứ hai phải đợi hoặc quay lại sau, không xông vào cùng lúc. Apps Script là công cụ viết chương trình nhỏ trong Google Sheet/Gmail của Google. Mỗi lần chạy chỉ được 6 phút, nên việc dài phải cắt nhỏ và nhớ đã làm đến đâu.

### 3.3 Sửa được một lỗi chưa chắc làm xong việc [Nguồn]
- SpreadsheetBench 2 (phụ lục D.1): trong các việc agent gặp lỗi khi chạy, MiniMax M2.5 sửa được ít nhất một lỗi ở 72% (template), 47% (mô hình tài chính), 34% (sửa lỗi bảng tính), nhưng vẫn hoàn thành đúng toàn việc chỉ 7%, 9%, 3% (con số theo hình 10 và lời giải thích của bài; hình và chữ lệch nhau ở nhóm cuối, 2% hay 3%). Claude Opus 4.6 giảm ít hơn (50% → 45% ở mô hình tài chính).
- Hàm ý [Đề xuất]: khi một bước AI lỗi giữa chừng, "thử lại cho tới khi hết lỗi" không bảo đảm kết quả đúng. Lỗi lặp lại → dừng, vào hàng lỗi, người xem.

!!! note "Từ khó trong mục này"
    SpreadsheetBench 2 là một bộ bài thi dành cho AI làm việc với bảng tính. **Agent** là AI tự làm nhiều bước liên tiếp để hoàn thành một việc. **Template** là mẫu bảng tính dựng sẵn. **Mô hình tài chính** là bảng tính tính toán tài chính. MiniMax M2.5 và Claude Opus 4.6 là tên hai mô hình AI.

!!! tip "Nói đơn giản"
    Chương trình báo "hết lỗi" không có nghĩa là kết quả đúng. AI có thể sửa được một lỗi nhưng cuối cùng vẫn làm sai cả việc. Vì thế, khi một bước AI cứ lỗi lặp lại, đừng bắt nó thử mãi: dừng lại, cho vào hàng lỗi và để người xem.

### 3.4 Phân loại lỗi để biết có thử lại không [Đề xuất]

| Loại | Ví dụ | Thử lại? | Đi đâu |
|---|---|---|---|
| Tạm thời | timeout, mạng, 429, 5xx của API | Có, tối đa 3 lần, chờ tăng dần | Hết lần → hàng lỗi |
| Nghiệp vụ | số lượng ≤ 0, mã hàng không tồn tại, vượt hạn mức | Không | Hàng lỗi, báo người tạo phiếu |
| Bảo mật | sai chữ ký, sai token | Không | Từ chối (401), ghi log cảnh báo |
| Đầu ra AI sai lược đồ | JSON hỏng, nhãn ngoài danh sách | Tối đa 1 lần | Coi như "không chắc", về người |
| Không rõ (hàm ghi trả lỗi mơ hồ) | API tạo đơn timeout sau khi gửi | Không tự thử | Kiểm xem đơn đã tạo chưa (tra theo mã), rồi quyết định |

Cách đọc bảng: timeout là "đợi quá lâu không thấy trả lời"; 429 là mã "bạn gọi quá nhiều, đợi chút"; 5xx là mã "máy chủ bên kia đang lỗi"; 401 là mã "không được phép"; token là mã thông hành; JSON là cách viết dữ liệu có khung rõ ràng để máy đọc; lược đồ là khung quy định dữ liệu phải có những mục nào. "Chờ tăng dần" nghĩa là lần thử sau đợi lâu hơn lần trước.

Dòng cuối là chỗ hay gây trùng: lần gọi đầu có thể đã thành công dù bên mình nhận timeout.

!!! tip "Nói đơn giản"
    Mỗi loại lỗi có một cách xử lý riêng. Lỗi do mạng thì thử lại vài lần là đủ. Lỗi do dữ liệu sai (số lượng bằng 0) thì thử một nghìn lần vẫn sai, nên đưa thẳng cho người. Lỗi "không rõ" là nguy hiểm nhất: bạn không biết việc đã làm xong chưa, nên phải tra xem đơn có chưa trước khi làm lại.

## 4) Chuỗi bài nhỏ

Bảy bài thực hành dưới đây làm theo thứ tự. Mỗi bài có việc cần làm và thứ bạn có sau bài.

### Bài Q5.1 — Khóa chống trùng cho mọi hành động ghi
- **Việc cần làm:** mỗi hành động ghi có khóa duy nhất: `ma_don:tao_phieu_kho`, `ma_phieu:gui_email_duyet`. Bảng `da_xu_ly` với khóa là khóa chính. Trước khi ghi, tra bảng; có rồi thì trả kết quả cũ. (Khóa chính là cột mà bảng không cho phép hai dòng trùng nhau.)
- **Bạn có sau bài:** bảng `da_xu_ly` + danh sách hành động ghi và khóa của nó.
- **Lỗi hay gặp:** dùng thời điểm làm khóa (mỗi lần gửi lại khác thời điểm); chỉ chống trùng ở bước đầu.

### Bài Q5.2 — Nhận nhanh, xử lý sau
- **Việc cần làm:** điểm nhận webhook chỉ kiểm chữ ký, ghi sự kiện vào hàng, trả 200. Một tiến trình khác lấy từ hàng ra xử lý. (Hàng ở đây là một danh sách xếp theo thứ tự đến, giống hàng người chờ.)
- **Bạn có sau bài:** hàng sự kiện (bảng hoặc tab) với trạng thái `moi / dang_xu_ly / xong / loi`.

### Bài Q5.3 — Khóa chống chạy đồng thời
- **Việc cần làm:** Apps Script: bọc phần ghi bằng `LockService.getScriptLock()`; Python: ràng buộc khóa chính trong SQLite (lần ghi thứ hai báo lỗi toàn vẹn) hoặc khóa file. Thử: chạy hai lần cùng lúc. (SQLite là một cơ sở dữ liệu nhỏ nằm trong một file.)
- **Bạn có sau bài:** bài thử "hai lần cùng lúc" → 1 bản ghi.

### Bài Q5.4 — Thử lại có giới hạn và hàng lỗi
- **Việc cần làm:** theo bảng 3.4. Hàng lỗi có: khóa, lý do, dữ liệu gốc (đã che), thời điểm, người phụ trách. Mỗi sáng một người xem hàng lỗi; xử lý xong ghi cách xử lý.
- **Bạn có sau bài:** hàng lỗi + quy tắc xem hằng ngày.

### Bài Q5.5 — Chạy lại an toàn
- **Việc cần làm:** nút "chạy lại" cho một phiếu trong hàng lỗi: đi qua cùng khóa chống trùng, nên bước đã thành công không làm lại.
- **Bạn có sau bài:** bài thử "lỗi ở bước 3, chạy lại" → bước 1-2 không lặp.

### Bài Q5.6 — Giám sát "im lặng"
- **Việc cần làm:** cảnh báo khi: không có sự kiện mới trong N giờ làm việc; hàng lỗi > M mục; tỷ lệ lỗi trong ngày > X%. Đối chiếu số đơn trên phần mềm với số đơn đã xử lý mỗi ngày (bài Q1.4). (N, M, X là các con số bạn tự chọn cho phù hợp; xem mục 9.)
- **Bạn có sau bài:** 3 cảnh báo + đối chiếu ngày.

### Bài Q5.7 — Bộ test 6 ca hỏng
- **Việc cần làm:** gói 6 ca ở mục 1 thành script chạy được; chạy trước mỗi lần sửa luồng. (Bạn có thể nhờ người biết code hoặc nhờ AI viết script này.)
- **Bạn có sau bài:** script test + kết quả lần chạy gần nhất.

## 5) Đường không code vs có code; khi nào buộc chuyển

Bài này có hai cách làm. Cách không code dùng tính năng có sẵn của công cụ như Make, n8n, Lark. Cách có code cần một chút lập trình để chặt chẽ hơn.

| | Không code | Có code |
|---|---|---|
| Chống trùng | Bộ lọc "nếu mã đã có trong bảng thì dừng" ở bước đầu luồng Make/n8n/Lark | Khóa chính trong bảng `da_xu_ly` cho mọi hành động ghi |
| Đồng thời | Thường không kiểm soát được rõ; tránh bằng cách cho một luồng duy nhất ghi | `LockService`, ràng buộc khóa chính |
| Thử lại | Cài đặt thử lại có sẵn của nền tảng (chi tiết từng nền tảng **chưa kiểm**) | Tự viết theo bảng 3.4 |
| Hàng lỗi | Tab "lỗi" + thông báo | Bảng + nút chạy lại |

**Buộc chuyển sang code [Đề xuất] khi:** có hành động ghi tốn tiền hoặc ra ngoài (tạo đơn, gửi tin khách, tạo chứng từ); nền tảng nguồn có gửi lại (như Haravan); đã từng có một lần trùng thật.

**Code mẫu (đã chạy thử 2026-11-11 bằng `python -I`, hàm giả thay API kho).** Kết quả: lần đầu gặp timeout, thử lại, tạo `PK-DH00007`; nền tảng gửi lại cùng đơn → trả kết quả cũ, không gọi hàm ghi lần nữa; chữ ký giả → 401; đơn số lượng 0 → hàng lỗi, không thử lại.

**Đoạn mã dưới đây làm gì?** Nó là một bộ xử lý đơn hàng thu nhỏ. Khi một đơn đến, nó kiểm chữ ký trước; sai thì từ chối. Rồi nó tra bảng xem đơn này đã làm chưa; nếu rồi thì trả kết quả cũ, không làm lại. Nếu chưa, nó tạo phiếu kho: gặp lỗi tạm thời thì thử lại tối đa 3 lần, chờ lâu dần; gặp lỗi nghiệp vụ thì cho thẳng vào hàng lỗi. Cuối cùng nó ghi lại "đã làm xong". Bạn **không cần đọc hiểu từng dòng**; chỉ cần nắm ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

```python
import base64, hashlib, hmac, json, sqlite3, time
SECRET = b"khoa-bi-mat-demo"
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE da_xu_ly (khoa TEXT PRIMARY KEY, ket_qua TEXT, ts REAL)")
db.execute("CREATE TABLE hang_loi (khoa TEXT, ly_do TEXT, du_lieu TEXT, ts REAL)")
class LoiTamThoi(Exception): pass

def ky(body): return base64.b64encode(hmac.new(SECRET, body, hashlib.sha256).digest()).decode()

def xu_ly(body, chu_ky, tao_phieu_kho, max_thu=3):
    if not hmac.compare_digest(ky(body), chu_ky): return 401, "sai chu ky"
    don = json.loads(body); khoa = f"{don['ma_don']}:tao_phieu_kho"
    cu = db.execute("SELECT ket_qua FROM da_xu_ly WHERE khoa=?", (khoa,)).fetchone()
    if cu: return 200, f"da xu ly truoc do: {cu[0]}"
    for lan in range(1, max_thu + 1):
        try: kq = tao_phieu_kho(don); break
        except LoiTamThoi as e:
            time.sleep(0.01 * 2 ** lan)                        # chờ tăng dần
            if lan == max_thu:
                db.execute("INSERT INTO hang_loi VALUES (?,?,?,?)", (khoa, str(e), body.decode(), time.time()))
                return 200, "vao hang loi"
        except ValueError as e:                                # lỗi nghiệp vụ: không thử lại
            db.execute("INSERT INTO hang_loi VALUES (?,?,?,?)", (khoa, str(e), body.decode(), time.time()))
            return 200, "vao hang loi (nghiep vu)"
    try: db.execute("INSERT INTO da_xu_ly VALUES (?,?,?)", (khoa, kq, time.time()))
    except sqlite3.IntegrityError: return 200, "chay song song, ban kia da ghi"
    return 200, kq
```

Giới hạn của mẫu: xử lý ngay trong lời gọi (chưa tách "nhận nhanh, xử lý sau"); nếu hàm ghi bên ngoài đã thành công mà ghi `da_xu_ly` thất bại thì vẫn có thể trùng ở lần sau. Muốn chặt hơn, hàm ghi bên ngoài cũng phải nhận khóa chống trùng (nếu API hỗ trợ) hoặc tra "đơn đã có phiếu kho chưa" trước khi tạo. Đoạn code đúng như in ở trên cũng đã được chạy lại (2026-11-11) với một hàm `tao_phieu_kho` giả truyền vào, cho cùng kết quả.

!!! tip "Nói đơn giản"
    Đoạn mã này làm đúng ba việc: kiểm tin có thật không, nhìn sổ xem đơn đã làm chưa, và nếu lỗi thì thử lại có hạn hoặc cho vào hàng lỗi. Mẫu này chưa hoàn hảo: nếu việc bên ngoài đã xong mà ghi sổ thất bại, đơn vẫn có thể bị làm lại ở lần sau.

## 6) Tiêu chí lên Q6 (đo được) [Đề xuất]

1. Bộ test 6 ca hỏng đạt 6/6 và chạy lại trước mỗi lần sửa luồng.
2. 4 tuần chạy thật: 0 hành động ghi trùng (đối chiếu bảng `da_xu_ly` với hệ thống đích).
3. Hàng lỗi được xem mỗi ngày làm việc; mục cũ nhất không quá 2 ngày.
4. Đã có ít nhất một lần cảnh báo "im lặng" hoặc đối chiếu ngày bắt được vấn đề, hoặc đã thử bằng cách tắt luồng có chủ đích.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

Ba tình huống giả định để bạn dễ hình dung.

**a) Cửa hàng mỹ phẩm dùng Haravan + n8n tự host (tiếp Q1).** Máy chủ n8n khởi động lại lúc 2 giờ sáng; Haravan gửi lại các đơn trong đêm vào buổi sáng. Không có khóa chống trùng → nhóm đóng gói nhận 2 thông báo, đóng 2 lần. Sửa: bước đầu luồng tra `ma_don` trong bảng đã xử lý; thêm cảnh báo khi 3 giờ làm việc liền không có đơn.

**b) Công ty xây lắp: Apps Script gửi email duyệt (tiếp Q4).** Hai kế toán cùng bấm "kiểm đạt" một phiếu trong vài giây → trưởng công trình nhận 2 email, duyệt 2 lần. Sửa: `LockService` quanh hàm chuyển trạng thái; khóa `ma_phieu:gui_email_duyet`; hàm chuyển trạng thái từ chối vì phiếu đã ở `cho_duyet_tp`.

**c) Nhà phân phối nông sản: bước AI đọc đơn Zalo trả JSON hỏng khi tin dài.** Thử lại 1 lần; vẫn hỏng → phiếu về sale với tin gốc, không thử tiếp. Đếm tỷ lệ này hằng tuần; nếu tăng sau khi đổi mô hình, chạy lại bộ ca (`../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` bài 9.3).

## 8) Tài liệu tham khảo

| Nguồn | Loại | Mức đọc | Tin cậy |
|---|---|---|---|
| Haravan, Connect webhook, https://docs.haravan.com/docs/tutorials/webhooks/connect-webhook/ | Tài liệu chính thức | Đọc trực tiếp | Cao; hay đổi |
| Google Apps Script LockService, https://developers.google.com/apps-script/reference/lock/lock-service | Tài liệu chính thức | Đọc trực tiếp | Cao |
| Google Apps Script quotas | Tài liệu chính thức | Đọc trực tiếp | Cao; hay đổi |
| SpreadsheetBench 2, arXiv 2606.29955, phụ lục D.1 | Benchmark | Toàn văn phụ lục | Cao cho benchmark |
| `../rag-tra-cuu-tai-lieu/cap-01`, `cap-07`, `cap-08`, `cap-09` | Tài liệu nội bộ | — | — |

## 9) Chưa kiểm chứng

- Cơ chế gửi lại, chữ ký, khóa chống trùng phía API của KiotViet, Sapo, MISA, Lark, Zalo: chưa đọc.
- Cài đặt thử lại/xử lý lỗi có sẵn của Make, Zapier, n8n: chưa đọc tài liệu chính thức.
- Thời gian chờ `tryLock/waitLock` (đơn vị, mặc định): trang tham chiếu đã đọc không nêu rõ.
- Các ngưỡng (3 lần thử, 2 ngày, N giờ, M mục, X%) là đề xuất.
- Code mẫu chưa chạy với webhook thật, chưa chạy đồng thời thật (chỉ mô phỏng bằng ràng buộc khóa chính).
