# Cấp K2: Bộ quy tắc thành mã, báo cáo lỗi có vị trí

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung.
> Liên quan: kiểm tổng hóa đơn bằng code đã có ở `../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` bài 2.6; file này mở rộng thành **sổ quy tắc** có mã, căn cứ, mức độ, và báo cáo lỗi chuẩn.

!!! tip "Tóm tắt nhanh"
    Bài này giải quyết một việc: kiểm hồ sơ (ví dụ hóa đơn) sao cho **lần nào chạy cũng ra cùng một kết quả**, giải thích được vì sao, và không phụ thuộc vào việc AI "kiểm giúp". Cách làm là biến từng dòng trong bảng kiểm thành một quy tắc có mã, rồi cho máy (code hoặc công thức Excel) chạy qua mọi quy tắc. Sau bài, bạn có một sổ quy tắc và một báo cáo lỗi cho biết lỗi nằm ở hồ sơ nào, quy tắc nào, dòng nào.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** kế toán dùng Excel nâng cao, hoặc người biết lập trình nhẹ, cùng với người phụ trách nghiệp vụ (người hiểu hồ sơ đó phải đúng những gì). Nếu bạn không biết lập trình, đừng lo: các đoạn mã trong bài bạn không cần tự viết. Bạn chỉ cần hiểu chúng làm gì, rồi nhờ người biết code hoặc nhờ AI viết và chạy giúp. Bài K2.3 còn có đường làm hoàn toàn bằng Excel.

**Bạn cần chuẩn bị:**
- Bảng kiểm (checklist) và bộ hồ sơ mẫu có đáp án đã làm ở cấp K0.
- Dữ liệu hồ sơ đã được chuyển thành dạng JSON ở cấp K1. (JSON là cách viết dữ liệu có khung rõ ràng để máy đọc được, ví dụ mỗi hóa đơn có các ô "tổng trước thuế", "tiền thuế", "tổng thanh toán".)
- Excel (cho đường không code), hoặc Python (cho đường có code).

**Sau bài này bạn sẽ có:**
1. **Sổ quy tắc** (`so_quy_tac`): mỗi quy tắc xác định là một hàm nhỏ (một đoạn code làm đúng một việc kiểm), có mã, mô tả, căn cứ, mức độ.
2. **Bộ chạy** đi qua *mọi* quy tắc cho mỗi hồ sơ, không bỏ quy tắc nào.
3. **Báo cáo lỗi** chuẩn: mỗi dòng gồm hồ sơ, mã quy tắc, kết quả, chi tiết, vị trí, căn cứ.
4. Bộ mẫu K0 chạy lại tự động sau mỗi lần sửa quy tắc.

**Thứ bạn cầm đi được sau bài:** sổ quy tắc (một file `so_quy_tac.py` hoặc một tab "Quy tắc" trong Excel), báo cáo lỗi dạng file CSV hoặc Excel, và một script kiểm thử chạy lại bộ mẫu.

## 2. Câu hỏi cấp này trả lời / lỗi của K1

*"Dữ liệu đã đúng. Giờ kiểm thế nào để kết quả lặp lại, giải thích được, và không phụ thuộc AI?"*

Ở cấp K1, chúng ta đã đưa dữ liệu hồ sơ về dạng đúng và đủ. Vấn đề còn lại là bước kiểm.

Lỗi còn lại sau K1: nếu vẫn đưa JSON cho LLM "kiểm giúp", ta mang lại đúng những vấn đề đã đo ở K0: kết quả đổi giữa các lần chạy, bỏ dòng, tự tính sai. (LLM là mô hình ngôn ngữ lớn, tức loại AI đứng sau Claude, ChatGPT.)

!!! tip "Nói đơn giản"
    Nhờ AI "xem hóa đơn này đúng chưa" giống như hỏi một người có thể trả lời khác nhau mỗi lần. Còn phép cộng, phép so ngày, phép tra danh sách thì máy làm được đúng và giống nhau mọi lần. Cấp này giao phần việc đó cho máy chạy theo quy tắc.

