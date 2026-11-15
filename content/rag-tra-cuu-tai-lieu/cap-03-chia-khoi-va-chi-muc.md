# Cấp 3 - Chia khối (chunk) và lập chỉ mục

> Ngày soạn: 2026-11-11. Nguyên tắc bền; thao tác/công cụ hay đổi, có ghi ngày.
> Quy ước: **[Nguồn]** = kết quả có trong nguồn đã đọc (mã ở mục 8). **[Đề xuất]** = ý kiến của nhóm soạn, chưa được nguồn nào kiểm chứng.
> Code mẫu: ghi "đã chạy thử" (scratchpad, Python 3.13, `python -I`, chỉ dùng thư viện chuẩn) hoặc "chưa chạy thử".

!!! tip "Tóm tắt nhanh"
    Muốn AI tra cứu tài liệu công ty, bạn không đưa cả tập tài liệu dày cộp cho nó, mà **cắt ra từng đoạn nhỏ có nhãn** (gọi là **khối**, tiếng Anh là *chunk*). Bài này dạy cách cắt theo tiêu đề để bảng giá không bị đứt đôi, gắn cho mỗi khối một "số hiệu" không đổi, và ghi tất cả vào một danh mục (gọi là **chỉ mục**). Sau bài, bạn có danh mục các khối kèm cách cập nhật khi tài liệu đổi, và một bộ câu hỏi thử nhỏ để chọn cách cắt bằng số đo thay vì cảm tính. Phần lớn có đường **không cần code**; phần có code, bạn chỉ cần nhờ người biết lập trình hoặc nhờ AI chạy giúp.

---

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người phụ trách vận hành, IT hoặc kế toán ở doanh nghiệp vừa và nhỏ (SME) Việt Nam, đã có thư mục `text/` chứa các tệp Markdown (đây là kết quả của Cấp 2). Markdown là kiểu tệp chữ thuần, có đánh dấu tiêu đề bằng dấu `#`. Bạn có thể có hoặc không có lập trình viên đi cùng.

**Bạn cần chuẩn bị:**
- Thư mục `text/` gồm các tài liệu đã chuyển thành chữ sạch ở Cấp 2.
- Một vài loại tài liệu thật của công ty để làm thử, ví dụ chính sách bán hàng, bảng giá, hợp đồng mẫu, hóa đơn đã trích JSON (JSON là cách viết dữ liệu có khung rõ ràng để máy đọc được), quy trình nội bộ (SOP).
- Một bảng tính (Google Sheet hoặc Excel) để ghi danh mục khối, nếu đi theo đường không code.

**Sau bài này bạn sẽ có:**
1. Mỗi tài liệu được chia thành các **khối** (chunk) theo tiêu đề, bảng không bị cắt đôi, mỗi khối có **mã ổn định** và siêu dữ liệu (file, trang, đường dẫn tiêu đề, ngày, phiên bản). *Siêu dữ liệu* là những thông tin "về" khối, giống nhãn dán ngoài hộp hồ sơ: hồ sơ này từ file nào, ở trang nào, thuộc mục nào.
2. Một **chỉ mục** (file danh mục khối; sau đó có thể thêm chỉ mục tìm kiếm ở Cấp 4) và quy trình **cập nhật khi tài liệu đổi**. Chỉ mục giống mục lục tra cứu của thư viện: nó cho biết cái gì nằm ở đâu.
3. Tùy chọn: một **lớp điều hướng/tóm tắt** (kiểu Airbnb) hoặc **ngữ cảnh gắn thêm cho từng khối** (kiểu "contextual retrieval" của Anthropic), chỉ làm khi đã đo thấy cần.
4. Một **bộ câu hỏi thử** nhỏ để so sánh cách chia (không chọn theo cảm tính).

**Thứ bạn cầm đi được sau bài:** tệp quy tắc chia khối, bộ câu hỏi thử, tệp danh sách khối (`chunks.jsonl`), nhật ký thay đổi, và danh sách kiểm lỗi chia khối.

**Không thuộc cấp này:** thuật toán tìm kiếm (Cấp 4), trả lời có trích dẫn (Cấp 5), chấm điểm hệ thống (Cấp 6; ở đây chỉ dùng bộ câu hỏi nhỏ).

---

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

**Lỗi ở Cấp 2 dẫn tới Cấp 3:**
- Có text sạch nhưng cả tài liệu 80 trang quá dài: nhét hết vào một lần hỏi thì tốn và loãng; nhét một đoạn tình cờ thì mất ngữ cảnh.
- Cắt thô theo số ký tự làm đứt giữa câu, giữa bảng giá, giữa điều khoản; câu trả lời dựa trên nửa bảng.
- Không có "địa chỉ" ổn định cho từng đoạn nên không trích dẫn và không biết đoạn nào đã đổi khi tài liệu cập nhật.

!!! tip "Nói đơn giản"
    Hãy hình dung bạn có một cuốn sổ tay 80 trang và muốn nhờ người khác tra giúp. Đưa cả cuốn thì họ ngợp. Xé bừa từng mảnh thì có mảnh chỉ còn nửa bảng giá. Cách hợp lý là chia theo từng mục, đánh số từng mục, để ai hỏi gì thì chỉ lấy đúng mục đó ra.

**Câu hỏi cấp này trả lời:** "Đơn vị nhỏ nhất mà tôi lưu, tìm và trích dẫn là gì, nó có địa chỉ ổn định không, và khi tài liệu đổi thì tôi cập nhật đúng phần nào?"

**Quy tắc đầu vào [Đề xuất]:** chỉ lên Cấp 3 khi tổng tài liệu mục tiêu không còn nhét vừa một lần hỏi. Anthropic cho biết nếu cơ sở tri thức dưới 200.000 token (khoảng 500 trang) thì có thể đưa cả vào prompt thay vì làm RAG **[Nguồn: T-A1]**; nếu dưới ngưỡng đó và hỏi ít, ở lại Cấp 0-2 là hợp lý (cân nhắc thêm chi phí mỗi lần hỏi và nhờ prompt caching).

(Giải thích từ ngữ: *token* là đơn vị AI dùng để đếm độ dài chữ, tạm hiểu là một mẩu từ. *Prompt* là đoạn chữ bạn gửi cho AI. *RAG* là cách làm cho AI tra tài liệu của bạn trước khi trả lời. *Prompt caching* là tính năng lưu sẵn phần chữ gửi lặp lại để mỗi lần hỏi đỡ tốn.)

---

## 3. Kiến thức nền (ngắn, chính xác)

### 3.1. Chunk là gì và vì sao cần
Chunk là đoạn text được lập chỉ mục và tìm riêng. Mô hình embedding có cửa sổ đầu vào cố định nên tài liệu dài phải chia nhỏ; chunk quá nhỏ thiếu ngữ cảnh, chunk quá lớn pha loãng thông tin, và chunk cắt ngang phần nội dung gắn kết có thể làm hại tác vụ phía sau **[Nguồn: P1]**.

(*Mô hình embedding* là một loại AI biến mỗi đoạn chữ thành một dãy số đại diện cho ý nghĩa, để máy so xem hai đoạn có "gần nghĩa" nhau không. *Cửa sổ đầu vào* là lượng chữ tối đa nó đọc được một lần.)

!!! tip "Nói đơn giản"
    Chunk giống một tấm thẻ ghi chú trong hộp phiếu. Thẻ quá ngắn thì không đủ ý. Thẻ quá dài thì loãng, tìm khó. Thẻ bị cắt ngang giữa một ý thì đọc không hiểu.

