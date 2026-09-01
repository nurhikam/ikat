#!/usr/bin/env bash
# Scaffold one invitation for one client.
#
#   ./bin/new-client.sh <slug> [theme]
#
# Produces <slug>.html + data/<slug>.json from the demo, wired to the theme.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLUG="${1:-}"
THEME="${2:-forest-lace}"

if [[ -z "$SLUG" ]]; then
  echo "usage: $(basename "$0") <slug> [theme]" >&2
  echo "themes: $(ls -1 "$ROOT/themes" | tr '\n' ' ')" >&2
  exit 1
fi

if [[ ! "$SLUG" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "slug harus huruf kecil, angka, dan tanda hubung saja: '$SLUG'" >&2
  exit 1
fi

if [[ ! -d "$ROOT/themes/$THEME" ]]; then
  echo "tema '$THEME' tidak ada. tersedia: $(ls -1 "$ROOT/themes" | tr '\n' ' ')" >&2
  exit 1
fi

DATA="$ROOT/data/$SLUG.json"
PAGE="$ROOT/$SLUG.html"

for f in "$DATA" "$PAGE"; do
  if [[ -e "$f" ]]; then
    echo "sudah ada: ${f#$ROOT/} — hapus dulu kalau memang mau ditimpa" >&2
    exit 1
  fi
done

sed "s/\"theme\": \"[^\"]*\"/\"theme\": \"$THEME\"/" "$ROOT/data/demo.json" > "$DATA"

cat > "$PAGE" <<HTML
<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Undangan Pernikahan</title>
<meta name="theme-color" content="#16301f">
<meta name="robots" content="noindex">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<link rel="stylesheet" href="engine/engine.css">
<link rel="stylesheet" href="themes/$THEME/theme.css" data-theme="$THEME">
</head>
<body>

<main id="app"></main>

<script src="engine/engine.js"></script>
<script>
  Ikat.init({ src: 'data/$SLUG.json' });
</script>

</body>
</html>
HTML

echo "dibuat:"
echo "  ${DATA#$ROOT/}"
echo "  ${PAGE#$ROOT/}   (tema: $THEME)"
echo
echo "berikutnya:"
echo "  \$EDITOR ${DATA#$ROOT/}"
echo "  buka http://localhost:8000/$SLUG.html?to=Nama%20Tamu"
