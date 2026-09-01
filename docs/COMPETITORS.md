# Kompetitor Undangan Digital Indonesia — ikat vs Pasar

> Riset: 1 Sep 2026. Sumber: halaman harga & fitur publik tiap platform (di-extract langsung), ditambah sniff header/teknologi. Harga promo sewaktu-waktu berubah — angka di sini snapshot saat riset.

## Ringkasan pasar

Pasar undangan digital Indonesia sangat terkomoditisasi. Shopee/Tokopedia sudah Rp 15–50rb untuk template statis. Platform website-undangan (SaaS) mematok **Rp 49k–299k** untuk B2C, dengan model langganan/masa aktif 7 hari–1 tahun. Hampir semua kompetitor:

- pakai **dashboard + database + login** (butuh backend, maintenance, dan biaya server per klien),
- **membatasi tamu/foto/revisi** per paket,
- **masa aktif terbatas** (habis = perpanjang bayar lagi),
- hosting di Cloudflare/WordPress/Laravel, tapi payload berat (SPA, jQuery, Bootstrap, builder).

**ikat** beda positioning: **engine statis vanilla** (tanpa build, tanpa backend wajib), 1 JSON per klien, 1 entry `themes.json` per tema, payload 22 KB, once-pay, dan wedge B2B2C ke vendor (WO/percetakan/MUA).

---

## Kompetitor yang dipetakan

| # | Platform | URL | Sejak | Klaim skala | Model utama |
|---|----------|-----|-------|-------------|-------------|
| 1 | **Datengdong** | datengdong.com | 2020 | — | Freemium tiered (Starter–Diamond) |
| 2 | **Satu Momen** | satumomen.com | — | — | Tiered + reseller credit |
| 3 | **Katsudoto** | katsudoto.id | 2018 | 11.755+ pasangan | Lite flat + Premium modular |
| 4 | **Wedew** | wedew.id | — | 40K+ nikahan, 500K+ tamu, Rp 5B+ angpao | Free forever + kalkulator add-on |
| 5 | **MomenKita** | momenkita.id | — | 12K+ pasangan | Non-Foto vs Dengan Foto + reseller |
| 6 | **Weddingku.id** | weddingku.id | — | — | Bronze/Silver/Gold per desain |
| 7 | **Momenika** | momenika.id | — | — | Website + Gambar/Video terpisah |
| 8 | **Invidoto** | invidoto.com | — | Solo & nasional, B2B+B2C | Self-create gratis + partnership 20rb |
| 9 | **Invitation Moment** | invitationmoment.com | — | — | Katalog wedding & non-wedding |
| 10 | **SebarUndangan** | sebarundangan.id | — | — | Gratis (freemium) |
| 11 | **Seremoni.id** | seremoni.id | — | — | Website undangan (WordPress) |
| 12 | **OurStory / OurMoment** | ourstoryinvitation.com / ourmoment.id | — | — | Template marketplace |

> Masih ada long-tail: nikahonline, undangku, walimatul.id, mokita.id, vitopia.co, sangmempelai.id, linkundangan.com, mengoendang.com, seundang.com, katakino.com, dll — pola harga/fitur mirip 12 di atas.

---

## Harga & paket (B2C)

