#!/usr/bin/env python3
"""Comprovacions ràpides abans de publicar Hort Osona."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


BASE = Path(__file__).resolve().parent


class PortalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.assets: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag in {"link", "img", "script"}:
            ref = values.get("href") or values.get("src")
            if ref:
                self.assets.append(ref)


def fail(message: str) -> None:
    print(f"❌ {message}")
    raise SystemExit(1)


def main() -> None:
    index_path = BASE / "index.html"
    if not index_path.exists():
        fail("Falta index.html. Executa python3 build_portal_v2.py")

    source = index_path.read_text(encoding="utf-8")
    match = re.search(r"const DOCS = (.*?);\n", source)
    if not match:
        fail("No s'ha trobat l'índex DOCS dins index.html")
    docs = json.loads(match.group(1))

    missing_docs = [path for path in docs if not (BASE / "docs" / path).is_file()]
    if missing_docs:
        fail("Documents registrats però absents: " + ", ".join(missing_docs))

    parser = PortalParser()
    parser.feed(source)
    duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicate_ids:
        fail("Identificadors HTML duplicats: " + ", ".join(duplicate_ids))

    missing_assets = []
    for ref in parser.assets:
        if re.match(r"^(https?:|data:|#)", ref):
            continue
        if not (BASE / ref).is_file():
            missing_assets.append(ref)
    if missing_assets:
        fail("Recursos locals absents: " + ", ".join(sorted(set(missing_assets))))

    json.loads((BASE / "manifest.json").read_text(encoding="utf-8"))

    script = re.search(r"<script>([\s\S]*)</script>", source)
    if not script:
        fail("No s'ha trobat el JavaScript del portal")
    result = subprocess.run(
        ["node", "-e", "new Function(process.argv[1])", script.group(1)],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail("JavaScript invàlid: " + result.stderr.strip())

    portal_js = script.group(1)
    if ".at(-1)" in portal_js:
        fail("JavaScript incompatible: usa indexació clàssica en lloc de .at(-1)")

    init_start = portal_js.find("document.addEventListener('DOMContentLoaded'")
    listener_pos = portal_js.find("getElementById('menu-btn').addEventListener", init_start)
    month_pos = portal_js.find("configureCurrentMonth();", init_start)
    if init_start < 0 or listener_pos < 0 or month_pos < 0:
        fail("No s'ha trobat la inicialització completa del portal")
    if listener_pos > month_pos:
        fail("Els botons s'han de registrar abans de configurar el mes")

    required_handlers = [
        "menu-btn", "home-btn", "search-btn", "chat-btn",
        "drawer-close", "search-close", "chat-close",
    ]
    missing_handlers = [
        item for item in required_handlers
        if f"getElementById('{item}').addEventListener" not in portal_js
    ]
    if missing_handlers:
        fail("Botons sense controlador: " + ", ".join(missing_handlers))

    print(
        f"✅ Portal correcte: {len(docs)} documents, recursos presents, "
        "JavaScript compatible i botons inicialitzats"
    )


if __name__ == "__main__":
    main()
