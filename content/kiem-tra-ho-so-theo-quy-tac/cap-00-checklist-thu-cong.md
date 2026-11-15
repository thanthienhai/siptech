# Cấp K0: Checklist và kiểm tra thủ công có kỷ luật

> Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.
> Nền chung về Project/Gem/GPT, bản giao việc 6 phần, sổ prompt: `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`. File này chỉ viết phần riêng của việc kiểm hồ sơ.

!!! tip "Tóm tắt nhanh"
    Hỏi AI "hóa đơn này có đúng không?" thì chỉ nhận về một câu trả lời chung chung, và bạn không biết nó đã kiểm những gì. Bài này dạy cách làm khác, **không cần biết lập trình**: viết ra một **checklist** (danh sách các điều cần kiểm, mỗi dòng một quy tắc), bắt AI trả về **bảng kiểm từng dòng**, rồi thử trên một bộ hồ sơ mẫu có đáp án để biết AI đúng hay sai. Sau bài, bạn có checklist, một Project/Gem/GPT dùng checklist đó, và bộ 10 hồ sơ mẫu.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** kế toán, nhân viên mua hàng, hành chính nhân sự, chủ SME (doanh nghiệp nhỏ và vừa). Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Một loại hồ sơ mà bạn gặp lặp lại nhiều nhất (thường là hóa đơn đầu vào trước khi thanh toán), và người đang làm việc kiểm hồ sơ đó để bạn hỏi "Anh/chị kiểm những gì?".
- Khoảng 10 hồ sơ đã xử lý xong, để làm bộ mẫu.
- Một tài khoản có thể tạo Project (Claude), Gem (Gemini) hoặc GPT (ChatGPT). Đây là tính năng cho bạn lưu sẵn chỉ dẫn để dùng lại nhiều lần. Cách dùng chung xem file `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`.
- Một bảng tính (Excel hoặc tương đương) để ghi checklist, bộ mẫu và bảng chấm; một cái máy tính bỏ túi để kiểm lại các phép cộng.

**Sau bài này bạn sẽ có:**
1. Một **checklist viết ra giấy** cho một loại hồ sơ. Mỗi dòng một quy tắc, có mã (ví dụ `HD-03`), có căn cứ.
2. Một Project/Gem/GPT "Kiểm hồ sơ loại X" dùng checklist đó, trả về **bảng kiểm**, không trả về đoạn văn.
3. Một **bộ 10 hồ sơ mẫu có đáp án** (biết trước hồ sơ nào lỗi gì).
4. Quy tắc: AI chỉ đề xuất; người ký duyệt.

**Thứ bạn cầm đi được sau bài:** file checklist, bộ hồ sơ mẫu có đáp án, một Project/Gem/GPT trả bảng kiểm, bảng chấm kết quả, và một trang quy tắc dữ liệu và duyệt.

## 2. Câu hỏi cấp này trả lời

*"Làm sao để việc hỏi AI 'hóa đơn này có đúng không?' thành một việc kiểm tra có danh sách, có kết quả từng dòng, và biết được AI đúng hay sai?"*

Cách dùng hiện tại thường có ba lỗi **[Đề xuất, quan sát]**:
- Không ai viết ra "đúng" nghĩa là gì. Mỗi người hỏi một kiểu.
- AI trả lời chung chung "hóa đơn hợp lệ". Bạn không biết nó đã kiểm những gì, bỏ qua những gì.
- Không có hồ sơ mẫu có đáp án, nên không biết AI bỏ sót bao nhiêu.

## 3. Kiến thức nền

### 3.1 Checklist là sản phẩm chính, không phải prompt

(Prompt là câu lệnh, câu chỉ dẫn bạn gõ cho AI.)

- Ca Erste Bank tách việc thành hai bước. Bước 1: trích quy tắc từ chính sách thành dạng có cấu trúc, làm **một lần**, và chuyên gia có thể xem và sửa. Bước 2: kiểm từng hồ sơ theo bộ quy tắc đó **[Nguồn: B5]**. Tác giả nêu lợi ích: không phải trích lại cho mỗi hồ sơ, chuyên gia sửa được bộ quy tắc, và khi sai thì biết sai ở bước trích hay bước kiểm.
- Trong ca đó, không phải đoạn chính sách nào cũng thành quy tắc kiểm được: 90 đoạn chỉ cho ra khoảng 36 quy tắc, vì nhiều đoạn nói về quy trình nội bộ, không nói về nội dung hồ sơ **[Nguồn: B5]**.
- **[Đề xuất]** Với SME: checklist là tài sản của bạn. Prompt chỉ là cách "đọc" checklist cho AI.

