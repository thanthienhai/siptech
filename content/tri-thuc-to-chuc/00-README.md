# Nhóm bài toán: Bộ nhớ và tri thức tổ chức

> Ngày soạn: 2026-11-11. Thuộc series "AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp".
> Quy ước: **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế, suy luận, ngưỡng của nhóm soạn. Mọi ngưỡng và cỡ mẫu là [Đề xuất].
> Không phải tư vấn pháp lý. Khung chung về dữ liệu: `../an-toan-du-lieu-va-phap-ly-vn.md`.

!!! tip "Tóm tắt nhanh"
    **Nhóm này giúp ai:** chủ doanh nghiệp nhỏ và vừa (SME), quản lý, kế toán, nhân sự, nhân viên văn phòng, những người đang thấy cách làm việc của công ty chỉ nằm trong đầu vài người giỏi và trong tin nhắn Zalo. Bạn **không cần biết lập trình**.

    **Giải quyết việc gì:** dùng AI để **tạo ra và giữ** tài liệu của công ty: biên bản họp, bản ghi chép từ ghi âm, quy trình làm việc (SOP), kho tri thức có người chịu trách nhiệm, báo cáo định kỳ.

    **Học theo thứ tự nào:** đi từ cấp C0 đến C7. Cấp đầu nhẹ nhất (chỉ cần một tài khoản AI và vài cuộc họp để thử), cấp sau mới thêm việc đo và vận hành.

    **Sau cùng có gì:** một bộ mẫu, bảng kiểm, sổ theo dõi và quy trình nhỏ mà công ty bạn tự dùng được, kèm cách tự kiểm tra xem AI có đang làm sai không.

## 1. Bài toán là gì

**Ai gặp việc này?** Gần như mọi công ty nhỏ và vừa. Ở SME, quy trình thường nằm trong đầu vài người làm giỏi và trong tin nhắn Zalo. Khi người đó bận, nghỉ phép hay nghỉ việc, công việc chậm hoặc sai.

**Hàng ngày nó trông thế nào?** Họp xong, mỗi người hiểu một kiểu và việc rơi rụng. Muốn hỏi "khách này giảm giá bao nhiêu" thì phải nhắn cho đúng một người. Có tài liệu Word hay Google Docs nhưng không ai biết bản nào mới nhất. Nhân viên cũ nghỉ thì cả cách làm của họ đi theo.

**Nhóm bài này giúp gì?** Dạy dùng AI để **tạo ra và giữ** tài liệu:

1. Tóm tắt họp, lập biên bản có danh sách việc (ai, việc gì, hạn).
2. Ghi âm tiếng Việt thành văn bản, biết nó sai ở đâu.
3. Viết SOP từ lời kể, ghi âm, tin nhắn của người làm giỏi (phỏng vấn có hướng dẫn bằng AI). SOP là chữ viết tắt của "quy trình thao tác chuẩn": bản hướng dẫn từng bước để ai làm cũng ra kết quả giống nhau.
4. Giữ kho tri thức có chủ: mỗi tài liệu có người chịu trách nhiệm, hạn rà soát, trạng thái.
5. Phát hiện mâu thuẫn và tài liệu lỗi thời.
6. Gom bài học sau sự cố/dự án; bàn giao khi nhân viên nghỉ.
7. Lập báo cáo định kỳ từ nhiều nguồn.

!!! tip "Nói đơn giản"
    Nhóm này giống việc **xây cuốn sổ tay của công ty** và giữ cho nó luôn đúng. AI là người giúp bạn viết nhanh, còn bạn (và người chủ của từng tài liệu) là người duyệt.

**Khác với nhóm RAG** (`../rag-tra-cuu-tai-lieu/`): RAG là cách cho AI **tìm và trả lời dựa trên** tài liệu có sẵn. Nhóm này làm ra tài liệu đó và giữ cho nó đúng. Đầu ra của nhóm này (SOP, bảng giá, chính sách đã có chủ và ngày hiệu lực) là đầu vào cho nhóm RAG và nhóm `../xu-ly-yeu-cau-khach/`.

