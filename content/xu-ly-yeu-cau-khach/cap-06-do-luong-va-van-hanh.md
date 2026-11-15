# Cấp 6 (C6): Đo chất lượng và vận hành

> Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** / **[Đề xuất]**.
> Dùng lại: bộ ca mẫu, Wilson, kappa, LLM-as-judge ở `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`; log, phiên bản prompt, sửa-chạy lại-phát hành, trôi dạt, chi phí ở `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md`. File này viết phần riêng: **số đo của chăm sóc khách**, **đo theo quyết định**, **chạy lặp pass^k**, **mô phỏng khách**, **phát hành từng phần**.

!!! tip "Tóm tắt nhanh"
    Hệ thống trả lời khách đã chạy vài tuần, nhưng bạn chưa biết nó đang làm **tốt hơn hay tệ hơn người**, và mỗi lần sửa có làm hỏng chỗ khác không. Bài này dạy cách đo bằng một bảng số hằng tuần, chạy lại một bộ ca mẫu mỗi khi đổi gì đó, và chỉ bật tính năng mới cho một phạm vi nhỏ trước. Sau bài, bạn có báo cáo một trang mỗi tuần và một ngưỡng rõ ràng để biết khi nào phải quay lại bản cũ. Bạn **không cần biết lập trình** để làm phần chính, vì Google Sheet là đủ.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** chủ shop và người phụ trách hệ thống, đã chạy C1 đến C5 trên khách thật ít nhất vài tuần. Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Hệ thống chăm sóc khách của các cấp C1 đến C5 đã chạy trên khách thật ít nhất vài tuần, kèm bảng hàng đợi (Sheet) của C2 đến C5.
- Bộ ca mẫu (các tình huống khách có đáp án đúng) đã lập ở C0.
- Sổ ca của C0, nơi ghi lại các ca khách đã gặp.

**Sau cấp này bạn sẽ có:**
1. Bảng số đo tuần: tỉ lệ tự giải quyết (SSR) và SSR trừ ca mở lại, hài lòng, tỉ lệ sai chính sách, chuyển thừa/thiếu, thời gian phản hồi, chi phí mỗi ca. Mỗi tỉ lệ kèm n (số ca dùng để tính) và khoảng tin cậy (khoảng cho biết con số thật có thể nằm ở đâu, vì số ca ít thì con số dao động nhiều).
2. Bộ ca hồi quy (bộ ca dùng để kiểm xem sửa xong có làm hỏng chỗ cũ không) chạy 3 lần mỗi ca, báo pass^1 và pass^3, chạy lại mỗi khi đổi SOP (quy trình xử lý chuẩn), prompt (lời dặn AI), mô hình.
3. Quy trình phát hành từng phần: một ý định, một kênh, hoặc một khung giờ trước.
4. Ngưỡng dừng: số nào xấu đi thì quay lại bản cũ.

**Thứ bạn cầm đi được sau bài:** bảng số đo tuần; bảng so các phiên bản trên bộ ca hồi quy; danh sách 10 vai khách giả; bản ghi ngưỡng dừng cho từng lần phát hành; báo cáo tuần một trang.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

Câu hỏi: *"Hệ thống đang làm tốt hơn hay tệ hơn người, và sửa xong có hỏng chỗ khác không?"*

Lỗi thường gặp ở các cấp trước:
- Chỉ đếm "AI trả lời được bao nhiêu tin".
- Không biết khách có quay lại vì việc chưa xong không.
- Sửa prompt cho một ca rồi hỏng ca khác.
- Đổi mô hình vì "nghe nói tốt hơn".

!!! tip "Nói đơn giản"
    Một tin nhắn được AI trả lời chưa có nghĩa là khách được giúp xong. Muốn biết, bạn cần đo kết quả cuối (khách có quay lại không, có bị trả lời sai chính sách không), và cần một bộ ca cố định để chạy lại sau mỗi lần sửa.

## 3. Kiến thức nền

### 3.1 Số đo của chăm sóc khách [Nguồn + Đề xuất]

