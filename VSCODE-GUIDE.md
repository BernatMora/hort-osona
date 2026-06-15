# 🛠️ Guia de VS Code per al projecte hort-osona

> VS Code és l'editor que farem servir per editar els fitxers `.md` (Markdown) i `.html` del projecte. Aquesta guia t'ensenya el flux de treball bàsic.

## ⌨️ Dreceres essencials

| Acció | Drecera | Notes |
|---|---|---|
| **Obrir paleta de comandes** | `⌘ + Shift + P` | El centre de control de VS Code |
| **Vista prèvia del Markdown** | `⌘ + K` → `V` | Obre costat a costat |
| **Cerca fitxers** | `⌘ + P` | Escriu part del nom |
| **Cerca dins del projecte** | `⌘ + Shift + F` | Cerca text a tots els fitxers |
| **Cerca dins del fitxer** | `⌘ + F` | Substitueix amb `⌘ + H` |
| **Anar a un encapçalament** | `⌘ + Shift + O` | Navega per les seccions del document |
| **Terminal integrat** | `⌘ + ò` (`` ` ``) | Per a `git`, scripts, etc. |
| **Comentari** | `⌘ + /` | Comenta/descomenta línia |

## 📝 Editar un fitxer `.md` (Markdown)

1. **Obre la carpeta del projecte**:
   - `⌘ + O` → selecciona `~/Desktop/hort-osona`
   
2. **Obre un fitxer**:
   - Sidebar esquerre (si no el tens visible: `⌘ + B`) → navega
   - O `⌘ + P` → escriu part del nom (p. ex. "bleda")
   
3. **Edita-lo** com si fos un editor de text normal

4. **Vista prèvia en directe**:
   - `⌘ + K` → `V` (primer K, deixar anar, V)
   - Veure's l'edició a l'esquerra i el render a la dreta
   - Es va actualitzant mentre escrius

5. **Desar**: `⌘ + S`

## 🌐 Obrir un fitxer `.html` al navegador

Per a les calculadores i eines interactives:

1. Click dret al fitxer → **"Reveal in Finder"** (veure'l al Finder)
2. Doble clic → s'obre al navegador per defecte

O des de terminal integrat:
```bash
open -a "Safari" ~/Desktop/hort-osona/calculadora-reg-imprimible.html
```

També pots fer servir l'extensió **Live Server** (veure extensions recomanades) que recarrega automàticament.

## 🔄 Sincronitzar amb Git des de VS Code

### Opció A — Terminal integrat
1. `⌘ + ò` per obrir el terminal
2. Escriu:
   ```bash
   git pull
   # ... editar fitxers ...
   git add .
   git commit -m "El que he canviat"
   git push
   ```
3. O més fàcil, amb el nostre script:
   ```bash
   ./hort-sync.sh "El que he canviat"
   ```

### Opció B — Paleta de comandes
1. `⌘ + Shift + P`
2. Escriu "Tasks: Run Task"
3. Tria "Hort: sync (commit + push)"
4. Escriu el missatge del commit
5. S'executa automàticament

### Opció C — Interfície gràfica
VS Code ja té Git integrat! Mira la barra lateral esquerra:
- 📁 **Explorer** — fitxers
- 🔍 **Search** — cerca
- 🌿 **Source Control** (Ctrl + Shift + G) — aquí tens:
  - Veure els canvis pendents
  - Fer commit amb missatge
  - Push i pull amb botons

## 🧩 Extensions recomanades (ja configurades)

Quan obris el projecte, VS Code et preguntarà si vols instal·lar-les. Accepta!

- **Markdown All in One** — dreceres, llistes, taules, tot
- **markdownlint** — corregeix errors d'estil del Markdown
- **markdown-mermaid** — diagrames dins del Markdown
- **Markdown Preview Enhanced** — vista prèvia millorada
- **Live Server** — servidor local per a HTML (recàrrega automàtica)
- **GitLens** — superpoders per a Git
- **Material Icon Theme** — icones més boniques
- **Catppuccin** — tema de colors suau

## 📂 Estructura típica d'edició

```
VS Code
├── Sidebar (esquerra):   explorador de fitxers
├── Editor (centre):      el fitxer que edites
├── Preview (dreta):      vista prèvia Markdown (⌘K, V)
└── Terminal (a baix):    `⌘ ò` per obrir
```

## 🎨 Personalització

### Canviar el tema
1. `⌘ + K` → `⌘ + T`
2. Tria un dels temes (recomano: "Light+", "Solarized Light", "Catppuccino Latte")

### Augmentar mida de la lletra
1. `⌘ + ,` (preferències)
2. Cerca "font size"
3. Puja-ho a 15-16

### Canviar idioma a català
1. `⌘ + Shift + P` → "Configure Display Language"
2. Busca "Catalan" — si està disponible, canvia

## 📚 Workflow recomanat per al dia a dia

1. **Obre VS Code** amb la carpeta del projecte
2. `⌘ + ò` per obrir el terminal
3. `git pull` (o `hort-sync.sh pull`) per baixar canvis de l'altre PC
4. **Edita** els fitxers que vulguis
5. `⌘ + S` per desar
6. **Revisa** els canvis a la pestanya "Source Control"
7. Fes **commit + push** amb `hort-sync.sh "missatge"` o des de la UI

## 🆘 Si alguna cosa no va

- **No veus la vista prèvia?** → Comprova que el fitxer té extensió `.md`
- **"Git no trobat"?** → VS Code sol trobar-lo sol; sinó, instal·la'l amb `xcode-select --install`
- **Vista prèvia buida?** → Desa el fitxer (`⌘ + S`) i espera 1 segon

## 📖 Recursos

- Documentació oficial: https://code.visualstudio.com/docs
- Markdown en 90 segons: https://commonmark.org/
- Catàcul de Markdown: https://www.markdownguide.org/cheat-sheet/
