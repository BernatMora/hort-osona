# 📝 CHANGELOG — Hort Osona

Tots els canvis notables al projecte, per data.

## [2026-06-18] — Generador de checklist mensual i prompt Open WebUI

### Afegit
- **`hort-checklist.py`** — generador intel·ligent de checklist mensual de l'hort:
  - Base de dades de ~60 tasques organitzades per mesos (1-12) i 7 categories
    (sembra, trasplantament, conreu, tractaments, collita, planificació, observació).
  - Càlcul de la **fase lunar real** per a qualsevol data (algorisme de cicles
    sinòdics, referència 6 gener 2000, període 29.530588 dies, ±1 dia).
  - Modes de sortida: Markdown imprimible, JSON estructurat, prompt Open WebUI,
    fragment HTML, o escriptura directa a `plans-mensuals/AAAA-MM-mes.md`.
  - Context climàtic del mes adaptat a Osona (gelades, calor, pluges, dates clau).
  - Recomanacions biodinàmiques segons la fase lunar (sembra, trasplantament,
    poda, adob verd).

- **Integració al lloc web** (`site/index.html`, 1.37 MB):
  - **Giny a la pàgina d'inici**: targeta esquerra amb el mes actual, fase
    lunar de la setmana en curs i top tasca prioritària; targeta dreta amb
    strip de 4 setmanes i botó "Obrir checklist completa".
  - **Pàgina `#checklist`** completa: taula lunar detallada, tasques
    organitzades per categoria amb **checkboxes persistents via localStorage**,
    dates clau a Osona i prompt Open WebUI amb **botó "Copiar"**.
  - Hash routing ampliat: `#checklist` carrega la pàgina completa.
  - Persistència del marcatge entre sessions (cada tasca té clau
    `checklist-YYYY-MM-titol`).

- **`site/checklist-data.json`** — dades estructurades del mes actual, generat
  automàticament per `build.py` cada vegada que es regenera el lloc.

- **`site/build.py`** — ampliat:
  - Importa `hort-checklist.py` dinàmicament.
  - Genera el JSON del mes actual i l'incrusta al template.
  - Passa el JSON com a placeholder `__CHECKLIST__` a `template.html`.

- **`site/template.html`** — ampliat:
  - CSS nou per a ginys mensils, taules lunars, llistes de tasques amb
    checkboxes, quadre de prompt estil terminal.
  - Funcions `renderChecklist()` i `isChecklistHash()` al router.
  - Persistència dels checkboxes via localStorage.
  - Botó de copiar prompt al porta-retalls.

- **`HORT-CHECKLIST.md`** — guia completa d'ús de l'eina, exemples de CLI,
  com afegir tasques i com funciona l'algorisme lunar.

### Modificat
- `site/build.py` — afegit `HORT-CHECKLIST.md` a `INFRASTRUCTURE_FILES`
  perquè no aparegui com a categoria "Altres".

### Com usar-ho
```bash
# Veure la checklist d'aquest mes
python hort-checklist.py

# Generar el fitxer del mes vinent a plans-mensuals/
python hort-checklist.py --date 2026-07 --write

# Prompt per Open WebUI (enganxar com a system prompt)
python hort-checklist.py --prompt
```

## [2026-06-16] — Lloc web unificat

### Afegit
- **Lloc web estàtic** a `site/index.html` (1.3 MB · 71 documents · 9 categories):
  - Sidebar amb categories collapsibles i comptadors.
  - Cercador client-side amb highlighting.
  - Hash routing per enllaços directes (`#doc=id`).
  - Paleta terra-verd-crema inspirada en l'horta d'Osona.
  - Tipografies: Fraunces (serif títols) + Inter (cos) + JetBrains Mono (codi).
  - Responsive + print stylesheet.
  - Zero dependències de runtime: tot és un únic fitxer HTML autocontingut.
- **`site/build.py`** — script Python que llegeix tots els `.md`, els
  classifica en 9 categories, els converteix a HTML i regenera el lloc.
- **`site/template.html`** — el template HTML amb placeholders, separat
  del codi de generació per facilitar edicions visuals.
- **`SETUP-SITE.md`** — guia de com regenerar i visualitzar el lloc.
- Esborrat `conserves.md` de la categoria "Conreu avançat" (ara és a
  "Transformació i fermentats" on pertany per la seva naturalesa).

### Modificat
- `00-index.md` — afegits enllaços al lloc web unificat i a SETUP-SITE.

## [2026-06-15] — Sessió inicial d'ampliació

### Afegit
- **3 noves fitxes de cultiu**:
  - `07-fitxes-cultius/col.md` (kale, bròquil, coliflor, llombarda, Brussel·les, colrave, col xina)
  - `07-fitxes-cultius/patata.md` (varietats locals, malalties, conservació)
  - `07-fitxes-cultius/bleda.md` (varietats catalanes)
  - `07-fitxes-cultius/pesol.md` (hibernació, fixació de nitrogen)
  - `07-fitxes-cultius/fava.md` (despuntes, dita "per Sant Andreu")
  - `07-fitxes-cultius/all.md` (conservació, all negre casolà)

- **3 eines operatives noves**:
  - `pla-12-mesos.md` — guia any-tipus amb dates clau d'Osona
  - `bitacola-setmanal.md` + `bitacola-setmanal-imprimible.html` — plantilla imprimible
  - `pla-tractaments-fitosanitaris.md` — calendari anual de tractaments ecològics

- **Calculadores i plantilles**:
  - `calculadora-reg-imprimible.html` — calculadora interactiva de reg
  - `calculadora-sembra.md` — càlcul de llavors i plantes necessàries
  - `pressupost-hort-imprimible.html` — pressupost anual amb càlcul automàtic

- **Guies noves**:
  - `guia-fermentats.md` — xucrut, kimchi, kombucha, kefir, etc.

- **Documentació**:
  - `README.md` — índex general del projecte
  - `SETUP-WINDOWS.md` — guia de sincronització amb Windows
  - `SYNC-SCRIPT.md` — ús dels scripts hort-sync
  - `hort-sync.sh` i `hort-sync.bat` — scripts de sincronització
  - `.gitignore` — exclusions adequades
  - `CHANGELOG.md` — aquest fitxer

- **Pla mensual actualitzat**:
  - `plans-mensuals/2026-06-juny.md` — ampliat amb calendari lunar, pla de reg, tractaments, compres, indicadors

### Modificat
- `00-index.md` — índex general actualitzat amb tots els nous documents

### Configuració
- Inicialitzat repositori Git a https://github.com/BernatMora/hort-osona (privat)
- Sincronització Mac ↔ Windows operativa
- 3 commits inicials: estat inicial, setup Windows, ampliació del projecte

## [2026-06-15] — Estat inicial del projecte

### Importat
- 136 fitxers de l'estat anterior del projecte (15 MB):
  - 8 fitxes de cultiu originals
  - 4 plans mensuals (incloent juny 2026)
  - 20+ guies avançades
  - 15+ guies de plantes medicinals
  - 30+ PDFs imprimibles
  - Calendari hort 2027
  - 30+ imatges

---

## Categories de canvis

- **Afegit** — funcionalitats noves
- **Modificat** — canvis en funcionalitats existents
- **Deprecat** — funcionalitats que s'eliminaran
- **Eliminat** — funcionalitats ja no disponibles
- **Seguretat** — vulnerabilitats solucionades
- **Configuració** — canvis en configuració

## Versions

Format basat en [Keep a Changelog](https://keepachangelog.com/ca/1.1.0/).
Aquest projecte segueix [Semantic Versioning](https://semver.org/spec/v2.0.0.html) per a les guies principals.
