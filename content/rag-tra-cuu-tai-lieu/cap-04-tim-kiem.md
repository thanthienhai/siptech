# Cấp 4 — Tìm kiếm (Search)

> Trạng thái: bản nháp nghiên cứu, ngày truy cập nguồn 2026-11-11.
> Quy ước: **[Nguồn]** = kết quả có trong nguồn đã đọc; **[Đề xuất]** = ý kiến của nhóm biên soạn, chưa được nguồn nào chứng minh; **[Đã chạy thử]** / **[Chưa chạy thử]** áp dụng cho code.

---

## 1) Mục tiêu và người đọc

**Người đọc:** chủ/quản lý SME ở Việt Nam và một người "làm IT kiêm nhiệm" (có thể chỉ biết Excel + chút Python). Đã qua C2 (tài liệu thành text có cấu trúc) và C3 (chia khối, đánh chỉ mục).

**Mục tiêu cấp này:** sau C4, doanh nghiệp có một "công cụ tìm" trả về đúng 3–5 khối tài liệu liên quan khi nhân viên hỏi, và **có con số** (recall@k, MRR) cho biết công cụ tìm tốt đến đâu trên chính tài liệu của mình. Chưa cần AI trả lời; C4 chỉ làm việc "tìm đúng chỗ".

**Sản phẩm cầm đi được:** (a) một công cụ tìm chạy được (không code: Project/Gem/GPT với tệp tải lên, hoặc code nhẹ: script Python / SQLite); (b) một **bộ câu hỏi vàng** 30–50 câu kèm đáp án đúng nằm ở khối nào; (c) một bảng điểm so sánh các cách tìm trên bộ câu hỏi đó.

---

## 2) Câu hỏi cấp này trả lời / lỗi của cấp trước dẫn đến cấp này

**Câu hỏi:** "Trong 2.000 trang tài liệu của công ty, khối nào chứa câu trả lời cho câu hỏi này?"

**Lỗi của cấp trước (C3) dẫn đến C4:**
- Có khối rồi nhưng tìm bằng Ctrl+F: nhân viên gõ "bảo hành bao lâu" mà tài liệu viết "thời hạn bảo hành" → trượt hoặc ra quá nhiều kết quả.
- Dán cả thư mục vào AI: tốn token, chậm, và (xem mục 3.7) AI dùng ngữ cảnh dài không đều.
- Không biết tìm "tốt" hay "dở" vì chưa đo. Hệ quả: cảm giác "AI trả lời sai" nhưng thật ra là **tìm sai khối**.

---

## 3) Kiến thức nền (ngắn, chính xác)

### 3.1 Tìm từ khóa — BM25
- BM25 là hàm chấm điểm dựa trên **từ xuất hiện trong câu hỏi và trong khối**: từ hiếm có trọng số cao hơn từ phổ biến, và khối quá dài bị trừ nhẹ. Không hiểu nghĩa, chỉ khớp chữ. **[Nguồn: BEIR, mô tả BM25 là "bag-of-words ... token-matching", mục 3–4]**
- Mạnh: mã sản phẩm, số hiệu điều khoản, tên riêng, số điện thoại — những thứ "phải khớp đúng chữ".
- Yếu: người hỏi dùng từ khác với tài liệu ("lexical gap", BEIR gọi là khoảng cách từ vựng).

### 3.2 Tìm vector — embedding
- Một mô hình embedding đổi mỗi khối thành một dãy số (vector). Câu hỏi cũng đổi thành vector; khối nào "gần" nhất (thường đo bằng cosine) thì được trả về. Bắt được ý nghĩa gần nhau dù khác chữ. **[Nguồn: BEIR mục 2.1; VN-MTEB mô tả "cosine similarity" để xếp hạng]**
- Yếu: có thể trượt mã/số/tên riêng; chất lượng phụ thuộc mô hình và ngôn ngữ; khối cần nhúng trước (tốn thời gian/tiền một lần).

### 3.3 Tìm lai (hybrid) và cách trộn
- Chạy cả BM25 và vector rồi trộn danh sách. Cách trộn phổ biến, không cần chuẩn hóa điểm: **Reciprocal Rank Fusion (RRF)** — mỗi khối nhận điểm `Σ 1/(k + hạng)` qua các danh sách. **[Nguồn: bài gốc Cormack, Clarke, Büttcher, SIGIR 2009 (xác nhận tồn tại qua Google Research); công thức và k=60 lấy từ các bài giải thích thứ cấp — tôi chưa đọc được nội dung PDF gốc, xem mục 9]**
- **[Nguồn: Anthropic, Contextual Retrieval]** Kết hợp embedding + BM25 tốt hơn embedding đơn lẻ (kết luận của Anthropic trên bộ dữ liệu của họ).
- **[Nguồn: Airbnb arXiv 2610.14428]** Hệ thống dùng BM25 + dense, không re-ranker; ở bảng 5 (n=132) "BM25 only" và "dense only" đều không tách khỏi hệ thống đầy đủ ở mức p<0,05 (p lần lượt 0,210 và 0,263). Đây là **không phát hiện được khác biệt** (mẫu nhỏ), không phải bằng chứng hai cách "bằng nhau". Và trong bài đó, cái tạo khác biệt là cách tổ chức nội dung (lớp điều hướng), không phải công cụ tìm.

