# SIPTech - Tư vấn giải pháp AI trong doanh nghiệp

Website giới thiệu series "AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp": các bài toán doanh nghiệp (danh sách cập nhật liên tục), mỗi bài một thang cấp độ, có nguồn và cách đo.

Site: https://thanthienhai.github.io/siptech/

## Cấu trúc

- `content/`: tài liệu Markdown (nguồn nội dung, sao từ `AI-Real`).
- `build.py`: dựng `content/` thành HTML tĩnh trong `site/`.
- `assets/`: CSS, favicon.
- `.github/workflows/pages.yml`: tự dựng và triển khai lên GitHub Pages khi push vào `main`.

## Thêm bài toán mới

Mỗi thư mục trong `content/` có `meta.json` là một bài toán. Site tự đếm số bài toán, số cấp độ, tự thêm vào trang chủ, trang "Tất cả bài toán", menu và chân trang.

```bash
python new_problem.py ten-thu-muc "Tên bài toán" --status draft
# sửa content/ten-thu-muc/meta.json, viết 00-README.md và cap-00-*.md, cap-01-*.md ...
git add -A && git commit -m "Thêm bài toán" && git push
```

`meta.json` gồm: `name`, `code` (ví dụ `C0–C9`), `tag`, `desc`, `out`, `icon`, `tags` (cho ô tìm kiếm), `order` (thứ tự), `status` (`published` đã có / `draft` đang soạn / `planned` sắp ra), `updated` (YYYY-MM-DD), và tùy chọn `step`, `step_label` để xuất hiện trong "Thứ tự gợi ý". Bài toán chỉ có `meta.json` (chưa có file `cap-*.md`) hiển thị là thẻ "Sắp ra", chưa có trang. Thêm `"hidden": true` để ẩn.

## Cách bài giảng được dựng từ Markdown

File trong `content/` vẫn viết theo quy ước nghiên cứu (`[Nguồn]`, `[Đề xuất]`, tham chiếu file bằng dấu huyền). `build.py` và `lesson.py` tự biến chúng thành bài giảng khi dựng, không cần sửa tay:

- Phần đầu bài ("Ngày soạn", bảng quy ước) gọn thành dòng ngày cập nhật, số phút đọc và khung "Trước khi học".
- Tham chiếu file như `../x/cap-01.md` mục 3 thành liên kết có tên bài và tên phần.
- Nhãn `[Nguồn]`, `[Đề xuất]`, `[Đã chạy thử]`... thành thẻ nhỏ có giải thích; mã nguồn (B5, V1...) thành liên kết tới danh sách tài liệu tham khảo.
- Mục "Chưa kiểm chứng" gập lại (dành cho người soạn), địa chỉ web thành liên kết.
- Thuật ngữ trong `lesson.py` (danh sách `GLOSSARY`) có giải nghĩa khi rê chuột và có trang Từ điển.

## Dựng cục bộ

```bash
pip install markdown
python build.py        # kết quả ở site/
```

## Lưu ý

Nội dung là tài liệu nghiên cứu, không phải tư vấn pháp lý hay tư vấn thuế. Các mục pháp lý chưa xác minh toàn văn; số liệu định lượng chưa có nguồn đo trên SME Việt Nam.
