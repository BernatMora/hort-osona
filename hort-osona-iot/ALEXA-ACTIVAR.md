# 🎤 Com activar la skill "Hort Osona" al teu Amazon Echo

Aquesta és la guia pas a pas per fer que el teu Amazon Echo (el que tu
anomenes "Eco") respongui a les preguntes sobre l'hort.

**Temps estimat**: 20 minuts (la majoria esperant que Amazon compili)
**Cost**: 0 € (tot gratuït)

---

## Què necessites

| Element | On és |
|---|---|
| El teu Mac amb `hort-osona-iot` | El que estàs usant ara |
| El teu iPhone amb l'app Alexa | App Store → cerca "Amazon Alexa" |
| El teu Amazon Echo (Eco) | A casa teva, connectat a la xarxa WiFi |
| Compte d'Amazon Developer | https://developer.amazon.com (gratis, un sol cop) |
| Tailscale | Ja instal·lat al Mac |
| Ollama amb `hermes3` | Ja instal·lat |

---

## PART 1: Preparar el backend (al Mac)

### Pas 1.1: Arrencar el backend + Tailscale Funnel

Obre el **Terminal** al Mac i executa:

```bash
cd ~/Desktop/hort-osona/hort-osona-iot
./scripts/start_alexa.sh
```

El script:
1. Comprova que Ollama està corrent
2. Comprova que tens Flask
3. Arrenca el backend al port 5050
4. Exposa'l amb Tailscale Funnel (URL HTTPS pública)
5. Et mostra la URL pública