## 2. Vì sao SME Việt Nam gặp bài toán này

Dưới đây là ba lý do, kèm nhãn cho biết mỗi ý lấy từ đâu.

- **[Nguồn, thứ cấp]** Khảo sát AWS/Strand (qua báo): 74% doanh nghiệp Việt Nam đã dùng AI ở giai đoạn "thăm dò"; rào cản lớn nhất là thiếu nhân lực (xem `../thuc-trang-sme-viet-nam.md`). "Thứ cấp" nghĩa là chúng ta đọc con số này qua một bài báo, không đọc khảo sát gốc.
- **[Nguồn]** Nghiên cứu 21 SMB (doanh nghiệp nhỏ và vừa) ở Kenya/Nigeria (arXiv 2610.31344, qua `../thuc-trang-sme-viet-nam.md`): lỗi lặp lại là "thiếu tri thức thể chế", tức là kiến thức làm việc của tổ chức không được ghi lại hay chia sẻ. Đây không phải số đo Việt Nam. (arXiv là kho đăng các bài nghiên cứu khoa học; chuỗi số đi kèm là mã của bài.)
- **[Đề xuất, quan sát]** Ở SME Việt Nam, quy định thường được "chốt" trong nhóm Zalo rồi trôi mất. Tài liệu Word/Google Docs nếu có thì không ai biết bản nào mới. Chưa có khảo sát đo trực tiếp điều này (xem mục 7).

!!! tip "Nói đơn giản"
    Hai ý đầu là số liệu của người khác, chỉ cho thấy vấn đề có thật ở nơi khác. Ý thứ ba là quan sát của nhóm soạn về công ty Việt Nam, chưa có số đo. Bạn hãy đối chiếu với công ty mình xem có đúng không.

## 3. Bằng chứng tóm tắt

Bảng dưới đây gom các nghiên cứu mà cả nhóm bài dựa vào, mỗi dòng kèm một ý "vậy thì SME nên làm gì". Bạn **không cần đọc hết ngay**; chi tiết và số liệu nằm ở mục 3 và 8 của từng cấp.

| Phát hiện | Nguồn | Ý nghĩa cho SME [Đề xuất] |
|---|---|---|
| Phần lớn thất bại còn lại của hệ thống Airbnb do SOP thiếu bước mà nhân viên giỏi vẫn làm | Airbnb arXiv 2610.14428 (qua `../nen-tang-bang-chung.md`) | Chất lượng tài liệu quyết định chất lượng AI phía sau |
| SOP viết cho người đọc thường bỏ tri thức ngầm (ví dụ ngưỡng "$250" là bao gồm hay không) | IBM arXiv 2611.11348 | Phỏng vấn phải hỏi ranh giới và ngoại lệ |
| Lỗi trả lời về cuộc họp chủ yếu là diễn giải quá tự tin, bịa con số, gán sai người nói, biến thảo luận thành quyết định, bịa việc cần làm | Microsoft arXiv 2608.20392 (bản ghi tiếng Anh) | Biên bản AI phải có trích nguyên văn và trạng thái "đã chốt/đề xuất" |
| Có danh sách tên người dự họp và tài liệu đi kèm thì gán người phụ trách đúng hơn rõ rệt (0,524 → 0,792 trên dữ liệu tổng hợp) | Otter.ai arXiv 2610.29319 | Luôn đưa danh sách người dự họp vào prompt (prompt là đoạn chỉ dẫn bạn gõ cho AI) |
| Tóm tắt họp Teams có Copilot nhanh hơn 19%, độ chính xác không đổi có ý nghĩa thống kê; người dùng tự ước tiết kiệm 36 phút, thí nghiệm đo được 12 phút (cả 4 tác vụ) | Slide thí nghiệm Microsoft (Edelman, 5/2024), 147 người trên Upwork | Đo bằng đồng hồ, không hỏi cảm nhận |
| Nhận dạng giọng nói tiếng Việt chênh rất lớn giữa các dịch vụ (cuộc gọi điện thoại: 6,7% đến 50,8% câu sai nghĩa) | mu-bench arXiv 2609.32082 | Tự đo trên ghi âm của chính công ty trước khi chọn |
| Bộ nhớ quy tắc dùng chung, có người duyệt, tuân thủ chính sách cao hơn RAG trên 10 tình huống tổng hợp | SAP Signavio arXiv 2607.03228 | Tách tri thức thành mục quy tắc nhỏ có chủ, có nguồn |
| LLM (mô hình ngôn ngữ lớn, loại AI đứng sau các chatbot) phát hiện mâu thuẫn trong văn bản báo nhầm nhiều (GPT-4o: tỷ lệ báo nhầm 0,399) | American Express arXiv 2601.02627 | Dùng AI để gợi ý, người chủ tài liệu quyết |
| ~900 đóng góp thành 1.144 mục bộ nhớ; **lợi ích chưa được đo** | SAP arXiv 2608.00122 (qua `../nen-tang-bang-chung.md`) | Gom bài học được, nhưng chưa có bằng chứng nó giúp |

