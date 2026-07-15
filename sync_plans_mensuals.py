"""
Sincronitza plans-mensuals/*.md a docs/plans-mensuals/*.html (i al revés).

Converteix Markdown a HTML basic (compatible amb la web) i el posa
a docs/plans-mensuals/<filename>.html (amb extensio .html, no .md).

Aixo es necessari perque la web fa fetch('docs/' + path) i busca
.fitxers.html, no .md.

Us:
    python sync_plans_mensuals.py
"""
import re
import html
from pathlib import Path
import sys

BASE = Path(r"C:\Users\iadmin\bernatlab\projects\hort-osona")
SRC = BASE / "plans-mensuals"
DST = BASE / "docs" / "plans-mensuals"


def md_to_html(text: str) -> str:
    """Conversio basica de Markdown a HTML. Suficient per a plans-mensuals/."""
    text = html.escape(text)

    # Capçaleres
    text = re.sub(r'^# (.+)$', r'<h1 id="\1">\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2 id="\1">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3 id="\1">\1</h3>', text, flags=re.MULTILINE)

    # Negreta i cursiva
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Llistes
    text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>\n?)+', lambda m: '<ul>\n' + m.group(0) + '</ul>\n', text, flags=re.DOTALL)

    # Taules simples
    lines = text.split('\n')
    in_table = False
    table_out = []
    for line in lines:
        if line.startswith('|') and not in_table:
            in_table = True
            table_out.append('<table>')
            table_out.append('<thead>')
            cells = [c.strip() for c in line.strip('|').split('|')]
            table_out.append('<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>')
            table_out.append('</thead>')
            table_out.append('<tbody>')
        elif line.startswith('|') and in_table:
            if '---' in line:
                continue  # separador Markdown
            cells = [c.strip() for c in line.strip('|').split('|')]
            table_out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        else:
            if in_table:
                table_out.append('</tbody>')
                table_out.append('</table>')
                in_table = False
            table_out.append(line)
    if in_table:
        table_out.append('</tbody>')
        table_out.append('</table>')
    text = '\n'.join(table_out)

    # Paràgrafs (línies en blanc separen)
    paragraphs = re.split(r'\n\s*\n', text)
    final = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith(('<h1', '<h2', '<h3', '<ul', '<table', '<blockquote')):
            final.append(p)
        else:
            final.append(f'<p>{p}</p>')
    return '\n'.join(final)


def sync_md_to_html():
    """Converteix cada .md de plans-mensuals/ a .html a docs/plans-mensuals/."""
    DST.mkdir(parents=True, exist_ok=True)
    converted = []
    for md_file in sorted(SRC.glob("*.md")):
        html_file = DST / (md_file.stem + ".html")
        content = md_file.read_text(encoding="utf-8")
        html_content = md_to_html(content)
        html_file.write_text(html_content, encoding="utf-8")
        converted.append((md_file.name, html_file.name, len(content), len(html_content)))
    return converted


def cleanup_old_md():
    """Esborra .md antics a docs/plans-mensuals/ que ja no son necessaris.

    La web busca .html pero historicament tambe ha acceptat .md (error 404
    que hem corregit). Aquesta funcio neteja els .md que puguin quedar.
    """
    if not DST.exists():
        return []
    removed = []
    for md_file in DST.glob("*.md"):
        # Comprovar si el .md correspon a un .md font actiu
        src_md = SRC / md_file.name
        if not src_md.exists():
            md_file.unlink()
            removed.append(md_file.name)
    return removed


if __name__ == "__main__":
    print("=" * 60)
    print("Sincronitzacio: plans-mensuals/*.md -> docs/plans-mensuals/*.html")
    print("=" * 60)

    print("\n[1] Convertint Markdown -> HTML...")
    converted = sync_md_to_html()
    if converted:
        print("  " + str(len(converted)) + " fitxers convertits:")
        for src, dst, size_md, size_html in converted:
            print("    " + src + " -> " + dst + " (" + str(size_md) + " -> " + str(size_html) + " bytes)")
    else:
        print("  Cap fitxer .md a plans-mensuals/")

    print("\n[2] Netejant .md antics a docs/plans-mensuals/...")
    removed = cleanup_old_md()
    if removed:
        print("  " + str(len(removed)) + " fitxers .md antics esborrats:")
        for name in removed:
            print("    " + name)
    else:
        print("  Res a netejar")

    print("\n[3] Estat final:")
    if DST.exists():
        for f in sorted(DST.iterdir()):
            print("  " + f.name + ": " + str(f.stat().st_size) + " bytes")

    print("\n" + "=" * 60)
    print("Fet.")
