# Cấp K5: Hợp đồng so với mẫu chuẩn; hồ sơ nhân sự và CV

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như quy ước chung. Không phải tư vấn pháp lý.
> Đã có, không viết lại: chia văn bản theo tiêu đề, mã ổn định (`../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md`); dữ liệu cá nhân và pháp luật VN (`../an-toan-du-lieu-va-phap-ly-vn.md`).

## 1. Mục tiêu và người đọc

**Người đọc:** hành chính nhân sự, người phụ trách hợp đồng ở SME (thường là giám đốc hoặc kế toán trưởng), người code nhẹ.

**Sau cấp này có:**
1. Với hợp đồng **theo mẫu của mình**: script so từng điều với mẫu chuẩn, chỉ ra điều thiếu, điều bị sửa (kèm phần chữ khác), điều mới thêm. Không dùng LLM.
2. Với hợp đồng **do bên kia soạn**: danh sách điều khoản bắt buộc / điều khoản cần cảnh giác, kiểm bằng K3, có bước tìm câu nhắm vào AI.
3. Với hồ sơ nhân sự: checklist đủ giấy tờ và kiểm khớp thông tin giữa các giấy tờ; quy tắc dữ liệu cá nhân rõ ràng.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Hợp đồng không phải bảng số. Kiểm thế nào cho có căn cứ, khi phần lớn rủi ro nằm ở câu chữ?"*

Lỗi nếu dùng K3 cho mọi thứ: đưa cả hợp đồng cho LLM hỏi "có vấn đề gì không?". Bằng chứng ở mục 3 cho thấy LLM bỏ sót đáng kể kể cả với mô hình mạnh nhất. Trong khi đó, phần lớn hợp đồng của SME là **mẫu của chính mình**, so được bằng code.

## 3. Kiến thức nền

### 3.1 Hai loại việc khác nhau [Đề xuất]

| | Hợp đồng theo mẫu của mình | Hợp đồng do bên kia soạn |
|---|---|---|
| Ví dụ | Hợp đồng lao động, hợp đồng bán hàng mẫu, phụ lục giá | Hợp đồng khách lớn gửi, hợp đồng thuê mặt bằng |
| Câu hỏi | Có đúng mẫu không, đã sửa chỗ nào | Có đủ điều khoản cần có không, có điều khoản bất lợi không |
| Cách làm | So văn bản bằng code | Checklist điều khoản + K3 + người đọc phần được trích |
| Rủi ro injection | Thấp (mình soạn) | Có (bên kia soạn) |

### 3.2 Bằng chứng về LLM rà hợp đồng
- **ContractScrub** (Thomson Reuters): 44 hợp đồng từ CUAD, 3.014 lỗi do 9 luật sư có ít nhất 8 năm kinh nghiệm gắn nhãn, 9 loại lỗi soạn thảo. Mô hình tốt nhất bắt 75% (recall trung bình theo loại); F1 cao nhất 0,655 **[Nguồn: B7]**. Loại có dấu hiệu từ vựng rõ (thuật ngữ được định nghĩa) recall trung bình 0,835; loại cần hiểu ý trong ngữ cảnh thấp hơn nhiều: thuật ngữ viết hoa nhưng không được định nghĩa 0,351, **gọi nhầm bên** 0,362, viết hoa sai ngữ cảnh 0,427 **[Nguồn: B7]**. Chi phí 0,13-1,52 USD mỗi hợp đồng với các mô hình mạnh; thời gian 23 giây đến gần 9 phút **[Nguồn: B7, bảng 2]**. Hạn chế: hợp đồng tiếng Anh, 10-15 trang.
- **CUAD** (2021): 510 hợp đồng, 41 loại điều khoản, 13.101 đoạn được gắn nhãn; tác giả ước giá trị gắn nhãn trên 2 triệu USD. Mô hình tốt nhất thời đó (DeBERTa-xlarge, đã huấn luyện riêng) chỉ đạt độ chính xác 44,0% khi tìm được 80% điều khoản, 17,8% khi tìm được 90% **[Nguồn: B9]**. Tác giả nhấn mạnh recall quan trọng hơn precision vì đây là việc "mò kim đáy bể" **[Nguồn: B9]**. Số này đã cũ, chỉ dùng để hiểu vì sao đo recall.
- **[Đề xuất] Rút ra:** (a) "gọi nhầm bên" là lỗi khó cho LLM; hợp đồng Việt Nam dùng "Bên A", "Bên B" dày đặc, nên cần người đọc; (b) phần kiểm được bằng code (điều có/không, số tiền, ngày, so với mẫu) nên làm bằng code; (c) phần còn lại, LLM là người đọc lượt đầu, không phải người kết luận.

