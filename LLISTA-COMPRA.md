# 🛒 Llista de la compra — Sistema Hort Intel·ligent

## ✅ Ja al carret

- [x] **TTGO LoRa32 ESP32 OLED — 868 MHz** (Bricogeek 1121, ~22 €)
  - URL: `https://tienda.bricogeek.com/lora/1121-ttgo-lora32-esp32-con-oled-868-mhz.html`

## 📦 A comprar (prioritat)

### 1. Receptor LoRa per a la Raspberry Pi 4 — **TROBAT!**
- **Producte triat**: **Waveshare SX1262 868M LoRa HAT** (compatible Raspberry Pi)
- **Per què**: HAT sobre GPIO (més estable que USB), xip SX1262 modern i sensible
- 🔗 Cerca Amazon: `"Waveshare SX1262 868M LoRa HAT"`
- 🔗 URL Waveshare: https://www.waveshare.com/wiki/SX1262_868M_LoRa_HAT
- **Filtra**: 868 MHz (NO 433 ni 915), connector SMA per antena exterior
- **Preu esperat**: 25-35 € (més econòmic que USB dongle)
- **Si NO trobes a Amazon**: directament a Waveshare.com (envien dins EU)

### 2. Sensor humitat terra capacitiu
- 🔗 https://www.amazon.es/s?k=sensor+humedad+suelo+capacitivo
- **Filtra**: "capacitivo" (NO "resistivo"), voltatge 3.3-5V, mida petita
- **Preu**: 5-10 € (compra'n 2 per si de cas)
- **Si NO trobes**: cerca `"capacitive soil moisture v1.2"`

### 3. Sensor BME280 (ambient: temperatura, humitat, pressió)
- 🔗 https://www.amazon.es/s?k=BME280
- **Filtra**: ha de dir **BME280** (no BMP280, que no té humitat)
- **Preu**: 5-12 €
- **Comprova**: 4 pins (VCC, GND, SCL, SDA) per I2C

### 4. Antena 868 MHz 5 dBi exterior
- 🔗 https://www.amazon.es/s?k=antena+868+mhz+5dbi
- **Filtra**: 868 MHz (NO 915 ni 2.4 GHz), connector SMA
- **Preu**: 10-15 €

### 5. Bateria 18650 3500 mAh
- 🔗 https://www.amazon.es/s?k=18650+3500mah
- **Filtra**: marques conegudes (Samsung 35E, LG MJ1, Panasonic NCR18650B)
- ⚠️ **EVITA** marques desconegudes (Ultrafire, Trustfire = falsificacions)
- **Preu**: 8-12 € per unitat (compra'n 2)

### 6. Portapiles 18650 amb cables
- 🔗 https://www.amazon.es/s?k=portapilas+18650
- **Preu**: 2-4 €

### 7. Panell solar 5V/1W amb USB
- 🔗 https://www.amazon.es/s?k=panel+solar+5v+1w
- **Filtra**: 5V, amb sortida USB o micro-USB
- **Preu**: 8-15 €

### 8. Caixa estanca IP65
- 🔗 https://www.amazon.es/s?k=caja+estanca+ip65
- **Filtra**: IP65 o IP66, mida ~150×100×70 mm
- **Preu**: 5-12 €
- **Alternativa**: Leroy Merlin tenen caixes de derivació bones i es veuen a la botiga

### 9. Cables Dupont (40 ut, mascle-femella + femella-femella)
- 🔗 https://www.amazon.es/s?k=cables+dupont+40
- **Preu**: 3-5 €

## 💰 Pressupost total

| Concepte | Mínim | Còmode |
|---|---|---|
| Hardware hort (1-7) | 75 € | 110 € |
| Muntatge (8-9) | 8 € | 17 € |
| **TOTAL** | **~85 €** | **~125 €** |

## 🛍️ Alternatives a Amazon ES

| Botiga | URL | Per què |
|---|---|---|
| **Bricogeek** | tienda.bricogeek.com | Té la placa 868 MHz, bona selecció IoT |
| **Iberobotics** | iberobotics.com | Especialistes robòtica/IoT espanyols |
| **Electan** | electan.com | Components electrònics |
| **Leroy Merlin** | leroymerlin.es | Caixes estanques, panells solars, cables |
| **Pimoroni** | shop.pimoroni.com | UK, bona selecció ESP32 + LoRa |

## 🧪 Ordre recomanat de compra

1. **Primera comanda** (tot el que cal per provar a casa — **la més important**):
   - Waveshare SX1262 868M LoRa HAT (~30 €) ← **receptor a la Pi 4**
   - Sensor humitat capacitiu (~7 €)
   - BME280 (~8 €)
   - Cables Dupont (~4 €)
   - **Total**: ~50 €

2. **Segona comanda** (muntar a l'hort):
   - Bateria 18650 (×2) (~18 €)
   - Portapiles (~3 €)
   - Panell solar (~10 €)
   - Caixa estanca (~8 €)
   - **Total**: ~40 €

3. **Tercera comanda** (opcional, millora l'abast):
   - Antena exterior 868 MHz 5 dBi (~12 €)

## 📝 Notes

- **A Amazon ES**, els productes IoT solen ser més cars que a AliExpress, però lliuren en 24-48h
- **Si una cerca no dóna resultats**, canvia la paraula clau (per exemple: "ESP32 LoRa" en lloc de "Heltec LoRa")
- **Sempre comprova la freqüència 868 MHz** al títol del producte, no només a la descripció
- **Guarda el rebut** de cada compra per si has de tornar res