### 3.2. Các chiến lược chia
| Chiến lược | Mô tả | Chi phí |
|---|---|---|
| Cắt cố định theo token/ký tự (có hoặc không chồng lấn) | Cửa sổ đều nhau | Rẻ nhất |
| Theo câu / theo đoạn | Cắt tại ranh giới câu hoặc dòng trống | Rẻ |
| Theo cấu trúc tài liệu (tiêu đề) | Cắt tại ranh giới mục do tác giả đặt; có thể gộp/tách theo ngưỡng kích thước | Rẻ (nếu Cấp 2 giữ được tiêu đề) |
| Ngữ nghĩa (semantic) | Cắt khi độ giống giữa các câu kề nhau thấp | Cần gọi mô hình embedding |
| Do LLM quyết định ranh giới (ví dụ LumberChunker, proposition) | LLM đọc rồi cắt hoặc tách thành mệnh đề | Đắt |
| Embed cả tài liệu rồi mới chia (late chunking / contextualized chunking) | Cần mô hình embedding ngữ cảnh dài | Cần mô hình chuyên biệt |

Giải thích nhanh các cách trong bảng: "chồng lấn" nghĩa là hai khối liền nhau có chung một đoạn ở rìa, để ý không bị đứt. "LLM" là mô hình ngôn ngữ lớn, tức loại AI như ChatGPT hay Claude. "Mệnh đề" (proposition) là một ý nhỏ, trọn nghĩa, tách ra từ câu dài. "Embed" là biến chữ thành dãy số như đã nói ở mục 3.1.

!!! tip "Nói đơn giản"
    Có sáu cách cắt, từ rẻ đến đắt. Cách rẻ nhất là cắt đều như cắt bánh mì. Cách ta sẽ ưu tiên là cắt theo tiêu đề có sẵn của tài liệu, vì tác giả đã chia mục giúp ta rồi.

### 3.3. Bằng chứng so sánh chiến lược chunking (tóm tắt và mức chắc chắn)

**Nhận xét chung:** các nghiên cứu cho kết quả không hoàn toàn thống nhất; hiệu ứng thường nhỏ; hầu hết dùng tiếng Anh. Không nguồn nào trong số đã đọc đo trên tiếng Việt hay tài liệu SME Việt Nam.

Bảng dưới đây dành cho ai muốn biết cơ sở. Bạn có thể đọc lướt và chỉ nhớ phần "Điều rút ra" ngay sau bảng. Vài từ chuyên môn trong bảng: *benchmark* là bộ đề dùng chung để chấm điểm các cách làm; *BEIR* và *GutenQA* là tên hai bộ đề như vậy; *nDCG@10* và *Recall@5* là các điểm số đo "đáp án đúng có nằm trong số kết quả đầu tiên không" (số càng cao càng tốt); *BM25* là cách tìm theo từ khóa; *dense* là cách tìm theo nghĩa bằng embedding; *breadcrumb* là đường dẫn tiêu đề kiểu "Chính sách > Đổi trả > Điều kiện"; *ablation* là thử bỏ từng phần để xem phần nào quan trọng; *parser* là công cụ đọc tệp gốc thành chữ.

| Mã | Nguồn và thiết kế | Kết quả chính (số liệu từ nguồn) | Mức chắc chắn |
|---|---|---|---|
| P1 | Zhou và cs., arXiv:2602.16974 (02/2026). Tái lập các nghiên cứu trước; sáu chiến lược; 4 mô hình embedding; 6 bộ BEIR (tìm tài liệu trong kho) và GutenQA (tìm đoạn trong một cuốn sách) | Tìm tài liệu trong kho: các cách theo cấu trúc (đoạn, cố định 256 token không chồng lấn, 5 câu) **thắng** các cách ngữ nghĩa và LLM; chênh nhau giữa các cách cấu trúc thường 1-3%; "proposition" thấp hơn đoạn 15-27%. Tìm đoạn trong một tài liệu dài: LumberChunker (dùng LLM) tốt nhất. Embed-cả-tài-liệu-trước **tăng** hiệu quả tìm trong kho nhưng **giảm** khi tìm trong một tài liệu (ví dụ -53,17% trung bình với Nomic, -3,83% với E5-large) | Trung bình-cao (có kiểm định thống kê, nhiều mô hình); nhưng tiếng Anh, bộ benchmark học thuật; bản nháp ẩn danh |
| P2 | Kuehlkamp và cs., arXiv:2610.10170 (10/2026). Thí nghiệm có nhóm đối chứng "giả" (đường dẫn tiêu đề xáo trộn), kích thước khối được khớp; 2 corpus tiếng Anh (200 bài Wikipedia, 1.585 bài khoa học QASPER) | Cắt đúng ranh giới mục quan trọng nhất: chuyển từ cắt cửa sổ cố định sang cắt theo cấu trúc +0,041 (Wikipedia) và +0,019 (QASPER) cov-nDCG@10; thêm đường dẫn tiêu đề thật chỉ thêm +0,011 và +0,009; đường dẫn **xáo trộn** không hơn không gắn gì (có khi tệ hơn). Chunk gắn ngữ cảnh do LLM viết (kiểu Anthropic) **thấp hơn** cắt theo cấu trúc trần; dưới ngân sách token thực tế, phần gắn thêm còn gây hại. Truy hồi hai tầng "chọn mục trước rồi chọn khối" tệ hơn tìm phẳng (-0,033 và -0,015) | Trung bình-cao về phương pháp (đối chứng, tiền đăng ký kiểm định); hiệu ứng **nhỏ** (+0,01-0,02), chỉ tiếng Anh, chỉ đo truy hồi, một mô hình tạo cấu trúc, tác giả nêu rõ |
| P3 | Bian và cs., arXiv:2610.31019 (10/2026). 120 cặp bản sửa liền kề của Wikipedia (Trung + Anh), 3 cách chia, đo phần phải embed lại | Cắt cố định không chồng lấn phải tính lại 57-68% khối so với 38-56% (đệ quy theo đoạn) và 43-54% (cắt theo nội dung); độ phủ bằng chứng trung bình chênh dưới 2 điểm phần trăm; ví dụ sửa 0,13% nội dung nhưng cắt cố định phải embed lại 49% còn cắt theo đoạn 8%; chèn 1% ở đầu bài làm cố định phải tính lại 100%; chồng lấn 32-64 token tốn thêm 10-26% đầu vào và giảm độ phủ tiếng Anh 3,0-3,9 điểm | Trung bình (mẫu nhỏ, một nguồn, một mô hình embedding; bản IEEE, tác giả nêu giới hạn) |
| P4 | Caspari và cs., arXiv:2608.16586 (CIKM 2026). 8 cách; 2 corpus lớn; 3 mô hình embedding; đo cả chi phí | Cách phức tạp (ngữ nghĩa, tóm tắt, contextual, late) **hiếm khi** thắng cách đơn giản một cách nhất quán; "title enrichment" (gắn tiêu đề tài liệu vào khối) là cải thiện rẻ tiền cạnh tranh ở nhiều cấu hình; cách tốt nhất đổi theo mô hình, bộ dữ liệu, kích thước kho, chỉ số. Ước tính dùng dịch vụ bên thứ ba sinh ngữ cảnh cho một kho 10.000 tài liệu tốn khoảng 9,6-14,73 USD (theo giá OpenRouter tại thời điểm viết) | Trung bình-cao; tiếng Anh; siêu tham số cố định, không tinh chỉnh riêng từng cách |
| P5 | Singh, arXiv:2609.31660 (09/2026). 4 văn bản quy phạm Ấn Độ (tiếng Anh), 800 câu hỏi do LLM sinh, 3 parser × 3 chunker × 5 embedding | Chunker "theo mục + gắn dấu vết tiêu đề (breadcrumb)" cho kết quả tốt nhất trong cấu hình thắng; chunk 256 token chồng lấn 32 tốt nhất (Recall@5 khoảng 0,90 so với khoảng 0,87 không chồng lấn); 384 và 512 token không hơn; BM25 thắng hoặc thua dense tuỳ văn bản; một mô hình embedding phổ thông kém hẳn trên câu hỏi về bảng; bằng chứng gần như luôn tồn tại trong khối (độ phủ trên 98%) nên sai khác nằm ở khâu xếp hạng | Trung bình-thấp (một tác giả, một lĩnh vực, câu hỏi do LLM sinh, chưa phản biện) |

