#!/usr/bin/env python3
"""Fetch CC0 sample wedding photos for the demo invitation.

    ./bin/fetch-sample-photos.py

Sample imagery in a template that gets sold has the same problem the music
does: a pretty picture off an image search is somebody's copyrighted work, and
it then ships to every client. These come from Openverse filtered to **CC0 and
public domain only** — no attribution obligation, no share-alike, nothing to
strip before a template is sold.

(Wikimedia Commons was the obvious first stop and the wrong one: its freely
licensed wedding photography is almost entirely 1950s halftone book scans.
Correct licence, museum-archive look.)

These are placeholders. A real invitation uses the couple's own photographs —
this only makes the demo read as an invitation rather than a wireframe.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "photos")
API = "https://api.openverse.org/v1/images/"
UA = "undangan-template/1.0 (https://github.com/nurhikam/undangan)"

QUERIES = [
    "wedding couple",
    "bride groom portrait",
    "wedding ceremony",
    "bridal bouquet",
    "wedding rings",
    "wedding reception table",
    "wedding dress bride",
]

# Openverse aggregates Wikimedia too; skip it for the reason in the docstring.
SKIP_SOURCES = {"wikimedia"}

# Modern CC0 stock first. The rest of the CC0 pool is largely museum and
# library scans — correctly licensed, and visibly Victorian.
SOURCE_RANK = {"stocksnap": 0, "flickr": 1, "rawpixel": 1, "nappy": 0, "sciencemuseum": 9}

ARCHIVAL = re.compile(
    r"unidentified|unknown|possibly|circa|\bc\.\s*1[89]|daguerre|carte de visite|"
    r"\bcdv\b|album|collection|negative|glass plate|studio portrait|"
    r"[12][0-9]{3}s?\s*$", re.I)

# slot name -> crop aspect
WANTED = [
    ("cover", "3:4"),
    ("bride", "1:1"),
    ("groom", "1:1"),
    ("gallery-1", "4:3"),
    ("gallery-2", "3:4"),
    ("gallery-3", "3:4"),
    ("gallery-4", "3:4"),
    ("closing", "4:5"),
]

ASPECT_PX = {
    "3:4": (600, 800),
    "1:1": (560, 560),
    "4:3": (900, 675),
    "4:5": (700, 875),
}


def search(term: str, page_size: int = 20):
    qs = urllib.parse.urlencode({
        "q": term,
        "license": "cc0,pdm",     # no attribution, no share-alike
        "size": "large",
        "page_size": str(page_size),
    })
    req = urllib.request.Request(API + "?" + qs, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            d = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  ! {term}: {e}", file=sys.stderr)
        return []

    out = []
    for r_ in d.get("results") or []:
        src = (r_.get("source") or "").lower()
        if src in SKIP_SOURCES:
            continue
        w, h = r_.get("width") or 0, r_.get("height") or 0
        if w < 1200 or h < 800:
            continue
        if not r_.get("url"):
            continue
        if ARCHIVAL.search(r_.get("title") or ""):
            continue
        out.append({
            "rank": SOURCE_RANK.get(src, 5),
            "title": (r_.get("title") or "untitled")[:60],
            "url": r_["url"],
            "license": f"{r_.get('license', '')} {r_.get('license_version', '')}".strip(),
            "source": r_.get("source", ""),
            "page": r_.get("foreign_landing_url", ""),
        })
    return out


def download(url: str, dest: str) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=90) as r, open(dest, "wb") as f:
            f.write(r.read())
        return os.path.getsize(dest) > 20000
    except Exception as e:
        print(f"  ! unduh gagal: {str(e)[:70]}", file=sys.stderr)
        return False


def convert(src: str, dest: str, aspect: str) -> bool:
    w, h = ASPECT_PX[aspect]
    vf = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf,
         "-c:v", "libwebp", "-quality", "78", "-compression_level", "6", dest],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ! ffmpeg: {r.stderr.strip()[:120]}", file=sys.stderr)
        return False
    return os.path.exists(dest)


def main() -> int:
    if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode != 0:
        sys.exit("butuh ffmpeg di PATH")
    os.makedirs(OUT, exist_ok=True)

    pool, seen = [], set()
    for q in QUERIES:
        hits = search(q)
        print(f"cari: {q:28s} -> {len(hits)}", file=sys.stderr)
        for c in hits:
            if c["url"] in seen:
                continue
            seen.add(c["url"])
            pool.append(c)
    pool.sort(key=lambda c: c["rank"])
    print(f"\nkandidat CC0/PDM: {len(pool)}\n", file=sys.stderr)

    if not pool:
        sys.exit("tidak ada kandidat — API mungkin sedang membatasi laju")

    credits, used = [], 0
    tmp = os.path.join(OUT, ".tmp")
    for name, aspect in WANTED:
        while used < len(pool):
            cand = pool[used]
            used += 1
            if not download(cand["url"], tmp):
                continue
            dest = os.path.join(OUT, f"{name}.webp")
            if not convert(tmp, dest, aspect):
                continue
            kb = os.path.getsize(dest) / 1024
            print(f"{name+'.webp':16s} {aspect:4s} {kb:5.0f} KB  <- {cand['title']}")
            credits.append((f"{name}.webp", cand))
            break

    if os.path.exists(tmp):
        os.remove(tmp)

    with open(os.path.join(OUT, "CREDITS.md"), "w", encoding="utf-8") as f:
        f.write("# Kredit foto contoh\n\n")
        f.write("Placeholder demo. Undangan sungguhan memakai foto milik pasangan sendiri.\n\n")
        f.write("Diambil lewat `bin/fetch-sample-photos.py` dari Openverse, disaring ke\n")
        f.write("**CC0 / public domain** — tanpa kewajiban atribusi dan tanpa share-alike,\n")
        f.write("jadi aman ikut dalam template yang dijual. Sumber tetap dicatat di bawah\n")
        f.write("sebagai catatan asal-usul, bukan karena lisensinya menuntut.\n\n")
        f.write("| Berkas | Judul | Lisensi | Sumber |\n|---|---|---|---|\n")
        for fn, c in credits:
            t = c["title"].replace("|", "-")
            f.write(f"| `{fn}` | [{t}]({c['page']}) | {c['license'].upper()} | {c['source']} |\n")

    total = sum(os.path.getsize(os.path.join(OUT, x))
                for x in os.listdir(OUT) if x.endswith(".webp"))
    print(f"\n{len(credits)} foto, total {total/1024:.0f} KB -> assets/photos/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