### 3.3 Hợp đồng lao động: nội dung chủ yếu
- Điều 21 Bộ luật Lao động 2019 (Luật 45/2019/QH14) liệt kê các nội dung chủ yếu của hợp đồng lao động. Theo bản tóm lược từ hethongphapluat.com gồm: thông tin người sử dụng lao động và người ký; thông tin người lao động; công việc và địa điểm làm việc; thời hạn hợp đồng; mức lương, hình thức và kỳ hạn trả lương, phụ cấp, khoản bổ sung; chế độ nâng bậc, nâng lương; thời giờ làm việc, nghỉ ngơi; trang bị bảo hộ lao động; bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp; đào tạo, bồi dưỡng, nâng cao kỹ năng nghề. Hướng dẫn chi tiết ở Thông tư 10/2020/TT-BLĐTBXH **[Nguồn: V6, V7; thứ cấp, chưa đọc văn bản gốc]**.
- **[Đề xuất]** Mười nội dung này là một checklist "có/không" tự nhiên. Nếu dùng mẫu hợp đồng của công ty, kiểm một lần trên mẫu (người có chuyên môn), sau đó chỉ cần so từng hợp đồng với mẫu.

### 3.4 Hồ sơ nhân sự, CV: dữ liệu cá nhân là rủi ro chính
- Theo tóm tắt của EY về NĐ 356/2025, ảnh giấy tờ tùy thân và lịch sử giao dịch ngân hàng nằm trong nhóm dữ liệu nhạy cảm **[Nguồn: `../an-toan-du-lieu-va-phap-ly-vn.md` mục 4.2, dẫn EY]**. Bộ hồ sơ nhân sự thường có ảnh CCCD, số tài khoản, giấy khám sức khỏe.
- CV do ứng viên soạn: nghiên cứu về prompt injection đã có các đánh giá riêng trên CV **[Nguồn: B8, phần tổng quan, dẫn Zhang et al. 2026 và Augey et al. 2026; chưa đọc hai bài này]**.
- **[Đề xuất]** Ở cấp này AI chỉ làm: trích thông tin có cấu trúc (K1), kiểm đủ giấy tờ, kiểm khớp thông tin giữa giấy tờ. **Không** để AI chấm điểm, xếp hạng hay loại ứng viên. Quyết định tuyển dụng ảnh hưởng tới con người; trách nhiệm và rủi ro thiên lệch cần tư vấn riêng.

## 4. Chuỗi bài nhỏ

### Bài K5.1: So hợp đồng với mẫu chuẩn bằng code
- **Làm:** lưu mẫu chuẩn (Word → text). Tách theo "Điều N." Với mỗi hợp đồng: điều bắt buộc có không; điều có trong mẫu thì chữ có giống mẫu không; điều nào không có trong mẫu.
- **Mã mẫu (đã chạy thử** 2026-11-11, `python -I -X utf8`, hợp đồng giả):
  ```python
  import re, difflib, unicodedata
  def chuan(s): return unicodedata.normalize("NFC", " ".join(s.split())).lower()
  def tach_dieu(text):
      phan = re.split(r"(?m)^(Điều\s+\d+\.?\s*[^\n]*)$", text)
      out = {}
      for i in range(1, len(phan), 2):
          ten = re.sub(r"^Điều\s+\d+\.?\s*", "", phan[i]).strip()
          out[chuan(ten)] = {"tieu_de": phan[i].strip(), "noi_dung": phan[i + 1].strip()}
      return out
  def so_mau(mau, hd, bat_buoc):
      m, h = tach_dieu(mau), tach_dieu(hd)
      kq = []
      for ten in bat_buoc:
          k = chuan(ten)
          if k not in h: kq.append(("THIEU", ten, "")); continue
          if k in m and chuan(m[k]["noi_dung"]) != chuan(h[k]["noi_dung"]):
              diff = [x for x in difflib.ndiff(m[k]["noi_dung"].split(), h[k]["noi_dung"].split())
                      if x[0] in "+-"]
              kq.append(("KHAC_MAU", h[k]["tieu_de"], " ".join(diff)))
      for k in h:
          if k not in m: kq.append(("DIEU_MOI", h[k]["tieu_de"], "khong co trong mau"))
      return kq
  ```
  Kết quả thử: mẫu có 4 điều; hợp đồng đổi ngày trả lương từ "ngày 5" thành "ngày 15", bỏ điều Bảo hiểm, thêm điều "Cam kết không cạnh tranh 24 tháng". Kết quả: `KHAC_MAU Điều 3. Mức lương: - 5 + 15`, `THIEU Bảo hiểm`, `DIEU_MOI Điều 5. Cam kết không cạnh tranh`.
