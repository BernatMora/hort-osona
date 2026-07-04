#!/usr/bin/env python3
"""
build_portal.py — Construeix el portal web del projecte hort-osona
a partir dels fitxers .md, .html i altres.

El portal resultant (portal.html) és un únic fitxer amb:
- Menú superior amb categories desplegables
- Navegació lateral amb les subseccions
- Vista central del document
- Cerca instantània
- Suport per scroll lateral a les taules

Ús:
  python3 build_portal.py
  python3 build_portal.py --serve    # obre un servidor local per provar
"""

import os
import sys
import re
import json
import html
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
SITE_DIR = BASE / "site"
SITE_DIR.mkdir(exist_ok=True)

# ============================================================
# CATEGORIES (mateixes que l'índex general)
# ============================================================

CATEGORIES = {
    "Inici": [
        ("00-index.md", "Índex general", "Punt de partida del projecte"),
        ("README.md", "README", "Resum ràpid del projecte"),
        ("CHANGELOG.md", "Historial de canvis", "Què s'ha afegit/modificat"),
    ],
    "Planificació": [
        ("pla-12-mesos.md", "Pla dels 12 mesos", "Guia any-tipus"),
        ("08-pla-mensual.md", "Pla d'acció mensual", "Tasques setmanals"),
        ("plans-mensuals/2026-06-juny.md", "Pla juny 2026", "El que toca ara"),
        ("planificacio-tardor-hivern-2026.md", "Tardor-hivern 2026-27", "Planificació temporada freda"),
        ("01-calendari-sembra.md", "Calendari de sembra", "Què sembrar quan"),
        ("calendari-lunar-osona.md", "Calendari lunar", "Biodinàmica lunar"),
        ("calendari-hort-2027.html", "Calendari hort 2027", "Vista any complet"),
        ("pla-hort.md", "Plànol de l'hort", "20 m² esquemàtic"),
        ("pla-hort-esquematic.md", "Plànol esquemàtic", "Versió simplificada"),
        ("pla-hort-illustrat.html", "Plànol il·lustrat", "Versió gràfica"),
        ("croquis-hort.md", "Croquis dibuixable", "Plantilla per imprimir"),
        ("pla-reg-personalitzat-2026.md", "Pla de reg personalitzat", "Adaptat al juny 2026"),
    ],
    "Fitxes de cultiu": [
        ("07-fitxes-cultius/all.md", "All", ""),
        ("07-fitxes-cultius/api.md", "Api", ""),
        ("07-fitxes-cultius/aromatiques.md", "Aromàtiques", ""),
        ("07-fitxes-cultius/bleda.md", "Bleda", ""),
        ("07-fitxes-cultius/carabasso.md", "Carabassó", ""),
        ("07-fitxes-cultius/carbassa.md", "Carbassa", ""),
        ("07-fitxes-cultius/ceba.md", "Ceba", ""),
        ("07-fitxes-cultius/col.md", "Col (kale, bròquil)", ""),
        ("07-fitxes-cultius/enciam.md", "Enciam", ""),
        ("07-fitxes-cultius/fava.md", "Fava", ""),
        ("07-fitxes-cultius/melo.md", "Meló", ""),
        ("07-fitxes-cultius/mongeta.md", "Mongeta", ""),
        ("07-fitxes-cultius/pastanaga.md", "Pastanaga", ""),
        ("07-fitxes-cultius/patata.md", "Patata", ""),
        ("07-fitxes-cultius/pebrot.md", "Pebrot", ""),
        ("07-fitxes-cultius/pesol.md", "Pèsol", ""),
        ("07-fitxes-cultius/porro.md", "Porro", ""),
        ("07-fitxes-cultius/rave.md", "Rave", ""),
        ("07-fitxes-cultius/tomaquet.md", "Tomàquet", ""),
    ],
    "Conreu avançat": [
        ("02-associacions-rotacions.md", "Associacions i rotacions", ""),
        ("03-gestio-plagues.md", "Gestió de plagues", ""),
        ("plagues-guia-visual.md", "Guia visual de plagues", ""),
        ("04-reg-fertilitzacio.md", "Reg i fertilització", ""),
        ("reg-imprimible.html", "Reg (imprimible)", ""),
        ("05-cobertes-adobs-verds.md", "Cobertes i adobs verds", ""),
        ("06-varietats-tradicionals.md", "Varietats tradicionals", ""),
        ("compost.md", "Compost", ""),
        ("planters-guia-completa.md", "Planters", ""),
        ("guardar-llavors.md", "Guardar llavors", ""),
        ("biodinamica-guia-completa.md", "Biodinàmica", ""),
        ("guia-avancada-osona.md", "Guia avançada Osona", ""),
        ("practiques-avancades.md", "Pràctiques avançades", ""),
        ("pla-tractaments-fitosanitaris.md", "Tractaments fitosanitaris", ""),
    ],
    "Eines operatives": [
        ("bitacola-setmanal.md", "Bitàcola setmanal", "Plantilla .md"),
        ("bitacola-setmanal-imprimible.html", "Bitàcola setmanal", "Imprimible"),
        ("calculadora-reg-imprimible.html", "Calculadora de reg", "Interactiva"),
        ("calculadora-sembra.md", "Calculadora de sembra", ""),
        ("pressupost-hort-imprimible.html", "Pressupost anual", "Interactiu"),
        ("HORT-CHECKLIST.md", "Generador de checklist", ""),
    ],
    "Conservació": [
        ("conserves.md", "Conserves", ""),
        ("guia-fermentats.md", "Fermentats", "Xucrut, kimchi, kombucha"),
    ],
    "Sòl i natura": [
        ("analisi-sol-guia-completa.md", "Anàlisi de sòl", ""),
        ("biologia-sol-curs.md", "Biologia del sòl", "Curs complet"),
        ("adventicies-guia-completa.md", "Adventícies", "Males herbes"),
        ("adventicies-utilitat-guia.md", "Adventícies útils", ""),
        ("pollinitzadors-guia-completa.md", "Pol·linitzadors", ""),
        ("canvi-climatic-osona.md", "Canvi climàtic", ""),
    ],
    "Fruiters": [
        ("fruiters-guia-completa.md", "Fruiters", ""),
        ("guia-avancada-osona.md", "Etnobotànica i arbres", ""),
    ],
    "Bolets": [
        ("bolets-guia-completa.md", "Guia de bolets", ""),
        ("bolets-imprimible.html", "Bolets (imprimible)", ""),
        ("bolets-atles-imprimible.html", "Atles visual", ""),
        ("bolets-atles-artistic-imprimible.html", "Atles artístic", ""),
    ],
    "Medicinal i remeieres": [
        ("remeieres-guia-completa.md", "Remeieres (guia completa)", ""),
        ("fitoterapia-curs.md", "Curs de fitoteràpia", ""),
        ("hort-medicinal-guia.md", "Hort medicinal", ""),
        ("hort-amb-nens-manual.md", "Hort amb nens", ""),
        ("apotecaria-casolana-guia.md", "Apotecaria casolana", ""),
        ("olis-massatge-guia.md", "Olis de massatge", ""),
        ("sabons-medicinals-guia.md", "Sabons medicinals", ""),
        ("cremes-ungeunts-especialitzats-guia.md", "Cremes i ungüents", ""),
        ("banys-terapeutics-guia.md", "Banys terapèutics", ""),
        ("productes-curatius-avancats-guia.md", "Productes curatius avançats", ""),
        ("primers-auxilis-verds-manual.md", "Primers auxilis verds", ""),
        ("curatius-resum-final.md", "Resum productes curatius", ""),
    ],
    "Eines i tecnologia": [
        ("eines-digitals-guia.md", "Eines digitals", ""),
        ("apps-planificacio-guia.md", "Apps de planificació", ""),
        ("rendiment-hort-guia.md", "Anàlisi de rendiment", ""),
    ],
    "Projectes familiars": [
        ("botiga-casolana-guia.md", "Botiga casolana", ""),
        ("decoracio-natural-manual.md", "Decoració natural", ""),
    ],
    "El meu hort": [
        ("fitxa-hort.md", "Fitxa del meu hort", ""),
        ("plans-mensuals/quadern-observacio-2026.md", "Quadern d'observacions 2026", ""),
        ("resum-final-base-coneixement.md", "Resum final base coneixement", ""),
    ],
    "Configuració": [
        ("VSCODE-GUIDE.md", "Guia de VS Code", ""),
        ("SETUP-WINDOWS.md", "Setup Windows", ""),
        ("SYNC-SCRIPT.md", "Ús dels scripts hort-sync", ""),
        ("SETUP-SITE.md", "Com regenerar el web", ""),
        ("SETUP-GITHUB-PAGES.md", "Publicar a GitHub Pages", ""),
    ],
}


