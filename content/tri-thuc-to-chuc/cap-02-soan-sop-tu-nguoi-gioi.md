# Cấp 2 (C2): Soạn SOP từ người làm giỏi bằng phỏng vấn có hướng dẫn

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác.
> Dùng lại, không viết lại: chuyển SOP thành prompt (`../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` Bài C0.3); chấm SOP từng bước (`../rag-tra-cuu-tai-lieu/cap-08-quy-trinh-nhieu-buoc.md` Bài 8.1). Cấp này lo phần **trước** đó: lấy SOP ra khỏi đầu người.

## 1. Mục tiêu và người đọc

**Người đọc:** chủ doanh nghiệp, trưởng bộ phận muốn "viết quy trình" nhưng chưa từng viết; nhân sự/đào tạo.

**Sau cấp này:**
1. Có **bộ câu hỏi phỏng vấn** chuẩn cho một quy trình.
2. Một quy trình quan trọng có **SOP v1** rút từ người làm giỏi, mỗi bước có người làm và nguồn (phút nào trong buổi phỏng vấn, tin nhắn nào).
3. SOP v1 đã được **người mới làm thử** và sửa theo chỗ kẹt.
4. Danh sách câu hỏi chưa ai trả lời được ghi rõ, không bị AI "điền cho đủ".

**Sản phẩm:** bộ câu hỏi; bản chép lời phỏng vấn; SOP v1 Markdown; nhật ký làm thử; script `kiem_sop.py`.

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Người làm giỏi biết làm nhưng không viết ra. Làm sao rút được quy trình đủ để người khác (và AI) làm theo?"*

Lỗi khi nhờ AI "viết SOP cho quy trình X" **[Đề xuất, quan sát]**: AI viết ra một SOP chung chung, đúng sách vở, sai với công ty. Không ai phát hiện vì nó trôi chảy. Bằng chứng gốc cho thấy chính chỗ thiếu này quyết định chất lượng AI về sau (mục 3.1).

## 3. Kiến thức nền

### 3.1 SOP thiếu bước là điểm nghẽn [Nguồn]

- **Airbnb** (arXiv 2610.14428, qua `../nen-tang-bang-chung.md`): phần lớn thất bại còn lại là do SOP **thiếu bước mà nhân viên giỏi vẫn làm**. Cải thiện cần viết thêm SOP, không phải sửa truy xuất.
- **IBM Japan** (arXiv 2611.11348): SOP được viết ngắn cho người đọc nên bỏ tri thức ngầm. Ví dụ của bài: SOP ghi "chi phí trên $250 cần quản lý duyệt", nhưng không nói $250 là **bao gồm hay không**, không nói lấy mã quản lý ở đâu. Bài chia phần thiếu thành 4 loại: **làm rõ quy trình**, **quy tắc riêng của tổ chức**, **ngoại lệ**, **chi tiết thực thi**. Hai loại đầu và ngoại lệ nên đưa vào SOP; chi tiết thực thi để ở tài liệu riêng (C3). Bài trích SOP-Bench: tác tử LLM chỉ thành công 27-48% trên SOP công nghiệp phức tạp (số thứ cấp, chưa đọc bài gốc).
- **Lưu ý về IBM:** tóm tắt bài ghi "8 quy trình, tỷ lệ tương đương chức năng tăng từ 12% lên 58%"; thân bài ghi 3 quy trình, 8/9 lần thử tương đương (89%). Hai chỗ không khớp. **Không trích các con số này**, chỉ dùng phân loại 4 loại.

### 3.2 AI làm người phỏng vấn được đến đâu [Nguồn]

