# Q1 — Tự động hóa thường (không AI)

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn; **[Thao tác]** = hay đổi, có ngày tra.

## 1) Mục tiêu và người đọc

**Người đọc:** người phụ trách vận hành, kế toán, hoặc "người giỏi Excel" của công ty. Biết công thức bảng tính; code là tùy chọn.

**Sau cấp này có:** một luồng tự động chạy hằng ngày cho 1-2 bước nhãn **Quy tắc** từ Q0. Ví dụ: biểu mẫu có trường bắt buộc → ghi vào bảng → chuyển đúng người theo luật → nhắc khi quá hạn.

**Thứ chạy được độc lập:** luồng tự động đó, kèm nhật ký chạy và một người chịu trách nhiệm. Không có AI. Nếu dừng ở đây, công ty vẫn có lợi.

## 2) Câu hỏi cấp này trả lời / lỗi của Q0

**Câu hỏi:** "Phần nào của quy trình làm được bằng luật cố định, để khỏi trả tiền và khỏi chịu rủi ro của AI?"

**Lỗi Q0 để lại:** đã biết bước nào chép tay, chờ ký, quên nhắc; nhưng vẫn làm tay.

**Lý do không nhảy thẳng lên AI:**
- **[Nguồn]** So sánh có kiểm soát (arXiv 2509.04198): RPA (UiPath) thành công 10/10 lần ở cả 3 bài thử; agent dùng máy tính (Claude Sonnet 4) thành công 0/1, 9/10 và 6/10, và chậm hơn có ý nghĩa thống kê (ví dụ bài hóa đơn: 20 giây so với 202,8 giây). Điểm mạnh của agent: dựng nhanh hơn (≈15 phút so với ≈240 phút ở bài hóa đơn). Tác giả kết luận agent chưa sẵn sàng cho luồng quan trọng. Giới hạn: 3 bài thử, 1 người dựng RPA, 1 công cụ mỗi loại.
- **[Nguồn]** τ-bench (arXiv 2406.12045): cùng một việc chạy 8 lần, gpt-4o thành công cả 8 lần ở dưới 25% số việc bán lẻ. Luật cố định thì cho cùng kết quả mỗi lần.
- **[Nguồn]** Anthropic "Building effective agents" (nhóm RAG đã đọc): tìm giải pháp đơn giản nhất, chỉ tăng độ phức tạp khi cần.

## 3) Kiến thức nền

### 3.1 Ba khối của mọi luồng tự động [Đề xuất]
1. **Kích hoạt (trigger):** biểu mẫu được nộp; dòng mới trong bảng; giờ định kỳ; sự kiện từ phần mềm (webhook).
2. **Luật:** điều kiện "nếu ... thì ..." viết được ra giấy.
3. **Hành động:** ghi dòng, gửi thông báo, tạo việc, gọi API.

Thêm hai thứ bắt buộc: **nhật ký** (mỗi lần chạy ghi một dòng) và **người chịu trách nhiệm** (ai nhận cảnh báo khi luồng lỗi).

### 3.2 Công cụ SME Việt Nam hay dùng [Thao tác, tra 2026-11-11]

