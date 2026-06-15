# 🌱 Sincronitzar el projecte `hort-osona` amb Windows

Guia pas a pas per configurar l'ordinador de la feina (Windows) i poder treballar al projecte hort-osona conjuntament amb el Mac.

---

## 📋 Què necessites

- Windows 10 o 11
- Connexió a internet
- El compte de GitHub **BernatMora** (amb el token actiu)
- ~15 minuts la primera vegada

---

## 🪟 Part 1 — Instal·lar Git a Windows

1. Descarrega Git per a Windows: **https://git-scm.com/download/win**
   - Si et pregunta, descarrega la versió **64-bit Git for Windows Setup**.
2. Executa l'instal·lador (`Git-xxx-64-bit.exe`).
3. Durant la instal·lació, **deixa totes les opcions per defecte** (ja van bé).
4. Quan acabi, **tanca totes les finestres de PowerShell o terminal** que estiguessin obertes i torna-les a obrir.
5. Obre **Git Bash** (cerca'l al menú Inici). Verifica que funciona escrivint:
   ```bash
   git --version
   ```
   Hauries de veure alguna cosa com `git version 2.47.x.windows.x`.

---

## 🔑 Part 2 — Configurar Git amb el teu nom i correu

Al **Git Bash**, executa una per una:

```bash
git config --global user.name "Bernat"
git config --global user.email "bernatmora@mac.com"
git config --global credential.helper manager
```

Què fa cada línia:
- Les dues primeres: defineixen qui ets als commits (mateixa identitat que al Mac).
- La tercera: desa el token al **credential manager de Windows**, per no haver-lo de tornar a escriure cada vegada.

---

## 🎫 Part 3 — Crear un token a GitHub (només la primera vegada)

⚠️ El token del Mac **no serveix al Windows** — cal un de nou (o pots fer servir el mateix des del navegador, veure opció B més avall).

### Opció A — Token clàssic (recomanada)

1. Obre al navegador: **https://github.com/settings/tokens/new**
2. Si et porta a una pàgina amb botons, fes clic a **Generate new token** → **Generate new token (classic)**.
3. Emplena:
   - **Note:** `Windows feina hort-osona`
   - **Expiration:** `90 days` (o el que vulguis)
   - **Scopes:** marca només la casella ✅ **`repo`**
4. Fes clic al botó verd **Generate token** (a baix de tot).
5. ⚠️ **Copia el token immediatament** — comença per `ghp_...` i no el tornaràs a veure. Guarda'l en un lloc segur (bloc de notes, gestor de contrasenyes...).

### Opció B — Autenticació pel navegador (més fàcil, menys segur)

Si tens Git recent, potser quan facis `git push` s'obrirà el navegador i et validarà directament amb el teu compte GitHub. Prova-ho: si funciona, no cal el token.

---

## 📥 Part 4 — Clonar el projecte a Windows

1. Decideix on vols tenir el projecte, per exemple:
   `C:\Users\elteuusuari\Documents\`
   (substitueix `elteuusuari` pel teu usuari real de Windows)

2. Al **Git Bash**, executa:
   ```bash
   cd /c/Users/elteuusuari/Documents
   git clone https://github.com/BernatMora/hort-osona.git
   ```
   - Si `elteuusuari` té espais (p. ex. "Bernat Mora"), posa-ho entre cometes o escapa els espais:
     ```bash
     cd "/c/Users/Bernat Mora/Documents"
     ```

3. La primera vegada et demanarà:
   - **Username:** `BernatMora`
   - **Password:** enganxa el token (`Ctrl+V` funciona) — no la contrasenya del compte

4. Hauries de veure moltes línies com `Receiving objects: 100% (XXXX/XXXX)`. Això és bo 🎉

5. Ja tens el projecte a Windows. Per entrar-hi:
   ```bash
   cd hort-osona
   ls
   ```
   Hauries de veure tots els teus fitxers (`00-index.md`, `01-calendari-sembra.md`, `07-fitxes-cultius/`, etc.).

---

## 🔄 Part 5 — El dia a dia: com sincronitzar

Cada vegada que vulguis treballar al projecte, obre **Git Bash** i:

### 1. Baixa els últims canvis de l'altre ordinador
```bash
cd /c/Users/elteuusuari/Documents/hort-osona
git pull
```

### 2. Treballa normalment
- Obre els fitxers `.md` amb VS Code, Notepad++, o qualsevol editor
- Obre els `.html` amb el navegador per revisar-los
- Fes tots els canvis que necessitis

### 3. Desar els canvis al GitHub (3 comandes)
```bash
git add .
git commit -m "Descripció breu del que has fet"
git push
```

Exemples de bons missatges de commit:
- `Actualitzo pla juny 2026 amb noves dates de sembra`
- `Afegixo fitxa cultiu de carxofa`
- `Corregeixo errors tipogràfics a 03-gestio-plagues.md`

---

## 🆘 Solució de problemes

### ❌ "Authentication failed"
- El token ha expirat o és incorrecte. Torna a la **Part 3** i genera'n un de nou.
- A Windows, pots esborrar la credencial antiga:
  ```bash
  git credential-manager erase https://github.com
  ```
  (potser cal fer-ho des de **Credencial Manager de Windows** → Credencials de Windows)

### ❌ "Your local changes would be overwritten by merge"
- Tens canvis locals que entren en conflicte amb els del Mac. Opció ràpida:
  ```bash
  git stash         # desa els teus canvis en un calaix temporal
  git pull          # baixa els canvis del Mac
  git stash pop     # aplica els teus canvis a sobre
  ```
  Si hi ha conflicte, Git t'ho dirà i l'hauràs de resoldre manualment a l'editor.

### ❌ "Please tell me who you are"
- No has fet la **Part 2**. Executa les dues primeres línies de la Part 2.

### ❌ "Permission denied (publickey)"
- Estàs intentant usar SSH en lloc de HTTPS. Assegura't que la URL comença per `https://`:
  ```bash
  git remote -v
  ```
  Si posa `git@github.com:...`, canvia'l:
  ```bash
  git remote set-url origin https://github.com/BernatMora/hort-osona.git
  ```

### ❌ M'he equivocat i he esborrat un fitxer!
- Git té historial complet. Per recuperar-lo:
  ```bash
  git log --diff-filter=D --name-only --pretty=format:"%H %s"    # troba quin commit el va esborrar
  git checkout <commit-hash>^ -- nom-del-fitxer.md                # el recupera
  ```
  Si no t'enfiles, pregunta'm — t'ajudo.

---

## ⚠️ Bones pràctiques

1. **Fes `git pull` abans de començar** a treballar cada dia.
2. **Fes `git push` al finalitzar** — no esperis dies.
3. **Commits petits i descriptius** — un commit per canvi lògic, no tot de cop.
4. **No treballeu el mateix fitxer alhora** des dels dos ordinadors — pot generar conflictes.
5. **Si tens dubtes**, executa `git status` — sempre et diu què passa.

---

## 📌 Resum ràpid de comandes

| Acció | Comandes |
|---|---|
| Baixar canvis de l'altre PC | `git pull` |
| Veure què has canviat | `git status` |
| Veure els canvis en detall | `git diff` |
| Desar canvis | `git add .` + `git commit -m "..."` + `git push` |
| Desfer canvis no desats | `git checkout -- nom-fitxer` |
| Historial | `git log --oneline` |

---

## 📞 Ajuda

Si alguna cosa no funciona, enganxa'm l'error exacte i t'ajudo. També pots obrir el projecte a GitHub per veure l'estat: **https://github.com/BernatMora/hort-osona**

Bona feina! 🌱
