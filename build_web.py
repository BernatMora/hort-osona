#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_web.py — Genera TOTA la web d'hort-osona, amb el que cal dia a dia a primera plana.

Objectiu: qui entra ha de veure d'un cop d'ull, segons el mes en curs,
QUE POT PLANTAR i AMB QUE HO POT ASSOCIAR. La resta del fons queda a un clic.

Genera (a la carpeta de sortida):
  index.html            portada: mes + que plantar ara + al costat de que
  associacions.html     totes les associacions, bancals i contradiccions
  calendari.html        els 12 mesos, cultiu a cultiu
  cultius.html          graella de les 37 fitxes
  tot.html              index complet del fons (per categories)
  cultiu/<slug>.html    una pagina per cultiu
  docs/<path>.html      una pagina per document (guies, plans, PDFs)
  img/*.svg             les il.lustracions dels cultius
  estil.css             estil compartit

Reutilitza el conversor markdown->HTML de build_portal_v2.py (codi provat).

Ús:  python3 build_web.py [--out DIR]
"""
import html
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import hort_data as hd

BASE = Path(__file__).resolve().parent
OUT = BASE / "preview"
MESOS_CA = ["gener", "febrer", "març", "abril", "maig", "juny",
            "juliol", "agost", "setembre", "octubre", "novembre", "desembre"]

# ─────────────────────────── ESTIL ───────────────────────────
CSS = """
:root{
  --bg:#F5EBD8; --paper:#FFFCF3; --ink:#2D2A22; --ink2:#6E6A5E; --oliva:#3D4A2A;
  --verd:#4E7A3A; --blau:#3E6E8E; --taronja:#C4762A; --morat:#7A5A8E;
  --terros:#9C5A34; --vermell:#B4442E; --linia:rgba(61,74,42,.14);
  --ombra:0 1px 2px rgba(45,42,34,.05), 0 10px 28px -16px rgba(45,42,34,.35);
  --radi:16px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-size:16px;line-height:1.6;
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
h1,h2,h3,h4{font-family:Georgia,"Times New Roman",serif;line-height:1.15;margin:0 0 .35em;font-weight:600}
h1{font-size:clamp(28px,6vw,44px);letter-spacing:-.01em}
h2{font-size:clamp(20px,3.4vw,27px)}
h3{font-size:18px}
p{margin:0 0 .8em}
a{color:var(--oliva);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1080px;margin:0 auto;padding:0 18px 96px}
header.top{background:var(--oliva);color:var(--paper);position:sticky;top:0;z-index:20;
  box-shadow:0 2px 10px rgba(0,0,0,.12)}
header.top .wrap{display:flex;align-items:center;gap:12px;padding:12px 18px;flex-wrap:wrap}
header.top a.marca{color:var(--paper);font-family:Georgia,serif;font-size:20px;font-weight:600}
header.top nav{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap}
header.top nav a{color:var(--paper);opacity:.85;padding:7px 12px;border-radius:999px;font-size:14.5px}
header.top nav a:hover,header.top nav a[aria-current]{background:rgba(255,252,243,.16);opacity:1;text-decoration:none}
.seccio{margin:34px 0 0}
.seccio>h2{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.seccio .sub{color:var(--ink2);font-size:15px;margin:-2px 0 16px}
.graella{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.graella.estreta{grid-template-columns:repeat(auto-fit,minmax(190px,1fr))}
.targeta{background:var(--paper);border-radius:var(--radi);box-shadow:var(--ombra);padding:18px 18px 16px;border:1px solid var(--linia)}
a.targeta{display:block;color:inherit}
a.targeta:hover{text-decoration:none;transform:translateY(-2px);transition:.15s}
.hero{margin-top:22px;background:var(--paper);border-radius:22px;box-shadow:var(--ombra);
  border:1px solid var(--linia);overflow:hidden}
.hero .cos{padding:26px 24px 22px;display:grid;gap:20px;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr)}
@media(max-width:760px){.hero .cos{grid-template-columns:1fr;padding:20px 18px}}
.hero .eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:12.5px;color:var(--ink2);font-weight:600}
.hero h1{margin:.1em 0 .15em}
.hero .clima{font-size:17px;color:var(--ink2);max-width:52ch}
.hero .dades{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.pill{background:var(--bg);border:1px solid var(--linia);border-radius:999px;padding:6px 13px;font-size:14px}
.pill.avis{background:#FBEDE7;border-color:#E8C9BB;color:#8C3A22}
.hero .accions{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.boto{display:inline-flex;align-items:center;gap:8px;background:var(--oliva);color:var(--paper);
  padding:13px 20px;border-radius:999px;font-weight:600;font-size:16px;border:0;cursor:pointer}
.boto:hover{text-decoration:none;background:#2F3A21}
.boto.buit{background:transparent;color:var(--oliva);border:1.5px solid var(--oliva)}
.ara{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.ara .col{border-radius:var(--radi);padding:14px 15px 10px;background:var(--paper);
  box-shadow:var(--ombra);border-top:5px solid var(--accent,var(--verd))}
.ara .col h3{display:flex;align-items:center;gap:8px;font-size:17px;margin-bottom:8px}
.ara .col .quants{font-size:12.5px;color:var(--ink2);font-weight:400;font-family:inherit}
.chips{display:flex;flex-wrap:wrap;gap:7px}
.chip{display:inline-flex;align-items:center;gap:6px;background:var(--bg);border:1px solid var(--linia);
  border-radius:999px;padding:5px 11px;font-size:14.5px;color:var(--ink)}
.chip:hover{border-color:var(--oliva);text-decoration:none}
.chip img{width:20px;height:20px;object-fit:contain}
.chip.bona{background:#EDF4E6;border-color:#C9DDB6}
.chip.dolenta{background:#FBEDE7;border-color:#EED0C2}
.chip.discutit{background:#FBF3DF;border-color:#E4CE9A;color:#7A5B १८}
.chip.discutit{background:#FBF3DF;border-color:#E4CE9A;color:#7A5B18}
/* CERCA GLOBAL */
.cerca-global{background:var(--paper);border:1px solid var(--linia);border-radius:var(--radi);
  box-shadow:var(--ombra);padding:14px 15px;margin-top:18px}
.cerca-global label{display:block;font-size:14.5px;color:var(--ink2);margin-bottom:8px}
.cerca-global input{width:100%;padding:15px 16px;border-radius:999px;border:1.5px solid var(--linia);
  background:#FFFDF7;font-size:17px;color:var(--ink)}
.cerca-global input:focus{outline:2px solid var(--oliva);outline-offset:1px}
#resultats{margin-top:12px}
#resultats .g{font-size:12.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--ink2);margin:10px 0 4px}
#resultats a{display:block;padding:11px 13px;border-radius:11px;background:var(--bg);margin-bottom:6px;
  font-size:16px;color:var(--ink)}
