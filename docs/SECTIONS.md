# Katalog section

Urutan section ditentukan array `sections` di file data. Ganti urutannya,
hapus yang tidak dipakai, atau pakai satu tipe berkali-kali (`event` biasanya
dua kali: akad dan resepsi).

Tipe yang tidak dikenal dilewati dengan peringatan di console, bukan crash —
supaya satu data lama tidak mematikan seluruh undangan.

---

### `cover`

Layar penuh, mengunci scroll sampai tamu menekan tombol buka.

```json
{ "type": "cover", "eyebrow": "The Wedding Of", "photo": "", "monogram": "D & R",
  "openLabel": "Buka Undangan", "guestLabel": "Kepada Yth.",
  "guestFallback": "Bapak/Ibu/Saudara/i" }
```

Nama dan tanggal tidak ditulis di sini — diambil dari `couple` dan `date`.

Nama tamu berasal dari query string. `guestFallback` dipakai kalau query string
kosong, supaya satu link generik (disebar ke grup WhatsApp, atau dipakai buat
preview) tetap terbaca sebagai undangan dan bukan slot kosong.

### `quote`

Ayat atau kutipan. Setiap field opsional; yang kosong tidak dirender.

```json
{ "type": "quote", "arabic": "…", "text": "…", "cite": "Q.S. Ar-Rum : 21" }
```

### `countdown`

Hitung mundur ke `date` di level root. Otomatis berganti jadi pesan "hari
bahagia telah tiba" setelah lewat.

```json
{ "type": "countdown", "heading": "Save the Date" }
```

### `couple`

Kedua mempelai beserta orang tua dan Instagram. Isinya dari `couple` di root,
section ini hanya membawa salam pembuka.

```json
{ "type": "couple", "greeting": "…", "intro": "…" }
```

### `event`

Boleh muncul berkali-kali. Merender strip hari-dalam-seminggu dengan tanggal
acara ditandai, jam, venue, tombol peta, dan tombol simpan ke Google Calendar.

```json
{ "type": "event", "heading": "Akad Nikah",
  "start": "2026-09-24T08:00:00+07:00", "end": "2026-09-24T10:00:00+07:00",
  "venue": "…", "address": "…", "maps": "https://maps.google.com/?q=…",
  "mapsLabel": "Petunjuk Lokasi" }
```

Selalu tulis offset (`+07:00`) di `start`/`end`. Waktu ditampilkan dalam
`meta.timezone`, bukan zona waktu tamu — tamu di Jeddah tetap harus membaca
jam acara waktu setempat.

### `gallery`

Tidak dirender kalau `photos` kosong.

```json
{ "type": "gallery", "heading": "Our Moments", "caption": "…",
  "photos": ["a.webp", { "src": "b.webp", "caption": "Lamaran" }] }
```

### `story`

Linimasa. Tidak dirender kalau `items` kosong.

```json
{ "type": "story", "heading": "Our Story",
  "items": [{ "when": "2019", "title": "Pertama Bertemu", "text": "…" }] }
```

### `gift`

Dua bentuk `accounts`: `bank` (dengan tombol salin nomor) dan `address`.

```json
{ "type": "gift", "heading": "Wedding Gift", "text": "…",
  "accounts": [
    { "kind": "bank", "bank": "BCA", "number": "1234567890", "holder": "…" },
    { "kind": "address", "label": "Alamat Pengiriman Hadiah", "holder": "…", "address": "…" }
  ] }
```

### `rsvp`

Form konfirmasi plus dinding tamu. Backend ditentukan `rsvp.adapter` di root,
bukan di sini.

```json
{ "type": "rsvp", "heading": "Konfirmasi Kehadiran", "text": "…",
  "guestbookHeading": "Dinding Tamu" }
```

### `closing`

Penutup: foto, wax seal, ucapan terima kasih.

```json
{ "type": "closing", "heading": "We are Getting Married!",
  "text": "…", "signoff": "…", "photo": "" }
```

---

## Section custom

Kalau satu klien butuh sesuatu yang tidak ada di katalog — denah kursi, live
streaming, protokol kesehatan — daftarkan sebelum `init()`:

```js
Ikat.register('livestream', function (s, cfg) {
  return '<section class="u-sec u-live" data-sec="livestream">' +
           '<h2 class="u-h2">' + s.heading + '</h2>' +
           '<a class="u-btn u-btn--primary" href="' + s.url + '">Tonton</a>' +
         '</section>';
});
Ikat.init({ src: 'data/klien.json' });
```

Pakai kelas `u-*` yang sudah ada supaya section custom ikut tertema otomatis
tanpa CSS tambahan.

## Nama tamu di URL

```
undangan.html?to=Keluarga%20Besar%20Wijaya
```

`to`, `u`, dan `kepada` semuanya diterima. Nama tersebut muncul di cover dan
mengisi otomatis field nama di form RSVP. Nilainya di-render lewat
`textContent`, bukan `innerHTML` — jadi link yang dibagikan ke ratusan tamu
tidak bisa dipakai untuk menyuntik markup.

Tanpa parameter, engine memakai `guestFallback` dari section `cover`.

## Backend RSVP

`rsvp.adapter` menerima tiga nilai:

| Adapter | Kapan dipakai | Butuh |
|---|---|---|
| `demo` | demo, preview ke calon klien, jualan sebelum ada hosting | tidak ada — simpan di localStorage |
| `script` | produksi murah, data masuk Google Sheet | URL Apps Script web app |
| `supabase` | produksi serius, banyak klien sekaligus | URL project, anon key, nama tabel |

```json
{ "rsvp": { "adapter": "script", "endpoint": "https://script.google.com/macros/s/…/exec", "guestbook": true } }
```

Untuk `supabase`, kunci RLS-nya: insert boleh, select boleh, update dan delete
ditolak. Anon key ada di sisi klien, jadi tabel harus aman meski key terbaca.

Adapter baru cukup mengekspos dua method:

```js
Ikat.adapters.myBackend = function (cfg) {
  return {
    list: function () { return Promise.resolve([]); },   // → array entri
    submit: function (entry) { return Promise.resolve(entry); }
  };
};
```
