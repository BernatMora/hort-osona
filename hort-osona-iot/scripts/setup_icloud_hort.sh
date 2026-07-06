#!/bin/bash
# setup_icloud_hort.sh — Sincronitza hort-osona/ amb iCloud Drive
#
# Crea un symlink a iCloud Drive per fer backup automatic de la carpeta
# del projecte. iCloud Drive sincronitza automaticament al núvol.
#
# Ús:
#   ./setup_icloud_hort.sh           # Crea el symlink
#   ./setup_icloud_hort.sh remove    # Elimina el symlink
#   ./setup_icloud_hort.sh status    # Comprova l'estat

set -e

ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
PROJECT_DIR="$HOME/Desktop/hort-osona"
LINK_NAME="Hort-Osona"
LINK_PATH="$ICLOUD_DIR/$LINK_NAME"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Comprovar precondicions
check_icloud() {
    if [ ! -d "$ICLOUD_DIR" ]; then
        echo -e "${RED}✗ iCloud Drive no está actiu${NC}"
        echo "Activa'l a: System Settings → Apple ID → iCloud → iCloud Drive"
        exit 1
    fi
}

check_project() {
    if [ ! -d "$PROJECT_DIR" ]; then
        echo -e "${RED}✗ No trobo $PROJECT_DIR${NC}"
        exit 1
    fi
}

status() {
    echo -e "${BLUE}=== Estat iCloud Drive ===${NC}"
    check_icloud
    check_project
    echo ""
    if [ -L "$LINK_PATH" ]; then
        TARGET=$(readlink "$LINK_PATH")
        echo -e "${GREEN}✓ Symlink actiu:${NC}"
        echo "   $LINK_PATH -> $TARGET"
        echo ""
        echo "Mida del projecte:"
        du -sh "$PROJECT_DIR" 2>&1 | tail -1
        echo ""
        echo "iCloud Drive:"
        df -h "$ICLOUD_DIR" 2>&1 | tail -1 | awk '{print "   Disponible: " $4 " de " $2}'
    elif [ -d "$LINK_PATH" ]; then
        echo -e "${YELLOW}⚠️  $LINK_PATH existeix pero NO es un symlink${NC}"
        echo "Es un directori real. Si vols sync automatic, cal eliminar-lo primer."
    else
        echo -e "${YELLOW}✗ Symlink no creat encara${NC}"
        echo "Executa: $0"
    fi
}

create_link() {
    check_icloud
    check_project

    if [ -L "$LINK_PATH" ]; then
        echo -e "${YELLOW}⚠️  El symlink ja existeix:${NC}"
        echo "   $LINK_PATH -> $(readlink "$LINK_PATH")"
        echo ""
        read -p "Vols recrear-lo? (s/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            exit 0
        fi
        rm "$LINK_PATH"
    fi

    if [ -d "$LINK_PATH" ]; then
        # Es un directori real - el movem a backup
        echo -e "${YELLOW}⚠️  $LINK_PATH ja existeix com a directori${NC}"
        BACKUP_PATH="${LINK_PATH}.backup.${TIMESTAMP}"
        mv "$LINK_PATH" "$BACKUP_PATH"
        echo "   Mogut a: $BACKUP_PATH"
    fi

    # Crear el symlink
    echo -e "${BLUE}Creant symlink...${NC}"
    ln -s "$PROJECT_DIR" "$LINK_PATH"

    echo ""
    echo -e "${GREEN}✓ Fet!${NC}"
    echo ""
    echo "El symlink esta actiu:"
    echo "  $LINK_PATH -> $PROJECT_DIR"
    echo ""
    echo "Ara iCloud Drive sincronitzara automaticament els canvis de"
    echo "la carpeta hort-osona/ al núvol."
    echo ""
    echo "A l'iPhone, obre l'app Fitxers -> iCloud Drive -> Hort-Osona"
    echo ""
    echo "Si vols comprovar l'estat: $0 status"
}

remove_link() {
    check_icloud

    if [ ! -L "$LINK_PATH" ]; then
        echo -e "${YELLOW}No hi ha cap symlink a $LINK_PATH${NC}"
        exit 0
    fi

    echo -e "${BLUE}Eliminant symlink...${NC}"
    rm "$LINK_PATH"
    echo -e "${GREEN}✓ Symlink eliminat${NC}"
    echo ""
    echo "IMPORTANT: iCloud ja no sincronitzara hort-osona/"
    echo "Si vols tornar-ho a activar: $0"
}

# Main
case "${1:-create}" in
    status)
        status
        ;;
    remove|delete)
        remove_link
        ;;
    create|install|*)
        create_link
        ;;
esac