!!! tip "Nói đơn giản"
    Hãy coi checklist như một tờ phiếu kiểm hàng mà ai cũng dùng chung. AI chỉ là người cầm tờ phiếu đó đi kiểm. Phiếu viết tốt thì ai kiểm cũng ra kết quả giống nhau, và khi sai bạn biết sai ở phiếu hay ở người kiểm.

### 3.2 Mỗi dòng checklist cần gì [Đề xuất]

Mỗi dòng checklist gồm các cột sau:

| Cột | Ví dụ |
|---|---|
| Mã | `HD-04` |
| Quy tắc (một ý, kiểm được) | "Tổng trước thuế + tiền thuế = tổng thanh toán" |
| Căn cứ | "Quy chế thanh toán nội bộ, mục 2" hoặc văn bản pháp luật (ghi số, điều, ngày hiệu lực) |
| Loại | **Xác định** (tính được, so được) / **Tra cứu** (phải xem sổ, danh sách) / **Mờ** (cần hiểu nghĩa) |
| Mức độ | Cao (chặn thanh toán) / Thấp (ghi chú) |
| Khi thiếu dữ liệu | Ghi "không rõ", không ghi "đạt" |

Cột **Loại** quyết định cấp sau: quy tắc xác định và tra cứu sẽ chuyển sang code (K2, K4); quy tắc mờ sang LLM có kiểm (K3). (LLM là mô hình ngôn ngữ lớn, tức loại AI đứng sau Claude, ChatGPT, Gemini. Các cấp K2, K3, K4 là những bài sau, không cần đọc ngay.)

!!! tip "Nói đơn giản"
    Ba loại quy tắc nghĩa là: **xác định** là cái máy tính cũng làm được (cộng trừ, so hai con số); **tra cứu** là phải mở một cuốn sổ hay một danh sách ra xem; **mờ** là phải hiểu nghĩa câu chữ, như "mô tả hàng có hợp lý không". Việc phân loại này giúp bạn biết sau này quy tắc nào nên giao cho máy làm, quy tắc nào vẫn cần AI đọc.

### 3.3 Bốn kết quả, không phải hai

Kết quả kiểm có bốn nhãn: **Đạt / Lỗi / Không rõ / Không áp dụng**. Ca Erste dùng 5 nhãn: tuân thủ, không tuân thủ, ngoại lệ chính sách, thiếu thông tin, cần người xem **[Nguồn: B5]**.

**[Đề xuất]** Có nhãn "không rõ" thì AI không bị ép đoán. Mọi "không rõ" đi đến người.

!!! tip "Nói đơn giản"
    Nếu chỉ có hai lựa chọn "đạt" hoặc "lỗi", AI sẽ chọn bừa một trong hai khi không thấy dữ liệu. Cho phép nó nói "không rõ" thì chỗ nào thiếu thông tin sẽ lộ ra, và người xem lại chính những chỗ đó.

## 4. Chuỗi bài nhỏ

Sáu bài thực hành dưới đây làm theo thứ tự. Mỗi bài có việc cần làm, thứ bạn có sau bài và (với phần lớn các bài) lỗi hay gặp để tránh.

### Bài K0.1: Chọn một loại hồ sơ và chép checklist thật
- **Việc cần làm:** chọn loại hồ sơ lặp nhiều nhất (thường là hóa đơn đầu vào trước khi thanh toán). Hỏi người đang làm: "Anh/chị kiểm những gì?" Ghi đúng như họ làm, kể cả bước họ không ghi trong quy chế. Gom thành 8 đến 15 dòng theo bảng ở mục 3.2.
- **Bạn có sau bài:** `checklist_hoa_don_v1.xlsx`.
- **Lỗi hay gặp:** chép quy định pháp luật thay vì việc thật; gộp hai ý vào một dòng ("đúng MST và đúng tên"); quên ghi căn cứ và ngày hiệu lực. (MST là mã số thuế.)

### Bài K0.2: Bộ 10 hồ sơ mẫu có đáp án
- **Việc cần làm:** lấy 10 hồ sơ đã xử lý. Ít nhất 4 hồ sơ có lỗi thật, hoặc bạn cố ý sửa một bản sao (đổi một con số, xóa một trường). Với mỗi hồ sơ, điền đáp án cho **từng dòng checklist**.
- **Bạn có sau bài:** `bo_mau_v1.xlsx`: mỗi hàng là một hồ sơ, mỗi cột là một mã quy tắc, mỗi ô ghi Đạt/Lỗi/Không áp dụng.
- **Lỗi hay gặp:** chỉ chọn hồ sơ "sạch"; đáp án chỉ ghi "hồ sơ lỗi" mà không ghi lỗi ở quy tắc nào.

