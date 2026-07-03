"""
gateway.py — Gateway LoRa→MQTT per a Hort Osona IoT

Aquest codi es posa al segon TTGO LoRa32, situat a casa, connectat per USB
a la Raspberry Pi. Rep els paquets LoRa del bridge i els publica al broker
MQTT del Mac (on el backend Python els escolta).

Instal·lació:
  - Mateixa instal·lació que el bridge (MicroPython a l'ESP32)
  - Connectar per USB a la Raspberry Pi
  - El gateway escolta contínuament per LoRa i envia per UART (MQTT via script extern)
"""

import json
import time
from machine import Pin, UART

# Configuració
LORA_FREQ = 868100000  # Ha de coincidir amb el bridge
LORA_SF = 9

# UART per comunicar amb la Raspberry (via USB)
# baudrate 115200, format JSON
UART_BAUDRATE = 115200


def init_lora():
    from sx127x import SX127x
    lora = SX127x(
        spi_id=1, sck=5, miso=19, mosi=27,
        cs=18, rst=14, dio0=26,
        frequency=LORA_FREQ,
        spreading_factor=LORA_SF,
    )
    return lora


def main():
    print("🌱 Hort Osona IoT — Gateway LoRa → MQTT")

    uart = UART(1, baudrate=UART_BAUDRATE, tx=1, rx=3)
    lora = init_lora()

    print(f"📡 Escoltant a {LORA_FREQ/1e6} MHz, SF{LORA_SF}...")

    while True:
        try:
            if lora.received():
                payload = lora.receive()
                try:
                    data = json.loads(payload.decode())
                    print(f"📥 Rebut: {data}")

                    # Envia per UART a la Raspberry (el script uart_to_mqtt.py l'agafa)
                    uart.write(json.dumps(data) + "\n")
                except (ValueError, UnicodeError) as e:
                    print(f"Paquet rebut invàlid: {e}")
            time.sleep_ms(100)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
