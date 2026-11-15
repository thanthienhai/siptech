# Q6 — Đo hiệu quả trước/sau và quyết định có đáng làm không

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

!!! tip "Tóm tắt nhanh"
    Tự động hóa xong, câu hỏi khó nhất là: công ty thật sự được gì, mất gì, và có đáng làm tiếp không? Bài này dạy bạn **đo** (thời gian, lỗi lọt ra ngoài, chi phí) rồi so với số đo nền ban đầu (Q0), **tính tháng hoàn vốn** bằng một công thức đơn giản, và ghi lại thành **một biên bản quyết định**: làm tiếp, thu hẹp, quay về làm tay, hoặc dừng. Bạn không cần biết lập trình; một bảng tính là đủ để bắt đầu.

## 1) Mục tiêu và người đọc

**Bài này dành cho ai:** chủ SME (doanh nghiệp nhỏ và vừa), người quyết định ngân sách; hoặc người phụ trách một quy trình và cần trình bày với cấp trên rằng "việc này có đáng không". Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Số đo nền của quy trình lúc chưa tự động hóa (bài này gọi là "đo nền Q0", và cách ghi giờ ở bài Q0.5). Mọi so sánh trước/sau đều dựa vào đây.
- Một bảng tính (Sheet) để ghi số đo bằng tay, hoặc bản xuất nhật ký từ nền tảng bạn đang dùng.
- Một quy trình đã được bật chạy thử (có hệ thống mới) để có số "sau".

**Sau bài này bạn sẽ có:**
1. Bảng đo 4 tuần, đặt cạnh số đo nền Q0: thời gian, lỗi lọt ra ngoài, chi phí.
2. Phép tính hoàn vốn (bao lâu thì tiền bỏ ra được lấy lại).
3. Một biên bản quyết định với bốn lựa chọn: **làm tiếp / thu hẹp / quay về làm tay / dừng**.
4. Cách áp dụng riêng cho từng bước: bước dùng AI, bước automation thường (tự động hóa theo quy tắc cố định, không có AI), và cả quy trình.

**Thứ bạn cầm đi được:** bảng đo và công thức hoàn vốn. Hai thứ này dùng được độc lập, cho mọi dự án tự động hóa, kể cả dự án không có AI.

## 2) Câu hỏi cấp này trả lời / lỗi của cấp trước

**Câu hỏi:** "Sau khi tự động hóa, công ty thật sự được gì, mất gì, và có nên mở rộng không?"

**Lỗi thường gặp [Đề xuất, quan sát]:**
- Chỉ khoe "AI trả lời trong 3 giây" mà quên thời gian người phải đọc lại và sửa.
- Không tính giờ dựng hệ thống và giờ bảo trì.
- Đo vào tuần đẹp nhất.
- So người giỏi làm tay với hệ thống mới trên các ca dễ.

Một số phần đã có ở nơi khác, bài này không viết lại:
- Phần đo thời gian, khoảng tin cậy khi n nhỏ (n là số mẫu đo được), và so A/B (chia hai nhóm để so sánh) nằm ở `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` (bài 6.5, 6.7, 6.8).
- Phần vận hành dài hạn (log là nhật ký ghi lại các lần chạy, phiên bản, trôi dạt là khi kết quả dần lệch đi theo thời gian, khi nào nên nâng cấp) nằm ở `cap-09-van-hanh.md`.

Điều bài này thêm vào: **đo theo quy trình nhiều bước, đo cả công của người duyệt, và ra quyết định theo từng bước**.

## 3) Kiến thức nền

### 3.1 Bằng chứng về đo năng suất thật [Nguồn]

Phần này điểm qua các nghiên cứu và báo cáo đã đo năng suất khi dùng AI. Mục đích là giúp bạn thấy người ta đo **cái gì** và **đo thế nào**, từ đó học cách đo cho công ty mình.

