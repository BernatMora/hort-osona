#!/bin/bash
# update_wpa_for_hotspot.sh — Actualitza el wpa_supplicant pel hotspot del iPhone
#
# Usage:
#   1. Activa el hotspot al iPhone (Settings -> Personal Hotspot)
#   2. Executa aquest script
#   3. Quan et demani, fica el nom exacte del iPhone i la contrasenya

# NO usem `set -e` perque alguns fitxers macOS estan protegits
# i volem continuar encara que no es puguin esborrar tots

BOOT_MOUNT="/Volumes/bootfs"
WPA_FILE="$BOOT_MOUNT/wpa_supplicant.conf"
SSH_FILE="$BOOT_MOUNT/ssh"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Comprovar que la microSD esta muntada
if [ ! -d "$BOOT_MOUNT" ]; then
    echo -e "${RED}✗ La microSD no esta muntada a $BOOT_MOUNT${NC}"
    echo "Insereix la microSD al Mac primer"
    exit 1
fi

# 1. Netejar fitxers macOS brossa (NO PARAR si algun falla)
echo -e "${BLUE}[1/4] Netejant fitxers macOS brossa (no critics)...${NC}"
for pattern in "._*" ".DS_Store" ".fseventsd" ".Trashes" ".TemporaryItems"; do
    # Usar -f perque no falli si no existeix
    for f in $BOOT_MOUNT/$pattern; do
        [ -e "$f" ] || continue
        rm -rf "$f" 2>/dev/null && echo "  ✓ Esborrat: $(basename "$f")" || true
    done
done
# .Spotlight-V100 pot ser un directori protegit - intentar pero no parar
rm -rf "$BOOT_MOUNT/.Spotlight-V100" 2>/dev/null && echo "  ✓ Esborrat: .Spotlight-V100" || echo "  (Spotlight protegit, no es critic)"

# 2. Assegurar que existeix el fitxer ssh
echo -e "${BLUE}[2/4] Assegurant que existeix el fitxer ssh...${NC}"
if [ -f "$SSH_FILE" ]; then
    echo "  ✓ Ja existeix"
else
    touch "$SSH_FILE"
    echo "  ✓ Creat: $SSH_FILE"
fi

# 3. Demanar dades del iPhone
echo -e "${BLUE}[3/4] Configurant wpa_supplicant pel hotspot del iPhone${NC}"
echo ""
echo -e "${YELLOW}Primer, activa el Personal Hotspot al teu iPhone:${NC}"
echo "  Settings -> Personal Hotspot -> Allow Others to Join"
echo "  Posa una contrasenya de 8+ caracters"
echo "  Apunta el NOM exacte del iPhone (per defecte: 'iPhone de Bernat')"
echo ""
echo -e "${YELLOW}Quin es el nom exacte del teu iPhone?${NC}"
read -p "Nom (SSID): " IPHONE_SSID

if [ -z "$IPHONE_SSID" ]; then
    echo -e "${RED}✗ El nom no pot ser buit${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Contrasenya del hotspot (minim 8 caracters):${NC}"
read -s -p "Contrasenya: " IPHONE_PASS
echo ""

if [ -z "$IPHONE_PASS" ]; then
    echo -e "${RED}✗ La contrasenya no pot ser buida${NC}"
    exit 1
fi

if [ "${#IPHONE_PASS}" -lt 8 ]; then
    echo -e "${RED}✗ La contrasenya ha de tenir minim 8 caracters${NC}"
    echo "  Actual: ${#IPHONE_PASS} caracters"
    exit 1
fi

# 4. Crear el nou wpa_supplicant.conf
echo ""
echo -e "${BLUE}[4/4] Creant wpa_supplicant.conf...${NC}"
cat > "$WPA_FILE" <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=ES
network={
    ssid="$IPHONE_SSID"
    psk="$IPHONE_PASS"
    key_mgmt=WPA-PSK
}
EOF

if [ -f "$WPA_FILE" ]; then
    echo -e "${GREEN}✓ Creat: $WPA_FILE${NC}"
    echo ""
    echo "Contingut:"
    cat "$WPA_FILE"
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ TOT LLEST!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Propers passos:"
    echo "1. Desmunta la microSD (Finder -> clic dret bootfs -> Expulsar)"
    echo "2. TREU la microSD del Mac"
    echo "3. DESENDOLLA la RPi (treu USB-C)"
    echo "4. POSA la microSD a la RPi"
    echo "5. ENDOLLA el USB-C"
    echo "6. ESPERA 2-3 minuts (LED verd parpellejant)"
    echo "7. AL MAC: ssh bernat@hortosona.local"
    echo ""
    echo -e "${YELLOW}IMPORTANT: el iPhone ha d'estar a prop amb el HOTSPOT ACTIU!${NC}"
else
    echo -e "${RED}✗ Error creant wpa_supplicant.conf${NC}"
    exit 1
fi
