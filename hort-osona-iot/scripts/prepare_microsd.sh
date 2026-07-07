#!/bin/bash
# prepare_microsd.sh — Prepara una microSD Raspberry Pi amb WiFi i SSH
#
# Usage:
#   1. Inserir la microSD al Mac
#   2. Executar: ./prepare_microsd.sh
#   3. Quan demani, escriure el nom WiFi i la contrasenya
#
# Segur: les dades no es guarden enlloc, nomes a la microSD

set -e

BOOT_MOUNT="/Volumes/bootfs"
WPA_FILE="$BOOT_MOUNT/wpa_supplicant.conf"
SSH_FILE="$BOOT_MOUNT/ssh"
COUNTRY="ES"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🌱 Hort Osona — Prep de microSD${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1. Comprovar que la particio boot existeix
if [ ! -d "$BOOT_MOUNT" ]; then
    echo -e "${RED}✗ No trobo la partició $BOOT_MOUNT${NC}"
    echo "Assegura't que la microSD esta inserida al Mac"
    exit 1
fi

echo -e "${GREEN}✓ Partició boot trobada: $BOOT_MOUNT${NC}"
echo ""

# 2. Demanar el nom WiFi
echo -e "${YELLOW}Quin es el nom de la teva xarxa WiFi (SSID)?${NC}"
read -p "SSID: " WIFI_SSID
if [ -z "$WIFI_SSID" ]; then
    echo -e "${RED}✗ El nom WiFi no pot ser buit${NC}"
    exit 1
fi

# 3. Demanar la contrasenya WiFi
echo ""
echo -e "${YELLOW}Contrasenya de la xarxa WiFi:${NC}"
read -s -p "Contrasenya: " WIFI_PASS
echo ""
if [ -z "$WIFI_PASS" ]; then
    echo -e "${RED}✗ La contrasenya no pot ser buida${NC}"
    exit 1
fi

# 4. Crear wpa_supplicant.conf
echo ""
echo -e "${BLUE}Creant wpa_supplicant.conf...${NC}"

cat > "$WPA_FILE" <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=$COUNTRY
network={
    ssid="$WIFI_SSID"
    psk="$WIFI_PASS"
    key_mgmt=WPA-PSK
}
EOF

if [ -f "$WPA_FILE" ]; then
    echo -e "${GREEN}✓ Creat: $WPA_FILE${NC}"
else
    echo -e "${RED}✗ Error creant wpa_supplicant.conf${NC}"
    exit 1
fi

# 5. Crear fitxer ssh (buit)
echo ""
echo -e "${BLUE}Creant fitxer ssh per activar SSH...${NC}"
touch "$SSH_FILE"

if [ -f "$SSH_FILE" ]; then
    echo -e "${GREEN}✓ Creat: $SSH_FILE${NC}"
else
    echo -e "${RED}✗ Error creant ssh${NC}"
    exit 1
fi

# 6. Resum
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Tot llest!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Fitxers creats a la microSD:"
echo "  - $WPA_FILE (configuracio WiFi)"
echo "  - $SSH_FILE (activa SSH)"
echo ""
echo -e "${YELLOW}Proper passos:${NC}"
echo "1. ${BLUE}Desmunta la microSD${NC} (al Finder: clic dret a bootfs -> Expulsar)"
echo "2. ${BLUE}Treu la microSD${NC} del Mac"
echo "3. ${BLUE}Munta el HAT${NC} a la RPi (amb la RPi DESENDOLLADA)"
echo "4. ${BLUE}Insereix la microSD${NC} a la RPi"
echo "5. ${BLUE}Endolla${NC} el cable USB-C"
echo "6. Espera 60-90 segons mentre arrenca"
echo "7. Al Mac: ${BLUE}ssh bernat@hortosona.local${NC}"
echo ""
echo "Si tens problemes, comprova:"
echo "  - El LED verd de la RPi ha de parpellejar (activitat)"
echo "  - El teu Mac ha d'estar a la mateixa xarxa WiFi"
echo "  - Si 'hortosona.local' no funciona, prova amb la IP (192.168.1.XXX)"
