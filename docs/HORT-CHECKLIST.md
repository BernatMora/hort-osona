<h1 id="-hort-checklist-generador-de-checklist-mensual-de-lx27hort">🌱 HORT-CHECKLIST — Generador de checklist mensual de l&#x27;hort</h1>
<p>Eina que genera automàticament cada mes:</p>
<ul>
<li>Una <strong>checklist de tasques</strong> de l&#x27;hort adaptades a Osona</li>
<li>El <strong>calendari lunar</strong> del mes amb recomanacions biodinàmiques</li>
<li>Un <strong>prompt enriquit</strong> per Open WebUI amb tot el context</li>
<li>Una <strong>pàgina web</strong> integrada al lloc unificat (<code>#checklist</code>)</li>
</ul>
<h2 id="ús-ràpid">Ús ràpid</h2>
<pre><code>
# Veure la checklist del mes actual
python hort-checklist.py

# Veure un mes concret
python hort-checklist.py --date 2026-07

# Generar el fitxer plans-mensuals/AAAA-MM-mes.md
python hort-checklist.py --write

# Imprimir el prompt per Open WebUI
python hort-checklist.py --prompt

# Sortida JSON estructurada
python hort-checklist.py --json

# Consultar la fase lunar d&#x27;una data concreta
python hort-checklist.py --print-fase 2026-08-15
</code></pre>
<h2 id="què-inclou-la-checklist">Què inclou la checklist</h2>
<ol>
<li><strong>Context climàtic</strong> del mes (per Osona, no genèric)</li>
<li><strong>Calendari lunar</strong> amb totes les setmanes i fases amb recomanacions</li>
<li><strong>Tasques organitzades per categoria</strong>:</li>
<li>🌱 Sembra</li>
<li>🌿 Trasplantament</li>
<li>🛠️ Conreu</li>
<li>🐞 Tractaments</li>
<li>🧺 Collita</li>
<li>📋 Planificació</li>
<li>👀 Observació</li>
<li>Cada tasca té <strong>prioritat</strong> (1-5) i <strong>descripció</strong></li>
<li><strong>Dates clau</strong> a Osona (Sant Jordi, Mare de Déu d&#x27;Agost, etc.)</li>
</ul>
<h2 id="integració-amb-el-lloc-web">Integració amb el lloc web</h2>
<p>Cada vegada que executes <code>python site/build.py</code>:</p>
<ol>
<li>El <code>build.py</code> importa <code>hort-checklist.py</code></li>
<li>Genera les dades JSON del mes actual</li>
<li>Les desa a <code>site/checklist-data.json</code></li>
<li>Les incrusta dins l&#x27;HTML generat</li>
<li>La pàgina d&#x27;inici mostra un <strong>giny</strong> amb:</li>
<li>Mes actual + fase lunar de la setmana en curs</li>
<li>Top tasca prioritària</li>
<li>Strip de les 4 primeres setmanes amb fases</li>
<li>La pàgina <code>#checklist</code> (o el botó &quot;Obrir checklist completa&quot;) mostra:</li>
<li>Totes les tasques amb checkboxes persistents (localStorage)</li>
<li>Taula del calendari lunar</li>
<li>Dates clau d&#x27;Osona</li>
<li>Prompt per copiar a Open WebUI</li>
</ul>
<h2 id="algorisme-de-la-fase-lunar">Algorisme de la fase lunar</h2>
<p>Usa l&#x27;algorisme de cicles sinòdics amb referència a la lluna nova del</p>
<p><strong>6 de gener de 2000 18:14 UTC</strong> (verificable). Període sinòdic: 29.530588 dies.</p>
<p>Precisió: ±1 dia (suficient per planificar tasques agrícoles).</p>
<pre><code>
from hort-checklist import fase_lunar
from datetime import date
nom, eti, emoji, desc = fase_lunar(date(2026, 6, 15))
# (&#x27;nova&#x27;, &#x27;Lluna nova&#x27;, &#x27;🌑&#x27;, &#x27;Repòs, planificar, netejar eines...&#x27;)
</code></pre>
<h2 id="afegir-o-modificar-tasques">Afegir o modificar tasques</h2>
<p>Edita la llista <code>TASQUES</code> al principi de <code>hort-checklist.py</code>. Cada tasca té:</p>
<pre><code>
{
    &quot;mesos&quot;: [6],                  # llista de mesos (1-12)
    &quot;cat&quot;: &quot;conreu&quot;,               # categoria (veure clau a dalt)
    &quot;prio&quot;: 5,                     # prioritat 1-5
    &quot;titol&quot;: &quot;Mulching a tot l&#x27;hort (URGENT)&quot;,
    &quot;desc&quot;: &quot;5-10 cm de palla, gespa seca o fulles...&quot;
}
</code></pre>
<h2 id="notes">Notes</h2>
<ul>
<li>L&#x27;eina <strong>no requereix cap connexió a Internet</strong> (les dades estan totes</li>
</ul>
<p>hard-coded al fitxer Python).</p>
<ul>
<li>Si vols un altre mes del qual no hi ha dades, l&#x27;afegixes a la llista</li>
</ul>
<p><code>TASQUES</code> i regeneres.</p>
<ul>
<li>Les fases lunars serveixen com a <strong>guia orientativa</strong> — a Osona, la</li>
</ul>
<p>temperatura i les gelades manen sempre.</p>
<h2 id="exemples">Exemples</h2>
<pre><code>
# Preparar el mes vinent
python hort-checklist.py --date 2026-07 --write

# Veure quin dia és bona per sembrar (prop de lluna nova o minvant)
python hort-checklist.py --print-fase 2026-09-15

# Generar el prompt per a una pregunta concreta a Open WebUI
python hort-checklist.py --prompt | pbcopy   # Mac
python hort-checklist.py --prompt | clip     # Windows
</code></pre>