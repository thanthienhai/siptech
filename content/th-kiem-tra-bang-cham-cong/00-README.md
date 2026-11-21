# Thực hành 06. Kiểm tra bảng chấm công trước khi tính lương

Công ty khoảng 25 nhân viên, hai chi nhánh, máy chấm công vân tay (hoặc app) xuất CSV mỗi lần quẹt một dòng. Trước khi tính lương, ai đó phải biết: ai thiếu quẹt ra hoặc vào, ai quẹt trùng, ai đi trễ hoặc về sớm theo ca, ai làm thêm quá ngưỡng, ai nghỉ mà chưa ghi phép, ai đi làm ngày lễ, và ai có dấu hiệu bị quẹt hộ. Bài này cho **coding agent viết chương trình tính công và liệt kê bất thường**, rồi **chấm lại bằng đáp án** để biết tin được tới đâu.

> **Dữ liệu 100% là DỮ LIỆU GIẢ để học.** Công ty, tên người, mã thẻ, giờ quẹt đều do `du-lieu/sinh_du_lieu.py` bịa ra (hạt giống cố định). Mọi ngưỡng (đi trễ mấy phút, làm thêm bao nhiêu giờ thì cảnh báo, ngày lễ) là **tham số giả định** của công ty giả, không phải quy định pháp luật. Quy định pháp luật về giờ làm thêm, nghỉ lễ, nghỉ phép: cần kiểm với văn bản hiện hành hoặc chuyên gia nhân sự; bài này không trích điều luật nào.

## Vì sao doanh nghiệp nhỏ ở Việt Nam hay gặp

Nhiều công ty nhỏ dùng máy chấm công vân tay hoặc app, xuất dữ liệu ra Excel rồi người làm lương tự đối chiếu (đây là quy trình mà tài liệu hướng dẫn của nhà cung cấp phần mềm mô tả: tải dữ liệu từ máy, xuất Excel; xem nguồn bên dưới). Việc đối chiếu thủ công dễ sót vì mỗi lần quẹt là một dòng, một tháng có hàng nghìn dòng, hai chi nhánh dùng hai máy xuất hai định dạng giờ khác nhau, và một số lỗi (quẹt trùng, quẹt khác máy cách vài phút) rất khó thấy bằng mắt. Bài này **không** khẳng định tỷ lệ doanh nghiệp gặp vấn đề (không có số liệu nguồn); đây là bài toán mô phỏng.

## Dữ liệu mẫu

**[Đo được]** (sinh ngày 2026-11-20 bằng `sinh_du_lieu.py`): 25 nhân viên (16 hành chính, 9 ca xoay), hai chi nhánh A và B, kỳ tháng 09/2026, **1160 dòng quẹt**, 750 ô nhân viên x ngày, và **61 bất thường thuộc 14 loại đã cài sẵn** cùng nhiều "bẫy giống lỗi mà không phải lỗi" (trễ đúng 5 phút, quẹt cách nhau 4 phút, làm thêm 29 phút, quẹt 4 lần vì nghỉ trưa, người làm thêm 36,18 giờ sát ngưỡng 40 giờ, quẹt vào ở chi nhánh nhà và ra ở chi nhánh kia cách nhau cả ngày). Định dạng lẫn lộn (máy A `yyyy-mm-dd hh:mm:ss`, máy B `dd/mm/yyyy hh:mm`), một mã thẻ lạ, một giờ trống, một ngày 31/09 không tồn tại. Đáp án do bộ tính tham chiếu trong script tính ra và đối chiếu với sổ bẫy đã cài (hai bên phải trùng tuyệt đối).

Nguồn dùng làm **tham chiếu định dạng** (không chép nội dung):
- [Nguồn] ZKTeco FAQ: https://www.zkteco.com/en/faq.html (bản ghi quẹt gồm mã người dùng, thời gian, kiểu xác thực, trạng thái vào/ra).
- [Nguồn] MISA AMIS, xuất dữ liệu máy chấm công ra Excel: https://amis.misa.vn/80067/tai-du-lieu-tu-may-cham-cong/
- [Nguồn] Hướng dẫn xuất chấm công của app ZKTeco (cộng đồng): https://cyclone-nepal.gitbook.io/user-manual-zkteco-fingerprint-attendance/export-attendance

Mình **không tìm được bộ dữ liệu chấm công tiếng Việt công khai** dùng được (dữ liệu cá nhân, ít ai đăng), nên dữ liệu được sinh.

