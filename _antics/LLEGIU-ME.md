# _antics — generadors retirats (2026-09-26)

Aquí hi ha els generadors que **ja no s'usen**. Es conserven per si cal consultar
com es feia alguna cosa, però **no s'han d'executar**: escriuen un `index.html`
a l'arrel del repo i el sobreescriurien amb el disseny vell.

| Fitxer | Què era |
|---|---|
| `build_portal_v1.py` | El primer portal (menú desplegable + visor de documents). |
| `build_site.py` | Un tercer intent (SPA a `site/`). Mai no va ser el publicat. |

**El generador bo, l'únic actiu, és `build_web.py`** (a l'arrel). Fa tota la web:
portada amb el mes i les associacions, calendari, cultius, fitxes, documents i PWA.
`md_render.py` és la seva biblioteca (conversor markdown→HTML i llista de documents),
extreta de l'antic `build_portal_v2.py`.

Per generar la web: `python3 build_web.py --out preview`
Per publicar-la: `./publicar.sh --si`
