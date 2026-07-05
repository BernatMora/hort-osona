# Node Emissor — Hort Osona IoT

Node autònom que llegeix sensors ambientals i del sòl a l'hort, i envia les
dades per **LoRa 868 MHz** a la Raspberry Pi de casa (400 m).

## Arquitectura

```
[Sensor humitat + BME280] --(analògic + I2C)--> [ESP32 + LoRa] --(LoRa 868)--> [RPi 4 + HAT LoRa] --> Supabase
                                                          |
                                                     Deep Sleep 15 min
                                                     (bateria 18650 + solar)
```

## Especificacions del node

- **Microcontrolador**: TTGO LoRa32 ESP32 (868 MHz, OLED 128x64 integrat)
- **Xip LoRa**: SX1276 (integrat al board)
- **Freqüència**: 868 MHz (compatible amb Europa/Espanya)
- **Alimentació**: 1× bateria 18650 + panell solar 5V
- **Consum**: < 10 µA en deep sleep
- **Autonomia**: mesos amb bateria + solar

## Sensors connectats

| Sensor | Mida | Protocol | Pin ESP32 | Adreça |
|---|---|---|---|---|
| BME280 (temp/hum/press) | I2C | 0x76 | SDA=21, SCL=22 | 0x76 |
| OLED SSD1306 128x64 | I2C | 0x3C | SDA=21, SCL=22 | 0x3C |
| Capacitive Soil Sensor v1.2 | Analògic | - | GPIO36 (VP) | - |
| Bateria (divisor 100k/100k) | Analògic | - | GPIO35 | - |

## Format del payload LoRa

CSV compacte (una sola línia):

```
T:18.5,H:62.3,P:1013.2,S:45,BAT:3.92
```

- **T**: temperatura (°C)
- **H**: humitat ambiental (%)
- **P**: pressió atmosfèrica (hPa)
- **S**: humitat del sòl (%)
- **BAT**: tensió bateria (V)

## Paràmetres LoRa

- **SF** (Spreading Factor): 10 (bon balanç abast/consum)
- **BW** (Bandwidth): 125 kHz
- **TX Power**: 17 dBm (~50 mW)
- **Freqüència**: 868 MHz (1 canal a la banda 868.0-868.6 MHz)

## Codi

Veure:
- [`src/main.cpp`](src/main.cpp) — Cicle principal: deep sleep + lectura + LoRa
- [`src/config.h`](src/config.h) — Pins i configuració
- [`platformio.ini`](platformio.ini) — Build amb PlatformIO

## Documentació

- [`specs/bom.json`](specs/bom.json) — Llista de materials
- [`docs/steps.json`](docs/steps.json) — Guia de muntatge pas a pas
- [`../../LLISTA-COMPRA.md`](../../LLISTA-COMPRA.md) — On comprar-ho

## Desenvolupament

```bash
# Compilar i pujar al TTGO LoRa32
pio run --target upload

# Monitor sèrie per veure els logs
pio device monitor
```
