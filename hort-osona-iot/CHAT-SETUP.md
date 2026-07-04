# 🤖 Sistema de xat amb IA local (RAG + Ollama)

> Com fer servir l'assistent hortolà que respon consultes en català basant-se en les fitxes del projecte.

## 🎯 Què és?

L'API de xat combina:
- **76-2.706 fitxes** locals del projecte (RAG)
- **Ollama** (model `hermes3:latest`, 8B paràmetres) — IA local, sense enviar res a Internet
- **FastAPI** — servidor web

Permet fer preguntes com:
- "Quan sembrar carbassa a Osona?"
- "Com combatre el pugó al tomàquet?"
- "Quines plantes medicinals puc cultivar?"

I obté respostes en **català** basant-se en les teves fitxes.

## 🏗️ Arquitectura

```
┌──────────┐    HTTP     ┌─────────────────┐    HTTP    ┌──────────┐
│ PWA/curl │ ──────────► │ FastAPI:8001    │ ────────► │ Ollama   │
│          │ ◄────────── │ (api_chat.py)   │ ◄──────── │ :11434   │
└──────────┘   JSON      └─────────────────┘   JSON     └──────────┘
                              │
                              ▼
                        ┌──────────┐
                        │  RAG     │ → 76 fitxes locals
                        └──────────┘
```

## 🚀 Com arrencar-ho

### 1. Assegura't que Ollama està actiu

```bash
# Si no s'està executant
open -a Ollama

# Comprova
curl http://localhost:11434/
# Hauria de respondre: "Ollama is running"
```

Si no tens `llama3.1`, no et preocupis — el sistema ara usa `hermes3:latest` per defecte.

Per instal·lar un model concret:
```bash
ollama pull hermes3:latest
# o
ollama pull llama3.1
```

### 2. Arrenca el backend de xat

Opció A — Amb l'script (recomanada):
```bash
cd ~/Desktop/hort-osona/hort-osona-iot
./start-chat.sh
```

Opció B — Manualment:
```bash
cd ~/Desktop/hort-osona/hort-osona-iot
python3 -m pip install --user fastapi uvicorn pydantic
python3 -m uvicorn backend.api_chat:app --host 0.0.0.0 --port 8001
```

Veuràs:
```
INFO:     Started server process [PID]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### 3. Prova'l!

```bash
# Health check
curl http://localhost:8001/chat/health

# Fer una pregunta
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Quan sembrar carbassa a Osona?"}'
```

Obre el navegador a:
- **http://localhost:8001/docs** — interfície Swagger amb tots els endpoints

## 📡 Endpoints

| Mètode | URL | Descripció |
|---|---|---|
| `GET` | `/chat/health` | Estat del sistema (model, docs carregats) |
| `POST` | `/chat` | Fer una pregunta |
| `GET` | `/docs` | Documentació interactiva (Swagger) |

### Exemple de resposta

```json
{
  "answer": "Segons la fitxa de cultiu proporcionada, a Osona es recomana sembrar carbassa en modals protegits com a abril...",
  "sources": [
    {"path": "07-fitxes-cultius/carbassa.md", "title": "Fitxa de cultiu: Carbassa", "score": 8.0},
    {"path": "pla-12-mesos.md", "title": "Pla dels 12 mesos", "score": 5.0}
  ],
  "question": "Quan sembrar carbassa?",
  "model": "hermes3:latest",
  "elapsed_ms": 31949
}
```

## 🛠️ Resolució de problemes

### ❌ "Ollama is not running"
```bash
open -a Ollama
sleep 5
curl http://localhost:11434/
```

### ❌ "model 'X' not found" a Ollama
```bash
# Mira quins models tens
ollama list

# Instal·la el que necessitis
ollama pull hermes3:latest
```

O canvia el model per defecte a `rag.py` (línia 43):
```python
def __init__(self, docs_dir: str = None, model: str = "elteumodel"):
```

### ❌ El backend penja en `/chat/health`
Normalment és perquè el RAG està carregant 76+ fitxes. La primera vegada triga ~25 segons, les següents van ràpides.

Si penja per sempre:
1. Comprova que tens permisos de lectura a tots els `.md`
2. Mira els logs d'Uvicorn per si hi ha un error
3. Prova de buidar el sistema: `pkill -f uvicorn` i tornar a arrencar

### ❌ "Port 8001 already in use"
```bash
lsof -i :8001
# Mata el procés que l'ocupa o canvia el port a l'script
```

## ⚡ Rendiment

- **Primera càrrega**: 25-30 segons (llegeix totes les fitxes)
- **Health check**: <2 segons
- **Pregunta simple**: 20-40 segons (depen d'Ollama)
- **Memòria**: ~1 GB (Ollama carrega el model a RAM)

## 🛑 Aturar el servidor

```bash
# Si l'has arrencat amb l'script: Ctrl+C

# Si l'has arrencat amb uvicorn en background:
pkill -f "uvicorn.*api_chat"
```

## 🌍 Configuració remota (Raspberry Pi)

Si vols usar el xat des de la Raspberry Pi de l'hort:

1. Assegura't que l'API escolta a `0.0.0.0` (ja ho fa)
2. Accedeix des d'un altre dispositiu: `http://IP-DE-LA-PI:8001/chat/health`
3. O usa Tailscale per accés segur des de fora de casa

A la PWA, configura `BACKEND_URL` a `http://hortpi.local:8001` o la IP de Tailscale.

## 📚 Més informació

- [rag.py](rag.py) — el sistema RAG
- [api_chat.py](backend/api_chat.py) — l'API FastAPI
- [README.md](README.md) — el projecte IoT complet
