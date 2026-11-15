# Cấp 1 (C1): Ghi âm tiếng Việt thành văn bản, đo được và hợp lệ

> Ngày soạn: 2026-11-11. **[Nguồn]** / **[Đề xuất]** như các file khác. Không phải tư vấn pháp lý.
> Dùng lại: CER và kiểm bằng mẫu (`../rag-tra-cuu-tai-lieu/cap-02-tai-lieu-thanh-text.md` Bài 2.4); gọi API (`../rag-tra-cuu-tai-lieu/cap-01-goi-api.md`); khoảng tin cậy khi n nhỏ (`../rag-tra-cuu-tai-lieu/cap-06-danh-gia.md`).

!!! tip "Tóm tắt nhanh"
    Ở cấp trước (C0), biên bản họp dựa vào ghi chú tay, nên hay sót. Bài này giúp bạn chuyển sang **ghi âm cuộc họp rồi để máy chép lời thành chữ**. Nhưng máy chép tiếng Việt có thể sai rất nặng, và ghi âm lại đụng đến **dữ liệu cá nhân**. Vì vậy bạn sẽ làm ba việc: đặt quy tắc ghi âm cho công ty, **tự đo** xem công cụ nào chép đủ tốt trên chính giọng nói của công ty bạn, và lập từ điển tên riêng để kiểm tra. Cuối bài bạn biết khi nào bản chép lời đủ tin để dùng, khi nào thì chưa.

## 1. Mục tiêu và người đọc

**Bài này dành cho ai:** người đã làm xong cấp C0 và muốn bỏ ghi chú tay; người phụ trách IT hoặc hành chính của công ty. Bạn không cần biết lập trình. Những chỗ có đoạn mã, bạn chỉ cần nhờ người biết code (hoặc nhờ AI) chạy giúp.

**Bạn cần chuẩn bị:**
- Kết quả của cấp C0 (mẫu biên bản và cách làm biên bản).
- Khoảng 10-15 phút ghi âm họp thật của công ty, được những người trong cuộc họp đồng ý cho ghi (Bài C1.2 sẽ nói rõ cách chọn đoạn).
- Một người chịu khó gõ lại chính xác nội dung các đoạn ghi âm đó thành chữ, để làm "đáp án".
- Một bảng tính (Google Sheet hoặc Excel) để lập từ điển tên riêng.
- Các công cụ chép lời bạn muốn thử, ví dụ tính năng có sẵn của phần mềm họp, một dịch vụ chép lời trên mạng, hoặc mô hình mở PhoWhisper (xem mục 3.5).

**Sau bài này bạn sẽ có:**
1. Có **quy tắc ghi âm** 1 trang: thông báo, đồng ý, nơi lưu, thời hạn xóa.
2. Đã **tự đo** 2-3 cách chép lời trên 10-15 phút ghi âm họp thật của công ty.
3. Có **từ điển tên riêng** (người, khách, sản phẩm, mã hàng) dùng để sửa và kiểm.
4. Biết khi nào bản chép lời **không đủ tốt** để đưa vào C0.

**Thứ bạn cầm đi được sau bài:** quy tắc ghi âm; bảng so sánh công cụ (WER, CER, tỷ lệ giữ tên riêng/con số); từ điển tên riêng; script `do_asr.py`. (Script là một đoạn chương trình ngắn. WER và CER là hai cách tính tỷ lệ chép sai, được giải thích ở mục 3.1.)

## 2. Câu hỏi cấp này trả lời / lỗi của cấp trước

*"Ghi âm rồi để máy chép lời có đủ tin để làm biên bản không, và có được phép ghi không?"*

Lỗi của C0: ghi chú tay sót; người ghi cũng là người phát biểu. Nhưng thêm ghi âm là thêm hai rủi ro: **chép sai** (tên người, con số) và **dữ liệu cá nhân** (giọng nói, nội dung).

!!! tip "Nói đơn giản"
    Ghi âm giải quyết chuyện "ghi chú tay bị sót", nhưng đổi lại bạn phải lo hai chuyện mới. Một là máy nghe nhầm, nhất là tên người và con số, đúng những thứ quan trọng nhất trong biên bản. Hai là giọng nói và nội dung cuộc họp là dữ liệu của con người, nên phải ghi đúng quy tắc.

## 3. Kiến thức nền

### 3.1 Chất lượng chép lời tiếng Việt: chênh rất lớn [Nguồn]

Trước hết là hai thước đo bạn sẽ gặp suốt bài này.

