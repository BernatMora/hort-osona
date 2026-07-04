# 📱 Accés des del mòbil — Hort Osona PWA

> Tens el projecte disponible des de qualsevol dispositiu amb navegador, fins i tot **offline**.

## 🌐 URL pública

**https://BernatMora.github.io/hort-osona/**

Aquesta URL:
- ✅ Funciona des de qualsevol lloc del món (no cal estar a casa)
- ✅ S'actualitza automàticament cada vegada que fas `git push`
- ✅ Està allotjada gratuïtament a GitHub Pages
- ✅ No cal tenir el Mac encès

## 📲 Instal·lar com a app al mòbil

### iPhone / iPad (Safari)

1. Obre **https://BernatMora.github.io/hort-osona/** a Safari
2. Toca el botó **Compartir** (quadrat amb fletxa cap amunt, baix de la pantalla)
3. Desplaça't i tria **"Afegir a la pantalla d'inici"**
4. Confirma el nom "Hort Osona" i toca **"Afegir"**
5. ✅ Tens una icona a la pantalla d'inici com una app

Quan l'obris:
- S'obre **a pantalla completa** (sense barra del Safari)
- Es veu igual que l'aplicació nadiua
- Funciona **offline** (gràcies al service worker)

### Android (Chrome)

1. Obre **https://BernatMora.github.io/hort-osona/** a Chrome
2. Toca el menú (3 punts verticals, dalt a la dreta)
3. Tria **"Instal·lar aplicació"** o **"Afegir a la pantalla d'inici"**
4. Confirma
5. ✅ Tens una icona al calaix d'apps

## ✨ Què pots fer des del mòbil

Un cop instal·lada l'app, tens accés a:

- **Tots els 92 documents** del projecte
- **Cerca instantània** a tot el contingut
- **14 categories** amb menús desplegables (no cal baixar tota la pàgina)
- **Sidebar amb totes les fitxes** (visible a la dreta)
- **Vista neta** del document seleccionat
- **Funciona offline** (un cop carregada la primera vegada)

## 🔄 Manteniment

Cada vegada que vulguis actualitzar el contingut:

```bash
cd ~/Desktop/hort-osona
python3 build_portal.py   # regenera l'index.html i copia assets PWA
./hort-sync.sh "missatge" # commit + push
```

En 30-60 segons, la versió nova és visible al mòbil (i a tot arreu).

Si vols, pots crear un àlies al terminal per fer-ho en una sola ordre:

```bash
# Afegeix això a ~/.zshrc:
alias hort-publish='cd ~/Desktop/hort-osona && python3 build_portal.py && ./hort-sync.sh "Actualitzar web"'
```

Després:
```bash
hort-publish "Afegida fitxa de carxofa"
```

## 🛠️ Com funciona tècnicament

- **GitHub Pages** serveix l'`index.html` des de la branca `main` del repositori
- L'`index.html` conté **tots els documents incrustats** (és un fitxer únic de 2,2 MB)
- El **service worker** (`service-worker.js`) emmagatzema el portal a la memòria cau
- El **manifest** (`manifest.json`) indica al mòbil com mostrar l'app
- Les **icones** (`icon-192.png`, `icon-512.png`) són el que apareix a la pantalla d'inici

## 🔧 Resolució de problemes

### ❌ La URL no carrega
- Comprova que el repo és **públic** (Settings → Danger Zone → Change repository visibility)
- Comprova que GitHub Pages està activat (Settings → Pages)
- Espera 5-10 minuts després d'activar (la primera vegada triga)

### ❌ "Afegir a la pantalla d'inici" no apareix
- A iOS: usa **Safari** (no Chrome ni altres navegadors)
- A Android: usa **Chrome**
- Assegura't que la URL comença per `https://` (no `http://`)

### ❌ L'app no funciona offline
- Primer obre l'app **amb connexió** perquè es descarregui
- Després ja funciona offline

### ❌ No es veuen els canvis nous
- Tanca l'app del tot (al mòbil)
- Reobre-la
- O bé: Configuració → Safari → Avançat → Dades de llocs web → cerca "BernatMora" → Esborra

## 📊 Què NO funciona (de moment)

- **El xat amb IA** (Ollama) — corre al teu Mac i el mòbil no hi pot accedir
  - Solució: configurar Tailscale o túnel (veure `hort-osona-iot/CHAT-SETUP.md`)
- **Sensors IoT** (humitat, temperatura) — també al Mac o Raspberry Pi
- **Sincronització Git** — és eina de desenvolupador, no per usuaris finals

## 💡 Idees per millorar

- [ ] Afegir **botó per afegir notes** (localStorage al mòbil)
- [ ] Afegir **checklist diària** amb sincronització
- [ ] Activar **Tailscale** per accedir al xat des del mòbil
- [ ] **Notificacions push** quan hi ha tasques importants
- [ ] **Mode fosc** per llegir a la nit a l'hort 🌙

## 📞 Ajuda

Si alguna cosa no funciona:
1. Comprova que el portal es genera bé: `python3 build_portal.py`
2. Comprova els assets PWA: `ls -la manifest.json icon-*.png service-worker.js`
3. Comprova que el push ha funcionat: `git log --oneline -3`