| Công cụ | Hợp với | Giới hạn đã xác minh | Lưu ý dữ liệu [Đề xuất] |
|---|---|---|---|
| Google Sheets + Apps Script | Công ty đã dùng Google; biểu mẫu Google Forms | Mỗi lần chạy tối đa 6 phút; tổng trigger 90 phút/ngày (gmail) hoặc 6 giờ/ngày (Workspace); 20 trigger/người/script; email gửi 100 người/ngày (gmail), 1.500 (Workspace) [Nguồn: trang quota chính thức] | Dữ liệu ở Google; dùng tài khoản công ty, không dùng gmail cá nhân |
| Lark Base + Automation, Lark Approval | Công ty dùng Lark làm chat nội bộ | Base nhận webhook: 5 sự kiện/giây mỗi luồng, 50/giây mỗi Base, 4 MB/yêu cầu, cần Bearer token [Nguồn: trợ giúp Lark] | Nơi lưu dữ liệu của Lark cho khách Việt Nam: **chưa kiểm** |
| Make | Nối nhiều ứng dụng có sẵn, kéo thả | Gói miễn phí 1.000 operations/tháng, 2 scenario, chu kỳ ≥15 phút; mỗi module chạy = 1 operation [Nguồn: trang giá, qua tóm tắt tìm kiếm] | Dữ liệu đi qua máy chủ Make ở nước ngoài |
| Zapier | Như Make | Giá, hạn mức: **chưa đọc trang chính thức** | Như Make |
| n8n tự host | Có người biết dựng máy chủ; muốn dữ liệu ở máy mình | Community (Sustainable Use License) miễn phí khi chỉ người trong tổ chức tạo/sửa workflow; không bán lại n8n như dịch vụ [Nguồn: FAQ giấy phép] | Dữ liệu ở máy chủ mình chọn; tự lo cập nhật bảo mật, sao lưu |
| Automation sẵn trong phần mềm bán hàng/kế toán | Luồng chỉ trong một phần mềm | Tùy phần mềm; **chưa kiểm** từng hãng | Không thêm chặng dữ liệu |

Khả năng kết nối phần mềm SME (đã xác minh một phần, xem `00-README.md` mục 5): KiotViet có Public API cho đơn, hóa đơn, hàng hóa, khách hàng; Haravan có webhook ký HMAC; MISA AMIS Kế toán cho phép đẩy chứng từ qua API; Sapo chưa tìm được tài liệu chính thức.

### 3.3 Cạm bẫy của automation thường [Đề xuất]
- **Luồng chạy ngầm, không ai xem.** Lỗi im lặng nhiều tuần. Cần cảnh báo khi lỗi và khi "không chạy" (ví dụ cả ngày không có dòng mới).
- **Chạy trùng.** Biểu mẫu nộp 2 lần, trigger chạy chồng nhau. Apps Script có `LockService` để "ngăn truy cập đồng thời vào một đoạn code" [Nguồn]. Chi tiết ở Q5.
- **Quyền rộng.** Kết nối Make/Zapier với "toàn bộ Gmail/Drive". Cấp quyền hẹp nhất có thể.
- **Phụ thuộc người dựng.** Người dựng nghỉ việc, không ai sửa được. Ghi sơ đồ và lưu ở nơi chung.

## 4) Chuỗi bài nhỏ

### Bài Q1.1 — Biểu mẫu thay tin nhắn
- **Làm:** chuyển yêu cầu đang gửi qua Zalo thành biểu mẫu (Google Forms, Lark Form, hoặc biểu mẫu trong phần mềm) với trường bắt buộc, danh sách chọn (dự án, loại chi phí), kiểm định dạng (số tiền là số, ngày hợp lệ).
- **Sản phẩm:** biểu mẫu + bảng nhận dữ liệu có cột `ma_phieu`, `trang_thai`, `nguoi_xu_ly`, `han`.
- **Lỗi:** để ô "ghi chú" tự do thay cho trường có cấu trúc; không có mã phiếu.

### Bài Q1.2 — Định tuyến bằng luật
- **Làm:** bảng tra "loại yêu cầu → người nhận", "số tiền > X → thêm người duyệt". Luật nằm ở **một bảng** người quản lý sửa được, không nằm rải trong code.
- **Sản phẩm:** bảng luật + luồng gửi thông báo cho người nhận (email, Lark, Zalo nhóm nội bộ).
- **Lỗi:** chép số hạn mức cứng vào nhiều chỗ; không có người dự phòng khi người nhận nghỉ.

### Bài Q1.3 — Nhắc hạn và leo thang
- **Làm:** trigger theo giờ quét các phiếu `cho_duyet` quá hạn; nhắc người xử lý; quá 2 lần thì báo cấp trên.
- **Sản phẩm:** luồng nhắc + cột `so_lan_nhac`.
- **Lỗi:** nhắc lúc nửa đêm; nhắc lặp vô hạn.

