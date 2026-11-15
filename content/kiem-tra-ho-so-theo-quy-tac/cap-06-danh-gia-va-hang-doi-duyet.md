# Cấp K6: Đánh giá theo từng quy tắc và hàng đợi duyệt

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung.
> Đã có, không viết lại: bộ ca mẫu, khoảng tin cậy Wilson khi n nhỏ, kappa, LLM-as-judge, đo thời gian tiết kiệm (`../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`); thiết kế hàng đợi, SLA, chống duyệt cho xong (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4). File này viết phần riêng: **đo theo từng quy tắc bằng hồ sơ cài lỗi sẵn**, và **chia việc cho người duyệt theo kết quả**.

!!! tip "Tóm tắt nhanh"
    Hệ thống kiểm hồ sơ có thể báo "đúng 92%" nhưng vẫn bỏ sót một nửa số lỗi ở một quy tắc quan trọng. Bài này dạy bạn đo **riêng từng quy tắc**, bằng cách tự tạo các hồ sơ **đã cài lỗi sẵn** nên biết trước đáp án. Sau đó bạn chia hồ sơ cho người duyệt: hồ sơ nào xem kỹ, hồ sơ nào xem nhanh, và kiểm xem người duyệt có thật sự xem hay không.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người vận hành hệ thống kiểm (thường là kế toán trưởng hoặc người biết code nhẹ) và người duyệt hồ sơ. Phần đo bằng bảng Excel thì người không biết lập trình vẫn làm được.

**Bạn cần chuẩn bị:**
- Sổ quy tắc của hệ thống kiểm (danh sách các quy tắc mà hệ thống đang dùng để kiểm hồ sơ).
- Một số hồ sơ thật đã được xác nhận là đúng, để sao chép ra làm hồ sơ thử.
- Một bảng Excel (hai sheet) để ghi đáp án và kết quả. Nếu muốn chạy tự động thì cần người biết code, hoặc nhờ AI, chạy giúp tệp `cham.py`.

**Sau bài này bạn sẽ có:**
1. Bộ hồ sơ **cài lỗi sẵn**: mỗi quy tắc có ít nhất vài ca lỗi và vài ca đạt, biết trước đáp án.
2. Bảng đo **theo từng quy tắc**: bắt được, bỏ sót (kết luận "đạt" khi có lỗi), báo nhầm, không rõ; kèm khoảng tin cậy (một khoảng cho biết con số đo được có thể dao động bao nhiêu, vì bộ mẫu nhỏ).
3. Quy tắc chia hồ sơ: hồ sơ nào người xem kỹ, hồ sơ nào xem nhanh, hồ sơ nào lấy mẫu kiểm lại.
4. Cách kiểm người duyệt có thật sự xem không.

**Thứ bạn cầm đi được sau bài:** thư mục `bo_cai_loi/` cùng tệp `dap_an.csv`; tệp `cham.py` và bảng đo mỗi lần đổi sổ quy tắc; quy tắc chia hồ sơ cho người duyệt; bảng theo dõi tải người duyệt theo tuần.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Hệ thống có bỏ sót lỗi không, ở quy tắc nào, và người duyệt có bắt được phần còn lại không?"*

Có hai cái bẫy thường gặp. Bẫy thứ nhất là chỉ đo con số tổng. Một con số như "đúng 92%" có thể che mất việc một quy tắc quan trọng bỏ sót một nửa số lỗi. Bẫy thứ hai là chỉ đo hệ thống mà quên rằng người duyệt cũng có thể bỏ qua.

!!! tip "Nói đơn giản"
    Đừng chỉ hỏi "cả hệ thống đúng bao nhiêu phần trăm". Hãy hỏi "quy tắc nào bỏ sót lỗi" và "người duyệt có thật sự xem không".

## 3. Kiến thức nền

### 3.1 Cài lỗi sẵn là cách tạo đáp án rẻ

Muốn đo hệ thống thì phải có đáp án đúng để so. Làm đáp án bằng tay cho hàng trăm hồ sơ rất tốn công. Cách rẻ hơn là **tự chèn lỗi vào hồ sơ rồi ghi lại chỗ đã chèn**, nhờ vậy ta biết chắc đáp án.

