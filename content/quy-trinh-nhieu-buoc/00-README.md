# Nhóm bài: Tự động hóa quy trình nghiệp vụ nhiều bước

Ngày soạn: 2026-11-11. Quy ước giống cả series: **[Nguồn]** là điều tài liệu nói; **[Đề xuất]** là suy luận hoặc thiết kế của nhóm soạn, chưa được kiểm chứng. Ngưỡng và cỡ mẫu do nhóm đặt ra đều là [Đề xuất].

!!! tip "Tóm tắt nhanh"
    Nhóm bài này dành cho người trong công ty hay phải chuyển một việc qua nhiều người và nhiều phần mềm (đơn hàng, đề nghị thanh toán, hồ sơ tuyển dụng, báo cáo tuần). Bạn sẽ học cách vẽ lại quy trình đang chạy, chọn bước nào để người làm, bước nào chỉ cần tự động hóa thường, bước nào mới đáng giao cho AI. Học theo thứ tự cấp Q0 đến Q6: vẽ và đo nền, tự động hóa bằng quy tắc, phân loại và chuyển đúng người, báo cáo định kỳ, chuỗi bước có điểm duyệt, xử lý lỗi, rồi đo hiệu quả. Sau cùng bạn có bộ bảng đo, các luồng chạy thật và một biên bản quyết định làm tiếp, thu hẹp hay dừng. Không bắt buộc đi hết các cấp.

## 1. Bài toán

**Ai gặp việc này?** Chủ doanh nghiệp nhỏ, quản lý, kế toán, nhân sự, nhân viên kho hay bán hàng, tức là bất kỳ ai có công việc phải đi qua tay nhiều người và nhiều công cụ. Bạn không cần biết lập trình.

**Hàng ngày nó trông thế nào?** Một việc trong công ty đi qua nhiều người và nhiều hệ thống (hệ thống ở đây là phần mềm hoặc nơi lưu dữ liệu, như Zalo, Google Sheets, phần mềm bán hàng, phần mềm kế toán). Ví dụ:

- Đơn hàng từ Zalo vào phần mềm bán hàng rồi sang kho.
- Đề nghị thanh toán từ nhân viên lên trưởng phòng rồi sang kế toán.
- CV từ email sang người phỏng vấn.
- Số bán hàng từ Sheets thành báo cáo tuần.

Ở mỗi chỗ chuyển tay, việc dễ chậm, dễ mất, hoặc bị nhập sai.

**Nhóm bài giúp gì?** Nhóm bài này dạy:

1. Vẽ quy trình đang chạy thật (dù chưa có văn bản), đo nền. ("Đo nền" là đo tình trạng hiện tại, như mất bao lâu, sai bao nhiêu lần, để sau này có cái mà so.)
2. Chọn bước nào giữ người, bước nào chỉ cần tự động hóa thường (quy tắc, công thức, kịch bản), bước nào mới đáng giao cho AI.
3. Phân loại và định tuyến yêu cầu đến đúng người. ("Định tuyến" là chuyển yêu cầu đến đúng nơi xử lý.)
4. Tổng hợp báo cáo định kỳ và phân tích bảng tính mà không để AI tính sai.
5. Dựng chuỗi bước có điểm duyệt cho đơn hàng, đề nghị thanh toán, tuyển dụng. ("Điểm duyệt" là chỗ dừng lại để người xem và bấm đồng ý trước khi việc đi tiếp.)
6. Xử lý lỗi, thử lại, chống chạy trùng.
7. Đo trước/sau để quyết định có đáng làm không.

**Nguyên tắc xuyên suốt:** không phải bước nào cũng cần AI. Nhiều bước làm bằng quy tắc hoặc automation thường rẻ hơn, nhanh hơn, và chắc hơn. (Automation là việc để máy tự làm theo luật đã đặt sẵn, ví dụ "có đơn mới thì tự thêm một dòng vào bảng".)

