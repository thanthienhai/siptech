# Thực hành 06. Kiểm tra bảng chấm công trước khi tính lương

## Bạn làm được gì sau bài toán này

Bạn biết cách nhờ một coding agent (chương trình AI tự đọc file, viết và chạy code) **viết chương trình tính công và liệt kê bất thường** từ bảng quẹt của máy chấm công: ai thiếu quẹt vào hoặc ra, quẹt trùng, đi trễ hoặc về sớm theo ca, làm thêm quá ngưỡng, vắng chưa ghi phép, đi làm ngày lễ, và ai có dấu hiệu bị quẹt hộ. Bạn biết **ẩn danh bảng chấm công** (mã `NV-xxx` thay họ tên) trước khi đưa cho agent, **chấm lại bằng đáp án** để biết tin được tới đâu, **chạy lại hằng tháng không cần agent**, và dùng bộ prompt mẫu cùng ba bài tập có bộ kiểm.

> **Dữ liệu 100% là DỮ LIỆU GIẢ để học.** Công ty (khoảng 25 nhân viên, hai chi nhánh), tên người, mã thẻ, giờ quẹt đều do `du-lieu/sinh_du_lieu.py` bịa ra (hạt giống cố định). Mọi ngưỡng (đi trễ mấy phút, làm thêm bao nhiêu giờ thì cảnh báo, ngày lễ) là **tham số giả định** của công ty giả, không phải quy định pháp luật. Giờ làm thêm, nghỉ lễ, nghỉ phép: cần kiểm với văn bản hiện hành hoặc chuyên gia nhân sự; bài toán này không trích điều luật nào.

## Bốn bài

| Bài | Mất bao lâu | Kết quả |
|---|---|---|
| [Bài 1. Chuẩn bị dữ liệu, ẩn danh, giao việc cho agent](cap-00-chuan-bi-du-lieu-va-giao-viec.md) | khoảng 30 phút (agent chạy thêm 4 đến 20 phút) | Bản dữ liệu đã ẩn danh, tự kiểm rò rỉ; thư mục agent có `tinh_cong.py` và các bảng công, bất thường |
| [Bài 2. Chạy thật Claude Code và Antigravity, chấm bằng đáp án](cap-01-chay-that-va-cham-ket-qua.md) | khoảng 30 đến 45 phút | Bảng kết quả bằng số; hai ca agent hiểu quy định khác đáp án; cách rà log lệnh ngoài thư mục |
| [Bài 3. Dùng hằng tháng](cap-02-dung-hang-thang.md) | dưới 10 phút mỗi tháng (chưa kể người duyệt) | Quy trình 6 bước chạy lại không cần agent, bộ tự kiểm 7 mục, bảng người duyệt |
| [Bài 4. Prompt mẫu và bài tập tự làm](cap-03-prompt-mau-va-bai-tap.md) | mỗi prompt vài phút, mỗi bài tập 10 đến 20 phút | 9 prompt (6 đã chạy thật), 3 bài tập có bộ kiểm bằng code, checklist dữ liệu thật |

## Sắp xếp thư mục trước khi làm

Tạo một thư mục trống làm nơi làm bài (ví dụ `bai-toan`) và sắp như sau:

```file
bai-toan/
  du-lieu/      giải nén du-lieu.zip vào đây (dữ liệu giả và bản giao việc)
  lan-chay-1/   thư mục RIÊNG của agent: bạn tạo ở Bài 1, chỉ chép file dữ liệu vào
  ket-qua/      giải nén bo-cham.zip vào đây (đáp án và bộ chấm), SAU KHI agent chạy xong
```

- Trong từng bài, lệnh chấm cho biết bạn đứng ở thư mục nào. Phần lớn bộ chấm cần `du-lieu/` và `ket-qua/` nằm **cạnh nhau**.
- **Để đáp án ngoài tầm agent.** Đừng giải nén `bo-cham.zip` trước khi agent chạy xong. Agent có thể đi lên thư mục cha để tìm file; việc này đã xảy ra trong các lần chạy của chúng tôi (xem bài 2).
- **Cần Python 3** (cách kiểm và cài: [Bài 1 của nhóm Bắt đầu](../th-bat-dau-voi-coding-agent/cap-00-lam-quen-cua-so-dong-lenh.md)). Một số bộ chấm đọc file Excel nên cần thư viện `openpyxl`: nếu thấy `ModuleNotFoundError`, gõ `pip install openpyxl`. **Chưa kiểm** trên máy sạch.

## Kết quả đo tóm tắt

Tất cả **[Đo được]**, ngày 2026-11-20, **n = 1 lần chạy mỗi dòng**, cùng prompt nguyên văn, cùng dữ liệu đã ẩn danh. Chấm bằng `ket-qua/cham.py`.

