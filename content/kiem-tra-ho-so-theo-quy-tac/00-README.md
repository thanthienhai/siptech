# Nhóm bài: Kiểm tra hồ sơ, chứng từ theo quy tắc

> Ngày soạn: 2026-11-11. Thuộc series "AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp".
> Quy ước: **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = suy luận hoặc thiết kế của nhóm soạn. Mọi ngưỡng, cỡ mẫu là [Đề xuất].
> Không phải tư vấn pháp lý hay tư vấn thuế. Đọc kèm `../an-toan-du-lieu-va-phap-ly-vn.md`.

## 1. Bài toán

**Đầu vào:** một bộ hồ sơ. Ví dụ: hóa đơn + phiếu nhập kho + đơn mua; một hợp đồng; một bộ hồ sơ nhân sự.
**Đầu ra:** danh sách lỗi có căn cứ. Mỗi lỗi ghi: quy tắc nào, kết quả (đạt / lỗi / không rõ), nằm ở đâu trong chứng từ, căn cứ quy tắc là gì.
**Người quyết định:** người duyệt. Hệ thống chỉ đề xuất.

Khác nhóm RAG (`../rag-tra-cuu-tai-lieu/`):

| | RAG tra cứu | Kiểm tra theo quy tắc |
|---|---|---|
| Đầu vào | Một câu hỏi | Một hồ sơ |
| Tài liệu đối chiếu | Kho tài liệu lớn, phải tìm | Bộ quy tắc nhỏ, biết trước, đi hết từng quy tắc |
| Đầu ra | Câu trả lời có trích dẫn | Bảng kiểm: mỗi quy tắc một kết quả |
| Lỗi nguy hiểm nhất | Trả lời sai | **Kết luận "đạt" khi thực ra có lỗi** (bỏ sót) |
| Phần làm bằng code | Kiểm trích dẫn | Phần lớn: đọc dữ liệu, tính toán, đối chiếu |

Vì bộ quy tắc biết trước, ta **không cần tìm kiếm** ở phần lớn bài toán. Đây là điểm làm bài toán này rẻ hơn RAG.

## 2. Vì sao SME Việt Nam gặp bài toán này

- Kế toán kiểm hóa đơn đầu vào trước khi thanh toán và kê khai. Hành chính nhân sự kiểm hồ sơ, hợp đồng lao động. Mua hàng đối chiếu đơn mua, phiếu giao, hóa đơn. Đây là việc lặp lại, tốn công, dễ sót khi mệt. **[Đề xuất, quan sát của nhóm soạn; chưa có khảo sát SME VN, xem `../thuc-trang-sme-viet-nam.md`]**
- Cách dùng AI "vô tội vạ" thường gặp: chụp hóa đơn dán vào chat, hỏi "hóa đơn này có đúng không?". Không có checklist, không có đáp án, không biết AI đã kiểm những gì. **[Đề xuất]**
- **Lợi thế riêng của Việt Nam:** hóa đơn điện tử có file XML gốc. Đọc XML bằng code thì không cần OCR, không cần mô hình, không có lỗi nhận dạng chữ. Phần đắt và dễ sai nhất của bài toán (biến chứng từ thành dữ liệu) gần như miễn phí với hóa đơn điện tử. Xem `cap-01`.

## 3. Bằng chứng tóm tắt

Chi tiết và mức tin cậy ở mục 8 của từng file cấp.

