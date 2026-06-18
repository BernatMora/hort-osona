#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build.py — Construeix site/index.html (SPA estàtic) a partir dels .md del projecte.

Ús:
    python site/build.py

Llegeix tots els .md del projecte (excepte infraestructura), els classifica en
9 categories seguint l'estructura del README, converteix cada .md a HTML i ho
embolcalla en un únic fitxer site/index.html amb:
  - Sidebar de categories
  - Cercador client-side
  - Renderitzat de la fitxa activa al centre
  - Disseny "quadern de camp": verd oliva + ocre + crema + serif Fraunces

La font de veritat continua sent els .md — aquest script només genera un
artefacte de lectura. Per actualitzar el lloc, edita els .md i torna a
correr build.py.
"""

from __future__ import annotations
import os
import re
import sys
import json
import html
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

import markdown


# ───────────────────────────── Configuració ─────────────────────────────

ROOT = Path(__file__).resolve().parent.parent          # arrel del projecte
SITE_DIR = Path(__file__).resolve().parent              # carpeta site/
OUT_FILE = SITE_DIR / "index.html"

# Fitxers d'infraestructura que NO entren al lloc (no són contingut de l'hort)
INFRASTRUCTURE_FILES = {
    "README.md",
    "CHANGELOG.md",
    "HORT-CHECKLIST.md",
    "SETUP-WINDOWS.md",
    "SETUP-SITE.md",
    "SYNC-SCRIPT.md",
    "VSCODE-GUIDE.md",
}

# Plantilles internes, no entren com a documents
INFRASTRUCTURE_DIRS = {
    "07-fitxes-cultius/_plantilla.md",
}

# Categorització explícita. Ordre = ordre al sidebar.
# Claus = noms de categoria; valors = llista de globs (relatius a l'arrel).
# Tot el que no aparegui aquí va a la categoria "Altres".
CATEGORIES: List[Tuple[str, str, List[str]]] = [
    (
        "Planificació i calendari",
        "📅",
        [
            "01-calendari-sembra.md",
            "08-pla-mensual.md",
            "pla-12-mesos.md",
            "pla-hort.md",
            "pla-hort-esquematic.md",
            "planificacio-tardor-hivern-2026.md",
            "calendari-lunar-osona.md",
            "pla-reg-personalitzat-2026.md",
            "pla-tractaments-fitosanitaris.md",
            "bitacola-setmanal.md",
            "calculadora-sembra.md",
            "plans-mensuals/*.md",
        ],
    ),
    (
        "Fitxes de cultiu",
        "🌱",
        ["07-fitxes-cultius/*.md"],
    ),
    (
        "Conreu avançat",
        "🛠️",
        [
            "02-associacions-rotacions.md",
            "03-gestio-plagues.md",
            "04-reg-fertilitzacio.md",
            "05-cobertes-adobs-verds.md",
            "06-varietats-tradicionals.md",
            "compost.md",
            "guardar-llavors.md",
            "planters-guia-completa.md",
            "practiques-avancades.md",
            "guia-avancada-osona.md",
            "croquis-hort.md",
            "plagues-guia-visual.md",
            "rendiment-hort-guia.md",
            "fruiters-guia-completa.md",
            "adventicies-guia-completa.md",
            "analisi-sol-guia-completa.md",
            "biologia-sol-curs.md",
            "pollinitzadors-guia-completa.md",
            "canvi-climatic-osona.md",
            "biodinamica-guia-completa.md",
        ],
    ),
    (
        "Plantes medicinals",
        "🌿",
        [
            "remeieres-guia-completa.md",
            "fitoterapia-curs.md",
            "apotecaria-casolana-guia.md",
            "hort-medicinal-guia.md",
            "aromatiques-guia-completa.md",
            "banys-terapeutics-guia.md",
            "olis-massatge-guia.md",
            "sabons-medicinals-guia.md",
            "cremes-ungeunts-especialitzats-guia.md",
            "productes-curatius-avancats-guia.md",
            "primers-auxilis-verds-manual.md",
            "curatius-resum-final.md",
        ],
    ),
    (
        "Bolets i biodiversitat",
        "🍄",
        ["bolets-guia-completa.md"],
    ),
    (
        "Transformació i fermentats",
        "🫙",
        [
            "guia-fermentats.md",
            "conserves.md",
        ],
    ),
    (
        "Projectes familiars",
        "👨‍👩‍👧",
        [
            "hort-amb-nens-manual.md",
            "decoracio-natural-manual.md",
            "botiga-casolana-guia.md",
        ],
    ),
    (
        "Eines i recursos",
        "🧰",
        [
            "eines-digitals-guia.md",
            "apps-planificacio-guia.md",
            "fitxa-hort.md",
        ],
    ),
    (
        "Resums i índex",
        "📚",
        [
            "00-index.md",
            "resum-final-base-coneixement.md",
        ],
    ),
]


# ───────────────────────────── Utilitats ─────────────────────────────

def slugify(path: str) -> str:
    """Identificador HTML segur a partir d'una ruta."""
    s = re.sub(r"[^a-zA-Z0-9._-]+", "-", path)
    s = s.strip("-").lower()
    return s or "doc"


def find_files_for_category(globs: List[str]) -> List[Path]:
    """Retorna els Paths que coincideixen amb algun glob, ordenats, sense duplicats."""
    seen: set = set()
    out: List[Path] = []
    for g in globs:
        for p in sorted(ROOT.glob(g)):
            if not p.is_file():
                continue
            rel = p.relative_to(ROOT).as_posix()
            if rel in INFRASTRUCTURE_FILES or rel in INFRASTRUCTURE_DIRS:
                continue
            if p.name.startswith("_"):  # plantilles
                continue
            if rel in seen:
                continue
            seen.add(rel)
            out.append(p)
    return out


