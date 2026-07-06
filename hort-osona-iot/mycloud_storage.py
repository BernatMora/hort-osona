#!/usr/bin/env python3
"""
mycloud_storage.py — Emmagatzematge local de dades IoT al My Cloud Home.

Aquest modul permet que la Raspberry Pi guardi les dades del node
LoRa al My Cloud Home a traves de la xarxa local (SMB/CIFS).

Us:
    from mycloud_storage import MyCloudStorage
    storage = MyCloudStorage("/mnt/mycloudhome/hort-osona")
    storage.save_measurement({"temperatura_c": 18.5, "humitat_sol_pct": 45, ...})

Configuracio:
    - El My Cloud Home ha d'estar muntat a la RPi amb CIFS
    - Veure: setup-mycloudhome.sh
"""

import json
import logging
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

# Configuracio per defecte
DEFAULT_BASE_PATH = "/mnt/mycloudhome/hort-osona"
DB_FILENAME = "data/db.sqlite"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)


class MyCloudStorage:
    """Emmagatzematge de dades al My Cloud Home."""

    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = os.environ.get("HORT_MYCLOUD_PATH", DEFAULT_BASE_PATH)
        self.base_path = Path(base_path)
        self.db_path = self.base_path / DB_FILENAME
        self._init_storage()

    def _init_storage(self):
        """Crea les carpetes i la BD si no existeixen."""
        if not self.base_path.exists():
            log.warning(f"Path no existeix: {self.base_path}")
            log.warning("El My Cloud Home esta muntat?")
            log.warning("  mount -t cifs //192.168.100.48/Public /mnt/mycloudhome -o guest")
            return

        # Crear carpetes necessaries
        (self.base_path / "data/2026").mkdir(parents=True, exist_ok=True)
        (self.base_path / "data/2027").mkdir(parents=True, exist_ok=True)
        (self.base_path / "data/backups").mkdir(parents=True, exist_ok=True)

        # Inicialitzar BD SQLite
        self._init_db()
        log.info(f"Storage inicialitzat a {self.base_path}")

    def _init_db(self):
        """Crea la taula de mesures si no existeix."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS mesures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    node_id TEXT,
                    temperatura_c REAL,
                    humitat_sol_pct INTEGER,
                    humitat_amb_pct REAL,
                    pressio_hpa REAL,
                    bateria_v REAL,
                    rssi_dbm REAL,
                    snr_db REAL,
                    boot_count INTEGER,
                    raw_json TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS consells_ia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    consell TEXT,
                    font TEXT
                )
            """)
            # Index per a cerques per data
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_mesures_ts
                ON mesures(ts DESC)
            """)
            conn.commit()
            conn.close()
        except sqlite3.OperationalError as e:
            log.error(f"No es pot accedir a la BD: {e}")

    def save_measurement(self, mesura: Dict[str, Any]) -> bool:
        """
        Guarda una mesura a la BD SQLite i com a JSONL mensual.

        Format del fitxer: data/AAAA/mm-mes-NODE.jsonl
        """
        if not self.base_path.exists():
            log.error(f"Path no existeix: {self.base_path}")
            return False

        # 1. Guardar a SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                INSERT INTO mesures (
                    ts, node_id, temperatura_c, humitat_sol_pct,
                    humitat_amb_pct, pressio_hpa, bateria_v,
                    rssi_dbm, snr_db, boot_count, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mesura.get("ts", datetime.now(timezone.utc).isoformat()),
                mesura.get("node_id", "unknown"),
                mesura.get("temperatura_c"),
                mesura.get("humitat_sol_pct"),
                mesura.get("humitat_amb_pct"),
                mesura.get("pressio_hpa"),
                mesura.get("bateria_v"),
                mesura.get("rssi_dbm"),
                mesura.get("snr_db"),
                mesura.get("boot_count"),
                json.dumps(mesura, ensure_ascii=False)
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            log.error(f"Error guardant a SQLite: {e}")
            return False

        # 2. Guardar a fitxer JSONL per mes
        try:
            now = datetime.now()
            year = now.year
            month_name = now.strftime("%m-%B").lower()  # "07-july"
            month_ca = {
                1: "gener", 2: "febrer", 3: "marc", 4: "abril",
                5: "maig", 6: "juny", 7: "juliol", 8: "agost",
                9: "setembre", 10: "octubre", 11: "novembre", 12: "desembre"
            }
            month_str = f"{now.month:02d}-{month_ca[now.month]}"
            node_id = mesura.get("node_id", "unknown")

            year_dir = self.base_path / "data" / str(year)
            year_dir.mkdir(exist_ok=True)
            jsonl_file = year_dir / f"{month_str}-{node_id}.jsonl"

            with open(jsonl_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(mesura, ensure_ascii=False) + "\n")
        except Exception as e:
            log.error(f"Error guardant JSONL: {e}")
            return False

        log.info(
            f"✅ Mesura desada: T={mesura.get('temperatura_c')}°C, "
            f"sol={mesura.get('humitat_sol_pct')}%, Vbat={mesura.get('bateria_v')}V"
        )
        return True

    def get_recent_measurements(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Recupera les ultimes mesures."""
        if not self.db_path.exists():
            return []
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM mesures
                ORDER BY ts DESC
                LIMIT ?
            """, (limit,))
            rows = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return rows
        except Exception as e:
            log.error(f"Error recuperant mesures: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadistiques de la BD."""
        if not self.db_path.exists():
            return {"error": "BD no accessible"}
        try:
            conn = sqlite3.connect(self.db_path)
            total = conn.execute("SELECT COUNT(*) FROM mesures").fetchone()[0]
            last = conn.execute(
                "SELECT ts FROM mesures ORDER BY ts DESC LIMIT 1"
            ).fetchone()
            conn.close()
            return {
                "total_mesures": total,
                "ultima_mesura": last[0] if last else None,
                "db_path": str(self.db_path),
                "db_size_mb": round(self.db_path.stat().st_size / 1024 / 1024, 2)
                    if self.db_path.exists() else 0
            }
        except Exception as e:
            return {"error": str(e)}

    def save_advice(self, advice: str, font: str = "ollama") -> bool:
        """Guarda un consell de IA."""
        if not self.db_path.exists():
            return False
        try:
            conn = sqlite3.connect(self.db_path)
            # Esborrar l'anterior
            conn.execute("DELETE FROM consells_ia")
            # Inserir el nou
            conn.execute("""
                INSERT INTO consells_ia (ts, consell, font)
                VALUES (?, ?, ?)
            """, (datetime.now(timezone.utc).isoformat(), advice, font))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            log.error(f"Error guardant consell: {e}")
            return False


# Test
if __name__ == "__main__":
    storage = MyCloudStorage()
    print("\n=== Estadistiques ===")
    print(json.dumps(storage.get_stats(), indent=2, ensure_ascii=False))

    # Exemple de mesura
    exemple = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "node_id": "hort-1",
        "temperatura_c": 18.5,
        "humitat_sol_pct": 45,
        "humitat_amb_pct": 62.0,
        "pressio_hpa": 1013.2,
        "bateria_v": 3.92,
        "rssi_dbm": -85,
        "snr_db": 9.5,
        "boot_count": 1,
    }
    print(f"\n=== Exemple de mesura ===")
    print(json.dumps(exemple, indent=2, ensure_ascii=False))

    # Guardar
    if storage.base_path.exists():
        storage.save_measurement(exemple)
        print("\n✅ Mesura d'exemple desada")
    else:
        print(f"\n⚠️  Path {storage.base_path} no existeix")
        print("   Cal muntar el My Cloud Home primer")