- **Brynjolfsson, Li, Raymond (NBER WP 31161, qua `../thuc-trang-sme-viet-nam.md`):** nghiên cứu trên 5.179 nhân viên CSKH (chăm sóc khách hàng), cho từng nhóm dùng công cụ vào các thời điểm so le nhau. Kết quả: số vấn đề giải quyết mỗi giờ tăng +14% trung bình, +34% với người mới, và gần như không đổi với người giỏi. Hàm ý: hãy đo theo từng nhóm người, và đo bằng chỉ số công việc (việc xong mỗi giờ), không đo bằng cảm nhận.
- **Dell'Acqua và cs. (HBS WP 24-013; chỉ đọc qua tóm tắt tìm kiếm):** 758 tư vấn viên BCG, được chia ngẫu nhiên. Với việc nằm trong "vùng" AI làm tốt: làm thêm 12,2% việc, nhanh hơn 25,1%. Với việc nằm ngoài vùng: kết quả đúng ít hơn 19 điểm phần trăm. Hàm ý: cùng một công cụ có thể làm hại ở một bước; vì vậy phải đo lỗi theo từng loại việc.
- **READY (arXiv 2609.02095):** đánh giá hệ thống "người + AI" bằng ba thứ cùng lúc: độ tin cậy đạt được, gánh nặng của người duyệt, và chi phí vận hành. Cách làm là chọn chính sách trên một bộ ca, rồi xác nhận lại trên một bộ ca khác. Ví dụ trong hình 1 của bài: độ tin cậy 76%, 22% ca phải qua người, khoảng 5,5 USD/ca (đây là ví dụ minh họa của bài).
- **TheAgentCompany:** báo cáo cả chi phí (khoảng 4,2 USD/việc với mô hình tốt nhất) và số bước, không chỉ tỷ lệ thành công. Gemini 2.0 Flash rẻ (dưới 1 USD) nhưng có lúc mắc vòng lặp (cứ lặp đi lặp lại một việc mà không xong).
- **MAP:** 74% hệ thống chạy thật dựa chủ yếu vào đánh giá của người; 75% không dùng benchmark chính thức (bộ đề thi chuẩn để chấm điểm mô hình) mà dùng A/B hoặc phản hồi chuyên gia.
- **Samsung SDS (arXiv 2505.20733):** ví dụ điển hình về một con số "hiệu quả" khó dùng. Ma trận nhầm lẫn (bảng đếm đúng/sai của từng loại) được đo thật trên 1.448 hóa đơn, nhưng câu "giảm 80-90% thời gian" chỉ là hiệu quả kỳ vọng, dựa trên các ca tự động hóa nói chung, và do nhóm của nhà cung cấp viết.
- **thuc-trang-sme-viet-nam.md:** các số ROI (tỷ lệ lãi so với vốn bỏ ra) ở Việt Nam, như doanh thu +16% hay kỳ vọng giảm 20% chi phí, đều là tự khai và từ nguồn có lợi ích liên quan. Không có nghiên cứu nào đo trước/sau ở SME Việt Nam.

!!! tip "Nói đơn giản"
    Đừng tin con số nào chỉ nói "nhanh hơn" mà không nói đo thế nào. Số đáng tin là số đo việc xong mỗi giờ, tính cả công người duyệt, trên cả ca dễ lẫn ca khó. Số do nhà cung cấp tự viết thì chỉ nên coi là gợi ý.

### 3.2 Đo gì cho quy trình nhiều bước [Đề xuất]

Bảng dưới liệt kê năm nhóm chỉ số nên đo. "Phiếu" là một đơn vị công việc đi qua quy trình (một đơn hàng, một đề nghị thanh toán...).

| Nhóm | Chỉ số | Ghi chú |
|---|---|---|
| Thời gian | Thời gian thao tác của người mỗi phiếu (gồm đọc lại, sửa, xử lý hàng lỗi); thời gian từ nhận đến xong (gồm chờ) | Tách hai loại: AI giảm thao tác, quy trình giảm chờ |
| Chất lượng | Lỗi lọt ra ngoài (khách/đối tác phát hiện); lỗi bị bắt ở cổng kiểm/người duyệt; phiếu trả lại | Lỗi lọt quan trọng nhất |
| Công người duyệt | % phiếu qua người; phút duyệt mỗi phiếu; % duyệt không sửa | Theo READY: đây là chi phí thật |
| Chi phí | Tiền API/tháng; tiền nền tảng (Make/Zapier/máy chủ n8n); giờ dựng; giờ bảo trì/tháng | Ghi giá tại ngày đo; không cố định |
| Độ tin cậy kỹ thuật | % lần chạy thành công; số mục hàng lỗi; số lần trùng | Từ Q5 |

(API là cổng để một phần mềm gọi dịch vụ AI; tiền API là tiền trả cho mỗi lần gọi. Make, Zapier, n8n là các nền tảng nối các việc lại thành một quy trình tự chạy.)

