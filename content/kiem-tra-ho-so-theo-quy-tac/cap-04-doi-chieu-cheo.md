# Cấp K4: Đối chiếu chéo nhiều chứng từ (đơn mua, phiếu nhập, hóa đơn)

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung.
> Đã có, không viết lại: công cụ đọc sổ, phân hạng quyền (`../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md`); quy trình đề nghị thanh toán dạng workflow (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 7.c). File này viết phần **nối các chứng từ với nhau**.

## 1. Mục tiêu và người đọc

**Người đọc:** kế toán công nợ, mua hàng, thủ kho; người code nhẹ.

**Sau cấp này có:**
1. Đối chiếu ba bên theo từng dòng hàng: đơn mua (PO) - phiếu nhập kho - hóa đơn.
2. **Bảng ánh xạ tên hàng** của nhà cung cấp sang mã hàng nội bộ, có người xác nhận.
3. Đối chiếu danh sách hóa đơn mua vào trên cổng thuế với sổ của mình.
4. Quy tắc về nhà cung cấp: MST khớp danh mục, thay đổi tài khoản ngân hàng thì người xác nhận.

## 2. Câu hỏi cấp này trả lời / lỗi của K2-K3

*"Một hóa đơn đúng về hình thức vẫn có thể sai: tính giá cao hơn giá đặt, tính hàng chưa giao, hoặc đã thanh toán rồi. Làm sao bắt?"*

Lỗi còn lại: K2 kiểm từng chứng từ một. Nhiều lỗi tốn tiền nhất chỉ thấy khi đặt hai, ba chứng từ cạnh nhau.

## 3. Kiến thức nền

### 3.1 Đối chiếu ba bên là gì [Đề xuất, mô tả thực hành phổ biến]
- **Đơn mua:** đã đặt gì, giá nào, bao nhiêu.
- **Phiếu nhập kho (hoặc biên bản giao nhận):** đã thực nhận bao nhiêu.
- **Hóa đơn:** nhà cung cấp đòi tiền bao nhiêu.
- Kiểm theo **từng dòng hàng**: đơn giá hóa đơn so với đơn mua; số lượng hóa đơn so với số đã nhận (cộng dồn nhiều đợt giao) và so với số đã đặt; đơn vị tính giống nhau.
- Đối chiếu hai bên (đơn mua - hóa đơn) dùng cho dịch vụ không có phiếu nhập.

### 3.2 Bằng chứng
- Ở FinDAS, quy tắc nối nhiều trường qua nhiều trang, có điều kiện, có tính toán; tác giả nêu đây là chỗ agent dễ bỏ sót ca biên và bịa giá trị không có căn cứ **[Nguồn: B1, mục 4.1]**.
- Ở Erste, phần lớn kết quả "thiếu thông tin" đến từ các quy tắc dẫn sang tài liệu khác mà hệ thống không truy cập được **[Nguồn: B5]**. **[Đề xuất]** Quy tắc tra cứu chỉ chạy được khi có dữ liệu. Cần chuẩn bị sổ trước khi viết quy tắc.
- ExtractBench có riêng nhãn thử thách "tham chiếu chéo, đối chiếu" trong nhóm tìm thông tin rải rác **[Nguồn: B2, phụ lục A]**; bài không báo điểm riêng cho nhãn này trong phần đã đọc.
- **Không có số đo tin được về tỷ lệ ngoại lệ hay tỷ lệ "không chạm tay" của đối chiếu ba bên.** Các con số trên blog nhà cung cấp phần mềm mâu thuẫn nhau (xem mục 9). Không dùng các con số đó trong bài giảng.

### 3.3 Khó nhất không phải phép so, mà là khóa nối [Đề xuất]
- Hóa đơn ghi tên hàng theo cách của người bán ("Thùng carton 5 lớp 60x40x40"). Đơn mua ghi mã nội bộ (`CT5`). Không có khóa chung thì không so được.
- Cách làm: **bảng ánh xạ** (MST người bán, tên hàng trên hóa đơn) → mã hàng nội bộ. LLM được phép **đề xuất** ánh xạ cho dòng mới; người xác nhận một lần; từ đó code dùng bảng. Đây là chỗ LLM có ích mà không quyết định gì.
- Số đơn mua trên hóa đơn: nhiều hóa đơn không ghi, hoặc ghi ở phần ghi chú. Nếu thiếu, đối chiếu theo (nhà cung cấp, khoảng ngày, mã hàng), và kết quả là `KHONG_RO` nếu có nhiều đơn mua ứng viên.
- **Dung sai** (cho phép lệch giá, lệch số lượng bao nhiêu) là quyết định của chủ doanh nghiệp, không phải của người viết code. Mặc định 0.

### 3.4 Đối chiếu với cổng thuế
- Hướng dẫn thứ cấp cho biết cổng hóa đơn điện tử cho tra cứu hóa đơn mua vào và xuất danh sách ra Excel hoặc XML **[Nguồn: V5, thứ cấp]**.
- **[Đề xuất]** Hai quy tắc có ích: (a) hóa đơn có trên cổng nhưng chưa có trong sổ (quên ghi nhận, hoặc hóa đơn lạ ghi tên công ty mình); (b) hóa đơn có trong sổ nhưng không thấy trên cổng (cần người tra lại). Không viết công cụ tự đăng nhập cổng thuế ở cấp này: rủi ro tài khoản, điều khoản sử dụng chưa đọc.

## 4. Chuỗi bài nhỏ