**WER** (tỷ lệ lỗi từ) = (thay + xóa + chèn) / số từ của bản đúng. Nói cách khác: lấy số chỗ máy chép sai (từ bị thay bằng từ khác, từ bị bỏ mất, từ bị thêm vào thừa), chia cho tổng số từ trong bản đúng. Con số càng thấp càng tốt. Tiếng Việt viết theo âm tiết (mỗi tiếng là một âm tiết) nên WER gần với tỷ lệ lỗi âm tiết. **CER** cũng tính như vậy nhưng trên **ký tự** (từng chữ cái) thay vì từng từ.

Bảng dưới đây là các số liệu mà những nhóm nghiên cứu đã đo. Vài thuật ngữ trong bảng: *tinh chỉnh* là huấn luyện thêm một mô hình có sẵn bằng dữ liệu của một ngôn ngữ cụ thể để nó làm tốt hơn; *Whisper* là một mô hình chép lời phổ biến; *batch* là chép lời cả file ghi âm đã có sẵn.

| Nguồn | Điều kiện | Số liệu |
|---|---|---|
| PhoWhisper (VinAI, arXiv 2406.02555) | Mô hình mở, tinh chỉnh Whisper trên 844 giờ, giọng 63 tỉnh thành | WER bản `large`: CommonVoice-vi 8,14%; VIVOS 4,67%; VLSP2020 Task-1 13,75%; VLSP2020 Task-2 26,68%. Bản `small`: 11,08 / 6,33 / 15,93 / 32,96% |
| PhoASR (Qualcomm, arXiv 2603.14779) | Bộ thử tổng hợp từ 11 bộ dữ liệu | `whisper-small` gốc chưa tinh chỉnh: WER 64,07% (không tính dấu câu, hoa thường) và 70,16% (có tính). Sau tinh chỉnh: 8,69% và 12,46% |
| PhoASR, theo vùng giọng | `whisper-small` tinh chỉnh 192 giờ cân bằng 3 miền | WER: Bắc 12,18%, Trung 16,56%, Nam 12,36%. Giọng miền Trung khó nhất trong mọi cấu hình |
| PhoASR, chất lượng dữ liệu | Lọc bộ dữ liệu công khai | Chỉ giữ ~62% dữ liệu sau lọc; bộ y khoa VietMed-L chỉ giữ ~26%. Nghĩa là nhãn của nhiều bộ dữ liệu công khai có sai |
| mu-bench (Sierra AI, arXiv 2609.32082) | 975 câu tiếng Việt qua điện thoại 8 kHz, khách đóng vai gọi tổng đài ngân hàng | Tỷ lệ câu **sai nghĩa** (UER, do LLM chấm, đồng thuận với người κ=0,78 trên cả 5 ngôn ngữ): Google Chirp-3 batch 6,7%; Microsoft Azure batch 22,1%; ElevenLabs Scribe v2 24,2%; OpenAI GPT-4o Mini Transcribe batch 40,1%; Deepgram Nova-3 50,8% |

Cách đọc bảng cho người không chuyên: hàng đầu cho thấy một mô hình mở được tinh chỉnh cho tiếng Việt đạt WER từ khoảng 4,67% đến 26,68% tùy bộ thử. Hàng thứ hai cho thấy cùng loại mô hình, nếu **chưa** tinh chỉnh thì sai rất nặng (WER 64,07%), còn sau tinh chỉnh chỉ còn 8,69%. Hàng thứ ba cho thấy giọng miền Trung khó nhất. Hàng thứ tư cho thấy nhiều bộ dữ liệu công khai có nhãn sai. Hàng cuối đo bằng cách khác: UER là tỷ lệ câu mà bản chép bị **sai nghĩa**, do một mô hình ngôn ngữ lớn (LLM, tức loại AI chat như ChatGPT, Claude) chấm; chữ κ (kappa) là chỉ số cho biết người và LLM chấm giống nhau đến mức nào. Hàng này là tổng đài ngân hàng qua điện thoại chất lượng thấp (8 kHz), không phải họp.

**Ý nghĩa [Đề xuất]:** (1) một mô hình phổ thông chưa tinh chỉnh có thể sai rất nặng với tiếng Việt; (2) cùng một nhà cung cấp, chế độ chạy (batch hay streaming) cho kết quả khác nhau (mu-bench nêu 2-4 điểm); (3) không bảng xếp hạng nào đo **họp tiếng Việt**. Vì vậy phải tự đo.

