# My Cloud Home + Hort Osona — Guia completa

## Visió general

El My Cloud Home és un NAS (Network Attached Storage) de Western Digital
que tens a la teva xarxa local. L'hem descobert a **192.168.100.48**.

```
                      ┌─────────────────┐
   LoRa 868MHz        │   My Cloud Home │     HTTP/SMB
   ────────────>     │   192.168.100.48│  <───────────  Mac (Finder)
                      │   2TB+ (varies)│
                      └─────────────────┘
                              ▲
                              │ SMB/CIFS
                              │
                      ┌─────────────────┐
                      │  Raspberry Pi   │
                      │  (receptor LoRa)│
                      └─────────────────┘
```

## Com accedir al My Cloud Home

### 1. Des del Finder (Mac)

Ja tens accés pel Finder. Obre la carpeta `Public/`.

**Si no el tens connectat:**
1. Finder → Xarxa
2. Busca el **My Cloud Home** (o `192.168.100.48`)
3. Fes login amb el compte WD
4. Selecciona la carpeta `Public`

### 2. Des del navegador web

Obre: `http://192.168.100.48/`

Veuràs el **Admin Dashboard** de WD amb:
- Llista d'usuaris
- Carpetes compartides
- Configuració del dispositiu

### 3. Des de la Raspberry Pi (quan arribi)

Muntar via SMB:

```bash
# Instal·lar CIFS
sudo apt install cifs-utils

# Crear punt de muntatge
sudo mkdir -p /mnt/mycloudhome

# Muntar (sense contrasenya si Public es obert)
sudo mount -t cifs //192.168.100.48/Public /mnt/mycloudhome \
    -o guest,uid=1000,gid=1000,iocharset=utf8

# Comprovar
ls /mnt/mycloudhome
```

**Per muntar automàticament al boot**, afegir a `/etc/fstab`:

```
//192.168.100.48/Public /mnt/mycloudhome cifs guest,uid=1000,gid=1000,iocharset=utf8 0 0
```

## Estructura creada

Quan executis `./setup-mycloudhome.sh` es crea:

```
/Public/hort-osona/
├── data/
│   ├── 2026/                # Dades any 2026
│   │   └── 07-juliol-hort-1.jsonl
│   ├── 2027/                # Dades any 2027
│   └── backups/             # Còpies de seguretat
├── portal/                  # Portal web
│   ├── index.html          # Pàgina principal
│   ├── docs/               # 78 documents
│   ├── search_index.json   # Índex de cerca
│   ├── manifest.json       # PWA
│   └── assets/
├── scripts/                 # Scripts útils
├── config/                  # Configuració
└── README.md                # Aquest fitxer
```

## Usos

### 1. Emmagatzemar dades del node IoT 🌱

Quan el node LoRa enviï dades a la RPi, es guardaran:

**Online (Supabase):** accessible des de qualsevol lloc
**Local (My Cloud Home):** dades històriques, gràfiques llargues, backup

```python
# A la RPi:
from mycloud_storage import MyCloudStorage

storage = MyCloudStorage("/mnt/mycloudhome/hort-osona")
storage.save_measurement({
    "ts": "2026-07-06T12:00:00Z",
    "node_id": "hort-1",
    "temperatura_c": 18.5,
    "humitat_sol_pct": 45,
    "bateria_v": 3.92,
    "rssi_dbm": -85
})
```

Això guarda:
- ✅ A `data/2026/07-juliol-hort-1.jsonl` (text pla, fàcil de processar)
- ✅ A `data/db.sqlite` (BD local, consultable)

### 2. Allotjar el portal Hort Osona 🌐

El portal web pot estar allotjat al My Cloud Home:

**Avantatges:**
- Accessible des de tota la xarxa local
- No depèn d'internet
- Còpia de seguretat automàtica (si actives Time Machine)

**Com:**
```bash
./deploy-portal-mychoudhome.sh
```

Després pots accedir a:
- `http://192.168.100.48/Public/hort-osona/portal/index.html`
- `http://192.168.100.48/Public/hort-osona/portal/`

## Configuració de Supabase + My Cloud Home