!!! tip "Nói đơn giản"
    Trước khi nghĩ đến AI, hãy nhìn xem việc của bạn đi qua những đâu. Có bước chỉ cần một công thức hoặc một luật cố định là xong. AI chỉ nên được giao những bước khó viết thành luật.

**Khác gì `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md`:** ở đó quy trình là phần mở rộng của hệ tra cứu tài liệu (workflow vs agent, 5 mẫu workflow, điểm duyệt, gói chuyển giao, trần bước). Ở đây **quy trình nghiệp vụ là đối tượng chính**; phần lớn bước không dùng AI. Nhóm này không viết lại các khái niệm đó mà tham chiếu. (Workflow là chuỗi bước cố định, đi theo đường đã vẽ sẵn. Agent là AI tự quyết bước tiếp theo.)

## 2. Vì sao SME Việt Nam gặp bài toán này

SME là doanh nghiệp nhỏ và vừa. Dưới đây là bốn lý do, mỗi lý do có nhãn cho biết đó là điều tài liệu nói hay là quan sát của nhóm soạn.

- **[Nguồn, gián tiếp]** Phần lớn doanh nghiệp Việt Nam dùng AI còn ở giai đoạn thăm dò (74% theo AWS/Strand, qua báo chí); rào cản lặp lại là kỹ năng, chi phí, dữ liệu rời rạc (`../thuc-trang-sme-viet-nam.md`).
- **[Đề xuất, quan sát]** Quy trình nằm trong đầu người làm lâu năm. Dữ liệu rải ở Zalo, Sheets, phần mềm bán hàng, phần mềm kế toán. Người dùng chép qua chép lại bằng tay, rồi dán vào chatbot để "nhờ AI làm cho nhanh".
- **[Nguồn]** Một doanh nghiệp Việt kể AI hiểu sai viết tắt địa phương, xử lý nhầm đơn, doanh thu có lúc giảm tới 50% khi thử (lời kể tại hội nghị, một trường hợp; `../thuc-trang-sme-viet-nam.md` mục 3.2).
- **[Đề xuất]** Phần mềm SME đang dùng phần lớn đã có cửa mở cho tự động hóa thường (API, webhook, automation có sẵn), nên bước đầu tiên thường không cần AI. Xem mục 5.

!!! tip "Nói đơn giản"
    API và webhook là "cửa" để một phần mềm nói chuyện với phần mềm khác mà không cần người chép tay. API là cửa để hỏi hoặc ra lệnh, webhook là cửa để phần mềm tự báo khi có việc mới. Nếu phần mềm bạn dùng đã có sẵn các cửa này thì việc nối chúng lại thường không cần đến AI.

## 3. Bằng chứng tóm tắt

Chi tiết và mức tin cậy ở mục 8 của từng file cấp. Nguồn **đọc toàn văn hoặc các mục chính** đánh dấu (TV); nguồn chỉ đọc tóm tắt đánh dấu (TT).

Bảng dưới là các nghiên cứu mà nhóm bài dựa vào. Bạn không cần đọc kỹ từng số. Hãy đọc cột cuối ("Hàm ý cho nhóm này") để biết mỗi nghiên cứu dẫn đến quy tắc làm việc nào. Một vài từ viết tắt trong bảng: "agent" là AI tự quyết bước tiếp theo; "RPA" là phần mềm làm thay các thao tác lặp lại trên màn hình theo kịch bản cố định; "pass^1", "pass^8" là tỷ lệ làm đúng ở lần chạy thứ nhất và khi phải đúng liên tiếp tám lần.

