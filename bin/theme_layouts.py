"""Varian layout per section, dipakai bin/make-theme.py.

Kenapa ada file ini: sampai sekarang tema cuma mengubah warna, font, dan bentuk
sampul. Diukur di 8 tema yang paling beda-beda, hasilnya urutan section identik,
kolom galeri identik (166px 166px di semuanya), dan tinggi section cuma beda
karena metrik font. Jadi 113 tema itu, di bawah sampulnya, satu template.

Warna nggak akan pernah menutupi itu. Yang bikin dua undangan terasa beda itu
**struktur**: berapa kolom galerinya, mempelainya ditumpuk atau dibelah, kartunya
punya kotak atau cuma garis. Di sinilah variasi itu tinggal, sebagai nilai spec
yang bisa dipasang-pasangkan, bukan file yang ditulis satu per satu.

Semua tetap di lapis tema. Nol perubahan di engine.js.
"""

# --------------------------------------------------------------------- galeri
#
# Setiap varian yang mengubah model kolom WAJIB me-reset
# `.u-gallery__item:first-child { grid-column: auto }`. Engine memberi item
# pertama `span 2` supaya jadi hero di grid 2 kolom bawaan; kalau span itu
# dibiarkan sementara kolomnya diganti jadi satu, grid bikin kolom implisit dan
# tata letaknya rusak (terukur: `34px 290.406px`, satu thumbnail mengkerut jadi
# 29px). Kena tiga varian sekaligus sebelum ketahuan.

GALLERY = {
    "duo": "",  # bawaan engine: 2 kolom, item pertama melebar

    "trio": """
.u-gallery__grid { grid-template-columns: repeat(3, 1fr); gap: 0.4rem; }
.u-gallery__item:first-child { grid-column: span 3; }
.u-gallery__photo { aspect-ratio: 1; }
.u-gallery__item:first-child .u-gallery__photo { aspect-ratio: 16 / 10; }
.u-gallery__cap { font-size: 0.62rem; }
""",

    "masonry": """
.u-gallery__grid { display: block; column-count: 2; column-gap: 0.6rem; }
.u-gallery__item:first-child { grid-column: auto; }
.u-gallery__item { break-inside: avoid; margin-bottom: 0.6rem; }
.u-gallery__photo { aspect-ratio: 3 / 4; }
.u-gallery__item:nth-child(3n+1) .u-gallery__photo { aspect-ratio: 1; }
.u-gallery__item:nth-child(3n+2) .u-gallery__photo { aspect-ratio: 4 / 5; }
""",

    "filmstrip": """
.u-gallery__grid {
  display: flex; gap: 0.6rem; overflow-x: auto; scroll-snap-type: x mandatory;
  margin-inline: calc(var(--u-gutter) * -1); padding: 0 var(--u-gutter) 0.5rem;
  scrollbar-width: none;
}
.u-gallery__grid::-webkit-scrollbar { display: none; }
.u-gallery__item:first-child { grid-column: auto; }
.u-gallery__item { flex: 0 0 68%; scroll-snap-align: center; }
.u-gallery__photo { aspect-ratio: 3 / 4; }
""",

    "stack": """
.u-gallery__grid { grid-template-columns: 1fr; gap: 1.1rem; }
.u-gallery__item:first-child { grid-column: auto; }
.u-gallery__photo { aspect-ratio: 4 / 3; }
.u-gallery__item:nth-child(even) { margin-inline-start: 14%; }
.u-gallery__item:nth-child(odd) { margin-inline-end: 14%; }
.u-gallery__item:first-child { margin-inline: 0; }
.u-gallery__item:first-child .u-gallery__photo { aspect-ratio: 3 / 4; }
""",

    "mosaic": """
.u-gallery__grid { grid-template-columns: repeat(4, 1fr); gap: 0.45rem; }
.u-gallery__item { grid-column: span 2; }
.u-gallery__item:first-child { grid-column: span 4; }
.u-gallery__photo { aspect-ratio: 1; }
.u-gallery__item:first-child .u-gallery__photo { aspect-ratio: 16 / 11; }
.u-gallery__item:nth-child(4) { grid-column: span 4; }
.u-gallery__item:nth-child(4) .u-gallery__photo { aspect-ratio: 2 / 1; }
""",
}

# -------------------------------------------------------------------- couple

COUPLE = {
    "stacked": "",  # bawaan: dua-duanya tengah

    "split": """
.u-couple__card { text-align: start; }
.u-person--bride { align-items: flex-start; text-align: start; }
.u-person--groom { align-items: flex-end; text-align: end; }
.u-couple__amp { align-self: center; }
.u-couple__greeting, .u-couple__intro { text-align: center; }
""",

    "offset": """
.u-person--bride { align-items: flex-start; text-align: start; margin-inline-end: 16%; }
.u-person--groom { align-items: flex-end; text-align: end; margin-inline-start: 16%; margin-top: -1rem; }
.u-couple__amp { margin-block: 0.75rem; }
.u-couple__greeting, .u-couple__intro { text-align: center; }
""",

    "framed": """
.u-person {
  border: 1px solid var(--u-line);
  border-radius: var(--u-radius);
  padding: 1.5rem 1rem 1.25rem;
}
.u-couple__amp { margin-block: 1rem; }
""",
}

