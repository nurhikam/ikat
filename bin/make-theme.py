#!/usr/bin/env python3
"""Render themes/<slug>/theme.css from themes/themes.json.

    ./bin/make-theme.py            # semua tema
    ./bin/make-theme.py butter     # satu tema

Kenapa digenerate: blok token tiap tema itu ~80% struktur yang sama — nama
variabel, urutan, komentar. Nulis tangan 11 kali artinya 11 kesempatan buat
drift, dan tema ke-12 jadi mahal. Yang bikin tema punya karakter cuma blok
dekorasinya, dan itu tetap ditulis tangan di themes/<slug>/decoration.css.

Efek sampingnya yang paling berguna: ini bukti klaim arsitekturnya. Kalau tema
beneran cuma token, tema baru = satu entri JSON + (opsional) satu file dekorasi,
tanpa nyentuh engine sama sekali.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme_layouts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(ROOT, "themes", "themes.json")


# --------------------------------------------------------------- pola latar
# SVG data-URI, di-inline. Nol file raster: undangan dibuka di parkiran gedung
# dengan sinyal satu bar, dan itu satu-satunya kondisi pakai yang penting.

def _svg(body: str, w: int = 80, h: int = 80) -> str:
    raw = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' "
           f"viewBox='0 0 {w} {h}'>{body}</svg>")
    return 'url("data:image/svg+xml,' + urllib.parse.quote(raw, safe="") + '")'


def pattern(kind: str, ink: str) -> str:
    c = urllib.parse.quote(ink, safe="")
    if kind == "dots":
        return _svg(f"<circle cx='20' cy='20' r='2' fill='{ink}' fill-opacity='.10'/>"
                    f"<circle cx='60' cy='60' r='2' fill='{ink}' fill-opacity='.10'/>", 80, 80)
    if kind == "grid":
        return _svg(f"<path d='M0 40h80M40 0v80' stroke='{ink}' stroke-opacity='.07' stroke-width='1'/>", 80, 80)
    if kind == "arcs":
        return _svg(f"<path d='M0 80a40 40 0 0 1 80 0' fill='none' stroke='{ink}' "
                    f"stroke-opacity='.09' stroke-width='1.2'/>", 80, 80)
    if kind == "waves":
        return _svg(f"<path d='M0 40q20-16 40 0t40 0' fill='none' stroke='{ink}' "
                    f"stroke-opacity='.09' stroke-width='1.2'/>", 80, 80)
    if kind == "chevron":
        return _svg(f"<path d='M0 50 20 30 40 50 60 30 80 50' fill='none' stroke='{ink}' "
                    f"stroke-opacity='.08' stroke-width='1.4'/>", 80, 80)
    if kind == "petals":
        return _svg(f"<g fill='none' stroke='{ink}' stroke-opacity='.09' stroke-width='1.1'>"
                    f"<path d='M40 14c9 10 9 22 0 32-9-10-9-22 0-32z'/>"
                    f"<path d='M14 40c10 9 22 9 32 0-10-9-22-9-32 0z'/></g>", 80, 80)
    if kind == "stars":
        return _svg(f"<g fill='{ink}' fill-opacity='.12'>"
                    f"<path d='M20 12l2 6 6 2-6 2-2 6-2-6-6-2 6-2z'/>"
                    f"<path d='M58 50l1.5 4.5L64 56l-4.5 1.5L58 62l-1.5-4.5L52 56l4.5-1.5z'/></g>", 80, 80)
    if kind == "grain":
        # Bintik risograph: kecil dan rapat. Titik gede jadinya kelihatan kayak
        # blob nyasar, bukan tekstur cetak.
        dots = [(3, 5, .9), (11, 14, .6), (19, 4, .8), (27, 17, .7), (7, 24, .75),
                (23, 29, .6), (15, 33, .85), (31, 8, .65), (35, 26, .7), (1, 34, .6)]
        g = "".join(f"<circle cx='{x}' cy='{y}' r='{r}'/>" for x, y, r in dots)
        return _svg(f"<g fill='{ink}' fill-opacity='.22'>{g}</g>", 38, 38)
    if kind == "ikat":
        # motif tenun ikat: berlian bergerigi, khas ikat Nusantara — ini asal namanya
        return _svg(f"<g fill='none' stroke='{ink}' stroke-opacity='.10' stroke-width='1.2'>"
                    f"<path d='M40 8 56 24 40 40 24 24z'/>"
                    f"<path d='M40 40 56 56 40 72 24 56z'/>"
                    f"<path d='M32 16h4M44 16h4M32 64h4M44 64h4'/></g>", 80, 80)
    return "none"


def ambient(accent: str, mood: str) -> str:
    """Cahaya lembut yang di-tile per tinggi viewport (engine yang atur ukurannya).

    Tidak ada gradient yang di-anchor ke 0% atau 100%: gradient yang mulai persis
    di tepi tile bikin garis sambungan horizontal yang kelihatan waktu di-scroll.
    Semuanya ditaruh di tengah-tengah dengan falloff yang habis sebelum tepi.
    """
    if mood == "unik":
        return (f"radial-gradient(ellipse 76% 26% at 50% 22%, {accent}1c, transparent 68%),"
                f"radial-gradient(ellipse 58% 22% at 88% 72%, {accent}12, transparent 66%)")
    return (f"radial-gradient(ellipse 74% 26% at 50% 20%, {accent}22, transparent 68%),"
            f"radial-gradient(ellipse 58% 24% at 10% 52%, {accent}16, transparent 66%),"
            f"radial-gradient(ellipse 54% 22% at 92% 78%, {accent}12, transparent 66%)")


# ------------------------------------------------------------------ render

def font_query(fonts: dict) -> str:
    fams = []
    for key in ("display", "heading", "body"):
        v = fonts.get(key)
        if v and v not in fams:
            fams.append(v)
    fams.append("Amiri")
    q = "&".join("family=" + f.replace(" ", "+") for f in fams)
    return f"https://fonts.googleapis.com/css2?{q}&display=swap"



def duotone(accent: str) -> str:
    """Duotone CSS dari warna aksen tema.

    grayscale -> sepia menaruh gambar di sekitar hue 35deg; rotasi selisihnya
    memindahkan seluruh gambar ke hue tema. Hasilnya foto yang sama terbaca
    menyatu dengan paletnya, bukan tempelan."""
    import colorsys
    h = accent.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hue = colorsys.rgb_to_hls(r, g, b)[0] * 360
    return (f"filter: grayscale(1) sepia(1) hue-rotate({round(hue - 35)}deg) "
            f"saturate(1.9) contrast(1.05);")


def photo_filter(t: dict) -> str:
    kind = (t.get("layout") or {}).get("photo", "natural")
    if kind == "duotone":
        return duotone(t["colors"]["accent"])
    return theme_layouts.PHOTO.get(kind) or ""


def render(t: dict) -> str:
    c, s, f = t["colors"], t["shape"], t["fonts"]
    pat = pattern(t.get("pattern", "none"), c["ink"])
    amb = ambient(c["accent"], t.get("mood", "pastel"))

    out = f"""/*! Ikat theme: {t['name']} — {t['blurb']}
 *
 * DIGENERATE oleh bin/make-theme.py dari themes/themes.json.
 * Jangan edit file ini langsung — edit spec-nya, atau
 * themes/{t['slug']}/decoration.css buat bagian yang butuh tangan.
 */

