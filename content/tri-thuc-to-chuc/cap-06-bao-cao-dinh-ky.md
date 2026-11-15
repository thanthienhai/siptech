# Cấp 6 (C6): Báo cáo định kỳ từ nhiều nguồn

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác.
> Dùng lại: gọi API, JSON có cấu trúc, chi phí (`../rag-tra-cuu-tai-lieu/cap-01-goi-api.md`); quy trình nhiều bước có cổng kiểm và điểm duyệt (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md`). Nhóm `../quy-trinh-nhieu-buoc/` có thể đi sâu phần tự động hóa; cấp này lo phần **nội dung đúng** của báo cáo.

!!! tip "Tóm tắt nhanh"
    Làm báo cáo tuần hoặc tháng thường mất nửa buổi để gom số từ nhiều nơi. Nhờ AI làm thì nhanh, nhưng AI hay cộng sai, tính phần trăm sai, hoặc đưa vào con số không có trong dữ liệu. Bài này dạy một cách làm đơn giản: **công thức tính số, AI chỉ viết lời, rồi có bước kiểm xem mọi con số trong lời văn có nằm trong bảng số hay không**. Sau bài, bạn có một quy trình báo cáo mà người duyệt ký trước khi gửi.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** chủ doanh nghiệp, trưởng phòng phải làm báo cáo tuần hoặc tháng; kế toán, admin. Bạn **không cần biết lập trình** để làm theo cách 1 ở mục 5.

**Bạn cần chuẩn bị:**
- Các file số liệu mà báo cáo của bạn đang dùng, ví dụ file xuất từ sàn bán hàng hoặc phần mềm bán hàng, file Excel kho.
- Biên bản họp, sổ việc, hàng đợi mâu thuẫn tài liệu, bài học đã tích lũy ở các cấp trước (C0, C4, C5).
- Một bảng tính Google Sheet hoặc Excel để tính số.
- Một tài khoản có thể tạo Project (Claude) hoặc Gem (Gemini). Đây là tính năng cho bạn lưu sẵn chỉ dẫn để dùng lại mỗi kỳ.

**Sau bài này, bạn sẽ có:**
1. Mỗi báo cáo định kỳ có **định nghĩa chỉ số** bằng văn bản (công thức, nguồn, chủ).
2. **Con số do công thức hoặc code tính**, không do AI tính.
3. AI chỉ viết phần lời từ bảng số đã tính và từ biên bản, sổ việc, hàng đợi (C0, C4, C5).
4. **Code kiểm mọi con số** trong phần lời phải có trong bảng số; phần nhận định phải có nguồn. (Code là đoạn chương trình ngắn do máy chạy; nếu bạn dùng cách không code thì người đọc dò từng số.)
5. Người duyệt ký trước khi gửi.

**Thứ bạn cầm đi được sau bài:** trang định nghĩa chỉ số; bảng tính số; Project hoặc script viết lời; `bao_cao.py`; kho báo cáo theo kỳ.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Mỗi thứ Hai mất nửa buổi gom số từ Shopee, Excel kho, Zalo nhóm bán hàng để viết báo cáo. AI làm được không mà không bịa số?"*

Ở các cấp C0 đến C5, bạn đã tạo ra nhiều nguồn tri thức: biên bản, sổ việc, bài học, hàng đợi mâu thuẫn. Báo cáo định kỳ là nơi gom chúng lại cho người ra quyết định.

Khi dùng AI "vô tội vạ" **[Đề xuất, quan sát]**, chuyện thường xảy ra như sau. Bạn dán file Excel vào khung chat, rồi nhờ "phân tích và viết báo cáo". AI cộng sai, tính phần trăm sai, hoặc đưa ra con số không có trong dữ liệu. Vì lời văn đọc rất trôi chảy nên ít ai kiểm lại.

## 3. Kiến thức nền

### 3.1 Bằng chứng [Nguồn]

- **Microsoft** (arXiv 2608.20392): trong các lỗi khi AI trả lời câu hỏi về cuộc họp, nhóm "bịa con số, danh sách đủ" chiếm 16,9%, đứng thứ hai. Báo cáo có nhiều con số hơn biên bản, nên rủi ro này càng đáng lo.
- **FRAME** (arXiv 2509.15901): trích sự kiện trước, viết sau, giảm bịa nội dung so với một prompt viết thẳng (chi tiết ở C0 mục 3.2). Prompt là đoạn chỉ dẫn bạn gõ cho AI.
- **Khảo sát Anthropic "State of AI Agents 2026"** (qua `../nen-tang-bang-chung.md`, thứ cấp, nhà cung cấp): phân tích dữ liệu/báo cáo là ứng dụng phi lập trình được nêu nhiều nhất (60%). Con số này cho thấy nhu cầu, không cho thấy chất lượng.

!!! tip "Nói đơn giản"
    Bằng chứng cho thấy hai điều. Một, AI hay sai nhất ở chỗ con số. Hai, bảo AI làm từng bước (trích trước, viết sau) thì ít bịa hơn là bảo viết một mạch. Còn việc nhiều người dùng AI để làm báo cáo chỉ nói lên nhu cầu, không chứng minh AI làm tốt.

### 3.2 Nguyên tắc [Đề xuất]

1. **Tách tính và viết.** Công thức Sheet hoặc code tính mọi con số, kể cả phần trăm thay đổi. AI nhận bảng số đã tính.
2. **Mọi con số trong lời văn phải nằm trong bảng.** Kiểm bằng code, không bằng lời dặn.
3. **Mọi nhận định định tính phải có nguồn** (biên bản ngày nào, bài học mã nào). "Định tính" là những nhận xét bằng lời, như nguyên nhân hay đánh giá, không phải con số.
4. **Báo cáo là tri thức.** Lưu theo kỳ, có phiên bản; kỳ sau so với kỳ trước.

!!! tip "Nói đơn giản"
    Hãy coi AI như một người viết lời bình rất nhanh nhưng không đáng tin về tính nhẩm. Con số do máy tính (công thức) làm, AI chỉ được dùng lại đúng những số đó, và mọi lời giải thích phải chỉ ra được nguồn.

## 4. Chuỗi bài nhỏ

Bảy bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và (nếu có) lỗi hay gặp để tránh.

### Bài C6.1: Định nghĩa báo cáo
- **Việc cần làm:** ghi ra những điều sau. Ai đọc báo cáo. Họ quyết định gì từ báo cáo. 5-8 chỉ số; với mỗi chỉ số ghi: tên, công thức, nguồn dữ liệu, chủ dữ liệu (người chịu trách nhiệm về số đó), kỳ. Ví dụ: "Doanh thu thuần tuần = tổng tiền đơn đã giao thành công trừ hoàn, theo file xuất từ sàn, chủ: trưởng bán hàng online".
- **Bạn có sau bài:** trang định nghĩa, đăng ký vào sổ C3.
- **Lỗi hay gặp:** chỉ số không có công thức nên mỗi kỳ mỗi người tính một kiểu.

### Bài C6.2: Gom nguồn
- **Việc cần làm:** liệt kê nguồn: file xuất từ sàn hoặc phần mềm bán hàng, Excel kho, sổ việc (C0), hàng đợi mâu thuẫn (C4), bài học (C5). Mỗi nguồn ghi: định dạng, ai xuất, khi nào. Ưu tiên nguồn có file; tin nhắn Zalo chỉ dùng cho phần định tính, và phải có trích dẫn.
- **Bạn có sau bài:** bảng nguồn.

### Bài C6.3: Bảng số do công thức tính
- **Việc cần làm:**
  - Đường không code: dùng một Sheet có ba tab. Tab dữ liệu thô là nơi dán dữ liệu xuất ra. Tab tính dùng công thức (SUMIFS là công thức cộng có điều kiện; pivot là bảng tổng hợp tự động). Tab "số cho báo cáo" gồm cả chênh lệch so với kỳ trước.
  - Đường code: hàm `tinh()` trong `bao_cao.py`.
- **Bạn có sau bài:** tab hoặc file JSON "số cho báo cáo". (JSON là cách viết danh sách có khung rõ ràng để máy đọc được.)
- **Lỗi hay gặp:** để AI tính phần trăm tăng giảm.

### Bài C6.4: AI viết phần lời
- **Việc cần làm:** đưa cho AI chỉ dẫn sau: "Chỉ dùng con số trong bảng sau, chép đúng định dạng. Không tính thêm. Mỗi nhận định về nguyên nhân phải dẫn nguồn trong danh sách biên bản/bài học kèm theo; không có nguồn thì viết 'chưa rõ nguyên nhân'." Đính kèm bảng số cùng biên bản và sổ việc trong kỳ.
- **Bạn có sau bài:** bản nháp lời.

### Bài C6.5: Kiểm con số bằng code
- **Việc cần làm:** chạy `kiem_loi_van()` (mục 5). Số nào không có trong bảng thì chặn, trả về người làm báo cáo.
- **Bạn có sau bài:** danh sách số lạ.

### Bài C6.6: Duyệt và gửi
- **Việc cần làm:** người duyệt xem bảng số và lời cạnh nhau; xem mọi nhận định có nguồn. Gửi kèm link bảng số.
- **Lỗi hay gặp:** chỉ đọc lời văn, không mở bảng.

### Bài C6.7: Lưu báo cáo làm tri thức
- **Việc cần làm:** lưu mỗi kỳ: bảng số, lời, người duyệt, phiên bản định nghĩa chỉ số. Khi đổi định nghĩa chỉ số, tăng phiên bản (giống prompt ở `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` Bài 9.2).
- **Bạn có sau bài:** kho báo cáo theo kỳ, để kỳ sau mở ra so với kỳ trước.

## 5. Đường không code vs có code

Bài này có hai cách làm. Cách 1 không cần code, đủ dùng khi mới bắt đầu. Cách 2 cần một chút lập trình, để máy tự tính và tự kiểm thay cho người.

| | Không code | Có code nhẹ |
|---|---|---|
| Tính số | Công thức Sheet/Excel | `tinh()` đọc CSV |
| Viết lời | Project/Gem với bảng số dán vào | API với bảng số JSON |
| Kiểm số | Người dò từng số | `kiem_loi_van()` |

(CSV là file bảng dữ liệu dạng chữ thuần, mở được bằng Excel. API là cách để chương trình của bạn gọi AI từ xa, thay cho việc gõ vào khung chat.)

**Đoạn mã dưới đây làm gì?** Nó có ba việc. Hàm `tinh()` đọc dữ liệu doanh thu và cộng lại thành tổng, cộng riêng theo từng kênh bán. Hàm `kiem_loi_van()` lấy một đoạn lời văn, tìm mọi con số trong đó, rồi báo ra những số **không có** trong bảng số đã tính. Hàm `llm_gia` là một "AI giả" để chạy thử: nó viết đúng hai số, nhưng tự "nghĩ ra" thêm một phần trăm. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

**Mã mẫu (đã chạy thử, `python -I -X utf8`; `llm_gia` là hàm giả thay API):**

```python
import csv, io, re

def tinh(csv_text):
    tong, theo_kenh = 0, {}
    for d in csv.DictReader(io.StringIO(csv_text)):
        v = int(d["doanh_thu"]); tong += v
        theo_kenh[d["kenh"]] = theo_kenh.get(d["kenh"], 0) + v
    so = {"tong_doanh_thu": tong}
    so.update({"dt_" + k: v for k, v in theo_kenh.items()})
    return so

def ve_so(s):
    return int(s.replace(".", "").replace(",", ""))

def kiem_loi_van(loi_van, so):
    hop_le = set(so.values())
    return [m for m in re.findall(r"\d[\d.,]*\d|\d", loi_van) if ve_so(m) not in hop_le]

def llm_gia(so):  # gia lap AI: dung 2 so dung, tu "nghi ra" mot phan tram
    return ("Tuần này tổng doanh thu đạt %s đồng, trong đó Shopee %s đồng. Doanh thu Zalo tăng 12%%."
            % (f"{so['tong_doanh_thu']:,}".replace(",", "."), f"{so['dt_shopee']:,}".replace(",", ".")))
```

**Kết quả chạy thử:** với 3 dòng doanh thu giả, bảng số là `{'tong_doanh_thu': 24900000, 'dt_shopee': 16600000, 'dt_zalo': 8300000}`. Lời văn giả có câu "tăng 12%" mà con số này không có trong bảng, nên code trả về `['12']`. Cách sửa đúng là để code tính `ty_le_tang_zalo` và đưa vào bảng, không phải dặn AI "đừng bịa".

!!! tip "Nói đơn giản"
    Bước kiểm này giống việc một người đối chiếu: đọc từng con số trong bài viết, rồi dò xem nó có trong bảng số gốc không. Số nào không tìm thấy thì bị giữ lại để người làm báo cáo xem. Nó không cần hiểu bài viết nói gì.

**Giới hạn:** cách kiểm này bắt số lạ, không bắt số đúng đặt sai chỗ (ghi doanh thu Shopee là doanh thu Zalo). Muốn chặt hơn: yêu cầu AI viết bằng chỗ giữ như `{dt_zalo}` rồi code điền số. (Chỗ giữ là ô trống có tên, ví dụ chữ `{dt_zalo}` để chương trình thay bằng số thật.) Ngày tháng, số thứ tự ("tuần 45") cần loại trừ khỏi phép kiểm hoặc đưa vào bảng.

**Khi nào buộc chuyển sang code [Đề xuất]:** > 3 nguồn phải gom mỗi kỳ; báo cáo hằng ngày; muốn tự gửi theo lịch (nhưng vẫn có người duyệt).

## 6. Tiêu chí lên cấp [Đề xuất]

Bạn có thể sang cấp tiếp theo khi đạt đủ các điều sau:
1. Mỗi báo cáo định kỳ có định nghĩa chỉ số trong sổ C3.
2. 8 kỳ liên tiếp: không con số nào trong báo cáo đã gửi bị phát hiện sai sau đó.
3. Mọi nhận định nguyên nhân có nguồn hoặc ghi "chưa rõ".
4. Đo thời gian làm báo cáo bằng đồng hồ trước và sau (không hỏi cảm nhận, xem C0 mục 3.4).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung:

- **Shop mỹ phẩm bán đa kênh (Shopee, TikTok Shop, Zalo):** báo cáo tuần cho chủ shop gồm: doanh thu theo kênh, tỷ lệ hoàn, top 5 sản phẩm, tồn kho dưới mức tối thiểu, việc đang mở từ sổ việc. Số lấy từ file xuất của sàn. Còn phần "vì sao tỷ lệ hoàn tăng" thì dẫn biên bản họp CSKH (chăm sóc khách hàng) hoặc ghi "chưa rõ".
- **Công ty dịch vụ vệ sinh công nghiệp 80 nhân viên, 12 hợp đồng tòa nhà:** báo cáo tháng cho giám đốc gồm: số ca, số khiếu nại theo tòa nhà, sự cố an toàn, bài học mới (C5), mâu thuẫn tài liệu chưa xử lý (C4). Không đưa tên nhân viên bị khiếu nại vào AI; dùng mã.
- **Hợp tác xã nông sản (Lâm Đồng):** báo cáo vụ gồm: sản lượng theo hộ (mã hộ), giá bán bình quân, đơn hàng chưa giao. Bảng tính sẵn của kế toán là nguồn số; AI chỉ viết phần tóm tắt cho đại hội xã viên.

## 8. Tài liệu tham khảo

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| Evaluation-as-Search (Microsoft) | https://arxiv.org/abs/2608.20392 | Các trang chính, phụ lục | Cao (tiếng Anh, hỏi-đáp họp) |
| Re-FRAME (FRAME) | https://arxiv.org/abs/2509.15901 | Các trang chính | Trung bình-Cao |
| Khảo sát ngành trong `../nen-tang-bang-chung.md` mục 3 | `../nen-tang-bang-chung.md` | Thứ cấp | Thấp-Trung bình |

## 9. Chưa kiểm chứng

- Không tìm được nghiên cứu đo LLM viết báo cáo kinh doanh định kỳ (độ chính xác con số) có số liệu công khai. Không trích số nào cho phần này.
- Cách xuất dữ liệu của Shopee, TikTok Shop, phần mềm bán hàng phổ biến ở Việt Nam (KiotViet, Sapo, MISA...): chưa kiểm trong phiên này; tên chỉ là ví dụ thường gặp, không khẳng định tính năng.
- Ngưỡng 8 kỳ, 3 nguồn là đề xuất.