Bảng dưới liệt kê các số nên theo dõi. Mỗi số có một định nghĩa rõ, để tuần nào cũng đếm giống nhau.

| Số đo | Định nghĩa | Nguồn định nghĩa |
|---|---|---|
| SSR (tỉ lệ tự phục vụ) | Tỉ lệ phiên khách hoàn tất với agent (trợ lý AI tự xử lý) mà không xin người | Nubank 2609.30137, mục 3.3 |
| tNPS | % người cho điểm cao (promoter) trừ % người cho điểm thấp (detractor) trong khảo sát ngay sau tương tác | Nubank 2609.30137, mục 3.3 |
| CSAT | Khảo sát hài lòng sau tương tác, thang Likert (thang điểm kiểu 1 đến 5) | Nubank 2606.08867, mục 3.4.3 |
| SSR trừ mở lại | Ca "tự giải quyết" mà khách không quay lại cùng việc trong 7 ngày | **[Đề xuất]** |
| Tỉ lệ sai chính sách | Ca có quyết định hoặc câu nói trái SOP, do người rà mẫu | **[Đề xuất]** |
| Chuyển thừa / chuyển thiếu | Xem C5 | Nubank 2609.30137 (chuyển không cần thiết); **[Đề xuất]** (chuyển thiếu) |

**[Nguồn]** Nubank: SSR và tNPS đánh đổi nhau; đo tNPS riêng cho AI và cho người (2606.08867, mục 3.4.3).

**[Đề xuất]** Không bao giờ báo SSR một mình. Luôn báo cạnh tỉ lệ sai chính sách và chuyển thiếu.

!!! tip "Nói đơn giản"
    SSR cao nghe rất đẹp, nhưng AI có thể "tự giải quyết" bằng cách trả lời sai hoặc giữ khách lại không cho gặp người. Vì vậy hãy xem SSR cùng với số ca sai chính sách và số ca đáng lẽ phải chuyển cho người mà không chuyển. Ba số này đi cùng nhau mới có nghĩa.

### 3.2 Chạy lặp: pass^k

**[Nguồn]** τ-bench (arXiv 2406.12045): pass^k = xác suất cả k lần chạy độc lập của cùng một tác vụ đều thành công, trung bình trên các tác vụ; ước lượng không chệch là trung bình của C(c,k)/C(n,k), với c lần đúng trên n lần chạy. gpt-4o: pass^1 trên 60%, pass^8 dưới 25% ở miền bán lẻ.

**[Nguồn]** SEATauBench (arXiv 2606.28715): điểm tiếng Anh dự báo khá tốt chất lượng trung bình ở tiếng Việt (tương quan 0,90) nhưng dự báo kém độ ổn định qua nhiều lần chạy (tương quan ρ³ từ 0,49 tới 0,88 tùy ngôn ngữ).

**[Đề xuất]** Đo độ ổn định trên chính tiếng Việt của bạn.

!!! tip "Nói đơn giản"
    AI có thể trả lời đúng lần này và sai lần sau với cùng một câu hỏi. pass^1 là tỉ lệ đúng khi chạy **một lần**. pass^3 là tỉ lệ đúng khi **cả ba lần** chạy đều đúng. Khách hàng không quan tâm "trung bình đúng", họ cần lần nào cũng đúng, nên pass^3 thường thấp hơn pass^1 và là con số trung thực hơn.

### 3.3 Mô phỏng khách: hữu ích, có giới hạn

Mô phỏng khách nghĩa là nhờ một AI đóng vai khách để thử hệ thống của bạn, thay vì chờ khách thật.

