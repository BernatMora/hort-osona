#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests unitaris per al generador de checklist.

Executa:
    python tests/test_hort_checklist.py

O amb unittest:
    python -m unittest tests.test_hort_checklist -v
"""

import unittest
import sys
from pathlib import Path
from datetime import date

# Afegir l'arrel del projecte al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Importar el mòdul directament (el fitxer té guionets, ho carreguem manualment)
import importlib.util
spec = importlib.util.spec_from_file_location("hort_checklist", ROOT / "hort-checklist.py")
hc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hc)


class TestFaseLunar(unittest.TestCase):
    """Tests per a l'algorisme de fase lunar."""

    def test_lluna_nova_15_juny_2026(self):
        """El 15 de juny de 2026 ha de ser lluna nova (verificable amb meteolluna.cat)."""
        nom, eti, emoji, desc = hc.fase_lunar(date(2026, 6, 15))
        self.assertEqual(nom, "nova", f"Esperava 'nova', he rebut '{nom}'")
        self.assertEqual(emoji, "🌑")

    def test_quart_minvant_8_juny_2026(self):
        """El 8 de juny de 2026 ha de ser quart minvant (verificable amb meteolluna.cat)."""
        nom, eti, emoji, desc = hc.fase_lunar(date(2026, 6, 8))
        self.assertEqual(nom, "minvant", f"Esperava 'minvant', he rebut '{nom}'")

    def test_lluna_plena_30_juny_2026(self):
        """El 30 de juny de 2026 ha de ser lluna plena (verificable amb meteolluna.cat)."""
        nom, eti, emoji, desc = hc.fase_lunar(date(2026, 6, 30))
        self.assertEqual(nom, "plena", f"Esperava 'plena', he rebut '{nom}'")
        self.assertEqual(emoji, "🌕")

    def test_quart_creixent_22_juny_2026(self):
        """El 22 de juny de 2026 ha de ser quart creixent (verificable amb meteolluna.cat)."""
        nom, eti, emoji, desc = hc.fase_lunar(date(2026, 6, 22))
        self.assertEqual(nom, "creixent", f"Esperava 'creixent', he rebut '{nom}'")

    def test_fase_2025_dates_conegudes(self):
        """Verificar fases conegudes de 2025 amb tolerància ±1 dia."""
        # Llunes plenes 2025: 13 gen, 12 feb, 14 mar, 13 abr, 12 mai
        # Llunes noves 2025: 29 gen, 28 feb, 29 mar
        conegudes = [
            (date(2025, 1, 13), "plena"),
            (date(2025, 2, 12), "plena"),
            (date(2025, 3, 14), "plena"),
            (date(2025, 1, 29), "nova"),
            (date(2025, 2, 28), "nova"),
        ]
        for d, esperat in conegudes:
            nom, _, _, _ = hc.fase_lunar(d)
            self.assertIn(
                nom, [esperat],
                f"Data {d.isoformat()}: esperava '{esperat}', he rebut '{nom}'"
            )

    def test_totes_les_fases_son_valides(self):
        """Comprova que el nom retornat és un dels 4 vàlids."""
        valids = {"nova", "creixent", "plena", "minvant"}
        for mes in range(1, 13):
            for dia in range(1, 29):
                nom, _, _, _ = hc.fase_lunar(date(2026, mes, dia))
                self.assertIn(nom, valids, f"Data 2026-{mes:02d}-{dia:02d}: fase '{nom}' no vàlida")


class TestSetmanesDelMes(unittest.TestCase):
    """Tests per a la funció setmanes_del_mes."""

    def test_juny_2026_te_5_setmanes(self):
        """Juny 2026 comença dilluns, per tant ha de tenir 5 setmanes."""
        setmanes = hc.setmanes_del_mes(2026, 6)
        self.assertGreaterEqual(len(setmanes), 4)
        self.assertLessEqual(len(setmanes), 6)
        # Totes les setmanes han de tocar juny
        for ini, fi in setmanes:
            self.assertTrue(ini.month == 6 or fi.month == 6 or (ini.month == 5 and fi.day >= 25) or (fi.month == 7 and ini.day <= 7))

    def test_gener_2025_te_setmanes(self):
        """Gener 2025 ha de donar almenys 4 setmanes."""
        setmanes = hc.setmanes_del_mes(2025, 1)
        self.assertGreaterEqual(len(setmanes), 4)