| Lần | Agent | Quy định | Thời gian | Bất thường đúng / bịa | Trạng thái ngày đúng | Người đúng hết cột |
|---|---|---|---|---|---|---|
| claude-lan0 | Claude Code | đầy đủ | không đo; log mất | 61/61, bịa 0 | 750/750 | 25/25 |
| claude-lan1 | Claude Code | đầy đủ | 247,8 giây | 61/61, bịa 0 | 750/750 | 25/25 |
| claude-rutgon | Claude Code | rút gọn | 326,1 giây | 61/61, bịa 0 | 750/750 | 25/25 |
| agy-lan0 | `agy` | đầy đủ | không đo; log mất | 61/61, bịa 0 | 750/750 | 25/25 |
| agy-lan1 | `agy` | đầy đủ | hết giờ 900 giây (thiếu báo cáo); log mất | 61/61, bịa 0 | 750/750 | 25/25 |
| agy-lan2 | `agy` | đầy đủ | 1.217,6 giây | 61/61, bịa 0 | 747/750 | 23/25 |
| agy-rutgon | `agy` | rút gọn | 1.126,8 giây | 61/61, bịa 0 | 747/750 | 22/25 |

Quan sát (không phải xếp hạng):

- Cả bảy lần tìm đủ 61 bất thường, không báo oan bẫy nào, và đều đưa ba ca "một quẹt giữa ca" cho người quyết thay vì đoán.
- Hai lần của `agy` khác đáp án ở **cách hiểu quy định** (ngày nghỉ nằm trong đơn nghỉ phép; ngày làm thêm quá 3 giờ bị bỏ trống giờ công), không phải lỗi cộng trừ. Chi tiết ở bài 2.
- Bộ tự kiểm không cần đáp án (`kiem_tra_dau_ra.py`) **đạt cả bảy bộ**, kể cả hai bộ khác đáp án: tự kiểm bắt lỗi hình thức, không bắt cách hiểu quy định khác ý bạn (bài 3).
- Chạy lại `tinh_cong.py` do agent viết, **không cần agent**: nội dung CSV giống hệt (hai bản đã thử), khoảng 0,3 giây.
- **Bài 4, ngày 2026-11-21, n = 1 mỗi prompt (Claude Code):** 6 prompt chạy thật. Kiểm chéo độc lập bắt đúng 2/2 ô chúng tôi cố ý sửa (và đoán sai nguyên nhân của một ô); thư gửi quản lý có đủ 37/37 ca cần xác nhận; đổi dung sai 5 lên 10 phút ra 12 xuống 10 lần `DI_TRE`, 6 xuống 5 `VE_SOM`, tổng 61 xuống 58 (trùng số đo tay ở bài 3).
- Lỗi và điều bất ngờ: lỗi in tiếng Việt ra màn hình Windows (Claude Code, tự sửa); `agy` hết giờ 900 giây; một lần `agy` chạy `git log` và `dir ..\..` ngoài thư mục làm việc dù prompt dặn không; báo cáo của `agy` dài gần gấp đôi yêu cầu "một trang"; ở chế độ chạy một lần, một lệnh Python của Claude Code bị chặn (bài 4).

**n nhỏ:** chỉ 1 đến 2 lần mỗi cấu hình, chưa đo được độ ổn định giữa các lần chạy, không đủ để kết luận agent nào tốt hơn. Dữ liệu giả và đáp án cùng do người soạn bài viết nên có thể dễ hơn thực tế.

## Đào sâu: cấu trúc thư mục trong bản gốc của tác giả
```
06-kiem-tra-bang-cham-cong/
  00-README.md, bai-1-...md, bai-2-...md, bai-3-...md, bai-4-...md
  du-lieu/
    sinh_du_lieu.py        sinh dữ liệu giả (hạt giống cố định) + đáp án
    an_danh.py             ẩn danh, tự kiểm rò rỉ, gắn lại tên (--giai-ma)
    prompt-giao-viec.txt   prompt nguyên văn của bài 1
    goc/                   dữ liệu "thô" như xuất từ máy (tên GIẢ): chỉ ở máy bạn
    an-danh/               bản đưa cho agent (4 CSV + quy_dinh_cong_ty.md + bản rút gọn)
  ket-qua/
    cham.py                chấm bằng đáp án; tom_tat_cham.py in tóm tắt; bao-cao-cham.json: kết quả chấm 7 lần
    kiem_tra_dau_ra.py     tự kiểm không cần đáp án
    dap-an.json            đáp án (mã ẩn danh); dap-an-goc.json (mã gốc); bang-ma-hoa.csv
    bai-tap/               kiem_bai_tap.py (bộ kiểm 3 bài tập), loi-giai-an-danh.py (lời giải bài tập 3)
    <lần chạy>/            đầu ra thật của agent (giữ cả bản lệch, bản hết giờ, bản mất log)
    chay_agent_giu_log.py, dung_anh.py   công cụ chạy giữ log và dựng ảnh
  logs/                    log gốc *.raw.jsonl và transcript *.json (4 lần của bài 2, 6 lần của bài 4)
  anh/                     13 ảnh PNG dùng trong bài
```

