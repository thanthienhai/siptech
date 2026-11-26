"""Trang phục vụ người dùng: Chọn bài toán phù hợp (tư vấn theo bộ luật), Tìm kiếm toàn trang.

Cả hai chạy hoàn toàn trong trình duyệt: không gửi câu trả lời hay từ khóa đi đâu.
"""
import html
import json
import re
from pathlib import Path

# ------------------------------------------------------------------ Chọn bài toán phù hợp

# Việc cần làm -> các nhóm bài nên xem (theo thứ tự ưu tiên). Slug phải có trong content/.
TASKS = [
    ("khach", "Trả lời khách hàng (Zalo, email, đổi trả, khiếu nại)", ["xu-ly-yeu-cau-khach", "th-phan-tich-danh-gia-khach-hang"]),
    ("hoso", "Kiểm tra chứng từ, hóa đơn, hợp đồng, hồ sơ", ["kiem-tra-ho-so-theo-quy-tac", "th-doi-soat-sao-ke-ngan-hang"]),
    ("tien", "Đối soát tiền: sao kê ngân hàng với đơn hàng", ["th-doi-soat-sao-ke-ngan-hang", "kiem-tra-ho-so-theo-quy-tac"]),
    ("tailieu", "Hỏi đáp trên tài liệu nội bộ (chính sách, bảng giá, quy định)", ["rag-tra-cuu-tai-lieu", "tri-thuc-to-chuc"]),
    ("quytrinh", "Viết quy trình, biên bản họp, bàn giao công việc", ["tri-thuc-to-chuc", "quy-trinh-nhieu-buoc"]),
    ("sodieu", "Làm sạch và gộp số liệu (danh bạ khách, báo cáo nhiều chi nhánh)", ["th-lam-sach-danh-ba-khach-hang", "th-gop-bao-cao-chi-nhanh"]),
    ("banhang", "Bán hàng online: mô tả sản phẩm, đọc đánh giá của khách", ["th-mo-ta-san-pham-hang-loat", "th-phan-tich-danh-gia-khach-hang"]),
    ("baogia", "Lập báo giá từ yêu cầu của khách", ["th-bao-gia-tu-email-yeu-cau", "xu-ly-yeu-cau-khach"]),
    ("nhansu", "Nhân sự: kiểm tra bảng chấm công trước khi tính lương", ["th-kiem-tra-bang-cham-cong"]),
    ("kho", "Kho và nhập hàng: tồn kho, đề xuất số lượng nhập", ["th-ton-kho-va-de-xuat-nhap-hang"]),
    ("tudong", "Nối nhiều việc thành một quy trình tự chạy, có người duyệt", ["quy-trinh-nhieu-buoc", "tri-thuc-to-chuc"]),
]

