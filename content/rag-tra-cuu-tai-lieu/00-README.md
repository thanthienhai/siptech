# Nhóm bài: Tra cứu thông tin trên một tập tài liệu (RAG)

> Thuộc series "AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp".
> Quy ước: **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = suy luận hoặc thiết kế của nhóm soạn. Mọi ngưỡng, cỡ mẫu là [Đề xuất].
> Không phải tư vấn pháp lý. Đọc kèm [An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md).

!!! tip "Tóm tắt nhanh"
    Nhóm bài này dạy cách để nhân viên (hoặc khách) **hỏi một câu và nhận câu trả lời lấy từ chính tài liệu của công ty**, kèm trích dẫn nguyên văn, hoặc nhận câu "tài liệu chưa đủ căn cứ" thay vì một câu trả lời bịa. Bạn đi từ dùng AI bằng tay, đến để máy tìm và trả lời, rồi đo xem nó đúng đến đâu và giữ cho nó chạy ổn. Đây cũng là nhóm nền: các nhóm bài khác dùng lại nhiều khối ở đây (dùng AI thủ công, gọi API, đánh giá, công cụ, vận hành).

## 1. Bài toán

**Ai gặp việc này:** chủ doanh nghiệp nhỏ, quản lý, nhân viên kinh doanh, kế toán, nhân sự, bất kỳ ai hay phải lục lại bảng giá, chính sách đổi trả, hợp đồng mẫu, quy trình nội bộ để trả lời một câu hỏi.

**Hằng ngày nó trông thế nào:** nhân viên mới hỏi "khách mua sỉ được chiết khấu bao nhiêu?"; người cũ phải nhớ hoặc lật lại tài liệu; mỗi người trả lời một kiểu; tài liệu có bản cũ lẫn bản mới. Nhờ AI trả lời thì nhanh, nhưng nếu AI không dựa vào đúng tài liệu thì nó dễ nói sai mà vẫn nghe rất đúng.

**Đầu vào:** một tập tài liệu nội bộ (bảng giá, chính sách, hợp đồng, quy trình) và câu hỏi của nhân viên hoặc khách.
**Đầu ra:** câu trả lời có trích dẫn nguyên văn từ tài liệu, hoặc từ chối khi tài liệu không đủ căn cứ.

!!! tip "Nói đơn giản"
    RAG là viết tắt của một cách làm quen thuộc: **tìm đoạn tài liệu liên quan trước, rồi mới đưa cho AI đọc và trả lời**. Giống như nhờ một nhân viên mở đúng trang sổ tay rồi đọc to cho bạn nghe, chứ không phải nhờ họ nhớ từ trí nhớ.

Đây là ví dụ xuyên suốt của series: đi từ dùng AI thủ công, gọi API, biến tài liệu thành văn bản (text), chia khối, tìm kiếm, trả lời có trích dẫn, đánh giá, công cụ, quy trình nhiều bước, đến vận hành. Mỗi cấp có hai đường: **không code** (dùng Project, Gem, GPT tùy chỉnh, là các tính năng cho bạn lưu sẵn chỉ dẫn và tài liệu để dùng lại) và **code nhẹ** (Python, một ngôn ngữ lập trình phổ biến).

Có sẵn một bộ slide minh họa 33 trang cho nhóm này: [tải file PowerPoint](RAG-tra-cuu-tai-lieu-C0-C9.pptx).

## 2. Vì sao bài toán này quan trọng với SME

**Quy trình và tài liệu thường nằm rải rác.** Ở SME, câu trả lời nằm trong file Excel của kế toán, trong tin nhắn Zalo, trong đầu vài người làm lâu năm. Việc đầu tiên là gom và làm sạch chúng; AI chỉ phát huy khi tài liệu đã có.

**AI trả lời sai ở đâu?** Nó hay "nói thêm" từ trí nhớ của nó thay vì từ tài liệu của bạn, và hiếm khi tự nói "tôi không biết". Vì vậy nhóm bài này đặt trọng tâm vào hai việc: bắt AI trích đúng nguyên văn, và đo xem nó trả lời đúng bao nhiêu thay vì tin cảm giác.

!!! tip "Nói đơn giản"
    Điểm mấu chốt của cả nhóm: kết quả tốt đến từ **tài liệu đủ và sạch, quy trình rõ, có đo và có người duyệt**, không đến từ việc mua công cụ đắt tiền. Đó là những việc doanh nghiệp nhỏ làm được.

## 3. Bằng chứng tóm tắt

Các số dưới đây lấy từ năm bài báo mà SIPTech đã đọc kỹ, chi tiết ở [Nền tảng bằng chứng](../nen-tang-bang-chung.md). Tất cả đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh, chưa có số đo trên SME Việt Nam.

