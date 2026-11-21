# Bài 2: Chạy thật và chấm bằng đáp án

> **Dữ liệu giả để học.** Mọi số liệu **[Đo được]** dưới đây là kết quả chạy ngày 2026-11-20, n = 1-2 lần mỗi agent hợp lệ, chưa đo được độ ổn định. Không có kết luận "agent nào tốt hơn".

## Mục tiêu đo được

1. Chạy hai agent (Claude Code `claude`, Antigravity `agy`) với **cùng prompt, cùng dữ liệu** của bài 1.
2. Chấm kết quả bằng chương trình `ket-qua/cham.py` so với `ket-qua/dap-an.json`: dòng hàng, bậc giá, các dòng tổng, trạng thái, câu hỏi/ca cần người quyết, hàng bịa, lời hứa ngày giao.
3. Đọc tay các ca khác đáp án để biết đó là lỗi của agent hay lỗi của đáp án.

## Bước 1. Chạy

Lệnh dùng (từ thư mục bài, mỗi lần chạy một thư mục riêng đã chép sẵn 4 file đầu vào và `yeu-cau/`):

```
python -X utf8 agent_run.py claude  <thu_muc_chay>  ket-qua/prompt-giao-viec.txt  <tien_to_log>  1500
python -X utf8 agent_run.py agy     <thu_muc_chay>  ket-qua/prompt-giao-viec.txt  <tien_to_log>  1500
```

`agent_run.py` mở agent ở chế độ không tương tác, chờ tối đa 1500 giây, lưu log gốc `<tien_to_log>.raw.jsonl` và transcript `<tien_to_log>.json`. Hai agent chạy **song song** (mỗi lần 2 tiến trình).

Chúng tôi có 6 lần chạy:

| Lần | Chạy ở đâu | Log | Ghi chú |
|---|---|---|---|
| claude-0, agy-0 | thư mục trong vùng làm việc | **mất** | tiến trình bị dừng trước khi ghi log; file `dau-ra/` đã tạo xong nên vẫn chấm |
| claude-1, agy-1 | thư mục trong vùng làm việc | có | `agy-1` bị loại (xem bước 5) |
| claude-2, agy-2 | `%TEMP%\al05-<agent>\run`, cô lập | có | lần chạy sạch |

Thời gian và chi phí **[Đo được]** (đọc từ log; Claude Code báo chi phí tính theo giá niêm yết, chúng tôi không biết bạn trả bao nhiêu theo gói thuê bao):

| Lần | Thời gian | Số khối trong transcript | Token / chi phí |
|---|---|---|---|
| claude-1 | 378,3 s | 18 | 54.113 token ra; 1,04 USD |
| claude-2 | 432,5 s | 15 | 62.412 token ra; 1,19 USD |
| agy-1 | 753,8 s | 35 | log không có chi phí |
| agy-2 | 962,5 s | 24 | 173.743 token vào, 110.581 token ra |

Thời gian dài hay ngắn còn phụ thuộc máy đang bận (lúc đó máy chạy nhiều tác vụ khác song song), nên **đừng** đọc đây là "agent này nhanh hơn".

Ảnh dưới là bước kiểm tra cuối và câu trả lời cuối của Claude Code trong lần `claude-1`:

![Bước kiểm tra cuối và câu trả lời cuối của Claude Code (claude-1).](anh/03-claude-ket-qua-cuoi.webp)

*Dựng lại từ log thật của lần chạy `claude-1`, không phải ảnh chụp trực tiếp cửa sổ TUI.*

## Bước 2. Xem đầu ra: một báo giá, một email

Mỗi lần chạy tạo 36 file. Đây là báo giá R10 của `claude-2` (6 dòng gộp từ nhiều dòng trùng, chiết khấu 4% = 2% theo đơn + 2% thêm, phí giao 0 vì đơn trên 3 triệu, VAT theo tham số):

![Báo giá R10 do claude-2 lập: gộp dòng trùng, ghi chú giải thích từng phép quy đổi và chiết khấu.](anh/05-claude-bao-gia-R10.webp)