## 3. Kiến thức nền

### 3.1 Vì sao dùng code cho quy tắc xác định

("Xác định" nghĩa là câu trả lời chỉ có một đáp án đúng, ví dụ tổng có bằng nhau hay không.)

- Hệ thống FinDAS của BMO giao các kiểm tra "luật định và cấu trúc" (trần khấu trừ, giới hạn số chữ số, phát hiện bất thường theo mẫu) cho hàm theo quy tắc, cho kết quả hợp lệ/không hợp lệ xác định. Kiểm số học (tính lại tổng từ thành phần) cũng là công cụ riêng, bỏ qua khi thiếu số. Tác giả nêu lý do: giảm khả năng LLM bịa kết luận tuân thủ, và kết luận dựa trên tiêu chí rõ ràng, kiểm toán được **[Nguồn: B1, phụ lục C]**.
- Kết quả LLM không lặp lại byte-for-byte (giống nhau từng ký tự) ngay cả khi đặt chế độ xác định (chế độ để cùng một câu hỏi cho cùng một câu trả lời). Có triển khai đổi nhãn kết luận ở 18 trong 70 yêu cầu trong cùng một ngày **[Nguồn: B6]**. **[Đề xuất]** Hồ sơ đã kết luận phải giải thích lại được sau 6 tháng; code làm được, LLM thì không.
- **Dùng AI để viết code quy tắc, không dùng AI để làm quy tắc.** **[Đề xuất]** Nhờ Claude/ChatGPT viết hàm Python cho từng dòng checklist là hợp lý; nhưng hàm phải chạy qua bộ mẫu có đáp án trước khi dùng.

!!! tip "Nói đơn giản"
    AI giỏi ở việc **viết** ra quy tắc, nhưng không nên là bên **áp dụng** quy tắc từng hồ sơ. Hãy nhờ AI viết hàm, rồi thử hàm trên bộ mẫu đã biết đáp án. Hàm nào ra đúng đáp án thì mới dùng thật.

### 3.2 Các loại quy tắc [Đề xuất]

Trước khi viết code, hãy phân loại từng dòng trong checklist. Loại nào làm bằng gì thì xem bảng dưới.

| Loại | Ví dụ | Làm bằng |
|---|---|---|
| Xác định trên một chứng từ | Tổng dòng = tổng trước thuế; MST đúng dạng; ngày không ở tương lai | Hàm code (K2) |
| Tra cứu | Nhà cung cấp đã duyệt; hóa đơn chưa ghi sổ; người ký có thẩm quyền | Hàm code đọc sổ, danh sách (K2, K4) |
| Đối chiếu nhiều chứng từ | Đơn giá hóa đơn = đơn giá đơn mua | Hàm code (K4) |
| Mờ | Mô tả hàng phù hợp ngành hàng; điều khoản phạt có rõ ràng | LLM có kiểm (K3) |

(MST là mã số thuế. "Chứng từ" là giấy tờ kế toán như hóa đơn, đơn mua. "Quy tắc mờ" là quy tắc cần hiểu nghĩa của câu chữ nên không có đáp án máy tính ra được.)

### 3.3 Hợp đồng của một hàm quy tắc [Đề xuất]

"Hợp đồng" ở đây là thỏa thuận giữa các quy tắc: mỗi quy tắc nhận gì vào, trả gì ra, và gặp tình huống xấu thì phải làm gì. Cả bộ quy tắc theo cùng một hợp đồng thì báo cáo mới đọc thống nhất được.

