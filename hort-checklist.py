#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
hort-checklist.py — Genera una checklist mensual personalitzada de l'hort.

Calcula:
  - El mes actual (o el mes passat com a `--date 2026-07`)
  - La fase lunar real per a cada setmana del mes
  - Les tasques de l'hort adaptades a Osona
  - Les recomanacions biodinàmiques segons la fase lunar
  - Un prompt enriquit per Open WebUI amb tot el context

Ús:
    python hort-checklist.py                       # mes actual
    python hort-checklist.py --date 2026-07        # juliol 2026
    python hort-checklist.py --write               # escriu plans-mensuals/AAAA-MM-mes.md
    python hort-checklist.py --prompt               # imprimeix només el prompt
    python hort-checklist.py --json                 # sortida estructurada (per a integració)
    python hort-checklist.py --html-fragment        # fragment HTML per al lloc web
"""

from __future__ import annotations
import argparse
import json
import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# ───────────────────────────── Constants ─────────────────────────────

# Ubicació
COMARCA = "Osona"
ALTITUD = "500-700 m"
CLIMA = "continental mediterrani"
GELADA_SEGURA = "15 d'abril"   # a partir d'aquí poques gelades
GELADA_TARDANA = "25 d'abril"  # Sant Marc — encara possibles
GELADA_PRIMERA = "15 d'octubre" # comencen les gelades de tardor
GELADA_FORTA = "1 de novembre" # gelades segures a Osona
CALOR_FORTA_INICI = "1 de juliol"
CALOR_FORTA_FI = "31 d'agost"
PLUGES_PRIMAVERA = (1, 5)   # març-maig
PLUGES_TARDOR = (9, 11)     # setembre-novembre

# Nom del mes en català
MESOS_CA = {
    1: "gener", 2: "febrer", 3: "març", 4: "abril",
    5: "maig", 6: "juny", 7: "juliol", 8: "agost",
    9: "setembre", 10: "octubre", 11: "novembre", 12: "desembre"
}

# Mes en curs (es pot sobreescriure amb --date)
def parse_date(s: str) -> Tuple[int, int]:
    """Accepta 'YYYY', 'YYYY-MM' o 'YYYY-MM-DD'."""
    parts = s.split("-")
    if len(parts) == 1:
        return int(parts[0]), date.today().month
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    d = date(int(parts[0]), int(parts[1]), int(parts[2]))
    return d.year, d.month


# ───────────────────────────── Fase lunar ─────────────────────────────

# Algorisme de fase lunar basat en cicles sinòdics (29.530588 dies).
# Referència: Conway (algorisme simple) — és aproximat (±1 dia) però prou bo
# per a planificar tasques agrícoles. La data de referència és una lluna nova
# coneguda: 2000-01-06 18:14 UTC.
LUNA_NOVA_REF = date(2000, 1, 6)
PERIODE_SINODIC = 29.530588

# Les 8 fases tradicionals
FASES_LUNARS = [
    ("nova",       "Lluna nova",       "🌑", "Repòs, planificar, netejar eines."),
    ("creixent",   "Quart creixent",   "🌓", "Sembra i trasplantar parts aèries (tomàquet, pebrot, enciam, cols)."),
    ("plena",      "Lluna plena",      "🌕", "Màxima activitat a sobre, bona per collir fruits i trasplantar."),
    ("minvant",    "Quart minvant",    "🌗", "Sembra i treballar arrels i bulbs (pastanaga, rave, ceba, all), poda, segar adob verd."),
]


def fase_lunar(d: date) -> Tuple[str, str, str, int]:
    """Retorna (nom, etiqueta, emoji, descripció) per a una data donada."""
    dies = (d - LUNA_NOVA_REF).days
    # Posició dins del cicle actual (0-1)
    pos = (dies % PERIODE_SINODIC) / PERIODE_SINODIC

    if pos < 0.0625 or pos >= 0.9375:
        nom, eti, emoji = "nova", "Lluna nova", "🌑"
    elif pos < 0.1875:
        nom, eti, emoji = "creixent", "Quart creixent", "🌓"
    elif pos < 0.3125:
        nom, eti, emoji = "creixent", "Quart creixent", "🌔"
    elif pos < 0.4375:
        nom, eti, emoji = "plena", "Lluna plena", "🌕"
    elif pos < 0.5625:
        nom, eti, emoji = "plena", "Lluna plena", "🌕"
    elif pos < 0.6875:
        nom, eti, emoji = "minvant", "Quart minvant", "🌗"
    elif pos < 0.8125:
        nom, eti, emoji = "minvant", "Quart minvant", "🌖"
    else:
        nom, eti, emoji = "nova", "Lluna nova", "🌑"

    # Descripció biodinàmica
    desc = {
        "nova":    "Repòs, planificar, netejar eines. No sembrar.",
        "creixent": "Sembra i trasplantar parts aèries (tomàquet, pebrot, enciam, cols).",
        "plena":   "Màxima activitat a sobre, bona per collir fruits i trasplantar.",
        "minvant": "Sembra i treballar arrels i bulbs (pastanaga, rave, ceba, all), poda, segar adob verd.",
    }[nom]
    return nom, eti, emoji, desc


def setmanes_del_mes(year: int, month: int) -> List[Tuple[date, date]]:
    """Retorna llista de (dilluns, diumenge) per a cada setmana que toca el mes."""
    primer = date(year, month, 1)
    # Dilluns de la setmana del primer dia
    dilluns_inicial = primer - timedelta(days=primer.weekday())
    setmanes = []
    cursor = dilluns_inicial
    while cursor.month <= month or cursor.month == 1 and month == 12:
        # Si la setmana toca el mes, l'afegim
        inici_setmana = cursor
        fi_setmana = cursor + timedelta(days=6)
        # Comprova si hi ha solapament amb el mes
        if inici_setmana.month == month or fi_setmana.month == month or \
           (inici_setmana < primer.replace(day=1) and fi_setmana >= primer):
            setmanes.append((inici_setmana, fi_setmana))
        cursor += timedelta(days=7)
        if cursor.year > year + 1:
            break
    # També afegim la setmana anterior si comença el dia 1-7 del mes
    return setmanes


# ───────────────────────────── Base de dades de tasques ─────────────────────────────
# Cada tasca té:
#   mesos: llista de mesos (1-12) on s'aplica
#   categoria: 'sembra' | 'trasplantament' | 'collita' | 'conreu' | 'planificacio' | 'tractaments' | 'observacio'
#   titol, desc, prioritat (1-5)
# Les dades s'inspiren en 08-pla-mensual.md, 01-calendari-sembra.md i els plans mensuals existents.

TASQUES: List[Dict] = [
    # ── Gener ─────────────────────────────────────────────────────
    {"mesos": [1], "cat": "planificacio", "prio": 4, "titol": "Comprovar magatzem de llavors",
     "desc": "Fer inventari del que tens, del que ha germinat bé, del que vols canviar. Comanar a Esporus o Les Refardes."},
    {"mesos": [1], "cat": "conreu", "prio": 3, "titol": "Protegir cultius d'hivern amb malles o túnel",
     "desc": "Cols, porros, escaroles, espinacs, bledes, alls tendres, cols de Brussel·les."},
    {"mesos": [1], "cat": "collita", "prio": 3, "titol": "Collir hivernals",
     "desc": "Cols, porros, escaroles, espinacs, bledes, alls tendres, cols de Brussel·les."},
    {"mesos": [1], "cat": "conreu", "prio": 4, "titol": "Podar arbres fruiters de pinyol",
     "desc": "Presseguer, cirerer, pruner. Podar pomers i perers (estructura)."},
    {"mesos": [1], "cat": "planificacio", "prio": 5, "titol": "Decidir varietats i fer plànol de l'any",
     "desc": "Rotació 4/5/6 anys, associacions, parcel·les. Plànol de l'hort."},
    {"mesos": [1], "cat": "planificacio", "prio": 3, "titol": "Reparar estructures, malles, tutors",
     "desc": "Hivernacles, túnels, tutors, reg."},

    # ── Febrer ─────────────────────────────────────────────────────
    {"mesos": [2], "cat": "trasplantament", "prio": 4, "titol": "Trasplantar cebes i porros a l'exterior (amb túnel)",
     "desc": "Si el sòl no és glaçat i tens túnel o protecció."},
    {"mesos": [2], "cat": "sembra", "prio": 3, "titol": "Plantar alls (última oportunitat)",
     "desc": "Si no ho vas fer al novembre. All blanc, all porro."},
    {"mesos": [2], "cat": "conreu", "prio": 4, "titol": "Podar oliveres, vinya, fruiters",
     "desc": "Acabar la poda abans que brotin. Pintar caules amb calç."},
    {"mesos": [2], "cat": "conreu", "prio": 4, "titol": "Tractament d'hivern a fruiters",
     "desc": "Oli mineral + coure contra formes hivernants de plagues."},
    {"mesos": [2], "cat": "sembra", "prio": 5, "titol": "Començar planters d'estiu amb calor de fons",
     "desc": "Tomàquet, pebrot, albergínia, basilic. A l'interior, 18-22°C."},
    {"mesos": [2], "cat": "conreu", "prio": 3, "titol": "Incorporar fems compostats",
     "desc": "A parcel·les de cultius d'estiu. Encoixinar sòl nu amb palla."},

    # ── Març ─────────────────────────────────────────────────────
    {"mesos": [3], "cat": "trasplantament", "prio": 4, "titol": "Trasplantar enciams, cols, apis",
     "desc": "A l'exterior, amb protecció si encara glaça."},
    {"mesos": [3], "cat": "sembra", "prio": 4, "titol": "Sembrar directament",
     "desc": "Pastanaga, ravenet, espinacs, pèsols."},
    {"mesos": [3], "cat": "sembra", "prio": 3, "titol": "Sembrar cebes tardorenques i porros",
     "desc": "Per collir a la tardor."},
    {"mesos": [3], "cat": "conreu", "prio": 3, "titol": "Acabar d'incorporar adobs verds hivernals",
     "desc": "Civada + veça segats. Tallar i incorporar superficialment."},
    {"mesos": [3], "cat": "tractaments", "prio": 3, "titol": "Polvoritzar fruiters amb coure",
     "desc": "Contra càncre, arna. Abans que obrin els borrons."},
    {"mesos": [3], "cat": "sembra", "prio": 4, "titol": "Repicar planter de tomàquet, pebrot, albergínia",
     "desc": "Quan tinguin 2-4 fulles vertaderes."},

    # ── Abril ─────────────────────────────────────────────────────
    {"mesos": [4], "cat": "trasplantament", "prio": 5, "titol": "Trasplantar tomaqueres, pebrots, albergínies",
     "desc": "A partir de Sant Jordi (23 abril) o amb túnel. ATENCIÓ: gelades tardanes possibles."},
    {"mesos": [4], "cat": "sembra", "prio": 4, "titol": "Sembrar carabassons, cogombres, carbasses",
     "desc": "A cobert o amb túnel. Trasplantar quan passi el risc de glaçada."},
    {"mesos": [4], "cat": "trasplantament", "prio": 3, "titol": "Trasplantar cols de primavera",
     "desc": "Bròquil, coliflor, col llombarda."},
    {"mesos": [4], "cat": "conreu", "prio": 4, "titol": "Muntar tutors per a tomaqueres",
     "desc": "Canyes, estructura o espiral. Important fer-ho abans que creixin."},
    {"mesos": [4], "cat": "tractaments", "prio": 3, "titol": "Polvoritzar equisetum preventiu",
     "desc": "Decocció de cua de cavall contra fongs (míldiu, oïdi). Cada 10-15 dies."},
    {"mesos": [4], "cat": "observacio", "prio": 4, "titol": "Anotar primers polls i plagues",
     "desc": "Pugó, primera Tuta. Posar trampes cromàtiques grogues."},

    # ── Maig ─────────────────────────────────────────────────────
    {"mesos": [5], "cat": "trasplantament", "prio": 5, "titol": "Trasplantar al màxim",
     "desc": "Tots els de fruit estiuenc. Si tens hivernacle, ja estan fora."},
    {"mesos": [5], "cat": "sembra", "prio": 4, "titol": "Sembrar mongetes, blat de moro, girasol, cogombre",
     "desc": "Directament a terra. Escalonat cada 15 dies per allargar collita."},
    {"mesos": [5], "cat": "conreu", "prio": 4, "titol": "Primer encoixinat de palla a tomaqueres",
     "desc": "5-10 cm de palla. Estalvia aigua i evita males herbes."},
    {"mesos": [5], "cat": "collita", "prio": 3, "titol": "Collir primers fruits",
     "desc": "Enciams, raves, pèsols, maduixes, primeres cebes tendres."},
    {"mesos": [5], "cat": "tractaments", "prio": 4, "titol": "Polvoritzar contra Tuta absoluta",
     "desc": "Feromones + Bacillus thuringiensis. Trampes a la tomaca."},
    {"mesos": [5], "cat": "tractaments", "prio": 3, "titol": "Començar purins d'ortiga",
     "desc": "Per a adob foliar i preventiu de pugons. Fermentació 10-15 dies."},

    # ── Juny ─────────────────────────────────────────────────────
    {"mesos": [6], "cat": "conreu", "prio": 5, "titol": "Mulching a tot l'hort (URGENT)",
     "desc": "5-10 cm de palla, gespa seca o fulles. Estalvia fins a 200-300 L/setmana."},
    {"mesos": [6], "cat": "conreu", "prio": 5, "titol": "Reg abundant al matí o vespre",
     "desc": "A les 19:00 amb difusor suau. 320 L/setmana de mitjana al juny."},
    {"mesos": [6], "cat": "conreu", "prio": 4, "titol": "Despuntar tomaqueres (deixar 4-5 rams)",
     "desc": "Llevar brots axil·lars per concentrar energia. Tallar fulles baixes malaltes."},
    {"mesos": [6], "cat": "sembra", "prio": 3, "titol": "Sembrar pastanagues de tardor i cols d'hivern",
     "desc": "Cols d'hivern, bròquil tardà, escaroles."},
    {"mesos": [6], "cat": "tractaments", "prio": 4, "titol": "Controlar Tuta, pugó, mosca blanca",
     "desc": "Inspecció setmanal. Trampes cromàtiques, Bacillus, sabó potàssic."},
    {"mesos": [6], "cat": "tractaments", "prio": 3, "titol": "Començar purí de consolda",
     "desc": "Rica en potassi. Per a tomaqueres i fruiters. Alternar amb ortiga."},
    {"mesos": [6], "cat": "collita", "prio": 3, "titol": "Collir: pèsols, faves, maduixes, cebes tendres, enciams",
     "desc": "Primers fruits: maduixes, cireres. Màxima activitat."},

    # ── Juliol ─────────────────────────────────────────────────────
    {"mesos": [7], "cat": "conreu", "prio": 5, "titol": "Reg diari (matinera o vespre)",
     "desc": "A Osona, juliol és el mes més sec. No regar al migdia."},
    {"mesos": [7], "cat": "conreu", "prio": 4, "titol": "Mulching abundant",
     "desc": "Reforçar palla. Control de l'evaporació."},
    {"mesos": [7], "cat": "tractaments", "prio": 4, "titol": "Polvoritzar sofre si oïdi",
     "desc": "Símptomes: pols blanca a fulles de carabassó, cogombre, vinya."},
    {"mesos": [7], "cat": "collita", "prio": 4, "titol": "Màxima collita d'estiu",
     "desc": "Tomàquets, pebrots, carabassons, mongeta tendra, albergínies."},
    {"mesos": [7], "cat": "sembra", "prio": 3, "titol": "Sembrar cols d'hivern, escaroles, pastanagues",
     "desc": "Cols d'hivern, kale, bròquil tardà, escaroles, pastanagues de tardor."},
    {"mesos": [7], "cat": "conreu", "prio": 3, "titol": "Tallar adobs verds estivals abans de granar",
     "desc": "Si tens facelia, mostassa, etc. Tallar i deixar en superfície."},

    # ── Agost ─────────────────────────────────────────────────────
    {"mesos": [8], "cat": "conreu", "prio": 4, "titol": "Reg de suport (matinera!)",
     "desc": "A les 7-8h. Reduir una mica el volum si plou."},
    {"mesos": [8], "cat": "collita", "prio": 5, "titol": "Collita abundant",
     "desc": "Tomàquets, pebrots, albergínies, melons, síndries, blat de moro."},
    {"mesos": [8], "cat": "conreu", "prio": 4, "titol": "Despuntar tomaqueres (apical)",
     "desc": "Tallar la gemma apical per aturar el creixement i concentrar en fruits."},
    {"mesos": [8], "cat": "sembra", "prio": 3, "titol": "Sembrar cols d'hivern, espinacs, raves",
     "desc": "Cols d'hivern, kale, espinacs, raves, pastanagues."},
    {"mesos": [8], "cat": "planificacio", "prio": 4, "titol": "Guardar llavors de les millors plantes",
     "desc": "Tomàquet, pebrot, mongeta. Triar les més sanes i primerenques."},
    {"mesos": [8], "cat": "conreu", "prio": 3, "titol": "Preparar parcel·les per a cultius de tardor",
     "desc": "Incorporar compost a les que alliberis."},

    # ── Setembre ─────────────────────────────────────────────────────
    {"mesos": [9], "cat": "sembra", "prio": 5, "titol": "Sembra de cols d'hivern, escaroles, espinacs, raves",
     "desc": "Finestres de sembra d'hivern. No deixar passar! Última oportunitat per cols."},
    {"mesos": [9], "cat": "trasplantament", "prio": 4, "titol": "Trasplantar planter d'hivern",
     "desc": "Cols, escaroles, porros. Preparar hivernacles i túnels."},
    {"mesos": [9], "cat": "collita", "prio": 3, "titol": "Collita final d'estiu",
     "desc": "Tomàquets, pebrots, albergínies, carabassons, carbasses. Guardar llavors."},
    {"mesos": [9], "cat": "sembra", "prio": 4, "titol": "Sembrar adobs verds hivernals",
     "desc": "Civada+veça, pèsol farratger. A les parcel·les que alliberis."},
    {"mesos": [9], "cat": "planificacio", "prio": 4, "titol": "Anotar resultats de l'any",
     "desc": "Per planificar el 2027. Què ha funcionat, què no."},

    # ── Octubre ─────────────────────────────────────────────────────
    {"mesos": [10], "cat": "trasplantament", "prio": 4, "titol": "Trasplantar enciams, cols, porros d'hivern",
     "desc": "Si tens planter fet, ara és el moment."},
    {"mesos": [10], "cat": "sembra", "prio": 5, "titol": "Sembra d'alls",
     "desc": "Cabeces i grans d'all blanc, all porro. A Osona, clàssic octubre-novembre."},
    {"mesos": [10], "cat": "collita", "prio": 3, "titol": "Collir: carbasses, moniatos, cols d'estiu, raves, espinacs",
     "desc": "Carbassa del Vimbodí, moniatos. Assecat i conserves."},
    {"mesos": [10], "cat": "conreu", "prio": 4, "titol": "Cobrir parcel·les lliures amb palla o adob verd",
     "desc": "No deixar sòl nu. Compost o palla o adob verd segat."},
    {"mesos": [10], "cat": "conreu", "prio": 3, "titol": "Podar fruiters (pomeres, pereres)",
     "desc": "Poda de tardor. Arbres de pinyol millor al febrer."},
    {"mesos": [10], "cat": "planificacio", "prio": 4, "titol": "Fer inventari de llavors guardades",
     "desc": "Comprovar germinació, organizar per any de collita."},
    {"mesos": [10], "cat": "planificacio", "prio": 3, "titol": "Comprar llavors per a la temporada vinent",
     "desc": "Esporus, Les Refardes. Comanar amb temps."},

    # ── Novembre ─────────────────────────────────────────────────────
    {"mesos": [11], "cat": "collita", "prio": 4, "titol": "Darreres collites",
     "desc": "Cols, porros, escaroles, espinacs, naps, raves, cols de Brussel·les."},
    {"mesos": [11], "cat": "conreu", "prio": 4, "titol": "Incorporar fems compostats",
     "desc": "A parcel·les lliures. Cobrir sòl amb palla o fullaraca."},
    {"mesos": [11], "cat": "conreu", "prio": 3, "titol": "Pintar calç als troncs dels fruiters",
     "desc": "Protecció contra gelades i plagues."},
    {"mesos": [11], "cat": "conreu", "prio": 3, "titol": "Podar arbres de pinyol",
     "desc": "Pruner, presseguer, cirerer. Plantar arbres a arrel nua."},
    {"mesos": [11], "cat": "planificacio", "prio": 4, "titol": "Fer balanç anual",
     "desc": "Quadern d'observació. Què ha funcionat, què no. Conserves finals."},

    # ── Desembre ─────────────────────────────────────────────────────
    {"mesos": [12], "cat": "conreu", "prio": 4, "titol": "Protegir cultius d'hivern amb malles o plàstic",
     "desc": "Contra gelades. Especialment cols i porros."},
    {"mesos": [12], "cat": "conreu", "prio": 3, "titol": "Cobrir plantes sensibles a gelades",
     "desc": "Romaní, sàlvia, alfalfa. Malles o fullaraca."},
    {"mesos": [12], "cat": "conreu", "prio": 4, "titol": "Cobrir planter exterior amb túnel o hivernacle",
     "desc": "Cols, enciams d'hivern. Protegir arrels."},
    {"mesos": [12], "cat": "conreu", "prio": 3, "titol": "Podar oliveres (si no s'ha fet al novembre)",
     "desc": "Plantar arbres fruiters a arrel nua (fins febrer)."},
    {"mesos": [12], "cat": "planificacio", "prio": 5, "titol": "Reparar eines, netejar, engreixar",
     "desc": "Tisores, aixada, aixadella. Neteja i oli de línia."},
    {"mesos": [12], "cat": "planificacio", "prio": 4, "titol": "Planificar l'any vinent",
     "desc": "Rotació, varietats, comandes, calendari de sembra."},
]


# Recomanacions generals per fase lunar (s'apliquen a qualsevol setmana del mes)
CONSELL_LUNAR_GENERAL = {
    "nova":    "🌑 Lluna nova — bona per netejar, planificar, no sembrar.",
    "creixent": "🌓🌔 Lluna creixent — sembra i trasplanta parts aèries.",
    "plena":   "🌕 Lluna plena — collita i trasplantaments, màxima activitat a sobre.",
    "minvant": "🌗🌖 Lluna minvant — sembra arrels/bulbs, poda, segar adob verd.",
}


# ───────────────────────────── Generació ─────────────────────────────

def tasques_del_mes(month: int) -> List[Dict]:
    return sorted(
        [t for t in TASQUES if month in t["mesos"]],
        key=lambda t: (-t["prio"], t["titol"])
    )


def consell_lunar_setmana(d: date) -> str:
    nom, eti, emoji, desc = fase_lunar(d)
    return f"**{emoji} {eti}** — {desc}"


def generar_checklist_markdown(year: int, month: int) -> str:
    """Genera el document de checklist en Markdown."""
    nom_mes = MESOS_CA[month]
    avui = date.today()
    es_avui = (year == avui.year and month == avui.month)
    titol = f"📅 Pla mensual de l'hort — {nom_mes.capitalize()} {year}"
    if es_avui:
        titol += "  *(mes actual)*"

    md = [f"# {titol}\n"]
    md.append(f"> **Comarca:** {COMARCA} · **{ALTITUD}** · Clima {CLIMA}")
    md.append(f"> Generat el {avui.strftime('%Y-%m-%d')} per `hort-checklist.py`")
    md.append("")

    # Context climàtic del mes
    md.append("## 🌡️ Context climàtic del mes\n")
    notes_climatiques = notes_per_mes(month)
    md.append(notes_climatiques)
    md.append("")

    # Setmanes i fase lunar
    md.append("## 🌙 Calendari lunar del mes\n")
    setmanes = setmanes_del_mes(year, month)
    md.append("| Setmana | Dates | Fase lunar | Recomanació |")
    md.append("|---------|-------|------------|-------------|")
    for i, (ini, fi) in enumerate(setmanes, 1):
        # Fase dominant: agafem el dia central
        centre = ini + timedelta(days=3)
        nom, eti, emoji, desc = fase_lunar(centre)
        md.append(f"| {i} | {ini.strftime('%d/%m')} – {fi.strftime('%d/%m')} | {emoji} {eti} | {desc} |")
    md.append("")

    # Tasques del mes, organitzades per categoria
    md.append("## 🌱 Tasques del mes\n")
    tasques = tasques_del_mes(month)
    per_cat: Dict[str, List[Dict]] = {}
    for t in tasques:
        per_cat.setdefault(t["cat"], []).append(t)
    ordre_cat = [
        ("sembra",         "🌱 Sembra"),
        ("trasplantament", "🌿 Trasplantament"),
        ("conreu",         "🛠️ Conreu"),
        ("tractaments",    "🐞 Tractaments"),
        ("collita",        "🧺 Collita"),
        ("planificacio",   "📋 Planificació"),
        ("observacio",     "👀 Observació"),
    ]
    for cat_key, cat_titol in ordre_cat:
        if cat_key not in per_cat:
            continue
        md.append(f"### {cat_titol}\n")
        for t in per_cat[cat_key]:
            checkbox = "- [ ]"
            prio_emoji = "🔥" * t["prio"] if t["prio"] >= 4 else ("•" * t["prio"])
            md.append(f"{checkbox} **{t['titol']}** `{prio_emoji}`")
            md.append(f"      {t['desc']}")
        md.append("")

    # Dates clau del mes
    md.append("## 📌 Dates clau a Osona\n")
    dates_clau = dates_clau_per_mes(month)
    for etiqueta, data in dates_clau:
        md.append(f"- **{etiqueta}** — {data}")
    md.append("")

    # Peu
    md.append("---")
    md.append(f"_Font: base de dades de `hort-checklist.py`. Regenera amb `python hort-checklist.py --write`._")
    md.append("")
    return "\n".join(md)


def notes_per_mes(month: int) -> str:
    parts = []
    if month in (1, 2, 12):
        parts.append("Hivern. **Hivernacles i túnels** actius. Protegir planter exterior.")
    if month in (1, 2, 3):
        parts.append("**Risc de glaçada** fins a mitjans d'abril. Planter a cobert.")
    if month in (3, 4, 5):
        parts.append("Pluges de primavera. **Bona època** per trasplantar i sembrar.")
    if month in (4,):
        parts.append(f"⚠️ **Gelada tardana** encara possible fins a {GELADA_TARDANA} (Sant Marc).")
    if month in (5, 6):
        parts.append("Temperatures suaus. Ideal per trasplantar cultius d'estiu.")
    if month in (6, 7, 8):
        parts.append(f"🔥 **Calor forta** entre {CALOR_FORTA_INICI} i {CALOR_FORTA_FI}. Reg de matinera o vespre, mulching obligatori.")
    if month in (7, 8):
        parts.append("Pic de calor i sequera. **Mulching 5-10 cm** indispensable.")
    if month in (9, 10):
        parts.append("Pluges de tardor. **Aprofitar** per sembrar adobs verds i cultius d'hivern.")
    if month in (10, 11):
        parts.append(f"⚠️ **Primeres gelades** a partir de {GELADA_PRIMA}.")
    if month in (11, 12):
        parts.append(f"**Gelada forta** a partir de {GELADA_FORTA}. Protegir cultius d'hivern.")
    return "\n".join(parts)


def dates_clau_per_mes(month: int) -> List[Tuple[str, str]]:
    """Retorna dates clau del mes per a Osona."""
    dates = []
    if month == 1:
        dates = [
            ("Sant Antoni", "17 de gener — protegir arbres fruiters joves"),
            ("ComprAR llavors", "tot el mes — comanar a Esporus o Les Refardes"),
        ]
    elif month == 2:
        dates = [
            ("Candelera", "2 de febrer — última oportunitat per plantar alls"),
            ("Inventari", "tot el febrer — revisar magatzem de conserves"),
        ]
    elif month == 3:
        dates = [
            ("Equinocci de primavera", "20-21 de març"),
            ("Fira de la Llavor de Vic", "cap de setmana proper — assistir!"),
        ]
    elif month == 4:
        dates = [
            ("Sant Jordi", "23 d'abril — trasplantar tomaqueres/pebrots a l'exterior (si no glaça)"),
            ("Sant Marc", "25 d'abril — darrera glaçada tardana possible"),
        ]
    elif month == 5:
        dates = [
            ("Sant Isidre", "15 de maig — patró dels pagesos"),
            ("ComprAR planter", "tot maig — si no has fet planter, comprar-lo"),
        ]
    elif month == 6:
        dates = [
            ("Revetlla de Sant Joan", "23-24 de juny — el·lícies, solstici d'estiu"),
            ("Inici calor forta", "1 de juliol entrant — reforçar reg"),
        ]
    elif month == 7:
        dates = [
            ("Pic de calor", "tot juliol — reg diari, mulching, ombra si cal"),
        ]
    elif month == 8:
        dates = [
            ("Mare de Déu d'Agost", "15 d'agost — primeres pluges possibles"),
            ("Guardar llavors", "tot agost — triar les millors plantes"),
        ]
    elif month == 9:
        dates = [
            ("Equinocci de tardor", "22-23 de setembre"),
            ("Sembra d'hivern", "tot setembre — última oportunitat per cols"),
        ]
    elif month == 10:
        dates = [
            ("Sembra d'alls", "tot octubre — clàssic d'Osona"),
            ("Fira de Sant Mateu (Vic)", "21 de setembre — fira de la terra"),
        ]
    elif month == 11:
        dates = [
            ("Castanyada", "1 de novembre — castanyes i primeres gelades"),
            ("Plantació fruiters", "tot novembre — arbres a arrel nua"),
        ]
    elif month == 12:
        dates = [
            ("Solstici d'hivern", "21-22 de desembre"),
            ("Nadal", "25 de desembre — balanç de l'any"),
        ]
    return dates


def generar_prompt_openwebui(year: int, month: int) -> str:
    """Genera un prompt enriquit per a Open WebUI amb tot el context."""
    nom_mes = MESOS_CA[month]
    avui = date.today()
    setmanes = setmanes_del_mes(year, month)
    tasques = tasques_del_mes(month)
    fase_actual = fase_lunar(avui if (year == avui.year and month == avui.month)
                              else date(year, month, 15))
    consell_actual = CONSELL_LUNAR_GENERAL[fase_actual[0]]

    prompt = f"""# 🌱 Context: Hort Osona — {nom_mes.capitalize()} {year}

