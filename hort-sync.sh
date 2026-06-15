#!/usr/bin/env bash
# hort-sync — sincronitza el projecte hort-osona amb GitHub
# Ús:
#   hort-sync                    # pull + status + add + commit + push
#   hort-sync "missatge"         # amb missatge directe
#   hort-sync pull               # només baixar canvis
#   hort-sync push "missatge"    # només pujar (amb missatge)
#   hort-sync status             # veure estat actual

set -e

# Detectar el directori del projecte (mateix on viu l'script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Comprovar que estem dins d'un repo git
if [ ! -d .git ]; then
  echo -e "${RED}❌ No s'ha trobat .git a $SCRIPT_DIR${NC}"
  echo "   Aquest script ha d'estar dins del directori del projecte hort-osona."
  exit 1
fi

branca() {
  git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD
}

pull_canvis() {
  echo -e "${BLUE}📥 Baixant canvis de GitHub (branca $(branca))...${NC}"
  if ! git pull --rebase --autostash; then
    echo -e "${RED}❌ Hi ha hagut conflictes. Resol'ls manualment i torna-ho a provar.${NC}"
    exit 1
  fi
  echo -e "${GREEN}✅ Pull fet${NC}"
}

veure_estat() {
  echo -e "${BLUE}📊 Estat del repositori:${NC}"
  git status --short
  CANVIS=$(git status --porcelain | wc -l | tr -d ' ')
  if [ "$CANVIS" -eq 0 ]; then
    echo -e "${GREEN}   Cap canvi pendent${NC}"
    return 1   # retorna fals: no hi ha res a fer
  fi
  echo -e "${YELLOW}   $CANVIS fitxer(s) amb canvis${NC}"
  return 0
}

fer_commit() {
  local missatge="$1"

  if [ -z "$missatge" ]; then
    # Si no hi ha missatge, mirar l'últim commit per inspirar-se
    echo -e "${YELLOW}📝 Escriu el missatge del commit (una línia, breu):${NC}"
    read -r missatge
    if [ -z "$missatge" ]; then
      missatge="Actualització $(date '+%Y-%m-%d %H:%M')"
      echo -e "${YELLOW}   (usant missatge per defecte: $missatge)${NC}"
    fi
  fi

  echo -e "${BLUE}📦 Afegint canvis i fent commit...${NC}"
  git add .
  git commit -m "$missatge"
  echo -e "${GREEN}✅ Commit fet: $missatge${NC}"
}

pujar_canvis() {
  echo -e "${BLUE}📤 Pujant canvis a GitHub...${NC}"
  if git push; then
    echo -e "${GREEN}✅ Push completat${NC}"
  else
    echo -e "${RED}❌ Error en el push. Comprova la connexió o l'autenticació.${NC}"
    exit 1
  fi
}

# Cos principal
case "${1:-all}" in
  pull)
    pull_canvis
    ;;
  push)
    shift
    pull_canvis
    if veure_estat; then
      fer_commit "$1"
    else
      echo -e "${GREEN}Res a pujar.${NC}"
    fi
    pujar_canvis
    ;;
  status|estat)
    veure_estat
    ;;
  ""|all|sync)
    pull_canvis
    if veure_estat; then
      fer_commit "$1"
      pujar_canvis
    else
      echo -e "${GREEN}🎉 Tot sincronitzat. No hi ha canvis pendents.${NC}"
    fi
    ;;
  -h|--help|help)
    echo "hort-sync — sincronitza el projecte hort-osona amb GitHub"
    echo ""
    echo "Ús:"
    echo "  hort-sync                    pull + add + commit + push"
    echo "  hort-sync \"missatge\"         amb missatge directe"
    echo "  hort-sync pull               només baixar canvis"
    echo "  hort-sync push \"missatge\"   només pujar (amb missatge)"
    echo "  hort-sync status             veure estat actual"
    ;;
  *)
    # Si el primer argument no és un subcomando, tractar-lo com a missatge
    pull_canvis
    if veure_estat; then
      fer_commit "$1"
      pujar_canvis
    else
      echo -e "${GREEN}🎉 Tot sincronitzat.${NC}"
    fi
    ;;
esac