| Platform | Paket termurah | Paket tengah (paling laku) | Paket atas | Masa aktif | Catatan |
|----------|---------------|---------------------------|------------|------------|---------|
| **ikat** | **Rp 99k** Basic — 1 tema, 1 tahun | **Rp 199k** Plus — semua tema (101), 2 tahun | **Rp 499k** Custom — tema dari nol, selamanya + file | 1 th / 2 th / selamanya | **Sekali bayar**, tanpa langganan. Reseller 50 undangan Rp 990k (modal **Rp 19.800**/undangan) |
| Datengdong | Gratis (Starter, 3 tamu, 3 foto, 3 hr) / **Rp 49k** | **Rp 99k** Silver (100 tamu, 10 foto, 1 bln) / **Rp 199k** Gold (1000 tamu) | **Rp 299k** Platinum/Diamond (2000–unlimited, 1 th) | 3 hr – 1 th | Edit profil cuma **7 jam** setelah aktif. Tamu dibatasi ketat di tier bawah |
| Satu Momen | **Rp 79k** Basic (7 hr, self-edit, tanpa admin) | **Rp 129k** Premium (30 hr, 2 revisi) / **Rp 199k** Prioritas (90 hr, unlimited revisi wajar) | **Rp 235,5k** Signature (180 hr) / **Rp 599k** Custom (1 th, .my.id) / **Rp 850k** Corporate (.com) | 7 hr – 1 th | Semua paket fitur sama, beda **durasi + revisi + admin**. Custom wajib konsultasi |
| Katsudoto Lite | **Rp 100k** flat | **Rp 250k** base Premium (15 galeri, 1 th) | Modular: tambah fitur à la carte (total bisa >500k) | 1 th (Lite & Premium), ada paket **selamanya** (Lamar/Mantu) | Lite = template terbatas, fitur dasar. Premium = semua desain + custom lagu/story/streaming |
| Wedew | **Gratis selamanya** (Starter, fitur lengkap) | **Rp 50k** Lite / **Rp 125k** Premium (most popular) | **Rp 250k / 500k / 1.000k** (kalkulator) | Selamanya (Starter) | Add-on: +50 tamu Rp 25k, +50 WA Rp 40k, +50 Email Rp 10k, App penerima tamu Rp 100k |
| MomenKita | **Rp 79k** Non-Foto (6 bln) | **Rp 129k** Dengan Foto (1 th) | Reseller: **Rp 299k/5** (59,9k each) / **Rp 499k/10** (49,9k each) | 6 bln – 1 th | Add-on: QR Check-in 75k, Google Sheet 50k, Custom Domain 100k, Custom Desain 350k |
| Weddingku.id | **Rp 100k** (diskon dari 300k) Basic/Minimal/Aquilla/Vella | **Rp 200k** (dari 400k) Klasik/Holy | **Rp 300k** (dari 500k) Rose/Tropis | — (tidak eksplisit, ~1 th) | Per desain beda harga. Produksi 1 jam (Sen–Jum 09–16) |
| Momenika | **Rp 69k** Tanpa Foto / **Rp 79k** Website (dari 125k) | — | Gambar JPG **20k**, Video Portrait **50k**, Landscape **60k** | **4 bulan** | Revisi 3×. Add-on: musik 10k, amplop 20k, RSVP sheet 25k, ekspres 50k |
| Invidoto | **Gratis** self-create | **Rp 20k**/undangan via partnership (reseller jual sesuka) | — | — | B2B focus, Solo. “Produsen undangan B2B dan B2C” |

**Insight harga:** ikat di tengah pasar B2C (99k–199k) tapi **modal reseller paling rendah** (19,8k vs 20k Invidoto, 49,9k MomenKita, 10–20 kredit Satu Momen yang setara ~25–50k). Satu Momen & MomenKita mengenakan **masa aktif pendek** — klien yang nikahnya 6 bulan lagi harus perpanjang atau beli paket mahal.

---

## Perbandingan fitur

