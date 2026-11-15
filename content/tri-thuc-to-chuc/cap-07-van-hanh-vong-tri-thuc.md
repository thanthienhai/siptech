# Cấp 7 (C7): Vận hành vòng tri thức

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác.
> Dùng lại, không viết lại: nhật ký, phiên bản prompt, quy trình sửa → chạy lại → phát hành, trôi dạt mô hình (`../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md`); bộ ca mẫu và thống kê n nhỏ (`../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`). Cấp này thêm **vòng đời của tài liệu**: tạo, duyệt, dùng, rà soát, hết hiệu lực, và cổng nối sang nhóm RAG, nhóm xử lý yêu cầu khách.

!!! tip "Tóm tắt nhanh"
    Có biên bản, SOP, sổ đăng ký rồi thì vấn đề tiếp theo là giữ cho chúng **còn đúng và còn được dùng** sau nhiều tháng. Bài này dạy cách đặt ra một **nhịp làm việc** hằng tuần, hằng tháng, hằng quý, một bảng chỉ số nhỏ để theo dõi "sức khỏe" tri thức, và một **cổng kiểm** chặn tài liệu chưa đạt điều kiện trước khi đưa cho trợ lý AI. Làm xong, bạn có lịch vận hành 1 trang, bảng chỉ số, bảng phân vai và một cổng kiểm (làm bằng bộ lọc Google Sheet, hoặc bằng đoạn mã nếu có người biết lập trình).

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người được giao "giữ tri thức" của công ty (thường là quản lý vận hành hoặc trợ lý giám đốc), và chủ doanh nghiệp. Bạn **không cần biết code**.

**Bạn cần chuẩn bị:**
- Các thứ đã làm ở những cấp trước: biên bản họp (C0), sổ đăng ký tài liệu (C3), hàng đợi mâu thuẫn và báo sai (C4), bài học (C5). Bài này không làm lại chúng, chỉ dạy cách giữ cho chúng chạy đều.
- Một bảng tính Google Sheet hoặc Excel (chính là sổ đăng ký tài liệu).
- Một lịch điện tử (Google Calendar hoặc Lark) để đặt lịch nhắc.
- Nếu công ty đã có trợ lý AI dùng tài liệu nội bộ (Project/Gem chung, kho RAG, chatbot trả lời khách), hãy biết nó đang dùng những tài liệu nào. (RAG là cách để AI tra cứu trong kho tài liệu của bạn rồi mới trả lời.)

**Sau bài này bạn sẽ có:**
1. Có **nhịp** cố định: việc hằng tuần, hằng tháng, hằng quý.
2. Có **5-8 chỉ số** về sức khỏe tri thức, xem mỗi tháng.
3. Có **cổng xuất**: chỉ tài liệu đạt điều kiện mới được đưa vào Project/Gem, kho RAG, trợ lý trả lời khách.
4. Mỗi lần tài liệu đổi, **ca thử** của các trợ lý dùng tài liệu đó được chạy lại. (Ca thử là một câu hỏi mẫu kèm đáp án đúng, dùng để kiểm xem trợ lý còn trả lời đúng không.)
5. Phân vai rõ, có người thay khi người giữ tri thức nghỉ.

**Thứ bạn cầm đi được sau bài:** lịch vận hành 1 trang; bảng chỉ số tháng; script `cong_xuat.py` (script là một đoạn chương trình ngắn, chỉ cần nếu bạn chọn đường có code); bảng phân vai.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Đã có biên bản, SOP, sổ đăng ký, bài học, báo cáo. Làm sao để 6 tháng sau nó vẫn đúng và vẫn được dùng?"*

(SOP là quy trình làm việc chuẩn, viết thành văn bản.)

Lỗi thường gặp sau C0-C6 **[Đề xuất, quan sát chung về quản trị tài liệu]**: hăng hái 2-3 tháng rồi bỏ; sổ không ai cập nhật; trợ lý AI vẫn trả lời theo tài liệu cũ vì không ai nối việc sửa tài liệu với việc cập nhật trợ lý.

!!! tip "Nói đơn giản"
    Làm tài liệu một lần thì dễ, giữ cho nó đúng theo thời gian mới khó. Cấp này không dạy thêm cách viết tài liệu. Nó dạy cách **duy trì**: có lịch, có người phụ trách, có số đo, và có cổng chặn tài liệu cũ hoặc sai lọt sang trợ lý AI.

## 3. Kiến thức nền

Phần này gồm năm nghiên cứu cho thấy vì sao phải vận hành đều đặn, một bảng chỉ số để theo dõi, và quy tắc cổng xuất.

