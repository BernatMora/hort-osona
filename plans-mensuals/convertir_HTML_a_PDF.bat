@echo off
REM ============================================================
REM Script Windows: convertir_HTML_a_PDF.bat
REM Converteix els fitxers HTML imprimibles a PDF
REM ============================================================
REM Us: doble clic a aquest fitxer
REM ============================================================

echo =====================================================
echo  Convertidor HTML -> PDF per al quadern d'hort Osona
echo =====================================================
echo.

cd /d "%USERPROFILE%\hort-osona\plans-mensuals\"

REM Provar Edge (sempre present a Windows 10/11)
where msedge >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [!] Usant Microsoft Edge per generar PDFs...
    echo.
    echo [!] Generant quadern-2026.pdf...
    start "" "msedge" --headless --disable-gpu --no-sandbox --print-to-pdf="quadern-2026.pdf" "file:///%USERPROFILE%/hort-osona/plans-mensuals/quadern-imprimible-2026.html"
    timeout /t 5
    echo [!] Generant fitxes-cultius-2026.pdf...
    start "" "msedge" --headless --disable-gpu --no-sandbox --print-to-pdf="fitxes-cultius-2026.pdf" "file:///%USERPROFILE%/hort-osona/plans-mensuals/fitxes-cultius-imprimibles.html"
    timeout /t 5
    goto :comprovar
)

REM Provar Chrome
where chrome >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [!] Usant Google Chrome per generar PDFs...
    echo.
    echo [!] Generant quadern-2026.pdf...
    start "" "chrome" --headless --disable-gpu --no-sandbox --print-to-pdf="quadern-2026.pdf" "file:///%USERPROFILE%/hort-osona/plans-mensuals/quadern-imprimible-2026.html"
    timeout /t 5
    echo [!] Generant fitxes-cultius-2026.pdf...
    start "" "chrome" --headless --disable-gpu --no-sandbox --print-to-pdf="fitxes-cultius-2026.pdf" "file:///%USERPROFILE%/hort-osona/plans-mensuals/fitxes-cultius-imprimibles.html"
    timeout /t 5
    goto :comprovar
)

:comprovar
echo.
if exist "quadern-2026.pdf" (
    echo [OK] Creat: %USERPROFILE%\hort-osona\plans-mensuals\quadern-2026.pdf
) else (
    echo [!] quadern-2026.pdf no s'ha pogut crear automaticament.
)

if exist "fitxes-cultius-2026.pdf" (
    echo [OK] Creat: %USERPROFILE%\hort-osona\plans-mensuals\fitxes-cultius-2026.pdf
) else (
    echo [!] fitxes-cultius-2026.pdf no s'ha pogut crear automaticament.
)

echo.
echo =====================================================
echo  METODE MANUAL (si l'automatic no ha funcionat):
echo =====================================================
echo  1. Obre l'Explorador d'arxius
echo  2. Vés a: %USERPROFILE%\hort-osona\plans-mensuals\
echo  3. Fes doble clic a 'quadern-imprimible-2026.html'
echo  4. Al navegador: Ctrl+P
echo  5. Tria 'Desar com a PDF' com a impressora
echo  6. Repeteix amb 'fitxes-cultius-imprimibles.html'
echo =====================================================
echo.
pause
