# An toàn dữ liệu và pháp lý Việt Nam khi dùng AI (áp dụng cho mọi cấp C0-C9)

> Ngày soạn/truy cập: 2026-11-11.
> **CẢNH BÁO: đây không phải tư vấn pháp lý.** Đây là tổng hợp từ nguồn công khai, phần lớn là nguồn thứ cấp (trang pháp luật, hãng tư vấn, báo chí). Chúng tôi **chưa đọc được toàn văn văn bản gốc** của các luật/nghị định. Trước khi ra quyết định có hậu quả pháp lý (chuyển dữ liệu ra nước ngoài, xử lý dữ liệu nhạy cảm, triển khai với khách hàng), hãy đọc văn bản gốc và hỏi luật sư.
> Quy ước: **[Nguồn]** = đọc được trong nguồn nêu tên; **[Đề xuất]** = của chúng tôi. Mức xác minh: **Đã xác minh (2 nguồn+)**, **Xác minh một phần**, **Chưa xác minh**.

## 1. Mục tiêu và người đọc

**Người đọc:** chủ SME, người phụ trách IT/kế toán/nhân sự ở Việt Nam đang dùng ChatGPT/Claude/Gemini.
**Mục tiêu:** (1) bảng quy tắc "được/không được đưa vào AI"; (2) biết cài đặt huấn luyện của từng dịch vụ và nơi kiểm tra; (3) nắm khung luật Việt Nam đang hiệu lực và việc nào cần hỏi chuyên gia; (4) có kế hoạch xử lý shadow AI.
**Sản phẩm:** trang quy tắc dữ liệu 1 tờ A4, bảng phân loại dữ liệu, danh sách tài khoản AI của công ty, mẫu ghi nhật ký sự cố.

## 2. Vì sao cần (liên hệ các cấp)

- C0 làm lộ dữ liệu nhanh nhất (dán vào chat tài khoản cá nhân).
- C1 làm dữ liệu đi hàng loạt qua khóa API: lỗi quy tắc nhân lên theo số lần gọi.
- C2-C5 (tài liệu, lập chỉ mục, tìm kiếm) tạo kho dữ liệu mới: bản trích văn bản, chỉ mục vector vẫn là dữ liệu cá nhân nếu chứa dữ liệu cá nhân. **[Đề xuất]**
- C7-C9 (công cụ/quy trình/vận hành) cho AI quyền hành động: cần phân quyền và nhật ký.

## 3. Kiến thức nền

### 3.1 Phân loại dữ liệu để quyết định (đề xuất, nguyên tắc bền)

| Mức | Ví dụ | Dùng với AI công cộng (tài khoản cá nhân/miễn phí) | Dùng với gói doanh nghiệp/API trả phí |
|---|---|---|---|
| Công khai | Bảng giá niêm yết, bài đăng website | Được | Được |
| Nội bộ thường | Quy trình, mẫu biểu không có tên người | Hạn chế; nên ẩn tên công ty/đối tác | Được, theo quy tắc công ty |
| Bí mật kinh doanh | Giá vốn, hợp đồng, công thức, mã nguồn, báo cáo tài chính chưa công bố | Không | Chỉ khi đã đọc điều khoản dữ liệu và có người duyệt |
| Dữ liệu cá nhân | Họ tên + SĐT, địa chỉ, email khách/nhân viên, CV | Không | Chỉ khi có cơ sở pháp lý, đã ẩn danh nếu có thể, đã kiểm tra chuyển ra nước ngoài |
| Dữ liệu cá nhân nhạy cảm | Sức khỏe, sinh trắc học, giao dịch tài khoản ngân hàng, định vị, CCCD... | Cấm tuyệt đối | Mặc định cấm; chỉ khi có tư vấn pháp lý |

(Danh sách loại dữ liệu nhạy cảm do luật quy định; xem mục 4 về thay đổi giữa Nghị định 13 và 356. Bảng trên là **đề xuất**, không phải trích luật.)

### 3.2 Ẩn danh/giả danh (pseudonymization) trước khi gửi (đề xuất)