- **Bài học từ lần chạy:** bản chạy thử cũng in tỷ lệ giống của Điều 3: **99%**. Sửa một con số chỉ làm tỷ lệ giảm 1%. **Không dùng ngưỡng tỷ lệ giống** để quyết định "gần đúng mẫu"; mọi khác biệt phải hiện phần chữ khác cho người đọc.
- **Sản phẩm:** `so_mau.py`; báo cáo mỗi hợp đồng một trang.
- **Lỗi:** mẫu chuẩn không có phiên bản (không biết so với mẫu nào); đánh số lại điều làm khóa đổi (vì vậy khóa là **tên điều**, không phải số điều); tiêu đề điều viết khác mẫu một chữ là bị coi là điều mới (ghi rõ trong báo cáo để người xem).

### Bài K5.2: Checklist điều khoản cho hợp đồng do bên kia soạn
- **Làm:** viết 8-15 câu hỏi hẹp theo khuôn K3.1. Gợi ý nhóm [Đề xuất]: thời hạn và gia hạn tự động; điều kiện đơn phương chấm dứt; mức phạt và trần phạt; trần trách nhiệm bồi thường; điều kiện thanh toán và lãi chậm trả; luật áp dụng, nơi giải quyết tranh chấp; chuyển giao hợp đồng cho bên thứ ba; độc quyền, không cạnh tranh.
- Mỗi câu trả về `DAT/LOI/KHONG_RO` + trích dẫn kiểm bằng code (K3.2). Chạy bước tìm câu lạ (K3.5) trước.
- **Sản phẩm:** `checklist_hd_doi_tac.md` + báo cáo mỗi hợp đồng: mỗi câu hỏi một dòng, kèm đoạn trích để giám đốc đọc.
- **Lỗi:** hỏi "điều khoản này có bất lợi không?" (không định nghĩa được "bất lợi"); để LLM tóm tắt hợp đồng thay vì trả lời từng câu.

### Bài K5.3: Kiểm nhất quán trong một hợp đồng bằng code
- **Làm:** những việc code làm được trước khi gọi LLM: (a) mọi "Điều N" được dẫn chiếu trong văn bản có tồn tại không; (b) mọi "Phụ lục X" được nhắc có đính kèm không; (c) tên, MST, địa chỉ các bên ở phần đầu khớp với khối chữ ký và với danh mục khách/nhà cung cấp; (d) số tiền viết bằng số và bằng chữ khớp nhau (cần hàm đọc số tiếng Việt; **chưa viết**).
- **Vì sao:** "dẫn chiếu sai điều, sai mục" là một loại lỗi của ContractScrub; mô hình tốt nhất bắt khoảng 0,67-0,80 **[Nguồn: B7, bảng 3]**. Dẫn chiếu tới điều không tồn tại thì regex bắt được hoàn toàn. **[Đề xuất]**

### Bài K5.4: Checklist hồ sơ nhân sự
- **Làm:** danh sách giấy tờ theo quy chế công ty (ví dụ: sơ yếu lý lịch, bản sao giấy tờ tùy thân, bằng cấp, giấy khám sức khỏe, hợp đồng lao động đã ký, tờ khai thông tin thuế, BHXH). Mỗi mục: có/không, còn hạn không (giấy khám sức khỏe), người kiểm.
- Kiểm khớp bằng code sau K1: họ tên, ngày sinh giữa các giấy tờ (so sau chuẩn hóa dấu); chức danh và mức lương trên hợp đồng khớp quyết định tuyển dụng.
- **Dữ liệu:** ảnh CCCD **không** gửi lên dịch vụ AI ngoài. Người nhập tay số giấy tờ, hoặc dùng công cụ chạy trên máy (xem `../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` bài 2.9).
- **Sản phẩm:** `checklist_ho_so_ns.xlsx` + `kiem_khop_ns.py`.

### Bài K5.5: Trích CV thành bảng, không xếp hạng
- **Làm:** trích các trường trong tin tuyển dụng yêu cầu (bằng cấp, chứng chỉ, số năm kinh nghiệm, kỹ năng) kèm vị trí trong CV. Quy tắc xác định (có chứng chỉ X không) chạy bằng code trên bảng trích. Người tuyển dụng đọc CV gốc cho mọi ứng viên đi tiếp và mọi ứng viên bị loại vì một quy tắc.
- Che họ tên, ảnh, ngày sinh, địa chỉ, số điện thoại trước khi gửi cho LLM; giữ bảng tra ngược trên máy công ty.
- **Lỗi:** dùng "điểm phù hợp" do LLM cho để loại người; không báo cho ứng viên về việc xử lý dữ liệu (cần tư vấn theo Luật 91/2025 và NĐ 356/2025).

## 5. Đường không code vs có code; khi nào buộc chuyển

| Việc | Không code | Có code |
|---|---|---|
| So với mẫu | Word: Review → Compare với mẫu chuẩn | `so_mau.py` hàng loạt |
| Hợp đồng đối tác | Project có checklist; người Ctrl+F kiểm trích dẫn | K3 + K5.2 tự động |
| Hồ sơ nhân sự | Excel checklist | `kiem_khop_ns.py` |

