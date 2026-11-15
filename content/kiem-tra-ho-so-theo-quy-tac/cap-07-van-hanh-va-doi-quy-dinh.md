# Cấp K7: Vận hành bộ quy tắc và xử lý khi quy định thay đổi

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung.
> Đã có, không viết lại: log mỗi lần gọi, phiên bản prompt, quy trình sửa → chạy lại → so sánh → phát hành, trôi dạt mô hình, chi phí, phân vai (`../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md`). File này viết phần riêng: **bộ quy tắc có ngày hiệu lực**, **cổng phát hành không thoái lui theo từng nhóm**, và **biến ý kiến người duyệt thành ca kiểm thử**.

!!! tip "Tóm tắt nhanh"
    Hệ thống kiểm hồ sơ chạy tốt hôm nay có thể sai vào tháng sau, vì quy định đổi, mẫu hóa đơn đổi hoặc mô hình AI đổi. Bài này chỉ cách giữ bộ quy tắc **có phiên bản và ngày hiệu lực**, chỉ cho một bản sửa được dùng khi nó **không làm xấu đi nhóm hồ sơ nào**, và biến mỗi lần người duyệt không đồng ý thành một **ca kiểm thử** giữ lại mãi. Sau bài, bạn có một quy trình rõ ràng để xử lý khi văn bản pháp luật hoặc quy chế nội bộ thay đổi, và sáu tháng sau vẫn giải thích được vì sao một hồ sơ đã được duyệt.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người chịu trách nhiệm hệ thống kiểm (kế toán trưởng, người biết code nhẹ) và chủ doanh nghiệp. Phần lớn bài làm được bằng bảng tính Excel, chỉ một phần nhỏ cần nhờ người biết code.

**Bạn cần chuẩn bị:** bài này tiếp nối các cấp trước, nên bạn nên có sẵn những thứ mà nội dung bài nhắc tới:
- Sổ quy tắc của hệ thống kiểm (mỗi quy tắc một dòng).
- Bộ cài lỗi (bộ hồ sơ có lỗi cố ý để thử hệ thống, từ cấp K6, xem K6.1) và chỗ ghi ý kiến không đồng ý của người duyệt (xem K2.5).
- Các văn bản pháp luật và quy chế nội bộ mà quy tắc dựa vào (ví dụ thuế, lao động, dữ liệu cá nhân).

**Sau bài này bạn sẽ có:**
1. Sổ quy tắc có **phiên bản** và **ngày hiệu lực** cho từng quy tắc; mỗi hồ sơ biết đã kiểm bằng phiên bản nào.
2. **Cổng phát hành:** bản sửa chỉ được dùng khi không nhóm hồ sơ nào xấu đi và mọi ca đã sửa trước đây vẫn đúng.
3. **Kho ca đã sửa:** mỗi lần người duyệt không đồng ý với hệ thống thành một ca kiểm thử.
4. Quy trình khi văn bản pháp luật hoặc quy chế nội bộ đổi.

**Thứ bạn cầm đi được sau bài:** `so quy tac` có cột phiên bản và hiệu lực; file `kho_ca_da_sua.csv`; `cong.py` (đoạn chương trình ngắn làm "cổng phát hành"); file `nhat_ky_thay_doi_quy_dinh.md`.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Quy định đổi, nhà cung cấp đổi mẫu hóa đơn, mô hình AI đổi. Làm sao sửa hệ thống mà không làm hỏng cái đang chạy, và sáu tháng sau vẫn giải thích được vì sao một hồ sơ đã được duyệt?"*

Các cấp trước giúp hệ thống chạy được. Cấp này lo chuyện khó hơn: giữ cho nó chạy **đúng theo thời gian**.