**Điều rút ra [Đề xuất, dựa trên P1-P5]:**
1. Với tài liệu đã có cấu trúc tiêu đề tốt (chính sách, SOP, hợp đồng mẫu), **chia theo tiêu đề và gắn đường dẫn tiêu đề** là điểm khởi đầu rẻ và đã có bằng chứng ủng hộ (P2, P4, P5).
2. Các cách đắt (LLM chia, tóm tắt, ngữ nghĩa) **chưa đủ bằng chứng** để làm mặc định (P1, P4).
3. Tránh cắt cố định không có ranh giới cho kho **hay sửa** (P3).
4. Kích thước khoảng 256-512 token với chồng lấn nhỏ là vùng thường được dùng trong các nghiên cứu trên (P1: 256; P4: 512 chồng 25; P5: 256 chồng 32 tốt nhất); **không có kích thước "đúng chung"**: P5 chỉ ra 256 là gần tối ưu trên chính corpus đó; phải đo trên tài liệu của bạn. Lưu ý token tiếng Việt thường nhiều hơn tiếng Anh (giả thuyết, chưa đo).
5. Tránh bê nguyên kết luận từ bài báo sang SME: không có bài nào đo tài liệu tiếng Việt.

!!! tip "Nói đơn giản"
    Các nghiên cứu cho thấy cách cắt đơn giản, theo tiêu đề có sẵn, thường không thua các cách cầu kỳ mà lại rẻ. Nhưng chênh lệch nhìn chung nhỏ, và toàn bộ nghiên cứu làm trên tiếng Anh. Vì vậy hãy lấy "cắt theo tiêu đề" làm điểm xuất phát, rồi tự đo trên tài liệu của mình.

### 3.4. "Contextual Retrieval" của Anthropic
- **Ý tưởng [Nguồn: T-A1, blog 2024-09-19]:** dùng Claude sinh một đoạn ngữ cảnh ngắn (50-100 token) cho **từng chunk** dựa trên toàn tài liệu, gắn vào đầu chunk trước khi embed và trước khi lập chỉ mục BM25. Prompt dùng cả tài liệu trong thẻ `<document>` và chunk trong thẻ `<chunk>`, yêu cầu "đưa ngữ cảnh ngắn gọn để định vị chunk này trong tài liệu nhằm cải thiện tìm kiếm", chỉ trả lời bằng ngữ cảnh.
- **Kết quả do Anthropic báo [Nguồn: T-A1; tự đo nội bộ]:** giảm tỷ lệ truy hồi hỏng top-20 (1 trừ recall@20) trung bình: Contextual Embeddings 35% (5,7% xuống 3,7%); cộng Contextual BM25 49% (5,7% xuống 2,9%); thêm reranking 67% (5,7% xuống 1,9%). Chi phí một lần cho bước sinh ngữ cảnh khoảng 1,02 USD mỗi triệu token tài liệu, với giả định chunk 800 token, tài liệu 8k token và dùng prompt caching (tính tại thời điểm viết blog, có thể đã đổi).
- **Lưu ý về độ chắc chắn:** P2 nhận xét các con số 35-49% đến từ benchmark nội bộ của hãng chưa phản biện, và trong thí nghiệm của P2 (mô hình sinh ngữ cảnh cục bộ 26B, tiếng Anh) cách này **thua** cắt theo cấu trúc; P4 thấy contextual hiếm khi thắng cách đơn giản và đắt khi chạy cả kho. Kết luận [Đề xuất]: **thử sau khi đã chia theo tiêu đề và có bộ câu hỏi đo**, không phải bước đầu.

(*Truy hồi* là bước máy đi tìm các đoạn liên quan. "Truy hồi hỏng" là khi đoạn chứa đáp án không nằm trong số được tìm ra. *Reranking* là bước xếp hạng lại danh sách kết quả cho đoạn đúng nhất lên đầu. *Thẻ* `<document>` và `<chunk>` là cách đánh dấu đầu và cuối của từng phần chữ trong lời nhắn, để AI biết đâu là tài liệu, đâu là đoạn cần mô tả.)

!!! tip "Nói đơn giản"
    Ý tưởng là dán thêm vào đầu mỗi tấm thẻ một dòng ghi chú "tấm thẻ này nói về cái gì trong cả tài liệu". Anthropic báo kết quả tốt, nhưng đó là số tự đo; hai nghiên cứu khác không thấy lợi rõ so với cách đơn giản. Cho nên chỉ thử sau khi đã cắt theo tiêu đề và đã có bộ câu hỏi để đo.

### 3.5. Lớp điều hướng/tóm tắt kiểu Airbnb (arXiv:2610.14428)
Đã đọc bài (10/2026). **Kết quả trong nguồn:**
- Lớp điều hướng dạng wiki khoảng 2.700 trang Markdown do GPT-4.1 sinh từ 2.881 bài SOP; mỗi trang nêu **việc quy trình giải quyết** (intent), có **liên kết có kiểu** về bài gốc bằng mã định danh ổn định, và **gộp** quy trình bị chia nhỏ ở nhiều bài thành một trang.
- Chỉ một công cụ tìm kiếm lai BM25 + dense, không reranker, không viết lại truy vấn.
- Bằng chứng trích nguyên văn được **kiểm bằng code** (mỗi đoạn trích phải là chuỗi con nguyên văn của bài gốc); bản tóm tắt không bao giờ được trích làm bằng chứng.
- Trên 132 ca thật: đủ bằng chứng 83,3% so với 59,8% của hệ RAG sản xuất (khoảng tin cậy Wilson 95% không giao nhau: 76,1-88,7 so với 51,3-67,8). Nhưng hai điều kiện **không giống nhau hoàn toàn** (vòng lặp tác tử khác, ngân sách truy vấn/lấy bài khác); tác giả nói rõ không khẳng định riêng cách biểu diễn gây ra khoảng cách.
- Ablation (cùng 132 ca, chỉ số đủ bằng chứng): hybrid 83,3%; chỉ BM25 78,0%; chỉ dense 78,8%; bỏ gộp thực thể 76,5%; bỏ tóm tắt ý định 78,8%; làm yếu liên kết có kiểu 81,1%; không có lớp nào (bài gốc thô) 78,0%. Các khoảng tin cậy đều giao nhau; kiểm định McNemar không tách được nhóm nào khỏi hệ đầy đủ (p nhỏ nhất 0,078); tác giả coi đây là xu hướng, không phải kết luận. Tác giả diễn giải: cách tổ chức nội dung quan trọng hơn thuật toán tìm.
- Kiểm tra lớp điều hướng: trích 3.168 liên kết, một mô hình mạnh hơn mô hình xây chấm từng liên kết; khoảng 96% đạt, khoảng 4% hỏng/không liên quan/thiếu cơ sở và bị xóa hoặc sinh lại khi bảo trì. Cả 2.881 bài đều được ít nhất một trang tham chiếu.
- Các ca không đủ bằng chứng chủ yếu do **nội dung thiếu trong bài gốc** (bước mà chuyên viên giỏi biết nhưng không ai viết ra), không do tìm sai (đánh giá định tính của tác giả).
- Phạm vi: kho SOP trưởng thành, công việc chịu được độ trễ (khoảng 90 giây mỗi ca so với khoảng 8-9 giây của hệ sản xuất), có người duyệt từng ca; không khẳng định lợi thế về độ trễ hay chi phí.
- **Điều nhóm soạn áp dụng [Đề xuất]:** với SME, lớp điều hướng là một **tệp Markdown nhỏ** (mỗi trang: "giải quyết việc gì", danh sách nguồn có mã khối, điều kiện, ngoại lệ) do AI nháp và **người duyệt**, rồi kiểm bằng code rằng mọi liên kết trỏ tới mã khối thật (mục 4, Bài 3.7).