### Bài K0.3: Project/Gem/GPT trả bảng kiểm
- **Việc cần làm:** tạo một Project. Phần chỉ dẫn gồm: vai trò của AI; toàn bộ checklist (dán cả bảng vào); yêu cầu **mỗi mã quy tắc một dòng** theo mẫu bên dưới; quy tắc "không thấy dữ liệu thì ghi KHÔNG RÕ"; quy tắc "chép nguyên văn đoạn làm căn cứ".
- **Mẫu đầu ra [Đề xuất, chưa đo]:**

  **Đoạn mã dưới đây làm gì?** Thực ra đây không phải chương trình, mà là *hàng tiêu đề của bảng kết quả* bạn muốn AI trả về: mỗi mã quy tắc một dòng, có kết quả, có đoạn chép nguyên văn từ chứng từ, có vị trí tìm thấy, có ghi chú. Bạn chỉ việc dán mẫu này vào chỉ dẫn của Project, không cần hiểu từng ký hiệu.

  ```
  | Mã | Kết quả (ĐẠT/LỖI/KHÔNG RÕ/KHÔNG ÁP DỤNG) | Chép nguyên văn từ chứng từ | Vị trí (trang, dòng, ô) | Ghi chú |
  ```
  Thêm vào chỉ dẫn: "Liệt kê đủ mọi mã trong checklist, kể cả mã đạt. Không gộp. Không tính lại số; chỉ chép số in trên chứng từ."
- **Bạn có sau bài:** một Project dùng được, kèm ảnh chụp chỉ dẫn lưu vào sổ prompt.
- **Lỗi hay gặp:** để AI tự nghĩ thêm quy tắc; để AI "tính lại cho đúng". Ví dụ, BMO phải viết rõ trong skill (bộ chỉ dẫn của hệ thống) rằng giá trị "in trên chứng từ" phải đọc từ dòng in, không được tự tính thay **[Nguồn: B1, phụ lục B.1]**.

!!! tip "Nói đơn giản"
    Hai điều dễ làm hỏng nhất: AI tự thêm quy tắc không có trong checklist, và AI "sửa" con số cho đúng thay vì chép con số đang in trên giấy. Vì vậy chỉ dẫn phải nói rõ: chỉ kiểm theo checklist, chỉ chép số in, không tính lại.

### Bài K0.4: Chạy bộ mẫu và chấm tay
- **Việc cần làm:** chạy 10 hồ sơ mẫu qua Project. So từng ô với đáp án. Đếm bốn thứ: (a) **bỏ sót** = đáp án là Lỗi, AI ghi Đạt; (b) báo nhầm = đáp án là Đạt, AI ghi Lỗi; (c) số ô Không rõ; (d) AI bỏ dòng, không trả đủ mã.
- **Bạn có sau bài:** bảng chấm. Ghi riêng số bỏ sót, vì đó là lỗi nguy hiểm nhất.
- **Lỗi hay gặp:** chỉ nhìn tổng "đúng 85%". Một bỏ sót ở quy tắc "trùng hóa đơn" nặng hơn mười báo nhầm.

### Bài K0.5: Chạy lại cùng hồ sơ 3 lần
- **Việc cần làm:** chạy cùng 3 hồ sơ, mỗi hồ sơ 3 lần, trong 2 ngày khác nhau. Đếm số ô đổi kết quả.
- **Vì sao:** nghiên cứu trên 14 triển khai LLM thương mại thấy cùng một yêu cầu gửi lặp lại cho kết quả khác nhau ở cả 14, và 12 trong số đó có lúc đổi nhãn kết luận; có mô hình chỉ đổi giữa hai ngày **[Nguồn: B6]**.
- **Bạn có sau bài:** số ô "không ổn định". Quy tắc nào hay đổi là ứng viên đầu tiên để chuyển sang code ở K2.

!!! tip "Nói đơn giản"
    AI không phải cái máy tính: hỏi hai lần cùng một câu có thể ra hai đáp án khác nhau. Bài này giúp bạn đo xem chuyện đó xảy ra nhiều hay ít với hồ sơ của bạn.

