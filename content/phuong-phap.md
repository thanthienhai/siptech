date: 2026-11-26

# Cách SIPTech soạn và kiểm chứng nội dung

Trang này nói rõ nội dung ở đây được làm thế nào, con số nào đáng tin tới đâu, và điều gì chưa làm được. Mục đích là để bạn dùng đúng mức: lấy phần có căn cứ, kiểm lại phần còn lại với người có chuyên môn.

!!! warning "SIPTech cung cấp tài liệu hướng dẫn, không phải tư vấn riêng"
    Nội dung giúp bạn hiểu và thử nghiệm việc dùng AI trong công việc văn phòng. Đây **không phải** tư vấn pháp lý, thuế, kế toán hay nhân sự cho tình huống cụ thể của doanh nghiệp bạn. Ở chỗ nào chạm tới luật, thuế hay dữ liệu cá nhân, các bài chỉ nêu nguyên tắc và dặn kiểm với người có chuyên môn.

## Bốn nhãn bạn sẽ gặp trong bài

Mọi nhận định trong bài được gắn một trong bốn nhãn. Đọc nhãn trước khi quyết định có dựa vào điều đó hay không.

| Nhãn | Nghĩa | Nên làm gì |
|---|---|---|
| **[Nguồn]** | Điều tài liệu gốc nói, có liên kết để bạn tự đọc | Dùng được. Mở nguồn nếu số liệu quan trọng với quyết định của bạn |
| **[Đo được]** | Kết quả chúng tôi tự chạy và chấm, kèm ngày, công cụ và số lần chạy | Dùng như một quan sát trên dữ liệu giả, không phải thống kê. Xem mục "Vì sao số lần chạy nhỏ" bên dưới |
| **[Đề xuất]** | Ý kiến hoặc thiết kế của nhóm soạn (ngưỡng, cỡ mẫu, thứ tự học) | Coi là điểm xuất phát. Chưa có số đo chứng minh |
| **[Minh họa]** | Ví dụ giả định để dễ hình dung | Đừng suy ra số liệu từ đó |

Với các nguồn nghiên cứu, trang [Nền tảng bằng chứng](nen-tang-bang-chung.md) ghi thêm **mức đọc**: đọc toàn văn, chỉ đọc tóm tắt, hay qua nguồn thứ cấp. Điều chỉ đọc qua tóm tắt thì không nên coi chắc bằng điều đã đọc toàn văn.

## Một bài toán được làm như thế nào

Các bài toán thực hành (nhóm "Thực hành với coding agent") đi qua cùng một quy trình:

1. **Tìm tài liệu giống thật.** Tìm mẫu công khai về định dạng và dạng lỗi (ví dụ cách trình bày sao kê, mẫu báo giá, bộ đánh giá tiếng Việt công khai). Chỉ dùng để tham chiếu định dạng, không chép nội dung có bản quyền hay dữ liệu cá nhân thật.
2. **Sinh dữ liệu giả có bẫy.** Tên, số điện thoại, số tài khoản, công ty đều bịa. Dữ liệu có viết tắt, không dấu, trùng, thiếu, định dạng lẫn lộn và những ca mơ hồ cố ý. Script sinh có hạt giống cố định nên chạy lại ra đúng bộ cũ.
3. **Viết đáp án trước khi chạy.** Mỗi dòng có đáp án đúng, và có nhãn "mơ hồ, đúng ra phải để người quyết". Đáp án nằm ngoài tầm của agent.
4. **Giao việc bằng prompt 6 phần** (vai trò, bối cảnh, nhiệm vụ, các bước, định dạng ra, ràng buộc). Prompt không đổi sau khi thấy kết quả để "cho đẹp"; nếu đổi thì giữ cả hai bản.
5. **Chạy thật bằng coding agent** (Claude Code và Antigravity), trong thư mục riêng.
6. **Chấm bằng code** theo đáp án: đúng bao nhiêu, bỏ sót gì, bịa gì, ca mơ hồ có chuyển cho người không.
7. **Giữ kết quả xấu.** Lần agent sai, lần mất log, lần phải chạy lại đều ở lại trong bài.
8. **Dựng ảnh từ log thật.** Ảnh "terminal" trong bài được dựng lại từ log của lần chạy (đã che đường dẫn máy và tên tổ chức), không phải ảnh chụp trực tiếp. Mỗi ảnh có chú thích nói rõ.

Bài mới được đăng ở trạng thái **Đang soạn**, và chỉ chuyển sang **Đã có** khi được người soạn rà soát. "Sắp ra" là thẻ giữ chỗ chưa có nội dung.