(Streaming là chép lời trực tiếp ngay khi người ta đang nói, khác với batch là chép sau khi đã có cả file.)

!!! tip "Nói đơn giản"
    Con số của người khác chỉ cho bạn biết "máy hay sai cỡ nào", không cho bạn biết "máy sai bao nhiêu ở công ty mình". Chưa ai đo họp tiếng Việt, nên cách duy nhất là bạn tự thử trên giọng nói của chính mình. Đó là việc của Bài C1.2 và C1.3.

### 3.2 WER không nói hết [Nguồn]

- mu-bench: WER coi "hi" và "hey" là lỗi ngang "cat" và "cap". Ở các câu chứa tên, email, mã số, WER chuẩn hóa **thấp hơn** (15,0% so với 18,7%) nhưng tỷ lệ câu sai nghĩa **cao hơn** (28,6% so với 17,0%).
- OSynth (Otter.ai, arXiv 2610.29319, tiếng Anh tổng hợp): khoảng 2/3 lỗi chép lời rơi vào tên riêng, con số/ngày, thuật ngữ. Đúng các thứ quyết định giá trị biên bản.
- **[Đề xuất]** Ngoài WER/CER, đo thêm **tỷ lệ giữ thực thể**: trong danh sách tên người, khách, mã hàng, con số có trong đoạn thử, bao nhiêu xuất hiện đúng trong bản chép. ("Thực thể" ở đây là những thứ cụ thể cần giữ đúng: tên, mã, con số, ngày.)

!!! tip "Nói đơn giản"
    WER đếm mọi từ sai như nhau. Nhưng nhầm "ạ" thành "à" khác hẳn nhầm "120 thùng" thành "12 thùng". Vì vậy ngoài WER, bạn nên đếm riêng: những tên và con số quan trọng, máy giữ đúng được bao nhiêu phần trăm.

### 3.3 Đừng để AI "sửa" bản chép lời quá tệ [Nguồn]

OSynth phụ lục V: khi đưa bản chép có WER khoảng 0,56 cho một LLM với lệnh "chỉ sửa thuật ngữ, không diễn giải", LLM **xóa trung bình ~25% số từ**; 13% lượt nói mất hơn nửa số từ, không báo. Với bản chép tốt (WER khoảng 0,10), cùng lệnh gần như không đổi gì. **[Đề xuất]** Quy tắc: đo trước; nếu bản chép tệ, sửa bằng người hoặc đổi công cụ, không nhờ LLM "làm sạch".

!!! tip "Nói đơn giản"
    Khi bản chép quá tệ, nhờ AI "sửa cho đẹp" lại làm mất cả nội dung mà không báo cho bạn. Nếu bản chép tệ, hãy nhờ người sửa hoặc đổi công cụ chép lời, đừng nhờ AI làm sạch.

### 3.4 Pháp lý khi ghi âm cuộc họp [Nguồn, xác minh một phần]

Phần này **không phải tư vấn pháp lý**. Chỉ là tóm tắt điều nhóm soạn đã đọc, để bạn biết cần hỏi luật sư những gì.

Đọc qua hethongphapluat.com (trang đăng lại văn bản), **chưa đối chiếu Công báo**:
- **Điều 32 Luật 91/2025/QH15** (ghi âm, ghi hình nơi công cộng, hoạt động công cộng): người bị ghi phải được biết, trừ khi luật quy định khác; dùng đúng mục đích; chỉ lưu trong thời gian cần thiết, hết hạn thì xóa, hủy.
- **Điều 25** (dữ liệu trong tuyển dụng, quản lý người lao động), khoản 3: biện pháp công nghệ, kỹ thuật trong quản lý lao động phải hợp pháp và người lao động phải được biết rõ; không được dùng dữ liệu thu bằng biện pháp trái luật.
- NĐ 356/2025 (theo EY, xem `../an-toan-du-lieu-va-phap-ly-vn.md`): đồng ý phải kiểm chứng và lưu được.

**[Đề xuất]** Họp nội bộ có phải "hoạt động công cộng" không: chưa rõ. Cách an toàn: coi bản ghi là dữ liệu cá nhân. Thông báo trong lịch họp; nói lại đầu cuộc họp (và để câu đó nằm trong bản ghi); cho phép tắt ghi ở phần nhạy cảm (nhân sự, lương, kỷ luật); xóa file âm thanh sau khi biên bản được duyệt, ví dụ 30 ngày.

