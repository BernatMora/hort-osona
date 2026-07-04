"""
rag.py — Sistema RAG (Retrieval-Augmented Generation) per a Hort Osona.

Combina:
  - 76 fitxes locals de hort (font de veritat)
  - Ollama (LLM local) per generar respostes

Ús:
  from rag import HortRAG
  rag = HortRAG()
  answer = rag.ask("Quan sembrar carbassa a Osona?")
"""

import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Tuple


class HortRAG:
    """Sistema RAG hortolà amb cerca per paraules clau i Ollama."""

    STOPWORDS = {
        'el', 'la', 'els', 'les', 'un', 'una', 'uns', 'unes', 'de', 'del',
        'a', 'al', 'als', 'i', 'o', 'per', 'amb', 'sense', 'que', 'què',
        'és', 'son', 'són', 'com', 'quan', 'on', 'molt', 'molta', 'poc',
        'poca', 'més', 'menys', 'fer', 'faig', 'fa', 'fas', 'fan', 'fer',
        'anar', 'vaig', 'vas', 'va', 'van', 'tenir', 'tinc', 'has', 'ha',
        'he', 'hem', 'heu', 'si', 'no', 'sí', 'també', 'però', 'ja',
    }

    # Fitxers d'infraestructura que NO s'han d'indexar
    INFRASTRUCTURE = {
        "README.md", "CHANGELOG.md", "HORT-CHECKLIST.md",
        "SETUP-SITE.md", "SETUP-GITHUB-PAGES.md", "SETUP-WINDOWS.md",
        "SYNC-SCRIPT.md", "VSCODE-GUIDE.md",
        "hort-osona-iot/README.md", "hort-osona-iot/INICI-RAPID.md",
        "hort-osona-iot/PEDIDO-AMAZON.md", "hort-osona-iot/LLISTA-CURTA.md",
    }

    def __init__(self, docs_dir: str = None, model: str = "hermes3:latest"):
        if docs_dir is None:
            # Per defecte, el directori arrel del projecte
            root = Path(__file__).resolve().parent.parent.parent
            docs_dir = root
        self.docs_dir = Path(docs_dir)
        self.model = model
        self.docs: List[Dict] = []
        self._load_docs()

    def _load_docs(self):
        """Carrega totes les fitxes .md del projecte."""
        self.docs = []
        for md_path in self.docs_dir.rglob("*.md"):
            rel = md_path.relative_to(self.docs_dir).as_posix()
            # Excloure fitxers d'infraestructura i projecte IoT
            if rel in self.INFRASTRUCTURE:
                continue
            if rel.startswith("hort-osona-iot/"):
                continue
            if md_path.name.startswith("_"):
                continue
            try:
                content = md_path.read_text(encoding="utf-8")
                # Títol = primera línia que comença per #
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_path.stem
                self.docs.append({
                    "path": rel,
                    "title": title,
                    "content": content[:2000],
                    "full_content": content,
                })
            except Exception as e:
                print(f"Error llegint {md_path}: {e}")
        print(f"[RAG] Carregades {len(self.docs)} fitxes útils")

    # Sinonims per millorar la cerca
    SYNONYMS = {
        "carbasso": "carbassa",
        "carbassons": "carabassons",
        "tomaca": "tomàquet",
        "tomates": "tomàquet",
        "enciam": "enciam",
        "albahaca": "alfàbrega",
        "cebolla": "ceba",
        "patata": "patata",
        "mildiu": "mildiu",
        "pulgon": "pugó",
        "pulgons": "pugons",
        "hongos": "fongs",
    }

    def _tokenize(self, text: str) -> List[str]:
        """Tokenitza un text: minúscules, sense accents, sense stopwords, amb sinònims."""
        text = text.lower()
        # Treure accents
        text = re.sub(r'[àá]', 'a', text)
        text = re.sub(r'[èé]', 'e', text)
        text = re.sub(r'[ìí]', 'i', text)
        text = re.sub(r'[òó]', 'o', text)
        text = re.sub(r'[ùú]', 'u', text)
        text = re.sub(r'[ç]', 'c', text)
        # Treure caràcters no-alfanumèrics
        words = re.findall(r'[a-z0-9]+', text)
        # Aplicar sinònims
        words = [self.SYNONYMS.get(w, w) for w in words]
        return [w for w in words if w not in self.STOPWORDS and len(w) > 2]

    def search(self, query: str, top_k: int = 4) -> List[Tuple[Dict, float]]:
        """Cerca les fitxes més rellevants per la consulta."""
        query_words = self._tokenize(query)
        if not query_words:
            return []
        results = []
        seen_titles = set()
        for doc in self.docs:
            # Evitar duplicats pel títol
            title_key = doc["title"].strip().lower()
            if title_key in seen_titles:
                continue
            content_lower = doc["content"].lower()
            content_normalized = re.sub(r'[àá]', 'a', content_lower)
            content_normalized = re.sub(r'[èé]', 'e', content_normalized)
            content_normalized = re.sub(r'[ìí]', 'i', content_normalized)
            content_normalized = re.sub(r'[òó]', 'o', content_normalized)
            content_normalized = re.sub(r'[ùú]', 'u', content_normalized)
            content_normalized = re.sub(r'[ç]', 'c', content_normalized)
            doc_tokens = self._tokenize(content_normalized)
            doc_token_set = set(doc_tokens)
            matches = sum(1 for w in query_words if w in doc_token_set)
            title_tokens = self._tokenize(doc["title"])
            title_matches = sum(1 for w in query_words if w in title_tokens)
            score = title_matches * 3 + matches
            if score > 0:
                results.append((doc, score))
                seen_titles.add(title_key)
        results.sort(key=lambda x: -x[1])
        return results[:top_k]

    def build_context(self, docs_with_score: List[Tuple[Dict, float]]) -> str:
        """Construeix el context per al LLM a partir dels documents trobats."""
        parts = []
        for i, (doc, score) in enumerate(docs_with_score, 1):
            parts.append(f"[Font {i}: {doc['title']}]\n{doc['content']}\n")
        return "\n---\n".join(parts)

    def ask_ollama(self, prompt: str, system: str = None, timeout: int = 120) -> str:
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
            return f"[Error: No es pot connectar amb Ollama. Assegura't que estigui actiu: ollama serve]"

    def ask(self, question: str) -> Dict:
        """Pregunta al sistema RAG. Retorna dict amb answer, sources, etc."""
        # 1) Cerca
        results = self.search(question, top_k=4)
        if not results:
            return {
                "answer": "No he trobat cap fitxa rellevant. Prova reformular la pregunta o ampliar el vocabulari.",
                "sources": [],
                "question": question,
            }
        # 2) Construeix context
        context = self.build_context(results)
        # 3) Prompt
        system = (
            "Ets un assistent hortolà expert. Respon SEMPRE en català, "
            "basant-te només en el context proporcionat. Si no tens prou "
            "informació, digue-ho. Sigut precís i pràctic. Format: resposta "
            "breu + llista de punts si cal. Cita les fonts amb [Font N]."
        )
        prompt = (
            f"CONTEXT (de les fitxes locals de l'hort d'Osona):\n\n{context}\n\n"
            f"--- \n\nPREGUNTA: {question}\n\n"
            f"RESPOSTA (en català, basada en el context):"
        )
        # 4) Genera
        answer = self.ask_ollama(prompt, system=system)
        return {
            "answer": answer,
            "sources": [{"path": d["path"], "title": d["title"], "score": s}
                        for d, s in results],
            "question": question,
        }


# Prova ràpida
if __name__ == "__main__":
    import sys
    rag = HortRAG()
    test_qs = [
        "Quan sembrar carbassa a Osona?",
        "Com combatre el mildiu del tomàquet?",
        "Quines plantes medicinals puc cultivar?",
    ]
    if len(sys.argv) > 1:
        test_qs = [" ".join(sys.argv[1:])]
    for q in test_qs:
        print("\n" + "=" * 60)
        print(f"Q: {q}")
        print("=" * 60)
        r = rag.ask(q)
        print(f"\nA: {r['answer']}\n")
        print("Fonts:")
        for s in r["sources"]:
            print(f"  • {s['title']} (score: {s['score']})")
