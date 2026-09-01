# Ikat — Marketing Plan

> Engine undangan digital: 11 tema, 22 KB halaman pertama, 1 JSON per klien.
> Pasar: ~1,5–2 juta pernikahan/tahun di Indonesia. Tantangan: komoditisasi ekstrem (Shopee/Tokopedia Rp 15–50rb).

---

## 1. Target Audience Analysis

### 1.1 Segmentasi Utama

| Segmen | Ukuran Pasar | Frekuensi Beli | Willingness to Pay | CAC | Prioritas |
|---|---|---|---|---|---|
| **B2B2C — Vendor (WO, MUA, Fotografer, Percetakan)** | ~30.000 WO/MUA aktif di JAWA + 15.000 luar Jawa | 10–30 undangan/bulan, berulang 12 bulan/tahun | Rp 990rb–2,9jt/paket reseller | Rendah (1 akuisisi = 120–360 transaksi/tahun) | **#1 — Primary** |
| **B2C — Pasangan langsung (self-serve)** | ~1,5jt pasangan/tahun, 40% pakai undangan digital (~600rb) | Sekali seumur hidup | Rp 99–199rb | Tinggi (one-shot, churn 100%) | **#2 — Secondary** |
| **B2B — Korporat/Event** | Kecil (launching, gala, corporate gathering) | Sporadis | Rp 499rb–2jt | Sangat tinggi | #3 — Opportunistic |

### 1.2 B2B2C vs B2C vs B2B — Keputusan

**Menang di B2B2C, monetisasi B2C sebagai etalase.**

| Dimensi | B2B2C (Vendor) | B2C (Pasangan) | B2B (Korporat) |
|---|---|---|---|
| **LTV** | Rp 2,4jt–7,2jt/tahun (10 undangan/bulan × Rp 19.800 modal × 12 bulan, dijual Rp 99rb) | Rp 99–199rb sekali | Rp 500rb–2jt sporadis |
| **CAC payback** | 1–2 transaksi | Harus profit di transaksi pertama | Tidak prediktabel |
| **Skalabilitas** | 1 WO onboard = 120+ undangan/tahun tanpa marketing tambahan | Tiap undangan butuh iklan/konten baru | Manual sales |
| **Kompetisi** | Rendah — kebanyakan kompetitor kejar B2C di marketplace | Sangat tinggi — 2.000+ seller di Shopee | Niche |
| **Retention** | Tinggi — switching cost (template, data tamu, brand) | Nol | Rendah |
| **Distribusi** | Vendor sudah punya trust + audiens | Harus bangun trust dari nol | Cold outreach |

**Kesimpulan:**
- **70% effort → B2B2C (WO/MUA/percetakan).** Satu WO di Bandung yang handle 15 wedding/bulan = Rp 1,18jt margin/bulan untuk dia, Rp 297rb revenue/bulan untuk Ikat (15 × Rp 19.800) — tanpa Ikat cari 15 pasangan satu per satu.
- **25% effort → B2C self-serve.** Landing + SEO + TikTok sebagai *lead magnet* dan *proof* untuk vendor ("lihat, pasangan memang cari ini").
- **5% effort → B2B korporat.** Layani kalau datang, jangan kejar.

### 1.3 Persona Detail

#### Persona A — "Rina WO" (Primary, B2B2C)
- **Profil:** 26–35 tahun, owner WO kecil-menengah di kota tier 1–2 (Jakarta, Bandung, Surabaya, Jogja, Medan). Handle 8–20 wedding/bulan. Tim 2–5 orang.
- **Pain:** Klien minta undangan digital, Rina lempar ke freelancer Rp 50rb yang hasilnya 5 MB, loading lama, revisi via DM berhari-hari. Tidak ada dashboard tamu.
- **Motivasi:** Tambah revenue tanpa tambah kerja. Mau jual undangan pakai brand sendiri, harga sendiri, margin 70–80%.
- **Channel:** Instagram, TikTok, komunitas WO (HIPAPI, grup WA WO se-kota), pameran wedding expo.
- **Objection:** "Ribet nggak setup-nya?" → Jawab: 1 JSON, 5 menit jadi.

#### Persona B — "Dinda & Adit" (Secondary, B2C)
- **Profil:** 23–30 tahun, menikah 2–4 bulan lagi. Budget undangan Rp 100–300rb. Aktif di TikTok/IG, cari "undangan digital aesthetic" atau "undangan tanpa foto prewed".
- **Pain:** Template marketplace jelek/lambat, DM seller slow response, tidak ada opsi tanpa foto prewed (mereka belum sempat foto).
- **Motivasi:** Cepat, cantik, murah, bisa ganti tema tanpa ulang. Link personal per tamu biar kelihatan niat.
- **Channel:** TikTok search, Instagram Reels, Google "undangan digital murah", rekomendasi teman.
- **Hook unik Ikat:** "Nggak punya foto prewed? Tetap jadi — monogram terukir, bukan kotak kosong." Segmen ini hampir tidak ada yang sasar.

#### Persona C — "MUA Sari" (B2B2C long-tail)
- **Profil:** MUA freelance, 50–200 klien/tahun. Tidak jual undangan tapi ditanya klien "kak ada rekomendasi undangan?"
- **Motivasi:** Komisi referral tanpa stok. Cukup share link dengan kode referral.
- **Value:** Affiliate Rp 20–30rb per closing, pasif.

---

## 2. Positioning

### 2.1 Positioning Statement