!!! tip "Nói đơn giản"
    Vì chưa rõ luật có áp dụng cho họp nội bộ hay không, cách an toàn là cư xử như thể có: báo trước cho mọi người, nói lại ngay đầu cuộc họp, tắt ghi ở phần nhạy cảm, và xóa file ghi âm sau khi biên bản đã duyệt. Những điểm còn mơ hồ nên hỏi luật sư.

### 3.5 Ba đường chép lời [Đề xuất]

1. **Tính năng có sẵn** của Meet/Teams/Zoom/Lark: tiện, nhưng hỗ trợ tiếng Việt chưa xác minh được (mục 9).
2. **API đám mây** (Google, Azure, OpenAI, ElevenLabs...): đo được bằng mu-bench ở điều kiện điện thoại; dữ liệu ra nước ngoài. (API là cách để chương trình của bạn gửi âm thanh lên dịch vụ của hãng khác và nhận lại chữ.)
3. **Mô hình mở chạy trên máy công ty** (PhoWhisper): âm thanh không rời công ty. Cần máy đủ mạnh; tốc độ chưa đo trong tài liệu này.

## 4. Chuỗi bài nhỏ

Năm bài thực hành dưới đây làm theo thứ tự. Mỗi bài có: việc cần làm, thứ bạn có sau bài, và (ở các bài có nêu) lỗi hay gặp để tránh.

### Bài C1.1: Quy tắc ghi âm 1 trang
- **Việc cần làm:** ghi ra giấy hoặc tài liệu: cuộc họp nào được ghi; câu thông báo mẫu; ai giữ file; lưu ở đâu (tài khoản công ty, không phải điện thoại cá nhân); xóa sau bao lâu; phần họp nào không ghi; dịch vụ nào được dùng.
- **Bạn có sau bài:** quy tắc, nhân viên ký đã đọc.
- **Lỗi hay gặp:** ghi âm bằng điện thoại cá nhân rồi gửi qua Zalo; giữ file mãi mãi.

### Bài C1.2: Dựng đoạn thử có đáp án
- **Việc cần làm:** chọn 3 đoạn, mỗi đoạn 3-5 phút, từ họp thật đã được đồng ý ghi: một đoạn yên tĩnh, một đoạn nói chồng, một đoạn có người giọng vùng khác. Một người gõ lại chính xác (mất khoảng vài lần thời lượng đoạn, chưa đo). Lập danh sách thực thể trong mỗi đoạn: tên, khách, mã hàng, con số, ngày.
- **Bạn có sau bài:** 3 cặp (âm thanh, bản đúng) + danh sách thực thể. "Bản đúng" chính là đáp án để so với bản máy chép.
- **Lỗi hay gặp:** chọn đoạn dễ nhất; gõ lại "cho gọn" thay vì nguyên văn.

### Bài C1.3: Đo 2-3 công cụ
- **Việc cần làm:** chạy cùng 3 đoạn qua 2-3 cách (ví dụ một tính năng có sẵn, một API, PhoWhisper). Tính WER, CER, tỷ lệ giữ thực thể bằng `do_asr.py`.
- **Chuẩn hóa trước khi so [Đề xuất]:** chữ thường, bỏ dấu câu, NFC (một chuẩn mã hóa chữ có dấu, để cùng một chữ luôn được lưu theo một cách), **thống nhất vị trí dấu thanh** ("hoà"/"hòa", "thuý"/"thúy"); quyết định "120" và "một trăm hai mươi" có tính là đúng không (nên tính đúng nếu nghĩa không đổi, như mu-bench).
- **Bạn có sau bài:** bảng so sánh.
- **Lỗi hay gặp:** so trên đoạn khác nhau; quên chuẩn hóa dấu thanh nên WER cao oan.

### Bài C1.4: Từ điển tên riêng
- **Việc cần làm:** lập Sheet 2 cột: cách viết đúng, các cách chép sai hay gặp ("Hòa Phát" / "hoà phát", "Hoa Phat"). Dùng để (a) đưa vào prompt C0 làm danh sách chuẩn; (b) kiểm tỷ lệ giữ thực thể. (Prompt là đoạn chỉ dẫn bạn gõ cho AI.) Nếu công cụ cho "gợi ý từ vựng" thì nạp vào (kiểm tính năng trước).
- **Bạn có sau bài:** từ điển 30-100 mục.

