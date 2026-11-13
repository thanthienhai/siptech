# Nhóm bài: Tra cứu thông tin trên một tập tài liệu (RAG)

> Thuộc series "AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp".
> Quy ước: **[Nguồn]** = điều tài liệu nói; **[Đề xuất]** = suy luận hoặc thiết kế của nhóm soạn. Mọi ngưỡng, cỡ mẫu là [Đề xuất].
> Không phải tư vấn pháp lý. Đọc kèm [An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md).

## 1. Bài toán

**Đầu vào:** một tập tài liệu nội bộ (bảng giá, chính sách, hợp đồng, quy trình) và câu hỏi của nhân viên hoặc khách.
**Đầu ra:** câu trả lời có trích dẫn nguyên văn từ tài liệu, hoặc từ chối khi tài liệu không đủ căn cứ.

Đây là ví dụ xuyên suốt của series: đi từ dùng AI thủ công, gọi API, biến tài liệu thành text, chia khối, tìm kiếm, trả lời có trích dẫn, đánh giá, công cụ, quy trình nhiều bước, đến vận hành. Mỗi cấp có hai đường: không code (Project, Gem, GPT tùy chỉnh) và code nhẹ (Python).

Bộ slide minh họa (33 slide) nằm cùng thư mục: `RAG-tra-cuu-tai-lieu-C0-C9.pptx`.

## 2. Thang cấp độ

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

## 3. Đọc trước

1. [Nền tảng bằng chứng](../nen-tang-bang-chung.md)
2. [Thực trạng SME Việt Nam](../thuc-trang-sme-viet-nam.md)
3. [An toàn dữ liệu và pháp lý](../an-toan-du-lieu-va-phap-ly-vn.md)

## 4. Giới hạn

- Không có nguồn nào đo trực tiếp trên SME Việt Nam. Bằng chứng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh.
- Mã mẫu đã chạy thử cục bộ, chưa chạy với API thật. Giá API không ghi số, chỉ ghi cách tự tính.
- Ngưỡng lên cấp và cỡ bộ ca mẫu là [Đề xuất].
