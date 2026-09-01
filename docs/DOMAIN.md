# Domain — beli, pasang, dan jaga

> Keputusan domain itu murah di awal, mahal kalau salah. Catatan ini
> ngasih opsi nama, di mana belinya, dan gimana pasangnya di Cloudflare
> supaya undangan klien tetap cepat di sinyal jelek.

## 1. Nama — opsi yang masih masuk akal

Kriteria: pendek, gampang diucap di WhatsApp voice note, nggak tabrakan
dengan brand besar, dan `.id`/`.com` masih kosong (cek ulang sebelum beli —
ketersediaan berubah harian).

| Opsi | Kenapa kepikiran | Cek dulu |
|---|---|---|
| `ikat.id` | Nama produknya sendiri. Paling bersih kalau masih kosong. | `whois ikat.id` — 4 huruf, kemungkinan sudah diambil. |
| `ikatundangan.id` | Deskriptif, SEO langsung nyambung. | Lebih panjang tapi jelas. |
| `undangikat.id` | Variasi kalau `ikat.id` sudah diambil. | — |
| `ikat.co.id` | Alternatif `.id` kalau `.id` habis. | Butuh SIUP/NIB untuk `.co.id`. |
| `ikatundangan.com` | Fallback `.com` kalau semua `.id` habis. | `.com` paling mahal renew-nya tapi paling universal. |
| `ikat.invite` / `ikat.wedding` | TLD baru, unik, tapi orang masih mikir `.com`. | Harga TLD baru sering mahal (Rp 400rb–1jt/tahun). |

**Rekomendasi urutan coba:**

1. `ikat.id` — cek dulu. Kalau kosong, ambil tanpa pikir panjang.
2. Kalau sudah diambil, `ikatundangan.id` atau `undangikat.id`.
3. `.com` hanya kalau `.id` beneran habis semua — `.id` lebih dipercaya
   tamu Indonesia dan lebih murah.

**Yang dihindari:**

- Tanda hubung (`ikat-undangan.id`) — susah diucap, gampang salah ketik.
- Angka (`ikat88.id`) — kelihatan spam.
- Nama yang mirip brand besar (`kats.id`, `ikats.id`) — typo-squatting
  liability dan susah di-branding.

**Subdomain untuk klien** (setelah domain utama jadi):

```
undangan.ikat.id/andi-sari?to=Budi
undangan.ikat.id/rina-doni?to=Keluarga%20Wijaya
```

Satu domain, banyak path — sesuai pola di `docs/DEPLOY.md`. Jangan bikin
satu subdomain per klien (`andi-sari.ikat.id`) — itu butuh wildcard cert
dan bikin DNS berantakan di skala 100 klien.

---

## 2. Di mana beli — registrar

| Registrar | Harga `.id` /tahun | Kelebihan | Kekurangan |
|---|---|---|---|
| **Cloudflare Registrar** | Harga pokok (tanpa markup) | Paling murah long-term, DNS sudah di Cloudflare jadi satu tempat. | Tidak jual semua TLD, UI minimal. |
| **Niagahoster (Hostinger)** | Rp 200–300rb | Support lokal, bisa bayar transfer bank/e-wallet, ada promo tahun pertama. | Renew sering naik, upsell hosting. |
| **Domainesia** | Rp 220–320rb | Support lokal responsif, panel sederhana. | Sama — harga renew bisa naik. |
| **Namecheap** | $10–15 (`.com`) | Murah untuk `.com`, gratis WhoisGuard. | `.id` tidak tersedia. |
| **Porkbun** | Harga pokok + tipis | Murah, transparan, gratis WHOIS privacy. | `.id` tidak tersedia. |

**Rekomendasi:**

- **Kalau mau simpel dan murah long-term:** beli `.id` di **Niagahoster**
  atau **Domainesia** (karena Cloudflare Registrar belum tentu jual `.id`),
  lalu pindahkan nameserver ke Cloudflare (gratis). Renew tetap di
  registrar asal, DNS di Cloudflare.
- **Kalau `.com`:** **Cloudflare Registrar** atau **Porkbun** — harga
  pokok, tanpa markup renew.
- **Hindari:** beli domain di tempat yang nggak kasih akses panel DNS
  penuh atau yang ngunci transfer 60 hari tanpa alasan.

**Checklist sebelum checkout:**

- [ ] Cek `whois` dan pastikan status `available`, bukan `premium` atau `reserved`.
- [ ] Aktifkan **auto-renew** — domain undangan yang expired bikin semua
      link tamu mati.
- [ ] Kunci **registrar lock** (transfer lock) biar nggak gampang dibajak.
- [ ] Isi kontak WHOIS dengan email yang aktif (untuk `.id` PANDI butuh
      validasi KTP/email).

---

## 3. DNS & Cloudflare setup

### 3.1 Pindahkan DNS ke Cloudflare (gratis)