- **Đại học Copenhagen** (arXiv 2610.23149): thí nghiệm ngẫu nhiên N=41 sinh viên, phỏng vấn qua chat bằng tiếng Anh. AI (mô hình mở 7B chạy cục bộ) hỏi 31 câu so với 14 câu của người phỏng vấn đã được huấn luyện (không phải chuyên gia); thu nhiều hơn khoảng 65% chữ mỗi buổi. Độ cụ thể của câu trả lời: không phát hiện khác biệt, nhưng thiết kế **không loại trừ** được chênh tới khoảng 0,75 điểm trên thang 5. Chỉ nhóm AI có người bấm bỏ qua câu hỏi (5/20 người). Ngày đầu AI hỏng (lặp câu, nói lan man), 4 buổi bị loại.
- **Kunumi/UFMG** (arXiv 2507.03811): tác tử LLM đi hỏi "nhân viên" để dựng lại mô tả một bảng dữ liệu; đạt 94,9% trên 864 mô phỏng. Nhưng **nhân viên cũng là LLM mô phỏng**. Bằng chứng yếu cho người thật.
- **[Đề xuất] Ý nghĩa:** AI giỏi hỏi đủ, hỏi nhiều, không mệt. Người giỏi hơn ở tạo tin tưởng và nhận ra chỗ "nói tránh". Với SME: để **người phỏng vấn**, AI **gợi ý câu hỏi đào sâu** và **kiểm khung còn thiếu gì**. Hoặc để AI hỏi qua chat, nhưng người xem lại toàn bộ.

### 3.3 Nguồn tri thức ở SME [Đề xuất]

1. Lời kể (phỏng vấn 30-45 phút, ghi âm có đồng ý, chép lời theo C1).
2. Quan sát làm thật (người phỏng vấn ghi các thao tác người làm giỏi **không kể**).
3. Tin nhắn Zalo/email cũ: nơi các ngoại lệ được xử lý ("lần trước khách X đổi thì mình làm sao?").
4. Biểu mẫu, file Excel đang dùng.

## 4. Chuỗi bài nhỏ

### Bài C2.1: Chọn quy trình và người
- **Thực hành:** liệt kê 10 quy trình; chấm (tần suất) × (thiệt hại khi làm sai) × (số người biết làm). Chọn quy trình điểm cao và chỉ 1-2 người biết. Chọn người làm giỏi **và** một người mới.
- **Sản phẩm:** bảng ưu tiên.
- **Lỗi thường gặp:** chọn quy trình dài nhất; chọn người giỏi nhưng không có thời gian.

### Bài C2.2: Bộ câu hỏi phỏng vấn
- **Thực hành [Đề xuất, dựa 4 loại của IBM]:** khung 9 câu, mỗi câu kèm câu đào sâu:
  1. Việc này bắt đầu khi nào? (cái gì kích hoạt)
  2. Cần những gì trong tay? (đầu vào, file, phần mềm)
  3. Anh/chị làm lần lượt thế nào? (từng bước, theo một ca **cụ thể gần nhất**)
  4. Ở bước nào phải quyết định? Dựa vào đâu? **Ngưỡng có tính đúng bằng không?**
  5. Lần gần nhất có gì khác thường? Xử lý sao? (ngoại lệ)
  6. Dấu hiệu nào cho biết đang sai?
  7. Ai cần được báo, khi nào?
  8. Người mới hay sai chỗ nào?
  9. Có quy định nào "ai cũng biết" mà chưa ghi ở đâu? (quy tắc riêng)
- **Sản phẩm:** bộ câu hỏi 1 trang.
- **Lỗi thường gặp:** hỏi "quy trình chung là gì" thay vì "kể lại ca hôm qua".

### Bài C2.3: Phỏng vấn có AI hỗ trợ
- **Đường A (người hỏi, AI gợi ý):** sau mỗi 10 phút, dán đoạn chép lời vào Project "Trợ lý phỏng vấn"; AI trả: (a) câu nào trong 9 câu chưa được trả lời; (b) 3 câu đào sâu, ưu tiên ngưỡng và ngoại lệ.
- **Đường B (AI hỏi qua chat):** người làm giỏi tự trả lời trong chat với chỉ dẫn "hỏi một câu một lần; không gợi ý câu trả lời; khi người trả lời nói 'thường thì', hỏi lại ca cụ thể". Người phỏng vấn đọc lại toàn bộ.
- **Đồng ý và dữ liệu:** buổi phỏng vấn là dữ liệu của người lao động (Điều 25 Luật 91/2025, xem `00-README.md` mục 6). Nói rõ mục đích, nơi lưu; sau khi SOP được duyệt, chỉ giữ SOP và các đoạn trích làm nguồn, xóa file âm thanh **[Đề xuất]**.
- **Sản phẩm:** bản chép lời có mốc thời gian.

