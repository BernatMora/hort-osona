#!/bin/bash
# ============================================================================
#  setup-mycloudhome.sh — Configura el My Cloud Home per a Hort Osona
#
#  Crea l'estructura de carpetes per:
#    - Dades del node IoT (LoRa → RPi → My Cloud Home)
#    - Portal web Hort Osona (versio estàtica)
#    - Scripts i configuracio
#
#  Us: ./setup-mycloudhome.sh
#  Cal tenir el My Cloud Home muntat al Mac via SMB
# ============================================================================

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🌱 Hort Osona — Configuració del My Cloud Home"
echo "================================================"
echo ""

# Detectar el My Cloud Home
echo "🔍 Buscant el My Cloud Home..."

# Provar el nom per defecte del My Cloud Home
POSSIBLE_MOUNTS=(
    "/Volumes/Public"
    "/Volumes/MyCloudHome"
    "$HOME/Public"
    "$HOME/MyCloudHome"
)

MOUNT_POINT=""
for path in "${POSSIBLE_MOUNTS[@]}"; do
    if [ -d "$path" ]; then
        MOUNT_POINT="$path"
        break
    fi
done

# Si no l'hem trobat, provar de muntar
if [ -z "$MOUNT_POINT" ]; then
    echo -e "${YELLOW}⚠️  No he trobat el My Cloud Home muntat${NC}"
    echo "Per muntar-lo:"
    echo "  1. Obre Finder → Xarxa"
    echo "  2. Clica al My Cloud Home (192.168.100.48)"
    echo "  3. Fes login amb les teves credencials"
    echo "  4. Selecciona la carpeta 'Public'"
    echo ""
    echo -e "${YELLOW}Si ja esta muntat, escriu el path complet (ex: /Volumes/Public):${NC}"
    read -p "Path del My Cloud Home: " MOUNT_POINT
    
    if [ ! -d "$MOUNT_POINT" ]; then
        echo "❌ El path no existeix. Aborta."
        exit 1
    fi
fi

echo -e "${GREEN}✅ Muntatge trobat: $MOUNT_POINT${NC}"

# Crear estructura de carpetes
HORT_DIR="$MOUNT_POINT/hort-osona"
echo ""
echo "📂 Creant estructura a $HORT_DIR..."

mkdir -p "$HORT_DIR/data/2026"
mkdir -p "$HORT_DIR/data/2027"
mkdir -p "$HORT_DIR/data/backups"
mkdir -p "$HORT_DIR/portal"
mkdir -p "$HORT_DIR/portal/docs"
mkdir -p "$HORT_DIR/portal/assets"
mkdir -p "$HORT_DIR/scripts"
mkdir -p "$HORT_DIR/config"

# Fitxer README dins de la carpeta hort-osona
cat > "$HORT_DIR/README.md" <<'EOF'
# Hort Osona — My Cloud Home

Aquesta carpeta conté les dades i el portal del projecte Hort Osona.

## Estructura

```
hort-osona/
├── data/                # Dades del node IoT
│   ├── 2026/           # Any 2026
│   ├── 2027/           # Any 2027
│   ├── backups/        # Còpies de seguretat
│   └── db.sqlite       # Base de dades local (creada per la RPi)
├── portal/              # Portal web estàtic
│   ├── index.html      # Pàgina principal
│   ├── docs/           # Documents .md convertits a HTML
│   └── assets/         # Icones, manifest.json, service worker
├── scripts/             # Scripts d'instal·lació i manteniment
└── config/              # Configuració (Supabase keys, etc.)
```

## Com accedir

### Des del Mac (ja tens)
- Obre Finder → Public → hort-osona

### Des del navegador (a la mateixa WiFi)
- `http://192.168.100.48/Public/hort-osona/portal/index.html`

### Des de la RPi
Muntar via SMB/CIFS a `/mnt/mycloudhome`.

## Manteniment

- **Còpies de seguretat**: activar Time Machine al Mac apuntant a `/Public`
- **Espai**: vigilar la mida de la carpeta `data/` (pot créixer molt)
EOF

echo -e "${GREEN}✅ Estructura creada${NC}"
echo ""
echo "📋 Resum:"
echo "   $HORT_DIR/"
echo "   ├── data/                (dades IoT)"
echo "   ├── portal/              (web estàtica)"
echo "   ├── scripts/             (scripts)"
echo "   └── config/              (configuració)"
echo ""
echo -e "${GREEN}✅ Setup complet!${NC}"
echo ""
echo "Proper pas:"
echo "  1. Copiar el portal a $HORT_DIR/portal/"
echo "  2. Configurar la RPi per accedir al My Cloud Home"