| Nguồn | Điều nói | Hàm ý cho nhóm này [Đề xuất] |
|---|---|---|
| MAP, arXiv 2512.04123 (TV, nhóm trước đã đọc) | 68% hệ thống chạy ≤10 bước rồi chuyển người; 16/20 ca dùng workflow có cấu trúc; 15/20 chạy bất đồng bộ; 66% chấp nhận trễ cỡ phút; 74% đánh giá bằng người | Chuỗi ngắn, cố định, chạy nền, người duyệt là chuẩn thực tế, không phải giải pháp tạm |
| TheAgentCompany, arXiv 2412.14161 (TV các mục kết quả) | 175 việc văn phòng giả lập; agent tốt nhất (Gemini 2.5 Pro) hoàn thành trọn 30,3%, trung bình 27,2 bước, khoảng 4,2 USD/việc; nhóm việc Admin 13,33%, Finance 8,33%, DS 14,29% thành công | Việc hành chính, tài chính, bảng tính là chỗ agent tự do yếu nhất; đừng giao trọn cho agent |
| τ-bench, arXiv 2406.12045 (TV) | gpt-4o pass^1 khoảng 61% (bán lẻ), 35% (hàng không); pass^8 dưới 25% ở bán lẻ; khoảng 55% lỗi là sai tham số/sai thông tin (kể cả tính sai tổng tiền) | Chạy nhiều lần cùng một việc không ra cùng kết quả; hành động ghi phải có cổng kiểm |
| READY, arXiv 2609.02095 (TT + các mục chính) | Hai hệ chênh 0,3 điểm phần trăm độ chính xác (72,8% và 72,5%) nhưng cần 39,2% và 29,6% số ca qua người duyệt để đạt cùng mục tiêu 76% | Câu hỏi đúng là "cần bao nhiêu người duyệt để đạt độ tin cậy X", không phải "AI đúng bao nhiêu %" |
| SpreadsheetBench 2, arXiv 2606.29955 (TV các mục kết quả) | 321 việc bảng tính doanh nghiệp; tốt nhất 34,89% đúng trọn việc, sửa lỗi bảng tính chỉ 12%; lỗi chính: xem chưa đủ (42,3%), sửa nhầm ô (32,9%) | Không để AI sửa trực tiếp bảng tính thật; AI đề xuất, code hoặc người áp |
| TrustDABench, arXiv 2608.24145 (TV các mục kết quả) | Khi dữ liệu thiếu/mâu thuẫn (không thể trả lời đúng), điểm từ chối trung bình (MRS) cao nhất chỉ 24,21% (GPT-5.5); ngay cả mô hình này không từ chối hợp lệ ở khoảng 2/3 số ca; 74,8% ca lỗi là "trả lời im lặng không có căn cứ"; dữ liệu mâu thuẫn gần như không bị phát hiện | Kiểm dữ liệu (trùng, thiếu, mâu thuẫn) bằng code trước khi đưa AI |
| Data referencing errors, arXiv 2606.32029 (TV) | Mô hình 1,7B-20B trích nhầm/bỏ sót giá trị bảng ở 5,71%-46,48% câu trả lời; nhắc trong prompt "đừng trích sai" không giải quyết | Hàng rào bằng prompt không đủ; cần đối chiếu số bằng code |
| RPA vs agent, arXiv 2509.04198 (TV) | RPA (UiPath) 10/10 lần thành công ở cả 3 bài; agent dùng máy tính 0/1, 9/10, 6/10 và chậm hơn; nhưng dựng nhanh hơn (≈15 phút so với ≈240 phút ở bài hóa đơn) | Bước lặp, ổn định: dùng automation thường. AI hợp cho thử nhanh và bước khó viết luật |
| Samsung SDS, arXiv 2505.20733 (TV các mục kết quả) | 1.448 hóa đơn giấy: độ chính xác 0,83, precision 1, recall 0,82; 242 ca hệ thống từ chối nhưng người duyệt chấp nhận | Thiết kế "nghi thì chuyển người" làm số ca qua người tăng; tính công này vào chi phí. Số "giảm 80-90% thời gian" là "hiệu quả kỳ vọng", nhà cung cấp tự báo |
| Dell'Acqua và cs., HBS WP 24-013 (TT, chỉ qua tóm tắt tìm kiếm) | 758 tư vấn viên, thử nghiệm ngẫu nhiên: việc "trong vùng" làm thêm 12,2% việc, nhanh 25,1%; việc "ngoài vùng" đúng ít hơn 19 điểm phần trăm | Cùng một công cụ có thể làm tốt hơn ở việc này và tệ hơn ở việc kia; phải đo theo từng việc |
| Brynjolfsson, Li, Raymond, NBER 31161 (TT, `../thuc-trang-sme-viet-nam.md`) | 5.179 nhân viên CSKH: năng suất +14% trung bình, +34% người mới, gần như không đổi với người giỏi | Đo theo nhóm người dùng, không chỉ trung bình |