(Chú thích từ ngữ: *SOP* là quy trình làm việc chuẩn. *Intent* là "ý định", tức việc mà trang đó giúp giải quyết. *Liên kết có kiểu* là liên kết có ghi rõ loại, ví dụ "quy định" hay "ngoại lệ". *Khoảng tin cậy Wilson 95%* là dải số mà kết quả thật nhiều khả năng nằm trong; hai dải không giao nhau nghĩa là chênh lệch khó là do ngẫu nhiên. *McNemar* và *p* là cách kiểm tra thống kê xem chênh lệch có đủ chắc không; p càng nhỏ càng chắc, và 0,078 là chưa đủ chắc. *Tác tử* là một chương trình AI tự thực hiện nhiều bước. *Độ trễ* là thời gian chờ có câu trả lời.)

!!! tip "Nói đơn giản"
    Airbnb làm thêm một "mục lục thông minh": mỗi trang cho biết nó giúp giải quyết việc gì và chỉ về đoạn gốc. Kết quả của họ có vẻ tốt, nhưng điều kiện so sánh không hoàn toàn giống nhau và chênh lệch giữa các phần chưa đủ chắc về mặt thống kê. Với công ty nhỏ, bạn có thể làm bản thu nhỏ: một tệp Markdown do AI nháp, người xem lại, và máy kiểm rằng các mã khối nhắc tới đều có thật.

---
## 4. Chuỗi bài nhỏ

Có chín bài thực hành, làm theo thứ tự từ 3.1 đến 3.9. Mỗi bài có mục tiêu, việc cần làm, thứ bạn có sau bài và (khi bản gốc nêu) lỗi thường gặp. Bài nào có đoạn mã thì đều có đường không code đi kèm hoặc có người biết code làm giúp.

### Bài 3.1 - Xác định "đơn vị ý nghĩa" của từng loại tài liệu
- **Mục tiêu:** quyết định một khối nên là gì với từng loại tài liệu **trước khi** viết code.
- **Việc cần làm [Đề xuất]:**
  1. Với mỗi loại, hỏi: "Người ta thường tra cứu cái gì?" Chính sách bán hàng: một điều khoản; bảng giá: một dòng sản phẩm kèm tiêu đề cột; hợp đồng: một điều; hóa đơn đã trích JSON: một hóa đơn (không chia nhỏ).
  2. Ghi một dòng cho mỗi loại: "khối = ...; tối đa N token; không bao giờ cắt: bảng, danh sách đánh số điều kiện".
  3. Chọn 15-30 **câu hỏi thử** có đáp án nằm ở đâu trong tài liệu (ghi file + mục). Đây là thước đo cho mọi bài sau.
- **Bạn có sau bài:** `quy_tac_chia_khoi.md` và `cau_hoi_thu.csv` (câu hỏi, file đúng, mục đúng). (CSV là tệp bảng đơn giản, mở được bằng Excel hoặc Google Sheet.)
- **Lỗi thường gặp:** chọn kích thước theo thói quen (ví dụ 1000 ký tự); bộ câu hỏi thử do chính AI sinh ra từ khối (dễ thiên lệch về cách chia; P5 cũng thừa nhận hạn chế này với câu hỏi do LLM sinh).

!!! tip "Nói đơn giản"
    Trước khi cắt, hãy tự hỏi: nhân viên thường tra cái gì? Nếu họ tra "điều kiện đổi trả" thì mỗi điều khoản là một khối; nếu họ tra giá một sản phẩm thì mỗi dòng giá kèm tiêu đề cột là một khối. Rồi soạn sẵn 15-30 câu hỏi kèm đáp án đúng nằm ở đâu, giống bộ đề kiểm tra để chấm điểm cách cắt của bạn.

### Bài 3.2 - Chia theo tiêu đề (không code hoặc code nhẹ)
- **Mục tiêu:** mỗi khối là một mục (hoặc một phần của mục nếu quá dài), kèm đường dẫn tiêu đề.
- **Đường không code [Đề xuất]:** dùng soạn thảo (Word/Docs/Notion) chia theo Heading; xuất mỗi Heading cấp 2 thành một file hoặc một dòng trong bảng tính (cột: file, đường dẫn tiêu đề, nội dung). Phù hợp dưới vài chục tài liệu. (Heading là kiểu định dạng "Tiêu đề 1, Tiêu đề 2..." có sẵn trong Word hay Google Docs, khác với việc chỉ tô chữ to lên.)
- **Đường code nhẹ:** đoạn mã dưới (đã chạy thử).
- **Đoạn mã dưới đây làm gì?** Nó đọc một tài liệu Markdown, cắt thành các khối theo tiêu đề (mỗi khối nhớ luôn đường dẫn tiêu đề của nó), không cắt ngang bảng, và chỉ cắt thêm tại dòng trống nếu một mục dài quá giới hạn. Mỗi khối được cấp hai mã: `id` là số hiệu cố định của khối, `h` là "dấu vân tay" của nội dung để biết khi nào nội dung đổi. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết nó làm gì, và nhờ người biết lập trình hoặc nhờ AI chạy giúp.
- **Mã mẫu - đã chạy thử** (scratchpad, `python -I`, thư viện chuẩn; chia theo tiêu đề `#`, không cắt ngang bảng, chỉ chia thêm tại dòng trống nếu một mục vượt `max_chars`):
  ```python
  import re, hashlib

  def norm(s): return re.sub(r"\s+", " ", s).strip()

  def chunk_markdown(text, source, max_chars=1200):
      path, buf, chunks, seen = [], [], [], {}
      def emit(body):
          hp = " > ".join(path)
          k = seen.get(hp, 0); seen[hp] = k + 1
          cid = hashlib.sha1(f"{source}|{hp}|{k}".encode("utf-8")).hexdigest()[:10]  # dinh danh
          h = hashlib.sha1(norm(body).encode("utf-8")).hexdigest()[:10]              # phat hien doi
          chunks.append({"id": cid, "h": h, "source": source, "heading_path": hp, "text": body})
      def flush():
          body = "\n".join(buf).strip()
          if not body: return
          cur = ""
          for b in re.split(r"\n\s*\n", body):          # bang la mot khoi lien, khong bi cat
              if cur and len(cur) + len(b) > max_chars: emit(cur); cur = ""
              cur = (cur + "\n\n" + b) if cur else b
          if cur: emit(cur)
      for line in text.splitlines():
          m = re.match(r"^(#{1,6})\s+(.*)", line)
          if m:
              flush(); buf.clear()
              path[:] = path[:len(m.group(1)) - 1] + [m.group(2).strip()]
          else:
              buf.append(line)
      flush()
      return chunks
  ```
  Thử trên một chính sách bán hàng mẫu (mục tiêu đề + bảng chiết khấu + mục "2.1 Điều kiện", "2.2 Quy trình") ra 3 khối: bảng chiết khấu nằm nguyên trong khối "1. Chiết khấu"; mỗi khối có `heading_path` như "Chính sách bán hàng 2026 > 2. Đổi trả > 2.1 Điều kiện". Chạy hai lần cho cùng mã khối (ổn định).
- **Giới hạn của mã (nói rõ):** (a) một đoạn đơn hoặc một bảng dài hơn `max_chars` vẫn thành khối lớn; bảng rất dài cần quy tắc "lặp tiêu đề cột khi tách" (Docling có tùy chọn `repeat_table_header` theo tài liệu của họ, xem Bài 3.3); (b) không xử lý khối mã (code fence) có dòng bắt đầu bằng `#`; (c) không đếm token, dùng ký tự thay thế gần đúng; (d) tiêu đề trùng nhau trong một file được đánh thứ tự `k`, nên thêm tiêu đề vào giữa có thể đổi mã các khối trùng tên sau nó.
- **Bạn có sau bài:** `chunks.jsonl`: mỗi dòng một khối. (JSONL là tệp chữ mà mỗi dòng là một bản ghi JSON, tức một khối.)
- **Lỗi thường gặp:** tài liệu không có cấu trúc tiêu đề (bản scan chuyển thẳng) nên mọi thứ thành một khối: phải quay lại Cấp 2 để giữ tiêu đề, hoặc dùng quy tắc theo đánh số "Điều 1.", "Mục 2." [Đề xuất]; tiêu đề "đẹp" nhưng sai cấp trong Word (dùng cỡ chữ to thay vì Heading) khiến công cụ chuyển không nhận ra cấp tiêu đề.

