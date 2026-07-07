# 🌱 Hort Osona — Visió completa del projecte

> **PWA + IoT + IA local + Cloud + Alexa + Backups** — un ecosistema personal d'horticultura ecològica a Osona.
>
> 📅 Última actualització: 2026-07-06
> 🏷️ Versió: 1.0 (consolidat)

---

## 🎯 Què és?

Un projecte personal que cobreix **tot el cicle de l'horticultura** amb tecnologia:

1. **Base de coneixement** (76+ fitxes en català) sobre horticultura ecològica a Osona
2. **PWA** (Progressive Web App) que funciona al mòbil i PC, **offline**, amb eines diàries
3. **Sistema IoT** amb sensors LoRa que envien dades en temps real des de l'hort
4. **IA local** (Ollama + RAG) per preguntar a l'hort amb llenguatge natural
5. **Skill d'Alexa** per preguntar a l'hort amb la veu
6. **Backups automàtics** a iCloud Drive i My Cloud Home (NAS local)
7. **Documents imprimibles** (PDF + HTML) per portar a l'hort

Tot **obert** al repo de GitHub: <https://github.com/BernatMora/hort-osona>

---

## 🏗️ Arquitectura global

```
┌──────────────────────────────────────────────────────────────────┐
│                          HORT (245 m)                            │
│  [3× Sensors humitat]──┐                                        │
│  [BME280]──────────────┤                                        │
│  [Pluviòmetre]─────────┼──> [Node TTGO LoRa32] ── LoRa 868MHz │
│  [Panell solar]────────┘   (ESP32 + bateria)    (5 km abast)   │
└──────────────────────────────────────────────────────────────────┘
                                                                   │
                                                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CASA — Raspberry Pi 4B                        │
│                                                                  │
│  [Waveshare LoRa HAT]──> [lora_receiver.py] ──> [Supabase Realtime]
│                                                                  │
│  [FastAPI /sensors]─────> ──>                                  │
│  [FastAPI /chat RAG]─────> Ollama (hermes3) ──> 76 fitxes .md   │
│  [Alexa Backend Flask]──>                                          │
└──────────────────────────────────────────────────────────────────┘
              │                            │
              ▼                            ▼
┌──────────────────────┐    ┌──────────────────────────────┐
│    Mac (casa)        │    │   Cloud / Internet           │
│  [PWA navegador]     │    │                              │
│  [Ollama extra]      │    │  [GitHub Pages] ──> PWA web  │
│  [Tailscale] ────────┼───>│  [Alexa Skills]  ──> veu     │
│  [Finder/SMB] ───────┼───>│  [Supabase]      ──> realtime│
└──────────────────────┘    │  [iCloud Drive]  ──> backup  │
                           │  [My Cloud Home] ──> NAS     │
                           └──────────────────────────────┘
```

---

## 📦 Components principals

### 1. Base de coneixement

**Ubicació**: fitxers `.md` a l'arrel del repo i a `docs/`

- **76 documents** en català sobre horticultura ecològica
- **9 categories** (Planificació, Fitxes cultiu, Conreu avançat, Medicinals, Bolets, etc.)
- **~28 fitxes de cultiu** específiques (carbassa, tomàquet, enciam, etc.)
- **12 guies avançades** (associacions, plagues, reg, compostatge, etc.)
- **Imprimible** en PDF i HTML per a cada secció

**Fitxers clau**:
- `00-index.md` — índex general
- `01-calendari-sembra.md` — calendari de sembra Osona
- `02-associacions-rotacions.md` — què plantar amb què
- `08-pla-mensual.md` — pla d'acció mensual
- `07-fitxes-cultius/*.md` — 28 fitxes individuals
- `plans-mensuals/` — quaderns mensuals

### 2. PWA (Progressive Web App)

**URL pública**: <https://BernatMora.github.io/hort-osona/>

**Tecnologia**: HTML + CSS + JS estàtic (zero backend per a la web), servit per GitHub Pages.

**Pàgines funcionals** (12 rutes):
| Ruta | Què fa |
|---|---|
| `#welcome` | Portada + targetes de les 9 categories |
| `#checklist` | Llista de tasques setmanals amb validació |
| `#quadern` | Bitàcola d'observacions diàries (amb tags, cerca, markdown) |
| `#calendari` | Vista 3×4 del quadern (mesos) |
| `#calendari-any` | Vista anual completa (12 mesos, lluna, tasques) |
| `#rotacions` | Rotacions de cultius recomanades |
| `#dates` | 9 localitats d'Osona + 27 cultius amb dates |
| `#meteo` | Meteo en temps real via Open-Meteo (7 localitats, 25+ WMO) |
| `#stats` | Estadístiques d'ús + gràfic 12 mesos |
| `#fonts` | 12 fonts locals + lectura amb tipografies |
| `#sensors` | Dades en temps real dels sensors (humitat, llum, etc.) |
| `#assistent` | Xat amb IA local (Ollama + RAG) |
| `#cerca` | Cercador avançat amb filtres (categoria, mes, text) |