# ============================================================
# CONVERSIÓ MARKDOWN → HTML (senzilla, sense dependències)
# ============================================================

def md_to_html(md_text):
    """Converteix Markdown bàsic a HTML."""
    if not md_text:
        return ""

    text = md_text
    # Extracció de blocs de codi (preservar)
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(1))
        return f"@@CODEBLOCK{len(code_blocks)-1}@@"
    text = re.sub(r"```([\s\S]*?)```", save_code, text)

    # Processar línia a línia
    lines = text.split("\n")
    out = []
    in_list = False
    in_ordered = False
    in_quote = False
    in_table = False
    table_rows = []

    def close_list():
        nonlocal in_list, in_ordered
        if in_list:
            out.append("</ul>")
            in_list = False
        if in_ordered:
            out.append("</ol>")
            in_ordered = False

    def close_quote():
        nonlocal in_quote
        if in_quote:
            out.append("</blockquote>")
            in_quote = False

    def close_table():
        nonlocal in_table, table_rows
        if in_table:
            # Processar les files acumulades
            html_table = ['<div class="table-wrap"><table>']
            for i, row in enumerate(table_rows):
                cells = [c.strip() for c in row.split("|")[1:-1]]
                tag = "th" if i == 0 else "td"
                html_table.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
            html_table.append("</table></div>")
            out.append("".join(html_table))
            in_table = False
            table_rows = []

    def inline(s):
        # Negreta, cursiva, codi, enllaços
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"__(.+?)__", r"<strong>\1</strong>", s)
        s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
        s = re.sub(r"_(.+?)_", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        # Enllaços [text](url)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}" target="_blank">{m.group(1)}</a>', s)
        # Línies horitzontals
        return s

    for line in lines:
        # Línia horitzontal
        if re.match(r"^-{3,}$|^\*{3,}$", line.strip()):
            close_list(); close_quote(); close_table()
            out.append("<hr>")
            continue

        # Títols
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            close_list(); close_quote(); close_table()
            level = len(m.group(1))
            text_inline = inline(m.group(2).strip())
            # Generar ID per a l'àncora
            anchor = re.sub(r"[^a-z0-9-]", "-", m.group(2).lower())
            anchor = re.sub(r"-+", "-", anchor).strip("-")
            out.append(f'<h{level} id="{anchor}">{text_inline}</h{level}>')
            continue

        # Llistes no ordenades
        m = re.match(r"^[\s]*[-*]\s+(.*)", line)
        if m:
            close_quote(); close_table()
            if in_ordered:
                out.append("</ol>"); in_ordered = False
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue

        # Llistes ordenades
        m = re.match(r"^[\s]*\d+\.\s+(.*)", line)
        if m:
            close_quote(); close_table()
            if in_list:
                out.append("</ul>"); in_list = False
            if not in_ordered:
                out.append("<ol>"); in_ordered = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue

        # Cites
        m = re.match(r"^>\s?(.*)", line)
        if m:
            close_list(); close_table()
            if not in_quote:
                out.append("<blockquote>"); in_quote = True
            out.append(f"<p>{inline(m.group(1))}</p>")
            continue

        # Taules
        if "|" in line and not line.strip().startswith("```"):
            close_list(); close_quote()
            # Detectar fila separadora (---|---|)
            if re.match(r"^\s*\|?[\s\-|:]+\|?\s*$", line) and "-" in line:
                in_table = True
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(line)
            continue
        else:
            close_table()

        # Paràgrafs
        close_list(); close_quote()
        if line.strip():
            out.append(f"<p>{inline(line)}</p>")
        else:
            out.append("")

    close_list(); close_quote(); close_table()

    # Restaurar blocs de codi
    result = "\n".join(out)
    for i, code in enumerate(code_blocks):
        code_escaped = html.escape(code.strip())
        result = result.replace(f"@@CODEBLOCK{i}@@", f'<pre><code>{code_escaped}</code></pre>')

    return result


# ============================================================
# GENERACIÓ DELS JSON DE DOCUMENTS
# ============================================================

def extract_title(text, fallback):
    """Extreu el primer títol (H1) del text markdown."""
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            # Treure emojis inicials i netejar
            title = line[2:].strip()
            return title
    return fallback

def get_doc_text(path):
    """Llegeix el text d'un document. Si és .md, retorna el text. Si és .html, retorna l'HTML interior."""
    if not path.exists():
        return None, None

    def sanitize(s):
        if not s: return s
        # Escapar seqüències que trenquen un <script> pare
        s = s.replace("</script", "<\\/script")
        s = s.replace("<!--", "<\\!--")
        return s

    if path.suffix == ".md":
        try:
            text = path.read_text(encoding="utf-8")
            title = extract_title(text, path.stem)
            html_content = md_to_html(text)
            return title, sanitize(html_content)
        except Exception as e:
            return None, f"<p style='color:#a00'>Error llegint {path}: {e}</p>"

    elif path.suffix == ".html":
        try:
            text = path.read_text(encoding="utf-8")
            title = extract_title_from_html(text, path.stem)
            # Extreure el cos (tot el que hi ha dins <body>)
            m = re.search(r"<body[^>]*>(.*?)</body>", text, re.DOTALL | re.IGNORECASE)
            if m:
                body = m.group(1)
            else:
                body = text
            return title, sanitize(body)
        except Exception as e:
            return None, f"<p style='color:#a00'>Error llegint {path}: {e}</p>"

    return None, None


def extract_title_from_html(text, fallback):
    m = re.search(r"<title>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.IGNORECASE | re.DOTALL)
    if m:
        # Treure tags HTML restants
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return fallback


# ============================================================
# CSS
# ============================================================

CSS = """
:root {
  --c-bg:        #F5EBD8;
  --c-bg-2:      #EFE3CB;
  --c-paper:     #FBF5E6;
  --c-ink:       #2B2418;
  --c-ink-2:     #5A4F3A;
  --c-line:      #D8C8A5;
  --c-line-2:    #C4B189;
  --c-olive:     #3D4A2A;
  --c-leaf:      #5C7A3A;
  --c-ochre:     #A8783E;
  --c-mud:       #6B4F2A;
  --c-accent-bg: #E8D9B0;
  --c-red:       #8C3A1A;
  --shadow:      0 1px 0 rgba(60,40,15,0.05), 0 2px 6px rgba(60,40,15,0.05);
  --radius:      6px;
  --header-h:    64px;
  --nav-h:       50px;
  --sidebar-w:   280px;
  --reading-max: 1000px;
}
*,*::before,*::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--c-bg); color: var(--c-ink); }
body {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  font-size: 16px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}

/* ===== HEADER ===== */
header {
  position: fixed; top: 0; left: 0; right: 0;
  height: var(--header-h);
  background: var(--c-olive);
  color: var(--c-paper);
  display: flex; align-items: center;
  padding: 0 1.5rem;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
header .logo {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.4rem; font-weight: 700;
  margin-right: 2rem;
  white-space: nowrap;
}
header .logo a { color: inherit; text-decoration: none; }
header .logo-sub {
  display: block;
  font-size: 0.7rem; font-weight: 400;
  opacity: 0.7; font-family: 'Inter', sans-serif;
  margin-top: 2px;
}
header .search {
  flex: 1; max-width: 480px;
  position: relative;
}
header .search input {
  width: 100%;
  padding: 0.55rem 2.5rem 0.55rem 1rem;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 4px;
  background: rgba(255,255,255,0.1);
  color: var(--c-paper);
  font-size: 0.95rem;
}
header .search input::placeholder { color: rgba(255,255,255,0.6); }
header .search input:focus { outline: none; background: rgba(255,255,255,0.2); }
header .search .results {
  position: absolute; top: 100%; left: 0; right: 0;
  background: var(--c-paper);
  color: var(--c-ink);
  max-height: 60vh; overflow-y: auto;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  display: none;
}
header .search .results.active { display: block; }
header .search .result-item {
  padding: 0.6rem 1rem;
  border-bottom: 1px solid var(--c-line);
  cursor: pointer;
  font-size: 0.9rem;
}
header .search .result-item:hover { background: var(--c-accent-bg); }
header .search .result-item .cat {
  font-size: 0.7rem; color: var(--c-ink-2);
  text-transform: uppercase; letter-spacing: 0.05em;
}
header .search .no-results { padding: 1rem; color: var(--c-ink-2); text-align: center; }
header .actions {
  margin-left: 1.5rem;
  display: flex; gap: 0.5rem;
}
header .actions a, header .actions button {
  background: rgba(255,255,255,0.1);
  color: var(--c-paper);
  border: 1px solid rgba(255,255,255,0.2);
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.85rem;
  display: inline-flex; align-items: center; gap: 0.3rem;
}
header .actions a:hover, header .actions button:hover { background: rgba(255,255,255,0.2); }

/* ===== NAV ===== */
nav.categories {
  position: fixed; top: var(--header-h); left: 0; right: 0;
  height: var(--nav-h);
  background: var(--c-paper);
  border-bottom: 1px solid var(--c-line);
  z-index: 90;
  display: flex; align-items: center;
  padding: 0 1rem;
  gap: 0.3rem;
  overflow-x: auto;
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
nav.categories .cat {
  position: relative;
}
nav.categories .cat-btn {
  background: none;
  border: none;
  padding: 0.6rem 1rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--c-ink);
  cursor: pointer;
  border-radius: 4px;
  display: inline-flex; align-items: center; gap: 0.3rem;
  font-family: inherit;
}
nav.categories .cat-btn:hover, nav.categories .cat-btn.active {
  background: var(--c-accent-bg);
}
nav.categories .cat-btn .arrow { font-size: 0.7rem; opacity: 0.6; }
nav.categories .dropdown {
  position: absolute; top: 100%; left: 0;
  background: var(--c-paper);
  border: 1px solid var(--c-line);
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  min-width: 320px;
  max-height: 70vh;
  overflow-y: auto;
  display: none;
  padding: 0.5rem 0;
}
nav.categories .cat:hover .dropdown,
nav.categories .cat.open .dropdown { display: block; }
nav.categories .dropdown a {
  display: block;
  padding: 0.5rem 1rem;
  color: var(--c-ink);
  text-decoration: none;
  font-size: 0.88rem;
  border-left: 3px solid transparent;
}
nav.categories .dropdown a:hover {
  background: var(--c-accent-bg);
  border-left-color: var(--c-olive);
}
nav.categories .dropdown a .desc {
  display: block;
  font-size: 0.75rem;
  color: var(--c-ink-2);
  margin-top: 2px;
}

/* ===== LAYOUT ===== */
main {
  padding-top: calc(var(--header-h) + var(--nav-h) + 1rem);
  padding-bottom: 2rem;
  padding-left: 1rem;
  padding-right: 1rem;
  display: grid;
  grid-template-columns: var(--sidebar-w) 1fr;
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

aside.sidebar {
  position: sticky;
  top: calc(var(--header-h) + var(--nav-h) + 1rem);
  align-self: start;
  max-height: calc(100vh - var(--header-h) - var(--nav-h) - 2rem);
  overflow-y: auto;
  background: var(--c-paper);
  border: 1px solid var(--c-line);
  border-radius: var(--radius);
  padding: 1rem;
  font-size: 0.88rem;
}
aside.sidebar h3 {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.1rem;
  margin: 0 0 0.7rem 0;
  color: var(--c-olive);
}
aside.sidebar .sec {
  margin-bottom: 0.8rem;
}
aside.sidebar .sec h4 {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--c-ink-2);
  margin: 0 0 0.3rem 0;
  font-weight: 600;
  cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
}
aside.sidebar .sec h4 .arrow { transition: transform 0.2s; }
aside.sidebar .sec.collapsed h4 .arrow { transform: rotate(-90deg); }
aside.sidebar .sec ul {
  list-style: none; margin: 0; padding: 0;
}
aside.sidebar .sec.collapsed ul { display: none; }
aside.sidebar .sec li a {
  display: block; padding: 0.3rem 0.5rem;
  color: var(--c-ink);
  text-decoration: none;
  border-radius: 3px;
  font-size: 0.85rem;
}
aside.sidebar .sec li a:hover { background: var(--c-accent-bg); }
aside.sidebar .sec li a.active { background: var(--c-olive); color: var(--c-paper); }
aside.sidebar .toggle-sidebar {
  background: var(--c-olive);
  color: var(--c-paper);
  border: none;
  padding: 0.3rem 0.6rem;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.75rem;
  margin-bottom: 0.5rem;
  width: 100%;
}
body.no-sidebar main { grid-template-columns: 1fr; }

article.content {
  background: var(--c-paper);
  border: 1px solid var(--c-line);
  border-radius: var(--radius);
  padding: 2rem 2.5rem;
  min-height: 60vh;
  max-width: var(--reading-max);
  margin: 0 auto;
  width: 100%;
  box-shadow: var(--shadow);
}

article.content h1 {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 2.2rem; font-weight: 700;
  color: var(--c-olive);
  margin: 0 0 0.3rem 0;
  line-height: 1.2;
}
article.content h1 + p, article.content > p:first-of-type {
  color: var(--c-ink-2); font-size: 0.95rem;
  margin-bottom: 1.5rem;
  font-style: italic;
}
article.content h2 {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.5rem; font-weight: 600;
  color: var(--c-olive);
  margin: 2rem 0 0.8rem;
  border-bottom: 1px solid var(--c-line);
  padding-bottom: 0.3rem;
}
article.content h3 { font-size: 1.15rem; color: var(--c-leaf); margin: 1.5rem 0 0.5rem; }
article.content h4 { font-size: 1rem; color: var(--c-mud); margin: 1.2rem 0 0.4rem; }
article.content p { margin: 0.7rem 0; }
article.content ul, article.content ol { margin: 0.5rem 0; padding-left: 1.5rem; }
article.content li { margin: 0.3rem 0; }
article.content blockquote {
  border-left: 4px solid var(--c-ochre);
  background: var(--c-accent-bg);
  margin: 1rem 0;
  padding: 0.7rem 1rem;
  font-style: italic;
  border-radius: 0 var(--radius) var(--radius) 0;
}
article.content blockquote p { margin: 0.3rem 0; }
article.content code {
  background: var(--c-bg-2);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.88em;
  color: var(--c-mud);
}
article.content pre {
  background: #1a1a1a;
  color: #e8e8e8;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 0.85rem;
}
article.content pre code { background: none; color: inherit; padding: 0; }
article.content hr { border: none; border-top: 1px dashed var(--c-line); margin: 2rem 0; }
article.content a { color: var(--c-olive); }
article.content a:hover { text-decoration: underline; }
article.content img { max-width: 100%; height: auto; border-radius: 4px; }

/* Taules amb scroll lateral */
article.content .table-wrap {
  overflow-x: auto;
  margin: 1rem 0;
  border: 1px solid var(--c-line);
  border-radius: 4px;
  background: var(--c-bg-2);
}
article.content table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
  min-width: 400px;
}
article.content th {
  background: var(--c-olive);
  color: var(--c-paper);
  padding: 0.6rem 0.8rem;
  text-align: left;
  font-weight: 600;
  position: sticky; top: 0;
  z-index: 1;
}
article.content td {
  padding: 0.5rem 0.8rem;
  border-bottom: 1px solid var(--c-line);
  vertical-align: top;
}
article.content tr:nth-child(even) td { background: var(--c-accent-bg); }
article.content tr:hover td { background: var(--c-bg); }

/* ===== WELCOME ===== */
article.welcome {
  text-align: center;
  padding: 3rem 2rem;
}
article.welcome h1 {
  font-size: 2.5rem; margin-bottom: 0.5rem;
}
article.welcome .lead {
  font-size: 1.1rem; color: var(--c-ink-2);
  max-width: 600px; margin: 0 auto 2rem;
}
article.welcome .stats {
  display: flex; justify-content: center; gap: 2rem;
  margin: 2rem 0; flex-wrap: wrap;
}
article.welcome .stat {
  background: var(--c-bg-2);
  padding: 1rem 1.5rem;
  border-radius: var(--radius);
  min-width: 120px;
}
article.welcome .stat .num {
  font-size: 2rem; font-weight: 700;
  color: var(--c-olive);
  font-family: 'Fraunces', serif;
}
article.welcome .stat .lbl { font-size: 0.85rem; color: var(--c-ink-2); }
article.welcome .quickstart {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.8rem;
  max-width: 700px; margin: 2rem auto 0;
  text-align: left;
}
article.welcome .quickstart a {
  display: block; padding: 0.7rem 1rem;
  background: var(--c-bg-2);
  color: var(--c-ink);
  text-decoration: none;
  border-radius: 4px;
  border-left: 4px solid var(--c-olive);
}
article.welcome .quickstart a:hover { background: var(--c-accent-bg); }

/* ===== BREADCRUMBS ===== */
.breadcrumb {
  font-size: 0.8rem;
  color: var(--c-ink-2);
  margin-bottom: 0.5rem;
}
.breadcrumb a { color: var(--c-ink-2); text-decoration: none; }
.breadcrumb a:hover { color: var(--c-olive); text-decoration: underline; }
.breadcrumb .sep { margin: 0 0.4rem; opacity: 0.5; }

/* ===== MOBILE ===== */
@media (max-width: 900px) {
  main { grid-template-columns: 1fr; }
  aside.sidebar {
    position: static;
    max-height: none;
  }
  header .logo-sub { display: none; }
  header .actions { display: none; }
  article.content { padding: 1.2rem 1rem; }
  nav.categories { padding: 0 0.5rem; }
  nav.categories .cat-btn { padding: 0.5rem 0.6rem; font-size: 0.85rem; }
}

/* ===== PRINT ===== */
@media print {
  header, nav.categories, aside.sidebar { display: none; }
  main { padding: 0; display: block; }
  article.content {
    box-shadow: none; border: none; max-width: 100%;
  }
  .table-wrap { overflow: visible; }
}
"""


# ============================================================
# JAVASCRIPT
# ============================================================

JS = """
const STATE = {
  currentDoc: null,
  docs: {},
  sidebarVisible: true,
};

// Carregar documents
async function loadDoc(path) {
  if (STATE.docs[path] !== undefined) {
    return STATE.docs[path];
  }
  return null; // ja estan tots incrustats
}

function showDoc(path) {
  const data = STATE.docs[path];
  if (!data) return;

  STATE.currentDoc = path;
  const content = document.getElementById('content');
  // Desescapar les substitucions fetes al build (split/join és més segur que regex)
  let html = data.html || '<p style="color:#a00">No s\\'ha pogut carregar el document.</p>';
  html = html.split('<\\/script').join('</script');
  html = html.split('<\\!--').join('<!--');
  content.innerHTML = html;

  // Actualitzar sidebar
  document.querySelectorAll('aside.sidebar a').forEach(a => {
    a.classList.toggle('active', a.dataset.path === path);
  });

  // Actualitzar breadcrumb
  const cat = data.cat || '';
  const title = data.title || path;
  document.getElementById('breadcrumb').innerHTML =
    `<a href="#" onclick="goHome()">Inici</a> <span class="sep">/</span> ` +
    `<span>${cat}</span> <span class="sep">/</span> ` +
    `<strong>${title}</strong>`;

  // Tancar menú obert
  document.querySelectorAll('.cat.open').forEach(c => c.classList.remove('open'));

  // Scroll a dalt
  window.scrollTo({top: 0, behavior: 'smooth'});
  content.scrollTop = 0;

  // Tancar sidebar en mòbil
  if (window.innerWidth < 900) {
    document.body.classList.remove('no-sidebar');
  }

  // Historial
  if (history.pushState) {
    history.pushState({path}, '', '#' + encodeURIComponent(path));
  }
}

function goHome() {
  STATE.currentDoc = null;
  document.getElementById('content').innerHTML = document.getElementById('welcome').innerHTML;
  document.querySelectorAll('aside.sidebar a').forEach(a => a.classList.remove('active'));
  document.getElementById('breadcrumb').innerHTML = '<strong>Inici</strong>';
  if (history.pushState) history.pushState({}, '', '#');
}

function init() {
  // Carregar STATE.docs des de l'objecte injectat
  if (window.PORTAL_DATA) {
    STATE.docs = window.PORTAL_DATA;
  }

  // Receptar canvis a la URL
  window.addEventListener('popstate', (e) => {
    const path = (e.state && e.state.path) || (location.hash ? decodeURIComponent(location.hash.slice(1)) : null);
    if (path && STATE.docs[path]) showDoc(path);
    else goHome();
  });

  // Establir hash inicial
  const initialPath = location.hash ? decodeURIComponent(location.hash.slice(1)) : null;
  if (initialPath && STATE.docs[initialPath]) {
    showDoc(initialPath);
  }

  // Cerca
  setupSearch();
}

function setupSearch() {
  const input = document.getElementById('searchInput');
  const results = document.getElementById('searchResults');
  if (!input) return;

  let timer;
  input.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(() => doSearch(input.value), 200);
  });
  input.addEventListener('focus', () => {
    if (input.value.length >= 2) doSearch(input.value);
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search')) results.classList.remove('active');
  });
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { input.value = ''; results.classList.remove('active'); }
  });
}

function doSearch(q) {
  const results = document.getElementById('searchResults');
  q = q.trim().toLowerCase();
  if (q.length < 2) { results.classList.remove('active'); return; }

  const matches = [];
  for (const [path, data] of Object.entries(STATE.docs)) {
    const title = (data.title || '').toLowerCase();
    const cat = (data.cat || '').toLowerCase();
    const text = (data.text || '').toLowerCase();
    const ti = title.includes(q) ? 10 : 0;
    const ci = cat.includes(q) ? 3 : 0;
    const xi = text.includes(q) ? 1 : 0;
    if (ti + ci + xi > 0) {
      matches.push({path, title: data.title, cat: data.cat, score: ti + ci + xi});
    }
  }
  matches.sort((a, b) => b.score - a.score);
  matches.splice(15);

  if (matches.length === 0) {
    results.innerHTML = '<div class="no-results">Cap resultat</div>';
  } else {
    results.innerHTML = matches.map(m =>
      `<div class="result-item" onclick="showDoc('${m.path}')">` +
      `<div class="cat">${m.cat}</div>` +
      `<strong>${m.title}</strong></div>`
    ).join('');
  }
  results.classList.add('active');
}

function toggleSidebar() {
  document.body.classList.toggle('no-sidebar');
}

// Tancar dropdowns en clicar fora
document.addEventListener('click', (e) => {
  if (!e.target.closest('.cat')) {
    document.querySelectorAll('.cat.open').forEach(c => c.classList.remove('open'));
  }
});

// Sidebar: collapse sections
function initSidebar() {
  document.querySelectorAll('aside.sidebar .sec h4').forEach(h => {
    h.addEventListener('click', () => {
      h.parentElement.classList.toggle('collapsed');
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  init();
  initSidebar();
});
"""


# ============================================================
# BENvinguda
# ============================================================

def make_welcome(n_docs, n_fitxes, n_cats):
    return f"""<article class="welcome">
  <h1>🌱 Hort Osona</h1>
  <p class="lead">Base de coneixement personal d'horticultura ecològica, plantes medicinals i conserves, adaptat a la comarca d'Osona.</p>

  <div class="stats">
    <div class="stat"><div class="num">{n_docs}</div><div class="lbl">Documents</div></div>
    <div class="stat"><div class="num">{n_fitxes}</div><div class="lbl">Fitxes cultiu</div></div>
    <div class="stat"><div class="num">{n_cats}</div><div class="lbl">Categories</div></div>
  </div>

  <h2 style="margin-top:2rem;">Com començar</h2>
  <p style="color:var(--c-ink-2); max-width:600px; margin:0 auto 1.5rem;">
    Navega pel menú superior desplegable o usa la cerca. Cada categoria té tots els seus documents organitzats.
  </p>

  <div class="quickstart">
    <a href="#" data-path="pla-12-mesos.md">📅 Pla dels 12 mesos</a>
    <a href="#" data-path="plans-mensuals/2026-06-juny.md">🌱 Pla juny 2026</a>
    <a href="#" data-path="07-fitxes-cultius/tomaquet.md">🍅 Tomàquet</a>
    <a href="#" data-path="01-calendari-sembra.md">📅 Calendari de sembra</a>
    <a href="#" data-path="02-associacions-rotacions.md">🌿 Associacions</a>
    <a href="#" data-path="pla-tractaments-fitosanitaris.md">🧪 Tractaments</a>
  </div>
</article>"""


def main():
    print("🌱 Construint portal hort-osona...")

    # Carregar tots els documents
    docs = {}
    errors = []
    for cat_name, items in CATEGORIES.items():
        for entry in items:
            if len(entry) == 2:
                path_str, title = entry
                desc = ""
            else:
                path_str, title, desc = entry
            path = BASE / path_str
            if not path.exists():
                errors.append(f"  ❌ No trobat: {path_str}")
                continue
            t, content = get_doc_text(path)
            if t is None and content is None:
                errors.append(f"  ❌ Error: {path_str}")
                continue
            docs[path_str] = {
                "title": t or title,
                "html": content or "",
                "cat": cat_name,
                "desc": desc or title,
                "text": (t or "") + " " + (content or ""),  # per a cerca
            }

    print(f"  ✅ {len(docs)} documents carregats")
    if errors:
        print("Errors:")
        for e in errors:
            print(e)

    # Limitar mida del camp "text" (per a JSON lleuger)
    for k, v in docs.items():
        if len(v.get("text", "")) > 5000:
            v["text"] = v["text"][:5000]

    # Construir el portal
    portal_data_json = json.dumps(docs, ensure_ascii=False)

    # HTML de la nav superior
    nav_html = ""
    for cat_name, items in CATEGORIES.items():
        items_html = "".join(
            f'<a href="#" data-path="{e[0]}" onclick="showDoc(\'{e[0]}\'); return false;">' +
            f'<strong>{e[1] if len(e)>=2 else e[0]}</strong>' +
            (f'<span class="desc">{e[2]}</span>' if len(e) >= 3 and e[2] else '') +
            '</a>'
            for e in items if e[0] in docs
        )
        nav_html += f'<div class="cat"><button class="cat-btn" type="button">{cat_name} <span class="arrow">▾</span></button><div class="dropdown">{items_html}</div></div>'

    # HTML del sidebar
    sidebar_html = ""
    for cat_name, items in CATEGORIES.items():
        items_html = "".join(
            f'<li><a href="#" data-path="{e[0]}" onclick="showDoc(\'{e[0]}\'); return false;">{e[1] if len(e)>=2 else ""}</a></li>'
            for e in items if e[0] in docs
        )
        if items_html:
            sidebar_html += f'<div class="sec"><h4>{cat_name} <span class="arrow">▼</span></h4><ul>{items_html}</ul></div>\n'

    n_fitxes = len([d for d in docs if d.startswith('07-fitxes-cultius/') and not d.endswith('_plantilla.md')])
    welcome_html = make_welcome(len(docs), n_fitxes, len(CATEGORIES))

    portal_html = """<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Base de coneixement d'hort ecològic a Osona — portal centralitzat">
<meta name="theme-color" content="#3D4A2A">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Hort Osona">
<meta name="mobile-web-app-capable" content="yes">
<title>Hort Osona · Portal</title>
<link rel="manifest" href="manifest.json">
<link rel="icon" type="image/svg+xml" href="icon.svg">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="icon-512.png">
<link rel="apple-touch-icon" href="icon-192.png">
<link rel="apple-touch-icon" sizes="512x512" href="icon-512.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>__CSS__</style>
</head>
<body>

<header>
  <div class="logo">
    <a href="#" id="logoLink">🌱 Hort Osona</a>
    <span class="logo-sub">Base de coneixement</span>
  </div>
  <div class="search">
    <input type="search" id="searchInput" placeholder="Cerca a tots els documents... (mín. 2 lletres)" autocomplete="off">
    <div id="searchResults" class="results"></div>
  </div>
  <div class="actions">
    <button onclick="window.print()" title="Imprimir">🖨️ Imprimir</button>
    <a href="https://github.com/BernatMora/hort-osona" target="_blank" title="Repositori GitHub">💻 GitHub</a>
  </div>
</header>

<nav class="categories">
__NAV__
</nav>

<main>
  <aside class="sidebar">
    <button class="toggle-sidebar" onclick="toggleSidebar()">⇆ Amagar/mostrar menú</button>
__SIDEBAR__
  </aside>

  <article class="content" id="content">
    <div class="breadcrumb" id="breadcrumb"></div>
    <div id="contentInner">
__WELCOME__
    </div>
  </article>
</main>

<!-- Dades del portal -->
<script>
window.PORTAL_DATA = __PORTAL_DATA__;
</script>

<script>__JS__</script>

</body>
</html>"""

    portal_html = portal_html.replace("__CSS__", CSS)
    portal_html = portal_html.replace("__NAV__", nav_html)
    portal_html = portal_html.replace("__SIDEBAR__", sidebar_html)
    portal_html = portal_html.replace("__WELCOME__", welcome_html)
    portal_html = portal_html.replace("__JS__", JS)
    portal_html = portal_html.replace("__PORTAL_DATA__", portal_data_json)

    # Guardar
    out_path = BASE / "index.html"
    out_path.write_text(portal_html, encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024
    print(f"\n✅ Portal generat: {out_path}")
    print(f"   Mida: {size_kb:.1f} KB")
    print(f"   Documents: {len(docs)}")
    print(f"   Categories: {len(CATEGORIES)}")

    # Copiar assets PWA a l'arrel (per a GitHub Pages i PWA mòbil)
    import shutil
    assets = [
        ("site/manifest.json", "manifest.json"),
        ("site/icon.svg", "icon.svg"),
        ("site/icon-192.png", "icon-192.png"),
        ("site/icon-512.png", "icon-512.png"),
        ("site/service-worker.js", "service-worker.js"),
    ]
    copied = []
    for src, dst in assets:
        src_path = BASE / src
        dst_path = BASE / dst
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            copied.append(dst)
    if copied:
        print(f"   Assets PWA copiats: {', '.join(copied)}")

    print(f"\nPer provar-lo:")
    print(f"  open ~/Desktop/hort-osona/index.html")
    print(f"  python3 -m http.server 8000  (a ~/Desktop/hort-osona)")


if __name__ == "__main__":
    main()
