# Cấp 4 (C4): Quyết định theo SOP bằng code, hành động ghi qua phiếu duyệt

> Ngày soạn: 2026-11-11. Quy ước: **[Nguồn]** / **[Đề xuất]**.
> Dùng lại: hạng công cụ C/D, idempotent, xác nhận của người ở `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` mục 3.4-3.5; hàng đợi duyệt, trạng thái, chạy lại ở `../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` bài 8.4-8.5. File này viết phần riêng: **ai quyết** (code hay AI), **phiếu hành động**, **hạn mức duyệt**, **xác nhận với khách**.

!!! tip "Tóm tắt nhanh"
    Khi khách xin đổi hàng hay hoàn tiền, câu hỏi khó nhất là "có được không, và ai bấm nút?". Bài này dạy một cách chia việc: những gì **tính được** (số ngày, số tiền, loại hàng) thì để **công thức hoặc code** quyết, AI chỉ **đọc tin khách** và **soạn câu trả lời**. Mọi hành động ghi (hoàn tiền, đổi hàng, dời lịch) đi qua một **phiếu** để người có quyền duyệt. Sau bài, bạn có một quy trình đổi trả mà AI không thể tự ý hoàn tiền.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người dùng kỹ thuật nhẹ và chủ shop, đã học xong cấp C3. Nếu bạn không biết lập trình, vẫn làm được bằng bảng tính (xem mục 5); phần mã chỉ để nhờ người biết code hoặc nhờ AI chạy giúp.

**Bạn cần chuẩn bị:**
- Kết quả của cấp C3 (tra được đơn hàng của khách).
- Bảng quyết định và bộ ca mẫu đã làm ở cấp C0 (bạn sẽ dùng lại ở Bài 4.1).
- Một bảng tính (Google Sheet hoặc Excel), hoặc một người biết code nếu muốn làm bằng code.

**Sau bài này bạn sẽ có:**
1. Hàm `xet_<loai>()` cho 1-3 loại yêu cầu (đổi trả, hoàn tiền, dời lịch). Hàm là một đoạn quy tắc viết sẵn: nhận thông tin đơn rồi tự tính điều kiện theo SOP (quy trình chuẩn của shop) và trả một trong ba kết quả: `du_dieu_kien` / `khong_du_dieu_kien` / `can_nguoi` (cần người xem), kèm lý do.
2. AI chỉ làm hai việc: **trích tham số** từ tin khách (tức là lấy ra các thông tin như mã đơn, lý do, ngày muốn dời) và **soạn câu** giải thích quyết định.
3. **Phiếu hành động** (tạo phiếu đổi, đề nghị hoàn tiền, dời lịch) vào hàng đợi (danh sách phiếu đang chờ xử lý); người duyệt theo hạn mức; hàm ghi **idempotent** (nghĩa là gọi lại nhiều lần cũng chỉ có tác dụng một lần, không hoàn tiền hai lần).
4. Quy tắc: chỉ báo khách "đã xong" khi hệ thống xác nhận thành công.

**Thứ bạn cầm đi được sau bài:** bảng hoặc hàm xét điều kiện, bảng phiếu hành động kèm hạn mức duyệt, và mẫu tin nhắn xin khách xác nhận.

## 2. Câu hỏi cấp này trả lời / lỗi của C3

Câu hỏi: *"Khách này có được đổi, được hoàn không, và ai bấm nút?"*

Lỗi ở C3: AI biết đơn ở đâu, nhưng quyết định vẫn do AI "đọc chính sách rồi suy ra". Các nghiên cứu dưới đây cho thấy đây là chỗ yếu.

Trước hết, hai từ cần biết. **Benchmark** là một bộ bài kiểm tra chuẩn để chấm điểm AI. **Agent** là AI được giao làm một chuỗi việc và được dùng công cụ (tra đơn, tạo phiếu...) thay vì chỉ trả lời chat.

