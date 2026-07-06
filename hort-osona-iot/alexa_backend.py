#!/usr/bin/env python3
"""
alexa_backend.py — Backend Flask per la skill Alexa "Hort Osona".

Aquest servidor escolta les peticions d'Alexa (via Alexa Skills Kit) i
les redirigeix al sistema RAG local (Ollama + corpus .md).

Quan l'usuari diu "Alexa, pregunta a l'hort quan he de regar":
1. Alexa envia un JSON amb la pregunta a aquest servidor
2. El servidor consulta Ollama amb el corpus hort-osona
3. Retorna la resposta en format que Alexa pot llegir

Per executar:
    source venv/bin/activate
    python3 alexa_backend.py

Per fer-lo accessible des d'Alexa (cloud), cal:
    - Un servidor public (VPS, AWS, etc.) O
    - Tailscale + Funnel O
    - Un tunnel com ngrok (només per proves)
"""

import json
import logging
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("Falta flask. Instal·la: pip install flask")
    sys.exit(1)

# Configuracio
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "hermes3:latest")
PROJECT_DIR = Path(__file__).parent
CORPUS_DIR = PROJECT_DIR.parent  # Directori hort-osona/

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

app = Flask(__name__)


# ──────────── INTEGRACIO AMB RAG ────────────
def query_ollama(prompt: str, max_tokens: int = 250) -> Optional[str]:
    """Consulta directa a Ollama."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": max_tokens
        }
    }
    try:
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
            return data.get("response", "").strip()
    except (urllib.error.URLError, OSError) as e:
        log.error(f"Error amb Ollama: {e}")
        return None


def search_corpus(query: str, n: int = 3) -> list:
    """Cerca simple al corpus per trobar el context."""
    results = []
    if not CORPUS_DIR.exists():
        return results

    query_lower = query.lower()
    # Paraules clau per buscar
    keywords = [w for w in query_lower.split() if len(w) > 3][:5]

    for md_file in CORPUS_DIR.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            text_lower = text.lower()
            score = sum(text_lower.count(k) for k in keywords)
            if score > 0:
                results.append((score, md_file, text[:2000]))
        except Exception:
            continue

    results.sort(reverse=True, key=lambda x: x[0])
    return results[:n]


def build_prompt(question: str, context: str = "") -> str:
    """Construeix el prompt per a Ollama."""
    system = """Ets l'Alexa, l'assistent de l'hort d'Osona. Respon SEMPRE en catala,
de manera curta i practica (maxim 3-4 frases). Sigues amable i propera.

Si no saps la resposta, suggereix consultar el portal web hort-osona."""

    if context:
        return f"""{system}

Context del hort:
{context}

Pregunta: {question}

Resposta (curta, en catala, 2-3 frases):"""
    else:
        return f"""{system}

Pregunta: {question}

Resposta (curta, en catala, 2-3 frases):"""


def get_agronomic_answer(question: str) -> str:
    """Pipeline complet: cerca al corpus + consulta a Ollama."""
    # 1. Buscar context al corpus
    results = search_corpus(question, n=2)
    context = ""
    if results:
        for score, fpath, text in results:
            context += f"\nDe {fpath.stem}:\n{text}\n"

    # 2. Si no hem trobat context, usar pregunta directa
    if not context:
        context = "No s'ha trobat context especific, utilitza el teu coneixement general sobre horticultura ecologica."

    # 3. Construir prompt i consultar Ollama
    prompt = build_prompt(question, context)
    answer = query_ollama(prompt, max_tokens=200)

    if not answer:
        return "Tinc problemes per connectar amb el sistema. Torna-ho a provar en uns moments."

    return answer


# ──────────── HANDLERS D'INTENTS ────────────
def handle_pregunta(question: str) -> str:
    """Intent: pregunta lliure."""
    if not question:
        return "Quina pregunta vols fer a l'hort?"
    return get_agronomic_answer(question)


def handle_estat_hort() -> str:
    """Intent: estat general de l'hort."""
    return get_agronomic_answer(
        "Fes-me un resum breu de l'estat general d'un hort ecologic "
        "a Osona a l'estiu: reg, plagues mes comuns, consells practics."
    )


def handle_quan_sembrar(cultiu: str) -> str:
    """Intent: quan sembrar un cultiu."""
    if not cultiu:
        return "De quin cultiu vols saber quan sembrar?"
    return get_agronomic_answer(f"Quan es l'epoca adequada per sembrar {cultiu} a la comarca d'Osona, Catalunya?")


def handle_quan_collir(cultiu: str) -> str:
    """Intent: quan collir un cultiu."""
    if not cultiu:
        return "De quin cultiu vols saber quan collir?"
    return get_agronomic_answer(f"Quan es l'epoca de collita de {cultiu} a Osona?")


def handle_com_combat(plaga: str) -> str:
    """Intent: com combatre una plaga."""
    if not plaga:
        return "Quina plaga vols combatre?"
    return get_agronomic_answer(f"Com puc combatre {plaga} de manera ecologica al meu hort a Osona?")


