# 🛒 PEDIDO AMAZON — Hort Osona IoT

> Llista exacta de compra per al sistema de sensors hort amb Raspberry Pi 4B,
> sensors Xiaomi MiFlora, LoRa 868MHz i backend Python.
> Data de preparació: 2026-07-03.

## 💰 Resum del pressupost

| Categoria | Preu aprox. |
|---|---|
| 🖥️ Raspberry Pi 4B (core) | 87€ |
| 📡 Sensors Xiaomi + LoRa | 103€ |
| 🔋 Alimentació solar (pont) | 22€ |
| 🔌 Cables i accessoris | 8€ |
| **TOTAL** | **~220€** |

---

## 🖥️ 1. Raspberry Pi 4B (core del sistema)

### 1.1 Raspberry Pi 4 Model B 4GB
- **Preu aprox**: 55-65€
- **Recomanació**: comprar a **Kubii** o **Melopero** (distribuïdors oficials a Espanya)
- **Alternativa Amazon**: cerca "Raspberry Pi 4 4GB"
- **Important**: NO compris a venedors tercers sense valoracions, hi ha moltes falsificacions

**Alternatives oficials**:
- [Kubii — Raspberry Pi 4 Model B 4GB](https://www.kubii.com/es/raspberry-pi-4/2048-raspberry-pi-4-model-b-4gb-kubii-3272496301371.html)
- [Melopero — Raspberry Pi 4B 4GB](https://www.melopero.com/shop/raspberry-pi/raspberry-pi-4/raspberry-pi-4-model-b-4gb/)

### 1.2 Carregador USB-C 5V/3A oficial
- **Preu aprox**: 12-15€
- **CRÍTIC**: ha de ser **5V/3A** mínim. Un de 2A farà reiniciar la Pi sota càrrega.
- **Recomanació**: el carregador oficial de Raspberry Pi

**A Amazon**:
- Cerca: "Raspberry Pi 4 USB-C alimentador oficial"
- O directament: [Cargador oficial Raspberry Pi 4 - Amazon](https://www.amazon.es/s?k=raspberry+pi+4+alimentador+oficial)

### 1.3 MicroSD 32GB Classe 10 A2
- **Preu aprox**: 8-12€
- **Recomanació**: Sandisk Extreme o Samsung EVO Select (A2 = bona velocitat d'escriptura aleatòria)
- **Per què A2**: la Raspberry Pi arrenca i llegeix molts fitxers petits, una targeta A2 va molt millor

**A Amazon**:
- [SanDisk Extreme 32GB A2 - Amazon](https://www.amazon.es/s?k=sandisk+extreme+32gb+micro+sd)
- [Samsung EVO Select 32GB A2 - Amazon](https://www.amazon.es/s?k=samsung+evo+select+32gb)

### 1.4 Carcassa amb dissipador
- **Preu aprox**: 10-15€
- **Recomanació**: carcassa d'alumini amb dissipador integrat. NO compris carcassa plàstica tancada, la Pi s'escalfarà massa.
- **Tipus recomanat**: FLIRC, Argon One (més cares), o una genèrica d'alumini amb pasta tèrmica

**A Amazon**:
- [Carcasa Raspberry Pi 4 aluminio disipador - Amazon](https://www.amazon.es/s?k=carcasa+raspberry+pi+4+aluminio+disipador)

**Subtotal secció 1: ~85-105€**

---

## 📡 2. Sensors i gateway LoRa

### 2.1 Xiaomi MiFlora 4-en-1 × 3 unitats
- **Preu aprox**: 12-18€ cadascun (3 unitats = 36-54€)
- **Què mesura**: humitat del sòl, llum, temperatura, fertilitat (EC), conductivitat
- **Connexió**: Bluetooth Low Energy (BLE)
- **Autonomia piles**: ~1 any (1× pila CR2032)
- **Recomanació**: comprar pack de 3 surt més econòmic

**A Amazon**:
- [Xiaomi MiFlora 4 en 1 sensor plantes - Amazon](https://www.amazon.es/s?k=xiaomi+miflora)
- Busca "MiFlora" o "HHCC" o "Flora Care"

**A AliExpress** (alternativa més barata, 2-3 setmanes):
- [MiFlora 4-in-1 AliExpress](https://es.aliexpress.com/wholesale?SearchText=miflora+4+in+1)

**Important**: Assegura't que la versió és la **4-en-1** (no la 2-en-1 antiga).

### 2.2 Xiaomi Mi Thermometer 2 × 1 unitat
- **Preu aprox**: 7-10€
- **Model**: LYWSD03MMC (aquest exactament)
- **Què mesura**: temperatura + humitat de l'aire
- **Què serveix**: posar-lo a 1 metre del terra, a l'ombra, per tenir dades ambientals

**A Amazon**:
- [Xiaomi Mi Thermometer 2 LYWSD03MMC - Amazon](https://www.amazon.es/s?k=xiaomi+mijia+thermometer+2)

**A AliExpress**:
- [Xiaomi Thermometer 2 AliExpress](https://es.aliexpress.com/wholesale?SearchText=lywsd03mmc)

### 2.3 TTGO LoRa32 V2 (868MHz) × 2 unitats
- **Preu aprox**: 18-25€ cadascun (2 unitats = 36-50€)
- **⚠️ CRÍTIC**: ha de ser **868MHz** (versió EU), NO 915MHz (US)
- **Versions recomanades**:
  - TTGO LoRa32 V2 (868MHz) — la més comuna i provada
  - Heltec WiFi LoRa 32 V3 — una mica més potent
- **Què fan**:
  - 1 unitat = **bridge** a l'hort (llegeix BLE, retransmet per LoRa)
  - 1 unitat = **gateway** a casa (rep LoRa, envia per USB a la Raspberry)

**A Amazon**:
- [TTGO LoRa32 V2 868MHz - Amazon](https://www.amazon.es/s?k=ttgo+lora32+v2+868)

**A AliExpress** (molt més econòmic, ~12€ cadascun, 2-3 setmanes):
- [TTGO LoRa32 V2 AliExpress](https://es.aliexpress.com/wholesale?SearchText=ttgo+lora32+v2+868mhz)

**Important**: Mira bé la descripció. La versió **868MHz** és per a Europa. La **915MHz** és per a Amèrica i NO funciona legalment aquí.

### 2.4 Antena 868MHz 5dBi SMA × 1
- **Preu aprox**: 4-6€
- **Per què**: el gateway a casa necessita una antena externa per arribar bé als 245m
- **Tipus**: antena "duck" SMA mascle, 5dBi, 868MHz
- **El bridge NO en porta** (la que porta integrada és suficient a 245m)

**A Amazon**:
- [Antena 868MHz 5dBi SMA - Amazon](https://www.amazon.es/s?k=antena+868mhz+5dbi+sma)

### 2.5 Caixa estanca IP65 × 1
- **Preu aprox**: 4-6€
- **Mida recomanada**: 158×90×65mm (per encabir el TTGO + bateria)
- **Per què**: protegir el bridge a l'hort de la pluja i humitat
- **On**: també a Leroy Merlin, Bricomart, ferreteries

**A Amazon**:
- [Caja estanca IP65 158x90x65mm - Amazon](https://www.amazon.es/s?k=caja+estanca+ip65+158x90x65)

**A Leroy Merlin** (si el vols veure en persona):
- Cerca "caja estanca IP65 158x90x65" a la web de Leroy Merlin

**Subtotal secció 2: ~95-130€**

---

## 🔋 3. Alimentació solar (per al bridge a l'hort)

### 3.1 Panell solar 5V/2W amb USB
- **Preu aprox**: 10-15€
- **Tipus**: panell solar portàtil amb sortida USB directa
- **Per què 2W**: el TTGO consumeix molt poc en deep sleep (~20µA), 2W és més que suficient
- **Mida típica**: 15×10 cm (portàtil)

**A Amazon**:
- [Panel solar 5V 2W USB - Amazon](https://www.amazon.es/s?k=panel+solar+5v+2w+usb)

**A AliExpress**:
- [Panel solar 5V 2W AliExpress](https://es.aliexpress.com/wholesale?SearchText=panel+solar+5v+2w+usb)

### 3.2 Bateria 18650 3000mAh × 1
- **Preu aprox**: 4-6€
- **Tipus**: 18650 (la gran, NO AA), 3.7V nominal
- **Capacitat recomanada**: 3000mAh o més
- **Recomanació**: Samsung INR18650-30Q, LG MJ1, o Panasonic NCR18650B (fiables)

**A Amazon**:
- [Bateria 18650 3000mAh - Amazon](https://www.amazon.es/s?k=bateria+18650+3000mah)

### 3.3 Mòdul TP4056 amb protecció × 1
- **Preu aprox**: 2-3€
- **Què és**: mòdul de càrrega per a bateries 18650 amb protecció contra sobrecàrrega
- **Variant recomanada**: TP4056 **amb** xip DW01A (protecció), NO la versió barata sense protecció

**A Amazon**:
- [Modulo TP4056 proteccion - Amazon](https://www.amazon.es/s?k=tp4056+proteccion)

**A AliExpress** (pack de 5 per 2€):
- [TP4056 amb protecció AliExpress](https://es.aliexpress.com/wholesale?SearchText=tp4056+protection)

**Subtotal secció 3: ~16-24€**

---

## 🔌 4. Cables i accessoris

### 4.1 Pack cables Dupont + resistències + brides
- **Preu aprox**: 5-8€
- **Què inclou**: 40 cables Dupont mascle-femella, 40 mascle-mascle, 40 femella-femella, 600 resistències assortides, brides de plàstic

**A Amazon**:
- [Kit cables Dupont resistencias - Amazon](https://www.amazon.es/s?k=dupont+kit+raspberry+pi)

### 4.2 Cable Ethernet Cat6 × 1
- **Preu aprox**: 3-5€
- **Mida**: 1-2 metres (de la Raspberry al router)
- **Per què**: la Pi funcionarà 24/7 a casa, millor Ethernet que WiFi

**A Amazon**:
- [Cable Ethernet Cat6 1m - Amazon](https://www.amazon.es/s?k=cable+ethernet+cat6+1m)

**Subtotal secció 4: ~8-13€**

---

## 📋 Resum final de comanda

| # | Producte | Quant. | Preu aprox. |
|---|---|---|---|
| 1 | Raspberry Pi 4B 4GB | 1 | 55-65€ |
| 2 | Carregador USB-C 5V/3A oficial | 1 | 12-15€ |
| 3 | MicroSD 32GB A2 | 1 | 8-12€ |
| 4 | Carcassa + dissipador alumini | 1 | 10-15€ |
| 5 | Xiaomi MiFlora 4-en-1 | 3 | 36-54€ |
| 6 | Xiaomi Mi Thermometer 2 | 1 | 7-10€ |
| 7 | TTGO LoRa32 V2 (868MHz) | 2 | 36-50€ |
| 8 | Antena 868MHz 5dBi SMA | 1 | 4-6€ |
| 9 | Caixa estanca IP65 | 1 | 4-6€ |
| 10 | Panell solar 5V/2W USB | 1 | 10-15€ |
| 11 | Bateria 18650 3000mAh | 1 | 4-6€ |
| 12 | Mòdul TP4056 amb protecció | 1 | 2-3€ |
| 13 | Pack cables Dupont | 1 | 5-8€ |
| 14 | Cable Ethernet Cat6 1m | 1 | 3-5€ |
| | **TOTAL** | | **~196-272€** |
| | **Mitjana realista** | | **~220€** |

---

## 🛒 Estratègia de comanda (3 opcions)

### 🥇 Opció A — Tot d'Amazon (ràpid, 1-2 dies)
- **Cost**: ~220€
- **Temps d'entrega**: 1-2 dies
- **Pros**: arriba de pressa, devolucions fàcils
- **Contres**: preus una mica més alts

### 🥈 Opció B — Mix Amazon + AliExpress (equilibrat)
- **Compra a Amazon** (urgent, 1-2 dies):
  - Raspberry Pi 4B 4GB
  - Carregador USB-C oficial
  - MicroSD
  - Carcassa
  - Xiaomi MiFlora (3)
  - Xiaomi Thermometer 2
  - Caixa estanca
  - Cables + Ethernet
  - **Subtotal**: ~140€
- **Compra a AliExpress** (2-3 setmanes, ~30€ menys):
  - TTGO LoRa32 V2 (868MHz) × 2
  - Antena 868MHz
  - Panell solar 5V/2W
  - Bateria 18650
  - TP4056
  - **Subtotal**: ~50€
- **TOTAL**: ~190€
- **Temps**: 1-2 dies (Amazon) + 2-3 setmanes (AliExpress)
- **Pros**: estalvies 30€ i tens el core del sistema ja en 2 dies

### 🥉 Opció C — Tot d'AliExpress (econòmic, 2-3 setmanes)
- **Cost**: ~160€
- **Temps d'entrega**: 2-3 setmanes
- **Pros**: el més econòmic
- **Contres**: trigarà més, devolucions complicades

---

## 🔍 Consells per evitar problemes

### ⚠️ Raspberry Pi
- **NO compris a venedors tercers** amb poques valoracions a Amazon — hi ha falsificacions
- Compra directament a **Kubii** o **Melopero** (distribuïdors oficials)
- O a Amazon, busca el venedor "Raspberry Pi" o "Kubii"

### ⚠️ TTGO LoRa32
- **MOLT IMPORTANT**: ha de ser **868MHz** (UE), NO 915MHz (US)
- Mira la descripció i les fotos del xip SX1276 — la versió 868MHz porta "868" marcat
- Si posa "LoRa32 V2" sense especificar freq., pregunta al venedor

### ⚠️ Xiaomi MiFlora
- Hi ha moltes còpies. Compra la versió oficial Xiaomi (blanc amb logotip Mi)
- Les còpies barates sovint no tenen el xip BLE correcte i no es poden aparellar

### ⚠️ MicroSD
- **NO compris targetes massa barates** de marques desconegudes
- Sandisk i Samsung són les més fiables
- Format A2 = Application class 2 (rendiment en IOPS, no velocitat)

---

## 📦 On instal·lar-ho

### Raspberry Pi (a casa)
- **Lloc ideal**: al costat del router, connectada per Ethernet
- **Alternatives**: darrere la TV, al calaix de l'oficina, al garatge
- **Important**: ventilació! No la tanquis en un espai sense circulació d'aire
- **Consum**: 5W = ~0,5€/mes = 6€/any

### Bridge LoRa (a l'hort)
- **Lloc ideal**: cobert de l'hort, a 5-10m dels sensors (per BLE)
- **Protegit**: dins la caixa estanca IP65
- **Alimentació**: panell solar + bateria 18650
- **Muntatge**: en un pal o paret, mirant cap amunt per captar bé el sol

### Sensors MiFlora (al sòl)
- **Profunditat**: enterra'ls a 20-30cm, on hi ha les arrels
- **Posició**: a 15-20cm de la planta
- **Orientació**: el cap blanc ha de quedar a la vista (per canviar piles)
- **Distribució**: 1 per parcel·la, separats 2-3m si tens una parcel·la gran

### Thermometer (ambient)
- **Posició**: a 1m del terra, a l'ombra
- **Lloc**: cobert, arbret, o sota un rafel
- **Important**: NO al sol directe (donaria lectures errònies)

---

## 🗓️ Què fer quan arribi tot

### Pas 1 — Muntatge de la Raspberry (1-2 hores)
1. Insereix la microSD flashejada amb Raspberry Pi OS Lite
2. Connecta la carcassa amb dissipador
3. Connecta Ethernet al router
4. Endolla l'alimentació USB-C
5. Espera 1-2 minuts i busca la IP al router
6. Connecta per SSH: `ssh bernat@hortpi.local`

### Pas 2 — Setup automàtic (10-15 min)
```bash
# Des del Mac
scp -r hort-osona-iot/ bernat@hortpi.local:~/
ssh bernat@hortpi.local
chmod +x ~/hort-osona-iot/setup-pi.sh
./hort-osona-iot/setup-pi.sh
```

### Pas 3 — Flashejar els TTGO (30 min)
1. Instal·la esptool: `pip install esptool`
2. Descarrega MicroPython per a ESP32
3. Flasheja el primer TTGO amb `bridge/main.py` (serà el bridge de l'hort)
4. Flasheja el segon TTGO amb `bridge/gateway.py` (serà el gateway de casa)

### Pas 4 — Configurar sensors (15 min)
1. Edita `bridge/main.py` amb les adreces MAC reals dels MiFlora
2. Torna a flashejar el TTGO bridge

### Pas 5 — Provar (1-2 hores)
1. Encén el bridge a l'hort (amb solar)
2. Connecta el gateway a la Raspberry per USB
3. Mira els logs: `sudo journalctl -u hort-backend -f`
4. Comprova l'API: `curl http://hortpi.local:8000/sensors`

### Pas 6 — Integrar amb la PWA (30 min)
1. Afegir una secció "📡 Sensors" al sidebar
2. Consumir els endpoints API
3. Mostrar les últimes lectures i gràfiques

---

## 📞 Suport

Si tens cap problema durant la compra o el muntatge, podem revisar-ho junts. 

---

**Creat amb 🫀 per Bernat Mora — Vic, 2026-07-03**
