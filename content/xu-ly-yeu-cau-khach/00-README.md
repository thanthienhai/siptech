# Nhóm bài: Xử lý yêu cầu khách theo quy trình

> Ngày soạn: 2026-11-11. Thuộc series "AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp".
> Quy ước: **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = suy luận hoặc thiết kế của nhóm soạn. Mọi ngưỡng, cỡ mẫu là [Đề xuất].
> Không phải tư vấn pháp lý. Phần dữ liệu cá nhân dùng chung xem `../an-toan-du-lieu-va-phap-ly-vn.md`.

## 1. Bài toán

Khách nhắn qua Zalo, Messenger, email: hỏi đơn ở đâu, muốn đổi size, đòi hoàn tiền, khiếu nại, xin dời lịch hẹn. Nhân viên phải (1) hiểu khách muốn gì và gấp tới đâu, (2) tra đơn, (3) đối chiếu chính sách, (4) **quyết định** làm gì, (5) **làm** (tạo phiếu đổi trả, hoàn tiền, dời lịch), (6) trả lời khách, (7) chuyển người khi vượt quyền.

**Điểm khác nhóm RAG** (`../rag-tra-cuu-tai-lieu/`): đầu ra của nhóm RAG là một câu trả lời có trích dẫn. Đầu ra ở đây là **quyết định và hành động có hậu quả** (tiền, lịch, cam kết với khách). Sai một câu trả lời thì sửa được. Hoàn tiền nhầm, hứa sai chính sách thì doanh nghiệp phải chịu.

## 2. Vì sao SME Việt Nam gặp bài toán này

- Kênh chính là chat (Zalo OA, Messenger, sàn TMĐT). Tin đến dồn dập, viết tắt, không dấu. **[Đề xuất, quan sát chung; chưa có số liệu VN đo được]**
- Chính sách đổi trả thường chỉ nằm trong đầu chủ shop hoặc rải rác trong tin nhắn cũ. Không có SOP thì AI không có gì để theo, và **nhân viên mới cũng vậy**.
- Nhân viên đang dán tin khách (có SĐT, địa chỉ) vào ChatGPT cá nhân để "soạn cho nhanh". Xem `../thuc-trang-sme-viet-nam.md` mục 3.2 về shadow AI.
- Có một ca SME Việt kể AI hiểu sai viết tắt, xử lý nhầm đơn **[Nguồn: VCCI/HUBA, lời kể, xem `../thuc-trang-sme-viet-nam.md` mục 3.2]**.

## 3. Bằng chứng tóm tắt

| Nguồn | Điều rút ra | Mức đọc |
|---|---|---|
| Nubank, arXiv 2606.08867 (KDD 2026) | Routine từ SOP; ca giao thẻ 3 công cụ; vài trăm nhãn nhị phân đủ dựng bộ chấm; rollout 1%; tNPS và tỉ lệ tự phục vụ (SSR) đánh đổi nhau; ca quản lý nợ thấp hơn nhân viên giỏi 23,6 điểm; agent không ra quyết định không đảo ngược | Đọc lại phần lớn toàn văn |
| Nubank, arXiv 2609.30137 | Mô phỏng khách trước khi phát hành; người chấm phân biệt sai 15/50 hội thoại mô phỏng; mô phỏng dài hơn hội thoại thật nhiều | Đọc phần lớn toàn văn |
| τ-bench, arXiv 2406.12045 | Chính sách viết bằng chữ + công cụ đọc/ghi; gpt-4o pass^1 ~61% (bán lẻ), pass^8 <25%; lỗi do quyết định sai 25%, làm thiếu yêu cầu ghép 19% | Đọc toàn văn phần chính |
| SEATauBench, arXiv 2606.28715 | Bản tiếng Việt khi bản địa hóa toàn bộ: pass@1 0,52 so với 0,62 tiếng Anh (trung bình 3 mô hình) | Đọc phần chính |
| Policy Loopholes, arXiv 2609.14400 | Chính sách có chỗ im lặng/mâu thuẫn làm agent xử lý không nhất quán; chặn bằng công cụ thì lỗ hổng không phát huy | Đọc phần chính |
| Airbnb, arXiv 2610.14428 | Thất bại còn lại chủ yếu do SOP thiếu bước | Qua `../nen-tang-bang-chung.md` |
| Moffatt v. Air Canada (2024) | Doanh nghiệp chịu trách nhiệm về lời chatbot nói | Nguồn thứ cấp (bản án gốc trả 403) |
| Luật BVQLNTD 19/2023/QH15 | Điều 31: tiếp nhận và giải quyết khiếu nại, thông báo đã nhận trong 03 ngày làm việc | Đọc qua trang văn bản, chưa đọc bản Công báo |

Chi tiết số liệu nằm trong từng file cấp.

## 4. Thang cấp độ

| Cấp | File | Một dòng |
|---|---|---|
| C0 | `cap-00-sop-tu-ca-that.md` | Viết SOP tối thiểu từ 30 ca đã xảy ra; bảng quyết định; kiểm lỗ hổng chính sách; bộ ca mẫu đầu tiên |
| C1 | `cap-01-soan-tra-loi-co-duyet.md` | Project/Gem soạn nháp trả lời theo SOP và mẫu câu; người duyệt 100%; cụm cấm hứa hẹn |
| C2 | `cap-02-phan-loai-va-muc-khan.md` | Phân loại ý định và mức khẩn ra JSON; luật cứng bằng code đè lên AI; "không chắc" thì chuyển người |
| C3 | `cap-03-tra-cuu-don.md` | Công cụ chỉ đọc tra đơn; kiểm danh tính bằng code; kiểm mọi số/ngày trong nháp khớp dữ liệu |
| C4 | `cap-04-quyet-dinh-va-hanh-dong-ghi.md` | Điều kiện SOP tính bằng code; AI chỉ đề xuất phiếu; người duyệt theo hạn mức; hàm ghi idempotent |
| C5 | `cap-05-chuyen-giao-cho-nguoi.md` | Khi nào chuyển, gói chuyển giao, khiếu nại và khách bực, hạn 03 ngày làm việc |
| C6 | `cap-06-do-luong-va-van-hanh.md` | SSR, hài lòng, sai chính sách, mở lại; chạy lặp (pass^k); phát hành từng phần nhỏ |