Ví dụ thật: theo các nguồn thứ cấp (tức là các trang tóm tắt, không phải văn bản gốc), NĐ 254/2026/NĐ-CP có hiệu lực từ 01/7/2026, thay NĐ 123/2020/NĐ-CP và NĐ 70/2025/NĐ-CP; TT 91/2026/TT-BTC thay TT 32/2025/TT-BTC; có thay đổi về thời điểm lập hóa đơn, nội dung hóa đơn với người mua là người tiêu dùng, trường hợp không phải lập hóa đơn **[Nguồn: V1, đọc qua tóm tắt]**. Một bộ quy tắc viết năm 2025 có thể sai từ tháng 7/2026 mà không ai biết.

!!! tip "Nói đơn giản"
    Quy tắc kiểm hồ sơ giống như bảng giá niêm yết: khi giá đổi mà bảng không đổi, mọi hóa đơn sau đó đều sai mà nhìn bề ngoài vẫn bình thường. Vì vậy mỗi quy tắc phải ghi rõ "áp dụng từ ngày nào" và "dựa trên văn bản nào".

## 3. Kiến thức nền

### 3.1 Bài học từ ESCROW (BMO) cho việc sửa bộ quy tắc

ESCROW là tên một nghiên cứu (của BMO) về cách sửa dần bộ quy tắc cho hệ thống AI. Dưới đây là những điều đáng học từ nghiên cứu này.

- **Chỉ sửa chỉ dẫn, không đụng vào mô hình.** Mô hình giữ nguyên; chỉ sửa "skill" (bộ chỉ dẫn viết bằng ngôn ngữ thường). LLM (mô hình ngôn ngữ lớn, tức AI biết đọc và viết văn bản) đề xuất bản sửa; **chỉ bản đã được chấm trên ca thật mới được triển khai**; mỗi thay đổi là một bản khác biệt (diff, tức bản so sánh cho thấy chỗ nào thêm, bỏ, sửa) đọc được, có phiên bản **[Nguồn: B1]**.
- **Cổng không thoái lui theo nhóm.** Bản sửa phải giữ mức của từng nhóm ca (trong cấu hình mặc định, dung sai 5% tương đối mỗi nhóm), vì tổng có thể tăng trong khi một nhóm giảm **[Nguồn: B1, mục 1 và bảng 3]**. "Dung sai" là mức tụt tối đa mà cổng còn chấp nhận.
- **Chống lặp lại lỗi cũ.** Các ca đã sửa được giữ trong một kho; mỗi bản sửa mới phải chạy lại trên kho này. Không có kho, điểm trên ca cũ tụt từ 0,857 xuống 0,7 qua 4 vòng; có kho, giữ khoảng 0,84 **[Nguồn: `../nen-tang-bang-chung.md` mục 1.4]**.
- **Nguồn ý kiến.** Ghi chú của người duyệt, phân tích log (nhật ký ghi lại mỗi lần hệ thống chạy), và khác biệt khi chính sách cập nhật; mỗi ý kiến được chuyển thành một ca có cấu trúc gồm mô tả lỗi và đầu ra đúng **[Nguồn: B1, phụ lục E]**.
- **Chi phí.** Chấm lại toàn bộ ca là phần tốn nhất, nên vòng lặp chỉ xử lý được vài trăm ca **[Nguồn: B1, hạn chế]**. **[Đề xuất]** Với SME, đây là lý do giữ đa số quy tắc bằng code: chạy lại hàng trăm ca bằng code mất vài giây và không tốn tiền.

!!! tip "Nói đơn giản"
    Có ba ý cần nhớ. Một: chỉ dùng bản sửa khi đã thử trên ca thật. Hai: đừng nhìn điểm tổng, hãy nhìn từng nhóm (hóa đơn, hợp đồng...), vì tổng có thể tăng trong khi một nhóm âm thầm xấu đi. Ba: giữ lại mọi ca đã từng sửa và thử lại chúng sau mỗi lần đổi, để lỗi cũ không quay lại.

### 3.2 Trích quy tắc một lần, dùng đến khi chính sách đổi