1. Thay tên người, SĐT, email, địa chỉ chi tiết, số tài khoản, mã số thuế, số CCCD bằng mã (`KH_001`); giữ bảng tra ngược **ở máy công ty**, không gửi.
2. Rút gọn thông tin gián tiếp có thể nhận ra người (ngày sinh đầy đủ, chức danh hiếm + nơi làm).
3. Có bước kiểm tự động (biểu thức chính quy cho SĐT/email/CCCD) trước khi gửi; chặn nếu còn.
4. Lưu ý: dữ liệu đã giả danh nhưng còn bảng tra ngược vẫn có thể bị coi là dữ liệu cá nhân; ẩn danh thực sự (không thể xác định lại) khó hơn. Nghị định 356 có điều khoản yêu cầu **khử nhận dạng (de-identify)** cho một số hình thức trao đổi dữ liệu **[Nguồn: tóm tắt EY về NĐ 356, xem mục 8]**.

### 3.3 Rủi ro rò rỉ thường gặp (đề xuất, theo kinh nghiệm chung)

- Dán dữ liệu vào tài khoản cá nhân/miễn phí có thể được dùng cải thiện mô hình (mục 5).
- Lịch sử chat, tệp tải lên, bộ nhớ (memory) lưu lại và hiện cho người dùng sau trên cùng tài khoản.
- Chia sẻ Project/Gem/GPT/đường link chat quá rộng.
- Tiện ích trình duyệt/ứng dụng "AI miễn phí" bên thứ ba.
- Khóa API lộ trong mã/Zalo/ảnh chụp màn hình (xem `rag-tra-cuu-tai-lieu/cap-01-goi-api.md`).
- Tài liệu có "lệnh ẩn" (prompt injection) khiến AI làm sai khi có quyền công cụ (C7+).
- Nhân viên nghỉ việc mang theo tài khoản cá nhân chứa dữ liệu công ty.

### 3.4 Shadow AI (AI dùng ngoài tầm kiểm soát)

**Cách xử lý đề xuất (không có nguồn định lượng):** (1) kiểm kê không phạt (bài C0.1 trong `rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`); (2) cấp công cụ chính thức dễ dùng hơn công cụ lậu; (3) quy tắc dữ liệu 1 trang; (4) tài khoản công ty có quản trị, chọn gói có điều khoản không huấn luyện mặc định; (5) soát định kỳ chi phí/thẻ công ty để thấy dịch vụ lạ.

## 4. Khung pháp lý Việt Nam (đã tra cứu 2026-11-11)

### 4.1 Luật Bảo vệ dữ liệu cá nhân (Luật số 91/2025/QH15)

| Điều | Nội dung | Mức xác minh | Nguồn |
|---|---|---|---|
| Số hiệu | 91/2025/QH15 | Xác minh (nhiều nguồn) | luatvietnam.vn; thuvienphapluat.vn (tiêu đề); kết quả tìm kiếm |
| Ngày thông qua | 26/6/2025, kỳ họp thứ 9 Quốc hội khóa XV | Xác minh một phần (chỉ từ kết quả tìm kiếm và tóm tắt, trang luatvietnam không nêu ngày) | tổng hợp kết quả tìm kiếm; hoatieu.vn/lsvn.vn (snippet) |
| Hiệu lực | 01/01/2026 | Xác minh (nhiều nguồn) | luatvietnam.vn (nêu Điều 5), lsvn.vn |
| Chuyển tiếp (Điều 5) | Quy định về dữ liệu cá nhân trong luật/nghị quyết ban hành trước 01/01/2026 tiếp tục áp dụng nếu không trái nguyên tắc của luật; hoạt động đã được đồng ý theo NĐ 13/2023 trước 01/01/2026 có thể tiếp tục không cần đồng ý lại | Xác minh một phần | luatvietnam.vn; lsvn.vn |
| Miễn trừ (Điều 38 khoản 2, 3) | Doanh nghiệp nhỏ và khởi nghiệp được **chọn** thực hiện hoặc không Điều 21, 22 và khoản 2 Điều 33 trong 5 năm từ 01/01/2026; hộ kinh doanh, doanh nghiệp siêu nhỏ không bắt buộc; **không áp dụng** nếu cung cấp dịch vụ xử lý dữ liệu cá nhân, trực tiếp xử lý dữ liệu nhạy cảm, hoặc xử lý dữ liệu số lượng lớn chủ thể | Xác minh một phần (một nguồn trích điều khoản) | luatvietnam.vn |
| Điều 21, 22 | Điều 21: đánh giá tác động xử lý dữ liệu cá nhân; Điều 22: cập nhật hồ sơ, gồm đánh giá chuyển dữ liệu xuyên biên giới; khoản 2 Điều 33: chỉ định nhân sự/dịch vụ bảo vệ dữ liệu | Xác minh một phần | luatvietnam.vn |
| Điều 20 | Chuyển dữ liệu cá nhân xuyên biên giới: lập hồ sơ đánh giá tác động và gửi cơ quan chuyên trách; đánh giá làm một lần cho toàn bộ thời gian hoạt động, cập nhật khi thay đổi | Xác minh một phần (tóm tắt từ kết quả tìm kiếm) | kết quả tìm kiếm (mục lục luật; bài tóm tắt) |
| Phạt | Có nguồn nêu mức tới 1%-5% doanh thu năm liền trước và tiêu đề bài báo nêu "tối đa 3 tỷ đồng" | **Chưa xác minh** (chỉ có tiêu đề/snippet; không rõ hành vi nào, mức nào) | lsvn.vn (tiêu đề bài) |