## Ba bài

1. [Bài 1. Chuẩn bị dữ liệu, ẩn danh, giao việc cho agent](cap-00-chuan-bi-du-lieu-va-giao-viec.md): bảng chấm công thô hay hỏng ở đâu; cách ẩn danh (mã `NV-xxx` thay tên, bỏ phòng ban và ghi chú đơn nghỉ, tự kiểm rò rỉ); viết quy định thành tệp; prompt 6 phần.
2. [Bài 2. Chạy thật Claude Code và Antigravity, chấm bằng đáp án](cap-01-chay-that-va-cham-ket-qua.md): lệnh chạy, ảnh agent làm việc, cách chấm, bảng kết quả, các lỗi và khác biệt gặp phải.
3. [Bài 3. Đưa vào dùng hằng tháng](cap-02-dung-hang-thang.md): chạy lại không cần agent, đổi ngưỡng, quy trình 8 bước, bộ tự kiểm không cần đáp án, người duyệt, giới hạn.

## Kết quả đo tóm tắt

Tất cả **[Đo được]**, ngày 2026-11-20, **n = 1 lần chạy mỗi dòng**, cùng prompt nguyên văn, cùng dữ liệu đã ẩn danh. Chấm bằng `ket-qua/cham.py`.

| Lần | Agent | Quy định | Thời gian | Bất thường đúng / bịa | Trạng thái ngày đúng | Người đúng hết cột |
|-----|-------|----------|-----------|-----------------------|----------------------|---------------------|
| claude-lan0 | Claude Code | đầy đủ | không đo; log mất | 61/61, bịa 0 | 750/750 | 25/25 |
| claude-lan1 | Claude Code | đầy đủ | 247,8 giây | 61/61, bịa 0 | 750/750 | 25/25 |
| claude-rutgon | Claude Code | rút gọn | 326,1 giây | 61/61, bịa 0 | 750/750 | 25/25 |
| agy-lan0 | agy | đầy đủ | không đo; log mất | 61/61, bịa 0 | 750/750 | 25/25 |
| agy-lan1 | agy | đầy đủ | hết giờ 900 giây (thiếu báo cáo); log mất | 61/61, bịa 0 | 750/750 | 25/25 |
| agy-lan2 | agy | đầy đủ | 1217,6 giây | 61/61, bịa 0 | 747/750 | 23/25 |
| agy-rutgon | agy | rút gọn | 1126,8 giây | 61/61, bịa 0 | 747/750 | 22/25 |

Quan sát (không phải xếp hạng):
- Cả bảy lần tìm đủ 61 bất thường, không báo oan bẫy nào, và đều đưa ba ca "một quẹt giữa ca" cho người quyết thay vì đoán.
- Hai lần của `agy` khác đáp án ở **cách hiểu quy định** (ngày nghỉ trong đơn nghỉ phép; ngày làm thêm quá 3 giờ bị bỏ trống giờ công), không phải lỗi cộng trừ. Chi tiết ở bài 2.
- Bộ tự kiểm không cần đáp án (`kiem_tra_dau_ra.py`) **đạt cả bảy bộ**, kể cả hai bộ khác đáp án: tự kiểm bắt lỗi hình thức, không bắt cách hiểu quy định khác ý bạn (bài 3).
- Chạy lại `tinh_cong.py` do agent viết, **không cần agent**: nội dung CSV giống hệt (hai bản đã thử), khoảng 0,3 giây.
- Lỗi và điều bất ngờ: lỗi in tiếng Việt ra console Windows (Claude Code, tự sửa); `agy` hết giờ 900 giây; một lần `agy` chạy `git log` và `dir ..\..` ngoài thư mục làm việc dù prompt dặn không; báo cáo của `agy` dài gần gấp đôi yêu cầu "một trang".

**n nhỏ:** chỉ 1 đến 2 lần mỗi cấu hình, chưa đo được độ ổn định giữa các lần chạy, không đủ để kết luận agent nào tốt hơn. Dữ liệu giả và đáp án cùng do người soạn bài viết nên có thể dễ hơn thực tế.

## Cấu trúc thư mục

