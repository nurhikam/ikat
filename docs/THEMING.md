# Membuat tema baru

Standar ini ada supaya template ke-2, ke-10, ke-50 bisa dibuat tanpa menyentuh
JavaScript sama sekali. Kalau kamu membuat tema baru dan mendapati dirinya harus
mengubah `engine.js`, berhenti — itu tanda ada token atau section yang kurang.
Tambahkan tokennya, jangan fork enginenya.

## Tiga lapis, tanggung jawab terpisah

```
data/*.json           APA isinya      nama, tanggal, venue, rekening, urutan section
engine/engine.js      APA strukturnya DOM + kelas + perilaku (countdown, RSVP, musik)
engine/engine.css     BAGAIMANA tata letaknya  spacing, state, motion, aksesibilitas
themes/<nama>/        BAGAIMANA rasanya         warna, font, ornamen
```

Aturan yang membuat ini tetap murah dirawat:

| Lapis | Boleh | Tidak boleh |
|---|---|---|
| `data/*.json` | apa saja | — |
| `engine/*` | struktur & perilaku universal | warna, font, ornamen spesifik tema |
| `themes/*` | override token, blok "decoration" pendek | mengubah DOM, menambah JS, mengubah urutan section |

Kalau ketiganya dijaga, mengganti tema = mengganti satu `<link>`.

## Bikin tema baru

Tema **tidak lagi ditulis tangan sebagai CSS**. Semuanya dirender dari satu
spec, `themes/themes.json`, oleh `bin/make-theme.py`.

Alasannya: blok token tiap tema itu ~80% struktur yang sama (nama variabel,
urutan, komentar). Menulis tangan sebelas kali berarti sebelas kesempatan untuk
melenceng, dan tema ke-12 jadi mahal. Yang benar-benar membedakan tema cuma blok
dekorasinya, dan itu tetap ditulis tangan.

### 1. Tambah satu entri di `themes/themes.json`

```json
{
  "slug": "nama-tema", "name": "Nama Tema",
  "blurb": "Satu kalimat buat galeri di landing page.",
  "mood": "pastel",            // pastel | hangat | unik  (jadi label di galeri)
  "pattern": "dots",           // none|dots|grid|arcs|waves|chevron|petals|stars|grain|ikat
  "fonts": { "display": "...", "heading": "...", "body": "...",
             "displayStack": "...", "headingStack": "...", "bodyStack": "..." },
  "colors": { ... 12 nilai ... },
  "shape":  { ... 9 nilai ... },
  "tracking": "0.24em"
}
```

`display`/`heading`/`body` itu nama keluarga font buat query Google Fonts;
`*Stack` itu nilai CSS lengkap dengan fallback-nya.

### 2. Render

```bash
./bin/make-theme.py nama-tema      # satu tema
./bin/make-theme.py                # semua
```

### 3. Pilih layout-nya

Warna dan font saja tidak cukup. Sebelum ada slot ini, 113 tema punya urutan
section yang sama, kolom galeri yang sama, dan tinggi yang cuma beda karena
metrik font — jadi di bawah sampulnya semuanya satu template.

```json
"layout": {
  "flow":    "classic | story-first | date-first | gallery-early",
  "gallery": "duo | trio | masonry | filmstrip | stack | mosaic",
  "couple":  "stacked | split | offset | framed",
  "event":   "centered | split | ticket | plain",
  "card":    "boxed | bleed | edge"
}
```

| Slot | Yang diubah |
|---|---|
| `flow` | urutan section (lewat `order` flexbox, DOM dan data tidak berubah) |
| `gallery` | model kolom: 2/3 kolom, masonry, gulir samping, satu kolom zigzag, mosaik |
| `couple` | mempelai ditumpuk tengah, dibelah kiri-kanan, digeser, atau dibingkai |
| `event` | kartu tengah, dibelah dua kolom, bentuk karcis, atau cuma garis |
| `card` | kartu berkotak, melebar penuh, atau dilepas jadi garis saja |

Semua varian ada di `bin/theme_layouts.py`. `theme_layouts.spread(index)` membagi
varian merata kalau kamu menambah banyak tema sekaligus.

**Kalau menambah varian galeri baru:** engine memberi item pertama
`grid-column: span 2` supaya jadi hero di grid 2 kolom bawaan. Varian yang
mengubah model kolom **wajib** me-reset `.u-gallery__item:first-child
{ grid-column: auto }`. Tanpa itu item pertama tetap minta dua kolom, grid
membuat kolom implisit, dan thumbnail mengkerut jadi 29px. Tiga varian kena ini
sekaligus sebelum ketahuan.

### 4. Kalau butuh bentuk yang token tidak bisa ungkapkan

Buat `themes/nama-tema/decoration.css`. Isinya digabungkan apa adanya di bawah
blok token waktu render. Di sinilah cincin emas `forest-lace` dan rendanya
tinggal. Kalau file ini lewat ~80 baris, kemungkinan besar kamu sedang melawan
engine: tambah tokennya, jangan lawan.

### 5. Lihat hasilnya

```
preview.html?theme=nama-tema
```

Tema baru otomatis muncul di galeri landing page setelah `./bin/make-site.py` —
tidak ada daftar manual yang perlu diingat.

