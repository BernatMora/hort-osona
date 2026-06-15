#!/bin/bash
# ============================================================
# Script: convertir_HTML_a_PDF.sh
# Converteix els fitxers HTML imprimibles a PDF
# ============================================================
# Ús: bash convertir_HTML_a_PDF.sh
# O simplement fer doble clic si tens Git Bash associat
# ============================================================

echo "🌱 Convertidor HTML → PDF per al quadern d'hort Osona"
echo "======================================================="
echo ""

# Anar al directori dels fitxers
cd ~/hort-osona/plans-mensuals/

# Comprovar quin mètode tenim disponible
metode=""

if command -v wkhtmltopdf &> /dev/null; then
    metode="wkhtmltopdf"
    echo "✅ Trobada eina: wkhtmltopdf"
elif command -v weasyprint &> /dev/null; then
    metode="weasyprint"
    echo "✅ Trobada eina: weasyprint"
elif command -v google-chrome &> /dev/null; then
    metode="chrome"
    echo "✅ Trobada eina: Google Chrome"
elif command -v chromium &> /dev/null; then
    metode="chromium"
    echo "✅ Trobada eina: Chromium"
elif command -v msedge &> /dev/null; then
    metode="msedge"
    echo "✅ Trobada eina: Microsoft Edge"
else
    metode="manual"
    echo "⚠️  No s'ha trobat cap conversor automàtic."
    echo "   Hauràs d'imprimir manualment des del navegador."
fi

echo ""

# Si tenim conversor, generar PDFs
if [ "$metode" != "manual" ]; then
    echo "📄 Generant quadern-imprimible-2026.pdf..."
    case $metode in
        wkhtmltopdf)
            wkhtmltopdf --enable-local-file-access --javascript-delay 1000 \
                quadern-imprimible-2026.html quadern-2026.pdf 2>&1 | head -5
            wkhtmltopdf --enable-local-file-access --javascript-delay 1000 \
                fitxes-cultius-imprimibles.html fitxes-cultius-2026.pdf 2>&1 | head -5
            ;;
        weasyprint)
            weasyprint quadern-imprimible-2026.html quadern-2026.pdf 2>&1 | head -5
            weasyprint fitxes-cultius-imprimibles.html fitxes-cultius-2026.pdf 2>&1 | head -5
            ;;
        chrome)
            google-chrome --headless --disable-gpu --no-sandbox \
                --print-to-pdf="quadern-2026.pdf" "file://$PWD/quadern-imprimible-2026.html" 2>&1 | head -5
            google-chrome --headless --disable-gpu --no-sandbox \
                --print-to-pdf="fitxes-cultius-2026.pdf" "file://$PWD/fitxes-cultius-imprimibles.html" 2>&1 | head -5
            ;;
        chromium)
            chromium --headless --disable-gpu --no-sandbox \
                --print-to-pdf="quadern-2026.pdf" "file://$PWD/quadern-imprimible-2026.html" 2>&1 | head -5
            chromium --headless --disable-gpu --no-sandbox \
                --print-to-pdf="fitxes-cultius-2026.pdf" "file://$PWD/fitxes-cultius-imprimibles.html" 2>&1 | head -5
            ;;
        msedge)
            msedge --headless --disable-gpu --no-sandbox \
                --print-to-pdf="quadern-2026.pdf" "file://$PWD/quadern-imprimible-2026.html" 2>&1 | head -5
            msedge --headless --disable-gpu --no-sandbox \
                --print-to-pdf="fitxes-cultius-2026.pdf" "file://$PWD/fitxes-cultius-imprimibles.html" 2>&1 | head -5
            ;;
    esac

    echo ""
    if [ -f "quadern-2026.pdf" ]; then
        echo "✅ Creat: $(pwd)/quadern-2026.pdf"
    fi
    if [ -f "fitxes-cultius-2026.pdf" ]; then
        echo "✅ Creat: $(pwd)/fitxes-cultius-2026.pdf"
    fi
else
    echo "📖 Mètode manual (recomanat):"
    echo ""
    echo "1. Obre l'Explorador d'arxius de Windows"
    echo "2. Vés a: C:\\Users\\iadmin\\hort-osona\\plans-mensuals\\"
    echo "3. Fes doble clic a 'quadern-imprimible-2026.html'"
    echo "4. Al navegador: Ctrl+P"
    echo "5. Tria 'Desar com a PDF' com a impressora"
    echo "6. Repeteix amb 'fitxes-cultius-imprimibles.html'"
    echo ""
    echo "💡 Alternativa: instal·la una eina gratuïta:"
    echo "   - 7-Zip (https://www.7-zip.org)"
    echo "   - wkhtmltopdf: winget install wkhtmltopdf"
    echo "   - Chrome: ja el tens segur!"
    echo "     Des del terminal: chrome --headless --print-to-pdf=quadern-2026.pdf file:///c/Users/iadmin/hort-osona/plans-mensuals/quadern-imprimible-2026.html"
fi

echo ""
echo "🌱 Fet! Bona collita!"