| Dimensi | ikat | Datengdong | Satu Momen | Katsudoto | Wedew | MomenKita | Weddingku | Momenika |
|---------|------|------------|------------|-----------|-------|-----------|-----------|----------|
| **Jumlah tema** | **101** (spec-driven, 11 awal + 90 ekspansi: adat, pop-culture, pastel 2026) | 4 (Starter) / All (Silver+) — puluhan | Puluhan (semua paket dapat semua) | Puluhan (Lite terbatas, Premium semua) | Puluhan | Semua tema per paket (non-foto vs foto dipisah) | Per desain (Basic/Minimal/dll) | Belasan |
| **Kustomisasi warna/font/shape** | Token penuh (12 warna, 9 shape, 3 font + stack, tracking, pattern) — tanpa sentuh JS | Warna & font terbatas (template lock) | Warna & font terbatas | **Bebas ganti warna & font** (Express Yourself) | Terbatas | Terbatas | Terbatas | Custom warna +20k |
| **Tanpa foto prewed** | **Monogram terukir** (dirancang, bukan kotak kosong) | Placeholder foto kosong | Placeholder | Placeholder | Placeholder | Paket Non-Foto khusus | Placeholder | Paket Tanpa Foto |
| **Guest personalization (?to=)** | ✅ `?to=Nama Tamu` → sampul + RSVP auto-isi, via `textContent` (XSS-safe) | ✅ Sapa Tamu | ✅ | ✅ Sapa Tamu (unlimited di paket atas) | ✅ Manajemen Tamu | ✅ Custom Tamu | ✅ | ✅ Unlimited nama tamu |
| **RSVP & Guestbook** | ✅ adapter `demo` (localStorage) + `supabase` (RLS, insert-only) | ✅ RSVP + Ucapan | ✅ | ✅ RSVP | ✅ RSVP & Komentar | ✅ RSVP | ✅ | ✅ +25k Google Sheet |
| **QR Check-in / Buku Tamu Digital** | ⏳ via Supabase (siap, belum UI scan) | Scanner (Beta) | — | ✅ **Buku Tamu Digital & QR** + Table & Souvenir Management | ✅ App Penerima Tamu (Android+iOS, +100k) | ✅ QR Check-in (+75k) | — | — |
| **Broadcast WA H-1 / Shareblast** | ⏳ (roadmap, via data tamu) | Shareblast (Beta) | WhatsApp support | WhatsApp Manual (unlimited di atas) + E-Invitation | WhatsApp add-on (+40k/50) | Wishlist WA | Manual | Manual |
| **Amplop digital / Gift** | ✅ bank + alamat, salin 1 ketuk | ✅ Kirim Hadiah | ✅ | ✅ Amplop Digital | ✅ Angpao Cashless (Rp 5B+) | ✅ Amplop Digital | ✅ | ✅ +20k |
| **Galeri foto/video** | ✅ gallery (foto + caption), lightbox | 3–unlimited foto, 1–unlimited video | Unlimited (semua paket) | 10–unlimited foto, GIF, crop, video | Gallery | Galeri Foto | Photo Gallery | Tambah video +20k |
| **Musik** | ✅ custom `music.src`, 1 baris ganti lagu, piano generatif 751KB | Upload (Silver+) | Free request lagu | Autoplay template / Custom lagu | Musik Autoplay | Musik Autoplay | — | Request +10k |
| **Countdown & Add to Calendar** | ✅ timezone-aware (`meta.timezone`, `wallClock()`) | ✅ Countdown | ✅ | ✅ Countdown + Add to Calendar | ✅ Countdown | ✅ | ✅ | ✅ Hitung mundur |
| **Peta & Live streaming** | ✅ maps link + streaming link | Link Lokasi + Streaming | — | Maps + Live Streaming + Filter IG | Maps | Live Streaming | — | Google Maps |
| **Love story / Timeline** | ✅ story section | Story | — | Love Story | Love Story | Our Story | — | — |
| **Revisi** | Unlimited (edit JSON sendiri, atau via admin) | — | 2× minor (Premium) / unlimited wajar (Prioritas+) | Unlimited Edit | Unlimited Edit | Free revisi | — | 3× (website), 2+1 (gambar/video) |

---

## Teknologi & performa