!!! tip "Nói đơn giản"
    Điểm chung của các nghiên cứu: AI làm một việc đơn lẻ có thể khá tốt, nhưng khi phải làm cả một chuỗi việc văn phòng thì hay sai, và mỗi lần chạy lại có thể ra một kết quả khác. Vì vậy ta giữ chuỗi ngắn, để máy làm các bước cố định, và để người duyệt ở những chỗ quan trọng.

## 4. Thang cấp độ của nhóm

Nhóm bài chia thành bảy cấp, từ Q0 đến Q6. Cấp sau dựa trên cấp trước, nhưng mỗi cấp đều cho ra một thứ chạy được.

| Cấp | File | Một dòng | Thứ chạy được ở cấp này |
|---|---|---|---|
| Q0 | `cap-00-ve-quy-trinh-va-do-nen.md` | Vẽ quy trình đang chạy, gán nhãn Người / Quy tắc / AI, đo nền | Bảng quy trình + bảng đo nền 2 tuần |
| Q1 | `cap-01-tu-dong-hoa-thuong.md` | Tự động hóa bằng quy tắc, không AI: biểu mẫu, chuyển dữ liệu, nhắc việc | Một luồng Sheets/Apps Script hoặc Lark Base/Make/n8n chạy hằng ngày |
| Q2 | `cap-02-phan-loai-dinh-tuyen.md` | Phân loại và định tuyến: quy tắc trước, AI sau, "không chắc" về người | Bộ định tuyến + bộ 50 ca có đáp án |
| Q3 | `cap-03-bao-cao-dinh-ky-va-so-lieu.md` | Báo cáo định kỳ: code tính số, AI viết lời, mọi con số đối chiếu bằng code | Báo cáo tuần tự sinh, có người duyệt trước khi gửi |
| Q4 | `cap-04-chuoi-buoc-co-diem-duyet.md` | Chuỗi bước có trạng thái và điểm duyệt: đơn hàng, đề nghị thanh toán, tuyển dụng | Một quy trình chạy trên phiếu thật, có nhật ký và hàng đợi duyệt |
| Q5 | `cap-05-loi-thu-lai-chong-trung.md` | Webhook, thử lại có giới hạn, chống chạy trùng, hàng lỗi | Bộ xử lý sự kiện qua 6 ca hỏng có chủ đích |
| Q6 | `cap-06-do-hieu-qua-va-quyet-dinh.md` | Đo trước/sau (thời gian, lỗi, chi phí), tính hoàn vốn, quyết định làm tiếp/thu hẹp/dừng | Bảng đo 4 tuần + biên bản quyết định |

Mỗi cấp chạy được độc lập. Một công ty có thể dừng ở Q1 và vẫn có lợi. Không bắt buộc đi hết.

**Nên bắt đầu từ cấp nào?** Nếu bạn chưa từng vẽ lại quy trình của mình, hãy bắt đầu từ Q0. Đó là cấp nền: nó cho bạn bức tranh và con số hiện tại để các cấp sau có cái mà so. Nếu bạn đã có sơ đồ quy trình và đã biết mỗi việc mất bao lâu, bạn có thể bỏ qua Q0 và vào thẳng Q1. Nếu bạn đã tự động hóa được các bước cố định (Q1) và đã tự chuyển được yêu cầu đến đúng người (Q2), bạn có thể bỏ qua hai cấp đó và nhảy tới cấp bạn đang thiếu. Riêng Q6 (đo hiệu quả) nên làm ở cuối, vì nó cần số liệu của các cấp trước.

