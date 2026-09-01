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

## Bikin tema baru dalam 5 langkah

```bash
cp -r themes/forest-lace themes/nama-tema-baru
```

1. **Ganti palet.** Sembilan token warna di `:root`. Itu saja sudah mengubah
   seluruh undangan.
2. **Ganti tiga font.** `--u-font-display` (nama mempelai), `--u-font-heading`
   (judul section), `--u-font-body`. Plus `--u-font-arabic` kalau ada ayat.
3. **Ganti ornamen.** `--u-orn-top` / `--u-orn-bottom` menerima `url()` SVG
   data-URI. Set `none` kalau tema tidak butuh ornamen antar-section.
4. **Ganti tekstur latar.** `--u-texture` — gradient, SVG pattern, atau `none`.
5. **Rapikan blok decoration.** Bagian paling bawah file. Kalau blok ini lewat
   ~80 baris, kemungkinan besar kamu sedang melawan engine.

Lalu daftarkan di `index.html`:

```html
<link rel="stylesheet" href="themes/nama-tema-baru/theme.css" data-theme="nama-tema-baru">
```

Atau serahkan ke data — `"theme": "nama-tema-baru"` di JSON — kalau kamu memang
mau tema dipilih saat runtime (dipakai template switcher; sedikit lebih lambat
karena CSS baru diminta setelah JSON turun).

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

`--u-radius`, `--u-radius-lg`, `--u-gutter`, `--u-sec-y`, `--u-stack`, `--u-max`.

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