### 3.4 Reranking
- Bước 2: lấy N khối ứng viên (ví dụ 100–150) từ bước tìm nhanh, rồi dùng mô hình chậm hơn, đọc cả câu hỏi lẫn khối cùng lúc (cross-encoder) để xếp lại.
- **[Nguồn: BEIR bảng 2, 3]** BM25 + cross-encoder (MiniLM 6 lớp) đạt nDCG@10 trung bình hơn BM25 khoảng +11% trên 18 bộ dữ liệu tiếng Anh, nhưng trên 1 triệu tài liệu DBPedia độ trễ ~450 ms (GPU) / 6100 ms (CPU) so với BM25 ~20 ms (CPU, phần cứng 2021).
- **[Nguồn: Anthropic, Contextual Retrieval]** Lấy top 150 rồi rerank xuống top 20 (dùng Cohere reranker) giảm tỷ lệ truy xuất hỏng top-20 từ 5,7% xuống 1,9% (so với embedding thuần) — trên các bộ dữ liệu riêng của Anthropic, cần tự kiểm trên dữ liệu mình.
- **[Nguồn: Airbnb]** Không dùng re-ranker vẫn đạt kết quả tốt trong bối cảnh kho tài liệu đã được biên tập kỹ. Tác giả nói rõ: re-ranker có thể giúp nhiều hơn ở kho dữ liệu "nhiễu hơn hoặc non hơn". **[Đề xuất]** SME nên thêm reranker **sau cùng**, chỉ khi bảng điểm cho thấy đáp án nằm ở hạng 6–20 thay vì top 5.

### 3.5 Bằng chứng so sánh (tóm tắt có nguồn)
| Phát hiện | Nguồn | Lưu ý |
|---|---|---|
| BM25 là mốc mạnh khi chuyển sang miền dữ liệu mới; mô hình dense có thể thua BM25 ở nhiều bộ dữ liệu | BEIR (arXiv 2104.08663): 18 bộ dữ liệu tiếng Anh, 10 hệ thống | Dữ liệu tiếng Anh, mô hình đời 2019–2021; các embedding đời sau đã tốt hơn |
| Mô hình multilingual-e5-large, bge-m3 vượt BM25 rõ rệt trên MIRACL (18 ngôn ngữ), trong đó có tiếng Việt: trung bình nDCG@10 M3-dense 69,2 vs BM25 31,9 (BM25 dùng tokenizer của XLM-R) | M3-Embedding (arXiv 2402.03216) bảng 1 | Bài của chính nhóm tác giả mô hình; BM25 ở đây dùng tokenizer subword, không phải bản BM25 tối ưu cho tiếng Việt |
| Dense+Sparse+Multi-vector của bge-m3 tốt hơn từng loại riêng lẻ trên MIRACL | M3-Embedding bảng 1 (All 71,5 vs Dense 69,2) | Chênh lệch nhỏ |
| BM25 vẫn rất tốt với tài liệu dài: trên MLDR, BM25 53,6 vs M3-Dense 52,5 nDCG@10 | M3-Embedding bảng 3 | Chỉ 13 ngôn ngữ, không gồm tiếng Việt |
| "Lệch từ vựng" của bộ dữ liệu có thể làm thiệt cho dense | BEIR mục 6 (TREC-COVID, ANCE tăng từ 0,654 lên 0,735 sau khi bổ sung nhãn) | Nhắc rằng benchmark không hoàn hảo; càng cần **bộ câu hỏi riêng** |

### 3.6 Đặc thù tiếng Việt
**Tách từ.** Tiếng Việt viết cách nhau bằng dấu cách giữa các *âm tiết*, không phải giữa các *từ* ("khởi nghiệp" là một từ hai âm tiết). Với BM25, mặc định coi mỗi âm tiết là một token thì "bảo hành" bị tách thành "bảo" + "hành" (ghép lại mất ý). Có các công cụ tách từ xác minh được tồn tại:
- **underthesea** — thư viện Python, README liệt kê "Word Segmentation", dùng `word_tokenize(text)`, giấy phép Apache-2.0. **[Nguồn: github.com/undertheseanlp/underthesea]**
- **pyvi** — "Python Vietnamese Core NLP Toolkit"; `ViTokenizer.tokenize(...)` để tách từ, `ViUtils.remove_accents(...)` để bỏ dấu. **[Nguồn: github.com/trungtv/pyvi]**
- **VnCoreNLP (RDRSegmenter)** — PhoBERT yêu cầu đầu vào đã tách từ ("INPUT TEXT MUST BE ALREADY WORD-SEGMENTED!") và khuyên dùng RDRSegmenter của VnCoreNLP. **[Nguồn: github.com/VinAIResearch/PhoBERT]** Lưu ý: yêu cầu này là của PhoBERT. Các mô hình embedding đa ngữ (e5, bge-m3) dùng tokenizer subword riêng, **tôi không có nguồn nói rằng chúng cần tách từ trước**.
- **[Chưa có bằng chứng]** Tôi không tìm được nguồn đáng tin so sánh BM25 có/không tách từ trên dữ liệu doanh nghiệp tiếng Việt. Phần 4, bài 3 hướng dẫn tự đo.

**Chuẩn hóa dấu.** Hai việc khác nhau:
1. *Chuẩn hóa Unicode (NFC)*: cùng một chữ "ế" có thể được mã hóa dạng dựng sẵn hoặc dạng tổ hợp (e + dấu mũ + dấu sắc). Văn bản copy từ Word, PDF, web hay lẫn hai dạng → so khớp trượt khó hiểu. **[Đề xuất]** luôn đưa về NFC (`unicodedata.normalize("NFC", s)` có sẵn trong thư viện chuẩn Python) cho cả tài liệu lẫn câu hỏi.
2. *Bỏ dấu*: người dùng thường gõ không dấu ("bao hanh"). **[Đề xuất]** lập chỉ mục *cả hai* (có dấu và không dấu) hoặc dùng tùy chọn bỏ dấu của công cụ. Rủi ro: bỏ dấu làm trùng nghĩa ("ma", "má", "mã"...). Cần đo trên bộ câu hỏi riêng. SQLite FTS5 có tùy chọn `remove_diacritics` cho bộ tách `unicode61`; giá trị 2 xử lý đúng mọi ký tự Latin. **[Nguồn: sqlite.org/fts5.html]** Cũng cần nhớ chữ "đ" không phải chữ có dấu tổ hợp nên thường phải ánh xạ riêng (code mẫu bên dưới đã làm).

