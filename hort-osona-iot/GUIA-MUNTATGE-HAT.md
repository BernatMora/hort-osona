# Com muntar el HAT SX1262 LoRa a la Raspberry Pi 4

## Què tens a les mans

A la caixa del HAT hi hauria d'haver:
- 1× placa HAT SX1262 LoRa 868 MHz (amb antena SMA cargolada)
- 1× antena 868 MHz (cargolada al HAT o a part)
- 2× separadors/torrets metàl·lics (de 12-15 mm)
- 4× cargols M2.5 (per subjectar els torrets)
- 1× tira de pins mascle (40 pins GPIO) — pot venir ja soldada o no

## Eines que necessites

- Tornavís Phillips (estrella) petit (PH0 o PH00)
- Si els pins NO estan soldats al HAT, **soldador + estany** (millor portar-ho a una botiga d'electrònica si no en tens)

## ⚠️ MOLT IMPORTANT: Apaga la RPi ABANS

**Mantingues la RPi DESENDOLLADA** (sense USB-C) mentre munts el HAT.
Si endolles la RPi amb el HAT mig muntat, pots fer curtcircuits.

---

## Pas 1: Preparar el HAT (1-2 min)

1. Mira el HAT: hauria de tenir una antena cargolada al connector SMA
2. Comprova que **NO hi ha cap cinta protectora** sobre els pins GPIO de la part inferior
3. Si veus una cinta groga/blanca, **tira-la**

## Pas 2: Muntar els separadors (5 min)

Els **separadors** (o "standoffs" o "torrets") són les peces metàl·liques que eleven el HAT perquè no toqui la RPi.

1. Posa la RPi damunt la taula amb els ports USB cap a tu
2. Agafa 2 dels 4 forats de la RPi — concretament els **2 que NO són del mig** (els del costat més allunyat dels USB)
3. Enfonsa un **separador metàl·lic** al forat de la dreta, des de la part superior
4. Cargola'l amb un cargol M2.5 per la part de sota de la RPi
5. Repeteix amb el segon separador a l'altre costat

```
Vista superior de la RPi (amb connectors USB mirant cap a tu):

   [GPIO pins - 40 pins a la part superior]
   ┌──────────────────────────────────────┐
   │  [Separador]              [Separador] │  ← 2 separadors aquí
   │                                       │
   │   [RPi amb el seu SoC, RAM, etc.]    │
   │                                       │
   │  [USB-C] [USB-A] [USB-A] [Ethernet]  │  ← connectors a la part inferior
   └──────────────────────────────────────┘
```

## Pas 3: Posar el HAT a sobre (3 min)

1. Agafa el HAT amb cura (no toquis el xip SX1262 ni l'antena)
2. Mira la part de sota del HAT — veuràs una tira de **40 pins mascle** (els GPIO)
3. **Alinieja els pins** del HAT amb els 40 forats GPIO de la RPi:
   - Els pins del HAT han de coincidir amb els pins de la RPi
   - La vora del HAT ha d'estar **paral·lela** a la vora dels pins GPIO
4. **Pressiona suaument** però fermament cap avall, amb els dits polzes repartint la força per igual
5. Has de sentir un **"click"** subtil quan els pins entren
6. ⚠️ Si un pin es doblega, **tira'l amb compte** amb un tornavís pla petit (mai amb les dents!)

```
Vistes laterals (pins del HAT entrant als forats de la RPi):

   [HAT SX1262 LoRa]
   ┌──────────────┐
   │              │
   │  [Xip SX1262]│  ← el xip gran
   │              │
   │  [Antena SMA]│
   └─┬─┬──────────┘
     │ │      ← pins GPIO
   ┌─┴─┴──────────┐
   │  [Separador]  │
   │  [RPi 4]      │
   │  [USB-C etc]  │
   └────────────────┘
```

## Pas 4: Cargolar el HAT als separadors (2 min)

1. Agafa els 2 cargols M2.5 que et queden
2. Per cada forat del HAT que coincideix amb un separador, cargola'ls
3. ⚠️ No cargolis massa fort — podries trencar la RPi

## Pas 5: Comprovar l'antena (1 min)

1. Assegura't que l'antena està **cargolada** al connector SMA
2. L'antena ha d'estar **vertical** (cap amunt), no horitzontal
3. Si tens l'antena per separat, cargola-la fent-la girar en sentit horari fins que faci contacte (no massa fort!)

## Pas 6: Verificar (3 min)

Abans d'endollar la RPi:

✅ **Comprova que**:
- Els pins GPIO del HAT estan **ben alineats** amb els de la RPi
- Cap pin está **doblegat** o **trencat**
- Els **2 cargols** dels separadors estan **cargolats**
- L'**antena** està **cargolada al SMA**
- El HAT queda **paral·lel** a la RPi, no inclinat
- **NO hi ha cap cosa metàl·lica** sota el HAT que toqui la RPi (causes curtcircuit!)

Si tot és correcte, pots **endollar la RPi** per primera vegada.

---

## Què passarà quan endollis

1. La RPi encén un **LED vermell** (power)
2. El HAT encén un **LED verd** (si en té)
3. La RPi arrenca (~30 segons)
4. Si has preconfigurat la microSD amb SSH i WiFi, ja pots connectar-te

## Què fer DESPRÉS (un cop la RPi arrenqui)

Connecta't per SSH des del Mac:

```bash
ssh bernat@hort-pi.local
```

I comprova que el HAT es detecta correctament:

```bash
# Comprovar SPI esta activat
ls /dev/spi*
# Ha de mostrar: /dev/spidev0.0  /dev/spidev0.1

# Comprovar GPIO del HAT (pin BUSY = GPIO 20)
raspi-gpio get 20
# Ha de mostrar el pin i el seu estat
```

Si `/dev/spi*` no mostra res, haurem d'activar SPI amb `sudo raspi-config`.

## Si els pins NO venen soldats al HAT

A vegades el HAT ve **sense els pins soldats** (perquè siguis tu qui decideixi com muntar-ho). En aquest cas:

1. **Opció fàcil**: porta'l a una botiga d'electrònica i que te'ls soldin (~5-10 €)
2. **DIY**: soldar tu mateix, per la part de sota del HAT, amb soldador i estany. **Necessita pràctica** — no ho intentis per primer cop amb un HAT de 30 €

## Resum visual

```
                    ❌ NO ❌                          ✅ SÍ ✅
                    
  HAT massa alt                      HAT ben muntat
  (sense separadors)                  
                                     
  ┌────────┐                         ┌────────┐
  │  HAT   │                         │  HAT   │
  └────────┘                         └────────┘
  ════════════                        │  pins  │
  ┌────────┐                         ┌────────┐
  │  RPi   │  ← curtcircuit!        │  RPi   │
  └────────┘    │ │ toca             └────────┘
  ════════════                        ════════════
                                     
                                      (amb separadors!)
```

## Dubtes freqüents

**P: He de soldar res?**
R: Si els pins GPIO ja vénen soldats al HAT (la majoria), no. Si no, cal soldar.

**P: I si l'antena no ve cargolada?**
R: Vindrà en una bossa a part. Cargola-la al connector SMA (sentit horari, sense massa força).

**P: L'orientació del HAT importa?**
R: Sí! El connector de l'antena ha d'estar **mirant cap amunt** (lluny de la RPi), no cap avall.

**P: Puc tocar el xip SX1262?**
R: Millor no — el greix dels dits pot fer malbé les soldadures. Agafa'l pels costats.

**P: Què passa si un pin es doblega?**
R: Amb un tornavís pla petit, redreça'l amb molt de compte. Si es trenca, toca soldar de nou (o comprar un HAT nou).