### Bài C2.4: AI soạn SOP nháp có nguồn
- **Thực hành:** chỉ dẫn: "Chỉ dùng nội dung trong bản chép lời. Mỗi bước đánh mã B1, B2... ghi `[Ai: ...]` và `[Nguồn: mã phỏng vấn, phút]`. Chỗ nào chưa có câu trả lời, ghi `?? câu hỏi` và **không tự điền**." Mẫu SOP có 8 mục: Mục đích, Phạm vi, Người chịu trách nhiệm, Đầu vào, Các bước, Ngoại lệ, Đầu ra, Nguồn.
- **Sản phẩm:** SOP v0.
- **Lỗi thường gặp:** AI bổ sung "best practice" không ai nói; bước không có nguồn.

### Bài C2.5: Kiểm khung bằng code
- **Thực hành:** chạy `kiem_sop.py` (mục 5). Code không biết SOP đúng hay sai; nó chỉ chặn SOP **thiếu khung**: thiếu mục, bước không có người làm, bước không có nguồn, từ mơ hồ ("nếu cần", "tùy", "khoảng"), câu hỏi `??` chưa trả lời.
- **Sản phẩm:** danh sách cần hỏi lại.

### Bài C2.6: Người làm giỏi duyệt
- **Thực hành:** in SOP, người làm giỏi gạch sửa; trả lời các `??`. Chỉ người làm giỏi (hoặc trưởng bộ phận) được chuyển trạng thái sang "đã duyệt".
- **Lỗi thường gặp:** người giỏi duyệt qua loa vì "đọc thấy đúng" (giống lỗi duyệt ở C0).

### Bài C2.7: Người mới làm thử
- **Thực hành [Đề xuất]:** người mới làm 3 ca thật chỉ bằng SOP, có người giỏi ngồi cạnh nhưng **không nhắc**. Ghi mọi chỗ kẹt: bước nào, thiếu gì. Mỗi chỗ kẹt là một bước hay ngoại lệ còn thiếu (đúng loại lỗi Airbnb tìm ra).
- **Sản phẩm:** nhật ký làm thử; SOP v1.
- **Lỗi thường gặp:** để người giỏi "chỉ nhanh"; không ghi lại.

### Bài C2.8: Đưa sang dùng
- **Thực hành:** đăng ký SOP v1 vào sổ (C3); chuyển thành prompt theo `../rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.md` Bài C0.3; mỗi chỗ kẹt ở C2.7 thành một ca thử.

## 5. Đường không code vs có code

| | Không code | Có code nhẹ |
|---|---|---|
| Phỏng vấn | Project "Trợ lý phỏng vấn"; chép lời có sẵn | Script ghép chép lời + gọi API sinh câu hỏi đào sâu |
| Kiểm SOP | Bảng kiểm 8 mục bằng mắt | `kiem_sop.py` chặn thiếu khung trước khi tới người duyệt |

**Mã mẫu (đã chạy thử, `python -I -X utf8`):**

```python
import re
MUC_BAT_BUOC = ["Mục đích", "Phạm vi", "Người chịu trách nhiệm", "Đầu vào",
                "Các bước", "Ngoại lệ", "Đầu ra", "Nguồn"]
CO_MO_HO = re.compile(r"\b(thường thì|tùy|khoảng|nếu cần|linh hoạt|v\.v)\b", re.I)

def kiem_sop(md):
    loi = []
    tieu_de = re.findall(r"^##\s+(.+)$", md, re.M)
    for m in MUC_BAT_BUOC:
        if not any(t.strip().startswith(m) for t in tieu_de):
            loi.append(("THIEU_MUC", m))
    buoc = re.findall(r"^(B\d+)\.\s+(.+)$", md, re.M)
    if not buoc:
        loi.append(("KHONG_CO_BUOC_DANH_MA", ""))
    for ma, nd in buoc:
        if "[Ai:" not in nd:
            loi.append(("BUOC_THIEU_NGUOI_LAM", ma))
        if "[Nguồn:" not in nd:
            loi.append(("BUOC_THIEU_NGUON", ma))
        m = CO_MO_HO.search(nd)
        if m:
            loi.append(("TU_MO_HO", ma + ": " + m.group(0)))
    for cau in re.findall(r"\?\?\s*(.+)", md):
        loi.append(("CAU_HOI_CHUA_TRA_LOI", cau.strip()))
    return loi
```