- **[Nguồn]** τ-bench (arXiv 2406.12045, một bộ bài kiểm tra cho agent trong các tình huống chăm sóc khách hàng): quyết định sai (hiểu sai luật của lĩnh vực, gọi sai loại hành động) chiếm 25% lỗi của gpt-4o ở miền bán lẻ. Bỏ chính sách khỏi prompt (prompt là đoạn chỉ dẫn gõ cho AI), điểm bán lẻ của gpt-4o chỉ giảm từ 61,2 xuống 56,8: tác giả nhận xét thành công chủ yếu đến từ dùng công cụ theo lẽ thường, chưa thật sự dùng chính sách. Ở miền hàng không (luật phức tạp), điểm giảm từ 33,2 xuống 10,8.
- **[Nguồn]** τ-bench định nghĩa pass^k = xác suất cả k lần chạy đều đúng. gpt-4o ở bán lẻ có pass^1 trên 60% nhưng pass^8 dưới 25%. Với khách, mỗi ca chỉ có một lần.
- **[Nguồn]** τ-bench thừa nhận phần thưởng (điểm) của họ có thể bằng 1 dù agent thực hiện mà **không** xin xác nhận của khách, tức là vi phạm chính sách mà vẫn được tính đúng.
- **[Nguồn]** Policy Loopholes (arXiv 2609.14400): ở miền bán lẻ, công cụ có 32 lượt kiểm hợp lệ và đưa đơn vào trạng thái cuối chặn các lệnh ghi sau; nhờ vậy 2 lỗ hổng chính sách không gây lỗi. Miền hàng không có câu "API không kiểm" điều kiện hủy, bồi thường, để agent là người kiểm duy nhất; ở đó lỗ hổng gây lỗi. (API là cổng để phần mềm này gọi phần mềm khác làm việc.)
- **[Nguồn]** Nubank: "Compose deterministic flows in code, not in prompts" (tạm dịch: dựng các luồng cố định bằng code, đừng dựng bằng prompt); hàm hành động idempotent; chỉ xác nhận với khách khi công cụ báo thành công rõ ràng; agent không ra quyết định không đảo ngược về tín dụng, nợ (2606.08867; `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` mục 3.4).

!!! tip "Nói đơn giản"
    Giống như để một nhân viên mới "tự đọc nội quy rồi tự quyết" có hoàn tiền hay không: lúc đúng lúc sai, và không ai biết lần này sẽ là lúc nào. Còn nếu điều kiện được tính bằng công thức cố định thì lần nào cũng ra cùng một kết quả. Khách chỉ có một lần để được xử lý đúng, nên ta cần cách thứ hai.

**[Đề xuất]** Kết luận cho SME: điều gì tính được (số ngày, số tiền, trạng thái, loại hàng) thì code tính. AI không được là nơi duy nhất kiểm điều kiện.

## 3. Kiến thức nền

### 3.1 Chia việc trong một ca đổi trả [Đề xuất]

Bảng dưới đây cho biết từng bước trong một ca đổi trả do ai làm, và hàng rào nào chặn sai sót ở bước đó. Chữ in đậm là hai chỗ quan trọng nhất: việc xét điều kiện do code làm, việc duyệt do người làm.

| Bước | Ai | Hàng rào |
|---|---|---|
| Hiểu khách muốn gì, lý do gì | AI | Lý do phải thuộc danh sách; không thuộc → `can_nguoi` |
| Tra đơn | Code (C3) | Kiểm danh tính |
| Xét điều kiện | **Code** (bảng quyết định C0) | Thứ tự luật ghi rõ |
| Soạn giải thích | AI | Kiểm cụm cấm (C1), kiểm số (C3) |
| Tạo phiếu | Code | Idempotent |
| Duyệt | **Người**, theo hạn mức | Kiểm quyền người duyệt bằng code |
| Thực hiện | Code, chỉ sau duyệt | Từ chối nếu chưa duyệt |
| Báo khách kết quả | AI soạn từ trạng thái thật | Không báo "đã hoàn" trước khi hệ thống xác nhận |

!!! tip "Nói đơn giản"
    AI giống người trực tổng đài: nghe khách, hiểu ý khách, viết câu trả lời cho lịch sự. Còn "có được đổi hay không" là việc của bảng quy tắc, và "có chi tiền hay không" là việc của người có quyền. Mỗi bên làm đúng phần của mình.

### 3.2 Thứ tự luật là một quyết định chính sách