```
  [Node LoRa]            [RPi]              [My Cloud Home]
      │                    │                       │
      │ Paquet JSON        │                       │
      ├───────────────────>│                       │
      │  (868 MHz)         │                       │
      │                    │                       │
      │                    │ 1. save_measurement() │
      │                    ├──────────────────────>│
      │                    │   (SQLite + JSONL)    │
      │                    │                       │
      │                    │ 2. Supabase insert    │
      │                    ├──────────>            │
      │                    │                       │
      │                    │ 3. Ollama consell     │
      │                    ├──────────>            │
      │                    │                       │
      │                    │ 4. Supabase consell   │
      │                    ├──────────>            │
      │                    │                       │
      │                    │ 5. save_advice()      │
      │                    ├──────────────────────>│
```

Per tant tens **dues còpies** de cada mesura:
- **Online** (Supabase): per veure des del mòbil, en viatges
- **Local** (My Cloud Home): per anàlisi llarg, gràfiques històriques

## Comandes útils

### Des del Mac

```bash
# Muntar el My Cloud Home (si no esta automatic)
mount -t smbfs //bernatmora@192.168.100.48/Public /Volumes/MyCloudHome

# Desar tot el portal
~/Desktop/hort-osona/hort-osona-iot/deploy-portal-mychoudhome.sh

# Crear l'estructura de carpetes
~/Desktop/hort-osona/hort-osona-iot/setup-mycloudhome.sh
```

### Des de la RPi

```bash
# Muntar
sudo mount -t cifs //192.168.100.48/Public /mnt/mycloudhome -o guest

# Provar el storage Python
cd /opt/hort-osona-iot
source venv/bin/activate
python3 mycloud_storage.py
```

## Avantatges vs Supabase

| Característica | My Cloud Home | Supabase |
|---|---|---|
| **Emmagatzematge** | Il·limitat (TB) | Fins a 500 MB gratis |
| **Velocitat d'escriptura** | Ràpida (xarxa local) | Limitada (internet) |
| **Accés des de fora** | Només amb VPN/Tailscale | Des de qualsevol lloc |
| **Privadesa** | Total (a casa) | Al núvol |
| **Cost** | Un sol pagament | Gratuït (amb limits) |
| **Consultes SQL** | Només local | Temps real |
| **Backup** | Si (Time Machine) | Automàtic |

## Limitacions del My Cloud Home

⚠️ **El My Cloud Home NO és un Linux complet** com un NAS tradicional:
- No pots instal·lar-hi Docker
- No pots fer-hi servir com a servidor web complet
- Té una interfície web limitada
- Per allotjar el portal, hem de confiar que WD permeti servir fitxers estàtics

**Alternativa més potent** (quan vulguis):
- Raspberry Pi 4 amb Nextcloud (veure `RPi-PROJECTES.md`)
- Raspberry Pi 4 amb Caddy/Nginx (servidor web complet)

## Troubleshooting

### El Mac no troba el My Cloud Home

1. Comprovar que el LED del My Cloud Home està encès
2. Comprovar el router que encara està connectat
3. Provar `ping 192.168.100.48` des del Mac
4. Reiniciar el My Cloud Home (desendollar 30 segons)

### La RPi no pot muntar

```bash
# Comprovar connectivitat
ping 192.168.100.48

# Comprovar CIFS
sudo apt install cifs-utils

# Muntar amb debug
sudo mount -t cifs //192.168.100.48/Public /mnt/mycloudhome -o guest,vers=3.0
```

### El portal no carrega

1. Comprovar que `index.html` existeix a `/Public/hort-osona/portal/`
2. Comprovar que el My Cloud Home serveix HTTP (port 80 obert)
3. Alguns My Cloud Home requereixen que la carpeta `Public` estigui compartida
4. Comprovar permisos: `chmod -R 755 /Public/hort-osona/portal/`

## Còpies de seguretat recomanades

1. **Time Machine al Mac** (recomanat)
   - Sistema Settings → General → Time Machine
   - Selecciona el My Cloud Home com a disc
   - Còpies cada hora automàticament

2. **Snapshot local** (manual)
   ```bash
   rsync -av /Volumes/Public/hort-osona/ ~/Backups/hort-osona-snap/
   ```

3. **Rètol diari** (senzill)
   ```bash
   cp -r /mnt/mycloudhome/hort-osona/data /tmp/data-$(date +%Y%m%d)
   ```

## Resum

| Què | On | Avantatge |
|---|---|---|
| Portal web | My Cloud Home | Ràpid, sense internet |
| Dades IoT | Supabase + My Cloud Home | Online + còpia local |
| Còpies seguretat | Time Machine → My Cloud Home | Automàtic |
| Scripts | RPi | Processat localment |

Endavant! 🌱