- Ca Erste: bộ quy tắc trích từ chính sách được dùng lại cho mọi hồ sơ **cho đến khi hướng dẫn cập nhật phiên bản mới**; chuyên gia xem và sửa được bộ quy tắc trước khi dùng **[Nguồn: B5]**.

!!! tip "Nói đơn giản"
    Không cần bắt AI đọc lại cả chính sách cho mỗi hồ sơ. Đọc một lần, rút ra bộ quy tắc, để chuyên gia xem lại, rồi dùng đi dùng lại cho tới khi chính sách có bản mới.

### 3.3 Ghi đủ cấu hình để tái hiện

- B6: cùng tên mô hình có thể cho kết quả khác qua hai đường gọi khác nhau; kết quả có thể đổi giữa các ngày dưới cùng tên mô hình; bản ghi chỉ ghi tên mô hình thì không xác định được cái gì đã được kiểm định **[Nguồn: B6]**. Đổi loại GPU (card đồ họa dùng để chạy mô hình) cũng làm 34/776 nhãn thay đổi trong hệ thống tự chạy của họ **[Nguồn: B6]**.
- **[Đề xuất]** SME không cần tái hiện từng byte (tức giống hệt đến từng ký tự). Cần: lưu đầu ra đã dùng để kết luận (K3.4); ghi tên mô hình, đường gọi (API trực tiếp hay qua nền tảng nào; API là cổng để chương trình của bạn gọi dịch vụ AI), phiên bản prompt (câu lệnh đưa cho AI), phiên bản sổ quy tắc, ngày. Khi nhà cung cấp ngừng mô hình, chạy lại bộ cài lỗi trên mô hình mới trước khi chuyển (theo `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` bài 9.4).

!!! tip "Nói đơn giản"
    Ghi "dùng ChatGPT" hay "dùng Claude" là chưa đủ. Mỗi lần kiểm, hãy ghi thêm mô hình nào, gọi qua đường nào, prompt bản nào, sổ quy tắc bản nào, ngày nào. Có vậy sau này bạn mới biết kết luận đó đến từ đâu.

## 4. Chuỗi bài nhỏ

Năm bài dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và (nếu có) lỗi hay gặp để tránh.

### Bài K7.1: Ngày hiệu lực cho từng quy tắc
- **Việc cần làm:** thêm vào sổ quy tắc bốn cột: `phien_ban`, `hieu_luc_tu`, `hieu_luc_den`, `can_cu` (số văn bản, điều, khoản). Bộ chạy chọn quy tắc theo **ngày của chứng từ** (ngày lập hóa đơn, ngày ký hợp đồng), không theo ngày chạy. Nói cách khác, hồ sơ lập năm ngoái vẫn phải kiểm theo quy tắc của năm ngoái, dù hôm nay bạn mới chạy kiểm.
- **Lưu ý:** với hóa đơn lập trước 01/7/2026 nhưng điều chỉnh, thay thế sau ngày này, một nguồn thứ cấp cho biết việc điều chỉnh, thay thế làm theo NĐ 254 và TT 91 **[Nguồn: V2, thứ cấp]**. Quy tắc "ngày nào áp quy định nào" phải do người có chuyên môn viết sau khi đọc văn bản gốc.
- **Bạn có sau bài:** sổ quy tắc có cột hiệu lực; báo cáo mỗi hồ sơ ghi `phien_ban_so_quy_tac`.
- **Lỗi hay gặp:** sửa thẳng quy tắc cũ (mất khả năng giải thích hồ sơ đã kiểm trước đó).

### Bài K7.2: Kho ca đã sửa từ ý kiến người duyệt
- **Việc cần làm:**
  1. Mỗi lần người duyệt không đồng ý (K2.5), ghi lại năm thứ: mã hồ sơ, mã quy tắc, hệ thống nói gì, đúng phải là gì, lý do.
  2. Hằng tuần, người vận hành chuyển các dòng này thành ca trong bộ cài lỗi (K6.1).
  3. Gắn nhãn nhóm cho mỗi ca (ví dụ: `hoa_don`, `ba_ben`, `hop_dong`, `ho_so_ns`).
