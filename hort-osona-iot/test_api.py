"""
test_api.py — Test standalone de l'API sense uvicorn
Reprodueix exactament el que fa api_chat.py però sense servidor web.
"""

import sys
import time
from pathlib import Path

print("=== TEST STANDALONE ===", flush=True)

# Afegir el path
sys.path.insert(0, str(Path(__file__).parent))

# Importar el que importa api_chat
print("1. Important fastapi/uvicorn...", flush=True)
t0 = time.time()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
print(f"   OK ({time.time()-t0:.1f}s)", flush=True)

print("2. Important rag...", flush=True)
t0 = time.time()
from rag import HortRAG
print(f"   OK ({time.time()-t0:.1f}s)", flush=True)

print("3. Important api_chat (que crea l'app)...", flush=True)
t0 = time.time()
import backend.api_chat as api_chat
print(f"   OK ({time.time()-t0:.1f}s)", flush=True)

print(f"4. App creada? {api_chat.app is not None}", flush=True)

print("5. Cridant get_rag()...", flush=True)
t0 = time.time()
rag = api_chat.get_rag()
print(f"   OK ({time.time()-t0:.1f}s), {len(rag.docs)} docs, model: {rag.model}", flush=True)

print("6. Provant /chat/health manualment...", flush=True)
t0 = time.time()
result = api_chat.chat_health()
print(f"   OK ({time.time()-t0:.1f}s): {result}", flush=True)

print("7. Provant /chat amb pregunta...", flush=True)
t0 = time.time()
req = api_chat.ChatRequest(question="Hola")
result = api_chat.chat(req)
print(f"   OK ({time.time()-t0:.1f}s): {str(result)[:200]}", flush=True)

print("\n✅ TOTS ELS TESTS HAN PASSAT", flush=True)
