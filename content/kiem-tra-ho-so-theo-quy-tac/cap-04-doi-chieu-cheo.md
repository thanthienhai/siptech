# Cấp K4: Đối chiếu chéo nhiều chứng từ (đơn mua, phiếu nhập, hóa đơn)

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung.
> Đã có, không viết lại: công cụ đọc sổ, phân hạng quyền (`../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md`); quy trình đề nghị thanh toán dạng workflow (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 7.c). File này viết phần **nối các chứng từ với nhau**.

!!! tip "Tóm tắt nhanh"
    Một hóa đơn nhìn đúng về hình thức vẫn có thể sai: tính giá cao hơn giá đã đặt, tính tiền hàng chưa giao, hoặc đã được thanh toán rồi. Những lỗi này chỉ lộ ra khi bạn đặt đơn mua, phiếu nhập kho và hóa đơn cạnh nhau. Bài này dạy cách so ba chứng từ theo từng dòng hàng, cách nối tên hàng của nhà cung cấp với mã hàng của mình, và cách đối chiếu với danh sách hóa đơn trên cổng thuế. Sau bài, bạn có bộ sổ, bảng ánh xạ và quy tắc đối chiếu để dùng hằng tuần.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** kế toán công nợ, người mua hàng, thủ kho. Người biết code nhẹ sẽ làm được phần có mã; những người còn lại có thể làm bằng Excel (xem mục 5).

**Bạn cần chuẩn bị:**
- Dữ liệu xuất từ phần mềm (hoặc lập tay bằng Excel): danh mục nhà cung cấp, đơn mua đang mở, phiếu nhập kho, hóa đơn đã ghi sổ (chi tiết ở Bài K4.1).
- Danh mục hàng nội bộ của bạn (để dán cho AI đề xuất mã hàng ở Bài K4.2).
- Hóa đơn của 3 tháng gần nhất, đã đọc ra dạng XML ở cấp K1 (XML là loại file chứa dữ liệu hóa đơn điện tử, máy đọc được).
- Danh sách hóa đơn mua vào tải từ cổng hóa đơn điện tử (dạng Excel), cho Bài K4.6.

**Sau bài này bạn sẽ có:**
1. Cách đối chiếu ba bên theo từng dòng hàng: đơn mua (PO, viết tắt của "purchase order", tức đơn đặt hàng gửi nhà cung cấp) - phiếu nhập kho - hóa đơn.
2. **Bảng ánh xạ tên hàng** (bảng "dịch" tên hàng trên hóa đơn của nhà cung cấp sang mã hàng nội bộ), có người xác nhận.
3. Cách đối chiếu danh sách hóa đơn mua vào trên cổng thuế với sổ của mình.
4. Quy tắc về nhà cung cấp: MST (mã số thuế) khớp danh mục, thay đổi tài khoản ngân hàng thì người xác nhận.

**Thứ bạn cầm đi được sau bài:** thư mục `so/` gồm 4 file CSV (bảng dữ liệu đơn giản, mở được bằng Excel); file `anh_xa_hang.csv`; hàm đối chiếu ba bên; ba quy tắc nhà cung cấp `NCC-01`, `NCC-02`, `NCC-03`; và báo cáo tuần đối chiếu với cổng thuế.

## 2. Câu hỏi cấp này trả lời / lỗi của K2-K3

*"Một hóa đơn đúng về hình thức vẫn có thể sai: tính giá cao hơn giá đặt, tính hàng chưa giao, hoặc đã thanh toán rồi. Làm sao bắt?"*

Lỗi còn lại sau các cấp trước: K2 kiểm từng chứng từ một. Nhưng nhiều lỗi tốn tiền nhất chỉ thấy khi đặt hai, ba chứng từ cạnh nhau. Ví dụ, nhìn riêng tờ hóa đơn thì mọi thứ đều hợp lệ; chỉ khi so với đơn mua bạn mới thấy giá đã bị đẩy lên.

## 3. Kiến thức nền