### Bài Q1.4 — Chuyển dữ liệu giữa hệ thống không chép tay
- **Làm:** chọn một chặng chép tay (ví dụ đơn Haravan → Sheet kho, phiếu đã duyệt → chứng từ MISA). Dùng webhook/API hoặc xuất-nhập file theo lịch. Đối chiếu số dòng hai bên mỗi ngày.
- **Sản phẩm:** luồng chuyển + bảng đối chiếu ngày (số dòng nguồn, số dòng đích, chênh).
- **Lỗi:** không đối chiếu, mất đơn im lặng; dùng tài khoản admin cho kết nối.

### Bài Q1.5 — Nhật ký và cảnh báo
- **Làm:** mỗi lần chạy ghi: thời điểm, luồng, `ma_phieu`, kết quả, lỗi. Gửi cảnh báo khi lỗi và khi 24 giờ không chạy.
- **Sản phẩm:** tab "nhật ký" + quy tắc cảnh báo. Mẫu trường log xem `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` bài 9.1 (bỏ các trường về mô hình).
- **Lỗi:** ghi cả SĐT, địa chỉ khách vào nhật ký mà không che.

### Bài Q1.6 — Đo lại so với nền
- **Làm:** sau 2 tuần, đo cùng cách như Q0.5. So sánh trung vị thời gian, số lỗi, thời gian chờ.
- **Sản phẩm:** bảng trước/sau. Ghi cả thời gian dựng và bảo trì.

## 5) Đường không code vs có code; khi nào buộc chuyển

| | Không code | Có code nhẹ |
|---|---|---|
| Công cụ | Forms + Sheets công thức; Lark Base automation; Make/Zapier; n8n giao diện | Apps Script; script Python chạy theo lịch; n8n node Code |
| Ưu | Dựng nhanh, người không biết code sửa được | Kiểm điều kiện phức tạp, đối chiếu, khóa chống trùng, nhật ký đầy đủ |
| Nhược | Khó kiểm trùng; khó test; chi phí tăng theo số lần chạy (Make tính theo module chạy) | Cần người bảo trì |

**Buộc chuyển sang code [Đề xuất] khi:** cần chống chạy trùng tin cậy (khóa, mã duy nhất); cần đối chiếu dữ liệu giữa hai hệ thống; số operation trên Make/Zapier vượt gói và tiền tăng nhanh; luồng cần chạy lâu hơn giới hạn (Apps Script 6 phút/lần); cần test tự động khi sửa luật.

## 6) Tiêu chí lên Q2 (đo được) [Đề xuất]

1. ≥1 luồng tự động chạy ≥2 tuần với ≥95% lần chạy thành công theo nhật ký.
2. Có cảnh báo lỗi đến một người cụ thể, đã thử cố ý làm lỗi một lần.
3. Bảng trước/sau cho thấy thời gian hoặc lỗi giảm, hoặc ghi rõ "không giảm" và lý do.
4. Còn lại một bước mà luật không làm được vì đầu vào là chữ tự do (tin nhắn, email, CV). Nếu không còn bước nào như vậy, **không cần lên Q2**.

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

**a) Công ty xây lắp 30 người (tiếp Q0).** Google Form "Đề nghị thanh toán" với trường: dự án (chọn), loại chi phí (chọn), số tiền (số), ảnh chứng từ (tải lên), người đề nghị (email công ty). Apps Script trigger khi nộp: gán `ma_phieu`, tra bảng luật (dự án → trưởng công trình; > 20 triệu → thêm giám đốc), gửi email kèm link duyệt. Trigger mỗi sáng 8 giờ nhắc phiếu chờ > 2 ngày. Không AI. Kết quả giả định: thời gian chờ trung vị từ 4 ngày xuống 2 ngày; lỗi "thiếu thông tin" gần như hết vì trường bắt buộc.

