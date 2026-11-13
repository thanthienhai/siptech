# Cấp K6: Đánh giá theo từng quy tắc và hàng đợi duyệt

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung.
> Đã có, không viết lại: bộ ca mẫu, khoảng tin cậy Wilson khi n nhỏ, kappa, LLM-as-judge, đo thời gian tiết kiệm (`../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`); thiết kế hàng đợi, SLA, chống duyệt cho xong (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4). File này viết phần riêng: **đo theo từng quy tắc bằng hồ sơ cài lỗi sẵn**, và **chia việc cho người duyệt theo kết quả**.

## 1. Mục tiêu và người đọc

**Người đọc:** người vận hành hệ thống kiểm (thường là kế toán trưởng hoặc người code nhẹ) và người duyệt.

**Sau cấp này có:**
1. Bộ hồ sơ **cài lỗi sẵn**: mỗi quy tắc có ít nhất vài ca lỗi và vài ca đạt, biết trước đáp án.
2. Bảng đo **theo từng quy tắc**: bắt được, bỏ sót (kết luận "đạt" khi có lỗi), báo nhầm, không rõ; kèm khoảng tin cậy.
3. Quy tắc chia hồ sơ: hồ sơ nào người xem kỹ, hồ sơ nào xem nhanh, hồ sơ nào lấy mẫu kiểm lại.
4. Cách kiểm người duyệt có thật sự xem không.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Hệ thống có bỏ sót lỗi không, ở quy tắc nào, và người duyệt có bắt được phần còn lại không?"*

Lỗi khi chỉ đo tổng: "đúng 92%" che mất việc một quy tắc quan trọng bỏ sót một nửa số lỗi. Lỗi khi chỉ đo hệ thống: quên rằng người duyệt cũng có thể bỏ qua.

## 3. Kiến thức nền

### 3.1 Cài lỗi sẵn là cách tạo đáp án rẻ
- ContractScrub tạo đáp án bằng ba bước: luật sư chọn hợp đồng thật, ghi lại các lỗi có sẵn, rồi **chèn thêm lỗi có chủ đích** theo từng loại, ghi mỗi lỗi chèn thành một bộ (loại, vị trí) **[Nguồn: B7, mục 3.2]**. Chỉ số chính là **recall** theo từng loại, vì bỏ sót đắt hơn báo nhầm và vì hợp đồng gốc có thể còn lỗi chưa ai biết **[Nguồn: B7, mục 3.3]**.
- FinDAS lấy mẫu **bằng nhau theo nhóm** (70 ca mỗi nhóm: thường, bịa giá trị, ca biên), không theo tần suất thật, để mỗi nhóm được đo cùng độ phân giải; một ca đổi tỷ lệ nhóm khoảng 1/70 **[Nguồn: B1, phụ lục G.1]**.
- **[Đề xuất]** SME làm như sau: lấy hồ sơ thật đã đúng, tạo bản sao, sửa đúng một chỗ ứng với một quy tắc (đổi đơn giá, xóa một điều, đổi MST một chữ số). Mỗi quy tắc mức "cao": ít nhất 5 ca lỗi, 5 ca đạt.

### 3.2 Bốn con số cho mỗi quy tắc [Đề xuất]

| Con số | Định nghĩa | Ý nghĩa |
|---|---|---|
| Bắt được | Đáp án lỗi, hệ thống `LOI` | Tốt |
| **Bỏ sót kết luận đạt** | Đáp án lỗi, hệ thống `DAT` | **Nguy hiểm nhất**: người duyệt dễ bỏ qua hồ sơ "đạt" |
| Không rõ | Hệ thống `KHONG_RO` | Không sai, nhưng tốn công người |
| Báo nhầm | Đáp án đạt, hệ thống `LOI` | Tốn công, làm người duyệt mất tin |

Mục tiêu cho quy tắc mức "cao": bỏ sót kết luận đạt bằng 0 trên bộ mẫu. Không rõ và báo nhầm là chi phí, chấp nhận được trong giới hạn sức người duyệt. Ca Erste cũng chọn hướng báo thừa thay vì báo thiếu **[Nguồn: B5]**.