**Mô hình embedding hỗ trợ tiếng Việt — chỉ nêu những cái có benchmark.** Nguồn chính: **VN-MTEB** (arXiv 2507.21500; GreenNode AI; Findings của EACL 2026): 41 bộ dữ liệu, 6 tác vụ, 18 mô hình, **tạo bằng cách dịch máy** bộ MTEB tiếng Anh. Điểm trung bình tác vụ Retrieval (15 bộ) trích từ bảng 3 của bài:

| Mô hình | Tham số | Chiều vector | Điểm Retrieval VN-MTEB | Điểm trung bình 6 tác vụ |
|---|---|---|---|---|
| multilingual-e5-large-instruct | 560M | 1024 | 40,88 | 67,99 |
| bge-m3 | 568M | 1024 | 39,84 | 64,90 |
| gte-multilingual-base | 305M | 768 | 38,38 | 65,22 |
| multilingual-e5-large | 560M | 1024 | 37,65 | 63,87 |
| multilingual-e5-base | 278M | 768 | 34,50 | 62,42 |
| multilingual-e5-small | 118M | 384 | 34,12 | 60,66 |

- Các mô hình 7B (gte-Qwen2-7B-instruct 46,05; e5-mistral-7b 41,73 ở Retrieval) cao hơn nhưng nặng hơn nhiều. **[Nguồn: VN-MTEB bảng 3]**
- **Giới hạn của benchmark này:** bộ dữ liệu là bản dịch máy từ tiếng Anh (chủ đề Wikipedia, khoa học, Quora...), **không phải** tài liệu bảng giá/bảo hành/nội quy. Chính tác giả nêu giới hạn về bối cảnh văn hóa/văn phong và thiếu tài liệu rất dài. **Điểm số chỉ để chọn ứng viên; phải tự kiểm trên dữ liệu riêng.**
- Về bge-m3: hỗ trợ >100 ngôn ngữ, đầu vào tới 8192 token, ba chế độ (dense, sparse, multi-vector), giấy phép MIT. **[Nguồn: arXiv 2402.03216; huggingface.co/BAAI/bge-m3]** Trên MIRACL, tiếng Việt không nằm trong 18 ngôn ngữ của bảng 1 (bảng liệt kê ar, bn, en, es, fa, fi, fr, hi, id, ja, ko, ru, sw, te, th, zh, de, yo) — vì vậy số MIRACL của M3 **không phải số tiếng Việt**. Tiếng Việt có mặt ở bài kiểm tra chéo ngôn ngữ MKQA (bảng 2 và 13: vi, M3-Dense Recall@100 là 76,6; Recall@20 là 69,6; BM25 lần lượt 46,6 và 33,6) — đó là truy vấn tiếng Việt tìm đoạn tiếng Anh, không phải tiếng Việt-tiếng Việt.
- Họ multilingual-e5 (small/base/large): đào tạo trên ~1 tỷ cặp văn bản đa ngữ; MIRACL trung bình 16 ngôn ngữ: large nDCG@10 66,5; BM25 39,3 (báo cáo kỹ thuật của chính Microsoft). **[Nguồn: arXiv 2402.05672]**
- Các mô hình nhỏ chuyên tiếng Việt có xuất hiện trong VN-MTEB (ví dụ `Vietnamese-Embedding` 568M, `halong-embedding` 278M, `vietnamese-bi-encoder` 135M), nhưng trong bảng 3 chúng **không vượt** các mô hình đa ngữ cùng cỡ ở Retrieval (34,18 / 34,45 / 25,37). **[Nguồn: VN-MTEB bảng 3]** Tôi không đánh giá thêm độ tin cậy của chúng.

**Kích thước và chi phí — cục bộ so với API.**
- Số tham số xem bảng trên: mE5-small 118M, bge-m3 568M. **[Nguồn: VN-MTEB bảng 3]** Dùng làm thước đo "nặng/nhẹ"; **tôi không có số liệu RAM/tốc độ được đo trên máy văn phòng thông thường** → **[Chưa kiểm chứng]**.
- Số đo gần nhất có nguồn: BEIR đo trên 1 triệu tài liệu — index dense 768 chiều ~3 GB, BM25 ~0,4 GB; độ trễ dense ~125–275 ms/câu trên CPU Xeon 8 nhân, BM25 ~20 ms (phần cứng 2021, mô hình tiếng Anh đời cũ). **[Nguồn: BEIR bảng 3]** Chỉ dùng để thấy tỷ lệ: BM25 nhẹ hơn nhiều lần; một SME có vài nghìn đến vài chục nghìn khối thì cả hai đều rẻ.
- Giá API embedding của các hãng thay đổi: **[Chưa kiểm chứng]** — xem giá hiện hành trên trang chính thức của nhà cung cấp tại thời điểm làm; tôi chưa truy cập trang giá nào nên không nêu con số.
- **[Đề xuất]** Nguyên tắc chọn: tài liệu nội bộ nhạy cảm/không muốn gửi ra ngoài → chạy mô hình cục bộ; tài liệu không nhạy cảm, ít người dùng, không có máy → API. Dù chọn đường nào, ghi lại tên + phiên bản mô hình dùng để nhúng; đổi mô hình = nhúng lại toàn bộ.

