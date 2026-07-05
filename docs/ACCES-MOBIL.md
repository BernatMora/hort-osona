<h1 id="-accés-des-del-mòbil-hort-osona-pwa">📱 Accés des del mòbil — Hort Osona PWA</h1>
<p>&gt; Tens el projecte disponible des de qualsevol dispositiu amb navegador, fins i tot <strong>offline</strong>.</p>
<h2 id="-url-pública">🌐 URL pública</h2>
<p><strong>https://BernatMora.github.io/hort-osona/</strong></p>
<p>Aquesta URL:</p>
<ul>
<li>✅ Funciona des de qualsevol lloc del món (no cal estar a casa)</li>
<li>✅ S&#x27;actualitza automàticament cada vegada que fas <code>git push</code></li>
<li>✅ Està allotjada gratuïtament a GitHub Pages</li>
<li>✅ No cal tenir el Mac encès</li>
</ul>
<h2 id="-installar-com-a-app-al-mòbil">📲 Instal·lar com a app al mòbil</h2>
<h3 id="iphone-ipad-safari">iPhone / iPad (Safari)</h3>
<ol>
<li>Obre <strong>https://BernatMora.github.io/hort-osona/</strong> a Safari</li>
<li>Toca el botó <strong>Compartir</strong> (quadrat amb fletxa cap amunt, baix de la pantalla)</li>
<li>Desplaça&#x27;t i tria <strong>&quot;Afegir a la pantalla d&#x27;inici&quot;</strong></li>
<li>Confirma el nom &quot;Hort Osona&quot; i toca <strong>&quot;Afegir&quot;</strong></li>
<li>✅ Tens una icona a la pantalla d&#x27;inici com una app</li>
</ul>
<p>Quan l&#x27;obris:</p>
<ul>
<li>S&#x27;obre <strong>a pantalla completa</strong> (sense barra del Safari)</li>
<li>Es veu igual que l&#x27;aplicació nadiua</li>
<li>Funciona <strong>offline</strong> (gràcies al service worker)</li>
</ul>
<h3 id="android-chrome">Android (Chrome)</h3>
<ol>
<li>Obre <strong>https://BernatMora.github.io/hort-osona/</strong> a Chrome</li>
<li>Toca el menú (3 punts verticals, dalt a la dreta)</li>
<li>Tria <strong>&quot;Instal·lar aplicació&quot;</strong> o <strong>&quot;Afegir a la pantalla d&#x27;inici&quot;</strong></li>
<li>Confirma</li>
<li>✅ Tens una icona al calaix d&#x27;apps</li>
</ul>
<h2 id="-què-pots-fer-des-del-mòbil">✨ Què pots fer des del mòbil</h2>
<p>Un cop instal·lada l&#x27;app, tens accés a:</p>
<ul>
<li><strong>Tots els 92 documents</strong> del projecte</li>
<li><strong>Cerca instantània</strong> a tot el contingut</li>
<li><strong>14 categories</strong> amb menús desplegables (no cal baixar tota la pàgina)</li>
<li><strong>Sidebar amb totes les fitxes</strong> (visible a la dreta)</li>
<li><strong>Vista neta</strong> del document seleccionat</li>
<li><strong>Funciona offline</strong> (un cop carregada la primera vegada)</li>
</ul>
<h2 id="-manteniment">🔄 Manteniment</h2>
<p>Cada vegada que vulguis actualitzar el contingut:</p>
<pre><code>
cd ~/Desktop/hort-osona
python3 build_portal.py   # regenera l&#x27;index.html i copia assets PWA
./hort-sync.sh &quot;missatge&quot; # commit + push
</code></pre>
<p>En 30-60 segons, la versió nova és visible al mòbil (i a tot arreu).</p>
<p>Si vols, pots crear un àlies al terminal per fer-ho en una sola ordre:</p>
<pre><code>
# Afegeix això a ~/.zshrc:
alias hort-publish=&#x27;cd ~/Desktop/hort-osona &amp;&amp; python3 build_portal.py &amp;&amp; ./hort-sync.sh &quot;Actualitzar web&quot;&#x27;
</code></pre>
<p>Després:</p>
<pre><code>
hort-publish &quot;Afegida fitxa de carxofa&quot;
</code></pre>
<h2 id="-com-funciona-tècnicament">🛠️ Com funciona tècnicament</h2>
<ul>
<li><strong>GitHub Pages</strong> serveix l&#x27;<code>index.html</code> des de la branca <code>main</code> del repositori</li>
<li>L&#x27;<code>index.html</code> conté <strong>tots els documents incrustats</strong> (és un fitxer únic de 2,2 MB)</li>
<li>El <strong>service worker</strong> (<code>service-worker.js</code>) emmagatzema el portal a la memòria cau</li>
<li>El <strong>manifest</strong> (<code>manifest.json</code>) indica al mòbil com mostrar l&#x27;app</li>
<li>Les <strong>icones</strong> (<code>icon-192.png</code>, <code>icon-512.png</code>) són el que apareix a la pantalla d&#x27;inici</li>
</ul>
<h2 id="-resolució-de-problemes">🔧 Resolució de problemes</h2>
<h3 id="-la-url-no-carrega">❌ La URL no carrega</h3>
<ul>
<li>Comprova que el repo és <strong>públic</strong> (Settings → Danger Zone → Change repository visibility)</li>
<li>Comprova que GitHub Pages està activat (Settings → Pages)</li>
<li>Espera 5-10 minuts després d&#x27;activar (la primera vegada triga)</li>
</ul>
<h3 id="-quotafegir-a-la-pantalla-dx27iniciquot-no-apareix">❌ &quot;Afegir a la pantalla d&#x27;inici&quot; no apareix</h3>
<ul>
<li>A iOS: usa <strong>Safari</strong> (no Chrome ni altres navegadors)</li>
<li>A Android: usa <strong>Chrome</strong></li>
<li>Assegura&#x27;t que la URL comença per <code>https://</code> (no <code>http://</code>)</li>
</ul>
<h3 id="-lx27app-no-funciona-offline">❌ L&#x27;app no funciona offline</h3>
<ul>
<li>Primer obre l&#x27;app <strong>amb connexió</strong> perquè es descarregui</li>
<li>Després ja funciona offline</li>
</ul>
<h3 id="-no-es-veuen-els-canvis-nous">❌ No es veuen els canvis nous</h3>
<ul>
<li>Tanca l&#x27;app del tot (al mòbil)</li>
<li>Reobre-la</li>
<li>O bé: Configuració → Safari → Avançat → Dades de llocs web → cerca &quot;BernatMora&quot; → Esborra</li>
</ul>
<h2 id="-què-no-funciona-de-moment">📊 Què NO funciona (de moment)</h2>
<ul>
<li><strong>El xat amb IA</strong> (Ollama) — corre al teu Mac i el mòbil no hi pot accedir</li>
<li>Solució: configurar Tailscale o túnel (veure <code>hort-osona-iot/CHAT-SETUP.md</code>)</li>
<li><strong>Sensors IoT</strong> (humitat, temperatura) — també al Mac o Raspberry Pi</li>
<li><strong>Sincronització Git</strong> — és eina de desenvolupador, no per usuaris finals</li>
</ul>
<h2 id="-idees-per-millorar">💡 Idees per millorar</h2>
<ul>
<li>[ ] Afegir <strong>botó per afegir notes</strong> (localStorage al mòbil)</li>
<li>[ ] Afegir <strong>checklist diària</strong> amb sincronització</li>
<li>[ ] Activar <strong>Tailscale</strong> per accedir al xat des del mòbil</li>
<li>[ ] <strong>Notificacions push</strong> quan hi ha tasques importants</li>
<li>[ ] <strong>Mode fosc</strong> per llegir a la nit a l&#x27;hort 🌙</li>
</ul>
<h2 id="-ajuda">📞 Ajuda</h2>
<p>Si alguna cosa no funciona:</p>
<ol>
<li>Comprova que el portal es genera bé: <code>python3 build_portal.py</code></li>
<li>Comprova els assets PWA: <code>ls -la manifest.json icon-*.png service-worker.js</code></li>
<li>Comprova que el push ha funcionat: <code>git log --oneline -3</code></li>
</ul>