!!! tip "Nói đơn giản"
    Đoạn mã giống một người đọc tài liệu từ đầu đến cuối, gặp tiêu đề mới thì đóng khối cũ, mở khối mới, và ghi nhớ mình đang ở mục nào. Bảng được giữ nguyên một cục, không bị cắt. Nếu bạn không có người biết code, cứ dùng đường không code: dùng Heading rồi chép từng mục vào một dòng của bảng tính.

### Bài 3.3 - Chia theo tiêu đề bằng thư viện (Docling chunking)
- **Mục tiêu:** dùng bộ chia có sẵn khi đã dùng Docling ở Cấp 2. (Docling là công cụ chuyển tài liệu sang chữ; thư viện là bộ công cụ lập trình viên có sẵn để dùng lại.)
- **Thông tin từ tài liệu Docling (qua kết quả tìm kiếm trên trang tài liệu chính thức, chưa chạy thử; tin cậy trung bình, kiểm lại trang gốc trước khi dùng):** `HybridChunker` là chia theo cấu trúc tài liệu rồi tinh chỉnh theo token; pha thứ hai gộp các khối nhỏ liền kề cùng tiêu đề (`merge_peers` mặc định bật); phương thức `contextualize()` trả về text kèm ngữ cảnh (tiêu đề) là dạng nên dùng để embed, text thô tách riêng; cần dùng cùng tokenizer với mô hình embedding; có tùy chọn `repeat_table_header` để lặp tiêu đề bảng khi bảng bị tách; có `LineBasedTokenChunker` giữ nguyên dòng cho bảng/danh sách/log.
- **Việc cần làm [Đề xuất]:** chạy trên 5 tài liệu mẫu, so với kết quả của Bài 3.2 bằng bộ câu hỏi thử ở Bài 3.1; chỉ chuyển sang thư viện nếu đạt tốt hơn hoặc tiết kiệm công.
- **Bạn có sau bài:** so sánh hai cách chia trên cùng bộ câu hỏi (bảng).
- **Lỗi thường gặp:** tokenizer chia khác tokenizer embedding làm khối vượt giới hạn; coi `contextualize()` và text thô là một.

(*Tokenizer* là bộ đếm và chia chữ thành token. Mỗi mô hình có một bộ riêng, nên nếu bộ chia khối đếm theo kiểu này mà mô hình embedding đếm theo kiểu khác thì khối có thể bị dài quá mức cho phép. Các tên như `HybridChunker` hay `merge_peers` là tên chức năng của Docling; bạn chỉ cần biết chúng làm việc gộp khối nhỏ, giữ tiêu đề bảng, v.v.)

!!! tip "Nói đơn giản"
    Nếu đã có sẵn công cụ cắt khối trong bộ công cụ đang dùng thì thử nó. Nhưng đừng tin ngay: hãy so với cách tự cắt bằng cùng bộ câu hỏi thử. Cách nào trả lời đúng nhiều hơn hoặc đỡ công hơn thì chọn.

### Bài 3.4 - Kích thước và chồng lấn (đo, không đoán)
- **Mục tiêu:** chọn kích thước/chồng lấn bằng số đo trên chính tài liệu của bạn.
- **Việc cần làm [Đề xuất]:** thử 3 mức (ví dụ 256, 384, 512 token) và chồng lấn 0 và khoảng 10% với bộ câu hỏi thử; đo: tỷ lệ câu hỏi mà khối đúng nằm trong top-K (K=5 hoặc 10, "recall@K"). Cần Cấp 4 để chạy tìm kiếm; nếu chưa có, dùng tìm bằng từ khóa BM25 đơn giản làm bước tạm.
- **Bằng chứng tham khảo (không thay thế việc đo):** P5: 256 token chồng 32 tốt nhất trên corpus đó, 384/512 không hơn; P3: chồng lấn 32-64 token làm tốn thêm 10-26% đầu vào và, trong tiếng Anh, giảm độ phủ 3,0-3,9 điểm dưới ngân sách ngữ cảnh cố định (do văn bản trùng chiếm chỗ); P4 dùng 512 token chồng 25. Ba nguồn không đồng ý về một giá trị; kết luận: **đo**.
- **Bạn có sau bài:** bảng `kich_thuoc.csv` (cấu hình, recall@5, số khối, tổng token đã embed).
- **Lỗi thường gặp:** chồng lấn lớn "cho chắc" làm tăng chi phí và nhân đôi nội dung trích dẫn; chỉ đo trên vài câu hỏi dễ.

!!! tip "Nói đơn giản"
    "Top-K" nghĩa là K kết quả đứng đầu. "Recall@5" là: trong 100 câu hỏi thử, bao nhiêu câu có đoạn đúng nằm trong 5 kết quả đầu. Các bài báo đưa ra những con số khác nhau cho kích thước đẹp nhất, nên đáp án thật sự là tự thử vài mức trên tài liệu của mình và chọn mức có điểm cao, chi phí vừa phải.

### Bài 3.5 - Gắn mã ổn định và siêu dữ liệu cho mỗi khối
- **Mục tiêu:** mỗi khối có địa chỉ không đổi khi nội dung không đổi, đủ thông tin để trích dẫn và cập nhật.
- **Việc cần làm [Đề xuất]:**
  1. **Mã khối** (`id`) không phụ thuộc nội dung chi tiết: băm (`file`, `đường dẫn tiêu đề`, thứ tự trong mục). Nhờ vậy sửa một câu trong điều khoản không đổi mã khối đó.
  2. **Mã nội dung** (`h`): băm nội dung đã chuẩn hoá; đổi khi nội dung đổi, dùng phát hiện thay đổi (Bài 3.8).
  3. Siêu dữ liệu tối thiểu: `source_file`, `sha256_cua_file`, `trang_bat_dau`, `trang_ket_thuc`, `heading_path`, `loai_tai_lieu`, `phien_ban` hoặc `ngay_hieu_luc`, `trang_thai` (hiệu lực/hết hiệu lực), `muc_nhay_cam` (từ Cấp 2), `so_ky_tu`.
  4. Quy tắc đặt tên: Airbnb dùng liên kết đến bài gốc bằng **mã định danh ổn định** **[Nguồn: P6]**; mã của bạn nên có tính chất tương tự (không phụ thuộc vị trí trong kho).
- **Mã minh hoạ - đã chạy thử** (xem mục 4 Bài 3.2 và 3.8): với bản `v1` và bản `v2` (đổi 8% thành 10%), mã `id` của ba khối giữ nguyên, mã `h` của đúng khối "1. Chiết khấu" đổi.
- **Bạn có sau bài:** `chunks.jsonl` có `id`, `h`, siêu dữ liệu đầy đủ.
- **Lỗi thường gặp:** dùng số thứ tự (1, 2, 3...) làm mã: chèn một đoạn là đổi hết; dùng băm nội dung làm mã duy nhất: sửa một chữ là mất địa chỉ cũ và các liên kết/trích dẫn cũ gãy.

(*Băm* là cách biến một đoạn chữ thành một chuỗi ký tự ngắn, cố định, sao cho cùng chữ thì cùng chuỗi, và chỉ cần đổi một chữ là chuỗi đổi hẳn. Nó giống "dấu vân tay" của đoạn chữ. `sha256` là một kiểu băm phổ biến.)

!!! tip "Nói đơn giản"
    Mỗi khối cần hai thứ khác nhau. Thứ nhất là **số hiệu** (`id`), như số căn cước: sửa nội dung thì số hiệu vẫn giữ để trích dẫn cũ còn đúng. Thứ hai là **dấu vân tay** (`h`) của nội dung: nội dung đổi thì dấu vân tay đổi, nhờ đó bạn biết khối nào cần xử lý lại. Đừng gộp hai thứ làm một.