Một bài của Đoàn Luật sư Hà Nội nêu thời hạn lập hồ sơ chuyển dữ liệu ra nước ngoài là 60 ngày từ lần chuyển đầu, nhưng bài này viết khi luật còn là dự thảo nên **không dùng**; thay bằng Nghị định 356 (4.2).

### 4.2 Nghị định 356/2025/NĐ-CP (hướng dẫn Luật)

- Ban hành 31/12/2025, hiệu lực 01/01/2026, **thay thế Nghị định 13/2023/NĐ-CP** **[Nguồn: EY Vietnam; kết quả tìm kiếm khác]**. Mức xác minh: nhiều nguồn thứ cấp thống nhất.
- Theo EY (một nguồn): hồ sơ đánh giá tác động chuyển dữ liệu ra nước ngoài chuyển từ nộp **sau** (NĐ 13) sang cơ chế **thẩm định trước** (NĐ 356); dùng Mẫu 09, 10; cơ quan có 15 ngày kết luận, doanh nghiệp có 30 ngày bổ sung; cập nhật 6 tháng/lần khi mục đích/bên nhận đổi; hồ sơ gửi cho Cục An ninh mạng và phòng, chống tội phạm sử dụng công nghệ cao (A05), Bộ Công an; có miễn trừ cho chuyển dữ liệu nhằm quản lý nhân sự theo pháp luật lao động.
- Miễn trừ theo EY: hộ kinh doanh và doanh nghiệp siêu nhỏ miễn hoàn toàn; doanh nghiệp nhỏ và khởi nghiệp miễn 5 năm từ 01/01/2026; không áp dụng nếu xử lý dữ liệu như một dịch vụ, trực tiếp xử lý dữ liệu nhạy cảm, hoặc từ 100.000 chủ thể dữ liệu tích lũy trở lên. Doanh nghiệp vừa không còn được liệt kê.
- Thay đổi loại dữ liệu: lịch sử hoạt động trực tuyến, mã số thuế, số sổ BHXH, số thẻ BHYT bị đưa khỏi nhóm "cơ bản"; nhóm nhạy cảm mở rộng gồm theo dõi hành vi, hoạt động viễn thông/mạng xã hội, tình trạng sức khỏe rộng hơn, thông tin định danh điện tử, ảnh giấy tờ tùy thân, lịch sử giao dịch/ngân hàng **[Nguồn: EY]**.
- Đồng ý: phải kiểm chứng và lưu được; cấm ô tick sẵn và diễn đạt gây hiểu nhầm **[Nguồn: EY]**.
- Vi phạm dữ liệu vị trí/sinh trắc học: thông báo cá nhân trong 72 giờ; lưu hồ sơ vi phạm ít nhất 5 năm **[Nguồn: EY]**.
- **Lệch số điều:** các bài phân tích gắn cơ chế chuyển dữ liệu ra nước ngoài với "Điều 18 NĐ 356" và Mẫu 09, trong khi Luật ghi Điều 20; có nguồn nói Nghị định hướng dẫn khoản 7 Điều 20. Nguồn không thống nhất về số điều/mẫu: **cần tra bản gốc**. Có file .doc của NĐ 356 trên vbpl.moj.gov.vn (xuất hiện trong kết quả tìm kiếm, **chúng tôi chưa tải/đọc**).

