# Guia de Muntatge — Node Sensor LoRa per a l'Hort

Guia pas a pas per muntar el node que mesurarà humitat i temperatura del
sòl a l'hort d'Osona i enviarà les dades via LoRaWAN a la Raspberry Pi.

## Visió general

```
    ┌─────────────────┐         LoRaWAN 868MHz         ┌─────────────────┐
    │   NODE EMISSOR  │ ──────────────────────────>    │   NODE RECEPTOR │
    │   (a l'hort)    │      (fins a 5 km)            │   (a casa, RPi) │
    │                 │                                │                 │
    │  ESP32 + LoRa   │                                │  RPi + HAT LoRa │
    │  + sensors      │                                │  + Supabase     │
    │  + bateria      │                                │  + web realtime │
    └─────────────────┘                                └─────────────────┘
```

## 1. Llista de components

### Hardware del node emissor (a l'hort)

| Component | Quantitat | Preu aprox. | On comprar |
|---|---|---|---|
| ESP32 LoRa SX1262 868MHz | 1 | 25 € | Amazon |
| Sensor humitat sòl capacitiu | 1 | 12 € | Amazon |
| Sensor temperatura DS18B20 (sonda acer) | 1 | 11 € | Amazon |
| Bateria LiPo 3.7V 2000mAh JST | 1 | 14 € | Amazon |
| Caixa estanca IP65 (100x60mm) | 1 | 12 € | Amazon |
| Breadboard 400 punts | 1 | 10 € | Amazon |
| Mòdul TP4056 (carregador LiPo) | 1 | 9 € | Amazon |
| Cables Dupont kit (M-F, M-M, F-F) | 1 pack | 13 € | Amazon |
| Panell solar 5V 1W (opcional) | 1 | 12 € | Amazon |
| Resistència 4.7kΩ (per DS18B20) | 1 | 5 € | Amazon |
| **TOTAL** | | **~120 €** | |

### Eines necessàries