1. **Ca triển khai thật có cấu trúc giống bài toán này.** BMO FinDAS kiểm tài liệu tài chính nộp kèm hồ sơ vay: 78 tài liệu chính sách, 23 loại tài liệu, hơn 100 skill, 15 công cụ. Nhóm công cụ "kiểm tra luật định và cấu trúc" là hàm theo quy tắc, cho kết quả hợp lệ/không hợp lệ xác định; tác giả viết việc giao các quyết định này cho công cụ thay vì cho LLM làm giảm khả năng LLM bịa kết luận tuân thủ **[Nguồn: ESCROW 2608.01772, phụ lục B, C]**.
2. **Quy tắc được trích một lần, kiểm nhiều lần.** Nguyên mẫu ở Erste Bank: 90 đoạn chính sách → 36 quy tắc JSON (ổn định qua 5 lần chạy); kiểm 11 hồ sơ vay × 36 quy tắc = 396 lượt; bắt được 11/13 ngoại lệ đã biết, thêm vài lỗi người bỏ sót; có báo nhầm, xu hướng báo thừa **[Nguồn: 2610.20155]**.
3. **Trích xuất bằng mô hình vẫn sai đáng kể.** GPT-4o sai 26,6% số trường trên hóa đơn DocILE; độ tự tin do mô hình tự báo (logprob, tự chấm) gần như không phân biệt được trường đúng/sai (AUC 0,69-0,74) **[Nguồn: 2606.24420]**. Trên ExtractBench, một mô hình giảm từ 87,9% ở tài liệu ngắn xuống 27,9% ở tài liệu dài **[Nguồn: 2607.29677, nhóm tác giả là nhà cung cấp công cụ]**.
4. **Rà hợp đồng bằng LLM còn bỏ sót nhiều.** ContractScrub (44 hợp đồng, luật sư gắn nhãn): mô hình tốt nhất bắt 75% lỗi; loại lỗi cần hiểu ngữ cảnh chỉ khoảng 35-43% **[Nguồn: 2608.20204]**.
5. **Kết quả LLM không lặp lại.** 14 triển khai thương mại, gửi cùng yêu cầu nhiều lần ở chế độ "xác định": cả 14 đều có lúc trả khác nhau, 12 có lúc đổi cả nhãn kết luận **[Nguồn: 2610.21300]**. Quy tắc bằng code thì lặp lại tuyệt đối.
6. **Hợp đồng do bên kia soạn có thể chứa câu nhắm vào AI rà soát.** 11 bộ lọc prompt injection bày bán sẵn đều không dùng được trên hợp đồng (báo nhầm tới 92%); LLM có prompt riêng làm tốt hơn nhiều **[Nguồn: 2611.08834]**.
7. Không có nguồn nào đo trên chứng từ SME Việt Nam. Khảo sát nhận dạng tài liệu tiếng Việt chỉ ra dấu thanh và thiếu dữ liệu là trở ngại chính **[Nguồn: 2506.05061]**.

**[Đề xuất] Rút ra:** quy tắc nào viết được bằng code thì viết bằng code. LLM chỉ dùng cho (a) đọc chứng từ không có dữ liệu gốc, (b) quy tắc cần hiểu nghĩa. Mọi kết luận của LLM phải kèm trích dẫn nguyên văn và bị code kiểm lại. Người duyệt xem mọi "lỗi" và "không rõ".

## 4. Thang cấp độ của nhóm

| Cấp | File | Một dòng |
|---|---|---|
| K0 | `cap-00-checklist-thu-cong.md` | Viết checklist, kiểm thủ công một hồ sơ bằng Project/Gem/GPT, có bộ hồ sơ mẫu có đáp án |
| K1 | `cap-01-chung-tu-thanh-du-lieu.md` | Chứng từ thành JSON có nguồn từng trường: XML trước, PDF có chữ sau, ảnh cuối cùng |
| K2 | `cap-02-quy-tac-thanh-ma.md` | Sổ quy tắc; quy tắc xác định chạy bằng code; báo cáo lỗi có vị trí và căn cứ |
| K3 | `cap-03-quy-tac-mo-bang-llm.md` | Quy tắc cần hiểu nghĩa giao LLM từng quy tắc một; trích dẫn kiểm bằng code; sai thì hạ về "không rõ" |
| K4 | `cap-04-doi-chieu-cheo.md` | Đối chiếu nhiều chứng từ: đơn mua, phiếu nhập, hóa đơn; trùng hóa đơn; nhà cung cấp |
| K5 | `cap-05-hop-dong-va-ho-so-nhan-su.md` | Hợp đồng so với mẫu chuẩn và điều khoản bắt buộc; hồ sơ nhân sự, CV |
| K6 | `cap-06-danh-gia-va-hang-doi-duyet.md` | Bộ hồ sơ cài lỗi sẵn; đo tỷ lệ bắt và bỏ sót theo từng quy tắc; hàng đợi duyệt |
| K7 | `cap-07-van-hanh-va-doi-quy-dinh.md` | Phiên bản bộ quy tắc; cổng không thoái lui theo nhóm; xử lý khi quy định thay đổi |

