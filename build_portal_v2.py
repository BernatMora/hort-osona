#!/usr/bin/env python3
"""
build_portal_v2.py — Reenginyeria del portal hort-osona, mobile-first.

Layout:
- MOBILE (<768px): header compacte + contingut a pantalla completa
  + ☰ que obre un drawer lateral amb les categories
- DESKTOP (>=768px): sidebar fixa 280px + contingut a la dreta

Principis:
- Cap element absolute que sobresurti
- Cap z-index estrany
- Un sol fitxer HTML amb tot incrustat
- Sense dependències externes (fora Google Fonts)
"""

import sys
import json
import re
import html
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

BASE = Path("/Users/bernatmorasanglas/Desktop/hort-osona")

# ──────────── CATEGORIES (mateix ordre que abans) ────────────
CATEGORIES: Dict[str, List[Tuple[str, str]]] = {
    "Inici": [
        ("00-index.md", "Índex general"),
        ("README.md", "README"),
        ("CHANGELOG.md", "Historial"),
    ],
    "Planificació": [
        ("pla-12-mesos.md", "Pla dels 12 mesos"),
        ("08-pla-mensual.md", "Pla d'acció mensual"),
        ("plans-mensuals/2026-06-juny.md", "Pla juny 2026"),
        ("planificacio-tardor-hivern-2026.md", "Tardor-hivern 2026-27"),
        ("01-calendari-sembra.md", "Calendari de sembra"),
        ("calendari-lunar-osona.md", "Calendari lunar"),
        ("fitxa-hort.md", "Plànol de l'hort"),
        ("pla-hort.md", "Plànol esquemàtic"),
        ("pla-reg-personalitzat-2026.md", "Pla de reg personalitzat"),
        ("croquis-hort.md", "Croquis dibuixable"),
    ],
    "Fitxes de cultiu": [
        ("07-fitxes-cultius/all.md", "All"),
        ("07-fitxes-cultius/alfabrega.md", "Alfàbrega"),
        ("07-fitxes-cultius/api.md", "Api"),
        ("07-fitxes-cultius/bleda.md", "Bleda"),
        ("07-fitxes-cultius/carbassa.md", "Carbassa"),
        ("07-fitxes-cultius/carabasso.md", "Carabassó"),
        ("07-fitxes-cultius/ceba.md", "Ceba"),
        ("07-fitxes-cultius/col.md", "Col"),
        ("07-fitxes-cultius/enciam.md", "Enciam"),
        ("07-fitxes-cultius/escarola.md", "Escarola"),
        ("07-fitxes-cultius/espinac.md", "Espinac"),
        ("07-fitxes-cultius/farigola.md", "Farigola"),
        ("07-fitxes-cultius/fava.md", "Fava"),
        ("07-fitxes-cultius/melo.md", "Meló"),
        ("07-fitxes-cultius/menta.md", "Menta"),
        ("07-fitxes-cultius/mongeta.md", "Mongeta"),
        ("07-fitxes-cultius/orenga.md", "Orenga"),
        ("07-fitxes-cultius/pastanaga.md", "Pastanaga"),
        ("07-fitxes-cultius/patata.md", "Patata"),
        ("07-fitxes-cultius/pebrot.md", "Pebrot"),
        ("07-fitxes-cultius/pesol.md", "Pèsol"),
        ("07-fitxes-cultius/porro.md", "Porro"),
        ("07-fitxes-cultius/rave.md", "Rave"),
        ("07-fitxes-cultius/romani.md", "Romaní"),
        ("07-fitxes-cultius/tomaquet.md", "Tomàquet"),
        ("07-fitxes-cultius/aromatiques.md", "Totes les aromàtiques"),
    ],
    "Conreu avançat": [
        ("02-associacions-rotacions.md", "Associacions i rotacions"),
        ("03-gestio-plagues.md", "Gestió de plagues"),
        ("04-reg-fertilitzacio.md", "Reg i fertilització"),
        ("05-cobertes-adobs-verds.md", "Cobertes i adobs verds"),
        ("06-varietats-tradicionals.md", "Varietats tradicionals"),
        ("compost.md", "Compost"),
        ("planters-guia-completa.md", "Planters"),
        ("guardar-llavors.md", "Guardar llavors"),
        ("biodinamica-guia-completa.md", "Biodinàmica"),
        ("guia-avancada-osona.md", "Guia avançada Osona"),
        ("practiques-avancades.md", "Pràctiques avançades"),
        ("pla-tractaments-fitosanitaris.md", "Tractaments fitosanitaris"),
    ],
    "Eines operatives": [
        ("bitacola-setmanal.md", "Bitàcola setmanal"),
        ("calculadora-sembra.md", "Calculadora de sembra"),
    ],
    "Conservació": [
        ("conserves.md", "Conserves"),
        ("guia-fermentats.md", "Fermentats"),
    ],
    "Sòl i natura": [
        ("analisi-sol-guia-completa.md", "Anàlisi de sòl"),
        ("biologia-sol-curs.md", "Biologia del sòl"),
        ("adventicies-guia-completa.md", "Adventícies"),
        ("pollinitzadors-guia-completa.md", "Pol·linitzadors"),
        ("canvi-climatic-osona.md", "Canvi climàtic"),
    ],
    "Fruiters": [
        ("fruiters-guia-completa.md", "Fruiters"),
    ],
    "Bolets": [
        ("bolets-guia-completa.md", "Guia de bolets"),
    ],
    "Medicinal i remeieres": [
        ("remeieres-guia-completa.md", "Remeieres"),
        ("fitoterapia-curs.md", "Curs de fitoteràpia"),
        ("hort-medicinal-guia.md", "Hort medicinal"),
        ("hort-amb-nens-manual.md", "Hort amb nens"),
        ("apotecaria-casolana-guia.md", "Apotecaria casolana"),
        ("olis-massatge-guia.md", "Olis de massatge"),
        ("sabons-medicinals-guia.md", "Sabons medicinals"),
        ("cremes-ungeunts-especialitzats-guia.md", "Cremes i ungüents"),
        ("banys-terapeutics-guia.md", "Banys terapèutics"),
        ("productes-curatius-avancats-guia.md", "Productes curatius avançats"),
        ("primers-auxilis-verds-manual.md", "Primers auxilis verds"),
    ],
    "Eines i tecnologia": [
        ("hort-osona-iot/README.md", "Sistema IoT (Raspberry Pi)"),
        ("hort-osona-iot/CHAT-SETUP.md", "Configurar el xat local"),
    ],
    "El meu hort": [
        ("ACCES-MOBIL.md", "Com accedir des del mòbil"),
        ("VSCODE-GUIDE.md", "Editar amb VS Code"),
        ("HORT-CHECKLIST.md", "Checklist de l'hort"),
    ],
}