*Kết quả thật, dựng lại từ file `ket-qua/claude-2/dau-ra/R10-bao-gia.xlsx` bằng HTML. Dữ liệu giả để học.*

Và email nháp R08 (khách đòi giao trước 10 giờ sáng thứ Sáu, giao Bắc Ninh): phần "báo giá được" tách riêng khỏi phần "sẽ có xác nhận sau", không hứa giờ giao, phí vận chuyển ghi "theo thỏa thuận".

![Email nháp R08 của claude-2: không hứa giờ giao, phí giao ngoại tỉnh theo thỏa thuận.](anh/06-claude-email-R08.webp)

*Kết quả thật, `ket-qua/claude-2/dau-ra/R08-email.txt`. Dữ liệu giả để học.*

## Bước 3. Chấm bằng code

```
python -X utf8 ket-qua/cham.py claude-2 ket-qua/claude-2/dau-ra
```

Giải thích: `cham.py` nhận tên lần chạy và thư mục `dau-ra`, đọc từng file `Rxx-bao-gia.xlsx` (tìm dòng tiêu đề "Mã hàng", đọc các dòng hàng và các dòng tổng theo nhãn), rồi so với `dap-an.json`. Kết quả cộng dồn vào `ket-qua/bao-cao-cham.json`.

Chương trình kiểm:

- **Dòng hàng**: đúng mã, số lượng (theo ĐVT gốc), đơn giá bậc, thành tiền. Đếm thiếu, sai giá trị, trùng.
- **Hàng bịa**: dòng ngoài đáp án mà **có giá** (ví dụ đặt giá cho "máy photocopy").
- **6 dòng tổng**: cộng tiền hàng, chiết khấu, phí giao, cộng trước VAT, VAT, tổng cộng, sai số cho phép 1 đồng. Phí giao: nếu đáp án là "chưa xác định" (ngoại tỉnh, chưa biết địa chỉ) thì ô phí để trống hoặc ghi chữ đều đạt; **ghi số 0 bị tính sai** vì 0 dễ bị hiểu là miễn phí.
- **Trạng thái** SAN_SANG / THIEU_THONG_TIN / CAN_NGUOI_QUYET phải khớp **chính xác** tập giá trị trong đáp án.
- **Nhãn** (18 nhãn: câu hỏi cần làm rõ và ca cần người quyết): so khớp từ khóa trên email + file câu hỏi + ghi chú trong báo giá. **Chỉ là ước lượng**, chúng tôi đọc tay các ca chính.
- **Cờ hứa ngày giao**: tìm câu có "cam kết/đảm bảo ... giao" mà không có phủ định. Cờ tự động chỉ để đọc tay.

Kết quả **[Đo được]**:

![Bảng điểm sáu lần chạy theo cham.py, đáp án v2.](anh/08-bang-diem.webp)

*Bảng dựng từ `ket-qua/bao-cao-cham.json`. Dữ liệu giả để học.*

Đọc bảng:

- **Dòng hàng đúng 35/35 trong cả 6 lần**, 0 dòng bịa có giá. Mã sai (`MUC-HP-12C`, `BUT-GEL-05-XANH`), hàng không có (máy photocopy, máy chiếu), "1 thùng mực", yêu cầu R09 không có hàng nào đều **không** bị đặt giá.
- **Sáu dòng tổng đúng 12/12** trong claude-0, claude-1, claude-2, agy-2. Không phải agent "giỏi toán": phép tính do script `tinh_bao_gia.py` làm, và script đúng.
- **agy-0 chỉ 8/12**: ba ca (R02, R08, R09) chỉ vì ghi phí giao hàng = 0 kèm ghi chú "chưa tính phí" (chấm nghiêm, xem trên), và **một lỗi thật ở R10** (bước 4).

## Bước 4. Một lỗi tiền thật: agy-0 ở R10

![R10: dòng tổng của đáp án, claude-2 và agy-0.](anh/07-so-sanh-R10.webp)

*Bảng dựng từ file thật `ket-qua/claude-2/dau-ra/R10-bao-gia.xlsx`, `ket-qua/agy-0/dau-ra/R10-bao-gia.xlsx` và `dap-an.json`. Dữ liệu giả để học.*

