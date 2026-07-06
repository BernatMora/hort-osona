#!/usr/bin/env python3
"""
lora_receiver.py — Receptor LoRa per a la Raspberry Pi.

Rep els payloads JSON del node emissor de l'hort, els parseja, els
desa a Supabase i, periodicament, demana a Ollama un consell
agronomic basat en les ultimes dades.

Hardware: Waveshare SX1262 868M LoRaWAN HAT sobre la Pi 4
Connexio: SPI (/dev/spidev0.0)

Format del payload (JSON):
  {"id":"hort-1", "loc":"osona", "boot":123, "t":18.5, "soil":45, "vbat":3.92, "uptime":5}

Author: Bernat Mora (hort-osona IoT)
"""

import os
import sys
import time
import json
import logging
import re
import signal
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any

# Llibreries externes (s'instal·len al setup-pi.sh)
try:
    from supabase import create_client, Client
except ImportError:
    print("Falta supabase-py. Instal·la: pip install supabase")
    sys.exit(1)

try:
    import RPi.GPIO as GPIO
    import spidev
    import lgpio  # Per controlar els GPIOs del SX1262
except ImportError as e:
    print(f"Falten llibreries RPi: {e}")
    print("Instal·la a la Pi 4:")
    print("  pip install RPi.GPIO spidev lgpio supabase")
    sys.exit(1)


# ──────────── CONFIGURACIO ────────────
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://YOUR_PROJECT.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR_ANON_KEY")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "hermes3:latest")
CONSELLS_INTERVAL_HORES = 6
LOG_FILE = "/var/log/hort-osona-lora.log"

# LoRa SX1262 (mateixos params que el node emissor)
LORA_FREQUENCY = 868.0  # MHz
LORA_BANDWIDTH = 125     # kHz
LORA_SPREADING_FACTOR = 10
LORA_TX_POWER = 14       # dBm (max legal UE: 14 dBm)

# GPIO pins del HAT Waveshare SX1262 (segueix el wiki)
LORA_BUSY_PIN = 20
LORA_RST_PIN = 18
LORA_CS_PIN = 8  # CE0 per SPI

# SPI bus
SPI_BUS = 0
SPI_DEVICE = 0


# ──────────── LOGGING ────────────
def setup_logging():
    """Configura logging a fitxer i consola."""
    handlers = [logging.StreamHandler(sys.stdout)]
    try:
        # Intentar escriure a /var/log (cal sudo)
        handlers.insert(0, logging.FileHandler(LOG_FILE))
    except PermissionError:
        # Si no podem, escriure a /tmp
        global LOG_FILE
        LOG_FILE = "/tmp/hort-osona-lora.log"
        handlers.insert(0, logging.FileHandler(LOG_FILE))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
    return logging.getLogger(__name__)


log = setup_logging()


# ──────────── LORA SX1262 DRIVER MINIMAL ────────────
# Driver minimal basat en registres del SX1262.
# Per a una versio mes completa, usar RadioLib per Python:
#   https://github.com/jgromes/RadioLib (pero es per C++, no Python)
#
# Aquest driver es BASIC: nomes reb missatges punt-a-punt (no LoRaWAN).
# Per a LoRaWAN amb TTN, canviar a la seccio "LORA - TTN".