# --------------------------------------------------------------------- event

EVENT = {
    "centered": "",  # bawaan

    "split": """
@media (min-width: 24rem) {
  .u-event__inner {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 0.5rem 1.25rem; text-align: start; align-items: start;
  }
  .u-event__heading { grid-column: 1 / -1; text-align: start; }
  .u-event__month  { grid-column: 1; margin-bottom: 0; }
  .u-week          { grid-column: 1 / -1; }
  .u-event__meta   { grid-column: 1 / -1; }
  .u-event__maps, .u-event__cal { justify-self: start; }
}
""",

    "ticket": """
/* Kartu tiket: permukaan terang dengan takik di kiri-kanan, seperti karcis. */
.u-event__inner {
  background: var(--u-surface);
  color: var(--u-ink);
  padding: 1.75rem 1.35rem;
  border-radius: var(--u-radius-lg);
  position: relative;
}
.u-event__inner::before,
.u-event__inner::after {
  content: ""; position: absolute; top: 52%;
  width: 22px; height: 22px; border-radius: 50%;
  background: var(--u-bg); transform: translateY(-50%);
}
.u-event__inner::before { left: -11px; }
.u-event__inner::after  { right: -11px; }
.u-event__dt { color: var(--u-ink-soft); }
.u-week__dow { color: var(--u-ink); }
.u-event__maps, .u-event__cal { color: var(--u-ink); border-color: var(--u-line); }
""",

    "plain": """
.u-event__inner {
  border-top: 1px solid var(--u-line-invert);
  border-bottom: 1px solid var(--u-line-invert);
  padding-block: 2rem;
}
.u-event__month { font-size: clamp(1.5rem, 7vw, 2.1rem); }
""",
}

# ---------------------------------------------------------------------- kartu

CARD = {
    "boxed": "",  # bawaan: permukaan terang + radius

    "bleed": """
.u-card {
  border-radius: 0;
  margin-inline: calc(var(--u-gutter) * -1);
  padding-inline: calc(var(--u-gutter) + 0.25rem);
}
""",

    # Kartu dilepas jadi cuma garis. RSVP sengaja dikecualikan: form-nya butuh
    # permukaan terang supaya kontras label dan input tetap lolos WCAG.
    "edge": """
.u-card:not(.u-rsvp__card) {
  background: transparent;
  color: var(--u-ink-invert);
  box-shadow: none;
  border-radius: 0;
  border-top: 1px solid var(--u-line-invert);
  border-bottom: 1px solid var(--u-line-invert);
  padding-inline: 0;
}
.u-card:not(.u-rsvp__card) .u-quote__cite,
.u-card:not(.u-rsvp__card) .u-person__parents,
.u-card:not(.u-rsvp__card) .u-person__ig { color: var(--u-ink-invert); opacity: 0.7; }
.u-card:not(.u-rsvp__card) .u-person__ig { box-shadow: inset 0 -1px 0 var(--u-line-invert); }
""",
}

ORDER = ["gallery", "couple", "event", "card"]
TABLES = {"gallery": GALLERY, "couple": COUPLE, "event": EVENT, "card": CARD}
KEYS = {k: list(v.keys()) for k, v in TABLES.items()}


def css(layout: dict) -> str:
    """Rangkai CSS dari pilihan varian. Varian yang tidak dikenal dilewati diam-diam
    supaya spec yang salah ketik tidak mematikan seluruh tema."""
    out = []
    for slot in ORDER:
        name = (layout or {}).get(slot)
        block = TABLES[slot].get(name)
        if block:
            out.append(f"/* layout.{slot} = {name} */{block.rstrip()}")
    return "\n\n".join(out)


def spread(index: int) -> dict:
    """Bagi varian merata lewat indeks tema.

    Pakai bilangan prima yang berbeda per slot supaya kombinasinya tidak
    berulang dalam siklus pendek: kalau semua slot maju bersamaan, tema ke-7 dan
    ke-14 bisa dapat kombinasi identik."""
    return {
        "gallery": KEYS["gallery"][index % len(KEYS["gallery"])],
        "couple":  KEYS["couple"][(index // 2) % len(KEYS["couple"])],
        "event":   KEYS["event"][(index // 3) % len(KEYS["event"])],
        "card":    KEYS["card"][(index // 5) % len(KEYS["card"])],
    }
