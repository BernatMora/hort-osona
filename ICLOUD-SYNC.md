# Sincronització amb iCloud Drive

## Què hem fet

Hem creat un **symlink** a iCloud Drive que apunta a la carpeta del projecte
`~/Desktop/hort-osona/`. Això vol dir que:

- ✅ Tots els canvis al projecte es sincronitzen **automàticament** al núvol
- ✅ Pots accedir al projecte des de l'iPhone (app Fitxers)
- ✅ Tens backup al núvol sense esforç
- ✅ Tens 2 TB de capacitat (el projecte ocupa 68 MB)

## Com funciona

```
~/Library/Mobile Documents/com~apple~CloudDocs/Hort-Osona
    ↓ (symlink)
~/Desktop/hort-osona/
```

iCloud Drive segueix el symlink i sincronitza tota la carpeta.

## Com accedir des de l'iPhone

1. Obre l'app **Fitxers** (Files)
2. Toca **"iCloud Drive"** (a la pestanya "Recursos" o "Browse")
3. Busca la carpeta **"Hort-Osona"**
4. Tindràs tots els .md disponibles per llegir (ideal per consultar l'hort al camp!)

## Què hem descartat

Abans de crear el symlink, hi havia una còpia antiga a iCloud (17 MB, del
10 de juny 2026) que **no estava sincronitzada** amb el projecte. Hem fet:

1. **Backup** de la còpia antiga a `~/Desktop/hort-osona-icloud-backup-20260706/`
2. **Eliminació** de la carpeta antiga
3. **Creació** del symlink net

Si mai necessites algun fitxer antic, és al backup.

## Comandos útils

```bash
# Comprovar l'estat
~/Desktop/hort-osona/hort-osona-iot/scripts/setup_icloud_hort.sh status

# Eliminar el symlink (si vols)
~/Desktop/hort-osona/hort-osona-iot/scripts/setup_icloud_hort.sh remove

# Recrear el symlink
~/Desktop/hort-osona/hort-osona-iot/scripts/setup_icloud_hort.sh
```

## Casos d'ús

- **Estàs al camp, sense Mac**: obre l'iPhone, l'app Fitxers, llegeix la fitxa
  de tomàquets per veure quan regar
- **Vols afegir fotos de l'hort**: fes-les al Mac, van a `~/Desktop/hort-osona/`,
  es sincronitzen a l'iPhone
- **Modifiques un .md al Mac**: l'iPhone ho veu en segons
- **El Mac es mor**: tens còpia completa a iCloud, pots descarregar-la al nou Mac

## Notes

- iCloud Drive trigarà uns minuts la primera vegada a pujar 68 MB
- Si la sincronització no apareix, obre System Settings → Apple ID → iCloud →
  iCloud Drive i comprova que està actiu
- Per forçar sincronització: obre Finder → iCloud Drive → Hort-Osona →
  botó dret → "Download Now"
