#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hort_data.py — Llegeix les fonts .md del projecte hort-osona i en treu dades
estructurades per construir la web. No inventa res: tot surt dels .md.

Fonts:
  01-calendari-sembra.md      -> que es pot sembrar/trasplantar/collir cada mes
  02-associacions-rotacions.md -> associacions bones i incompatibilitats
  07-fitxes-cultius/*.md      -> fitxes: dades rapides + associacions propies
  plans-mensuals/*.md         -> pla del mes (clima i tasques)
  hort-checklist.py           -> tasques i notes del mes (modul del projecte)
"""
import re
import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple

BASE = Path(__file__).resolve().parent

MESOS = ["gener", "febrer", "març", "abril", "maig", "juny",
         "juliol", "agost", "setembre", "octubre", "novembre", "desembre"]

# codi del calendari -> (clau interna, verb per a la UI)
ACTIVITATS = {
    "M": ("planter", "Sembrar en planter"),
    "S": ("terra", "Sembrar a terra"),
    "T": ("trasplantar", "Trasplantar"),
    "C": ("collir", "Collir"),
}


def _neteja(s: str) -> str:
    s = s.strip()
    s = s.replace("**", "").replace("*", "")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ─────────────────────────── CALENDARI ───────────────────────────
def grups_calendari() -> Dict[str, List[Tuple[str, List[str]]]]:
    """Retorna {grup: [(cultiu, [12 cel·les])]} tal com surt del calendari."""
    txt = (BASE / "01-calendari-sembra.md").read_text(encoding="utf-8")
    grups: Dict[str, List[Tuple[str, List[str]]]] = {}
    grup = "Altres"
    for linia in txt.split("\n"):
        if linia.startswith("## "):
            titol = linia[3:].strip()
            # nomes les seccions de cultius (les altres no tenen taula)
            if any(p in titol for p in ("Hortalisses", "Bulbs", "Aromàtiques", "Aromatiques")):
                grup = titol.split("(")[0].strip()
            continue
        if not linia.startswith("|"):
            continue
        cels = [c.strip() for c in linia.strip().strip("|").split("|")]
        if len(cels) != 13:
            continue
        nom = _neteja(cels[0])
        if not nom or nom.lower().startswith("cultiu") or set(nom) <= set("-: "):
            continue
        grups.setdefault(grup, []).append((nom, [_neteja(c) for c in cels[1:]]))
    return grups


def per_mes() -> Dict[int, Dict[str, List[Tuple[str, str]]]]:
    """{mes(1-12): {planter/terra/trasplantar/collir: [(cultiu, grup), ...]}}"""
    out = {m: {k: [] for k in ("planter", "terra", "trasplantar", "collir")} for m in range(1, 13)}
    for grup, files in grups_calendari().items():
        for nom, cels in files:
            for i, cel in enumerate(cels):
                for codi in re.split(r"[·/,]", cel):
                    codi = codi.strip()
                    if codi in ACTIVITATS:
                        out[i + 1][ACTIVITATS[codi][0]].append((nom, grup))
    return out


# ─────────────────────────── ASSOCIACIONS ───────────────────────────
def _files_taula(bloc: str) -> List[List[str]]:
    files = []
    for linia in bloc.split("\n"):
        if not linia.startswith("|"):
            continue
        cels = [_neteja(c) for c in linia.strip().strip("|").split("|")]
        if len(cels) < 2 or set("".join(cels)) <= set("-: "):
            continue
        if cels[0].lower().startswith("cultiu"):
            continue
        files.append(cels)
    return files


# frases que no son noms de planta (avisos, regles, rotacions)
_SOROLL = re.compile(r"^(totes les|altres|cap greu|rota\b|evita\b|no plantar|millor|sempre|"
                     r"les tres|rotar|esperar|transmeten|comparteixen)", re.I)


_VERBS = re.compile(r"\b(espanta|repeleix|repel·leix|repel|atrau|millora|fixa|protegeix|confon|"
                    r"aprofita|competeix|atura|inhibeix|transmet|comparteix|trenca|dona|fa ombra|"
                    r"augmenta|redu|afavoreix|necessita|aporta|enforteix|neteja|ombreja)\b", re.I)


def _neta_item(x: str):
    x = x.strip().lstrip("-•*· ").strip()
    x = x.strip("*.;,:· ")
    x = re.sub(r"\s+", " ", x)
    if not x or len(x) > 30:
        return None
    if "**" in x or ":" in x or "(" in x:
        return None
    if _SOROLL.match(x) or _VERBS.search(x):
        return None
    if x.lower().startswith(("a la mateixa", "any rere", "durant la", "el seu ", "la seva ")):
        return None
    return x


def _llista(text: str) -> List[str]:
    text = re.sub(r"\([^)]*\)", "", text)          # fora aclariments entre parentesis
    parts = re.split(r"[,;/]|\si\s", text)
    out = []
    for p in parts:
        n = _neta_item(p)
        if n:
            out.append(n)
    return out


def associacions() -> Dict[str, Dict[str, List[str]]]:
    """{cultiu: {'bons': [...], 'dolents': [...], 'motiu_bons': str, 'motiu_dolents': str}}"""
    txt = (BASE / "02-associacions-rotacions.md").read_text(encoding="utf-8")
    # separar les dues taules per la seccio
    tros_bons = txt.split("## 2.")[0]
    tros_dolents = txt.split("## 2.")[1] if "## 2." in txt else ""

    data: Dict[str, Dict[str, List[str]]] = {}

    def entrada(nom: str) -> Dict[str, List[str]]:
        return data.setdefault(nom, {"bons": [], "dolents": [], "discutits": [],
                                     "motiu_bons": "", "motiu_dolents": ""})

    for cels in _files_taula(tros_bons):
        if len(cels) < 3:
            continue
        e = entrada(cels[0])
        e["bons"] += _llista(cels[1])
        if cels[2] and not e["motiu_bons"]:
            e["motiu_bons"] = cels[2]
    for cels in _files_taula(tros_dolents):
        if len(cels) < 3:
            continue
        e = entrada(cels[0])
        e["dolents"] += _llista(cels[1])
        if cels[2] and not e["motiu_dolents"]:
            e["motiu_dolents"] = cels[2]

    # REGLA PRUDENT: si una fila diu que son bons i una altra que son dolents,
    # es queda com a DOLENT i es marca com a DISCUTIT (millor no arriscar-se).
    for a, d in data.items():
        for b in list(d["bons"]):
            for c, dd in data.items():
                if normalitza(c) == normalitza(b) and \
                   normalitza(a) in [normalitza(x) for x in dd["dolents"]]:
                    d["bons"].remove(b)
                    d["discutits"].append(b)
                    break

    # treure duplicats mantenint l'ordre
    for e in data.values():
        for k in ("bons", "dolents", "discutits"):
            vist, net = set(), []
            for x in e[k]:
                if x.lower() not in vist:
                    vist.add(x.lower())
                    net.append(x)
            e[k] = net
    return data


def associacions_fitxes() -> Dict[str, Dict[str, List[str]]]:
    """Les associacions que cada fitxa declara de si mateixa."""
    out = {}
    for fitxa in sorted((BASE / "07-fitxes-cultius").glob("*.md")):
        if fitxa.name.startswith("_"):
            continue
        txt = fitxa.read_text(encoding="utf-8")
        bloc = re.search(r"##\s*Associacions\s*\n(.*?)(?=\n##\s|\Z)", txt, re.S)
        if not bloc:
            continue
        cos = bloc.group(1)
        bones, dolentes = [], []
        actual = None
        for linia in cos.split("\n"):
            l = linia.strip()
            if re.match(r"[-*]?\s*\*\*(Bones|Associacions bones|✅)", l, re.I):
                actual = "bons"
                resta = re.sub(r"^[-*]?\s*(\*\*)?[^:]*:\s*(\*\*)?", "", l)
                bones += _llista(resta)
                continue
            if re.match(r"[-*]?\s*\*\*(Dolentes|Associacions dolentes|❌)", l, re.I):
                actual = "dolents"
                resta = re.sub(r"^[-*]?\s*(\*\*)?[^:]*:\s*(\*\*)?", "", l)
                dolentes += _llista(resta)
                continue
            if re.match(r"^#{3,}\s*(✅|❌)", l):
                actual = "bons" if "✅" in l else "dolents"
                continue
            if l.startswith(("-", "•", "*")) and actual:
                # una linia pot portar diverses plantes ("Api, all, ceba, porro"):
                # les separem perque despres es puguin comparar una a una
                tros = _neteja(l.lstrip("-•* ").split("(")[0])
                for item in (_llista(tros) or []):
                    (bones if actual == "bons" else dolentes).append(item)
        # tambe pot venir en una sola linia: "- **Bones**: a, b, c"
        for m2 in re.finditer(r"\*\*(?:Bones|Associacions bones)\*\*:\s*([^\n]+)", cos):
            bones += _llista(m2.group(1))
        for m2 in re.finditer(r"\*\*(?:Dolentes|Associacions dolentes)\*\*:\s*([^\n]+)", cos):
            dolentes += _llista(m2.group(1))
        # duplicats fora
        bones = _unics(bones)
        dolentes = _unics(dolentes)
        # REGLA PRUDENT dins d'una mateixa fitxa: si surt a les dues llistes,
        # fora de "bones" i cap a "discutits" (no el posem com a bo si dubtem).
        discutits = [x for x in bones if x.lower() in [d.lower() for d in dolentes]]
        bones = [x for x in bones if x.lower() not in [d.lower() for d in dolentes]]
        slug = fitxa.stem
        if bones or dolentes or discutits:
            out[slug] = {"bons": bones, "dolents": dolentes, "discutits": discutits}
    return out


def conflictes() -> List[Tuple[str, str, str]]:
    """Parells on les fonts no es posen d'acord (per arreglar la documentacio).

    Comprova tres coses:
      1. la taula general contra si mateixa
      2. una fitxa contra si mateixa
      3. una fitxa contra una altra (A diu que B es bo i B diu que A es dolent)
    """
    gen = associacions()
    fit = associacions_fitxes()
    trobats = []

    def clau(n: str) -> str:
        return normalitza(n)

    # 1. taula general contra si mateixa
    for a, d in gen.items():
        for b in d["bons"]:
            for c, dd in gen.items():
                if clau(c) == clau(b) and clau(a) in [clau(x) for x in dd["dolents"]]:
                    trobats.append((a, c, "taula general: una fila els fa bons i l'altra dolents"))

    # 2. una fitxa contra si mateixa
    for slug, d in fit.items():
        for b in d["bons"]:
            if clau(b) in [clau(x) for x in d["dolents"]]:
                trobats.append((slug, b, "la mateixa fitxa el posa a bones i a dolentes"))

    # 3. fitxa contra fitxa
    for slug_a, da in fit.items():
        for b in da["bons"]:
            b_slug = ALIES.get(clau(b), clau(b)).replace(" ", "-")
            if b_slug in fit:
                db = fit[b_slug]
                if clau(slug_a) in [clau(x) for x in db["dolents"]] or \
                   slug_a in [clau(x).replace(" ", "-") for x in db["dolents"]]:
                    trobats.append((slug_a, b_slug,
                                    f"la fitxa de {slug_a} diu que es bo, i la de {b_slug} diu el contrari"))

    vist, out = set(), []
    for a, b, m in trobats:
        k = tuple(sorted([clau(a), clau(b)])) + (m,)
        if k not in vist:
            vist.add(k)
            out.append((a, b, m))
    return out


# ─────────────────────────── FITXES DE CULTIU ───────────────────────────
CAMPS = ["Nom científic", "Família botànica", "Cicle", "Profunditat d'arrel",
         "Exigència de nutrients", "Necessitats hídriques", "Rusticitat a Osona",
         "pH ideal", "Marc de plantació", "Profunditat de sembra",
         "Dies des de sembra fins a collita", "Conservació", "Reg", "Tutors"]


def fitxes() -> List[Dict]:
    out = []
    for fitxa in sorted((BASE / "07-fitxes-cultius").glob("*.md")):
        if fitxa.name.startswith("_"):
            continue
        txt = fitxa.read_text(encoding="utf-8")
        m = re.search(r"^#\s*Fitxa de cultiu:\s*(.+)$", txt, re.M)
        titol = _neteja(m.group(1)) if m else fitxa.stem
        nom = re.sub(r"\s*\(.*?\)\s*", "", titol).strip()
        cientific = ""
        mc = re.search(r"\(([^)]+)\)", titol)
        if mc:
            cientific = _neteja(mc.group(1))
        camps = {}
        for k in CAMPS:
            mk = re.search(r"\*\*" + re.escape(k) + r"\*\*:\s*(.+)", txt)
            if mk:
                camps[k] = _neteja(mk.group(1))
        assoc = associacions_fitxes().get(fitxa.stem, {"bons": [], "dolents": [], "discutits": []})
        ss = (BASE / "07-fitxes-cultius" / "img" / (fitxa.stem + ".svg"))
        out.append({
            "slug": fitxa.stem,
            "nom": nom,
            "titol": titol,
            "cientific": cientific,
            "camps": camps,
            "bons": assoc["bons"],
            "dolents": assoc["dolents"],
            "discutits": assoc.get("discutits", []),
            "svg": ss.name if ss.exists() else None,
        })
    return out


def _unics(llista: List[str]) -> List[str]:
    vist, out = set(), []
    for x in llista:
        if x.lower() not in vist:
            vist.add(x.lower())
            out.append(x)
    return out


# noms del calendari que no coincideixen amb el nom de la fitxa
ALIES = {
    "col": "col", "mongeta tendra": "mongeta", "mongeta seca": "mongeta",
    "basilic": "alfabrega", "bleda rave": "bleda", "bleda-rave": "bleda",
    "moniato": "moniato", "blat de moro": "blat-de-moro",
}
# cultius sense fitxa propia pero amb document: on els enviem
DOC_ALTERNATIU = {  # noms del calendari -> document
    "julivert": "07-fitxes-cultius/aromatiques.md", "cibulet": "07-fitxes-cultius/aromatiques.md", "anet": "07-fitxes-cultius/aromatiques.md",
    "coriantre": "07-fitxes-cultius/aromatiques.md", "comi": "07-fitxes-cultius/aromatiques.md", "salvia": "07-fitxes-cultius/aromatiques.md",
    "espigol": "07-fitxes-cultius/aromatiques.md", "orenga": "07-fitxes-cultius/aromatiques.md", "farigola": "07-fitxes-cultius/aromatiques.md",
    "menta": "07-fitxes-cultius/aromatiques.md", "romani": "07-fitxes-cultius/aromatiques.md",
}


def normalitza(nom: str) -> str:
    """Nom de cultiu del calendari -> clau normalitzada per buscar-hi la fitxa."""
    n = re.sub(r"\s*\(.*?\)\s*", " ", nom)      # fora parentesis
    n = n.replace("·", " ").strip().lower()
    n = re.sub(r"\s+", " ", n)
    return ALIES.get(n, n)


def index_cultius() -> Dict[str, Dict]:
    """{clau normalitzada: {'slug','nom','svg','doc'}} amb totes les fitxes."""
    idx = {}
    for f in fitxes():
        idx[normalitza(f["nom"])] = {"slug": f["slug"], "nom": f["nom"],
                                     "svg": f["svg"], "doc": f"07-fitxes-cultius/{f['slug']}.md"}
    return idx


def enllac_cultiu(nom: str) -> Dict[str, str]:
    """On ha d'anar un clic sobre aquest cultiu (fitxa propia o document alternatiu)."""
    clau = normalitza(nom)
    idx = index_cultius()
    if clau in idx:
        return {"tipus": "fitxa", **idx[clau]}
    if clau in DOC_ALTERNATIU:
        return {"tipus": "doc", "doc": DOC_ALTERNATIU[clau], "nom": nom, "slug": "", "svg": None}
    return {"tipus": "cap", "nom": nom, "slug": "", "svg": None, "doc": ""}


# ─────────────────────────── MES ───────────────────────────
def _hort_checklist():
    spec = importlib.util.spec_from_file_location("hc", BASE / "hort-checklist.py")
    hc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hc)
    return hc


def mes_info(mes: int) -> Dict:
    """Clima, tasques i dates clau del mes (del modul hort-checklist.py)."""
    try:
        hc = _hort_checklist()
        return {
            "clima": hc.notes_per_mes(mes),
            "tasques": [{"cat": t.get("cat", ""), "titol": t.get("titol", ""),
                         "desc": t.get("desc", ""), "prio": t.get("prio", 3)}
                        for t in hc.tasques_del_mes(mes)],
            "dates": [{"quan": a, "que": b} for a, b in hc.dates_clau_per_mes(mes)],
        }
    except Exception as e:  # pragma: no cover
        print(f"avís: no he pogut llegir hort-checklist.py: {e}")
        return {"clima": "", "tasques": [], "dates": []}


def pla_del_mes(mes: int) -> str:
    """Retorna el nom del fitxer de pla mensual per al mes donat, si existeix."""
    for f in sorted((BASE / "plans-mensuals").glob("*.md")):
        if re.match(rf"^\d{{4}}-{mes:02d}-", f.name):
            return f.name
    return ""