```
06-kiem-tra-bang-cham-cong/
  00-README.md, bai-1-...md, bai-2-...md, bai-3-...md
  du-lieu/
    sinh_du_lieu.py        sinh dữ liệu giả (hạt giống cố định) + đáp án
    an_danh.py             ẩn danh, tự kiểm rò rỉ, gắn lại tên (--giai-ma)
    goc/                   dữ liệu "thô" như xuất từ máy (tên GIẢ) - chỉ ở máy bạn
    an-danh/               bản đưa cho agent (4 CSV + quy_dinh_cong_ty.md + bản rút gọn)
  ket-qua/
    prompt-giao-viec.txt   prompt nguyên văn
    cham.py                chấm bằng đáp án;  bao-cao-cham.json: kết quả chấm 7 lần
    kiem_tra_dau_ra.py     tự kiểm không cần đáp án
    dap-an.json            đáp án (mã ẩn danh); dap-an-goc.json (mã gốc); bang-ma-hoa.csv
    <lần chạy>/            đầu ra thật của agent (giữ cả bản lệch, bản hết giờ, bản mất log)
    chay_agent_giu_log.py, dung_anh.py   công cụ chạy giữ log và dựng ảnh
  logs/                    log gốc *.raw.jsonl và transcript *.json của 4 lần có log
  anh/                     12 ảnh PNG dùng trong bài
```

## Cách chạy lại

```
cd du-lieu
python -X utf8 sinh_du_lieu.py      # sinh dữ liệu giả và đáp án
python -X utf8 an_danh.py           # ẩn danh (+ python -X utf8 an_danh.py --dap-an để tạo dap-an.json)
```

Rồi chép bốn CSV và `quy_dinh_cong_ty.md` từ `an-danh/` vào một thư mục RIÊNG, dán prompt trong `ket-qua/prompt-giao-viec.txt` cho agent, và chấm: `python -X utf8 ket-qua/cham.py <thư_mục_đầu_ra> <nhãn>`. Cần Python 3.13 (hoặc gần đó). `dung_anh.py` cần thêm công cụ `term.py` và `agent_run.py` của chuỗi bài (đặt biến môi trường `AGENTLAB` trỏ tới thư mục chứa chúng).

## Ghi chú trung thực về log và ảnh

- Ba lần chạy (`claude-lan0`, `agy-lan0`, `agy-lan1`) **không có log gốc** do lỗi của người chạy (tiến trình bọc bị cắt, và công cụ không lưu phần đã chạy khi hết giờ). Các tệp đầu ra của chúng được giữ và chấm; bài ghi rõ.
- Các ảnh terminal trong `anh/` là **bản dựng lại từ log thật** của lần chạy ghi dưới ảnh, không phải ảnh chụp trực tiếp cửa sổ TUI.
- Ảnh terminal dựng lại từ log đã che đường dẫn máy và tên tổ chức.
- Trong `logs/`, để không lộ thông tin máy cá nhân, đường dẫn và tên thư mục người dùng đã được thay bằng `<thu-muc-lam-viec>`, `<thu-muc-bai>` hoặc `<user>`, tên thư mục đồng bộ đám mây (có tên tổ chức) thay bằng `<thu-muc-dong-bo>`, tên chủ tài khoản máy trong kết quả `ls` thay bằng `user`, và với log của Claude Code đã bỏ các sự kiện hệ thống ban đầu (khởi tạo, hook, danh sách lệnh). Phần nội dung làm việc của agent không bị sửa.
- Cả bốn tệp `logs/*.raw.jsonl` đã kiểm: mọi dòng đều là JSON hợp lệ (agy-lan2: 445 dòng, agy-rutgon: 341, claude-lan1: 209, claude-rutgon: 273, sau khi bỏ sự kiện hệ thống của Claude Code). Một lỗi ký tự điều khiển từng xuất hiện ở `agy-lan2.raw.jsonl` do bước che đường dẫn của chính mình; đã dựng lại các log từ bản gốc bằng bước che đã sửa, nên lỗi không còn.
- Phiên bản đọc được từ log: Claude Code 2.1.329, mô hình `claude-sonnet-5-5`; `agy` 1.5.13 (log không ghi tên mô hình).

## Giới hạn

- Dữ liệu giả, kịch bản do người soạn cài; chưa có ca qua đêm, giờ máy lệch, đổi mã thẻ, nghỉ nửa ngày, đi công tác.
- Quy định pháp luật không được tra cứu hay trích; mọi ngưỡng là giả định.
- Ẩn danh bằng mã không phải ẩn danh tuyệt đối; việc đưa dữ liệu nhân sự ra dịch vụ đám mây cần xem quy định nội bộ và pháp lý.
- Chương trình `tinh_cong.py` do agent viết chỉ được thử trên dữ liệu tháng 09/2026 của bài.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây.