## Dades bàsiques
- **Comarca:** {COMARCA} (Catalunya central)
- **Altitud:** {ALTITUD}
- **Clima:** {CLIMA}
- **Mida hort:** ~20 m² (4×5 m)
- **Sòl:** sorrenc (drena ràpid, +30% aigua vs sòl normal)
- **Filosofia:** ecològica, sense químics de síntesi

## Mes actual
Estem a **{nom_mes.capitalize()} de {year}**. {notes_per_mes(month).replace(chr(10), ' ')}

## Fase lunar actual
{consell_actual}

## Setmanes i fases lunars del mes
"""
    for i, (ini, fi) in enumerate(setmanes, 1):
        centre = ini + timedelta(days=3)
        nom, eti, emoji, desc = fase_lunar(centre)
        prompt += f"- **Setmana {i}** ({ini.strftime('%d/%m')} – {fi.strftime('%d/%m')}): {emoji} {eti} — {desc}\n"

    prompt += f"""
## Tasques prioritàries del mes (per categoria)

"""
    per_cat: Dict[str, List[Dict]] = {}
    for t in tasques:
        per_cat.setdefault(t["cat"], []).append(t)
    ordre_cat = [
        ("sembra", "Sembra"),
        ("trasplantament", "Trasplantament"),
        ("conreu", "Conreu"),
        ("tractaments", "Tractaments"),
        ("collita", "Collita"),
        ("planificacio", "Planificació"),
    ]
    for cat_key, cat_titol in ordre_cat:
        if cat_key not in per_cat:
            continue
        prompt += f"### {cat_titol}\n"
        for t in per_cat[cat_key]:
            prio_str = "🔴" if t["prio"] >= 5 else ("🟠" if t["prio"] >= 4 else "🟡")
            prompt += f"- {prio_str} **{t['titol']}** — {t['desc']}\n"
        prompt += "\n"

    prompt += f"""## Dates clau a Osona aquest mes