Khi hai dòng của bảng cùng khớp (hàng sale **và** lỗi do shop), dòng nào đứng trước sẽ thắng. Đây là lỗi "mơ hồ khi kết hợp" và "điều khoản mâu thuẫn" trong phân loại của arXiv 2609.14400. Viết thứ tự đó ra trong SOP, không để code ngầm quyết.

!!! tip "Nói đơn giản"
    Ví dụ: shop quy định "hàng sale không đổi trả", nhưng khách nhận phải áo bị rách. Hai quy tắc cùng đúng, nhưng chỉ một quy tắc được thắng. Chủ shop phải nói rõ quy tắc nào đứng trước, rồi ghi vào SOP, để nhân viên và hệ thống làm giống nhau.

### 3.3 Hạn mức duyệt [Đề xuất]

Hạn mức duyệt là quy định số tiền hoặc loại việc nào thì ai có quyền bấm đồng ý.

| Hành động | Ai duyệt |
|---|---|
| Tạo phiếu đổi size (không tiền) | Nhân viên trực |
| Hoàn tiền < 500.000đ | Trưởng ca |
| Hoàn tiền ≥ 500.000đ, ngoại lệ chính sách | Chủ shop |
| Hủy đơn đã thanh toán | Chủ shop |

Con số 500.000đ là ví dụ. Kiểm quyền người duyệt bằng code: trưởng ca bấm duyệt phiếu thuộc quyền chủ shop thì hệ thống từ chối.

### 3.4 Khung pháp lý liên quan hoàn tiền [Nguồn: Luật 19/2023 qua caselaw.vn; chưa đọc Công báo]

Điều 38 (giao kết hợp đồng trong giao dịch từ xa): nếu doanh nghiệp cung cấp thông tin không chính xác, không đầy đủ theo Điều 37, người tiêu dùng có quyền đơn phương chấm dứt hợp đồng trong 30 ngày kể từ ngày giao kết; doanh nghiệp phải hoàn tiền trong 30 ngày kể từ khi nhận thông báo. **[Đề xuất]** Nghĩa là thông tin sai do AI nói ra có thể biến thành nghĩa vụ hoàn tiền. Đây là thêm một lý do cho C1 và C3. Không suy rộng: điều kiện cụ thể phải đọc văn bản gốc.

!!! warning "Cẩn thận"
    Đoạn trên chỉ là tóm tắt để bạn hiểu rủi ro, **không phải tư vấn pháp lý**. Nguồn mới đọc qua công cụ tóm tắt, chưa đọc văn bản gốc. Trước khi áp dụng cho shop của bạn, hãy đọc điều luật gốc hoặc hỏi người có chuyên môn.

### 3.5 Hỏi khách xác nhận trước khi ghi

**[Nguồn]** Chính sách miền hàng không của τ-bench yêu cầu agent liệt kê chi tiết hành động và chờ khách trả lời "yes" trước khi cập nhật dữ liệu. **[Đề xuất]** Với SME: trước khi tạo phiếu, nháp gửi khách tóm tắt "Shop sẽ đổi áo mã ... sang size L, anh/chị gửi hàng về ..., phí ship ... Anh/chị xác nhận giúp shop nhé". Chỉ tạo phiếu khi khách xác nhận.

!!! tip "Nói đơn giản"
    Đọc lại cho khách nghe "shop sẽ làm gì" và chờ khách gật đầu, rồi mới ghi vào hệ thống. Cách này tránh được tình huống khách hiểu một đằng, shop làm một nẻo.

## 4. Chuỗi bài nhỏ

Sáu bài dưới đây làm theo thứ tự. Mỗi bài có việc cần làm; một số bài có thêm phần thử, lỗi hay gặp hoặc cách làm không cần code.

### Bài 4.1: Bảng quyết định thành hàm
- **Việc cần làm:** chuyển bảng quyết định C0 của 1 loại (đổi trả) thành hàm `xet_doi_tra(don, ly_do, hom_nay)`. Làm lần lượt như sau: (1) mỗi dòng của bảng là một nhánh `if` (nghĩa là "nếu... thì..."), có chú thích số dòng; (2) đặt dòng cuối là `can_nguoi`, để mọi trường hợp không khớp luật nào đều chuyển cho người.
- **Thử:** toàn bộ ca biên trong bộ ca mẫu C0 (đúng ngày thứ 7, ngày thứ 8, hàng sale lỗi, lý do lạ). Ca biên là ca nằm sát ranh giới của luật, nơi dễ sai nhất.
- **Không code:** bảng tính có công thức `IF` tính số ngày và trả "đủ/không đủ/cần người"; nhân viên điền ô, AI chỉ soạn câu.