PAGE_TEMPLATE = """
<section class="ghero"><div class="wrap">
  <div class="crumb"><a href="index.html">Trang chủ</a> <i>/</i> Chọn bài toán phù hợp</div>
  <span class="pill">Công cụ gợi ý</span>
  <h1>Chọn bài toán phù hợp với bạn</h1>
  <p class="lead">Trả lời bốn câu ngắn, bạn sẽ có danh sách bài nên đọc theo thứ tự. Câu trả lời xử lý ngay trong trình duyệt, không gửi đi đâu.</p>
</div></section>
<section class="sec"><div class="wrap narrow">
  <form id="adv" class="adv" novalidate>
    <fieldset class="aq"><legend><span class="an">1</span> Việc bạn muốn cải thiện nhất là gì?</legend>
      <div class="aopts">__TASKS__</div></fieldset>
    <fieldset class="aq"><legend><span class="an">2</span> Quy trình xử lý việc đó đã được viết ra chưa?</legend>
      <div class="aopts">
        <label class="ao"><input type="radio" name="qt" value="chua"><span><b>Chưa</b> Mỗi người làm một kiểu, hoặc nằm trong đầu một vài người</span></label>
        <label class="ao"><input type="radio" name="qt" value="mot"><span><b>Một phần</b> Có ghi chú hoặc mẫu, nhưng còn nhiều chỗ trống</span></label>
        <label class="ao"><input type="radio" name="qt" value="co"><span><b>Có rõ ràng</b> Ai cũng làm theo cùng một quy trình</span></label>
      </div></fieldset>
    <fieldset class="aq"><legend><span class="an">3</span> Bạn (hoặc người sẽ làm) quen với máy tính tới đâu?</legend>
      <div class="aopts">
        <label class="ao"><input type="radio" name="kn" value="co-ban"><span><b>Cơ bản</b> Chủ yếu dùng điện thoại, Zalo, email; chưa dùng AI hoặc mới thử</span></label>
        <label class="ao"><input type="radio" name="kn" value="excel"><span><b>Dùng được Excel</b> Chưa dùng dòng lệnh</span></label>
        <label class="ao"><input type="radio" name="kn" value="code"><span><b>Có người biết code</b> Hoặc bạn tự chạy được script</span></label>
      </div></fieldset>
    <fieldset class="aq"><legend><span class="an">4</span> Dữ liệu của việc này có thông tin cá nhân hoặc nhạy cảm không?</legend>
      <div class="aopts">
        <label class="ao"><input type="radio" name="dl" value="co"><span><b>Có</b> Tên, số điện thoại, địa chỉ khách; lương, chấm công nhân viên; số tài khoản</span></label>
        <label class="ao"><input type="radio" name="dl" value="khong"><span><b>Không</b> Chỉ là số liệu hoặc tài liệu công khai trong công ty</span></label>
        <label class="ao"><input type="radio" name="dl" value="khong-chac"><span><b>Không chắc</b></span></label>
      </div></fieldset>
    <div class="aact"><button type="submit" class="btn pri big">Xem gợi ý</button><button type="reset" class="btn ghost" id="areset">Làm lại</button></div>
    <p class="amsg" id="amsg" role="alert" hidden>Hãy trả lời đủ cả bốn câu.</p>
  </form>
  <div id="aout" class="aout" aria-live="polite" tabindex="-1" hidden></div>
  <p class="fine">Đây là gợi ý theo bộ luật đơn giản của SIPTech dựa trên các bài hiện có trên trang <b>(Đề xuất)</b>. Nó không phải tư vấn riêng cho doanh nghiệp của bạn và chưa được đo xem có giúp người học chọn đúng hơn hay không. Cách chúng tôi làm việc: <a href="phuong-phap.html">Phương pháp</a>.</p>
</div></section>
<script>
(function(){
  var D = __DATA__;
  var form = document.getElementById('adv'), out = document.getElementById('aout'), msg = document.getElementById('amsg');
  function val(n){ var e = form.querySelector('input[name="'+n+'"]:checked'); return e ? e.value : ''; }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function link(slug, why){
    var p = D.groups[slug]; if(!p) return '';
    return '<li class="rc2"><a href="'+p.url+'"><b>'+esc(p.name)+'</b></a><span class="rm">'+esc(p.meta)+'</span><p>'+esc(why)+'</p></li>';
  }
  function build(){
    var task = D.tasks[val('task')], qt = val('qt'), kn = val('kn'), dl = val('dl');
    var steps = [], notes = [];
    var tailieu = (val('task') === 'tailieu');
    if (dl !== 'khong') {
      steps.push(link('an-toan-du-lieu', 'Đọc trước khi đưa dữ liệu khách hàng, nhân viên hay tài chính vào bất kỳ công cụ AI nào: dữ liệu nào được đưa, dữ liệu nào không.'));
      notes.push('Dữ liệu có thông tin cá nhân: thử bằng <b>dữ liệu giả hoặc đã ẩn danh</b> trước. Các bài <a href="'+D.groups['th-lam-sach-danh-ba-khach-hang'].url+'">Làm sạch danh bạ</a> và <a href="'+D.groups['th-kiem-tra-bang-cham-cong'].url+'">Kiểm tra bảng chấm công</a> có hướng dẫn ẩn danh từng bước.');
    }
    if (kn === 'co-ban') {
      steps.push(link('rag-tra-cuu-tai-lieu-c0', 'Bắt đầu không cần cài gì: dùng Claude, ChatGPT hay Gemini có sẵn, nhưng có kỷ luật (bản giao việc 6 phần, sổ prompt, quy tắc dữ liệu).'));
    } else if (kn === 'excel') {
      steps.push(link('th-bat-dau-voi-coding-agent', 'Bốn bài nhập môn: cài coding agent, làm quen dòng lệnh, giao việc đầu tiên trong thư mục riêng, quy tắc an toàn.'));
    }
    if (qt !== 'co' && val('task') !== 'quytrinh') {
      steps.push(link('tri-thuc-to-chuc', qt === 'chua'
        ? 'Chưa có quy trình thì AI không có gì để làm theo và sẽ tự điền chỗ trống, mỗi lần một kiểu. Viết SOP tối thiểu từ các ca đã xảy ra trước.'
        : 'Quy trình còn chỗ trống thì AI sẽ tự điền chỗ đó. Lấp các chỗ trống bằng SOP viết từ ca thật trước khi giao cho AI.'));
    }
    task.forEach(function(s, i){
      var why = D.why[s] || '';
      steps.push(link(s, i === 0 ? 'Bài toán gần nhất với việc bạn chọn. ' + why : why));
    });
    if (kn === 'co-ban') notes.push('Bạn chưa cần dòng lệnh. Làm các bài bằng đường không code (Project, Gem, GPT tùy chỉnh) trước; khi cần tự động hóa lặp lại thì chuyển sang <a href="'+D.groups['th-bat-dau-voi-coding-agent'].url+'">coding agent</a>.');
    if (kn === 'code') notes.push('Có người biết code: bạn có thể vào thẳng Bài 2 và Bài 3 của bài toán, dùng Bài 1 để lấy dữ liệu mẫu và prompt.');
    notes.push('Mọi con số trong bài là kết quả trên <b>dữ liệu giả</b> với số lần chạy nhỏ. Hãy đo lại trên dữ liệu của bạn và để người duyệt kết quả cuối.');
    var seen = {}; steps = steps.filter(function(h){ var k = h.slice(0, 90); if(seen[k]) return false; seen[k] = 1; return !!h; });
    var n = 0;
    out.innerHTML = '<h2>Gợi ý của SIPTech cho bạn</h2><ol class="rcl">' + steps.map(function(h){ n++; return h.replace('<li class="rc2">', '<li class="rc2" data-n="'+n+'">'); }).join('') + '</ol>'
      + '<div class="admonition tip"><p class="admonition-title">Lưu ý cho trường hợp của bạn</p><ul>' + notes.map(function(x){ return '<li>'+x+'</li>'; }).join('') + '</ul></div>';
    out.hidden = false; out.focus(); out.scrollIntoView({behavior:'smooth', block:'start'});
  }
  form.addEventListener('submit', function(e){
    e.preventDefault();
    if (!val('task') || !val('qt') || !val('kn') || !val('dl')) { msg.hidden = false; return; }
    msg.hidden = true; build();
  });
  document.getElementById('areset').addEventListener('click', function(){ out.hidden = true; msg.hidden = true; });
})();
</script>
"""


