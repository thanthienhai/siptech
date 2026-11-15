# Nhóm bài: Xử lý yêu cầu khách theo quy trình

> Ngày soạn: 2026-11-11. Thuộc series "AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp".
> Quy ước: **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = suy luận hoặc thiết kế của nhóm soạn. Mọi ngưỡng, cỡ mẫu là [Đề xuất].
> Không phải tư vấn pháp lý. Phần dữ liệu cá nhân dùng chung xem `../an-toan-du-lieu-va-phap-ly-vn.md`.

!!! tip "Tóm tắt nhanh"
    Nhóm bài này dành cho chủ doanh nghiệp nhỏ và nhân viên chăm sóc khách, những người hằng ngày trả lời tin nhắn hỏi đơn, đổi trả, hoàn tiền, khiếu nại. Việc khó ở đây không chỉ là **trả lời** mà là **quyết định và làm** (hoàn tiền, dời lịch, cam kết với khách), nên sai thì doanh nghiệp chịu. Bạn học theo bảy cấp từ C0 đến C6: bắt đầu bằng việc viết quy trình xử lý (SOP) từ các ca đã xảy ra, rồi nhờ AI soạn nháp trả lời cho người duyệt, rồi mới dần thêm phân loại, tra đơn, đề xuất hành động, chuyển người và đo kết quả. Sau cùng bạn có một quy trình xử lý yêu cầu khách rõ ràng, có người duyệt ở những chỗ có hậu quả. Dừng ở cấp nào cũng đã có ích.

## 1. Bài toán

**Ai gặp việc này?** Chủ cửa hàng bán qua mạng, nhân viên chăm sóc khách hàng, người quản lý dịch vụ có lịch hẹn. Nói chung là bất kỳ ai ngày nào cũng ngồi trả lời khách qua tin nhắn.

**Hằng ngày nó trông thế nào?** Khách nhắn qua Zalo, Messenger, email: hỏi đơn ở đâu, muốn đổi size, đòi hoàn tiền, khiếu nại, xin dời lịch hẹn. Với mỗi tin, nhân viên phải (1) hiểu khách muốn gì và gấp tới đâu, (2) tra đơn, (3) đối chiếu chính sách, (4) **quyết định** làm gì, (5) **làm** (tạo phiếu đổi trả, hoàn tiền, dời lịch), (6) trả lời khách, (7) chuyển người khi vượt quyền.

!!! tip "Nói đơn giản"
    Trả lời khách chỉ là bước (6) trong bảy bước. Phần nặng nhất là bước (4) và (5): quyết định đúng và làm đúng. Nhóm bài này giúp bạn đặt AI vào từng bước một cách an toàn, thay vì giao hết cho AI một lần.

**Nhóm bài giúp gì?** Đi từ việc nhỏ nhất (viết ra quy trình mà lâu nay chỉ nằm trong đầu chủ shop) đến việc lớn hơn (AI soạn nháp, phân loại tin, tra đơn, đề xuất phiếu hành động, chuyển người, đo kết quả). Mỗi bước đều có chỗ cho người kiểm trước khi việc có hậu quả đến với khách.

**Điểm khác nhóm RAG** (`../rag-tra-cuu-tai-lieu/`): RAG là cách cho AI tra tài liệu của bạn rồi trả lời. Đầu ra của nhóm RAG là một câu trả lời có trích dẫn. Đầu ra ở đây là **quyết định và hành động có hậu quả** (tiền, lịch, cam kết với khách). Sai một câu trả lời thì sửa được. Hoàn tiền nhầm, hứa sai chính sách thì doanh nghiệp phải chịu.

## 2. Vì sao SME Việt Nam gặp bài toán này

SME là doanh nghiệp nhỏ và vừa. Có bốn lý do khiến bài toán này khó với họ:

- Kênh chính là chat (Zalo OA, tức tài khoản Zalo chính thức của doanh nghiệp; Messenger; sàn TMĐT, tức sàn thương mại điện tử). Tin đến dồn dập, viết tắt, không dấu. **[Đề xuất, quan sát chung; chưa có số liệu VN đo được]**
- Chính sách đổi trả thường chỉ nằm trong đầu chủ shop hoặc rải rác trong tin nhắn cũ. Không có SOP (văn bản ghi rõ từng bước xử lý một loại việc) thì AI không có gì để theo, và **nhân viên mới cũng vậy**.
- Nhân viên đang dán tin khách (có SĐT, địa chỉ) vào ChatGPT cá nhân để "soạn cho nhanh". Đây là "shadow AI", nghĩa là dùng AI ngoài tầm kiểm soát của doanh nghiệp. Xem `../thuc-trang-sme-viet-nam.md` mục 3.2 về shadow AI.
- Có một ca SME Việt kể AI hiểu sai viết tắt, xử lý nhầm đơn **[Nguồn: VCCI/HUBA, lời kể, xem `../thuc-trang-sme-viet-nam.md` mục 3.2]**.

!!! tip "Nói đơn giản"
    Gốc của vấn đề không phải AI kém, mà là quy trình chưa được viết ra. Khi chính sách chỉ nằm trong đầu một người, cả nhân viên mới lẫn AI đều phải đoán. Vì vậy cấp đầu tiên (C0) là viết quy trình ra giấy.

## 3. Bằng chứng tóm tắt

Bảng dưới đây gom các nghiên cứu và nguồn mà cả nhóm bài dựa vào. Bạn không cần đọc hết. Cột giữa là điều chính rút ra, cột cuối cho biết người soạn đã đọc nguồn đó tới đâu. Phần giải thích các từ viết tắt nằm ngay sau bảng.

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

**Các từ viết tắt trong bảng, nói bằng lời thường:**

- **Routine:** một chuỗi bước xử lý cố định mà AI làm theo, viết ra từ SOP.
- **Agent:** một chương trình AI không chỉ trả lời mà còn tự gọi công cụ và làm việc theo các bước.
- **Nhãn nhị phân:** nhãn chỉ có hai giá trị, đúng hoặc sai. "Bộ chấm" là bộ ca mẫu dùng để chấm xem AI làm đúng hay sai.
- **Rollout 1%:** cho một phần rất nhỏ khách dùng thử trước khi mở rộng.
- **tNPS và SSR:** tNPS là điểm khách hài lòng sau một lần trao đổi; SSR là tỉ lệ khách tự giải quyết xong mà không cần gặp nhân viên. Bảng nói hai chỉ số này đánh đổi nhau, tức là tăng cái này có thể làm giảm cái kia.
- **pass^1, pass^8, pass@1:** cách đếm AI làm đúng. Hiểu đơn giản, pass^8 là làm đúng cả tám lần chạy lặp lại cùng một tình huống, nên khó đạt hơn pass^1 là làm đúng một lần.
- **arXiv:** kho đăng bài nghiên cứu miễn phí, mã số đi kèm giúp bạn tìm đúng bài.
- **BVQLNTD:** Bảo vệ quyền lợi người tiêu dùng.

!!! tip "Nói đơn giản"
    Điều đáng nhớ từ bảng: AI làm tốt một lần chưa có nghĩa là làm tốt đều đặn (pass^8 thấp hơn nhiều so với pass^1); bản tiếng Việt thấp hơn bản tiếng Anh; và phần lớn lỗi nằm ở chính sách viết thiếu hoặc quyết định sai, không chỉ ở câu chữ.

Chi tiết số liệu nằm trong từng file cấp.

## 4. Thang cấp độ

Thang này có bảy cấp, đánh số từ C0 đến C6. Cấp sau xây trên cấp trước, nhưng mỗi cấp tự đứng được. Đọc cột "File" để biết bài nào, cột "Một dòng" để biết cấp đó làm gì.

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

**Nên bắt đầu từ cấp nào?** Nếu bạn chưa có quy trình xử lý nào viết ra giấy, bắt đầu từ C0, vì các cấp sau đều dựa vào SOP. Nếu doanh nghiệp đã có SOP rõ ràng, đã viết ra và nhân viên đang làm theo, bạn có thể đọc lướt C0 rồi vào thẳng C1. Cũng vậy với các cấp khác: cấp nào bạn đã làm được và đang chạy ổn thì bỏ qua, chuyển sang cấp tiếp theo khi bạn thật sự cần.