### Bài 4.2: AI trích tham số, không quyết định
- **Việc cần làm:** làm theo ba bước. (1) Viết prompt chỉ cho AI xuất JSON dạng `{ma_don, ly_do, ...}`, trong đó `ly_do` phải thuộc một danh sách cố định (JSON là cách viết thông tin có khung rõ ràng để máy đọc được). (2) Code gọi `xet_doi_tra()` để xét điều kiện. (3) AI nhận kết quả và soạn giải thích từ mẫu câu.
- **Lỗi hay gặp:** để AI trả luôn "đủ điều kiện"; cho AI tự tính số ngày.

### Bài 4.3: Phiếu hành động và hàng đợi
- **Việc cần làm:** tạo bảng `phieu` (Sheet hoặc SQLite; SQLite là một loại cơ sở dữ liệu nhỏ, nằm gọn trong một file) với các cột: `key = ma_don:hanh_dong`, hành động, tham số chính xác, số tiền, trạng thái (`cho_duyet` / `da_duyet` / `tu_choi` / `da_thuc_hien`), người duyệt cần có, người đã duyệt, lý do.
- **Người duyệt thấy:** tin khách, kết quả tra đơn, kết quả `xet_...` kèm lý do, tham số sẽ chạy, nháp gửi khách.

### Bài 4.4: Idempotent và chặn chạy khi chưa duyệt
- **Việc cần làm:** kiểm bốn điều. (1) Gọi `tao_phieu` hai lần cùng key thì chỉ có một phiếu. (2) `thuc_hien` khi chưa duyệt thì báo lỗi. (3) Duyệt sai quyền thì báo lỗi. (4) Thực hiện hai lần thì chỉ một lần thật.
- **Thử:** giả lập mạng lỗi giữa chừng; chạy lại; đếm số lần hoàn tiền thật (phải là 1).

### Bài 4.5: Xác nhận với khách
- **Việc cần làm:** thêm bước khách xác nhận trước khi tạo phiếu; sau khi thực hiện, nháp báo kết quả đọc từ trạng thái phiếu, không từ lời AI.

### Bài 4.6: Mở rộng sang loại thứ hai
- **Việc cần làm:** làm lại 4.1-4.5 cho dời lịch hoặc hoàn tiền. Đo lại bộ ca mẫu của loại thứ nhất để chắc không hỏng (kiểu kho ca cũ của BMO, `../nen-tang-bang-chung.md` mục 1.4). Ý là: thêm chức năng mới đôi khi làm hỏng chức năng cũ, nên phải chạy lại các ca đã đúng trước đó.

## 5. Đường không code vs có code

Cách không code dùng bảng tính và người bấm nút, đủ dùng khi mới bắt đầu. Cách code nhẹ cần người biết lập trình, để máy tự chặn các lỗi mà bảng tính khó chặn.

| | Không code | Code nhẹ |
|---|---|---|
| Xét điều kiện | Bảng tính `IF` | Hàm Python |
| Phiếu | Dòng trong Sheet, người đổi trạng thái | Bảng + hàm `tao_phieu/duyet/thuc_hien` |
| Thực hiện | Người làm trong phần mềm bán hàng | Code gọi API ghi **sau** duyệt; hoặc vẫn để người làm |

**Đoạn mã dưới đây làm gì?** Nó là một bản mô phỏng nhỏ của cả quy trình. Hàm `xet_doi_tra` xét xem đơn có đủ điều kiện đổi trả không (đã giao chưa, hàng sale hay không, quá bao nhiêu ngày, lý do có nằm trong quy định không). Hàm `tao_phieu` tạo phiếu và tự chọn người duyệt theo số tiền. Hàm `duyet` chỉ cho đúng người có quyền bấm. Hàm `thuc_hien` từ chối nếu phiếu chưa được duyệt, và nếu gọi hai lần thì chỉ làm một lần. Bạn **không cần đọc hiểu từng dòng**; chỉ cần nắm ý nghĩa của nó, và nhờ người biết lập trình (hoặc nhờ AI) chạy giúp khi bạn cần đến cấp độ này.

