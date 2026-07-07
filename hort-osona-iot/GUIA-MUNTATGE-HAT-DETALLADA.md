# Muntar el HAT SX1262 LoRa a la RPi 4 — Guia SUPER detallada

Aquesta guia és per si la primera no t'ha quedat clara. Anem **pas a pas
absolut**, sense pressuposar res.

## 🧰 El que necessites tenir a la taula

1. La RPi 4 (nua, sense res connectat)
2. El HAT SX1262 LoRa (amb els pins GPIO)
3. Els 2 separadors (torrets) metàl·lics
4. Els 2 cargols M2.5
5. Un tornavís Phillips (estrella) petit
6. Una taula plana i ben il·luminada
7. Els teus ulls (i si tens, ulleres de lectura)

⚠️ **RPi DESENDOLLADA** durant tot el procés.

---

## Pas 0: Identificar les parts (1 min)

Agafa el HAT i mira'l amb cura. Hauries de veure:

- **Una antena** cargolada a un connector daurat (l'anomenat SMA) — al costat
- **Un xip negre quadrat** gran (és el SX1262) — al centre
- **Una tira de 40 pins mascle** a la part de sota (són les pues que connecten a la RPi)
- **4 forats** als cantons (2 amb forats rodons, 2 amb forats quadrats)
- **Possibles LEDs** (verd, vermell, blau)

A la RPi 4 hauries de veure:

- **40 forats quadrats** a la part de dalt (els GPIO pins)
- **4 forats rodons** als cantons (per cargolar)
- Un **xip quadrat** al centre (la CPU)
- Diversos connectors als costats

---

## Pas 1: Posar la RPi dreta sobre la taula (30 seg)

1. Agafa la RPi
2. Posa-la **horitzontal** sobre la taula
3. **Connectors USB mirant cap a tu** (cap avall de la taula)
4. La tira de **40 forats GPIO ha d'estar a la part de DALT** (allunyada de tu)

```
   DALT  (lluny de tu)
   ┌────────────────────────────────────┐
   │ [40 forats GPIO]    <- el HAT va aquí
   ├────────────────────────────────────┤
   │                                    │
   │          [RPi]                     │
   │                                    │
   ├────────────────────────────────────┤
   │ [USB-C] [USB-A] [USB-A] [Ethernet] │ <-- connectors
   └────────────────────────────────────┘
   BAIX  (cap a tu)
```

---

## Pas 2: Identificar on van els separadors (1 min)

Mira la RPi. Veuràs **4 forats** rodons petits:
- 2 a la **part de dalt** (prop dels GPIO)
- 2 a la **part de baix** (prop dels USB)

⚠️ **NO posis els separadors als 2 forats de la PART DE BAIX** (els del costat dels USB).
✅ **POSA-LOS als 2 forats de la PART DE DALT** (els que estan més a prop dels GPIO).

Per què? Perquè el HAT ha d'anar a la part de dalt, i els separadors l'aguanten allà.

```
   DALT
   ┌────────────────────────────────────┐
   │ ⓞ [40 forats GPIO]  ⓞ <-- posar aquí els 2 separadors
   ├────────────────────────────────────┤
   │                                    │
   │          [RPi]                     │
   │                                    │
   ├────────────────────────────────────┤
   │ ⓞ [USB...]  ⓞ <-- NO posar res aquí
   └────────────────────────────────────┘
   BAIX
```

---

## Pas 3: Cargolar els 2 separadors (3 min)

Necessites: 2 separadors + 2 cargols M2.5 + tornavís

1. Agafa **un separador** (el troç metàl·lic amb un forat al mig)
2. **Passa'l pel forat de DALT-DRETA** de la RPi, **des de dalt** (la part llarga del separador cap amunt)
3. Per la part de sota de la RPi, **cargola un cargol M2.5** amb el tornavís
4. **No cargolis massa fort!** Només ferma, no cal estrènyer
5. Repeteix amb el **forat de DALT-ESQUERRA**

Si no tens una tercera mà, pots:
- Posar la RPi sobre la cantonada d'un llibre gruixut (que sobresurti de la taula)
- Així el forat queda penjant i pots cargolar per sota

**Comprova**: els 2 separadors han de sortir **cap amunt** de la RPi, com dues columnes.

---

## Pas 4: Agafar el HAT i orientar-lo (2 min)

1. Agafa el HAT amb **dues mans** pels costats
2. Dona-li la volta (pins GPIO cap avall, cara amb components cap amunt)
3. Mira'l des de la perspectiva dels pins:
   - L'**antena SMA** ha d'estar **mirant cap amunt** (cap a la part de la RPi allunyada de tu)
   - Els **40 pins** han d'estar **mirant cap avall** (cap a la RPi)
   - Els **4 forats del HAT** han de coincidir amb els **2 separadors** de la RPi + 2 forats de la RPi

**Visualització** (mirant des de la part de sobre):

```
   ┌────────────────────────────────────┐
   │  [Connector antena SMA]            │  <- a DALT
   │                                    │
   │  [Xip SX1262]                      │
   │                                    │
   │  [40 pins mascle] ⓞ ⓞ <-- forats del HAT
   └────────────────────────────────────┘
```

---

## Pas 5: L'alineació perfecta (la part difícil) (3 min)

Aquest és el pas on la gent s'equivoca. Vés a poc a poc:

1. **Mira els 40 pins** del HAT (una tira de pues metàl·liques)
2. **Mira els 40 forats** de la RPi (una tira de forats quadrats)
3. **Alinieja'ls**:
   - El pin 1 del HAT ha d'anar al forat 1 de la RPi
   - El pin 40 del HAT ha d'anar al forat 40 de la RPi
4. **Comprova** que el HAT està **paral·lel** a la RPi (no inclinat)
5. **Comprova** que els **2 forats** del HAT coincideixen amb els **2 separadors** que has posat

**Consell**: posa el HAT a 1 cm per sobre de la RPi, mira des del costat si els pins estan alineats, i quan estiguin, baixa'l a poc a poc.

---

## Pas 6: Pressionar el HAT cap avall (1 min, amb cura)

1. Agafa el HAT amb els **2 polzes** sobre la part central (no als costats, on podries doblegar alguna cosa)
2. Amb els **2 dits índex**, aguanta la RPi per sota (o deixa-la sobre la taula)
3. **Pressiona** amb els polzes, **a poc a poc**, repartint la força per igual
4. Has de sentir que els pins **"xupen"** suaument cap a dins
5. **Continua pressionant** fins que el HAT toqui els separadors
6. ⚠️ Si notes que **un pin es resisteix** o **no entra**, **atura't** i mira des del costat

**Comprova**:
- El HAT està horitzontal?
- Tots els 40 pins estan igual de profunds?
- Els 2 forats del HAT coincideixen amb els 2 separadors?

Si tot és correcte, ja està! Salta al pas 7.

Si un pin es doblega, veure's **Mètode de recuperació** al final.

---

## Pas 7: Cargolar el HAT als separadors (2 min)

1. Agafa els **2 cargols M2.5** que et queden
2. Per cada forat del HAT que coincideix amb un separador:
   - Posa el cargol a la part de dalt del HAT
   - Cargola'l al separador amb el tornavís
   - **No massa fort** — podries trencar la RPi

---

## Pas 8: Verificar l'antena (30 seg)

1. Mira l'antena al connector SMA
2. Ha d'estar **cargolada** (no fluixa)
3. L'antena ha d'estar **vertical** (cap amunt)
4. Si la vols doblegar, millor **horitzontal** i cap amunt — mai cap avall

---

## ✅ Comprovació final (1 min)

Abans d'endollar la RPi, comprova **TOT**:

- [ ] Els **40 pins** del HAT estan **ben endollats** als 40 forats de la RPi
- [ ] **Cap pin** està **doble** o **fora** del forat
- [ ] El HAT queda **horitzontal** (no inclinat)
- [ ] Els **2 cargols** dels separadors estan **cargolats**
- [ ] L'**antena** està **cargolada** al SMA
- [ ] **Cap cosa metàl·lica** toca la RPi per sota (curtcircuit!)

Si tot és correcte, **endolla la RPi** amb el cable USB-C. Hauries de veure:
- **LED vermell** encès (power)
- **LED verd** parpellejant (activitat del sistema)
- Després d'1-2 minuts, el **LED del HAT** (si en té) pot encendre's

---

## 🆘 Mètode de recuperació: si un pin es doblega

1. **NO CONTINUIS** pressionant — atura't
2. Agafa un **tornavís pla petit** (molt fi)
3. Amb molt de compte, redreça el pin doblegat
4. Comprova des del costat que el pin queda vertical
5. Torna a intentar el pas 6

Si el pin es trenca (es parteix o es doblega massa), toca soldar de nou o canviar el HAT.

---

## 📞 Què fer si no t'hi veus

Si la taula no té bona llum, **posa la RPi sota una làmpada** o **obre el mòbil amb llanterna** apuntant a la RPi. És molt important veure els pins clarament.

Si tens **gent a casa** que t'ajudi, **dona'ls la RPi per aguantar** mentre tu mous el HAT. 4 mans són millors que 2.

---

## 🎬 Un cop muntat

Ja pots:
1. Inserir la microSD a la RPi (amb el sistema operatiu)
2. Endollar el USB-C
3. Esperar 60-90 segons
4. Connectar per SSH: `ssh bernat@hortosona.local`
5. Gaudir del sistema!

---

## Què pot fallar i com resoldre-ho

| Problema | Solució |
|---|---|
| Un pin es doblega | Redreçar amb tornavís pla petit |
| El HAT no acaba d'entrar | Comprovar que està ben alineat (pas 5) |
| Els separadors no caben | Provar els altres 2 forats de la RPi |
| No tinc tornavís | Usar la punta d'un ganivet o tisores planes (amb compte!) |
| L'antema no es cargola | Normal — forçar suaument, no massa |
| El HAT queda tort | Tornar a posar — no cal soldar res |
| Em fa por fer-ho malament | Demana ajuda a algú, o porta-ho a una botiga d'electrònica |
