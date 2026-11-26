date: 2026-11-11

# Dùng AI mà không làm lộ dữ liệu: quy tắc an toàn và khung pháp lý Việt Nam

Nhân viên dán hợp đồng vào ChatGPT, kế toán tải sao kê lên một công cụ "AI miễn phí", giám đốc để API key trong tin nhắn Zalo. Những việc đó diễn ra mỗi ngày, và đều có thể làm lộ dữ liệu của khách hàng lẫn của chính công ty. Bài này dành cho chủ SME và người phụ trách IT, kế toán, nhân sự ở Việt Nam đang dùng ChatGPT, Claude hay Gemini. Sau khi đọc, bạn có: bảng quy tắc "được đưa vào AI, không được đưa vào AI"; cách kiểm cài đặt huấn luyện của từng dịch vụ; bức tranh khung luật Việt Nam đang hiệu lực; và kế hoạch xử lý shadow AI.

!!! warning "Đây không phải tư vấn pháp lý"
    Bài là tổng hợp từ nguồn công khai, phần lớn là nguồn thứ cấp (trang pháp luật, hãng tư vấn, báo chí). SIPTech **chưa đọc được toàn văn** các luật và nghị định gốc. Trước khi ra quyết định có hậu quả pháp lý (chuyển dữ liệu ra nước ngoài, xử lý dữ liệu nhạy cảm, triển khai với khách hàng), hãy đọc văn bản gốc và hỏi luật sư. Mỗi mục pháp lý có nhãn mức xác minh: [[v:ok]] (từ hai nguồn trở lên), [[v:part]], [[v:no]]. Ngày tra cứu: 11/11/2026.

## Vì sao mọi cấp của series đều cần bài này

- **C0 (dùng AI thủ công)** làm lộ dữ liệu nhanh nhất: dán vào chat bằng tài khoản cá nhân.
- **C1 (gọi API)** đưa dữ liệu đi hàng loạt qua khóa API, nên lỗi quy tắc nhân lên theo số lần gọi.
- **C2 đến C5 (tài liệu, lập chỉ mục, tìm kiếm)** tạo kho dữ liệu mới: bản trích văn bản và chỉ mục vector vẫn là dữ liệu cá nhân nếu chứa dữ liệu cá nhân (đề xuất của SIPTech).
- **C7 đến C9 (công cụ, quy trình, vận hành)** cho AI quyền hành động, nên cần phân quyền và nhật ký.

## Dữ liệu nào được đưa vào AI?

!!! proposal "Đề xuất của SIPTech, không phải trích luật"
    Bảng phân loại dưới đây là nguyên tắc bền để quyết định. Danh sách loại dữ liệu nhạy cảm do luật quy định: xem phần khung pháp lý về thay đổi giữa Nghị định 13 và Nghị định 356.

| Mức | Ví dụ | Với AI công cộng (tài khoản cá nhân, miễn phí) | Với gói doanh nghiệp hoặc API trả phí |
|---|---|---|---|
| Công khai | Bảng giá niêm yết, bài đăng website | Được | Được |
| Nội bộ thường | Quy trình, mẫu biểu không có tên người | Hạn chế; nên ẩn tên công ty và đối tác | Được, theo quy tắc công ty |
| Bí mật kinh doanh | Giá vốn, hợp đồng, công thức, mã nguồn, báo cáo tài chính chưa công bố | Không | Chỉ khi đã đọc điều khoản dữ liệu và có người duyệt |
| Dữ liệu cá nhân | Họ tên kèm số điện thoại, địa chỉ, email khách hoặc nhân viên, CV | Không | Chỉ khi có cơ sở pháp lý, đã ẩn danh nếu có thể, đã kiểm tra việc chuyển ra nước ngoài |
| Dữ liệu cá nhân nhạy cảm | Sức khỏe, sinh trắc học, giao dịch ngân hàng, định vị, CCCD | Không (mặc định) | Mặc định không đưa vào; chỉ khi có tư vấn pháp lý |

### Ẩn danh trước khi gửi