> **Untuk WO/MUA yang mau jual undangan digital pakai brand sendiri, Ikat adalah engine undangan white-label yang halaman pertamanya 22 KB — kebuka di sinyal satu bar — dengan 11 tema siap jual dan margin 80% per undangan.**

Untuk pasangan langsung:

> **Undangan yang kebuka, bukan yang bikin tamu nunggu. 22 KB, 11 tema, ganti tema tanpa bikin ulang.**

### 2.2 Differentiator (4 Wedge)

| Wedge | Klaim Ikat | Kompetitor Marketplace | Bukti |
|---|---|---|---|
| **1. B2B2C white-label** | Brand vendor 100%, Ikat tidak muncul di depan klien | Jual pakai brand marketplace/seller | Demo: subdomain vendor, tanpa watermark |
| **2. Self-serve, bukan DM** | 1 JSON → jadi. Ganti tema = 1 setelan | Tiap order = chat bolak-balik 2–3 hari | `bin/new-client.sh` + preview live |
| **3. Guest management** | Link personal `?to=`, RSVP → Supabase/Sheet, export, QR check-in (roadmap) | Hanya halaman cantik | RSVP + rekap unduh di Plus |
| **4. Performa** | 22 KB halaman pertama, musik lazy-load | 5–8 MB, gagal di sinyal parkiran gedung | Lighthouse + ukur di deployment live |

### 2.3 Tagline & Pesan

- **Utama (B2B2C):** "Jual undangan digital pakai nama kalian. Modal Rp 19.800, jual Rp 99.000."
- **B2C:** "Undangan yang kebuka sebelum tamu sempat nutup."
- **Niche (tanpa prewed):** "Nggak sempat prewed? Undangannya tetap jadi."

### 2.4 Kompetitor Map

| Kompetitor | Harga | Kelemahan yang kita serang |
|---|---|---|
| Shopee/Tokopedia seller (Rp 15–50rb) | Paling murah | Lambat (5–8 MB), DM manual, tidak white-label, tidak ada guest management |
| Katamu, Invitanku (Rp 99–300rb) | Menengah | Template terbatas, tidak white-label untuk WO kecil |
| Custom agency (Rp 500rb–2jt) | Mahal | Overkill untuk WO yang butuh volume |

Ikat tidak perang harga di Rp 15rb. Ikat perang di **margin reseller + performa + self-serve**.

---

## 3. Pricing Strategy

### 3.1 Pricing Saat Ini (site/index.html)

| Paket | Harga | Isi | Durasi | Target |
|---|---|---|---|---|
| **Basic** | Rp 99.000 | 1 tema, link personal, RSVP, countdown | 1 tahun | B2C sensitif harga |
| **Plus** | Rp 199.000 | 11 tema gonta-ganti, warna custom, galeri, musik custom, amplop digital, rekap unduh | 2 tahun | B2C mainstream — **hero product** |
| **Custom** | Rp 499.000 | Tema dari nol, domain sendiri, ilustrasi custom, 2× revisi | Selamanya + file | B2C premium / B2B |
| **Reseller 50** | Rp 990.000 (Rp 19.800/invite) | 50 slot undangan, white-label | — | WO/MUA — **hero B2B2C** |

### 3.2 Evaluasi & Rekomendasi

**Yang sudah benar:**
- Sekali bayar (bukan langganan) — sesuai ekspektasi pasar Indonesia untuk produk nikahan.
- Plus sebagai hero (paling laku) — anchoring Basic vs Custom bikin Plus terlihat value.
- Reseller math transparan (modal vs jual) — WO langsung hitung margin.

**Yang perlu ditambah (30 hari ke depan):**

| Paket Baru | Harga | Rasional |
|---|---|---|
| **Reseller 20** | Rp 499.000 (Rp 24.950/invite) | Entry point WO kecil yang ragu beli 50. Turunkan barrier. |
| **Reseller 100** | Rp 1.690.000 (Rp 16.900/invite) | Upsell WO besar. Margin WO naik, lock-in Ikat naik. |
| **Affiliate/Referral** | Gratis daftar, komisi Rp 25.000/closing | Untuk MUA/fotografer yang tidak mau stok. Link referral `?ref=kode`. |
| **Add-on: QR Check-in** | Rp 49.000/event | Guest management wedge — scan tamu di resepsi, rekap hadir. Roadmap Q2. |
| **Add-on: Broadcast WA H-1** | Rp 29.000/100 tamu | Kirim pengingat via WA otomatis. High value, low cost. Roadmap Q2. |

**Yang jangan dilakukan:**
- Jangan turunkan Basic di bawah Rp 79rb — perang harga Rp 15rb tidak bisa dimenangkan dan merusak persepsi reseller (WO tidak mau jual barang yang kelihatan murahan).
- Jangan langganan bulanan — pasangan Indonesia tidak mau "sewa" undangan nikahan.

### 3.3 Psikologi Harga Indonesia

- Tampilkan harga **"sekali bayar"** besar-besar — kata "langganan" bikin bounce 40%+ di segmen ini.
- Tampilkan **math reseller** di landing (sudah ada) — WO Indonesia hitung margin dulu, estetika belakangan.
- **Gratis ganti tanggal** — objection umum "kalau batal/ganti tanggal gimana?" sudah dijawab di FAQ, pertahankan.
- **Bayar via QRIS / transfer manual** — jangan paksa kartu kredit. 70%+ transaksi nikahan Indonesia via transfer bank/e-wallet.

---

## 4. Acquisition Channels

### 4.1 Organic (60% effort, 0 rupiah ad spend)

#### A. TikTok — Channel #1 (40% organic effort)