| Dimensi | ikat | Pasar (rata-rata) |
|---------|------|-------------------|
| **Stack** | **Vanilla JS + CSS**, tanpa framework, tanpa build step, tanpa bundler, tanpa `npm install` | Nuxt/Vue (Datengdong), WordPress + LiteSpeed (Weddingku, MomenKita), Laravel/PHP (Katsudoto, Wedew), jQuery+Bootstrap (banyak template marketplace) |
| **Payload halaman pertama** | **22 KB terkompresi** (18,6 KB gz engine: 10,9 KB JS + 7,6 KB CSS), diukur dari deployment live. Musik & foto lazy setelah tap | **500 KB – 8 MB** (SPA + font + gambar hero + builder JS). Banyak gagal di sinyal 1 bar parkiran gedung |
| **Hosting** | **Statis murni** — bisa di GitHub Pages, Cloudflare Pages (POP Jakarta), Netlify, bahkan file tunggal via `build-single.py`. Bandwidth unlimited (Cloudflare) | Butuh server dinamis (PHP/Node/WordPress) + database. Vercel Hobby larang komersial, Netlify 100 GB/bulan, shared hosting lemot |
| **Build / deploy** | `python3 -m http.server` langsung jalan. `bin/new-client.sh` → 1 JSON + 1 HTML. `bin/build-single.py --inline-media` → 1 file HTML kirim via WA | Wajib dashboard, login, migrasi DB, update plugin WordPress, renewal SSL manual |
| **Offline / single-file** | ✅ `build-single.py` → 1 HTML dengan musik+foto inline (serah terima pasca-acara, tanpa hosting) | ❌ Tidak ada opsi single-file; undangan mati kalau server mati |
| **Keamanan data klien** | `.gitignore` blok `data/*.json` kecuali `demo.json`; workflow Pages **gagal build** kalau ada JSON klien nyelip; data sensitif (rekening, alamat, HP) tidak masuk repo publik | Data klien di database vendor (risiko bocor, dijual, atau hilang saat vendor tutup). Tidak ada guard `.gitignore` |
| **Timezone correctness** | `Intl.DateTimeFormat` pakai `meta.timezone` (Asia/Jakarta), bukan zona tamu. Tamu di Jeddah tetap lihat jam WIB benar | Banyak pakai zona browser/server → jam resepsi geser (bug “04:00 padahal 11:00 WIB”) |
| **Aksesibilitas** | Kontras ≥ WCAG AA, field ≥16px (anti iOS auto-zoom), `background-attachment: fixed` dihindari (Safari iOS), `textContent` bukan `innerHTML` | Sering gagal kontras, input 15px (auto-zoom), `fixed` background patah di iOS |
| **Viewport bug** | Fix iframe `svh`/`vh` bohong (cap 860px saat `window.parent !== window`, `--u-vh` measured, ambient di `::before`) | Tidak ditangani — tombol “Buka Undangan” sering tidak terjangkau di HP dengan address bar |
| **Skalabilitas vendor** | **1 site, N klien sebagai path** (`/andi-sari?to=Budi`) — 100 klien = 1 deploy, 1 domain | 1 site per klien (100 klien = 100 project/domain/deploy) atau 1 dashboard berat yang harus di-maintain |

---

## Keunggulan ikat — daftar ekstensif

### A. Performa & keandalan (wedge #4)

1. **22 KB halaman pertama** — kebuka sebelum tamu sempat menutup tab. Kompetitor 5–8 MB gagal di sinyal parkiran gedung, tempat tamu justru membukanya.
2. **Tanpa build step** — `python3 -m http.server` langsung jalan. Kompetitor butuh `npm install`, bundler, dan build pipeline yang bisa pecah.
3. **Zero dependency** — tidak ada `node_modules`, tidak ada supply-chain attack, tidak ada `npm audit` merah.
4. **Vanilla JS 10,9 KB gz** — bukan React/Vue/Next. Tidak ada hydration, tidak ada framework churn.
5. **Musik & foto lazy** — baru di-fetch setelah tamu tap “Buka Undangan” / “Putar musik”. Kompetitor load semua di awal.
6. **POP Jakarta (Cloudflare Pages)** — edge terdekat tamu Indonesia. Kompetitor di Virginia/Singapura buang keunggulan “kebuka cepat di sinyal jelek”.
7. **Bandwidth unlimited** — viral di grup keluarga besar tidak bikin tagihan. Netlify/Vercel ada cap.
8. **Single-file fallback** — `build-single.py --inline-media` jadi 1 HTML kirim via WA/email, tetap kebuka tanpa hosting. Tidak ada kompetitor yang punya ini.
9. **Fix viewport bohong** — satu-satunya yang menangani bug `svh`/`vh` di dalam iframe (tombol “Buka Undangan” selalu terjangkau, 320×505 s/d 430×745 + landscape + iframe 2200px).
10. **Safari iOS hardened** — no `background-attachment: fixed`, input ≥16px, kontras AA, `Audio` stub untuk container tanpa audio.