"""
    for etiqueta, data in dates_clau_per_mes(month):
        prompt += f"- **{etiqueta}** — {data}\n"

    prompt += """
## Varietats locals preferents
Ceba de Vic, Pebrot d'Olot, Mongeta del Ganxet, Tomàquet de Montserrat, Poma de Tona,
Carbassa del Vimbodí, Carabassó de la Plana, Pastanaga de Núria, Enciam de l'Urgell.

## Fonts locals de referència
- Esporus (Vic/Manresa)
- L'Era (Manresa)
- CCPAE
- Fundació Miquel Agustí
- Escola Agrària de Manresa

## Com respondre
1. Dona consells pràctics adaptats a Osona, no genèrics.
2. Explica sempre el PERQUÈ agronòmic.
3. Quan una pregunta correspongui a una fitxa del projecte hort-osona, referencia-la
   pel nom del fitxer (p. ex. "01-calendari-sembra.md", "03-gestio-plagues.md").
4. Si la pregunta és nova i rellevant, suggereix crear o actualitzar una fitxa.
5. Dates i calendaris SEMPRE adaptats a Osona: gelades fins a finals d'abril,
   calor forta juliol-agost.
6. Si no saps alguna cosa, digue-ho honestament.

## Recordatori
Aquest hort és un projecte de vida. Cuida el sòl, cuida la biodiversitat, i el
sistema et cuidarà a tu. Bona collita! 🌱
"""
    return prompt


def generar_html_fragment(year: int, month: int) -> str:
    """Genera un fragment HTML per incrustar al lloc web."""
    nom_mes = MESOS_CA[month]
    avui = date.today()
    setmanes = setmanes_del_mes(year, month)
    tasques = tasques_del_mes(month)

    parts = [f'<div class="checklist">']
    parts.append(f'<h2>📅 {nom_mes.capitalize()} {year}</h2>')
    parts.append(f'<p class="clima">{notes_per_mes(month).replace(chr(10), "<br>")}</p>')

    parts.append('<h3>🌙 Setmanes i fases</h3><ul class="lunar">')
    for i, (ini, fi) in enumerate(setmanes, 1):
        centre = ini + timedelta(days=3)
        nom, eti, emoji, desc = fase_lunar(centre)
        parts.append(f'<li><strong>Setmana {i}</strong> ({ini.strftime("%d/%m")} – {fi.strftime("%d/%m")}): {emoji} {eti} — {desc}</li>')
    parts.append('</ul>')

    per_cat: Dict[str, List[Dict]] = {}
    for t in tasques:
        per_cat.setdefault(t["cat"], []).append(t)
    parts.append('<h3>🌱 Tasques</h3>')
    ordre_cat = [
        ("sembra", "🌱 Sembra"),
        ("trasplantament", "🌿 Trasplantament"),
        ("conreu", "🛠️ Conreu"),
        ("tractaments", "🐞 Tractaments"),
        ("collita", "🧺 Collita"),
        ("planificacio", "📋 Planificació"),
        ("observacio", "👀 Observació"),
    ]
    for cat_key, cat_titol in ordre_cat:
        if cat_key not in per_cat:
            continue
        parts.append(f'<h4>{cat_titol}</h4><ul class="tasques">')
        for t in per_cat[cat_key]:
            prio_str = "🔴" if t["prio"] >= 5 else ("🟠" if t["prio"] >= 4 else "🟡")
            parts.append(f'<li data-prio="{t["prio"]}"><label><input type="checkbox"><strong>{prio_str} {t["titol"]}</strong> <small>{t["desc"]}</small></label></li>')
        parts.append('</ul>')

    parts.append('</div>')
    return "\n".join(parts)


def generar_json(year: int, month: int) -> Dict:
    """Retorna l'estructura completa en JSON."""
    nom_mes = MESOS_CA[month]
    avui = date.today()
    setmanes = []
    for i, (ini, fi) in enumerate(setmanes_del_mes(year, month), 1):
        centre = ini + timedelta(days=3)
        nom, eti, emoji, desc = fase_lunar(centre)
        setmanes.append({
            "n": i,
            "inici": ini.isoformat(),
            "fi": fi.isoformat(),
            "fase": {"nom": nom, "etiqueta": eti, "emoji": emoji, "desc": desc}
        })
    tasques = tasques_del_mes(month)
    return {
        "year": year,
        "month": month,
        "mes_ca": nom_mes,
        "comarca": COMARCA,
        "clima_nota": notes_per_mes(month),
        "data_generacio": avui.isoformat(),
        "setmanes": setmanes,
        "tasques": tasques,
        "dates_clau": [{"etiqueta": e, "data": d} for e, d in dates_clau_per_mes(month)],
    }