Vài từ trong bảng mà người mới có thể chưa gặp:

- **Project/Gem:** tính năng của Claude (Project) và Gemini (Gem) cho bạn lưu sẵn chỉ dẫn để dùng lại.
- **JSON:** một cách viết thông tin có khung rõ ràng để máy đọc được.
- **Code (mã, chương trình):** phần việc do máy làm theo luật cố định, không phụ thuộc AI "nghĩ". "Luật cứng bằng code đè lên AI" nghĩa là luật nào máy đã tính thì AI không được làm ngược lại.
- **Idempotent:** làm một việc nhiều lần vẫn chỉ ra một kết quả, ví dụ bấm hoàn tiền hai lần vẫn chỉ hoàn một lần.
- **Người duyệt theo hạn mức:** việc nhỏ người có quyền thấp duyệt được, việc tiền lớn thì phải lên người có quyền cao hơn.

!!! tip "Nói đơn giản"
    Bạn không cần làm hết bảy cấp. Với nhiều doanh nghiệp nhỏ, SOP (C0) cộng với AI soạn nháp có người duyệt (C1) đã là bước tiến lớn. Cấp từ C2 trở đi có dùng code, nên cần người biết lập trình hỗ trợ.

## 5. Tái dùng khối nào của nhóm RAG

Nhóm RAG (tra cứu tài liệu) đã dạy sẵn nhiều thứ dùng chung được, nên nhóm này không viết lại. Bảng dưới cho biết khối nào nằm ở file nào và dùng lại ở cấp nào của nhóm này.

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

!!! tip "Nói đơn giản"
    Có thể bạn chưa quen mấy từ trong bảng. API là cách một phần mềm nhờ phần mềm khác làm việc. Function calling và MCP là hai cách cho AI dùng công cụ. Wilson và kappa là hai cách tính cho biết kết quả đo có đáng tin không. LLM-as-judge là dùng một AI để chấm điểm AI khác. Injection là kiểu tấn công nhét lệnh lạ vào nội dung để lừa AI. Log là sổ ghi lại những gì hệ thống đã làm. Bạn chỉ cần mở các file RAG khi đến cấp cần dùng, không phải học trước.

## 6. Rủi ro pháp lý và dữ liệu chính

Bảy rủi ro dưới đây là lý do nhóm bài đặt người duyệt và code kiểm ở những chỗ nhất định. Đây không phải tư vấn pháp lý.

1. **Hứa sai chính sách.** Tòa (Canada) buộc Air Canada bồi thường vì chatbot nói sai chính sách giá vé tang lễ **[Nguồn thứ cấp: CX Today]**. Ở Việt Nam, Luật 19/2023 cấm cung cấp thông tin "sai lệch, không đầy đủ, không chính xác" (Điều 10 khoản 1 điểm a) **[Nguồn: caselaw.vn]**. **[Đề xuất]** Coi mọi câu AI gửi khách là lời của doanh nghiệp.
2. **Lộ đơn của người khác.** Khách gõ mã đơn của người khác. Kiểm danh tính bằng code (C3), không bằng prompt (prompt là đoạn chỉ dẫn bạn viết cho AI).
3. **Hành động ghi sai, ghi trùng.** Hoàn tiền hai lần do AI thử lại. Hàm idempotent (làm lại cũng chỉ ra một kết quả) và người duyệt (C4).
4. **Dữ liệu cá nhân của khách** đi qua AI đám mây (AI chạy trên máy chủ của nhà cung cấp, không chạy trên máy bạn): xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 4 và 6 (Luật 91/2025, NĐ 356/2025). Luật 19/2023 Điều 17-18 yêu cầu thông báo mục đích và có sự đồng ý khi thu thập, sử dụng thông tin người tiêu dùng **[Nguồn: caselaw.vn]**.
5. **Công khai đang nói chuyện với AI.** Luật 71/2025 Điều 44 (theo tóm tắt) yêu cầu thông báo khi hệ thống AI tương tác trực tiếp với người **[xem file pháp lý chung, mục 4.4]**. Nghiên cứu cũ cho thấy công khai làm giảm mua hàng (C1). **[Đề xuất]** Vẫn công khai; bù bằng chất lượng và chuyển người nhanh.
6. **Khiếu nại.** Luật 19/2023 Điều 31: phải tổ chức tiếp nhận, giải quyết; thông báo đã nhận trong 03 ngày làm việc **[Nguồn: caselaw.vn]**. Khiếu nại luôn có người phụ trách (C5).
7. **Tin gửi chủ động qua Zalo** (ZNS/tin theo mẫu): phải dùng mẫu được duyệt (C1, C5). Chi tiết quy tắc chưa kiểm chứng.