!!! tip "Nói đơn giản"
    Hãy xem mỗi cấp như một bậc thang, nhưng bạn không phải leo từ bậc thấp nhất nếu đã đứng sẵn ở bậc cao hơn. Làm được điều cấp đó dạy thì bỏ qua, chưa làm được thì bắt đầu từ đó. Dừng lại ở bậc nào đã đủ lợi cũng là một lựa chọn tốt.

## 5. Bối cảnh công cụ ở Việt Nam (đã tra 2026-11-11, hay đổi)

Bảng dưới liệt kê các công cụ phổ biến ở Việt Nam và điều nhóm soạn đã kiểm tra được về khả năng nối chúng với nhau. Phần "chưa xác minh" hoặc "chưa kiểm chứng" nghĩa là nhóm soạn chưa tìm thấy hoặc chưa đọc tài liệu chính thức, nên đừng coi đó là thông tin chắc chắn. Giá và giới hạn thay đổi thường xuyên, hãy mở trang chính thức của từng công cụ trước khi quyết định.

| Công cụ | Điều đã xác minh | Mức |
|---|---|---|
| Google Apps Script | Mỗi lần chạy tối đa 6 phút; tổng thời gian trigger 90 phút/ngày (gmail) hoặc 6 giờ/ngày (Workspace); 20 trigger/người/script; UrlFetch 20.000/ngày (gmail), 100.000/ngày (Workspace). Có `LockService` chống chạy đồng thời | Trang chính thức |
| KiotViet | Có Public API: đơn đặt hàng, hóa đơn, hàng hóa, khách hàng (đọc/tạo/sửa/hủy); chỉ tài khoản admin thấy mã API, lấy ở Thiết lập → Cửa hàng → Kết nối API. Có trang "thiết lập webhook" (bản Hotel); webhook bản bán lẻ, gói cước, giới hạn tốc độ **chưa xác minh** | Trang hướng dẫn chính thức |
| Haravan | Webhook có chữ ký HMAC (`X-Haravan-Hmacsha256`); chờ phản hồi 5 giây; không trả 200 thì gửi lại 19 lần trong 48 giờ; 19 lần lỗi liền thì tự xóa đăng ký | Tài liệu chính thức |
| Sapo | **Chưa tìm được** tài liệu API/webhook chính thức trong phiên này | Chưa kiểm chứng |
| MISA AMIS Kế toán | Có thiết lập "Cho phép đẩy dữ liệu từ phần mềm khác qua kết nối API"; tạo chứng từ kho, đơn mua hàng qua API (R21); đồng bộ phiếu xuất kho ra ngoài (R23). Tài liệu endpoint cho kế toán và meInvoice **chưa đọc** | Trang trợ giúp chính thức (2021-2023) |
| Lark | Base có automation kích hoạt bằng webhook (mỗi luồng tối đa 5 sự kiện/giây, mỗi Base 50/giây, 4 MB/yêu cầu, Bearer token); có Approval API v4 và sự kiện thay đổi trạng thái phê duyệt | Trợ giúp chính thức (Base); Approval qua tài liệu thứ cấp |
| Zalo OA / ZNS | Gửi tin giao dịch qua API máy chủ; tên gọi có thể đã đổi sang ZBS; hạn mức OA mới, đơn giá theo tin chỉ thấy qua bên tích hợp | Chưa kiểm chứng trên developers.zalo.me |
| Make | Gói miễn phí 1.000 operations/tháng, 2 scenario hoạt động, chu kỳ tối thiểu 15 phút; mỗi module chạy tính 1 operation | Trang giá chính thức qua tóm tắt tìm kiếm |
| n8n tự host | Bản Community (Sustainable Use License) miễn phí khi chỉ người trong tổ chức tạo/sửa workflow; cấm bán lại n8n như dịch vụ | Trang FAQ giấy phép chính thức |