# ──────────── UTILITATS ────────────

def extract_title(content: str, fallback: str) -> str:
    """Extreu el primer # del markdown."""
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def md_to_html(text: str) -> str:
    """Conversió molt bàsica de markdown a HTML. Suficient per a la majoria de contingut."""
    # Escapar HTML per seguretat
    text = html.escape(text)

    # Restaurar els blocs de codi (que han estat escapats)
    # No, els blocs de codi s'han d'escapar igual, els tractarem com a pre>code

    lines = text.split('\n')
    out = []
    in_code = False
    in_list = False
    in_table = False
    table_rows = []

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    def flush_table():
        nonlocal in_table, table_rows
        if in_table:
            out.append('</table>')
            in_table = False
            table_rows = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Blocs de codi
        if stripped.startswith('```'):
            flush_list()
            flush_table()
            if in_code:
                out.append('</code></pre>')
                in_code = False
            else:
                out.append('<pre><code>')
                in_code = True
            i += 1
            continue

        if in_code:
            out.append(line)
            i += 1
            continue

        # Taules (línia amb |)
        if '|' in line and not in_code:
            flush_list()
            if not in_table:
                # Comprovar si la següent línia és separadora
                if i + 1 < len(lines) and re.match(r'^\s*\|?[\s\-:|]+\|?\s*$', lines[i+1]):
                    in_table = True
                    table_rows = []
                    out.append('<table>')
            if in_table:
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if i + 1 < len(lines) and re.match(r'^\s*\|?[\s\-:|]+\|?\s*$', lines[i+1]):
                    # Separador
                    out.append('<thead><tr>')
                    for c in cells:
                        out.append(f'<th>{inline_md(c)}</th>')
                    out.append('</tr></thead><tbody>')
                    i += 2
                    continue
                else:
                    out.append('<tr>')
                    for c in cells:
                        out.append(f'<td>{inline_md(c)}</td>')
                    out.append('</tr>')
                    i += 1
                    continue

        # Capçaleres
        m = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if m:
            flush_list()
            flush_table()
            level = len(m.group(1))
            content_str = inline_md(m.group(2))
            out.append(f'<h{level} id="{slugify(m.group(2))}">{content_str}</h{level}>')
            i += 1
            continue

        # Llistes
        m = re.match(r'^[\-\*]\s+(.+)$', stripped)
        if m:
            if not in_list:
                out.append('<ul>')
                in_list = True
            out.append(f'<li>{inline_md(m.group(1))}</li>')
            i += 1
            continue
        m = re.match(r'^\d+\.\s+(.+)$', stripped)
        if m:
            if not in_list:
                out.append('<ol>')
                in_list = True
            out.append(f'<li>{inline_md(m.group(1))}</li>')
            i += 1
            continue

        # Línia buida
        if not stripped:
            flush_list()
            flush_table()
            i += 1
            continue

        # Paràgraf
        flush_list()
        flush_table()
        out.append(f'<p>{inline_md(stripped)}</p>')
        i += 1

    flush_list()
    flush_table()
    if in_code:
        out.append('</code></pre>')
    return '\n'.join(out)


def inline_md(text: str) -> str:
    """Format inline: **negreta**, *cursiva*, `codi`, [text](url)."""
    # Codi inline (primer per evitar que s'interpreti altres coses dins)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Negreta
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Cursiva
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    # Enllaços [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text


def slugify(text: str) -> str:
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'\s+', '-', text)
    return text[:60]


def read_doc(rel_path: str) -> Tuple[str, str, str]:
    """Retorna (path, title, html_content) o None si no existeix."""
    p = BASE / rel_path
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    title = extract_title(text, p.stem)
    # Si és .md, convertir; si és .html, agafar el body
    if p.suffix == ".md":
        content = md_to_html(text)
    else:
        # Extreure body d'un HTML
        m = re.search(r'<body[^>]*>(.*)</body>', text, re.DOTALL | re.IGNORECASE)
        content = m.group(1) if m else text
        # Treure scripts i styles
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)

    # Si la fitxa té una imatge SVG associada, inserir-la al principi
    img_path = p.parent / "img" / f"{p.stem}.svg"
    if img_path.exists():
        img_html = f'<div class="doc-hero"><img src="img/{p.stem}.svg" alt="{title}" loading="lazy"></div>'
        content = img_html + content

    return rel_path, title, content


# ──────────── MAIN ────────────

