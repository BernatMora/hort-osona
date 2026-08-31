#!/usr/bin/env python3
"""Elimina la secció bernat-pc del MenuBernatLab.html i mou Ollama al MacBook."""
import re

PATH = '/home/bernat/www-menu/MenuBernatLab.html'
src = open(PATH, encoding='utf-8').read()
orig = src

# 1) Eliminar título H2 + grid de bernat-pc
src = src.replace(
    '    <h2 class="section-title">🖥️ bernat-pc — Serveis únics (la resta si està apagat)</h2>\n    <div class="grid" id="grid-bernatpc"></div>\n\n',
    ''
)

# 2) Eliminar el bloc BERNATPC_URLS sencer (declaración + items)
src = re.sub(
    r'\n    // 🟠 BERNAT-PC \(100\.121\.249\.107\)[\s\S]*?\n    \];',
    '',
    src, count=1
)

# 3) ALL_URLS sin bernat-pc
src = src.replace(
    'const ALL_URLS = [...RASPBERRY_URLS, ...BERNATPC_URLS, ...BERNATLAB_URLS];',
    'const ALL_URLS = [...RASPBERRY_URLS, ...BERNATLAB_URLS];'
)

# 4) render(): quitar gridPc
src = src.replace(
    '''      const gridPi = document.getElementById("grid-raspberry");
      const gridPc = document.getElementById("grid-bernatpc");
      const gridBl = document.getElementById("grid-bernatlab");
      gridPi.innerHTML = "";
      gridPc.innerHTML = "";
      gridBl.innerHTML = "";''',
    '''      const gridPi = document.getElementById("grid-raspberry");
      const gridBl = document.getElementById("grid-bernatlab");
      gridPi.innerHTML = "";
      gridBl.innerHTML = "";'''
)

src = src.replace(
    '''      for (const u of BERNATPC_URLS) {
        if (matches(u)) { gridPc.appendChild(createCard(u)); total++; }
      }
''',
    ''
)

# 5) Footer
src = src.replace('bernat-pc + Raspberry Pi + Docker', 'Raspberry Pi + MacBook Pro + Docker')

# 6) Ollama del MacBook Pro (100.67.26.116) en RASPBERRY_URLS
old_pi2 = '''      { id: 'pi-2', icon: "☁️", name: "Nextcloud", url: "http://100.115.134.76:8080/", desc: "Núvol privat (fitxers, fotos, calendaris)", section: "raspberry" },'''
assert old_pi2 in src, 'linha pi-2 no trobada'
src = src.replace(old_pi2, old_pi2 + '''
      { id: 'pi-mac', icon: "🧠", name: "Ollama (IA al MacBook Pro)", url: "http://100.67.26.116:11434/", desc: "Motor IA local (llama3.2:3b) — host actual de la IA del bot", section: "raspberry" },''')

open(PATH, 'w', encoding='utf-8').write(src)

# Verificaciones
assert 'BERNATPC_URLS' not in src, 'queda BERNATPC_URLS'
assert 'grid-bernatpc' not in src, 'queda grid-bernatpc'
assert '100.121.249.107' not in src, 'queda IP bernat-pc'
assert "100.67.26.116:11434" in src, 'no esta Ollama Mac'
print('OK: seccion bernat-pc eliminada, Ollama Mac afegit, footer actualitzat')