Kenapa TikTok dulu: sumber ide Ikat sendiri dari TikTok @editmateproject. Algoritma TikTok kasih reach gratis untuk niche "undangan digital" yang search volume-nya naik 200%+ menjelang musim nikah (Syawal–Muharram, Juni–Agustus).

| Taktik | Detail | Target |
|---|---|---|
| **Akun @ikat.undangan** | 1 video/hari, 15–30 detik. Format: screen-record buka undangan + text overlay hook | 1.000 followers bulan 1, 5.000 bulan 3 |
| **Hook yang terbukti** | "Undangan 22 KB vs 5 MB — tes di sinyal 1 bar" (split screen), "Nggak punya foto prewed? Coba ini" (before/after monogram), "Ganti 11 tema dalam 10 detik" | 3 hook, rotasi |
| **Hashtag** | #UndanganDigital #UndanganPernikahan #UndanganOnline #WeddingTikTok #TanpaPrewed | 5 hashtag/video |
| **CTA** | "Link di bio — coba 11 tema gratis" (ke preview.html) | Klik bio → preview |
| **Programmatic video (Remotion)** | Generate varian video otomatis dari React — lihat §5.3. 11 tema × 3 hook × 2 format (9:16, 1:1) = 66 varian tanpa edit manual. Render via `npx remotion render` atau `@remotion/renderer` self-host. | Skala konten tanpa editor |

#### B. Instagram Reels + Carousel (20% organic effort)

- Reels = repost TikTok (rasio sama, watermark dihapus).
- Carousel: "5 kesalahan undangan digital yang bikin tamu nggak datang" — edukasi + soft sell.
- Highlight IG: Tema (11 cover), Harga, Testimoni, Cara Pesan, Reseller.

#### C. SEO — Google Search (20% organic effort)

| Keyword (ID) | Volume est. | Intent | Landing |
|---|---|---|---|
| undangan digital murah | 2.400/bulan | Transaksional | site/index.html#harga |
| undangan pernikahan online | 1.900/bulan | Transaksional | site/index.html |
| undangan digital tanpa foto | 300/bulan | Niche, low comp | Blog post + demo monogram |
| template undangan digital | 800/bulan | B2B2C | Halaman reseller |
| undangan digital 2026 | 500/bulan | Trend | Artikel palet 2026 |

Taktik SEO:
- Landing sudah ada (`site/index.html`) — tambahkan `sitemap.xml`, `robots.txt`, schema.org `Product` untuk 3 paket.
- Blog 1 artikel/minggu (di `site/blog/` atau Notion → static): "Warna undangan 2026", "Cara sebar undangan WA tanpa diblokir", "Checklist sebar undangan H-7".
- Backlink: daftar di 10 direktori WO Indonesia (weddingku.com, bridestory.com vendor listing gratis).

#### D. Pinterest (10% organic effort)

- 11 pin per tema (foto sampul + link preview). Pinterest adalah search engine visual — umur pin 6–12 bulan vs 24 jam di IG.
- Board: "Undangan Digital Aesthetic 2026", "Undangan Tanpa Prewed".

#### E. WhatsApp & Komunitas (10% organic effort)

- Grup WA WO se-kota: join 5 grup, jangan spam — jawab pertanyaan "ada rekomendasi undangan?" dengan value dulu.
- Katalog WA Business: 3 produk (Basic/Plus/Custom) + 1 produk Reseller.

### 4.2 Paid (20% effort, budget bertahap)

| Channel | Budget Awal | Targeting | Kreatif | KPI |
|---|---|---|---|---|
| **TikTok Ads (Spark Ads)** | Rp 50.000/hari (Rp 1,5jt/bulan) | 22–35 th, interest: wedding, engaged, baru tunangan, radius 50km dari kota besar | Video UGC "22 KB" + CTA "Coba Gratis" | CPC < Rp 800, CVR landing→WA > 3% |
| **Instagram Ads (Reels placement)** | Rp 30.000/hari (Rp 900rb/bulan) | Lookalike dari follower + interest WO/MUA | Carousel 11 tema | CPC < Rp 1.200 |
| **Google Search Ads** | Rp 20.000/hari (Rp 600rb/bulan) | Exact: "undangan digital", "undangan online" | Text ad → landing #harga | CPC < Rp 2.000, CVR > 5% |

**Aturan paid:**
- Mulai paid HANYA setelah organic jalan 30 hari dan landing conversion > 2% — jangan bakar uang untuk landing yang belum terbukti.
- Kill rule: kalau CPC > 2× target selama 7 hari, matikan dan revisi kreatif.
- Scale rule: kalau ROAS > 3× selama 14 hari, naikkan budget 30%/minggu (jangan 2× langsung — reset learning phase).

**Total paid bulan 1–3: Rp 3jt/bulan.** Target: 30–50 closing B2C (Rp 99–199rb) + 3–5 reseller (Rp 499rb–990rb) = revenue Rp 5–12jt → ROAS 1,6–4×.

### 4.3 Partnerships (20% effort, highest leverage)

Lihat §7 untuk detail WO/MUA. Ringkas:

| Mitra | Model | Komisi/Margin | Target |
|---|---|---|---|
| WO kecil-menengah | Reseller white-label (20/50/100 slot) | Margin 75–80% untuk WO | 10 WO bulan 1, 30 WO bulan 3 |
| MUA / Fotografer | Affiliate referral link | Rp 25.000/closing | 20 affiliate bulan 2 |
| Percetakan undangan fisik | Bundling: cetak + digital | Rp 15.000/closing atau paket | 5 percetakan bulan 2 |
| Wedding expo | Booth sharing dengan WO mitra | Bagi hasil | 1 expo/kuartal |