!!! proposal "Đề xuất của SIPTech"
    1. Thay tên người, số điện thoại, email, địa chỉ chi tiết, số tài khoản, mã số thuế, số CCCD bằng mã (ví dụ `KH_001`). Giữ bảng tra ngược **ở máy công ty**, không gửi đi.
    2. Rút gọn thông tin gián tiếp có thể nhận ra người (ngày sinh đầy đủ, chức danh hiếm kèm nơi làm).
    3. Có bước kiểm tự động (biểu thức chính quy cho số điện thoại, email, CCCD) trước khi gửi; chặn nếu còn sót.
    4. Dữ liệu đã giả danh nhưng còn bảng tra ngược vẫn có thể bị coi là dữ liệu cá nhân; ẩn danh thực sự (không thể xác định lại) khó hơn nhiều.

Nghị định 356 có điều khoản yêu cầu **khử nhận dạng** cho một số hình thức trao đổi dữ liệu, theo tóm tắt của EY [[S2]].

### Những đường rò rỉ hay gặp

- Dán dữ liệu vào tài khoản cá nhân hoặc miễn phí có thể bị dùng để cải thiện mô hình (xem phần dịch vụ AI bên dưới).
- Lịch sử chat, tệp tải lên và bộ nhớ (memory) được lưu lại, và hiện ra với người dùng sau trên cùng tài khoản.
- Chia sẻ Project, Gem, GPT hoặc đường link chat quá rộng.
- Tiện ích trình duyệt hoặc ứng dụng "AI miễn phí" của bên thứ ba.
- Khóa API lộ trong mã nguồn, Zalo hoặc ảnh chụp màn hình (xem [Cấp C1: Gọi AI qua API](rag-tra-cuu-tai-lieu/cap-01-goi-api.md)).
- Tài liệu chứa "lệnh ẩn" (prompt injection) khiến AI làm sai khi có quyền công cụ (từ C7).
- Nhân viên nghỉ việc mang theo tài khoản cá nhân chứa dữ liệu công ty.

### Shadow AI: AI dùng ngoài tầm kiểm soát

!!! proposal "Cách xử lý đề xuất (không có nguồn định lượng)"
    1. Kiểm kê không phạt (xem bài kiểm kê ở [Cấp C0: Dùng AI thủ công](rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md)).
    2. Cấp công cụ chính thức dễ dùng hơn công cụ "lậu".
    3. Một trang quy tắc dữ liệu.
    4. Tài khoản công ty có quản trị, chọn gói có điều khoản không huấn luyện mặc định.
    5. Soát định kỳ chi phí và thẻ công ty để thấy dịch vụ lạ.

Bằng chứng về quy mô shadow AI ở Việt Nam và trên thế giới: xem [Thực trạng SME Việt Nam](thuc-trang-sme-viet-nam.md).

## Khung pháp lý Việt Nam

### Luật Bảo vệ dữ liệu cá nhân (Luật số 91/2025/QH15)

| Mục | Nội dung | Mức xác minh |
|---|---|---|
| Số hiệu | 91/2025/QH15 [[S1]] | [[v:ok]] |
| Ngày thông qua | 26/6/2025, kỳ họp thứ 9 Quốc hội khóa XV. Chỉ có từ kết quả tìm kiếm và tóm tắt; trang luatvietnam không nêu ngày | [[v:part]] |
| Hiệu lực | 01/01/2026 [[S1]] [[S3]] | [[v:ok]] |
| Chuyển tiếp (Điều 5) | Quy định về dữ liệu cá nhân trong luật hoặc nghị quyết ban hành trước 01/01/2026 tiếp tục áp dụng nếu không trái nguyên tắc của luật. Hoạt động đã được đồng ý theo Nghị định 13/2023 trước 01/01/2026 có thể tiếp tục không cần xin đồng ý lại [[S1]] [[S3]] | [[v:part]] |
| Miễn trừ (Điều 38 khoản 2, 3) | Doanh nghiệp nhỏ và khởi nghiệp được **chọn** thực hiện hoặc không Điều 21, Điều 22 và khoản 2 Điều 33 trong 5 năm từ 01/01/2026; hộ kinh doanh và doanh nghiệp siêu nhỏ không bắt buộc. **Không áp dụng** nếu cung cấp dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu nhạy cảm, hoặc xử lý dữ liệu số lượng lớn chủ thể [[S1]] | [[v:part]] |
| Điều 21, 22, khoản 2 Điều 33 | Điều 21: đánh giá tác động xử lý dữ liệu cá nhân. Điều 22: cập nhật hồ sơ, gồm đánh giá chuyển dữ liệu xuyên biên giới. Khoản 2 Điều 33: chỉ định nhân sự hoặc dịch vụ bảo vệ dữ liệu [[S1]] | [[v:part]] |
| Điều 20 | Chuyển dữ liệu cá nhân xuyên biên giới: lập hồ sơ đánh giá tác động và gửi cơ quan chuyên trách; đánh giá làm một lần cho toàn bộ thời gian hoạt động, cập nhật khi có thay đổi. Tóm tắt từ kết quả tìm kiếm | [[v:part]] |
| Mức phạt | Có nguồn nêu mức tới 1% đến 5% doanh thu năm liền trước, và một tiêu đề bài báo nêu "tối đa 3 tỷ đồng" [[S3]]. Chỉ có tiêu đề, không rõ hành vi nào, mức nào | [[v:no]] |

