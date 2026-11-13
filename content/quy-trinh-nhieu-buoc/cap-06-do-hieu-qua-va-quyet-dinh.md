# Q6 — Đo hiệu quả trước/sau và quyết định có đáng làm không

Ngày soạn: 2026-11-11. **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = thiết kế của nhóm soạn.

## 1) Mục tiêu và người đọc

**Người đọc:** chủ SME, người quyết định ngân sách; người phụ trách quy trình cần trình bày "có đáng không".

**Sau cấp này có:** bảng đo 4 tuần so với đo nền Q0 (thời gian, lỗi lọt, chi phí), tính hoàn vốn, và một biên bản quyết định: **làm tiếp / thu hẹp / quay về làm tay / dừng**. Có thể áp cho từng bước: bước AI, bước automation thường, và cả quy trình.

**Thứ chạy được độc lập:** bảng đo và công thức hoàn vốn. Dùng được cho mọi dự án tự động hóa, kể cả không có AI.

## 2) Câu hỏi cấp này trả lời / lỗi của cấp trước

**Câu hỏi:** "Sau khi tự động hóa, công ty thật sự được gì, mất gì, và có nên mở rộng không?"

**Lỗi thường gặp [Đề xuất, quan sát]:** chỉ khoe "AI trả lời trong 3 giây" mà quên thời gian người đọc lại và sửa; không tính giờ dựng và bảo trì; đo trên tuần đẹp nhất; so người giỏi làm tay với hệ thống mới trên ca dễ.

Phần đo thời gian, khoảng tin cậy khi n nhỏ, so A/B đã có ở `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` (bài 6.5, 6.7, 6.8). Phần vận hành dài hạn (log, phiên bản, trôi dạt, khi nào nâng cấp) ở `cap-09-van-hanh.md`. Cấp này thêm: **đo theo quy trình nhiều bước, đo cả công người duyệt, và quyết định theo từng bước**.

## 3) Kiến thức nền

### 3.1 Bằng chứng về đo năng suất thật [Nguồn]
- **Brynjolfsson, Li, Raymond (NBER WP 31161, qua `../thuc-trang-sme-viet-nam.md`):** 5.179 nhân viên CSKH, triển khai so le: số vấn đề giải quyết mỗi giờ +14% trung bình, +34% với người mới, gần như không đổi với người giỏi. Hàm ý: đo theo nhóm người, đo bằng chỉ số công việc (việc xong mỗi giờ), không bằng cảm nhận.
- **Dell'Acqua và cs. (HBS WP 24-013; chỉ đọc qua tóm tắt tìm kiếm):** 758 tư vấn viên BCG, chia ngẫu nhiên. Việc trong "vùng" AI làm tốt: thêm 12,2% việc, nhanh hơn 25,1%. Việc ngoài vùng: đúng ít hơn 19 điểm phần trăm. Hàm ý: cùng công cụ có thể làm hại ở một bước; phải đo lỗi theo từng loại việc.
- **READY (arXiv 2609.02095):** đánh giá hệ thống người + AI bằng ba thứ cùng lúc: độ tin cậy đạt được, gánh nặng người duyệt, chi phí vận hành; chọn chính sách trên một bộ ca rồi xác nhận trên bộ ca khác. Ví dụ trong hình 1 của bài: độ tin cậy 76%, 22% ca qua người, khoảng 5,5 USD/ca (ví dụ minh họa của bài).
- **TheAgentCompany:** báo cáo cả chi phí (khoảng 4,2 USD/việc với mô hình tốt nhất) và số bước, không chỉ tỷ lệ thành công. Gemini 2.0 Flash rẻ (dưới 1 USD) nhưng có lúc mắc vòng lặp.
- **MAP:** 74% hệ thống chạy thật dựa chủ yếu vào đánh giá của người; 75% không dùng benchmark chính thức mà dùng A/B hoặc phản hồi chuyên gia.
- **Samsung SDS (arXiv 2505.20733):** ví dụ điển hình về số "hiệu quả" khó dùng: ma trận nhầm lẫn đo thật trên 1.448 hóa đơn, nhưng "giảm 80-90% thời gian" là hiệu quả kỳ vọng dựa trên các ca tự động hóa nói chung, do nhóm nhà cung cấp viết.
- **thuc-trang-sme-viet-nam.md:** các số ROI ở Việt Nam (doanh thu +16%, kỳ vọng giảm 20% chi phí) là tự khai, nguồn có lợi ích; không có nghiên cứu đo trước/sau ở SME Việt Nam.