- ContractScrub tạo đáp án bằng ba bước: luật sư chọn hợp đồng thật, ghi lại các lỗi có sẵn, rồi **chèn thêm lỗi có chủ đích** theo từng loại, ghi mỗi lỗi chèn thành một bộ (loại, vị trí) **[Nguồn: B7, mục 3.2]**. Chỉ số chính là **recall** theo từng loại (recall = trong số các lỗi có thật, hệ thống bắt được bao nhiêu phần). Họ chọn recall vì bỏ sót đắt hơn báo nhầm, và vì hợp đồng gốc có thể còn lỗi chưa ai biết **[Nguồn: B7, mục 3.3]**.
- FinDAS lấy mẫu **bằng nhau theo nhóm** (70 ca mỗi nhóm: thường, bịa giá trị, ca biên), không theo tần suất thật, để mỗi nhóm được đo cùng độ phân giải. Một ca đổi tỷ lệ nhóm khoảng 1/70 **[Nguồn: B1, phụ lục G.1]**. (Ca biên là ca nằm sát ranh giới giữa đúng và sai, khó quyết định.)
- **[Đề xuất]** SME (doanh nghiệp nhỏ và vừa) làm như sau: lấy hồ sơ thật đã đúng, tạo bản sao, sửa đúng một chỗ ứng với một quy tắc (đổi đơn giá, xóa một điều, đổi MST một chữ số; MST là mã số thuế). Mỗi quy tắc mức "cao": ít nhất 5 ca lỗi, 5 ca đạt.

!!! tip "Nói đơn giản"
    Bạn lấy một hồ sơ đúng, photo ra, cố ý sửa sai một chỗ. Vì chính bạn sửa nên bạn biết đáp án. Rồi xem hệ thống có phát hiện ra chỗ sai đó không.

### 3.2 Bốn con số cho mỗi quy tắc [Đề xuất]

Với mỗi quy tắc, ta đếm bốn con số sau. Trong bảng, `LOI` là hệ thống báo có lỗi, `DAT` là hệ thống báo đạt, `KHONG_RO` là hệ thống không kết luận được.

| Con số | Định nghĩa | Ý nghĩa |
|---|---|---|
| Bắt được | Đáp án lỗi, hệ thống `LOI` | Tốt |
| **Bỏ sót kết luận đạt** | Đáp án lỗi, hệ thống `DAT` | **Nguy hiểm nhất**: người duyệt dễ bỏ qua hồ sơ "đạt" |
| Không rõ | Hệ thống `KHONG_RO` | Không sai, nhưng tốn công người |
| Báo nhầm | Đáp án đạt, hệ thống `LOI` | Tốn công, làm người duyệt mất tin |

Mục tiêu cho quy tắc mức "cao": bỏ sót kết luận đạt bằng 0 trên bộ mẫu. Không rõ và báo nhầm là chi phí, chấp nhận được trong giới hạn sức người duyệt. Ca Erste cũng chọn hướng báo thừa thay vì báo thiếu **[Nguồn: B5]**.

!!! tip "Nói đơn giản"
    Trong bốn con số, con số đáng sợ nhất là "bỏ sót kết luận đạt": hồ sơ có lỗi mà hệ thống lại bảo "đạt". Người duyệt thường lướt qua hồ sơ đã được bảo là đạt, nên lỗi lọt thẳng ra ngoài. Báo nhầm và không rõ chỉ tốn công người xem.

### 3.3 Chia việc cho người duyệt

- Trong B4, lọc theo tín hiệu tin cậy cho phép tự động 80% số trường tự tin nhất với độ đúng 99,1%, phần còn lại cho người **[Nguồn: B4; tiếng Anh, một mô hình]**. MAP ghi nhận các nhóm dùng LLM chấm đều kết hợp người: ca tin cậy thấp chuyển chuyên gia, lấy mẫu ngẫu nhiên phần tin cậy cao để kiểm tiếp **[Nguồn: `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` mục 3.4, dẫn MAP]**. (LLM là mô hình AI ngôn ngữ lớn; "LLM chấm" là dùng một AI để chấm điểm.)
- Hệ thống thiết bị y tế (B6) nhắc rằng hướng dẫn của cơ quan quản lý cảnh báo cả chuyên gia cũng có xu hướng **dựa quá mức vào gợi ý tự động** **[Nguồn: B6, mở đầu]**.
- **[Đề xuất] Quy tắc chia:**
  - Có `LOI` hoặc `KHONG_RO` ở quy tắc mức cao → **xem kỹ**: người mở chứng từ gốc tại vị trí được chỉ.
  - Toàn `DAT` → **xem nhanh**: người ký, nhưng hệ thống chọn ngẫu nhiên một phần (ví dụ 1 trong 10) để xem kỹ.
  - Quy tắc mờ có trích dẫn bị hàng rào hạ → luôn xem kỹ.