## Vì sao số lần chạy nhỏ, và bạn nên đọc kết quả thế nào

Mỗi agent thường chỉ chạy một đến vài lần mỗi bài toán. Với cỡ mẫu đó:

- Kết quả **cho thấy agent làm được gì và sai ở kiểu nào**, không đo được độ ổn định.
- Chúng tôi **không kết luận "agent A tốt hơn agent B"** từ một vài lần chạy. Thời gian chạy cũng không so sánh được khi giới hạn thời gian khác nhau.
- Có những thứ lặp lại ở nhiều bài toán, và đó mới là điều đáng học: agent làm tốt phần có luật rõ (chuẩn hóa, cộng trừ, ghép theo mã); hay hỏng ở chỗ viết cứng số của dữ liệu mẫu vào script, thêm câu không có trong nguồn, hứa việc chưa làm; và **tự báo "đạt" khi vẫn sai**. Vì vậy mọi bài đều dạy dựng bộ chấm độc lập và để người soi mẫu.

## Agent chạy trên máy bạn: điều cần biết

Coding agent đọc file, viết và chạy lệnh trên máy bạn. Trong các lần chạy của chúng tôi, có lần agent mở file đáp án nằm ngoài thư mục làm việc, có lần chạy lệnh ngoài thư mục dù được dặn không. Câu "chỉ làm trong thư mục này" trong prompt **không phải hàng rào**. Hàng rào thật là: thư mục riêng, dữ liệu giả hoặc đã ẩn danh trước, không để đáp án hay bí mật cạnh đó, và đọc kỹ câu xin quyền. Chi tiết ở nhóm [Bắt đầu với coding agent](th-bat-dau-voi-coding-agent/00-README.md) và trang [An toàn dữ liệu và pháp lý](an-toan-du-lieu-va-phap-ly-vn.md).

## Những điều chúng tôi chưa làm được

- **Chưa có số đo trên SME Việt Nam.** Bằng chứng định lượng đến từ tổ chức lớn hoặc nhóm kỹ thuật mạnh. Giả thuyết về thực trạng dùng AI ở doanh nghiệp nhỏ trong nước chỉ có bằng chứng gián tiếp.
- **Chưa thử với người học thật.** Các bài viết cho người chưa biết code, nhưng chưa có người ngoài làm theo từ đầu đến cuối. Chúng tôi đã nhờ agent AI đọc thử vai người mới và vai người hoài nghi để bắt chỗ khó hiểu và chỗ nói quá; việc đó giúp sửa lỗi, nhưng **không thay được người học thật**.
- **Pháp lý chưa xác minh toàn văn.** Nhiều văn bản mới chỉ đọc qua nguồn thứ cấp. Cần luật sư hoặc đọc văn bản gốc trước khi áp dụng.
- **Công cụ thay đổi nhanh.** Giao diện, tính năng, điều khoản và giá của Claude, ChatGPT, Gemini, Antigravity có thể đổi sau ngày ghi trong bài. Chỗ nào chưa kiểm được, bài ghi "chưa kiểm".
- **Tiếng Việt có thể kém hơn tiếng Anh.** Một số phép đo công khai trên các mô hình đời 2024 đến 2025 cho thấy điều đó (xem [Nền tảng bằng chứng](nen-tang-bang-chung.md)); mô hình mới hơn có thể khác và chúng tôi chưa tự đo trên văn bản của doanh nghiệp bạn. Hãy đo trên dữ liệu của chính bạn.

## Cập nhật và sửa lỗi

- Mỗi bài ghi ngày cập nhật. Các thay đổi đáng kể được ghi ở trang [Nhật ký cập nhật](cap-nhat.md).
- Thấy sai hoặc thiếu? Dùng trang [Hỏi và góp ý](gop-y.html) (hoặc mở yêu cầu trực tiếp tại [kho mã nguồn trên GitHub](https://github.com/thanthienhai/siptech/issues)). Nội dung sai sẽ được sửa và ghi vào nhật ký, kể cả khi sai là do chúng tôi.

## Về chính trang web này

- Trang không dùng cookie theo dõi và không cài công cụ phân tích truy cập. Chữ (Be Vietnam Pro) tải từ Google Fonts, nên trình duyệt của bạn có gửi yêu cầu tới máy chủ của Google khi mở trang.
- Dữ liệu tải về trong các bài thực hành đều là dữ liệu giả. Đừng đặt dữ liệu thật của doanh nghiệp vào thư mục thử.
- Mã nguồn của trang công khai trên GitHub, gồm cả công cụ dựng trang và công cụ kiểm bài.