### 3.3 Chia việc cho người duyệt
- Trong B4, lọc theo tín hiệu tin cậy cho phép tự động 80% số trường tự tin nhất với độ đúng 99,1%, phần còn lại cho người **[Nguồn: B4; tiếng Anh, một mô hình]**. MAP ghi nhận các nhóm dùng LLM chấm đều kết hợp người: ca tin cậy thấp chuyển chuyên gia, lấy mẫu ngẫu nhiên phần tin cậy cao để kiểm tiếp **[Nguồn: `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4, dẫn MAP]**.
- Hệ thống thiết bị y tế (B6) nhắc rằng hướng dẫn của cơ quan quản lý cảnh báo cả chuyên gia cũng có xu hướng **dựa quá mức vào gợi ý tự động** **[Nguồn: B6, mở đầu]**.
- **[Đề xuất] Quy tắc chia:**
  - Có `LOI` hoặc `KHONG_RO` ở quy tắc mức cao → **xem kỹ**: người mở chứng từ gốc tại vị trí được chỉ.
  - Toàn `DAT` → **xem nhanh**: người ký, nhưng hệ thống chọn ngẫu nhiên một phần (ví dụ 1 trong 10) để xem kỹ.
  - Quy tắc mờ có trích dẫn bị hàng rào hạ → luôn xem kỹ.

### 3.4 Kiểm người duyệt
- **[Đề xuất]** Thỉnh thoảng đưa vào hàng đợi một hồ sơ cài lỗi đã biết (không báo trước), mà hệ thống đã cố ý ghi `DAT`. Nếu người duyệt ký qua, đó là tín hiệu "duyệt cho xong". Cách này cần người duyệt được thông báo chung rằng có kiểm như vậy, và không dùng để phạt.

## 4. Chuỗi bài nhỏ

### Bài K6.1: Dựng bộ hồ sơ cài lỗi
- **Làm:** với mỗi quy tắc trong sổ, tạo ít nhất 5 bản sao có lỗi, mỗi bản một lỗi; giữ 5 hồ sơ đạt. Với hóa đơn XML: sửa bản sao XML (không phải hóa đơn thật đã nộp). Ghi `dap_an.csv`: (hồ sơ, mã quy tắc, kết quả đúng).
- **Sản phẩm:** thư mục `bo_cai_loi/` + `dap_an.csv`.
- **Lỗi:** một bản sao có nhiều lỗi (không biết quy tắc nào bắt); quên ca đạt "khó" (giao hàng nhiều đợt đúng, hợp đồng khác mẫu nhưng đã được duyệt).

### Bài K6.2: Chấm theo từng quy tắc
- **Mã mẫu (đã chạy thử** 2026-11-11, `python -I -X utf8`, dữ liệu giả):
  ```python
  import math
  from collections import defaultdict
  def wilson(k, n, z=1.96):
      if n == 0: return (0.0, 1.0)
      p = k / n; d = 1 + z*z/n
      c = (p + z*z/(2*n)) / d; h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
      return (max(0, c-h), min(1, c+h))
  def cham(dap_an, he_thong):        # {(ho_so, ma): 'LOI'|'DAT'|'KHONG_RO'}
      t = defaultdict(lambda: {"bat": 0, "sot": 0, "nham": 0, "khong_ro": 0, "co_loi": 0})
      for (hs, ma), dung in dap_an.items():
          du = he_thong.get((hs, ma), "KHONG_RO"); s = t[ma]
          if du == "KHONG_RO": s["khong_ro"] += 1
          if dung == "LOI":
              s["co_loi"] += 1
              if du == "LOI": s["bat"] += 1
              elif du == "DAT": s["sot"] += 1
          elif du == "LOI": s["nham"] += 1
      for ma, s in sorted(t.items()):
          lo, hi = wilson(s["bat"], s["co_loi"])
          print(f"{ma}: bat {s['bat']}/{s['co_loi']} (KTC95 {lo:.0%}-{hi:.0%}), "
                f"sot_ket_luan_dat {s['sot']}, bao_nham {s['nham']}, khong_ro {s['khong_ro']}")
  ```
  Kết quả thử trên 20 hồ sơ giả: `HD-04: bat 10/10 (KTC95 72%-100%), sot_ket_luan_dat 0, bao_nham 0, khong_ro 0`; `HDG-02: bat 4/8 (KTC95 22%-78%), sot_ket_luan_dat 2, bao_nham 1, khong_ro 2`. Đọc: quy tắc code `HD-04` bắt hết 10 ca, nhưng với n = 10 khoảng tin cậy dưới vẫn là 72%; quy tắc mờ `HDG-02` có 2 ca bỏ sót kết luận đạt → chưa được để "xem nhanh".
- **Sản phẩm:** `cham.py` + bảng đo mỗi lần đổi sổ quy tắc.

### Bài K6.3: Đo độ ổn định của quy tắc mờ
- **Làm:** chạy quy tắc mờ 3 lần trên bộ cài lỗi (khác giờ, khác ngày). Ô nào đổi kết quả → ghi là "không ổn định". Quy tắc có nhiều ô không ổn định: viết lại câu hỏi hẹp hơn (K3.1) hoặc chuyển phần kiểm được sang code.
- **Vì sao:** B6 thấy dao động có thể chỉ xuất hiện giữa các ngày; đo một buổi có thể kết luận nhầm là ổn định **[Nguồn: B6]**.

### Bài K6.4: Quy tắc chia hồ sơ và đo tải người duyệt
- **Làm:** áp quy tắc ở 3.3. Đếm mỗi tuần: % hồ sơ xem kỹ, % xem nhanh, thời gian trung bình mỗi loại, số lần người duyệt không đồng ý với hệ thống (theo mã quy tắc).
- **Sản phẩm:** bảng tuần. Nếu % xem kỹ quá cao so với sức người, giảm báo nhầm ở quy tắc gây nhiều nhất; **không** giảm bằng cách đổi `KHONG_RO` thành `DAT`.

### Bài K6.5: Hồ sơ kiểm người duyệt
- **Làm:** mỗi tháng đưa 2-3 hồ sơ cài lỗi vào hàng đợi với kết quả hệ thống bị đặt là `DAT`. Ghi người duyệt có phát hiện không. Thông báo trước với nhóm rằng có kiểm như vậy.
- **Lỗi:** dùng kết quả để phạt (người duyệt sẽ xem mọi hồ sơ là đáng ngờ, hàng đợi ứ).

## 5. Đường không code vs có code; khi nào buộc chuyển

- **Không code:** bảng Excel hai sheet (đáp án, kết quả), `COUNTIFS` theo mã quy tắc; khoảng Wilson tính bằng công thức (xem `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`).
- **Có code:** `cham.py` chạy sau mỗi lần sửa quy tắc, kết quả lưu theo phiên bản (nối với K7).
- **Buộc chuyển sang code khi [Đề xuất]:** hơn khoảng 10 quy tắc hoặc hơn 50 hồ sơ trong bộ cài lỗi; hoặc sửa quy tắc hơn một lần mỗi tháng.

## 6. Tiêu chí lên K7 (đo được) [Đề xuất]

1. Mọi quy tắc mức "cao" có ít nhất 5 ca lỗi + 5 ca đạt trong bộ cài lỗi.
2. Bỏ sót kết luận đạt = 0 trên bộ cài lỗi cho mọi quy tắc mức "cao" được phép "xem nhanh"; quy tắc nào chưa đạt thì luôn "xem kỹ".
3. Quy tắc chia hồ sơ đã chạy ít nhất 4 tuần, có số tải người duyệt.
4. Đã chạy K6.5 ít nhất một lần.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa; số giả định]

**a) Công ty phân phối linh kiện điện tử, 300 hóa đơn đầu vào mỗi tháng.** Bộ cài lỗi 60 hồ sơ cho 9 quy tắc hóa đơn và 6 quy tắc ba bên. Sau K6.2: 13 quy tắc code không bỏ sót; quy tắc mờ "mô tả hàng phù hợp" có 1 bỏ sót trong 6 ca lỗi → luôn xem kỹ. Tuần đầu: 35% hồ sơ xem kỹ, phần lớn do `BB-05` (giao thiếu) báo nhầm khi phiếu nhập về chậm. Sửa: đợi 2 ngày sau ngày hóa đơn mới chạy `BB-05`.

**b) Trung tâm đào tạo lái xe, hồ sơ học viên.** Quy tắc: đủ giấy khám sức khỏe còn hạn, ảnh đúng quy cách, khớp họ tên giữa đơn và giấy tờ. Bộ cài lỗi: 20 hồ sơ, mỗi hồ sơ sửa một chỗ (đổi một chữ trong tên, ngày khám quá hạn). Kết quả giả định: quy tắc khớp tên báo nhầm khi tên có dấu khác kiểu gõ (NFC/NFD) → sửa chuẩn hóa Unicode ở K1, không sửa quy tắc.

## 8. Tài liệu tham khảo

| Mã | Nguồn | Tin cậy |
|---|---|---|
| B7 | ContractScrub, arXiv 2608.20204, mục 3.2-3.3 | Trung bình-cao |
| B1 | ESCROW, arXiv 2608.01772, phụ lục G.1 | Trung bình-cao |
| B4 | ExtractConf, arXiv 2606.24420 | Trung bình |
| B5 | Erste, arXiv 2610.20155 | Trung bình |
| B6 | arXiv 2610.21300 | Trung bình |
| R6 | Nhóm RAG, đánh giá | `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` |

## 9. Chưa kiểm chứng

- Các ngưỡng (5 ca lỗi + 5 ca đạt, 1 trong 10 để xem kỹ, 2-3 hồ sơ kiểm người duyệt mỗi tháng) là đề xuất, chưa có nguồn. Với 5 ca, khoảng tin cậy rất rộng: chỉ để phát hiện hỏng.
- Lỗi cài sẵn có thể dễ hơn lỗi thật (lỗi thật thường tinh vi hơn); chưa có nguồn đo chênh lệch này cho chứng từ.
- Cách kiểm người duyệt bằng hồ sơ cài lỗi (K6.5) chưa có nguồn đo tác dụng; cần cân nhắc yếu tố quan hệ lao động.
- Chưa có số đo tải người duyệt thật ở SME Việt Nam.
