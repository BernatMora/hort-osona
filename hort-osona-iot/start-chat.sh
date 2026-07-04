#!/usr/bin/env bash
# start-chat.sh — Arrenca el backend de xat (port 8001)
# Assegura que Ollama està actiu, instal·la deps si cal, i arrenca l'API

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

PORT=8001
VENV_DIR="$DIR/.venv"

echo "🌱 Hort Osona — Arrencant el backend de xat"
echo "==========================================="

# 1) Comprovar/Obrir Ollama
if ! curl -s -m 3 http://localhost:11434/ >/dev/null 2>&1; then
  echo "⚠️  Ollama no està actiu. Obrint..."
  open -a Ollama
  sleep 5
  if ! curl -s -m 3 http://localhost:11434/ >/dev/null 2>&1; then
    echo "❌ Ollama no respon. Assegura't que estigui instal·lat:"
    echo "   brew install ollama  &&  ollama serve"
    exit 1
  fi
fi
echo "✅ Ollama actiu (port 11434)"

# Mostrar models disponibles
MODELS=$(curl -s http://localhost:11434/api/tags 2>/dev/null | grep -oE '"name":"[^"]+"' | cut -d'"' -f4 | tr '\n' ' ')
echo "📦 Models disponibles: $MODELS"

# 2) Crear venv si no existeix
if [ ! -d "$VENV_DIR" ]; then
  echo "🔧 Creant entorn virtual Python..."
  python3 -m venv "$VENV_DIR"
fi

# 3) Instal·lar deps
echo "📚 Instal·lant/verificant dependències..."
"$VENV_DIR/bin/pip" install -q --upgrade pip
"$VENV_DIR/bin/pip" install -q fastapi uvicorn pydantic requests 2>&1 | tail -3

# 4) Comprovar que el port estigui lliure
if lsof -i :$PORT 2>/dev/null | grep -q LISTEN; then
  echo "⚠️  Port $PORT ja està en ús. Vols continuar igual? (s/n)"
  read -r ans
  if [ "$ans" != "s" ] && [ "$ans" != "S" ]; then
    exit 1
  fi
fi

# 5) Arrencar API
echo ""
echo "🚀 Arrencant API de xat a http://localhost:$PORT"
echo "   (Prem Ctrl+C per aturar)"
echo "==========================================="
exec "$VENV_DIR/bin/python" -m uvicorn backend.api_chat:app --host 0.0.0.0 --port $PORT --reload