---

## 5. Content Strategy

### 5.1 Content Pillars (4 pilar, rotasi mingguan)

| Pilar | Proporsi | Contoh Topik | Format |
|---|---|---|---|
| **Performa & Teknologi** | 30% | "Tes buka undangan di sinyal 1 bar", "Kenapa undangan 5 MB gagal di parkiran gedung" | Video split-screen, carousel edukasi |
| **Tema & Estetika** | 30% | "11 tema Ikat — ganti dalam 10 detik", "Warna 2026: Butter Yellow vs Cloud Dancer" | Video showcase, Pinterest pin |
| **Tanpa Prewed / Inklusif** | 20% | "Nggak sempat prewed? Pakai foto kecil atau monogram", "Undangan tetap cantik tanpa foto" | Before/after, testimoni |
| **Bisnis Reseller** | 20% | "Modal Rp 19.800 jual Rp 99.000 — hitungannya", "WO ini jual 20 undangan/bulan pakai Ikat" | Carousel math, video testimoni WO |

### 5.2 Kalender Konten (mingguan, 7 post)

| Hari | Platform | Konten |
|---|---|---|
| Senin | TikTok + Reels | Video performa (22 KB test) |
| Selasa | IG Carousel | Edukasi (kesalahan undangan digital) |
| Rabu | TikTok + Reels | Showcase 1 tema (rotasi 11 tema = 11 minggu) |
| Kamis | Pinterest | 2 pin tema baru |
| Jumat | TikTok + Reels | Hook tanpa-prewed / monogram |
| Sabtu | IG Story + WA Status | Behind the scenes / testimoni / countdown promo |
| Minggu | Blog/SEO | 1 artikel (500–800 kata) |

### 5.3 Programmatic Video dengan React (Remotion)

> Sumber: `second-brain/Resources/Learning-DevOps/Remotion - Programmatic Video with React.md` — engine video berbasis React (frame = fungsi, `useCurrentFrame()` + `interpolate()`/`spring()`), render via headless Chrome + FFmpeg.

**Peluang untuk Ikat:** Ikat sudah punya 11 tema sebagai data JSON (`themes/themes.json`). Remotion bisa generate video marketing massal tanpa editor:

| Use case | Cara | Output |
|---|---|---|
| **Showcase 11 tema** | 1 komponen Remotion baca `themes.json` → render tiap tema sebagai card animasi (fade + spring) | 11 video 15 detik (1 per tema) + 1 kompilasi 30 detik |
| **Varian hook** | `inputProps` = `{ theme, hook, cta }` → parameterized rendering | 11 tema × 3 hook = 33 varian otomatis |
| **WA Status / Story** | Render 1080×1920 (9:16) + 1080×1080 (1:1) dari komponen sama, ganti `width`/`height` di `<Composition>` | 2 format per video tanpa re-edit |
| **Musim nikah countdown** | `calculateMetadata()` hitung durasi dinamis + tanggal nikah dari props | Video "H-30 menuju hari H" personal per klien (upsell) |

**Stack:**
```bash
npx create-video@latest --yes --blank ikat-promo
# Komponen baca themes.json, pakai interpolate() untuk fade, spring() untuk card entrance
npx remotion render Showcase out/showcase-butter.mp4 --props='{"theme":"butter"}'
# Batch: loop 11 tema
for t in butter cloud-dancer mocha-mousse lilac-haze rosewater dusty-sage forest-lace noir-editorial terracotta-sun riso-zine pearl-chrome; do
  npx remotion render Showcase out/showcase-$t.mp4 --props="{\"theme\":\"$t\"}"
done
```

**Lisensi Remotion:** Gratis untuk tim ≤ 3 orang (Ikat = 1 orang → gratis). Jika pakai automasi massal (render > 1.000/bulan), Company License $0.01/render (min $100/bulan) — masih murah vs editor Rp 50rb/video.

**Prioritas:** Validasi manual dulu (bulan 1 — rekam layar + CapCut). Jika 1 hook terbukti viral (> 10rb views), baru automasi dengan Remotion di bulan 2.

### 5.4 Prinsip Konten Indonesia

- **Bahasa:** Indonesia santai, bukan formal. "Kebuka" bukan "terbuka", "nggak" bukan "tidak" — sesuai copy landing yang sudah ada.
- **Musik:** Jangan pakai lagu komersial di konten — pakai piano generate Ikat sendiri (`bin/make-music.py`) atau royalty-free TikTok library.
- **Waktu post:** 19:00–21:00 WIB (prime time scroll), Selasa–Kamis engagement tertinggi untuk niche wedding.
- **CTA selalu 1:** "Coba 11 tema gratis — link di bio" (jangan "follow + like + komen + share" sekaligus).

---

## 6. Funnel

### 6.1 Funnel B2C (Pasangan)

```
Discovery                    Consideration              Conversion              Retention
(TikTok/IG/Google)           (Landing + Preview)        (WA Chat → Bayar)       (Referral)
        |                            |                          |                     |
  10.000 views               800 klik ke landing        80 chat WA             20% refer teman
  (1 video viral)            (8% CTR bio)               (10% landing→WA)       (4 closing tambahan)
        |                            |                          |
        v                            v                          v
  Impression →              Klik → Preview            Chat → Closing
  CTR 2–5%                  Preview rate 40%          Closing 25–35%
                            (320 preview)             (20–28 closing)
```

**Angka funnel B2C (benchmark realistis Indonesia):**