Mã mẫu (đã chạy thử bằng `python -I -X utf8`, 2026-11-11; SOP là giả định; "thực hiện" chỉ đổi cờ, không gọi API thật):

```python
from datetime import date
SOP = {"so_ngay_doi_tra": 7, "nguong_hoan_can_chu": 500000, "khong_doi_tra": {"hang_sale", "do_lot"}}

def xet_doi_tra(don, ly_do, hom_nay):
    if don.get("trang_thai") != "da_giao":
        return "khong_du_dieu_kien", ["don chua giao xong"]
    if ly_do == "loi_san_pham":                       # dong nay dung TRUOC dong hang sale: quyet dinh cua SOP
        return "du_dieu_kien", ["loi tu shop: doi tra khong ap han"]
    if don.get("loai") in SOP["khong_doi_tra"]:
        return "khong_du_dieu_kien", [f"loai {don['loai']} khong doi tra theo SOP"]
    if "ngay_giao" not in don:
        return "can_nguoi", ["thieu ngay giao"]
    so_ngay = (hom_nay - date.fromisoformat(don["ngay_giao"])).days
    if so_ngay > SOP["so_ngay_doi_tra"]:
        return "khong_du_dieu_kien", [f"da {so_ngay} ngay > {SOP['so_ngay_doi_tra']} ngay"]
    if ly_do not in {"khong_vua", "doi_y"}:
        return "can_nguoi", [f"ly do '{ly_do}' SOP chua quy dinh"]
    return "du_dieu_kien", [f"trong han ({so_ngay} ngay)"]

PHIEU = {}
def tao_phieu(ma_don, hanh_dong, so_tien):
    key = f"{ma_don}:{hanh_dong}"
    if key in PHIEU: return PHIEU[key]                # AI thu lai khong tao phieu thu hai
    nguoi = "chu_shop" if so_tien >= SOP["nguong_hoan_can_chu"] else "truong_ca"
    PHIEU[key] = {"key": key, "hanh_dong": hanh_dong, "so_tien": so_tien,
                  "trang_thai": "cho_duyet", "nguoi_duyet": nguoi}
    return PHIEU[key]

def duyet(key, nguoi, dong_y):
    p = PHIEU[key]
    if nguoi != p["nguoi_duyet"]: raise PermissionError(f"{nguoi} khong co quyen duyet {key}")
    p["trang_thai"] = "da_duyet" if dong_y else "tu_choi"; return p

def thuc_hien(key):
    p = PHIEU[key]
    if p["trang_thai"] != "da_duyet": raise RuntimeError("Chua duyet: khong thuc hien")
    if p.get("da_thuc_hien"): return p                # idempotent
    p["da_thuc_hien"] = True                          # cho goi API hoan tien/tao phieu that
    return p
```

Kết quả chạy thử (hôm nay 2026-11-11): giao 1/11, không vừa → không đủ (10 ngày > 7); giao 8/11 → đủ (3 ngày); lý do "màu khác ảnh" → `can_nguoi`; hàng sale lỗi → đủ (vì dòng lỗi đứng trước). Gọi `tao_phieu` hai lần → cùng một phiếu; `thuc_hien` trước duyệt → bị chặn; trưởng ca duyệt phiếu 1.250.000đ → bị chặn; chủ shop duyệt rồi thực hiện → thành công một lần.

!!! tip "Nói đơn giản"
    Kết quả chạy thử cho thấy bốn "hàng rào" hoạt động đúng: không đủ điều kiện thì bị từ chối, trường hợp lạ thì chuyển cho người, người không đủ quyền thì không duyệt được, và chưa duyệt thì không chi tiền được.

**Buộc chuyển sang code khi [Đề xuất]:** bảng tính `IF` không còn đọc được (trên khoảng 6-8 dòng); cần chặn duyệt sai quyền; cần chạy lại an toàn khi lỗi giữa chừng.

