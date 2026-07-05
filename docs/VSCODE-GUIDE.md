<h1 id="-guia-de-vs-code-per-al-projecte-hort-osona">🛠️ Guia de VS Code per al projecte hort-osona</h1>
<p>&gt; VS Code és l&#x27;editor que farem servir per editar els fitxers <code>.md</code> (Markdown) i <code>.html</code> del projecte. Aquesta guia t&#x27;ensenya el flux de treball bàsic.</p>
<h2 id="-dreceres-essencials">⌨️ Dreceres essencials</h2>
<table>
<thead><tr>
<th>Acció</th>
<th>Drecera</th>
<th>Notes</th>
</tr></thead><tbody>
<tr>
<td><strong>Obrir paleta de comandes</strong></td>
<td><code>⌘ + Shift + P</code></td>
<td>El centre de control de VS Code</td>
</tr>
<tr>
<td><strong>Vista prèvia del Markdown</strong></td>
<td><code>⌘ + K</code> → <code>V</code></td>
<td>Obre costat a costat</td>
</tr>
<tr>
<td><strong>Cerca fitxers</strong></td>
<td><code>⌘ + P</code></td>
<td>Escriu part del nom</td>
</tr>
<tr>
<td><strong>Cerca dins del projecte</strong></td>
<td><code>⌘ + Shift + F</code></td>
<td>Cerca text a tots els fitxers</td>
</tr>
<tr>
<td><strong>Cerca dins del fitxer</strong></td>
<td><code>⌘ + F</code></td>
<td>Substitueix amb <code>⌘ + H</code></td>
</tr>
<tr>
<td><strong>Anar a un encapçalament</strong></td>
<td><code>⌘ + Shift + O</code></td>
<td>Navega per les seccions del document</td>
</tr>
<tr>
<td><strong>Terminal integrat</strong></td>
<td><code>⌘ + ò</code> (`<code> </code> ``)</td>
<td>Per a <code>git</code>, scripts, etc.</td>
</tr>
<tr>
<td><strong>Comentari</strong></td>
<td><code>⌘ + /</code></td>
<td>Comenta/descomenta línia</td>
</tr>
</table>
<h2 id="-editar-un-fitxer-md-markdown">📝 Editar un fitxer <code>.md</code> (Markdown)</h2>
<ol>
<li><strong>Obre la carpeta del projecte</strong>:</li>
<li><code>⌘ + O</code> → selecciona <code>~/Desktop/hort-osona</code></li>
</ul>
<ol>
<li><strong>Obre un fitxer</strong>:</li>
<li>Sidebar esquerre (si no el tens visible: <code>⌘ + B</code>) → navega</li>
<li>O <code>⌘ + P</code> → escriu part del nom (p. ex. &quot;bleda&quot;)</li>
</ul>
<ol>
<li><strong>Edita-lo</strong> com si fos un editor de text normal</li>
</ul>
<ol>
<li><strong>Vista prèvia en directe</strong>:</li>
<li><code>⌘ + K</code> → <code>V</code> (primer K, deixar anar, V)</li>
<li>Veure&#x27;s l&#x27;edició a l&#x27;esquerra i el render a la dreta</li>
<li>Es va actualitzant mentre escrius</li>
</ul>
<ol>
<li><strong>Desar</strong>: <code>⌘ + S</code></li>
</ul>
<h2 id="-obrir-un-fitxer-html-al-navegador">🌐 Obrir un fitxer <code>.html</code> al navegador</h2>
<p>Per a les calculadores i eines interactives:</p>
<ol>
<li>Click dret al fitxer → <strong>&quot;Reveal in Finder&quot;</strong> (veure&#x27;l al Finder)</li>
<li>Doble clic → s&#x27;obre al navegador per defecte</li>
</ul>
<p>O des de terminal integrat:</p>
<pre><code>
open -a &quot;Safari&quot; ~/Desktop/hort-osona/calculadora-reg-imprimible.html
</code></pre>
<p>També pots fer servir l&#x27;extensió <strong>Live Server</strong> (veure extensions recomanades) que recarrega automàticament.</p>
<h2 id="-sincronitzar-amb-git-des-de-vs-code">🔄 Sincronitzar amb Git des de VS Code</h2>
<h3 id="opció-a-terminal-integrat">Opció A — Terminal integrat</h3>
<ol>
<li><code>⌘ + ò</code> per obrir el terminal</li>
<li>Escriu:</li>
</ul>
<pre><code>
   git pull
   # ... editar fitxers ...
   git add .
   git commit -m &quot;El que he canviat&quot;
   git push
</code></pre>
<ol>
<li>O més fàcil, amb el nostre script:</li>
</ul>
<pre><code>
   ./hort-sync.sh &quot;El que he canviat&quot;
</code></pre>
<h3 id="opció-b-paleta-de-comandes">Opció B — Paleta de comandes</h3>
<ol>
<li><code>⌘ + Shift + P</code></li>
<li>Escriu &quot;Tasks: Run Task&quot;</li>
<li>Tria &quot;Hort: sync (commit + push)&quot;</li>
<li>Escriu el missatge del commit</li>
<li>S&#x27;executa automàticament</li>
</ul>
<h3 id="opció-c-interfície-gràfica">Opció C — Interfície gràfica</h3>
<p>VS Code ja té Git integrat! Mira la barra lateral esquerra:</p>
<ul>
<li>📁 <strong>Explorer</strong> — fitxers</li>
<li>🔍 <strong>Search</strong> — cerca</li>
<li>🌿 <strong>Source Control</strong> (Ctrl + Shift + G) — aquí tens:</li>
<li>Veure els canvis pendents</li>
<li>Fer commit amb missatge</li>
<li>Push i pull amb botons</li>
</ul>
<h2 id="-extensions-recomanades-ja-configurades">🧩 Extensions recomanades (ja configurades)</h2>
<p>Quan obris el projecte, VS Code et preguntarà si vols instal·lar-les. Accepta!</p>
<ul>
<li><strong>Markdown All in One</strong> — dreceres, llistes, taules, tot</li>
<li><strong>markdownlint</strong> — corregeix errors d&#x27;estil del Markdown</li>
<li><strong>markdown-mermaid</strong> — diagrames dins del Markdown</li>
<li><strong>Markdown Preview Enhanced</strong> — vista prèvia millorada</li>
<li><strong>Live Server</strong> — servidor local per a HTML (recàrrega automàtica)</li>
<li><strong>GitLens</strong> — superpoders per a Git</li>
<li><strong>Material Icon Theme</strong> — icones més boniques</li>
<li><strong>Catppuccin</strong> — tema de colors suau</li>
</ul>
<h2 id="-estructura-típica-dx27edició">📂 Estructura típica d&#x27;edició</h2>
<pre><code>
VS Code
├── Sidebar (esquerra):   explorador de fitxers
├── Editor (centre):      el fitxer que edites
├── Preview (dreta):      vista prèvia Markdown (⌘K, V)
└── Terminal (a baix):    `⌘ ò` per obrir
</code></pre>
<h2 id="-personalització">🎨 Personalització</h2>
<h3 id="canviar-el-tema">Canviar el tema</h3>
<ol>
<li><code>⌘ + K</code> → <code>⌘ + T</code></li>
<li>Tria un dels temes (recomano: &quot;Light+&quot;, &quot;Solarized Light&quot;, &quot;Catppuccino Latte&quot;)</li>
</ul>
<h3 id="augmentar-mida-de-la-lletra">Augmentar mida de la lletra</h3>
<ol>
<li><code>⌘ + ,</code> (preferències)</li>
<li>Cerca &quot;font size&quot;</li>
<li>Puja-ho a 15-16</li>
</ul>
<h3 id="canviar-idioma-a-català">Canviar idioma a català</h3>
<ol>
<li><code>⌘ + Shift + P</code> → &quot;Configure Display Language&quot;</li>
<li>Busca &quot;Catalan&quot; — si està disponible, canvia</li>
</ul>
<h2 id="-workflow-recomanat-per-al-dia-a-dia">📚 Workflow recomanat per al dia a dia</h2>
<ol>
<li><strong>Obre VS Code</strong> amb la carpeta del projecte</li>
<li><code>⌘ + ò</code> per obrir el terminal</li>
<li><code>git pull</code> (o <code>hort-sync.sh pull</code>) per baixar canvis de l&#x27;altre PC</li>
<li><strong>Edita</strong> els fitxers que vulguis</li>
<li><code>⌘ + S</code> per desar</li>
<li><strong>Revisa</strong> els canvis a la pestanya &quot;Source Control&quot;</li>
<li>Fes <strong>commit + push</strong> amb <code>hort-sync.sh &quot;missatge&quot;</code> o des de la UI</li>
</ul>
<h2 id="-si-alguna-cosa-no-va">🆘 Si alguna cosa no va</h2>
<ul>
<li><strong>No veus la vista prèvia?</strong> → Comprova que el fitxer té extensió <code>.md</code></li>
<li><strong>&quot;Git no trobat&quot;?</strong> → VS Code sol trobar-lo sol; sinó, instal·la&#x27;l amb <code>xcode-select --install</code></li>
<li><strong>Vista prèvia buida?</strong> → Desa el fitxer (<code>⌘ + S</code>) i espera 1 segon</li>
</ul>
<h2 id="-recursos">📖 Recursos</h2>
<ul>
<li>Documentació oficial: https://code.visualstudio.com/docs</li>
<li>Markdown en 90 segons: https://commonmark.org/</li>
<li>Catàcul de Markdown: https://www.markdownguide.org/cheat-sheet/</li>
</ul>