#!/usr/bin/env python3
"""Render site/index.html (landing page Ikat) dari themes/themes.json.

    ./bin/make-site.py

Galerinya digenerate dari spec tema yang sama yang dipakai bin/make-theme.py,
jadi nambah tema ke-12 otomatis nongol di halaman jualan. Nggak ada daftar
manual yang bisa basi.

Harga disandarkan ke survei pasar undangan digital Indonesia, bukan karangan:
modal reseller di pasar sekitar Rp 20rb/undangan, reseller jual Rp 80-99rb,
platform vendor Rp 1,5jt-5jt. Angka hitungan reseller di halaman ditandai
sebagai contoh, bukan janji.
"""

from __future__ import annotations

import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "themes", "themes.json")
OUT = os.path.join(ROOT, "site", "index.html")

E = html.escape

PLANS = [
    {
        "name": "Basic", "for": "Buat yang butuh cepat dan beres",
        "price": "Rp 99.000", "unit": "sekali bayar",
        "features": [
            "Pilih 1 dari 101 tema",
            "Link personal per tamu",
            "RSVP dan dinding tamu",
            "Hitung mundur dan tombol lokasi",
            "Aktif 1 tahun",
        ],
        "cta": "Pesan Basic", "hero": False,
    },
    {
        "name": "Plus", "for": "Paling banyak dipakai",
        "price": "Rp 199.000", "unit": "sekali bayar",
        "features": [
            "Semua 101 tema, boleh gonta-ganti",
            "Warna disesuaikan foto kalian",
            "Galeri foto dan musik pilihan sendiri",
            "Amplop digital dan salin rekening",
            "Rekap tamu bisa diunduh",
            "Aktif 2 tahun",
        ],
        "cta": "Pesan Plus", "hero": True,
    },
    {
        "name": "Custom", "for": "Kalau maunya nggak ada di daftar",
        "price": "Rp 499.000", "unit": "sekali bayar",
        "features": [
            "Tema dirancang khusus dari nol",
            "Nama domain sendiri",
            "Ilustrasi atau motif custom",
            "Dua kali revisi desain",
            "Aktif selamanya, file diserahkan",
        ],
        "cta": "Diskusi Custom", "hero": False,
    },
]

WHY = [
    ("22 KB", "Kebuka sebelum tamu sempat nutup",
     "Halaman pertama cuma 22 KB (terkompresi), diukur dari situs yang beneran live, bukan di "
     "laptop sendiri. Undangan yang ngirim 5 MB bakal gagal di parkiran gedung dengan sinyal "
     "satu bar, dan di situlah tamu kalian bakal membukanya."),
    ("01", "Tiap tamu dapat namanya sendiri",
     "Link-nya bawa nama tamu, muncul di sampul, dan form RSVP-nya terisi otomatis. Nggak perlu "
     "mereka ngetik ulang."),
    ("02", "Ganti tema tanpa ulang dari awal",
     "Data kalian kepisah dari tampilan. Ganti tema itu satu setelan, bukan bikin ulang. "
     "101 tema, semuanya bisa dicoba sebelum mutusin."),
    ("03", "Nggak punya foto prewed? Tetap jadi",
     "Tanpa foto, sampulnya berubah jadi monogram terukir yang memang dirancang, bukan kotak "
     "kosong. Banyak pasangan nggak sempat atau nggak mau prewed, dan itu bukan versi cacat."),
]

FAQ = [
    ("Berapa lama sampai jadi?",
     "Kalau datanya sudah lengkap, Basic dan Plus biasanya jadi di hari yang sama. Custom butuh "
     "beberapa hari karena temanya dirancang dari nol."),
    ("Tamu perlu install aplikasi?",
     "Nggak. Undangannya halaman web biasa, dibuka lewat link di WhatsApp. Jalan di HP apa pun "
     "yang punya browser."),
    ("Data RSVP masuk ke mana?",
     "Ke spreadsheet atau database milik kalian sendiri, dan bisa diunduh kapan saja. Kami nggak "
     "nyimpen daftar tamu kalian di tempat yang nggak bisa kalian ambil."),
    ("Bisa pakai lagu sendiri?",
     "Bisa, tinggal kirim filenya. Bawaan tiap tema pakai piano yang kami bikin sendiri supaya "
     "aman dipakai berulang. Kalau mau lagu komersial, pastikan kalian punya izinnya, karena "
     "undangan yang disebar ke ratusan orang itu hitungannya menyebarkan lagu itu."),
    ("Bisa pakai domain sendiri?",
     "Bisa di paket Custom dan Reseller. Basic dan Plus pakai subdomain kami."),
    ("Kalau acaranya batal atau ganti tanggal?",
     "Ganti tanggal gratis, tinggal bilang. Isi undangan memang dirancang buat bisa diubah tanpa "
     "bikin ulang halamannya."),
]