def main():
    # Carregar tots els documents
    docs: Dict[str, Dict] = {}
    for cat_name, items in CATEGORIES.items():
        for rel_path, _label in items:
            result = read_doc(rel_path)
            if result:
                path, title, content = result
                docs[path] = {"title": title, "html": content, "category": cat_name}

    print(f"Carregats {len(docs)} documents")

    # IMPORTANT: Guardem els metadades al DOCS pero NO el HTML.
    # El HTML es llegeix sota demanda (lazy loading) des de docs/<path>.html
    # Aixo redueix el portal de 1.2 MB a ~50 KB
    docs_meta = {}
    for path, d in docs.items():
        docs_meta[path] = {"title": d["title"], "category": d["category"]}
    docs_json = json.dumps(docs_meta, ensure_ascii=False)

    # Generar l'estructura del sidebar (categories -> items)
    sidebar_data = {}
    for cat_name, items in CATEGORIES.items():
        sidebar_data[cat_name] = []
        for rel_path, label in items:
            if rel_path in docs:
                sidebar_data[cat_name].append({
                    "path": rel_path,
                    "label": label,
                    "title": docs[rel_path]["title"]
                })

    sidebar_json = json.dumps(sidebar_data, ensure_ascii=False)

    # ──────────── GENERAR FITXERS HTML PER A CADA DOCUMENT ────────────
    docs_dir = BASE / "docs"
    docs_dir.mkdir(exist_ok=True)
    # Netejar fitxers antics
    for f in docs_dir.rglob("*"):
        if f.is_file():
            f.unlink()
    for path, d in docs.items():
        # Subdir per categoria: docs/<categoria>/<fitxer>.html
        out_path = docs_dir / path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(d["html"], encoding="utf-8")
    print(f"✅ {len(docs)} fitxers HTML generats a {docs_dir.relative_to(BASE)}/")

    # ──────────── GENERAR INDEX DE CERCA (search_index.json) ────────────
    search_index = []
    for path, d in docs.items():
        plain = (d["title"] + " " + re.sub(r"<[^>]+>", " ", d["html"])).lower()
        search_index.append({
            "path": path,
            "title": d["title"],
            "category": d["category"],
            "plain": plain
        })
    (BASE / "search_index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8"
    )
    print(f"✅ search_index.json ({len(search_index)} entrades)")

    # ──────────── HTML ────────────
    portal = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Base de coneixement d'hort ecològic a Osona">