### 3.1 Đối chiếu ba bên là gì [Đề xuất, mô tả thực hành phổ biến]

Ba chứng từ, mỗi cái trả lời một câu hỏi khác nhau:

- **Đơn mua:** đã đặt gì, giá nào, bao nhiêu.
- **Phiếu nhập kho (hoặc biên bản giao nhận):** đã thực nhận bao nhiêu.
- **Hóa đơn:** nhà cung cấp đòi tiền bao nhiêu.

Cách kiểm là so theo **từng dòng hàng**:
- đơn giá trên hóa đơn so với đơn giá trên đơn mua;
- số lượng trên hóa đơn so với số đã nhận (cộng dồn nếu giao nhiều đợt) và so với số đã đặt;
- đơn vị tính phải giống nhau.

Với dịch vụ không có phiếu nhập kho, ta chỉ đối chiếu hai bên (đơn mua - hóa đơn).

!!! tip "Nói đơn giản"
    Giống như bạn đi chợ rồi nhận hóa đơn. Bạn nhìn lại danh sách đã đặt, nhìn số hàng thật sự nhận được, rồi mới trả tiền. Ba thứ phải khớp nhau từng món, không chỉ khớp tổng tiền.

### 3.2 Bằng chứng

- Ở FinDAS (một nghiên cứu về agent, tức chương trình AI tự thực hiện nhiều bước), quy tắc nối nhiều trường qua nhiều trang, có điều kiện, có tính toán. Tác giả nêu đây là chỗ agent dễ bỏ sót ca biên (trường hợp đặc biệt ít gặp) và bịa giá trị không có căn cứ **[Nguồn: B1, mục 4.1]**.
- Ở Erste, phần lớn kết quả "thiếu thông tin" đến từ các quy tắc dẫn sang tài liệu khác mà hệ thống không truy cập được **[Nguồn: B5]**. **[Đề xuất]** Quy tắc tra cứu chỉ chạy được khi có dữ liệu. Cần chuẩn bị sổ trước khi viết quy tắc.
- ExtractBench (một bộ bài kiểm tra khả năng trích thông tin) có riêng nhãn thử thách "tham chiếu chéo, đối chiếu" trong nhóm tìm thông tin rải rác **[Nguồn: B2, phụ lục A]**; bài không báo điểm riêng cho nhãn này trong phần đã đọc.
- **Không có số đo tin được về tỷ lệ ngoại lệ hay tỷ lệ "không chạm tay" của đối chiếu ba bên.** Các con số trên blog nhà cung cấp phần mềm mâu thuẫn nhau (xem mục 9). Không dùng các con số đó trong bài giảng.

!!! tip "Nói đơn giản"
    Đối chiếu nhiều chứng từ là việc khó với AI nếu bạn chỉ đưa chứng từ rồi hỏi "có sai không". Cái AI cần là dữ liệu đã được chuẩn bị sẵn (sổ), nếu không nó sẽ trả về "thiếu thông tin" hoặc đoán bừa.

### 3.3 Khó nhất không phải phép so, mà là khóa nối [Đề xuất]

"Khóa nối" là thông tin chung giữa hai chứng từ để biết dòng này ứng với dòng kia.

- Hóa đơn ghi tên hàng theo cách của người bán ("Thùng carton 5 lớp 60x40x40"). Đơn mua ghi mã nội bộ (`CT5`). Không có khóa chung thì không so được.
- Cách làm: **bảng ánh xạ** (MST người bán, tên hàng trên hóa đơn) → mã hàng nội bộ. LLM (mô hình AI ngôn ngữ lớn, như ChatGPT hay Claude) được phép **đề xuất** ánh xạ cho dòng mới; người xác nhận một lần; từ đó code dùng bảng. Đây là chỗ LLM có ích mà không quyết định gì.
- Số đơn mua trên hóa đơn: nhiều hóa đơn không ghi, hoặc ghi ở phần ghi chú. Nếu thiếu, đối chiếu theo (nhà cung cấp, khoảng ngày, mã hàng), và kết quả là `KHONG_RO` (nghĩa là "chưa rõ, cần người xem") nếu có nhiều đơn mua ứng viên.
- **Dung sai** (cho phép lệch giá, lệch số lượng bao nhiêu) là quyết định của chủ doanh nghiệp, không phải của người viết code. Mặc định 0.