### 3.7 Khi nào KHÔNG cần vector (và có khi không cần tìm kiếm)
- **Corpus nhỏ → đưa thẳng vào prompt.** Anthropic: nếu kho tri thức nhỏ hơn 200.000 token (~500 trang), có thể đưa toàn bộ vào prompt, không cần RAG; kèm prompt caching có thể giảm độ trễ >2 lần và chi phí tới 90%. **[Nguồn: Anthropic, Contextual Retrieval]** Con số 200.000 token là ngữ cảnh của mô hình Claude lúc bài đăng; **[Chưa kiểm chứng]** giới hạn ngữ cảnh hiện hành của từng sản phẩm/gói — xem trang mô hình của nhà cung cấp.
- **Nhưng ngữ cảnh dài không miễn phí về chất lượng.** Liu và cộng sự: hiệu năng thường cao nhất khi thông tin cần nằm ở đầu hoặc cuối ngữ cảnh và giảm rõ khi nằm ở giữa (đường chữ U); có trường hợp (GPT-3.5-Turbo, 20–30 tài liệu) thấp hơn cả khi không đưa tài liệu nào (56,1%); mô hình cửa sổ dài hơn không nhất thiết dùng ngữ cảnh tốt hơn. **[Nguồn: arXiv 2307.03172]** Cảnh báo: đây là các mô hình 2023 (GPT-3.5, Claude 1.3, MPT, LongChat); mô hình đời mới có thể khác — **tự đo trên mô hình đang dùng**.
- Cũng từ bài đó: hiệu năng bão hòa sớm hơn recall của bộ truy xuất — dùng 50 tài liệu thay 20 chỉ tăng ~1–1,5%. **[Nguồn: arXiv 2307.03172, mục 5]** Gợi ý: đừng đẩy k quá lớn.
- **[Đề xuất] Quy tắc 3 vùng cho SME** (ngưỡng là điểm xuất phát, phải kiểm lại):
  1. Toàn bộ tài liệu cần dùng < ~100 trang và ít thay đổi → **nhét thẳng vào prompt/Project**, bỏ qua C4 (nhưng vẫn làm bộ câu hỏi vàng để kiểm).
  2. 100–500 trang → thử nhét thẳng vs BM25 top-k; so điểm trên bộ câu hỏi.
  3. > 500 trang, hoặc nhiều nhóm tài liệu, hoặc cần trích dẫn chính xác từng điều khoản → cần tìm kiếm (C4).
- Tìm kiếm rẻ nhất (từ khóa) vẫn hữu ích kể cả khi dùng ngữ cảnh dài: để *tiền lọc* tài liệu nào đưa vào.

### 3.8 Lưu trữ nhẹ (chỉ nêu cái xác minh được)
- **SQLite FTS5**: có sẵn từ SQLite 3.9.0 (trong bản "amalgamation"), tìm bằng `MATCH`, xếp hạng bằng hàm `bm25()` có sẵn (giá trị càng nhỏ càng khớp), cho phép đặt trọng số cột (`bm25(email, 10.0, 5.0)`); bộ tách từ có `unicode61` (mặc định), `ascii`, `porter`, `trigram`. **[Nguồn: sqlite.org/fts5.html]** **[Đã chạy thử]** trên SQLite 3.45.3 (Python 3.13, Windows): với `tokenize='unicode61 remove_diacritics 2'`, truy vấn "bao hanh" và "bảo hành" đều khớp khối "bảo hành".
- Tìm vector trong SQLite hay thư viện vector chuyên dụng (FAISS, Chroma, sqlite-vec...): **[Chưa kiểm chứng]** — tôi chưa đọc tài liệu của các công cụ này, không khuyến nghị cụ thể. Với vài nghìn khối, **[Đề xuất]** có thể lưu vector dạng file `.npy`/JSON và tính cosine bằng NumPy; không cần cơ sở dữ liệu vector.

---

## 4) Chuỗi bài nhỏ

### Bài 4.1 — Lập bộ câu hỏi vàng (golden set)
- **Mục tiêu:** có thước đo trước khi chọn công cụ.
- **Thực hành:**
  1. Từ C3, mỗi khối có mã (ví dụ `BH-01`, `GIA-03`, `NQ-07`).
  2. Hỏi 3–5 nhân viên thật: "tuần qua anh/chị đã hỏi gì về tài liệu?" + lấy từ tin nhắn Zalo/email. Giữ nguyên cách gõ (có cả không dấu, viết tắt).
  3. Với mỗi câu, ghi *mã khối chứa đáp án* (có thể 1–2 khối). Ghi cả câu **không có đáp án** trong tài liệu (10–20% bộ) để dùng ở C5.
  4. Tối thiểu 30 câu; ưu tiên 50. Chia ra loại: tra cứu số (giá), điều kiện (bảo hành), quy trình, câu phải ghép 2 khối.
- **Sản phẩm:** bảng 3 cột `câu hỏi | khối đúng | loại` (Excel/CSV).
- **Lỗi thường gặp:** để một người biết tài liệu rõ viết câu hỏi → câu quá giống chữ trong tài liệu, điểm ảo cao; không có câu không-đáp-án; sửa tài liệu mà không cập nhật mã khối.
- **[Đề xuất]** 30–50 câu là quy ước thực dụng của chúng tôi, không phải ngưỡng thống kê. Với n nhỏ, chênh lệch vài điểm là nhiễu — Airbnb với n=132 vẫn không tách được các cấu hình ở p<0,05. **[Nguồn: Airbnb bảng 5]**

