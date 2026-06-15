# 🚜 hort-sync — Sincronització ràpida

Script que fa `pull + add + commit + push` en una sola ordre. N'hi ha un per Mac (`hort-sync.sh`) i un per Windows (`hort-sync.bat`).

## 📦 Instal·lació

### Mac (zsh)
L'script ja és dins del projecte. Per poder cridar-lo des de qualsevol lloc, afegeix un àlies al teu `.zshrc`:

```bash
echo 'alias hort-sync="~/Desktop/hort-osona/hort-sync.sh"' >> ~/.zshrc
source ~/.zshrc
```

### Windows (cmd / PowerShell)
L'script ja és dins del projecte. Per cridar-lo des de qualsevol lloc, afegeix el directori al PATH o crea un àlies de PowerShell:

**Opció 1 — Afegir al PATH** (obert a Configuració → Sistema → Variables d'entorn):
```
%USERPROFILE%\Documents\hort-osona
```

**Opció 2 — Àlies a PowerShell** (afegir al perfil `$PROFILE`):
```powershell
function hort-sync { & "C:\Users\elteuusuari\Documents\hort-osona\hort-sync.bat" $args }
```

## 🚀 Ús

Des de qualsevol lloc, simplement:

```bash
# Mac
hort-sync                    # pull, status, add, commit (et demana missatge), push
hort-sync "missatge"         # amb missatge directe
hort-sync pull               # només baixar canvis
hort-sync push "missatge"    # pujar (després de pull)
hort-sync status             # veure què hi ha pendent
hort-sync help               # ajuda
```

```cmd
:: Windows (cmd)
hort-sync.bat
hort-sync.bat "missatge"
hort-sync.bat pull
hort-sync.bat status
```

## 🔁 Workflow recomanat

1. **Matí a l'ordinador A:**
   ```bash
   hort-sync        # baixa canvis de l'altre PC
   # ... treballar ...
   hort-sync "afegeixo nova fitxa de col"   # al final del dia
   ```

2. **A l'ordinador B (quan hi arribis):**
   ```bash
   hort-sync        # baixa canvis del PC A
   # ... treballar ...
   hort-sync "actualitzo pla juliol"   # al final
   ```

3. **Tots dos treballen alhora?** Cap problema — cada `hort-sync` fa `pull` abans de `push`. Si hi ha conflicte (mateix fitxer, mateixa línia), t'avisarà.

## ⚠️ Si hi ha conflicte

L'script atura i et diu:
```
❌ Hi ha hagut conflictes. Resol'ls manualment i torna-ho a provar.
```

Solució:
1. `git status` — veuràs els fitxers en conflicte
2. Obre'ls amb un editor (VS Code marca els conflictes visualment)
3. Tria què queda, elimina els marcadors `<<<<`, `====`, `>>>>`
4. `git add .` + `git commit -m "Resolc conflicte"` + `git push`

## 🛠️ Detalls tècnics

- L'script detecta automàticament el directori del projecte (busca `.git/` amunt i avall).
- El pull utilitza `--rebase --autostash` per evitar commits innecessaris de merge.
- Si no proporciones missatge, et el demana interactiuament.
- Si encara no tens res a pujar, et diu "Tot sincronitzat" i no fa cap commit buit.