def category_for(path: Path) -> Tuple[str, str]:
    """Retorna (nom_categoria, emoji) per a un Path, o (Altres, 📦) si no n'hi ha cap de coincident."""
    rel = path.relative_to(ROOT).as_posix()
    for name, emoji, globs in CATEGORIES:
        for g in globs:
            # glob simple amb suport de subdirectoris
            if "**" in g:
                continue
            if "/" in g and g.endswith("/*.md"):
                sub, pat = g.split("/", 1)
                if rel.startswith(sub + "/") and fnmatch(rel.split("/", 1)[1], pat):
                    return name, emoji
            elif "/" in g:
                if rel == g:
                    return name, emoji
            else:
                if rel == g:
                    return name, emoji
    return "Altres", "📦"


def fnmatch(name: str, pattern: str) -> bool:
    """Fnmatch simple per patrons com '*.md' (sense llibreria)."""
    regex = re.escape(pattern).replace(r"\*\*", ".*").replace(r"\*", "[^/]*").replace(r"\?", ".")
    return re.fullmatch(regex, name) is not None


def extract_title_and_summary(md_text: str, fallback: str) -> Tuple[str, str]:
    """Extreu el primer # i el primer paràgraf com a resum curt."""
    title = fallback
    summary = ""
    lines = md_text.splitlines()
    for ln in lines:
        ln = ln.strip()
        if ln.startswith("# "):
            title = ln[2:].strip()
            break
    # Primer paràgraf no buit, no blockquote, no llista
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        if ln.startswith(("#", ">", "-", "*", "|", "!")):
            continue
        summary = ln
        break
    return title, summary[:200]


# ───────────────────────────── Generació ─────────────────────────────

def build():
    # 1) Recollir tots els .md i classificar
    all_md = [p for p in ROOT.rglob("*.md")
              if ".git" not in p.parts
              and p.relative_to(ROOT).as_posix() not in INFRASTRUCTURE_FILES
              and p.relative_to(ROOT).as_posix() not in INFRASTRUCTURE_DIRS
              and not p.name.startswith("_")]

    # 2) Assignar categoria
    by_cat: Dict[str, List[Path]] = {}
    cat_emoji: Dict[str, str] = {}
    for cat, emoji, _ in CATEGORIES:
        by_cat[cat] = []
        cat_emoji[cat] = emoji
    by_cat.setdefault("Altres", [])
    cat_emoji.setdefault("Altres", "📦")

    for p in all_md:
        cat, emoji = category_for(p)
        by_cat[cat].append(p)
        cat_emoji[cat] = emoji

    # 3) Per cada document, generar HTML i metadades
    docs = []
    for cat in by_cat:
        for p in sorted(by_cat[cat], key=lambda x: x.name.lower()):
            rel = p.relative_to(ROOT).as_posix()
            md_text = p.read_text(encoding="utf-8")
            title, summary = extract_title_and_summary(md_text, p.stem)
            body_html = markdown.markdown(
                md_text,
                extensions=["tables", "fenced_code", "toc", "sane_lists", "nl2br"],
                output_format="html5",
            )
            docs.append({
                "id": slugify(rel),
                "path": rel,
                "title": title,
                "summary": summary,
                "category": cat,
                "html": body_html,
            })

    # 4) Estructura per al sidebar (comptar docs per categoria)
    sidebar = []
    for cat, emoji, _ in CATEGORIES:
        sidebar.append({
            "name": cat,
            "emoji": emoji,
            "count": len(by_cat.get(cat, [])),
        })
    if by_cat.get("Altres"):
        sidebar.append({"name": "Altres", "emoji": "📦", "count": len(by_cat["Altres"])})

    total_docs = len(docs)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 4b) Generar dades de la checklist del mes actual (per al giny del lloc web)
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "hort_checklist", ROOT / "hort-checklist.py"
        )
        hc = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hc)
        from datetime import date as _date
        today = _date.today()
        checklist_data = hc.generar_json(today.year, today.month)
        # Desa el JSON a site/ perquè es pugui consumir independentment
        (SITE_DIR / "checklist-data.json").write_text(
            json.dumps(checklist_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        print(f"⚠️  No s'ha pogut generar la checklist: {e}")
        checklist_data = None

    # 5) Renderitzar HTML
    out = render_html(docs, sidebar, total_docs, generated_at, checklist_data)
    OUT_FILE.write_text(out, encoding="utf-8")

    # 6) Resum per consola
    size_kb = OUT_FILE.stat().st_size / 1024
    print(f"✅ site/index.html generat")
    print(f"   Documents:  {total_docs}")
    print(f"   Categories: {len(sidebar)}")
    print(f"   Mida:       {size_kb:.1f} KB")
    print(f"   Data:       {generated_at}")
    for s in sidebar:
        print(f"     - {s['emoji']}  {s['name']:<25} {s['count']:>3} docs")


def render_html(docs, sidebar, total_docs, generated_at, checklist_data=None):
    docs_json = json.dumps(docs, ensure_ascii=False)
    sidebar_json = json.dumps(sidebar, ensure_ascii=False)
    checklist_json = json.dumps(checklist_data, ensure_ascii=False) if checklist_data else "null"

    template_path = SITE_DIR / "template.html"
    tpl = template_path.read_text(encoding="utf-8")

    out = (tpl
           .replace("__DOCS__", docs_json)
           .replace("__SIDEBAR__", sidebar_json)
           .replace("__CHECKLIST__", checklist_json)
           .replace("__TOTAL__", str(total_docs))
           .replace("__NCAT__", str(len(sidebar)))
           .replace("__DATE__", generated_at))
    return out


if __name__ == "__main__":
    build()
