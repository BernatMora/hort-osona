#!/bin/bash
# publicar.sh — posa la web nova a l'arrel del repo (i despres cal hort-sync).
# NO publica sol: cal dir-ho explicitament amb --si.
set -u
cd "$(dirname "$0")"
set -eu
if [ "${1:-}" != "--si" ]; then
  echo "Aixo SUBSTITUEIX index.html, docs/ i afegeix les pagines noves a l'arrel del repo."
  echo "Quan ho tinguis clar:  ./publicar.sh --si   i despres  ./hort-sync.sh"
  exit 0
fi
echo "--- copia de seguretat de l'index actual ---"
cp -a index.html "index.html.bak.pre-nou-disseny-$(date +%Y%m%d-%H%M)" 2>/dev/null && echo "  feta"
echo "--- generant a l'arrel ---"
python3 build_web.py --out .
echo "--- comprovant enllacos ---"
python3 - <<'PY'
from pathlib import Path
import re
arrel = Path('.')
nav = 0
for f in list(arrel.glob('*.html')) + list((arrel/'cultiu').glob('*.html')):
    for u in re.findall(r'href="([^"#][^"]*)"', f.read_text(encoding='utf-8')):
        if u.startswith(('http','mailto','tel:')): continue
        if not (f.parent/u).resolve().exists(): nav += 1
print('  enllacos trencats a les pagines publiques:', nav)
PY
echo "--- llest: ara ./hort-sync.sh per pujar-ho a GitHub ---"