def advisor_body(groups, root_url):
    """groups: danh sách dict nhóm của build.py. Trả về HTML thân trang."""
    by = {g["slug"]: g for g in groups if g["has_pages"]}
    info = {}
    for slug, g in by.items():
        unit = g.get("unit", "cấp")
        info[slug] = {"name": g["name"], "url": f"{slug}/index.html",
                      "meta": ("Thực hành · " if g.get("lab") else "") + f'{g["n"]} {unit}' + (" · đang soạn" if g["status"] == "draft" else "")}
    # hai mục đặc biệt
    info["an-toan-du-lieu"] = {"name": "An toàn dữ liệu và pháp lý", "url": "an-toan-du-lieu-va-phap-ly-vn.html", "meta": "Tài liệu nền"}
    if "rag-tra-cuu-tai-lieu" in by:
        info["rag-tra-cuu-tai-lieu-c0"] = {"name": "Dùng AI thủ công một cách có kỷ luật (Cấp 0)",
                                           "url": "rag-tra-cuu-tai-lieu/cap-00-dung-ai-thu-cong.html", "meta": "Đường không code · Cấp 0"}
    why = {
        "xu-ly-yeu-cau-khach": "Soạn trả lời có người duyệt, phân loại mức khẩn, tra đơn chỉ đọc, hành động ghi qua phiếu duyệt.",
        "kiem-tra-ho-so-theo-quy-tac": "Chứng từ thành dữ liệu, kiểm theo quy tắc, đối chiếu nhiều nguồn, ra danh sách lỗi có căn cứ.",
        "rag-tra-cuu-tai-lieu": "Hỏi đáp trên tài liệu của bạn, trả lời kèm trích dẫn nguyên văn và biết từ chối khi thiếu căn cứ.",
        "tri-thuc-to-chuc": "Biên bản họp, SOP từ người giỏi, bàn giao: nền cho mọi bài toán khác.",
        "quy-trinh-nhieu-buoc": "Nối việc thành chuỗi có điểm duyệt, báo cáo định kỳ, đo hiệu quả trước và sau.",
        "th-doi-soat-sao-ke-ngan-hang": "Thực hành làm thật: ghép sao kê với đơn hàng bằng script do agent viết, số tiền do code tính.",
        "th-lam-sach-danh-ba-khach-hang": "Thực hành làm thật: gộp khách trùng, chuẩn hóa số điện thoại, không xóa dữ liệu.",
        "th-mo-ta-san-pham-hang-loat": "Thực hành làm thật: viết mô tả hàng loạt mà không bịa thông số.",
        "th-phan-tich-danh-gia-khach-hang": "Thực hành làm thật: từ hàng trăm đánh giá ra chủ đề, ca nguy cấp và việc nên sửa.",
        "th-bao-gia-tu-email-yeu-cau": "Thực hành làm thật: báo giá từ email lộn xộn, tiền do code tính, chiết khấu vượt quyền chuyển người quyết.",
        "th-kiem-tra-bang-cham-cong": "Thực hành làm thật: tìm bất thường trong dữ liệu chấm công đã ẩn danh.",
        "th-ton-kho-va-de-xuat-nhap-hang": "Thực hành làm thật: phân loại ABC, tồn kho an toàn, đề xuất nhập có kèm tiền vốn.",
        "th-gop-bao-cao-chi-nhanh": "Thực hành làm thật: gộp nhiều file Excel mỗi nơi một kiểu, kiểm tổng, chạy lại hằng tháng.",
    }
    tasks = {k: [s for s in v if s in info] for k, _, v in TASKS}
    data = {"groups": info, "tasks": tasks, "why": why}
    radios = "".join(
        f'<label class="ao"><input type="radio" name="task" value="{k}"><span>{html.escape(t)}</span></label>' for k, t, _ in TASKS)
    return PAGE_TEMPLATE.replace("__TASKS__", radios).replace("__DATA__", json.dumps(data, ensure_ascii=False))