!!! tip "Nói đơn giản"
    Hai câu hỏi quan trọng nhất: "Người mất bao nhiêu phút cho mỗi phiếu, tính cả việc đọc lại và sửa?" và "Có lỗi nào lọt ra tới khách không?". Các chỉ số còn lại giúp bạn hiểu **vì sao** hai số đó thay đổi.

### 3.3 Công thức hoàn vốn [Đề xuất]

Hai công thức dưới đây cho biết mỗi tháng tiết kiệm được bao nhiêu và bao lâu thì lấy lại vốn:

`tiết kiệm/tháng = số phiếu/tháng × phút tiết kiệm/phiếu ÷ 60 × giá giờ công − chi phí vận hành/tháng`

`tháng hoàn vốn = chi phí dựng ÷ tiết kiệm/tháng` (nếu tiết kiệm ≤ 0 thì không bao giờ hoàn vốn).

Hai điều cần nhớ khi điền số:
- Chi phí dựng gồm giờ của người trong công ty, không chỉ tiền thuê ngoài.
- "Phút tiết kiệm" phải tính trên thời gian của người, gồm cả thời gian duyệt và xử lý lỗi.

!!! tip "Nói đơn giản"
    Lấy số tiền công tiết kiệm được mỗi tháng, trừ đi tiền chạy hệ thống mỗi tháng. Phần còn lại là "lãi" hằng tháng. Chia tiền đã bỏ ra để dựng cho phần lãi đó, bạn được số tháng hoàn vốn. Nếu phần lãi không dương thì hệ thống không bao giờ tự trả được vốn.

## 4) Chuỗi bài nhỏ

Sáu bài thực hành dưới đây làm theo thứ tự. Mỗi bài có việc cần làm và thứ bạn có sau bài.

### Bài Q6.1 — Chốt cách đo trước khi bật
- **Việc cần làm:** viết ra trước (trước khi xem số sau): chỉ số nào, đo thế nào, ngưỡng nào thì làm tiếp, ngưỡng nào thì dừng. Người ký: chủ quy trình và người quyết định ngân sách.
- **Bạn có sau bài:** một trang "kế hoạch đo".
- **Lỗi hay gặp:** chọn chỉ số sau khi đã thấy số.

### Bài Q6.2 — Đo cùng cách như đo nền
- **Việc cần làm:** dùng cùng loại phiếu, cùng người (hoặc cùng nhóm người mới/cũ), cùng cách ghi giờ như ở Q0.5. Nếu được, hãy xen kẽ tuần có và tuần không có hệ thống mới, hoặc chia ngẫu nhiên các phiếu (xem `cap-06-danh-gia.md` bài 6.7 mục f).
- **Bạn có sau bài:** bảng 4 tuần.

### Bài Q6.3 — Đo theo bước
- **Việc cần làm:** với mỗi bước (Q1 automation, Q2 định tuyến, bước AI ở Q4), ghi riêng thời gian của người và lỗi. Một bước AI có thể làm chậm cả quy trình nếu người duyệt mất nhiều phút hơn so với làm tay.
- **Bạn có sau bài:** bảng theo bước, với kết luận cho từng bước: giữ / thay bằng quy tắc / trả về người.

### Bài Q6.4 — Khoảng tin cậy, không chỉ trung bình
- **Việc cần làm:** báo trung vị (số nằm giữa khi xếp các số đo từ nhỏ đến lớn) và khoảng giá trị, thay vì chỉ trung bình. Dùng khoảng tin cậy bootstrap (xáo trộn và lấy mẫu lại nhiều lần từ chính dữ liệu của bạn) cho chênh lệch thời gian, và khoảng Wilson (một cách tính khoảng cho tỷ lệ, hợp với mẫu nhỏ) cho tỷ lệ lỗi. Với n nhỏ, chỉ kết luận khi chênh lệch rất rõ.
- **Bạn có sau bài:** bảng có khoảng tin cậy.

!!! tip "Nói đơn giản"
    Khoảng tin cậy cho bạn biết "con số thật có thể nằm trong khoảng nào". Khoảng càng rộng thì càng chưa nên kết luận. Nếu hai khoảng chồng lên nhau, đừng vội nói bên nào tốt hơn.

### Bài Q6.5 — Hoàn vốn
- **Việc cần làm:** dùng công thức ở mục 3.3 với số đo thật; thử ba kịch bản về số phiếu (thấp / vừa / cao).
- **Bạn có sau bài:** bảng hoàn vốn ba kịch bản.

