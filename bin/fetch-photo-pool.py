#!/usr/bin/env python3
"""Ambil kolam foto CC0 yang besar, lalu bagikan set berbeda ke tiap tema.

    ./bin/fetch-photo-pool.py            # ambil + assign
    ./bin/fetch-photo-pool.py --assign   # assign ulang saja, tanpa unduh

Kenapa ada: 113 tema memakai delapan foto yang sama, dan foto sampulnya identik
di semuanya. Itu penyebab tunggal terbesar kenapa preview-nya terasa seragam —
jauh lebih terasa daripada warna. Palet boleh beda-beda, tapi kalau gambar
pertamanya sama, mata membacanya sebagai satu template.

Semua CC0/public domain lewat Openverse: nol atribusi, nol share-alike, aman
ikut template yang dijual berulang.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POOL = os.path.join(ROOT, "assets", "photos", "pool")
SPEC = os.path.join(ROOT, "themes", "themes.json")
API = "https://api.openverse.org/v1/images/"
UA = "ikat-template/1.0 (https://github.com/nurhikam/ikat)"

# Tiap kategori dipakai untuk slot yang beda di undangan, jadi bentuknya beda.
# (query, jumlah, nama, rasio)
CATEGORIES = [
    ("wedding couple portrait",      14, "couple",  "3:4"),
    ("bride groom walking outdoor",  10, "walk",    "3:4"),
    ("wedding rings detail",          8, "ring",    "1:1"),
    ("bridal bouquet flowers",       10, "bloom",   "1:1"),
    ("wedding table decoration",      8, "table",   "4:3"),
    ("bride dress portrait",         10, "dress",   "3:4"),
    ("wedding venue arch outdoor",    8, "venue",   "4:3"),
    ("holding hands couple",          8, "hands",   "1:1"),
]

ASPECT_PX = {"3:4": (640, 854), "1:1": (600, 600), "4:3": (900, 675), "4:5": (700, 875)}

SKIP_SOURCES = {"wikimedia"}
SOURCE_RANK = {"stocksnap": 0, "nappy": 0, "flickr": 1, "rawpixel": 1}
ARCHIVAL = re.compile(
    r"unidentified|unknown|possibly|circa|\bc\.\s*1[89]|daguerre|carte de visite|"
    r"\bcdv\b|collection|negative|glass plate|[12][0-9]{3}s?\s*$", re.I)


def search(term: str, page_size: int = 40):
    qs = urllib.parse.urlencode({
        "q": term, "license": "cc0,pdm", "size": "large", "page_size": str(page_size)})
    req = urllib.request.Request(API + "?" + qs, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  ! {term}: {e}", file=sys.stderr)
        return []
    out = []
    for x in d.get("results") or []:
        src = (x.get("source") or "").lower()
        if src in SKIP_SOURCES or not x.get("url"):
            continue
        if (x.get("width") or 0) < 1100 or (x.get("height") or 0) < 750:
            continue
        if ARCHIVAL.search(x.get("title") or ""):
            continue
        out.append({"rank": SOURCE_RANK.get(src, 5), "url": x["url"],
                    "title": (x.get("title") or "untitled")[:60],
                    "license": f"{x.get('license','')} {x.get('license_version','')}".strip(),
                    "source": src, "page": x.get("foreign_landing_url", "")})
    out.sort(key=lambda c: c["rank"])
    return out


def grab(url: str, dest_tmp: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=90) as r, open(dest_tmp, "wb") as f:
            f.write(r.read())
        return os.path.getsize(dest_tmp) > 20000
    except Exception:
        return False


def convert(src: str, dest: str, aspect: str) -> bool:
    w, h = ASPECT_PX[aspect]
    vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf,
                        "-c:v", "libwebp", "-quality", "74", "-compression_level", "6", dest],
                       capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(dest)


# ------------------------------------------------------- sumber kedua: Commons
#
# SUDAH DICOBA 2026-09-02, DAN HASILNYA TIDAK BISA DIPAKAI. Jangan diaktifkan
# lagi tanpa memeriksa gambarnya satu per satu.
#
# Teorinya masuk akal: Commons selalu bisa diakses tanpa kunci, dan walaupun foto
# pernikahannya kebanyakan scan buku 1950-an, DETAIL (bunga, cincin, lilin,
# dedaunan) mestinya modern. Kenyataannya, setelah disaring ke PD/CC0 yang
# tersisa justru:
#
#   bloom -> lukisan still-life abad ke-17 (Bosschaert, Renoir, Daniels)
#   leaf  -> foto arsip hitam-putih perkebunan eucalyptus
#   ring  -> patung polikrom abad pertengahan yang memegang buku
#   cloth -> tekstur kain polos (kepakai sebagai TEKSTUR, bukan foto galeri)
#
# Penyebabnya struktural, bukan apes: yang jatuh ke public domain itu karya yang
# hak ciptanya sudah kedaluwarsa, jadi karya lama. Fotografi pernikahan modern
# yang benar-benar bebas ada di stok CC0 (Openverse/StockSnap/Pexels), bukan di
# Commons.
#
# Filter lisensinya sendiri sudah benar: CC BY-SA gugur bukan karena share-alike,
# tapi karena BY mewajibkan atribusi — dan undangan pernikahan tidak mungkin
# memuat kredit foto di bawah galerinya.

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
COMMONS_FREE = ("cc0", "public domain", "pd-", "no restrictions")

COMMONS_CATEGORIES = [
    ("bouquet roses flowers",     8, "bloom", "1:1"),
    ("eucalyptus leaves branch",  8, "leaf",  "1:1"),
    ("candle table setting",      6, "table", "4:3"),
    ("wedding ring detail",       4, "ring",  "1:1"),
    ("silk fabric texture",       8, "cloth", "4:3"),
]


def _strip(v: str) -> str:
    return re.sub(r"<[^>]+>", "", v or "").strip()


def search_commons(term: str, limit: int = 30):
    u = COMMONS_API + "?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": term + " filemime:image/jpeg", "gsrnamespace": "6",
        "gsrlimit": str(limit), "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "iiurlwidth": "1400"})
    try:
        req = urllib.request.Request(u, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  ! {term}: {e}", file=sys.stderr)
        return []
    out = []
    for p in ((d.get("query") or {}).get("pages") or {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata") or {}
        lic = _strip((em.get("LicenseShortName") or {}).get("value", "")).lower()
        w, h = ii.get("width") or 0, ii.get("height") or 0
        if not any(f in lic for f in COMMONS_FREE):
            continue
        if w < 1100 or h < 800 or not (0.5 <= w / h <= 2.2):
            continue
        if ARCHIVAL.search(p["title"]):
            continue
        out.append({"url": ii.get("thumburl") or ii.get("url"),
                    "title": p["title"].replace("File:", "")[:60],
                    "license": _strip((em.get("LicenseShortName") or {}).get("value", "")),
                    "source": "wikimedia", "page": ii.get("descriptionurl", "")})
    return out


def fetch_commons(credits: list, seen: set) -> list:
    tmp = os.path.join(POOL, ".tmp")
    for query, want, name, aspect in COMMONS_CATEGORIES:
        cands = search_commons(query)
        print(f"{name:8s} <- commons: {query:28s} {len(cands)} PD/CC0", file=sys.stderr)
        got = 0
        for c in cands:
            if got >= want:
                break
            if not c["url"] or c["url"] in seen:
                continue
            seen.add(c["url"])
            if not grab(c["url"], tmp):
                continue
            fn = f"{name}-c{got+1:02d}.webp"
            if not convert(tmp, os.path.join(POOL, fn), aspect):
                continue
            credits.append({"file": fn, "aspect": aspect, "cat": name,
                            **{k: c[k] for k in ("title", "license", "source", "page")}})
            got += 1
        print(f"         -> {got}/{want}", file=sys.stderr)
    if os.path.exists(tmp):
        os.remove(tmp)
    return credits


def fetch_pool() -> list:
    os.makedirs(POOL, exist_ok=True)
    tmp = os.path.join(POOL, ".tmp")
    credits, seen = [], set()

    for query, want, name, aspect in CATEGORIES:
        cands = search(query)
        print(f"{name:8s} <- {query:32s} {len(cands)} kandidat", file=sys.stderr)
        got = 0
        for c in cands:
            if got >= want:
                break
            if c["url"] in seen:
                continue
            seen.add(c["url"])
            if not grab(c["url"], tmp):
                continue
            dest = os.path.join(POOL, f"{name}-{got+1:02d}.webp")
            if not convert(tmp, dest, aspect):
                continue
            credits.append({"file": f"{name}-{got+1:02d}.webp", "aspect": aspect,
                            "cat": name, **{k: c[k] for k in ("title", "license", "source", "page")}})
            got += 1
        print(f"         -> {got}/{want}", file=sys.stderr)

    if os.path.exists(tmp):
        os.remove(tmp)

    # credits = fetch_commons(credits, seen)   # lihat catatan di atas

    with open(os.path.join(POOL, "pool.json"), "w", encoding="utf-8") as f:
        json.dump(credits, f, ensure_ascii=False, indent=2)

    with open(os.path.join(POOL, "CREDITS.md"), "w", encoding="utf-8") as f:
        f.write("# Kolam foto contoh\n\nPlaceholder demo, semuanya CC0 / public domain lewat "
                "Openverse. Nol kewajiban atribusi dan nol share-alike, jadi aman ikut template "
                "yang dijual. Sumber dicatat sebagai jejak asal-usul, bukan karena lisensinya "
                "menuntut.\n\n| Berkas | Judul | Lisensi | Sumber |\n|---|---|---|---|\n")
        for c in credits:
            f.write(f"| `{c['file']}` | [{c['title'].replace('|','-')}]({c['page']}) | "
                    f"{c['license'].upper()} | {c['source']} |\n")
    return credits


def assign() -> None:
    """Bagikan set foto per tema, deterministik dari slug.

    Deterministik penting: tema yang sama selalu dapat foto yang sama, jadi
    regenerate nggak bikin galeri berubah-ubah dan diff-nya tetap kecil."""
    # Dua sumber digabung PER KATEGORI, bukan pilih salah satu. Openverse punya
    # foto pasangan tapi sering menolak; Commons selalu bisa tapi cuma bagus
    # untuk detail. Kalau dipilih all-or-nothing, satu sumber yang gagal bikin
    # slot sampul kosong dan semua tema balik seragam.
    by_cat = {}

    def add(cat, ref):
        by_cat.setdefault(cat, [])
        if ref not in by_cat[cat]:
            by_cat[cat].append(ref)

    pj = os.path.join(POOL, "pool.json")
    if os.path.exists(pj):
        for c in json.load(open(pj, encoding="utf-8")):
            add(c["cat"], "assets/photos/pool/" + c["file"])

    legacy = os.path.join(ROOT, "assets", "photos")
    have = {f for f in os.listdir(legacy) if f.endswith(".webp")}
    LEGACY = {
        "couple": ["cover.webp", "gallery-3.webp", "gallery-2.webp", "closing.webp"],
        "walk":   ["closing.webp", "gallery-2.webp", "gallery-1.webp", "cover.webp"],
        "ring":   ["gallery-4.webp", "groom.webp", "bride.webp"],
        "bloom":  ["bride.webp", "gallery-4.webp"],
        "dress":  ["gallery-3.webp", "cover.webp", "gallery-1.webp"],
        "table":  ["groom.webp", "gallery-4.webp"],
        "venue":  ["gallery-2.webp", "closing.webp", "gallery-1.webp"],
        "hands":  ["bride.webp", "cover.webp", "gallery-4.webp"],
    }
    for cat, names in LEGACY.items():
        for n in names:
            if n in have:
                add(cat, "assets/photos/" + n)

    if not by_cat:
        sys.exit("nggak ada foto sama sekali")

    spec = json.load(open(SPEC, encoding="utf-8"))
    for t in spec["themes"]:
        seed = int(hashlib.sha256(t["slug"].encode()).hexdigest()[:8], 16)

        def pick(cat, offset=0):
            lst = by_cat.get(cat) or []
            return lst[(seed + offset) % len(lst)] if lst else ""

        cover = pick("couple", 0)
        closing = pick("walk", 1)

        # Galeri: permutasi, bukan pilihan per kategori.
        #
        # Kategori itu daftar pendek (2-4 foto), jadi memilih satu per kategori
        # cuma menghasilkan 6 set berbeda untuk 113 tema. Mengurutkan ulang
        # seluruh kolam per tema jauh lebih murah dan jauh lebih bervariasi:
        # foto yang sama, susunan yang berbeda — dan karena tiap tema juga punya
        # layout galeri yang berbeda, hasil akhirnya terbaca beda.
        every = sorted({ref for lst in by_cat.values() for ref in lst})
        rot = seed % len(every)
        ordered = every[rot:] + every[:rot]
        step = 1 + (seed >> 8) % max(1, len(every) - 1)
        picked, i = [], 0
        while len(picked) < min(6, len(ordered)):
            ref = ordered[(i * step) % len(ordered)]
            if ref not in picked:
                picked.append(ref)
            i += 1
            if i > len(ordered) * 3:
                break
        # Sampul jangan diulang di galeri kalau masih ada pilihan lain.
        if cover in picked and len(every) > len(picked):
            spare = [r for r in ordered if r not in picked and r != cover]
            if spare:
                picked[picked.index(cover)] = spare[0]

        t["photos"] = {"cover": cover, "closing": closing, "gallery": picked}

    with open(SPEC, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
        f.write("\n")

    covers = len({t["photos"]["cover"] for t in spec["themes"]})
    print(f"{len(spec['themes'])} tema dapat set foto | sampul unik: {covers}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assign", action="store_true", help="assign ulang tanpa unduh")
    a = ap.parse_args()
    if not a.assign:
        if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode != 0:
            sys.exit("butuh ffmpeg di PATH")
        got = fetch_pool()
        total = sum(os.path.getsize(os.path.join(POOL, x))
                    for x in os.listdir(POOL) if x.endswith(".webp"))
        print(f"\n{len(got)} foto, {total/1024:.0f} KB -> assets/photos/pool/")
    assign()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