### 4.3 Nghị định 13/2023/NĐ-CP

Theo EY và các nguồn, đã bị NĐ 356/2025 thay thế từ 01/01/2026. Ngày ban hành và hiệu lực gốc của NĐ 13 (theo trí nhớ: 17/4/2023, hiệu lực 01/7/2023) **chưa xác minh trong phiên này**. Dùng NĐ 13 chỉ để hiểu quá trình chuyển tiếp.

### 4.4 Luật Công nghiệp công nghệ số (Luật số 71/2025/QH15)

- Thông qua 14/6/2025; hiệu lực 01/01/2026 (một số điều hiệu lực 01/7/2025); 6 chương, 51 điều **[Nguồn: tóm tắt từ kết quả tìm kiếm, thuvienphapluat.vn/luatvietnam.vn; chưa đọc toàn văn]**. Mức: xác minh một phần.
- Nội dung liên quan AI theo tóm tắt: Điều 44 yêu cầu hệ thống AI tương tác trực tiếp với người phải thông báo cho người dùng biết đang tương tác với AI (trừ khi hiển nhiên) và sản phẩm số do AI tạo thuộc danh mục do Bộ trưởng Bộ KH&CN ban hành phải có dấu hiệu nhận dạng từ 01/01/2026; Điều 45 nêu trách nhiệm bên cung cấp AI gồm tuân thủ pháp luật dữ liệu và bảo vệ dữ liệu cá nhân. **Chưa xác minh** danh mục sản phẩm nào đã được ban hành.

### 4.5 Luật Trí tuệ nhân tạo (Luật số 134/2025/QH15)

- Thông qua 10/12/2025 (kỳ họp thứ 10, Quốc hội khóa XV), hiệu lực **01/3/2026**, 35 điều **[Nguồn: daibieunhandan.vn; vneconomy.vn]**. Con số bỏ phiếu 429/434 đại biểu được hai báo nêu; phần trăm khác nhau (90,70% ở một báo, 98,8% ở báo khác: **không dùng tỷ lệ**; 429/434 tính ra khoảng 98,8%).
- Phân loại rủi ro: cao, trung bình, thấp (Điều 9) **[Nguồn: daibieunhandan.vn]**. Trung bình: có thể gây nhầm lẫn/thao túng vì người dùng không biết đang tương tác với AI hoặc nội dung do AI tạo.
- Các hành vi bị cấm (6 nhóm, theo báo Znews, **không có số điều**): lợi dụng/chiếm đoạt hệ thống AI để vi phạm pháp luật; dùng AI cho mục đích bị cấm (giả mạo người/sự kiện để lừa dối, khai thác nhóm yếu thế...); **thu thập, xử lý, sử dụng dữ liệu để phát triển, huấn luyện, thử nghiệm, vận hành AI trái pháp luật về dữ liệu, bảo vệ dữ liệu cá nhân, sở hữu trí tuệ, an ninh mạng**; cản trở/vô hiệu giám sát của con người; che giấu thông tin phải minh bạch hoặc xóa/làm sai lệch nhãn/cảnh báo bắt buộc; lạm dụng hoạt động nghiên cứu/thử nghiệm/chứng nhận **[Nguồn: znews.vn]**.
- Giám sát con người với quyết định quan trọng; lĩnh vực rủi ro cao gồm tài chính, y tế, tư pháp, lao động, giáo dục chịu yêu cầu chặt hơn về dữ liệu, kiểm thử, giám sát **[Nguồn: vneconomy.vn]**.
- Kết quả tìm kiếm còn nêu thời hạn chuyển tiếp (18 tháng với y tế, giáo dục, tài chính; 12 tháng còn lại) và **Nghị định 142/2026/NĐ-CP** hiệu lực 01/5/2026: **chưa xác minh** (chỉ nằm trong tóm tắt kết quả tìm kiếm, không đọc được văn bản).
- **[Đề xuất] Ý nghĩa cho SME:** (a) chatbot đối mặt khách hàng nên ghi rõ "đang trả lời bởi AI"; (b) không dùng dữ liệu khách trái luật để huấn luyện/tinh chỉnh; (c) quyết định ảnh hưởng quyền lợi cá nhân (tuyển dụng, tín dụng, kỷ luật) giữ người quyết định cuối. Đây là diễn giải thận trọng của chúng tôi, không phải kết luận pháp lý.