### 3.1 Bằng chứng về giữ chất lượng khi thay đổi [Nguồn]

- **BMO ESCROW** (arXiv 2608.01772, qua `../nen-tang-bang-chung.md`): qua 4 vòng sửa skill, không có kho ca cũ thì điểm trên ca cũ tụt 0,857 → 0,7; có kho ca cũ giữ khoảng 0,84. Ý: mỗi lần đổi tài liệu/quy tắc phải chạy lại ca cũ. (Skill ở đây là một bộ chỉ dẫn đóng gói sẵn cho AI. "Kho ca cũ" là tập hợp các ca thử đã dùng trước đó.)
- **Airbnb** (arXiv 2610.14428): lớp tóm tắt do AI sinh trôi khi kho đổi; bảo trì là gánh nặng thật. ("Trôi" nghĩa là dần dần lệch khỏi tài liệu gốc mà không ai để ý.)
- **SAP** (arXiv 2608.00122): nguy cơ nhiễm độc bộ nhớ dùng chung; điểm tin cậy chưa hiệu chuẩn. ("Nhiễm độc" là khi một ghi chú sai lọt vào kho dùng chung và lan sang mọi người dùng nó.)
- **SAP Signavio** (arXiv 2607.03228): bộ nhớ cần chủ sở hữu, quyền đọc/sửa, quy trình duyệt, trách nhiệm giải trình; lỗi còn lại do mục quy tắc viết quá rộng, nghĩa là chất lượng biên soạn quyết định kết quả.
- **IBM Japan** (arXiv 2611.11348): khi SOP đổi mà tri thức bổ sung không được giữ riêng, các chỉnh sửa trước bị mất ("trôi SOP-kỹ năng").

!!! tip "Nói đơn giản"
    Năm ví dụ trên cùng nói một điều: **mỗi lần có thay đổi, chất lượng dễ tụt âm thầm**. Cách phòng là chạy lại các ca thử cũ sau mỗi thay đổi, có chủ cho từng mục tri thức, có người duyệt trước khi nhập kho, và viết quy tắc cho gọn, rõ.

### 3.2 Chỉ số sức khỏe tri thức [Đề xuất]

Bảng dưới đây là tám con số bạn xem mỗi tháng, giống như khám sức khỏe định kỳ cho kho tri thức. Cột "Nguồn" cho biết số liệu lấy từ cấp nào hoặc từ đâu (C0 là biên bản, C3 là sổ đăng ký, C4 là mâu thuẫn và báo sai, C5 là bài học).

| Chỉ số | Cách tính | Nguồn |
|---|---|---|
| Độ phủ sổ | Tài liệu AI đang dùng có trong sổ / tổng tài liệu AI đang dùng | C3 |
| Quá hạn rà soát | Tài liệu "hiệu lực" quá hạn / tổng "hiệu lực" | C3 |
| Độ trễ quyết định → tài liệu | Trung vị số ngày từ quyết định chốt (C0) tới khi tài liệu cập nhật | C0, C3 |
| Mâu thuẫn mở | Số mâu thuẫn chưa quyết > 5 ngày | C4 |
| Bài học đã áp dụng | Bài học "đã áp dụng vào tài liệu" / bài học đã duyệt | C5 |
| Chất lượng biên bản | Việc bị sửa/bịa/sót khi duyệt, trên mẫu 5 cuộc họp/tháng | C0 |
| Dùng thật | Số lần tài liệu được trợ lý trích dẫn hoặc được mở | nhật ký RAG |
| Báo sai | Số "báo sai" mỗi tháng và thời gian xử lý | C4 |

(Trung vị là giá trị nằm ở giữa khi xếp các số từ nhỏ đến lớn; nó ít bị kéo lệch bởi một vài trường hợp quá dài hoặc quá ngắn. Nhật ký là bản ghi lại trợ lý đã được hỏi gì, trả lời bằng tài liệu nào.)

Với SME nhỏ, các tỷ lệ này tính trên vài chục tài liệu: xem xu hướng, không kết luận từ một tháng (xem `../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md` mục 3.2).

!!! tip "Nói đơn giản"
    Đừng cố theo dõi cả tám con số ngay từ tháng đầu nếu thấy nặng; bài đặt mục tiêu 5-8 chỉ số. Quan trọng là **xem đều mỗi tháng và nhìn xu hướng** (đang tốt lên hay xấu đi), vì với vài chục tài liệu, một tháng chưa đủ để kết luận gì.

### 3.3 Cổng xuất sang nhóm khác [Đề xuất]

