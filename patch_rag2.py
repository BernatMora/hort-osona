#!/usr/bin/env python3
"""Substitueix el bloc ask_ollama del rag.py de la RPi per una versio amb failover."""
import re, py_compile

PATH = "/home/bernat/hort-osona/hort-osona-iot/rag.py"
with open(PATH, "rb") as f:
    src = f.read().decode("utf-8")

# Detectar line ending dominant
NL = "\r\n" if src.count("\r\n") > src.count("\n") - src.count("\r\n") else "\n"

m_start = re.search(r'^    def ask_ollama\(.*$', src, re.MULTILINE)
m_end = re.search(r'^    def ask\(', src, re.MULTILINE)
assert m_start and m_end and m_end.start() > m_start.start(), "marcadors no trobats"

new_block_l = [
    '    def ask_ollama(self, prompt: str, system: str = None, timeout: int = None) -> str:',
    '        """Envia el prompt a Ollama: prova els hosts en ordre; el primer que resol guanya."""',
    '        if timeout is None:',
    '            timeout = self.timeout',
    '        payload = {',
    '            "model": self.model,',
    '            "prompt": prompt,',
    '            "stream": False,',
    '            "options": {',
    '                "temperature": 0.4,',
    '                "num_predict": 600,',
    '            }',
    '        }',
    '        if system:',
    '            payload["system"] = system',
    '        body = json.dumps(payload).encode("utf-8")',
    '        for host in self.ollama_hosts:',
    "            url = f\"{host.rstrip('/')}/api/generate\"",
    '            try:',
    '                req = urllib.request.Request(',
    '                    url,',
    '                    data=body,',
    '                    headers={"Content-Type": "application/json"},',
    '                )',
    '                r = urllib.request.urlopen(req, timeout=timeout)',
    '                data = json.loads(r.read())',
    '                # Host bo: el deixem primer (sticky) per a les seguents crides',
    '                if self.ollama_hosts[0] != host:',
    '                    self.ollama_hosts.remove(host)',
    '                    self.ollama_hosts.insert(0, host)',
    '                    print(f"[RAG] Ollama: switch a {host}")',
    '                return data.get("response", "").strip()',
    '            except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:',
    '                print(f"[RAG] Ollama host {host} ha fallat: {e}")',
    '                last_err = e',
    '                continue',
    '        return "[Error: cap Ollama accessible (provats: " + ", ".join(self.ollama_hosts) + ")]"',
    '',
]
new_block = (NL).join(new_block_l) + NL

src_new = src[:m_start.start()] + new_block + NL + src[m_end.start():]

# pre-escalfar: primer host de la llista
src_new = src_new.replace(
    "url = f\"{self.ollama_host.rstrip('/')}/api/generate\"",
    "url = f\"{self.ollama_hosts[0].rstrip('/')}/api/generate\""
)

# neteja: evitar doble linia en blanc abans de def ask
src_new = re.sub(r'\n{3,}(    def ask\()', r'\n\n\1', src_new)

with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(src_new)

py_compile.compile(PATH, doraise=True)
print("OK: ask_ollama substituit amb failover, sintaxi correcta")
# comprova que no queda cap referencia a ollama_host singular fora del __init__
leftover = [i+1 for i, l in enumerate(src_new.splitlines()) if "self.ollama_host." in l]
print("referencies ollama_host singular restants:", leftover if leftover else "cap")