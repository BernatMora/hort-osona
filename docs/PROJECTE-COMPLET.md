<h1 id="-hort-osona-visió-completa-del-projecte">🌱 Hort Osona — Visió completa del projecte</h1>
<blockquote><strong>PWA + IoT + IA local + Cloud + Alexa + Backups</strong> — un ecosistema personal d&#x27;horticultura ecològica a Osona.</blockquote>
<blockquote></blockquote>
<blockquote>📅 Última actualització: 2026-07-06</blockquote>
<blockquote>🏷️ Versió: 1.0 (consolidat)</blockquote>
<p>---</p>
<h2 id="-què-és">🎯 Què és?</h2>
<p>Un projecte personal que cobreix <strong>tot el cicle de l&#x27;horticultura</strong> amb tecnologia:</p>
<ol>
<li><strong>Base de coneixement</strong> (76+ fitxes en català) sobre horticultura ecològica a Osona</li>
<li><strong>PWA</strong> (Progressive Web App) que funciona al mòbil i PC, <strong>offline</strong>, amb eines diàries</li>
<li><strong>Sistema IoT</strong> amb sensors LoRa que envien dades en temps real des de l&#x27;hort</li>
<li><strong>IA local</strong> (Ollama + RAG) per preguntar a l&#x27;hort amb llenguatge natural</li>
<li><strong>Skill d&#x27;Alexa</strong> per preguntar a l&#x27;hort amb la veu</li>
<li><strong>Backups automàtics</strong> a iCloud Drive i My Cloud Home (NAS local)</li>
<li><strong>Documents imprimibles</strong> (PDF + HTML) per portar a l&#x27;hort</li>
</ol>
<p>Tot <strong>obert</strong> al repo de GitHub: &lt;https://github.com/BernatMora/hort-osona&gt;</p>
<p>---</p>
<h2 id="-arquitectura-global">🏗️ Arquitectura global</h2>
<pre><code>
┌──────────────────────────────────────────────────────────────────┐
│                          HORT (245 m)                            │
│  [3× Sensors humitat]──┐                                        │
│  [BME280]──────────────┤                                        │
│  [Pluviòmetre]─────────┼──&gt; [Node TTGO LoRa32] ── LoRa 868MHz │
│  [Panell solar]────────┘   (ESP32 + bateria)    (5 km abast)   │
└──────────────────────────────────────────────────────────────────┘
                                                                   │
                                                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CASA — Raspberry Pi 4B                        │
│                                                                  │
│  [Waveshare LoRa HAT]──&gt; [lora_receiver.py] ──&gt; [Supabase Realtime]
│                                                                  │
│  [FastAPI /sensors]─────&gt; ──&gt;                                  │
│  [FastAPI /chat RAG]─────&gt; Ollama (hermes3) ──&gt; 76 fitxes .md   │
│  [Alexa Backend Flask]──&gt;                                          │
└──────────────────────────────────────────────────────────────────┘
              │                            │
              ▼                            ▼
┌──────────────────────┐    ┌──────────────────────────────┐
│    Mac (casa)        │    │   Cloud / Internet           │
│  [PWA navegador]     │    │                              │
│  [Ollama extra]      │    │  [GitHub Pages] ──&gt; PWA web  │
│  [Tailscale] ────────┼───&gt;│  [Alexa Skills]  ──&gt; veu     │
│  [Finder/SMB] ───────┼───&gt;│  [Supabase]      ──&gt; realtime│
└──────────────────────┘    │  [iCloud Drive]  ──&gt; backup  │
                           │  [My Cloud Home] ──&gt; NAS     │
                           └──────────────────────────────┘