Mỗi cấp chạy được độc lập. Có thể dừng ở K2 nếu chỉ kiểm hóa đơn điện tử: phần lớn giá trị nằm ở K1-K2 với XML.

## 5. Tái dùng khối nào của nhóm RAG

| Khối | Ở đâu | Dùng cho |
|---|---|---|
| Bản giao việc 6 phần, sổ prompt | `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` | K0 |
| Gọi API, JSON có cấu trúc, chi phí | `../rag-tra-cuu-tai-lieu/cap-01-goi-api.md` | K1, K3 |
| PDF/scan thành text, CER, kiểm tổng hóa đơn, bảo mật gửi tài liệu | `../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` | K1 |
| Chia khối theo tiêu đề, mã ổn định | `../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` | K5 (tách điều khoản) |
| Kiểm trích dẫn nguyên văn bằng code | `../rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md` | K3 |
| Bộ ca mẫu, Wilson, kappa, LLM-as-judge | `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` | K6 |
| Công cụ đọc/ghi, phân hạng quyền, injection | `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` | K4 (tra sổ), K5 |
| Workflow, điểm duyệt, tình huống 7.c | `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` | K4-K6 |
| Log, phiên bản, phát hành, trôi dạt | `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` | K7 |

Nhóm này chỉ viết phần khác biệt. Không lặp lại nội dung các file trên.

## 6. Rủi ro pháp lý và dữ liệu chính

1. **Quy định hóa đơn đã thay đổi trong năm 2026.** Theo nhiều nguồn thứ cấp (EY và các trang kế toán), Nghị định 254/2026/NĐ-CP ban hành 30/6/2026, hiệu lực 01/7/2026, thay thế Nghị định 123/2020/NĐ-CP (đã sửa bởi Nghị định 70/2025/NĐ-CP); Thông tư 91/2026/TT-BTC thay Thông tư 32/2025/TT-BTC **[Nguồn: EY, đọc qua công cụ tóm tắt; chưa đọc văn bản gốc]**. Bài nào còn dẫn NĐ 123 hay NĐ 70 làm căn cứ hiện hành phải sửa. Đây cũng là ví dụ thật cho K7: bộ quy tắc phải có ngày hiệu lực và căn cứ.
2. **Định dạng XML:** theo EY, NĐ 254 không còn quy định chi tiết định dạng, giao Bộ trưởng Bộ Tài chính hướng dẫn. Văn bản kỹ thuật trước đây là Quyết định 1450/QĐ-TCT (2021). **Tên thẻ XML trong code mẫu chưa đối chiếu văn bản gốc**; phải sửa theo file thật.
3. **Dữ liệu cá nhân:** hồ sơ nhân sự, CV, ảnh CCCD là dữ liệu cá nhân; theo tóm tắt của EY về NĐ 356/2025, ảnh giấy tờ tùy thân và lịch sử giao dịch ngân hàng thuộc nhóm nhạy cảm. Gửi lên dịch vụ AI ở nước ngoài có thể là chuyển dữ liệu xuyên biên giới. Xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 3.1, 4, 6.
4. **Trách nhiệm:** kết luận của hệ thống không phải căn cứ duy nhất để từ chối thanh toán, kê khai thuế, hay từ chối ứng viên. Quyết định về con người (tuyển dụng) cần thận trọng thêm; xem `cap-05`.
5. **Tấn công qua tài liệu:** hợp đồng, hóa đơn, CV do bên ngoài soạn. Có thể chứa câu hoặc chữ ẩn nhắm vào AI. Xem `cap-03`, `cap-05`.

## 7. Danh sách kiểm chứng trước khi xuất bản