Chạy thử với SOP "Xử lý đơn đổi hàng" giả: bắt thiếu mục "Người chịu trách nhiệm", "Nguồn"; B2 thiếu nguồn và có "nếu cần"; B3 thiếu người làm; câu "Hàng giảm giá có được đổi không" chưa trả lời.

**Khi nào buộc chuyển sang code [Đề xuất]:** > 5 SOP đang soạn cùng lúc; muốn chặn tự động trước khi tới người duyệt; muốn ghép nguồn (phút phỏng vấn) thành link.

## 6. Tiêu chí lên cấp [Đề xuất]

1. ≥ 3 quy trình có SOP v1 đã qua người giỏi duyệt **và** người mới làm thử 3 ca.
2. `kiem_sop.py` (hoặc bảng kiểm) không còn lỗi; mọi `??` đã có câu trả lời hoặc ghi rõ "chưa quyết, người quyết: X".
3. Ở lần làm thử thứ 3, người mới không kẹt ở bước nào chưa có trong SOP.
4. Bắt đầu có nhiều tài liệu đến mức không biết bản nào mới: đó là lúc cần C3.

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

- **Văn phòng kế toán dịch vụ 12 người (TP.HCM), quy trình "khóa sổ tháng cho khách hộ kinh doanh":** chỉ chị kế toán trưởng biết thứ tự đối chiếu. Câu ngưỡng quan trọng: "hóa đơn đầu vào trễ bao nhiêu ngày thì đưa sang kỳ sau?" Ngoại lệ lấy từ Zalo: khách gửi hóa đơn qua ảnh chụp. Không dán số liệu khách thật vào AI; dùng ca đã che mã số thuế.
- **Nhà hàng 2 chi nhánh (Cần Thơ), quy trình "nhận hàng tươi buổi sáng":** bếp trưởng kiểm cá bằng mắt, mũi. Phỏng vấn có quan sát tại chỗ (Bài C2.3 đường A) vì nhiều thao tác không được kể. Ngưỡng: "nhiệt độ thùng trên bao nhiêu độ thì trả hàng?"
- **Xưởng in bao bì 30 người, quy trình "duyệt file in của khách":** tin nhắn Zalo cũ chứa nhiều ngoại lệ ("file không viền chảy thì báo khách, không tự kéo"). Mỗi ngoại lệ thành một dòng trong mục Ngoại lệ, nguồn là ngày tin nhắn.

## 8. Tài liệu tham khảo

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| Separation of Skilling Context for SOP-based Agents (IBM Japan) | https://arxiv.org/abs/2611.11348 | Gần toàn văn | Trung bình (3 quy trình, số liệu tóm tắt và thân bài lệch nhau) |
| Can AI interview? AI-led vs Human-led Chat Interviews (Copenhagen) | https://arxiv.org/abs/2610.23149 | Phần chính và phụ lục | Cao cho bối cảnh của bài (sinh viên, tiếng Anh, chat) |
| LLMs for Tacit Knowledge Discovery in Organizational Contexts | https://arxiv.org/abs/2507.03811 | Phần chính | Thấp cho người thật (mô phỏng toàn bộ) |
| Airbnb Agentic RAG via Portable Skills | https://arxiv.org/abs/2610.14428 | Qua `../nen-tang-bang-chung.md` | Cao |
| SOP-Bench (trích lại trong bài IBM) | (chưa tra) | Không đọc | Thấp |

## 9. Chưa kiểm chứng

- Chưa có nghiên cứu nào đo AI phỏng vấn **bằng tiếng Việt** hay phỏng vấn để **rút quy trình nghề** (bài Copenhagen về trải nghiệm học tập).
- Bộ 9 câu hỏi và cách làm thử 3 ca là đề xuất, chưa đo.
- Các con số trong bài IBM (12% → 58%, 89%, 79,5%) chưa dùng vì mâu thuẫn nội bộ.
- Thời gian gõ lại, thời gian phỏng vấn cần cho một quy trình: chưa có số.
- Việc giữ đoạn trích phỏng vấn làm nguồn sau khi nhân viên nghỉ (liên quan Điều 25 khoản 2) cần hỏi luật sư.