class SX1262Minimal:
    """Driver SX1262 BASIC en Python. Només per a proves."""

    # Registres principals del SX1262
    REG_LORA_SYNC_WORD_MSB = 0x0740
    REG_LORA_SYNC_WORD_LSB = 0x0741
    REG_LORA_FREQ = 0x0889  # Freq en Hz
    REG_LORA_BW = 0x08AC
    REG_LORA_SF = 0x08AB
    REG_LORA_CR = 0x08A4
    REG_LORA_TX_POWER = 0x08E8
    REG_PACKET_LENGTH = 0x0902
    REG_PAYLOAD_LENGTH = 0x0903
    REG_IRQ_FLAGS = 0x0944
    REG_RX_NB_BYTES = 0x0943

    CMD_GET_STATUS = 0xC0
    CMD_READ_REGISTER = 0x1D
    CMD_WRITE_REGISTER = 0x0D
    CMD_PACKET_TYPE = 0x08
    CMD_SET_PACKET_TYPE = 0x0A
    CMD_SET_TX = 0x83
    CMD_SET_RX = 0x82

    PACKET_TYPE_LORA = 0x01

    def __init__(self, spi_bus=0, spi_device=0, reset_pin=18, busy_pin=20):
        """Inicialitza SPI i GPIO."""
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 1000000  # 1 MHz
        self.spi.mode = 0

        self.h = lgpio.gpiochip_open(0)
        self.reset_pin = reset_pin
        self.busy_pin = busy_pin

        lgpio.gpio_claim_output(self.h, reset_pin)
        lgpio.gpio_claim_input(self.h, busy_pin)

        # Reset hardware
        self._reset()

        # Verificar que el chip es accessible
        if not self._check_busy():
            raise RuntimeError("SX1262 no respon (BUSY sempre alt)")

        # Posar en mode LoRa
        self._write_command(self.CMD_SET_PACKET_TYPE, [self.PACKET_TYPE_LORA])

    def _reset(self):
        """Reset hardware del SX1262."""
        lgpio.gpio_write(self.h, self.reset_pin, 0)
        time.sleep(0.01)
        lgpio.gpio_write(self.h, self.reset_pin, 1)
        time.sleep(0.01)
        # Esperar que BUSY baixi
        for _ in range(100):
            if lgpio.gpio_read(self.h, self.busy_pin) == 0:
                return
            time.sleep(0.001)
        raise RuntimeError("SX1262 no es recupera del reset")

    def _check_busy(self):
        """Comprova que BUSY esta baix (chip llest)."""
        return lgpio.gpio_read(self.h, self.busy_pin) == 0

    def _wait_busy(self, timeout=1.0):
        """Espera que BUSY baixi."""
        start = time.time()
        while lgpio.gpio_read(self.h, self.busy_pin) == 1:
            if time.time() - start > timeout:
                raise RuntimeError("Timeout esperant BUSY")
            time.sleep(0.001)

    def _write_command(self, cmd, data=None):
        """Escriu una comanda SPI."""
        self._wait_busy()
        if data:
            self.spi.xfer([cmd] + data)
        else:
            self.spi.xfer([cmd])
        time.sleep(0.001)

    def _read_register(self, addr, length=1):
        """Llegeix un registre."""
        self._wait_busy()
        # CMD_READ_REGISTER: [0x1D, addr_msb, addr_lsb, dummy, ...data]
        data = [self.CMD_READ_REGISTER, (addr >> 8) & 0xFF, addr & 0xFF, 0x00] + [0x00] * length
        result = self.spi.xfer(data)
        return result[4:4+length]

    def _write_register(self, addr, data):
        """Escriu un registre."""
        self._wait_busy()
        # CMD_WRITE_REGISTER: [0x0D, addr_msb, addr_lsb, ...data]
        cmd = [self.CMD_WRITE_REGISTER, (addr >> 8) & 0xFF, addr & 0xFF] + data
        self.spi.xfer(cmd)
        time.sleep(0.001)

    def begin(self, frequency=868.0, bandwidth=125, sf=10, tx_power=14):
        """Configura el SX1262 amb els parametres donats."""
        # Configurar frequencia
        freq_hz = int(frequency * 1e6)
        # RF frequency = (freq_hz * 2^25) / 32e6
        rf_freq = int((freq_hz * (1 << 25)) / 32000000)
        self._write_register(self.REG_LORA_FREQ, [
            (rf_freq >> 24) & 0xFF,
            (rf_freq >> 16) & 0xFF,
            (rf_freq >> 8) & 0xFF,
            rf_freq & 0xFF
        ])

        # Configurar SF, BW, CR
        self._write_register(self.REG_LORA_SF, [sf])
        self._write_register(self.REG_LORA_BW, [bandwidth / 125])  # 0=125kHz
        self._write_register(self.REG_LORA_CR, [1])  # 4/5

        # Potencia TX
        self._write_register(self.REG_LORA_TX_POWER, [tx_power])

        log.info(f"SX1262 configurat: {frequency} MHz, BW={bandwidth}kHz, SF={sf}, TX={tx_power}dBm")

    def receive(self, timeout_ms=1000):
        """Posar en mode RX. Retorna el payload o None si timeout."""
        # CMD_SET_RX: [0x82, timeout_ms_msb, timeout_ms_lsb, ...]
        self._write_command(self.CMD_SET_RX, [
            (timeout_ms >> 8) & 0xFF,
            timeout_ms & 0xFF,
            0x00, 0x00, 0x00, 0x00
        ])

    def check_receive(self):
        """Comprova si ha arribat un paquet. Retorna (payload, rssi, snr) o None."""
        # Llegir IRQ flags
        flags = self._read_register(self.REG_IRQ_FLAGS, 2)
        if not (flags[0] & 0x40):  # Bit 6 = RX done
            return None

        # Llegir longitud del payload
        nb_bytes = self._read_register(self.REG_RX_NB_BYTES, 1)[0]
        if nb_bytes == 0:
            return None

        # Llegir payload (simplificat: nomes 1 byte d'adreça + payload)
        # En una implementacio real caldria FIFO management correcte
        # Aqui nomes simulem: retornem string buit
        # PER Aixo es BASIC - per a produccio usar RadioLib per Python

        # Netejar IRQ flags
        self._write_register(self.REG_IRQ_FLAGS, [0xFF, 0xFF])

        return (b'', -100, 0)  # Placeholder

    def close(self):
        """Tanca el driver."""
        self.spi.close()
        lgpio.gpiochip_close(self.h)