- **Bạn có sau bài:** `kho_ca_da_sua.csv` (CSV là kiểu file bảng đơn giản, mở được bằng Excel); ca đã vào kho không xóa.

!!! tip "Nói đơn giản"
    Mỗi lần người duyệt nói "hệ thống làm sai chỗ này", đó là một bài học miễn phí. Hãy ghi nó thành một ca kiểm thử và giữ mãi, để sau này mọi bản sửa đều phải qua được ca đó.

### Bài K7.3: Cổng phát hành theo nhóm
- **Việc cần làm:** trước mỗi lần đổi sổ quy tắc, đổi prompt hoặc đổi mô hình, chạy "cổng" này để quyết định có cho dùng bản mới hay không.

  **Đoạn mã dưới đây làm gì?** Nó so kết quả của bản cũ và bản mới trên cùng bộ ca. Với từng nhóm ca (hóa đơn, hợp đồng...), nó kiểm tra tỷ lệ đúng của bản mới có tụt so với bản cũ không. Nó cũng kiểm tra những ca nằm trong kho ca đã sửa có còn đúng không. Nếu một nhóm tụt hoặc một ca đã sửa bị hỏng lại, cổng trả `TU_CHOI` kèm lý do; nếu không, trả `NHAN`. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp.

  **Mã mẫu (đã chạy thử** 2026-11-11, `python -I -X utf8`, dữ liệu giả):

  ```python
  def cong(cu, moi, kho_ca_da_sua, dung_sai=0.0):
      """cu/moi: {ma_ca: (nhom, dung_bool)}; kho_ca_da_sua: tap ma_ca phai luon dung."""
      ly_do = []
      for n in sorted({g for g, _ in cu.values()}):
          a = [d for k, (g, d) in cu.items() if g == n]
          b = [moi[k][1] for k, (g, _) in cu.items() if g == n]
          ra, rb = sum(a)/len(a), sum(b)/len(b)
          if rb < ra - dung_sai: ly_do.append(f"nhom {n} tut {ra:.0%} -> {rb:.0%}")
      hong = [k for k in kho_ca_da_sua if not moi[k][1]]
      if hong: ly_do.append(f"ca da sua bi hong lai: {hong}")
      return ("NHAN", []) if not ly_do else ("TU_CHOI", ly_do)
  ```

**Kết quả thử:** có hai bản sửa.
- Bản sửa thứ nhất làm đúng thêm một ca hợp đồng, không làm sai ca nào. Cổng trả `NHAN`.
- Bản sửa thứ hai cũng làm đúng thêm ca hợp đồng nhưng làm sai một ca hóa đơn. Tổng vẫn 75% như cũ, nhưng cổng trả `TU_CHOI` với lý do `nhom hoa_don tut 100% -> 50%` và `ca da sua bi hong lai: ['c2']`.

!!! tip "Nói đơn giản"
    Ví dụ trên cho thấy vì sao phải nhìn từng nhóm: hai bản sửa có điểm tổng giống nhau, nhưng một bản làm hỏng nhóm hóa đơn mà nhìn tổng thì không thấy. Cổng bắt được điều đó.

- **[Đề xuất]** Dung sai mặc định 0 cho quy tắc mức "cao" (ESCROW dùng 5% tương đối, nhưng với vài chục ca của SME, một ca đã vượt 5%).
- **Bạn có sau bài:** `cong.py` chạy trước mỗi lần đổi sổ quy tắc, prompt, hoặc mô hình.

### Bài K7.4: Quy trình khi quy định hoặc quy chế đổi
- **Việc cần làm [Đề xuất]:**
  1. Một người được giao theo dõi văn bản (thuế, lao động, dữ liệu cá nhân) và quy chế nội bộ; mỗi tháng ghi "có gì mới".
  2. Khi có văn bản mới: liệt kê quy tắc bị ảnh hưởng (tìm theo cột `can_cu`).
  3. Viết phiên bản mới của quy tắc với `hieu_luc_tu`; giữ phiên bản cũ.
  4. Thêm ca cài lỗi cho điểm mới (ví dụ quy tắc mới về nội dung hóa đơn).
  5. Chạy cổng K7.3. Người có thẩm quyền ký phát hành.