### 3.2 Đo gì cho quy trình nhiều bước [Đề xuất]

| Nhóm | Chỉ số | Ghi chú |
|---|---|---|
| Thời gian | Thời gian thao tác của người mỗi phiếu (gồm đọc lại, sửa, xử lý hàng lỗi); thời gian từ nhận đến xong (gồm chờ) | Tách hai loại: AI giảm thao tác, quy trình giảm chờ |
| Chất lượng | Lỗi lọt ra ngoài (khách/đối tác phát hiện); lỗi bị bắt ở cổng kiểm/người duyệt; phiếu trả lại | Lỗi lọt quan trọng nhất |
| Công người duyệt | % phiếu qua người; phút duyệt mỗi phiếu; % duyệt không sửa | Theo READY: đây là chi phí thật |
| Chi phí | Tiền API/tháng; tiền nền tảng (Make/Zapier/máy chủ n8n); giờ dựng; giờ bảo trì/tháng | Ghi giá tại ngày đo; không cố định |
| Độ tin cậy kỹ thuật | % lần chạy thành công; số mục hàng lỗi; số lần trùng | Từ Q5 |

### 3.3 Công thức hoàn vốn [Đề xuất]
`tiết kiệm/tháng = số phiếu/tháng × phút tiết kiệm/phiếu ÷ 60 × giá giờ công − chi phí vận hành/tháng`
`tháng hoàn vốn = chi phí dựng ÷ tiết kiệm/tháng` (nếu tiết kiệm ≤ 0 thì không bao giờ hoàn vốn).
Chi phí dựng gồm giờ của người trong công ty, không chỉ tiền thuê ngoài. "Phút tiết kiệm" phải tính trên thời gian người, gồm duyệt và xử lý lỗi.

## 4) Chuỗi bài nhỏ

### Bài Q6.1 — Chốt cách đo trước khi bật
- **Làm:** viết trước (trước khi xem số sau): chỉ số nào, đo thế nào, ngưỡng nào thì làm tiếp, ngưỡng nào thì dừng. Người ký: chủ quy trình + người quyết định ngân sách.
- **Sản phẩm:** một trang "kế hoạch đo". **Lỗi:** chọn chỉ số sau khi thấy số.

### Bài Q6.2 — Đo cùng cách như đo nền
- **Làm:** cùng loại phiếu, cùng người (hoặc cùng nhóm người mới/cũ), cùng cách ghi giờ như Q0.5. Nếu được, xen kẽ tuần có/không có hệ thống mới, hoặc chia ngẫu nhiên phiếu (`cap-06-danh-gia.md` bài 6.7 mục f).
- **Sản phẩm:** bảng 4 tuần.

### Bài Q6.3 — Đo theo bước
- **Làm:** với mỗi bước (Q1 automation, Q2 định tuyến, bước AI ở Q4), ghi thời gian người và lỗi riêng. Một bước AI có thể làm chậm cả quy trình nếu người duyệt mất nhiều phút hơn làm tay.
- **Sản phẩm:** bảng theo bước: giữ / thay bằng quy tắc / trả về người.

### Bài Q6.4 — Khoảng tin cậy, không chỉ trung bình
- **Làm:** báo trung vị và khoảng; khoảng tin cậy bootstrap cho chênh thời gian; Wilson cho tỷ lệ lỗi. Với n nhỏ, chỉ kết luận khi chênh rất rõ.
- **Sản phẩm:** bảng có khoảng tin cậy.