(Quy tắc mờ là quy tắc phải nhờ AI đọc hiểu, không kiểm được bằng phép so sánh cứng. Hàng rào là bước chặn tự động: nếu câu trích dẫn của AI không khớp chứng từ thì hệ thống hạ kết luận xuống.)

!!! tip "Nói đơn giản"
    Hồ sơ nào hệ thống thấy có vấn đề hoặc không chắc thì người xem kỹ. Hồ sơ nào hệ thống báo đạt hết thì người xem nhanh, nhưng vẫn bốc ngẫu nhiên một vài hồ sơ để xem kỹ, phòng khi hệ thống sai mà không ai biết.

### 3.4 Kiểm người duyệt

- **[Đề xuất]** Thỉnh thoảng đưa vào hàng đợi một hồ sơ cài lỗi đã biết (không báo trước), mà hệ thống đã cố ý ghi `DAT`. Nếu người duyệt ký qua, đó là tín hiệu "duyệt cho xong". Cách này cần người duyệt được thông báo chung rằng có kiểm như vậy, và không dùng để phạt.

## 4. Chuỗi bài nhỏ

Năm bài thực hành dưới đây làm theo thứ tự. Mỗi bài ghi rõ việc cần làm và thứ bạn có sau bài; một số bài có thêm phần lỗi hay gặp.

### Bài K6.1: Dựng bộ hồ sơ cài lỗi
- **Việc cần làm:** với mỗi quy tắc trong sổ, tạo ít nhất 5 bản sao có lỗi, mỗi bản một lỗi; giữ 5 hồ sơ đạt. Với hóa đơn XML (XML là định dạng tệp hóa đơn điện tử máy đọc được): sửa bản sao XML (không phải hóa đơn thật đã nộp). Ghi `dap_an.csv` (CSV là tệp bảng đơn giản, mở được bằng Excel) gồm các cột: (hồ sơ, mã quy tắc, kết quả đúng).
- **Bạn có sau bài:** thư mục `bo_cai_loi/` + `dap_an.csv`.
- **Lỗi hay gặp:** một bản sao có nhiều lỗi (không biết quy tắc nào bắt); quên ca đạt "khó" (giao hàng nhiều đợt đúng, hợp đồng khác mẫu nhưng đã được duyệt).

### Bài K6.2: Chấm theo từng quy tắc
- **Việc cần làm:** chạy đoạn mã mẫu dưới đây để chấm kết quả của hệ thống so với `dap_an.csv`, cho từng quy tắc. Bạn không cần tự viết; chỉ cần nhờ người biết code hoặc nhờ AI chạy giúp.

  **Đoạn mã dưới đây làm gì?** Nó nhận hai thứ: bảng đáp án (hồ sơ nào, quy tắc nào, đáp án đúng là `LOI` hay `DAT`) và kết quả của hệ thống. Nó đếm cho từng quy tắc bốn con số ở mục 3.2 (bắt được, bỏ sót kết luận đạt, báo nhầm, không rõ). Nó cũng tính thêm khoảng tin cậy Wilson, là khoảng cho biết tỷ lệ bắt được thật sự có thể nằm trong đâu khi bộ mẫu còn ít. Bạn **không cần đọc hiểu từng dòng**; chỉ cần nhờ người biết lập trình (hoặc nhờ AI) chạy giúp.

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

!!! tip "Nói đơn giản"
    Quy tắc `HD-04` bắt đủ 10 trên 10 ca lỗi, nhưng vì chỉ thử 10 ca nên ta chưa dám nói nó chắc chắn đúng hoàn toàn. Quy tắc `HDG-02` có 2 ca lỗi bị bảo là "đạt", nên hồ sơ qua quy tắc này chưa được phép xem nhanh.

- **Bạn có sau bài:** `cham.py` + bảng đo mỗi lần đổi sổ quy tắc.

### Bài K6.3: Đo độ ổn định của quy tắc mờ
- **Việc cần làm:** chạy quy tắc mờ 3 lần trên bộ cài lỗi (khác giờ, khác ngày). Ô nào đổi kết quả → ghi là "không ổn định". Quy tắc có nhiều ô không ổn định: viết lại câu hỏi hẹp hơn (K3.1) hoặc chuyển phần kiểm được sang code.
- **Vì sao:** B6 thấy dao động có thể chỉ xuất hiện giữa các ngày; đo một buổi có thể kết luận nhầm là ổn định **[Nguồn: B6]**.