**Jangan pernah mengedit `themes/<slug>/theme.css` langsung.** File itu
digenerate dan akan tertimpa. Edit spec-nya, atau `decoration.css`.

## Token

### Warna

| Token | Untuk |
|---|---|
| `--u-bg` | latar utama undangan |
| `--u-bg-2` | latar halaman di luar kolom (desktop) |
| `--u-surface` | permukaan kartu terang |
| `--u-surface-2` | permukaan sekunder, dasar placeholder foto |
| `--u-ink` | teks di atas `--u-surface` |
| `--u-ink-soft` | teks sekunder di atas `--u-surface` |
| `--u-ink-invert` | teks di atas `--u-bg` |
| `--u-accent` | logam/aksen: tombol utama, garis, cincin foto |
| `--u-accent-ink` | teks di atas `--u-accent` |
| `--u-highlight` | satu aksen kontras — dipakai tanggal aktif & wax seal |
| `--u-line` | garis pemisah di atas surface |
| `--u-line-invert` | garis pemisah di atas bg |

### Tipografi

`--u-font-display`, `--u-font-heading`, `--u-font-body`, `--u-font-arabic`,
`--u-size-display`, `--u-size-h2`, `--u-size-h3`, `--u-size-body`,
`--u-size-small`, `--u-leading`, `--u-tracking-caps`.

Ukuran memakai `clamp()` — ganti nilainya, jangan ganti jadi angka mati, kalau
tidak tipografi berhenti responsif.

### Bentuk & ritme

Siluet itu separuh dari yang membedakan satu tema dengan tema lain. Warna saja
membuat sepuluh tema terlihat seperti satu tema dalam sepuluh suasana hati.

| Token | Untuk | Contoh nilai |
|---|---|---|
| `--u-frame-radius` | potret sampul | `50% / 42%` oval, `999px 999px 0 0` gapura, `0` kotak |
| `--u-frame-border` | cincin sampul | `6px solid #fff`, `1px solid var(--u-accent)`, `0` |
| `--u-avatar-radius` | potret mempelai | `50%`, `999px 999px 14px 14px` |
| `--u-photo-radius` | foto galeri | `0px`, `14px`, `999px 999px 0 0` |
| `--u-pill-radius` | tanggal aktif, badge | `999px` atau `0px` |
| `--u-polaroid-tilt` | foto penutup | `-2.5deg`, atau `0deg` biar tegak |
| `--u-shadow` | bayangan bersama | `0 18px 40px rgba(0,0,0,.35)`, atau `8px 8px 0 #000` untuk kesan cetak |

Plus `--u-radius`, `--u-radius-lg`, `--u-gutter`, `--u-sec-y`, `--u-stack`, `--u-max`.

`--u-max` (default `30rem`) menahan undangan tetap selebar ponsel di desktop.
Naikkan hanya kalau tema memang dirancang lebar.

### Dekorasi & motion

`--u-orn-top`, `--u-orn-bottom`, `--u-orn-size`, `--u-texture`, `--u-ease`, `--u-dur`.

Setiap section otomatis punya dua slot ornamen (`.u-orn--top`, `.u-orn--bottom`).
Engine hanya menyediakan slotnya; tema yang memutuskan diisi apa — atau
disembunyikan, seperti `forest-lace` menyembunyikan renda di cover dan closing.

## Aturan ornamen: SVG, bukan PNG

`forest-lace` tidak mengirim satu pun file raster. Renda, cincin emas, tekstur
daun, dan wax seal semuanya CSS/SVG — total tema ~7 KB gzip.

Ini bukan kerapian belaka, ini fitur produk. Tamu membuka undangan di parkiran
gedung dengan sinyal satu bar. Undangan pesaing yang mengirim 8 MB watercolor
PNG akan gagal di situ. Kalau sebuah tema benar-benar butuh raster, kompres ke
WebP dan jaga total aset di bawah 300 KB.

## Catatan yang menghemat waktumu

- **Font script butuh ruang vertikal.** Ascender dan descender-nya panjang.
  Naikkan `--u-leading` atau margin ampersand, jangan pakai `line-height` < 1.
- **Section kosong hilang sendiri.** `gallery` tanpa foto dan `story` tanpa item
  tidak merender apa pun. Tema tidak perlu mengantisipasi keadaan kosong.
- **Foto boleh tidak ada.** Tanpa `photo`, engine merender monogram, bukan frame
  rusak. Ini keadaan yang didukung penuh, bukan degradasi — pasangan tanpa foto
  prewedding adalah segmen nyata. Pastikan monogram terbaca di temamu.
- **Uji dua-duanya.** Buka dengan `?to=Nama%20Tamu` dan tanpa parameter.
- **`prefers-reduced-motion` sudah ditangani engine.** Jangan tambahkan animasi
  di tema tanpa guard yang sama.

## Checklist sebelum tema dianggap selesai

- [ ] Terbaca di lebar 320 px dan 430 px
- [ ] Kontras teks ≥ 4.5:1 pada `--u-surface` maupun `--u-bg`
- [ ] Focus ring terlihat saat tab lewat form RSVP
- [ ] Tanpa foto sama sekali, undangan masih tampak sengaja
- [ ] Total aset tema di bawah 300 KB
- [ ] `prefers-reduced-motion: reduce` tidak menyisakan animasi
- [ ] Console bersih