- Vào: dữ liệu hồ sơ (JSON từ K1) + ngữ cảnh (sổ, danh sách).
- Ra: đúng một trong `DAT`, `LOI`, `KHONG_RO`, `KHONG_AP_DUNG`, kèm `chi_tiet` (số cụ thể, vị trí). Bốn giá trị này lần lượt nghĩa là: đạt, lỗi, không rõ, không áp dụng.
- Thiếu dữ liệu → `KHONG_RO`, không phải `DAT`.
- Hàm ném lỗi (tức là bản thân đoạn code bị trục trặc khi chạy) → bộ chạy ghi `KHONG_RO` kèm lỗi, không dừng cả hồ sơ, không bỏ dòng.
- Tiền dùng `Decimal` (kiểu số trong Python tính tiền chính xác, không bị sai số lẻ như số thực thông thường). Dung sai làm tròn (nếu có) ghi rõ trong sổ quy tắc và có người duyệt con số đó.

!!! tip "Nói đơn giản"
    Có hai nguyên tắc dễ nhớ. Một: **thiếu số thì nói "không rõ", đừng nói "đạt"**. Hai: **mỗi quy tắc đều phải để lại một dòng kết quả**, kể cả khi nó hỏng. Như vậy không bao giờ có chuyện hồ sơ "sạch" chỉ vì một quy tắc bị bỏ qua âm thầm.

## 4. Chuỗi bài nhỏ

Năm bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và (ở những bài có) lỗi hay gặp để tránh.

### Bài K2.1: Chuyển checklist K0 thành sổ quy tắc
- **Việc cần làm:** mỗi dòng "xác định" và "tra cứu" thành một mục có các trường sau: `ma` (mã quy tắc), `mo_ta` (mô tả), `can_cu` (căn cứ: dựa vào đâu mà có quy tắc này), `muc_do` (mức độ nghiêm trọng), `hieu_luc_tu` (hiệu lực từ ngày nào), `ham` (hàm làm việc kiểm). Quy tắc mờ để lại cho K3 nhưng vẫn có mã trong sổ (kết quả tạm `KHONG_RO`, người xem).
- **Bạn có sau bài:** `so_quy_tac.py` hoặc tab "Quy tắc" trong Excel.
- **Lỗi hay gặp:** một hàm kiểm hai ý; không ghi căn cứ; không ghi ngày hiệu lực (sẽ thành vấn đề ở K7).