### Bài 3.6 - Tiền tố ngữ cảnh: đường dẫn tiêu đề và "contextual retrieval"
- **Mục tiêu:** mỗi khối khi tìm kiếm tự mô tả được nó thuộc đâu.
- **Mức 1 - đường dẫn tiêu đề (rẻ nhất) [Nguồn: P2, P4, P5; Đề xuất cách dùng]:** trước khối khi embed/tìm, thêm dòng như `[Tên tài liệu > Mục > Mục con]`. P2 đo: đường dẫn **thật** có ích nhỏ (+0,011/+0,009) và đường dẫn **sai** (xáo trộn) không có ích; vì vậy đường dẫn phải đúng. P2 thấy phần lớn lợi ích đến từ cấp đầu tiên của đường dẫn rồi chững lại (khám phá phụ, không phải kết luận). P4: gắn tiêu đề tài liệu là cải thiện rẻ tiền và cạnh tranh.
- **Mức 2 - ngữ cảnh do LLM sinh cho từng khối [Nguồn: T-A1]:** dùng prompt của Anthropic (dạng mô tả ở 3.4). **Chỉ làm khi** bộ câu hỏi thử cho thấy khối bị mất ngữ cảnh (ví dụ khối "Điều kiện: 7 ngày" mà không nói đang nói về hàng nào). Đo trước-sau trên cùng bộ câu hỏi. Lưu ý P2 và P4 (mục 3.3) cho kết quả không thuận lợi hơn cách đơn giản; chi phí ở P4 và T-A1 (mục 3.4).
- **Không code [Đề xuất]:** thêm thủ công một câu mô tả đầu mỗi mục trong tài liệu nguồn ("Mục này nói về đổi trả cho hàng loại A").
- **Bạn có sau bài:** `chunks.jsonl` có thêm trường `text_for_index` (tiền tố + nội dung) tách khỏi `text` (nguyên văn, dùng để trích dẫn).
- **Lỗi thường gặp:** trích dẫn phần tiền tố do AI sinh ra như thể là nguyên văn (Airbnb nhấn mạnh tóm tắt không bao giờ được trích làm bằng chứng, chỉ nguyên văn bài gốc **[P6]**); tiền tố sai gây hại (P2).

!!! tip "Nói đơn giản"
    Có hai mức. Mức rẻ: dán tên tài liệu và tên mục vào đầu mỗi khối, ví dụ "Chính sách bán hàng > Đổi trả > Điều kiện", để khối đứng riêng vẫn biết mình thuộc đâu. Mức đắt: nhờ AI viết thêm một câu mô tả cho từng khối. Chỉ làm mức đắt khi bộ câu hỏi thử cho thấy khối bị "mất ngữ cảnh". Luôn giữ **hai bản**: bản có tiền tố để tìm, bản nguyên văn để trích dẫn.

### Bài 3.7 - Lớp điều hướng/tóm tắt kiểu Airbnb (tùy chọn)
- **Mục tiêu:** cho kho tài liệu quy trình/chính sách nhiều, một "mục lục thông minh" nói mỗi trang giải quyết việc gì và trỏ về khối nguồn.
- **Việc cần làm [Đề xuất, mô phỏng thiết kế P6 ở quy mô nhỏ]:**
  1. Xác định 10-30 "việc" mà nhân viên thường cần làm ("khách yêu cầu đổi hàng", "đại lý xin tăng chiết khấu").
  2. Cho mỗi việc, nhờ AI nháp một trang: tiêu đề, **việc này giải quyết gì / không giải quyết gì**, các bước tóm tắt, và danh sách mã khối nguồn (`id`) mà trang dựa vào, kèm kiểu liên kết (ví dụ `quy_dinh`, `ngoai_le`, `bieu_mau`). Nếu quy trình bị chia ở nhiều tài liệu, gộp vào một trang (P6: bỏ gộp là mất nhiều nhất trong ablation, xu hướng không có ý nghĩa thống kê).
  3. **Người duyệt từng trang.** P6 tự xây tự động không người; ở quy mô SME nên có người vì tài liệu ít và rủi ro cao hơn khi sai chính sách.
  4. **Kiểm bằng code:** mọi `id` trong trang phải tồn tại trong `chunks.jsonl`; mọi đoạn trích dẫn dùng ở Cấp 5 phải là chuỗi con nguyên văn của khối nguồn (tương tự validator của P6). Mã kiểm chuỗi con **chưa chạy thử** dưới dạng riêng (logic `trich in van_ban_goc`, tương tự phần `norm` đã chạy trong `chunk_markdown`).
  5. Khi tài liệu đổi: kiểm liên kết gãy, sinh lại trang bị ảnh hưởng (P6 mô tả ba bước bảo trì: kiểm cấu trúc, kiểm ngữ nghĩa bằng mô hình độc lập, xóa/sinh lại trang bị đánh dấu).
- **Bạn có sau bài:** thư mục `dieu_huong/*.md`, `kiem_lien_ket.py`.
- **Lỗi thường gặp:** trang điều hướng làm "bản thay thế" và được trích dẫn như nguồn; để AI tự gộp mà không ai xem; không kiểm định kỳ nên trang trôi lệch sau khi tài liệu nguồn đổi (P6 nêu rõ lớp tạo ra sẽ "trôi" khi kho đổi và đó là gánh nặng thật).

(*Validator* là đoạn chương trình kiểm tra tự động. "Chuỗi con nguyên văn" nghĩa là đoạn trích phải có mặt y hệt, từng chữ, trong bài gốc. Phần kiểm này chỉ là phép tìm xem đoạn trích có nằm trong bài gốc không.)

!!! tip "Nói đơn giản"
    Đây là tùy chọn. Bạn soạn một "mục lục theo việc": ví dụ trang "Khách muốn đổi hàng" nói rõ trang này giải quyết gì, rồi chỉ về đúng các khối gốc (quy định, ngoại lệ, biểu mẫu). AI được phép nháp, nhưng **người phải xem từng trang**, và máy kiểm rằng mọi mã khối trỏ tới đều có thật. Trang tóm tắt chỉ để tìm đường, không bao giờ được dùng làm bằng chứng; bằng chứng luôn là nguyên văn bài gốc.

### Bài 3.8 - Lập chỉ mục và cập nhật khi tài liệu đổi (drift)
- **Mục tiêu:** khi file nguồn đổi, chỉ xử lý lại phần đổi; phát hiện khối bị bỏ mồ côi. (*Drift* là hiện tượng "trôi": nguồn đã đổi mà bản đã xử lý vẫn là bản cũ. Khối "mồ côi" là khối còn trong danh mục nhưng nội dung gốc của nó đã bị xóa.)
- **Việc cần làm [Đề xuất]:**
  1. Lập chỉ mục = bảng/tệp danh mục các khối với `id`, `h`, siêu dữ liệu; ở Cấp 4 thêm chỉ mục tìm kiếm.
  2. Mỗi lần chạy: tính `sha256` từng file nguồn; file không đổi thì bỏ qua. File đổi thì chia lại và so với danh mục cũ theo `id`: `giữ` (cùng `id`, cùng `h`), `ĐỔI` (cùng `id`, khác `h`: embed/tóm tắt lại), `mới`, `XÓA` (đánh dấu hết hiệu lực, **không xóa ngay** nếu có trích dẫn cũ).
  3. Lưu `phien_ban`/`ngay_hieu_luc`; tài liệu bị thay thế đánh dấu `het_hieu_luc` thay vì xóa, tránh trả lời theo chính sách cũ.
  4. Nếu có lớp điều hướng hoặc ngữ cảnh do LLM sinh: sinh lại phần liên quan khối `ĐỔI`.