!!! tip "Nói đơn giản"
    Bảng ánh xạ giống một cuốn từ điển: bên trái là cách nhà cung cấp gọi món hàng, bên phải là cách công ty bạn gọi. AI được phép gợi ý dòng mới cho từ điển, nhưng một người phải gật đầu thì dòng đó mới được dùng. Còn dung sai là câu hỏi "lệch bao nhiêu thì còn chấp nhận", và chỉ chủ doanh nghiệp được trả lời.

### 3.4 Đối chiếu với cổng thuế

- Hướng dẫn thứ cấp (tài liệu của bên thứ ba, không phải văn bản gốc của cơ quan thuế) cho biết cổng hóa đơn điện tử cho tra cứu hóa đơn mua vào và xuất danh sách ra Excel hoặc XML **[Nguồn: V5, thứ cấp]**.
- **[Đề xuất]** Hai quy tắc có ích: (a) hóa đơn có trên cổng nhưng chưa có trong sổ (quên ghi nhận, hoặc hóa đơn lạ ghi tên công ty mình); (b) hóa đơn có trong sổ nhưng không thấy trên cổng (cần người tra lại). Không viết công cụ tự đăng nhập cổng thuế ở cấp này: rủi ro tài khoản, điều khoản sử dụng chưa đọc.

## 4. Chuỗi bài nhỏ

Sáu bài thực hành dưới đây làm theo thứ tự. Mỗi bài có việc cần làm và thứ bạn có sau bài; một số bài có thêm lỗi hay gặp để tránh.

### Bài K4.1: Chuẩn bị sổ
- **Việc cần làm:** xuất từ phần mềm (hoặc lập Excel) bốn thứ: danh mục nhà cung cấp (MST, tên, tài khoản ngân hàng, ngày cập nhật); đơn mua đang mở theo dòng; phiếu nhập theo dòng; hóa đơn đã ghi sổ (MST, ký hiệu, số, số tiền, ngày thanh toán).
- **Bạn có sau bài:** thư mục `so/` với 4 file CSV, có ngày xuất.
- **Lỗi hay gặp:** dùng sổ cũ; sổ không có số đơn mua trên phiếu nhập.

### Bài K4.2: Bảng ánh xạ tên hàng
- **Việc cần làm:** lấy tên hàng từ 3 tháng hóa đơn (đọc từ XML ở K1). Với mỗi cặp (MST người bán, tên hàng) chưa có trong bảng, cho LLM đề xuất mã hàng nội bộ từ danh mục hàng (dán danh mục vào cho nó xem). Người mua hàng xác nhận hoặc sửa. Lưu thành file `anh_xa_hang.csv` có cột `nguoi_xac_nhan` và `ngay`.
- **Bạn có sau bài:** bảng ánh xạ. Dòng nào chưa xác nhận thì quy tắc ba bên ra `KHONG_RO` cho dòng đó.
- **Lỗi hay gặp:** để LLM ánh xạ trực tiếp lúc kiểm, không lưu (mỗi lần một kết quả khác, xem B6 ở `cap-03`).

### Bài K4.3: Hàm đối chiếu ba bên
- **Việc cần làm:** nhờ người biết lập trình (hoặc nhờ AI) chạy hàm mẫu dưới đây với sổ của bạn. Nếu bạn làm bằng Excel thì xem mục 5.