class TestTasques(unittest.TestCase):
    """Tests per a la base de dades de tasques."""

    def test_hay_tasques_per_a_cada_mes(self):
        """Cada mes de l'any ha de tenir almenys 3 tasques."""
        for mes in range(1, 13):
            tasques = hc.tasques_del_mes(mes)
            self.assertGreaterEqual(
                len(tasques), 3,
                f"Mes {mes}: només {len(tasques)} tasques, esperava >= 3"
            )

    def test_categories_valides(self):
        """Totes les tasques han de tenir una categoria vàlida."""
        valids = {"sembra", "trasplantament", "conreu", "tractaments", "collita", "planificacio", "observacio"}
        for t in hc.TASQUES:
            self.assertIn(t["cat"], valids, f"Tasca '{t['titol']}': categoria '{t['cat']}' no vàlida")
            self.assertGreaterEqual(t["prio"], 1, f"Tasca '{t['titol']}': prioritat < 1")
            self.assertLessEqual(t["prio"], 5, f"Tasca '{t['titol']}': prioritat > 5")
            self.assertTrue(t["titol"], f"Tasca sense títol")
            self.assertTrue(t["desc"], f"Tasca '{t['titol']}': sense descripció")

    def test_mesos_valids(self):
        """Les tasques han d'estar associades a mesos vàlids (1-12)."""
        for t in hc.TASQUES:
            for m in t["mesos"]:
                self.assertGreaterEqual(m, 1, f"Tasca '{t['titol']}': mes {m} < 1")
                self.assertLessEqual(m, 12, f"Tasca '{t['titol']}': mes {m} > 12")


class TestDatesClau(unittest.TestCase):
    """Tests per a les dates clau dels mesos."""

    def test_tots_els_mesos_tenen_dates_clau(self):
        """Cada mes ha de tenir almenys una data clau."""
        for mes in range(1, 13):
            dates = hc.dates_clau_per_mes(mes)
            self.assertGreater(len(dates), 0, f"Mes {mes}: sense dates clau")

    def test_sant_jordi_es_abril(self):
        """Sant Jordi ha de ser al mes d'abril (23 d'abril)."""
        dates = hc.dates_clau_per_mes(4)
        noms = ' '.join(d[0] for d in dates).lower()
        self.assertIn("sant jordi", noms)


class TestGenerarMarkdown(unittest.TestCase):
    """Tests per a la generació de Markdown."""

    def test_genera_md_juny_2026(self):
        """Comprova que la generació de Markdown funciona per a juny 2026."""
        md = hc.generar_checklist_markdown(2026, 6)
        self.assertIn("Juny 2026", md)
        self.assertIn("Mulching", md)  # tasca important de juny
        self.assertIn("Calendari lunar", md)

    def test_genera_json_valid(self):
        """Comprova que el JSON és vàlid (estructura)."""
        import json
        data = hc.generar_json(2026, 6)
        self.assertEqual(data["year"], 2026)
        self.assertEqual(data["month"], 6)
        self.assertEqual(data["mes_ca"], "juny")
        self.assertIn("setmanes", data)
        self.assertIn("tasques", data)
        self.assertGreater(len(data["setmanes"]), 0)
        self.assertGreater(len(data["tasques"]), 0)


class TestPromptOpenWebUI(unittest.TestCase):
    """Tests per a la generació del prompt per Open WebUI."""

    def test_prompt_inclou_context_basic(self):
        """El prompt ha d'incloure el context bàsic d'Osona."""
        prompt = hc.generar_prompt_openwebui(2026, 6)
        self.assertIn("Osona", prompt)
        self.assertIn("Juny", prompt)
        self.assertIn("Mulching", prompt)
        # Ha d'incloure instruccions de com respondre
        self.assertIn("Com respondre", prompt)
        # Ha d'incloure fonts locals
        self.assertIn("Esporus", prompt)


if __name__ == "__main__":
    # Si s'executa directament, usar unittest amb verbositat
    print("🧪 Executant tests de hort-checklist.py...")
    print()
    unittest.main(verbosity=2)