Một bài của Đoàn Luật sư Hà Nội nêu thời hạn lập hồ sơ chuyển dữ liệu ra nước ngoài là 60 ngày từ lần chuyển đầu. Bài viết khi luật còn là dự thảo nên **không dùng**; thay bằng Nghị định 356 ở dưới.

### Nghị định 356/2025/NĐ-CP (hướng dẫn Luật)

Ban hành 31/12/2025, hiệu lực 01/01/2026, **thay thế Nghị định 13/2023/NĐ-CP** [[S2]]. Nhiều nguồn thứ cấp thống nhất điểm này [[v:ok]]. Các chi tiết dưới đây chủ yếu theo EY, một nguồn thứ cấp:

- **Chuyển dữ liệu ra nước ngoài:** từ nộp hồ sơ **sau** (Nghị định 13) chuyển sang **thẩm định trước**. Dùng Mẫu 09 và 10; cơ quan có 15 ngày kết luận, doanh nghiệp có 30 ngày bổ sung; cập nhật 6 tháng một lần khi mục đích hoặc bên nhận đổi. Hồ sơ gửi Cục An ninh mạng và phòng, chống tội phạm sử dụng công nghệ cao (A05), Bộ Công an. Có miễn trừ cho chuyển dữ liệu nhằm quản lý nhân sự theo pháp luật lao động [[S2]].
- **Miễn trừ:** hộ kinh doanh và doanh nghiệp siêu nhỏ miễn hoàn toàn; doanh nghiệp nhỏ và khởi nghiệp miễn 5 năm từ 01/01/2026; không áp dụng nếu xử lý dữ liệu như một dịch vụ, trực tiếp xử lý dữ liệu nhạy cảm, hoặc từ 100.000 chủ thể dữ liệu tích lũy trở lên. Theo nguồn thứ cấp [[S2]], doanh nghiệp vừa không thấy được liệt kê trong nhóm miễn trừ. **Chưa đọc văn bản gốc**: đừng kết luận doanh nghiệp vừa phải tuân thủ đầy đủ nếu chưa hỏi người có chuyên môn.
- **Đổi loại dữ liệu:** lịch sử hoạt động trực tuyến, mã số thuế, số sổ BHXH, số thẻ BHYT bị đưa khỏi nhóm "cơ bản". Nhóm nhạy cảm mở rộng gồm theo dõi hành vi, hoạt động viễn thông và mạng xã hội, tình trạng sức khỏe rộng hơn, thông tin định danh điện tử, ảnh giấy tờ tùy thân, lịch sử giao dịch và ngân hàng [[S2]].
- **Sự đồng ý:** phải kiểm chứng và lưu được; cấm ô tick sẵn và diễn đạt gây hiểu nhầm [[S2]].
- **Vi phạm dữ liệu vị trí hoặc sinh trắc học:** thông báo cá nhân trong 72 giờ; lưu hồ sơ vi phạm ít nhất 5 năm [[S2]].

!!! verify "Lệch số điều giữa các nguồn: cần tra bản gốc"
    Các bài phân tích gắn cơ chế chuyển dữ liệu ra nước ngoài với "Điều 18 Nghị định 356" và Mẫu 09, trong khi Luật ghi Điều 20; có nguồn nói Nghị định hướng dẫn khoản 7 Điều 20. Bản .doc của Nghị định 356 có trên cổng văn bản pháp luật của Bộ Tư pháp [[S9]] nhưng SIPTech chưa tải và đọc.

