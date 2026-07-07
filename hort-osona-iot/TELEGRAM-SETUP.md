# 🤖 Hort Osona — Bot de Telegram

> Guia per crear, configurar i arrencar el bot de Telegram del projecte.

## 🎯 Què és?

Un bot de Telegram que et permet **preguntar a l'hort** des del mòbil amb
missatges normals, sense instal·lar cap app addicional.

**Avantatges vs Alexa**:
- ✅ Molt més fàcil de provar (només un xat)
- ✅ No cal cap compte d'Amazon Developer
- ✅ Funciona amb qualsevol compte de Telegram (que és gratuït)
- ✅ Pots veure tot l'historial de preguntes
- ✅ Pots compartir el bot amb família/amics

## 📋 Què necessites

| Element | On és |
|---|---|
| Compte de Telegram | App Store / Google Play → "Telegram" (gratis) |
| 5 minuts del teu temps |  |
| El token del @BotFather | Ja el tens! |
| Ollama corrent al Mac | Ja el tens |
| `python-telegram-bot` | Cal instal·lar |

## 🔐 Pas 1 — Guardar el token de forma segura

⚠️ **MAI** posis el token directament al codi. Usa un fitxer `.env`.

### 1.1. Crear el fitxer `.env`

Al Mac, obre el **Terminal** i executa:

```bash
cd ~/Desktop/hort-osona/hort-osona-iot
cp .env.example .env
```

### 1.2. Editar `.env` amb el teu token

Obre el fitxer `.env` amb el teu editor preferit:

```bash
nano .env
# o
code .env
# o qualsevol altre editor
```

I posa el teu token real a la línia `TELEGRAM_BOT_TOKEN=`:

```bash
TELEGRAM_BOT_TOKEN=8983276598:AAF1JNYZecE6zX4lRj940rcAz91d8_VUBuo
```

⚠️ **Important**:
- El fitxer `.env` ja està al `.gitignore`, **NO es puja a GitHub**
- **No comparteixis** el fitxer `.env` amb ningú
- Si el token es filtra, pots revocar-lo a @BotFather amb `/revoke`

## 📦 Pas 2 — Instal·lar dependències

```bash
# Activar el teu venv de Python (si en tens)
source ~/path/to/your/venv/bin/activate

# O usar el Python global
pip install python-telegram-bot python-dotenv
```

## 🚀 Pas 3 — Arrencar el bot

### 3.1. Assegura't que Ollama està corrent

```bash
ollama serve
```

(Si ja el tens com a servei, no cal fer res)

### 3.2. Arrencar el bot

```bash
cd ~/Desktop/hort-osona/hort-osona-iot
python telegram_bot.py
```

Hauries de veure:

```
==========================================
🌱 Hort Osona - Bot de Telegram
==========================================

Directori: /Users/.../hort-osona-iot
RAG script: /Users/.../hort-osona-iot/rag.py
RAG existeix: True
Token: OK (configurat)

Arrencant bot...
Bot arrencat. Esperant missatges...
Prem Ctrl+C per parar.
```

## 📱 Pas 4 — Provar el bot

1. Obre **Telegram** al mòbil (o PC)
2. Busca el bot pel seu **username** (el que vas posar al BotFather)
3. Toca **"Iniciar"** o envia `/start`
4. Hauries de rebre el missatge de benvinguda

### Proves que pots fer

| Prova | Què esperar |
|---|---|
| `/start` | Missatge de benvinguda |
| `/ajuda` | Llista d'opcions |
| `/info` | Info tècnica del sistema |
| "Quan sembrar carbassa?" | Resposta del RAG (5-15s) |
| "Com combatre el pugó?" | Resposta amb fonts citades |
| `/sensors` | Placeholder (fins que RPi estigui OK) |
| `/pregunta pregunta llarga amb espais` | També funciona |

## 🔧 Solució de problemes

### El bot no arrenca

Comprova:
1. El token està ben posat al `.env` (sense espais, amb els `:` correctes)
2. `python-telegram-bot` està instal·lat: `pip list | grep telegram`
3. Ollama està corrent: `curl http://localhost:11434/api/version`

### El bot arrenca però no respon

1. Mira el log: `tail -f ~/Library/Logs/hort-osona-alexa/` o el terminal on l'has arrencat
2. Comprova que el RAG funciona sol: `python rag.py "prova"`

### Timeout al respondre

El RAG triga 5-15 segons. Si triga més:
- Prova amb una pregunta més curta
- O augmenta el timeout al codi (línia `timeout=120`)

### "Conflict: terminated by other getUpdates request"

Tens 2 instàncies del bot corrent. Para-les totes dues i arrenca només una:

```bash
pkill -f telegram_bot.py
python telegram_bot.py
```

## 🔄 Comparació amb Alexa

| Característica | Telegram | Alexa |
|---|---|---|
| **Cost** | 0 € | 0 € |
| **Configuració** | 5 min | 20-30 min |
| **Privadesa** | Total (local) | Total (local) |
| **Veu** | ❌ | ✅ |
| **Sempre a mà** | ✅ (mòbil) | ✅ (Eco) |
| **Compartir** | ✅ fàcil | ❌ complicat |
| **API oberta** | ✅ | ❌ parcial |

## 🛣️ Properes passes

Quan el bot funcioni, podem afegir:
- [ ] Comanda `/sensors` real (dades de la RPi)
- [ ] Notificacions automàtiques (alerta si humitat < 30%)
- [ ] Comanda `/temperatura` (última mesura)
- [ ] Comanda `/reg` (registrar un reg al quadern)
- [ ] Imatges (enviar foto d'una plaga → rebre diagnòstic)

## 📞 Suport

Si tens cap problema, obre un issue a GitHub o escriu-me.