### Bài K0.6: Quy tắc dữ liệu và quy tắc duyệt cho hồ sơ
- **Việc cần làm:** áp phân hạng dữ liệu trong `../an-toan-du-lieu-va-phap-ly-vn.md` cho từng loại hồ sơ. Hóa đơn bán hàng doanh nghiệp: thường thuộc hạng nội bộ. Hồ sơ nhân sự có CCCD, số tài khoản: thuộc hạng nhạy cảm, **không dán vào tài khoản AI cá nhân**. Viết một dòng: "Bảng kiểm của AI là gợi ý. Người duyệt ký tên trên phiếu." (CCCD là căn cước công dân.)
- **Bạn có sau bài:** một trang quy tắc, dán vào chỉ dẫn Project.

## 5. Đường không code vs có code

Bài này làm hoàn toàn bằng chat, không cần code (K0). Từ cấp K1 trở đi sẽ dùng code (chương trình nhỏ để máy tự làm). Bảng dưới đây so sánh hai đường.

| | Không code (K0) | Có code (từ K1) |
|---|---|---|
| Đọc chứng từ | Tải file vào chat | Đọc XML, PDF bằng script |
| Kiểm số | AI đọc, người kiểm lại bằng máy tính | Code tính, không cần AI |
| Lặp lại | Kết quả có thể đổi giữa các lần | Quy tắc code lặp lại tuyệt đối |
| Lưu vết | Chép kết quả vào bảng tính | Log tự động |

(XML là định dạng file hóa đơn điện tử mà máy đọc được trực tiếp. Script là một đoạn chương trình ngắn. Log là nhật ký ghi lại mỗi lần máy kiểm.)

**Buộc chuyển sang K1-K2 khi [Đề xuất]:** (a) bài K0.4 có bất kỳ bỏ sót nào ở quy tắc mức "cao" mà quy tắc đó tính được bằng số; hoặc (b) bài K0.5 có ô đổi kết quả; hoặc (c) hơn khoảng 30 hồ sơ mỗi tuần; hoặc (d) hồ sơ là hóa đơn điện tử có XML (lúc đó code rẻ hơn chat).

!!! tip "Nói đơn giản"
    Nếu AI từng bỏ sót một lỗi nặng mà máy tính cũng tính ra được, hoặc cùng một hồ sơ cho ra hai kết quả khác nhau, thì đó là dấu hiệu nên chuyển phần kiểm đó cho code. Code làm lại bao nhiêu lần cũng ra cùng một kết quả.

## 6. Tiêu chí lên cấp K1 (đo được) [Đề xuất]

Bạn có thể sang cấp K1 khi đạt đủ các điều sau:
1. Checklist có ít nhất 8 dòng, mỗi dòng có mã, căn cứ, loại, mức độ; người phụ trách nghiệp vụ ký xác nhận.
2. Bộ mẫu có ít nhất 10 hồ sơ, ít nhất 4 hồ sơ có lỗi, đáp án đến từng mã quy tắc.
3. Đã chạy K0.4 và K0.5, có số bỏ sót, báo nhầm, không ổn định.
4. Đã biết quy tắc nào là xác định / tra cứu / mờ.

Với n = 10 (tức chỉ có 10 hồ sơ), số đo chỉ để **phát hiện hỏng**, không phải để kết luận chính xác (xem `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`, mục 3.2).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa; tên hư cấu]

Ba tình huống giả định để bạn dễ hình dung.

**a) Công ty phân phối bao bì, 12 người, kế toán 1 người.** Hồ sơ: hóa đơn đầu vào trước khi chi tiền.

Checklist v1 (trích): `HD-01` đủ trường số, ký hiệu, ngày, MST bên bán, MST bên mua · `HD-02` MST bên mua đúng MST công ty · `HD-03` tổng dòng = tổng trước thuế · `HD-04` trước thuế + thuế = tổng thanh toán · `HD-05` bên bán có trong danh sách nhà cung cấp · `HD-06` chưa từng ghi sổ hóa đơn này · `HD-07` (mờ) mô tả hàng phù hợp với hàng công ty mua.

Kết quả K0.4 giả định: AI ghi "đạt" ở `HD-06` cho cả 10 hồ sơ, vì nó không có sổ. Bài học: quy tắc tra cứu không thể làm trong chat; phải có dữ liệu (K4).

**b) Chuỗi 3 phòng khám nha, hành chính nhân sự 1 người.** Hồ sơ: hợp đồng lao động mới.

Checklist v1 (trích): `LD-01` có đủ các nội dung chủ yếu theo Điều 21 BLLĐ 2019 (danh sách nội dung: xem `cap-05`, cần kiểm văn bản gốc) · `LD-02` mức lương khớp quyết định tuyển dụng · `LD-03` thời hạn khớp loại hợp đồng · `LD-04` (mờ) điều khoản lạ so với mẫu công ty. (BLLĐ là Bộ luật Lao động.)

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
