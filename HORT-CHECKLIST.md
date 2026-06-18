# 🌱 HORT-CHECKLIST — Generador de checklist mensual de l'hort

Eina que genera automàticament cada mes:
- Una **checklist de tasques** de l'hort adaptades a Osona
- El **calendari lunar** del mes amb recomanacions biodinàmiques
- Un **prompt enriquit** per Open WebUI amb tot el context
- Una **pàgina web** integrada al lloc unificat (`#checklist`)

## Ús ràpid

```bash
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

# Consultar la fase lunar d'una data concreta
python hort-checklist.py --print-fase 2026-08-15
```

## Què inclou la checklist

1. **Context climàtic** del mes (per Osona, no genèric)
2. **Calendari lunar** amb totes les setmanes i fases amb recomanacions
3. **Tasques organitzades per categoria**:
   - 🌱 Sembra
   - 🌿 Trasplantament
   - 🛠️ Conreu
   - 🐞 Tractaments
   - 🧺 Collita
   - 📋 Planificació
   - 👀 Observació
4. Cada tasca té **prioritat** (1-5) i **descripció**
5. **Dates clau** a Osona (Sant Jordi, Mare de Déu d'Agost, etc.)

## Integració amb el lloc web

Cada vegada que executes `python site/build.py`:

1. El `build.py` importa `hort-checklist.py`
2. Genera les dades JSON del mes actual
3. Les desa a `site/checklist-data.json`
4. Les incrusta dins l'HTML generat
5. La pàgina d'inici mostra un **giny** amb:
   - Mes actual + fase lunar de la setmana en curs
   - Top tasca prioritària
   - Strip de les 4 primeres setmanes amb fases
6. La pàgina `#checklist` (o el botó "Obrir checklist completa") mostra:
   - Totes les tasques amb checkboxes persistents (localStorage)
   - Taula del calendari lunar
   - Dates clau d'Osona
   - Prompt per copiar a Open WebUI

## Algorisme de la fase lunar

Usa l'algorisme de cicles sinòdics amb referència a la lluna nova del
**6 de gener de 2000 18:14 UTC** (verificable). Període sinòdic: 29.530588 dies.
Precisió: ±1 dia (suficient per planificar tasques agrícoles).

```python
from hort-checklist import fase_lunar
from datetime import date
nom, eti, emoji, desc = fase_lunar(date(2026, 6, 15))
# ('nova', 'Lluna nova', '🌑', 'Repòs, planificar, netejar eines...')
```

## Afegir o modificar tasques

Edita la llista `TASQUES` al principi de `hort-checklist.py`. Cada tasca té:

```python
{
    "mesos": [6],                  # llista de mesos (1-12)
    "cat": "conreu",               # categoria (veure clau a dalt)
    "prio": 5,                     # prioritat 1-5
    "titol": "Mulching a tot l'hort (URGENT)",
    "desc": "5-10 cm de palla, gespa seca o fulles..."
}
```

## Notes

- L'eina **no requereix cap connexió a Internet** (les dades estan totes
  hard-coded al fitxer Python).
- Si vols un altre mes del qual no hi ha dades, l'afegixes a la llista
  `TASQUES` i regeneres.
- Les fases lunars serveixen com a **guia orientativa** — a Osona, la
  temperatura i les gelades manen sempre.

## Exemples

```bash
# Preparar el mes vinent
python hort-checklist.py --date 2026-07 --write

# Veure quin dia és bona per sembrar (prop de lluna nova o minvant)
python hort-checklist.py --print-fase 2026-09-15

# Generar el prompt per a una pregunta concreta a Open WebUI
python hort-checklist.py --prompt | pbcopy   # Mac
python hort-checklist.py --prompt | clip     # Windows
```