CATS = [
    ("semua", "Semua"),
    ("adat", "Adat"),
    ("pop", "Pop Culture"),
    ("pastel", "Pastel"),
    ("hangat", "Hangat"),
    ("unik", "Unik"),
]
# 12 featured buat landing — 1 page tanpa scroll panjang
FEATURED = [
    "forest-lace", "batik-solo", "spiderman", "barbie-dream",
    "ghibli-breeze", "cherry-blossom", "olive-grove", "sunset-blvd",
    "noir-editorial", "bauhaus", "terrazzo", "y2k-chrome",
]

def theme_card(t: dict) -> str:
    cat = E(t.get("category", t.get("mood", "unik")))
    return f"""        <a class="theme rise" href="preview.html?theme={E(t['slug'])}" target="_blank" rel="noopener" data-cat="{cat}">
          <div class="theme__shot">
            <img src="thumbs/{E(t['slug'])}.webp" alt="Tema {E(t['name'])}" loading="lazy" decoding="async" width="440" height="749">
          </div>
          <p class="theme__name">{E(t['name'])}</p>
          <p class="theme__blurb">{E(t['blurb'])}</p>
          <span class="theme__tag">{cat}</span>
        </a>"""


def plan_card(p: dict) -> str:
    feats = "\n".join(f"            <li>{E(x)}</li>" for x in p["features"])
    badge = '<span class="plan__badge">Paling laku</span>\n          ' if p["hero"] else ""
    return f"""        <div class="plan{' plan--hero' if p['hero'] else ''} rise">
          {badge}<p class="plan__name">{E(p['name'])}</p>
          <p class="plan__for">{E(p['for'])}</p>
          <p class="plan__price">{E(p['price'])} <span class="plan__unit">{E(p['unit'])}</span></p>
          <ul class="plan__list">
{feats}
          </ul>
          <a class="btn btn--{'primary' if p['hero'] else 'ghost'}" href="#kontak">{E(p['cta'])}</a>
        </div>"""


def build() -> str:
    themes = json.load(open(SPEC, encoding="utf-8"))["themes"]
    n = len(themes)
    by_slug = {t["slug"]: t for t in themes}
    featured = [by_slug[s] for s in FEATURED if s in by_slug]
    featured_cards = "\n".join(theme_card(t) for t in featured)
    all_cards = "\n".join(theme_card(t) for t in themes)
    filter_btns = "\n".join(
        f'          <button class="chip{" chip--on" if v=="semua" else ""}" data-filter="{E(v)}">{E(label)}</button>'
        for v, label in CATS)
    plans = "\n".join(plan_card(p) for p in PLANS)
    why = "\n".join(
        f"""        <div class="why__item rise">
          <p class="why__n">{E(k)}</p>
          <h3>{E(h)}</h3>
          <p>{E(b)}</p>
        </div>""" for k, h, b in WHY)
    faq = "\n".join(
        f"""        <details>
          <summary>{E(q)}</summary>
          <p>{E(a)}</p>
        </details>""" for q, a in FAQ)

    # Tiga tema buat tumpukan di hero: satu pastel, satu gelap, satu nyeleneh.
    stack = ["butter", "noir-editorial", "riso-zine"]
    stack_imgs = "\n".join(
        f'          <img src="thumbs/{s}.webp" alt="" width="440" height="749" loading="eager">'
        for s in stack)

    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ikat - Undangan pernikahan digital yang kebuka cepat</title>
<meta name="description" content="{n} tema undangan pernikahan digital. Halaman pertama 22 KB, jadi kebuka walau sinyal tamu cuma satu bar. Link personal per tamu, RSVP, dan rekap yang bisa diunduh.">
<meta name="theme-color" content="#faf9f7">

<meta property="og:title" content="Ikat - Undangan pernikahan digital yang kebuka cepat">
<meta property="og:description" content="{n} tema, halaman pertama 22 KB, link personal per tamu.">
<meta property="og:type" content="website">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="site.css">
</head>
<body>

<header class="nav">
  <div class="wrap nav__in">
    <a class="nav__logo" href="#"><span class="nav__mark" aria-hidden="true"></span>Ikat</a>
    <nav class="nav__links">
      <a href="#tema">Tema</a>
      <a href="#kenapa">Kenapa Ikat</a>
      <a href="#harga">Harga</a>
      <a href="#vendor">Vendor</a>
    </nav>
    <a class="btn btn--primary" href="preview.html?theme=butter" target="_blank" rel="noopener">Coba Demo</a>
  </div>
</header>