- **Mã so sánh - đã chạy thử** (scratchpad): so hai bản chính sách (đổi chiết khấu 8% thành 10%) in ra: `DOI` cho khối "1. Chiết khấu", `giu` cho hai khối còn lại.
- **Bằng chứng về ảnh hưởng của cách chia đến chi phí cập nhật [Nguồn: P3]:** trên bản sửa thật của Wikipedia (Trung + Anh), cắt cố định không chồng lấn phải tính lại nhiều hơn cắt theo đoạn tới 13-20 điểm phần trăm ở cấu hình đã đóng băng; chèn 1% ở đầu bài làm cắt cố định phải tính lại 100%, trong khi cắt theo đoạn/nội dung dưới 30% ở ba vị trí đã thử; độ phủ truy hồi chênh dưới 2 điểm. Điều này ủng hộ [Đề xuất] chia theo tiêu đề/đoạn cho kho hay sửa; nhưng P3 không đo trên tiếng Việt hay tài liệu SME, và tác giả nói chưa chứng minh tương đương về độ phủ.
- **Bạn có sau bài:** `cap_nhat.py` (so sánh), nhật ký `thay_doi.csv`.
- **Lỗi thường gặp:** lập chỉ mục lại toàn bộ mỗi lần (tốn); xóa khối cũ làm gãy trích dẫn lịch sử; PDF chuyển lại cho ra khác nhau chút ít (khoảng trắng, dấu nối dòng) làm mọi `h` đổi: chuẩn hoá khoảng trắng và Unicode trước khi băm (P3 cũng ghi trong thí nghiệm của họ rằng nhiễu trích xuất không phân biệt được với chỉnh sửa khi so byte-giống-hệt).

!!! tip "Nói đơn giản"
    Mỗi lần có tài liệu mới, máy so "dấu vân tay" cũ và mới. Khối nào cùng số hiệu, cùng dấu vân tay thì giữ nguyên, khối nào đổi dấu vân tay thì xử lý lại, khối nào mới thì thêm, khối nào mất thì đánh dấu hết hiệu lực (đừng xóa ngay, vì còn trích dẫn cũ). Nếu cách cắt ổn thì sửa một câu chỉ làm đổi đúng một khối, tiết kiệm nhiều công và tiền xử lý lại.

### Bài 3.9 - Các bẫy cần kiểm: bảng bị cắt đôi, mất ngữ cảnh, đại từ
- **Mục tiêu:** có danh sách kiểm lỗi chia khối trước khi tin vào chỉ mục.
- **Việc cần làm [Đề xuất]:** bốc ngẫu nhiên 20 khối và kiểm:
  1. Bảng không bị cắt giữa chừng; bảng dài tách ra thì mỗi phần lặp tiêu đề cột.
  2. Khối đứng riêng vẫn hiểu được: không bắt đầu bằng "Điều này", "Như trên", "Mức chiết khấu nêu ở bảng trên".
  3. Điều kiện/ngoại lệ không bị tách khỏi quy định chính (ví dụ "trừ hàng khuyến mại" nằm ở khối khác).
  4. Số liệu gắn đơn vị (VND, %, ngày) nằm cùng khối.
  5. Khối quá nhỏ (một dòng) gộp với khối kề cùng mục (Docling gộp khối nhỏ cùng tiêu đề theo `merge_peers`, theo tài liệu của họ).
  6. Mã khối ổn định qua hai lần chạy.
- P5 ghi nhận một mô hình embedding phổ thông kém hẳn trên câu hỏi về bảng và các cách truy hồi đều khó với câu hỏi tra bảng và câu hỏi phủ định; cho thấy bảng là điểm yếu chung, đáng kiểm riêng.
- **Bạn có sau bài:** `kiem_loi_khoi.csv` (khối, loại lỗi, cách sửa).
- **Lỗi thường gặp:** chỉ kiểm khối "đẹp"; sửa tay vào `chunks.jsonl` mà không sửa nguồn (lần chạy sau mất sửa).

!!! tip "Nói đơn giản"
    Hãy bốc thăm ngẫu nhiên 20 khối và đọc như người lạ: khối này có tự hiểu được không, có bảng nào bị đứt, có chỗ nào "trừ trường hợp..." bị tách khỏi quy định chính không. Bốc ngẫu nhiên, đừng chỉ chọn khối đẹp, vì lỗi thường nằm ở chỗ bạn ít nhìn tới.

---

## 5. Đường không code vs đường có code; khi nào buộc phải chuyển

Bảng dưới đây cho thấy, với mỗi việc, bạn có thể làm bằng tay hoặc nhờ code. Đường không code đủ dùng khi mới bắt đầu và số tài liệu ít.

| Việc | Không code | Có code |
|---|---|---|
| Chia khối | Soạn theo Heading; mỗi mục một file/dòng bảng tính | Bài 3.2/3.3 |
| Mã ổn định | Quy ước tay: `TÀI-LIỆU-ĐIỀU-MỤC` (ví dụ `CSBH-2026-2.1`) | Băm tự động (Bài 3.5) |
| Siêu dữ liệu | Cột trong bảng tính | `chunks.jsonl` |
| Lớp điều hướng | Trang Markdown/Notion do AI nháp, người duyệt | Thêm kiểm liên kết và kiểm trích nguyên văn bằng code |
| Cập nhật khi đổi | Nhật ký thay đổi thủ công theo phiên bản tài liệu | So sánh `id`/`h` tự động (Bài 3.8) |
| Dùng với công cụ có sẵn (Project/Gem/GPT tùy chỉnh) | Tải các khối đã chia (hoặc tài liệu đã làm sạch) lên làm kiến thức nền; giới hạn số file/dung lượng của từng nền tảng **chưa kiểm chứng** | API với chỉ mục riêng |

(Project, Gem, GPT tùy chỉnh là các tính năng của Claude, Gemini, ChatGPT cho bạn tải tài liệu lên để AI dùng làm kiến thức nền khi trả lời. API là cổng để chương trình của bạn gọi trực tiếp AI mà không qua khung chat.)

**Buộc chuyển sang code khi [Đề xuất]:** (a) hơn khoảng 100 tài liệu hoặc khoảng 5.000 khối; (b) tài liệu đổi hằng tuần; (c) cần mã khối ổn định để trích dẫn có kiểm tra (Cấp 5); (d) cần kiểm tự động liên kết/trích nguyên văn. Ngưỡng là ước lượng của nhóm soạn, chưa có nguồn.

!!! tip "Nói đơn giản"
    Làm tay vẫn được khi bạn chỉ có vài chục tài liệu ít đổi. Khi tài liệu nhiều (hàng trăm), đổi hằng tuần, hoặc bạn cần máy tự kiểm trích dẫn, thì nên nhờ người biết code. Các con số ngưỡng ở đây chỉ là ước lượng.

---

## 6. Tiêu chí lên Cấp 4 (đo được)

Chỉ lên Cấp 4 (tìm kiếm) khi **tất cả** thỏa **[Đề xuất; ngưỡng gợi ý]**:
1. 100% tài liệu mục tiêu đã thành khối; mỗi khối có `id`, `h`, `source_file`, trang, `heading_path`.
2. Hai lần chạy liên tiếp trên cùng dữ liệu cho cùng tập `id` (kiểm bằng `cmp`); sửa một câu trong một tài liệu chỉ làm đổi `h` của khối chứa câu đó (kiểm bằng so sánh Bài 3.8). (`cmp` là lệnh có sẵn trên máy để so hai tệp xem có giống hệt nhau không.)
3. Kiểm 20 khối ngẫu nhiên theo Bài 3.9: 0 bảng bị cắt đôi; không quá 2/20 khối không tự đứng được.
4. Có bộ 15-30 câu hỏi thử có đáp án (Bài 3.1), và ít nhất với **tìm bằng từ khóa đơn giản** đáp án đúng nằm trong top-10 ở một tỷ lệ bạn đặt (ví dụ 80%); nếu dưới ngưỡng, sửa cách chia/tiền tố trước khi thêm công cụ tìm phức tạp.
5. Có quy trình cập nhật (Bài 3.8) và đã thử chạy một lần với tài liệu thật đã đổi.

Cấp 4 sẽ đo lại kích thước/chồng lấn và có/không tiền tố với công cụ tìm thật.