| Stage | Metric | Target | Cara ukur |
|---|---|---|---|
| Awareness | Views (TikTok) | 10.000/bulan (bulan 1) → 50.000/bulan (bulan 3) | TikTok Analytics |
| Interest | Landing visits | 800/bulan → 4.000/bulan | Plausible/GA4 |
| Consideration | Preview clicks (`preview.html?theme=`) | 40% dari landing | Event `preview_click` |
| Intent | WA clicks (`wa.me`) | 10% dari landing | Event `wa_click` |
| Conversion | Closing (bayar) | 25–35% dari WA chat | Manual / Sheet |
| Revenue | — | 20 closing × Rp 149rb avg = Rp 2,98jt/bulan (bulan 1) | Sheet |

### 6.2 Funnel B2B2C (WO/MUA)

```
Discovery                    Consideration              Conversion              Expansion
(IG/WA grup/Expo)            (Landing #vendor + Demo)   (Reseller purchase)     (Repeat order)
        |                            |                          |                     |
  200 WO lihat               40 klik #vendor            5 beli paket 20/50     60% reorder bulan 2
  (konten reseller)          (20% CTR)                  (12,5% vendor→beli)    (3 reorder)
        |                            |                          |
        v                            v                          v
  Outreach →                 Edukasi →                  Trial →
  Response 15%               Demo 50%                   Closing 12,5%
```

| Stage | Metric | Target | Cara ukur |
|---|---|---|---|
| Awareness | WO reached (DM + grup + expo) | 200/bulan | Manual list |
| Interest | Klik #vendor | 20% dari reached | Event `vendor_click` |
| Consideration | Chat tanya reseller | 50% dari klik vendor | WA label "reseller" |
| Conversion | Beli paket reseller | 12,5% dari klik vendor (5/bulan awal) | Sheet |
| Expansion | Reorder / upsell 50→100 | 60% reorder dalam 60 hari | Sheet |
| LTV | Revenue per WO/tahun | Rp 2,4–7,2jt | Sheet |

### 6.3 Optimasi Funnel

| Bottleneck | Gejala | Fix |
|---|---|---|
| Views tinggi, klik landing rendah | CTR bio < 3% | Ganti hook/CTA, pakai link shortener dengan preview image |
| Landing tinggi, preview rendah | Preview < 20% | Galeri di atas fold sudah ada — cek load time, pastikan thumbs < 50 KB |
| Preview tinggi, WA rendah | WA < 5% | Harga terlalu tinggi di persepsi — tonjolkan "sekali bayar" + testimoni |
| WA tinggi, closing rendah | Closing < 15% | Response time > 5 menit — set auto-reply WA + template jawaban FAQ |

---

## 7. Partnerships (WO / MUA / Percetakan)

### 7.1 Model Kemitraan

| Model | Untuk Siapa | Cara Kerja | Harga untuk Mitra | Margin Mitra |
|---|---|---|---|---|
| **Reseller White-label** | WO kecil-menengah (5+ wedding/bulan) | Beli slot 20/50/100. Jual pakai brand sendiri, harga sendiri. Ikat tidak muncul. | Rp 499rb/20, Rp 990rb/50, Rp 1,69jt/100 | 75–83% (jual Rp 99rb) |
| **Affiliate Referral** | MUA, fotografer, venue | Daftar gratis, dapat link `ikat.link/ref/NAMA`. Tiap closing dapat komisi. | Gratis | Rp 25.000/closing |
| **Bundling** | Percetakan undangan fisik | Paket "Cetak 100 + Digital Plus" — percetakan jual, Ikat fulfill digital. | Rp 75.000/digital (percetakan jual Rp 149rb) | Rp 74.000 untuk percetakan |
| **Expo / Pameran** | WO pameran | Bagi booth, Ikat sediakan demo device + brosur, WO bawa klien. | Bagi hasil 70/30 (WO/Ikat) | — |

### 7.2 Paket Reseller Detail

```
Reseller 20  — Rp 499.000  (Rp 24.950/slot)  — Starter, WO baru coba
Reseller 50  — Rp 990.000  (Rp 19.800/slot)  — Paling laku (hero)
Reseller 100 — Rp 1.690.000 (Rp 16.900/slot) — WO besar, lock-in
```

- Slot tidak hangus 1 tahun. Habis → top-up paket lagi (reorder).
- White-label: subdomain `undangan.namawO.com` (CNAME ke Cloudflare Pages) atau path `ikat.link/namawO-klien`.
- Dashboard (roadmap): WO login, lihat semua undangan kliennya, rekap RSVP per event.

### 7.3 Cara Akuisisi WO/MUA (Taktik Spesifik Indonesia)

| Taktik | Detail | Target | Biaya |
|---|---|---|---|
| **DM Instagram manual** | Cari hashtag #WOBandung #WOJogja #MUASurabaya → DM 20/hari dengan template personal (bukan broadcast). "Hai kak, lihat WO kakak handle wedding aesthetic — kita ada engine undangan white-label, modal 19rb jual 99rb, mau lihat demo 2 menit?" | 600 DM/bulan, response 10–15% (60–90 balasan) | 0 (waktu 1 jam/hari) |
| **Grup WA WO se-kota** | Join via undangan di IG bio WO / tanya teman. 5 grup × 50 WO = 250 WO. Share value dulu (tips sebar undangan WA), soft sell minggu ke-2. | 250 WO reach/bulan | 0 |
| **HIPAPI / Asosiasi** | Daftar anggota HIPAPI (Himpunan Pengusaha Jasa Pernikahan Indonesia) — direktori + event. | 1 komunitas/bulan | Rp 0–300rb iuran |
| **Wedding expo tier 2** | Expo di kota tier 2 (Solo, Malang, Makassar) — biaya booth 1/3 Jakarta, kompetisi reseller lebih sepi. Titip brosur di booth WO mitra kalau belum mampu sewa booth sendiri. | 1 expo/kuartal | Rp 500rb–2jt titip brosur |
| **Referral WO → WO** | WO yang sudah reseller dapat 5 slot gratis kalau bawa 1 WO baru yang beli paket 50. | Viral loop | 5 × Rp 19.800 = Rp 99rb CAC |
| **Free sample** | Kasih 1 undangan gratis untuk WO (pakai data dummy WO itu sendiri sebagai demo portfolio mereka). WO pakai untuk pitch ke klien — kalau klien closing, WO sudah hooked. | 10 free sample/bulan | 10 × Rp 0 (cost = waktu 10 menit/sample) |

