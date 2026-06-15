@echo off
REM hort-sync.bat — sincronitza el projecte hort-osona amb GitHub (Windows)
REM Ús:
REM   hort-sync                       pull + add + commit + push
REM   hort-sync "missatge"            amb missatge directe
REM   hort-sync pull                  només baixar canvis
REM   hort-sync push "missatge"       només pujar
REM   hort-sync status                veure estat

chcp 65001 >nul
setlocal enabledelayedexpansion

REM Canviar al directori de l'script
cd /d "%~dp0"

REM Colors (PowerShell)
set "GREEN=[32m"
set "RED=[31m"
set "YELLOW=[33m"
set "BLUE=[34m"
set "NC=[0m"

REM Comprovar que estem en un repo git
if not exist ".git" (
  echo %RED%❌ No s'ha trobat .git en %cd%%NC%
  echo    Aquest script ha d'estar dins del directori del projecte hort-osona.
  exit /b 1
)

REM Detectar subcomando
set "SUBCOMANDO=%~1"
if "%SUBCOMANDO%"=="" set "SUBCOMANDO=all"
if "%SUBCOMANDO%"=="sync" set "SUBCOMANDO=all"
if "%SUBCOMANDO%"=="estat" set "SUBCOMANDO=status"
if "%SUBCOMANDO%"=="-h" goto :help
if "%SUBCOMANDO%"=="--help" goto :help
if "%SUBCOMANDO%"=="help" goto :help

REM === PULL ===
:pull
echo %BLUE%📥 Baixant canvis de GitHub...%NC%
git pull --rebase --autostash
if errorlevel 1 (
  echo %RED%❌ Hi ha hagut conflictes. Resol'ls manualment i torna-ho a provar.%NC%
  exit /b 1
)
echo %GREEN%✅ Pull fet%NC%
goto :eof

REM === STATUS ===
:status
echo %BLUE%📊 Estat del repositori:%NC%
git status --short
for /f %%a in ('git status --porcelain ^| find /c /v ""') do set CANVIS=%%a
if "%CANVIS%"=="0" (
  echo %GREEN%   Cap canvi pendent%NC%
) else (
  echo %YELLOW%   %CANVIS% fitxer(s) amb canvis%NC%
)
goto :eof

REM === HELP ===
:help
echo hort-sync.bat — sincronitza el projecte hort-osona amb GitHub
echo.
echo Ús:
echo   hort-sync                       pull + add + commit + push
echo   hort-sync "missatge"            amb missatge directe
echo   hort-sync pull                  només baixar canvis
echo   hort-sync push "missatge"       només pujar
echo   hort-sync status                veure estat
exit /b 0

REM === MAIN LOGIC ===
:main
call :pull

REM Mirar si hi ha canvis
git status --porcelain > "%TEMP%\hort_sync_status.txt"
set /a CANVIS=0
for /f %%a in ('type "%TEMP%\hort_sync_status.txt" ^| find /c /v ""') do set /a CANVIS=%%a
del "%TEMP%\hort_sync_status.txt"

if %CANVIS%==0 (
  echo %GREEN%🎉 Tot sincronitzat. No hi ha canvis pendents.%NC%
  exit /b 0
)

echo %YELLOW%   %CANVIS% fitxer(s) amb canvis%NC%

REM Demanar missatge si no s'ha donat
set "MISSATGE=%~2"
if "%SUBCOMANDO%"=="push" set "MISSATGE=%~2"
if "%SUBCOMANDO%" neq "push" if "%~1" neq "" if "%SUBCOMANDO%"=="all" set "MISSATGE=%~1"

if "%MISSATGE%"=="" (
  set /p MISSATGE="📝 Escriu el missatge del commit (una línia, breu): "
  if "!MISSATGE!"=="" (
    set "MISSATGE=Actualització %date% %time:~0,5%"
    echo %YELLOW%   (usant missatge per defecte: !MISSATGE!)%NC%
  )
)

echo %BLUE%📦 Afegint canvis i fent commit...%NC%
git add .
git commit -m "!MISSATGE!"
if errorlevel 1 (
  echo %RED%❌ Error en el commit.%NC%
  exit /b 1
)
echo %GREEN%✅ Commit fet: !MISSATGE!%NC%

echo %BLUE%📤 Pujant canvis a GitHub...%NC%
git push
if errorlevel 1 (
  echo %RED%❌ Error en el push. Comprova la connexió o autenticació.%NC%
  exit /b 1
)
echo %GREEN%✅ Push completat%NC%

exit /b 0
