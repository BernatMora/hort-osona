# 📝 CHANGELOG — Hort Osona

Tots els canvis notables al projecte, per data.

## [2026-07-03] — Sensors IoT + Assistent IA local (RAG + Ollama)

### Sensors IoT — pàgina #sensors
- Nova pàgina `#sensors` a la PWA que consumeix l'API REST del backend Raspberry (`/api/sensors`, `/api/sensors/{parcela}/history?hours=24`)
- **Targetes de sensor** amb humitat del sòl, llum, temperatura, conductivitat, bateria
- **Gràfiques SVG natives** (sense llibreries externes) de les últimes 24h per parcel·la
- **Alerta visual** quan humitat < 30% (targeta amb borde vermell)
- **Auto-refresc** cada 60 segons
- **Configuració URL backend** via localStorage (per defecte `http://hortpi.local:8000`)
- Hash routing `#sensors` afegit

### Assistent IA local (Ollama + RAG)
- **`hort-osona-iot/rag.py`** (~8.8 KB): sistema RAG que indexa 147 fitxes locals (76 web + d'altres) i respon amb cites
- **Tokenitzador** robust: lowercase, sense accents, stopwords, **sinònims** (carbasso→carbassa, tomaca→tomàquet, pulgon→pugó, etc.)
- **Cerca per paraules clau** amb bonus títol ×3 i exclusió de duplicats
- **Model per defecte**: `llama3.1` (Ollama 0.31.1 al Mac)
- **`hort-osona-iot/backend/api_chat.py`** (~2.5 KB): API FastAPI amb `GET /chat/health` i `POST /chat`
- **Singleton RAG** a FastAPI per evitar recarregar documents a cada petició
- **CORS obert** per permetre accés des de la PWA allotjada a GitHub Pages
- **`hort-osona-iot/ollama_test.py`** (~3.2 KB): script de verificació d'Ollama

### Pàgina #assistent (xat UI)
- Nova pàgina `#assistent` a la PWA amb interfície de xat
- **8 preguntes suggerides** predefinides
- **Missatge de benvinguda** amb presentació
- **Format de xat** (usuari a la dreta, assistent a l'esquerra)
- **Fonts citades** com a enllaços clicables a les fitxes originals
- **Configuració URL backend** via localStorage (per defecte `http://localhost:8001`)
- **Animació de typing** "Pensant..." durant la generació
- **100% local i privat** — sense núvol

### Tests i validació
- Ad-hoc verification completa: **34/34 checks passen, 0 fallits**
- 3 preguntes reals validades end-to-end (carbassa, planter tomàquet, adventícies útils)
- Temps de resposta RAG: 5-15 segons (variable segons model)
- 4 fonts citades per pregunta
- `node --check` JS OK, 16/16 tests unitaris
- Backend actiu al port 8001, 147 docs indexats

## [2026-07-03] — PWA, GitHub Pages i millora responsive

### PWA completa
- **`site/manifest.json`**: PWA manifest amb nom, 4 dreceres (Checklist, Quadern, Rotacions, Estadístiques), icones 192/512, paleta terra-verd
- **`site/service-worker.js`**: service worker amb cache-first per assets locals, network-first per Open-Meteo
- **Icones PWA**: `icon.svg`, `icon-192.png`, `icon-512.png` (verd oliva, planta amb fruit)
- **Banner d'instal·lació** PWA al navegador (Chrome, Edge) — botons "Instal·lar" i "Més tard" amb memòria de 7 dies
- **Mode offline**: un cop instal·lada, l'app funciona sense Internet
- **Notificacions programables**: API Notification + scheduling de tasques
- **API pública**: `window.hortOsona.demanarPermisNotif()`, `.mostrarNotif()`, `.programarNotif()`

### Reconfiguració per a GitHub Pages
- El `site/build.py` ara genera `index.html` i tots els fitxers PWA a l'**arrel del repo** (no pas a `site/`)
- Compatible amb GitHub Pages triant `main` + `/ (root)` (l'única opció que permet la UI actual)
- Nova constant `GENERATED_AT_ROOT` per excloure fitxers generats de la categorització
- **Publicat a**: <https://BernatMora.github.io/hort-osona/>

### Fix responsive mòbil
- `html, body { overflow-x: hidden; max-width: 100% }` — sense scroll horitzontal
- `@media (max-width: 820px)`: layout vertical amb `grid-template-rows: auto 1fr`
- **Sidebar sticky** al top quan es fa scroll (max-height 50vh)
- Nou `@media (max-width: 480px)`: ajustos per a mòbils petits

### Neteja
- Esborrat `site/index.html` duplicat — ja no cal, es regenera a l'arrel
- `site/` conté només els **orígens** (build.py, template.html, manifest.json, service-worker.js, icones, font del checklist)

## [2026-07-03] — Lots 3, 4 i 5: contingut i funcionalitats avançades

### Afegit (Lot 3 — Contingut)
- **5 fitxes noves**:
  - `07-fitxes-cultius/porro.md` (all porro)
  - `07-fitxes-cultius/api.md` (api)
  - `07-fitxes-cultius/rave.md` (rave)
  - `07-fitxes-cultius/melo.md` (meló)
  - `adventicies-utilitat-guia.md` (plantes adventícies útils)

### Afegit (Lot 4 — Funcionalitats web)
- **Pàgina `#calendari`**: vista anual 3×4 de les entrades del quadern
  d'observació. Dies marcats amb color ocre + recompte d'entrades
  - Llegenda visual, targetes resum
  - Integrada amb el localStorage del quadern
- **Exportació ICS**: genera un fitxer `.ics` vàlid amb totes les
  tasques del mes actual. Importable a Google Calendar, Apple Calendar,
  Outlook. Botó verd al checklist
- 2 targetes noves a la pàgina d'inici: Calendari i Fonts

### Afegit (Lot 5 — Final)
- **Pàgina `#fonts`**: índex de 12 fonts locals catalanes
  (Esporus, L'Era, CCPAE, Fundació Miquel Agustí, Escola Agrària
  de Manresa, Xarxa Catalana de Graners, ADRÓ, Vivers Vern, etc.)
  organitzades per categoria. Substitueix el lector RSS perquè les
  fonts locals no publiquen feeds
- **Impressió / PDF**: CSS `@media print` dedicat + botó
  "🖨 Imprimir / PDF" a la checklist. Amaga sidebar, form,
  botons; neteja el layout per a A4
- **Estadístiques avançades**: pàgina `#stats` enriquida amb
  - Mesos més actius (del quadern)
  - Temes més registrats (per paraules clau)
  - Recomanacions personalitzades basades en patrons
  - Mostra la localitat meteorològica configurada
- 2 targetes noves a la pàgina d'inici: Calendari d'observacions
  i Fonts locals

### Modificat
- `site/build.py`: afegides 5 fitxes noves a la categorització
- `site/template.html`: +600 línies (4 pàgines noves + CSS d'impressió)
- `CHANGELOG.md`: reescrit per netejar duplicats

---

## [2026-06-18] — Generador de checklist mensual i prompt Open WebUI

### Afegit
- **`hort-checklist.py`** — generador intel·ligent (721 línies)
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
- **`HORT-CHECKLIST.md`** — guia d'ús completa del generador.
- **`tests/test_hort_checklist.py`** — 16 tests unitaris (6 classes).
  Tots passen. Inclouen validació de:
  - Fase lunar per a dates reals (verificables amb meteolluna.cat)
  - Totes les fases possibles
  - Validesa de les categories i prioritats de tasques
  - Dates clau dels mesos
  - Generació de Markdown i JSON
  - Generació del prompt per Open WebUI
- **Bug `setmanes_del_mes` corregit** — la funció retornava 0 setmanes
  per a gener 2025 a causa d'un error de precedència d'operadors al `while`.
  Reescrita amb condicions explícites i límit d'iteracions segur.
- **Bug de tests corregit** — les dates de fase lunar dels tests eren
  errònies (el meu record de les fases no coincidia amb l'algorisme
  que ja era correcte). Tests actualitzats amb dates verificades a
  meteolluna.cat (8 juny = minvant, 15 juny = nova, 22 juny = creixent,
  30 juny = plena).

### Modificat
- `site/build.py` — pipeline de generació ampliat per integrar el giny
  i la pàgina del checklist.
- `site/template.html` — CSS i JS nous per al giny i la pàgina.

---

## [2026-06-16] — Lloc web unificat

### Afegit
- **Lloc web estàtic** a `site/index.html` (1.3 MB · 71 documents · 9 categories)
  - Sidebar amb 9 categories, cerca client-side
  - Renderitzat Markdown, hash routing per a back/forward
  - Identitat visual: paleta terra-verd-crema, tipografia Fraunces
- **Pipeline Python** a `site/build.py` per regenerar el lloc
- **Template HTML** a `site/template.html`
- `SETUP-SITE.md` — instruccions d'ús del pipeline

### Modificat
- `00-index.md` — enllaços al lloc
- `CHANGELOG.md` — aquesta entrada
- `README.md` — nova secció "Lloc web unificat"

---

## [2026-06-15] — Sessió inicial d'ampliació

(Detalls de la sessió d'ampliació del projecte — 15 fitxes de cultiu afegides,
estructura de planificació revisada, documentació ampliada.)

---

## [2026-06-15] — Estat inicial del projecte

(Projecte creat amb 60+ fitxes base sobre hort ecològic, plantes medicinals,
bolets, conserves i etnobotànica d'Osona.)

---

Format basat en [Keep a Changelog](https://keepachangelog.com/ca/1.1.0/).
Aquest projecte segueix [Semantic Versioning](https://semver.org/spec/v2.0.0.html) per a les guies principals.
