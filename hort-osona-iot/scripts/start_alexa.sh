#!/bin/bash
# start_alexa.sh — Arrenca el backend Alexa i l'exposa amb Tailscale Funnel
#
# Ús:
#   ./start_alexa.sh           # Arrenca i exposa (mode complet)
#   ./start_alexa.sh local     # Només arrenca el backend (port 5050)
#
# Requisits:
#   - Ollama corrent (ollama serve)
#   - Tailscale instal·lat i autenticat
#   - Tailscale Funnel activat (https://tailscale.com/kb/1223/funnel/)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$HOME/Library/Logs/hort-osona-alexa"
mkdir -p "$LOG_DIR"

PORT=5050
LOG_FILE="$LOG_DIR/alexa_backend.log"
TAILSCALE_LOG="$LOG_DIR/tailscale-funnel.log"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🌱 Hort Osona — Alexa Backend Starter${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1. Comprovar Ollama
echo -e "${BLUE}[1/5]${NC} Comprovant Ollama..."
if ! curl -s --max-time 3 http://localhost:11434/api/version > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Ollama no està corrent. Arrencant...${NC}"
    ollama serve > "$LOG_DIR/ollama.log" 2>&1 &
    sleep 5
    if ! curl -s --max-time 3 http://localhost:11434/api/version > /dev/null 2>&1; then
        echo -e "${RED}✗ No s'ha pogut arrencar Ollama${NC}"
        exit 1
    fi
fi
OLLAMA_VERSION=$(curl -s http://localhost:11434/api/version | python3 -c "import json,sys; print(json.load(sys.stdin)['version'])" 2>/dev/null)
echo -e "${GREEN}✓ Ollama v$OLLAMA_VERSION${NC}"

# 2. Comprovar Python i Flask
echo -e "${BLUE}[2/5]${NC} Comprovant Python i Flask..."
PYTHON=/Users/bernatmorasanglas/.hermes/hermes-agent/venv/bin/python
if [ ! -f "$PYTHON" ]; then
    PYTHON=$(which python3)
fi
if ! $PYTHON -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Flask no instal·lat. Instal·lant...${NC}"
    $PYTHON -m pip install flask
fi
echo -e "${GREEN}✓ Python + Flask${NC}"

# 3. Comprovar si el port esta lliure
echo -e "${BLUE}[3/5]${NC} Comprovant port $PORT..."
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port $PORT ocupat. Alliberant...${NC}"
    lsof -ti :$PORT | xargs kill -9 2>/dev/null || true
    sleep 2
fi
echo -e "${GREEN}✓ Port $PORT lliure${NC}"

# 4. Arrencar el backend
echo -e "${BLUE}[4/5]${NC} Arrencant backend Flask..."
cd "$PROJECT_DIR"
ALEXA_PORT=$PORT nohup $PYTHON alexa_backend.py > "$LOG_FILE" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$LOG_DIR/backend.pid"
sleep 3

# Verificar
if ! curl -s --max-time 3 http://localhost:$PORT/health > /dev/null 2>&1; then
    echo -e "${RED}✗ Backend no ha arrencat correctament${NC}"
    echo "Mira el log: tail -f $LOG_FILE"
    exit 1
fi
echo -e "${GREEN}✓ Backend corrent (PID $BACKEND_PID)${NC}"
echo "   Log: $LOG_FILE"

# Si l'usuari nomes vol local, acabem aqui
if [ "${1:-}" = "local" ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Backend actiu a http://localhost:$PORT${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo "Prova: curl http://localhost:$PORT/health"
    echo "Per parar: kill \$(cat $LOG_DIR/backend.pid)"
    exit 0
fi

# 5. Tailscale Funnel
echo -e "${BLUE}[5/5]${NC} Configurant Tailscale Funnel..."
if ! tailscale status >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Tailscale no està autenticat.${NC}"
    echo ""
    echo "Obre https://login.tailscale.com/admin/console i segueix les instruccions."
    echo "O executa: sudo tailscale up"
    exit 1
fi

# Comprovar si Funnel está activat
if ! tailscale funnel --bg $PORT > "$TAILSCALE_LOG" 2>&1; then
    echo -e "${YELLOW}⚠️  Funnel pot necessitar activació:${NC}"
    echo "Ves a https://login.tailscale.com/admin/acls/file i afegeix:"
    echo '  "funnel": true'
    echo ""
    echo "O simplement activa'l per al teu dispositiu."
    echo ""
    echo "Mira el log: tail -f $TAILSCALE_LOG"
    exit 1
fi

sleep 2
FUNNEL_URL=$(tailscale funnel --json 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for uid, info in data.get('Funnel', {}).items():
        for port, listeners in info.get('Listeners', {}).items():
            for listener in listeners:
                if listener.get('https') and int(port) == $PORT:
                    print(listener['https'].rstrip('/') + '/alexa')
                    sys.exit(0)
except Exception as e:
    pass
" 2>/dev/null)

if [ -z "$FUNNEL_URL" ]; then
    echo -e "${YELLOW}⚠️  No s'ha pogut obtenir la URL de Funnel${NC}"
    echo "Comprova: tailscale funnel status"
    exit 1
fi

echo -e "${GREEN}✓ Tailscale Funnel actiu${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 TOT LLEST!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "URL pública del backend:"
echo -e "${BLUE}$FUNNEL_URL${NC}"
echo ""
echo "Proxims passos:"
echo "1. Obre https://developer.amazon.com/alexa/console/ask"
echo "2. Crea una skill 'Hort Osona'"
echo "3. Interaction Model -> JSON Editor -> enganxa interaction-model.json"
echo "4. Endpoint -> HTTPS -> enganxa: $FUNNEL_URL"
echo "5. Build Model"
echo "6. A l'app Alexa del mobil: Skills -> Dev Skills -> Hort Osona -> Enable"
echo "7. Digues: 'Eco, pregunta a l'hort quan he de regar'"
echo ""
echo "Per parar-ho tot:"
echo "  kill \$(cat $LOG_DIR/backend.pid)"
echo "  tailscale funnel --off $PORT"
