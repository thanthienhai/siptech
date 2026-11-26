"""Thành phần trình bày cho bài thực hành: khung prompt có nút sao chép, bước đánh số, hình có chú thích, mục "Đào sâu" gập lại.

Quy ước viết trong file .md (python-markdown):

  ```prompt          khung "Prompt" (dán vào agent), có nút Sao chép
  ```lenh            khung "Lệnh" (gõ vào Terminal), có nút Sao chép
  ```ketqua          khung "Kết quả mẫu" (chỉ để xem, không phải gõ)
  ```file            khung "Nội dung file"
  ```bash, ```python, ... : khối mã thường, có nút Sao chép nhỏ

  ### Bước 3. Tên bước        -> đầu mục có số tròn
  !!! see "Bạn sẽ thấy"       -> khung xanh: kết quả mong đợi của bước
  !!! stuck "Gặp lỗi?"        -> khung vàng: cách xử lý
  !!! info "Bài này"          -> thẻ tóm tắt đầu bài (thời gian, cần có, kết quả)
  ## Đào sâu: ...             -> gập lại, dành cho người muốn hiểu thêm
  ![mô tả](anh/x.webp)        + dòng sau là *chú thích*  -> hình có chú thích, bấm để phóng to
"""
import re

KINDS = {
    "prompt": ("Prompt", "Sao chép rồi dán vào agent"),
    "lenh": ("Lệnh", "Gõ hoặc dán vào cửa sổ dòng lệnh (Terminal)"),
    "ketqua": ("Kết quả mẫu", "Chỉ để so sánh, không cần gõ"),
    "file": ("Nội dung file", ""),
}

PRE_RE = re.compile(r'<pre><code(?: class="language-([\w+-]+)")?>(.*?)</code></pre>', re.S)


def _code(m):
    lang = (m.group(1) or "").lower()
    inner = m.group(2)
    if lang in KINDS:
        label, hint = KINDS[lang]
        copy = lang != "ketqua"
        head = (f'<div class="ch"><span class="cl">{label}</span>' + (f'<span class="chint">{hint}</span>' if hint else "")
                + ('<button type="button" class="cp" data-cp>Sao chép</button>' if copy else "") + "</div>")
        return f'<div class="cb cb-{lang}">{head}<pre tabindex="0"><code>{inner}</code></pre></div>'
    cls = f' class="language-{lang}"' if lang else ""
    return (f'<div class="cb cb-plain"><button type="button" class="cp mini" data-cp aria-label="Sao chép">Sao chép</button>'
            f"<pre tabindex=\"0\"><code{cls}>{inner}</code></pre></div>")


STEP_RE = re.compile(r'<h3 id="([^"]*)">\s*(?:\d+(?:\.\d+)*\.?\s*)?Bước\s+(\d+)\s*[.:)\-—]\s*(.*?)</h3>', re.S)
FIG_RE = re.compile(r'<p>(<a class="zoom"[^>]*>\s*<img [^>]*>\s*</a>)</p>\s*<p><em>(.*?)</em></p>', re.S)
DEEP_RE = re.compile(r'<h2 id="([^"]*)">\s*(?:\d+\.\s*)?(Đào sâu[^<]*)</h2>(.*?)(?=<h2 id=|\Z)', re.S)


def _deep(m):
    title = re.sub(r"^Đào sâu\s*[:\-—.]?\s*", "", m.group(2)).strip()
    return (f'<details class="deep" id="{m.group(1)}"><summary><b>Đào sâu</b>'
            + (f" · {title}" if title else "") + f' <span class="dh">(không bắt buộc, bấm để mở)</span></summary>{m.group(3)}</details>')


def lesson_ui(body):
    body = PRE_RE.sub(_code, body)
    body = STEP_RE.sub(lambda m: f'<h3 class="stepH" id="{m.group(1)}"><span class="sn">{m.group(2)}</span><span>{m.group(3)}</span></h3>', body)
    body = FIG_RE.sub(r"<figure>\1<figcaption>\2</figcaption></figure>", body)
    body = DEEP_RE.sub(_deep, body)
    return body


SCRIPT = """<script>
document.addEventListener('click',function(e){var b=e.target.closest('[data-cp]');if(!b)return;
var box=b.closest('.cb');var pre=box&&box.querySelector('pre');if(!pre)return;var t=pre.innerText.replace(/\\n$/,'');
function ok(){var o=b.textContent;b.textContent='Đã chép';b.classList.add('done');setTimeout(function(){b.textContent=o;b.classList.remove('done')},1600)}
function fb(){var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{document.execCommand('copy');ok()}catch(x){b.textContent='Bôi đen rồi Ctrl+C'}document.body.removeChild(a)}
if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(ok,fb)}else{fb()}});
</script>"""
