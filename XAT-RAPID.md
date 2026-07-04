# 🧠 Xat local RAG — Guia d'ús ràpida

Pots preguntar coses sobre el teu hort en català i el sistema respon amb informació extreta dels teus 73 documents locals. **Tot funciona en local** — cap dada no surt del teu Mac.

## Ús ràpid (consola)

```bash
cd ~/Desktop/hort-osona/hort-osona-iot

# Fer una pregunta
python3 rag.py "Quan sembrar carbassa a Osona?"

# Fer les 3 preguntes d'exemple
python3 rag.py
```

## Ús com a API (PWA / frontend)

```bash
cd ~/Desktop/hort-osona/hort-osona-iot
python3 -m uvicorn backend.api_chat:app --host 0.0.0.0 --port 8001
```

Un cop arrencat, l'API està disponible a:
- Salut: `http://localhost:8001/chat/health`
- Preguntar: `POST http://localhost:8001/chat` amb `{"question": "Quan plantar all?"}`

## Exemples de preguntes que funcionen bé

| Tema | Pregunta d'exemple |
|---|---|
| **Sembra** | Quan sembrar carbassa a Osona? |
| **Plagues** | Com combatre el mildiu del tomàquet? |
| **Medicinal** | Quines plantes medicinals puc cultivar al meu hort? |
| **Reg** | Quin reg necessita la carbassa a l'estiu? |
| **Collita** | Quan collir el porro? |
| **Associacions** | Què puc plantar al costat de les cols? |
| **Varietats** | Quines varietats de tomàquet resisteixen millor la calor? |
| **Compost** | Com fer compost ràpid a l'estiu? |

## Com funciona

1. **Ollama** corre al port 11434 amb el model `hermes3:latest` (4.6 GB)
2. **`rag.py`** llegeix els 73+ `.md` del projecte i fa cerca per paraules clau
3. Per cada pregunta:
   - Troba els 4 documents més rellevants
   - Els passa com a context al LLM
   - Genera una resposta en català amb cites de les fonts

## Requisits

- **Ollama** instal·lat i en marxa (`brew install ollama`, `ollama serve`)
- **Model `hermes3:latest`** descarregat (`ollama pull hermes3:latest`)
- **Python 3** amb `fastapi`, `uvicorn`, `pydantic` (ja instal·lats)

## Temps de resposta

- **Primera pregunta**: 30-60 segons (carrega tots els documents)
- **Preguntes següents**: 10-20 segons

## Si falla

1. Comprova que Ollama corre: `curl http://localhost:11434/`
2. Comprova el model: `ollama list` (ha de ser-hi `hermes3:latest`)
3. Si s'ha quedat penjat: `pkill ollama && open -a Ollama`
4. Errors concrets → mira `CHAT-SETUP.md` (més detallat)