### 4.6 Còn thiếu (chưa tìm/chưa xác minh)

- Luật Dữ liệu 2024 (Luật số 60/2024/QH15, theo trí nhớ, hiệu lực 01/7/2025) và quy định về "dữ liệu quan trọng/dữ liệu cốt lõi" chuyển ra nước ngoài: **chưa tra**.
- Nghị định xử phạt vi phạm hành chính về bảo vệ dữ liệu cá nhân: thấy tiêu đề một tài liệu EY "Decree 330 ... sanctions for personal data protection" trong kết quả tìm kiếm nhưng **chưa đọc**; không dùng mức phạt cho tới khi đọc.
- Văn bản về sở hữu trí tuệ với nội dung do AI tạo, và quy định ngành (ngân hàng, y tế, giáo dục): chưa tra.
- Hướng dẫn chính thức của Bộ Công an/A05 cho SME về hồ sơ: chưa tra.

## 5. Dịch vụ AI: dữ liệu có bị dùng để huấn luyện không (đọc 2026-11-11)

Nguyên tắc bền **[Đề xuất]**: gói tiêu dùng/miễn phí thường có cài đặt cho phép dùng chat cải thiện mô hình; gói doanh nghiệp và API thường mặc định không huấn luyện nhưng vẫn có giữ log chống lạm dụng. Điều khoản và ngày hiệu lực thay đổi: mỗi lần triển khai phải đọc lại trang trong cột nguồn.

| Dịch vụ | Điều đọc được | Nguồn, ngày trang |
|---|---|---|
| **Anthropic, Claude Free/Pro/Max** | Chat và phiên code được dùng để huấn luyện nếu bạn bật "model improvement" trong cài đặt riêng tư; hội thoại bị gắn cờ an toàn có thể được dùng để cải thiện phát hiện vi phạm; chat Incognito không dùng để cải thiện Claude kể cả khi đã bật; phản hồi (thumbs) lưu tối đa 5 năm, tách khỏi ID người dùng khi dùng; dữ liệu thô từ connector không bị dùng trừ khi bạn dán vào chat | privacy.claude.com/en/articles/10023580 , trang ghi 16/3/2026 |
| **Anthropic, Team/Enterprise/API** | Mặc định **không** dùng đầu vào/đầu ra của sản phẩm thương mại để huấn luyện; ngoại lệ khi bạn gửi phản hồi/báo lỗi hoặc chủ động cho phép (thì cả hội thoại liên quan có thể được lưu tối đa 5 năm và dùng). Trang này không nêu thời gian lưu log API thường | privacy.claude.com/en/articles/7996868 , trang ghi 18/8/2026 |
| **OpenAI, ChatGPT cá nhân** | Có cài đặt "Improve the model for everyone" (Settings, Data Controls) hoặc cổng riêng tư "Do not train on my content"; tắt thì không huấn luyện trên hội thoại mới; phản hồi thumbs up/down có thể đưa cả hội thoại vào huấn luyện; Temporary Chat không dùng để huấn luyện (theo bản mới) | help.openai.com/en/articles/5722486 , **chỉ đọc qua tóm tắt kết quả tìm kiếm** (trang chính thức openai.com và help.openai.com trả 403 khi tải); nhiều phiên bản có ngày "Updated" khác nhau |
| **OpenAI, Business/Enterprise/API** | Mặc định không huấn luyện trên đầu vào/đầu ra cho người dùng doanh nghiệp (cả hai nguồn). Với API: "kể từ 1/3/2023 dữ liệu gửi API không dùng để huấn luyện (trừ khi bạn chủ động chia sẻ)"; log chống lạm dụng giữ **tối đa 30 ngày** mặc định; Zero Data Retention là tùy chọn cần được duyệt, không phải mặc định | developers.openai.com/api/docs/guides/your-data (đọc trực tiếp; trang không ghi ngày xuất bản); help.openai.com (qua tóm tắt tìm kiếm) |
| **Google, Gemini Apps (cá nhân)** | Một phần chat được người (kể cả nhà cung cấp dịch vụ của Google) xem xét; chat được tách khỏi tài khoản trước khi gửi; chat đã xem xét lưu tới 3 năm và xóa hoạt động không xóa chúng; tắt "Keep Activity" thì chat tương lai không dùng để cải thiện, nhưng chat vẫn lưu 72 giờ; Temporary Chat không dùng để huấn luyện; trang dặn "đừng nhập thông tin bí mật mà bạn không muốn người xem xét thấy" | support.google.com/gemini/answer/13594961 |
| **Google, Gemini API** | Dịch vụ **không trả phí**: Google có thể dùng đầu vào/đầu ra để cải thiện sản phẩm, người xem xét có thể đọc; trang dặn "không gửi thông tin nhạy cảm, bí mật hay cá nhân" (ngoại lệ EEA, Thụy Sĩ, Anh: áp dụng điều khoản trả phí). Dịch vụ **trả phí**: không dùng prompt để cải thiện sản phẩm, xử lý theo Data Processing Addendum, có ghi log trong thời gian giới hạn để chống vi phạm/bảo mật/yêu cầu pháp lý. Grounding with Google Search: lưu 30 ngày. Hiệu lực 23/3/2026 | aistudio.google.com/docs/terms (đã chuyển hướng từ ai.google.dev/gemini-api/terms) |

