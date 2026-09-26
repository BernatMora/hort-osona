# 📌 Pendents — hort-osona

Llista de feina acordada per a properes sessions (darrera revisió: 2026-08-31).

## 1. Completar els SVGs de les fitxes de cultiu
Ja en tenen (15): api, escarola, espinac, meló, porro, rave, lufa, albergínia, cogombre,
nap, moniato, blat-de-moro, maduixa (+ els 20 del lot "20 SVGs" en execució).

Falten (16):
- [ ] all
- [ ] alfabrega
- [ ] aromatiques
- [ ] bleda
- [ ] carabasso
- [ ] carbassa
- [ ] ceba
- [ ] col
- [ ] enciam
- [ ] farigola
- [ ] fava
- [ ] menta
- [ ] mongeta
- [ ] orenga
- [ ] pastanaga
- [ ] patata
- [ ] pebrot
- [ ] pesol
- [ ] romani
- [ ] tomaquet

Nota: 200x200, mateix estil dels existents (`07-fitxes-cultius/img/rave.svg` com a referència:
fons crema amb gradient radial, terra, il·lustració plana amb gradients). El builder els
incrusta sol si el fitxer existeix (`docs/.../img/<nom>.svg` es genera amb el build).

## 2. Guia de multiplicació de plantes  ✅ FETA (2026-08-31: multiplicacio-guia.md)

## 3. Fitxes de cultiu noves  ✅ FETES (2026-08-31: blat-de-moro.md, maduixa.md)

Seguir el to/estructura de les fitxes existents i registrar-les a
`build_portal_v2.py`, README i 00-index.

## 4. Fitxes tardor-hivern noves + marcs  ✅ FETA (2026-09-14: broquil, calcots, canonges, rucula.md)

Afegides per la llista de marcs (imatge). Fitxes noves amb marcs de plantació.
Actualitzats marcs existents (bleda, col, enciam, api, maduixa). Pendents:
SVGs per a les fitxes noves si es volen.

## Idees en reserva (no acordades)
- Guia de fauna de l'hort (senglars, conills, ocells): barreres, protecció i convivència
- Circuit d'intercanvi de llavors (on, quan, com etiquetar-les)

---

## Fet el 2026-09-26 (disseny nou)

- [x] Generador unificat (`build_web.py` + `md_render.py`); els antics a `_antics/`.
- [x] Portada amb **que plantar aquest mes** i **al costat de que**, mobil primer.
- [x] Una pagina per cultiu i una per document; calendari anual en colors.
- [x] PWA instal·lable i les 33 il·lustracions SVG en us.
- [x] Detector automatic de contradiccions a les associacions.

## Pendent (per ordre)

- [x] **Publicat** el 26/09/2026 (commit `7b2275c`): la web nova es a bernatmora.github.io/hort-osona.
- [x] **Contradiccions d'associacions**: resolt amb un **criteri prudent automatic** (26/09/2026).
      Si un parell surt com a bo en una font i com a dolent en una altra, la web **no el posa
      com a bo**: el marca com a **⚠️ discutit** i el deixa fora. N'hi ha 5 a les fitxes
      (all↔cols, patata↔api, pebrot↔alberginia, pesol↔all/ceba/porro, tomaquet↔api/pebrot/alberginia)
      i 3 a la taula general. Es poden resoldre definitivament decidint quina font mana.
- [x] **Cerca global** a la portada: un sol camp que busca entre cultius, pagines i tots els
      documents (index generat al build, funciona tambe sense connexio).
- [ ] Acabar els SVG de les fitxes que no en tenen.