### 7.4 Onboarding Mitra (5 Langkah)

1. **Demo 2 menit:** Kirim link `preview.html?theme=butter` + video 30 detik ganti tema.
2. **Hitungan margin:** Kirim math "50 undangan × Rp 79.200 margin = Rp 3,96jt" — WO Indonesia butuh angka, bukan janji.
3. **Free sample:** Bikin 1 undangan gratis pakai nama WO (misal `demo-wo-ayu.html`) — WO langsung punya portfolio.
4. **Closing:** Transfer → kirim 50 slot + panduan 1 halaman (PDF) cara bikin undangan untuk klien.
5. **Follow-up H+7:** "Sudah coba jual ke klien minggu ini? Butuh bantuan pitch?" — 60% WO butuh dorongan pertama.

### 7.5 Kontrak & Kepercayaan

- Tidak perlu kontrak formal untuk paket 20/50 — transfer = deal. Untuk 100, MOU 1 halaman (hak white-label, durasi slot, support).
- **Jaminan:** "Slot tidak habis dalam 1 tahun? Sisa slot bisa refund 50%." — hilangkan risiko WO rugi.
- **Brand promise:** "Kami tidak pernah hubungi klien kalian. Klien adalah milik kalian sepenuhnya." — tulis di landing #vendor, ini objection #1 WO.

---

## 8. Metrics & KPIs

### 8.1 North Star Metric

**Jumlah undangan aktif (live invitations) per bulan.** Naik = produk dipakai, bukan cuma dibeli.

### 8.2 KPI per Funnel Stage

| KPI | Bulan 1 | Bulan 2 | Bulan 3 | Cara Ukur |
|---|---|---|---|---|
| **Awareness** | | | | |
| TikTok views | 10.000 | 25.000 | 50.000 | TikTok Analytics |
| IG reach | 3.000 | 8.000 | 15.000 | IG Insights |
| Landing visits | 800 | 2.000 | 4.000 | Plausible/GA4 |
| **Acquisition** | | | | |
| WA chats (B2C) | 80 | 200 | 400 | WA Business label |
| WO contacted | 200 | 200 | 200 | Sheet |
| WO responded | 30 (15%) | 40 (20%) | 50 (25%) | Sheet |
| **Conversion** | | | | |
| B2C closing | 20 | 50 | 100 | Sheet |
| Reseller sold (paket) | 3 | 7 | 12 | Sheet |
| Affiliate daftar | 0 | 10 | 25 | Sheet |
| **Revenue** | | | | |
| B2C revenue | Rp 2,98jt | Rp 7,45jt | Rp 14,9jt | Sheet |
| B2B2C revenue | Rp 2,97jt | Rp 6,93jt | Rp 11,88jt | Sheet |
| Total revenue | Rp 5,95jt | Rp 14,38jt | Rp 26,78jt | Sheet |
| Paid spend | Rp 3jt | Rp 3jt | Rp 4jt | Ads dashboard |
| **Retention** | | | | |
| Reseller reorder rate (60 hari) | — | 30% | 60% | Sheet |
| B2C referral rate | 10% | 15% | 20% | Kode referral |
| **Unit Economics** | | | | |
| CAC B2C | Rp 37.500 | Rp 30.000 | Rp 25.000 | Spend / closing |
| CAC B2B2C | Rp 99.000 | Rp 75.000 | Rp 50.000 | Spend+waktu / reseller |
| LTV B2B2C (12 bulan) | Rp 2,4jt | Rp 3,6jt | Rp 4,8jt | Avg reorder × margin |
| LTV/CAC B2B2C | 24× | 48× | 96× | — |

### 8.3 Dashboard Mingguan (15 Menit Review Senin Pagi)

```
Minggu ke-__:
- Views TikTok: ___ (target: 2.500/minggu)
- Landing visits: ___ (target: 200/minggu)
- WA chats: ___ (target: 20/minggu)
- Closing B2C: ___ (target: 5/minggu)
- WO contacted/responded: ___/___ (target: 50/8 per minggu)
- Reseller sold: ___ (target: 1/minggu bulan 1)
- Revenue minggu: Rp ___ (target: Rp 1,5jt/minggu bulan 1)
- Bottleneck minggu ini: ___
- Fix minggu depan: ___
```

### 8.4 Kapan Pivot / Kill