<meta name="theme-color" content="#3D4A2A">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Hort Osona">
<meta name="mobile-web-app-capable" content="yes">
<title>Hort Osona</title>
<link rel="manifest" href="manifest.json">
<link rel="icon" type="image/svg+xml" href="icon.svg">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<style>
:root {{
  --c-bg: #F5EBD8;
  --c-paper: #FFFCF3;
  --c-ink: #2D2A22;
  --c-ink-2: #6B665A;
  --c-olive: #3D4A2A;
  --c-olive-bg: #E8E2CC;
  --c-ochre: #B5853A;
  --c-line: #D9D0B5;
  --shadow: 0 1px 3px rgba(0,0,0,0.1);
  --header-h: 56px;
  --sidebar-w: 280px;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body {{
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", system-ui, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: var(--c-ink);
  background: var(--c-bg);
  -webkit-text-size-adjust: 100%;
  -webkit-tap-highlight-color: transparent;
}}

button {{
  font: inherit;
  color: inherit;
  background: none;
  border: none;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}}

a {{ color: var(--c-olive); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

/* ──────────── LAYOUT ──────────── */
.app {{
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: var(--header-h) 1fr;
  height: 100vh;
  height: 100dvh;
}}

/* Header (mòbil) */
.header {{
  grid-row: 1;
  grid-column: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 12px;
  background: var(--c-olive);
  color: var(--c-paper);
  height: var(--header-h);
  position: relative;
  z-index: 10;
}}

.header .menu-btn {{
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  font-size: 24px;
  color: var(--c-paper);
}}

.header .menu-btn:hover,
.header .menu-btn:active {{
  background: rgba(255,255,255,0.15);
}}

.header .title {{
  font-weight: 600;
  font-size: 1.05rem;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}

.header .search-toggle {{
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  font-size: 20px;
  color: var(--c-paper);
}}

/* Main content */
.main {{
  grid-row: 2;
  grid-column: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 16px;
  padding-bottom: env(safe-area-inset-bottom, 16px);
}}

/* ──────────── DRAWER (mòbil) ──────────── */
.drawer-bg {{
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 50;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}}

.drawer-bg.open {{
  opacity: 1;
  pointer-events: auto;
}}

.drawer {{
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 85%;
  max-width: 340px;
  background: var(--c-paper);
  z-index: 51;
  transform: translateX(-100%);
  transition: transform 0.25s ease-out;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 12px rgba(0,0,0,0.2);
}}

.drawer.open {{ transform: translateX(0); }}

.drawer-header {{
  padding: 16px;
  background: var(--c-olive);
  color: var(--c-paper);
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.drawer-header .title {{
  font-weight: 600;
  font-size: 1.1rem;
}}

.drawer-close {{
  width: 36px;
  height: 36px;
  border-radius: 8px;
  font-size: 20px;
  color: var(--c-paper);
}}

.drawer-search {{
  padding: 12px;
  border-bottom: 1px solid var(--c-line);
}}

.drawer-search input {{
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--c-line);
  border-radius: 8px;
  font-size: 0.95rem;
  background: var(--c-bg);
  color: var(--c-ink);
}}

.drawer-content {{
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}}

.cat-section {{
  border-bottom: 1px solid var(--c-line);
}}

.cat-toggle {{
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--c-ink-2);
  text-align: left;
}}

.cat-toggle .arrow {{
  font-size: 0.8rem;
  transition: transform 0.2s;
}}

.cat-section.open .cat-toggle .arrow {{
  transform: rotate(180deg);
}}

.cat-section.open .cat-toggle {{
  color: var(--c-olive);
}}

.cat-items {{
  list-style: none;
  padding: 0 0 8px 0;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
}}

.cat-section.open .cat-items {{
  max-height: 5000px;
}}

.cat-items li a {{
  display: block;
  padding: 10px 16px 10px 24px;
  font-size: 0.95rem;
  color: var(--c-ink);
  border-left: 3px solid transparent;
}}

.cat-items li a:hover,
.cat-items li a:active {{
  background: var(--c-olive-bg);
  border-left-color: var(--c-olive);
  text-decoration: none;
}}

/* Search overlay (mòbil) */
.search-overlay {{
  position: fixed;
  inset: 0;
  background: var(--c-bg);
  z-index: 60;
  display: none;
  flex-direction: column;
}}

.search-overlay.open {{ display: flex; }}

.search-bar {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--c-olive);
  color: var(--c-paper);
  height: var(--header-h);
}}

.search-bar input {{
  flex: 1;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  background: rgba(255,255,255,0.95);
  color: var(--c-ink);
}}

.search-bar input:focus {{
  outline: 2px solid var(--c-ochre);
  outline-offset: 1px;
}}

.search-results {{
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}}

.search-result {{
  display: block;
  padding: 12px 16px;
  border-bottom: 1px solid var(--c-line);
  color: var(--c-ink);
}}

.search-result:hover,
.search-result:active {{
  background: var(--c-olive-bg);
  text-decoration: none;
}}

.search-result .title {{
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 2px;
}}

.search-result .cat {{
  font-size: 0.75rem;
  color: var(--c-ink-2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.search-result .snippet {{
  font-size: 0.85rem;
  color: var(--c-ink-2);
  margin-top: 4px;
}}

/* ──────────── CHAT ──────────── */
.chat-overlay {{
  position: fixed;
  inset: 0;
  background: var(--c-bg);
  z-index: 60;
  display: none;
  flex-direction: column;
}}

.chat-overlay.open {{ display: flex; }}

.chat-bar {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--c-olive);
  color: var(--c-paper);
  height: var(--header-h);
}}

.chat-title {{
  flex: 1;
  font-weight: 600;
  font-size: 1rem;
}}

.chat-status {{
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 10px;
  background: rgba(255,255,255,0.15);
  color: var(--c-paper);
}}

.chat-status.online {{ background: #4a7a3a; }}
.chat-status.offline {{ background: #a04040; }}
.chat-status.thinking {{ background: #b5853a; }}

.chat-messages {{
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}}

.chat-msg {{
  max-width: 85%;
  padding: 10px 14px;
  border-radius: 14px;
  line-height: 1.4;
  word-wrap: break-word;
  font-size: 0.95rem;
}}

.chat-msg-bot {{
  background: var(--c-paper);
  border: 1px solid var(--c-line);
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}}

.chat-msg-user {{
  background: var(--c-olive);
  color: var(--c-paper);
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}}

.chat-msg-error {{
  background: #fce4e4;
  border: 1px solid #d97070;
  color: #6b1f1f;
  align-self: flex-start;
  font-size: 0.9rem;
}}

.chat-msg-thinking {{
  background: var(--c-paper);
  border: 1px solid var(--c-line);
  align-self: flex-start;
  font-style: italic;
  color: var(--c-ink-2);
}}

.chat-msg-sources {{
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--c-line);
  font-size: 0.8rem;
  color: var(--c-ink-2);
}}

.chat-msg-sources ul {{
  margin: 4px 0 0 16px;
  padding: 0;
}}

.chat-form {{
  display: flex;
  gap: 8px;
  padding: 8px 12px;
  background: var(--c-paper);
  border-top: 1px solid var(--c-line);
  padding-bottom: calc(8px + env(safe-area-inset-bottom, 0px));
}}

.chat-form input {{
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--c-line);
  border-radius: 20px;
  font-size: 1rem;
  background: var(--c-bg);
  color: var(--c-ink);
}}

.chat-form input:focus {{
  outline: 2px solid var(--c-ochre);
  outline-offset: 1px;
}}

.chat-form button {{
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--c-olive);
  color: var(--c-paper);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}}

.chat-form button:hover,
.chat-form button:active {{
  background: #2a3420;
}}

.chat-form button:disabled {{
  background: var(--c-ink-2);
  opacity: 0.6;
}}

/* ──────────── DESKTOP (≥768px) ──────────── */
@media (min-width: 768px) {{
  .chat-overlay {{
    /* A escriptori, obre com a panell lateral dret (no pantalla completa) */
    left: auto;
    top: var(--header-h);
    right: 0;
    bottom: 0;
    width: 420px;
    border-left: 1px solid var(--c-line);
    box-shadow: -4px 0 12px rgba(0,0,0,0.1);
  }}

  .app {{
    grid-template-columns: var(--sidebar-w) 1fr;
    grid-template-rows: var(--header-h) 1fr;
  }}

  .header {{
    grid-column: 1 / -1;
  }}

  .header .menu-btn {{
    display: none;
  }}

  /* Sidebar fixa a l'esquerra (visible) */
  .drawer {{
    position: relative;
    transform: none;
    width: 100%;
    max-width: none;
    height: auto;
    flex: 1;
    z-index: 1;
    box-shadow: none;
    border-right: 1px solid var(--c-line);
    grid-column: 1;
    grid-row: 2;
  }}

  .drawer-bg {{
    display: none;
  }}

  .drawer-header {{
    display: none;
  }}

  .drawer-search {{
    background: var(--c-paper);
  }}

  /* El main ocupa la columna 2 */
  .main {{
    grid-column: 2;
    grid-row: 2;
    padding: 24px 32px;
  }}
}}

/* ──────────── TIPOGRAFIA DEL CONTINGUT ──────────── */
.doc h1 {{
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.8rem;
  color: var(--c-olive);
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--c-olive-bg);
}}

.doc .doc-hero {{
  display: block;
  text-align: center;
  margin: 0 0 20px 0;
  padding: 0;
}}

.doc .doc-hero img {{
  max-width: 240px;
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

.doc h2 {{
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.35rem;
  color: var(--c-olive);
  margin-top: 24px;
  margin-bottom: 12px;
}}

.doc h3 {{
  font-size: 1.1rem;
  color: var(--c-ink);
  margin-top: 18px;
  margin-bottom: 8px;
}}

.doc p {{
  margin-bottom: 12px;
}}

.doc ul, .doc ol {{
  margin: 0 0 12px 24px;
}}

.doc li {{ margin-bottom: 4px; }}

.doc code {{
  background: var(--c-olive-bg);
  padding: 2px 5px;
  border-radius: 3px;
  font-family: "SF Mono", Menlo, monospace;
  font-size: 0.88em;
  color: var(--c-ochre);
}}

.doc pre {{
  background: var(--c-olive-bg);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 12px 0;
  font-size: 0.88rem;
  line-height: 1.4;
}}

.doc pre code {{
  background: none;
  padding: 0;
  color: var(--c-ink);
}}

.doc table {{
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  font-size: 0.9rem;
  display: block;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}}

.doc th, .doc td {{
  border: 1px solid var(--c-line);
  padding: 6px 10px;
  text-align: left;
  vertical-align: top;
}}

.doc th {{
  background: var(--c-olive-bg);
  font-weight: 600;
}}

.doc blockquote {{
  border-left: 3px solid var(--c-ochre);
  padding-left: 12px;
  margin: 12px 0;
  color: var(--c-ink-2);
  font-style: italic;
}}

.doc hr {{
  border: none;
  border-top: 1px solid var(--c-line);
  margin: 20px 0;
}}

/* Benvinguda */
.welcome {{
  text-align: center;
  padding: 32px 16px;
}}

.welcome h1 {{
  font-family: Georgia, serif;
  font-size: 2rem;
  color: var(--c-olive);
  margin-bottom: 12px;
}}

.welcome .subtitle {{
  color: var(--c-ink-2);
  font-size: 1.05rem;
  margin-bottom: 24px;
}}

.welcome .stats {{
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
}}

.welcome .stat {{
  background: var(--c-paper);
  border: 1px solid var(--c-line);
  border-radius: 8px;
  padding: 16px 20px;
  min-width: 100px;
}}

.welcome .stat .num {{
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--c-olive);
}}

.welcome .stat .lbl {{
  font-size: 0.8rem;
  color: var(--c-ink-2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

.welcome h2 {{
  font-family: Georgia, serif;
  font-size: 1.2rem;
  color: var(--c-olive);
  margin: 24px 0 12px;
}}

.welcome .quick {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-top: 16px;
}}

.welcome .quick a {{
  display: block;
  padding: 12px 16px;
  background: var(--c-paper);
  border: 1px solid var(--c-line);
  border-radius: 8px;
  text-align: left;
  font-size: 0.9rem;
  color: var(--c-ink);
}}

.welcome .quick a:hover,
.welcome .quick a:active {{
  border-color: var(--c-olive);
  text-decoration: none;
  background: var(--c-olive-bg);
}}

/* Enllaços interns del doc */
.doc a[href^="#"] {{
  color: var(--c-ochre);
}}

/* Scrollbar */
.main::-webkit-scrollbar,
.drawer-content::-webkit-scrollbar,
.search-results::-webkit-scrollbar,
.doc pre::-webkit-scrollbar,
.doc table::-webkit-scrollbar {{
  width: 6px;
  height: 6px;
}}

.main::-webkit-scrollbar-thumb,
.drawer-content::-webkit-scrollbar-thumb,
.search-results::-webkit-scrollbar-thumb,
.doc pre::-webkit-scrollbar-thumb,
.doc table::-webkit-scrollbar-thumb {{
  background: var(--c-line);
  border-radius: 3px;
}}

/* Print */
@media print {{
  .header, .drawer, .drawer-bg, .search-overlay {{ display: none !important; }}
  .app {{ grid-template-columns: 1fr; grid-template-rows: 1fr; }}
  .main {{ grid-column: 1; grid-row: 1; padding: 0; overflow: visible; }}
  .doc pre {{ white-space: pre-wrap; word-break: break-word; }}
}}
</style>
</head>
<body>

<div class="app">

  <!-- HEADER -->
  <header class="header">
    <button class="menu-btn" id="menu-btn" aria-label="Obrir menú">☰</button>
    <div class="title">🌱 Hort Osona</div>
    <button class="search-toggle" id="chat-btn" aria-label="Xat amb l'hort" title="Pregunta a l'hort">💬</button>
    <button class="search-toggle" id="search-btn" aria-label="Cerca">🔍</button>
  </header>

  <!-- SIDEBAR/DRAWER -->
  <aside class="drawer" id="drawer" aria-label="Categories">
    <div class="drawer-header">
      <div class="title">Categories</div>
      <button class="drawer-close" id="drawer-close" aria-label="Tancar">✕</button>
    </div>
    <div class="drawer-search">
      <input type="search" id="sidebar-search" placeholder="Cerca un document..." autocomplete="off">
    </div>
    <div class="drawer-content" id="drawer-content">
      <!-- S'omple amb JS -->
    </div>
  </aside>

  <!-- BACKDROP -->
  <div class="drawer-bg" id="drawer-bg"></div>

  <!-- MAIN -->
  <main class="main" id="main">
    <div class="welcome" id="welcome">
      <h1>🌱 Hort Osona</h1>
      <p class="subtitle">Base de coneixement d'horticultura ecològica, plantes medicinals i conserves, adaptat a la comarca d'Osona.</p>
      <div class="stats">
        <div class="stat"><div class="num">{len(docs)}</div><div class="lbl">Documents</div></div>
        <div class="stat"><div class="num">{len([d for d in docs if d.startswith('07-fitxes-cultius/')])}</div><div class="lbl">Fitxes cultiu</div></div>
        <div class="stat"><div class="num">{len(CATEGORIES)}</div><div class="lbl">Categories</div></div>
      </div>
      <h2>Com començar</h2>
      <p style="color: var(--c-ink-2);">Toca el botó ☰ per obrir el menú i triar un document, o bé 🔍 per cercar.</p>
      <div class="quick">
        <a href="#" data-path="pla-12-mesos.md" onclick="return openDoc(this.dataset.path)">📅 Pla dels 12 mesos</a>
        <a href="#" data-path="plans-mensuals/2026-06-juny.md" onclick="return openDoc(this.dataset.path)">📅 Pla juny 2026</a>
        <a href="#" data-path="07-fitxes-cultius/tomaquet.md" onclick="return openDoc(this.dataset.path)">🍅 Tomàquet</a>
        <a href="#" data-path="01-calendari-sembra.md" onclick="return openDoc(this.dataset.path)">🌱 Calendari de sembra</a>
        <a href="#" data-path="02-associacions-rotacions.md" onclick="return openDoc(this.dataset.path)">🌿 Associacions</a>
        <a href="#" data-path="pla-tractaments-fitosanitaris.md" onclick="return openDoc(this.dataset.path)">🧪 Tractaments</a>
      </div>
    </div>
    <article class="doc" id="doc" style="display:none"></article>
  </main>

  <!-- SEARCH OVERLAY -->
  <div class="search-overlay" id="search-overlay">
    <div class="search-bar">
      <input type="search" id="search-input" placeholder="Cerca..." autocomplete="off" autofocus>
      <button class="drawer-close" id="search-close" aria-label="Tancar" style="color: var(--c-paper)">✕</button>
    </div>
    <div class="search-results" id="search-results"></div>
  </div>

  <!-- CHAT PANEL -->
  <div class="chat-overlay" id="chat-overlay">
    <div class="chat-bar">
      <span class="chat-title">💬 Xat amb l'hort</span>
      <span class="chat-status" id="chat-status">desconnectat</span>
      <button class="drawer-close" id="chat-close" aria-label="Tancar" style="color: var(--c-paper)">✕</button>
    </div>
    <div class="chat-messages" id="chat-messages">
      <div class="chat-msg chat-msg-bot">
        <strong>🌱 Hort Osona</strong><br>
        Hola! Soc el teu assistent hortolà. Pregunta'm qualsevol cosa sobre el teu hort a Osona.<br><br>
        <em>Exemples:</em>
        <ul style="margin: 8px 0 0 16px; font-size: 0.9rem;">
          <li>Quan sembrar carbassa?</li>
          <li>Com combatre el mildiu?</li>
          <li>Quines plantes medicinals puc cultivar?</li>
        </ul>
      </div>
    </div>
    <form class="chat-form" id="chat-form">
      <input type="text" id="chat-input" placeholder="Pregunta a l'hort..." autocomplete="off" required>
      <button type="submit" id="chat-send" aria-label="Enviar">➤</button>
    </form>
  </div>

</div>

<script>
const SIDEBAR = {sidebar_json};
const DOCS = {docs_json};

// ──────────── INDEX DE CERCA ────────────
// Carreguem l'index de cerca sota demanda des de search_index.json
let SEARCH_INDEX = [];
let SEARCH_INDEX_READY = false;
let SEARCH_INDEX_LOADING = null;

async function loadSearchIndex() {{
  if (SEARCH_INDEX_READY) return SEARCH_INDEX;
  if (SEARCH_INDEX_LOADING) return SEARCH_INDEX_LOADING;
  SEARCH_INDEX_LOADING = fetch('search_index.json')
    .then(r => r.ok ? r.json() : [])
    .then(idx => {{
      SEARCH_INDEX = idx;
      SEARCH_INDEX_READY = true;
      return idx;
    }})
    .catch(() => []);
  return SEARCH_INDEX_LOADING;
}}

// Precarregar l'index en iniciar
setTimeout(loadSearchIndex, 100);

// ──────────── RENDER SIDEBAR ────────────
function renderSidebar(filter = '') {{
  const container = document.getElementById('drawer-content');
  const filterLower = filter.toLowerCase().trim();
  let html = '';

  for (const [catName, items] of Object.entries(SIDEBAR)) {{
    const filtered = items.filter(it =>
      !filterLower ||
      it.title.toLowerCase().includes(filterLower) ||
      it.label.toLowerCase().includes(filterLower)
    );
    if (filtered.length === 0) continue;

    const itemsHtml = filtered.map(it =>
      `<li><a href="#" data-path="${{it.path}}" onclick="return openDoc('${{it.path}}')">${{escapeHtml(it.label)}}</a></li>`
    ).join('');

    html += `<div class="cat-section" data-cat="${{escapeHtml(catName)}}">
      <button class="cat-toggle" onclick="toggleCat(this.parentElement)" aria-expanded="false">
        <span>${{escapeHtml(catName)}}</span>
        <span class="arrow">▼</span>
      </button>
      <ul class="cat-items">${{itemsHtml}}</ul>
    </div>`;
  }}

  container.innerHTML = html;
}}

// Escapa caracters especials de regex per construir patrons segurs
function escapeRegex(str) {{
  return str.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
}}

function toggleCat(section) {{
  const wasOpen = section.classList.toggle('open');
  const btn = section.querySelector('.cat-toggle');
  if (btn) btn.setAttribute('aria-expanded', wasOpen ? 'true' : 'false');
}}

// ──────────── DRAWER ────────────
function openDrawer() {{
  document.getElementById('drawer').classList.add('open');
  document.getElementById('drawer-bg').classList.add('open');
}}

function closeDrawer() {{
  document.getElementById('drawer').classList.remove('open');
  document.getElementById('drawer-bg').classList.remove('open');
}}

// ──────────── OPEN DOC ────────────
async function openDoc(path) {{
  const d = DOCS[path];
  if (!d) return false;
  const doc = document.getElementById('doc');
  const welcome = document.getElementById('welcome');
  welcome.style.display = 'none';
  doc.style.display = 'block';
  doc.innerHTML = '<p style="padding:24px;color:var(--c-ink-2)">⏳ Carregant...</p>';

  // Carregar HTML sota demanda
  try {{
    const r = await fetch('docs/' + encodeURI(path));
    if (!r.ok) throw new Error('HTTP ' + r.status);
    let html = await r.text();
    html = html.split('<\\/script').join('</script');
    html = html.split('<\\!--').join('<!--');
    doc.innerHTML = html;
  }} catch (e) {{
    doc.innerHTML = '<p style="padding:24px;color:#a04040">❌ Error carregant el document: ' + escapeHtml(e.message) + '</p>';
  }}

  // Scroll a dalt
  document.getElementById('main').scrollTop = 0;
  // Tancar drawer i search si estan oberts (en mòbil)
  closeDrawer();
  closeSearch();
  // Actualitzar hash per compartir
  history.replaceState(null, '', '#' + encodeURIComponent(path));
  return false;
}}

// ──────────── SEARCH ────────────
function openSearch() {{
  const ov = document.getElementById('search-overlay');
  ov.classList.add('open');
  setTimeout(() => document.getElementById('search-input').focus(), 50);
}}

function closeSearch() {{
  document.getElementById('search-overlay').classList.remove('open');
  document.getElementById('search-input').value = '';
  document.getElementById('search-results').innerHTML = '';
}}

async function doSearch(q) {{
  const results = document.getElementById('search-results');
  if (!q || q.length < 2) {{
    results.innerHTML = '<p style="padding:16px;color:var(--c-ink-2)">Escriu almenys 2 lletres per cercar.</p>';
    return;
  }}
  // Assegurar que l'index esta carregat
  await loadSearchIndex();
  const qLower = q.toLowerCase();
  const matches = [];
  for (const item of SEARCH_INDEX) {{
    const idx = item.plain.indexOf(qLower);
    if (idx >= 0) {{
      const start = Math.max(0, idx - 40);
      const end = Math.min(item.plain.length, idx + q.length + 60);
      let snippet = item.plain.substring(start, end);
      if (start > 0) snippet = '…' + snippet;
      if (end < item.plain.length) snippet = snippet + '…';
      const safeQ = escapeRegex(qLower);
      snippet = snippet.replace(new RegExp('(' + safeQ + ')', 'gi'), '<mark>$1</mark>');
      matches.push({{ ...item, snippet }});
    }}
  }}
  if (matches.length === 0) {{
    results.innerHTML = '<p style="padding:16px;color:var(--c-ink-2)">Cap resultat per a "' + escapeHtml(q) + '".</p>';
    return;
  }}
  results.innerHTML = matches.slice(0, 30).map(m =>
    `<a href="#" class="search-result" data-path="${{m.path}}" onclick="return openDoc('${{m.path}}')">
      <div class="title">${{escapeHtml(m.title)}}</div>
      <div class="cat">${{escapeHtml(m.category)}}</div>
      <div class="snippet">${{snippet}}</div>
    </a>`
  ).join('');
}}

// ──────────── UTILS ────────────
function escapeHtml(s) {{
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}}

// ──────────── CHAT (RAG local) ────────────
// IMPORTANT: des del mobil NO es pot accedir a 'localhost' perque localhost
// sempre apunta al propi dispositiu. Cal usar la IP del Mac a la xarxa local.
// Si el backend es a una Raspberry Pi o altre maquina, canviar aqui.
//
// Prioritat de URLs:
// 1. window.CHAT_API_URL (definit a l'HTML) - te prioritat
// 2. localhost:8001 - nomes funciona des de l'ordinador
// 3. IP del Mac a la xarxa local (192.168.100.110:8001) - funciona des de mobil
const FALLBACK_CHAT_URLS = [
  'http://192.168.100.110:8001/chat',
  'http://localhost:8001/chat'
];
let CHAT_API = window.CHAT_API_URL || FALLBACK_CHAT_URLS[0];
let currentUrlIndex = 0;

function setChatStatus(text, cls) {{
  const el = document.getElementById('chat-status');
  el.textContent = text;
  el.className = 'chat-status ' + (cls || '');
}}

function openChat() {{
  document.getElementById('chat-overlay').classList.add('open');
  setTimeout(() => document.getElementById('chat-input').focus(), 50);
  // Comprovar estat de l'API (prova totes les URLs)
  checkChatHealth();
}}

function closeChat() {{
  document.getElementById('chat-overlay').classList.remove('open');
}}

function appendChatMsg(html, kind) {{
  const div = document.createElement('div');
  div.className = 'chat-msg chat-msg-' + (kind || 'bot');
  div.innerHTML = html;
  const container = document.getElementById('chat-messages');
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}}

async function checkChatHealth() {{
  // Provar totes les URLs fins que una funcioni
  for (let i = 0; i < FALLBACK_CHAT_URLS.length; i++) {{
    const url = FALLBACK_CHAT_URLS[i].replace('/chat', '/chat/health');
    try {{
      const r = await fetch(url, {{ cache: 'no-store' }});
      if (r.ok) {{
        const data = await r.json();
        if (data.status === 'ok') {{
          CHAT_API = FALLBACK_CHAT_URLS[i];
          currentUrlIndex = i;
          setChatStatus('connectat · ' + (data.model || ''), 'online');
          return true;
        }}
      }}
    }} catch (e) {{
      // provar la seguent
    }}
  }}
  setChatStatus('desconnectat', 'offline');
  return false;
}}

async function sendChat(question) {{
  // Mostrar pregunta de l'usuari
  appendChatMsg(escapeHtml(question), 'user');

  // Mostrar "pensant..."
  const thinking = appendChatMsg('🤔 Pensant...', 'thinking');
  setChatStatus('pensant...', 'thinking');
  const sendBtn = document.getElementById('chat-send');
  const input = document.getElementById('chat-input');
  sendBtn.disabled = true;
  input.disabled = true;

  // Assegurar-nos que tenim una URL connectada
  const connected = await checkChatHealth();
  if (!connected) {{
    thinking.remove();
    appendChatMsg(buildOfflineHelp(), 'error');
    setChatStatus('desconnectat', 'offline');
    sendBtn.disabled = false;
    input.disabled = false;
    input.focus();
    return;
  }}

  try {{
    const r = await fetch(CHAT_API, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ question }})
    }});
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const data = await r.json();
    thinking.remove();

    // Renderitzar resposta amb format basic
    let answer = data.answer || '(Sense resposta)';
    // Convertir markdown molt basic a HTML
    answer = escapeHtml(answer)
      .replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>')
      .replace(/\\n\\n/g, '</p><p>')
      .replace(/\\n/g, '<br>')
      .replace(/^/, '<p>')
      .replace(/$/, '</p>');

    // Afegir fonts
    let sources = '';
    if (data.sources && data.sources.length > 0) {{
      sources = '<div class="chat-msg-sources"><strong>📚 Fonts:</strong><ul>';
      data.sources.slice(0, 4).forEach(s => {{
        sources += '<li>' + escapeHtml(s.title) + '</li>';
      }});
      sources += '</ul></div>';
    }}

    appendChatMsg(answer + sources, 'bot');
    setChatStatus('connectat', 'online');
  }} catch (e) {{
    thinking.remove();
    let msg = '❌ Error: ' + escapeHtml(e.message);
    if (e.message.includes('Failed to fetch') || e.message.includes('NetworkError')) {{
      msg = buildOfflineHelp();
    }}
    appendChatMsg(msg, 'error');
    setChatStatus('desconnectat', 'offline');
  }} finally {{
    sendBtn.disabled = false;
    input.disabled = false;
    input.focus();
  }}
}}

function buildOfflineHelp() {{
  // Detectar si estem en mobil/tablet
  const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
  const url = FALLBACK_CHAT_URLS[0];
  const ipMatch = url.match(/http:\/\/([\d.]+):/);
  const ip = ipMatch ? ipMatch[1] : 'la IP del Mac';
  let help = '❌ No puc connectar amb el servidor del xat.<br><br>';
  help += '<strong>Com resoldre-ho:</strong><ol style="margin:8px 0 0 20px;font-size:0.9rem;line-height:1.5">';
  if (isMobile) {{
    help += '<li>Assegura\\'t que el <strong>iPhone i el Mac estan a la mateixa WiFi</strong></li>';
    help += '<li>Obre el <strong>Terminal</strong> al Mac i executa:<br>' +
      '<code style="display:block;background:#f0e8d8;padding:6px 8px;border-radius:4px;margin:4px 0;font-size:0.85rem">cd ~/Desktop/hort-osona/hort-osona-iot && python3 -m uvicorn backend.api_chat:app --host 0.0.0.0 --port 8001</code></li>';
    help += '<li>Espera que aparegui "Uvicorn running on http://0.0.0.0:8001"</li>';
  }} else {{
    help += '<li>El backend no esta arrencat. Obre el <strong>Terminal</strong> i executa:<br>' +
      '<code style="display:block;background:#f0e8d8;padding:6px 8px;border-radius:4px;margin:4px 0;font-size:0.85rem">cd ~/Desktop/hort-osona/hort-osona-iot && python3 -m uvicorn backend.api_chat:app --port 8001</code></li>';
  }}
  help += `<li>Prem <button onclick="checkChatHealth(); document.getElementById('chat-input').focus();" style="background:#3D4A2A;color:#FFFCF3;border:none;padding:4px 10px;border-radius:4px;cursor:pointer">🔄 Tornar a provar</button> un cop arrencat</li>`;
  help += '</ol>';
  help += '<div style="margin-top:10px;font-size:0.8rem;color:#6B665A">URL que provem: <code>' + escapeHtml(url) + '</code></div>';
  return help;
}}

// ──────────── INIT ────────────
document.addEventListener('DOMContentLoaded', () => {{
  renderSidebar();

  // Botons header
  document.getElementById('menu-btn').addEventListener('click', openDrawer);
  document.getElementById('search-btn').addEventListener('click', openSearch);
  document.getElementById('chat-btn').addEventListener('click', openChat);
  document.getElementById('drawer-close').addEventListener('click', closeDrawer);
  document.getElementById('search-close').addEventListener('click', closeSearch);
  document.getElementById('chat-close').addEventListener('click', closeChat);
  document.getElementById('drawer-bg').addEventListener('click', closeDrawer);

  // Sidebar search
  document.getElementById('sidebar-search').addEventListener('input', (e) => {{
    renderSidebar(e.target.value);
  }});

  // Search overlay
  document.getElementById('search-input').addEventListener('input', (e) => {{
    doSearch(e.target.value);
  }});

  // Chat form
  document.getElementById('chat-form').addEventListener('submit', (e) => {{
    e.preventDefault();
    const input = document.getElementById('chat-input');
    const q = input.value.trim();
    if (!q) return;
    input.value = '';
    sendChat(q);
  }});

  // Escape per tancar
  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') {{
      closeDrawer();
      closeSearch();
      closeChat();
    }}
  }});

  // Obrir document des de hash
  if (location.hash.length > 1) {{
    const path = decodeURIComponent(location.hash.substring(1));
    if (DOCS[path]) openDoc(path);
  }}
}});
</script>
</body>
</html>"""

    out = BASE / "index.html"
    out.write_text(portal, encoding="utf-8")
    size_kb = out.stat().st_size / 1024
    print(f"✅ {out} ({size_kb:.0f} KB)")

    # Copiar assets PWA
    for src, dst in [("site/manifest.json", "manifest.json"),
                      ("site/icon.svg", "icon.svg"),
                      ("site/icon-192.png", "icon-192.png"),
                      ("site/icon-512.png", "icon-512.png"),
                      ("site/service-worker.js", "service-worker.js")]:
        sp = BASE / src
        dp = BASE / dst
        if sp.exists():
            shutil.copy2(sp, dp)
    print("✅ Assets PWA copiats")


if __name__ == "__main__":
    main()