### Bài Q6.6 — Biên bản quyết định
- **Việc cần làm:** viết một trang gồm: số đo, so với ngưỡng đã ký ở Q6.1, rủi ro còn lại, quyết định, người chịu trách nhiệm, ngày xem lại. Sau đó chuyển sang vận hành theo `cap-09-van-hanh.md`.
- **Bạn có sau bài:** biên bản đã ký.

## 5) Đường không code vs có code; khi nào buộc chuyển

Bài này có hai cách làm. Cách không code đủ dùng khi số phiếu còn ít. Cách có code giúp máy tự tổng hợp thay cho người.

| | Không code | Có code |
|---|---|---|
| Ghi số | Sheet đo tay; xuất nhật ký từ nền tảng | Tổng hợp tự động từ log JSONL và bảng phiếu |
| Thống kê | Trung vị, min/max bằng công thức | Bootstrap, Wilson (mẫu dưới) |

(JSONL là một kiểu tệp nhật ký, mỗi dòng ghi một lần chạy theo khung rõ ràng để máy đọc được. "Mẫu dưới" nghĩa là đoạn mã mẫu ngay bên dưới. Min/max là giá trị nhỏ nhất và lớn nhất.)

**Buộc chuyển sang code [Đề xuất] khi:**
- số phiếu đủ lớn đến mức đo tay bị bỏ dở;
- cần khoảng tin cậy;
- cần tổng hợp chi phí API từ log.

**Kết quả của code mẫu (đã chạy thử 2026-11-11 bằng `python -I`; số liệu là GIẢ ĐỊNH).** Với 15 phiếu trước và 15 phiếu sau:
- Trung vị thời gian: 13 → 7 phút.
- Khoảng tin cậy 95% của chênh lệch trung bình: khoảng 0,9 đến 8,5 phút (rộng).
- Tỷ lệ lỗi lọt: 2/15 (Wilson 3,7%-37,9%) và 1/15 (1,2%-29,8%). Hai khoảng chồng nhau nên **không kết luận được lỗi giảm**.
- Hoàn vốn: 400 phiếu/tháng, tiết kiệm 5 phút/phiếu, giá giờ công 60.000 đồng, vận hành 1,5 triệu/tháng, dựng 8 triệu → 16 tháng; nếu chỉ 50 phiếu/tháng → không bao giờ hoàn vốn.

**Đoạn mã dưới đây làm gì?** Nó gồm ba hàm nhỏ. Hàm đầu tính khoảng Wilson cho một tỷ lệ lỗi. Hàm thứ hai tính khoảng tin cậy cho chênh lệch thời gian trước và sau, bằng cách lấy mẫu lại 5.000 lần. Hàm thứ ba tính số tháng hoàn vốn theo công thức ở mục 3.3. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết nó làm gì, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi số phiếu của bạn đủ lớn.

```python
import math, random, statistics as st

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return round(c - h, 3), round(c + h, 3)

def bootstrap_chenh(a, b, lan=5000, seed=1):
    r = random.Random(seed); ds = sorted(st.mean(r.choices(a, k=len(a))) - st.mean(r.choices(b, k=len(b)))
                                        for _ in range(lan))
    return round(ds[int(.025*lan)], 1), round(ds[int(.975*lan)], 1)

def hoa_von(phieu_thang, phut_tk, gia_gio, chi_phi_thang, chi_phi_dung):
    tiet_kiem = phieu_thang * phut_tk / 60 * gia_gio - chi_phi_thang
    return None if tiet_kiem <= 0 else round(chi_phi_dung / tiet_kiem, 1)
```

Bài học từ ví dụ giả định: một quy trình nhanh gấp đôi vẫn có thể mất hơn một năm mới hoàn vốn, và không hoàn vốn nếu số phiếu ít. Đó là lý do Q1 (automation thường, rẻ) thường đáng làm trước Q2-Q4.

!!! tip "Nói đơn giản"
    Nhanh gấp đôi chưa chắc đã có lãi. Số phiếu mỗi tháng quyết định rất nhiều: ít phiếu thì tiền tiết kiệm nhỏ, không đủ trả tiền chạy hệ thống. Vì vậy hãy làm phần rẻ và chắc (automation thường) trước, rồi mới cân nhắc phần có AI.

## 6) Tiêu chí "xong" và quyết định tiếp [Đề xuất]

Bạn đã xong Q6 khi có đủ:
1. Kế hoạch đo đã ký trước khi bật.
2. Bảng 4 tuần (hoặc ≥100 phiếu) so với đo nền, có khoảng tin cậy.
3. Bảng theo bước và bảng hoàn vốn ba kịch bản.
4. Biên bản quyết định và ngày xem lại.

