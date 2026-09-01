#!/usr/bin/env python3
"""Bundle one invitation into a single self-contained HTML file.

    ./bin/build-single.py data/demo.json -o dist/demo.html

Why this exists: a single file can be emailed to a client, opened from a USB
stick, or dropped on any host with no build step and no directory layout to get
wrong. It is also the artefact to hand over when a client wants to keep the
invitation after the event.

    --fragment   emit only <title>/<link>/<style>/markup/<script>, with no
                 <!doctype>/<html>/<head>/<body> wrapper — for embedding in a
                 host page that supplies its own document skeleton.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMPORT_RE = re.compile(r'@import\s+url\(\s*["\']?([^"\')]+)["\']?\s*\)\s*;', re.I)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def split_imports(css: str):
    """CSS @import is only legal at the top of a stylesheet, so concatenating
    two files would silently kill the second one's font imports. Pull them out
    and emit them as <link> instead — which also lets them download in
    parallel rather than after the CSS is parsed."""
    urls = IMPORT_RE.findall(css)
    return IMPORT_RE.sub("", css), urls


def guard(text: str) -> str:
    """Keep a literal </script> in the data from ending the script element."""
    return text.replace("</", "<\\/")


def build(data_path: str, fragment: bool = False, title: str | None = None) -> str:
    cfg = json.loads(read(data_path))
    theme = cfg.get("theme", "forest-lace")

    theme_css_path = os.path.join(ROOT, "themes", theme, "theme.css")
    if not os.path.exists(theme_css_path):
        sys.exit(f"tema '{theme}' tidak ada: {theme_css_path}")

    engine_css, imports_a = split_imports(read(os.path.join(ROOT, "engine", "engine.css")))
    theme_css, imports_b = split_imports(read(theme_css_path))
    engine_js = read(os.path.join(ROOT, "engine", "engine.js"))

    links = "\n".join(
        f'<link rel="stylesheet" href="{u}">'
        for u in dict.fromkeys(imports_a + imports_b)   # de-dup, keep order
    )
    # The static tag names the file in a tab, a bookmark, or a gallery listing;
    # the engine still sets document.title from meta.title once it runs. Use
    # --title when the two should differ (a template catalogue, say).
    title = title or (cfg.get("meta") or {}).get("title", "Undangan Pernikahan")
    data_json = guard(json.dumps(cfg, ensure_ascii=False, separators=(",", ":")))

    head = f"""<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{links}
<style>
/* engine — structure */
{engine_css}
/* theme: {theme} */
{theme_css}
</style>"""

    body = f"""<main id="app"></main>
<script>
{engine_js}
</script>
<script>
Undangan.init({{ data: {data_json} }});
</script>"""

    if fragment:
        return head + "\n\n" + body + "\n"

    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#16301f">
<meta name="robots" content="noindex">
{head}
</head>
<body>
{body}
</body>
</html>
"""


def main() -> int:
    p = argparse.ArgumentParser(description="Bundle an invitation into one HTML file.")
    p.add_argument("data", help="path to the client's JSON data file")
    p.add_argument("-o", "--out", help="output path (default: stdout)")
    p.add_argument("--fragment", action="store_true",
                   help="omit the document skeleton (for embedding hosts)")
    p.add_argument("--title", help="override the static <title> tag")
    args = p.parse_args()

    html = build(args.data, fragment=args.fragment, title=args.title)

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(html)
        kb = len(html.encode("utf-8")) / 1024
        print(f"{args.out}  ({kb:.1f} KB, satu file, tanpa dependency lokal)")
    else:
        sys.stdout.write(html)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