**[Nguồn]** Nubank (arXiv 2609.30137) dùng khách giả do LLM (mô hình ngôn ngữ lớn, loại AI sinh chữ) đóng và trả lời công cụ bằng dữ liệu giả tại ranh giới công cụ, để sàng lọc phiên bản trước khi lên A/B thật (A/B là cách chạy hai phiên bản song song cho hai nhóm khách để so kết quả):
- Thứ tự điểm giữa các phiên bản trên mô phỏng khớp khá với thật (Pearson r = 0,74; Kendall τ = 0,67 trên 4 phiên bản). Hai chỉ số này đều đo mức độ "xếp hạng giống nhau".
- Hội thoại mô phỏng **dài hơn nhiều** thật: 22,4% hội thoại mô phỏng có tổng lời khách ≤50 từ, so với 89,0% ở thật.
- Bảy chuyên gia nhìn 50 hội thoại thật và 50 mô phỏng: nhận đúng 42/50 thật và 35/50 mô phỏng; 15 hội thoại mô phỏng bị tưởng là thật.
- Thời gian mỗi phiên bản giảm từ 21,2 ngày xuống 4,4 ngày (tỉ lệ 4,8), nhưng phần lớn công sức là tích hợp. Mô phỏng không thử backend (phần hệ thống phía sau như kho, đơn hàng), độ trễ, trạng thái lưu, tác dụng phụ.
- Họ vẫn quyết phát hành bằng A/B thật; mô phỏng chỉ để loại phiên bản kém.

**[Đề xuất]** Với SME: không cần công cụ mô phỏng riêng. Bản thu nhỏ: viết 10 "vai khách" (vội, bực, viết không dấu, hỏi nhiều ý, đưa mã đơn người khác) từ Sổ ca C0; dùng AI đóng vai với công cụ giả ở C3; chỉ dùng để tìm lỗi, không dùng làm số báo cáo.

!!! tip "Nói đơn giản"
    Khách do AI đóng thì tiện và rẻ, nhưng chưa giống khách thật: họ nói dài hơn và lịch sự hơn. Hãy dùng nó như một cách **tìm lỗi nhanh**, và không đưa kết quả đó vào báo cáo như số liệu thật.

### 3.4 Phát hành từng phần

**[Nguồn]** Nubank: mỗi phiên bản bắt đầu ở 1-5% lưu lượng, theo dõi SSR, tNPS, tỉ lệ chuyển, tỉ lệ lỗi (2606.08867, mục 4.5.1); đổi mô hình được coi như đổi prompt, phải chạy đủ bộ đánh giá (mục 4.5.3).

**[Đề xuất]** SME không có đủ lưu lượng để chia 1%. Chia theo **phạm vi**: một ý định (hỏi đơn), một kênh (Zalo OA, tài khoản chính thức của doanh nghiệp trên Zalo), một khung giờ (ngoài giờ), hoặc một nhân viên dùng trước. Với vài chục ca mỗi tuần, A/B chỉ phát hiện được chênh rất lớn (xem Wilson ở `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` mục 3.2).

!!! tip "Nói đơn giản"
    Đừng bật tính năng mới cho tất cả khách cùng lúc. Hãy bật cho một phạm vi nhỏ (ví dụ chỉ câu hỏi về đơn hàng, chỉ trên Zalo, chỉ ngoài giờ làm việc). Nếu có chuyện, ít khách bị ảnh hưởng và bạn dễ quay lại bản cũ.

### 3.5 SOP đổi là thay đổi lớn nhất

**[Nguồn]** BMO ESCROW: không có kho ca cũ thì sau 4 vòng cập nhật điểm trên ca cũ tụt từ 0,857 xuống 0,7; có kho này giữ khoảng 0,84 (`../nen-tang-bang-chung.md` mục 1.4).

**[Đề xuất]** Mỗi lần đổi chính sách (thêm khuyến mãi, đổi hạn đổi trả), tăng phiên bản SOP, cập nhật đáp án bộ ca, chạy lại toàn bộ. Quy trình chung: `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` bài 9.3.

!!! tip "Nói đơn giản"
    Khi chính sách của shop thay đổi, câu trả lời đúng của nhiều ca cũng thay đổi theo. Nếu không cập nhật đáp án và chạy lại bộ ca, hệ thống sẽ tiếp tục "nhớ" chính sách cũ mà bạn không hay biết.

