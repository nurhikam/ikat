# Ikat

**Live: https://nurhikam.github.io/ikat/** · **Galeri: https://nurhikam.github.io/ikat/galeri.html**

Undangan pernikahan digital. **113 tema**, satu JSON per klien, tanpa build step
di sisi klien (semua di-generate dulu, yang di-deploy persis yang ada di repo).

*Ikat* artinya mengikat, dan juga teknik tenun bermotif. Dua-duanya pas untuk
sesuatu yang menjual motif.

Halaman pertama undangan **22 KB terkompresi**, diukur dari deployment live dan
bukan dari localhost. Musik (751 KB) dan foto (190 KB) baru diambil setelah
tamu menekan tombol.

## Coba

| | |
|---|---|
| Landing page | https://nurhikam.github.io/ikat/ |
| Undangan demo | https://nurhikam.github.io/ikat/preview.html?theme=butter |
| Ganti tema | https://nurhikam.github.io/ikat/preview.html?theme=<slug> |
| Galeri + filter | https://nurhikam.github.io/ikat/galeri.html |

## Jalankan lokal

```bash
python3 -m http.server 8000
```

Tanpa dependency, tanpa `npm install`, tanpa bundler.

## Struktur

```
themes/themes.json        SATU sumber kebenaran untuk semua tema
bin/make-theme.py         themes.json  -> themes/<slug>/theme.css
bin/make-site.py          themes.json  -> site/index.html + site/galeri.html
bin/make-thumbs.py        screenshot cover asli per tema (Playwright) -> site/thumbs/
bin/new-client.sh         bikin undangan buat satu klien
bin/build-single.py       bundel jadi satu file HTML
bin/make-og.py            banner OG 1200x630
bin/make-music.py         render piano bawaan tema dari kode

engine/engine.js          renderer + perilaku, universal, tak pernah disentuh per tema
engine/engine.css         tata letak, state, motion, aksesibilitas
themes/<slug>/            theme.css (digenerate) + decoration.css (ditulis tangan)
data/<klien>.json         isi undangan + urutan section
site/                     landing: index.html, galeri.html, site.css, thumbs/, og.png
```

Kontrak yang bikin ini bisa dijual berulang:

> **Tema tidak boleh menyentuh JavaScript. Data tidak boleh menyentuh CSS.**

Semua tema dibangun tanpa mengubah `engine.js` satu baris pun. Kalau tema
berikutnya ternyata butuh, itu tandanya ada token yang kurang: tambahkan
tokennya, jangan fork enginenya.

### Beda tema = beda layout, bukan cuma warna

Siluet (layout) adalah separuh yang bikin tema keliatan beda; warna doang bikin
seratus tema keliatan satu tema dalam seratus mood. Karena itu semua layout
dikerjakan di `decoration.css` per tema via CSS murni, lewat dua hook:

1. **Reorder alur section** — `#app { display:flex }` + `order:` per
   `[data-sec]`. Tema bisa mulai dari event, countdown, atau couple — bukan
   selalu cover → quote → countdown.
2. **Cover composition** — `.u-cover__frame` di-shape/di-posisikan ulang:
   full-bleed foto (teks overlay), arch, oval, organic blob, polaroid rotated,
   atau kartu inset.

## Katalog tema

113 tema dalam 6 kategori (filter di galeri): **atelier** (12), **adat** (12),
**pop** (10), **pastel** (12), **hangat** (19), **unik** (48).

### Atelier Collection — 12 tema quiet luxury

Koleksi premium di atas 101 tema biasa: desaturated warm neutrals, tactile
(blind emboss, wax seal, pearl strand, torn paper), font pairing 3 tingkat
(high-contrast serif + script + clean sans). Setiap tema punya layout signature
sendiri:

| Slug | Layout cover |
|---|---|
| `atelier-emboss` | full-bleed grayscale, teks atas |
| `atelier-sage-arch` | arch foto tinggi |
| `atelier-pearl` | oval + pearl strand, couple side-by-side |
| `atelier-burgundy` | full-bleed burgundy + gold frame |
| `atelier-torn` | full-bleed + torn-paper edge |
| `atelier-cream` | oval hangat, story jadi cards |
| `atelier-mauve` | organic blob frame |
| `atelier-editorial` | full-bleed, names kiri-bawah, alur mulai dari event |
| `atelier-layered` | double-frame ghosted, gallery overlap |
| `atelier-royal` | full-bleed + double gold cartouche |
| `atelier-lace` | arch + lace scallop |
| `atelier-noir` | full-bleed cinematic, countdown pertama |

### 101 tema lama — 8 layout family

Dibagi ke keluarga layout sesuai karakter kategorinya (di-append ke
`decoration.css` tiap tema, idempotent):

| Family | Tema |
|---|---|
| arch (frame budaya) | adat — batik-solo, kebaya-velvet, jogja-senja, … |
| oval (lembut) | pastel — rosewater, lilac-haze, cherry-blossom, … |
| bloom (organic blob) | hangat — sunflower, marrakech, desert-bloom, … |
| cine (full-bleed) | pop gelap — star-wars, ocean-depth, … |
| editorial (names kiri-bawah) | pop vivid + unik bold — barbie-dream, terrazzo, bauhaus, … |
| glow (dark + inner frame) | unik gelap — velvet-plum, midnight-rose, ruby-gala, … |
| paper (polaroid rotated) | unik terang — riso-zine, origami, wabi-sabi, … |
| journal (couple-first) | butter, eucalyptus, glass-morphism, … |

## Bikin undangan buat klien

```bash
./bin/new-client.sh andi-sari butter
$EDITOR data/andi-sari.json
```

Bagikan sebagai `https://…/andi-sari.html?to=Nama%20Tamu`.

Atau jadikan satu file yang bisa dikirim lewat WhatsApp:

```bash
./bin/build-single.py data/andi-sari.json --inline-media -o dist/andi-sari.html
```

`--inline-media` menanam musik dan foto, jadi benar-benar satu file, tapi
ukurannya melonjak ke ~1 MB. Untuk disebar ke tamu pakai versi hosted.

## Yang sudah jalan

- Sampul pengunci, terbuka lewat tombol
- Nama tamu personal dari `?to=`, dirender lewat `textContent` bukan `innerHTML`
- Hitung mundur, sadar zona waktu acara (bukan zona waktu tamu)
- Strip hari dengan tanggal acara ditandai, tombol simpan ke kalender
- Salin nomor rekening satu ketuk
- RSVP + dinding tamu, tiga backend: localStorage / Google Sheet / Supabase
- Musik latar, diambil hanya saat ditekan
- Tanpa foto pun tetap jadi: sampulnya berubah jadi monogram terukir

## Dokumentasi

| | |
|---|---|
| [docs/THEMING.md](docs/THEMING.md) | bikin tema baru |
| [docs/SECTIONS.md](docs/SECTIONS.md) | katalog section, skema data, backend RSVP |
| [docs/DEPLOY.md](docs/DEPLOY.md) | ke mana di-deploy, dan kenapa data klien tidak boleh publik |

## Aset dan lisensi

Kode engine bebas dipakai ulang. Musik bawaan digenerate dari
`bin/make-music.py`, jadi jelas statusnya waktu template dijual. Foto contoh
CC0/public domain dari Openverse, tercatat di `assets/photos/CREDITS.md`.

**Hati-hati merek dagang:** beberapa tema lama memakai nama properti berhak
cipta (Spiderman, Barbie, dll). Palet/motif boleh mirip, **nama dan tagline
tidak** — wajib di-rename sebelum jualan serius (lihat catatan proyek).

Untuk lagu pilihan pasangan, ganti `music.src` dengan file yang mereka punya
haknya. Jangan bundel lagu komersial ke dalam template yang dijual berulang:
tiap pengiriman ke klien itu distribusi ulang.

**Data klien tidak pernah masuk repo ini.** `data/<klien>.json` berisi nomor
rekening dan alamat; `.gitignore` menolaknya dan workflow Pages gagal build
kalau ada yang nyelip. Lihat [docs/DEPLOY.md](docs/DEPLOY.md).