**b) Phòng khám nha 12 người, đặt lịch qua Zalo OA và điện thoại.** Luồng Lark Base: lễ tân nhập lịch hẹn vào Base; automation gửi nhắc cho bác sĩ phụ trách trước 1 ngày; lịch hủy tự đổi trạng thái ghế trống. Lưu ý: tên bệnh nhân + tình trạng răng là dữ liệu sức khỏe, thuộc nhóm nhạy cảm theo NĐ 356 (tóm tắt EY); không đưa vào AI, chỉ ghi mã bệnh nhân trong thông báo. Gửi tin nhắc cho bệnh nhân qua ZNS cần kiểm điều kiện, giá trên developers.zalo.me (chưa kiểm).

**c) Cửa hàng mỹ phẩm (tiếp Q0).** Webhook đơn mới từ Haravan → n8n tự host → ghi dòng vào Sheet kho và báo nhóm đóng gói. Bước 6 "chép sang Sheet theo dõi" đã bỏ ở Q0.

## 8) Tài liệu tham khảo

| Nguồn | Loại | Mức đọc | Tin cậy |
|---|---|---|---|
| Průcha, Matoušková, Strnad, "Are LLM Agents the New RPA?", arXiv 2509.04198 | So sánh có kiểm soát, nhỏ | Toàn văn | Trung bình (3 bài thử, 1 người dựng) |
| τ-bench, arXiv 2406.12045 | Benchmark (Sierra) | Toàn văn | Cao cho thiết lập đó; mô hình cũ (2024) |
| Google Apps Script quotas, https://developers.google.com/apps-script/guides/services/quotas | Tài liệu chính thức | Đọc trực tiếp | Cao; hay đổi |
| Google Apps Script LockService, https://developers.google.com/apps-script/reference/lock/lock-service | Tài liệu chính thức | Đọc trực tiếp | Cao |
| Lark: webhook triggers trong Base, https://larksuite.com/hc/en-US/articles/661148936282 và 956909912947 | Trợ giúp chính thức | Qua tóm tắt tìm kiếm | Trung bình-cao |
| Make pricing, https://www.make.com/en/pricing | Trang giá | Qua tóm tắt tìm kiếm | Trung bình; đổi thường xuyên |
| n8n license FAQ, https://docs.n8n.io/n8n-community-license/community-license/license-faq | Tài liệu chính thức | Qua tóm tắt tìm kiếm | Cao |
| KiotViet Kết nối API, https://www.kiotviet.vn/huong-dan-su-dung-kiotviet/retail-ket-noi-api/ | Hướng dẫn chính thức | Đọc trực tiếp | Cao; thiếu chi tiết kỹ thuật |
| Haravan connect webhook, https://docs.haravan.com/docs/tutorials/webhooks/connect-webhook/ | Tài liệu chính thức | Đọc trực tiếp | Cao |
| MISA AMIS Kế toán kết nối API, https://helpact.misa.vn/?p=12579 | Trợ giúp chính thức | Qua tóm tắt tìm kiếm | Trung bình (2021-2023) |

## 9) Chưa kiểm chứng

- Zapier: giá, hạn mức, vị trí dữ liệu. Make: vị trí máy chủ, điều khoản xử lý dữ liệu.
- Lark: nơi lưu dữ liệu cho khách Việt Nam; Lark Approval có tự động hóa không cần code tới mức nào.
- KiotViet: webhook bản bán lẻ, gói nào có API, giới hạn tốc độ. Sapo: API/webhook. Automation có sẵn trong phần mềm bán hàng/kế toán: chưa kiểm từng hãng.
- ZNS/ZBS: điều kiện, giá, quy định nội dung.
- Ngưỡng 95% thành công, 2 tuần, 20 triệu, 2 ngày ở mục 6-7 là đề xuất/giả định.
- Kết quả RPA vs agent có thể khác với mô hình mới hơn; bài dùng Claude Sonnet 4 (2025-05).