**Khi nào cho code tự gọi API ghi:** chỉ khi đã qua C6 với số đo, và chỉ với hành động đảo ngược được, tiền nhỏ. Mặc định nhân viên vẫn bấm trong phần mềm. Hạng D trong `../rag-tra-cuu-tai-lieu/cap-07-cong-cu-tool.md` mục 3.5 vẫn áp dụng.

## 6. Tiêu chí lên cấp (C4 → C5) [Đề xuất]

Bạn có thể sang cấp C5 khi đạt đủ các điều sau:
1. Hàm xét điều kiện đạt 100% trên mọi ca biên của bộ ca mẫu (đây là code, nên phải đúng tuyệt đối).
2. AI trích tham số đúng ≥ một ngưỡng chủ shop ký nhận trên ≥30 ca, chạy 3 lần mỗi ca; báo cả pass^1 và pass^3 (C6).
3. 0 hành động ghi chạy khi chưa duyệt; 0 phiếu trùng trong bài thử lỗi mạng.
4. Mọi phiếu truy vết được: tin khách → tham số → kết quả xét → người duyệt → kết quả thực hiện.
5. Thứ tự luật đã viết vào SOP và được chủ shop ký.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

### 7.a Shop giày online, hoàn tiền khi hết hàng đổi
Khách đổi size, size mới hết hàng. SOP: đề nghị đổi mẫu khác hoặc hoàn tiền. AI hỏi khách chọn. Khách chọn hoàn 890.000đ → phiếu `hoan_tien`, người duyệt chủ shop (≥500.000đ). Chủ shop chuyển khoản tay, đánh dấu đã thực hiện; AI soạn báo khách từ trạng thái phiếu.

### 7.b Spa, dời lịch có đặt cọc
`xet_doi_lich(lich, gio_moi, bay_gio)`: tính số giờ còn lại tới lịch cũ; ≥24 giờ → đủ, giữ cọc; <24 giờ → mất cọc trừ lý do sức khỏe (lý do sức khỏe → `can_nguoi`). Phiếu `doi_lich` không có tiền → nhân viên trực duyệt. Hành động ghi vào lịch chỉ sau duyệt và khi khung giờ mới còn trống (code kiểm lại lúc thực hiện, không tin kết quả lúc soạn).

### 7.c Cửa hàng vật liệu xây dựng, trả hàng dư
Khách công trình trả gạch dư. Điều kiện: chưa vỡ, cùng lô, trong 15 ngày (giả định). Số tiền thường lớn → mọi phiếu hoàn tiền lên chủ. AI chỉ giúp gom thông tin (mã đơn, số lượng, ảnh) và soạn phiếu.

## 8. Tài liệu tham khảo

| Nguồn | Loại | Đọc | Tin cậy |
|---|---|---|---|
| τ-bench, arXiv 2406.12045 | Benchmark | Toàn văn phần chính, phụ lục chính sách | Cao về phương pháp; số mô hình 2024 |
| Policy Loopholes, arXiv 2609.14400 | Bài báo trên benchmark | Phần chính, phụ lục | Trung bình-Cao |
| Nubank, arXiv 2606.08867 | Bài báo, triển khai thật | Phần lớn toàn văn | Cao |
| BMO ESCROW, arXiv 2608.01772 | Bài báo | Qua `../nen-tang-bang-chung.md` | Cao |
| Luật 19/2023/QH15 Điều 37-38, caselaw.vn | Văn bản luật | Qua công cụ tóm tắt | Trung bình |

## 9. Chưa kiểm chứng

- Điều kiện và thời hạn trong Điều 38 Luật 19/2023 chỉ qua tóm tắt; chưa đọc Điều 37 (thông tin bắt buộc trong giao dịch từ xa).
- Chưa có nguồn về tỉ lệ sai khi AI trích tham số trên tin tiếng Việt thật.
- Ngưỡng 500.000đ, 24 giờ, 15 ngày: ví dụ giả định.
- API ghi (hoàn tiền, tạo phiếu đổi) của KiotViet, Sapo, Haravan: chưa đọc; ví dụ giữ hành động thực hiện bằng tay.
