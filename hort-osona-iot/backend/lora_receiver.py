#!/usr/bin/env python3
"""
lora_receiver.py — Receptor LoRa per a la Raspberry Pi.

Rep els payloads CSV del node emissor de l'hort, els parseja, els
desa a Supabase i, periodicament, demana a Ollama un consell
agronomic basat en les ultimes dades.

Hardware: Waveshare SX1262 868M LoRa HAT sobre la Pi 4
Connexio: SPI (/dev/spidev0.0)

Author: Bernat Mora (hort-osona IoT)
"""

import os
import sys
import time
import json
import logging
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Llibreries externes
try:
    from supabase import create_client, Client
except ImportError:
    print("Falta supabase. Instal·la: pip install supabase")
    sys.exit(1)

try:
    import RPi.GPIO as GPIO
    from SX126x import SX126x  # Llibreria Waveshare oficial
except ImportError:
    print("Falten llibreries RPi. Instal·la a la Pi 4:")
    print("  pip install RPi.GPIO spidev")
    print("  git clone https://github.com/lesept777/SX126x.git && cd SX126x && sudo python3 setup.py install")
    sys.exit(1)


# ──────────── CONFIGURACIO ────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://YOUR_PROJECT.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR_ANON_KEY")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "hermes3:latest")
CONSELLS_INTERVAL_HORES = 6  # Cada quantes hores demanem un consell a Ollama
LOG_FILE = "/var/log/hort-osona-lora.log"

# LoRa SX1262 (mateixos params que el node emissor)
LORA_FREQUENCY = 868
LORA_BANDWIDTH = 125
LORA_SPREADING_FACTOR = 10
LORA_TX_POWER = 17

# ──────────── LOGGING ────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)


# ──────────── CLIENTS ────────────
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ──────────── PARSER PAYLOAD CSV ────────────
PAYLOAD_RE = re.compile(
    r"T:([-\d.]+),H:([-\d.]+),P:([-\d.]+),S:(\d+),BAT:([-\d.]+)"
)

def parse_payload(raw: str) -> dict | None:
    """Converteix 'T:18.5,H:62.3,P:1013.2,S:45,BAT:3.92' a dict."""
    m = PAYLOAD_RE.match(raw.strip())
    if not m:
        log.warning(f"Payload mal format: {raw!r}")
        return None
    try:
        return {
            "temperatura_c": float(m.group(1)),
            "humitat_amb_pct": float(m.group(2)),
            "pressio_hpa": float(m.group(3)),
            "humitat_sol_pct": int(m.group(4)),
            "bateria_v": float(m.group(5)),
            "ts": datetime.now(timezone.utc).isoformat(),
            "node_id": "hort-osona-01",
        }
    except ValueError as e:
        log.error(f"Error parsejant payload: {e}")
        return None


# ──────────── SUPABASE: INSERT mesura ────────────
def save_measurement(mesura: dict) -> bool:
    """Guarda una mesura a la taula `mesures` de Supabase."""
    try:
        result = supabase.table("mesures").insert(mesura).execute()
        log.info(f"✅ Mesura desada: {mesura['temperatura_c']}°C, {mesura['humitat_sol_pct']}% sol")
        return True
    except Exception as e:
        log.error(f"❌ Error desant a Supabase: {e}")
        return False


# ──────────── OLLAMA: CONSELL AGRONOMIC ────────────
def get_agronomic_advice(ultimes_mesures: list[dict]) -> str | None:
    """Demana a Ollama un consell basat en les ultimes mesures."""
    if not ultimes_mesures:
        return None

    # Resum de les ultimes mesures
    context_lines = [
        f"Mesures dels sensors de l'hort d'Osona (node {ultimes_mesures[0]['node_id']}):"
    ]
    for m in ultimes_mesures[-10:]:  # Ultimes 10
        context_lines.append(
            f"- {m['ts']}: T={m['temperatura_c']}°C, "
            f"H_amb={m['humitat_amb_pct']}%, P={m['pressio_hpa']}hPa, "
            f"Sol={m['humitat_sol_pct']}%, Bat={m['bateria_v']}V"
        )
    context = "\n".join(context_lines)

    prompt = f"""{context}

Ets un expert en horticultura ecològica de la comarca d'Osona (Catalunya).
Analitza les dades dels sensors i dona 2-3 recomanacions PRACTIQUES i CURTES
(amb prioritat: ⚠️ URGENT, 🟠 ATENCIO, 🟢 OK).

Inclou:
- Estat general de l'hort
- Si cal regar (basant-te en humitat del sol)
- Si hi ha risc de gelada, calor extrema o malaltia
- Alertes tecniques (bateria baixa, sensor erroni)

Respon en catala, menys de 200 paraules, format llista."""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 400}
    }

    try:
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
            return data.get("response", "").strip()
    except Exception as e:
        log.error(f"❌ Error amb Ollama: {e}")
        return None