# ------------------------------------------------------------------ Tìm kiếm

SEARCH_BODY = """
<section class="ghero"><div class="wrap">
  <div class="crumb"><a href="index.html">Trang chủ</a> <i>/</i> Tìm kiếm</div>
  <h1>Tìm trong SIPTech</h1>
  <p class="lead">Tìm theo tên bài, mục, từ khóa. Không cần gõ dấu: &quot;dien dan&quot; vẫn ra &quot;điền dần&quot;.</p>
</div></section>
<section class="sec"><div class="wrap narrow">
  <form id="sf" role="search" class="sform"><label class="sr" for="sq">Từ khóa</label>
    <input id="sq" type="search" placeholder="Ví dụ: đối soát, prompt, chấm công, ẩn danh" autocomplete="off" autofocus>
    <button class="btn pri" type="submit">Tìm</button></form>
  <p class="count" id="scount" aria-live="polite"></p>
  <ol class="sres" id="sres"></ol>
  <p class="empty" id="sempty" hidden>Không có kết quả. Thử từ ngắn hơn, hoặc xem <a href="bai-toan.html">tất cả bài toán</a> và <a href="tu-dien.html">từ điển thuật ngữ</a>.</p>
</div></section>
<script>
(function(){
  var idx = null, q = document.getElementById('sq'), res = document.getElementById('sres'), cnt = document.getElementById('scount'), empty = document.getElementById('sempty');
  function norm(t){ return String(t).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/đ/g,'d'); }
  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function run(){
    var terms = norm(q.value).split(/\\s+/).filter(Boolean);
    res.innerHTML = ''; empty.hidden = true;
    if (!idx || !terms.length) { cnt.textContent = ''; return; }
    var scored = [];
    idx.forEach(function(p){
      var s = 0, ok = true;
      terms.forEach(function(t){
        var m = 0;
        if (p._t.indexOf(t) > -1) m += 8;
        if (p._h.indexOf(t) > -1) m += 4;
        if (p._d.indexOf(t) > -1) m += 3;
        if (p._x.indexOf(t) > -1) m += 1;
        if (p._g.indexOf(t) > -1) m += 2;
        if (!m) ok = false; s += m;
      });
      if (ok) scored.push([s, p]);
    });
    scored.sort(function(a, b){ return b[0] - a[0]; });
    cnt.textContent = scored.length ? ('Có ' + scored.length + ' kết quả' + (scored.length > 30 ? ', hiện 30 kết quả đầu' : '')) : '';
    empty.hidden = scored.length > 0;
    res.innerHTML = scored.slice(0, 30).map(function(a){
      var p = a[1];
      return '<li class="sr1"><a href="' + p.u + '"><b>' + esc(p.t) + '</b></a>' + (p.g ? '<span class="sg">' + esc(p.g) + '</span>' : '') + '<p>' + esc(p.d) + '</p></li>';
    }).join('');
  }
  fetch('search-index.json').then(function(r){ return r.json(); }).then(function(d){
    idx = d.map(function(p){ p._t = norm(p.t); p._h = norm(p.h); p._d = norm(p.d); p._x = norm(p.x); p._g = norm(p.g || ''); return p; });
    var u = new URLSearchParams(location.search).get('q'); if (u) q.value = u; run();
  }).catch(function(){ cnt.textContent = 'Không tải được chỉ mục tìm kiếm. Hãy thử lại sau.'; });
  q.addEventListener('input', run);
  document.getElementById('sf').addEventListener('submit', function(e){ e.preventDefault(); run(); });
})();
</script>
"""


