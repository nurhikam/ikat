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
    by_cat, prefix = {}, "assets/photos/pool/"
    pj = os.path.join(POOL, "pool.json")
    if os.path.exists(pj):
        for c in json.load(open(pj, encoding="utf-8")):
            by_cat.setdefault(c["cat"], []).append(c["file"])

    if not by_cat:
        # Cadangan: kolam belum keunduh (Openverse lagi nolak). Delapan foto lama
        # tetap dipakai, tapi dirotasi. Empat di antaranya cukup kuat jadi sampul,
        # jadi keseragaman sampul turun dari 1 foto ke 4 tanpa jaringan sama sekali.
        legacy = os.path.join(ROOT, "assets", "photos")
        have = {f for f in os.listdir(legacy) if f.endswith(".webp")}
        pick_from = lambda names: [n for n in names if n in have]
        by_cat = {
            "couple": pick_from(["cover.webp", "gallery-3.webp", "gallery-2.webp", "closing.webp"]),
            "walk":   pick_from(["closing.webp", "gallery-2.webp", "gallery-1.webp", "cover.webp"]),
            "ring":   pick_from(["gallery-4.webp", "groom.webp", "bride.webp"]),
            "bloom":  pick_from(["bride.webp", "gallery-4.webp", "groom.webp"]),
            "dress":  pick_from(["gallery-3.webp", "cover.webp", "gallery-1.webp"]),
            "table":  pick_from(["groom.webp", "gallery-4.webp", "bride.webp"]),
            "venue":  pick_from(["gallery-2.webp", "closing.webp", "gallery-1.webp"]),
            "hands":  pick_from(["bride.webp", "cover.webp", "gallery-4.webp"]),
        }
        by_cat = {k: v for k, v in by_cat.items() if v}
        prefix = "assets/photos/"
        if not by_cat:
            sys.exit("nggak ada foto sama sekali di assets/photos/")
        print("kolam belum ada -> pakai 8 foto lama, dirotasi", file=sys.stderr)

    spec = json.load(open(SPEC, encoding="utf-8"))
    for t in spec["themes"]:
        seed = int(hashlib.sha256(t["slug"].encode()).hexdigest()[:8], 16)

        def pick(cat, offset=0):
            lst = by_cat.get(cat) or []
            return (prefix + lst[(seed + offset) % len(lst)]) if lst else ""

        t["photos"] = {
            "cover":   pick("couple", 0),
            "closing": pick("walk", 1),
            "gallery": [pick("ring", 2), pick("bloom", 3), pick("dress", 4),
                        pick("table", 5), pick("venue", 6), pick("hands", 7)],
        }

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