def save_advice(advice: str) -> bool:
    """Guarda el consell a la taula `consells_ia` (substituint l'anterior)."""
    try:
        # Substituir l'anterior (mantenim nomes l'ultim)
        supabase.table("consells_ia").delete().gt("id", 0).execute()
        # Inserir el nou
        supabase.table("consells_ia").insert({
            "ts": datetime.now(timezone.utc).isoformat(),
            "consell": advice,
            "font": OLLAMA_MODEL
        }).execute()
        log.info("✅ Consell desat a Supabase")
        return True
    except Exception as e:
        log.error(f"❌ Error desant consell: {e}")
        return False


# ──────────── LORA: RECEPCIO ────────────
def setup_lora() -> SX126x:
    """Configura el HAT Waveshare SX1262."""
    # GPIO pins (segueix el wiki Waveshare)
    BUSY_PIN = 20
    RST_PIN = 18
    DIO1_PIN = -1  # No sempre es fa servir
    TXEN_PIN = -1
    RXEN_PIN = -1

    lora = SX126x(
        spi_bus=0,
        spi_cs=0,
        reset_pin=RST_PIN,
        busy_pin=BUSY_PIN,
        dio1_pin=DIO1_PIN,
        txen_pin=TXEN_PIN,
        rxen_pin=RXEN_PIN,
        lora={
            "frequency": LORA_FREQUENCY,
            "spreading_factor": LORA_SPREADING_FACTOR,
            "bandwidth": LORA_BANDWIDTH,
            "coding_rate": 1,
            "tx_power": LORA_TX_POWER
        }
    )

    log.info("LoRa SX1262 inicialitzat correctament")
    return lora


def on_receive(lora: SX126x, payload: bytes, rssi: float, snr: float):
    """Callback quan arriba un paquet."""
    try:
        text = payload.decode("utf-8").strip()
    except UnicodeDecodeError:
        log.warning(f"Payload no UTF-8: {payload!r}")
        return

    log.info(f"📡 RX ({rssi}dBm, SNR={snr}dB): {text}")

    mesura = parse_payload(text)
    if mesura is None:
        return

    # Afegir metadades LoRa
    mesura["rssi_dbm"] = rssi
    mesura["snr_db"] = snr

    save_measurement(mesura)


# ──────────── LOOP PRINCIPAL ────────────
def main():
    log.info("=== Receptor LoRa Hort Osona ===")
    log.info(f"Supabase: {SUPABASE_URL}")
    log.info(f"Ollama: {OLLAMA_URL} ({OLLAMA_MODEL})")

    # Inicialitzar LoRa
    lora = setup_lora()
    lora.set_callback(on_receive)
    lora.receive()  # Mode recepcio continua

    last_advice_time = 0  # timestamp ultim consell

    try:
        while True:
            time.sleep(60)  # Cada minut, comprovem

            # Cada CONSELLS_INTERVAL_HORES, demanem un consell a Ollama
            now = time.time()
            if now - last_advice_time > CONSELLS_INTERVAL_HORES * 3600:
                try:
                    res = supabase.table("mesures") \
                        .select("*") \
                        .order("ts", desc=True) \
                        .limit(10) \
                        .execute()
                    mesures = res.data
                    if mesures:
                        advice = get_agronomic_advice(mesures)
                        if advice:
                            save_advice(advice)
                            last_advice_time = now
                except Exception as e:
                    log.error(f"Error en el bucle de consells: {e}")

    except KeyboardInterrupt:
        log.info("Aturat per l'usuari")
        lora.close()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