!!! tip "Nói đơn giản"
    Điểm chung của cả bảng: **AI viết nhanh nhưng hay sai ở những chỗ khó thấy** (ai nói gì, ai nhận việc gì, con số nào). Vì vậy mỗi cấp trong nhóm đều có một bước để người kiểm tra lại.

**Giới hạn lớn nhất:** không nguồn nào đo trên cuộc họp tiếng Việt hay SME Việt Nam. Các số về họp đều trên bản ghi tiếng Anh (QMSum/AMI/ICSI) hoặc dữ liệu tổng hợp (dữ liệu do máy tạo ra, không phải cuộc họp thật).

## 4. Thang cấp độ của nhóm

Nhóm có 8 cấp, từ C0 đến C7. Cấp sau dựa vào cấp trước. Cột "File" là tên bài giảng của từng cấp.

| Cấp | File | Một dòng |
|---|---|---|
| C0 | `cap-00-bien-ban-hop-co-khuon.md` | Biên bản họp theo mẫu bằng Project/Gem; mỗi việc có trích nguyên văn; người chủ trì duyệt |
| C1 | `cap-01-ghi-am-thanh-van-ban.md` | Ghi âm tiếng Việt thành văn bản; tự đo WER/CER và tỷ lệ giữ tên riêng, con số; quy tắc ghi âm |
| C2 | `cap-02-soan-sop-tu-nguoi-gioi.md` | Phỏng vấn có hướng dẫn bằng AI để rút SOP từ người làm giỏi; thử SOP bằng người mới |
| C3 | `cap-03-so-dang-ky-tri-thuc.md` | Sổ đăng ký tài liệu: chủ sở hữu, hạn rà soát, trạng thái, nguồn; tách SOP lõi và ghi chú ngữ cảnh |
| C4 | `cap-04-mau-thuan-va-loi-thoi.md` | Phát hiện mâu thuẫn và lỗi thời: code so con số, AI gợi ý, chủ tài liệu quyết |
| C5 | `cap-05-bai-hoc-va-ban-giao.md` | Gom bài học sau sự cố/dự án; gói bàn giao khi nghỉ việc; quét dữ liệu nhạy cảm, kiểm trùng |
| C6 | `cap-06-bao-cao-dinh-ky.md` | Báo cáo định kỳ nhiều nguồn: code tính số, AI viết lời, code kiểm mọi con số |
| C7 | `cap-07-van-hanh-vong-tri-thuc.md` | Vận hành: nhịp rà soát, chỉ số, phân vai, đưa tài liệu sang RAG/CSKH, chạy lại ca thử |

