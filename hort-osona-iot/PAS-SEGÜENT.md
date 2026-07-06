# Pas següent: connectar la skill al backend del Mac

## On ets ara

✅ Skill **"Hort Osona"** creada a Alexa Developer Console
✅ Model d'interacció **build OK** (Amazon ha acceptat el JSON)
❌ Falta posar l'**endpoint** (la URL on Amazon enviarà les preguntes)

## Què has de fer ara

Necessitem una **URL HTTPS pública** que apunti al backend del teu Mac.
Això és perquè Amazon Alexa (cloud AWS) no pot accedir a `127.0.0.1` o
`192.168.100.110` (la teva IP local).

La forma més fàcil i gratuïta és **Tailscale Funnel**, que ja tens
instal·lat al Mac.

---

## Pas 1: Autenticar Tailscale (un sol cop)

1. Obre la **app Tailscale** al Mac (la icona que sembla una T a la
   barra de menús dalt a la dreta, prop del rellotge)
2. Si diu "Tailscale is off", clica **"Log In..."**
3. S'obrirà Safari amb una pàgina de login de Tailscale
4. Fes login amb el teu compte (Gmail, Apple, Microsoft — el que hagis
   triat quan vas crear el compte)
5. Torna a Tailscale — ara hauria de dir "Tailscale is on" amb la teva
   IP

Si **no tens compte de Tailscale**:
1. A la pàgina de login, tria **"Don't have an account? Sign up"**
2. Crea un compte gratuït
3. Torna al Mac i accepta el node

---

## Pas 2: Activar Tailscale Funnel

Un cop Tailscale està connectat, al **Terminal** del Mac:

```bash
# Comprovar que funciona
tailscale status
# Ha de mostrar el teu Mac amb la seva IP 100.x.x.x

# Activar Funnel (pot trigar uns segons)
sudo tailscale set --accept-routes
tailscale funnel --bg 5050
```

Si et demana permís a l'ACL:
1. Obre https://login.tailscale.com/admin/acls/file al navegador
2. Crea o edita el fitxer d'ACL
3. Assegura't que tens:
   ```json
   {
     "acls": [
       // ... la teva config
     ],
     "funnel": {
       "your-mac-name": ["https://your-mac-name.tail-net.ts.net:443"]
     }
   }
   ```
4. A `Settings` → `Devices`, troba el teu Mac i activa el toggle
   **"Funnel"**

Alternativa més fàcil:
1. Obre https://login.tailscale.com/admin/machines
2. Clica el teu Mac
3. A la dreta, activa **"Edit ACLs"** o **"Enable Funnel"**

---

## Pas 3: Arrencar el backend amb l'script

Al **Terminal** del Mac:

```bash
cd ~/Desktop/hort-osona/hort-osona-iot
./scripts/start_alexa.sh
```

Hauries de veure:
```
🎉 TOT LLEST!
URL pública del backend:
https://something.tail-net.ts.net/alexa
```

📋 **Copia aquesta URL** (la que comença per `https://`)

---

## Pas 4: Posar l'endpoint a Alexa Developer Console

1. Torna a https://developer.amazon.com/alexa/console/ask
2. Clica la teva skill **"Hort Osona"**
3. Al menú de l'esquerra, clica **"Endpoint"**
4. A "Service Endpoint Type", selecciona **"HTTPS"**
5. A la caixa **"Default Region"**, enganxa la URL que vas copiar
6. Clica **"Save Endpoints"**

---

## Pas 5: Activar la skill al teu Echo

1. Al teu iPhone, obre l'**app Alexa**
2. Toca **"More"** (a baix a la dreta)
3. Toca **"Skills & Games"**
4. Toca la lupa 🔍 i busca **"Hort Osona"**
5. Si no surt, toca la categoria **"Your Skills"** o **"Dev Skills"**
6. Toca **"Hort Osona"** → **"Enable to use"**

---

## Pas 6: Primeres proves amb veu

Al teu Amazon Echo (que tu anomenes "Eco"):

```
Eco, obre hort osona
Eco, pregunta a l'hort quan he de regar
Eco, pregunta a l'hort com combatre el mildiu
Eco, pregunta a l'hort quan sembro tomàquets
Eco, pregunta a l'hort sobre cols
```

⏱️ Alexa trigarà uns 10-15 segons a respondre (Ollama és local i triga).
Tindràs paciència — no és tan ràpid com ChatGPT perquè corre al teu Mac.

---

## Si Tailscale no funciona / prefereixes una altra opció

### Opció B: ngrok (molt fàcil, gratuït)

1. Descarrega ngrok: https://ngrok.com/download (gratis, compte amb email)
2. Instal·la'l: `brew install ngrok`
3. Autentica: `ngrok config add-authtoken <el_teu_token>`
4. Arrenca el backend: `cd ~/Desktop/hort-osona/hort-osona-iot && python3 alexa_backend.py &`
5. En una altra terminal: `ngrok http 5050`
6. Copia la URL `https://xxx.ngrok-free.app/alexa`
7. Posa-la a l'endpoint d'Alexa Developer Console

### Opció C: Servidor propi (VPS)

Si tens un servidor a internet (DigitalOcean, AWS, etc.), pots desplegar-hi
el backend amb nginx + HTTPS. Més feina, però més estable.

---

## Quan vulguis parar-ho tot

```bash
# Parar el backend
kill $(cat ~/Library/Logs/hort-osona-alexa/backend.pid)

# Parar Tailscale Funnel
tailscale funnel --off 5050
```

---

## Si algo falla

Comparteix-me:
- L'**error exacte** que surt (text o captura)
- A quin **pas** t'has quedat encallat
- Si la URL de Tailscale t'ha funcionat o no

I t'ajudo a resoldre-ho.