| Sinyal | Arti | Aksi |
|---|---|---|
| TikTok views < 2.000/bulan setelah 30 hari & 30 video | Hook salah atau niche terlalu sempit | Ganti 3 hook baru, test 14 hari lagi |
| Landing→WA < 3% setelah 500 visits | Harga atau copy tidak meyakinkan | A/B test headline, tambah testimoni, coba harga Rp 79rb untuk Basic |
| WA→closing < 15% setelah 50 chat | Response time atau objection handling | Set auto-reply < 2 menit, buat FAQ script 10 objection |
| WO response < 5% setelah 200 DM | Targeting atau pesan salah | Ganti kota, ganti template DM, coba free sample dulu baru DM |
| Reseller reorder < 20% setelah 60 hari | WO tidak berhasil jual ke kliennya | Bantu WO dengan template pitch + brosur untuk klien WO |

---

## 9. 30-60-90 Day Plan

### Hari 1–30: Foundation & Validation

**Tujuan:** Buktikan 1 hook TikTok jalan + 3 reseller pertama.

| Minggu | Tugas | Deliverable | Owner |
|---|---|---|---|
| 1 | Setup tracking: Plausible/GA4 di landing, event `preview_click`/`wa_click`/`vendor_click`, WA Business + label | Dashboard live | Solo |
| 1 | Riset hashtag & kompetitor: 20 video TikTok undangan digital teratas, catat hook + views + CTA | Sheet riset | Solo |
| 1 | Buat 3 hook video (22 KB test, ganti 11 tema, tanpa prewed) — rekam layar + CapCut, 9:16 | 3 video jadi | Solo |
| 1 | Tulis 2 artikel SEO: "Warna Undangan 2026" + "Undangan Digital Tanpa Foto Prewed" | 2 artikel publish | Solo |
| 2 | Post 1 video/hari TikTok + Reels (7 video/minggu), jam 19:00 WIB | 14 video publish | Solo |
| 2 | Mulai DM WO: 20/hari × 5 hari = 100 WO, kota Bandung + Jogja dulu (tier 2, kompetisi sepi) | 100 DM terkirim | Solo |
| 2 | Buat brosur 1 halaman reseller (PDF): math margin + 11 tema + cara order | PDF jadi | Solo |
| 3 | Follow-up WO yang respond (target 15), kasih free sample 1 undangan/WO | 5 free sample terkirim | Solo |
| 3 | Join 3 grup WA WO, share value (bukan jualan) | 3 grup joined | Solo |
| 3 | Setup Pinterest: 11 pin (1 per tema) | 11 pin live | Solo |
| 4 | Review funnel: views→landing→WA→closing. Identifikasi bottleneck #1. | Laporan minggu 4 | Solo |
| 4 | Closing push: follow-up semua WA chat yang belum closing dengan promo "gratis ganti tema 1×" | 3 reseller + 15 B2C closing | Solo |

**Target akhir Hari 30:**
- 10.000 TikTok views, 800 landing visits, 20 B2C closing, 3 reseller paket 20/50
- Revenue: ~Rp 5–6jt
- Validasi: 1 hook dengan > 5.000 views (jika tidak, ganti hook di bulan 2)

**Budget Hari 1–30: Rp 0 paid** (organic only — validasi dulu sebelum bakar uang).

---

### Hari 31–60: Scale Organic + Mulai Paid

**Tujuan:** 50 B2C + 7 reseller, mulai paid dengan ROAS > 2×.

| Minggu | Tugas | Deliverable |
|---|---|---|
| 5 | Launch TikTok Spark Ads: Rp 50rb/hari, boost video dengan views organik tertinggi | Ads live, CPC < Rp 800 |
| 5 | Launch Google Search Ads: Rp 20rb/hari, keyword "undangan digital" | Ads live |
| 5 | Buat paket Reseller 20 (Rp 499rb) — turunkan barrier WO kecil | Paket live di landing |
| 5 | Daftar affiliate: buat link `?ref=` sederhana (Sheet + kode manual dulu, belum perlu sistem) | 5 affiliate daftar |
| 6 | Automasi video (jika 1 hook > 10rb views): setup Remotion — 1 komponen baca `themes.json`, generate 11 varian showcase | 11 video Remotion jadi |
| 6 | Outreach percetakan: 10 percetakan undangan fisik di Bandung/Jogja, tawar bundling | 2 percetakan deal |
| 6 | Publish 2 artikel SEO lagi: "Cara Sebar Undangan WA Tanpa Diblokir" + "Checklist H-7 Sebar Undangan" | 2 artikel |
| 7 | Follow-up reseller bulan 1: bantu pitch, kasih template WA untuk klien WO | 30% reorder |
| 7 | Testimoni: minta 3 WO + 5 pasangan kasih testimoni video/foto (tukar 1 bulan gratis) | 8 testimoni terkumpul |
| 8 | Review + optimasi: kill ads dengan CPC > 2× target, scale yang ROAS > 3× | Laporan minggu 8 |
| 8 | Wedding expo: titip brosur di 1 expo tier 2 via WO mitra | 50 brosur tersebar |

**Target akhir Hari 60:**
- Kumulatif: 70 B2C closing, 10 reseller, 10 affiliate
- Revenue bulan 2: ~Rp 14jt
- Paid ROAS: > 2×

**Budget Hari 31–60: Rp 3jt paid + Rp 500rb operasional (brosur, expo titip).**

---

### Hari 61–90: Leverage & Systemize

**Tujuan:** 100 B2C + 12 reseller di bulan 3, sistem referral jalan, siap scale.

