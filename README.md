# Ikat

**Live: https://nurhikam.github.io/ikat/**

Undangan pernikahan digital. Sebelas tema, satu JSON per klien, tanpa build step.

*Ikat* artinya mengikat, dan juga teknik tenun bermotif. Dua-duanya pas untuk
sesuatu yang menjual motif.

Halaman pertama undangan **22 KB terkompresi**, diukur dari deployment di atas
dan bukan dari localhost. Musik (751 KB) dan foto (190 KB) baru diambil setelah
tamu menekan tombol.

## Coba

| | |
|---|---|
| Landing page | https://nurhikam.github.io/ikat/ |
| Undangan demo | https://nurhikam.github.io/ikat/demo.html?to=Nama%20Tamu |
| Ganti tema | https://nurhikam.github.io/ikat/preview.html?theme=butter |

## Jalankan lokal

```bash
python3 -m http.server 8000
```

Tanpa dependency, tanpa `npm install`, tanpa bundler. Yang di-deploy persis yang
ada di repo.

## Struktur

```
themes/themes.json      SATU sumber kebenaran untuk semua tema
bin/make-theme.py       themes.json  -> themes/<slug>/theme.css
bin/make-site.py        themes.json  -> site/index.html  (galeri + harga)
bin/new-client.sh       bikin undangan buat satu klien
bin/build-single.py     bundel jadi satu file HTML
bin/make-music.py       render piano bawaan tema dari kode
bin/fetch-sample-photos.py   ambil foto contoh CC0

engine/engine.js        renderer + perilaku, universal, tak pernah disentuh per klien
engine/engine.css       tata letak, state, motion, aksesibilitas
themes/<slug>/          theme.css (digenerate) + decoration.css (ditulis tangan)
data/<klien>.json       isi undangan + urutan section
site/                   landing page: index.html (digenerate), site.css, thumbs/
```

Kontrak yang bikin ini bisa dijual berulang:

> **Tema tidak boleh menyentuh JavaScript. Data tidak boleh menyentuh CSS.**

Kesebelas tema dibangun tanpa mengubah `engine.js` satu baris pun. Kalau tema
berikutnya ternyata butuh, itu tandanya ada token yang kurang: tambahkan
tokennya, jangan fork enginenya.

## Sebelas tema

| Tema | Karakter |
|---|---|
| `butter` | Butter yellow dan krim, warna yang paling disebut untuk 2026 |
| `cloud-dancer` | Dusty blue di atas Cloud Dancer, Pantone 2026 |
| `mocha-mousse` | Mocha dan karamel, Pantone 2025 yang pindah ke palet nikahan |
| `lilac-haze` | Lilac lembut, paling ringan |
| `rosewater` | Blush pink dan gading |
| `dusty-sage` | Sage kering dan tulang, netral |
| `forest-lace` | Hijau botani gelap, renda, emas antik |
| `noir-editorial` | Hitam pekat, tipografi jadi bintangnya |
| `terracotta-sun` | Tanah liat dan lengkung gapura |
| `riso-zine` | Cetak risograph dua warna |
| `pearl-chrome` | Mutiara, krom, kilau iridescent |

Palet disandarkan ke forecast warna pernikahan 2026, bukan selera. Tema baru:
[docs/THEMING.md](docs/THEMING.md).

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

Untuk lagu pilihan pasangan, ganti `music.src` dengan file yang mereka punya
haknya. Jangan bundel lagu komersial ke dalam template yang dijual berulang:
tiap pengiriman ke klien itu distribusi ulang.

**Data klien tidak pernah masuk repo ini.** `data/<klien>.json` berisi nomor
rekening dan alamat; `.gitignore` menolaknya dan workflow Pages gagal build
kalau ada yang nyelip. Lihat [docs/DEPLOY.md](docs/DEPLOY.md).
