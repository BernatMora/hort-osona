#!/bin/bash
# ============================================================================
#  setup-pi.sh — Setup complet de la Raspberry Pi per a Hort Osona IoT
#  Execució: chmod +x setup-pi.sh && ./setup-pi.sh
#  Temps aproximat: 10-15 min
# ============================================================================

set -e  # Atura si qualsevol comanda falla

echo "🌱 Hort Osona IoT — Setup de la Raspberry Pi"
echo "================================================"
echo ""

# 1) Actualitzar el sistema
echo "📦 [1/8] Actualitzant sistema..."
sudo apt update && sudo apt upgrade -y
echo "    ✅ Sistema actualitzat"

# 2) Instal·lar dependències
echo ""
echo "📦 [2/8] Instal·lant dependències..."
sudo apt install -y \
    mosquitto \
    mosquitto-clients \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    sqlite3 \
    bluez \
    bluetooth \
    libbluetooth-dev
echo "    ✅ Dependències instal·lades"

# 3) Crear usuari hort
echo ""
echo "👤 [3/8] Configurant usuari hort..."
if ! id "hort" &>/dev/null; then
    sudo useradd -m -s /bin/bash hort
    sudo passwd hort
    sudo usermod -aG sudo,dialout,gpio,bluetooth hort
    echo "    ✅ Usuari 'hort' creat"
else
    echo "    ⏭️  Usuari 'hort' ja existeix"
fi

# 4) Configurar Mosquitto (MQTT broker)
echo ""
echo "📡 [4/8] Configurant Mosquitto MQTT..."
sudo tee /etc/mosquitto/conf.d/hort.conf > /dev/null <<'EOF'
# Hort Osona IoT — MQTT broker
listener 1883
allow_anonymous true
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
EOF
sudo systemctl enable mosquitto
sudo systemctl restart mosquitto
echo "    ✅ Mosquitto actiu a port 1883"

# 5) Crear estructura del projecte
echo ""
echo "📂 [5/8] Creant estructura del projecte..."
sudo mkdir -p /opt/hort-osona-iot/{backend,bridge,data,logs}
sudo chown -R hort:hort /opt/hort-osona-iot

# Copiar fitxers del projecte (assumint que ja existeixen a ~/hort-osona-iot)
if [ -d "$HOME/hort-osona-iot" ]; then
    cp -r $HOME/hort-osona-iot/* /opt/hort-osona-iot/
    sudo chown -R hort:hort /opt/hort-osona-iot
    echo "    ✅ Fitxers copiats a /opt/hort-osona-iot/"
else
    echo "    ⚠️  No s'ha trobat ~/hort-osona-iot — caldrà clonar el repo"
fi

# 6) Crear entorn virtual Python
echo ""
echo "🐍 [6/8] Configurant entorn Python..."
sudo -u hort python3 -m venv /opt/hort-osona-iot/venv
sudo -u hort /opt/hort-osona-iot/venv/bin/pip install --upgrade pip
sudo -u hort /opt/hort-osona-iot/venv/bin/pip install \
    paho-mqtt \
    fastapi \
    uvicorn[standard] \
    bleak \
    miflora
echo "    ✅ Entorn Python configurat"

# 7) Configurar servei systemd per al backend
echo ""
echo "⚙️ [7/8] Configurant servei systemd..."
sudo tee /etc/systemd/system/hort-backend.service > /dev/null <<'EOF'
[Unit]
Description=Hort Osona IoT — Backend
After=network.target mosquitto.service
Wants=mosquitto.service

[Service]
Type=simple
User=hort
Group=hort
WorkingDirectory=/opt/hort-osona-iot/backend
Environment="PATH=/opt/hort-osona-iot/venv/bin"
ExecStart=/opt/hort-osona-iot/venv/bin/python /opt/hort-osona-iot/backend/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable hort-backend
echo "    ✅ Servei hort-backend configurat"

# 8) Configurar Tailscale (opcional — per accedir des de fora)
echo ""
echo "🔒 [8/8] Configurant Tailscale (opcional)..."
if ! command -v tailscale &> /dev/null; then
    curl -fsSL https://tailscale.com/install.sh | sh
    echo "    ✅ Tailscale instal·lat — caldrà autenticar amb: sudo tailscale up"
else
    echo "    ⏭️  Tailscale ja instal·lat"
fi

echo ""
echo "================================================"
echo "✅ Setup complet!"
echo ""
echo "📋 Propers passos:"
echo "   1. Autenticar Tailscale:    sudo tailscale up"
echo "   2. Verificar MQTT:          mosquitto_sub -h localhost -t 'hort/#' -v"
echo "   3. Iniciar backend:         sudo systemctl start hort-backend"
echo "   4. Veure logs:              sudo journalctl -u hort-backend -f"
echo "   5. Accedir a l'API:         http://hortpi.local:8000/sensors"
echo ""
echo "🌱 Bon hort!"
