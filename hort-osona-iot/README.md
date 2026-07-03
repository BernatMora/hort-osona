# 🌱 Hort Osona IoT — Sistema de sensors per al teu hort

Monitoratge d'humitat, temperatura, llum i conductivitat del sòl del teu hort a Osona, amb sensors Xiaomi MiFlora, comunicació LoRa 868MHz i backend a Raspberry Pi 4.

## 🎯 Què fa

- **3 sensors d'humitat del sòl** (1 per parcel·la)
- **1 sensor ambient** (temperatura + humitat de l'aire)
- Comunicació **LoRa 868MHz** (245m de distància, baixa potència)
- **Backend Python** a Raspberry Pi 4 amb FastAPI + MQTT
- **Integració amb la PWA** [hort-osona](https://BernatMora.github.io/hort-osona/) — gràfiques i alertes al mòbil

## 🏗️ Arquitectura

```
[Hort 245m]                              [Casa]
                                          ┌─────────────────────┐
  ┌────────────────────────┐              │  Raspberry Pi 4     │
  │ 3× MiFlora             │              │  ├── Mosquitto MQTT  │
  │ 1× Thermometer 2       │              │  ├── FastAPI backend │
  │      │                 │              │  ├── SQLite DB       │
  │      │ Bluetooth       │              │  └── Tailscale       │
  │      ▼                 │              │         ▲            │
  │  TTGO LoRa32 (bridge)  │              │         │            │
  │  └─ solar 5V + 18650   │──── LoRa ────┘  TTGO LoRa32 (gw)   │
  │                                                │             │
  └────────────────────────────────────────────────┘  USB ────────┘
                                                            │
                                                            ▼
                                                    [PWA Hort Osona]
                                                    Mac / iPhone / iPad
```

## 🛒 Hardware

| Component | Quantitat | Preu aprox. | On |
|---|---|---|---|
| Raspberry Pi 4B 4GB | 1 | 55€ | Amazon / Kubii |
| Carregador USB-C 5V/3A | 1 | 12€ | Amazon |
| MicroSD 32GB A2 | 1 | 8€ | Amazon |
| Carcasa + dissipador | 1 | 12€ | Amazon |
| Xiaomi MiFlora | 3 | 45€ | AliExpress / Amazon |
| Xiaomi Thermometer 2 | 1 | 8€ | AliExpress / Amazon |
| TTGO LoRa32 V2 (868MHz) | 2 | 40€ | AliExpress / Banggood |
| Antena 868MHz 5dBi | 1 | 5€ | AliExpress |
| Caixa estanca IP65 | 1 | 5€ | Amazon / Leroy Merlin |
| Panell solar 5V/2W | 1 | 12€ | AliExpress |
| Bateria 18650 + TP4056 | 1 | 10€ | AliExpress |
| Cables + accessoris | - | 8€ | AliExpress |
| **TOTAL** | | **~220€** | |

## 🚀 Instal·lació

### Pas 1 — Preparar la Raspberry Pi

1. Descarrega [Raspberry Pi Imager](https://www.raspberrypi.com/software/) al Mac
2. Flasheja Raspberry Pi OS Lite (64-bit) a la microSD
3. Configura WiFi + SSH abans del primer boot
4. Primer boot headless → connecta per SSH

### Pas 2 — Executar el setup

```bash
# Copia el projecte a la Raspberry
scp -r hort-osona-iot/ bernat@hortpi.local:~/

# SSH a la Raspberry
ssh bernat@hortpi.local

# Executa el setup
chmod +x ~/hort-osona-iot/setup-pi.sh
./hort-osona-iot/setup-pi.sh
```

Això instal·la:
- Mosquitto MQTT
- Python venv amb FastAPI, paho-mqtt, bleak
- Servei systemd hort-backend (s'inicia automàticament)
- Tailscale (per accedir des de fora)

### Pas 3 — Flashejar els TTGO LoRa32

1. Instal·la [esptool](https://github.com/espressif/esptool): `pip install esptool`
2. Descarrega [MicroPython per a ESP32](https://micropython.org/download/ESP32/)
3. Flasheja:
   ```bash
   esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-XXXXXXXX.bin
   ```
4. Copia `bridge/main.py` (per al bridge de l'hort) i `bridge/gateway.py` (per al gateway de casa)

### Pas 4 — Configurar sensors

Edita `bridge/main.py` amb les adreces MAC reals dels teus MiFlora:

```python
SENSORS = [
    {"name": "parcela1", "address": "C4:7C:8D:XX:XX:XX", "type": "miflora"},
    {"name": "parcela2", "address": "C4:7C:8D:YY:YY:YY", "type": "miflora"},
    {"name": "parcela3", "address": "C4:7C:8D:ZZ:ZZ:ZZ", "type": "miflora"},
    {"name": "ambient",  "address": "AA:BB:CC:DD:EE:04", "type": "thermometer"},
]
```

## 🔌 Comandes útils

```bash
# Veure logs del backend
sudo journalctl -u hort-backend -f

# Escoltar missatges MQTT
mosquitto_sub -h localhost -t 'hort/#' -v

# Test API
curl http://hortpi.local:8000/health
curl http://hortpi.local:8000/sensors

# Reiniciar servei
sudo systemctl restart hort-backend
```

## 🔌 Endpoints API

| Mètode | URL | Descripció |
|---|---|---|
| GET | `/health` | Estat del servei |
| GET | `/sensors` | Totes les últimes lectures |
| GET | `/sensors/{parcela}` | Última lectura d'una parcel·la |
| GET | `/sensors/{parcela}/history?hours=24` | Històric d'una parcel·la |

## 📡 Temes MQTT

- `hort/sensors/miflora/{id}` — Dades del sensor MiFlora
- `hort/sensors/thermometer/{id}` — Dades del Thermometer
- `hort/sensors/status` — Estat dels sensors (online/offline, bateria)

## 🔮 Roadmap

- [ ] Gràfiques a la PWA
- [ ] Alertes intel·ligents (humitat < 30% durant 3 dies)
- [ ] Càmera IP per a fotos automàtiques
- [ ] Integració amb PlantNet/GPT-4V per a diagnòstic de malalties
- [ ] Panell solar més potent + sistema autònom
- [ ] Múltiples horts (federació)

## 📜 Llicència

MIT — ús lliure, sense garanties.

## 🌱 Agraïments

Creat amb 🫀 per Bernat Mora a Vic, Osona. Per a la terra, no per a la pantalla.