Một tài liệu chỉ được đưa vào kho của trợ lý (RAG, Project/Gem chung, chatbot khách) khi: "hiệu lực"; có chủ đang làm việc; không quá hạn rà soát; đã đánh dấu được dùng cho AI; mức nhạy cảm cho phép; không có mâu thuẫn mở. Cổng này là **code hoặc bộ lọc Sheet**, không phải lời dặn.

!!! tip "Nói đơn giản"
    "Cổng xuất" giống chốt kiểm tra ở cửa kho: tài liệu nào thiếu một trong sáu điều kiện trên thì không được đi qua. Điểm mấu chốt là cổng phải **tự chặn bằng công cụ** (bộ lọc Sheet hoặc đoạn mã), không chỉ nhắc nhau bằng lời, vì lời dặn thì rất dễ bị quên.

## 4. Chuỗi bài nhỏ

Sáu bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm và thứ bạn có sau bài.

### Bài C7.1: Lịch vận hành
- **Việc cần làm [Đề xuất]:** chia việc theo ba nhịp.
  - *Hằng tuần (30 phút):* chạy kiểm sổ (C3), xem hàng đợi mâu thuẫn và báo sai (C4), nhắc chủ tài liệu quá hạn.
  - *Hằng tháng (1-2 giờ):* tính bảng chỉ số; lấy mẫu 5 biên bản kiểm chất lượng; xem bài học chưa áp dụng; chạy lại ca thử của các trợ lý.
  - *Hằng quý:* rà quy tắc ghi âm và dữ liệu (C1, C5); kiểm điều khoản công cụ AI (theo `../an-toan-du-lieu-va-phap-ly-vn.md` mục 5); chọn 1-2 quy trình mới để làm SOP (C2).
- **Bạn có sau bài:** lịch trên Google Calendar/Lark, có người nhận.
- **Lỗi hay gặp:** lịch ghi chung chung, không gắn tên người nhận; làm hăng hái vài tuần đầu rồi bỏ (đúng lỗi nêu ở mục 2).

### Bài C7.2: Phân vai
- **Việc cần làm:** đặt ra ba vai tối thiểu: *chủ tài liệu* (quyết nội dung); *người giữ sổ* (chạy kiểm, nhắc, cổng xuất); *người duyệt AI* (duyệt biên bản, bài học, báo cáo). Một người có thể giữ nhiều vai, nhưng chủ tài liệu không tự duyệt thay đổi do AI đề xuất cho tài liệu quan trọng của chính mình nếu có người khác làm được **[Đề xuất]**. Mỗi vai có người dự phòng.
- **Bạn có sau bài:** bảng phân vai trong sổ C3.
- **Lỗi hay gặp:** vai nào cũng chỉ có một người, nên người đó nghỉ là hệ thống dừng; chủ tài liệu tự duyệt luôn thay đổi AI đề xuất cho chính tài liệu của mình.

### Bài C7.3: Cổng xuất bằng code
- **Việc cần làm:** chạy `cong_xuat.py` (xem mục 5) trước mỗi lần cập nhật kho của trợ lý. Tài liệu bị chặn kèm lý do được gửi cho chủ. Nếu chưa có người biết code, dùng bộ lọc Sheet ở mục 5 để làm việc tương tự.
- **Bạn có sau bài:** danh sách được xuất / bị chặn mỗi lần cập nhật.
- **Lỗi hay gặp:** chạy cổng xong nhưng tài liệu bị chặn không ai báo cho chủ nên không ai sửa.

### Bài C7.4: Tài liệu đổi → chạy lại ca thử
- **Việc cần làm:** mỗi trợ lý (nhóm RAG, nhóm xử lý yêu cầu khách) có bảng ca thử gắn với mã tài liệu. Khi tài liệu đổi (phát hiện bằng `../rag-tra-cuu-tai-lieu/cap-03-chia-khoi-va-chi-muc.md` Bài 3.8), làm lần lượt:
  1. Cập nhật đáp án của ca bị ảnh hưởng.
  2. Chạy lại toàn bộ ca, không chỉ ca liên quan (bài học ESCROW ở mục 3.1).
  3. Chỉ phát hành khi không ca cũ nào hỏng (quy trình ở `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` Bài 9.3).
- **Bạn có sau bài:** dòng nhật ký: tài liệu đổi, ca chạy lại, kết quả.
- **Lỗi hay gặp:** chỉ chạy lại các ca "có vẻ liên quan", nên bỏ lọt ca cũ bị hỏng.