## 4. Chuỗi bài nhỏ

Bảy bài thực hành dưới đây làm theo thứ tự. Mỗi bài ghi rõ việc cần làm, thứ bạn có sau bài, và lỗi hay gặp khi bản gốc có nêu.

### Bài 6.1: Nhật ký ca đủ để tính số
- **Việc cần làm:** mỗi ca ghi: mã, kênh, ý định, mức khẩn, tuyến (AI/người), lý do chuyển, quyết định, phiếu (nếu có), kết quả duyệt, thời điểm nhận/gửi, khách có quay lại cùng việc trong 7 ngày không, điểm khảo sát (nếu có), token và tiền (token là đơn vị tính lượng chữ AI đọc và viết, dùng để tính tiền). Che SĐT, địa chỉ. Khung log (nhật ký ghi lại từng việc hệ thống làm) chung: `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` bài 9.1.

### Bài 6.2: Khảo sát sau tương tác
- **Việc cần làm:** sau ca đóng, gửi một câu hỏi 1-5 hoặc 0-10. Gửi cả cho ca người xử lý để so. Ghi tỉ lệ trả lời: tỉ lệ thấp thì số hài lòng lệch về khách rất vui hoặc rất bực.
- **Lỗi hay gặp:** chỉ khảo sát ca AI; đổi câu hỏi giữa chừng.

### Bài 6.3: Rà mẫu sai chính sách hằng tuần
- **Việc cần làm:** lấy ngẫu nhiên 20-30 ca đã đóng. Người chấm theo bộ tiêu chí cố định: quyết định đúng SOP; câu nói không trái SOP; số liệu đúng; có chuyển khi phải chuyển. Nếu dùng LLM chấm (nhờ một AI chấm thay người), phải đối chiếu với người trước (`../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` bài 6.6). **[Nguồn]** Nubank: prompt chấm viết tay ở một bộ chấm còn kém đoán lớp đa số (68,88% so với 77,78%).

!!! tip "Nói đơn giản"
    "Đoán lớp đa số" nghĩa là lúc nào cũng đoán theo nhóm đông nhất. Câu nguồn trên cho thấy một AI chấm điểm được dặn bằng lời viết tay vẫn có thể kém cả cách đoán đơn giản ấy. Vì vậy đừng tin AI chấm điểm khi chưa so với người chấm.

### Bài 6.4: Bộ ca hồi quy chạy 3 lần
- **Việc cần làm:** bộ ca mẫu C0 cộng mọi ca lỗi thật đã gặp. Mỗi ca chạy 3 lần. Tính pass^1, pass^3. Ca chuyển từ đúng sang sai giữa hai phiên bản thì đọc từng ca.
- **Bạn có sau bài:** bảng so phiên bản.

### Bài 6.5: Vai khách giả
- **Việc cần làm:** 10 vai khách viết từ Sổ ca; AI đóng vai, công cụ giả trả các trạng thái lạ (C3). Đọc toàn bộ hội thoại tìm lỗi. Không báo số từ đây.

### Bài 6.6: Phát hành từng phần và ngưỡng dừng
- **Việc cần làm:** chọn phạm vi nhỏ (ví dụ chỉ ý định "hỏi đơn" trên Zalo OA). Viết trước: số nào, xấu tới mức nào thì quay lại bản cũ (ví dụ có 1 ca sai chính sách liên quan tiền; tỉ lệ mở lại tăng gấp đôi). Chạy 2 tuần. Quyết định mở rộng, giữ, hay lùi.

### Bài 6.7: Báo cáo tuần một trang
- **Việc cần làm:** 6 số ở mục 1 kèm n và khoảng tin cậy; 3 ca lỗi đáng chú ý; thay đổi đã làm; quyết định tuần tới. Người chủ quy trình ký.

## 5. Đường không code vs có code

Bài này có hai cách làm. Cách không code đủ dùng khi mới bắt đầu. Cách code nhẹ giúp máy tính số và chạy bộ ca hàng loạt thay bạn.