### Nghị định 13/2023/NĐ-CP

Theo EY và các nguồn khác, đã bị Nghị định 356/2025 thay thế từ 01/01/2026 [[S2]]. Ngày ban hành và hiệu lực gốc của Nghị định 13 (theo trí nhớ: 17/4/2023, hiệu lực 01/7/2023) [[v:no]] trong lần tra cứu này. Chỉ nên dùng Nghị định 13 để hiểu quá trình chuyển tiếp.

### Luật Công nghiệp công nghệ số (Luật số 71/2025/QH15) [[v:part]]

Thông qua 14/6/2025; hiệu lực 01/01/2026 (một số điều hiệu lực 01/7/2025); 6 chương, 51 điều. Theo tóm tắt từ kết quả tìm kiếm, chưa đọc toàn văn [[S7]]:

- **Điều 44:** hệ thống AI tương tác trực tiếp với người phải thông báo cho người dùng biết đang tương tác với AI (trừ khi hiển nhiên). Sản phẩm số do AI tạo thuộc danh mục do Bộ trưởng Bộ KH&CN ban hành phải có dấu hiệu nhận dạng từ 01/01/2026.
- **Điều 45:** trách nhiệm của bên cung cấp AI, gồm tuân thủ pháp luật dữ liệu và bảo vệ dữ liệu cá nhân.
- Danh mục sản phẩm nào đã được ban hành: [[v:no]].

### Luật Trí tuệ nhân tạo (Luật số 134/2025/QH15)

- Thông qua 10/12/2025 (kỳ họp thứ 10, Quốc hội khóa XV), hiệu lực **01/3/2026**, 35 điều [[S4]] [[S5]]. Hai báo nêu cùng số phiếu 429/434 đại biểu nhưng phần trăm khác nhau (90,70% và 98,8%), nên **không dùng tỷ lệ**; 429/434 tính ra khoảng 98,8%.
- **Phân loại rủi ro:** cao, trung bình, thấp (Điều 9) [[S4]]. Mức trung bình: có thể gây nhầm lẫn hoặc thao túng vì người dùng không biết đang tương tác với AI hay nội dung do AI tạo.
- **Hành vi bị cấm** (6 nhóm, theo Znews, không có số điều) [[S6]]: lợi dụng hoặc chiếm đoạt hệ thống AI để vi phạm pháp luật; dùng AI cho mục đích bị cấm (giả mạo người hoặc sự kiện để lừa dối, khai thác nhóm yếu thế); **thu thập, xử lý, sử dụng dữ liệu để phát triển, huấn luyện, thử nghiệm, vận hành AI trái pháp luật về dữ liệu, bảo vệ dữ liệu cá nhân, sở hữu trí tuệ, an ninh mạng**; cản trở hoặc vô hiệu giám sát của con người; che giấu thông tin phải minh bạch hoặc xóa, làm sai lệch nhãn và cảnh báo bắt buộc; lạm dụng hoạt động nghiên cứu, thử nghiệm, chứng nhận.
- **Giám sát con người** với quyết định quan trọng; lĩnh vực rủi ro cao gồm tài chính, y tế, tư pháp, lao động, giáo dục chịu yêu cầu chặt hơn về dữ liệu, kiểm thử, giám sát [[S5]].
- Kết quả tìm kiếm còn nêu thời hạn chuyển tiếp (18 tháng với y tế, giáo dục, tài chính; 12 tháng với lĩnh vực còn lại) và **Nghị định 142/2026/NĐ-CP** hiệu lực 01/5/2026. Hai điểm này [[v:no]]: chỉ nằm trong tóm tắt kết quả tìm kiếm, không đọc được văn bản [[S8]].

!!! proposal "Ý nghĩa cho SME (diễn giải thận trọng của SIPTech, không phải kết luận pháp lý)"
    - Chatbot đối mặt khách hàng nên ghi rõ "đang trả lời bởi AI".
    - Không dùng dữ liệu khách trái luật để huấn luyện hoặc tinh chỉnh.
    - Quyết định ảnh hưởng quyền lợi cá nhân (tuyển dụng, tín dụng, kỷ luật) giữ người quyết định cuối.

### Còn thiếu