Một vài từ trong bảng: **Project/Gem** là tính năng của Claude và Gemini cho phép lưu sẵn chỉ dẫn để dùng lại. **WER/CER** là hai tỷ lệ đo xem bản chép lời sai bao nhiêu từ hoặc ký tự (bài C1 giải thích kỹ). **CSKH** là chăm sóc khách hàng. **Code** là phần việc để máy làm, bạn có thể nhờ người biết lập trình hoặc nhờ AI chạy giúp.

**Nên bắt đầu từ cấp nào? [Đề xuất]** Hầu hết người mới nên bắt đầu ở **C0** (biên bản họp), vì ai cũng gặp và không cần công cụ gì thêm ngoài tài khoản AI. Chỉ cần làm C1 khi bạn thật sự cần ghi âm cuộc họp. Nếu công ty bạn đã có biên bản họp theo mẫu và được duyệt đều đặn, bạn có thể bỏ qua C0 và nhảy sang cấp có việc đang đau nhất: C2 nếu quy trình nằm trong đầu một vài người, C3 nếu tài liệu có nhưng lộn xộn. Phần "Thứ tự đọc" ở mục 8 cho biết người đã học nhóm RAG nên vào từ đâu.

Mỗi cấp có thứ chạy độc lập, rẻ, kiểm soát được. Có điểm duyệt của người ở chỗ rủi ro. Hàng rào bằng code được ưu tiên hơn hàng rào bằng prompt. Code mẫu ở cả 8 cấp đã chạy thử bằng `python -I -X utf8` với dữ liệu giả (không gọi API thật; ở C6 dùng hàm giả thay AI). API là cách để chương trình của bạn "gọi" một dịch vụ AI qua mạng.

!!! tip "Nói đơn giản"
    "Hàng rào bằng code hơn hàng rào bằng prompt" nghĩa là: thay vì chỉ **dặn** AI "đừng bịa", ta để một đoạn chương trình nhỏ **tự kiểm** xem AI có bịa không. Lời dặn có thể bị quên, còn phép kiểm thì không.

## 4b. Nguồn đã đọc và mức đọc

Mục này cho bạn biết nhóm soạn đã đọc mỗi nguồn kỹ đến đâu, để bạn biết nguồn nào tin được nhiều hơn. Mã dạng 2608.20392 là mã arXiv của bài nghiên cứu.

- **Đọc các trang chính qua alphaXiv (gần toàn văn, gồm bảng kết quả):** Microsoft EaS 2608.20392; FRAME 2509.15901; Otter OSynth 2610.29319; PhoWhisper 2406.02555; PhoASR 2603.14779; mu-bench 2609.32082; IBM SOP 2611.11348; American Express 2601.02627; SAP Signavio 2607.03228; AI phỏng vấn Copenhagen 2610.23149; tri thức ngầm mô phỏng 2507.03811.
- **Đọc trực tiếp:** 12 trang slide Microsoft (Edelman, 5/2024).
- **Qua công cụ tóm tắt trang web:** Điều 25, 32 Luật 91/2025 trên hethongphapluat.com; bài lsvn.vn về xóa dữ liệu NLĐ (NLĐ là người lao động).
- **Qua file nền của series (không đọc lại):** MAP, Nubank, Airbnb, BMO ESCROW, SAP 2608.00122.
- **Chỉ thấy tiêu đề/tóm tắt, chưa đọc:** QMSum 2104.05938; 2608.18177; 2609.03148; 2608.27391; 2603.14541; 2509.05983.

## 5. Tái dùng khối nào của nhóm RAG

Nhóm RAG đã dạy sẵn một số "khối" dùng chung. Nhóm này không viết lại, chỉ trỏ về và bổ sung phần khác biệt. Nếu bạn chưa học nhóm RAG, cứ mở khối được nhắc khi bài của nhóm này gọi tên.

