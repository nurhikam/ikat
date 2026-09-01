# Marketing — aset, video, dan workflow

> Satu tempat untuk semua tooling promo Ikat. Tema di `themes/themes.json`
> adalah sumber kebenaran — semua aset digenerate dari sana, bukan
> diedit manual.

## Tooling ringkas

| Tool | Untuk | Perintah |
|---|---|---|
| `bin/make-assets.py` | OG image, square post, story cover, favicon | `make-assets --theme butter --og -o /tmp/og.png` |
| `bin/make-promo-video.py` | Promo video 6s per tema (PIL + ffmpeg) | `make-promo-video --theme butter -o dist/promo.mp4` |
| `bin/ikat-mcp.py` | MCP server — semua di atas via agent | `python3 bin/ikat-mcp.py` (stdio) |

Semua tool **offline-capable**: PIL + DejaVu Sans + ffmpeg. Tidak butuh
Node, tidak butuh Google Fonts, tidak butuh network. Warna dan bentuk
dari `themes/themes.json` sudah cukup untuk bawa identitas tema di
format promo 6 detik.

---

## 1. Gambar statis — `bin/make-assets.py`

```
./bin/make-assets.py --list
./bin/make-assets.py --theme butter --og -o /tmp/og-butter.png
./bin/make-assets.py --theme noir-editorial --square -o /tmp/square.png
./bin/make-assets.py --theme butter --story -o /tmp/story.png
./bin/make-assets.py --theme butter --favicon -o /tmp/favicon.png
./bin/make-assets.py --all --og --square --story -o dist/assets/
./bin/make-assets.py --all --og -o dist/assets/ --format webp
```

| Kind | Ukuran | Untuk |
|---|---|---|
| `og` | 1200×630 | Open Graph / Twitter card / link preview |
| `square` | 1080×1080 | Instagram feed, square post |
| `story` | 1080×1920 | Instagram story, reels cover, TikTok cover |
| `favicon` | 512×512 | PWA / favicon source (downscale ke 32/180) |

- `--format png|webp|jpg` — default `png`. `webp` paling kecil untuk web.
- Tanpa `--og/--square/--story/--favicon`, default-nya `--og`.
- `--all` + `-o dist/assets/` → satu file per tema per kind.

**Cara pakai OG image di undangan:**

```html
<meta property="og:image" content="https://ikat.id/assets/og-butter.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
```

Generate dulu, commit ke `site/assets/` atau `dist/assets/`, lalu
referensikan di `data/<klien>.json` atau di `site/index.html`.

---

## 2. Video promo — `bin/make-promo-video.py`

```
./bin/make-promo-video.py --list
./bin/make-promo-video.py --theme butter --preview -o /tmp/preview.png
./bin/make-promo-video.py --theme butter -o dist/promo-butter.mp4
./bin/make-promo-video.py --theme butter --format square -o dist/promo-square.mp4
./bin/make-promo-video.py --all --format vertical -o dist/
./bin/make-promo-video.py --theme butter --no-encode --frames-dir /tmp/frames
```

| Preset | Ukuran | Untuk |
|---|---|---|
| `vertical` | 1080×1920 | Reels, story, TikTok (default) |
| `horizontal` | 1920×1080 | YouTube, OG video |
| `square` | 1080×1080 | Feed video |

- `--duration 6.0` — durasi detik (default 6s).
- `--fps 30` — frame rate (default 30).
- `--preview` — render 1 frame PNG (tengah video) tanpa encode — cepat
  untuk cek visual.
- `--no-encode` — simpan PNG sequence saja, skip ffmpeg.
- `--width/--height` — override dimensi preset.

**Struktur video 6 detik:**

```
0.0–1.0s  Title card — nama tema fade + scale in
1.0–3.0s  Palette — swatch warna + blurb slide in
3.0–5.0s  Mock card — kartu undangan pakai warna tema
5.0–6.0s  CTA — "Undangan yang kebuka" + tombol
```

**Kenapa PIL + ffmpeg, bukan Remotion?**

- VPS ini tidak punya `drawtext` di ffmpeg dan belum ada project
  Remotion di repo. PIL + ffmpeg jalan sekarang tanpa setup Node.
- Catatan Remotion ada di second-brain:
  `Resources/Learning-DevOps/Remotion - Programmatic Video with React.md`.
  Ketika preview React sudah ada, ganti renderer PIL dengan komposisi
  Remotion dan pertahankan CLI yang sama — lihat §5 di bawah.