### Bài 4.2 — Hiểu và đo recall@k, MRR (bằng tay trước)
- **Giải thích đơn giản:**
  - **recall@k** (ở đây theo kiểu "có trúng hay không"): trong k khối đầu tiên công cụ trả về, có chứa khối đúng không? Điểm = tỷ lệ câu hỏi có trúng. recall@5 = 0,8 nghĩa là 80% câu hỏi có khối đúng nằm trong 5 kết quả đầu.
  - **MRR** (mean reciprocal rank): với mỗi câu, lấy 1 / (hạng của khối đúng đầu tiên) — hạng 1 được 1, hạng 2 được 0,5, hạng 5 được 0,2, không thấy được 0; rồi lấy trung bình. MRR cao = khối đúng hay đứng đầu.
  - Cách dùng: recall@k cho biết "có đủ nguyên liệu đưa cho AI không"; MRR cho biết "có xếp đúng thứ tự không". BEIR dùng nDCG@10 thay hai số này vì xử lý được mức liên quan nhiều bậc; với SME một khối-đúng/câu thì recall@k và MRR đã đủ. **[Nguồn: BEIR mục 3.3 nói lý do chọn nDCG@10; phần "đủ cho SME" là Đề xuất]**
- **Thực hành:** lấy 10 câu đầu, tìm bằng tay (Ctrl+F hoặc để AI Project tìm), điền hạng của khối đúng, tính tay recall@3, recall@5, MRR trong Excel (`=IF(hạng="";0;1/hạng)`).
- **Sản phẩm:** một sheet điểm cơ sở ("Ctrl+F" hoặc "hỏi thẳng AI Project") để so sánh.
- **Lỗi thường gặp:** đo trên đúng câu đã dùng để chỉnh công cụ (quá khớp) → chia bộ ra: 2/3 để chỉnh, 1/3 giữ lại chỉ chấm một lần.

### Bài 4.3 — BM25 từ khóa với tiếng Việt (code nhẹ)
- **Mục tiêu:** chạy được công cụ tìm từ khóa, thử 3 cách xử lý chữ Việt, đo bằng bộ câu hỏi.
- **Thực hành:** chạy script dưới đây trên các khối của bạn (đọc từ CSV/JSON thay cho 4 khối mẫu). Thử ba biến thể: (a) có dấu; (b) bỏ dấu cả hai phía; (c) có dấu + cặp âm tiết liền nhau (bigram, xấp xỉ tách từ). Sau đó thử `underthesea.word_tokenize` hoặc `pyvi.ViTokenizer.tokenize` thay cho `tokens`. Ghi recall@3/@5 và MRR cho từng biến thể.

```python
# BM25 thuần Python — [Đã chạy thử] Python 3.13 với `python -I -X utf8`, 4 khối mẫu
import math, re, unicodedata
from collections import Counter

def norm(s):                      # NFC + chữ thường (giữ dấu)
    return unicodedata.normalize("NFC", s).lower()

def strip_marks(s):               # bỏ dấu; "đ" cần xử lý riêng
    s = unicodedata.normalize("NFD", norm(s)).replace("đ", "d")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def tokens(s):  return re.findall(r"\w+", norm(s))
def bigrams(t): return t + [a + "_" + b for a, b in zip(t, t[1:])]

class BM25:
    def __init__(self, docs, k1=1.2, b=0.75, tok=tokens):
        self.tok, self.k1, self.b = tok, k1, b
        self.tf = [Counter(tok(d)) for d in docs]
        self.len = [sum(c.values()) for c in self.tf]
        self.avg = sum(self.len) / len(docs)
        df, n = Counter(t for c in self.tf for t in c), len(docs)
        self.idf = {t: math.log(1 + (n - d + .5) / (d + .5)) for t, d in df.items()}
    def top(self, q, k=5):
        sc = []
        for tf, L in zip(self.tf, self.len):
            sc.append(sum(self.idf[t] * tf[t] * (self.k1 + 1) /
                          (tf[t] + self.k1 * (1 - self.b + self.b * L / self.avg))
                          for t in self.tok(q) if t in tf))
        return sorted(range(len(sc)), key=lambda i: -sc[i])[:k]

def recall_at_k(ranked, gold, k): return 1.0 if gold in ranked[:k] else 0.0
def rr(ranked, gold): return 1 / (ranked.index(gold) + 1) if gold in ranked else 0.0
```
  Kết quả chạy thử trên 4 khối/4 câu mẫu của chúng tôi: cả ba biến thể đều đạt recall@1 = recall@3 = MRR = 1,00. Quy mô quá nhỏ nên **chỉ chứng minh code chạy đúng, không chứng minh biến thể nào tốt hơn.**
- **Hoặc dùng SQLite FTS5** (ít code hơn, nhanh hơn khi nhiều khối; **[Đã chạy thử]**):
```python
import sqlite3
c = sqlite3.connect("kb.db")
c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS t USING fts5(id UNINDEXED, body, "
          "tokenize='unicode61 remove_diacritics 2')")
c.executemany("INSERT INTO t VALUES (?,?)", [("BH-01", "Máy giặt được bảo hành 24 tháng ...")])
# bọc cụm từ trong ngoặc kép để tránh lỗi cú pháp với ký tự đặc biệt
rows = c.execute("SELECT id, bm25(t) FROM t WHERE t MATCH ? ORDER BY bm25(t) LIMIT 5",
                 ('"bao hanh"',)).fetchall()
```
  Lưu ý khi đưa câu hỏi người dùng vào `MATCH`: ký tự như `"`, `-`, `:` có ý nghĩa cú pháp; hãy làm sạch hoặc đặt từng từ trong ngoặc kép, nối bằng `OR`.
- **Sản phẩm:** `search.py` (hoặc `kb.db`) + bảng điểm 3–4 biến thể.
- **Lỗi thường gặp:** quên chuẩn hóa NFC khi nạp tài liệu từ Word/PDF; bỏ dấu cho tài liệu nhưng không bỏ dấu cho câu hỏi (hoặc ngược lại); không bỏ từ dừng thì không sao với BM25 (idf đã giảm trọng số), đừng tốn công sớm.

