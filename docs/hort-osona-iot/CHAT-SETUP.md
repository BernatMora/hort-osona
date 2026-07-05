<h1 id="-sistema-de-xat-amb-ia-local-rag-ollama">🤖 Sistema de xat amb IA local (RAG + Ollama)</h1>
<p>&gt; Com fer servir l&#x27;assistent hortolà que respon consultes en català basant-se en les fitxes del projecte.</p>
<h2 id="-què-és">🎯 Què és?</h2>
<p>L&#x27;API de xat combina:</p>
<ul>
<li><strong>76-2.706 fitxes</strong> locals del projecte (RAG)</li>
<li><strong>Ollama</strong> (model <code>hermes3:latest</code>, 8B paràmetres) — IA local, sense enviar res a Internet</li>
<li><strong>FastAPI</strong> — servidor web</li>
</ul>
<p>Permet fer preguntes com:</p>
<ul>
<li>&quot;Quan sembrar carbassa a Osona?&quot;</li>
<li>&quot;Com combatre el pugó al tomàquet?&quot;</li>
<li>&quot;Quines plantes medicinals puc cultivar?&quot;</li>
</ul>
<p>I obté respostes en <strong>català</strong> basant-se en les teves fitxes.</p>
<h2 id="-arquitectura">🏗️ Arquitectura</h2>
<pre><code>
┌──────────┐    HTTP     ┌─────────────────┐    HTTP    ┌──────────┐
│ PWA/curl │ ──────────► │ FastAPI:8001    │ ────────► │ Ollama   │
│          │ ◄────────── │ (api_chat.py)   │ ◄──────── │ :11434   │
└──────────┘   JSON      └─────────────────┘   JSON     └──────────┘
                              │
                              ▼
                        ┌──────────┐
                        │  RAG     │ → 76 fitxes locals
                        └──────────┘
</code></pre>
<h2 id="-com-arrencar-ho">🚀 Com arrencar-ho</h2>
<h3 id="1-assegurax27t-que-ollama-està-actiu">1. Assegura&#x27;t que Ollama està actiu</h3>
<pre><code>
# Si no s&#x27;està executant
open -a Ollama

# Comprova
curl http://localhost:11434/
# Hauria de respondre: &quot;Ollama is running&quot;
</code></pre>
<p>Si no tens <code>llama3.1</code>, no et preocupis — el sistema ara usa <code>hermes3:latest</code> per defecte.</p>
<p>Per instal·lar un model concret:</p>
<pre><code>
ollama pull hermes3:latest
# o
ollama pull llama3.1
</code></pre>
<h3 id="2-arrenca-el-backend-de-xat">2. Arrenca el backend de xat</h3>
<p>Opció A — Amb l&#x27;script (recomanada):</p>
<pre><code>
cd ~/Desktop/hort-osona/hort-osona-iot
./start-chat.sh
</code></pre>
<p>Opció B — Manualment:</p>
<pre><code>
cd ~/Desktop/hort-osona/hort-osona-iot
python3 -m pip install --user fastapi uvicorn pydantic
python3 -m uvicorn backend.api_chat:app --host 0.0.0.0 --port 8001
</code></pre>
<p>Veuràs:</p>
<pre><code>
INFO:     Started server process [PID]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
</code></pre>
<h3 id="3-provax27l">3. Prova&#x27;l!</h3>
<pre><code>
# Health check
curl http://localhost:8001/chat/health

# Fer una pregunta
curl -X POST http://localhost:8001/chat \
  -H &quot;Content-Type: application/json&quot; \
  -d &#x27;{&quot;question&quot;: &quot;Quan sembrar carbassa a Osona?&quot;}&#x27;
