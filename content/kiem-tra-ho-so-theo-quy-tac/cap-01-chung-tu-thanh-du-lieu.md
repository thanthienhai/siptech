# Cấp K1: Chứng từ thành dữ liệu có nguồn

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung.
> Đã có ở nhóm RAG, không viết lại: ba loại PDF, OCR vs mô hình thị giác, CER, kiểm tổng hóa đơn bằng code, chi phí, bảo mật khi gửi tài liệu (`../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md`); gọi API trả JSON (`../rag-tra-cuu-tai-lieu/cap-01-goi-api.md`). File này viết phần khác: **chọn nguồn dữ liệu gốc trước khi nghĩ tới AI**, và **mỗi trường phải biết nó đến từ đâu**.

## 1. Mục tiêu và người đọc

**Người đọc:** kế toán hoặc nhân viên biết dùng Excel; người code nhẹ cho phần XML.

**Sau cấp này có:**
1. Bảng kiểm kê: mỗi loại chứng từ lấy dữ liệu từ đâu (XML, file xuất từ phần mềm, PDF có chữ, ảnh).
2. Script đọc hóa đơn điện tử XML thành JSON, **không OCR, không LLM**.
3. Lược đồ JSON cho chứng từ không có dữ liệu gốc (phiếu giao, đơn mua giấy), mỗi trường kèm **giá trị chép nguyên văn** và **vị trí**.
4. Một hàm kiểm "giá trị có thật trong chứng từ không" và hàm chuẩn hóa số kiểu Việt Nam.

## 2. Câu hỏi cấp này trả lời / lỗi của K0

*"Làm sao có dữ liệu đúng để kiểm, thay vì để AI vừa đọc vừa kiểm trong một lần?"*

Lỗi ở K0: AI đọc sai một con số thì cả bảng kiểm sai theo, mà người duyệt không thấy. Trong chat, việc đọc và việc kết luận dính vào nhau.

## 3. Kiến thức nền

### 3.1 Thứ tự ưu tiên nguồn dữ liệu [Đề xuất]
1. **Dữ liệu gốc có cấu trúc:** file XML hóa đơn điện tử; danh sách hóa đơn xuất từ cổng hóa đơn điện tử của cơ quan thuế; file xuất từ phần mềm kế toán, kho, bán hàng. Đọc bằng code. Gần như không sai.
2. **PDF có lớp chữ:** trích chữ trực tiếp, rồi mới trích trường.
3. **Ảnh, scan:** mô hình thị giác hoặc OCR. Đắt nhất, sai nhiều nhất. Dùng khi không còn cách nào.

Câu hỏi đầu tiên khi gặp một chứng từ: *"Có bản dữ liệu gốc không? Xin được không?"* Nhiều khi xin nhà cung cấp gửi kèm XML rẻ hơn mọi mô hình.

### 3.2 Hóa đơn điện tử Việt Nam: điều đã biết và chưa biết
- Hóa đơn điện tử dùng định dạng XML, gồm phần dữ liệu nghiệp vụ hóa đơn và phần dữ liệu chữ ký số; hóa đơn có mã của cơ quan thuế có thêm phần dữ liệu về mã **[Nguồn: tóm tắt trang meinvoice.vn về file XML; trang này nói theo NĐ 123/2020]**.
- Thành phần dữ liệu và tên thẻ XML từng được quy định ở Quyết định 1450/QĐ-TCT ngày 07/10/2021 (thay Quyết định 635/QĐ-TCT năm 2020) **[Nguồn: kết quả tìm kiếm, thuvienphapluat, luatvietnam; chưa đọc toàn văn]**. Một nguồn cho biết tên thẻ viết tắt, không dấu **[Nguồn: thứ cấp]**.
- **Thay đổi 2026:** theo EY, NĐ 254/2026/NĐ-CP (hiệu lực 01/7/2026) thay NĐ 123/2020 và không còn quy định chi tiết định dạng, giao Bộ trưởng Bộ Tài chính hướng dẫn **[Nguồn: V1, đọc qua công cụ tóm tắt]**.
- **Chưa xác minh:** tên từng thẻ (ví dụ thẻ số hóa đơn, MST người bán, tổng tiền). Vì vậy code mẫu để tên thẻ trong **một bảng ánh xạ**. Người học mở 3-5 file XML thật của mình, sửa bảng đó, rồi mới chạy.
- Xem, tra cứu: các hướng dẫn thứ cấp nêu cách mở XML bằng phần mềm xem của cơ quan thuế (iTaxViewer) để xem nội dung và trạng thái chữ ký; cổng hóa đơn điện tử cho tra cứu hóa đơn mua vào và xuất danh sách ra Excel hoặc XML **[Nguồn: meinvoice.vn, xcyber.vn, hướng dẫn MISA; thứ cấp, giao diện có thể đổi]**.
- **[Đề xuất]** Kiểm chữ ký số XML bằng code tự viết là việc khó và dễ sai. Ở cấp này không tự viết. Dùng phần mềm xem chính thức hoặc tra cứu trên cổng; ghi kết quả vào một trường `da_tra_cuu_cong_thue` (người điền).