| Khối RAG | Dùng ở đâu | Phần khác biệt viết ở nhóm này |
|---|---|---|
| `cap-00` bản giao việc 6 phần, SOP thành prompt, Sổ prompt | C0, C2 | C2 viết **cách lấy SOP ra từ người**, C0 RAG giả định SOP đã có |
| `cap-01` gọi API, JSON có cấu trúc, chi phí | C1, C6 | Không lặp lại |
| `cap-02` tài liệu thành text, kiểm bằng mẫu | C1 (CER), C5 | C1 áp dụng cho âm thanh |
| `cap-03` mã ổn định, phát hiện tài liệu đổi (Bài 3.8) | C3, C4 | C3 thêm **chủ sở hữu và hạn rà soát**; C4 thêm **mâu thuẫn giữa các tài liệu** |
| `cap-05` kiểm trích nguyên văn bằng code | C0, C4 | Áp cho trích dẫn từ bản ghi họp |
| `cap-06` bộ ca mẫu, khoảng tin cậy khi n nhỏ, kappa | C0, C1, C2, C7 | Không lặp lại |
| `cap-08` mục 7.b quy trình biên bản họp | C0 | C0 đi sâu vào lỗi đặc thù của họp và thứ tự xây dựng |
| `cap-09` nhật ký, phiên bản, trôi dạt | C7 | C7 thêm vòng đời tài liệu (không chỉ prompt) |

(JSON là một cách viết dữ liệu có khung rõ ràng để máy đọc được. "Khoảng tin cậy khi n nhỏ" là cách nói thật thà rằng số đo trên ít mẫu thì chưa chắc chắn. Kappa là một con số đo mức hai người chấm có đồng ý với nhau không.)

## 6. Rủi ro pháp lý và dữ liệu chính

Khi đưa cuộc họp, ghi âm hay hồ sơ nhân viên cho AI, bạn đang xử lý dữ liệu cá nhân. Đây là các rủi ro chính. Chi tiết ở mục 3 của C1 và C5. Tất cả **chưa đối chiếu Công báo**, tức là chưa so với bản luật chính thức. Đây không phải tư vấn pháp lý.

1. **Ghi âm cuộc họp.** Điều 32 Luật 91/2025/QH15 (theo bản đăng trên hethongphapluat.com) nói về ghi âm, ghi hình **nơi công cộng, hoạt động công cộng**: phải cho người bị ghi biết, dùng đúng mục đích, xóa khi hết thời hạn cần thiết. Họp nội bộ có thuộc "hoạt động công cộng" không thì **chưa rõ**. **[Đề xuất]** Coi giọng nói và nội dung họp là dữ liệu cá nhân; thông báo trước, ghi nhận đồng ý, đặt thời hạn xóa.
2. **Dữ liệu người lao động.** Điều 25 Luật 91/2025 (cùng nguồn): biện pháp công nghệ, kỹ thuật trong quản lý lao động phải để người lao động "biết rõ"; khi chấm dứt hợp đồng phải xóa, hủy dữ liệu cá nhân của người lao động, trừ khi có thỏa thuận hoặc luật quy định khác. Ảnh hưởng trực tiếp tới bàn giao (C5) và hồ sơ phỏng vấn (C2).
3. **Giọng nói để nhận diện người nói** có thể là dữ liệu sinh trắc học (dữ liệu về đặc điểm cơ thể như giọng nói, vân tay; thuộc nhóm nhạy cảm). **Chưa kiểm chứng.** **[Đề xuất]** Không dùng tính năng đăng ký giọng nói trên dịch vụ nước ngoài khi chưa hỏi luật sư.
4. **Gửi bản ghi ra nước ngoài** (dịch vụ AI đám mây) có thể là chuyển dữ liệu cá nhân xuyên biên giới: xem `../an-toan-du-lieu-va-phap-ly-vn.md` mục 6.
5. **Nhiễm độc kho tri thức:** một ghi chú sai hoặc có lệnh ẩn được nhập vào kho sẽ lan sang mọi trợ lý dùng kho đó. SAP tự nêu rủi ro này **[Nguồn]**. Hàng rào: người duyệt mọi lần nhập, mỗi mục có nguồn.
6. **Lộ bí mật qua bài học/bàn giao:** mật khẩu, số điện thoại khách trong ghi chú. Hàng rào: quét bằng code trước khi nhập (C5).