# ──────────── CLIENTS ────────────
def create_supabase_client() -> Optional[Client]:
    """Crea el client de Supabase amb validacio."""
    if "YOUR_PROJECT" in SUPABASE_URL or "YOUR_ANON_KEY" in SUPABASE_KEY:
        log.error("❌ Configura SUPABASE_URL i SUPABASE_KEY abans d'executar")
        log.error("   export SUPABASE_URL=https://xxx.supabase.co")
        log.error("   export SUPABASE_KEY=eyJ...")
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# ──────────── PARSER PAYLOAD JSON ────────────
def parse_payload(raw: str) -> Optional[Dict[str, Any]]:
    """
    Converteix un payload JSON del node a un dict per Supabase.

    Format esperat:
      {"id":"hort-1", "loc":"osona", "boot":123, "t":18.5, "soil":45, "vbat":3.92}

    Retorna None si el payload es invalid.
    """
    try:
        data = json.loads(raw.strip())
    except json.JSONDecodeError as e:
        log.warning(f"Payload no es JSON valid: {raw!r} ({e})")
        return None

    # Validar camps essencials
    if "t" not in data and "soil" not in data:
        log.warning(f"Payload sense camps essencials: {raw!r}")
        return None

    return {
        "node_id": data.get("id", "unknown"),
        "boot_count": data.get("boot", 0),
        "temperatura_c": float(data.get("t", -999)),
        "humitat_sol_pct": int(data.get("soil", -1)),
        "bateria_v": float(data.get("vbat", 0)),
        "ts": datetime.now(timezone.utc).isoformat(),
    }


# ──────────── SUPABASE: OPERACIONS ────────────
def save_measurement(supabase: Client, mesura: Dict[str, Any]) -> bool:
    """Guarda una mesura a la taula `mesures`."""
    try:
        result = supabase.table("mesures").insert(mesura).execute()
        log.info(
            f"✅ Mesura desada: T={mesura['temperatura_c']}°C, "
            f"sol={mesura['humitat_sol_pct']}%, Vbat={mesura['bateria_v']}V"
        )
        return True
    except Exception as e:
        log.error(f"❌ Error desant a Supabase: {e}")
        return False