### 3.3 Khi phải dùng mô hình đọc chứng từ: bằng chứng
- **Ảnh hay OCR + ảnh?** Nghiên cứu của SAP trên khoảng 1.000 tài liệu doanh nghiệp thật (phiếu giao hàng, tài liệu tài chính, nhiều ngôn ngữ, trong đó khoảng 5 tài liệu bằng đồng Việt Nam): với mô hình mạnh, chỉ đưa ảnh cho kết quả tương đương đưa OCR + ảnh; F1 trung bình theo mô hình dao động khoảng 50-77% tùy mô hình và kiểu đầu vào (riêng đầu vào chỉ OCR: 66-74%). Sửa mô tả lược đồ, ví dụ, chỉ dẫn tăng thêm khoảng 2 điểm (76,8 → 78,9) **[Nguồn: B3]**. Lỗi điển hình: ghi "002" thay vì "2"; đọc nhầm chữ "I" thành số "1"; đọc chữ X Latin thành chữ Hy Lạp trông giống hệt; lấy số lượng ở dòng bên cạnh **[Nguồn: B3, phụ lục D]**.
- **Độ tự tin của mô hình không dùng được để lọc.** Trên 55 trường hóa đơn DocILE, GPT-4o sai 26,6% số trường. Dùng logprob để đoán trường nào sai: AUC 0,705; hỏi mô hình tự chấm: 0,692; gọi 5 lần lấy đa số: 0,744 với giá gấp 5 **[Nguồn: B4]**. Tín hiệu tốt nhất lại là **phía tài liệu**: độ rõ của vùng chữ, giá trị có khớp với chữ OCR không, và hai cách đọc khác nhau có trùng nhau không. Gộp các tín hiệu này: AUC 0,928; tự động 80% trường tự tin nhất thì đúng 99,1% (so với 73,3% nếu không lọc) **[Nguồn: B4; chỉ tiếng Anh, một mô hình]**.
- **Tài liệu dài bị cắt.** Trên ExtractBench (370 tài liệu, 4.869 trang, 67 loại), một mô hình giảm từ 87,9% ở tài liệu ngắn xuống 27,9% ở tài liệu dài, do bỏ sót dòng trong danh sách dài; các mô hình chung và agent viết code không trả vị trí từng chữ **[Nguồn: B2; tác giả là LlamaIndex, hệ thống đứng đầu là của họ]**. Cùng bài: lên mô hình đắt hơn không chắc tốt hơn; một họ mô hình gần như không đổi điểm khi giá tăng gần 23 lần **[Nguồn: B2, phụ lục D.4]**.

**[Đề xuất] Rút ra cho SME:**
- Hàng rào bằng code rẻ nhất: **"giá trị trích ra có xuất hiện nguyên văn trong chữ của chứng từ không?"** Không có thì nghi bịa hoặc nghi mô hình tự sửa.
- Yêu cầu mô hình **chép nguyên văn** ("1.500.000"), để **code** chuẩn hóa thành số. Đừng để mô hình đổi định dạng.
- Không tin mô hình tự nói "tôi chắc chắn".
- Chứng từ dài (bảng kê nhiều trang): đếm số dòng bằng code và so với số dòng trên chứng từ.

## 4. Chuỗi bài nhỏ

### Bài K1.1: Kiểm kê nguồn dữ liệu gốc
- **Làm:** với mỗi loại chứng từ trong checklist K0, ghi: có XML/Excel gốc không; ai giữ; lấy bằng cách nào (email nhà cung cấp, cổng thuế, phần mềm kế toán). Gửi thư cho 3 nhà cung cấp lớn nhất xin gửi kèm XML.
- **Sản phẩm:** `nguon_du_lieu.xlsx` với cột `nguon_uu_tien` (xml / xuat_phan_mem / pdf_chu / anh).
- **Lỗi:** mặc định "chụp ảnh rồi đưa AI" trong khi XML đã nằm sẵn trong hộp thư.