!!! tip "Nói đơn giản"
    Bảng này trả lời câu hỏi "phần mềm tôi đang dùng có cho máy tự nối vào không". Với những dòng ghi "chưa xác minh", cách an toàn là hỏi nhà cung cấp phần mềm hoặc nhờ người biết kỹ thuật kiểm tra giúp, trước khi lên kế hoạch dựa vào chúng.

## 6. Tái dùng khối nào của nhóm RAG

RAG là cách cho AI tra cứu trong tài liệu của bạn rồi mới trả lời. Nhóm bài RAG đã viết sẵn nhiều khối nền (cách giao việc cho AI, cách gọi AI qua API, cách đo kết quả, cách cho AI dùng công cụ, cách vận hành). Nhóm này không viết lại mà dùng lại, theo bảng dưới.

| Cần | Dùng lại | Ghi chú cho nhóm này |
|---|---|---|
| Bản giao việc, SOP thành prompt | `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` | Dùng ở Q0 khi chép quy trình |
| Gọi API, JSON có cấu trúc, chi phí token, thử lại khi lỗi API | `../rag-tra-cuu-tai-lieu/cap-01-goi-api.md` | Q2 trở đi |
| Bộ ca có đáp án, khoảng tin cậy khi n nhỏ, đo thời gian | `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` | Q0 (đo nền), Q2, Q6 |
| Hàm đọc/ghi, phân hạng A-D, idempotent, injection | `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` | Q4, Q5 |
| Workflow vs agent, điểm duyệt, gói chuyển giao, trần bước | `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` | Q4 |
| Log, phiên bản prompt, trôi dạt, sổ sự cố | `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` | Q5, Q6 |
| Tra cứu chính sách/bảng giá khi một bước cần căn cứ | `../rag-tra-cuu-tai-lieu/cap-04-tim-kiem.md`, `cap-05-tra-loi-co-trich-dan.md` | Khi một bước cần trích văn bản |

Một vài thuật ngữ trong bảng: "SOP" là tài liệu hướng dẫn quy trình chuẩn của công ty; "prompt" là câu lệnh bạn gõ cho AI; "JSON" là cách viết dữ liệu có khung rõ ràng để máy đọc được; "token" là đơn vị AI dùng để đếm chữ và tính tiền; "idempotent" là tính chất của một thao tác mà chạy hai lần cũng chỉ cho kết quả như chạy một lần (ví dụ không tạo hai đơn trùng); "injection" là kiểu tấn công nhét lệnh lạ vào dữ liệu để đánh lừa AI; "log" là nhật ký ghi lại những gì hệ thống đã làm.

Các nhóm khác, chỉ nhắc, không đi sâu: soạn trả lời khách (`../xu-ly-yeu-cau-khach/00-README.md`), kiểm chứng từ theo quy tắc (`../kiem-tra-ho-so-theo-quy-tac/00-README.md`), tóm tắt họp và SOP (`../tri-thuc-to-chuc/00-README.md`).

## 7. Rủi ro pháp lý và dữ liệu chính

Không phải tư vấn pháp lý. Nền tảng ở `../an-toan-du-lieu-va-phap-ly-vn.md`.

Khi một việc chạy qua nhiều phần mềm, dữ liệu của khách hàng và nhân viên cũng đi qua nhiều nơi. Sáu điểm dưới đây là những chỗ cần để ý nhất.