**Đoạn mã dưới đây làm gì?** Nó nhận một đơn mua, danh sách các phiếu nhập kho (giao nhiều đợt thì cộng dồn) và một hóa đơn, rồi so từng dòng hàng. Nó kiểm số đơn mua và MST người bán có khớp không, mã hàng có trên đơn mua không, đơn vị tính có giống nhau không, đơn giá có lệch không, số lượng trên hóa đơn có vượt số đã nhập kho hoặc số đã đặt không. Mỗi lỗi có một mã `BB-00` đến `BB-06`. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết hàm này làm gì, và nhờ người biết code hoặc nhờ AI chạy giúp.

- **Mã mẫu (đã chạy thử** 2026-11-11, `python -I -X utf8`, dữ liệu giả lập):

  ```python
  from decimal import Decimal as D
  DUNG_SAI_GIA = D("0"); DUNG_SAI_SL = D("0")    # chu doanh nghiep quyet

  def doi_chieu(po, grn_list, hd):
      loi = []
      if hd["so_po"] != po["so_po"]:
          loi.append(("BB-00", "hoa don ghi PO khac", f"hd:{hd['so_po']} po:{po['so_po']}"))
      if hd["mst_ban"] != po["mst_ncc"]:
          loi.append(("BB-01", "MST ban khac NCC tren PO", f"{hd['mst_ban']} vs {po['mst_ncc']}"))
      da_nhap = {}
      for g in grn_list:                          # giao nhieu dot: cong don
          for ma, sl in g["dong"].items(): da_nhap[ma] = da_nhap.get(ma, D(0)) + sl
      for ma, d in hd["dong"].items():            # ma = ma noi bo, sau khi qua bang anh xa
          p = po["dong"].get(ma)
          if p is None:
              loi.append(("BB-02", "ma hang co tren HD, khong co tren PO", ma)); continue
          if d["dvt"] != p["dvt"]:
              loi.append(("BB-03", "don vi tinh khac", f"{ma}: {d['dvt']} vs {p['dvt']}")); continue
          if abs(d["don_gia"] - p["don_gia"]) > DUNG_SAI_GIA:
              loi.append(("BB-04", "don gia HD khac PO", f"{ma}: {d['don_gia']} vs {p['don_gia']}"))
          if d["sl"] - da_nhap.get(ma, D(0)) > DUNG_SAI_SL:
              loi.append(("BB-05", "SL tren HD vuot SL da nhap kho", f"{ma}: {d['sl']} vs {da_nhap.get(ma, 0)}"))
          if d["sl"] > p["sl"]:
              loi.append(("BB-06", "SL tren HD vuot SL dat", f"{ma}: {d['sl']} vs {p['sl']}"))
      return loi
  ```

**Kết quả thử:** đơn mua 1.000 thùng giá 4.500 và 200 cuộn băng keo giá 11.500; nhập kho hai đợt (600 + 400 thùng; 180 cuộn); hóa đơn 1.000 thùng giá 4.500 và 200 cuộn giá 12.000. Hàm trả đúng hai lỗi: `BB-04 BK5: 12000 vs 11500` và `BB-05 BK5: 200 vs 180`. Dòng thùng carton giao hai đợt được cộng dồn, không báo nhầm.

!!! tip "Nói đơn giản"
    Ở ví dụ trên, nhà cung cấp tính 12.000 một cuộn trong khi bạn đặt giá 11.500, và tính tiền 200 cuộn trong khi kho mới nhận 180. Hàm chỉ ra đúng hai chỗ đó. Còn 1.000 thùng giao thành hai đợt (600 + 400) thì hàm cộng lại nên không báo nhầm.

- **Chưa xử lý trong mẫu:** quy đổi đơn vị (thùng ↔ cái), hóa đơn gộp nhiều đơn mua, hàng trả lại, chiết khấu. Gặp các ca này thì trả `KHONG_RO`, đừng đoán.

