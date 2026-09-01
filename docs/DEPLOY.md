# Deploy

Ada satu hal yang menentukan seluruh jawabannya, dan lebih baik disadari
sekarang daripada setelah seratus klien:

> **Data klien tidak boleh masuk repo publik.**

`data/<klien>.json` berisi nomor rekening, alamat rumah, nomor HP, dan nama
tamu. GitHub Pages di paket gratis mensyaratkan repo publik. Artinya nomor
rekening klienmu akan bisa dibaca siapa saja — dan karena git menyimpan
riwayat, menghapusnya belakangan tidak menghapus jejaknya.

Jadi pisahkan dua hal yang memang beda:

| Yang di-deploy | Ke mana | Kenapa |
|---|---|---|
| Engine + tema + demo (etalase) | GitHub Pages | publik memang tujuannya — ini portofolio jualanmu |
| Undangan klien asli | Cloudflare Pages | source tetap privat, edge-nya ada di Jakarta |

## 1. Etalase — GitHub Pages

Sudah ada workflow-nya di `.github/workflows/pages.yml`. Sekali setup:

1. Push repo ini ke GitHub.
2. **Settings → Pages → Source: GitHub Actions**.
3. Push ke `main`. Situsnya terbit di
   `https://<user>.github.io/undangan/`.

Yang terbit hanya `data/demo.json` — data fiktif. Jangan pernah menaruh
`data/<klien-asli>.json` di repo ini; `.gitignore` sudah menahan `data/*.json`
kecuali `demo.json` supaya tidak kelepasan.

## 2. Undangan klien — Cloudflare Pages

Kenapa Cloudflare dan bukan yang lain:

- **Repo boleh privat**, dan tetap gratis. Ini alasan utamanya.
- **Ada POP di Jakarta.** Karena argumen jualanmu adalah "undangan ini kebuka
  cepat di sinyal jelek", asal servernya penting. Deploy ke edge Singapura atau
  Virginia membuang keunggulan itu.
- **Bandwidth tidak dibatasi** di paket gratis. Satu undangan viral di grup
  keluarga besar tidak bikin tagihan.
- Vercel Hobby **melarang penggunaan komersial** — kamu jualan, jadi itu bukan
  pilihan tanpa upgrade. Netlify gratis dibatasi 100 GB/bulan.

### Cara yang tidak menskala (jangan)

Satu site Cloudflare per klien. Seratus klien = seratus project, seratus
domain, seratus deploy.

### Cara yang menskala

**Satu site, banyak klien sebagai path.**

```
undangan.domainmu.com/andi-sari?to=Budi%20Santoso
undangan.domainmu.com/rina-doni?to=Keluarga%20Wijaya
```

Repo privat terpisah (`undangan-klien`) yang isinya:

```
engine/          disalin dari repo ini, atau dipasang sebagai submodule
themes/
assets/
data/            satu JSON per klien — repo ini privat, jadi aman
andi-sari.html   dibuat oleh bin/new-client.sh
rina-doni.html
```

Deploy:

```bash
npx wrangler pages deploy . --project-name ikat
```

Klien baru = dua file + satu deploy. Tidak ada infrastruktur baru per klien.

### RSVP

Adapter `demo` (localStorage) tidak menyimpan apa pun di server — kiriman tamu
hanya ada di browser tamu itu sendiri. Bagus untuk preview, tidak berguna untuk
acara sungguhan.

Untuk produksi pakai `supabase`: satu tabel `rsvp` untuk semua klien, dengan
kolom `client` sebagai pembeda. RLS-nya insert boleh, select boleh, update dan
delete ditolak — anon key ada di sisi klien jadi tabelnya harus aman walau key
terbaca. Lihat [SECTIONS.md](SECTIONS.md#backend-rsvp).

## 3. Tanpa hosting sama sekali

```bash
./bin/build-single.py data/andi-sari.json --inline-media -o dist/andi-sari.html
```

Satu file, semua aset tertanam, bisa dikirim lewat WhatsApp atau email dan
dibuka langsung. Berguna untuk serah terima ke klien setelah acara, atau untuk
klien yang tidak mau punya link sama sekali.

**Tapi jangan pakai ini untuk menyebar ke tamu.** `--inline-media` menanam
musik sebagai data URI, jadi ukurannya melonjak dari ~22 KB ke ~1 MB dan
seluruhnya harus turun sebelum halaman tampil. Versi hosted memuat musik hanya
ketika tamu menekan tombol putar — itu bedanya undangan yang kebuka instan dan
undangan yang bikin tamu nutup tab.