| | Không code | Code nhẹ |
|---|---|---|
| Nhật ký | Sheet hàng đợi C2-C5 | Bảng log tự ghi |
| Tính số | Công thức Sheet (COUNTIF) | Script tính tỉ lệ, Wilson, pass^k |
| Bộ hồi quy | Chạy tay qua Project/Gem, 3 lần | Script chạy hàng loạt qua API |

(COUNTIF là công thức đếm số ô thỏa một điều kiện trong Google Sheet hoặc Excel. Script là một đoạn chương trình ngắn. API là cổng để một chương trình khác gọi AI chạy tự động, không cần ngồi gõ tay. Project/Gem là tính năng lưu sẵn chỉ dẫn của Claude và Gemini.)

**Đoạn mã dưới đây làm gì?** Nó tính ra các con số của báo cáo tuần từ một danh sách ca giả: SSR thô, SSR trừ ca mở lại, số ca sai chính sách, khoảng tin cậy Wilson cho các tỉ lệ đó, và pass^1, pass^3 cho một bộ 20 ca chạy 3 lần. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

**Mã mẫu (đã chạy thử bằng `python -I -X utf8`, 2026-11-11; dữ liệu giả):**

```python
from math import comb, sqrt

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d; h = z*sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (round(c-h, 3), round(c+h, 3))

def pass_hat_k(ket_qua_moi_ca, k):
    """pass^k khong chech (tau-bench): trung binh C(c,k)/C(n,k) tren cac ca."""
    return sum(comb(sum(r), k) / comb(len(r), k) for r in ket_qua_moi_ca) / len(ket_qua_moi_ca)

phieu = ([{"tu": True,  "sai": False, "mo_lai": False}] * 52 +
         [{"tu": True,  "sai": True,  "mo_lai": True}]  * 3 +
         [{"tu": True,  "sai": False, "mo_lai": True}]  * 5 +
         [{"tu": False, "sai": False, "mo_lai": False}] * 40)
n = len(phieu)
ssr_that = sum(1 for p in phieu if p["tu"] and not p["mo_lai"])
sai = sum(p["sai"] for p in phieu)
print(f"SSR tho={sum(p['tu'] for p in phieu)/n:.0%}; SSR tru mo lai={ssr_that/n:.0%} {wilson(ssr_that, n)}")
print(f"Sai chinh sach={sai}/{n} {wilson(sai, n)}")
ca = [[1,1,1]]*14 + [[1,1,0]]*4 + [[1,0,0]]*2       # 20 ca x 3 lan
print(f"pass^1={pass_hat_k(ca,1):.2f}, pass^3={pass_hat_k(ca,3):.2f}")
```

Kết quả: SSR thô 60%, SSR trừ mở lại 52% (khoảng 95%: 42-62%); sai chính sách 3/100 (khoảng 1-8,5%); 0 lỗi trên 30 ca vẫn cho giới hạn trên khoảng 11%; pass^1 = 0,87 nhưng pass^3 = 0,70. Đọc: trên 100 ca, "SSR 60%" và "SSR 52%" đã khác nhau vì 8 ca khách quay lại. Và một bộ ca đạt 87% mỗi lần chỉ đạt 70% nếu đòi cả 3 lần đều đúng.

!!! tip "Nói đơn giản"
    Hai điều rút ra từ ví dụ trên. Một, cùng một hệ thống nhưng "SSR 60%" hay "SSR 52%" tùy bạn có tính cả ca khách quay lại hay không, nên phải tính cả. Hai, "không thấy lỗi nào trong 30 ca" chưa có nghĩa là tỉ lệ lỗi bằng 0, vì với số ca ít, tỉ lệ lỗi thật vẫn có thể lên tới khoảng 11%.

**Buộc chuyển sang code khi [Đề xuất]:** bộ hồi quy trên khoảng 30 ca × 3 lần chạy tay mất hơn nửa ngày; cần báo cáo tuần tự động; đổi mô hình hoặc SOP thường xuyên.