- 🪛 **Soldador** (30-50 W, amb estany)
- 🔧 **Pinces** (petites, de precisió)
- 🔪 **Tallador** o tisores
- 📏 **Cinta mètrica**
- 🖊️ **Retolador permanent** (per marcar cables)
- 🔌 **Cable USB-C** (per connectar ESP32 a l'ordinador)
- 💻 **Ordinador** amb port USB (per flashejar)

### Hardware del receptor (a casa)

- Raspberry Pi 4 (2 GB) o Pi Zero 2 W
- HAT Waveshare SX1262 868/915M LoRaWAN
- Font alimentació 5V 3A
- MicroSD 32 GB

## 2. Esquema de connexions

### Node emissor (ESP32 + sensors)

```
                            ┌──────────────────────┐
                            │    ESP32-S3 DevKit  │
                            │                      │
                            │   3V3 ──┬── VCC (sensor humitat)
                            │          ├── VCC (DS18B20)  
                            │          └── VCC (TP4056 OUT+)
                            │                      │
                            │   GND ──┬── GND (sensor humitat)
                            │          ├── GND (DS18B20)
                            │          └── GND (TP4056 OUT-)
                            │                      │
                            │   GPIO 4 ──── DATA (DS18B20)
                            │   GPIO 34 ─── AOUT (sensor humitat)
                            │                      │
                            │   SX1262 LoRa        │
                            │   (integrat)         │
                            │                      │
                            └──────┬───────────────┘
                                   │
                            ┌──────┴───────┐
                            │  Bateria     │
                            │  LiPo 3.7V   │
                            │  2000mAh     │
                            └──────────────┘
```

### Detall de cada connexió

**Sensor humitat del sòl (capacitiu):**
| Cable | Pin ESP32 |
|---|---|
| VCC (vermell) | 3V3 |
| GND (negre) | GND |
| AOUT (groc) | GPIO 34 (ADC1_CH6) |

**Sensor temperatura DS18B20 (sonda acer):**
| Cable | Pin ESP32 |
|---|---|
| VCC (vermell) | 3V3 |
| GND (negre) | GND |
| DATA (groc) | GPIO 4 + resistència 4.7kΩ a 3V3 |

**Mòdul TP4056 (carregador bateria):**
| Pin | Connexió |
|---|---|
| IN+ | Panell solar + (5V) |
| IN- | Panell solar - |
| OUT+ | Bateria JST + |
| OUT- | Bateria JST - |

## 3. Procediment de muntatge

### Pas 1: Preparar l'entorn de treball

1. **Espai net i ben il·luminat**
2. **Eines a mà** (soldador, pinces, cables)
3. **Comprovar tots els components** amb la llista
4. **Llegir TOT el manual** abans de començar

### Pas 2: Soldar el sensor DS18B20 (el més delicat)

1. **Identificar els 3 cables** del sensor (vermell, negre, groc)
2. **Posar termo-retràctil** als extrems dels cables
3. **Soldar la resistència 4.7kΩ** entre el cable groc (DATA) i el vermell (VCC)
4. **Aïllar amb termo-retràctil** la connexió

⚠️ **Compte**: si la resistència no està ben soldada, el sensor no funcionarà.

### Pas 3: Muntar el circuit a la breadboard

1. **Posar l'ESP32** a la breadboard
2. **Connectar el sensor d'humitat**:
   - VCC → 3V3
   - GND → GND
   - AOUT → GPIO 34
3. **Connectar el sensor DS18B20**:
   - VCC → 3V3
   - GND → GND
   - DATA → GPIO 4
4. **Verificar totes les connexions** amb un multímetre (continuïtat)

### Pas 4: Connectar la bateria i el TP4056

1. **Connectar la bateria** al TP4056 (B+/B-)
2. **Verificar** que el LED del TP4056 s'encén (carregant o carregat)
3. **Connectar OUT+/OUT-** del TP4056 a 3V3/GND de l'ESP32
   - ATENCIÓ: no connectar directament a 3V3, sinó via un diode o
     un circuit de protecció (per evitar carregar la bateria per USB)

### Pas 5: Provar el node abans de tancar la caixa

1. **Connectar l'ESP32** al Mac via USB-C
2. **Obrir el Serial Monitor** (PlatformIO o Arduino IDE)
3. **Verificar que arrenca** i envia missatges LoRa
4. **Comprovar lectures** dels sensors (humitat, temperatura)

### Pas 6: Muntar a la caixa estanca

1. **Foradar la caixa** per a:
   - Entrada del cable del sensor d'humitat (a la part inferior)
   - Entrada del cable del sensor de temperatura
   - Entrada del panell solar
   - Forat per a l'antena LoRa (a la part superior)
2. **Posar premsaestopes** als forats (per garantir IP65)
3. **Col·locar la breadboard** dins la caixa
4. **Fixar amb cinta adhesiva de doble cara** o cargols
5. **Tancar la caixa** i verificar que queda hermètica

### Pas 7: Instal·lar a l'hort

1. **Triar una ubicació**:
   - A prop de les plantes que vols monitorar
   - Amb bona cobertura LoRa (provar amb un altre node primer)
   - Protegida de la pluja directa (sota un arbre?)
2. **Col·locar el panell solar** orientat al sud
3. **Enterrar parcialment** la sonda de temperatura al sòl
4. **Clavar el sensor d'humitat** al sòl (la part metàl·lica)
5. **Fixar la caixa** a un pal o paret (cargols o brides)

## 4. Configuració del software (a fer a l'ordinador)

### Pas 1: Instal·lar PlatformIO

```bash
# Instal·lar Python 3.11+ (si no el tens)
brew install python3

# Instal·lar PlatformIO
pip3 install platformio

# Verificar
pio --version
```

### Pas 2: Descarregar el codi del projecte

```bash
cd ~/Desktop/hort-osona/hort-osona-iot/node-emissor
```

### Pas 3: Compilar i pujar el firmware

```bash
# Connectar l'ESP32 via USB-C
pio run --target upload
```

### Pas 4: Monitoritzar

```bash
pio device monitor
```

Hauries de veure missatges com:
```
[Node] Iniciant...
[Sensor] Humitat: 45%, Temperatura: 18°C
[LoRa] Enviant: {"node":"hort-1","hum":45,"temp":18}
[LoRa] OK
[DeepSleep] Dormint 15 min...
```

## 5. Solució de problemes

### L'ESP32 no es detecta per USB

1. **Provar un altre cable USB-C** (alguns només carreguen, no transmeten dades)
2. **Instal·lar els drivers CH340/CP2102**:
   - macOS: `brew install --cask cp210x-vcp-driver`
3. **Premer el botó BOOT** mentre connectes

### El sensor d'humitat retorna valors estranys

1. **Comprovar connexions** (VCC, GND, AOUT)
2. **Calibrar**: deixar al sec i al banyat per obtenir els valors mín/màx
3. **Provar amb un altre pin** ADC (provar GPIO 35)

### El sensor DS18B20 retorna -127°C

1. **Comprovar la resistència 4.7kΩ** (ha d'estar entre DATA i VCC)
2. **Comprovar el cable** (fer-lo més curt si és molt llarg)
3. **Provar sense breadboard** (directe als pins)

### LoRa no connecta

1. **Comprovar l'antena** (ha d'estar connectada!)
2. **Verificar la freqüència**: 868 MHz per Espanya
3. **Comprovar la cobertura** (provar a prop del receptor primer)

## 6. Manteniment

### Cada 6 mesos
- Netejar el panell solar
- Comprovar la bateria (no ha d'estar inflada)
- Verificar connexions

### Cada any
- Substituir la bateria si ha perdut > 30% de capacitat
- Comprovar l'estanquitat de la caixa (juntes, premsaestopes)
- Actualitzar el firmware (si n'hi ha de nou)

## 7. Cronograma realista

| Setmana | Tasca |
|---|---|
| 1 | Rep les comandes d'Amazon (1-2 dies) |
| 2 | Muntar a la breadboard i provar |
| 3 | Soldar i muntar a la caixa estanca |
| 4 | Instal·lar a l'hort i configurar RPi |
| 5+ | Monitorar, ajustar, afegir funcionalitats |

## 8. Proves prèvies al muntatge final

Abans de tancar la caixa, **sempre** fes aquestes proves:

- [ ] El node arrenca sense errors
- [ ] Llegeix el sensor d'humitat (valors entre 0-100%)
- [ ] Llegeix el sensor de temperatura (valors entre -10 i 50°C)
- [ ] Envia un missatge LoRa (visible al receptor)
- [ ] Entra en deep sleep correctament
- [ ] Es desperta del deep sleep
- [ ] La bateria dura > 24h

Només quan totes les proves passin, pots tancar la caixa.

## 9. Seguretat

⚠️ **ATENCIÓ**:
- Mai connectar la bateria a l'inrevés (+/-)
- Mai soldar la bateria directament (risc d'incendi)
- Usar un fusible de 2A entre la bateria i l'ESP32
- No deixar la caixa oberta sota la pluja
- Apagar l'ESP32 abans de tocar els pins

## 10. Eines opcionals útils

- **Multímetre** (per comprovar tensions)
- **Estació de soldadura** (amb control de temperatura)
- **Cautxú de silicona** (per segellar la caixa encara més)
- **Cinta termoretràctil** (per aïllar connexions)
- **Brides d'exterior** (per fixar a arbres o pals)