</code></pre>
<p>---</p>
<h2 id="-components-principals">📦 Components principals</h2>
<h3 id="1-base-de-coneixement">1. Base de coneixement</h3>
<p><strong>Ubicació</strong>: fitxers <code>.md</code> a l&#x27;arrel del repo i a <code>docs/</code></p>
<ul>
<li><strong>76 documents</strong> en català sobre horticultura ecològica</li>
<li><strong>9 categories</strong> (Planificació, Fitxes cultiu, Conreu avançat, Medicinals, Bolets, etc.)</li>
<li><strong>~28 fitxes de cultiu</strong> específiques (carbassa, tomàquet, enciam, etc.)</li>
<li><strong>12 guies avançades</strong> (associacions, plagues, reg, compostatge, etc.)</li>
<li><strong>Imprimible</strong> en PDF i HTML per a cada secció</li>
</ul>
<p><strong>Fitxers clau</strong>:</p>
<ul>
<li><code>00-index.md</code> — índex general</li>
<li><code>01-calendari-sembra.md</code> — calendari de sembra Osona</li>
<li><code>02-associacions-rotacions.md</code> — què plantar amb què</li>
<li><code>08-pla-mensual.md</code> — pla d&#x27;acció mensual</li>
<li><code>07-fitxes-cultius/*.md</code> — 28 fitxes individuals</li>
<li><code>plans-mensuals/</code> — quaderns mensuals</li>
</ul>
<h3 id="2-pwa-progressive-web-app">2. PWA (Progressive Web App)</h3>
<p><strong>URL pública</strong>: &lt;https://BernatMora.github.io/hort-osona/&gt;</p>
<p><strong>Tecnologia</strong>: HTML + CSS + JS estàtic (zero backend per a la web), servit per GitHub Pages.</p>
<p><strong>Pàgines funcionals</strong> (12 rutes):</p>
<table>
<thead><tr>
<th>Ruta</th>
<th>Què fa</th>
</tr></thead><tbody>
<tr>
<td><code>#welcome</code></td>
<td>Portada + targetes de les 9 categories</td>
</tr>
<tr>
<td><code>#checklist</code></td>
<td>Llista de tasques setmanals amb validació</td>
</tr>
<tr>
<td><code>#quadern</code></td>
<td>Bitàcola d&#x27;observacions diàries (amb tags, cerca, markdown)</td>
</tr>
<tr>
<td><code>#calendari</code></td>
<td>Vista 3×4 del quadern (mesos)</td>
</tr>
<tr>
<td><code>#calendari-any</code></td>
<td>Vista anual completa (12 mesos, lluna, tasques)</td>
</tr>
<tr>
<td><code>#rotacions</code></td>
<td>Rotacions de cultius recomanades</td>
</tr>
<tr>
<td><code>#dates</code></td>
<td>9 localitats d&#x27;Osona + 27 cultius amb dates</td>
</tr>
<tr>
<td><code>#meteo</code></td>
<td>Meteo en temps real via Open-Meteo (7 localitats, 25+ WMO)</td>
</tr>
<tr>
<td><code>#stats</code></td>
<td>Estadístiques d&#x27;ús + gràfic 12 mesos</td>
</tr>
<tr>
<td><code>#fonts</code></td>
<td>12 fonts locals + lectura amb tipografies</td>
</tr>
<tr>
<td><code>#sensors</code></td>
<td>Dades en temps real dels sensors (humitat, llum, etc.)</td>
</tr>
<tr>
<td><code>#assistent</code></td>
<td>Xat amb IA local (Ollama + RAG)</td>
</tr>
<tr>
<td><code>#cerca</code></td>
<td>Cercador avançat amb filtres (categoria, mes, text)</td>
</tr>
</tbody></table>
<p><strong>Característiques PWA</strong>:</p>
<ul>
<li>✅ Instal·lable (banner automàtic al mòbil)</li>
<li>✅ Funciona <strong>offline</strong> (service worker v2 amb cache-first)</li>
<li>✅ Persistent (localStorage per entrades del quadern, tasques, configuració)</li>
<li>✅ 3 temes visuals (estiu/tardor/hivern) amb auto-detecció per mes</li>
<li>✅ 76 docs indexats, cerca instantània</li>
<li>✅ <strong>Reenginyeria recent</strong>: 1.2 MB → 52 KB amb lazy load</li>
</ul>
<p><strong>Fitxers clau</strong>:</p>
<ul>
<li><code>site/template.html</code> — HTML + CSS + JS (tot en un)</li>
<li><code>site/build.py</code> — pipeline que converteix <code>.md</code> → <code>index.html</code></li>
<li><code>site/manifest.json</code> + <code>site/service-worker.js</code> + <code>site/icon-*.png</code> — PWA</li>
<li><code>index.html</code> (generat) — fitxer estàtic final</li>
<li><code>CHANGELOG.md</code> — registre de canvis</li>
</ul>
<h3 id="3-sistema-iot-hort-raspberry-pi">3. Sistema IoT (hort → Raspberry Pi)</h3>
<p><strong>Ubicació</strong>: <code>hort-osona-iot/</code></p>
<p><strong>Stack tecnològic</strong>:</p>
<ul>
<li><strong>Hardware</strong>: ESP32 (TTGO LoRa32 V2) + Waveshare SX1262 868MHz HAT (RPi)</li>
<li><strong>Protocol</strong>: LoRa 868 MHz (5 km abast, 245 m a l&#x27;hort)</li>
<li><strong>Backend</strong>: FastAPI + Mosquitto MQTT + SQLite + Supabase</li>
<li><strong>Llenguatge</strong>: C++ (firmware) + Python (receptor, backend)</li>
</ul>
<p><strong>Components nous afegits recentment</strong>:</p>
<ul>
<li>✅ Node emissor LoRa complet (firmware + documentació) — <code>node-emissor/</code></li>
<li>✅ Receptor LoRa per Raspberry Pi — <code>backend/lora_receiver.py</code></li>
<li>✅ Schema Supabase — <code>backend/supabase_schema.sql</code></li>
<li>✅ Documentació completa — <code>GUIA-MUNTATGE-NODE.md</code></li>
</ul>
<p><strong>Sensors</strong> (previstos):</p>
<ul>
<li>3× Xiaomi MiFlora (humitat sòl, llum, T, conductivitat, bateria)</li>
<li>1× BME280 (T ambient, humitat, pressió)</li>
<li>1× Pluviòmetre</li>
<li>Panell solar + bateria 18650 + TP4056</li>
</ul>
<p><strong>Fitxers clau</strong>:</p>
<ul>
<li><code>hort-osona-iot/README.md</code> — visió general</li>
<li><code>hort-osona-iot/setup-pi.sh</code> — instal·lador automàtic RPi</li>
<li><code>hort-osona-iot/PEDIDO-AMAZON.md</code> + <code>LLISTA-CURTA.md</code> — compres</li>
<li><code>hort-osona-iot/node-emissor/src/main.cpp</code> — firmware ESP32</li>
<li><code>hort-osona-iot/backend/lora_receiver.py</code> — receptor RPi</li>
<li><code>hort-osona-iot/INICI-RAPID.md</code> — quickstart</li>
</ul>
<h3 id="4-assistent-ia-local-ollama-rag">4. Assistent IA local (Ollama + RAG)</h3>
<p><strong>Stack</strong>: Ollama (hermes3 o llama3.1) + RAG sobre 76 fitxes</p>
<p><strong>Característiques</strong>:</p>
<ul>
<li>Respon en <strong>català</strong> amb cites</li>
<li>Sinònims catalans (carbasso → carbassa, etc.)</li>
<li>Stopwords eliminats</li>
<li>Bonus per coincidències al títol</li>
<li>Model local (sense enviar res a Internet)</li>
<li>Suport GPU (Apple Silicon / NVIDIA / CPU)</li>
</ul>
<p><strong>Integració</strong>:</p>
<ul>
<li>🌐 <strong>Web</strong> (PWA): pàgina <code>#assistent</code> amb xat UI</li>
<li>🎤 <strong>Veu</strong> (Alexa): skill &quot;Hort Osona&quot; — <code>hort-osona-iot/ALEXA-GUIA.md</code></li>
<li>🔌 <strong>API</strong> (RPi): <code>hort-osona-iot/backend/api_chat.py</code> (port 8001)</li>
</ul>
<p><strong>Fitxers clau</strong>:</p>
<ul>
<li><code>hort-osona-iot/rag.py</code> — sistema RAG (8.8 KB, ~200 línies)</li>
<li><code>hort-osona-iot/backend/api_chat.py</code> — API FastAPI</li>
<li><code>hort-osona-iot/ollama_test.py</code> — test de l&#x27;API Ollama</li>
<li><code>hort-osona-iot/RAG-README.md</code> — documentació</li>
<li><code>hort-osona-iot/CHAT-SETUP.md</code> — setup del xat</li>
</ul>
<h3 id="5-skill-dx27alexa-quothort-osonaquot">5. Skill d&#x27;Alexa &quot;Hort Osona&quot;</h3>
<p><strong>Funcionalitat</strong>: preguntar a l&#x27;hort amb la veu des d&#x27;un Amazon Echo</p>
<p><strong>Preguntes que entén</strong>:</p>
<ul>
<li>&quot;Alexa, pregunta a l&#x27;hort quan sembrar carbassa&quot;</li>
<li>&quot;Alexa, pregunta a l&#x27;hort com combatre el pugó&quot;</li>
<li>&quot;Alexa, pregunta a l&#x27;hort què fer al juliol&quot;</li>
</ul>
<p><strong>Stack</strong>:</p>
<ul>
<li>Amazon Alexa Skills Kit (cloud)</li>
<li>Flask backend (RPi o Mac) — <code>alexa_backend.py</code></li>
<li>Model d&#x27;interacció JSON — <code>alexa-skill/interaction-model.json</code></li>
<li>RAG local (reutilitza el sistema d&#x27;Ollama)</li>
</ul>
<p><strong>Fitxers clau</strong>:</p>
<ul>
<li><code>hort-osona-iot/ALEXA-GUIA.md</code> — guia completa</li>
<li><code>hort-osona-iot/ALEXA-ACTIVAR.md</code> — com activar la skill</li>
<li><code>hort-osona-iot/COM-TROBAR-SKILL.md</code> — com trobar-la a l&#x27;app Alexa</li>
<li><code>hort-osona-iot/alexa_backend.py</code> — backend Flask (port 5050)</li>
<li><code>hort-osona-iot/alexa-skill/interaction-model.json</code> — intents + utterances</li>
<li><code>hort-osona-iot/scripts/start_alexa.sh</code> — script d&#x27;arrencada</li>
</ul>
<h3 id="6-sistema-de-backups">6. Sistema de backups</h3>
<p><strong>3 capes de seguretat</strong>:</p>
<ol>
<li><strong>GitHub</strong> (remot, privat/públic) — control de versions</li>
<li><strong>iCloud Drive</strong> (2 TB) — <code>ICLOUD-SYNC.md</code> + <code>scripts/setup_icloud_hort.sh</code></li>
<li><strong>My Cloud Home</strong> (WD NAS, 192.168.100.48) — <code>MYCLOUDHOME-GUIA.md</code> + <code>mycloud_storage.py</code></li>
</ol>
<p><strong>Configuració</strong>:</p>
<ul>
<li>iCloud: rsync diari via launchd (macOS) o cron (Linux)</li>
<li>My Cloud Home: SMB/CIFS muntat + script d&#x27;export automàtic</li>
</ul>
<h3 id="7-documents-imprimibles">7. Documents imprimibles</h3>
<p><strong>Ubicació</strong>: <code>plans-mensuals/</code> i arrel (<code>*-2026.pdf</code>)</p>
<p><strong>Tipus</strong>:</p>
<ul>
<li>📅 Quadern d&#x27;observació anual (PDF + HTML)</li>
<li>🌱 Fitxes de cultius (PDF + HTML)</li>
<li>🧪 Conserves casolanes (PDF + HTML)</li>
<li>💧 Pla de reg (PDF)</li>
</ul>
<p><strong>Generació</strong>:</p>
<ul>
<li>HTML imprimible amb CSS @media print</li>
<li>Conversió a PDF via <code>convertir_HTML_a_PDF.sh</code> (Playwright/Chromium headless)</li>
</ul>
<p>---</p>
<h2 id="-estadístiques-del-projecte-2026-07-06">📊 Estadístiques del projecte (2026-07-06)</h2>
<table>
<thead><tr>
<th>Mètrica</th>
<th>Valor</th>
</tr></thead><tbody>
<tr>
<td><strong>Total fitxers al repo</strong></td>
<td>327</td>
</tr>
<tr>
<td><strong>Directoris</strong></td>
<td>9</td>
</tr>
<tr>
<td><strong>Documents .md</strong></td>
<td>~120</td>
</tr>
<tr>
<td><strong>Fitxes de cultiu</strong></td>
<td>28</td>
</tr>
<tr>
<td><strong>Pàgines PWA</strong></td>
<td>12</td>
</tr>
<tr>
<td><strong>Tests unitaris</strong></td>
<td>16 (16/16 OK)</td>
</tr>
<tr>
<td><strong>Mida portal</strong></td>
<td>52 KB (reenginyeria)</td>
</tr>
<tr>
<td><strong>Mida PWA completa</strong></td>
<td>1.5 MB</td>
</tr>
<tr>
<td><strong>Línies de codi IoT</strong></td>
<td>~3,000 (C++ + Python)</td>
</tr>
<tr>
<td><strong>Línies de codi PWA</strong></td>
<td>~10,000 (HTML+CSS+JS)</td>
</tr>
<tr>
<td><strong>Total línies de codi</strong></td>
<td>~15,000+</td>
</tr>
<tr>
<td><strong>Commits totals</strong></td>
<td>50+</td>
</tr>
<tr>
<td><strong>Dies des de l&#x27;inici</strong></td>
<td>~30 dies</td>
</tr>
</tbody></table>
<p>---</p>
<h2 id="-eines-i-tecnologies">🔧 Eines i tecnologies</h2>
<table>
<thead><tr>
<th>Capa</th>
<th>Eines</th>
</tr></thead><tbody>
<tr>
<td><strong>Base de coneixement</strong></td>
<td>Markdown, git</td>
</tr>
<tr>
<td><strong>PWA</strong></td>
<td>HTML5, CSS3 (Grid + variables), JS vanilla, Service Workers, Web App Manifest</td>
</tr>
<tr>
<td><strong>Build</strong></td>
<td>Python 3.11 (build.py, generar-pdf.py)</td>
</tr>
<tr>
<td><strong>PWA hosting</strong></td>
<td>GitHub Pages</td>
</tr>
<tr>
<td><strong>Backend IoT</strong></td>
<td>FastAPI, Mosquitto MQTT, SQLite, Supabase</td>
</tr>
<tr>
<td><strong>Receptor LoRa</strong></td>
<td>Python 3.11, pyserial, spidev</td>
</tr>
<tr>
<td><strong>Firmware emissor</strong></td>
<td>C++ (Arduino/ESP32), PlatformIO, LoRa library</td>
</tr>
<tr>
<td><strong>IA local</strong></td>
<td>Ollama, hermes3 / llama3.1, RAG custom</td>
</tr>
<tr>
<td><strong>Skill Alexa</strong></td>
<td>Alexa Skills Kit, Flask, JSON interaction model</td>
</tr>
<tr>
<td><strong>Cloud</strong></td>
<td>iCloud Drive (rsync), My Cloud Home (SMB/CIFS)</td>
</tr>
<tr>
<td><strong>PDF</strong></td>
<td>reportlab (Python)</td>
</tr>
<tr>
<td><strong>Testing</strong></td>
<td>pytest (16 tests)</td>
</tr>
<tr>
<td><strong>Accés remot</strong></td>
<td>Tailscale (VPN)</td>
</tr>
<tr>
<td><strong>Documentació</strong></td>
<td>Markdown, reportlab</td>
</tr>
</tbody></table>
<p>---</p>
<h2 id="-com-començar">🚀 Com començar</h2>
<h3 id="per-a-tu-desenvolupador">Per a tu (desenvolupador)</h3>
<pre><code>
# Clonar el repo
git clone https://github.com/BernatMora/hort-osona.git
cd hort-osona

# Regenerar la PWA des dels .md
python site/build.py

# Servir localment
python -m http.server 8765
# Obre http://127.0.0.1:8765/index.html
</code></pre>
<h3 id="per-accedir-des-del-mòbil">Per accedir des del mòbil</h3>
<ol>
<li>Obre &lt;https://BernatMora.github.io/hort-osona/&gt; al navegador</li>
<li>Tria &quot;Afegir a pantalla d&#x27;inici&quot; (banner automàtic a Android)</li>
<li>Ja tens la PWA instal·lada</li>
</ol>
<h3 id="per-usar-lx27assistent-ia">Per usar l&#x27;assistent IA</h3>
<ol>
<li>Instal·la <a href="https://ollama.com" target="_blank" rel="noopener">Ollama</a> al Mac</li>
<li>Descarrega un model: <code>ollama pull hermes3</code></li>
<li>Engega el backend: <code>cd hort-osona-iot &amp;&amp; python -m uvicorn backend.api_chat:app --host 0.0.0.0 --port 8001</code></li>
<li>Obre la PWA, vés a <code>#assistent</code> i pregunta!</li>
</ol>
<h3 id="per-activar-alexa">Per activar Alexa</h3>
<ol>
<li>Segueix <code>hort-osona-iot/ALEXA-ACTIVAR.md</code></li>
<li>Engega: <code>./scripts/start_alexa.sh</code></li>
<li>Digues &quot;Alexa, pregunta a l&#x27;hort...&quot;</li>
</ol>
<p>---</p>
<h2 id="-roadmap">🛣️ Roadmap</h2>
<h3 id="-fet">✅ Fet</h3>
<ul>
<li class="task-item"><label><input type="checkbox" data-task-index="0" checked> <span>Base de coneixement (76 fitxes)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="1" checked> <span>PWA funcional amb 12 pàgines</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="2" checked> <span>Cercador avançat</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="3" checked> <span>Calendari anual</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="4" checked> <span>Mode diari ric (tags, markdown, imatges)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="5" checked> <span>Sistema IoT (LoRa + MiFlora + RPi)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="6" checked> <span>IA local (Ollama + RAG)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="7" checked> <span>Skill Alexa</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="8" checked> <span>Backups (iCloud + My Cloud Home)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="9" checked> <span>Reenginyeria portal (1.2 MB → 52 KB)</span></label></li>
</ul>
<h3 id="-en-curs">🔄 En curs</h3>
<ul>
<li class="task-item"><label><input type="checkbox" data-task-index="10"> <span>Muntatge final del hardware (RPi + sensors)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="11"> <span>Configuració Tailscale per accés remot</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="12"> <span>Tests unitaris del frontend</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="13"> <span>Documentació d&#x27;arquitectura (C4, ADR)</span></label></li>
</ul>
<h3 id="-futures-idees">💡 Futures idees</h3>
<ul>
<li class="task-item"><label><input type="checkbox" data-task-index="14"> <span>Càmera IP al·lerta de plagues (TensorFlow Lite a RPi)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="15"> <span>App mòbil nativa (Flutter) amb notificacions push</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="16"> <span>Integració calendari Google/Apple</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="17"> <span>Sistema de reg automatitzat (electrovàlvules)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="18"> <span>Versió multi-hort (compartir entre veïns)</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="19"> <span>Bot oficial de Telegram</span></label></li>
<li class="task-item"><label><input type="checkbox" data-task-index="20"> <span>ML per a prediccions de collita</span></label></li>
</ul>
<p>---</p>
<h2 id="-índex-de-documentació">📚 Índex de documentació</h2>
<table>
<thead><tr>
<th>Tema</th>
<th>Fitxer</th>
</tr></thead><tbody>
<tr>
<td>Visió general del projecte</td>
<td><code>README.md</code></td>
</tr>
<tr>
<td>Canvis</td>
<td><code>CHANGELOG.md</code></td>
</tr>
<tr>
<td>Setup al Windows</td>
<td><code>SETUP-WINDOWS.md</code></td>
</tr>
<tr>
<td>Setup a GitHub Pages</td>
<td><code>SETUP-GITHUB-PAGES.md</code></td>
</tr>
<tr>
<td>Setup del lloc</td>
<td><code>SETUP-SITE.md</code></td>
</tr>
<tr>
<td>Accés mòbil</td>
<td><code>ACCES-MOBIL.md</code></td>
</tr>
<tr>
<td>Accés mòbil (docs)</td>
<td><code>docs/ACCES-MOBIL.md</code></td>
</tr>
<tr>
<td>VSCode</td>
<td><code>VSCODE-GUIDE.md</code></td>
</tr>
<tr>
<td>Test RAG</td>
<td><code>TEST-RAG.md</code></td>
</tr>
<tr>
<td>Xat ràpid</td>
<td><code>XAT-RAPID.md</code></td>
</tr>
<tr>
<td>Llista de compra</td>
<td><code>LLISTA-COMPRA.md</code></td>
</tr>
<tr>
<td>Sincronització</td>
<td><code>SYNC-SCRIPT.md</code></td>
</tr>
<tr>
<td><strong>IoT — visió general</strong></td>
<td><code>hort-osona-iot/README.md</code></td>
</tr>
<tr>
<td><strong>IoT — inici ràpid</strong></td>
<td><code>hort-osona-iot/INICI-RAPID.md</code></td>
</tr>
<tr>
<td><strong>IoT — llista compra</strong></td>
<td><code>hort-osona-iot/PEDIDO-AMAZON.md</code></td>
</tr>
<tr>
<td><strong>IoT — llista curta</strong></td>
<td><code>hort-osona-iot/LLISTA-CURTA.md</code></td>
</tr>
<tr>
<td><strong>IoT — Tailscale Mac</strong></td>
<td><code>hort-osona-iot/GUIA-TAILSCALE-MAC.pdf</code></td>
</tr>
<tr>
<td><strong>IoT — muntatge node</strong></td>
<td><code>hort-osona-iot/GUIA-MUNTATGE-NODE.md</code></td>
</tr>
<tr>
<td><strong>IoT — Alexa guia</strong></td>
<td><code>hort-osona-iot/ALEXA-GUIA.md</code></td>
</tr>
<tr>
<td><strong>IoT — Alexa activar</strong></td>
<td><code>hort-osona-iot/ALEXA-ACTIVAR.md</code></td>
</tr>
<tr>
<td><strong>IoT — Alexa skill</strong></td>
<td><code>hort-osona-iot/COM-TROBAR-SKILL.md</code></td>
</tr>
<tr>
<td><strong>IoT — setup xat</strong></td>
<td><code>hort-osona-iot/CHAT-SETUP.md</code></td>
</tr>
<tr>
<td><strong>IoT — RAG</strong></td>
<td><code>hort-osona-iot/RAG-README.md</code></td>
</tr>
<tr>
<td><strong>IoT — My Cloud</strong></td>
<td><code>hort-osona-iot/MYCLOUDHOME-GUIA.md</code></td>
</tr>
<tr>
<td><strong>IoT — iCloud sync</strong></td>
<td><code>hort-osona-iot/ICLOUD-SYNC.md</code></td>
</tr>
<tr>
<td><strong>IoT — projectes RPi</strong></td>
<td><code>hort-osona-iot/RPi-PROJECTES.md</code></td>
</tr>
<tr>
<td><strong>IoT — pas següent</strong></td>
<td><code>hort-osona-iot/PAS-SEGÜENT.md</code></td>
</tr>
<tr>
<td><strong>Consolidat (aquest)</strong></td>
<td><code>PROJECTE-COMPLET.md</code></td>
</tr>
</tbody></table>
<p>---</p>
<h2 id="-versions">🏷️ Versions</h2>
<ul>
<li><strong>v1.0</strong> (2026-07-06): Estat consolidat amb IoT + IA + Alexa + Cloud</li>
</ul>
<p>---</p>
<h2 id="-llicència">📜 Llicència</h2>
<p>Projecte personal sense llicència explícita. Si t&#x27;interessa, contacta amb Bernat Mora.</p>
<p>---</p>
<h2 id="-agraïments">✨ Agraïments</h2>
<p>A tots els que han contribuït amb idees, codi, inspiració i eines:</p>
<ul>
<li>Ollama per fer la IA local accessible</li>
<li>Open-Meteo per les dades meteorològiques gratuïtes</li>
<li>Tailscale per la xarxa privada gratuïta</li>
<li>Reportlab pels PDFs</li>
<li>GitHub Pages per l&#x27;allotjament gratuït de la PWA</li>
<li>La comunitat open-source en general</li>
</ul>