# ───────────────────────────── Main ─────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Genera checklist mensual de l'hort d'Osona")
    ap.add_argument("--date", default=None,
                    help="Mes a generar (YYYY, YYYY-MM o YYYY-MM-DD). Per defecte: mes actual")
    ap.add_argument("--write", action="store_true",
                    help="Escriu el fitxer a plans-mensuals/AAAA-MM-mes.md")
    ap.add_argument("--prompt", action="store_true",
                    help="Imprimeix només el prompt per Open WebUI")
    ap.add_argument("--json", action="store_true",
                    help="Imprimeix l'estructura completa en JSON")
    ap.add_argument("--html-fragment", action="store_true",
                    help="Imprimeix un fragment HTML per incrustar al lloc web")
    ap.add_argument("--print-fase", default=None,
                    help="Imprimeix la fase lunar d'una data concreta (YYYY-MM-DD)")
    args = ap.parse_args()

    if args.print_fase:
        d = date(*[int(x) for x in args.print_fase.split("-")])
        nom, eti, emoji, desc = fase_lunar(d)
        print(f"{d.isoformat()}: {emoji} {eti} — {desc}")
        return

    if args.date:
        year, month = parse_date(args.date)
    else:
        today = date.today()
        year, month = today.year, today.month

    if args.prompt:
        print(generar_prompt_openwebui(year, month))
        return

    if args.json:
        print(json.dumps(generar_json(year, month), ensure_ascii=False, indent=2))
        return

    if args.html_fragment:
        print(generar_html_fragment(year, month))
        return

    if args.write:
        # Escriu a plans-mensuals/AAAA-MM-mes.md
        out_dir = Path(__file__).resolve().parent.parent / "plans-mensuals"
        out_dir.mkdir(exist_ok=True)
        out = out_dir / f"{year}-{month:02d}-{MESOS_CA[month]}.md"
        out.write_text(generar_checklist_markdown(year, month), encoding="utf-8")
        print(f"✅ Escrit: {out.relative_to(Path(__file__).resolve().parent.parent)}")
        print(f"   ({out.stat().st_size} bytes)")
        return

    # Per defecte: imprimeix el markdown
    print(generar_checklist_markdown(year, month))


if __name__ == "__main__":
    main()