### Bài K2.2: Bộ chạy và báo cáo
- **Việc cần làm:** dùng bộ chạy mẫu dưới đây, chạy qua mọi quy tắc cho một hóa đơn và xuất báo cáo lỗi.
- **Mã mẫu (đã chạy thử** 2026-11-11, `python -I -X utf8`, trên hóa đơn giả lập của K1):

  **Đoạn mã dưới đây làm gì?** Nó làm ba việc. Thứ nhất, nó dựng một "danh sách quy tắc" và cho phép khai báo thêm từng quy tắc với mã, mô tả, căn cứ, mức độ. Thứ hai, nó có ba quy tắc mẫu: `HD-03` kiểm số lượng nhân đơn giá có bằng thành tiền từng dòng không, và tổng các dòng có bằng tổng trước thuế không; `HD-04` kiểm tổng trước thuế cộng tiền thuế có bằng tổng thanh toán không; `HD-06` kiểm hóa đơn này đã ghi sổ rồi hay chưa (chống trả tiền hai lần). Thứ ba, hàm `kiem` chạy **mọi** quy tắc cho một hóa đơn và ghi một dòng kết quả cho mỗi quy tắc, kể cả khi quy tắc đó bị hỏng. (Tên biến trong mã viết không dấu; `thanh_tien` là thành tiền, `don_gia` là đơn giá, `da_ghi_so` là danh sách hóa đơn đã ghi sổ.) Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi cần.

  ```python
  from decimal import Decimal as D
  import re
  DAT, LOI, KHONG_RO = "DAT", "LOI", "KHONG_RO"
  QUY_TAC = []                                   # (ma, mo_ta, can_cu, muc_do, ham)
  def quy_tac(ma, mo_ta, can_cu, muc_do):
      def wrap(f): QUY_TAC.append((ma, mo_ta, can_cu, muc_do, f)); return f
      return wrap

  @quy_tac("HD-03", "Tong dong hang = tong truoc thue", "Checklist v1, muc 3", "cao")
  def tong_dong(hd, ctx):
      if any(d["thanh_tien"] is None for d in hd["dong"]) or hd["tong_truoc_thue"] is None:
          return KHONG_RO, "thieu so lieu"
      bad = [d["_vi_tri"] for d in hd["dong"] if d["sl"] is not None and d["don_gia"] is not None
             and d["sl"] * d["don_gia"] != d["thanh_tien"]]
      if bad: return LOI, "SL x don gia != thanh tien tai " + ",".join(bad)
      s = sum(d["thanh_tien"] for d in hd["dong"])
      return (DAT, "") if s == hd["tong_truoc_thue"] else (LOI, f"tong dong {s} != {hd['tong_truoc_thue']}")

  @quy_tac("HD-04", "Truoc thue + thue = tong thanh toan", "Checklist v1, muc 4", "cao")
  def tong_tt(hd, ctx):
      a, b, c = hd["tong_truoc_thue"], hd["tien_thue"], hd["tong_tt"]
      if None in (a, b, c): return KHONG_RO, "thieu so lieu"
      return (DAT, "") if a + b == c else (LOI, f"{a}+{b} != {c}")

  @quy_tac("HD-06", "Khong trung hoa don da ghi so", "Quy che thanh toan", "cao")
  def trung(hd, ctx):
      k = (hd.get("mst_ban"), hd.get("ky_hieu"), hd.get("so_hd"))
      return (LOI, f"trung {k}") if k in ctx["da_ghi_so"] else (DAT, "")

  def kiem(hd, ctx):
      bao_cao = []
      for ma, mo_ta, can_cu, muc_do, f in QUY_TAC:      # MOI quy tac PHAI co mot ket qua
          try: kq, ct = f(hd, ctx)
          except Exception as e: kq, ct = KHONG_RO, f"loi ham: {e}"
          bao_cao.append({"ma": ma, "ket_qua": kq, "chi_tiet": ct, "can_cu": can_cu,
                          "muc_do": muc_do, "nguon": hd["_nguon"]})
      return bao_cao
  ```

  **Kết quả chạy thử:** File đầy đủ trong scratchpad (thư mục nháp của người soạn) có 6 quy tắc (thêm đủ trường, dạng MST, nhà cung cấp đã duyệt). Kết quả thử: hóa đơn giả lập đúng cho 6/6 `DAT`. Sửa cố ý tiền thuế thêm 1 đồng và số lượng dòng 2 từ 200 thành 201: `HD-03 LOI SL x don gia != thanh tien tai HHDVu[2]`, `HD-04 LOI 6900000+552001 != 7452000`; các quy tắc khác vẫn `DAT`.

  !!! tip "Nói đơn giản"
      Khi cố ý sửa sai hai chỗ nhỏ (thêm 1 đồng tiền thuế, đổi số lượng ở dòng 2), máy bắt đúng hai quy tắc liên quan và chỉ rõ dòng nào sai (`HHDVu[2]` là dòng hàng hóa dịch vụ thứ 2). Bốn quy tắc còn lại vẫn báo đạt. Đó chính là kiểu báo cáo ta muốn có.

- **Bạn có sau bài:** `bao_cao_<so_ho_so>.csv`, mở được bằng Excel. (CSV là file bảng dạng chữ thuần, Excel mở được.) Vị trí (`HHDVu[2]`) giúp người duyệt mở đúng dòng trên phần mềm xem hóa đơn.