**Característiques PWA**:
- ✅ Instal·lable (banner automàtic al mòbil)
- ✅ Funciona **offline** (service worker v2 amb cache-first)
- ✅ Persistent (localStorage per entrades del quadern, tasques, configuració)
- ✅ 3 temes visuals (estiu/tardor/hivern) amb auto-detecció per mes
- ✅ 76 docs indexats, cerca instantània
- ✅ **Reenginyeria recent**: 1.2 MB → 52 KB amb lazy load

**Fitxers clau**:
- `site/template.html` — HTML + CSS + JS (tot en un)
- `site/build.py` — pipeline que converteix `.md` → `index.html`
- `site/manifest.json` + `site/service-worker.js` + `site/icon-*.png` — PWA
- `index.html` (generat) — fitxer estàtic final
- `CHANGELOG.md` — registre de canvis

### 3. Sistema IoT (hort → Raspberry Pi)

**Ubicació**: `hort-osona-iot/`

**Stack tecnològic**:
- **Hardware**: ESP32 (TTGO LoRa32 V2) + Waveshare SX1262 868MHz HAT (RPi)
- **Protocol**: LoRa 868 MHz (5 km abast, 245 m a l'hort)
- **Backend**: FastAPI + Mosquitto MQTT + SQLite + Supabase
- **Llenguatge**: C++ (firmware) + Python (receptor, backend)

**Components nous afegits recentment**:
- ✅ Node emissor LoRa complet (firmware + documentació) — `node-emissor/`
- ✅ Receptor LoRa per Raspberry Pi — `backend/lora_receiver.py`
- ✅ Schema Supabase — `backend/supabase_schema.sql`
- ✅ Documentació completa — `GUIA-MUNTATGE-NODE.md`

**Sensors** (previstos):
- 3× Xiaomi MiFlora (humitat sòl, llum, T, conductivitat, bateria)
- 1× BME280 (T ambient, humitat, pressió)
- 1× Pluviòmetre
- Panell solar + bateria 18650 + TP4056

**Fitxers clau**:
- `hort-osona-iot/README.md` — visió general
- `hort-osona-iot/setup-pi.sh` — instal·lador automàtic RPi
- `hort-osona-iot/PEDIDO-AMAZON.md` + `LLISTA-CURTA.md` — compres
- `hort-osona-iot/node-emissor/src/main.cpp` — firmware ESP32
- `hort-osona-iot/backend/lora_receiver.py` — receptor RPi
- `hort-osona-iot/INICI-RAPID.md` — quickstart

### 4. Assistent IA local (Ollama + RAG)

**Stack**: Ollama (hermes3 o llama3.1) + RAG sobre 76 fitxes

**Característiques**:
- Respon en **català** amb cites
- Sinònims catalans (carbasso → carbassa, etc.)
- Stopwords eliminats
- Bonus per coincidències al títol
- Model local (sense enviar res a Internet)
- Suport GPU (Apple Silicon / NVIDIA / CPU)

**Integració**:
- 🌐 **Web** (PWA): pàgina `#assistent` amb xat UI
- 🎤 **Veu** (Alexa): skill "Hort Osona" — `hort-osona-iot/ALEXA-GUIA.md`
- 🔌 **API** (RPi): `hort-osona-iot/backend/api_chat.py` (port 8001)

**Fitxers clau**:
- `hort-osona-iot/rag.py` — sistema RAG (8.8 KB, ~200 línies)
- `hort-osona-iot/backend/api_chat.py` — API FastAPI
- `hort-osona-iot/ollama_test.py` — test de l'API Ollama
- `hort-osona-iot/RAG-README.md` — documentació
- `hort-osona-iot/CHAT-SETUP.md` — setup del xat

### 5. Skill d'Alexa "Hort Osona"

**Funcionalitat**: preguntar a l'hort amb la veu des d'un Amazon Echo

**Preguntes que entén**:
- "Alexa, pregunta a l'hort quan sembrar carbassa"
- "Alexa, pregunta a l'hort com combatre el pugó"
- "Alexa, pregunta a l'hort què fer al juliol"

**Stack**:
- Amazon Alexa Skills Kit (cloud)
- Flask backend (RPi o Mac) — `alexa_backend.py`
- Model d'interacció JSON — `alexa-skill/interaction-model.json`
- RAG local (reutilitza el sistema d'Ollama)

**Fitxers clau**:
- `hort-osona-iot/ALEXA-GUIA.md` — guia completa
- `hort-osona-iot/ALEXA-ACTIVAR.md` — com activar la skill
- `hort-osona-iot/COM-TROBAR-SKILL.md` — com trobar-la a l'app Alexa
- `hort-osona-iot/alexa_backend.py` — backend Flask (port 5050)
- `hort-osona-iot/alexa-skill/interaction-model.json` — intents + utterances
- `hort-osona-iot/scripts/start_alexa.sh` — script d'arrencada

### 6. Sistema de backups

**3 capes de seguretat**:
1. **GitHub** (remot, privat/públic) — control de versions
2. **iCloud Drive** (2 TB) — `ICLOUD-SYNC.md` + `scripts/setup_icloud_hort.sh`
3. **My Cloud Home** (WD NAS, 192.168.100.48) — `MYCLOUDHOME-GUIA.md` + `mycloud_storage.py`

**Configuració**:
- iCloud: rsync diari via launchd (macOS) o cron (Linux)
- My Cloud Home: SMB/CIFS muntat + script d'export automàtic

### 7. Documents imprimibles

**Ubicació**: `plans-mensuals/` i arrel (`*-2026.pdf`)

**Tipus**:
- 📅 Quadern d'observació anual (PDF + HTML)
- 🌱 Fitxes de cultius (PDF + HTML)
- 🧪 Conserves casolanes (PDF + HTML)
- 💧 Pla de reg (PDF)

**Generació**:
- HTML imprimible amb CSS @media print
- Conversió a PDF via `convertir_HTML_a_PDF.sh` (Playwright/Chromium headless)

---

## 📊 Estadístiques del projecte (2026-07-06)

| Mètrica | Valor |
|---|---|
| **Total fitxers al repo** | 327 |
| **Directoris** | 9 |
| **Documents .md** | ~120 |
| **Fitxes de cultiu** | 28 |
| **Pàgines PWA** | 12 |
| **Tests unitaris** | 16 (16/16 OK) |
| **Mida portal** | 52 KB (reenginyeria) |
| **Mida PWA completa** | 1.5 MB |
| **Línies de codi IoT** | ~3,000 (C++ + Python) |
| **Línies de codi PWA** | ~10,000 (HTML+CSS+JS) |
| **Total línies de codi** | ~15,000+ |
| **Commits totals** | 50+ |
| **Dies des de l'inici** | ~30 dies |

---

## 🔧 Eines i tecnologies

| Capa | Eines |
|---|---|
| **Base de coneixement** | Markdown, git |
| **PWA** | HTML5, CSS3 (Grid + variables), JS vanilla, Service Workers, Web App Manifest |
| **Build** | Python 3.11 (build.py, generar-pdf.py) |
| **PWA hosting** | GitHub Pages |
| **Backend IoT** | FastAPI, Mosquitto MQTT, SQLite, Supabase |
| **Receptor LoRa** | Python 3.11, pyserial, spidev |
| **Firmware emissor** | C++ (Arduino/ESP32), PlatformIO, LoRa library |
| **IA local** | Ollama, hermes3 / llama3.1, RAG custom |
| **Skill Alexa** | Alexa Skills Kit, Flask, JSON interaction model |
| **Cloud** | iCloud Drive (rsync), My Cloud Home (SMB/CIFS) |
| **PDF** | reportlab (Python) |
| **Testing** | pytest (16 tests) |
| **Accés remot** | Tailscale (VPN) |
| **Documentació** | Markdown, reportlab |

---

## 🚀 Com començar

### Per a tu (desenvolupador)

```bash
# Clonar el repo
git clone https://github.com/BernatMora/hort-osona.git
cd hort-osona

# Regenerar la PWA des dels .md
python site/build.py

# Servir localment
python -m http.server 8765
# Obre http://127.0.0.1:8765/index.html
```

### Per accedir des del mòbil

1. Obre <https://BernatMora.github.io/hort-osona/> al navegador
2. Tria "Afegir a pantalla d'inici" (banner automàtic a Android)
3. Ja tens la PWA instal·lada

### Per usar l'assistent IA

1. Instal·la [Ollama](https://ollama.com) al Mac
2. Descarrega un model: `ollama pull hermes3`
3. Engega el backend: `cd hort-osona-iot && python -m uvicorn backend.api_chat:app --host 0.0.0.0 --port 8001`
4. Obre la PWA, vés a `#assistent` i pregunta!

### Per activar Alexa

1. Segueix `hort-osona-iot/ALEXA-ACTIVAR.md`
2. Engega: `./scripts/start_alexa.sh`
3. Digues "Alexa, pregunta a l'hort..."

---

## 🛣️ Roadmap

### ✅ Fet
- [x] Base de coneixement (76 fitxes)
- [x] PWA funcional amb 12 pàgines
- [x] Cercador avançat
- [x] Calendari anual
- [x] Mode diari ric (tags, markdown, imatges)
- [x] Sistema IoT (LoRa + MiFlora + RPi)
- [x] IA local (Ollama + RAG)
- [x] Skill Alexa
- [x] Backups (iCloud + My Cloud Home)
- [x] Reenginyeria portal (1.2 MB → 52 KB)

### 🔄 En curs
- [ ] Muntatge final del hardware (RPi + sensors)
- [ ] Configuració Tailscale per accés remot
- [ ] Tests unitaris del frontend
- [ ] Documentació d'arquitectura (C4, ADR)

### 💡 Futures idees
- [ ] Càmera IP al·lerta de plagues (TensorFlow Lite a RPi)
- [ ] App mòbil nativa (Flutter) amb notificacions push
- [ ] Integració calendari Google/Apple
- [ ] Sistema de reg automatitzat (electrovàlvules)
- [ ] Versió multi-hort (compartir entre veïns)
- [ ] Bot oficial de Telegram
- [ ] ML per a prediccions de collita

---

## 📚 Índex de documentació

| Tema | Fitxer |
|---|---|
| Visió general del projecte | `README.md` |
| Canvis | `CHANGELOG.md` |
| Setup al Windows | `SETUP-WINDOWS.md` |
| Setup a GitHub Pages | `SETUP-GITHUB-PAGES.md` |
| Setup del lloc | `SETUP-SITE.md` |
| Accés mòbil | `ACCES-MOBIL.md` |
| Accés mòbil (docs) | `docs/ACCES-MOBIL.md` |
| VSCode | `VSCODE-GUIDE.md` |
| Test RAG | `TEST-RAG.md` |
| Xat ràpid | `XAT-RAPID.md` |
| Llista de compra | `LLISTA-COMPRA.md` |
| Sincronització | `SYNC-SCRIPT.md` |
| **IoT — visió general** | `hort-osona-iot/README.md` |
| **IoT — inici ràpid** | `hort-osona-iot/INICI-RAPID.md` |
| **IoT — llista compra** | `hort-osona-iot/PEDIDO-AMAZON.md` |
| **IoT — llista curta** | `hort-osona-iot/LLISTA-CURTA.md` |
| **IoT — Tailscale Mac** | `hort-osona-iot/GUIA-TAILSCALE-MAC.pdf` |
| **IoT — muntatge node** | `hort-osona-iot/GUIA-MUNTATGE-NODE.md` |
| **IoT — Alexa guia** | `hort-osona-iot/ALEXA-GUIA.md` |
| **IoT — Alexa activar** | `hort-osona-iot/ALEXA-ACTIVAR.md` |
| **IoT — Alexa skill** | `hort-osona-iot/COM-TROBAR-SKILL.md` |
| **IoT — setup xat** | `hort-osona-iot/CHAT-SETUP.md` |
| **IoT — RAG** | `hort-osona-iot/RAG-README.md` |
| **IoT — My Cloud** | `hort-osona-iot/MYCLOUDHOME-GUIA.md` |
| **IoT — iCloud sync** | `hort-osona-iot/ICLOUD-SYNC.md` |
| **IoT — projectes RPi** | `hort-osona-iot/RPi-PROJECTES.md` |
| **IoT — pas següent** | `hort-osona-iot/PAS-SEGÜENT.md` |
| **Consolidat (aquest)** | `PROJECTE-COMPLET.md` |

---

## 🏷️ Versions

- **v1.0** (2026-07-06): Estat consolidat amb IoT + IA + Alexa + Cloud

---

## 📜 Llicència

Projecte personal sense llicència explícita. Si t'interessa, contacta amb Bernat Mora.

---

## ✨ Agraïments

A tots els que han contribuït amb idees, codi, inspiració i eines:
- Ollama per fer la IA local accessible
- Open-Meteo per les dades meteorològiques gratuïtes
- Tailscale per la xarxa privada gratuïta
- Reportlab pels PDFs
- GitHub Pages per l'allotjament gratuït de la PWA
- La comunitat open-source en general
