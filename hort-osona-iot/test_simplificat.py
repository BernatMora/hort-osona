"""
test_simplificat.py — Test ultra-simplificat
"""
import time
print("A. start", flush=True)
t0 = time.time()
import sys
sys.path.insert(0, "/Users/bernatmorasanglas/Desktop/hort-osona/hort-osona-iot")
print(f"B. path afegit ({time.time()-t0:.1f}s)", flush=True)
t0 = time.time()
from fastapi import FastAPI
print(f"C. fastapi importat ({time.time()-t0:.1f}s)", flush=True)
t0 = time.time()
from pydantic import BaseModel
print(f"D. pydantic importat ({time.time()-t0:.1f}s)", flush=True)
t0 = time.time()
from rag import HortRAG
print(f"E. rag importat ({time.time()-t0:.1f}s)", flush=True)

t0 = time.time()
rag = HortRAG()
print(f"F. HortRAG creat ({time.time()-t0:.1f}s), {len(rag.docs)} docs", flush=True)

t0 = time.time()
result = rag.search("carbassa", top_k=2)
print(f"G. search fet ({time.time()-t0:.1f}s), {len(result)} resultats", flush=True)

t0 = time.time()
answer = rag.ask("Quan sembrar carbassa?")
print(f"H. ask fet ({time.time()-t0:.1f}s)", flush=True)
print(f"   Resposta: {answer['answer'][:200]}", flush=True)
print(f"   Fonts: {[s['title'] for s in answer['sources']]}", flush=True)

print("\n✅ TOT OK!", flush=True)