**[Đề xuất] Quy tắc thực hành:** (1) SME không dùng bản miễn phí/cá nhân cho dữ liệu mức "bí mật" trở lên; (2) nếu dùng cá nhân thì tắt tùy chọn huấn luyện và vẫn không dán dữ liệu cá nhân; (3) với Gemini API, tài khoản miễn phí = dữ liệu có thể bị xem: chỉ dùng dữ liệu công khai; (4) ghi vào Sổ prompt gói/tài khoản nào đang dùng cho nghiệp vụ nào; (5) kiểm tra lại các trang này mỗi quý.

**Điều chưa nêu được:** nơi lưu trữ dữ liệu (vùng/quốc gia) của từng dịch vụ cho khách Việt Nam, và việc có/không DPA riêng cho doanh nghiệp Việt, chưa đọc. Quan trọng với chuyển dữ liệu ra nước ngoài (mục 6).

## 6. Chuyển dữ liệu ra nước ngoài khi dùng AI đám mây [Đề xuất cách suy luận; cần luật sư]

Khi gửi dữ liệu cá nhân của người ở Việt Nam đến máy chủ AI ở nước ngoài, về cơ bản đó có thể được coi là **chuyển dữ liệu cá nhân xuyên biên giới** (Điều 20 Luật 91/2025, theo tóm tắt). Các bước sàng lọc:
1. Dữ liệu gửi có dữ liệu cá nhân không? Nếu đã ẩn danh thật sự thì nghĩa vụ nhẹ hơn (cần luật sư xác nhận cái gì là "ẩn danh thật sự").
2. Doanh nghiệp có thuộc nhóm được miễn (hộ kinh doanh, siêu nhỏ, nhỏ/khởi nghiệp trong 5 năm) và **không** thuộc ngoại lệ (xử lý dữ liệu nhạy cảm, dịch vụ xử lý dữ liệu, số lượng lớn)? Nguồn tóm tắt: miễn một số điều (Điều 21, 22, khoản 2 Điều 33) chứ chưa chắc miễn mọi nghĩa vụ **[Nguồn: luatvietnam.vn]**.
3. Có sự đồng ý hợp lệ, lưu được bằng chứng (NĐ 356 yêu cầu đồng ý kiểm chứng được)?
4. Nếu bắt buộc lập hồ sơ: ai nộp, nộp cho ai (A05 theo EY), biểu mẫu nào (Mẫu 09/10 theo EY), chờ thẩm định trước theo EY.
5. Cách giảm rủi ro rẻ nhất: **không gửi dữ liệu cá nhân** (ẩn danh trước khi gọi API), giữ bảng tra ngược trong nước.

## 7. Chuỗi bài nhỏ

### Bài A1: Phân loại dữ liệu công ty
- **Mục tiêu:** có bảng phân loại 5 mức.
- **Thực hành:** liệt kê 20 loại tài liệu hay dán vào AI (hợp đồng, sao kê, CV, danh sách khách...), gán mức theo 3.1, ghi người chịu trách nhiệm.
- **Sản phẩm:** bảng phân loại. **Lỗi:** coi "dữ liệu khách" là một loại; không tách nhạy cảm.