def handle_quan_regar() -> str:
    """Intent: quan regar."""
    return get_agronomic_answer(
        "Quan i quant he de regar l'hort a l'estiu a la comarca d'Osona? "
        "Considera temperatures altes i possibles sequeres."
    )


def handle_help() -> str:
    """Intent: ajuda."""
    return (
        "Pots dir coses com: "
        "Alexa, pregunta a l'hort quan he de sembrar tomàquets. "
        "Alexa, pregunta a l'hort com combatre el mildiu. "
        "Alexa, pregunta a l'hort quan he de regar. "
        "O simplement: Alexa, pregunta a l'hort sobre cols."
    )


# ──────────── WEBHOOK D'ALEXA ────────────
@app.route("/alexa", methods=["POST"])
def alexa_webhook():
    """Rep les peticions d'Alexa Skills Kit."""
    try:
        body = request.get_json()
    except Exception as e:
        log.error(f"Error llegint JSON: {e}")
        return jsonify({"error": "Invalid JSON"}), 400

    request_type = body.get("request", {}).get("type")
    log.info(f"Rebut request type: {request_type}")

    if request_type == "LaunchRequest":
        # Quan l'usuari obre la skill sense pregunta
        speech = "Hola! Soc l'Alexa de l'hort d'Osona. Que vols saber avui?"
        return build_alexa_response(speech, end_session=False)

    elif request_type == "IntentRequest":
        intent = body["request"]["intent"]
        intent_name = intent["name"]
        slots = intent.get("slots", {})

        log.info(f"Intent: {intent_name}, slots: {slots}")

        # Extreure valors dels slots
        def get_slot(name):
            slot = slots.get(name, {})
            value = slot.get("value", "")
            return value if value else ""

        if intent_name == "PreguntaHortIntent":
            pregunta = get_slot("Pregunta")
            speech = handle_pregunta(pregunta)
        elif intent_name == "EstatHortIntent":
            speech = handle_estat_hort()
        elif intent_name == "QuanSembrarIntent":
            cultiu = get_slot("Cultiu")
            speech = handle_quan_sembrar(cultiu)
        elif intent_name == "QuanCollirIntent":
            cultiu = get_slot("Cultiu")
            speech = handle_quan_collir(cultiu)
        elif intent_name == "ComCombatentIntent":
            plaga = get_slot("Plaga")
            speech = handle_com_combat(plaga)
        elif intent_name == "QuanRegarIntent":
            speech = handle_quan_regar()
        elif intent_name == "HelpIntent":
            speech = handle_help()
        elif intent_name in ("CancelIntent", "StopIntent"):
            speech = "Adeu! Bon hort!"
            return build_alexa_response(speech, end_session=True)
        elif intent_name == "NavigateHomeIntent":
            speech = "D'acord. Que vols saber?"
            return build_alexa_response(speech, end_session=False)
        else:
            # Fallback
            speech = "No t'he entes. Pots repetir la pregunta?"
            return build_alexa_response(speech, end_session=False)

        return build_alexa_response(speech, end_session=True)

    elif request_type == "SessionEndedRequest":
        return "", 200

    return "", 400


def build_alexa_response(speech: str, end_session: bool = True) -> dict:
    """Construeix la resposta JSON per Alexa."""
    return jsonify({
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech
            },
            "shouldEndSession": end_session
        }
    })


@app.route("/health", methods=["GET"])
def health():
    """Endpoint de salut per comprovar que el backend funciona."""
    return jsonify({
        "status": "ok",
        "ollama_url": OLLAMA_URL,
        "ollama_model": OLLAMA_MODEL,
        "corpus_dir": str(CORPUS_DIR),
        "timestamp": datetime.now().isoformat()
    })


@app.route("/", methods=["GET"])
def index():
    """Pagina d'informacio."""
    return """
    <h1>🌱 Hort Osona — Alexa Backend</h1>
    <p>Backend Flask per la skill Alexa "Hort Osona".</p>
    <h2>Endpoints:</h2>
    <ul>
        <li><code>POST /alexa</code> — Webhook per Alexa Skills Kit</li>
        <li><code>GET /health</code> — Comprovar l'estat</li>
    </ul>
    <h2>Intents suportats:</h2>
    <ul>
        <li>PreguntaHortIntent (pregunta lliure)</li>
        <li>EstatHortIntent (resum general)</li>
        <li>QuanSembrarIntent (quan sembrar X)</li>
        <li>QuanCollirIntent (quan collir X)</li>
        <li>ComCombatentIntent (com combatre X)</li>
        <li>QuanRegarIntent (consells de reg)</li>
    </ul>
    """


if __name__ == "__main__":
    print("🌱 Hort Osona — Alexa Backend")
    print("================================")
    print(f"Ollama: {OLLAMA_URL} ({OLLAMA_MODEL})")
    print(f"Corpus: {CORPUS_DIR}")
    print()
    print("Escoltant a http://0.0.0.0:5000")
    print("Endpoints:")
    print("  POST /alexa    - Webhook Alexa")
    print("  GET  /health   - Estat del servei")
    print("  GET  /         - Documentacio")
    print()
    print("Per Alexa, exposa aquest servidor amb un tunnel o VPS.")
    print()

    app.run(host="0.0.0.0", port=5000, debug=False)
