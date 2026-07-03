"""
ollama_test.py — Prova que Ollama funciona i l'API respon.

Ús:
  python ollama_test.py
  python ollama_test.py --model llama3.1
"""

import sys
import json
import urllib.request
import urllib.error
import time

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1"


def check_ollama_running():
    """Comprova que el servidor Ollama està actiu."""
    try:
        r = urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=2)
        return r.status == 200
    except (urllib.error.URLError, ConnectionError, OSError):
        return False


def list_models():
    """Llista els models disponibles."""
    r = urllib.request.urlopen(OLLAMA_URL + "/api/tags", timeout=5)
    data = json.loads(r.read())
    return [m["name"] for m in data.get("models", [])]


def ask_model(model, prompt, timeout=60):
    """Envia una pregunta al model i retorna la resposta."""
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 200,
        }
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    start = time.time()
    r = urllib.request.urlopen(req, timeout=timeout)
    data = json.loads(r.read())
    elapsed = time.time() - start
    return data.get("response", ""), elapsed


def main():
    print("=" * 60)
    print("Test d'Ollama — Assistent hortolà")
    print("=" * 60)

    # 1) Comprovar servidor
    print("\n[1] Comprovant servidor Ollama...")
    if not check_ollama_running():
        print("    ❌ Ollama no està actiu!")
        print("    Inicia'l amb: ollama serve &")
        sys.exit(1)
    print("    ✅ Servidor actiu a", OLLAMA_URL)

    # 2) Llistar models
    print("\n[2] Models disponibles:")
    models = list_models()
    for m in models:
        print(f"    • {m}")

    # 3) Provar el model per defecte
    model = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--model" else DEFAULT_MODEL
    if model not in models:
        print(f"\n    ⚠️  Model '{model}' no instal·lat. Usant '{models[0]}'")
        model = models[0] if models else None
        if not model:
            print("    ❌ Cap model instal·lat. Executa: ollama pull llama3.1")
            sys.exit(1)

    print(f"\n[3] Provant model '{model}'...")
    test_prompts = [
        "Hola, qui ets?",
        "Quines verdures es poden plantar a l'hort al juliol a la comarca d'Osona (Catalunya)?",
        "Explica breument què és el mildiu del tomàquet",
    ]
    for i, p in enumerate(test_prompts, 1):
        print(f"\n    Pregunta {i}: {p}")
        try:
            answer, elapsed = ask_model(model, p, timeout=120)
            preview = answer[:200] + ("..." if len(answer) > 200 else "")
            print(f"    Resposta ({elapsed:.1f}s):")
            print(f"    {preview}")
        except Exception as e:
            print(f"    ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("✅ Ollama funciona correctament!")
    print("=" * 60)


if __name__ == "__main__":
    main()