!!! warning "Cẩn thận"
    Các điểm 1 đến 3 là chỗ pháp luật **chưa rõ** hoặc **chưa kiểm chứng**. Khi chưa chắc, hãy làm theo hướng an toàn trong phần [Đề xuất] (thông báo trước, ghi nhận đồng ý, đặt thời hạn xóa) và hỏi luật sư trước khi dùng cho dữ liệu thật.

## 7. Danh sách kiểm chứng trước khi xuất bản

Đây là việc nhóm soạn **còn phải làm** trước khi coi tài liệu là hoàn chỉnh. Bạn đọc cứ coi mỗi dòng chưa đánh dấu là "chưa chắc chắn".

**Pháp lý**
- [ ] Đọc bản gốc Luật 91/2025/QH15 (Điều 25, 32 và điều về dữ liệu sinh trắc học) trên Công báo hoặc vbpl.moj.gov.vn; đối chiếu với bản đăng lại đã dùng.
- [ ] Xác định họp nội bộ, họp trực tuyến có thuộc phạm vi Điều 32 hay không; hỏi luật sư.
- [ ] Xác định giọng nói/voice enrollment có là dữ liệu sinh trắc học theo NĐ 356/2025.
- [ ] Thời hạn lưu hồ sơ người lao động theo luật lao động, BHXH, thuế (ảnh hưởng mục "xóa khi nghỉ việc").

**Công cụ (hay đổi)**
- [ ] Google Meet "Take notes for me", Teams Copilot, Zoom, Lark Minutes: có hỗ trợ tiếng Việt không, ở gói nào. Chưa xác minh được (C1 mục 9).
- [ ] Cách xuất lịch sử nhóm Zalo (máy tính/điện thoại): chưa xác minh.
- [ ] Gems chuyển sang skills từ 11/2026 (theo `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md`).

**Số liệu và đo**
- [ ] Đo WER/CER trên ghi âm họp tiếng Việt thật của 1-2 SME (chưa có nguồn nào đo họp tiếng Việt).
- [ ] Đo thử tỷ lệ việc bịa/bỏ sót trong biên bản AI trên 10-20 cuộc họp tiếng Việt có đáp án.
- [ ] Mâu thuẫn trong bài IBM: tóm tắt ghi "8 quy trình, 12% lên 58%", thân bài ghi "3 quy trình, 8/9 lần (89%)". Không trích số nào của bài này cho tới khi rõ.
- [ ] Kiểm lại số liệu Microsoft EaS và Otter OSynth với bản mới (bài 2026, có thể còn sửa).

**Kỹ thuật**
- [ ] Chạy code mẫu với API thật và với PhoWhisper cục bộ trên máy văn phòng phổ thông (chưa làm).

!!! tip "Nói đơn giản"
    Danh sách này là sự thành thật của nhóm soạn: chỗ nào chưa đối chiếu luật, chưa thử công cụ, chưa đo trên tiếng Việt thì ghi rõ. Hãy dùng các cấp như **cách làm để bạn tự thử và tự đo**, đừng coi các số liệu ở đây là kết quả chắc chắn cho công ty bạn.

## 8. Thứ tự đọc

Bạn đọc theo thứ tự này: `../nen-tang-bang-chung.md` → `../an-toan-du-lieu-va-phap-ly-vn.md` → file này → C0 đến C7. Người đã qua C0-C1 của nhóm RAG có thể bắt đầu ở C0 nhóm này ngay.

!!! tip "Nói đơn giản"
    Ba trang đầu là nền (bằng chứng và an toàn dữ liệu), đọc lướt cũng được. Sau đó làm lần lượt từ C0. Nếu chỉ có thời gian cho một bài, hãy làm C0.