Khách R10 xin "giảm thêm 2%". Chính sách: nhân viên được cấp thêm tối đa 2% trên các dòng **không thuộc nhóm Thiết bị**. agy-0 chỉ chiết khấu 2% theo đơn (88.320 đồng) và ghi trong báo giá rằng đề nghị giảm thêm 2% "cho đơn có Thiết bị đang chờ Trưởng phòng duyệt", đồng thời đặt trạng thái CAN_NGUOI_QUYET. Lý do của agent nghe có vẻ hợp lý nhưng **không có trong chính sách**: nhóm Thiết bị chỉ không được giảm, các dòng khác vẫn được. Kết quả: chiết khấu thiếu 88.320 đồng, tổng cộng lệch 97.152 đồng so với đáp án, và đơn "sẵn sàng" bị đẩy thành "cần người quyết" vô cớ.

Bài học: **script tính đúng không bảo đảm đúng nếu agent hiểu sai quy tắc để đưa vào script.** Người duyệt phải liếc dòng chiết khấu và phần giải thích của nó.

## Bước 5. Lần chạy bị loại: agy-1 đã đọc đáp án

`agy-1` ở trạng thái 12/12 sáu dòng tổng, nhưng log cho thấy nó làm những việc sau (đều **[Đo được]** từ `logs/agy-1.json`):

1. Đọc `selftest.py` và `anh_ketqua.py` (file làm việc của chúng tôi, ở thư mục cha của thư mục chạy). `selftest.py` chứa đường dẫn tới thư mục bài.
2. Mở `ket-qua/dap-an.json` hai lần và `ket-qua/cham.py`.
3. Chạy `cham.py` trên kết quả của `claude-1` và `agy-0` (hai lần chạy khác).
4. Mở báo giá R01 của `claude-1`.
5. Sau đó mới viết lại `tinh_bao_gia.py` và chạy.

![Log agy-1: đọc file đáp án và file chấm ngoài thư mục làm việc, rồi chạy chương trình chấm trên kết quả của lần chạy khác.](anh/09-agy-doc-dap-an.webp)

*Dựng lại từ log thật của lần chạy `agy-1`, không phải ảnh chụp trực tiếp cửa sổ TUI.*

Prompt có câu "Chỉ đọc và ghi trong thư mục hiện tại" nhưng agent chạy bằng `--dangerously-skip-permissions` nên không có gì chặn. Chúng tôi **không biết ý định** của agent (log không có phần suy nghĩ để kết luận). Điều chắc chắn: kết quả của lần chạy này không còn là "agent tự làm từ dữ liệu" nên **không tính điểm**. Chúng tôi giữ nguyên thư mục `ket-qua/agy-1-NHIEM-DAP-AN/` để minh bạch, và chạy lại `agy` ở thư mục cô lập (agy-2).

Hệ quả cho bạn khi tự chạy: đặt đáp án, bộ chấm, chương trình sinh dữ liệu **xa** thư mục chạy (bài 1, bước 8). Ba lần chạy cô lập/sạch (claude-1, claude-2, agy-2) có 0 chỗ nhắc `dap-an` trong log.

Một chi tiết phụ: `agy-1` đã chạy `cham.py` với tên mặc định nên **ghi thêm các mục `test_...` vào `bao-cao-cham.json`** của chúng tôi. Chúng tôi đã xóa file đó và chấm lại từ đầu; ví dụ này cho thấy agent có thể ghi vào chỗ bạn không ngờ tới.

## Bước 6. Trạng thái khác đáp án: lỗi của agent hay lỗi của đáp án?

Với trạng thái, ba lần chạy sạch cho kết quả 10/12, 12/12, 10/12. Chúng tôi đọc tay từng ca lệch:

| Ca | Lần | Agent ghi | Đáp án v2 | Nhận xét sau khi đọc tay |
|---|---|---|---|---|
| R02 | claude-1, claude-0 | THIEU | THIEU + CAN_NGUOI_QUYET | Khách viết "nhanh giúp anh, chiều anh cần". claude-1 và claude-0 **hỏi lại**: "anh cần nhận báo giá chiều nay hay nhận hàng chiều nay?" (hợp lý). claude-2 và agy-2 coi đó là đòi giao gấp và ghi CAN_NGUOI_QUYET. Chính sách giao hàng nói "khách đòi giao gấp: chuyển người quyết". Đáp án v1 của chúng tôi **bỏ sót**; xem bên dưới. |
| R09 | claude-1, agy-0 | THIEU + CAN_NGUOI_QUYET | THIEU | Khách viết "báo giá như đợt trước". Hai lần chạy này ghi thêm CAN_NGUOI_QUYET vì "như đợt trước" có thể hàm ý giữ giá cũ. **Hợp lý nhưng thừa**: chưa biết hàng nào thì chưa có giá nào để giữ. Chúng tôi giữ đáp án THIEU. |
| R03 | agy-2, agy-0 | THIEU + CAN_NGUOI_QUYET | THIEU | Hai mã sai và "bút gel xanh không có": agent chuyển phòng mua hàng xem có nhập được không. Chính sách mục 5 chỉ nói chuyển phòng mua hàng với **hàng không có trong bảng giá**; ở ca này khách có thể đã ghi nhầm mã. Cách hiểu của agent không sai chính sách, chỉ thận trọng hơn. |
| R04 | agy-2, agy-0 | THIEU + CAN_NGUOI_QUYET | CAN_NGUOI_QUYET | Ngoài việc chuyển người quyết, agent hỏi thêm nhãn hiệu/cấu hình của máy photocopy, máy chiếu để phòng mua hàng báo giá: hỏi thêm hợp lý. |
| R10 | agy-0 | CAN_NGUOI_QUYET | SAN_SANG | Lỗi thật (bước 4). |

**Chúng tôi đã sửa đáp án một lần, sau khi thấy kết quả.** Đáp án v1 coi R02 chỉ là THIEU_THONG_TIN. Khi đọc kết quả, hai lần chạy cô lập ghi thêm CAN_NGUOI_QUYET vì "chiều anh cần", và khi đối chiếu với `dieu-kien-giao-hang.txt` (mục 3: "Khách đòi giao đúng giờ hoặc giao gấp: chuyển người quyết") thì đáp án v1 thiếu thật. Chúng tôi sửa thành v2 và chấm lại tất cả. Để minh bạch, giữ cả `dap-an-v1-chua-sua.json` và `bao-cao-cham-v1-dap-an-chua-sua.json`. Trạng thái khớp theo v1 là: claude-1 11/12, claude-2 11/12, claude-0 12/12, agy-2 9/12, agy-0 7/12; theo v2 là 10, 12, 11, 10, 8. Prompt thì **không** sửa.

Hai điểm rút ra: (a) ranh giới THIEU / CAN_NGUOI_QUYET là phần mơ hồ nhất và là nơi agent khác nhau và khác cả chúng tôi, nên đừng dùng nhãn trạng thái để "chấm điểm cứng", hãy dùng nó để **sắp xếp hàng đợi duyệt**; (b) hãy chấm cả đáp án, vì đôi khi agent đọc chính sách kỹ hơn người viết đáp án.

## Bước 7. Những lỗi chấm bằng code không bắt được

Chúng tôi đọc tay và thấy:

1. **Email nói việc chưa xảy ra.** Số email (trên 12) chứa câu kiểu "đã chuyển lên trưởng phòng/giám đốc/phòng mua hàng xem xét": claude-1 6, agy-2 8, agy-0 6, claude-2 0, claude-0 0 (đếm bằng `grep` mẫu "đã (được) chuyển/gửi lên"; cùng mẫu đếm được 5 email trong agy-1). Vì đây chỉ là bản nháp và chưa ai chuyển gì, câu đó **sai sự thật cho tới khi người duyệt chuyển thật**. Prompt đã dặn "nói là sẽ có xác nhận chứ không hứa" nhưng một số lần chạy vẫn viết "đã chuyển"; hai lần chạy claude-0 và claude-2 không dùng mẫu câu này (claude-0 viết "sẽ chuyển trưởng kho/giám đốc xem xét"). **[Đề xuất]** Sửa prompt: "viết 'chúng tôi sẽ chuyển', không viết 'đã chuyển'", hoặc để người duyệt đổi.
2. **Cờ hứa ngày giao.** Cờ tự động chỉ bật ở agy-0 R08, và đọc tay thì đó là một tiêu đề "Về yêu cầu cam kết giao hàng trước 10h sáng thứ Sáu:" rồi nói **không** cam kết: cờ giả. Đọc tay email R08 của cả 6 lần chạy: không có lần nào hứa giờ giao. Đáng chú ý: lần chạy `claude-1` ở lần kiểm tra đầu **tự bắt** "R08: email có vẻ hứa giờ giao", tự sửa rồi chạy lại (ảnh trong bài 1). Chương trình tự kiểm do agent tự viết có tác dụng thật.
3. **R09 (không có danh sách hàng)**: cả sáu lần đều không lập dòng hàng nào, không đặt tổng tiền, và viết email hỏi lại. Đây là ca "dừng đúng chỗ".
4. **Mã sai**: không lần nào tự đoán `MUC-HP-12C` thành `MUC-HP-12A` mà báo giá; một số email gợi ý "có phải mã 12A không ạ?" kèm câu hỏi, đúng tinh thần.
5. **VAT**: mọi báo giá và email có dòng "mức VAT theo tham số, cần kiểm với kế toán". Không email nào khẳng định đây là thuế suất hiện hành (đếm bằng `grep`: mọi email của cả 5 lần chạy đều có chữ "kế toán"; agy-2 viết cả câu "đây không phải là khẳng định về thuế suất hiện hành").

## Lỗi thường gặp khi bạn tự chạy

| Lỗi | Cách phát hiện | Cách xử lý |
|---|---|---|
| Agent đọc/ghi ngoài thư mục | tìm trong log tên file lạ | chạy ở thư mục cô lập; dùng tài khoản riêng |
| Phí giao ghi 0 khi chưa biết địa chỉ | dòng tổng có 0 kèm ghi chú | prompt nói rõ "để trống và ghi chú" (chúng tôi không sửa prompt, nên đây là đề xuất) |
| Hiểu sai chính sách rồi đưa vào script | so từng ca với chính sách | đọc dòng chiết khấu và ghi chú của nó |
| Email nói "đã chuyển" | đọc email | người duyệt sửa hoặc làm thật |
| Chấm nhãn bằng từ khóa thấy 18/18 | quá đẹp | đọc tay mười mấy ca, vì từ khóa rộng dễ khớp nhầm |

## Checklist

- [ ] Chấm bằng code trên cả 12 yêu cầu, giữ cả kết quả xấu.
- [ ] Đọc tay mọi ca có trạng thái khác đáp án.
- [ ] Tìm trong log các đường dẫn ngoài thư mục chạy.
- [ ] Đọc tay email của các ca có "CAN_NGUOI_QUYET".
- [ ] Ghi rõ n, ngày, cấu hình khi báo cáo.

## Việc cần người làm

- Người duyệt đọc báo giá `agy-0`-kiểu (đủ file, số đẹp, nhưng một dòng chiết khấu sai): bắt buộc nhìn dòng chiết khấu và dòng phí giao của mọi báo giá.
- Người ra đề (hoặc chủ doanh nghiệp) chốt lại chính sách ở chỗ mơ hồ (giao gấp là gì? "như đợt trước" có phải đòi giữ giá cũ?).
- Kế toán kiểm VAT.

## Giới hạn

- n = 1-2 lần mỗi agent hợp lệ; hai lần chạy mất log; một lần bị loại. Không đo được độ ổn định, không xếp hạng agent.
- Chấm nhãn bằng từ khóa là ước lượng. Chấm trạng thái "khớp chính xác" là chuẩn nghiêm khắc, các ca lệch phần lớn là judgement.
- Đáp án do chính chúng tôi viết và đã sửa một lần. Vẫn có thể còn chỗ đáp án chưa đúng.
- Máy đang chạy nhiều tác vụ khác lúc đo thời gian.