1. Daftar di [dash.cloudflare.com](https://dash.cloudflare.com) → **Add a Site** → masukkan domain.
2. Pilih paket **Free** — cukup untuk semua kebutuhan Ikat.
3. Cloudflare kasih 2 nameserver (`*.ns.cloudflare.com`). Ganti di panel
   registrar (Niagahoster/Domainesia → DNS Management → Custom Nameserver).
4. Tunggu propagasi (5 menit – 24 jam). Cek di `whatsmydns.net`.

### 3.2 Record yang perlu

Untuk **etalase** (GitHub Pages) + **undangan klien** (Cloudflare Pages)
di satu domain:

```
Type    Name        Value / Target                  Proxy   TTL
CNAME   @           <user>.github.io                DNS     Auto
CNAME   www         <user>.github.io                DNS     Auto
CNAME   undangan    ikat.pages.dev                  Proxied Auto
TXT     @           v=spf1 -all                     DNS     Auto
```

- `ikat.id` → GitHub Pages (landing + demo). Cloudflare **DNS only**
  (awan abu-abu) — biar Pages yang handle cert-nya.
- `undangan.ikat.id` → Cloudflare Pages (repo privat klien). **Proxied**
  (awan oranye) — biar dapat edge Jakarta + cache.
- `www` → redirect ke apex (atur di Cloudflare Rules → Redirect).

> **Kenapa `undangan.*` di-proxied?** Karena argumen jualan Ikat adalah
> "kebuka di sinyal satu bar". Cloudflare punya POP di Jakarta — request
> tamu di Solo nggak perlu muter ke Singapura/Virginia. Ini yang bikin
> 22 KB itu beneran 22 KB di lapangan, bukan cuma di lab.

### 3.3 SSL / HTTPS

- **Mode:** `Full (strict)` di Cloudflare → SSL → Overview.
- GitHub Pages dan Cloudflare Pages sama-sama issue cert otomatis (Let's
  Encrypt) — tidak perlu beli cert.
- Aktifkan **Always Use HTTPS** dan **Automatic HTTPS Rewrites**.
- HSTS: aktifkan setelah yakin semua subdomain sudah HTTPS (max-age 6 bulan).

### 3.4 Cache & performa

```
Cloudflare → Caching → Configuration
  Browser Cache TTL: 4 hours
  Caching Level: Standard
  Always Online: On

Cloudflare → Speed → Optimization
  Auto Minify: JS, CSS, HTML — On
  Brotli: On
  Early Hints: On
```

Untuk Cloudflare Pages (`undangan.*`), cache HTML jangan terlalu lama
(klien bisa ganti tanggal) — set `Cache-Control: public, max-age=300`
di header Pages (via `_headers` file di repo privat).

### 3.5 Email (opsional, tapi disarankan)

Biar bisa kirim dari `halo@ikat.id` tanpa sewa mail server:

- **Cloudflare Email Routing** (gratis) — forward `halo@ikat.id` → Gmail
  pribadi. Cukup untuk terima balasan tamu/klien.
- **Zoho Mail** (gratis 5 user) atau **Google Workspace** (Rp 80rb/user)
  kalau butuh kirim massal.
- Jangan lupa SPF/DKIM/DMARC kalau kirim email dari domain — tanpa itu
  masuk spam.

---

## 4. Biaya ringkas (estimasi 2026)

| Item | Biaya/tahun | Catatan |
|---|---|---|
| Domain `.id` | Rp 220–320rb | Sekali setahun, auto-renew |
| Domain `.com` (kalau pakai) | Rp 180–250rb | — |
| Cloudflare DNS + proxy | Gratis | Paket Free cukup |
| Cloudflare Pages (klien) | Gratis | 500 build/bulan, unlimited bandwidth |
| GitHub Pages (etalase) | Gratis | Repo publik |
| Email routing | Gratis | Cloudflare Email Routing |
| **Total minimal** | **~Rp 250rb/tahun** | Domain doang |

---

## 5. Langkah beli — urutan yang disarankan

```bash
# 1. Cek ketersediaan
whois ikat.id
# atau online: https://pandi.id/whois  /  https://who.is/

# 2. Beli di registrar (Niagahoster/Domainesia untuk .id)
#    — aktifkan auto-renew + registrar lock

# 3. Tambah site di Cloudflare, ganti nameserver

# 4. Verifikasi DNS sudah di Cloudflare
dig NS ikat.id +short
# harus keluar *.ns.cloudflare.com

# 5. Pasang record (CNAME / A) sesuai §3.2

# 6. Deploy etalase ke GitHub Pages (sudah ada workflow di .github/workflows/pages.yml)
#    Deploy klien ke Cloudflare Pages:
npx wrangler pages deploy . --project-name ikat

# 7. Cek HTTPS + redirect
curl -I https://ikat.id
curl -I https://undangan.ikat.id/andi-sari?to=Test
```

---

## 6. Jaga domain jangan hilang

- Kalender: set reminder **H-30** sebelum expired (selain auto-renew).
- Email WHOIS harus yang aktif — notifikasi expired masuk ke sana.
- Jangan pakai email kantor yang bisa hangus kalau resign.
- Backup: catat **auth code / EPP code** di password manager — ini kunci
  pindah registrar kalau butuh.
- Kalau domain premium/berharga, aktifkan **2FA** di registrar + Cloudflare.

---

*Terakhir diperbarui: 2026-09-01. Harga registrar bisa berubah — cek ulang
sebelum checkout. Untuk arsitektur deploy lengkap lihat `docs/DEPLOY.md`.*