### Bài C7.5: Chống nhiễm độc kho
- **Việc cần làm:** đặt bốn quy tắc nhập kho. Một, chỉ người có quyền mới nhập vào kho. Hai, mọi mục có nguồn. Ba, mục do AI sinh (thẻ quy tắc, bài học, tóm tắt) được đánh dấu và **không được trích làm nguồn** thay tài liệu gốc (giống quy tắc của Airbnb ở nhóm RAG). Bốn, tài liệu từ bên ngoài (email khách, file nhà cung cấp) không vào kho tri thức nội bộ khi chưa qua chủ.
- **Bạn có sau bài:** quy tắc nhập kho 5 dòng.
- **Lỗi hay gặp:** để bản tóm tắt do AI viết đứng thay tài liệu gốc, rồi lần sau AI trích lại chính bản tóm tắt đó.

### Bài C7.6: Đo chi phí và giá trị
- **Việc cần làm:** mỗi quý ghi giờ công cho vận hành (lịch C7.1) và các số đo trước-sau có đồng hồ (thời gian làm biên bản, báo cáo; thời gian người mới làm được việc). Quyết định giữ, thu hẹp, hay mở rộng dựa trên số này.
- **Bạn có sau bài:** bảng quý.
- **Lỗi hay gặp:** chỉ ước chừng "chắc là nhanh hơn" mà không bấm giờ thật.

## 5. Đường không code vs có code

Cách không code đủ dùng khi bạn mới bắt đầu. Cách có code giúp máy tự làm những việc lặp lại, và cần một người biết lập trình (hoặc nhờ AI) hỗ trợ.

| | Không code | Có code nhẹ |
|---|---|---|
| Chỉ số | Tab "Chỉ số" trong Sheet sổ đăng ký | Script đọc các sổ, xuất bảng |
| Cổng xuất | Bộ lọc Sheet (lọc theo các cột điều kiện) | `cong_xuat.py` chạy trước khi cập nhật kho |
| Nhắc việc | Lịch, nhắc thủ công | Script gửi email theo lịch (Task Scheduler/cron) |

(Task Scheduler là công cụ đặt lịch chạy việc tự động trên Windows, cron là công cụ tương tự trên Linux.)

**Đoạn mã dưới đây làm gì?** Nó đọc bảng tài liệu (dạng CSV, tức là bảng chữ tách bằng dấu phẩy, xuất được từ Excel hoặc Google Sheet) rồi kiểm từng tài liệu theo sáu điều kiện ở mục 3.3: còn hiệu lực không, chủ còn đang làm việc không, có quá hạn rà soát không, đã được phép dùng cho AI chưa, mức nhạy cảm có cho phép không, và có mâu thuẫn mở không. Tài liệu đạt hết thì vào danh sách "được xuất"; thiếu điều kiện nào thì vào danh sách "bị chặn" kèm lý do. Bạn **không cần đọc hiểu từng dòng**; chỉ cần nắm ý nghĩa của nó, và nhờ người biết lập trình (hoặc nhờ AI) chạy giúp khi cần.

**Mã mẫu (đã chạy thử, `python -I -X utf8`):**

```python
import csv, io
from datetime import date
MUC_CHO_PHEP = {"cong_khai", "noi_bo"}

def cong_xuat(csv_text, hom_nay, nhan_vien_dang_lam, mau_thuan_mo):
    duoc, bi_chan = [], []
    for d in csv.DictReader(io.StringIO(csv_text)):
        ly_do = []
        if d["trang_thai"] != "hieu_luc": ly_do.append("khong_hieu_luc")
        if d["chu_so_huu"] not in nhan_vien_dang_lam: ly_do.append("khong_co_chu")
        if (hom_nay - date.fromisoformat(d["ra_soat_lan_cuoi"])).days > int(d["chu_ky_ngay"]):
            ly_do.append("qua_han_ra_soat")
        if d["duoc_dung_cho_AI"] != "co": ly_do.append("chua_duoc_phep_AI")
        if d["muc_nhay_cam"] not in MUC_CHO_PHEP: ly_do.append("nhay_cam:" + d["muc_nhay_cam"])
        if d["ma"] in mau_thuan_mo: ly_do.append("co_mau_thuan_chua_xu_ly")
        (bi_chan if ly_do else duoc).append((d["ma"], ly_do))
    return duoc, bi_chan
```

**Kết quả chạy thử** với 4 tài liệu giả: chỉ `BG-2026Q4` được xuất; `SOP-BH-01` bị chặn vì còn mâu thuẫn mở (ví dụ của C4); hợp đồng khách `HD-KH-ABC` bị chặn vì mức "bí mật"; `SOP-KHO-02` bị chặn vì chủ đã nghỉ và quá hạn rà soát.

