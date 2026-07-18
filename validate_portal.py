#!/usr/bin/env python3
"""Valida estructura, enllaços, metadades i contingut sensible d’Hort Osona."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from build_portal_v2 import BASE, CATEGORIES, HIGH_RISK_DOCS


MONTHS = {
    "01": "gener", "02": "febrer", "03": "març", "04": "abril",
    "05": "maig", "06": "juny", "07": "juliol", "08": "agost",
    "09": "setembre", "10": "octubre", "11": "novembre", "12": "desembre",
}


def validate() -> list[str]:
    errors: list[str] = []
    catalogued: list[str] = []
    for category, items in CATEGORIES.items():
        for rel_path, _label in items:
            catalogued.append(rel_path)
            path = BASE / rel_path
            if not path.exists():
                errors.append(f"{category}: falta {rel_path}")
                continue
            text = path.read_text(encoding="utf-8")
            if not re.search(r"^#\s+\S", text, re.M):
                errors.append(f"{rel_path}: falta un títol H1")
            match = re.search(r"plans-mensuals/2026-(\d{2})-", rel_path)
            if match:
                expected = MONTHS[match.group(1)]
                title = re.search(r"^#\s+(.+)$", text, re.M)
                if title and expected not in title.group(1).lower():
                    errors.append(f"{rel_path}: el títol no correspon a {expected}")

            for href in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if href.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean = unquote(href.split("#", 1)[0])
                candidates = (path.parent / clean, BASE / clean)
                if clean == "site/index.html":
                    candidates += (BASE / "index.html",)
                if clean and not any(candidate.exists() for candidate in candidates):
                    errors.append(f"{rel_path}: enllaç inexistent {href}")

    if len(catalogued) != len(set(catalogued)):
        errors.append("Hi ha documents duplicats al catàleg")
    for rel_path in HIGH_RISK_DOCS:
        if rel_path not in catalogued:
            errors.append(f"Document sensible fora del catàleg: {rel_path}")

    index = (BASE / "index.html").read_text(encoding="utf-8") if (BASE / "index.html").exists() else ""
    for marker in ("canonical", "og:title", "Avui al meu hort", "Política editorial"):
        if marker not in index:
            errors.append(f"index.html: falta {marker}")
    for required in ("robots.txt", "sitemap.xml", "404.html"):
        if not (BASE / required).exists():
            errors.append(f"Falta {required}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)
    print("Portal vàlid: estructura, enllaços, risc editorial i SEO correctes")
