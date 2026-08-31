#!/usr/bin/env python3
"""Fix critic: afegir self.ollama_hosts al __init__ del rag.py de la RPi."""
import re, py_compile

PATH = "/home/bernat/hort-osona/hort-osona-iot/rag.py"
with open(PATH, "rb") as f:
    src = f.read().decode("utf-8")

if "self.ollama_hosts" in src.split("def ask_ollama")[0]:
    print("init ja te ollama_hosts — res a fer")
else:
    # Anchor: la linia self.timeout del __init__
    m = re.search(r"^(\s*)self\.timeout = .*$", src, re.MULTILINE)
    assert m, "anchor self.timeout no trobat"
    indent = m.group(1)
    NL = "\r\n" if "\r\n" in src else "\n"
    inject = (
        f"{indent}# Hosts Ollama en ordre de preferencia (OLLAMA_HOSTS=\"u1,u2\");"
        f"{NL}"
        f"{indent}# fallback: OLLAMA_HOST unic. El primer que resol guanya (sticky).{NL}"
        f"{indent}hosts_env = os.environ.get('OLLAMA_HOSTS', ''){NL}"
        f"{indent}if hosts_env:{NL}"
        f"{indent}    self.ollama_hosts = [h.strip() for h in hosts_env.split(',') if h.strip()]{NL}"
        f"{indent}else:{NL}"
        f"{indent}    self.ollama_hosts = [os.environ.get('OLLAMA_HOST', 'http://localhost:11434')]{NL}"
    )
    src = src[:m.end()] + NL + inject.rstrip(NL) + src[m.end():]
    with open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(src)
    py_compile.compile(PATH, doraise=True)
    print("OK: __init__ amb ollama_hosts, sintaxi correcta")

# Test funcional rapid (sense tocar el bot en marxa): instanciar i preguntar coses trivial
import subprocess
test = (
    "import sys; sys.path.insert(0, '/home/bernat/hort-osona/hort-osona-iot'); "
    "from rag import HortRAG; r = HortRAG(); "
    "print('hosts:', r.ollama_hosts)"
)
out = subprocess.run(
    ["/home/bernat/hort-osona/hort-osona-iot/venv/bin/python", "-c", test],
    capture_output=True, text=True, timeout=120,
)
print("TEST:", out.stdout.strip()[-200:], out.stderr.strip()[-200:] if out.returncode else "")