### Bài K2.3: Cùng quy tắc, đường không code bằng Excel
- **Việc cần làm:**
  1. Nhập JSON/XML vào Excel (Power Query hoặc dán bảng). (Power Query là công cụ có sẵn trong Excel để nạp dữ liệu từ file. XML là một dạng file dữ liệu có cấu trúc, giống JSON về mục đích.)
  2. Mỗi quy tắc một cột công thức, ví dụ `=IF(TongTruocThue+TienThue=TongTT,"DAT","LOI")`.
  3. Tra trùng bằng `COUNTIFS` trên sheet "Đã ghi sổ". (`COUNTIFS` là hàm đếm số dòng thỏa nhiều điều kiện cùng lúc.)
  4. Thiếu ô → `"KHONG_RO"` (dùng `IF(ISBLANK(...))`, hàm kiểm ô có trống hay không).
- **Bạn có sau bài:** `kiem_hoa_don.xlsx` có tab Quy tắc (mã, căn cứ) và tab Kết quả.
- **Lỗi hay gặp:** công thức so số thực có phần thập phân (nên làm tròn về đồng trước khi so); để ô trống được hiểu là 0.

### Bài K2.4: Chạy bộ mẫu làm kiểm thử hồi quy
("Kiểm thử hồi quy" là chạy lại toàn bộ bộ mẫu sau mỗi lần sửa, để chắc rằng sửa chỗ này không làm hỏng chỗ khác.)

- **Việc cần làm:** mỗi hồ sơ trong bộ mẫu K0.2 đã có đáp án theo mã. Viết một script (đoạn chương trình ngắn) so `bao_cao` với đáp án, in mọi ô lệch. Chạy mỗi khi sửa một quy tắc.
- **Bạn có sau bài:** `kiem_thu.py`; quy ước "không sửa quy tắc nếu chưa chạy kiểm thử".
- **Lỗi hay gặp:** sửa đáp án cho khớp với code thay vì sửa code.

