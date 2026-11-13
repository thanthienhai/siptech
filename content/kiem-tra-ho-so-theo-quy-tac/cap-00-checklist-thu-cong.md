# Cấp K0: Checklist và kiểm tra thủ công có kỷ luật

> Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.
> Nền chung về Project/Gem/GPT, bản giao việc 6 phần, sổ prompt: `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`. File này chỉ viết phần riêng của việc kiểm hồ sơ.

## 1. Mục tiêu và người đọc

**Người đọc:** kế toán, nhân viên mua hàng, hành chính nhân sự, chủ SME. Không cần code.

**Sau cấp này có:**
1. Một **checklist viết ra giấy** cho một loại hồ sơ. Mỗi dòng một quy tắc, có mã (ví dụ `HD-03`), có căn cứ.
2. Một Project/Gem/GPT "Kiểm hồ sơ loại X" dùng checklist đó, trả về **bảng kiểm**, không trả về đoạn văn.
3. Một **bộ 10 hồ sơ mẫu có đáp án** (biết trước hồ sơ nào lỗi gì).
4. Quy tắc: AI chỉ đề xuất; người ký duyệt.

## 2. Câu hỏi cấp này trả lời

*"Làm sao để việc hỏi AI 'hóa đơn này có đúng không?' thành một việc kiểm tra có danh sách, có kết quả từng dòng, và biết được AI đúng hay sai?"*

Lỗi của cách dùng hiện tại **[Đề xuất, quan sát]**:
- Không ai viết ra "đúng" nghĩa là gì. Mỗi người hỏi một kiểu.
- AI trả lời chung chung "hóa đơn hợp lệ". Không biết nó đã kiểm những gì, bỏ qua những gì.
- Không có hồ sơ mẫu có đáp án, nên không biết AI bỏ sót bao nhiêu.

## 3. Kiến thức nền

### 3.1 Checklist là sản phẩm chính, không phải prompt
- Ca Erste Bank tách hai bước: (1) trích quy tắc từ chính sách thành dạng có cấu trúc một lần, chuyên gia xem và sửa được; (2) kiểm từng hồ sơ theo bộ quy tắc đó **[Nguồn: B5]**. Tác giả nêu lợi ích: không phải trích lại cho mỗi hồ sơ, chuyên gia sửa được bộ quy tắc, và khi sai thì biết sai ở bước trích hay bước kiểm.
- Trong ca đó, không phải đoạn chính sách nào cũng thành quy tắc kiểm được: 90 đoạn chỉ cho ra khoảng 36 quy tắc, vì nhiều đoạn nói về quy trình nội bộ, không nói về nội dung hồ sơ **[Nguồn: B5]**.
- **[Đề xuất]** Với SME: checklist là tài sản. Prompt chỉ là cách "đọc" checklist cho AI.

### 3.2 Mỗi dòng checklist cần gì [Đề xuất]

| Cột | Ví dụ |
|---|---|
| Mã | `HD-04` |
| Quy tắc (một ý, kiểm được) | "Tổng trước thuế + tiền thuế = tổng thanh toán" |
| Căn cứ | "Quy chế thanh toán nội bộ, mục 2" hoặc văn bản pháp luật (ghi số, điều, ngày hiệu lực) |
| Loại | **Xác định** (tính được, so được) / **Tra cứu** (phải xem sổ, danh sách) / **Mờ** (cần hiểu nghĩa) |
| Mức độ | Cao (chặn thanh toán) / Thấp (ghi chú) |
| Khi thiếu dữ liệu | Ghi "không rõ", không ghi "đạt" |

Cột **Loại** quyết định cấp sau: quy tắc xác định và tra cứu sẽ chuyển sang code (K2, K4); quy tắc mờ sang LLM có kiểm (K3).

### 3.3 Bốn kết quả, không phải hai
Đạt / Lỗi / Không rõ / Không áp dụng. Ca Erste dùng 5 nhãn: tuân thủ, không tuân thủ, ngoại lệ chính sách, thiếu thông tin, cần người xem **[Nguồn: B5]**. **[Đề xuất]** Có nhãn "không rõ" thì AI không bị ép đoán. Mọi "không rõ" đi đến người.

## 4. Chuỗi bài nhỏ

### Bài K0.1: Chọn một loại hồ sơ và chép checklist thật
- **Làm:** chọn loại hồ sơ lặp nhiều nhất (thường là hóa đơn đầu vào trước khi thanh toán). Hỏi người đang làm: "Anh/chị kiểm những gì?" Ghi đúng như họ làm, kể cả bước họ không ghi trong quy chế. Gom thành 8-15 dòng theo bảng 3.2.
- **Sản phẩm:** `checklist_hoa_don_v1.xlsx`.
- **Lỗi thường gặp:** chép quy định pháp luật thay vì việc thật; gộp hai ý vào một dòng ("đúng MST và đúng tên"); quên ghi căn cứ và ngày hiệu lực.