- Có thể dùng LLM để **đề xuất** danh sách quy tắc bị ảnh hưởng từ bản so sánh văn bản cũ/mới (như bước trích quy tắc của Erste), nhưng người duyệt mọi thay đổi **[Đề xuất, dựa trên B5]**.
- **Bạn có sau bài:** `nhat_ky_thay_doi_quy_dinh.md`.

### Bài K7.5: Lưu trữ và giải thích lại
- **Việc cần làm:** với mỗi hồ sơ đã kết luận, lưu các thứ sau:
  1. Chứng từ gốc (hoặc đường dẫn kèm hash SHA-256, tức một "dấu vân tay" của file để biết file có bị sửa không; cách làm ở `../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` bài 2.5).
  2. JSON đã trích (JSON là cách viết dữ liệu có khung rõ ràng để máy đọc được).
  3. Báo cáo.
  4. Phiên bản sổ quy tắc.
  5. Log lời gọi LLM.
  6. Người duyệt và quyết định.
- Thử mỗi quý: chọn ngẫu nhiên 3 hồ sơ cũ, giải thích lại vì sao được duyệt chỉ từ dữ liệu đã lưu.
- **Lưu ý:** thời hạn lưu trữ chứng từ kế toán, hóa đơn theo pháp luật: chưa tra trong phiên này; hỏi kế toán trưởng hoặc tư vấn. Bài này không phải tư vấn pháp lý.
- **Bạn có sau bài:** một nếp lưu trữ đủ để giải thích lại từng hồ sơ cũ.

## 5. Đường không code vs có code; khi nào buộc chuyển

- **Không code:** sổ quy tắc là file Excel có cột phiên bản và hiệu lực, lưu mỗi phiên bản thành file riêng; bộ cài lỗi chạy tay khi đổi; nhật ký thay đổi là một tài liệu.
- **Có code:** sổ quy tắc trong Git (công cụ lưu lịch sử mọi lần sửa file); `cham.py` + `cong.py` chạy tự động khi có thay đổi.
- **Buộc chuyển sang code khi [Đề xuất]:** sổ quy tắc đổi hơn một lần mỗi quý; hoặc có quy tắc mờ dùng LLM (vì mô hình đổi mà không báo); hoặc hơn một người sửa sổ.

!!! tip "Nói đơn giản"
    Mới bắt đầu, Excel và vài file lưu riêng là đủ. Khi sổ quy tắc đổi thường xuyên, có nhiều người cùng sửa, hoặc có quy tắc phải nhờ AI phán đoán, hãy nhờ người biết code dựng phần tự động.

## 6. Tiêu chí "vận hành được" (đo được) [Đề xuất]

1. Mọi quy tắc có phiên bản, hiệu lực, căn cứ; mọi báo cáo ghi phiên bản sổ quy tắc.
2. Kho ca đã sửa có ít nhất 20 ca sau 3 tháng (nếu ít hơn, hoặc hệ thống rất tốt, hoặc người duyệt không ghi ý kiến: kiểm bằng K6.5).
3. Mọi thay đổi trong 3 tháng đều qua cổng K7.3 và có người ký.
4. Đã xử lý ít nhất một thay đổi quy định theo K7.4 (NĐ 254/2026 là ứng viên ngay).
5. Thử giải thích lại 3 hồ sơ cũ thành công.

Khi nào **dừng** hoặc **thu hẹp**: lỗi lọt sau duyệt nhiều hơn làm tay; người duyệt không theo kịp hàng đợi trong 4 tuần liền; hoặc không ai theo dõi thay đổi quy định.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung:

