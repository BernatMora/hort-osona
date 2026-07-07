#!/bin/bash
# ============================================================================
#  setup-pi.sh — Setup COMPLET de la Raspberry Pi per a Hort Osona IoT
#  Execució: chmod +x setup-pi.sh && ./setup-pi.sh
#  Temps aproximat: 15-20 min
#  Inclou: LoRa SX1262, Supabase, Ollama (opcional), Tailscale
# ============================================================================

set -e  # Atura si qualsevol comanda falla

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🌱 Hort Osona IoT — Setup de la Raspberry Pi"
echo "=============================================="
echo ""

# Verificar que estem a la RPi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null && [ ! -f /etc/rpi-issue ]; then
    echo -e "${YELLOW}⚠️  Avis: Sembla que no estem a una Raspberry Pi${NC}"
    echo "   Continuant igualment, pero algunes coses poden no funcionar..."
    echo ""
fi

# Demanar confirmacio
read -p "Continuar amb el setup? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Setup cancel·lat."
    exit 1
fi

# 1) Actualitzar el sistema
echo ""
echo -e "${GREEN}📦 [1/10] Actualitzant sistema...${NC}"
sudo apt update && sudo apt upgrade -y
echo -e "    ${GREEN}✅ Sistema actualitzat${NC}"

# 2) Instal·lar dependencies del sistema
echo ""
echo -e "${GREEN}📦 [2/10] Instal·lant dependencies del sistema...${NC}"
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    sqlite3 \
    libatlas-base-dev \
    libopenjp2-7 \
    libtiff5 \
    i2c-tools \
    spi-tools
echo -e "    ${GREEN}✅ Dependencies instal·lades${NC}"

# 3) Habilitar SPI i I2C
echo ""
echo -e "${GREEN}⚙️ [3/10] Habilitant SPI i I2C...${NC}"
if ! grep -q "^dtparam=spi=on" /boot/config.txt; then
    echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
    echo "    SPI habilitat"
fi
if ! grep -q "^dtparam=i2c_arm=on" /boot/config.txt; then
    echo "dtparam=i2c_arm=on" | sudo tee -a /boot/config.txt
    echo "    I2C habilitat"
fi
echo -e "    ${GREEN}✅ SPI i I2C habilitats (reboot necessari per activar)${NC}"

# 4) Instal·lar Ollama (LLM local)
echo ""
echo -e "${GREEN}🤖 [4/10] Instal·lant Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "    ${GREEN}✅ Ollama instal·lat${NC}"
    echo "    Descarregant model hermes3 (pot trigar 5-10 min)..."
    sudo systemctl start ollama
    sleep 5
    ollama pull hermes3:latest
    echo -e "    ${GREEN}✅ Model hermes3 descarregat${NC}"
else
    echo -e "    ${YELLOW}⏭️  Ollama ja instal·lat${NC}"
fi

# 5) Crear estructura de directoris
echo ""
echo -e "${GREEN}📂 [5/10] Creant estructura de directoris...${NC}"
sudo mkdir -p /opt/hort-osona-iot/{backend,bridge,data,logs,venv}
sudo chown -R $USER:$USER /opt/hort-osona-iot
echo -e "    ${GREEN}✅ Estructura creada a /opt/hort-osona-iot/${NC}"

# 6) Crear entorn virtual Python
echo ""
echo -e "${GREEN}🐍 [6/10] Configurant entorn Python...${NC}"
python3 -m venv /opt/hort-osona-iot/venv
source /opt/hort-osona-iot/venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install \
    supabase \
    paho-mqtt \
    fastapi \
    "uvicorn[standard]" \
    requests \
    RPi.GPIO \
    spidev \
    lgpio \
    python-telegram-bot \
    python-dotenv
echo -e "    ${GREEN}✅ Entorn Python configurat${NC}"

