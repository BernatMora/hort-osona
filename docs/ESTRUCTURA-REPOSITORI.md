<h1 id="fonts-i-artefactes-generats">Fonts i artefactes generats</h1>
<p>Per conservar les URLs públiques actuals, els fitxers existents continuen al seu lloc. La regla a partir d’ara és:</p>
<ul>
<li>Els <code>.md</code> són la <strong>font editable</strong>.</li>
<li><code>build_portal_v2.py</code> i els scripts de generació són les <strong>eines</strong>.</li>
<li><code>index.html</code>, <code>docs/</code>, <code>search_index.json</code>, els <code><em>-imprimible.html</code> i els <code></em>-2026.pdf</code> són <strong>artefactes generats</strong>.</li>
<li>Els PDF nous de gran mida s’han de publicar preferentment com a GitHub Release i no duplicar-se sense necessitat.</li>
</ul>
<p>Abans de publicar: regenera, executa <code>python validate_portal.py</code> i comprova que el diff només contingui canvis esperats.</p>