### B. Desain & tema (moat kreatif)

11. **101 tema vs 10–40 kompetitor** — dari pastel 2026 (butter, Cloud Dancer, mocha mousse, lilac haze) sampai adat (Batik Solo, Kebaya Velvet, Bali Lotus, Minang Songket, Toraja Ukir, Dayak Borneo, dll) dan pop-culture (Ghibli, Harry Potter, Minecraft, dll).
12. **Spec-driven theming** — `themes/themes.json` jadi SOT, `bin/make-theme.py` generate `theme.css`. Tema ke-102 = 1 entry JSON, tanpa sentuh `engine.js`. Kompetitor: edit template satu-satu, rawan drift.
13. **Kontrak “tema tidak boleh sentuh JS, data tidak boleh sentuh CSS”** — terbukti: 101 tema tanpa ubah `engine.js` satu baris. Kompetitor campur aduk, tiap tema = fork.
14. **Token lengkap** — 12 warna, 9 shape (radius, frame, avatar, photo, pill, tilt, shadow), 3 font + stack, tracking, pattern (dots/grid/arcs/waves/chevron/petals/stars/grain/ikat). Kompetitor: ganti warna saja kadang berbayar (+20k).
15. **Palet 2026 forecast-based** — bukan selera desainer. Butter yellow, Cloud Dancer (Pantone 2026), mocha mousse, lilac haze — warna yang memang dicari pengantin 2026.
16. **Monogram tanpa foto** — pasangan tanpa prewed (segmen yang hampir tidak ada kompetitor yang layani) tetap dapat sampul “terukir”, bukan kotak rusak.
17. **Tipografi sebagai bintang** — tema `noir-editorial` dan `forest-lace` pakai tipografi, bukan stok foto. Beda dari template pasaran yang semua pakai foto bunga yang sama.

### C. Model bisnis & harga (wedge #1 & #2)

18. **Sekali bayar, bukan langganan** — Basic 99k (1 th), Plus 199k (2 th), Custom 499k (selamanya). Kompetitor: 7 hari–4 bulan, habis = bayar lagi. Klien yang booking 6 bulan sebelum hari-H dirugikan model sewa.
19. **Modal reseller terendah** — Rp 19.800/undangan (paket 50 @ 990k) vs 49,9k (MomenKita), 20k (Invidoto, tapi fitur terbatas), 25–50k (Satu Momen kredit). Margin jual 79,2k/undangan kalau jual 99k.
20. **B2B2C ke vendor, bukan B2C ke pengantin** — 1 WO = 10–30 undangan/bulan seumur hidup; 1 pengantin = sekali. Kompetitor fokus B2C, berebut iklan yang sama.
21. **Self-serve, bukan DM** — `bin/new-client.sh andi-sari butter` → 1 JSON + 1 HTML, tanpa chat bolak-balik “kak revisi warna ya”. Kompetitor: “DM untuk custom” = tidak scalable.
22. **White-label reseller** — vendor pakai brand sendiri, tetapkan harga sendiri, ikat tidak muncul di depan klien. Kompetitor reseller masih pakai subdomain vendor.
23. **1 site, N klien sebagai path** — `undangan.domainmu.com/andi-sari?to=Budi` — 100 klien = 1 deploy. Kompetitor: 1 site per klien = 100 project.
24. **Harga transparan di landing** — galeri + pricing auto-generate dari `themes.json` via `bin/make-site.py`. Tidak ada “hubungi admin untuk harga”.