# 7) Copiar fitxers del projecte
echo ""
echo -e "${GREEN}📋 [7/10] Copiant fitxers del projecte...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "$SCRIPT_DIR" ]; then
    cp -r $SCRIPT_DIR/backend/* /opt/hort-osona-iot/backend/
    cp -r $SCRIPT_DIR/bridge/* /opt/hort-osona-iot/bridge/ 2>/dev/null || true
    cp $SCRIPT_DIR/rag.py /opt/hort-osona-iot/ 2>/dev/null || true
    cp $SCRIPT_DIR/telegram_bot.py /opt/hort-osona-iot/ 2>/dev/null || true
    cp $SCRIPT_DIR/.env.example /opt/hort-osona-iot/ 2>/dev/null || true

    # Crear .env buit si no existeix (l'usuari l'ha d'omplir)
    if [ ! -f /opt/hort-osona-iot/.env ]; then
        cp $SCRIPT_DIR/.env.example /opt/hort-osona-iot/.env
        chmod 600 /opt/hort-osona-iot/.env
        echo -e "    ${YELLOW}⚠️  Creat .env buit. Recorda posar-hi el TELEGRAM_BOT_TOKEN${NC}"
    fi
    echo -e "    ${GREEN}✅ Fitxers copiats${NC}"
else
    echo -e "    ${YELLOW}⚠️  Cal copiar manualment des de $SCRIPT_DIR${NC}"
fi

# 8) Configurar servei systemd
echo ""
echo -e "${GREEN}⚙️ [8/10] Configurant serveis systemd...${NC}"

# Servei: receptor LoRa
sudo tee /etc/systemd/system/hort-lora-receiver.service > /dev/null <<'EOF'
[Unit]
Description=Hort Osona IoT — Receptor LoRa
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/hort-osona-iot
Environment="PATH=/opt/hort-osona-iot/venv/bin"
Environment="OLLAMA_URL=http://localhost:11434"
ExecStart=/opt/hort-osona-iot/venv/bin/python /opt/hort-osona-iot/backend/lora_receiver.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Servei: API Chat
sudo tee /etc/systemd/system/hort-api-chat.service > /dev/null <<'EOF'
[Unit]
Description=Hort Osona IoT — API Chat (FastAPI)
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/hort-osona-iot
Environment="PATH=/opt/hort-osona-iot/venv/bin"
ExecStart=/opt/hort-osona-iot/venv/bin/python -m uvicorn backend.api_chat:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Servei: Ollama
sudo tee /etc/systemd/system/ollama.service > /dev/null <<'EOF'
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=exec
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="HOME=/usr/share/ollama"

[Install]
WantedBy=multi-user.target
EOF

# Servei: Bot de Telegram (carrega .env amb TELEGRAM_BOT_TOKEN)
if [ -f $SCRIPT_DIR/systemd/hort-osona-telegram.service ]; then
    sudo cp $SCRIPT_DIR/systemd/hort-osona-telegram.service /etc/systemd/system/
    echo -e "    ${GREEN}✅ Servei bot Telegram instal·lat${NC}"
fi

sudo systemctl daemon-reload
echo -e "    ${GREEN}✅ Serveis creats (no activats encara)${NC}"

# 9) Configurar Tailscale (opcional, per accés remot)
echo ""
echo -e "${GREEN}🔒 [9/10] Configurant Tailscale (opcional)...${NC}"
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
    echo -e "    ${GREEN}✅ Tailscale instal·lat${NC}"
    echo -e "    ${YELLOW}Per autenticar: sudo tailscale up${NC}"
else
    echo -e "    ${YELLOW}⏭️  Tailscale ja instal·lat${NC}"
fi

# 10) Verificar instal·lacio
echo ""
echo -e "${GREEN}🔍 [10/10] Verificant instal·lacio...${NC}"
echo ""

# Comprovar Python
PYTHON_VERSION=$(python3 --version 2>&1)
echo "  Python: $PYTHON_VERSION"

# Comprovar SPI
if ls /dev/spidev* 2>/dev/null; then
    echo "  SPI: ✅ Disponible"
else
    echo -e "  SPI: ${YELLOW}⚠️  No disponible (reboot necessari)${NC}"
fi

# Comprovar Ollama
if systemctl is-active --quiet ollama; then
    echo "  Ollama: ✅ Actiu"
else
    echo "  Ollama: ⏸️  Inactiu (s'iniciarà al reboot)"
fi

# Comprovar el codi
if [ -f /opt/hort-osona-iot/backend/lora_receiver.py ]; then
    echo "  Codi: ✅ Instal·lat a /opt/hort-osona-iot/"
else
    echo "  Codi: ❌ No trobat"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}✅ Setup complet!${NC}"
echo ""
echo "📋 Propers passos:"
echo ""
echo "  1. Configurar Supabase (crear compte a supabase.com):"
echo "     export SUPABASE_URL=https://xxx.supabase.co"
echo "     export SUPABASE_KEY=eyJ..."
echo "     Afegir-les a /etc/environment o .bashrc"
echo ""
echo "  2. Executar l'schema SQL:"
echo "     psql \$DATABASE_URL < backend/supabase_schema.sql"
echo ""
echo "  3. Autenticar Tailscale (opcional):"
echo "     sudo tailscale up"
echo ""
echo "  4. Activar els serveis:"
echo "     sudo systemctl enable --now ollama"
echo "     sudo systemctl enable --now hort-lora-receiver"
echo "     sudo systemctl enable --now hort-api-chat"
echo "     sudo systemctl enable --now hort-osona-telegram"
echo ""
echo "  5. Configurar el bot de Telegram (important!):"
echo "     sudo nano /opt/hort-osona-iot/.env"
echo "     # Afegeix el teu TELEGRAM_BOT_TOKEN"
echo "     sudo systemctl restart hort-osona-telegram"
echo ""
echo "  6. Verificar que tot funciona:"
echo "     sudo systemctl status hort-lora-receiver"
echo "     sudo journalctl -u hort-lora-receiver -f"
echo "     curl http://localhost:8001/health"
echo ""
echo "  6. REINICIAR la RPi (per activar SPI/I2C):"
echo "     sudo reboot"
echo ""
echo "🌱 Bon hort!"