### Bài A2: Trang quy tắc 1 tờ A4
- **Thực hành:** 5 điều "không dán", 5 điều "được dán", nơi hỏi khi nghi ngờ, người duyệt, hậu quả. Nhân viên ký đã đọc.
- **Lỗi:** quy tắc quá dài, không ai đọc.

### Bài A3: Ẩn danh bằng script
- **Thực hành:** viết hàm thay SĐT/email/CCCD/tên bằng mã; lưu bảng tra ngược cục bộ; kiểm hồi quy với 20 mẫu, đếm sót. **Sản phẩm:** `anonymize.py` + báo cáo sót. **Lỗi:** quên tên viết thường/không dấu; địa chỉ nhà.
- **Chưa chạy thử trong tài liệu này.**

### Bài A4: Cài đặt tài khoản và đối chiếu điều khoản
- **Thực hành:** với mỗi dịch vụ công ty dùng, chụp màn hình cài đặt huấn luyện, ghi ngày, so với bảng mục 5; lập lịch kiểm lại hằng quý.
- **Lỗi:** tin ảnh chụp cũ; nhân viên dùng bản cá nhân khác bản công ty.

### Bài A5: Kiểm kê shadow AI và kế hoạch chuyển
- **Thực hành:** dùng khảo sát C0.1; chia công cụ thành "cho phép / cho phép có điều kiện / cấm"; chuyển người dùng sang công cụ chính thức.
- **Lỗi:** cấm hàng loạt mà không có công cụ thay thế.

### Bài A6: Quy trình sự cố
- **Thực hành:** nếu nhân viên lỡ dán dữ liệu cá nhân/bí mật: (1) báo trong ngày; (2) xóa hội thoại và kiểm tra cài đặt huấn luyện; (3) ghi lại thông tin gì, vào dịch vụ nào, thời điểm; (4) đánh giá có phải vi phạm cần thông báo (hỏi luật sư; NĐ 356 có quy định thông báo vi phạm, EY nêu 72 giờ cho dữ liệu vị trí/sinh trắc học). **Lỗi:** giấu sự cố vì sợ bị phạt.

## 8. Tài liệu tham khảo

Truy cập 2026-11-11. Tin cậy: Cao = nhà cung cấp/cơ quan chính thức; Trung bình = hãng tư vấn/trang pháp luật/báo chí; Thấp = snippet tìm kiếm, chưa đọc nội dung.