### Bài K4.4: Trùng hóa đơn và đã thanh toán
- **Việc cần làm:** mở rộng quy tắc `HD-06` (làm ở K2). Khóa chính (MST, ký hiệu, số) dùng để bắt hóa đơn trùng. Thêm khóa phụ (MST, số tiền, ngày ±3 ngày) để bắt hóa đơn thay thế hoặc hóa đơn gửi lại dưới số khác. Khóa phụ khớp thì trả `KHONG_RO` (để người xem), không phải `LOI`.
- **Lưu ý quy định:** cách xử lý hóa đơn sai sót, thay thế, điều chỉnh đã đổi theo NĐ 70/2025 và nay theo NĐ 254/2026 **[Nguồn: V1, V2, thứ cấp]** (NĐ là viết tắt của Nghị định). Quy tắc trùng phải tính đến hóa đơn thay thế/điều chỉnh; đọc văn bản gốc trước khi viết. Đây là tài liệu kỹ thuật, không phải tư vấn pháp lý.

### Bài K4.5: Quy tắc nhà cung cấp
- **Việc cần làm:** viết ba quy tắc:
  1. `NCC-01`: MST trên hóa đơn có trong danh mục.
  2. `NCC-02`: tên người bán trên hóa đơn khớp danh mục (so sau khi chuẩn hóa chữ hoa, dấu, "Công ty TNHH" ↔ "CTY TNHH"; khác thì `KHONG_RO`).
  3. `NCC-03`: **tài khoản nhận tiền trên đề nghị thanh toán khác tài khoản trong danh mục thì luôn `LOI`; người gọi điện xác nhận với nhà cung cấp qua số điện thoại đã lưu, không qua số trên email**.
- **Vì sao NCC-03 chặt [Đề xuất]:** đổi tài khoản nhận tiền là kiểu gian lận qua email phổ biến; đây là quyết định của người, không phải của máy.

### Bài K4.6: Đối chiếu với danh sách trên cổng thuế
- **Việc cần làm:** mỗi tuần, người có quyền tải danh sách hóa đơn mua vào (Excel). Script (đoạn chương trình ngắn) so với sổ theo khóa (MST, ký hiệu, số). Xuất hai danh sách: "có trên cổng, chưa có trong sổ"; "có trong sổ, không thấy trên cổng".
- **Bạn có sau bài:** `doi_chieu_cong_thue.py` + báo cáo tuần.
- **Lỗi hay gặp:** để script lưu mật khẩu cổng thuế.

## 5. Đường không code vs có code; khi nào buộc chuyển

Cách không code đủ dùng khi mới bắt đầu. Cách có code giúp máy làm thay những việc lặp lại.

| | Không code | Có code |
|---|---|---|
| Ba bên | Excel: ba sheet, `XLOOKUP` theo (số PO, mã hàng), `SUMIFS` số đã nhập | `doi_chieu()` |
| Ánh xạ tên hàng | Sheet ánh xạ, người điền | LLM đề xuất, người duyệt, code dùng |
| Cổng thuế | Lọc Excel thủ công | Script so khóa |

(`XLOOKUP` là hàm Excel tìm một giá trị trong bảng khác; `SUMIFS` là hàm cộng các số thỏa điều kiện, ở đây dùng để cộng số đã nhập qua nhiều đợt giao.)

**Buộc chuyển sang code khi [Đề xuất]:** có giao hàng nhiều đợt thường xuyên; hơn khoảng 100 dòng hóa đơn mỗi tháng; hoặc hơn 1 kho.

## 6. Tiêu chí lên K5 (đo được) [Đề xuất]

Bạn có thể sang cấp K5 khi đạt đủ các điều sau:

1. Có 4 sổ ở K4.1, có ngày cập nhật, người chịu trách nhiệm.
2. Ít nhất 90% dòng hàng trên hóa đơn của 3 tháng gần nhất có ánh xạ đã xác nhận (phần còn lại ra `KHONG_RO`).
3. Trên bộ mẫu cài lỗi ba bên (giá lệch, giao thiếu, đơn vị khác, giao nhiều đợt đúng): 0 bỏ sót, 0 báo nhầm ở ca giao nhiều đợt đúng.
4. `NCC-03` đã chạy thử với một ca tài khoản bị đổi.
5. Đã chạy K4.6 ít nhất 4 tuần liên tiếp.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