### Bài C1.5: Ngưỡng dùng được
- **Việc cần làm [Đề xuất]:** đặt ngưỡng trước khi xem kết quả: ví dụ tỷ lệ giữ thực thể ≥ 90% và không đoạn nào CER > 15% thì dùng cho C0 có duyệt; dưới ngưỡng thì chỉ dùng làm "trợ nhớ" cho người viết biên bản.
- **Bạn có sau bài:** dòng quyết định trong Sổ prompt (sổ ghi các chỉ dẫn bạn dùng cho AI, đã lập ở cấp C0).

## 5. Đường không code vs có code

Bài này có hai cách làm. Cách 1 không cần code, đủ dùng khi mới bắt đầu. Cách 2 cần một chút lập trình, để máy tự đo thay cho người.

| | Không code | Có code nhẹ |
|---|---|---|
| Chép lời | Tính năng có sẵn của phần mềm họp | API hoặc PhoWhisper chạy cục bộ |
| Đo | Đếm tay lỗi tên/con số trên 3 đoạn | `do_asr.py` tính WER/CER/thực thể |

**Đoạn mã dưới đây làm gì?** Nó làm bốn việc. Một, "chuẩn hóa" văn bản: đổi về chữ thường, thống nhất cách đặt dấu thanh, bỏ dấu câu. Hai, đếm số chỗ khác nhau giữa bản đúng và bản máy chép. Ba, từ đó tính WER và CER. Bốn, kiểm xem các tên và con số quan trọng có còn đúng trong bản chép không. Bạn **không cần đọc hiểu từng dòng**; chỉ cần biết ý nghĩa của nó, và nhờ một người biết lập trình (hoặc nhờ AI) chạy giúp khi cần.

**Mã mẫu (đã chạy thử, `python -I -X utf8`):**

```python
import re, unicodedata
DAU = {"oà": "òa", "oá": "óa", "oả": "ỏa", "oã": "õa", "oạ": "ọa",
       "oè": "òe", "oé": "óe", "oẻ": "ỏe", "oẽ": "õe", "oẹ": "ọe",
       "uỳ": "ùy", "uý": "úy", "uỷ": "ủy", "uỹ": "ũy", "uỵ": "ụy"}

def chuan(s):
    s = unicodedata.normalize("NFC", s).lower()
    for moi, cu in DAU.items():
        s = s.replace(moi, cu)
    return re.sub(r"[^\w\s]", " ", s).split()

def khoang_cach(a, b):
    d = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(b) + 1):
            cur = d[j]
            d[j] = min(d[j] + 1, d[j - 1] + 1, prev + (a[i - 1] != b[j - 1]))
            prev = cur
    return d[len(b)]

def wer(ref, hyp):
    r, h = chuan(ref), chuan(hyp)
    return khoang_cach(r, h) / max(len(r), 1)

def cer(ref, hyp):
    r, h = "".join(chuan(ref)), "".join(chuan(hyp))
    return khoang_cach(list(r), list(h)) / max(len(r), 1)

def giu_thuc_the(hyp, thuc_the):
    h = " ".join(chuan(hyp))
    giu = [t for t in thuc_the if " ".join(chuan(t)) in h]
    return len(giu) / max(len(thuc_the), 1), sorted(set(thuc_the) - set(giu))
```

**Kết quả chạy thử:** bản đúng là "Anh Tuấn chốt giao 120 thùng cho Hòa Phát ngày 15 tháng 11", bản chép là "anh tuấn chốt giao một trăm hai mươi thùng cho hoà phát ngày 15 tháng 11". **Không** thống nhất dấu thanh: WER 0,38, giữ thực thể 50% (mất "Hòa Phát" và "120"). **Có** thống nhất dấu thanh: WER 0,31, giữ thực thể 75% (chỉ còn "120" viết bằng chữ). Bài học: lỗi đo có thể lớn hơn lỗi máy; phải chuẩn hóa trước khi kết luận.

!!! tip "Nói đơn giản"
    Máy chép "hoà phát" còn bạn viết "Hòa Phát": hai cách viết đều đúng, nhưng nếu không thống nhất thì phép đo coi là sai và điểm bị thấp oan. Vì vậy đừng so sánh công cụ khi chưa chuẩn hóa chữ.

**Khi nào buộc chuyển sang code [Đề xuất]:** muốn so công cụ một cách công bằng; muốn âm thanh không rời công ty (chạy PhoWhisper); hơn khoảng 5 giờ ghi âm/tuần.

## 6. Tiêu chí lên cấp [Đề xuất]