| Phát hiện | Nguồn | Ý nghĩa cho SME |
|---|---|---|
| 70% hệ thống AI đang chạy thật dùng prompt trên mô hình có sẵn; 68% chạy dưới 10 bước rồi chuyển cho người **[Nguồn]** | MAP, arXiv 2512.04123 | Hệ thống hẹp, ít bước, có người duyệt là mô hình thực tế, không cần xây hệ thống lớn |
| Airbnb sinh hướng dẫn từ 2.881 bài quy trình, kiểm bằng code rằng mọi đoạn trích đều là chuỗi con nguyên văn của bài nguồn; kết quả 100% đoạn trích hợp lệ **[Nguồn]** | Airbnb, arXiv 2610.14428 | Hàng rào bằng code đáng tin hơn chỉ nhắc trong prompt |
| Thử BM25 riêng, vector riêng, và bỏ từng phần của lớp điều hướng: không cấu hình nào khác hệ thống đầy đủ ở mức ý nghĩa thống kê (p nhỏ nhất 0,078, n=132) **[Nguồn]** | Airbnb, arXiv 2610.14428 | Kiểu tìm kiếm quan trọng ít hơn người ta tưởng |
| Phần thất bại còn lại chủ yếu do quy trình (SOP) thiếu bước mà nhân viên giỏi vẫn làm **[Nguồn]** | Airbnb, arXiv 2610.14428 | Muốn tốt hơn thì viết thêm SOP, không phải đổi công cụ tìm |

!!! tip "Nói đơn giản"
    Ba chữ cần nhớ khi đọc bảng: **BM25** là cách tìm theo từ khóa như ô tìm kiếm thông thường; **vector** là cách tìm theo nghĩa; **SOP** là quy trình làm việc chuẩn viết thành văn bản.

## 4. Thang cấp độ

Mười cấp từ C0 đến C9, đi theo thứ tự. Mỗi cấp có một thứ bạn cầm đi được, nên dừng ở cấp nào cũng đã có kết quả dùng được.

| Cấp | Nội dung | Sản phẩm cầm đi được |
|---|---|---|
| [C0](cap-00-dung-ai-thu-cong.md) | Dùng AI thủ công có kỷ luật, prompt như bản giao việc | Bản giao việc sáu phần, nhật ký thử |
| [C1](cap-01-goi-api.md) | Gọi AI qua API, chi phí token, structured output | Script gọi API có log và kiểm JSON |
| [C2](cap-02-tai-lieu-thanh-text.md) | PDF/scan thành text có cấu trúc; kiểm chất lượng | Text có cấu trúc và báo cáo chất lượng |
| [C3](cap-03-chia-khoi-va-chi-muc.md) | Chia khối theo tiêu đề, mã ổn định, cập nhật | Bộ khối có mã và chỉ mục |
| [C4](cap-04-tim-kiem.md) | BM25, vector, lai; đo recall@k và MRR | Tìm kiếm có số đo |
| [C5](cap-05-tra-loi-co-trich-dan.md) | Trả lời có trích dẫn, kiểm nguyên văn bằng code | Trả lời có căn cứ hoặc từ chối |
| [C6](cap-06-danh-gia.md) | Bộ ca mẫu, LLM-as-judge, khoảng tin cậy khi n nhỏ | Bảng đánh giá theo từng ca |
| [C7](cap-07-cong-cu-tool.md) | Function calling, hàm đọc/ghi, prompt injection, MCP | Công cụ chia hạng A-D |
| [C8](cap-08-quy-trinh-nhieu-buoc.md) | Workflow so với agent, điểm duyệt của người | Quy trình có điểm duyệt |
| [C9](cap-09-van-hanh.md) | Log, phiên bản prompt, kiểm tra trước phát hành, trôi dạt | Nhịp vận hành và cổng phát hành |

**Nên bắt đầu từ cấp nào? [Đề xuất]**
- Chưa từng dùng AI cho công việc có kỷ luật: bắt đầu từ **C0**. Không cần code.
- Đã có prompt dùng ổn nhưng muốn chạy hàng loạt: vào **C1**.
- Có sẵn nhiều PDF, bản scan: đi từ **C2** đến **C5** để cho AI trả lời có căn cứ.
- Đã có hệ thống tra cứu chạy: đọc **C6** (đo) và **C9** (vận hành) để không bị "chạy được nhưng không biết đúng bao nhiêu".
- **C7** và **C8** chỉ cần khi AI phải làm thêm việc (tra đơn, gửi yêu cầu duyệt), không chỉ trả lời.

!!! tip "Nói đơn giản"
    Từ C2 trở đi có phần dùng code. Nếu bạn không biết lập trình, hãy làm theo đường "không code" của từng bài và nhờ người biết code (hoặc nhờ AI) khi cần tới cấp cao hơn.

## 5. Đọc trước

Ba bài nền nên đọc trước khi bắt đầu:

1. [Nền tảng bằng chứng](../nen-tang-bang-chung.md): các bài báo về hệ thống AI chạy thật.
2. [Thực trạng SME Việt Nam](../thuc-trang-sme-viet-nam.md): số liệu về SME dùng AI, và những số nên tránh.
3. [An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md): dữ liệu nào được đưa vào AI, đặc biệt quan trọng vì nhóm bài này đưa tài liệu nội bộ cho AI đọc.

## 6. Giới hạn

- Không có nguồn nào đo trực tiếp trên SME Việt Nam. Bằng chứng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.
- Mã mẫu đã chạy thử cục bộ, chưa chạy với API thật. Giá API không ghi số, chỉ ghi cách tự tính.
- Ngưỡng lên cấp và cỡ bộ ca mẫu là [Đề xuất].
