# 🌱 Hort Osona IoT — Guia d'inici ràpid

> Sistema de sensors per al teu hort amb Raspberry Pi 4 + LoRa + Xiaomi MiFlora.
> Versió completa: veure [README.md](README.md).
> Llista de compra: veure [PEDIDO-AMAZON.md](PEDIDO-AMAZON.md).

## 📋 Què és?

Un sistema que monitora l'estat del teu hort a Osona en temps real:
- **Humitat del sòl** (3 parcel·les)
- **Temperatura i humitat ambient**
- **Lluminositat** (per saber si els cultius tenen prou sol)
- **Temperatura del sòl**

Les dades es transmeten via **LoRa 868MHz** (245m de distància) i es desen a una **Raspberry Pi 4** a casa. La PWA existent a [hort-osona](https://BernatMora.github.io/hort-osona/) mostrarà gràfiques i alertes.

## 🏗️ Arquitectura en 30 segons

```
[Hort 245m]                    [Casa]                   [Internet]
3× MiFlora → TTGO bridge → LoRa → TTGO gw → USB → Raspberry Pi 4
                                      ↓
                                  Mosquitto + FastAPI + SQLite
                                      ↓
                                   API REST
                                      ↓
                          PWA Hort Osona (Mac/iPhone/iPad)
```

## 💰 Cost total: ~220€

- Raspberry Pi 4B 4GB: 60€
- 3 sensors MiFlora: 50€
- 2 TTGO LoRa32: 40€
- 1 Termòmetre Xiaomi: 8€
- Panell solar + bateria: 20€
- Accessoris: 40€

## 🚀 3 passes per començar

### 1. Compra tot el material
👉 Vés a [PEDIDO-AMAZON.md](PEDIDO-AMAZON.md) per la llista completa amb enllaços.

### 2. Munta la Raspberry
1. Descarrega [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Flasheja Raspberry Pi OS Lite (64-bit) a la microSD
3. Configura WiFi + SSH abans del primer boot
4. Connecta per SSH i executa `setup-pi.sh`

### 3. Flasheja els TTGO i configura els sensors
1. Instal·la [MicroPython](https://micropython.org/download/ESP32/) a cada TTGO
2. Copia `bridge/main.py` al TTGO bridge (a l'hort)
3. Copia `bridge/gateway.py` al TTGO gateway (a casa)

## 📂 Estructura del projecte

```
hort-osona-iot/
├── README.md                    # Documentació completa
├── PEDIDO-AMAZON.md            # Llista de compra amb enllaços
├── INICI-RAPID.md              # Aquest fitxer
├── setup-pi.sh                 # Setup automàtic per a Raspberry Pi
├── backend/
│   ├── main.py                 # API FastAPI + MQTT listener
│   └── uart_to_mqtt.py         # Script USB→MQTT
└── bridge/
    ├── main.py                 # Codi per al TTGO bridge (LoRa TX)
    └── gateway.py              # Codi per al TTGO gateway (LoRa RX)
```

## 🔌 Endpoints API

Un cop en marxa, l'API estarà disponible a `http://hortpi.local:8000`:

- `GET /health` — Estat del servei
- `GET /sensors` — Totes les últimes lectures
- `GET /sensors/{parcela}` — Última lectura d'una parcel·la
- `GET /sensors/{parcela}/history?hours=24` — Històric

## 🎯 Què pots fer un cop funcioni

1. **Veure gràfiques en temps real** al mòbil (integració amb PWA)
2. **Rebre alertes** quan la humitat del sòl baixa del 30%
3. **Detectar gelades** amb el termòmetre ambient
4. **Optimitzar el reg** basant-te en dades reals
5. **Detectar malalties** (futur: amb càmera i GPT-4V)

## 📞 Ajuda

Si tens dubtes durant el muntatge, podem revisar-ho junts. La majoria de la documentació està al [README.md](README.md) complet.

---

**Fet amb 🫀 per Bernat Mora — Vic, 2026**