### Bài 4.4 — Tìm vector (embedding) và so với BM25
- **Mục tiêu:** thêm tìm theo ý nghĩa, chọn 1–2 mô hình ứng viên, đo cùng bộ câu hỏi.
- **Thực hành (code nhẹ):** chọn 2 ứng viên từ bảng 3.6 (ví dụ một mô hình nhỏ multilingual-e5-small và một mô hình lớn hơn như bge-m3 hoặc multilingual-e5-large). Nhúng toàn bộ khối một lần, lưu vector; nhúng câu hỏi; xếp hạng bằng cosine. **Đọc thẻ mô hình để biết cách dùng đúng** (một số mô hình yêu cầu tiền tố cho câu hỏi/đoạn văn, một số thì không; ví dụ thẻ bge-m3 nói không cần chỉ dẫn cho truy vấn, nhưng tôi chưa đọc được thẻ e5 nên **[Chưa kiểm chứng]** cú pháp tiền tố của e5). Tính recall@k và MRR như bài 4.3.
- **Thực hành (không code):** Gemini/ChatGPT/Claude tải tệp lên Project/Gem/GPT thực chất đã có bước tìm bên trong nhưng ta **không thấy** nó lấy khối nào → xem bài 4.7.
- **Sản phẩm:** bảng điểm: BM25 vs vector (mô hình A) vs vector (mô hình B), chia theo loại câu hỏi (tra cứu số / điều kiện / quy trình).
- **Lỗi thường gặp:** nhúng khối quá dài hoặc quá ngắn so với giới hạn mô hình (bge-m3 nhận tới 8192 token **[Nguồn: arXiv 2402.03216]**; giới hạn độ dài của họ e5 **[Chưa kiểm chứng]**, xem thẻ mô hình; riêng BEIR chỉ dùng 512 word-piece đầu của mỗi tài liệu cho các mô hình neural thời đó); dùng mô hình khác nhau để nhúng khối và câu hỏi; so điểm cosine tuyệt đối giữa các mô hình khác nhau (không so được).

### Bài 4.5 — Tìm lai (hybrid) bằng RRF
- **Mục tiêu:** kết hợp BM25 + vector.
- **Thực hành:** với mỗi câu hỏi lấy top 20 từ BM25 và top 20 từ vector; điểm RRF của khối = `1/(60+hạng_BM25) + 1/(60+hạng_vector)` (khối vắng ở một danh sách thì bỏ phần đó); xếp lại. k=60 là giá trị thường dùng **[Nguồn: bài giải thích thứ cấp, xem mục 9]**; thử thêm k=10 và k=100 xem điểm có đổi không.
```python
# [Chưa chạy thử] — RRF cho nhiều danh sách xếp hạng (mỗi danh sách là list id theo thứ tự tốt → kém)
def rrf(lists, k=60):
    s = {}
    for lst in lists:
        for r, d in enumerate(lst, 1):
            s[d] = s.get(d, 0) + 1 / (k + r)
    return sorted(s, key=s.get, reverse=True)
```
- **Sản phẩm:** dòng thứ ba trong bảng điểm: "lai".
- **Lỗi thường gặp:** trộn điểm thô BM25 với cosine (khác thang đo) — nên trộn theo hạng; lai nhưng không so với từng cách riêng nên không biết có đáng không. Nhớ bài học Airbnb: chưa chắc lai tốt hơn từng cách riêng một cách có ý nghĩa thống kê trong bối cảnh kho được biên tập kỹ; để số liệu của bạn quyết định.

### Bài 4.6 — Reranking (tùy chọn) và cải thiện khối
- **Mục tiêu:** chỉ làm khi bảng điểm cho thấy khối đúng thường ở hạng 6–20.
- **Thực hành:** (i) rẻ nhất: **sửa nội dung/khối** trước (thêm tiêu đề, tóm tắt "khối này trả lời câu hỏi gì" — đây là hướng mà bài Airbnb tạo khác biệt lớn nhất: bỏ "thực thể gộp" làm tụt gần nhất, p=0,078; bỏ lớp điều hướng thì mất khả năng tách; **[Nguồn: Airbnb bảng 5]** nhưng không cấu hình nào đạt p<0,05, nên đọc là "xu hướng"); (ii) thêm ngữ cảnh ngắn cho mỗi khối trước khi lập chỉ mục (Anthropic Contextual Retrieval: giảm lỗi truy xuất top-20 từ 5,7% xuống 3,7% nếu dùng Contextual Embeddings, 2,9% nếu thêm Contextual BM25 — trên bộ dữ liệu của Anthropic; sinh ngữ cảnh tốn ước tính một lần $1,02/triệu token tài liệu với prompt caching theo giả định trong bài); (iii) rerank bằng một mô hình cross-encoder hoặc API reranker: top 50–150 → top 5–10. **[Chưa kiểm chứng]** mô hình rerank nào hỗ trợ tiếng Việt tốt — tôi chưa đọc benchmark rerank tiếng Việt cụ thể ngoài nhóm tác vụ Reranking của VN-MTEB (3 bộ dữ liệu, bảng 3).
- **Sản phẩm:** so sánh trước/sau trên cùng bộ câu hỏi; ghi độ trễ trung bình mỗi câu.
- **Lỗi thường gặp:** rerank khi top-k ban đầu đã không chứa khối đúng (recall@50 thấp) — reranker không cứu được; bỏ qua chi phí độ trễ (BEIR: xếp lại bằng cross-encoder chậm hơn BM25 hàng chục lần).

### Bài 4.7 — Kiểm tra công cụ "hộp đen" (Project/Gem/GPT tùy chỉnh)
- **Mục tiêu:** đường không code cũng có số đo.
- **Thực hành:** dùng cùng bộ câu hỏi vàng; với mỗi câu, yêu cầu công cụ **nêu rõ tên tệp/đoạn nó dùng** rồi chấm "trúng/trượt" bằng tay. Ghi tỷ lệ trúng. Làm lại sau khi đổi cách đặt tên tệp, tách tệp, thêm mục lục.
- **Sản phẩm:** điểm "trúng nguồn" của hộp đen; quyết định có cần chuyển sang đường code không (mục 5).
- **Lỗi thường gặp:** tin câu trả lời nghe hợp lý mà không kiểm nguồn; một tệp PDF scan chưa OCR (C2 phải xong); tệp quá lớn bị công cụ cắt bớt mà không báo — **[Chưa kiểm chứng]** giới hạn tệp/ngữ cảnh hiện hành của từng sản phẩm, xem tài liệu chính thức.

