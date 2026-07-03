# 🌐 SETUP-GITHUB-PAGES — Publica el lloc web a Internet

Aquesta guia activa **GitHub Pages** perquè el lloc web unificat
(`site/index.html`) sigui accessible a Internet des d'una URL pública
tipus `https://BernatMora.github.io/hort-osona/site/`.

## Per què

Ara mateix el lloc només és accessible des del teu PC (via `127.0.0.1:8765`).
Amb GitHub Pages qualsevol persona pot accedir-hi des de qualsevol lloc,
sense que calgui tenir el teu PC encès.

## Requisit previ

El repositori ha de ser **públic**. Si el vols mantenir privat, necessites
**GitHub Pro** o passar a l'opció alternativa (Cloudflare Tunnel — veure
SETUP-SITE.md).

Per fer-lo públic:
1. <https://github.com/BernatMora/hort-osona/settings>
2. Scroll fins a "Danger Zone"
3. "Change repository visibility" → "Make public"
4. Confirma

## Activar GitHub Pages

1. Vés a <https://github.com/BernatMora/hort-osona/settings/pages>
2. A "Build and deployment" → "Source", tria **"Deploy from a branch"**
3. A "Branch", tria **main** i la carpeta **/site** (no pas /(root))
4. Clica "Save"
5. Espera 1-2 minuts. GitHub et mostrarà la URL pública
6. Recarrega la pàgina; hauria d'aparèixer un missatge verd
   "Your site is live at..."

## URL resultant

```
https://BernatMora.github.io/hort-osona/site/
```

Afegeix-la als bookmarks del mòbil per consultar-la des de l'hort.

## Actualitzar el lloc

Cada vegada que facis `git push` al repo, GitHub Pages regenerarà el lloc
automàticament en 30-60 segons. No cal fer res més.

Per tant, el workflow queda:
```bash
# Després d'editar els .md
python site/build.py       # regenera site/index.html
git add .
git commit -m "..."
git push                   # GitHub Pages es desplega automàticament
```

## Verificació

Un cop activat, comprova:
- [ ] La URL respon (no dóna 404)
- [ ] Es veuen les 9 categories
- [ ] La cerca funciona
- [ ] El giny del mes actual mostra Juny 2026
- [ ] La pàgina `#checklist` funciona

## Solució de problemes

**El lloc mostra 404**: espera 1-2 minuts més, GitHub trigar una mica la
primera vegada.

**Mostra README en lloc del lloc**: comprova que la branca és `main` i la
carpeta és `/site` (no pas `/(root)`).

**Les fonts Google no carreguen**: comprova que tens connexió a Internet.
El lloc necessita accedir a fonts.googleapis.com.

**L'antic commit apareix**: buida la caché del navegador (Ctrl+F5).

## Personalització opcional (més endavant)

- **Domini propi** (`hort-osona.cat`): Settings → Pages → "Custom domain"
- **HTTPS forçat**: ja ve activat per defecte
- **Subdomini `www`**: afegeix un CNAME al DNS

## Privadesa

Un cop el lloc sigui públic, **tot el que hi hagi a `site/index.html` serà
visible a Internet**. Com que l'SPA només conté els teus `.md` ja presents
al repo, no hi hauria d'haver cap dada privada. Si en algun moment hi
afegeixes notes personals o contrasenyes, fes-les abans de `git push`.