!!! tip "Nói đơn giản"
    Trước khi sang bước tìm kiếm, hãy chắc rằng nền đã vững: mọi tài liệu đã thành khối có nhãn, chạy lại hai lần ra cùng số hiệu, kiểm thử 20 khối không có bảng đứt, và dùng tìm từ khóa đơn giản cũng ra đúng đáp án ở mức bạn đặt ra.

---

## 7. Ví dụ cho SME Việt Nam

Bảng dưới đây gợi ý một khối nên là gì với từng loại tài liệu quen thuộc. Các mã trong cột "Mã ví dụ" chỉ là ví dụ để bạn hình dung cách đặt tên, không phải mã thật.

| Tài liệu | Đơn vị khối [Đề xuất] | Mã ví dụ | Lưu ý |
|---|---|---|---|
| Chính sách bán hàng | Một mục/điều khoản (heading cấp 2-3) | `CSBH2026#2.1-dieu-kien` | Gắn ngày hiệu lực; bản cũ đánh dấu `het_hieu_luc` |
| Bảng giá | Một nhóm sản phẩm kèm hàng tiêu đề cột; **hoặc** một dòng + tiêu đề cột lặp lại | `BG2026Q4#nhom-A` | Không cắt giữa bảng; đơn vị VND ghi trong khối |
| Hợp đồng mẫu | Một điều | `HD-MAU-01#dieu-7` | Điều khoản trừ/ngoại lệ ở cùng khối hoặc có liên kết có kiểu |
| Hóa đơn đã trích JSON (Cấp 2) | Một hóa đơn = một khối (hoặc bảng dữ liệu, không cần chia) | `HDN-0001234` | Phù hợp tìm bằng lọc trường (Cấp 4), không cần vector |
| SOP nội bộ (đổi trả, bảo hành) | Một bước hoặc một quy trình ngắn; lớp điều hướng gộp theo "việc cần làm" | `SOP-DOITRA#buoc-3` | Dạng này gần nhất với trường hợp Airbnb (P6) |

(Cột "Phù hợp tìm bằng lọc trường" nghĩa là với hóa đơn, bạn có thể tìm bằng cách lọc theo các cột như số hóa đơn, ngày, nhà cung cấp, giống lọc trong Excel, chứ không cần tìm theo nghĩa. "Vector" là dãy số mà mô hình embedding tạo ra từ chữ.)

---

## 8. Tài liệu tham khảo

Ngày truy cập tất cả: **2026-11-11**.

**Bài báo (đã đọc nội dung qua alphaXiv)**
- **P1.** Zhou, Wang, Koopman, Zuccon. "Beyond Chunk-Then-Embed: A Comprehensive Taxonomy and Evaluation of Document Chunking Strategies for Information Retrieval", arXiv:2602.16974 (02/2026). https://www.alphaxiv.org/abs/2602.16974 . Loại: bài báo (tái lập). Tin cậy: trung bình-cao.
- **P2.** Kuehlkamp, Moreira, Rund. "Does Document Structure Help Dense Retrieval? A Placebo-Controlled Ablation of Four Mechanisms Across Two Corpora", arXiv:2610.10170 (10/2026). https://www.alphaxiv.org/abs/2610.10170 . Loại: bài báo. Tin cậy: trung bình-cao về phương pháp; hiệu ứng nhỏ; tiếng Anh.
- **P3.** Bian và cs. "Chunk Recomputation under Real Document Revisions...", arXiv:2610.31019 (10/2026). https://www.alphaxiv.org/abs/2610.31019 . Loại: bài báo. Tin cậy: trung bình.
- **P4.** Caspari và cs. "When Is Complex Chunking Worth It? A Multi-Objective Evaluation of Chunking Methods at Scale", arXiv:2608.16586 (CIKM 2026). https://www.alphaxiv.org/abs/2608.16586 . Loại: bài báo hội nghị. Tin cậy: trung bình-cao.
- **P5.** Singh. "Parser, Chunking, and Embedding Interactions in Retrieval-Augmented Generation over Indian Government Regulatory Documents", arXiv:2609.31660 (09/2026). https://www.alphaxiv.org/abs/2609.31660 . Loại: bài báo chưa phản biện. Tin cậy: trung bình-thấp.
- **P6.** Bako, Min, Shao, Cheng, Mehdad (Airbnb). "Frustratingly Easy Agentic RAG via Portable Skills: A Case Study in Customer Support", arXiv:2610.14428 (10/2026). https://www.alphaxiv.org/abs/2610.14428 . Loại: bài báo nghiên cứu trường hợp. Tin cậy: trung bình (một công ty, 132 ca, điều kiện so sánh không khớp hoàn toàn, tác giả tự nêu).

**Blog/tài liệu**
- **T-A1.** Anthropic. "Introducing Contextual Retrieval" (2024-09-19). https://www.anthropic.com/news/contextual-retrieval . Loại: blog kỹ thuật chính thức. Tin cậy: cao về mô tả phương pháp; số liệu là tự đo, chưa phản biện (P2 nêu rõ).
- **T-D1.** Docling - tài liệu chunking và ví dụ Hybrid chunking. https://docling-project.github.io/docling/concepts/chunking/ và https://docling-project.github.io/docling/examples/hybrid_chunking/ . Loại: tài liệu chính thức. Tin cậy: trung bình (chỉ thấy tóm tắt qua kết quả tìm kiếm; chưa chạy thử mã).

---

## 9. Chưa kiểm chứng / cần kiểm tra lại

1. **Mọi bằng chứng so sánh chunking ở 3.3 là tiếng Anh hoặc Trung-Anh**, chủ yếu benchmark học thuật; **không có** số đo trên tiếng Việt hay tài liệu SME Việt Nam. Cần tự đo bằng bộ câu hỏi thử (Bài 3.1, 3.4).
2. **Số lượng token tiếng Việt so với tiếng Anh** cho cùng nội dung (ảnh hưởng chọn kích thước): chưa đo; chỉ là giả thuyết.
3. **Contextual Retrieval:** số liệu 35/49/67% là tự đo của Anthropic; P2 và P4 không tái lập lợi ích so với cách đơn giản trong điều kiện của họ. Chưa có nghiên cứu độc lập đã đọc cho tài liệu tiếng Việt.
4. **Lớp điều hướng Airbnb:** ablation không đạt ý nghĩa thống kê (p nhỏ nhất 0,078); phép so với RAG sản xuất không khớp điều kiện; chưa biết hiệu quả khi kho nhỏ (hàng chục tài liệu) hay khi có người duyệt.
5. **Bài báo SAP arXiv:2608.00122 (bộ nhớ dạng cặp hỏi-đáp):** theo thông tin dự án, không đọc lại trong phiên này nên không dùng làm bằng chứng ở Cấp 3.
6. **Docling HybridChunker, `merge_peers`, `repeat_table_header`, `LineBasedTokenChunker`:** chỉ từ tóm tắt tìm kiếm của trang tài liệu chính thức; cần đọc trang gốc và chạy thử.
7. **Giới hạn số file/dung lượng/cách tải kiến thức** của Claude Project, Gemini Gem, ChatGPT tùy chỉnh: không kiểm chứng trong phiên này.
8. **Mã chưa chạy thử riêng:** kiểm trích nguyên văn (chuỗi con), kiểm liên kết lớp điều hướng. Đã chạy thử: `chunk_markdown` (chia theo tiêu đề, mã ổn định hai lần chạy), so sánh `id`/`h` giữa hai phiên bản.
9. **Ngưỡng định lượng** ở mục 5 và mục 6 (số tài liệu/khối, 80%, 2/20): ước lượng của nhóm soạn.
10. **Thiết kế mã khối:** đề xuất hai mã (`id` theo đường dẫn tiêu đề + thứ tự; `h` theo nội dung) là thiết kế của nhóm soạn, không từ bài báo; điểm yếu đã biết: chèn tiêu đề trùng tên làm đổi mã các khối sau (Bài 3.2). Cần thử trên tài liệu thật có tiêu đề trùng.
