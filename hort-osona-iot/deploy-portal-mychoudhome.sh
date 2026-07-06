#!/bin/bash
# ============================================================================
#  deploy-portal-mychoudhome.sh — Desplega el portal Hort Osona al My Cloud Home
#
#  Copia el portal generat (index.html, docs/, assets/) a la carpeta
#  Public/hort-osona/portal/ del My Cloud Home.
#
#  Cal que el My Cloud Home estigui muntat al Mac.
# ============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORTAL_SOURCE="$PROJECT_DIR/../index.html"
DOCS_SOURCE="$PROJECT_DIR/../docs"
SEARCH_INDEX="$PROJECT_DIR/../search_index.json"

echo "🌱 Hort Osona — Deploy del portal al My Cloud Home"
echo "==================================================="
echo ""

# Trobar el punt de muntatge
POSSIBLE_MOUNTS=(
    "/Volumes/Public/hort-osona/portal"
    "/Volumes/MyCloudHome/Public/hort-osona/portal"
    "$HOME/Public/hort-osona/portal"
)

DEST_DIR=""
for path in "${POSSIBLE_MOUNTS[@]}"; do
    parent=$(dirname "$(dirname "$path")")  # /Volumes/Public/hort-osona
    if [ -d "$parent" ]; then
        DEST_DIR="$path"
        break
    fi
done

# Si no l'hem trobat, preguntar
if [ -z "$DEST_DIR" ]; then
    echo -e "${YELLOW}⚠️  No he trobat el My Cloud Home muntat${NC}"
    echo "Per muntar-lo:"
    echo "  1. Obre Finder → Xarxa"
    echo "  2. Clica al My Cloud Home (192.168.100.48)"
    echo "  3. Fes login amb les teves credencials"
    echo "  4. Selecciona 'Public'"
    echo ""
    read -p "Escriu el path COMPLET del portal (ex: /Volumes/Public/hort-osona/portal): " DEST_DIR
    
    if [ ! -d "$(dirname "$DEST_DIR")" ]; then
        echo "❌ Path no vàlid. Aborta."
        exit 1
    fi
fi

echo -e "${GREEN}✅ Destinació: $DEST_DIR${NC}"

# Verificar que tenim el portal
if [ ! -f "$PORTAL_SOURCE" ]; then
    echo "❌ No trobo $PORTAL_SOURCE"
    echo "   Primer cal generar el portal amb: cd .. && python3 build_portal_v2.py"
    exit 1
fi

# Generar el portal si cal
echo ""
echo "📦 [1/3] Generant portal..."
cd "$PROJECT_DIR/.."
python3 build_portal_v2.py 2>&1 | tail -3

# Crear estructura
echo ""
echo "📂 [2/3] Copiant fitxers al My Cloud Home..."
mkdir -p "$DEST_DIR/docs"
mkdir -p "$DEST_DIR/assets"

# Copiar el portal
cp "$PORTAL_SOURCE" "$DEST_DIR/index.html"
echo "  ✅ index.html"

# Copiar els documents
if [ -d "$DOCS_SOURCE" ]; then
    cp -r "$DOCS_SOURCE/"*.md "$DEST_DIR/docs/" 2>/dev/null || true
    DOC_COUNT=$(ls "$DEST_DIR/docs/" 2>/dev/null | wc -l | tr -d ' ')
    echo "  ✅ docs/ ($DOC_COUNT fitxers)"
fi

# Copiar el search_index.json
if [ -f "$SEARCH_INDEX" ]; then
    cp "$SEARCH_INDEX" "$DEST_DIR/search_index.json"
    echo "  ✅ search_index.json"
fi

# Copiar els assets PWA
ASSETS_DIR="$PROJECT_DIR/../assets"
if [ -d "$ASSETS_DIR" ]; then
    cp "$ASSETS_DIR"/* "$DEST_DIR/assets/" 2>/dev/null || true
    echo "  ✅ assets/"
else
    # Provar des de l'arrel
    for f in manifest.json icon.svg icon-192.png icon-512.png service-worker.js; do
        if [ -f "$PROJECT_DIR/../$f" ]; then
            cp "$PROJECT_DIR/../$f" "$DEST_DIR/"
            echo "  ✅ $f"
        fi
    done
fi

# Resum
echo ""
echo -e "${GREEN}📋 Resum del deploy ==="
echo "   Portal: file://$DEST_DIR/index.html"
echo "   Tamany: $(du -sh "$DEST_DIR" | cut -f1)"
echo ""

# Comprovar acces
echo "🌐 Com accedir al portal:"
echo "   Des del navegador: http://192.168.100.48/Public/hort-osona/portal/index.html"
echo "   Des del Mac: file://$DEST_DIR/index.html"
echo ""

echo -e "${GREEN}✅ Deploy complet!${NC}"