### D. Data & privasi

25. **Data = 1 JSON per klien** — `data/<slug>.json` berisi semua (couple, date, sections, gift). Klien baru = 1 file, bukan 1 row di DB yang butuh migrasi.
26. **Tidak ada vendor lock-in** — JSON + HTML statis bisa dipindah hosting mana saja, bahkan jadi file tunggal. Kompetitor: data di DB vendor, pindah = hilang.
27. **Guard privasi berlapis** — `.gitignore` blok `data/*.json`, workflow Pages gagal build kalau ada JSON klien nyelip. Kompetitor: nomor rekening & alamat rumah di DB vendor yang bisa bocor.
28. **Repo publik aman** — yang di GitHub Pages cuma `data/demo.json` fiktif. Undangan klien asli di repo privat Cloudflare Pages. Kompetitor tidak punya pemisahan ini.

### E. Fungsional & DX (wedge #3 — guest management)

29. **Urutan section bebas** — `sections: [cover, quote, countdown, couple, event, gallery, story, gift, rsvp]` bisa di-reorder, dihapus, atau dipakai berulang (mis. 2× `event` untuk akad & resepsi). Kompetitor: urutan template kaku.
30. **Tipe section unknown = warning, bukan crash** — data lama tetap render, tidak matikan undangan. Kompetitor: template error = blank page.
31. **Timezone-aware** — `meta.timezone: Asia/Jakarta` + helper `wallClock()` untuk strip hari. Kompetitor sering pakai zona browser → tanggal geser.
32. **RSVP adapter ganda** — `demo` (localStorage, untuk preview) dan `supabase` (1 tabel `rsvp` untuk semua klien, RLS insert-only, anon key aman). Kompetitor: cuma 1 backend, tidak ada opsi offline preview.
33. **Salin rekening 1 ketuk** — `navigator.clipboard` + fallback. Kompetitor ada yang masih suruh seleksi manual.
34. **Guest link personal** — `?to=Nama Tamu` di sampul + auto-isi RSVP, XSS-safe via `textContent`. Kompetitor ada yang pakai `innerHTML` (rentan injeksi).
35. **Aksesibilitas bawaan** — kontras AA, focus ring, motion `prefers-reduced-motion`, semantic HTML. Kompetitor jarang audit.

### F. Ekosistem & leverage (di luar undangan)

36. **Bagian dari ekosistem `nurhikam`** — ikat bukan produk孤立. Ada `second-brain` (vault pengetahuan), `framedeck` (video → MCP, bisa bikin promo video undangan otomatis via `bin/make-promo-video.py`), `mail-server` (100 mailbox self-host, untuk outreach vendor), `sahamind` (AI analyst, pola pikir data-driven yang sama). Kompetitor: cuma jualan template.
37. **Aset lisensi bersih** — musik piano generatif (`bin/make-music.py`, sintesis aditif stdlib + ffmpeg, 64s/751KB) dan foto CC0 via `bin/fetch-sample-photos.py` (bukan “dari Google”, bukan lagu Barasuara yang butuh lisensi). Tiap kirim ke klien = distribusi ulang, jadi lisensi harus benar. Kompetitor sering pakai aset tanpa lisensi jelas.
38. **Dokumentasi sebagai produk** — `docs/THEMING.md`, `docs/SECTIONS.md`, `docs/DEPLOY.md`, `docs/COMPETITORS.md` (ini), `architecture.svg` — vendor/reseller bisa belajar tanpa tanya admin. Kompetitor: tutorial cuma video WA.
39. **Skrip otomasi** — `bin/make-theme.py`, `bin/make-site.py`, `bin/new-client.sh`, `bin/build-single.py`, `bin/make-music.py`, `bin/fetch-sample-photos.py` — semua one-liner, tanpa GUI. Kompetitor: klik-klik dashboard yang tidak bisa di-script.
40. **Landing yang menjual** — `site/index.html` dengan galeri 101 tema + pricing + kalkulasi reseller, auto-generate, bisa jadi etalase langsung. Kompetitor: landing terpisah dari dashboard, tidak sinkron.