### Bài K0.2: Bộ 10 hồ sơ mẫu có đáp án
- **Làm:** lấy 10 hồ sơ đã xử lý. Ít nhất 4 hồ sơ có lỗi thật hoặc cố ý sửa một bản sao (đổi một con số, xóa một trường). Với mỗi hồ sơ, điền đáp án cho **từng dòng checklist**.
- **Sản phẩm:** `bo_mau_v1.xlsx`: hàng = hồ sơ, cột = mã quy tắc, ô = Đạt/Lỗi/Không áp dụng.
- **Lỗi:** chỉ chọn hồ sơ "sạch"; đáp án chỉ ghi "hồ sơ lỗi" mà không ghi lỗi ở quy tắc nào.

### Bài K0.3: Project/Gem/GPT trả bảng kiểm
- **Làm:** tạo Project. Chỉ dẫn gồm: vai trò; toàn bộ checklist (dán bảng); yêu cầu **mỗi mã quy tắc một dòng** theo mẫu dưới; quy tắc "không thấy dữ liệu thì ghi KHÔNG RÕ"; quy tắc "chép nguyên văn đoạn làm căn cứ".
- **Mẫu đầu ra [Đề xuất, chưa đo]:**
  ```
  | Mã | Kết quả (ĐẠT/LỖI/KHÔNG RÕ/KHÔNG ÁP DỤNG) | Chép nguyên văn từ chứng từ | Vị trí (trang, dòng, ô) | Ghi chú |
  ```
  Thêm: "Liệt kê đủ mọi mã trong checklist, kể cả mã đạt. Không gộp. Không tính lại số; chỉ chép số in trên chứng từ."
- **Sản phẩm:** Project dùng được + ảnh chụp chỉ dẫn lưu vào sổ prompt.
- **Lỗi:** để AI tự nghĩ thêm quy tắc; để AI "tính lại cho đúng" (BMO phải viết rõ trong skill: giá trị "in trên chứng từ" phải đọc từ dòng in, không được tự tính thay **[Nguồn: B1, phụ lục B.1]**).

### Bài K0.4: Chạy bộ mẫu và chấm tay
- **Làm:** chạy 10 hồ sơ mẫu. So từng ô với đáp án. Đếm: (a) **bỏ sót** = đáp án Lỗi, AI ghi Đạt; (b) báo nhầm = đáp án Đạt, AI ghi Lỗi; (c) Không rõ; (d) AI bỏ dòng, không trả đủ mã.
- **Sản phẩm:** bảng chấm. Ghi riêng bỏ sót, vì đó là lỗi nguy hiểm nhất.
- **Lỗi:** chỉ nhìn tổng "đúng 85%". Một bỏ sót ở quy tắc "trùng hóa đơn" nặng hơn mười báo nhầm.

### Bài K0.5: Chạy lại cùng hồ sơ 3 lần
- **Làm:** chạy cùng 3 hồ sơ, mỗi hồ sơ 3 lần, trong 2 ngày khác nhau. Đếm số ô đổi kết quả.
- **Vì sao:** nghiên cứu trên 14 triển khai LLM thương mại thấy cùng yêu cầu gửi lặp lại cho kết quả khác nhau ở cả 14, và 12 có lúc đổi nhãn kết luận; có mô hình chỉ đổi giữa hai ngày **[Nguồn: B6]**.
- **Sản phẩm:** số ô "không ổn định". Quy tắc nào hay đổi là ứng viên đầu tiên để chuyển sang code ở K2.

### Bài K0.6: Quy tắc dữ liệu và quy tắc duyệt cho hồ sơ
- **Làm:** áp phân hạng dữ liệu trong `../an-toan-du-lieu-va-phap-ly-vn.md` cho từng loại hồ sơ. Hóa đơn bán hàng doanh nghiệp: thường hạng nội bộ. Hồ sơ nhân sự có CCCD, số tài khoản: nhạy cảm, **không dán vào tài khoản AI cá nhân**. Viết một dòng: "Bảng kiểm của AI là gợi ý. Người duyệt ký tên trên phiếu."
- **Sản phẩm:** một trang quy tắc, dán vào chỉ dẫn Project.

## 5. Đường không code vs có code

| | Không code (K0) | Có code (từ K1) |
|---|---|---|
| Đọc chứng từ | Tải file vào chat | Đọc XML, PDF bằng script |
| Kiểm số | AI đọc, người kiểm lại bằng máy tính | Code tính, không cần AI |
| Lặp lại | Kết quả có thể đổi giữa các lần | Quy tắc code lặp lại tuyệt đối |
| Lưu vết | Chép kết quả vào bảng tính | Log tự động |