- Luật Dữ liệu 2024 (Luật số 60/2024/QH15, theo trí nhớ, hiệu lực 01/7/2025) và quy định về "dữ liệu quan trọng, dữ liệu cốt lõi" chuyển ra nước ngoài: chưa tra.
- Nghị định xử phạt vi phạm hành chính về bảo vệ dữ liệu cá nhân: thấy tiêu đề một tài liệu của EY nhắc "Decree 330" trong kết quả tìm kiếm nhưng chưa đọc. Không dùng mức phạt cho tới khi đọc.
- Văn bản về sở hữu trí tuệ với nội dung do AI tạo, và quy định ngành (ngân hàng, y tế, giáo dục): chưa tra.
- Hướng dẫn chính thức của Bộ Công an và A05 cho SME về hồ sơ: chưa tra.

## Dịch vụ AI nào dùng dữ liệu của bạn để huấn luyện?

!!! proposal "Nguyên tắc bền (đề xuất của SIPTech)"
    Gói tiêu dùng và miễn phí thường có cài đặt cho phép dùng chat để cải thiện mô hình. Gói doanh nghiệp và API thường mặc định không huấn luyện nhưng vẫn giữ log chống lạm dụng. Điều khoản và ngày hiệu lực thay đổi: mỗi lần triển khai phải đọc lại trang trong cột nguồn.

Nội dung đọc ngày 11/11/2026:

| Dịch vụ | Điều đọc được | Nguồn |
|---|---|---|
| **Claude Free, Pro, Max** (Anthropic) | Chat và phiên code được dùng để huấn luyện nếu bạn bật "model improvement" trong cài đặt riêng tư. Hội thoại bị gắn cờ an toàn có thể được dùng để cải thiện phát hiện vi phạm. Chat Incognito không dùng để cải thiện Claude kể cả khi đã bật. Phản hồi (thumbs) lưu tối đa 5 năm, tách khỏi ID người dùng khi dùng. Dữ liệu thô từ connector không bị dùng trừ khi bạn dán vào chat. Trang ghi ngày 16/3/2026 | [[S10]] |
| **Claude Team, Enterprise, API** (Anthropic) | Mặc định **không** dùng đầu vào, đầu ra của sản phẩm thương mại để huấn luyện; ngoại lệ khi bạn gửi phản hồi, báo lỗi hoặc chủ động cho phép (khi đó cả hội thoại liên quan có thể lưu tối đa 5 năm và được dùng). Trang không nêu thời gian lưu log API thường. Trang ghi ngày 18/8/2026 | [[S11]] |
| **ChatGPT cá nhân** (OpenAI) | Có cài đặt "Improve the model for everyone" (Settings, Data Controls) hoặc cổng riêng tư "Do not train on my content"; tắt thì không huấn luyện trên hội thoại mới. Phản hồi thumbs up hoặc down có thể đưa cả hội thoại vào huấn luyện. Temporary Chat không dùng để huấn luyện (theo bản mới). **Chỉ đọc qua tóm tắt tìm kiếm**: trang chính thức trả lỗi 403, nhiều phiên bản có ngày "Updated" khác nhau | [[S13]] |
| **ChatGPT Business, Enterprise, API** (OpenAI) | Mặc định không huấn luyện trên đầu vào, đầu ra cho người dùng doanh nghiệp (cả hai nguồn). API: "kể từ 1/3/2023 dữ liệu gửi API không dùng để huấn luyện (trừ khi bạn chủ động chia sẻ)"; log chống lạm dụng giữ **tối đa 30 ngày** mặc định; Zero Data Retention là tùy chọn cần được duyệt, không phải mặc định. Trang API không ghi ngày xuất bản | [[S12]] [[S13]] |
| **Gemini Apps cá nhân** (Google) | Một phần chat được người (kể cả nhà cung cấp dịch vụ của Google) xem xét; chat được tách khỏi tài khoản trước khi gửi; chat đã xem xét lưu tới 3 năm và xóa hoạt động không xóa chúng. Tắt "Keep Activity" thì chat tương lai không dùng để cải thiện, nhưng chat vẫn lưu 72 giờ. Temporary Chat không dùng để huấn luyện. Trang dặn "đừng nhập thông tin bí mật mà bạn không muốn người xem xét thấy" | [[S14]] |
| **Gemini API** (Google) | Dịch vụ **không trả phí**: Google có thể dùng đầu vào, đầu ra để cải thiện sản phẩm, người xem xét có thể đọc; trang dặn "không gửi thông tin nhạy cảm, bí mật hay cá nhân" (ngoại lệ EEA, Thụy Sĩ, Anh: áp dụng điều khoản trả phí). Dịch vụ **trả phí**: không dùng prompt để cải thiện sản phẩm, xử lý theo Data Processing Addendum, có ghi log trong thời gian giới hạn. Grounding with Google Search lưu 30 ngày. Hiệu lực 23/3/2026 | [[S15]] |