### Bài K4.1: Chuẩn bị sổ
- **Làm:** xuất từ phần mềm (hoặc lập Excel): danh mục nhà cung cấp (MST, tên, tài khoản ngân hàng, ngày cập nhật); đơn mua đang mở theo dòng; phiếu nhập theo dòng; hóa đơn đã ghi sổ (MST, ký hiệu, số, số tiền, ngày thanh toán).
- **Sản phẩm:** thư mục `so/` với 4 file CSV, có ngày xuất.
- **Lỗi:** dùng sổ cũ; sổ không có số đơn mua trên phiếu nhập.

### Bài K4.2: Bảng ánh xạ tên hàng
- **Làm:** lấy tên hàng từ 3 tháng hóa đơn (đọc từ XML ở K1). Với mỗi cặp (MST người bán, tên hàng) chưa có trong bảng, cho LLM đề xuất mã hàng nội bộ từ danh mục hàng (dán danh mục). Người mua hàng xác nhận hoặc sửa. Lưu `anh_xa_hang.csv` có cột `nguoi_xac_nhan`, `ngay`.
- **Sản phẩm:** bảng ánh xạ. Dòng nào chưa xác nhận thì quy tắc ba bên ra `KHONG_RO` cho dòng đó.
- **Lỗi:** để LLM ánh xạ trực tiếp lúc kiểm, không lưu (mỗi lần một kết quả khác, xem B6 ở `cap-03`).

### Bài K4.3: Hàm đối chiếu ba bên
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
  Kết quả thử: đơn mua 1.000 thùng giá 4.500 và 200 cuộn băng keo giá 11.500; nhập kho hai đợt (600 + 400 thùng; 180 cuộn); hóa đơn 1.000 thùng giá 4.500 và 200 cuộn giá 12.000. Hàm trả đúng hai lỗi: `BB-04 BK5: 12000 vs 11500` và `BB-05 BK5: 200 vs 180`. Dòng thùng carton giao hai đợt được cộng dồn, không báo nhầm.
- **Chưa xử lý trong mẫu:** quy đổi đơn vị (thùng ↔ cái), hóa đơn gộp nhiều đơn mua, hàng trả lại, chiết khấu. Gặp các ca này thì trả `KHONG_RO`, đừng đoán.

### Bài K4.4: Trùng hóa đơn và đã thanh toán
- **Làm:** mở rộng `HD-06` (K2): khóa chính (MST, ký hiệu, số); khóa phụ (MST, số tiền, ngày ±3 ngày) để bắt hóa đơn thay thế hoặc gửi lại dưới số khác. Khóa phụ khớp → `KHONG_RO` (người xem), không phải `LOI`.
- **Lưu ý quy định:** cách xử lý hóa đơn sai sót, thay thế, điều chỉnh đã đổi theo NĐ 70/2025 và nay theo NĐ 254/2026 **[Nguồn: V1, V2, thứ cấp]**. Quy tắc trùng phải tính đến hóa đơn thay thế/điều chỉnh; đọc văn bản gốc trước khi viết.

### Bài K4.5: Quy tắc nhà cung cấp
- **Làm:** `NCC-01` MST trên hóa đơn có trong danh mục; `NCC-02` tên người bán trên hóa đơn khớp danh mục (so sau khi chuẩn hóa chữ hoa, dấu, "Công ty TNHH" ↔ "CTY TNHH"; khác → `KHONG_RO`); `NCC-03` **tài khoản nhận tiền trên đề nghị thanh toán khác tài khoản trong danh mục → luôn `LOI`, người gọi điện xác nhận với nhà cung cấp qua số điện thoại đã lưu, không qua số trên email**.
- **Vì sao NCC-03 chặt [Đề xuất]:** đổi tài khoản nhận tiền là kiểu gian lận qua email phổ biến; đây là quyết định của người, không phải của máy.

### Bài K4.6: Đối chiếu với danh sách trên cổng thuế
- **Làm:** mỗi tuần, người có quyền tải danh sách hóa đơn mua vào (Excel). Script so với sổ theo khóa (MST, ký hiệu, số). Xuất hai danh sách: "có trên cổng, chưa có trong sổ"; "có trong sổ, không thấy trên cổng".
- **Sản phẩm:** `doi_chieu_cong_thue.py` + báo cáo tuần.
- **Lỗi:** để script lưu mật khẩu cổng thuế.

## 5. Đường không code vs có code; khi nào buộc chuyển

| | Không code | Có code |
|---|---|---|
| Ba bên | Excel: ba sheet, `XLOOKUP` theo (số PO, mã hàng), `SUMIFS` số đã nhập | `doi_chieu()` |
| Ánh xạ tên hàng | Sheet ánh xạ, người điền | LLM đề xuất, người duyệt, code dùng |
| Cổng thuế | Lọc Excel thủ công | Script so khóa |

**Buộc chuyển sang code khi [Đề xuất]:** có giao hàng nhiều đợt thường xuyên; hơn khoảng 100 dòng hóa đơn mỗi tháng; hoặc hơn 1 kho.

## 6. Tiêu chí lên K5 (đo được) [Đề xuất]

1. Có 4 sổ ở K4.1, có ngày cập nhật, người chịu trách nhiệm.
2. Ít nhất 90% dòng hàng trên hóa đơn của 3 tháng gần nhất có ánh xạ đã xác nhận (phần còn lại ra `KHONG_RO`).
3. Trên bộ mẫu cài lỗi ba bên (giá lệch, giao thiếu, đơn vị khác, giao nhiều đợt đúng): 0 bỏ sót, 0 báo nhầm ở ca giao nhiều đợt đúng.
4. `NCC-03` đã chạy thử với một ca tài khoản bị đổi.
5. Đã chạy K4.6 ít nhất 4 tuần liên tiếp.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

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