<main>

  <section class="hero">
    <div class="wrap hero__in">
      <div>
        <p class="hero__eyebrow">{n} tema siap pakai</p>
        <h1>Undangan yang <em>kebuka</em>, bukan yang bikin tamu nunggu.</h1>
        <p class="hero__sub">Halaman pertamanya 22 KB. Tamu kalian buka di parkiran gedung dengan sinyal satu bar, dan tetap muncul.</p>
        <div class="hero__cta">
          <a class="btn btn--primary" href="preview.html?theme=butter" target="_blank" rel="noopener">Coba Demo</a>
          <a class="btn btn--ghost" href="#harga">Lihat Harga</a>
        </div>
      </div>
      <div class="stack" aria-hidden="true">
{stack_imgs}
      </div>
    </div>
  </section>

  <section class="sec sec--alt" id="tema">
    <div class="wrap">
      <div class="sec__head">
        <h2>{n} tema, semuanya bisa dibuka sekarang</h2>
        <p>Bukan gambar contoh. Tiap kartu di bawah membuka undangan sungguhan yang jalan, lengkap dengan hitung mundur dan RSVP-nya.</p>
      </div>
      <div class="themes">
{featured_cards}
      </div>
      <p style="text-align:center;margin-top:1.75rem"><a class="btn btn--ghost" href="galeri.html">Lihat semua {n} tema &rarr;</a></p>
    </div>
  </section>

  <section class="sec" id="kenapa">
    <div class="wrap">
      <div class="sec__head">
        <h2>Yang bikin beda bukan bunganya</h2>
        <p>Undangan cantik itu barang biasa sekarang. Empat hal ini yang jarang diurus orang.</p>
      </div>
      <div class="why">
{why}
      </div>
    </div>
  </section>

  <section class="sec sec--alt" id="harga">
    <div class="wrap">
      <div class="sec__head">
        <h2>Harga</h2>
        <p>Sekali bayar, nggak ada langganan. Harga di bawah sudah termasuk pemasangan data kalian.</p>
      </div>
      <div class="plans">
{plans}
      </div>

      <div class="vendor" id="vendor">
        <div>
          <h3>Buat WO, percetakan, dan MUA</h3>
          <p>Kalian sudah punya kliennya tiap bulan. Ambil paket reseller, pakai brand sendiri, dan tetapkan harga jual kalian sendiri. Kami nggak muncul di depan klien kalian.</p>
          <a class="btn btn--primary" href="#kontak">Jadi Reseller</a>
        </div>
        <div class="math">
          <div class="math__row"><span>Paket 50 undangan</span><span>Rp 990.000</span></div>
          <div class="math__row"><span>Modal per undangan</span><span>Rp 19.800</span></div>
          <div class="math__row"><span>Harga jual umum di pasar</span><span>Rp 99.000</span></div>
          <div class="math__row math__row--total"><span>Selisih per undangan</span><span>Rp 79.200</span></div>
          <p class="math__note">Contoh hitungan, bukan janji hasil. Harga jual dipakai dari rentang yang umum dipasang reseller undangan digital di Indonesia; angka kalian tergantung cara dan pasar kalian sendiri.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="sec" id="tanya">
    <div class="wrap">
      <div class="sec__head">
        <h2>Yang sering ditanya</h2>
      </div>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="sec sec--alt" id="kontak">
    <div class="wrap sec__head" style="margin-bottom:0">
      <h2>Mau mulai?</h2>
      <p>Kirim tanggal, nama kalian berdua, dan tema yang disuka. Sisanya kami yang urus.</p>
      <p style="margin-top:1.5rem">
        <a class="btn btn--primary" href="https://wa.me/">Chat WhatsApp</a>
      </p>
    </div>
  </section>

</main>

<footer class="foot">
  <div class="wrap foot__in">
    <span>Ikat - undangan pernikahan digital</span>
    <span><a href="https://github.com/nurhikam/ikat" target="_blank" rel="noopener">Kode sumbernya terbuka</a></span>
  </div>
</footer>

<script>
  // Reveal saat masuk layar. IntersectionObserver, bukan listener scroll -
  // listener scroll jalan tiap frame dan bikin patah-patah di HP murah.
  (function () {{
    var items = [].slice.call(document.querySelectorAll('.rise'));
    if (!('IntersectionObserver' in window) ||
        window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
      items.forEach(function (n) {{ n.classList.add('in'); }});
      return;
    }}
    var io = new IntersectionObserver(function (es) {{
      es.forEach(function (e) {{
        if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }}
      }});
    }}, {{ rootMargin: '0px 0px -8% 0px', threshold: 0.06 }});
    items.forEach(function (n, i) {{
      n.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(n);
    }});
  }})();
</script>