**Pháp lý (bắt buộc):**
- [ ] Đọc văn bản gốc NĐ 254/2026/NĐ-CP và TT 91/2026/TT-BTC: nội dung bắt buộc trên hóa đơn, trách nhiệm người mua, lưu trữ, xử lý hóa đơn sai sót. Xác nhận NĐ 70/2025 và NĐ 123/2020 đã hết hiệu lực toàn bộ hay còn điều khoản chuyển tiếp.
- [ ] Tìm văn bản hiện hành về định dạng XML hóa đơn (QĐ 1450/QĐ-TCT còn hiệu lực không, có văn bản thay thế không). Đối chiếu tên thẻ với 5 file XML thật từ 3 nhà cung cấp hóa đơn khác nhau.
- [ ] Đọc toàn văn Điều 21 Bộ luật Lao động 2019 và Thông tư 10/2020/TT-BLĐTBXH (nội dung hợp đồng lao động); kiểm còn hiệu lực.
- [ ] Kiểm NĐ 356/2025 về ảnh giấy tờ tùy thân, dữ liệu ứng viên, chuyển dữ liệu ra nước ngoài (dùng chung danh sách với `../an-toan-du-lieu-va-phap-ly-vn.md`).

**Công cụ:**
- [ ] Menu, nút xuất Excel/XML trên cổng hóa đơn điện tử của cơ quan thuế (chỉ có hướng dẫn thứ cấp).
- [ ] Tính năng của phần mềm kế toán và hóa đơn (MISA và các hãng khác) liên quan đến tải hóa đơn đầu vào, kiểm hóa đơn: chưa đọc tài liệu chính thức; không nêu tính năng cụ thể trong bài.
- [ ] Giao diện Project/Gem/GPT: dùng chung kiểm tra với nhóm RAG.

**Kỹ thuật:**
- [ ] Code mẫu `k1`-`k7` đã chạy với `python -I` trên dữ liệu giả lập, hàm LLM giả. Chưa chạy với API thật, chưa chạy trên chứng từ thật.
- [ ] Chưa có số đo nào trên chứng từ SME Việt Nam. Người học phải tự đo (`cap-06`).
- [ ] Số liệu "tỷ lệ ngoại lệ", "tỷ lệ không chạm tay" của ngành AP chỉ thấy ở blog nhà cung cấp, mâu thuẫn nhau: không dùng (xem `cap-04` mục 9).

## 8. Nguồn chính đã đọc

| Mã | Nguồn | Mức đọc |
|---|---|---|
| B1 | ESCROW / FinDAS, BMO, arXiv 2608.01772 | Phần lớn các trang (phương pháp, thực nghiệm, phụ lục B-G) qua công cụ trích PDF; số chính đã có trong `../nen-tang-bang-chung.md` |
| B2 | ExtractBench, LlamaIndex, arXiv 2607.29677 | Phần lớn các trang chính |
| B3 | OCR or Not?, SAP + Stanford, arXiv 2603.02789 | Gần toàn văn |
| B4 | ExtractConf (Beyond Logprobs), Perfios, arXiv 2606.24420 | Gần toàn văn |
| B5 | LLM-Based Policy Compliance Verification of Loan Applications, TU Wien + Erste Bank, arXiv 2610.20155 | Toàn văn |
| B6 | Making every stage of medical device document assessment deterministic, arXiv 2610.21300 | Phần lớn các trang |
| B7 | ContractScrub, Thomson Reuters, arXiv 2608.20204 | Phần lớn các trang |
| B8 | Prompt injection guards on legal contracts, Ivo AI, arXiv 2611.08834 | Phần lớn các trang |
| B9 | CUAD, arXiv 2103.06268 | Phần lớn các trang |
| B10 | Survey on Vietnamese Document Analysis and Recognition, arXiv 2506.05061 | Phần lớn các trang |
| V1 | EY: Nghị định 254/2026/NĐ-CP | Đọc qua công cụ tóm tắt trang |
| V2 | Kết quả tìm kiếm về NĐ 70/2025, QĐ 1450/QĐ-TCT, cổng hóa đơn điện tử, BLLĐ 2019 Điều 21 | Chỉ tóm tắt tìm kiếm hoặc trang thứ cấp |
