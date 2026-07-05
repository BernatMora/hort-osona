<h1 id="-changelog-hort-osona">📝 CHANGELOG — Hort Osona</h1>
<p>Tots els canvis notables al projecte, per data.</p>
<h2 id="2026-07-03-sensors-iot-assistent-ia-local-rag-ollama">[2026-07-03] — Sensors IoT + Assistent IA local (RAG + Ollama)</h2>
<h3 id="sensors-iot-pàgina-sensors">Sensors IoT — pàgina #sensors</h3>
<ul>
<li>Nova pàgina <code>#sensors</code> a la PWA que consumeix l&#x27;API REST del backend Raspberry (<code>/api/sensors</code>, <code>/api/sensors/{parcela}/history?hours=24</code>)</li>
<li><strong>Targetes de sensor</strong> amb humitat del sòl, llum, temperatura, conductivitat, bateria</li>
<li><strong>Gràfiques SVG natives</strong> (sense llibreries externes) de les últimes 24h per parcel·la</li>
<li><strong>Alerta visual</strong> quan humitat &lt; 30% (targeta amb borde vermell)</li>
<li><strong>Auto-refresc</strong> cada 60 segons</li>
<li><strong>Configuració URL backend</strong> via localStorage (per defecte <code>http://hortpi.local:8000</code>)</li>
<li>Hash routing <code>#sensors</code> afegit</li>
</ul>
<h3 id="assistent-ia-local-ollama-rag">Assistent IA local (Ollama + RAG)</h3>
<ul>
<li><strong><code>hort-osona-iot/rag.py</code></strong> (~8.8 KB): sistema RAG que indexa 147 fitxes locals (76 web + d&#x27;altres) i respon amb cites</li>
<li><strong>Tokenitzador</strong> robust: lowercase, sense accents, stopwords, <strong>sinònims</strong> (carbasso→carbassa, tomaca→tomàquet, pulgon→pugó, etc.)</li>
<li><strong>Cerca per paraules clau</strong> amb bonus títol ×3 i exclusió de duplicats</li>
<li><strong>Model per defecte</strong>: <code>llama3.1</code> (Ollama 0.31.1 al Mac)</li>
<li><strong><code>hort-osona-iot/backend/api_chat.py</code></strong> (~2.5 KB): API FastAPI amb <code>GET /chat/health</code> i <code>POST /chat</code></li>
<li><strong>Singleton RAG</strong> a FastAPI per evitar recarregar documents a cada petició</li>
<li><strong>CORS obert</strong> per permetre accés des de la PWA allotjada a GitHub Pages</li>
<li><strong><code>hort-osona-iot/ollama_test.py</code></strong> (~3.2 KB): script de verificació d&#x27;Ollama</li>
</ul>
<h3 id="pàgina-assistent-xat-ui">Pàgina #assistent (xat UI)</h3>
<ul>
<li>Nova pàgina <code>#assistent</code> a la PWA amb interfície de xat</li>
<li><strong>8 preguntes suggerides</strong> predefinides</li>
<li><strong>Missatge de benvinguda</strong> amb presentació</li>
<li><strong>Format de xat</strong> (usuari a la dreta, assistent a l&#x27;esquerra)</li>
<li><strong>Fonts citades</strong> com a enllaços clicables a les fitxes originals</li>
<li><strong>Configuració URL backend</strong> via localStorage (per defecte <code>http://localhost:8001</code>)</li>
<li><strong>Animació de typing</strong> &quot;Pensant...&quot; durant la generació</li>
<li><strong>100% local i privat</strong> — sense núvol</li>
</ul>
<h3 id="tests-i-validació">Tests i validació</h3>
<ul>
<li>Ad-hoc verification completa: <strong>34/34 checks passen, 0 fallits</strong></li>
<li>3 preguntes reals validades end-to-end (carbassa, planter tomàquet, adventícies útils)</li>
<li>Temps de resposta RAG: 5-15 segons (variable segons model)</li>
<li>4 fonts citades per pregunta</li>
<li><code>node --check</code> JS OK, 16/16 tests unitaris</li>
<li>Backend actiu al port 8001, 147 docs indexats</li>
</ul>
<h2 id="2026-07-03-pwa-github-pages-i-millora-responsive">[2026-07-03] — PWA, GitHub Pages i millora responsive</h2>
<h3 id="pwa-completa">PWA completa</h3>
<ul>
<li><strong><code>site/manifest.json</code></strong>: PWA manifest amb nom, 4 dreceres (Checklist, Quadern, Rotacions, Estadístiques), icones 192/512, paleta terra-verd</li>
<li><strong><code>site/service-worker.js</code></strong>: service worker amb cache-first per assets locals, network-first per Open-Meteo</li>
<li><strong>Icones PWA</strong>: <code>icon.svg</code>, <code>icon-192.png</code>, <code>icon-512.png</code> (verd oliva, planta amb fruit)</li>
<li><strong>Banner d&#x27;instal·lació</strong> PWA al navegador (Chrome, Edge) — botons &quot;Instal·lar&quot; i &quot;Més tard&quot; amb memòria de 7 dies</li>
<li><strong>Mode offline</strong>: un cop instal·lada, l&#x27;app funciona sense Internet</li>
<li><strong>Notificacions programables</strong>: API Notification + scheduling de tasques</li>
<li><strong>API pública</strong>: <code>window.hortOsona.demanarPermisNotif()</code>, <code>.mostrarNotif()</code>, <code>.programarNotif()</code></li>
</ul>
<h3 id="reconfiguració-per-a-github-pages">Reconfiguració per a GitHub Pages</h3>
<ul>
<li>El <code>site/build.py</code> ara genera <code>index.html</code> i tots els fitxers PWA a l&#x27;<strong>arrel del repo</strong> (no pas a <code>site/</code>)</li>
<li>Compatible amb GitHub Pages triant <code>main</code> + <code>/ (root)</code> (l&#x27;única opció que permet la UI actual)</li>
<li>Nova constant <code>GENERATED_AT_ROOT</code> per excloure fitxers generats de la categorització</li>
<li><strong>Publicat a</strong>: &lt;https://BernatMora.github.io/hort-osona/&gt;</li>
</ul>
<h3 id="fix-responsive-mòbil">Fix responsive mòbil</h3>
<ul>
<li><code>html, body { overflow-x: hidden; max-width: 100% }</code> — sense scroll horitzontal</li>
<li><code>@media (max-width: 820px)</code>: layout vertical amb <code>grid-template-rows: auto 1fr</code></li>
<li><strong>Sidebar sticky</strong> al top quan es fa scroll (max-height 50vh)</li>
<li>Nou <code>@media (max-width: 480px)</code>: ajustos per a mòbils petits</li>
</ul>
<h3 id="neteja">Neteja</h3>
<ul>
<li>Esborrat <code>site/index.html</code> duplicat — ja no cal, es regenera a l&#x27;arrel</li>
<li><code>site/</code> conté només els <strong>orígens</strong> (build.py, template.html, manifest.json, service-worker.js, icones, font del checklist)</li>
</ul>
<h2 id="2026-07-03-lots-3-4-i-5-contingut-i-funcionalitats-avançades">[2026-07-03] — Lots 3, 4 i 5: contingut i funcionalitats avançades</h2>
<h3 id="afegit-lot-3-contingut">Afegit (Lot 3 — Contingut)</h3>
<ul>
<li><strong>5 fitxes noves</strong>:</li>
<li><code>07-fitxes-cultius/porro.md</code> (all porro)</li>
<li><code>07-fitxes-cultius/api.md</code> (api)</li>
<li><code>07-fitxes-cultius/rave.md</code> (rave)</li>
<li><code>07-fitxes-cultius/melo.md</code> (meló)</li>
<li><code>adventicies-utilitat-guia.md</code> (plantes adventícies útils)</li>
</ul>
<h3 id="afegit-lot-4-funcionalitats-web">Afegit (Lot 4 — Funcionalitats web)</h3>
<ul>
<li><strong>Pàgina <code>#calendari</code></strong>: vista anual 3×4 de les entrades del quadern</li>
</ul>
<p>d&#x27;observació. Dies marcats amb color ocre + recompte d&#x27;entrades</p>
<ul>
<li>Llegenda visual, targetes resum</li>
<li>Integrada amb el localStorage del quadern</li>
<li><strong>Exportació ICS</strong>: genera un fitxer <code>.ics</code> vàlid amb totes les</li>
</ul>
<p>tasques del mes actual. Importable a Google Calendar, Apple Calendar,</p>
<p>Outlook. Botó verd al checklist</p>
<ul>
<li>2 targetes noves a la pàgina d&#x27;inici: Calendari i Fonts</li>
</ul>
<h3 id="afegit-lot-5-final">Afegit (Lot 5 — Final)</h3>
<ul>
<li><strong>Pàgina <code>#fonts</code></strong>: índex de 12 fonts locals catalanes</li>
</ul>
<p>(Esporus, L&#x27;Era, CCPAE, Fundació Miquel Agustí, Escola Agrària</p>
<p>de Manresa, Xarxa Catalana de Graners, ADRÓ, Vivers Vern, etc.)</p>
<p>organitzades per categoria. Substitueix el lector RSS perquè les</p>
<p>fonts locals no publiquen feeds</p>
<ul>
<li><strong>Impressió / PDF</strong>: CSS <code>@media print</code> dedicat + botó</li>
</ul>
<p>&quot;🖨 Imprimir / PDF&quot; a la checklist. Amaga sidebar, form,</p>
<p>botons; neteja el layout per a A4</p>
<ul>
<li><strong>Estadístiques avançades</strong>: pàgina <code>#stats</code> enriquida amb</li>
<li>Mesos més actius (del quadern)</li>
<li>Temes més registrats (per paraules clau)</li>
<li>Recomanacions personalitzades basades en patrons</li>
<li>Mostra la localitat meteorològica configurada</li>
<li>2 targetes noves a la pàgina d&#x27;inici: Calendari d&#x27;observacions</li>
</ul>
<p>i Fonts locals</p>
<h3 id="modificat">Modificat</h3>
<ul>
<li><code>site/build.py</code>: afegides 5 fitxes noves a la categorització</li>
<li><code>site/template.html</code>: +600 línies (4 pàgines noves + CSS d&#x27;impressió)</li>
<li><code>CHANGELOG.md</code>: reescrit per netejar duplicats</li>
</ul>
<p>---</p>
<h2 id="2026-06-18-generador-de-checklist-mensual-i-prompt-open-webu">[2026-06-18] — Generador de checklist mensual i prompt Open WebUI</h2>
<h3 id="afegit">Afegit</h3>
<ul>
<li><strong><code>hort-checklist.py</code></strong> — generador intel·ligent (721 línies)</li>
<li>Base de dades de ~60 tasques organitzades per mesos (1-12) i 7 categories</li>
</ul>
<p>(sembra, trasplantament, conreu, tractaments, collita, planificació, observació).</p>
<ul>
<li>Càlcul de la <strong>fase lunar real</strong> per a qualsevol data (algorisme de cicles</li>
</ul>
<p>sinòdics, referència 6 gener 2000, període 29.530588 dies, ±1 dia).</p>
<ul>
<li>Modes de sortida: Markdown imprimible, JSON estructurat, prompt Open WebUI,</li>
</ul>
<p>fragment HTML, o escriptura directa a <code>plans-mensuals/AAAA-MM-mes.md</code>.</p>
<ul>
<li>Context climàtic del mes adaptat a Osona (gelades, calor, pluges, dates clau).</li>
<li>Recomanacions biodinàmiques segons la fase lunar (sembra, trasplantament,</li>
</ul>
<p>poda, adob verd).</p>
<ul>
<li><strong>Integració al lloc web</strong> (<code>site/index.html</code>, 1.37 MB):</li>
<li><strong>Giny a la pàgina d&#x27;inici</strong>: targeta esquerra amb el mes actual, fase</li>
</ul>
<p>lunar de la setmana en curs i top tasca prioritària; targeta dreta amb</p>
<p>strip de 4 setmanes i botó &quot;Obrir checklist completa&quot;.</p>
<ul>
<li><strong>Pàgina <code>#checklist</code></strong> completa: taula lunar detallada, tasques</li>
</ul>
<p>organitzades per categoria amb <strong>checkboxes persistents via localStorage</strong>,</p>
<p>dates clau a Osona i prompt Open WebUI amb <strong>botó &quot;Copiar&quot;</strong>.</p>
<ul>
<li>Hash routing ampliat: <code>#checklist</code> carrega la pàgina completa.</li>
<li>Persistència del marcatge entre sessions (cada tasca té clau</li>
</ul>
<p><code>checklist-YYYY-MM-titol</code>).</p>
<ul>
<li><strong><code>HORT-CHECKLIST.md</code></strong> — guia d&#x27;ús completa del generador.</li>
<li><strong><code>tests/test_hort_checklist.py</code></strong> — 16 tests unitaris (6 classes).</li>
</ul>
<p>Tots passen. Inclouen validació de:</p>
<ul>
<li>Fase lunar per a dates reals (verificables amb meteolluna.cat)</li>
<li>Totes les fases possibles</li>
<li>Validesa de les categories i prioritats de tasques</li>
<li>Dates clau dels mesos</li>
<li>Generació de Markdown i JSON</li>
<li>Generació del prompt per Open WebUI</li>
<li><strong>Bug <code>setmanes_del_mes</code> corregit</strong> — la funció retornava 0 setmanes</li>
</ul>
<p>per a gener 2025 a causa d&#x27;un error de precedència d&#x27;operadors al <code>while</code>.</p>
<p>Reescrita amb condicions explícites i límit d&#x27;iteracions segur.</p>
<ul>
<li><strong>Bug de tests corregit</strong> — les dates de fase lunar dels tests eren</li>
</ul>
<p>errònies (el meu record de les fases no coincidia amb l&#x27;algorisme</p>
<p>que ja era correcte). Tests actualitzats amb dates verificades a</p>
<p>meteolluna.cat (8 juny = minvant, 15 juny = nova, 22 juny = creixent,</p>
<p>30 juny = plena).</p>
<h3 id="modificat">Modificat</h3>
<ul>
<li><code>site/build.py</code> — pipeline de generació ampliat per integrar el giny</li>
</ul>
<p>i la pàgina del checklist.</p>
<ul>
<li><code>site/template.html</code> — CSS i JS nous per al giny i la pàgina.</li>
</ul>
<p>---</p>
<h2 id="2026-06-16-lloc-web-unificat">[2026-06-16] — Lloc web unificat</h2>
<h3 id="afegit">Afegit</h3>
<ul>
<li><strong>Lloc web estàtic</strong> a <code>site/index.html</code> (1.3 MB · 71 documents · 9 categories)</li>
<li>Sidebar amb 9 categories, cerca client-side</li>
<li>Renderitzat Markdown, hash routing per a back/forward</li>
<li>Identitat visual: paleta terra-verd-crema, tipografia Fraunces</li>
<li><strong>Pipeline Python</strong> a <code>site/build.py</code> per regenerar el lloc</li>
<li><strong>Template HTML</strong> a <code>site/template.html</code></li>
<li><code>SETUP-SITE.md</code> — instruccions d&#x27;ús del pipeline</li>
</ul>
<h3 id="modificat">Modificat</h3>
<ul>
<li><code>00-index.md</code> — enllaços al lloc</li>
<li><code>CHANGELOG.md</code> — aquesta entrada</li>
<li><code>README.md</code> — nova secció &quot;Lloc web unificat&quot;</li>
</ul>
<p>---</p>
<h2 id="2026-06-15-sessió-inicial-dx27ampliació">[2026-06-15] — Sessió inicial d&#x27;ampliació</h2>
<p>(Detalls de la sessió d&#x27;ampliació del projecte — 15 fitxes de cultiu afegides,</p>
<p>estructura de planificació revisada, documentació ampliada.)</p>
<p>---</p>
<h2 id="2026-06-15-estat-inicial-del-projecte">[2026-06-15] — Estat inicial del projecte</h2>
<p>(Projecte creat amb 60+ fitxes base sobre hort ecològic, plantes medicinals,</p>
<p>bolets, conserves i etnobotànica d&#x27;Osona.)</p>
<p>---</p>
<p>Format basat en <a href="https://keepachangelog.com/ca/1.1.0/" target="_blank" rel="noopener">Keep a Changelog</a>.</p>
<p>Aquest projecte segueix <a href="https://semver.org/spec/v2.0.0.html" target="_blank" rel="noopener">Semantic Versioning</a> per a les guies principals.</p>