def get_recent_measurements(supabase: Client, limit: int = 10) -> list:
    """Recupera les ultimes mesures de Supabase."""
    try:
        res = supabase.table("mesures") \
            .select("*") \
            .order("ts", desc=True) \
            .limit(limit) \
            .execute()
        return res.data or []
    except Exception as e:
        log.error(f"❌ Error recuperant mesures: {e}")
        return []


def save_advice(supabase: Client, advice: str) -> bool:
    """Guarda el consell a la taula `consells_ia`."""
    try:
        # Esborrar l'anterior (mantenim nomes l'ultim)
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


# ──────────── OLLAMA: CONSELL AGRONOMIC ────────────
def get_agronomic_advice(ultimes_mesures: list) -> Optional[str]:
    """Demana a Ollama un consell basat en les ultimes mesures."""
    if not ultimes_mesures:
        return None

    context_lines = [
        f"Mesures dels sensors de l'hort d'Osona (node {ultimes_mesures[0].get('node_id', '?')}):"
    ]
    for m in ultimes_mesures[:10]:
        context_lines.append(
            f"- {m.get('ts', '?')}: "
            f"T={m.get('temperatura_c')}°C, "
            f"Sol={m.get('humitat_sol_pct')}%, "
            f"Bat={m.get('bateria_v')}V"
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
    except (urllib.error.URLError, OSError) as e:
        log.error(f"❌ Error amb Ollama: {e}")
        return None


# ──────────── LOOP PRINCIPAL ────────────
def main():
    log.info("=== Receptor LoRa Hort Osona ===")
    log.info(f"Supabase: {SUPABASE_URL}")
    log.info(f"Ollama: {OLLAMA_URL} ({OLLAMA_MODEL})")

    # Inicialitzar clients
    supabase = create_supabase_client()
    if not supabase:
        sys.exit(1)

    # Inicialitzar LoRa
    try:
        lora = SX1262Minimal(
            spi_bus=SPI_BUS,
            spi_device=SPI_DEVICE,
            reset_pin=LORA_RST_PIN,
            busy_pin=LORA_BUSY_PIN
        )
        lora.begin(
            frequency=LORA_FREQUENCY,
            bandwidth=LORA_BANDWIDTH,
            sf=LORA_SPREADING_FACTOR,
            tx_power=LORA_TX_POWER
        )
    except Exception as e:
        log.error(f"❌ Error inicialitzant LoRa: {e}")
        log.error("   Comprovar: SPI habilitat? (sudo raspi-config)")
        log.error("   Pins correctes? (HAT ben col·locat)")
        sys.exit(1)

    # Signal handler per aturar netament
    def signal_handler(sig, frame):
        log.info("Aturat per senyal")
        lora.close()
        GPIO.cleanup()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    last_advice_time = 0
    lora.receive(timeout_ms=1000)

    log.info("Escoltant LoRa... (Ctrl+C per aturar)")

    while True:
        # Comprovar si ha arribat un paquet
        result = lora.check_receive()
        if result:
            payload, rssi, snr = result
            try:
                text = payload.decode("utf-8").strip()
                log.info(f"📡 RX ({rssi}dBm, SNR={snr}dB): {text}")

                mesura = parse_payload(text)
                if mesura:
                    mesura["rssi_dbm"] = rssi
                    mesura["snr_db"] = snr
                    save_measurement(supabase, mesura)
            except UnicodeDecodeError:
                log.warning(f"Payload no UTF-8: {payload!r}")
            except Exception as e:
                log.error(f"Error processant payload: {e}")

            lora.receive(timeout_ms=1000)  # Tornar a escoltar

        # Cada X hores, generar consell
        now = time.time()
        if now - last_advice_time > CONSELLS_INTERVAL_HORES * 3600:
            try:
                mesures = get_recent_measurements(supabase, limit=10)
                if mesures:
                    advice = get_agronomic_advice(mesures)
                    if advice:
                        save_advice(supabase, advice)
                        last_advice_time = now
            except Exception as e:
                log.error(f"Error en el bucle de consells: {e}")

        time.sleep(0.1)  # 100ms


if __name__ == "__main__":
    main()