## Cách chạy lại

```
cd du-lieu
python -X utf8 sinh_du_lieu.py      # sinh dữ liệu giả và đáp án
python -X utf8 an_danh.py           # ẩn danh (+ python -X utf8 an_danh.py --dap-an để tạo dap-an.json)
```

Rồi chép bốn CSV và `quy_dinh_cong_ty.md` từ `an-danh/` vào một thư mục RIÊNG, dán prompt trong `du-lieu/prompt-giao-viec.txt` cho agent, và chấm: `python -X utf8 ket-qua/cham.py <thư_mục_đầu_ra> <nhãn>`. Cần Python 3.13 (hoặc gần đó). `dung_anh.py` cần thêm công cụ `term.py` và `agent_run.py` của chuỗi bài (đặt biến môi trường `AGENTLAB` trỏ tới thư mục chứa chúng).

## Ghi chú trung thực về log và ảnh

- Ba lần chạy của bài 2 (`claude-lan0`, `agy-lan0`, `agy-lan1`) **không có log gốc** do lỗi của người chạy (tiến trình bọc bị cắt, và công cụ không lưu phần đã chạy khi hết giờ). Các tệp đầu ra của chúng được giữ và chấm; bài ghi rõ.
- Các ảnh terminal trong `anh/` là **bản dựng lại từ log thật** của lần chạy ghi dưới ảnh, không phải ảnh chụp trực tiếp cửa sổ TUI. Ảnh đã che đường dẫn máy và tên tổ chức.
- Trong `logs/`, để không lộ thông tin máy cá nhân, đường dẫn và tên người dùng đã được thay bằng `<thu-muc-lam-viec>`, `<thu-muc-bai>` hoặc `<user>`, tên thư mục đồng bộ đám mây thay bằng `<thu-muc-dong-bo>`, tên chủ tài khoản máy trong kết quả `ls` thay bằng `user`, và với log của Claude Code đã bỏ các sự kiện hệ thống ban đầu (khởi tạo, hook, danh sách lệnh). Phần nội dung làm việc của agent không bị sửa.
- Mọi tệp `logs/*.raw.jsonl` đã kiểm: mọi dòng đều là JSON hợp lệ.
- Phiên bản đọc từ log: bài 2 chạy bằng Claude Code 2.1.329, mô hình `claude-sonnet-5-5`, và `agy` 1.5.13 (log không ghi tên mô hình); bài 4 chạy bằng Claude Code 2.1.330, cùng mô hình.
- Thư mục `ket-qua/` chứa đáp án: **không đưa cho agent**.

## Giới hạn

- Dữ liệu giả, kịch bản do người soạn cài; chưa có ca qua đêm, giờ máy lệch, đổi mã thẻ, nghỉ nửa ngày, đi công tác.
- Quy định pháp luật không được tra cứu hay trích; mọi ngưỡng là giả định.
- Ẩn danh bằng mã không phải ẩn danh tuyệt đối; việc đưa dữ liệu nhân sự ra dịch vụ đám mây cần xem quy định nội bộ và pháp lý.
- `tinh_cong.py` do agent viết chỉ được thử trên dữ liệu tháng 09/2026 của bài (và hai biến thể ở bài 4).
- Agent chạy lệnh thật trên máy: câu dặn "chỉ đọc và ghi trong thư mục hiện tại" không phải hàng rào (bài 2 đã gặp một ca ngược lại).
- Bài 4: mỗi prompt chạy thật n = 1; ba prompt (1, 4, 5) chưa chạy thử; lệnh macOS, Linux chưa chạy thử.

## Tải về

- [Dữ liệu mẫu (du-lieu.zip)](du-lieu.zip): dữ liệu giả, kèm script sinh dữ liệu và bản giao việc.
- [Bộ chấm và kết quả mẫu (bo-cham.zip)](bo-cham.zip): đáp án, script chấm và đầu ra của các lần chạy. Nếu bạn tự chạy agent, đừng để file này trong thư mục làm việc của agent.

Log gốc của các lần chạy không được đăng ở đây. Bấm vào ảnh trong bài để xem cỡ lớn.