---

## Kejujuran — di mana ikat masih kalah

| Gap | Dampak | Rencana |
|-----|--------|---------|
| **Belum ada QR check-in UI** (baru data + Supabase) | Vendor butuh scan di hari-H; kompetitor (Katsudoto, Wedew, MomenKita) sudah ada app | Prioritas #1 wedge #3: tambah section `checkin` + halaman scan |
| **Belum ada broadcast WA H-1** | Kompetitor (Datengdong Shareblast, Katsudoto WA Manual) bisa blast pengingat | Integrasi WA gateway (pakai `mail-server` infra) |
| **Belum ada dashboard GUI** | Non-teknis harus edit JSON (walau ada `new-client.sh`) | Bungkus `data/*.json` dengan form web minimal (tetap statis, tanpa DB) |
| **Belum ada app penerima tamu** | Wedew & Katsudoto punya app Android+iOS | PWA scan QR cukup untuk MVP, tanpa app store |
| **Verifikasi Safari iPhone masih headless WebKit** | User sudah 2× temukan bug yang lolos headless | Pinjam/test di iPhone fisik sebelum launch |
| **Pola Cloudflare “1 site, N path” belum di-run** | Masih teori di `docs/DEPLOY.md` | Uji dengan 2 klien dummy di Cloudflare Pages |
| **SEO undangan** | Kompetitor WordPress punya SEO plugin | Undangan memang tidak butuh SEO (link privat), tapi landing butuh |

---

## Metodologi riset

- **Web search** 20+ query: `katundang`, `datengdong`, `weddingku`, `invitto`, `moment`, `sebarundangan`, `wedew`, `katsudoto`, `momenkita`, `invidoto`, `momenika`, `invitationmoment`, plus varian “harga paket undangan digital”.
- **Extract** 10+ halaman harga/fitur (Datengdong /price, Satu Momen /harga, Katsudoto /undangan-website & /undangan-lite & /v2/package, Wedew /harga, MomenKita / & /reseller, Weddingku.id /, Momenika /pricelist).
- **Header sniff** 6 domain (Server, X-Powered-By, body hints) untuk tech stack.
- **Cross-check** dengan `themes/themes.json` (101 tema), `site/index.html` (pricing), `engine/*` (ukuran gz), dan `second-brain/Projects/ikat — Engine template undangan digital.md` (4 wedges).

> Jika ada harga/fitur yang berubah setelah 1 Sep 2026, update tabel di atas dan sebutkan tanggal snapshot baru.

---

## Sumber

- datengdong.com/price — Harga Undangan Online (Starter–Diamond)
- satumomen.com/harga — Harga Undangan Online (Basic–Enterprise + Reseller)
- katsudoto.id/undangan-website, /undangan-lite, /v2/package — Paket & fitur Katsudoto
- wedew.id/harga — Harga Wedew (Starter FREE – 1.000k + kalkulator)
- momenkita.id & /reseller — Paket Non-Foto/Dengan Foto + Reseller
- weddingku.id — Pilihan Desain & harga Bronze/Silver/Gold
- momenika.id/pricelist — Website 69–79k + Gambar/Video
- invidoto.com — Partnership 20rb/undangan
- invitationmoment.com — Katalog & FAQ
- sebarundangan.id, seremoni.id, ourstoryinvitation.com — freemium & marketplace
- Header sniff (cloudflare, wordpress, litespeed) — 1 Sep 2026
- ikat: `themes/themes.json`, `site/index.html`, `engine/engine.js` (37.657 B, 10.912 B gz), `engine/engine.css` (26.856 B, 7.655 B gz), `bin/make-site.py`, `docs/*`