@import url("{font_query(f)}");

:root {{
  /* warna */
  --u-bg: {c['bg']};
  --u-bg-2: {c['bg2']};
  --u-surface: {c['surface']};
  --u-surface-2: {c['surface2']};
  --u-ink: {c['ink']};
  --u-ink-soft: {c['inkSoft']};
  --u-ink-invert: {c['inkInvert']};
  --u-accent: {c['accent']};
  --u-accent-ink: {c['accentInk']};
  --u-highlight: {c['highlight']};
  --u-line: {c['line']};
  --u-line-invert: {c['lineInvert']};

  /* tipografi */
  --u-font-display: {f['displayStack']};
  --u-font-heading: {f['headingStack']};
  --u-font-body: {f['bodyStack']};
  --u-font-arabic: "Amiri", "Traditional Arabic", serif;
  --u-tracking-caps: {t.get('tracking', '0.24em')};

  /* bentuk */
  --u-radius: {s['radius']};
  --u-radius-lg: {s['radiusLg']};
  --u-frame-radius: {s['frameRadius']};
  --u-frame-border: {s['frameBorder']};
  --u-avatar-radius: {s['avatarRadius']};
  --u-photo-radius: {s['photoRadius']};
  --u-pill-radius: {s['pillRadius']};
  --u-polaroid-tilt: {s['polaroidTilt']};
  --u-shadow: {s['shadow']};

  /* latar */
  --u-texture: {pat};
  --u-ambient: {amb};
"""
    if t.get("ornTop"):
        out += f"  --u-orn-top: {t['ornTop']};\n"
        out += f"  --u-orn-bottom: {t.get('ornBottom', t['ornTop'])};\n"
        out += f"  --u-orn-size: {t.get('ornSize', '30px')};\n"
    out += "}\n"

    lay = theme_layouts.css(t.get("layout") or {})
    if lay:
        out += ("\n/* ------------------------------------------------- layout (dari spec) */\n"
                + lay + "\n")

    deco = os.path.join(ROOT, "themes", t["slug"], "decoration.css")
    if os.path.exists(deco):
        with open(deco, encoding="utf-8") as fh:
            out += "\n/* --------------------------------------------- dekorasi (ditulis tangan) */\n"
            out += fh.read().rstrip() + "\n"

    # Komposisi sampul dan gradasi foto sengaja DI BAWAH dekorasi. Family cover
    # lama mengunci tinggi bingkai dengan !important, jadi apa pun yang ditaruh
    # di atasnya kalah. Yang di bawah ini memang dimaksudkan menggantikannya.
    cov = theme_layouts.COVER.get((t.get("layout") or {}).get("cover", "keep")) or ""
    pf = photo_filter(t)
    if cov or pf:
        out += "\n/* ------------------------------------ komposisi sampul + gradasi foto */\n"
        if pf:
            out += f".u-photo {{ {pf} }}\n"
        if cov:
            out += cov.rstrip() + "\n"
    return out


def main() -> int:
    with open(SPEC, encoding="utf-8") as fh:
        themes = json.load(fh)["themes"]

    only = sys.argv[1] if len(sys.argv) > 1 else None
    n = 0
    for t in themes:
        if only and t["slug"] != only:
            continue
        d = os.path.join(ROOT, "themes", t["slug"])
        os.makedirs(d, exist_ok=True)
        css = render(t)
        with open(os.path.join(d, "theme.css"), "w", encoding="utf-8") as fh:
            fh.write(css)
        has_deco = os.path.exists(os.path.join(d, "decoration.css"))
        print(f"  {t['slug']:16s} {len(css)/1024:5.1f} KB  {t['name']}"
              f"{'  + dekorasi' if has_deco else ''}")
        n += 1

    if only and n == 0:
        sys.exit(f"tema '{only}' tidak ada di themes.json")
    print(f"\n{n} tema dirender")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