1. **Dữ liệu cá nhân chạy qua nhiều dịch vụ.** Một luồng đơn hàng có thể đi qua Zalo, Make (máy chủ nước ngoài), API mô hình (nước ngoài), Sheets. Mỗi chặng có thể là chuyển dữ liệu cá nhân ra nước ngoài theo Luật 91/2025/QH15 và NĐ 356/2025 (số điều cụ thể còn lệch giữa các nguồn, xem file nền mục 4). **[Đề xuất]** Vẽ "bản đồ dữ liệu" ở Q0: mỗi bước, dữ liệu gì, đi đâu, lưu bao lâu.
2. **Tuyển dụng.** CV là dữ liệu cá nhân; quyết định loại/nhận ảnh hưởng quyền lợi người lao động. **[Đề xuất]** AI chỉ trích trường và xếp hàng đợi; người quyết định loại. Luật AI 134/2025 nêu giám sát con người với quyết định quan trọng và lao động là lĩnh vực rủi ro cao hơn (nguồn báo chí, chưa đọc toàn văn).
3. **Thanh toán.** Không có công cụ chi tiền trong luồng AI (hạng D ở `cap-07`). Lệnh chi do người làm trên hệ thống ngân hàng.
4. **Nơi lưu và nhật ký.** Log của Make/n8n/Apps Script chứa dữ liệu thật. **[Đề xuất]** Che trước khi ghi, đặt thời hạn xóa, phân quyền xem.
5. **Tài khoản và khóa API.** Một khóa API KiotViet/Haravan cho phép đọc toàn bộ khách hàng. Cất trong kho bí mật của nền tảng, không dán vào kịch bản dùng chung. (Khóa API giống một chìa khóa: ai cầm được nó là có quyền như bạn.)
6. **Miễn trừ cho doanh nghiệp nhỏ** (Điều 38 Luật 91 theo tóm tắt) chỉ miễn một số điều và không áp dụng khi xử lý dữ liệu nhạy cảm hoặc số lượng lớn; NĐ 356 theo EY nêu ngưỡng 100.000 chủ thể. Cần luật sư xác nhận cho từng công ty.

!!! tip "Nói đơn giản"
    Ba quy tắc dễ nhớ: đừng để AI tự chi tiền; để người quyết định những việc ảnh hưởng đến quyền lợi người khác (như loại hay nhận một ứng viên); và đừng dán khóa truy cập vào nơi nhiều người cùng xem được.

## 8. Danh sách kiểm chứng trước khi xuất bản

Đây là danh sách việc nhóm soạn còn phải kiểm lại trước khi coi nhóm bài là hoàn chỉnh. Nó cũng cho bạn biết những chỗ nào trong nhóm bài còn chưa chắc.

- [ ] Đọc toàn văn bài Dell'Acqua và cs. (SSRN 4573321) để xác nhận 12,2%, 25,1%, 19 điểm phần trăm, n=758 (hiện chỉ qua tóm tắt tìm kiếm).
- [ ] Đọc lại READY mục 5 (bảng kết quả 16 hệ) nếu dùng thêm số ngoài cặp 72,8%/72,5%.
- [ ] Mở trang KiotViet "Hướng dẫn sử dụng Public API": cách xác thực, webhook bản bán lẻ, giới hạn tốc độ, gói cước nào có API.
- [ ] Tìm tài liệu API/webhook chính thức của Sapo; nếu không có, ghi rõ trong bài.
- [ ] Đọc tài liệu endpoint MISA AMIS Kế toán và MISA meInvoice; xác nhận còn hiệu lực.
- [ ] Đối chiếu developers.zalo.me: tên ZNS/ZBS, đơn giá, hạn mức OA mới, điều kiện webhook.
- [ ] Đọc trang chính thức Lark Approval v4 (tạo phiếu, sự kiện), và nơi lưu dữ liệu của Lark cho khách Việt Nam.
- [ ] Mở trang giá Make, Zapier tại ngày xuất bản; không ghi giá cố định trong bài.
- [ ] Kiểm pháp lý bằng văn bản gốc (mục 7) với luật sư, nhất là ca tuyển dụng.
- [ ] Chạy lại 4 đoạn code mẫu (scratchpad, `python -I`) sau khi chỉnh; nối API thật trên dữ liệu thử, không dùng dữ liệu khách.
- [ ] Thay mọi ví dụ giả định (số phút, số phiếu, lương giờ) bằng số đo thật từ ít nhất một doanh nghiệp thử, ghi rõ cỡ mẫu.
