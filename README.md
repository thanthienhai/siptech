# SIPTech - Tư vấn giải pháp AI trong doanh nghiệp

Website giới thiệu series "AI cho SME Việt Nam, từ khối nhỏ nhất đến nghiệp vụ phức tạp": 5 bài toán doanh nghiệp, 40 cấp độ, có nguồn và cách đo.

Site: https://thanthienhai.github.io/siptech/

## Cấu trúc

- `content/`: tài liệu Markdown (nguồn nội dung, sao từ `AI-Real`).
- `build.py`: dựng `content/` thành HTML tĩnh trong `site/`.
- `assets/`: CSS, favicon.
- `.github/workflows/pages.yml`: tự dựng và triển khai lên GitHub Pages khi push vào `main`.

## Dựng cục bộ

```bash
pip install markdown
python build.py        # kết quả ở site/
```

## Lưu ý

Nội dung là tài liệu nghiên cứu, không phải tư vấn pháp lý hay tư vấn thuế. Các mục pháp lý chưa xác minh toàn văn; số liệu định lượng chưa có nguồn đo trên SME Việt Nam.
