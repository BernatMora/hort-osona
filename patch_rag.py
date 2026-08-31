#!/usr/bin/env python3
"""Aplica failover d'Ollama hosts al rag.py de la RPi (edicio in-place segura)."""
import re, sys

PATH = "/home/bernat/hort-osona/hort-osona-iot/rag.py"
src = open(PATH, encoding="utf-8").read()

# 1) __init__: llista de hosts amb fallback
old_init = """        self.model = model or os.environ.get('OLLAMA_MODEL', 'gemma3:1b')
        self.ollama_host = ollama_host or os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
        self.timeout = timeout or int(os.environ.get('OLLAMA_TIMEOUT', '180'))"""
new_init = """        self.model = model or os.environ.get('OLLAMA_MODEL', 'gemma3:1b')
        # Llista de hosts Ollama en ordre de preferencia (OLLAMA_HOSTS="u1,u2").
        # El primer que respondi guanya; l'ultim es el fallback local.
        hosts_env = os.environ.get('OLLAMA_HOSTS', '')
        if hosts_env:
            self.ollama_hosts = [h.strip() for h in hosts_env.split(',') if h.strip()]
        else:
            self.ollama_hosts = [ollama_host or os.environ.get('OLLAMA_HOST', 'http://localhost:11434')]
        self.timeout = timeout or int(os.environ.get('OLLAMA_TIMEOUT', '180'))"""
assert old_init in src, "init no trobat"
src = src.replace(old_init, new_init)

# 2) ask_ollama: provar hosts en ordre, guardar quin funciona
old_ask = '''    def ask_ollama(self, prompt: str, system: str = None, timeout: int = 120) -> str:
        """Envia un prompt a Ollama i retorna la resposta."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 600,
            }
        }
        if system:
            payload["system"] = system
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            r = urllib.request.urlopen(req, timeout=timeout)
            data = json.loads(r.read())
            return data.get("response", "").strip()
        except (urllib.error.URLError, OSError) as e:
            return f"[Error: No es pot connectar amb Ollama. Assegura't que estigui actiu: ollama serve]"'''
new_ask = '''    def ask_ollama(self, prompt: str, system: str = None, timeout: int = 120) -> str:
        """Envia un prompt a Ollama, provo els hosts en ordre i uso el primer que resol."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 600,
            }
        }
        if system:
            payload["system"] = system
        body = json.dumps(payload).encode("utf-8")
        last_err = None
        for host in self.ollama_hosts:
            url = f"{host.rstrip('/')}/api/generate"
            try:
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers={"Content-Type": "application/json"},
                )
                r = urllib.request.urlopen(req, timeout=timeout)
                data = json.loads(r.read())
                # Aquest host funciona: el deixem primer (sticky per a les seguents)
                if self.ollama_hosts[0] != host:
                    self.ollama_hosts.remove(host)
                    self.ollama_hosts.insert(0, host)
                    print(f"[RAG] Ollama: switch a {host}")
                return data.get("response", "").strip()
            except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
                print(f"[RAG] Ollama host {host} ha fallat: {e}")
                last_err = e
                continue
        return "[Error: cap Ollama accessible (provat: " + ", ".join(self.ollama_hosts) + ")]"'''
assert old_ask in src, "ask_ollama no trobat"
src = src.replace(old_ask, new_ask)

# 3) pre-escalfar: usar el primer host de la llista
old_pre = '''            url = f"{self.ollama_host.rstrip('/')}/api/generate"'''
new_pre = '''            url = f"{self.ollama_hosts[0].rstrip('/')}/api/generate"'''
if old_ask in src:
    pass
if old_pre in src:
    src = src.replace(old_pre, new_pre)

open(PATH, "w", encoding="utf-8").write(src)
print("rag.py patchejat OK")

# Verificacio de sintaxi
import py_compile
py_compile.compile(PATH, doraise=True)
print("sintaxi OK")