| Tiêu đề | URL | Loại | Tin cậy |
|---|---|---|---|
| Luật BVDLCN 2025 có hiệu lực khi nào? (luatvietnam.vn) | https://luatvietnam.vn/dan-su/luat-bao-ve-du-lieu-ca-nhan-2025-co-hieu-luc-khi-nao-568-103652-article.html | Trang pháp luật | Trung bình |
| EY Vietnam: Nghị định 356/2025/NĐ-CP | https://www.ey.com/vi_vn/technical/tax/tax-and-law-updates/nghi-dinh-so-356-2025-nd-cp-quy-dinh-chi-tiet-mot-so-dieu-va-bien-phap-thi-hanh-luat-bao-ve-du-lieu-ca-nhan | Hãng tư vấn | Trung bình-Cao |
| Doanh nghiệp xóa dữ liệu NLĐ khi nghỉ việc (lsvn.vn) | https://lsvn.vn/tu-nam-2026-doanh-nghiep-phai-xoa-du-lieu-ca-nhan-cua-nguoi-lao-dong-khi-nghi-viec-a167358.html | Trang pháp luật | Trung bình |
| Quốc hội thông qua Luật Trí tuệ nhân tạo (Báo Đại biểu Nhân dân) | https://daibieunhandan.vn/quoc-hoi-thong-qua-luat-tri-tue-nhan-tao-10399959.html | Báo chí của cơ quan Quốc hội | Trung bình-Cao |
| Luật Trí tuệ nhân tạo có hiệu lực từ 1/3/2026 (VnEconomy) | https://vneconomy.vn/luat-tri-tue-nhan-tao-se-co-hieu-luc-tu-ngay-132026.htm | Báo chí | Trung bình |
| 6 hành vi bị cấm khi sử dụng AI (Znews) | https://znews.vn/6-hanh-vi-bi-cam-khi-su-dung-tri-tue-nhan-tao-post1609885.html | Báo chí | Trung bình |
| Luật Công nghiệp công nghệ số 71/2025/QH15 (thuvienphapluat.vn) | https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Luat-Cong-nghiep-cong-nghe-so-2025-so-71-2025-QH15-621341.aspx | Trang pháp luật | Thấp-Trung bình (chỉ thấy kết quả tìm kiếm; trang thuvienphapluat trả 403 khi tải) |
| Luật AI 134/2025/QH15 (thuvienphapluat.vn) | https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/Luat-Tri-tue-nhan-tao-2025-so-134-2025-QH15-679013.aspx | Trang pháp luật | Thấp (403, chưa đọc) |
| NĐ 356/2025 bản .doc (vbpl.moj.gov.vn) | https://vbpl.moj.gov.vn/TW/Lists/vbpq/Attachments/187276/ND.356.2025.doc | Cổng văn bản pháp luật (Bộ Tư pháp) | Cao nhưng **chưa đọc**; đọc đầu tiên khi kiểm tra |
| Anthropic: Is my data used for model training? (consumer) | https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training | Trợ giúp nhà cung cấp | Cao |
| Anthropic: commercial products | https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training | Trợ giúp nhà cung cấp | Cao |
| OpenAI: Your data (API) | https://developers.openai.com/api/docs/guides/your-data | Tài liệu nhà cung cấp | Cao |
| OpenAI: How your data is used to improve model performance | https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance | Trợ giúp nhà cung cấp | Thấp-Trung bình (chỉ qua tóm tắt tìm kiếm) |
| Google: Gemini Apps Privacy Hub | https://support.google.com/gemini/answer/13594961 | Trợ giúp nhà cung cấp | Cao |
| Google: Gemini API Additional Terms | https://aistudio.google.com/docs/terms | Điều khoản nhà cung cấp | Cao |
| MAP, arXiv 2512.04123 | https://arxiv.org/abs/2512.04123 | Bài báo | Cao (chưa đọc lại; không dùng số liệu ở file này) |

## 9. Chưa kiểm chứng / cần kiểm tra lại

1. **Toàn văn** Luật 91/2025/QH15, NĐ 356/2025, Luật 71/2025, Luật 134/2025: chưa đọc bản gốc. Đọc trước hết bản .doc NĐ 356 trên vbpl.moj.gov.vn và Công báo.
2. Ngày thông qua Luật 91/2025 (26/6/2025) chỉ có qua kết quả tìm kiếm tóm tắt.
3. Số điều của chuyển dữ liệu xuyên biên giới trong NĐ 356 (Điều 18 theo bài phân tích hay khác) và số biểu mẫu (09, 10, 01a/01b).
4. Mức phạt (1%-5% doanh thu; 3 tỷ đồng): chưa xác minh; chưa đọc nghị định xử phạt.
5. Nghị định 142/2026/NĐ-CP và thời hạn chuyển tiếp 12/18 tháng của Luật AI: chỉ nằm trong tóm tắt tìm kiếm.
6. Danh mục sản phẩm số do AI tạo phải gắn dấu nhận dạng (Luật 71/2025): chưa biết đã ban hành chưa.
7. Luật Dữ liệu 2024 và quy định dữ liệu quan trọng/cốt lõi: chưa tra.
8. ChatGPT consumer: chỉ qua tóm tắt tìm kiếm nhiều phiên bản; cần mở trang chính thức bằng trình duyệt.
9. Nơi lưu dữ liệu, DPA, thời gian lưu log của từng dịch vụ cho khách Việt Nam: chưa đọc.
10. Cách tính "doanh nghiệp nhỏ/siêu nhỏ/khởi nghiệp" áp dụng cho từng SME cụ thể (theo luật hỗ trợ doanh nghiệp nhỏ và vừa): chưa tra.
11. Tất cả bảng phân loại, quy tắc, quy trình ở mục 3, 6, 7 là **đề xuất của chúng tôi**, không phải yêu cầu pháp luật.

**Nhắc lại:** tài liệu này không thay thế tư vấn pháp lý. Với dữ liệu nhạy cảm, quy mô lớn, hoặc gửi ra nước ngoài, hãy tham vấn luật sư/đơn vị bảo vệ dữ liệu cá nhân trước khi triển khai.
