# 🌐 SETUP-SITE — Com regenerar el lloc web unificat

Aquest directori (`site/`) conté un generador estàtic que converteix tots els
fitxers `.md` del projecte en un únic **SPA estàtic** (sense backend,
tot client-side) navegable i cercable.

## Què hi ha

- **`template.html`** — el template HTML/CSS/JS amb placeholders (`__DOCS__`,
  `__SIDEBAR__`, `__TOTAL__`, `__NCAT__`, `__DATE__`).
- **`build.py`** — script Python que llegeix tots els `.md`, els classifica
  en 9 categories seguint l'estructura del README, els converteix a HTML
  amb `markdown` 3.10+ i substitueix els placeholders al template.
- **`index.html`** — l'artefacte generat (1.3 MB, 71 documents, autocontingut).
- **`extracted.js`** — fitxer de validació temporal (es pot esborrar).

## Com regenerar

Des de l'arrel del projecte:

```bash
python site/build.py
```

Sortida esperada:

```
✅ site/index.html generat
   Documents:  71
   Categories: 9
   Mida:       1356.2 KB
   ...
```

## Com visualitzar localment

Com que el lloc carrega Google Fonts i ha de servir-se via HTTP (no
`file://`), cal un servidor local:

```bash
# Opció 1: Python (ja ve instal·lat)
python -m http.server 8765 --bind 127.0.0.1

# Opció 2: VS Code — extensió "Live Server"
# Clic dret a site/index.html → "Open with Live Server"
```

Després obre: <http://127.0.0.1:8765/site/index.html>

## Característiques

- **Sidebar** amb 9 categories collapsibles i recompte de documents.
- **Cercador** client-side amb highlighting (cerca a títol, resum i path).
- **Hash routing** (`#doc=id`) per enllaços directes i back/forward del
  navegador.
- **Paleta terra-verd-crema** inspirada en l'horta d'Osona.
- **Tipografies** Fraunces (serif, títols) + Inter (cos) + JetBrains Mono
  (codi) via Google Fonts.
- **Responsive** (breakpoint a 820px) i **print stylesheet** per imprimir
  fitxes individuals.
- **Sense dependències de runtime**: tot és un únic fitxer HTML.

## Com afegir o moure documents

Edita la llista `CATEGORIES` al principi de `build.py` (cap a la línia 30).
Cada categoria té:

```python
("Nom de la categoria", "📅", [
    "01-calendari-sembra.md",
    "07-fitxes-cultius/*.md",   # també admet globs amb subdirectori
    "plans-mensuals/*.md",
])
```

L'ordre en aquesta llista és l'ordre d'aparició al sidebar.

## Fitxers exclosos

Per defecte s'exclouen:
- Fitxers d'infraestructura: `README.md`, `CHANGELOG.md`, `SETUP-WINDOWS.md`,
  `SYNC-SCRIPT.md`, `VSCODE-GUIDE.md`, `SETUP-SITE.md`.
- Plantilles: qualsevol fitxer que comenci per `_` (p. ex.
  `07-fitxes-cultius/_plantilla.md`).

Si vols incloure'n algun, edita els sets `INFRASTRUCTURE_FILES` i
`INFRASTRUCTURE_DIRS` al `build.py`.

## Per què un directori a part?

- No embruta l'arrel del projecte amb artefactes generats.
- Permet ignorar `site/index.html` del Git (es regenera) o pujar-lo si
  vols tenir-lo sempre disponible.
- Si un dia vols GitHub Pages, simplement activa'l a `Settings → Pages`
  triant la branca i `/site` com a carpeta.

## Validació

Després de cada `build.py`, valida que:

1. L'script no ha donat errors.
2. El recompte de documents és l'esperat (71 actualment).
3. En obrir al navegador, el sidebar mostra totes les categories i la
   cerca retorna resultats.
4. (Opcional) Comprova el JS amb `node --check site/extracted.js`
   després d'extreure'l amb una eina o un one-liner.