### Bài K1.2: Đọc hóa đơn XML bằng code
- **Làm:** sửa bảng `MAP` theo file XML thật; chạy trên 20 hóa đơn; mở 5 hóa đơn bằng phần mềm xem chính thức và so từng trường.
- **Mã mẫu (đã chạy thử** 2026-11-11, `python -I -X utf8`, trên **một hóa đơn giả lập** do nhóm soạn tạo; **tên thẻ chưa đối chiếu văn bản gốc**):
  ```python
  import xml.etree.ElementTree as ET
  from decimal import Decimal as D
  MAP = {  # truong -> duong dan the: SUA THEO FILE THAT
      "so_hd": ".//TTChung/SHDon", "ky_hieu": ".//TTChung/KHHDon", "ngay": ".//TTChung/NLap",
      "mst_ban": ".//NBan/MST", "mst_mua": ".//NMua/MST",
      "tong_truoc_thue": ".//TToan/TgTCThue", "tien_thue": ".//TToan/TgTThue", "tong_tt": ".//TToan/TgTTTBSo"}
  DONG = {"ten": "THHDVu", "dvt": "DVTinh", "sl": "SLuong", "don_gia": "DGia", "thanh_tien": "ThTien"}
  TIEN = {"tong_truoc_thue", "tien_thue", "tong_tt"}

  def doc_xml(path):
      root = ET.parse(path).getroot()            # file hong -> bao loi, khong doan
      out, thieu = {"_nguon": path, "_vi_tri": {}}, []
      for k, p in MAP.items():
          el = root.find(p)
          if el is None or not (el.text or "").strip():
              out[k] = None; thieu.append(k); continue
          out[k] = D(el.text.strip()) if k in TIEN else el.text.strip()
          out["_vi_tri"][k] = p                  # vi tri = duong dan the
      out["dong"] = []
      for i, hh in enumerate(root.iter("HHDVu"), 1):
          d = {k: (hh.findtext(t) or "").strip() or None for k, t in DONG.items()}
          for k in ("sl", "don_gia", "thanh_tien"):
              d[k] = D(d[k]) if d[k] else None
          d["_vi_tri"] = f"HHDVu[{i}]"; out["dong"].append(d)
      out["_thieu"] = thieu
      return out
  ```
  Kết quả: đọc đủ 9 trường và 2 dòng hàng; số tiền ở dạng `Decimal` (không dùng `float` cho tiền).
- **Sản phẩm:** `doc_xml.py` + `hoa_don_json/*.json`.
- **Lỗi:** dùng `float` cho tiền; bỏ qua namespace XML (nếu file thật có `xmlns`, đường dẫn thẻ phải kèm namespace; **chưa kiểm** file thật có hay không); tin rằng hóa đơn hợp lệ chỉ vì đọc được XML (đọc được không có nghĩa chữ ký hợp lệ).

### Bài K1.3: Lược đồ JSON cho chứng từ không có dữ liệu gốc
- **Làm:** với phiếu giao hàng, đơn mua giấy, viết lược đồ. Mỗi trường có ba phần:
  ```json
  {"so_luong": {"gia_tri": "1.000", "vi_tri": "trang 1, bảng dòng 2, cột SL", "ghi_chu": null}}
  ```
  `gia_tri` là **chuỗi chép nguyên văn**; không thấy thì `null`. Thêm `so_dong_tren_chung_tu` để code đếm.
- **Sản phẩm:** `luoc_do_phieu_giao.json` + 3 ví dụ điền tay.
- **Lỗi:** cho mô hình trả số đã chuẩn hóa ngay (mất khả năng kiểm với bản gốc).