---

## 5) Đường không code vs đường có code; khi nào buộc phải chuyển

| | Không code | Có code nhẹ |
|---|---|---|
| Cách làm | Tải tệp (đã chuẩn hóa ở C2/C3) lên Project/Gem/GPT; hoặc dán toàn bộ vào ngữ cảnh khi < ~100 trang | Python + BM25 / SQLite FTS5; thêm embedding khi cần |
| Mạnh | Nhanh, 0 hạ tầng | Thấy và chỉnh được từng khối trả về; đo được recall@k, MRR; kiểm soát dữ liệu nhạy cảm |
| Yếu | Không nhìn thấy bên trong; khó đo; giới hạn tệp/ngữ cảnh đổi theo sản phẩm | Cần người bảo trì; phải nhúng lại khi đổi mô hình |

**Buộc phải chuyển sang code khi (đề xuất, ngưỡng chỉnh theo thực tế):**
1. Điểm "trúng nguồn" của hộp đen < 80% sau khi đã tối ưu tên tệp/mục lục (bài 4.7).
2. Tài liệu vượt giới hạn tệp/ngữ cảnh của công cụ đang dùng.
3. Cần ghi log "khối nào đã được dùng" để kiểm toán (sang C5/C6).
4. Dữ liệu không được phép tải lên dịch vụ ngoài.
5. Nhiều nhóm người dùng khác quyền truy cập tài liệu (cần lọc theo quyền trước khi đưa cho AI).

---

## 6) Tiêu chí lên cấp tiếp theo (C5) — đo được

**[Đề xuất]** — các ngưỡng là điểm xuất phát của nhóm biên soạn, không phải chuẩn ngành; chỉnh theo mức rủi ro (bảng giá/bảo hành sai tốn tiền hơn FAQ nội bộ):
- Có bộ câu hỏi vàng ≥ 30 câu, trong đó có câu không-đáp-án, được người ngoài nhóm viết ít nhất một phần.
- recall@5 ≥ 0,85 trên phần câu có đáp án (với tài liệu có mức rủi ro cao: ≥ 0,95), và MRR được ghi lại làm mốc.
- Với câu hỏi cần mã/số/điều khoản: không có lỗi "trượt do bỏ dấu/tách từ" còn tái hiện được.
- Đã ghi tên + phiên bản công cụ tìm / mô hình embedding, ngày lập chỉ mục, quy trình cập nhật chỉ mục khi tài liệu đổi.
- Biết độ trễ trung bình mỗi câu hỏi và chi phí mỗi 1.000 câu (hoặc ghi "bằng 0 vì chạy cục bộ").
- Nếu điểm thấp: quyết định rõ nguyên nhân thuộc về *tài liệu thiếu nội dung* (sửa ở C2/C3; đây là nguyên nhân thất bại còn lại chủ yếu trong bài Airbnb **[Nguồn: Airbnb mục 7]**), hay *công cụ tìm* (ở lại C4).

---

## 7) Ví dụ cho SME Việt Nam

**Công ty phân phối điện máy nhỏ (30 nhân viên).** Tài liệu: bảng giá tháng (Excel → C2 thành text), chính sách bảo hành theo hãng (PDF), quy định đổi trả, nội quy nhân sự.

Bộ câu hỏi vàng mẫu (viết kiểu nhân viên thật):
| Câu hỏi | Khối đúng | Loại | Vì sao khó |
|---|---|---|---|
| "may giat 9kg gia bao nhieu" | `GIA-03` | tra cứu số | không dấu; "9kg" là token mã — BM25 mạnh, vector có thể trượt |
| "máy giặt hỏng động cơ năm thứ 5 có được bảo hành không" | `BH-01` | điều kiện | từ "năm thứ 5" ↔ "10 năm" khác chữ — cần ý nghĩa |
| "khách đổi trả trong mấy ngày" | `DT-02` | quy trình | "đổi trả" vs "đổi, trả hàng" — bigram/tách từ giúp |
| "xin nghỉ phép phải báo trước bao lâu" | `NQ-07` | nội quy | từ đồng nghĩa "báo trước" vs "xin trước" |
| "có bán máy lạnh Hãng X không" | *(không có đáp án)* | ngoài phạm vi | để dùng ở C5 |

Quy trình mẫu: (1) làm bảng điểm cơ sở bằng Ctrl+F; (2) BM25; (3) thêm embedding; (4) so; (5) chọn cấu hình rẻ nhất đạt ngưỡng ở mục 6. **Lưu ý:** bảng giá thay đổi hàng tháng → ghi ngày hiệu lực vào từng khối ngay từ C3 để C5 xử lý "tài liệu cũ".

Một đại lý bảo hiểm/công ty xây dựng có ~300 trang quy trình: có thể vừa khung "nhét thẳng vào ngữ cảnh" — thử và so với BM25 trước khi đầu tư embedding.

---

## 8) Tài liệu tham khảo

