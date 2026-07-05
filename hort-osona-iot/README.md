# 🌱 Hort Osona IoT — Sistema complert

Sistema de monitoratge de l'hort amb sensors, LoRa, Raspberry Pi, Supabase i Ollama.

## 🏗️ Arquitectura

```
┌──────────────────────┐                                ┌──────────────────────┐
│  HORT (400 m)         │                                │  CASA (Raspberry Pi 4) │
│                       │                                │                       │
│  [Sensor humitat]─┐   │                                │                       │
│  [BME280]─────────┤   │     LoRa 868 MHz              │  [Waveshare LoRa HAT] │
│  [18650 + Solar]──┤   │ ────────────────────────────> │           │           │
│  [TTGO LoRa32]   │   │   T:18.5,H:62.3,P:1013.2,    │           ↓           │
│   (ESP32 + OLED)  │   │   S:45,BAT:3.92                │  [lora_receiver.py]   │
└──────────────────────┘                                │           │           │
                                                          │           ↓           │
                                                          │  [Supabase Realtime]  │
                                                          │           │           │
                                                          │           ↓           │
                                                          │  [Ollama + Hermes]   │
                                                          │  (consells cada 6h)   │
                                                          └──────────┬───────────┘
                                                                     │
                                                                     ↓
                                                          ┌──────────────────────┐
                                                          │  GitHub Pages (PWA)   │
                                                          │  Hort Osona Portal    │
                                                          │  + Vista "Hort live"  │
                                                          └──────────────────────┘
```

## 📁 Estructura del projecte

```
hort-osona-iot/
├── node-emissor/                  # ESP32 + sensors (a l'hort)
│   ├── README.md                  # Visió general del node
│   ├── platformio.ini             # Build config
│   ├── src/
│   │   ├── main.cpp              # Cicle deep sleep + sensors + LoRa
│   │   └── config.h              # Pins del TTGO LoRa32
│   ├── specs/bom.json            # Llista de materials
│   └── docs/steps.json           # Guia de muntatge pas a pas
│
├── backend/                       # Raspberry Pi (a casa)
│   ├── lora_receiver.py           # Rep LoRa → Supabase → Ollama
│   ├── api_chat.py                # Xat RAG amb Ollama (existent)
│   ├── main.py                    # Backend MQTT (existent)
│   ├── uart_to_mqtt.py            # Bridge UART-MQTT (existent)
│   └── supabase_schema.sql        # Schema SQL per a Supabase
│
└── web/                           # Frontend (PWA)
    └── hort-live.html             # Vista amb dades realtime
```

## 🔄 Flux de dades

1. **Node hort** (cada 15 min):
   - Es desperta del deep sleep
   - Llegeix BME280 (T, H, P) + sensor sol + bateria
   - Mostra a l'OLED 5 segons
   - Envia payload CSV per LoRa
   - Torna a dormir

2. **Receptor Pi 4** (continu):
   - Escolta LoRa amb el HAT SX1262
   - Parseja el CSV
   - INSERT a Supabase (`mesures`)
   - Cada 6h: crida Ollama, desa consell (`consells_ia`)

3. **Web** (a l'obrir):
   - Carrega últimes 100 mesures
   - Mostra stats (T, H, sol, bat)
   - Dibuixa gràfic 24h
   - Subscriu al Realtime de Supabase
   - Actualitza stats quan arriba nova mesura

## 🚀 Com posar-ho en marxa

### Pas 1: Configurar Supabase
1. Crear compte a https://supabase.com
2. Crear nou projecte
3. Anar a SQL Editor i executar `backend/supabase_schema.sql`
4. Copiar URL i anon key → posar-les a `lora_receiver.py` i `web/hort-live.html`

### Pas 2: Muntar el node emissor
- Seguir `node-emissor/docs/steps.json` (10 passos)
- Flashejar amb `pio run --target upload` (PlatformIO)

### Pas 3: Muntar el receptor a la Pi 4
- Connectar el HAT Waveshare SX1262 als pins GPIO
- Instal·lar dependencies:
  ```bash
  pip install supabase RPi.GPIO spidev
  git clone https://github.com/lesept777/SX126x.git
  cd SX126x && sudo python3 setup.py install
  ```
- Editar `lora_receiver.py` amb les claus Supabase
- Executar: `python3 lora_receiver.py`

### Pas 4: Activar la vista web
- Editar `web/hort-live.html` amb les claus Supabase
- O afegir el botó al portal principal (build_portal_v2.py)

## 📊 Format del payload LoRa

```
T:18.5,H:62.3,P:1013.2,S:45,BAT:3.92
```

- **T**: temperatura (°C)
- **H**: humitat ambiental (%)
- **P**: pressió atmosfèrica (hPa)
- **S**: humitat del sòl (%)
- **BAT**: tensió bateria (V)

## 💰 Cost del hardware

| Component | Preu |
|---|---|
| TTGO LoRa32 868 MHz | 22 € |
| BME280 | 8 € |
| Sensor sol capacitiu (×2) | 7 € |
| Bateria 18650 (×2) | 16 € |
| Panell solar 5V | 10 € |
| Caixa IP65 | 8 € |
| Cables Dupont | 4 € |
| **HAT Waveshare SX1262** | **30 €** |
| **TOTAL** | **~105 €** |

## 🎯 Cosa a fer

- [x] Hardware especificat (Bricogeek + Amazon ES)
- [x] Node emissor firmware (PlatformIO)
- [x] Receptor Python (RPi 4 + LoRa → Supabase)
- [x] Schema Supabase (2 taules + Realtime)
- [x] Vista web amb dades realtime
- [ ] Comprar hardware
- [ ] Muntar el node
- [ ] Muntar el receptor
- [ ] Crear compte Supabase
- [ ] Provar el flux complet