### Bài K1.4: Trích bằng mô hình + kiểm bằng code
- **Làm:** **[NC]** trong Project: dán lược đồ, yêu cầu trả đúng JSON. **[PY]** gọi API như `../rag-tra-cuu-tai-lieu/cap-01-goi-api.md`. Sau đó chạy hàm kiểm dưới với chữ của chứng từ (lớp chữ PDF, hoặc bản OCR).
- **Mã mẫu (đã chạy thử** 2026-11-11, `python -I`, dữ liệu giả lập):
  ```python
  import re, unicodedata
  from decimal import Decimal as D
  def so_vn(s):          # '1.500.000' -> 1500000 ; '1.500.000,50' -> 1500000.50
      s = s.strip().replace(" ", "")
      if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", s): return D(s.replace(".", "").replace(",", "."))
      if re.fullmatch(r"\d+(,\d+)?", s): return D(s.replace(",", "."))
      raise ValueError(f"so khong ro dinh dang: {s!r}")   # '1,500' -> nguoi xem
  def co_trong_text(g, text):
      n = lambda x: unicodedata.normalize("NFC", " ".join(str(x).split()))
      return n(g) in n(text)
  def kiem_ban_trich(trich, text):
      return {k: "THIEU" if v["gia_tri"] is None else
                 "OK" if co_trong_text(v["gia_tri"], text) else "KHONG_THAY_TRONG_GOC"
              for k, v in trich.items()}
  ```
  Kết quả thử: chứng từ ghi "Đơn giá 4.500"; bản trích ghi `"4500"` bị gắn `KHONG_THAY_TRONG_GOC`. Đây là đúng ý: mô hình đã tự đổi định dạng, nên phải yêu cầu chép nguyên văn rồi để `so_vn` chuẩn hóa. Chuỗi "1,500" bị từ chối vì không rõ là một nghìn năm trăm hay một phẩy năm.
- **Sản phẩm:** `kiem_trich.py`; mọi trường không phải `OK` vào hàng đợi người.
- **Lỗi:** áp hàm kiểm lên ảnh không có lớp chữ (không có "text gốc" để so; khi đó chỉ còn cách đọc lại hoặc người xem).

### Bài K1.5: Đọc hai lần theo hai cách (tùy chọn)
- **Làm:** gọi lần 1 "điền từng trường của lược đồ"; lần 2 "liệt kê mọi cặp nhãn - giá trị bạn thấy trên chứng từ". So hai kết quả bằng code; trường lệch đi đến người.
- **Vì sao:** trong B4, cách đọc theo từng trường có xu hướng bịa giá trị cho trường trống; cách đọc toàn văn có xu hướng bỏ sót; độ lệch giữa hai cách là tín hiệu có ích nhất trong các tín hiệu thêm vào **[Nguồn: B4]**. **[Đề xuất]** Không cần bộ phân loại học máy như bài báo; chỉ cần quy tắc "lệch thì người xem".
- **Lỗi:** dùng hai lần gọi giống hệt nhau (chỉ đo dao động ngẫu nhiên, không đo cách đọc khác).

### Bài K1.6: Đo theo từng trường trên bộ mẫu
- **Làm:** dùng bộ mẫu K0.2. Với mỗi trường: tỷ lệ đúng, tỷ lệ `null`, tỷ lệ bị hàm kiểm gắn cờ. Tách riêng **tiền, MST, ngày, số chứng từ**: mục tiêu 0 lỗi lọt sau hàm kiểm.
- **Sản phẩm:** `do_truong.xlsx`. Cách tính khoảng tin cậy: `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`.

## 5. Đường không code vs có code; khi nào buộc chuyển

| Việc | Không code | Có code |
|---|---|---|
| Hóa đơn điện tử | Mở XML bằng phần mềm xem, gõ lại vào Excel | `doc_xml.py` |
| Danh sách hóa đơn mua vào | Xuất Excel từ cổng thuế, lọc bằng Excel | Đọc file Excel đã xuất bằng `pandas` |
| Phiếu giao, đơn mua giấy | Project trả JSON, dán vào Excel; người so với ảnh | Gọi API + `kiem_trich.py` |

**Buộc chuyển sang code khi [Đề xuất]:** có XML (code rẻ hơn gõ tay ngay từ hóa đơn đầu tiên); hoặc hơn khoảng 30 chứng từ ảnh/PDF mỗi tuần; hoặc K1.6 cho thấy có lỗi tiền/MST lọt.

## 6. Tiêu chí lên K2 (đo được) [Đề xuất]

1. Mọi loại chứng từ trong checklist có nguồn ưu tiên được ghi; ít nhất loại nhiều nhất đã dùng nguồn gốc (XML/Excel) nếu có.
2. Trên 20 hóa đơn XML: 100% trường khớp với phần mềm xem chính thức.
3. Với chứng từ không có dữ liệu gốc: mỗi trường có `gia_tri` nguyên văn và `vi_tri`; trên bộ mẫu, 0 lỗi tiền/MST/ngày lọt qua hàm kiểm (lỗi bị gắn cờ thì được tính là bắt được).
4. Có bảng `do_truong.xlsx`.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

**a) Nhà phân phối thực phẩm khô, 40 nhà cung cấp.** Trước: kế toán chụp hóa đơn PDF, nhập tay vào phần mềm. Sau K1: xin mọi nhà cung cấp gửi XML kèm thư; tải danh sách hóa đơn mua vào trên cổng thuế mỗi tuần để biết hóa đơn nào chưa nhận được file. `doc_xml.py` chạy trên thư mục XML; không dùng AI cho hóa đơn. AI chỉ dùng cho phiếu giao hàng viết tay của 5 nhà cung cấp nhỏ, qua K1.4.

