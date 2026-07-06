# Alexa Skill "Hort Osona" — Guia completa

## Visió general

Skill d'Alexa que et permet **preguntar a l'hort amb la veu**. Utilitza
el sistema RAG local (Ollama + corpus .md) per respondre preguntes
sobre cultius, plagues, èpoques de sembra, etc.

## Arquitectura

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Amazon Echo   │ ───> │ Alexa Skills Kit │ ───> │  Flask Backend  │
│   (la teva      │      │  (cloud AWS)     │      │  (RPi o Mac)    │
│    veu)         │ <─── │                  │ <─── │  Port 5050      │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                                            │
                                                            ▼
                                                    ┌──────────────────┐
                                                    │  Ollama + RAG    │
                                                    │  (hermes3)       │
                                                    │  + corpus .md    │
                                                    └──────────────────┘
```

## Flux d'una pregunta

1. **Usuari**: "Alexa, pregunta a l'hort quan he de regar"
2. **Alexa**: envia a Alexa Skills Kit (cloud AWS)
3. **ASK**: envia POST JSON al teu backend
4. **Flask**: rep, valida, consulta Ollama
5. **Ollama**: cerca al corpus + genera resposta
6. **Flask**: retorna JSON a ASK
7. **Alexa**: llegeix la resposta en veu

## Què pots dir

| Frase | Intent | Exemple |
|---|---|---|
| "Alexa, pregunta a l'hort quan he de sembrar tomàquets" | `QuanSembrarIntent` | Cultiu: tomàquet |
| "Alexa, pregunta a l'hort com combatre el mildiu" | `ComCombatentIntent` | Plaga: mildiu |
| "Alexa, pregunta a l'hort quan he de regar" | `QuanRegarIntent` | - |
| "Alexa, pregunta a l'hort quan collim carbasses" | `QuanCollirIntent` | Cultiu: carbassa |
| "Alexa, pregunta a l'hort {qualsevol cosa}" | `PreguntaHortIntent` | Text lliure |
| "Alexa, pregunta a l'hort com esta l'hort" | `EstatHortIntent` | - |
| "Alexa, pregunta a l'hort ajuda" | `HelpIntent` | - |

## Instal·lació (pas a pas)

### 1. Requisits previs

- Python 3.8+
- Ollama instal·lat amb model `hermes3` (o un altre)
- Compte d'Amazon Developer (gratuït)
- Un compte AWS Lambda (o servidor propi exposat)

### 2. Instal·lar el backend

```bash
cd ~/Desktop/hort-osona/hort-osona-iot

# Crear entorn virtual
python3 -m venv venv
source venv/bin/activate

# Instal·lar dependencies
pip install flask

# Assegurar que Ollama esta arrencat
ollama serve &

# Provar el backend
python3 alexa_backend.py
```

Hauria de dir:
```
Escoltant a http://0.0.0.0:5000
```

### 3. Exposar el backend (per a proves)

⚠️ **Important**: Amazon Alexa NO pot accedir a `127.0.0.1`. Cal
exposar el servidor amb un túnel o desplegar-lo en un servidor.

#### Opció A: ngrok (proves, gratuït)

```bash
# Instal·lar ngrok
brew install ngrok

# Expose el port
ngrok http 5050
```

ngrok et donarà una URL tipus:
```
https://a1b2c3d4.ngrok.io/alexa
```

#### Opció B: Tailscale Funnel (recomanat per a ús personal)

```bash
# Instal·lar Tailscale
brew install tailscale

# Autenticar (un sol cop)
sudo tailscale up

# Exposar el port
tailscale funnel 5050
```

Et donarà una URL tipus:
```
https://macbookpro-de-bernat.tail-net.ts.net/alexa
```

#### Opció C: Servidor propi / VPS (producció)

Desplega el backend a un servidor (DigitalOcean, AWS, etc.) amb HTTPS.

### 4. Crear la skill a Alexa Developer Console

1. Anar a https://developer.amazon.com/alexa/console/ask
2. Clicar **"Create Skill"**
3. Nom: `Hort Osona`
4. Idioma: **Catalan (ca-ES)** o **Spanish (es-ES)** — Amazon no té CA oficial
5. Tipus: **Custom**
6. Hosting: **Provision your own**
7. Clicar **"Create skill"**

### 5. Configurar el model d'interacció

1. Al menú, **"Interaction Model"** → **"JSON Editor"**
2. Enganxa el contingut de `alexa-skill/interaction-model.json`
3. Clicar **"Save Model"**
4. Clicar **"Build Model"** (pot trigar 1-2 min)

### 6. Configurar el endpoint

1. Al menú, **"Endpoint"**
2. Tipus: **"HTTPS"**
3. URL: la URL del túnel (p. ex. `https://macbook.tailscale.ts.net/alexa`)
4. Clicar **"Save Endpoints"**