**a) Văn phòng dịch vụ kế toán (tiếp ví dụ `cap-02`).** Tháng 7/2026: người theo dõi văn bản ghi NĐ 254/2026 và TT 91/2026 có hiệu lực. Danh sách quy tắc có `can_cu` chứa "NĐ 123" hoặc "NĐ 70": 4 quy tắc. Kế toán trưởng đọc văn bản gốc, viết phiên bản mới cho 2 quy tắc, giữ 2 quy tắc không đổi nhưng cập nhật căn cứ. Thêm 6 ca cài lỗi. Cổng K7.3 nhận. Hóa đơn lập trước 01/7 vẫn kiểm bằng phiên bản cũ.

**b) Công ty thương mại dùng LLM cho quy tắc "mô tả hàng phù hợp".** Nhà cung cấp API thông báo ngừng mô hình đang dùng. Người vận hành chạy bộ cài lỗi trên mô hình mới 3 lần (K6.3): nhóm `hoa_don` giữ nguyên, một ca trong kho ca đã sửa bị sai lại. Cổng từ chối. Sửa câu hỏi của quy tắc (thêm một ví dụ lỗi), chạy lại, cổng nhận, rồi mới chuyển.

**c) Công ty xây dựng sửa quy chế tạm ứng.** Hạn mức theo chức danh đổi từ 01/1. Chỉ sửa bảng hạn mức có cột hiệu lực; quy tắc `TU-01` không đổi code. Hồ sơ tạm ứng tháng 12 vẫn kiểm theo hạn mức cũ.

## 8. Tài liệu tham khảo

| Mã | Nguồn | Tin cậy |
|---|---|---|
| B1 | Shu et al., ESCROW, BMO, arXiv 2608.01772. https://www.alphaxiv.org/abs/2608.01772 | Trung bình-cao; không công bố mã, dữ liệu |
| B5 | Voboril, Erste Bank, arXiv 2610.20155 | Trung bình |
| B6 | Suzuki, arXiv 2610.21300 | Trung bình |
| V1 | EY, NĐ 254/2026/NĐ-CP. https://www.ey.com/vi_vn/technical/tax/tax-and-law-updates/nghi-dinh-254-2026-nd-cp-ve-hoa-don-dien-tu-va-chung-tu-dien-tu | Trung bình-cao; đọc qua tóm tắt |
| V2 | Kết quả tìm kiếm về NĐ 254/2026 (thuvienphapluat.vn, luatvietnam.vn bảng so sánh, ketoanleanh.edu.vn). https://luatvietnam.vn/thue-phi-le-phi/bang-so-sanh-nghi-dinh-254-2026-va-nghi-dinh-123-2020-nd-cp-nd-cp-ve-hoa-don-chung-tu-dien-tu-565-110463-article.html | Thấp-trung bình; các nguồn chưa thống nhất chi tiết |
| R9 | Nhóm RAG, vận hành | `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` |

## 9. Chưa kiểm chứng

- **NĐ 254/2026/NĐ-CP, TT 91/2026/TT-BTC:** chưa đọc văn bản gốc. Các nguồn thứ cấp chưa thống nhất NĐ 70/2025 và Điều 1 NĐ 41/2022 bị bãi bỏ toàn bộ hay một phần; quy định chuyển tiếp (ví dụ biên lai giấy dùng đến 31/12/2026) chỉ thấy ở một nguồn.
- Một kết quả tìm kiếm khác nhắc dự thảo nghị định thay NĐ 123 và NĐ 70 được công bố 21/4/2026; có thể đó là dự thảo của NĐ 254, chưa kiểm.
- Thời hạn lưu trữ chứng từ, hóa đơn: chưa tra.
- Các con số "20 ca sau 3 tháng", "3 hồ sơ mỗi quý", dung sai 0 là đề xuất.
- Hiệu quả của cổng không thoái lui ở quy mô vài chục ca (SME) chưa ai đo; ESCROW đo với 210 ca mỗi tập.