</body>
</html>
"""


def build_galeri() -> str:
    themes = json.load(open(SPEC, encoding="utf-8"))["themes"]
    n = len(themes)
    all_cards = "\n".join(theme_card(t) for t in themes)
    filter_btns = "\n".join(
        f'          <button class="chip{" chip--on" if v=="semua" else ""}" data-filter="{E(v)}">{E(label)}</button>'
        for v, label in CATS)
    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Galeri — {n} tema Ikat</title>
<meta name="description" content="{n} tema undangan pernikahan digital Ikat. Filter per kategori.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap">
<link rel="stylesheet" href="site.css">
</head>
<body>
<header class="nav">
  <div class="wrap nav__in">
    <a class="nav__logo" href="index.html"><span class="nav__mark" aria-hidden="true"></span>Ikat</a>
    <nav class="nav__links">
      <a href="index.html#tema">Tema</a>
      <a href="index.html#kenapa">Kenapa Ikat</a>
      <a href="index.html#harga">Harga</a>
    </nav>
    <a class="btn btn--primary" href="preview.html?theme=butter" target="_blank" rel="noopener">Coba Demo</a>
  </div>
</header>
<main>
  <section class="sec">
    <div class="wrap">
      <div class="sec__head">
        <h2>Galeri — {n} tema</h2>
        <p>Saring per kategori atau cari. Tiap kartu buka undangan sungguhan.</p>
      </div>
      <div class="gallery__bar">
        <div class="chips">
{filter_btns}
        </div>
        <input class="gallery__search" type="search" placeholder="Cari: batik, pastel, spiderman…" aria-label="Cari tema">
      </div>
      <p class="gallery__count" aria-live="polite"></p>
      <div class="themes" id="galeri-grid">
{all_cards}
      </div>
    </div>
  </section>
</main>
<footer class="foot">
  <div class="wrap foot__in">
    <span>Ikat — undangan pernikahan digital</span>
    <span><a href="https://github.com/nurhikam/ikat" target="_blank" rel="noopener">Kode sumbernya terbuka</a></span>
  </div>
</footer>
<script>
(function () {{
  var chips=[].slice.call(document.querySelectorAll('.chip'));
  var cards=[].slice.call(document.querySelectorAll('#galeri-grid .theme'));
  var search=document.querySelector('.gallery__search');
  var count=document.querySelector('.gallery__count');
  var active='semua';
  function apply() {{
    var q=(search.value||'').toLowerCase().trim();
    var shown=0;
    cards.forEach(function (c) {{
      var cat=(c.getAttribute('data-cat')||'').toLowerCase();
      var name=(c.querySelector('.theme__name')||{{textContent:''}}).textContent.toLowerCase();
      var okCat=active==='semua'||cat===active;
      var okQ=!q||name.indexOf(q)!==-1||cat.indexOf(q)!==-1;
      var show=okCat&&okQ;
      c.style.display=show?'':'none';
      if(show) shown++;
    }});
    count.textContent=shown+' tema';
    var params=new URLSearchParams(location.search);
    if(active!=='semua') params.set('cat',active); else params.delete('cat');
    if(q) params.set('q',q); else params.delete('q');
    history.replaceState(null,'',params.toString()?'?'+params.toString():location.pathname);
  }}
  chips.forEach(function (b) {{
    b.addEventListener('click',function() {{
      chips.forEach(function(x){{x.classList.remove('chip--on')}});
      b.classList.add('chip--on');
      active=b.getAttribute('data-filter')||'semua';
      apply();
    }});
  }});
  if(search) search.addEventListener('input',apply);
  // init dari URL ?cat=&q=
  try{{
    var p=new URLSearchParams(location.search);
    var c=p.get('cat'); if(c){{ active=c; chips.forEach(function(b){{b.classList.toggle('chip--on',b.getAttribute('data-filter')===c)}}); }}
    var q=p.get('q'); if(q&&search) search.value=q;
  }}catch(e){{}}
  apply();
  // reveal
  var items=[].slice.call(document.querySelectorAll('.rise'));
  if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches){{
    items.forEach(function(n){{n.classList.add('in')}});
  }} else {{
    var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}})}},{{rootMargin:'0px 0px -8% 0px',threshold:0.06}});
    items.forEach(function(n,i){{n.style.transitionDelay=(i%4)*70+'ms';io.observe(n)}});
  }}
}})();
</script>
</body>
</html>
"""

def main() -> int:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    h = build()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(h)
    g = build_galeri()
    out2 = os.path.join(ROOT, "site", "galeri.html")
    with open(out2, "w", encoding="utf-8") as f:
        f.write(g)
    n = len(json.load(open(SPEC, encoding="utf-8"))["themes"])
    print(f"site/index.html  ({len(h)/1024:.1f} KB, 12 featured)")
    print(f"site/galeri.html ({len(g)/1024:.1f} KB, {n} tema + filter)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