| # | Tiêu đề | URL | Loại | Truy cập | Tin cậy |
|---|---|---|---|---|---|
| 1 | Thakur et al., *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of IR Models* | https://arxiv.org/abs/2104.08663 | Bài báo (NeurIPS Datasets & Benchmarks; bản arXiv v4) | 2026-11-11 | Cao (đã đọc nội dung); dữ liệu tiếng Anh, mô hình đời 2021 |
| 2 | Chen et al., *M3-Embedding / BGE M3* | https://arxiv.org/abs/2402.03216 | Bài báo (ACL Findings 2024; bản v5 12/2025) | 2026-11-11 | Cao về số liệu; tác giả là nhóm làm ra mô hình |
| 3 | Wang et al., *Multilingual E5 Text Embeddings: A Technical Report* | https://arxiv.org/abs/2402.05672 | Báo cáo kỹ thuật | 2026-11-11 | Trung bình–cao; nhóm tác giả mô hình |
| 4 | Pham et al., *VN-MTEB: Vietnamese Massive Text Embedding Benchmark* | https://arxiv.org/abs/2507.21500 | Bài báo (arXiv; Findings EACL 2026 theo trang ACL Anthology) | 2026-11-11 | Trung bình–cao; dữ liệu dịch máy |
| 5 | Bako et al., Airbnb, *Frustratingly Easy Agentic RAG via Portable Skills* | https://arxiv.org/abs/2610.14428 | Bài báo/ca triển khai | 2026-11-11 | Trung bình–cao; mẫu nhỏ n=132, một bối cảnh |
| 6 | Anthropic, *Introducing Contextual Retrieval* | https://www.anthropic.com/news/contextual-retrieval | Blog kỹ thuật chính thức | 2026-11-11 | Trung bình (dữ liệu và mô hình của hãng; thao tác có thể đã đổi) |
| 7 | Liu et al., *Lost in the Middle* | https://arxiv.org/abs/2307.03172 | Bài báo (TACL) | 2026-11-11 | Cao; mô hình 2023 |
| 8 | SQLite, *FTS5 Extension* | https://www.sqlite.org/fts5.html | Tài liệu chính thức | 2026-11-11 | Cao (đọc ~100.000 ký tự đầu của ~172.000) |
| 9 | BAAI, *bge-m3* (model card) | https://huggingface.co/BAAI/bge-m3 | Thẻ mô hình | 2026-11-11 | Trung bình (thao tác/thông số có thể đổi) |
| 10 | underthesea | https://github.com/undertheseanlp/underthesea | Repo mã nguồn (README) | 2026-11-11 | Trung bình; chưa kiểm chất lượng tách từ |
| 11 | pyvi | https://github.com/trungtv/pyvi | Repo mã nguồn (README) | 2026-11-11 | Trung bình; chưa kiểm chất lượng |
| 12 | VinAI, PhoBERT | https://github.com/VinAIResearch/PhoBERT | Repo mã nguồn (README) | 2026-11-11 | Trung bình–cao cho yêu cầu tách từ của PhoBERT |
| 13 | Cormack, Clarke, Büttcher, *Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods* (SIGIR 2009) | https://research.google/pubs/pub36196/ | Bài báo ngắn (trang liệt kê) | 2026-11-11 | Cao về sự tồn tại; **nội dung PDF chưa đọc được** |

---

## 9) Chưa kiểm chứng / cần kiểm tra lại

1. **RRF và k=60:** công thức và con số 60 tôi lấy từ các bài giải thích thứ cấp (kết quả tìm kiếm); PDF gốc không trích được văn bản. Cần đọc bài gốc trước khi xuất bản.
2. **Tách từ có giúp BM25 tiếng Việt không?** Không có nguồn đã đọc cho kết luận này. Phải tự đo (bài 4.3). Ví dụ 4 câu của chúng tôi không đủ để kết luận.
3. **Bỏ dấu có hại/lợi bao nhiêu?** Không có số liệu nguồn; chỉ có cách làm và rủi ro đồng âm.
4. **Số liệu M3/mE5 trên MIRACL không gồm tiếng Việt** (bảng 1 M3; bảng 6 mE5 không có "vi"). Số tiếng Việt chỉ có ở VN-MTEB (dịch máy) và MKQA (chéo ngôn ngữ).
5. **Chi phí API embedding/rerank và giá đám mây:** chưa truy cập trang giá nào. RAM/tốc độ chạy cục bộ trên máy văn phòng: chưa có số đo nguồn.
6. **Tiền tố và giới hạn token của multilingual-e5:** trang Hugging Face không đọc được nội dung; chưa xác minh cú pháp `query:`/`passage:` và giới hạn độ dài.
7. **Thư viện vector (FAISS, Chroma, sqlite-vec...):** chưa đọc tài liệu; không khuyến nghị.
8. **Các con số Anthropic** (5,7% → 1,9%; $1,02/triệu token; 200.000 token) là của bài blog tại thời điểm đăng, trên bộ dữ liệu của hãng; phần tóm tắt tôi đọc qua công cụ tóm tắt trang, chưa đối chiếu từng chữ với bản gốc; giới hạn ngữ cảnh/tính năng hiện hành đã thay đổi theo thời gian.
9. **Ngưỡng "< 100 trang nhét thẳng", "recall@5 ≥ 0,85", "30–50 câu hỏi"** là đề xuất của nhóm, chưa được nghiên cứu nào xác nhận.
10. **Mô hình tiếng Việt chuyên biệt** (Vietnamese-Embedding, halong-embedding...): chỉ có điểm VN-MTEB của người đánh giá; chưa đọc thẻ mô hình/giấy phép.
11. **Code:** BM25 thuần Python và FTS5 **đã chạy thử** (scratchpad, 4 khối mẫu); đoạn RRF **chưa chạy thử**; đoạn nhúng vector **chưa viết/chưa chạy**.
12. Các mô hình/sản phẩm (Project/Gem/GPT, giới hạn tệp) đổi nhanh — đây là phần "thao tác"; phần "nguyên tắc" (đo trước, so sánh rẻ → đắt, tiền xử lý chữ Việt) bền hơn. Nên rà lại mỗi quý.