(SME là doanh nghiệp nhỏ và vừa.) Ba tình huống giả định để bạn dễ hình dung:

**a) Xưởng in bao bì, mua giấy cuộn từ 4 nhà cung cấp.** Giấy giao theo tấn, đơn mua đặt theo tấn, nhưng phiếu cân thực tế lệch vài chục kg mỗi cuộn. Chủ xưởng quyết dung sai số lượng (ví dụ ±0,5%) và ghi vào sổ quy tắc kèm tên người quyết; đơn giá dung sai 0. Bảng ánh xạ cần thiết vì mỗi nhà cung cấp gọi cùng loại giấy một tên khác.

**b) Chuỗi 6 quán cà phê, mua sữa, cà phê hạt, ly nhựa.** Không có phần mềm kho; phiếu nhập là ảnh chụp phiếu giao ký nhận ở quán. K1 đọc ảnh, K4 đối chiếu hai bên (đơn đặt qua Zalo được chép vào Google Sheets → hóa đơn) và ba bên khi có ảnh phiếu giao. Ảnh không đọc được → `KHONG_RO`, quản lý quán xác nhận số nhận.

**c) Công ty thương mại thiết bị y tế nhập hàng trong nước.** Ngoài ba bên, có quy tắc `NCC-04` "lô hàng thiết bị có giấy tờ kèm theo yêu cầu trong hợp đồng" (danh sách giấy tờ lấy từ hợp đồng mua; có/không có, người xác nhận). Đây là quy tắc tra cứu trên hồ sơ, không cần LLM nếu danh sách giấy tờ đã được viết ra.

## 8. Tài liệu tham khảo

| Mã | Nguồn | Tin cậy |
|---|---|---|
| B1 | ESCROW / FinDAS, arXiv 2608.01772, mục 4.1 | Trung bình-cao |
| B5 | Voboril, Erste Bank, arXiv 2610.20155 | Trung bình |
| B2 | ExtractBench, arXiv 2607.29677, phụ lục A | Trung bình (tác giả là nhà cung cấp) |
| V1 | EY về NĐ 254/2026 | Trung bình-cao; qua tóm tắt |
| V2 | Các trang tóm tắt NĐ 70/2025 (meinvoice.vn, ihoadon.vn, PwC). https://www.pwc.com/vn/vn/publications/2025/250416-changes-to-invoicing-regulations.pdf | Chỉ đọc kết quả tìm kiếm |
| V5 | Hướng dẫn tra cứu hóa đơn đầu vào (MISA, xcyber). https://sme.misa.vn/351069/cach-lay-hoa-don-dau-vao-tren-trang-thue-dien-tu/ ; https://xcyber.vn/?p=13832 | Thấp; giao diện có thể đổi |
| R8 | Nhóm RAG, tình huống 7.c | `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` |

## 9. Chưa kiểm chứng

- **Số liệu ngành về đối chiếu ba bên** (chỉ qua một lượt tìm kiếm, không đọc báo cáo gốc): một blog gán cho Ardent Partners tỷ lệ ngoại lệ 9% (nhóm tốt nhất) và 22% (trung bình); một blog gán cho APQC tỷ lệ xử lý thẳng 52-58% với đối chiếu theo quy tắc; một trang khác gán cho Ardent/IOFM 85-92%. Các con số mâu thuẫn, đều từ trang bán phần mềm. **Không dùng.**
- Quy định về hóa đơn thay thế, điều chỉnh theo NĐ 254/2026 và TT 91/2026: chưa đọc gốc.
- Các bước trên cổng hóa đơn điện tử: thứ cấp.
- Phần mềm kế toán nào ở Việt Nam đã có sẵn đối chiếu ba bên hoặc tải hóa đơn đầu vào tự động: chưa đọc tài liệu chính thức nên không nêu.
- Dung sai ví dụ ±0,5% là minh họa, không phải khuyến nghị.