!!! tip "Nói đơn giản"
    Đoạn mã chỉ làm đúng một việc bạn có thể tự làm bằng tay trên Sheet: đi qua từng tài liệu, hỏi sáu câu "có/không", và tách ra nhóm được đi tiếp, nhóm bị giữ lại kèm lý do. Code giúp việc này nhanh và không bị bỏ sót khi có nhiều tài liệu.

**Khi nào buộc chuyển sang code [Đề xuất]:** có ≥ 2 trợ lý dùng chung kho; cập nhật kho hơn 1 lần/tuần; > 100 tài liệu.

## 6. Tiêu chí "đang vận hành" [Đề xuất]

Đây là cấp cuối của nhóm. Coi là đang vận hành khi đủ 6 tháng liên tục:
1. Lịch tuần và tháng được làm ≥ 90% số lần.
2. Mọi lần cập nhật kho trợ lý đi qua cổng xuất; không tài liệu bị chặn nào lọt vào kho (kiểm ngẫu nhiên).
3. Mỗi lần tài liệu đổi có dòng nhật ký chạy lại ca thử.
4. Bảng chỉ số tháng có đủ 6 tháng; xu hướng quá hạn rà soát và mâu thuẫn mở không tăng.
5. Đã qua ít nhất một lần nghỉ việc hoặc đổi người giữ sổ mà hệ thống vẫn chạy.

**Khi nào nâng cấp lên công cụ chuyên dụng [Đề xuất]:** Sheet chậm hoặc hay bị sửa nhầm; > 300 tài liệu; cần phân quyền theo từng tài liệu; cần nhiều trợ lý dùng chung một bộ nhớ quy tắc (hướng SAP Signavio). Lúc đó cân nhắc phần mềm quản lý tài liệu có phân quyền và lịch sử, hoặc thuê làm (xem `../rag-tra-cuu-tai-lieu/cap-09-van-hanh.md` Bài 9.9).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung:

- **Công ty logistics nội địa 60 người (Hà Nội):** trợ lý nội bộ trả lời tài xế và điều phối về quy trình giao hàng, đối soát COD (đối chiếu tiền thu hộ khi giao hàng). Người giữ sổ: trợ lý giám đốc vận hành. Mỗi khi bảng phí đổi, cổng xuất chặn bảng cũ, ca thử "phí giao nội thành dưới 3 kg" chạy lại trước khi trợ lý dùng bảng mới.
- **Phòng khám đa khoa tư nhân:** chỉ SOP hành chính (đặt lịch, thu phí, xuất hóa đơn) qua cổng xuất sang trợ lý lễ tân; mọi tài liệu chuyên môn y khoa mức "nhạy cảm" bị chặn khỏi trợ lý dùng dịch vụ AI bên ngoài.
- **Công ty phần mềm gia công 20 người (Đà Nẵng):** bài học sau sự cố triển khai (C5) và SOP phát hành (C2) là kho chung cho trợ lý lập trình; theo đúng cảnh báo của SAP, mỗi mục nhập kho phải có người duyệt và nguồn, chống ghi chú sai lan sang mọi người.

## 8. Tài liệu tham khảo

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| BMO ESCROW | https://arxiv.org/abs/2608.01772 | Qua `../nen-tang-bang-chung.md` | Cao |
| Airbnb Agentic RAG via Portable Skills | https://arxiv.org/abs/2610.14428 | Qua `../nen-tang-bang-chung.md` | Cao |
| SAP Shared Organizational Memory | https://arxiv.org/abs/2608.00122 | Qua `../nen-tang-bang-chung.md` | Cao về mô tả |
| SAP Signavio Organizational Memory | https://arxiv.org/abs/2607.03228 | Phần lớn | Trung bình |
| IBM Japan, Separation of Skilling Context | https://arxiv.org/abs/2611.11348 | Gần toàn văn | Trung bình |
| Nhóm RAG cap-03, cap-06, cap-09 | `../rag-tra-cuu-tai-lieu/` | Đã đọc phần liên quan | Nội bộ |

## 9. Chưa kiểm chứng

- Không có nguồn đo hiệu quả của "vận hành vòng tri thức" ở SME. Bảng chỉ số, lịch, ngưỡng 90%, 6 tháng, 300 tài liệu đều là đề xuất.
- Chưa so sánh công cụ quản lý tài liệu (Notion, Lark, Google Drive có nhãn, phần mềm trong nước) về phân quyền, lịch sử, nhắc hạn.
- Quy tắc "chủ tài liệu không tự duyệt" có thể không khả thi ở doanh nghiệp rất nhỏ; cần thử với người học.