### Bài Q6.5 — Hoàn vốn
- **Làm:** công thức 3.3 với số đo thật; thử ba kịch bản số phiếu (thấp/vừa/cao).
- **Sản phẩm:** bảng hoàn vốn ba kịch bản.

### Bài Q6.6 — Biên bản quyết định
- **Làm:** một trang: số đo, so với ngưỡng đã ký ở Q6.1, rủi ro còn lại, quyết định, người chịu trách nhiệm, ngày xem lại. Chuyển sang vận hành theo `cap-09-van-hanh.md`.
- **Sản phẩm:** biên bản đã ký.

## 5) Đường không code vs có code; khi nào buộc chuyển

| | Không code | Có code |
|---|---|---|
| Ghi số | Sheet đo tay; xuất nhật ký từ nền tảng | Tổng hợp tự động từ log JSONL và bảng phiếu |
| Thống kê | Trung vị, min/max bằng công thức | Bootstrap, Wilson (mẫu dưới) |

**Buộc chuyển sang code [Đề xuất] khi:** số phiếu đủ lớn để đo tay bị bỏ; cần khoảng tin cậy; cần tổng hợp chi phí API từ log.

**Code mẫu (đã chạy thử 2026-11-11 bằng `python -I`; số liệu là GIẢ ĐỊNH).** Kết quả với 15 phiếu trước và 15 phiếu sau: trung vị 13 → 7 phút; khoảng tin cậy 95% của chênh trung bình khoảng 0,9 đến 8,5 phút (rộng); tỷ lệ lỗi lọt 2/15 (Wilson 3,7%-37,9%) và 1/15 (1,2%-29,8%), hai khoảng chồng nhau nên **không kết luận được lỗi giảm**. Hoàn vốn: 400 phiếu/tháng, tiết kiệm 5 phút/phiếu, giá giờ công 60.000 đồng, vận hành 1,5 triệu/tháng, dựng 8 triệu → 16 tháng; nếu chỉ 50 phiếu/tháng → không bao giờ hoàn vốn.

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

## 6) Tiêu chí "xong" và quyết định tiếp [Đề xuất]

Xong Q6 khi:
1. Có kế hoạch đo đã ký trước khi bật.
2. Có bảng 4 tuần (hoặc ≥100 phiếu) so với đo nền, có khoảng tin cậy.
3. Có bảng theo bước và bảng hoàn vốn ba kịch bản.
4. Có biên bản quyết định và ngày xem lại.

Gợi ý quyết định:

| Kết quả | Quyết định |
|---|---|
| Thời gian giảm rõ, lỗi lọt không tăng, hoàn vốn trong ngưỡng đã ký | Làm tiếp; chuyển vận hành (`cap-09`) |
| Thời gian giảm, lỗi lọt tăng | Thu hẹp: trả bước gây lỗi về người hoặc về quy tắc |
| Bước AI tốn công duyệt hơn làm tay | Bỏ bước AI, giữ phần automation thường |
| Không hoàn vốn ở kịch bản vừa | Dừng hoặc chỉ giữ Q1 |
| Không đủ số để kết luận | Đo tiếp có thời hạn; không mở rộng |

## 7) Ví dụ cho SME Việt Nam (giả định minh họa)

**a) Cửa hàng mỹ phẩm (chuỗi Q0-Q5).** Đo theo bước: Q1 (webhook Haravan → kho) giảm 2 phút/đơn, gần như không tốn chi phí thêm ngoài máy chủ n8n; Q2 (AI đọc tin Zalo) giảm thêm 1,5 phút/đơn nhưng nhân viên mới phải sửa 20% đơn nháp. Quyết định: giữ cả hai, đào tạo thêm người mới, xem lại sau 1 tháng. Nếu tỷ lệ sửa không giảm, trả bước đọc tin về người cho khách sỉ (tin dài, nhiều món).

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