#resultats a:hover{background:#EFE6D2;text-decoration:none}
#resultats a span{color:var(--ink2);font-size:13.5px}
.buidet{color:var(--ink2);font-size:14.5px;font-style:italic}
.bancal{background:var(--paper);border-radius:var(--radi);box-shadow:var(--ombra);padding:16px;border-left:5px solid var(--verd)}
.bancal h3{margin-bottom:4px}
.bancal .com{color:var(--ink2);font-size:14.5px;margin-top:6px}
.taula{width:100%;border-collapse:collapse;background:var(--paper);border-radius:var(--radi);overflow:hidden;box-shadow:var(--ombra);font-size:15px}
.taula th,.taula td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--linia);vertical-align:top}
.taula th{background:#EDE6D3;font-family:Georgia,serif;font-size:15px}
.taula tr:last-child td{border-bottom:0}
.ok{color:var(--verd);font-weight:600}
.no{color:var(--vermell);font-weight:600}
.veins{background:var(--paper);border-radius:var(--radi);box-shadow:var(--ombra);padding:14px 15px;border:1px solid var(--linia)}
.veins .titol{display:flex;align-items:center;gap:9px;font-family:Georgia,serif;font-size:17px;margin-bottom:9px}
.veins .titol img{width:26px;height:26px;object-fit:contain}
.veins .fila{display:flex;gap:8px;align-items:flex-start;margin-bottom:7px}
.veins .et{font-size:13px;color:var(--ink2);flex:0 0 54px;padding-top:4px}
.cultiu-card{display:flex;gap:12px;align-items:center;background:var(--paper);border-radius:14px;
  padding:12px 14px;box-shadow:var(--ombra);border:1px solid var(--linia)}
.cultiu-card img{width:44px;height:44px;flex:0 0 44px;object-fit:contain}
.cultiu-card .n{font-family:Georgia,serif;font-size:17px}
.cultiu-card .f{color:var(--ink2);font-size:13px}
.dades-rapides{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));margin:0 0 8px}
.dada{background:var(--paper);border:1px solid var(--linia);border-radius:12px;padding:10px 12px}
.dada .k{font-size:12px;text-transform:uppercase;letter-spacing:.08em;color:var(--ink2)}
.dada .v{font-size:15.5px}
.cal{overflow-x:auto;background:var(--paper);border-radius:var(--radi);box-shadow:var(--ombra);padding:6px}
.cal table{border-collapse:collapse;font-size:12.5px;min-width:720px}
.cal th,.cal td{padding:3px 2px;text-align:center}
.cal th.mes{writing-mode:vertical-rl;transform:rotate(180deg);font-weight:600;color:var(--ink2);height:52px}
.cal td.nom{text-align:left;white-space:nowrap;padding-right:10px;font-size:14px}
.cal .c{width:20px;height:20px;border-radius:5px;display:block;margin:auto;font-size:11px;
  line-height:20px;font-weight:700;color:#fff}
.c-plantar{background:var(--verd)}
.c-trasplantar{background:var(--blau)}
.c-collir{background:var(--taronja)}
.llista-tasques{list-style:none;padding:0;margin:0}
.llista-tasques li{background:var(--paper);border:1px solid var(--linia);border-radius:12px;
  padding:12px 14px;margin-bottom:9px;box-shadow:var(--ombra)}
.llista-tasques .t{font-weight:600}
.llista-tasques .d{color:var(--ink2);font-size:14.5px}
.prio{display:inline-block;font-size:11.5px;text-transform:uppercase;letter-spacing:.08em;
  color:var(--paper);background:var(--morat);border-radius:6px;padding:2px 7px;margin-right:8px}
footer.peu{margin-top:46px;padding-top:20px;border-top:1px solid var(--linia);color:var(--ink2);font-size:14.5px}
nav.bottom{position:fixed;bottom:0;left:0;right:0;display:flex;background:var(--paper);
  border-top:1px solid var(--linia);z-index:30;box-shadow:0 -4px 18px rgba(0,0,0,.06)}
nav.bottom a{flex:1;text-align:center;padding:9px 4px 8px;font-size:12px;color:var(--ink2)}
nav.bottom a .i{display:block;font-size:19px;line-height:1.2}
nav.bottom a[aria-current]{color:var(--oliva);font-weight:600}
@media(min-width:820px){nav.bottom{display:none}}
.cercador{display:flex;gap:8px;margin:0 0 14px}
.cercador input{flex:1;padding:13px 15px;border-radius:999px;border:1.5px solid var(--linia);
  background:var(--paper);font-size:16px;color:var(--ink)}
.cercador input:focus{outline:2px solid var(--oliva);outline-offset:1px}


/* ── MOBIL PRIMER: es mira al hort, a plena llum, amb una ma ── */
body{font-size:17px;line-height:1.65}
h1{font-size:clamp(30px,8vw,46px)}
h2{font-size:clamp(21px,5.5vw,28px)}
.chip{font-size:16px;padding:9px 14px;min-height:40px;background:#FFFDF7}
.chip.bona{background:#E9F2E0}
.chip.dolenta{background:#FAE9E1}
.boto{padding:15px 22px;font-size:17px;width:100%;justify-content:center}
@media(min-width:640px){.boto{width:auto}}
nav.bottom a{padding:10px 2px 9px;font-size:11.5px;min-height:56px}
nav.bottom a .i{font-size:21px}
header.top nav a{padding:9px 13px;font-size:15.5px}
.ara .col .chip{font-size:16.5px;padding:10px 14px}
.ara .col .chip img{width:28px;height:28px}
.veins .et{flex:0 0 58px;font-size:14px}
.veins .titol{font-size:18.5px}
.hero .accions{gap:10px}
.hero .accions .boto{flex:1 1 100%}
.pill{font-size:15px;padding:8px 14px}
.llista-tasques li{padding:14px 15px}
.llista-tasques input[type=checkbox]{width:26px;height:26px;flex:0 0 26px}
.dada{padding:12px 14px}
.dada .v{font-size:16.5px}
.cultiu-card img{width:84px;height:84px;flex:0 0 84px}
.cal .c{width:22px;height:22px;line-height:22px}
.cal table{font-size:13.5px;min-width:660px}
/* instal.lar a la pantalla d'inici */
.instal{display:flex;gap:10px;align-items:center;background:#FBF6E7;border:1px solid #E9DCB4;
  border-radius:14px;padding:12px 14px;font-size:15px;margin-top:14px}
.instal button{margin-left:auto;background:var(--oliva);color:var(--paper);border:0;
  border-radius:999px;padding:9px 14px;font-size:14.5px;cursor:pointer}
.off{position:fixed;left:12px;right:12px;bottom:70px;z-index:40;background:#8C3A22;color:#fff;
  border-radius:12px;padding:10px 14px;font-size:14.5px;display:none}
.off.visible{display:block}

/* ── VISUAL: hero estacional, tira de l'any, lluna, diagrama, checklist ── */
.hero{border:0;position:relative;background:linear-gradient(135deg,#FFFCF3 0%,#F3EAD3 55%,#E7DCC0 100%)}
.hero.estiu{background:linear-gradient(135deg,#FFFCF3 0%,#FBF0D2 55%,#F6E2B8 100%)}
.hero.tardor{background:linear-gradient(135deg,#FFFCF3 0%,#F6E7D4 55%,#EED6BC 100%)}
.hero.hivern{background:linear-gradient(135deg,#FFFCF3 0%,#EDEFE6 55%,#DDE4D6 100%)}
.hero.primavera{background:linear-gradient(135deg,#FFFCF3 0%,#EFF4E3 55%,#DDEBC9 100%)}
.hero .mes-gran{font-family:Georgia,serif;font-size:clamp(40px,11vw,86px);line-height:.95;
  letter-spacing:-.02em;margin:.02em 0 .1em;color:var(--oliva)}
.hero .any{font-size:clamp(16px,3vw,22px);color:var(--ink2);font-family:Georgia,serif}
.lluna{display:flex;gap:12px;align-items:center;background:rgba(255,252,243,.75);
  border:1px solid var(--linia);border-radius:14px;padding:10px 14px;margin-top:14px}
.lluna .f{font-size:30px;line-height:1}
.lluna .t{font-size:14.5px;color:var(--ink2)}
.lluna .t strong{color:var(--ink);display:block;font-size:15.5px}
.tira-any{display:flex;gap:4px;margin-top:16px}
.tira-any span{flex:1;text-align:center;font-size:11.5px;padding:5px 0;border-radius:7px;
  background:rgba(255,252,243,.6);color:var(--ink2);border:1px solid transparent}
.tira-any span.ara{background:var(--oliva);color:var(--paper);font-weight:700}
.tira-mes{display:flex;gap:6px;overflow-x:auto;padding:10px 2px 14px;margin-top:16px;
  scroll-snap-type:x proximity}
.tira-mes .dia{flex:0 0 auto;width:52px;text-align:center;background:rgba(255,252,243,.8);
  border:1px solid var(--linia);border-radius:12px;padding:7px 0 6px;scroll-snap-align:center}
.tira-mes .dia.avui{background:var(--oliva);border-color:var(--oliva)}
.tira-mes .dia.avui .n,.tira-mes .dia.avui .l{color:var(--paper)}
.tira-mes .dia.clau{border-color:var(--vermell);border-width:1.5px}
.tira-mes .n{font-size:13px;font-weight:700}
.tira-mes .l{font-size:16px;line-height:1.1}
.tira-mes .q{font-size:9.5px;color:var(--ink2);text-transform:uppercase;letter-spacing:.04em}
.radial{width:100%;height:auto;display:block}
.radial text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif}
.ara .col{display:flex;flex-direction:column}
.ara .col .chips{gap:8px}
.ara .col .chip{font-size:15px;padding:7px 13px}
.ara .col .chip img{width:26px;height:26px}
.cultiu-card{flex-direction:column;text-align:center;gap:8px;padding:16px 10px 13px}
.cultiu-card img{width:76px;height:76px;flex:0 0 76px}
.llista-tasques li{display:flex;gap:11px;align-items:flex-start}
.llista-tasques input[type=checkbox]{width:22px;height:22px;flex:0 0 22px;margin-top:2px;accent-color:var(--verd)}
.llista-tasques li.fet{opacity:.55}
.llista-tasques li.fet .t{text-decoration:line-through}
.comp{display:inline-flex;align-items:center;gap:7px;background:var(--paper);border:1px solid var(--linia);
  border-radius:999px;padding:9px 15px;font-size:14.5px;color:var(--ink);cursor:pointer}
.comp:hover{border-color:var(--oliva);text-decoration:none}
@media print{
  .hero,.targeta,.bancal,.veins,.llista-tasques li{box-shadow:none;border:1px solid #ccc}
  .tira-mes .dia{width:44px}
  a[href]::after{content:""}
}
@media print{header.top,nav.bottom,.boto{display:none}body{background:#fff}}
.doc{background:var(--paper);border-radius:var(--radi);box-shadow:var(--ombra);padding:26px 26px 18px;border:1px solid var(--linia)}
.doc h2{font-size:24px;margin-top:1.4em;padding-top:.5em;border-top:1px solid var(--linia)}
.doc h2:first-child{margin-top:0;border-top:0;padding-top:0}
.doc h3{font-size:18.5px;margin-top:1.2em;color:var(--verd)}
.doc table{width:100%;border-collapse:collapse;margin:1em 0;font-size:14.5px;display:block;overflow-x:auto}
.doc th,.doc td{border:1px solid var(--linia);padding:7px 9px;text-align:left}
.doc th{background:#EDE6D3}
.doc code{background:#EFE8D6;padding:1px 5px;border-radius:5px;font-size:14px}
.doc pre{background:#2D2A22;color:#F5EBD8;padding:14px;border-radius:10px;overflow-x:auto}
.doc pre code{background:none;color:inherit}
.doc blockquote{margin:1em 0;padding:10px 16px;border-left:4px solid var(--oliva);background:#F2EBD9;border-radius:0 10px 10px 0}
.doc img{max-width:100%}
.doc ul,.doc ol{padding-left:22px}
.doc li{margin:.25em 0}
.torna{display:inline-block;margin-bottom:14px;font-size:14.5px}
.llista-docs{list-style:none;padding:0;margin:0;columns:2;column-gap:26px}
@media(max-width:700px){.llista-docs{columns:1}}
.llista-docs li{break-inside:avoid;margin-bottom:6px;font-size:15.5px}
.grup-docs{margin-bottom:22px}
.grup-docs h3{color:var(--oliva);margin-bottom:6px}
"""

NAV = [("index.html", "Ara", "🌱"), ("calendari.html", "Calendari", "📅"),
       ("associacions.html", "Al costat de què", "🤝"), ("cultius.html", "Cultius", "🥬"),
       ("tot.html", "Tot el fons", "📚")]


def esc(t) -> str:
    return html.escape(str(t if t is not None else ""))


def cap(titol: str, actiu: str = "", desc: str = "", pref: str = "") -> str:
    nav = "".join(
        f'<a href="{pref}{u}"{" aria-current=\"page\"" if u == actiu else ""}>{i} {esc(t)}</a>'
        for u, t, i in NAV)
    return f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(titol)} · Hort Osona</title>
<meta name="description" content="{esc(desc or 'Hort ecològic a Osona: què plantar aquest mes, associacions de cultius i guies pràctiques.')}">
<meta name="theme-color" content="#3D4A2A">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Hort Osona">
<meta name="mobile-web-app-capable" content="yes">
<link rel="manifest" href="{pref}manifest.json">
<link rel="apple-touch-icon" href="{pref}icon.svg">
<link rel="stylesheet" href="{pref}estil.css">
<link rel="icon" href="{pref}icon.svg">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="marca" href="{pref}index.html">🥬 Hort Osona</a>
  <nav>{nav}</nav>
</div></header>
<main class="wrap">
"""


def peu(pref: str = "") -> str:
    any_ = datetime.now().year
    bottom = "".join(
        f'<a href="{pref}{u}"><span class="i">{i}</span>{esc(t)}</a>' for u, t, i in NAV)
    return f"""</main>
<nav class="bottom">{bottom}</nav>
<footer class="peu"><div class="wrap">
  <p><strong>Hort Osona</strong> · horticultura ecològica, plantes medicinals i conserves adaptades a Osona.
  Contingut fet a partir de l'experiència al propi hort · {any_}.</p>
  <p><a href="{pref}tot.html">Tot el fons</a> ·
     <a href="{pref}associacions.html">Associacions</a> ·
     <a href="{pref}calendari.html">Calendari</a> ·
     <a href="{pref}cultius.html">Fitxes de cultiu</a></p>
  <p class="buidet">Aquesta web no substitueix el que veus al tros: la temperatura i les gelades manen sempre.</p>
</div></footer>
<div class="off" id="off">📴 Sense connexió — estas veient la copia desada al mòbil.</div>
<script>
// Service worker: la web funciona sense cobertura al tros.
if('serviceWorker' in navigator){{navigator.serviceWorker.register('{pref}sw.js').catch(()=>{{}});}}
// Avis si es queda sense xarxa.
function estatXarxa(){{const o=document.getElementById('off');
  if(o)o.classList.toggle('visible',!navigator.onLine);}}
addEventListener('online',estatXarxa);addEventListener('offline',estatXarxa);estatXarxa();
</script>
</body></html>"""


def chips_cultius(noms, tipus="neutre") -> str:
    out = []
    for nom in noms:
        e = hd.enllac_cultiu(nom)
        icona = f'<img src="img/{esc(e["svg"])}" alt="" loading="lazy">' if e.get("svg") else ""
        desti = f'cultiu/{esc(e["slug"])}.html' if e["tipus"] == "fitxa" else (
            f'docs/{esc(e["doc"])[:-3]}.html' if e["tipus"] == "doc" else "")
        cls = f"chip {tipus}" if tipus != "neutre" else "chip"
        if desti:
            out.append(f'<a class="{cls}" href="{desti}">{icona}{esc(nom)}</a>')
        else:
            out.append(f'<span class="{cls}">{icona}{esc(nom)}</span>')
    return "".join(out)


def targeta_ara(titol, icona, noms, accent, nota="") -> str:
    cos = chips_cultius(noms) if noms else f'<p class="buidet">{esc(nota or "Cap cultiu aquest mes.")}</p>'
    return f"""<div class="col" style="--accent:{accent}">
  <h3>{icona} {esc(titol)} <span class="quants">{len(noms)}</span></h3>
  <div class="chips">{cos}</div>
</div>"""


def associacions_del_mes(noms) -> list:
    """Per a cada cultiu que es pot posar ara: els seus veins bons i dolents."""
    gen = hd.associacions()
    fitxa_assoc = hd.associacions_fitxes()
    files = []
    for nom in noms:
        e = hd.enllac_cultiu(nom)
        bons, dolents = [], []
        if e["slug"] and e["slug"] in fitxa_assoc:
            bons = fitxa_assoc[e["slug"]]["bons"]
            dolents = fitxa_assoc[e["slug"]]["dolents"]
        if not bons and not dolents:
            for k, v in gen.items():
                if hd.normalitza(k) == hd.normalitza(nom) or \
                   hd.normalitza(nom).startswith(hd.normalitza(k)[:5]):
                    bons, dolents = v["bons"], v["dolents"]
                    break
        disc = list(dict.fromkeys(fitxa_assoc.get(e["slug"], {}).get("discutits", [])))[:4] \
            if e["slug"] in fitxa_assoc else []
        b = list(dict.fromkeys(bons))[:7]
        d = list(dict.fromkeys(dolents))[:6]
        if b or d or disc:
            files.append({"nom": nom, "enllac": e, "bons": b, "dolents": d, "discutits": disc})
    return files


def bloc_veins(files) -> str:
    out = []
    for f in files:
        icona = f'<img src="img/{esc(f["enllac"]["svg"])}" alt="" loading="lazy">' if f["enllac"].get("svg") else ""
        titol = (f'<a href="cultiu/{esc(f["enllac"]["slug"])}.html">{esc(f["nom"])}</a>'
                 if f["enllac"]["tipus"] == "fitxa" else esc(f["nom"]))
        bones = "".join(f'<span class="chip bona">{esc(x)}</span>' for x in f["bons"]) or '<span class="buidet">—</span>'
        dolentes = "".join(f'<span class="chip dolenta">{esc(x)}</span>' for x in f["dolents"]) or '<span class="buidet">—</span>'
        fila_disc = ""
        if f.get("discutits"):
            ch = "".join(f'<span class="chip discutit" title="A la documentacio surt com a bo i com a dolent; millor no arriscar-se">{esc(x)}</span>'
                         for x in f["discutits"])
            fila_disc = f'<div class="fila"><span class="et">⚠️ Discutit</span><span class="chips">{ch}</span></div>'
        out.append(f"""<div class="veins">
  <div class="titol">{icona}{titol}</div>
  <div class="fila"><span class="et">✅ Amb</span><span class="chips">{bones}</span></div>
  <div class="fila"><span class="et">❌ Lluny</span><span class="chips">{dolentes}</span></div>
  {fila_disc}
</div>""")
    return "".join(out)


def receptes_bancals():
    return [
        {"titol": "El bancal antimosca", "cultius": ["Pastanaga", "Ceba", "Enciam"],
         "com": "La ceba (o el porro) confon la mosca de la pastanaga: la fitxa diu que redueix "
                "el 60-80 % dels danys. L'enciam aprofita els buits i no competeix."},
        {"titol": "Amanides de tardor", "cultius": ["Enciam", "Escarola", "Canonges", "Rúcula"],
         "com": "Es cullen del mateix bancal i al mateix ritme. Un rave enmig fa de marcador de "
                "fileres i madura en 30-70 dies."},
        {"titol": "El bancal de cols", "cultius": ["Col", "Api", "Remolatxa", "Espinac"],
         "com": "L'api repeleix la papallona de la col; remolatxa i espinac omplen els espais. "
                "A les vores, una filera de rave com a planta trampa."},
        {"titol": "Lleguminoses que donen nitrogen", "cultius": ["Fava", "Espinac", "Pastanaga"],
         "com": "La fava fa ombra i fixa nitrogen; espinac i pastanaga ho aprofiten al costat. "
                "Aquí no hi posis ceba ni all: les inhibeixen."},
        {"titol": "Els marges aromàtics", "cultius": ["Julivert", "Cibulet", "Coriantre"],
         "com": "Vorejant els bancals: atrauen insectes beneficiosos. L'anet, millor lluny de les pastanagues."},
    ]


def comprova_bancals(bancals, gen, fit) -> list:
    problemes = []
    for b in bancals:
        for i, a in enumerate(b["cultius"]):
            for c in b["cultius"][i + 1:]:
                ka, kc = hd.normalitza(a), hd.normalitza(c)
                for k, v in gen.items():
                    nk = hd.normalitza(k)
                    if nk not in (ka, kc):
                        continue
                    altres = [hd.normalitza(x) for x in v["dolents"]]
                    if (nk == ka and kc in altres) or (nk == kc and ka in altres):
                        problemes.append(f"{b['titol']}: {a} + {c} (la taula general els fa dolents)")
                for slug, v in fit.items():
                    if slug not in (ka.replace(" ", "-"), kc.replace(" ", "-")):
                        continue
                    altres = [hd.normalitza(x) for x in v["dolents"]]
                    if (slug == kc.replace(" ", "-") and ka in altres) or \
                       (slug == ka.replace(" ", "-") and kc in altres):
                        problemes.append(f"{b['titol']}: {a} + {c} (la fitxa de {slug} els fa dolents)")
    return sorted(set(problemes))


# ─────────────────────────── PORTADA ───────────────────────────
INDEX_CERCA = []


def pagina_index() -> str:
    mes = datetime.now().month
    pm = hd.per_mes()[mes]
    info = hd.mes_info(mes)
    cultius = hd.fitxes()

    dara, vist = [], set()
    for clau in ("planter", "terra", "trasplantar"):
        for nom, _ in pm[clau]:
            k = hd.normalitza(nom)
            if k not in vist:
                vist.add(k)
                dara.append(nom)

    veins = bloc_veins(associacions_del_mes(dara))
    bancals = "".join(
        f'<div class="bancal"><h3>{esc(t["titol"])}</h3>'
        f'<div class="chips">{"".join(f"<span class=\'chip\'>{esc(c)}</span>" for c in t["cultius"])}</div>'
        f'<p class="com">{esc(t["com"])}</p></div>'
        for t in receptes_bancals())

    dates = "".join(f'<span class="pill avis">{esc(d["quan"])}: {esc(d["que"])}</span>'
                    for d in info["dates"])

    cultiu_cards = "".join(
        f'<a class="cultiu-card" href="cultiu/{esc(f["slug"])}.html">'
        + (f'<img src="img/{esc(f["svg"])}" alt="" loading="lazy">' if f["svg"] else "<span></span>")
        + f'<span><span class="n">{esc(f["nom"])}</span><br>'
          f'<span class="f">{esc(f["camps"].get("Família botànica", "")[:40])}</span></span></a>'
        for f in cultius)

    ara = "".join([
        targeta_ara("Sembrar a terra", "🌱", [n for n, _ in pm["terra"]], "var(--verd)"),
        targeta_ara("Sembrar en planter", "🪴", [n for n, _ in pm["planter"]], "var(--morat)",
                    "Al setembre es va més de sembra directa; el planter és per als mesos de fred."),
        targeta_ara("Trasplantar", "🌿", [n for n, _ in pm["trasplantar"]], "var(--blau)"),
        targeta_ara("Collir", "🧺", [n for n, _ in pm["collir"]], "var(--taronja)"),
    ])
    total = sum(len(v) for v in pm.values())

    return cap("Què plantar ara", "index.html",
               f"Què plantar a Osona al {MESOS_CA[mes-1]} i amb què associar-ho.") + f"""
<section class="hero {ESTACIO[mes]}">
  <div class="cos">
    <div>
      <div class="eyebrow">Aquest mes a Osona</div>
      <div class="mes-gran">{esc(MESOS_CA[mes - 1])}</div>
      <p class="clima">{esc(re.sub(r'\*\*', '', info["clima"]))}</p>
      <div class="dades">
        <span class="pill">{total} cultius en joc aquest mes</span>
        {setmana_en_curs()}
        {dates}
      </div>
      {bloc_lluna()}
      <div class="accions">
        <a class="boto" href="#plantar">🌱 Què puc plantar ara</a>
        <a class="boto buit" href="#associacions">🤝 Al costat de què</a>
      </div>
    </div>
    <div>
      <div class="eyebrow">Les tasques del mes</div>
      {llista_tasques(info["tasques"])}
      <p class="buidet" style="font-size:13.5px;margin-top:8px">Marca el que vagis fent: es desa al teu mòbil.</p>
    </div>
  </div>
  <div class="wrap" style="padding-bottom:6px">{tira_any(mes)}{tira_mes()}</div>
</section>

{caixa_cerca(index_cerca([])) if False else caixa_cerca(INDEX_CERCA)}

<section class="seccio" id="plantar">
  <h2>🌱 Què pots plantar aquest mes</h2>
  <p class="sub">Tret del calendari de sembra adaptat a Osona. Toca un cultiu i veus la seva fitxa.</p>
  <div class="ara">{ara}</div>
</section>

<section class="seccio" id="associacions">
  <h2>🤝 Al costat de què</h2>
  <p class="sub">Els veïns bons i dolents dels cultius que pots posar ara mateix.
     <a href="associacions.html">Veure la taula completa →</a></p>
  <div class="graella">{veins}</div>
  <div class="targeta" style="margin-top:18px">
    <h3>🔎 El diagrama del mes: {esc(dara[0]) if dara else ''}</h3>
    <p class="sub">El cultiu al mig, els bons veins a l'esquerra i els dolents a la dreta.</p>
    {diagrama_radial(dara[0] if dara else '', *(lambda f: (f['bons'], f['dolents']))(associacions_del_mes(dara)[0]) if dara and associacions_del_mes(dara) else ([], []))}
  </div>
  <h3 style="margin-top:26px">🧺 Receptes de bancal</h3>
  <p class="sub">Combinacions ja quadrades amb les seves associacions.</p>
  <div class="graella">{bancals}</div>
</section>

<section class="seccio">
  <h2>🥬 Tots els cultius</h2>
  <p class="sub">{len(cultius)} fitxes amb calendari, sembra, conreu, plagues i collita.</p>
  <div class="cercador"><input id="q" type="search" placeholder="Cerca un cultiu… (tomàquet, ceba, fava)" aria-label="Cerca un cultiu"></div>
  <div class="graella estreta" id="llista-cultius">{cultiu_cards}</div>
</section>

<div class="instal">📲 <span>Emporta-te-la al tros: afegeix-la a la pantalla d'inici i funciona sense cobertura.</span>
  <button type="button" id="btn-instal">Com es fa?</button></div>
<script>
document.getElementById('btn-instal').addEventListener('click',function(){{
  const es = /iPhone|iPad|iPod/.test(navigator.userAgent);
  alert(es ? 'Safari: toca Compartir ⬆️ i despres "Afegir a la pantalla d\'inici".'
           : 'Menú del navegador (⋮) i despres "Instal·la l\'aplicació" o "Afegeix a la pantalla d\'inici".');
}});
</script>

<section class="seccio">
  <h2>📚 La resta del fons</h2>
  <p class="sub">Guies, plans mensuals, plagues, conserves i remeieres.</p>
  <div class="graella estreta">
    <a class="targeta" href="docs/03-gestio-plagues.html">🐞 Plagues i malalties</a>
    <a class="targeta" href="docs/04-reg-fertilitzacio.html">💧 Reg i fertilització</a>
    <a class="targeta" href="docs/02-associacions-rotacions.html">🌿 Associacions i rotacions</a>
    <a class="targeta" href="docs/conserves.html">🥫 Conserves</a>
    <a class="targeta" href="docs/remeieres-guia-completa.html">🌿 Plantes remeieres</a>
    <a class="targeta" href="tot.html">📚 Índex complet</a>
  </div>
</section>
<script>
const q=document.getElementById('q');
if(q)q.addEventListener('input',()=>{{const t=q.value.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
document.querySelectorAll('#llista-cultius .cultiu-card').forEach(c=>{{const n=c.textContent.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');c.style.display=n.includes(t)?'':'none';}});}});
</script>
<script>
(function(){{
  const ul=document.getElementById('tasques'); if(!ul) return;
  ul.querySelectorAll('li').forEach(li=>{{
    const k='hort-'+li.dataset.k, c=li.querySelector('input');
    try{{ if(localStorage.getItem(k)==='1'){{c.checked=true;li.classList.add('fet');}} }}catch(e){{}}
    c.addEventListener('change',()=>{{
      li.classList.toggle('fet',c.checked);
      try{{ localStorage.setItem(k,c.checked?'1':'0'); }}catch(e){{}}
    }});
  }});
}})();
</script>
""" + peu()


# ─────────────────────────── ALTRES PAGINES ───────────────────────────
def pagina_associacions() -> str:
    gen = hd.associacions()
    fit = hd.associacions_fitxes()
    files = "".join(
        f'<tr><td><strong>{esc(k)}</strong></td>'
        f'<td class="ok">{esc(", ".join(dict.fromkeys(d["bons"])))}</td>'
        f'<td class="no">{esc(", ".join(dict.fromkeys(d["dolents"])))}</td></tr>'
        for k, d in sorted(gen.items()) if d["bons"] or d["dolents"])
    bh = "".join(
        f'<div class="bancal"><h3>{esc(t["titol"])}</h3>'
        f'<div class="chips">{"".join(f"<span class=\'chip\'>{esc(c)}</span>" for c in t["cultius"])}</div>'
        f'<p class="com">{esc(t["com"])}</p></div>' for t in receptes_bancals())
    ch = "".join(f'<li><strong>{esc(a)}</strong> ↔ <strong>{esc(b)}</strong>: {esc(m)}</li>'
                 for a, b, m in hd.conflictes())
    # parells que la documentacio dona com a bons i com a dolents alhora
    disc = []
    vist = set()
    for k, d in sorted(gen.items()):
        for x in d.get("discutits", []):
            disc.append((k, x))
    for slug, d in sorted(fit.items()):
        for x in d.get("discutits", []):
            clau = tuple(sorted([slug.lower(), hd.normalitza(x)]))
            if clau not in vist:
                vist.add(clau)
                disc.append((slug, x))
    dh = "".join(f'<li><strong>{esc(a)}</strong> + <strong>{esc(b)}</strong>: '
                 f'<span class="chip discutit">⚠️ discutit</span> '
                 f'<span class="buidet">surt com a bo en una font i com a dolent en una altra; el criteri '
                 f'de la web es deixar-los lluny</span></li>' for a, b in disc)
    return cap("Al costat de què", "associacions.html") + f"""
<section class="seccio">
  <h2>🤝 Què va al costat de què</h2>
  <p class="sub">Taula completa, tal com surt de les fitxes i de la guia d'associacions.</p>
  <div class="targeta" style="overflow-x:auto">
  <table class="taula"><thead><tr><th>Cultiu</th><th>✅ Bones associacions</th><th>❌ Incompatibles</th></tr></thead>
  <tbody>{files}</tbody></table>
  </div>
</section>
<section class="seccio">
  <h2>🧺 Receptes de bancal</h2>
  <div class="graella">{bh}</div>
</section>
<section class="seccio">
  <h2>⚠️ Parells discutits</h2>
  <p class="sub">La documentació els dona com a bons en una font i com a dolents en una altra.
     La web aplica un criteri prudent: <strong>no els posa junts</strong>. Si vols, es poden resoldre
     definitivament decidint quina font mana.</p>
  <div class="targeta"><ul>{dh or '<li>Cap parell discutit.</li>'}</ul></div>
</section>
<section class="seccio">
  <h2>🔍 Contradiccions que queden per resoldre</h2>
  <p class="sub">Creuaments que el generador detecta i que encara no estan coberts pel criteri prudent.</p>
  <div class="targeta"><ul>{ch or '<li>Cap contradicció detectada.</li>'}</ul></div>
</section>
""" + peu()


def pagina_cultiu(f) -> str:
    c = f["camps"]
    ordre = ["Família botànica", "Cicle", "Profunditat d'arrel", "Exigència de nutrients",
             "Necessitats hídriques", "Rusticitat a Osona", "pH ideal", "Marc de plantació",
             "Profunditat de sembra", "Dies des de sembra fins a collita", "Reg", "Conservació"]
    dades = "".join(
        f'<div class="dada"><div class="k">{esc(k)}</div><div class="v">{esc(c[k])}</div></div>'
        for k in ordre if c.get(k))
    bons = "".join(f'<span class="chip bona">{esc(x)}</span>' for x in dict.fromkeys(f["bons"]))
    dolents = "".join(f'<span class="chip dolenta">{esc(x)}</span>' for x in dict.fromkeys(f["dolents"]))
    discutits = "".join(f'<span class="chip discutit">{esc(x)}</span>'
                        for x in dict.fromkeys(f.get("discutits", [])))
    icona = f'<img src="../img/{esc(f["svg"])}" alt="" style="width:76px;height:76px">' if f["svg"] else ""
    return cap(f["nom"], pref="../") + f"""
<section class="seccio" style="margin-top:22px">
  <div class="targeta" style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">
    {icona}
    <div><h1 style="margin-bottom:2px">{esc(f["nom"])}</h1>
    <p class="buidet" style="margin:0">{esc(f["cientific"])}</p></div>
  </div>
</section>
<section class="seccio">
  <h2>Dades ràpides</h2>
  <div class="dades-rapides">{dades or '<p class="buidet">Sense dades a la fitxa.</p>'}</div>
</section>
<section class="seccio">
  <h2>🤝 Al costat de què</h2>
  <div class="targeta">{diagrama_radial(f["nom"], f["bons"], f["dolents"]) or '<p class="buidet">Sense associacions declarades a la fitxa.</p>'}</div>
  <div class="graella" style="margin-top:14px">
    <div class="targeta"><h3>✅ Bones</h3><div class="chips">{bons or '<span class="buidet">—</span>'}</div></div>
    <div class="targeta"><h3>❌ Dolentes</h3><div class="chips">{dolents or '<span class="buidet">—</span>'}</div></div>
  </div>
  {f'<div class="targeta" style="margin-top:14px"><h3>⚠️ Discutits a la documentació</h3><p class="sub" style="margin:0 0 8px">Surt com a bo en una font i com a dolent en una altra: el criteri és no arriscar-se i deixar-los lluny.</p><div class="chips">{discutits}</div></div>' if discutits else ''}
</section>
<section class="seccio">
  <h2>📖 Fitxa completa</h2>
  <p class="sub">Calendari a Osona, sembra, conreu, plagues, collita, varietats i conservació.</p>
  <p><a class="boto" href="../docs/07-fitxes-cultius/{esc(f["slug"])}.html">Obrir la fitxa sencera →</a></p>
</section>
""" + peu(pref="../")


def pagina_calendari() -> str:
    grups = hd.grups_calendari()
    capcalera = "".join(f'<th class="mes">{esc(m[:3])}</th>' for m in MESOS_CA)
    files = []
    for grup, cultius in grups.items():
        files.append(f'<tr><td class="nom" colspan="13" style="padding-top:12px;font-family:Georgia,serif;color:var(--ink2)">{esc(grup)}</td></tr>')
        for nom, cels in cultius:
            celes = []
            for cel in cels:
                if "S" in cel or "M" in cel:
                    cls = "c-plantar"
                elif "T" in cel:
                    cls = "c-trasplantar"
                elif "C" in cel:
                    cls = "c-collir"
                else:
                    celes.append("<td></td>")
                    continue
                lletra = "".join(sorted(set(re.sub(r"[^SMTC]", "", cel))))
                celes.append(f'<td><span class="c {cls}" title="{esc(cel)}">{esc(lletra[:2])}</span></td>')
            e = hd.enllac_cultiu(nom)
            nom_html = (f'<a href="cultiu/{esc(e["slug"])}.html">{esc(nom)}</a>'
                        if e["tipus"] == "fitxa" else esc(nom))
            files.append(f'<tr><td class="nom">{nom_html}</td>{"".join(celes)}</tr>')
    return cap("Calendari de sembra", "calendari.html") + f"""
<section class="seccio">
  <h2>📅 Tot l'any d'un cop d'ull</h2>
  <p class="sub">Verd = sembrar · Blau = trasplantar · Taronja = collir. Passa el ratolí per sobre per veure la lletra original.</p>
  <div class="cal"><table><thead><tr><th></th>{capcalera}</tr></thead><tbody>{''.join(files)}</tbody></table></div>
  <p class="sub" style="margin-top:14px">M = sembra en planter · S = sembra a terra · T = trasplantament · C = collita.
  Calibrat per a Osona: gelades fins a finals d'abril, estius secs i calorosos.</p>
</section>
""" + peu()


def pagina_cultius() -> str:
    cultius = hd.fitxes()
    cards = "".join(
        f'<a class="cultiu-card" href="cultiu/{esc(f["slug"])}.html">'
        + (f'<img src="img/{esc(f["svg"])}" alt="" loading="lazy">' if f["svg"] else "<span></span>")
        + f'<span><span class="n">{esc(f["nom"])}</span><br><span class="f">'
          f'{esc(f["camps"].get("Família botànica", ""))}</span></span></a>'
        for f in cultius)
    return cap("Fitxes de cultiu", "cultius.html") + f"""
<section class="seccio">
  <h2>🥬 {len(cultius)} fitxes de cultiu</h2>
  <p class="sub">Dades ràpides, associacions i la fitxa sencera.</p>
  <div class="cercador"><input id="q" type="search" placeholder="Cerca un cultiu…" aria-label="Cerca un cultiu"></div>
  <div class="graella estreta" id="llista-cultius">{cards}</div>
</section>
<script>
const q=document.getElementById('q');
q.addEventListener('input',()=>{{const t=q.value.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
document.querySelectorAll('#llista-cultius .cultiu-card').forEach(c=>{{const n=c.textContent.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');c.style.display=n.includes(t)?'':'none';}});}});
</script>
""" + peu()


def pagina_tot(arbre) -> str:
    grups = "".join(
        f'<div class="grup-docs"><h3>{esc(cat)}</h3><ul class="llista-docs">'
        + "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for u, t in items)
        + "</ul></div>"
        for cat, items in arbre)
    total = sum(len(i) for _, i in arbre)
    return cap("Tot el fons", "tot.html") + f"""
<section class="seccio">
  <h2>📚 Tot el fons ({total} documents)</h2>
  <p class="sub">Guies, plans, cultius, conserves, plagues, remeieres i documents per imprimir.</p>
  <div class="targeta">{grups}</div>
</section>
""" + peu()




# ─────────────────────────── VISUAL ───────────────────────────
ESTACIO = {12: "hivern", 1: "hivern", 2: "hivern", 3: "primavera", 4: "primavera",
           5: "primavera", 6: "estiu", 7: "estiu", 8: "estiu", 9: "tardor",
           10: "tardor", 11: "tardor"}


def tira_any(mes: int) -> str:
    """Tira de l'any amb el mes actual destacat: context immediat."""
    return '<div class="tira-any">' + "".join(
        f'<span class="{"ara" if i == mes else ""}">{esc(MESOS_CA[i-1][:3].upper())}</span>'
        for i in range(1, 13)) + "</div>"


def tira_mes() -> str:
    """El mes dia a dia amb la lluna de cada dia (visual i util per sembrar)."""
    import calendar
    from datetime import date
    hc = hd._hort_checklist()
    avui = date.today()
    ultim = calendar.monthrange(avui.year, avui.month)[1]
    clau = {d["quan"].lower() for d in hd.mes_info(avui.month)["dates"]}
    cells = []
    for dia in range(1, ultim + 1):
        try:
            _, eti, emoji, _ = hc.fase_lunar(date(avui.year, avui.month, dia))
        except Exception:
            eti, emoji = "", "·"
        cls = "dia"
        if dia == avui.day:
            cls += " avui"
        cells.append(f'<div class="{cls}"><div class="n">{dia}</div>'
                     f'<div class="l">{emoji}</div><div class="q">{esc(eti.split()[-1][:7] if eti else "")}</div></div>')
    return ('<div class="tira-mes">' + "".join(cells) + "</div>")


def bloc_lluna() -> str:
    """La lluna d'avui amb el consell del projecte: el ganxo de tornar cada setmana."""
    from datetime import date
    try:
        _, eti, emoji, desc = hd._hort_checklist().fase_lunar(date.today())
    except Exception:
        return ""
    return (f'<div class="lluna"><div class="f">{emoji}</div><div class="t">'
            f'<strong>{esc(eti)}</strong>{esc(desc)}</div></div>')


def setmana_en_curs() -> str:
    """La setmana en curs, perque la web tingui sentit cada dia i no nomes cada mes."""
    from datetime import date
    hc = hd._hort_checklist()
    avui = date.today()
    try:
        for inici, fi in hc.setmanes_del_mes(avui.year, avui.month):
            if inici <= avui <= fi:
                return (f'<span class="pill">Setmana del {inici.day} al {fi.day} '
                        f'de {MESOS_CA[fi.month-1]}</span>')
    except Exception:
        pass
    return ""


def diagrama_radial(nom: str, bons, dolents, svg=None, ample_text=26) -> str:
    """Diagrama SVG VERTICAL: el cultiu a dalt, veins bons i dolents sota.

    Vertical a proposit: al mobil (que es com es mira la web) una versio
    horitzontal de 720 px queda amb la lletra a la meitat de mida.
    Aqui l'amplada es 360 i la lletra va a 15-16 px reals.
    """
    bons, dolents = list(dict.fromkeys(bons))[:8], list(dict.fromkeys(dolents))[:8]
    if not bons and not dolents:
        return ""
    files = max(len(bons), len(dolents))
    alt = 96 + files * 46
    amplada = 360
    cx = amplada / 2
    p = []
    # el cultiu, dalt de tot
    p.append(f'<rect x="{cx-95:.0f}" y="10" width="190" height="52" rx="26" fill="#3D4A2A"/>')
    p.append(f'<text x="{cx:.0f}" y="43" text-anchor="middle" fill="#FFFCF3" '
             f'font-size="19" font-weight="600">{esc(nom[:20])}</text>')
    # tronc vertical
    if bons or dolents:
        p.append(f'<line x1="{cx:.0f}" y1="62" x2="{cx:.0f}" y2="86" stroke="#C9DDB6" stroke-width="3"/>')
        p.append(f'<line x1="96" y1="86" x2="264" y2="86" stroke="#C9DDB6" stroke-width="3"/>')
    # columnes: bons a l'esquerra, dolents a la dreta
    for costat, llista, fill, stroke, emoji in (("esq", bons, "#EDF4E6", "#C9DDB6", "✅"),
                                               ("dreta", dolents, "#FBEDE7", "#EED0C2", "❌")):
        for i, text in enumerate(llista):
            y = 98 + i * 46
            x0 = 6 if costat == "esq" else 196
            ample = 158
            xmig = x0 + ample / 2
            p.append(f'<line x1="{xmig:.0f}" y1="86" x2="{xmig:.0f}" y2="{y:.0f}" '
                     f'stroke="{stroke}" stroke-width="2"/>')
            p.append(f'<rect x="{x0}" y="{y:.0f}" width="{ample}" height="40" rx="12" '
                     f'fill="{fill}" stroke="{stroke}"/>')
            p.append(f'<text x="{xmig:.0f}" y="{y+25:.0f}" text-anchor="middle" fill="#2D2A22" '
                     f'font-size="15">{emoji} {esc(text[:17])}</text>')
    return (f'<svg class="radial" viewBox="0 0 {amplada} {alt:.0f}" role="img" '
            f'aria-label="Associacions del {esc(nom)}" style="max-width:400px;margin:0 auto">'
            f'{"".join(p)}</svg>')


def llista_tasques(tasques, clau_pref="tasques") -> str:
    """Checklist interactiva: es desa al navegador, no cal servidor."""
    out = []
    for i, t in enumerate(tasques):
        k = f"{clau_pref}-{i}"
        out.append(f'<li data-k="{k}"><input type="checkbox" id="{k}">'
                   f'<label for="{k}" style="cursor:pointer">'
                   f'<span class="prio">{esc(t["cat"])}</span>'
                   f'<span class="t">{esc(t["titol"])}</span>'
                   f'<div class="d">{esc(t["desc"])}</div></label></li>')
    return '<ul class="llista-tasques" id="tasques">' + "".join(out) + "</ul>"




# ─────────────────────────── CERCA GLOBAL ───────────────────────────
def index_cerca(arbre):
    """Index de tot el que es pot trobar: cultius, pagines i documents."""
    e = []
    for f in hd.fitxes():
        e.append({"t": f["nom"], "u": f"cultiu/{f['slug']}.html", "g": "Cultiu",
                  "k": " ".join([f["nom"], f["cientific"], f["camps"].get("Família botànica", ""),
                                 " ".join(f["bons"]), " ".join(f["dolents"])]).lower()})
    for u, t in (("index.html", "Què plantar ara"), ("calendari.html", "Calendari de sembra"),
                 ("associacions.html", "Què va al costat de què"), ("cultius.html", "Totess les fitxes de cultiu"),
                 ("tot.html", "Tot el fons")):
        e.append({"t": t, "u": u, "g": "Pàgina", "k": t.lower()})
    for cat, items in arbre:
        for u, t in items:
            e.append({"t": t, "u": u, "g": "Document", "k": (t + " " + cat).lower()})
    return e


def caixa_cerca(index) -> str:
    import json as _json
    dades = _json.dumps(index, ensure_ascii=False).replace("</", "<\\/")
    return f"""
<section class="seccio" id="cercar">
  <div class="cerca-global">
    <label for="q2">🔍 Cercar qualsevol cosa: un cultiu, una plaga, una guia, una conserva…</label>
    <input id="q2" type="search" placeholder="tomàquet · mildiu · conserves · pastanaga" autocomplete="off">
    <div id="resultats" hidden></div>
  </div>
</section>
<script>
const INDEX = {dades};
const entrada = document.getElementById('q2'), res = document.getElementById('resultats');
function normalitza(t){{
  return t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
}}
entrada.addEventListener('input', () => {{
  const q = normalitza(entrada.value.trim());
  if (q.length < 2) {{ res.hidden = true; res.innerHTML = ''; return; }}
  const trobats = INDEX.filter(x => normalitza(x.k).includes(q) || normalitza(x.t).includes(q)).slice(0, 24);
  if (!trobats.length) {{
    res.hidden = false;
    res.innerHTML = '<p class="buidet">No hi ha res amb «' + entrada.value + '».</p>';
    return;
  }}
  let html = '', grup = '';
  for (const x of trobats) {{
    if (x.g !== grup) {{ grup = x.g; html += '<div class="g">' + grup + 's</div>'; }}
    html += '<a href="' + x.u + '">' + x.t + ' <span>· ' + x.g + '</span></a>';
  }}
  res.hidden = false;
  res.innerHTML = html;
}});
</script>"""


# ─────────────────────────── MAIN ───────────────────────────
def copia_si_cal(origen: Path, desti: Path):
    """Copia nomes si son fitxers diferents (generar a l'arrel del projecte
    faria que origen i desti siguin el mateix i shutil peta)."""
    o, d = Path(origen).resolve(), Path(desti).resolve()
    if o == d:
        return False
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(o, d)
    return True


def carrega_md_render():
    """Conversor markdown->HTML: md_render.py (o build_portal_v2.py si te el nom vell)."""
    import importlib.util
    for nom in ("md_render.py", "build_portal_v2.py"):
        cami = BASE / nom
        if cami.exists():
            spec = importlib.util.spec_from_file_location("md_render", cami)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    raise SystemExit("No trobo md_render.py (ni build_portal_v2.py) al costat de build_web.py")


def genera_docs(v2):
    arbre = []
    n = 0
    for cat, items in v2.CATEGORIES.items():
        fets = []
        for rel, label in items:
            r = v2.read_doc(rel)
            if not r:
                continue
            path, title, cos = r
            # els enllacos interns dels documents apunten als .md originals:
            # els redirigim a la pagina .html equivalent
            cos = re.sub(r'href="([^"#:]+)\.md(#[^"]*)?"',
                         lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', cos)
            desti = OUT / "docs" / (path[:-3] + ".html")
            desti.parent.mkdir(parents=True, exist_ok=True)
            desti.write_text(
                cap(title, "", title, pref="../")
                + '<a class="torna" href="../tot.html">← Tot el fons</a>'
                  f'<article class="doc">{cos}</article>'
                  '<p class="sub" style="margin-top:18px">Extret del fons de coneixement d\'Hort Osona.</p>'
                + peu(pref="../"), encoding="utf-8")
            fets.append((f"docs/{path[:-3]}.html", label or title))
            n += 1
        if fets:
            arbre.append((cat, fets))
    return arbre, n


def main():
    global OUT
    if "--out" in sys.argv:
        OUT = Path(sys.argv[sys.argv.index("--out") + 1])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cultiu").mkdir(parents=True, exist_ok=True)
    (OUT / "estil.css").write_text(CSS, encoding="utf-8")

    imgs = OUT / "img"
    imgs.mkdir(exist_ok=True)
    origen = BASE / "07-fitxes-cultius" / "img"
    n_img = 0
    if origen.exists():
        for svg in origen.glob("*.svg"):
            if copia_si_cal(svg, imgs / svg.name):
                n_img += 1
    icona_trobada = False
    for extra in ("icon.svg", "site/icon.svg"):
        if (BASE / extra).exists():
            copia_si_cal(BASE / extra, OUT / "icon.svg")
            icona_trobada = True
            break
    if not icona_trobada:  # icona propia, sense dependencies
        (OUT / "icon.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="64" height="64" rx="14" fill="#3D4A2A"/>'
            '<path d="M32 12c10 4 16 12 16 22 0 10-7 18-16 18S16 44 16 34c0-10 6-18 16-22z" fill="#8FBF5A"/>'
            '<path d="M32 16v32M32 26c-5 0-8-3-9-7M32 34c5 0 8-3 9-7" stroke="#3D4A2A" '
            'stroke-width="2.5" fill="none" stroke-linecap="round"/></svg>', encoding="utf-8")
        print("   icona generada (no n'hi havia cap al repo)")
    for pwa in ("manifest.json", "service-worker.js"):
        if (BASE / pwa).exists():
            copia_si_cal(BASE / pwa, OUT / pwa)

    gen, fit = hd.associacions(), hd.associacions_fitxes()
    problemes = comprova_bancals(receptes_bancals(), gen, fit)
    if problemes:
        print("⚠️  bancals amb parells discutits:")
        for p in problemes:
            print("   -", p)

    v2 = carrega_md_render()
    arbre, n_docs = genera_docs(v2)
    global INDEX_CERCA
    INDEX_CERCA = index_cerca(arbre)
    print(f"   index de cerca: {len(INDEX_CERCA)} entrades")

    pagines = {"index.html": pagina_index(), "associacions.html": pagina_associacions(),
               "calendari.html": pagina_calendari(), "cultius.html": pagina_cultius(),
               "tot.html": pagina_tot(arbre)}
    for nom, cos in pagines.items():
        (OUT / nom).write_text(cos, encoding="utf-8")

    n_fitxes = 0
    for f in hd.fitxes():
        (OUT / "cultiu" / f"{f['slug']}.html").write_text(pagina_cultiu(f), encoding="utf-8")
        n_fitxes += 1

    # PWA: manifest + service worker amb la llista real de fitxers
    fitxers = ["index.html", "associacions.html", "calendari.html", "cultius.html",
               "tot.html", "estil.css", "icon.svg"] + \
              [f"cultiu/{f['slug']}.html" for f in hd.fitxes()] + \
              [f"img/{s.name}" for s in (OUT / "img").glob("*.svg")] + \
              [f"docs/{p.relative_to(OUT / 'docs').as_posix()}" for p in (OUT / "docs").rglob("*.html")]
    manifest = {
        "name": "Hort Osona — què plantar i amb què",
        "short_name": "Hort Osona",
        "description": "Què plantar aquest mes a Osona i amb què es pot associar. Funciona sense connexió.",
        "start_url": "./index.html", "scope": "./", "display": "standalone",
        "background_color": "#F5EBD8", "theme_color": "#3D4A2A", "lang": "ca",
        "icons": [{"src": "icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    versio = datetime.now().strftime("%Y%m%d%H%M")
    sw = ("const CACHE='hort-osona-" + versio + "';\n"
          "const FITXERS=" + json.dumps(fitxers, ensure_ascii=False) + ";\n"
          "self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE)"
          ".then(c=>c.addAll(FITXERS)).then(()=>self.skipWaiting()));});\n"
          "self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all("
          "k.filter(x=>x!==CACHE).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));});\n"
          "self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;"
          "e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(resp=>{"
          "const copia=resp.clone();caches.open(CACHE).then(c=>c.put(e.request,copia));return resp;"
          "}).catch(()=>caches.match('index.html'))));});\n")
    (OUT / "sw.js").write_text(sw, encoding="utf-8")
    print(f"   PWA: manifest + sw.js amb {len(fitxers)} fitxers per funcionar sense cobertura")
    print(f"✅ {OUT}")
    print(f"   {len(pagines)} pagines · {n_fitxes} fitxes de cultiu · {n_docs} documents · {n_img} il·lustracions")
    print(f"   contradiccions detectades: {len(hd.conflictes())}")


if __name__ == "__main__":
    main()