Mỗi cấp chạy được độc lập. Dừng ở C1 hoặc C2 vẫn có ích.

## 5. Tái dùng khối nào của nhóm RAG

| Khối | File RAG | Dùng lại ở cấp |
|---|---|---|
| Bản giao việc 6 phần, Sổ prompt, SOP thành prompt | `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` | C0, C1 |
| Gọi API, JSON có cấu trúc, chi phí | `../rag-tra-cuu-tai-lieu/cap-01-goi-api.md` | C2 |
| Tra chính sách có trích dẫn | `../rag-tra-cuu-tai-lieu/cap-05-tra-loi-co-trich-dan.md` | C1, C3 (khi chính sách dài) |
| Bộ ca mẫu, Wilson, kappa, LLM-as-judge | `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` | C0, C6 |
| Function calling, hạng công cụ A-D, injection, MCP | `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` | C3, C4 |
| Workflow, hàng đợi duyệt, gói chuyển giao, tình huống 7.a | `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` | C4, C5 |
| Log, phiên bản, sửa-chạy lại-phát hành, trôi dạt | `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` | C6 |

Nhóm này chỉ viết phần khác biệt: SOP từ ca thật, ý định và mức khẩn, kiểm danh tính khi tra đơn, quyết định bằng code, phiếu hành động, chuyển giao, số đo chăm sóc khách.

## 6. Rủi ro pháp lý và dữ liệu chính

1. **Hứa sai chính sách.** Tòa (Canada) buộc Air Canada bồi thường vì chatbot nói sai chính sách giá vé tang lễ **[Nguồn thứ cấp: CX Today]**. Ở Việt Nam, Luật 19/2023 cấm cung cấp thông tin "sai lệch, không đầy đủ, không chính xác" (Điều 10 khoản 1 điểm a) **[Nguồn: caselaw.vn]**. **[Đề xuất]** Coi mọi câu AI gửi khách là lời của doanh nghiệp.
2. **Lộ đơn của người khác.** Khách gõ mã đơn của người khác. Kiểm danh tính bằng code (C3), không bằng prompt.
3. **Hành động ghi sai, ghi trùng.** Hoàn tiền hai lần do AI thử lại. Hàm idempotent và người duyệt (C4).
4. **Dữ liệu cá nhân của khách** đi qua AI đám mây: xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 4 và 6 (Luật 91/2025, NĐ 356/2025). Luật 19/2023 Điều 17-18 yêu cầu thông báo mục đích và có sự đồng ý khi thu thập, sử dụng thông tin người tiêu dùng **[Nguồn: caselaw.vn]**.
5. **Công khai đang nói chuyện với AI.** Luật 71/2025 Điều 44 (theo tóm tắt) yêu cầu thông báo khi hệ thống AI tương tác trực tiếp với người **[xem file pháp lý chung, mục 4.4]**. Nghiên cứu cũ cho thấy công khai làm giảm mua hàng (C1). **[Đề xuất]** Vẫn công khai; bù bằng chất lượng và chuyển người nhanh.
6. **Khiếu nại.** Luật 19/2023 Điều 31: phải tổ chức tiếp nhận, giải quyết; thông báo đã nhận trong 03 ngày làm việc **[Nguồn: caselaw.vn]**. Khiếu nại luôn có người phụ trách (C5).
7. **Tin gửi chủ động qua Zalo** (ZNS/tin theo mẫu): phải dùng mẫu được duyệt (C1, C5). Chi tiết quy tắc chưa kiểm chứng.

## 7. Danh sách kiểm chứng trước khi xuất bản

- [ ] Đọc bản Công báo Luật 19/2023/QH15: Điều 10, 17, 18, 31, 37, 38; ngoại lệ cho doanh nghiệp siêu nhỏ ở Điều 31.
- [ ] Đọc NĐ 55/2024/NĐ-CP (hướng dẫn Luật 19/2023): có thời hạn giải quyết khiếu nại cụ thể không; quy định giao dịch từ xa.
- [ ] Đọc bản án gốc Moffatt v. Air Canada, 2024 BCCRT 149 trên CanLII (bị 403 khi tải); xác nhận số tiền 812,02 CAD và các lập luận.
- [ ] Đọc bản gốc Luo và cs. (Marketing Science 2019) trước khi trích "giảm hơn 79,7%"; hiện chỉ có tóm tắt.
- [ ] Zalo: quy tắc mẫu tin (ZNS, nay trang ghi "ZBS Template Message"), tiêu chí duyệt, giá. Trang đọc được không có tiêu chí.
- [ ] API chỉ-đọc của KiotViet, Sapo, MISA: chưa đọc tài liệu chính thức. Mới đọc tài liệu Haravan.
- [ ] Kiểm lại các tính năng Project/Gem/GPT tùy chỉnh (xem `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` mục 9).
- [ ] Đo thử phân loại ý định trên tin nhắn tiếng Việt thật (không dấu, viết tắt) của chính doanh nghiệp. Chưa có nguồn đo cho SME Việt Nam.
- [ ] Code mẫu đã chạy bằng hàm giả ở scratchpad; chưa chạy với API thật.