!!! tip "Nói đơn giản"
    Gộp lại thành một nguyên tắc: AI gửi gì cho khách thì doanh nghiệp chịu trách nhiệm như chính nhân viên gửi. Vì thế những việc có hậu quả (tiền, lịch, khiếu nại, dữ liệu cá nhân) nên có người duyệt hoặc có code kiểm, đừng chỉ dựa vào lời dặn trong prompt.

!!! warning "Cẩn thận"
    Các điều luật ở trên chỉ để bạn biết có vấn đề cần hỏi chuyên gia, không phải tư vấn pháp lý. Một số điều còn ghi "theo tóm tắt" hoặc "chưa kiểm chứng". Xem mục 7 bên dưới để biết cái gì chưa được đọc bản gốc.

## 7. Danh sách kiểm chứng trước khi xuất bản

Đây là danh sách những điều nhóm soạn chưa đối chiếu xong với bản gốc. Chúng được giữ lại để bạn biết chỗ nào nên dè dặt khi dùng. Ô nào chưa đánh dấu là việc chưa làm.

- [ ] Đọc bản Công báo Luật 19/2023/QH15: Điều 10, 17, 18, 31, 37, 38; ngoại lệ cho doanh nghiệp siêu nhỏ ở Điều 31.
- [ ] Đọc NĐ 55/2024/NĐ-CP (hướng dẫn Luật 19/2023): có thời hạn giải quyết khiếu nại cụ thể không; quy định giao dịch từ xa.
- [ ] Đọc bản án gốc Moffatt v. Air Canada, 2024 BCCRT 149 trên CanLII (bị 403 khi tải); xác nhận số tiền 812,02 CAD và các lập luận.
- [ ] Đọc bản gốc Luo và cs. (Marketing Science 2019) trước khi trích "giảm hơn 79,7%"; hiện chỉ có tóm tắt.
- [ ] Zalo: quy tắc mẫu tin (ZNS, nay trang ghi "ZBS Template Message"), tiêu chí duyệt, giá. Trang đọc được không có tiêu chí.
- [ ] API chỉ-đọc của KiotViet, Sapo, MISA: chưa đọc tài liệu chính thức. Mới đọc tài liệu Haravan.
- [ ] Kiểm lại các tính năng Project/Gem/GPT tùy chỉnh (xem `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` mục 9).
- [ ] Đo thử phân loại ý định trên tin nhắn tiếng Việt thật (không dấu, viết tắt) của chính doanh nghiệp. Chưa có nguồn đo cho SME Việt Nam.
- [ ] Code mẫu đã chạy bằng hàm giả ở scratchpad; chưa chạy với API thật.

!!! tip "Nói đơn giản"
    Hai điều cần nhớ từ danh sách này. Một là các con số và điều luật trong nhóm bài chưa phải cái nào cũng được đọc từ bản gốc, nên hãy kiểm lại trước khi dùng cho việc quan trọng. Hai là chưa có số đo nào cho tin nhắn tiếng Việt thật của doanh nghiệp bạn, nên khi dùng AI phân loại tin, hãy tự thử trên tin nhắn của chính bạn.
