# Projectes per a la Raspberry Pi (independentment de l'hort IoT)

Llista d'idees i projectes que pots muntar amb la Raspberry Pi,
independents del projecte principal de l'hort. Útils per quan vulguis
experimentar amb la RPi sense tenir el hardware de l'hort a punt.

## 1. Servidor domèstic

### Pi-hole (bloquejador d'anuncis a tota la xarxa)

```bash
curl -sSL https://install.pi-hole.net | bash
```

**Què fa**: bloqueja anuncis i trackers per a TOTS els dispositius
de la teva WiFi. Funciona com a DNS sinkhole.

**Utilitat**: navegació més ràpida, menys consum de dades, privadesa.

### Servidor web personal

```bash
sudo apt install nginx php-fpm
```

**Què pots fer**:
- Allotjar la teva pàgina personal
- Servir el portal d'Hort Osona
- Self-hosted Git (Gitea)
- Servidor de fitxers (Nextcloud)

### Nextcloud (núvol personal)

```bash
sudo snap install nextcloud
```

**Què fa**: alternativa pròpia a Google Drive / Dropbox. 100% privadesa.

## 2. Media center

### Plex o Jellyfin (servidor multimèdia)

```bash
curl https://repo.jellyfin.org/install-debuntu.sh | sudo bash
```

**Què fa**: converteix la RPi en un servidor de pel·lícules/sèries
accessible des de la TV, mòbil, tablet, etc.

**Necessites**: un disc dur extern amb les teves pel·lícules.

### RetroPie (emulador de jocs retro)

```bash
sudo apt install retropie
```

**Què fa**: emula consoles antigues (NES, SNES, Mega Drive, PS1, etc.)
amb els jocs que ja tens.

**Necessites**: un gamepad USB i ROMs (que has de tenir legalment).

## 3. Automatització de la casa

### Home Assistant (domòtica)

```bash
sudo apt install homeassistant
```

**Què pots fer**:
- Controlar llums (Philips Hue, Sonoff, etc.)
- Termòstats intel·ligents
- Sensors de porta/finestra
- Automatitzacions ("quan arribo a casa, encén els llums")
- Integrar amb el temps, calendari, etc.

**És el projecte maker més popular del món** per a RPi.

### Monitor de consum elèctric

Amb un sensor de corrent (CT clamp) connectat a l'ADC de la RPi pots
monitorar el consum de cada aparell de casa teva en temps real.

**Cost**: ~20 € (sensor SCT-013)

## 4. Serveis de xarxa

### Servidor VPN (WireGuard)

```bash
sudo apt install wireguard
```

**Què fa**: connexió segura quan estàs fora de casa (WiFi pública,
hotel, etc.). Pots accedir a la teva xarxa domèstica com si fossis a casa.

### AdGuard Home (alternativa a Pi-hole)

```bash
curl -s -S -L https://raw.githubusercontent.com/AdguardTeam/AdGuardHome/master/scripts/install.sh | sh -s -- -v
```

**Avantatges vs Pi-hole**:
- Interfície web més bonica
- Configuració per-client
- Suport per a DoH (DNS over HTTPS)

### Servidor de jocs LAN

Minecraft, Terraria, Valheim, etc. La RPi 4 pot gestionar servidors
petits per jugar amb amics.

```bash
# Minecraft
wget https://launcher.mojang.com/v1/objects/.../server.jar
java -Xmx1024M -Xms1024M -jar server.jar nogui
```

## 5. Aprenentatge / educació

### Servidor LLM local (el que ja tenim!)

```bash
ollama serve
ollama pull hermes3
```

**Models bons en català**:
- `hermes3` (4.7 GB, recomanat)
- `llama3.1:8b` (Meta)
- `qwen2.5:7b` (excel·lent multilingüe)
- `gemma2:9b` (Google)

### RAG local (el que ja tenim!)

El sistema que hem muntat amb `rag.py` et permet preguntar a la teva
base de coneixement personal en català. Pots adaptar-lo a:

- Preguntar als teus apunts
- Preguntar a manuals tècnics
- Preguntar a la teva biblioteca de receptes
- Preguntar a documentació mèdica (amb precaució)

