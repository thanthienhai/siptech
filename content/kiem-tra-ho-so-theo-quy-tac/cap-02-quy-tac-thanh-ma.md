# Cấp K2: Bộ quy tắc thành mã, báo cáo lỗi có vị trí

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung.
> Liên quan: kiểm tổng hóa đơn bằng code đã có ở `../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` bài 2.6; file này mở rộng thành **sổ quy tắc** có mã, căn cứ, mức độ, và báo cáo lỗi chuẩn.

## 1. Mục tiêu và người đọc

**Người đọc:** người code nhẹ (hoặc kế toán dùng Excel nâng cao) cùng người phụ trách nghiệp vụ.

**Sau cấp này có:**
1. **Sổ quy tắc** (`so_quy_tac`): mỗi quy tắc xác định là một hàm nhỏ, có mã, mô tả, căn cứ, mức độ.
2. **Bộ chạy** đi qua *mọi* quy tắc cho mỗi hồ sơ, không bỏ quy tắc nào.
3. **Báo cáo lỗi** chuẩn: mỗi dòng = hồ sơ, mã quy tắc, kết quả, chi tiết, vị trí, căn cứ.
4. Bộ mẫu K0 chạy lại tự động sau mỗi lần sửa quy tắc.

## 2. Câu hỏi cấp này trả lời / lỗi của K1

*"Dữ liệu đã đúng. Giờ kiểm thế nào để kết quả lặp lại, giải thích được, và không phụ thuộc AI?"*

Lỗi còn lại sau K1: nếu vẫn đưa JSON cho LLM "kiểm giúp", ta mang lại đúng những vấn đề đã đo ở K0: kết quả đổi giữa các lần chạy, bỏ dòng, tự tính sai.

## 3. Kiến thức nền

### 3.1 Vì sao code cho quy tắc xác định
- Hệ thống FinDAS của BMO giao các kiểm tra "luật định và cấu trúc" (trần khấu trừ, giới hạn số chữ số, phát hiện bất thường theo mẫu) cho hàm theo quy tắc, cho kết quả hợp lệ/không hợp lệ xác định; kiểm số học (tính lại tổng từ thành phần) cũng là công cụ riêng, bỏ qua khi thiếu số. Tác giả nêu lý do: giảm khả năng LLM bịa kết luận tuân thủ, và kết luận dựa trên tiêu chí rõ ràng, kiểm toán được **[Nguồn: B1, phụ lục C]**.
- Kết quả LLM không lặp lại byte-for-byte ngay cả khi đặt chế độ xác định; có triển khai đổi nhãn kết luận ở 18 trong 70 yêu cầu trong cùng một ngày **[Nguồn: B6]**. **[Đề xuất]** Hồ sơ đã kết luận phải giải thích lại được sau 6 tháng; code làm được, LLM thì không.
- **Dùng AI để viết code quy tắc, không dùng AI để làm quy tắc.** **[Đề xuất]** Nhờ Claude/ChatGPT viết hàm Python cho từng dòng checklist là hợp lý; nhưng hàm phải chạy qua bộ mẫu có đáp án trước khi dùng.

### 3.2 Ba loại quy tắc [Đề xuất]

| Loại | Ví dụ | Làm bằng |
|---|---|---|
| Xác định trên một chứng từ | Tổng dòng = tổng trước thuế; MST đúng dạng; ngày không ở tương lai | Hàm code (K2) |
| Tra cứu | Nhà cung cấp đã duyệt; hóa đơn chưa ghi sổ; người ký có thẩm quyền | Hàm code đọc sổ, danh sách (K2, K4) |
| Đối chiếu nhiều chứng từ | Đơn giá hóa đơn = đơn giá đơn mua | Hàm code (K4) |
| Mờ | Mô tả hàng phù hợp ngành hàng; điều khoản phạt có rõ ràng | LLM có kiểm (K3) |

### 3.3 Hợp đồng của một hàm quy tắc [Đề xuất]
- Vào: dữ liệu hồ sơ (JSON từ K1) + ngữ cảnh (sổ, danh sách).
- Ra: đúng một trong `DAT`, `LOI`, `KHONG_RO`, `KHONG_AP_DUNG`, kèm `chi_tiet` (số cụ thể, vị trí).
- Thiếu dữ liệu → `KHONG_RO`, không phải `DAT`.
- Hàm ném lỗi → bộ chạy ghi `KHONG_RO` kèm lỗi, không dừng cả hồ sơ, không bỏ dòng.
- Tiền dùng `Decimal`. Dung sai làm tròn (nếu có) ghi rõ trong sổ quy tắc và có người duyệt con số đó.

## 4. Chuỗi bài nhỏ

### Bài K2.1: Chuyển checklist K0 thành sổ quy tắc
- **Làm:** mỗi dòng "xác định" và "tra cứu" thành một mục: `ma`, `mo_ta`, `can_cu`, `muc_do`, `hieu_luc_tu`, `ham`. Quy tắc mờ để lại cho K3 nhưng vẫn có mã trong sổ (kết quả tạm `KHONG_RO`, người xem).
- **Sản phẩm:** `so_quy_tac.py` hoặc tab "Quy tắc" trong Excel.
- **Lỗi:** một hàm kiểm hai ý; không ghi căn cứ; không ghi ngày hiệu lực (sẽ thành vấn đề ở K7).