### 7. Afegir capacitats de veu en català

⚠️ **Limitació**: Amazon Alexa no suporta **veu en català** oficialment.
Tindràs veu espanyola. Per millorar:

1. Al menú, **"Interfaces"** → activar **"Alexa Presentation Language"**
2. Per a veu catalana natural, esperar a Amazon o usar altres solucions (veure "Alternatives")

### 8. Provar la skill

1. Al menú, **"Test"** → activar **"Test in development"**
2. Provar amb text: escriure "pregunta a l'hort quan he de regar"
3. Hauries de veure la resposta

## Ús amb el teu Amazon Echo

Un cop publicada la skill (veure més avall):

1. Obre l'app Alexa al mòbil
2. **Settings** → **Your Skills** → **Dev Skills**
3. Activa **"Hort Osona"**
4. Digues: "Alexa, obre hort osona" o "Alexa, pregunta a l'hort..."

## Publicar la skill (per a ús personal)

⚠️ Per a ús personal NO cal publicar-la oficialment. Només cal
activar-la en mode "development" al teu compte.

**Però** si vols compartir-la:
1. Anar a **"Distribution"** → **"Skill privacy"**
2. Omplir els formularis
3. **"Distribution"** → **"Availability"**
4. **"Submit for review"** (pot trigar setmanes)

## Proves automatitzades

Jo he validat el backend amb 5 tests reals. Resultats:

| Test | Resultat |
|---|---|
| `PreguntaHortIntent` ("Quan he de sembrar tomàquets a Osona?") | ✅ Resposta correcta |
| `QuanRegarIntent` | ✅ Resposta vàlida |
| `ComCombatentIntent` (mildiu) | ⚠️ Resposta parcial (corpus incomplet) |
| `QuanSembrarIntent` (enciam) | ✅ Resposta correcta |
| `HelpIntent` | ✅ Llistat de comandaments |

## Limitacions conegudes

### 1. Veu en català

Amazon Alexa no té veu en català. Les respostes es llegeixen en espanyol.

**Alternatives**:
- Usar una altra plataforma (Google Assistant sí té català limitat)
- Text-to-speech local (espeak-ng, festival)
- Esperar a Amazon

### 2. Latència

- Ollama triga ~10 segons per resposta
- Total: ~12-15 segons entre pregunta i resposta
- Acceptable per a ús personal

### 3. Precisió de les respostes

- Depèn de la informació al corpus
- Si el corpus no té info, Ollama pot inventar coses (hallucinations)
- Solució: afegir més fitxes al projecte hort-osona

## Troubleshooting

### El backend no respon

```bash
# Comprovar que Flask está escoltant
lsof -i :5050

# Comprovar els logs
tail -f /tmp/alexa_backend.log
```

### Alexa diu "Hi ha hagut un problema"

1. Comprovar la URL del endpoint (ha de ser HTTPS)
2. Comprovar que el túnel está actiu
3. Comprovar els logs del backend

### Respostes massa llargues

Editar `alexa_backend.py` línia 167:
```python
"num_predict": 200  # Reduir a 100-150
```

### Millorar respostes

- Afegir més fitxes al projecte `hort-osona/`
- Les respostes seran més bones automàticament
- O canviar el prompt per ser més estricte

## Cost

| Component | Cost |
|---|---|
| Amazon Developer account | Gratuït |
| ngrok (proves) | Gratuït (1 túnel) |
| Tailscale (ús personal) | Gratuït (100 dispositius) |
| Ollama | Gratuït (local) |
| Flask | Gratuït (open source) |
| **Total** | **0 €** |

## Recursos

- [Alexa Skills Kit docs](https://developer.amazon.com/en-US/docs/alexa/alexa-skills-kit.html)
- [ASK CLI](https://developer.amazon.com/en-US/docs/alexa/smapi/ask-cli-intro.html)
- [Alexa Presentation Language](https://developer.amazon.com/en-US/docs/alexa/alexa-presentation-language/apl-overview.html)
- [Tailscale Funnel](https://tailscale.com/kb/1223/funnel/)

## Fitxers del projecte

- `alexa-skill/interaction-model.json` — Model d'interacció (intents, slots)
- `alexa_backend.py` — Backend Flask
- `ALEXA-GUIA.md` — Aquesta guia

## Crèdits

- **Autor**: Bernat Mora
- **Corpus**: Projecte Hort Osona (78 fitxes .md)
- **LLM**: Ollama + hermes3 (local)
- **Plataforma**: Amazon Alexa Skills Kit