!!! proposal "Quy tắc thực hành (đề xuất của SIPTech)"
    1. SME không dùng bản miễn phí hoặc cá nhân cho dữ liệu mức "bí mật" trở lên.
    2. Nếu dùng cá nhân thì tắt tùy chọn huấn luyện, và vẫn không dán dữ liệu cá nhân.
    3. Gemini API: tài khoản miễn phí nghĩa là dữ liệu có thể bị xem, chỉ dùng dữ liệu công khai.
    4. Ghi vào sổ prompt: gói và tài khoản nào đang dùng cho nghiệp vụ nào.
    5. Kiểm tra lại các trang này mỗi quý.

**Chưa nêu được:** nơi lưu trữ dữ liệu (vùng, quốc gia) của từng dịch vụ cho khách Việt Nam, và việc có hay không DPA riêng cho doanh nghiệp Việt. Điều này quan trọng với việc chuyển dữ liệu ra nước ngoài, xem phần tiếp theo.

## Chuyển dữ liệu ra nước ngoài khi dùng AI đám mây

Khi gửi dữ liệu cá nhân của người ở Việt Nam đến máy chủ AI ở nước ngoài, về cơ bản việc đó có thể được coi là **chuyển dữ liệu cá nhân xuyên biên giới** (Điều 20 Luật 91/2025, theo tóm tắt). Dưới đây là cách tự sàng lọc; đây là cách suy luận do SIPTech đề xuất và cần luật sư xác nhận.

1. **Dữ liệu gửi có dữ liệu cá nhân không?** Nếu đã ẩn danh thật sự thì nghĩa vụ nhẹ hơn (cần luật sư xác nhận thế nào là "ẩn danh thật sự").
2. **Doanh nghiệp có thuộc nhóm được miễn** (hộ kinh doanh, siêu nhỏ, nhỏ hoặc khởi nghiệp trong 5 năm) và **không** thuộc ngoại lệ (xử lý dữ liệu nhạy cảm, dịch vụ xử lý dữ liệu, số lượng lớn)? Theo tóm tắt, chỉ miễn một số điều (Điều 21, 22, khoản 2 Điều 33) chứ chưa chắc miễn mọi nghĩa vụ [[S1]].
3. **Có sự đồng ý hợp lệ, lưu được bằng chứng không?** Nghị định 356 yêu cầu đồng ý phải kiểm chứng được [[S2]].
4. **Nếu bắt buộc lập hồ sơ:** ai nộp, nộp cho ai (A05 theo EY), biểu mẫu nào (Mẫu 09, 10 theo EY), và phải chờ thẩm định trước [[S2]].
5. **Cách giảm rủi ro rẻ nhất:** không gửi dữ liệu cá nhân. Ẩn danh trước khi gọi API, giữ bảng tra ngược trong nước.

## Sáu bài thực hành nhỏ

Các bài này là đề xuất của SIPTech, không phải yêu cầu pháp luật.