**Si et surt un error d'autenticació Tailscale**:
```bash
sudo tailscale up
```
Segueix les instruccions (t'enviarà un link per activar el node).

**Si Tailscale Funnel no està activat al teu compte**:
1. Obre https://login.tailscale.com/admin/acls/file
2. Crea/edita el fitxer d'ACLs
3. Afegeix o modifica la secció `"acls"` o afegeix `"funnel"` permissions
4. Tailscale et demana confirmar

> 💡 **Comprova el log si algo falla**:
> ```bash
> tail -f ~/Library/Logs/hort-osona-alexa/alexa_backend.log
> ```

Quan tot funcioni veuràs:

```
🎉 TOT LLEST!
URL pública del backend:
https://macbookpro-de-bernat.tail-net.ts.net/alexa
```

📋 **Copia aquesta URL** — la necessitaràs al pas 3.2.

---

## PART 2: Crear la skill a Alexa Developer Console

### Pas 2.1: Crear compte de developer (un sol cop)

Si ja tens compte → salta al pas 2.2.

1. Obre https://developer.amazon.com
2. Clica **"Sign in"** i fes login amb el teu compte d'Amazon
3. Un cop dins, vés a https://developer.amazon.com/alexa/console/ask
4. Si et demana registrar-te com a developer, accepta (gratis, 0 €)
5. Accepta els termes del "Amazon Developer Services Agreement"

### Pas 2.2: Crear la skill

1. A https://developer.amazon.com/alexa/console/ask clica **"Create Skill"**

2. Omple el formulari:

| Camp | Valor |
|---|---|
| Skill name | `Hort Osona` |
| Default language | **English (US)** ⚠️ Amazon no suporta ca-ES |
| Choose a model | **Custom** |
| Choose a method to host | **Provision your own** |

3. Clica **"Create skill"** (botó blau dalt a la dreta)

4. Tria **"Start from scratch"** i clica **"Continue with custom model"**

### Pas 2.3: Enganxar el model d'interacció

1. Al menú de l'esquerra, clica **"Interaction Model"**
2. Clica la pestanya **"JSON Editor"**
3. **Esborra** tot el que hi hagi
4. Obre el fitxer següent al teu Mac:
   ```
   ~/Desktop/hort-osona/hort-osona-iot/alexa-skill/interaction-model.json
   ```
5. **Copia TOT** el contingut (⌘+A, ⌘+C al TextEdit o VSCode)
6. **Enganxa** al JSON Editor d'Amazon
7. Clica **"Save Model"** (botó dalt)
8. Clica **"Build Model"** — espera 1-2 minuts

Si tot va bé veuràs un check ✓ verd al costat de "Build Model".

### Pas 2.4: Configurar l'endpoint

1. Al menú de l'esquerra, clica **"Endpoint"**
2. Sota "Service Endpoint Type", selecciona **"HTTPS"**
3. A la caixa **"Default Region"**, enganxa la URL que vas copiar al pas 1.1
   (ha d'acabar en `/alexa`)
4. Selecciona **"My development endpoint is a sub-domain of a domain that has a wildcard certificate from a certificate authority"**
5. Clica **"Save Endpoints"** (dalt)

### Pas 2.5: Activar la interfície de veu (opcional però recomanable)

1. Al menú de l'esquerra, clica **"Interfaces"**
2. Activa **"Alexa Presentation Language"** (per si vols pantalles)
3. Clica **"Save Interfaces"**

---

## PART 3: Provar la skill

### Pas 3.1: Provar-la al simulador (ràpid!)

1. A Alexa Developer Console, clica la pestanya **"Test"** (a dalt)
2. A "Test is enabled for:" selecciona **"Development"**
3. A la caixa de text, escriu (o clica el micròfon i parla):

```
open hort osona
```

4. Hauries de veure una resposta vàlida!

Prova altres coses:
- `pregunta a l'hort quan he de regar`
- `pregunta a l'hort com combatre el mildiu`
- `pregunta a l'hort quan sembro tomàquets`

### Pas 3.2: Activar-la al teu Amazon Echo (per veu real)

1. Al teu iPhone, obre l'**app Alexa**
2. Toca **"More"** (a baix a la dreta, amb 3 línies)
3. Toca **"Skills & Games"**
4. Toca la lupa 🔍 (a dalt) i busca: **"Hort Osona"**
5. Si no surt, toca la categoria **"Your Skills"** (potser cal "Dev Skills")
6. Toca **"Hort Osona"** i després **"Enable"**

Si Alexa et demana linked account, simplement prem "No" o "Skip" — la nostra skill no necessita compte.

### Pas 3.3: Primeres proves amb veu

Ara ja pots parlar al teu Eco! Prova:

```
Eco, obre hort osona
Eco, pregunta a l'hort quan he de regar
Eco, pregunta a l'hort com combatre el mildiu
Eco, pregunta a l'hort quan sembro tomàquets
Eco, pregunta a l'hort sobre cols
```

⏱️ **Tingues paciència**: Ollama triga uns 10-15 segons a respondre. Alexa et dirà "espera un moment" o farà un so mentre processa.

---

## PART 4: Solució de problemes

### "Hi ha hagut un problema amb la resposta de la skill"

1. Comprova que el backend està corrent:
   ```bash
   curl http://localhost:5050/health
   ```
   Ha de tornar `{"status": "ok", ...}`

2. Comprova que Tailscale Funnel està actiu:
   ```bash
   tailscale funnel status
   ```
   Ha de mostrar el port 5050 actiu

3. Prova la URL pública des d'un altre dispositiu (mòbil amb 4G):
   ```bash
   curl https://la-teva-url.ts.net/health
   ```

### "El micro d'Alexa no m'entén 'hort osona'"

Prova altres variants:
- "Alexa, obre **hort osona**" (Amazon entén millor "hort" que "eco")
- Fes servir l'invocació exacta del model: `hort osona` (en minúscules al JSON)

Si tot falla, pots canviar l'**invocation name** al JSON del model d'interacció:
```json
"invocationName": "el meu hort"
```
I tornar a fer "Build Model".

### "La resposta és en castellà i la voldria en català"

⚠️ **Amazon Alexa NO té veu en català oficialment** (juliol 2026).

Alternatives que es podrien afegir més endavant:
- Integrar Google Translate TTS
- Usar una Raspberry Pi amb TTS local (espeak-ng)
- Canviar a Google Assistant (sí té ca-ES limitat)

### "Ollama triga massa"

Si vols accelerar:
- Usa un model més petit: `ollama pull llama3.2:3b` (2 GB en lloc de 4.7 GB)
- O `phi3:mini` (2.3 GB)
- Edita `alexa_backend.py` línia 30: `OLLAMA_MODEL = "llama3.2:3b"`

### El backend es para sol

El script `start_alexa.sh` no és persistent — si tanques el terminal, es para.

**Per fer-lo persistent** (que corri sempre al Mac):
1. Obre **System Settings** → **General** → **Login Items**
2. Clica **"+"** i afegeix `~/Desktop/hort-osona/hort-osona-iot/scripts/start_alexa.sh`
3. Marca la casella "Hide" (perquè no s'obri una finestra)

O millor, usa `launchd`:

```bash
# Crear fitxer launchd
cat > ~/Library/LaunchAgents/com.hort-osona.alexa.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hort-osona.alexa</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/bernatmorasanglas/Desktop/hort-osona/hort-osona-iot/scripts/start_alexa.sh</string>
        <string>local</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/hort-osona-alexa.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/hort-osona-alexa.error.log</string>
</dict>
</plist>
EOF

# Carregar
launchctl load ~/Library/LaunchAgents/com.hort-osona.alexa.plist
```

Ara el backend arrencarà automàticament quan engeguis el Mac.

---

## PART 5: Modes d'ús recomanats

### Ús diari

Un cop configurat, simplement:
1. Assegura't que el Mac està encès (o el backend corrent)
2. Digues: **"Eco, pregunta a l'hort sobre ..."**

### Quan vols parar-ho

```bash
# Parar el backend
kill $(cat ~/Library/Logs/hort-osona-alexa/backend.pid)

# Parar Tailscale Funnel
tailscale funnel --off 5050
```

### Quan vulguis millorar respostes

Les respostes depenen del corpus `hort-osona/`. Si hi afegeixes una fitxa
nova (p. ex. "plagues/2026-pulgó.md"), les respostes milloraran
automàticament la propera vegada.

---

## Resum

```
✓ Backend corrent al port 5050
✓ Expossat amb Tailscale Funnel (HTTPS)
✓ Skill creada a Alexa Developer Console
✓ Model d'interacció amb 11 intents en català
✓ Activada a l'app Alexa del teu iPhone
✓ Proves amb veu al teu Amazon Echo funcionals

Cost total: 0 €
Temps: 20 minuts
Limitació: veu espanyola d'Alexa (no catalana)
```

A gaudir! 🌱🎤