!!! tip "Nói đơn giản"
    AI có thể trả lời khác nhau cho cùng một câu hỏi. Vì vậy hãy hỏi lại nhiều lần, vào nhiều ngày khác nhau. Câu nào lúc đúng lúc sai thì câu hỏi đó chưa đáng tin.

### Bài K6.4: Quy tắc chia hồ sơ và đo tải người duyệt
- **Việc cần làm:** áp quy tắc ở 3.3. Đếm mỗi tuần: % hồ sơ xem kỹ, % xem nhanh, thời gian trung bình mỗi loại, số lần người duyệt không đồng ý với hệ thống (theo mã quy tắc).
- **Bạn có sau bài:** bảng tuần. Nếu % xem kỹ quá cao so với sức người, giảm báo nhầm ở quy tắc gây nhiều nhất; **không** giảm bằng cách đổi `KHONG_RO` thành `DAT`.

### Bài K6.5: Hồ sơ kiểm người duyệt
- **Việc cần làm:** mỗi tháng đưa 2-3 hồ sơ cài lỗi vào hàng đợi với kết quả hệ thống bị đặt là `DAT`. Ghi người duyệt có phát hiện không. Thông báo trước với nhóm rằng có kiểm như vậy.
- **Lỗi hay gặp:** dùng kết quả để phạt (người duyệt sẽ xem mọi hồ sơ là đáng ngờ, hàng đợi ứ).

## 5. Đường không code vs có code; khi nào buộc chuyển

- **Không code:** bảng Excel hai sheet (đáp án, kết quả), `COUNTIFS` theo mã quy tắc (`COUNTIFS` là hàm Excel đếm số dòng thỏa nhiều điều kiện); khoảng Wilson tính bằng công thức (xem `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`).
- **Có code:** `cham.py` chạy sau mỗi lần sửa quy tắc, kết quả lưu theo phiên bản (nối với K7).
- **Buộc chuyển sang code khi [Đề xuất]:** hơn khoảng 10 quy tắc hoặc hơn 50 hồ sơ trong bộ cài lỗi; hoặc sửa quy tắc hơn một lần mỗi tháng.

!!! tip "Nói đơn giản"
    Ít quy tắc, ít hồ sơ thì Excel là đủ. Khi quy tắc và hồ sơ nhiều lên, hoặc bạn sửa quy tắc thường xuyên, hãy nhờ người biết code để máy chấm tự động sau mỗi lần sửa.

## 6. Tiêu chí lên K7 (đo được) [Đề xuất]

Bạn có thể sang K7 khi đạt đủ các điều sau:

1. Mọi quy tắc mức "cao" có ít nhất 5 ca lỗi + 5 ca đạt trong bộ cài lỗi.
2. Bỏ sót kết luận đạt = 0 trên bộ cài lỗi cho mọi quy tắc mức "cao" được phép "xem nhanh"; quy tắc nào chưa đạt thì luôn "xem kỹ".
3. Quy tắc chia hồ sơ đã chạy ít nhất 4 tuần, có số tải người duyệt.
4. Đã chạy K6.5 ít nhất một lần.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa; số giả định]

Hai tình huống giả định để bạn dễ hình dung:

**a) Công ty phân phối linh kiện điện tử, 300 hóa đơn đầu vào mỗi tháng.** Bộ cài lỗi 60 hồ sơ cho 9 quy tắc hóa đơn và 6 quy tắc ba bên. Sau K6.2: 13 quy tắc code không bỏ sót; quy tắc mờ "mô tả hàng phù hợp" có 1 bỏ sót trong 6 ca lỗi → luôn xem kỹ. Tuần đầu: 35% hồ sơ xem kỹ, phần lớn do `BB-05` (giao thiếu) báo nhầm khi phiếu nhập về chậm. Sửa: đợi 2 ngày sau ngày hóa đơn mới chạy `BB-05`.

**b) Trung tâm đào tạo lái xe, hồ sơ học viên.** Quy tắc: đủ giấy khám sức khỏe còn hạn, ảnh đúng quy cách, khớp họ tên giữa đơn và giấy tờ. Bộ cài lỗi: 20 hồ sơ, mỗi hồ sơ sửa một chỗ (đổi một chữ trong tên, ngày khám quá hạn). Kết quả giả định: quy tắc khớp tên báo nhầm khi tên có dấu khác kiểu gõ (NFC/NFD, hai cách máy tính lưu cùng một chữ có dấu, nhìn giống hệt nhau nhưng máy coi là khác) → sửa chuẩn hóa Unicode ở K1, không sửa quy tắc.

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