## 6. Tiêu chí "vận hành ổn định" và khi nào mở rộng [Đề xuất]

Không có cấp sau trong nhóm này. Một phạm vi được coi là vận hành ổn định khi, trong ≥4 tuần:
1. Có báo cáo tuần đủ 6 số kèm n và khoảng tin cậy.
2. Tỉ lệ sai chính sách liên quan tiền = 0 trong mẫu rà; tổng tỉ lệ sai chính sách không cao hơn ca người làm (rà cùng tiêu chí).
3. SSR trừ mở lại và hài lòng không thấp hơn trước khi bật, hoặc thấp hơn trong mức chủ shop ký chấp nhận.
4. Mọi thay đổi SOP/prompt/mô hình đều có lần chạy hồi quy, lưu kết quả.
5. Có người chủ quy trình và người thay thế.

Mở rộng sang ý định, kênh tiếp theo chỉ khi phạm vi hiện tại đạt các điều trên. Khi nào nên thuê làm hoặc dùng sản phẩm có sẵn: `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` bài 9.9.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa; số là giả]

Ba tình huống giả định để bạn dễ hình dung.

### 7.a Shop thời trang, phát hành "hỏi đơn" trên Zalo OA trước
Tuần 1-2 chỉ ý định `hoi_tinh_trang_don`, ngoài giờ. Ngưỡng dừng: 1 ca lộ đơn người khác, hoặc tỉ lệ mở lại vượt 2 lần mức trước. Báo cáo tuần cho thấy nhiều ca mở lại do trạng thái "giao thất bại" chưa có mẫu câu → thêm mẫu, tăng phiên bản, chạy hồi quy, rồi mới mở rộng sang `doi_tra`.

### 7.b Chuỗi 3 tiệm spa, so AI với nhân viên
Một tiệm dùng C1-C5 cho `doi_lich`, hai tiệm làm tay. So hài lòng và tỉ lệ khách bỏ lịch sau khi dời. Với vài chục ca mỗi tuần mỗi tiệm, chỉ kết luận được khi chênh rất lớn; ghi rõ điều này trong báo cáo.

### 7.c Nhà phân phối thiết bị văn phòng, đổi chính sách bảo hành
Chính sách bảo hành đổi từ 6 lên 12 tháng. Tăng SOP lên v3; sửa đáp án 8 ca trong bộ hồi quy; chạy lại toàn bộ 3 lần; 2 ca cũ về đổi trả bị hỏng do prompt còn câu "6 tháng" → sửa trước khi phát hành.

## 8. Tài liệu tham khảo

| Nguồn | Loại | Đọc | Tin cậy |
|---|---|---|---|
| Nubank, arXiv 2606.08867 | Bài báo KDD 2026, triển khai thật | Phần lớn toàn văn | Cao |
| Nubank, *Screen Before You Serve*, arXiv 2609.30137 | Bài báo, triển khai thật | Phần lớn toàn văn | Cao (một tổ chức, ngân hàng lớn) |
| τ-bench, arXiv 2406.12045 | Benchmark | Toàn văn phần chính | Cao về định nghĩa pass^k |
| SEATauBench, arXiv 2606.28715 | Benchmark có tiếng Việt | Phần chính | Trung bình-Cao |
| BMO ESCROW, arXiv 2608.01772 | Bài báo | Qua `../nen-tang-bang-chung.md` | Cao |

## 9. Chưa kiểm chứng

- Không có nguồn đo SSR, hài lòng, sai chính sách của agent chăm sóc khách tại SME Việt Nam.
- Cửa sổ 7 ngày cho "mở lại", 20-30 ca rà mỗi tuần, 4 tuần: đề xuất.
- Mô phỏng thu nhỏ bằng 10 vai khách chưa được so với hội thoại thật; Nubank cho thấy mô phỏng dài hơn thật rất nhiều.
- Tỉ lệ khách Việt trả lời khảo sát sau chat qua Zalo/Messenger: chưa có số liệu.