### Bài K2.2: Bộ chạy và báo cáo
- **Mã mẫu (đã chạy thử** 2026-11-11, `python -I -X utf8`, trên hóa đơn giả lập của K1):
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
  File đầy đủ trong scratchpad có 6 quy tắc (thêm đủ trường, dạng MST, nhà cung cấp đã duyệt). Kết quả thử: hóa đơn giả lập đúng cho 6/6 `DAT`. Sửa cố ý tiền thuế thêm 1 đồng và số lượng dòng 2 từ 200 thành 201: `HD-03 LOI SL x don gia != thanh tien tai HHDVu[2]`, `HD-04 LOI 6900000+552001 != 7452000`; các quy tắc khác vẫn `DAT`.
- **Sản phẩm:** `bao_cao_<so_ho_so>.csv`, mở được bằng Excel. Vị trí (`HHDVu[2]`) giúp người duyệt mở đúng dòng trên phần mềm xem hóa đơn.

### Bài K2.3: Cùng quy tắc, đường không code bằng Excel
- **Làm:** nhập JSON/XML vào Excel (Power Query hoặc dán bảng). Mỗi quy tắc một cột công thức, ví dụ `=IF(TongTruocThue+TienThue=TongTT,"DAT","LOI")`. Tra trùng bằng `COUNTIFS` trên sheet "Đã ghi sổ". Thiếu ô → `"KHONG_RO"` (dùng `IF(ISBLANK(...))`).
- **Sản phẩm:** `kiem_hoa_don.xlsx` có tab Quy tắc (mã, căn cứ) và tab Kết quả.
- **Lỗi:** công thức so số thực có phần thập phân (nên làm tròn về đồng trước khi so); để ô trống được hiểu là 0.

### Bài K2.4: Chạy bộ mẫu làm kiểm thử hồi quy
- **Làm:** mỗi hồ sơ trong bộ mẫu K0.2 đã có đáp án theo mã. Viết một script so `bao_cao` với đáp án, in mọi ô lệch. Chạy mỗi khi sửa một quy tắc.
- **Sản phẩm:** `kiem_thu.py`; quy ước "không sửa quy tắc nếu chưa chạy kiểm thử".
- **Lỗi:** sửa đáp án cho khớp với code thay vì sửa code.

### Bài K2.5: Hàng đợi duyệt tối thiểu
- **Làm:** mọi hồ sơ có ít nhất một `LOI` hoặc `KHONG_RO` ở mức "cao" vào hàng đợi; hồ sơ toàn `DAT` vẫn cần người ký, nhưng xem nhanh. Thiết kế hàng đợi, SLA, chống "duyệt cho xong": theo `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4 và bài 8.4.
- **Thêm riêng cho bài toán này [Đề xuất]:** người duyệt phải thấy chứng từ gốc cạnh báo cáo; mỗi lần người duyệt **không đồng ý** với một kết quả, ghi mã quy tắc và lý do. Đó là nguồn ca mới cho bộ mẫu (K6, K7).

## 5. Đường không code vs có code; khi nào buộc chuyển

| | Excel (K2.3) | Python (K2.2) |
|---|---|---|
| Hợp với | 1 loại hồ sơ, dưới khoảng 200 hồ sơ/tháng, một người dùng | Nhiều loại hồ sơ, nhiều nguồn |
| Ưu | Kế toán tự sửa được | Kiểm thử hồi quy tự động, log, nối với K3-K4 |
| Nhược | Công thức dễ bị sửa nhầm, khó biết ai sửa | Cần người bảo trì |

**Buộc chuyển sang Python khi [Đề xuất]:** có quy tắc tra cứu nhiều sổ (trùng hóa đơn qua nhiều năm), có quy tắc mờ cần gọi LLM, hoặc hơn 2 người cùng sửa file Excel.

## 6. Tiêu chí lên K3 (đo được) [Đề xuất]

1. 100% quy tắc xác định và tra cứu trong checklist đã chạy bằng code hoặc công thức.
2. Trên bộ mẫu: 0 bỏ sót ở quy tắc xác định (nếu có bỏ sót, đó là lỗi code hoặc lỗi dữ liệu K1; sửa trước khi lên cấp).
3. Mỗi dòng báo cáo có vị trí và căn cứ.
4. Kiểm thử hồi quy chạy được trong một lệnh.
5. Có danh sách quy tắc mờ còn lại, mỗi quy tắc có 3 ví dụ đạt và 3 ví dụ lỗi lấy từ hồ sơ thật.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

**a) Cửa hàng vật liệu điện nước, 2 chi nhánh.** Sổ quy tắc hóa đơn đầu vào 9 quy tắc, 7 bằng code, 2 tra cứu (nhà cung cấp, trùng). Trước khi chạy code, kế toán từng thanh toán hai lần một hóa đơn do nhà cung cấp gửi lại qua hai email. `HD-06` bắt trường hợp này bằng khóa (MST bên bán, ký hiệu, số).

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
