# Llista de compra Hort Osona IoT

> Versió curta per imprimir. Llista completa amb alternatives a `PEDIDO-AMAZON.md`.

## Resum

- **Cost total estimat**: ~220€
- **Temps d'entrega**: 1-2 dies
- **Estratègia**: Tot d'Amazon España

---

## Llista per secció

### 🖥️ Raspberry Pi 4B (core)

| # | Producte | Preu |
|---|---|---|
| 1 | Raspberry Pi 4 Model B 4GB (Kubii o Amazon) | 55-65€ |
| 2 | Carregador USB-C 5V/3A oficial | 12-15€ |
| 3 | MicroSD 32GB Classe 10 A2 (Sandisk o Samsung) | 8-12€ |
| 4 | Carcassa alumini + dissipador | 10-15€ |

### 📡 Sensors i LoRa

| # | Producte | Quant. | Preu |
|---|---|---|---|
| 5 | Xiaomi MiFlora 4-en-1 (humitat, llum, T, fertilitat) | 3 | 45€ |
| 6 | Xiaomi Mi Thermometer 2 (T + humitat aire) | 1 | 8€ |
| 7 | TTGO LoRa32 V2 (868MHz, NO 915MHz) | 2 | 40€ |
| 8 | Antena 868MHz 5dBi SMA | 1 | 5€ |
| 9 | Caixa estanca IP65 158×90×65mm | 1 | 5€ |

### 🔋 Solar (per al pont a l'hort)

| # | Producte | Preu |
|---|---|---|
| 10 | Panell solar 5V/2W USB | 12€ |
| 11 | Bateria 18650 3000mAh | 5€ |
| 12 | Mòdul TP4056 AMB PROTECCIÓ | 3€ |

### 🔌 Cables

| # | Producte | Preu |
|---|---|---|
| 13 | Pack cables Dupont + resistències | 5€ |
| 14 | Cable Ethernet Cat6 1m | 3€ |

**TOTAL ESTIMAT: ~225€**

---

## Coses importants a recordar

### ⚠️ Versions crítiques
- **TTGO LoRa32**: ha de ser **868MHz** (UE), mai 915MHz (US)
- **TP4056**: ha de portar **xip DW01A** de protecció
- **MicroSD**: ha de ser **classe A2** (no només A1)

### ⚠️ On comprar per seguretat
- **Raspberry Pi 4**: directament a **Kubii** o **Melopero** (evitar venedors tercers amb poques valoracions)
- **MiFlora originals**: marca Xiaomi, no còpies barates
- **TTGO**: venedor amb valoracions + especificar "868MHz" al títol

---

## Després de rebre

1. **Obre tots els paquets** i comprova que no falta res
2. **Comprova el número de sèrie** de la Raspberry (ha de ser P4B 4GB)
3. **Carrega la Raspberry** amb Raspberry Pi Imager + Raspberry Pi OS Lite 64-bit
4. **Executa `setup-pi.sh`** (veure `INICI-RAPID.md`)
5. **Flasheja els TTGO** amb el codi de `bridge/`

---

## Adreces útils

- **PWA Hort Osona**: https://BernatMora.github.io/hort-osona/
- **Llista completa**: `PEDIDO-AMAZON.md`
- **Guia ràpida**: `INICI-RAPID.md`
- **Documentació completa**: `README.md`
- **Repo GitHub**: https://github.com/BernatMora/hort-osona

---

*Imprimit el 2026-07-03 per Bernat Mora — Vic, Osona*