**Codec:** H.264, yuv420p, CRF 18, `+faststart` (moov di depan — penting
untuk preview di WhatsApp/IG).

---

## 3. MCP server — `bin/ikat-mcp.py`

Stdio JSON-RPC 2.0, tanpa SDK — pola yang sama dengan `framedeck`
(`Resources/Agentic/framedeck — Bikin video kebaca agent lewat MCP.md`).

```json
{
  "mcpServers": {
    "ikat": {
      "command": ["python3", "/home/dev/work/ikat/bin/ikat-mcp.py"]
    }
  }
}
```

Claude Code:

```bash
claude mcp add ikat -- python3 bin/ikat-mcp.py
```

opencode (`opencode.json`):

```json
{ "mcp": { "ikat": { "type": "local", "command": ["python3", "bin/ikat-mcp.py"], "enabled": true } } }
```

| Tool | Untuk |
|---|---|
| `ikat_list_themes` | List semua tema + palette |
| `ikat_theme_info` | Detail satu tema |
| `ikat_generate_og` | OG image satu tema → path |
| `ikat_generate_assets` | Batch og/square/story/favicon → manifest |
| `ikat_generate_promo` | Video promo atau preview PNG → path |
| `ikat_render_preview` | Preview PNG ukuran bebas → path |

Semua tool yang menghasilkan file mengembalikan **absolute path** — baca
path itu sebagai image untuk verifikasi visual (sama seperti `framedeck`).

---

## 4. Workflow — dari tema baru sampai post

```bash
# 1. Tambah tema di themes/themes.json, lalu render CSS + site
./bin/make-theme.py nama-tema
./bin/make-site.py

# 2. Generate aset untuk tema baru
./bin/make-assets.py --theme nama-tema --og --square --story -o dist/assets/
./bin/make-promo-video.py --theme nama-tema --preview -o /tmp/preview.png
# cek preview, kalau ok:
./bin/make-promo-video.py --theme nama-tema -o dist/promo-nama-tema-vertical.mp4

# 3. Batch untuk semua tema (mis. sebelum launch)
./bin/make-assets.py --all --og -o dist/assets/ --format webp
./bin/make-promo-video.py --all --format vertical -o dist/

# 4. Pakai di site / sosmed
# - OG: <meta property="og:image" content=".../og-nama-tema.webp">
# - Feed: upload square ke Instagram
# - Story: upload story cover + promo video ke Reels/TikTok
```

---

## 5. Upgrade path — ke Remotion

PIL + ffmpeg adalah **fallback yang sengaja**. Ketika ada preview React
yang bisa di-render headless, upgrade path-nya:

1. `npx create-video@latest` di `video/` (atau pakai `video/` yang sudah
   ada kalau pernah di-init).
2. Satu komposisi per tema — `src/Root.tsx` baca `themes/themes.json`
   sebagai `defaultProps` (parameterized rendering, lihat Remotion docs
   `parameterized-rendering`).
3. Animasi pakai `useCurrentFrame()` + `interpolate()`/`spring()` — jangan
   CSS transitions (flicker saat export).
4. Render via `npx remotion render <Comp> out/video.mp4` atau
   `@remotion/renderer` (`renderMedia()`) untuk self-host.
5. Pertahankan CLI `bin/make-promo-video.py` sebagai wrapper — deteksi
   apakah `video/` ada, kalau ada pakai Remotion, kalau tidak fallback ke
   PIL. Jadi CI yang belum punya Node tetap jalan.

Referensi: `Resources/Learning-DevOps/Remotion - Programmatic Video with React.md`
di second-brain (ringkasan `remotion.dev` per 31 Aug 2026).

---

## 6. Checklist sebelum publish aset

- [ ] Preview di HP (bukan cuma di laptop) — teks masih kebaca di 320px?
- [ ] OG image dites di [opengraph.xyz](https://www.opengraph.xyz) atau
      `curl` + cek `og:image` kebaca.
- [ ] Video diputar di WhatsApp preview (moov di depan — `+faststart` sudah).
- [ ] Warna di video/gambar masih akurat (bandingkan dengan `preview.html?theme=...`).
- [ ] File di-optimize: `png` → `webp` untuk web, `mp4` sudah CRF 18.

---

*Terakhir diperbarui: 2026-09-01. Untuk domain & hosting lihat `docs/DOMAIN.md`,
untuk arsitektur tema lihat `docs/THEMING.md`.*