Tính năng so sánh văn bản của Word là cách không code tốt cho K5.1 **[Đề xuất; tên menu có thể khác theo phiên bản, chưa kiểm]**.
**Buộc chuyển sang code khi [Đề xuất]:** hơn khoảng 10 hợp đồng mẫu mỗi tháng; hoặc nhiều mẫu và nhiều phiên bản mẫu; hoặc cần lưu vết ai duyệt khác mẫu.

## 6. Tiêu chí lên K6 (đo được) [Đề xuất]

1. Mỗi mẫu hợp đồng có phiên bản, ngày hiệu lực, người duyệt nội dung pháp lý.
2. K5.1 chạy trên 10 hợp đồng đã ký: mọi khác biệt so với mẫu được liệt kê, người xác nhận từng khác biệt là chấp nhận hay không.
3. K5.2 có ít nhất 8 câu hỏi, mỗi câu 10 ca mẫu, đo theo `cap-06`.
4. Bộ hồ sơ nhân sự: 0 lần gửi ảnh giấy tờ tùy thân ra dịch vụ ngoài (kiểm bằng log).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

**a) Chuỗi nhà thuốc 8 điểm, 40 nhân viên.** Hợp đồng lao động theo 2 mẫu (dược sĩ, nhân viên bán hàng). K5.1 so từng hợp đồng mới với mẫu; khác biệt thường gặp là mức lương và địa điểm, đều được duyệt theo quyết định tuyển dụng (code so số với quyết định). Hồ sơ nhân sự: K5.4 kiểm đủ chứng chỉ hành nghề cho vị trí dược sĩ (có/không, người kiểm bản gốc).

**b) Công ty cho thuê thiết bị sự kiện.** Khách doanh nghiệp lớn gửi hợp đồng theo mẫu của họ. K5.2 với 10 câu hỏi; câu "trần trách nhiệm bồi thường" thường ra `KHONG_RO` vì hợp đồng dẫn sang "điều khoản chung" đính kèm riêng. Đó là tín hiệu đúng: xin phụ lục trước khi ký.

**c) Công ty logistics nhỏ thuê kho.** Hợp đồng thuê kho do chủ kho soạn, 20 trang. Trước K3: K5.3 bắt hai dẫn chiếu tới "Điều 14.3" không tồn tại và một "Phụ lục 2" không đính kèm. Không cần LLM cho phát hiện này.

## 8. Tài liệu tham khảo

| Mã | Nguồn | Tin cậy |
|---|---|---|
| B7 | Bang et al., ContractScrub, arXiv 2608.20204. https://www.alphaxiv.org/abs/2608.20204 | Trung bình-cao |
| B9 | Hendrycks et al., CUAD, NeurIPS 2021, arXiv 2103.06268. https://www.alphaxiv.org/abs/2103.06268 | Cao cho bộ dữ liệu; số mô hình đã cũ |
| B8 | Heimann et al., arXiv 2611.08834 | Trung bình |
| V6 | hethongphapluat.com, Bộ luật Lao động 2019, Điều 21. https://hethongphapluat.com/bo-luat-lao-dong-2019/dieu-21 | Trung bình; đọc qua công cụ tóm tắt, không chép được nguyên văn |
| V7 | Kết quả tìm kiếm về Điều 21 và TT 10/2020/TT-BLĐTBXH (lsvn.vn, thuvienphapluat.vn). https://lsvn.vn/noi-dung-hop-dong-lao-dong-theo-bo-luat-lao-dong-2019-1693541008-a134722.html | Thấp-trung bình |
| A | `../an-toan-du-lieu-va-phap-ly-vn.md` | Tổng hợp thứ cấp |

## 9. Chưa kiểm chứng

- **Nguyên văn Điều 21 BLLĐ 2019** và TT 10/2020/TT-BLĐTBXH: chưa đọc bản gốc; danh sách ở 3.3 là tóm lược thứ cấp. Chưa kiểm có văn bản sửa đổi sau 2019.
- Chưa có nguồn nào đo LLM rà hợp đồng tiếng Việt.
- Mã K5.1 đã chạy trên một cặp mẫu/hợp đồng giả; chưa thử với hợp đồng thật có mục con (1.1, a, b), bảng, hay tiêu đề không theo dạng "Điều N.".
- Hàm đối chiếu số tiền bằng số và bằng chữ tiếng Việt: chưa viết.
- Quy định về xử lý dữ liệu ứng viên, thông báo cho ứng viên, quyết định tự động: chưa tra cứu; cần luật sư.
- Hai bài về injection trên CV (Zhang et al. 2026; Augey et al. 2026) chỉ biết qua phần tổng quan của B8.
