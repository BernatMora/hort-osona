"""
api_chat.py — Endpoint /api/chat per a la PWA hort-osona.

Combina el sistema RAG (rag.py) amb l'API FastAPI existent.
"""

import sys
from pathlib import Path

# Assegurar que podem importar rag
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
except ImportError:
    print("Falten dependències. Instal·la: pip install fastapi uvicorn pydantic")
    sys.exit(1)

from rag import HortRAG


# === Models Pydantic ===
class ChatRequest(BaseModel):
    question: str
    model: str = "hermes3:latest"


class SourceInfo(BaseModel):
    path: str
    title: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]
    question: str
    model: str
    elapsed_ms: int


# === App ===
app = FastAPI(title="Hort Osona Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialitza RAG (singleton)
_rag = None


def get_rag():
    global _rag
    if _rag is None:
        _rag = HortRAG()
    return _rag


@app.get("/chat/health")
def chat_health():
    """Comprova l'estat del xat."""
    try:
        rag = get_rag()
        return {
            "status": "ok",
            "model": rag.model,
            "docs_loaded": len(rag.docs),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Pregunta al sistema RAG."""
    import time
    start = time.time()
    try:
        rag = get_rag()
        if req.model != rag.model:
            # Si canvia el model, recarrega
            rag = HortRAG(model=req.model)
        result = rag.ask(req.question)
        elapsed = int((time.time() - start) * 1000)
        return ChatResponse(
            answer=result["answer"],
            sources=[SourceInfo(**s) for s in result["sources"]],
            question=result["question"],
            model=rag.model,
            elapsed_ms=elapsed,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Main ===
if __name__ == "__main__":
    import uvicorn
    print("🚀 Hort Osona Chat API — http://0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