| Bài | Làm gì | Sản phẩm | Lỗi hay gặp |
|---|---|---|---|
| A1. Phân loại dữ liệu công ty | Liệt kê 20 loại tài liệu hay dán vào AI (hợp đồng, sao kê, CV, danh sách khách), gán mức theo bảng phân loại ở trên, ghi người chịu trách nhiệm | Bảng phân loại 5 mức | Coi "dữ liệu khách" là một loại; không tách phần nhạy cảm |
| A2. Trang quy tắc một tờ A4 | Viết 5 điều "không dán", 5 điều "được dán", nơi hỏi khi nghi ngờ, người duyệt, hậu quả; nhân viên ký đã đọc | Một trang quy tắc | Quy tắc quá dài, không ai đọc |
| A3. Ẩn danh bằng script | Viết hàm thay số điện thoại, email, CCCD, tên bằng mã; lưu bảng tra ngược cục bộ; kiểm hồi quy với 20 mẫu, đếm sót | `anonymize.py` và báo cáo sót (chưa chạy thử trong tài liệu này) | Quên tên viết thường hoặc không dấu; địa chỉ nhà |
| A4. Cài đặt tài khoản và đối chiếu điều khoản | Với mỗi dịch vụ công ty dùng, chụp màn hình cài đặt huấn luyện, ghi ngày, so với bảng dịch vụ ở trên; lập lịch kiểm lại hằng quý | Ảnh chụp và lịch kiểm | Tin ảnh chụp cũ; nhân viên dùng bản cá nhân khác bản công ty |
| A5. Kiểm kê shadow AI và kế hoạch chuyển | Dùng khảo sát ở Cấp C0; chia công cụ thành "cho phép", "cho phép có điều kiện", "cấm"; chuyển người dùng sang công cụ chính thức | Danh sách công cụ và kế hoạch chuyển | Cấm hàng loạt mà không có công cụ thay thế |
| A6. Quy trình sự cố | Nếu nhân viên lỡ dán dữ liệu cá nhân hoặc bí mật: (1) báo trong ngày; (2) xóa hội thoại và kiểm tra cài đặt huấn luyện; (3) ghi lại thông tin gì, vào dịch vụ nào, thời điểm; (4) đánh giá có phải vi phạm cần thông báo không (hỏi luật sư; Nghị định 356 có quy định thông báo vi phạm, EY nêu 72 giờ cho dữ liệu vị trí và sinh trắc học) [[S2]] | Mẫu nhật ký sự cố | Giấu sự cố vì sợ bị phạt |

## Cần kiểm tra lại trước khi dựa vào bài này

1. **Toàn văn** Luật 91/2025/QH15, Nghị định 356/2025, Luật 71/2025, Luật 134/2025: chưa đọc bản gốc. Đọc trước hết bản .doc của Nghị định 356 [[S9]] và Công báo.
2. Ngày thông qua Luật 91/2025 (26/6/2025) chỉ có qua tóm tắt tìm kiếm.
3. Số điều của chuyển dữ liệu xuyên biên giới trong Nghị định 356 (Điều 18 theo bài phân tích hay số khác) và số biểu mẫu (09, 10, 01a, 01b).
4. Mức phạt (1% đến 5% doanh thu; 3 tỷ đồng): chưa xác minh; chưa đọc nghị định xử phạt.
5. Nghị định 142/2026/NĐ-CP và thời hạn chuyển tiếp 12 hoặc 18 tháng của Luật AI.
6. Danh mục sản phẩm số do AI tạo phải gắn dấu nhận dạng (Luật 71/2025): chưa biết đã ban hành chưa.
7. Luật Dữ liệu 2024 và quy định dữ liệu quan trọng, dữ liệu cốt lõi.
8. ChatGPT cá nhân: chỉ qua tóm tắt tìm kiếm của nhiều phiên bản; cần mở trang chính thức bằng trình duyệt.
9. Nơi lưu dữ liệu, DPA, thời gian lưu log của từng dịch vụ cho khách Việt Nam.
10. Cách tính "doanh nghiệp nhỏ, siêu nhỏ, khởi nghiệp" áp dụng cho từng SME cụ thể (theo luật hỗ trợ doanh nghiệp nhỏ và vừa).
11. Mọi bảng phân loại, quy tắc, quy trình trong bài là **đề xuất của SIPTech**, không phải yêu cầu pháp luật.

!!! warning "Nhắc lại"
    Bài này không thay thế tư vấn pháp lý. Với dữ liệu nhạy cảm, quy mô lớn, hoặc gửi ra nước ngoài, hãy tham vấn luật sư hoặc đơn vị bảo vệ dữ liệu cá nhân trước khi triển khai.

## Nguồn

Truy cập ngày 11/11/2026. Nhãn màu cho biết SIPTech đã đọc tới đâu: "Nguồn chính thức" là nhà cung cấp hoặc cơ quan nhà nước.