### Programació i CI/CD

```bash
# Instal·lar Gitea (alternativa a GitHub)
wget -O gitea https://dl.gitea.com/gitea/1.21/gitea-1.21-linux-arm-6
chmod +x gitea
```

Pots tenir el teu propi GitHub personal amb issues, PRs, wiki, etc.

## 6. Internet de les Coses (IoT)

### Gateway MQTT (Mosquitto)

```bash
sudo apt install mosquitto mosquitto-clients
```

Permet que tots els teus dispositius IoT es comuniquin entre ells.

### Node-RED (programació visual per a IoT)

```bash
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```

**Què fa**: eina visual per crear fluxos de dades amb nodes drag&drop.
Ideal per a automatitzacions complexes sense programar.

### Monitor ambiental

Amb sensors BME280 (T, H, P) pots monitorar:
- Temperatura i humitat de cada habitació
- Qualitat de l'aire (amb sensor SGP30)
- Pressió atmosfèrica

Tot visible des d'una web responsive.

## 7. Seguretat i vigilància

### Servidor de càmeres (motionEye)

```bash
sudo pip install motioneye
```

**Què fa**: servidor de videovigilància amb detecció de moviment.
Pots accedir des del mòbil.

**Necessites**: càmeres IP o USB.

### PiVPN (servidor VPN fàcil)

```bash
curl -L https://install.pivpn.io | bash
```

**Avantatges**:
- Setup guiat (pregunta pas a pas)
- Suporta WireGuard i OpenVPN
- Auto-configura el firewall

## 8. Educatiu / nens

### Scratch 3 offline

```bash
sudo apt install scratch3
```

Programació visual per a nens. Pot fer-se servir sense internet.

### Minecraft Pi Edition

```bash
sudo apt install minecraft-pi
```

Versió especial de Minecraft per a RPi, amb API de Python per
programar dins del joc.

### RetroAchievements (gaming + accomplishments)

Complement per RetroPie que afegeix "achievements" als jocs retro.

## 9. Productivitat personal

### Servidor de calendaris (Radicale)

```bash
sudo pip install --upgrade radicale
```

Calendaris i contactes sincronitzats entre dispositius, sense Google.

### Servidor de notes (Joplin Server)

```bash
# Versio Docker
docker run -d --name joplin-server ...
```

Notes xifrades, sincronitzades, accessibles des de qualsevol dispositiu.

## 10. Hobby / experimentació

### Estació meteorològica

Amb sensors BME280, pluviòmetre, anemòmetre pots muntar una estació
meteorològica completa amb gràfiques històriques.

**Cost**: ~50 €

### Ràdio definida per programari (SDR)

Amb un receptor USB RTL-SDR (~25 €) pots:
- Escoltar ràdio AM/FM
- Escoltar trucades de ràdio amateur
- Rebat metalls d'avions (ADS-B)
- Rep telemes de satèl·lits

**Cost**: 25 € (RTL-SDR dongle)

### AstroPi (estació espacial ISS)

La RPi Zero 2 W és igual que les que van a l'Estació Espacial
Internacional. Pots simular experiments semblants als que fan els
astronautes.

## Prioritats recomanades

Si acabes d'arribar al món de la RPi:

1. **Pi-hole** (15 min, útil des del primer dia)
2. **Tailscale** (5 min, accés segur des de fora)
3. **Nextcloud** (30 min, núvol personal)
4. **Home Assistant** (1-2 h, domòtica)
5. **Plex/Jellyfin** (30 min, media center)
6. **Minecraft Pi** (15 min, diversió amb nens)

## Recursos

- [Raspberry Pi Foundation](https://www.raspberrypi.org/)
- [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)
- [PiMyLifeUp](https://pimylifeup.com/) — tutorials pas a pas
- [r/selfhosted](https://www.reddit.com/r/selfhosted/) — comunitat

## Notes

- Tots aquests serveis poden coexistir en una sola RPi 4 (4 GB)
- Per a molts serveis, una RPi Zero 2 W és insuficient
- La RPi 4 (4 GB) és la més versàtil per a múltiples serveis
- Usa Docker (`docker compose`) per aïllar serveis i facilitar backups