| Minggu | Tugas | Deliverable |
|---|---|---|
| 9 | Launch program referral WO→WO: "Bawa 1 WO baru, dapat 5 slot gratis" — umumkan di grup WA + DM | 3 referral WO baru |
| 9 | Scale Remotion: generate 33 varian (11 tema × 3 hook) untuk TikTok Ads A/B test | 33 video varian |
| 9 | IG Ads Reels: Rp 30rb/hari, carousel 11 tema | Ads live |
| 10 | Build dashboard WO sederhana (opsional, jika > 15 reseller): login lihat slot terpakai/sisa + rekap RSVP | Dashboard v1 atau Sheet upgrade |
| 10 | SEO: 2 artikel lagi + daftar di 5 direktori WO (weddingku.com dll) | Backlink 5 |
| 10 | Affiliate push: 15 MUA/fotografer baru via DM + komisi Rp 25rb | 15 affiliate baru |
| 11 | Roadmap guest management: spec QR check-in + broadcast WA H-1, validasi dengan 5 WO (mau bayar Rp 49rb?) | Spec + 5 validasi |
| 11 | Scale paid: naikkan budget 30% untuk channel dengan ROAS > 3× | Budget Rp 4jt/bulan |
| 12 | Review 90 hari: hitung LTV/CAC per channel, tentukan channel #1 untuk scale 2× di kuartal 2 | Laporan 90 hari |
| 12 | Plan Q2: target 50 reseller aktif, QR check-in launch, Cloudflare Pages multi-client live | Roadmap Q2 |

**Target akhir Hari 90:**
- Bulan 3: 100 B2C closing + 12 reseller + 25 affiliate aktif
- Revenue bulan 3: ~Rp 26jt
- Kumulatif 90 hari: ~Rp 46jt revenue, 170 B2C + 22 reseller
- Validasi guest management: 5 WO commit bayar add-on

**Budget Hari 61–90: Rp 4jt paid + Rp 1jt operasional.**

---

### Ringkasan Budget 90 Hari

| Periode | Paid Ads | Operasional | Total | Revenue Target | Net |
|---|---|---|---|---|---|
| Hari 1–30 | Rp 0 | Rp 200rb | Rp 200rb | Rp 5,9jt | +Rp 5,7jt |
| Hari 31–60 | Rp 3jt | Rp 500rb | Rp 3,5jt | Rp 14,3jt | +Rp 10,8jt |
| Hari 61–90 | Rp 4jt | Rp 1jt | Rp 5jt | Rp 26,7jt | +Rp 21,7jt |
| **Total 90 hari** | **Rp 7jt** | **Rp 1,7jt** | **Rp 8,7jt** | **Rp 46,9jt** | **+Rp 38,2jt** |

> Catatan: Revenue adalah gross. Belum potong biaya hosting (Cloudflare gratis), domain (~Rp 150rb/tahun), dan waktu founder. Net di atas adalah sebelum gaji founder — untuk solo founder, ini sudah profit dari bulan 1.

---

## Appendix

### A. Musim Nikah Indonesia (Timing Campaign)

| Periode | Intensitas Nikah | Aksi Marketing |
|---|---|---|
| **Syawal–Dzulhijjah (Apr–Jul 2026)** | Puncak #1 — antrean gedung penuh | Push maksimal, naikkan budget 50% |
| **Muharram–Safar (Jul–Agu 2026)** | Puncak #2 | Push, target pasangan yang booking gedung 3 bulan sebelumnya (Apr–Mei) |
| **Maulid–Rabiul Akhir (Sep–Nov)** | Menengah | Fokus reseller (WO booking untuk puncak berikutnya) |
| **Rajab–Sya'ban (Des–Feb)** | Rendah | Build content backlog, SEO, Remotion automasi |
| **Ramadhan (Feb–Mar 2026)** | Sangat rendah (hampir tidak ada nikah) | Jangan paid ads — fokus partnership & produk (QR check-in) |

### B. Tools Stack (Gratis/Murah)

| Kebutuhan | Tool | Biaya |
|---|---|---|
| Landing + hosting etalase | GitHub Pages (sudah ada) | Gratis |
| Hosting undangan klien | Cloudflare Pages | Gratis |
| Analytics | Plausible (self-host) atau GA4 | Gratis |
| WA Business | WhatsApp Business App + label | Gratis |
| Desain brosur/PDF | Canva free | Gratis |
| Video edit (bulan 1) | CapCut desktop | Gratis |
| Video programmatic (bulan 2+) | Remotion (tim ≤ 3 gratis) | Gratis |
| SEO keyword | Google Keyword Planner + Trends | Gratis |
| Email (jika perlu) | — | Tidak perlu di 90 hari pertama (WA > email di Indonesia) |

### C. Kompetitor Watchlist

Pantau 2×/bulan: harga, tema baru, promo di Shopee/Tokopedia/IG. Catat di Sheet. Jika kompetitor turun harga < Rp 50rb, jangan ikut — tekankan wedge performa + white-label.

### D. Referensi

- Business context: `second-brain/Projects/ikat — Engine template undangan digital.md` (4 wedge, pasar 1,5–2jt nikah/tahun)
- Pricing: `site/index.html` (Basic 99k, Plus 199k, Custom 499k, Reseller 50 = 990k)
- Video generation: `second-brain/Resources/Learning-DevOps/Remotion - Programmatic Video with React.md` (React → MP4 via headless Chrome + FFmpeg, parameterized rendering, gratis untuk tim ≤ 3)
- Deploy: `docs/DEPLOY.md` (GitHub Pages untuk etalase, Cloudflare Pages untuk klien — POP Jakarta)
- Themes: `themes/themes.json` (11 tema, SOT untuk generate konten programmatic)

---

*Dokumen ini adalah rencana kerja, bukan ramalan. Angka target adalah patokan untuk deteksi bottleneck — jika meleset > 50%, revisi taktiknya, bukan angkanya. Review mingguan, commit bulanan.*