:::sources
S1 | Luật Bảo vệ dữ liệu cá nhân 2025 có hiệu lực khi nào? | luatvietnam.vn · trang pháp luật | https://luatvietnam.vn/dan-su/luat-bao-ve-du-lieu-ca-nhan-2025-co-hieu-luc-khi-nao-568-103652-article.html | thu | Độ tin cậy trung bình.
S2 | Nghị định số 356/2025/NĐ-CP quy định chi tiết một số điều và biện pháp thi hành Luật Bảo vệ dữ liệu cá nhân | EY Vietnam · hãng tư vấn | https://www.ey.com/vi_vn/technical/tax/tax-and-law-updates/nghi-dinh-so-356-2025-nd-cp-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-bao-ve-du-lieu-ca-nhan | thu | Độ tin cậy trung bình đến cao. Một nguồn thứ cấp cho hầu hết chi tiết của nghị định.
S3 | Từ năm 2026, doanh nghiệp phải xóa dữ liệu cá nhân của người lao động khi nghỉ việc | lsvn.vn · trang pháp luật | https://lsvn.vn/tu-nam-2026-doanh-nghiep-phai-xoa-du-lieu-ca-nhan-cua-nguoi-lao-dong-khi-nghi-viec-a167358.html | thu | Độ tin cậy trung bình. Phần mức phạt chỉ có tiêu đề bài.
S4 | Quốc hội thông qua Luật Trí tuệ nhân tạo | Báo Đại biểu Nhân dân | https://daibieunhandan.vn/quoc-hoi-thong-qua-luat-tri-tue-nhan-tao-10399959.html | thu | Báo của cơ quan Quốc hội. Độ tin cậy trung bình đến cao.
S5 | Luật Trí tuệ nhân tạo có hiệu lực từ 1/3/2026 | VnEconomy · báo chí | https://vneconomy.vn/luat-tri-tue-nhan-tao-se-co-hieu-luc-tu-ngay-132026.htm | thu | Độ tin cậy trung bình.
S6 | 6 hành vi bị cấm khi sử dụng trí tuệ nhân tạo | Znews · báo chí | https://znews.vn/6-hanh-vi-bi-cam-khi-su-dung-tri-tue-nhan-tao-post1609885.html | thu | Độ tin cậy trung bình; không có số điều.
S7 | Luật Công nghiệp công nghệ số 71/2025/QH15 | thuvienphapluat.vn · trang pháp luật | https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Luat-Cong-nghiep-cong-nghe-so-2025-so-71-2025-QH15-621341.aspx | chua | Chỉ thấy kết quả tìm kiếm; trang trả lỗi 403.
S8 | Luật Trí tuệ nhân tạo 134/2025/QH15 | thuvienphapluat.vn · trang pháp luật | https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Luat-Tri-tue-nhan-tao-2025-so-134-2025-QH15-679013.aspx | chua | Trang trả lỗi 403, chưa đọc.
S9 | Nghị định 356/2025 bản .doc | vbpl.moj.gov.vn · cổng văn bản pháp luật của Bộ Tư pháp | https://vbpl.moj.gov.vn/TW/Lists/vbpq/Attachments/187276/ND.356.2025.doc | chua | Nguồn chính thức nhưng SIPTech chưa tải và đọc. Nên đọc đầu tiên khi kiểm tra.
S10 | Is my data used for model training? (tài khoản cá nhân) | Anthropic · trợ giúp nhà cung cấp | https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training | off | Trang ghi ngày 16/3/2026.
S11 | Is my data used for model training? (sản phẩm thương mại) | Anthropic · trợ giúp nhà cung cấp | https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training | off | Trang ghi ngày 18/8/2026.
S12 | Your data (API) | OpenAI · tài liệu nhà cung cấp | https://developers.openai.com/api/docs/guides/your-data | off | Đọc trực tiếp; trang không ghi ngày xuất bản.
S13 | How your data is used to improve model performance | OpenAI · trợ giúp nhà cung cấp | https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance | tom | Chỉ qua tóm tắt tìm kiếm; trang chính thức trả lỗi 403.
S14 | Gemini Apps Privacy Hub | Google · trợ giúp nhà cung cấp | https://support.google.com/gemini/answer/13594961 | off |
S15 | Gemini API Additional Terms | Google · điều khoản nhà cung cấp | https://aistudio.google.com/docs/terms | off | Hiệu lực 23/3/2026; đã chuyển hướng từ ai.google.dev/gemini-api/terms.
:::