def build_search_index(out_dir):
    """Quét các trang HTML đã dựng, tạo search-index.json (tiêu đề, nhóm, mục, mô tả, đoạn đầu)."""
    out_dir = Path(out_dir)
    entries = []
    for f in sorted(out_dir.rglob("*.html")):
        rel = f.relative_to(out_dir).as_posix()
        if rel in ("404.html", "tim-kiem.html"):
            continue
        t = f.read_text(encoding="utf-8")
        m = re.search(r"<title>(.*?)</title>", t, re.S)
        title = html.unescape(m.group(1)).replace(" · SIPTech", "") if m else rel
        d = re.search(r'<meta name="description" content="([^"]*)"', t)
        desc = html.unescape(d.group(1)) if d else ""
        art = re.search(r"<article.*?</article>", t, re.S)
        body = art.group(0) if art else t
        heads = " · ".join(html.unescape(re.sub(r"<[^>]+>", "", h)) for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body, re.S))
        plain = re.sub(r"<script.*?</script>|<style.*?</style>|<pre.*?</pre>", " ", body, flags=re.S)
        plain = html.unescape(re.sub(r"<[^>]+>", " ", plain))
        plain = re.sub(r"\s+", " ", plain).strip()
        g = ""
        if "/" in rel:
            g = title.split(" · ")[-1] if " · " in title else ""
        entries.append({"t": title.split(" · ")[0] if g else title, "g": g, "u": rel, "d": desc, "h": heads[:700], "x": plain[:900]})
    (out_dir / "search-index.json").write_text(json.dumps(entries, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return len(entries)
