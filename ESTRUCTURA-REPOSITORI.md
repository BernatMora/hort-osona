# Fonts i artefactes generats

Per conservar les URLs públiques actuals, els fitxers existents continuen al seu lloc. La regla a partir d’ara és:

- Els `.md` són la **font editable**.
- `build_portal_v2.py` i els scripts de generació són les **eines**.
- `index.html`, `docs/`, `search_index.json`, els `*-imprimible.html` i els `*-2026.pdf` són **artefactes generats**.
- Els PDF nous de gran mida s’han de publicar preferentment com a GitHub Release i no duplicar-se sense necessitat.

Abans de publicar: regenera, executa `python validate_portal.py` i comprova que el diff només contingui canvis esperats.