Gợi ý quyết định:

| Kết quả | Quyết định |
|---|---|
| Thời gian giảm rõ, lỗi lọt không tăng, hoàn vốn trong ngưỡng đã ký | Làm tiếp; chuyển vận hành (`cap-09`) |
| Thời gian giảm, lỗi lọt tăng | Thu hẹp: trả bước gây lỗi về người hoặc về quy tắc |
| Bước AI tốn công duyệt hơn làm tay | Bỏ bước AI, giữ phần automation thường |
| Không hoàn vốn ở kịch bản vừa | Dừng hoặc chỉ giữ Q1 |
| Không đủ số để kết luận | Đo tiếp có thời hạn; không mở rộng |

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

Ba tình huống dưới đây là giả định để bạn dễ hình dung, không phải số đo thật.

**a) Cửa hàng mỹ phẩm (chuỗi Q0-Q5).** Đo theo bước:
- Q1 (webhook Haravan → kho; webhook là cách một phần mềm tự báo tin cho phần mềm khác khi có đơn mới) giảm 2 phút/đơn, gần như không tốn chi phí thêm ngoài máy chủ n8n.
- Q2 (AI đọc tin Zalo) giảm thêm 1,5 phút/đơn, nhưng nhân viên mới phải sửa 20% đơn nháp.

Quyết định: giữ cả hai, đào tạo thêm người mới, xem lại sau 1 tháng. Nếu tỷ lệ sửa không giảm, trả bước đọc tin về người cho khách sỉ (tin dài, nhiều món).

**b) Công ty xây lắp (đề nghị thanh toán).** Thời gian từ nộp đến chi: trung vị 4 → 2 ngày, gần hết nhờ biểu mẫu, định tuyến, nhắc hạn (Q1, không AI). Bước AI trích trường hóa đơn tiết kiệm khoảng 1 phút/phiếu với 60 phiếu/tháng: tiền API nhỏ, nhưng tiết kiệm cũng nhỏ. Quyết định: giữ Q1; bước AI để tùy chọn, không mở rộng.

**c) Công ty dịch vụ kế toán (báo cáo công nợ, Q3).** Báo cáo cho 40 khách từ 2 ngày công/tháng còn nửa ngày; 0 số không nguồn lọt qua duyệt trong 4 tuần; một lần dữ liệu MISA xuất thiếu do lỗi đồng bộ, bộ kiểm dữ liệu bắt được. Quyết định: làm tiếp, thêm đối chiếu số dòng với MISA.

## 8) Tài liệu tham khảo

| Nguồn | Loại | Mức đọc | Tin cậy |
|---|---|---|---|
| Brynjolfsson, Li, Raymond, NBER WP 31161 | Nghiên cứu có đối chứng (so le) | Trang tóm tắt (qua file nền) | Cao cho bối cảnh đó |
| Dell'Acqua và cs., HBS WP 24-013, SSRN 4573321 (https://mitsloan.mit.edu/sites/default/files/2023-10/SSRN-id4573321.pdf) | Thử nghiệm ngẫu nhiên đăng ký trước | **Chỉ qua tóm tắt tìm kiếm** | Cao về thiết kế; số cần đối chiếu |
| READY, arXiv 2609.02095 | Khung đánh giá | Tóm tắt + mục chính | Trung bình-cao |
| TheAgentCompany, arXiv 2412.14161 | Benchmark | Toàn văn mục kết quả | Cao cho giả lập |
| MAP, arXiv 2512.04123 | Khảo sát | Nhóm trước đọc toàn văn | Cao, có thiên lệch mẫu |
| Samsung SDS, arXiv 2505.20733 | Nghiên cứu ca của nhà cung cấp | Toàn văn mục 5 | Thấp cho số hiệu quả |

## 9) Chưa kiểm chứng

- Không có nghiên cứu đo trước/sau tự động hóa quy trình ở SME Việt Nam. Mọi số ở mục 5 và 7 là giả định.
- Số Dell'Acqua chưa đối chiếu bản gốc; số Brynjolfsson lấy từ trang tóm tắt NBER.
- Giá giờ công 60.000 đồng, chi phí vận hành 1,5 triệu, chi phí dựng 8 triệu là giả định minh họa, không phải số thị trường.
- Ngưỡng quyết định ở mục 6 là đề xuất; mỗi công ty tự đặt và ký trước khi đo.