**b) Công ty xây dựng nhỏ, 3 công trình.** Chứng từ: biên bản nghiệm thu khối lượng (Word, PDF có chữ), phiếu xuất vật tư (ảnh chụp điện thoại). Biên bản: trích lớp chữ, mô hình điền lược đồ, `kiem_trich.py` kiểm mọi khối lượng có trong chữ gốc. Phiếu ảnh: K1.5 hai lần đọc; lệch thì kỹ thuật viên công trình xác nhận.

**c) Trung tâm ngoại ngữ, tuyển 10 giáo viên mỗi quý.** CV nhiều mẫu, PDF có chữ. Lược đồ: họ tên, bằng cấp, chứng chỉ, năm kinh nghiệm, mỗi trường có vị trí. Che số CCCD, địa chỉ, số điện thoại trước khi gửi lên dịch vụ ngoài (xem `cap-05`).

## 8. Tài liệu tham khảo

| Mã | Nguồn | Tin cậy |
|---|---|---|
| B2 | Zhang et al., ExtractBench, arXiv 2607.29677. https://www.alphaxiv.org/abs/2607.29677 | Trung bình: bộ dữ liệu công khai, nhưng tác giả là nhà cung cấp và sản phẩm của họ đứng đầu |
| B3 | Shen et al., OCR or Not?, SAP + Stanford, arXiv 2603.02789. https://www.alphaxiv.org/abs/2603.02789 | Trung bình-cao: dữ liệu thật nhưng nội bộ; mô hình 2024-2025 |
| B4 | Kumar, Beyond Logprobs (ExtractConf), arXiv 2606.24420. https://www.alphaxiv.org/abs/2606.24420 | Trung bình: một tác giả, một mô hình, tiếng Anh, tập kiểm 267 trường |
| B1 | ESCROW, BMO, arXiv 2608.01772 (quy tắc "đọc dòng in, không tự tính"; chuẩn hóa dấu phẩy) | Trung bình-cao |
| V1 | EY, Bản tin thuế tháng 7/2026, NĐ 254/2026/NĐ-CP. https://www.ey.com/vi_vn/technical/tax/tax-and-law-updates/nghi-dinh-254-2026-nd-cp-ve-hoa-don-dien-tu-va-chung-tu-dien-tu | Trung bình-cao (hãng tư vấn); đọc qua công cụ tóm tắt |
| V3 | Quyết định 1450/QĐ-TCT (2021), trang tra cứu: https://thuvienphapluat.vn/van-ban/thue-phi-le-phi/quyet-dinh-1450-qd-tct-2021-thanh-phan-chua-du-lieu-nghiep-vu-hoa-don-dien-tu-490526.aspx | Chưa đọc toàn văn |
| V4 | MISA meInvoice, "Hóa đơn điện tử file XML". https://www.meinvoice.vn/tin-tuc/9169/hoa-don-dien-tu-file-xml/ | Thấp-trung bình: trang nhà cung cấp, viết theo NĐ 123 |
| V5 | xcyber.vn, file XML hóa đơn điện tử. https://xcyber.vn/?p=15270 ; hướng dẫn lấy hóa đơn đầu vào (MISA). https://sme.misa.vn/351069/cach-lay-hoa-don-dau-vao-tren-trang-thue-dien-tu/ | Thấp: thứ cấp; giao diện cổng có thể đổi |

## 9. Chưa kiểm chứng

- **Tên thẻ XML** trong `MAP` là ví dụ, chưa đối chiếu QĐ 1450/QĐ-TCT hay văn bản thay thế; chưa biết file thật có namespace không.
- Văn bản nào quy định định dạng XML sau NĐ 254/2026; QĐ 1450 còn hiệu lực không.
- Các bước trên cổng hóa đơn điện tử (tra cứu, xuất Excel/XML) chỉ có từ hướng dẫn thứ cấp.
- Chưa có số đo độ chính xác của mô hình thị giác trên phiếu giao, hóa đơn ảnh tiếng Việt. Khảo sát B10 không có số liệu này.
- Kết quả B4 (lọc theo tín hiệu tài liệu) cần OCR có điểm tin cậy từng chữ; dịch vụ OCR nào hỗ trợ tiếng Việt và trả điểm này: chưa kiểm.