</code></pre>
<p>Obre el navegador a:</p>
<ul>
<li><strong>http://localhost:8001/docs</strong> — interfície Swagger amb tots els endpoints</li>
</ul>
<h2 id="-endpoints">📡 Endpoints</h2>
<table>
<thead><tr>
<th>Mètode</th>
<th>URL</th>
<th>Descripció</th>
</tr></thead><tbody>
<tr>
<td><code>GET</code></td>
<td><code>/chat/health</code></td>
<td>Estat del sistema (model, docs carregats)</td>
</tr>
<tr>
<td><code>POST</code></td>
<td><code>/chat</code></td>
<td>Fer una pregunta</td>
</tr>
<tr>
<td><code>GET</code></td>
<td><code>/docs</code></td>
<td>Documentació interactiva (Swagger)</td>
</tr>
</table>
<h3 id="exemple-de-resposta">Exemple de resposta</h3>
<pre><code>
{
  &quot;answer&quot;: &quot;Segons la fitxa de cultiu proporcionada, a Osona es recomana sembrar carbassa en modals protegits com a abril...&quot;,
  &quot;sources&quot;: [
    {&quot;path&quot;: &quot;07-fitxes-cultius/carbassa.md&quot;, &quot;title&quot;: &quot;Fitxa de cultiu: Carbassa&quot;, &quot;score&quot;: 8.0},
    {&quot;path&quot;: &quot;pla-12-mesos.md&quot;, &quot;title&quot;: &quot;Pla dels 12 mesos&quot;, &quot;score&quot;: 5.0}
  ],
  &quot;question&quot;: &quot;Quan sembrar carbassa?&quot;,
  &quot;model&quot;: &quot;hermes3:latest&quot;,
  &quot;elapsed_ms&quot;: 31949
}
</code></pre>
<h2 id="-resolució-de-problemes">🛠️ Resolució de problemes</h2>
<h3 id="-quotollama-is-not-runningquot">❌ &quot;Ollama is not running&quot;</h3>
<pre><code>
open -a Ollama
sleep 5
curl http://localhost:11434/
</code></pre>
<h3 id="-quotmodel-x27xx27-not-foundquot-a-ollama">❌ &quot;model &#x27;X&#x27; not found&quot; a Ollama</h3>
<pre><code>
# Mira quins models tens
ollama list

# Instal·la el que necessitis
ollama pull hermes3:latest
</code></pre>
<p>O canvia el model per defecte a <code>rag.py</code> (línia 43):</p>
<pre><code>
def __init__(self, docs_dir: str = None, model: str = &quot;elteumodel&quot;):
</code></pre>
<h3 id="-el-backend-penja-en-chathealth">❌ El backend penja en <code>/chat/health</code></h3>
<p>Normalment és perquè el RAG està carregant 76+ fitxes. La primera vegada triga ~25 segons, les següents van ràpides.</p>
<p>Si penja per sempre:</p>
<ol>
<li>Comprova que tens permisos de lectura a tots els <code>.md</code></li>
<li>Mira els logs d&#x27;Uvicorn per si hi ha un error</li>
<li>Prova de buidar el sistema: <code>pkill -f uvicorn</code> i tornar a arrencar</li>
</ul>
<h3 id="-quotport-8001-already-in-usequot">❌ &quot;Port 8001 already in use&quot;</h3>
<pre><code>
lsof -i :8001
# Mata el procés que l&#x27;ocupa o canvia el port a l&#x27;script
</code></pre>
<h2 id="-rendiment">⚡ Rendiment</h2>
<ul>
<li><strong>Primera càrrega</strong>: 25-30 segons (llegeix totes les fitxes)</li>
<li><strong>Health check</strong>: &lt;2 segons</li>
<li><strong>Pregunta simple</strong>: 20-40 segons (depen d&#x27;Ollama)</li>
<li><strong>Memòria</strong>: ~1 GB (Ollama carrega el model a RAM)</li>
</ul>
<h2 id="-aturar-el-servidor">🛑 Aturar el servidor</h2>
<pre><code>
# Si l&#x27;has arrencat amb l&#x27;script: Ctrl+C

# Si l&#x27;has arrencat amb uvicorn en background:
pkill -f &quot;uvicorn.*api_chat&quot;
</code></pre>
<h2 id="-configuració-remota-raspberry-pi">🌍 Configuració remota (Raspberry Pi)</h2>
<p>Si vols usar el xat des de la Raspberry Pi de l&#x27;hort:</p>
<ol>
<li>Assegura&#x27;t que l&#x27;API escolta a <code>0.0.0.0</code> (ja ho fa)</li>
<li>Accedeix des d&#x27;un altre dispositiu: <code>http://IP-DE-LA-PI:8001/chat/health</code></li>
<li>O usa Tailscale per accés segur des de fora de casa</li>
</ul>
<p>A la PWA, configura <code>BACKEND_URL</code> a <code>http://hortpi.local:8001</code> o la IP de Tailscale.</p>
<h2 id="-més-informació">📚 Més informació</h2>
<ul>
<li><a href="rag.py" target="_blank" rel="noopener">rag.py</a> — el sistema RAG</li>
<li><a href="backend/api_chat.py" target="_blank" rel="noopener">api_chat.py</a> — l&#x27;API FastAPI</li>
<li><a href="README.md" target="_blank" rel="noopener">README.md</a> — el projecte IoT complet</li>
</ul>