### Bài K2.5: Hàng đợi duyệt tối thiểu
- **Việc cần làm:** mọi hồ sơ có ít nhất một `LOI` hoặc `KHONG_RO` ở mức "cao" vào hàng đợi (danh sách hồ sơ chờ người duyệt); hồ sơ toàn `DAT` vẫn cần người ký, nhưng xem nhanh. Thiết kế hàng đợi, SLA (thời hạn cam kết xử lý), chống "duyệt cho xong": theo `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4 và bài 8.4.
- **Thêm riêng cho bài toán này [Đề xuất]:** người duyệt phải thấy chứng từ gốc cạnh báo cáo; mỗi lần người duyệt **không đồng ý** với một kết quả, ghi mã quy tắc và lý do. Đó là nguồn ca mới cho bộ mẫu (K6, K7).

## 5. Đường không code vs có code; khi nào buộc chuyển

Bài này có hai đường: Excel (làm ở K2.3) và Python (làm ở K2.2). Bảng dưới so sánh để bạn chọn.

| | Excel (K2.3) | Python (K2.2) |
|---|---|---|
| Hợp với | 1 loại hồ sơ, dưới khoảng 200 hồ sơ/tháng, một người dùng | Nhiều loại hồ sơ, nhiều nguồn |
| Ưu | Kế toán tự sửa được | Kiểm thử hồi quy tự động, log, nối với K3-K4 |
| Nhược | Công thức dễ bị sửa nhầm, khó biết ai sửa | Cần người bảo trì |

(Log là bản ghi lại từng việc máy đã làm, để sau này xem lại. Người bảo trì là người biết code, chịu trách nhiệm sửa khi có lỗi.)

**Buộc chuyển sang Python khi [Đề xuất]:** có quy tắc tra cứu nhiều sổ (trùng hóa đơn qua nhiều năm), có quy tắc mờ cần gọi LLM, hoặc hơn 2 người cùng sửa file Excel.

## 6. Tiêu chí lên K3 (đo được) [Đề xuất]

Bạn có thể sang cấp K3 khi đạt đủ các điều sau:

1. 100% quy tắc xác định và tra cứu trong checklist đã chạy bằng code hoặc công thức.
2. Trên bộ mẫu: 0 bỏ sót ở quy tắc xác định (nếu có bỏ sót, đó là lỗi code hoặc lỗi dữ liệu K1; sửa trước khi lên cấp).
3. Mỗi dòng báo cáo có vị trí và căn cứ.
4. Kiểm thử hồi quy chạy được trong một lệnh.
5. Có danh sách quy tắc mờ còn lại, mỗi quy tắc có 3 ví dụ đạt và 3 ví dụ lỗi lấy từ hồ sơ thật.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống để bạn dễ hình dung. SME là doanh nghiệp nhỏ và vừa.

**a) Cửa hàng vật liệu điện nước, 2 chi nhánh.** Sổ quy tắc hóa đơn đầu vào 9 quy tắc, 7 bằng code, 2 tra cứu (nhà cung cấp, trùng). Trước khi chạy code, kế toán từng thanh toán hai lần một hóa đơn do nhà cung cấp gửi lại qua hai email. `HD-06` bắt trường hợp này bằng khóa (MST bên bán, ký hiệu, số). (Khóa ở đây là bộ ba thông tin ghép lại để nhận ra một hóa đơn là duy nhất.)

**b) Văn phòng kế toán dịch vụ, làm sổ cho 25 hộ kinh doanh.** Mỗi khách một thư mục XML. Cùng một sổ quy tắc chạy cho cả 25 khách, chỉ đổi `ctx` (MST của khách, danh sách nhà cung cấp quen của khách). Báo cáo gửi khách là file Excel, mỗi dòng một lỗi có vị trí. Lưu ý: dữ liệu của khách là dữ liệu bên thứ ba; thỏa thuận với khách trước khi dùng dịch vụ AI ngoài cho bất kỳ bước nào (K3).

**c) Công ty may gia công.** Quy tắc nội bộ về đề nghị tạm ứng: `TU-01` số tiền không vượt hạn mức theo chức danh (tra bảng hạn mức), `TU-02` có chữ ký trưởng bộ phận (người xác nhận, vì chữ ký trên ảnh không tin máy đọc: xem `../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` mục 3.4), `TU-03` không có tạm ứng cũ quá 30 ngày chưa quyết toán (tra sổ).

## 8. Tài liệu tham khảo

| Mã | Nguồn | Tin cậy |
|---|---|---|
| B1 | ESCROW / FinDAS, BMO, arXiv 2608.01772, phụ lục C (bốn nhóm công cụ). https://www.alphaxiv.org/abs/2608.01772 | Trung bình-cao |
| B6 | Suzuki, arXiv 2610.21300. https://www.alphaxiv.org/abs/2610.21300 | Trung bình (xung đột lợi ích đã công bố) |
| B5 | Voboril, Erste Bank, arXiv 2610.20155 (quy tắc JSON tách khỏi bước kiểm). https://www.alphaxiv.org/abs/2610.20155 | Trung bình |
| R2 | Nhóm RAG, bài 2.6 kiểm tổng hóa đơn | `../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` |
| R8 | Nhóm RAG, điểm duyệt, hàng đợi | `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` |

## 9. Chưa kiểm chứng

- Các quy tắc ví dụ (MST 10 hoặc 13 chữ số dạng `xxxxxxxxxx-xxx`, khóa trùng hóa đơn gồm MST + ký hiệu + số) là phán đoán của nhóm soạn; chưa đối chiếu văn bản gốc về cấu trúc MST và ký hiệu hóa đơn sau NĐ 254/2026.
- Quy tắc "tổng trước thuế + thuế = tổng thanh toán" chưa xét hóa đơn nhiều thuế suất, chiết khấu, phí khác; cần bổ sung theo mẫu hóa đơn thật.
- Đường Excel (K2.3) chưa dựng thử.
- Chưa có số đo thời gian tiết kiệm trên SME thật.