**Buộc chuyển sang K1-K2 khi [Đề xuất]:** (a) bài K0.4 có bất kỳ bỏ sót nào ở quy tắc mức "cao" mà quy tắc đó tính được bằng số; hoặc (b) bài K0.5 có ô đổi kết quả; hoặc (c) hơn khoảng 30 hồ sơ mỗi tuần; hoặc (d) hồ sơ là hóa đơn điện tử có XML (lúc đó code rẻ hơn chat).

## 6. Tiêu chí lên cấp K1 (đo được) [Đề xuất]

1. Checklist có ít nhất 8 dòng, mỗi dòng có mã, căn cứ, loại, mức độ; người phụ trách nghiệp vụ ký xác nhận.
2. Bộ mẫu có ít nhất 10 hồ sơ, ít nhất 4 hồ sơ có lỗi, đáp án đến từng mã quy tắc.
3. Đã chạy K0.4 và K0.5, có số bỏ sót, báo nhầm, không ổn định.
4. Đã biết quy tắc nào là xác định / tra cứu / mờ.

Với n = 10, số đo chỉ để **phát hiện hỏng**, không phải để kết luận chính xác (xem `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`, mục 3.2).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa; tên hư cấu]

**a) Công ty phân phối bao bì, 12 người, kế toán 1 người.** Hồ sơ: hóa đơn đầu vào trước khi chi tiền.
Checklist v1 (trích): `HD-01` đủ trường số, ký hiệu, ngày, MST bên bán, MST bên mua · `HD-02` MST bên mua đúng MST công ty · `HD-03` tổng dòng = tổng trước thuế · `HD-04` trước thuế + thuế = tổng thanh toán · `HD-05` bên bán có trong danh sách nhà cung cấp · `HD-06` chưa từng ghi sổ hóa đơn này · `HD-07` (mờ) mô tả hàng phù hợp với hàng công ty mua.
Kết quả K0.4 giả định: AI ghi "đạt" ở `HD-06` cho cả 10 hồ sơ, vì nó không có sổ. Bài học: quy tắc tra cứu không thể làm trong chat; phải có dữ liệu (K4).

**b) Chuỗi 3 phòng khám nha, hành chính nhân sự 1 người.** Hồ sơ: hợp đồng lao động mới.
Checklist v1 (trích): `LD-01` có đủ các nội dung chủ yếu theo Điều 21 BLLĐ 2019 (danh sách nội dung: xem `cap-05`, cần kiểm văn bản gốc) · `LD-02` mức lương khớp quyết định tuyển dụng · `LD-03` thời hạn khớp loại hợp đồng · `LD-04` (mờ) điều khoản lạ so với mẫu công ty.
Quy tắc dữ liệu: bản hợp đồng dán vào AI phải che số CCCD, số tài khoản. Dùng tài khoản doanh nghiệp đã đọc điều khoản dữ liệu.

**c) Xưởng gỗ xuất khẩu, mua hàng 2 người.** Hồ sơ: phiếu giao hàng của nhà cung cấp gỗ. Phần lớn quy tắc là đối chiếu với đơn mua (K4). K0 chỉ dùng để viết checklist và gom bộ mẫu.

## 8. Tài liệu tham khảo

| Mã | Nguồn | Tin cậy |
|---|---|---|
| B1 | Shu et al., ESCROW, BMO, arXiv 2608.01772 (NeurIPS 2026). https://www.alphaxiv.org/abs/2608.01772 | Trung bình-cao: ca production thật; không công bố mã và dữ liệu |
| B5 | Voboril, LLM-Based Policy Compliance Verification of Loan Applications, arXiv 2610.20155. https://www.alphaxiv.org/abs/2610.20155 | Trung bình: nguyên mẫu thực tập, 11 hồ sơ, không chấm đầy đủ đúng/sai |
| B6 | Suzuki, deterministic medical device document assessment, arXiv 2610.21300. https://www.alphaxiv.org/abs/2610.21300 | Trung bình: tác giả thuộc công ty bán sản phẩm được thử; phần đo API thương mại là đo từ ngoài |
| R0 | Nhóm RAG, cấp 0 | `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` |

## 9. Chưa kiểm chứng

- Không có số đo nào về độ chính xác của Claude/ChatGPT/Gemini bản desktop khi đọc hóa đơn, hợp đồng tiếng Việt.
- Giao diện Project/Gem/GPT: xem mục 9 của `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`.
- Ví dụ checklist ở mục 7 là minh họa. Chưa đối chiếu với nội dung bắt buộc trên hóa đơn theo NĐ 254/2026 (văn bản gốc chưa đọc).
- Kết quả B6 đo trên tài liệu tiếng Anh và API của các hãng tại thời điểm thử; mức dao động của bản desktop chưa ai đo.
