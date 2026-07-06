# RAG Local — Hort Osona

Sistema RAG (Retrieval-Augmented Generation) que permet preguntar a la base
de coneixement de l'hort d'Osona en llenguatge natural, en català, usant un
LLM local (Ollama).

## Què és?

Un RAG combina:
1. **Cerca** (R) — Busca a les fitxes `.md` del projecte
2. **Generació** (G) — Un LLM local (Ollama) genera respostes basant-se
   en el context trobat

## Requisits

- macOS amb Apple Silicon (M1/M2/M3) o Intel amb RAM ≥ 8 GB
- Python 3.10+ amb `urllib` (estàndard, no cal instal·lar res)
- [Ollama](https://ollama.com) instal·lat
- Model `hermes3:latest` descarregat (4.7 GB)

## Instal·lació

### 1. Instal·la Ollama

```bash
brew install ollama
```

Si ja el tens (al sistema ja estava instal·lat), comprova:

```bash
ollama --version
```

### 2. Descarrega el model

```bash
ollama pull hermes3:latest
```

Alternatives si vols provar un altre:
- `ollama pull llama3.1:8b` (Meta, multilingüe)
- `ollama pull qwen2.5:7b` (xinès, però excel·lent en català)
- `ollama pull gemma2:9b` (Google)

### 3. Arrenca Ollama

```bash
# Opció A: com a servei (recomanat)
brew services start ollama

# Opció B: manual
OLLAMA_FLASH_ATTENTION="1" OLLAMA_KV_CACHE_TYPE="q8_0" ollama serve
```

Comprova que funciona:

```bash
curl http://localhost:11434/api/version
# Hauria de retornar {"version":"0.31.1"}
```

## Ús

### Línia de comandes

Des del directori `hort-osona-iot/`:

```bash
python3 rag.py "Quan sembrar carbassa a Osona?"
python3 rag.py "Com combatre el mildiu del tomàquet?"
python3 rag.py "Quines plantes medicinals puc cultivar?"
```

Sortida esperada:

```
[RAG] Carregades 2797 fitxes útils

============================================================
Q: Quan sembrar carbassa a Osona?
============================================================

A: La millor època per sembrar carbassa a Osona és...

Fonts:
  • Fitxa de cultiu: Carbassa (Cucurbita maxima) (score: 8)
  • Calendari de sembra (score: 5)
  ...
```

### API REST

Posa en marxa el servidor backend:

```bash
cd backend
python3 -m uvicorn api_chat:app --host 0.0.0.0 --port 8001
```

Prova'l:

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Quan sembrar carbassa?"}'
```

### Des del mòbil (PWA)

La web de Hort Osona ja té integrat el xat RAG. Per fer-lo servir
cal que el backend estigui arrencat al Mac:

1. Arrenca el backend al Mac (port 8001)
2. Obre https://BernatMora.github.io/hort-osona/ al mòbil
3. Toca el botó 💬 (xat)
4. Escriu la pregunta

El xat detecta si el backend és accessible i, si no, mostra
instruccions per arrencar-lo.

## Com funciona internament

```
Pregunta ──┐
           ▼
   ┌──────────────┐
   │  Cerca       │  Tokenitza, aplica sinònims, compta matches
   │  paraules    │  a totes les fitxes .md
   │  clau        │
   └──────┬───────┘
          │ Top 4 fitxes
          ▼
   ┌──────────────┐
   │  Construeix  │  Junta les 4 fitxes en un context
   │  context     │
   └──────┬───────┘
          │ Context + pregunta
          ▼
   ┌──────────────┐
   │  Ollama      │  Model hermes3 genera resposta
   │  (LLM local) │  en català, basada en context
   └──────┬───────┘
          │ Resposta
          ▼
   "La millor època per sembrar carbassa..."
```

## Estructura

- `rag.py` — Classe `HortRAG` amb `search()`, `ask()`, `ask_ollama()`
- `backend/api_chat.py` — API REST amb FastAPI
- `ollama_test.py` — Test bàsic de connexió amb Ollama
- `test_simplificat.py` — Test de cerca sense Ollama

## Fitxers indexats

- **Total**: 2.797 entrades (a partir de 78 fitxes `.md` principals)
- **Exclosos**: README, CHANGELOG, fitxers d'infraestructura
- **Sinònims**: "carbasso" → "carbassa", "tomaca" → "tomàquet", etc.

## Tests realitzats

| Pregunta | Resultat |
|---|---|
| Quan sembrar carbassa a Osona? | ✅ Abril-maig |
| Com combatre el mildiu del tomàquet? | ✅ Rotació + cobertura |
| Quines plantes medicinals? | ✅ 8 plantes d'Osona |
| Quins bolets a la tardor? | ✅ Cep, rovelló, trompeta |
| Quantes vegades regar a l'estiu? | ✅ Diari juliol-agost |

## Limitacions

- **Velocitat**: ~10 segons per resposta (CPU Apple Silicon)
- **Precisió**: depèn de la qualitat de les fitxes
- **Català**: hermes3 és bo en català però no perfecte
- **Context**: només 2000 caràcters per fitxa (per evitar prompts massa llargs)

## Millores futures

- [ ] Usar embeddings (nomic-embed-text) per cerca semàntica
- [ ] Augmentar el context a 4000 caràcters
- [ ] Afegir historial de conversa
- [ ] Persistir els tests com a suite oficial