Bạn có thể sang cấp tiếp theo khi đạt đủ các điều sau:
1. Có quy tắc ghi âm đã ký; 100% file ghi âm nằm ở nơi lưu của công ty, có ngày xóa.
2. Đã đo ≥ 2 công cụ trên ≥ 3 đoạn có đáp án; công cụ chọn đạt ngưỡng ở Bài C1.5.
3. Biên bản C0 làm từ bản chép lời không làm tăng số việc bịa/sót so với ghi chú tay (so trên ≥ 5 cuộc họp).

## 7. Ví dụ cho SME Việt Nam [Đề xuất, minh họa]

Ba tình huống giả định để bạn dễ hình dung:

- **Trung tâm tiếng Anh 3 cơ sở (Hà Nội), họp giáo viên trộn Việt-Anh:** "deadline", "placement test", tên lớp "IELTS 6.5 tối 2-4-6". Lỗi dự kiến: thuật ngữ tiếng Anh bị phiên âm. Từ điển tên riêng có cả thuật ngữ Anh. (Chép lời trộn Việt-Anh là một hướng nghiên cứu riêng, ví dụ arXiv 2509.05983; chưa đọc.)
- **Công ty vận tải 25 xe (Đà Nẵng), họp điều độ có tài xế giọng miền Trung:** PhoASR cho thấy giọng miền Trung khó nhất. Đoạn thử phải có giọng này; nếu thực thể (biển số, tên tuyến) giữ dưới ngưỡng, giữ ghi chú tay cho phần điều độ.
- **Cửa hàng mỹ phẩm online, họp qua Google Meet với cộng tác viên:** không ghi âm phần nói về khách cụ thể; nếu có, thay tên khách bằng mã trước khi đưa bản chép cho AI.

## 8. Tài liệu tham khảo

| Tài liệu | URL | Đã đọc | Tin cậy |
|---|---|---|---|
| PhoWhisper: ASR for Vietnamese (VinAI) | https://arxiv.org/abs/2406.02555 | Toàn văn (bài 2 trang) | Cao; bộ thử là đọc/tin tức, không phải họp |
| Vietnamese ASR: A Revisit (PhoASR, Qualcomm) | https://arxiv.org/abs/2603.14779 | Gần toàn văn | Cao |
| mu-bench: Multilingual Utterance Transcription (Sierra AI) | https://arxiv.org/abs/2609.32082 | Toàn văn | Cao cho điện thoại, đóng vai ngân hàng; không phải họp |
| OSynth (Otter.ai) | https://arxiv.org/abs/2610.29319 | Phần chính, phụ lục E, V | Trung bình (tổng hợp, tiếng Anh) |
| Điều 25, 32 Luật BVDLCN 2025 (hethongphapluat.com) | https://hethongphapluat.com/luat-bao-ve-du-lieu-ca-nhan-2025/dieu-32 | Đọc qua công cụ tóm tắt, có trích ngắn | Trung bình (trang đăng lại, chưa đối chiếu Công báo) |
| Google Workspace Updates: more languages for "take notes for me" (3/2025) | https://workspaceupdates.googleblog.com/2025/03/more-languages-for-take-notes-for-me-in-google-meet.html | Chỉ qua kết quả tìm kiếm | Thấp |

## 9. Chưa kiểm chứng

- **Chưa có số đo chép lời cho họp tiếng Việt** (nhiều người, nói chồng, micro laptop). Các số ở 3.1 là đọc, tin tức, điện thoại.
- VLSP2020 Task-2 là loại âm thanh gì (bài PhoWhisper không mô tả); không suy diễn thêm.
- Google Meet "Take notes for me": bài 3/2025 thêm 7 ngôn ngữ, **không có tiếng Việt**; danh sách hiện tại chưa đọc. Teams Copilot, Zoom AI Companion, Lark Minutes: chưa xác minh hỗ trợ tiếng Việt và gói nào.
- Tốc độ chạy PhoWhisper trên máy văn phòng không có GPU: chưa đo. (GPU là card đồ họa, giúp chạy mô hình AI nhanh hơn.)
- Họp nội bộ có thuộc Điều 32 không; giọng nói có phải dữ liệu sinh trắc học không: cần luật sư.
- Thời hạn xóa 30 ngày và các ngưỡng ở Bài C1.5 là đề xuất.
- Tên mô hình trong mu-bench (ví dụ "gpt-6-astra" làm giám khảo) lấy nguyên văn bài; chưa đối chiếu nhà cung cấp.
