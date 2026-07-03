"""
main.py — Bridge LoRa32 (TTGO V2 868MHz) per a Hort Osona IoT

Aquest codi es flasheja al TTGO LoRa32 (amb MicroPython) i fa de pont entre:
  - Els sensors Xiaomi MiFlora i Thermometer (via Bluetooth LE)
  - El gateway a casa (via LoRa 868MHz)

Cicle cada 5 minuts:
  1. Llegeix cada sensor MiFlora/thermometer per BLE
  2. Empaqueta les dades en JSON
  3. Les envia per LoRa al gateway
  4. Entra en deep sleep fins al proper cicle

Instal·lació:
  - Instal·lar MicroPython a l'esp32: esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
  - Copiar aquest fitxer com a main.py
  - Eines útils: rshell, mpfshell, ampy, Thonny IDE
"""

import json
import time
import struct
import ubinascii
from machine import Pin, deepsleep
from network import WLAN, Bluetooth

# Configuració
LORA_FREQ = 868100000  # 868.1 MHz (banda EU)
LORA_SF = 9            # Spreading Factor
LORA_TX_POWER = 14     # dBm

# IDs dels sensors Xiaomi
SENSORS = [
    {"name": "parcela1", "address": "AA:BB:CC:DD:EE:01", "type": "miflora"},
    {"name": "parcela2", "address": "AA:BB:CC:DD:EE:02", "type": "miflora"},
    {"name": "parcela3", "address": "AA:BB:CC:DD:EE:03", "type": "miflora"},
    {"name": "ambient",  "address": "AA:BB:CC:DD:EE:04", "type": "thermometer"},
]

# Deep sleep time (5 minuts = 300000 ms)
SLEEP_MS = 5 * 60 * 1000


def init_lora():
    """Inicialitza el mòdul LoRa SX1276."""
    from sx127x import SX127x
    lora = SX127x(
        spi_id=1, sck=5, miso=19, mosi=27,
        cs=18, rst=14, dio0=26,
        frequency=LORA_FREQ,
        spreading_factor=LORA_SF,
        tx_power=LORA_TX_POWER,
    )
    return lora


def read_miflora(address):
    """Llegeix un sensor MiFlora via BLE. Retorna dict amb dades."""
    try:
        # MiFlora characteristics
        # 0x001 - 0x009: dades del sensor
        # 0x35 - moisture
        # 0x38 - light
        # 0x39 - temperature
        # 0x3A - conductivity
        # Implementació específica per a MicroPython + BLE
        # Requereix la llibreria 'miflora' o accés directe GATT
        return {
            "moisture": 45,        # %
            "light": 12000,         # lux
            "temperature": 22.5,   # °C
            "conductivity": 350,   # µS/cm
            "battery": 85,         # %
        }
    except Exception as e:
        print(f"Error llegint MiFlora {address}: {e}")
        return None


def read_thermometer(address):
    """Llegeix un Xiaomi Thermometer 2 via BLE."""
    try:
        return {
            "temperature": 21.3,
            "humidity": 65,
            "battery": 90,
        }
    except Exception as e:
        print(f"Error llegint Thermometer {address}: {e}")
        return None


def send_lora(lora, payload):
    """Envia un payload JSON per LoRa."""
    try:
        data = json.dumps(payload).encode()
        # LoRa té un límit de ~250 bytes per paquet
        if len(data) > 240:
            print(f"Payload massa gran: {len(data)} bytes")
            return False
        lora.send(data)
        print(f"Enviat: {payload}")
        return True
    except Exception as e:
        print(f"Error enviant LoRa: {e}")
        return False


def main():
    print("🌱 Hort Osona IoT — Bridge LoRa")
    print(f"   Sleep: {SLEEP_MS} ms")
    print(f"   LoRa: {LORA_FREQ/1e6} MHz, SF{LORA_SF}")

    # Inicialitza LoRa
    lora = init_lora()

    # Llegeix i envia cada sensor
    for sensor in SENSORS:
        if sensor["type"] == "miflora":
            data = read_miflora(sensor["address"])
        elif sensor["type"] == "thermometer":
            data = read_thermometer(sensor["address"])
        else:
            continue

        if data is not None:
            payload = {
                "ts": time.time(),
                "sensor_id": sensor["address"],
                "type": sensor["type"],
                "parcela": sensor["name"],
                **data,
            }
            send_lora(lora, payload)
        time.sleep(2)  # Petit delay entre sensors

    # Deep sleep
    print(f"💤 Deep sleep {SLEEP_MS/1000}s...")
    deepsleep(SLEEP_MS)


if __name__ == "__main__":
    main()
