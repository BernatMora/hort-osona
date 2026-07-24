"""Actualitza la portada d'Hort Osona per mostrar el pla del mes actual.

Us:
    python set_current_month.py              # Usa el mes actual
    python set_current_month.py 2026-08      # Força un mes concret
    python set_current_month.py 2026-08-agost  # Força un mes concret (amb nom)
"""
import re
import sys
import datetime
from pathlib import Path

MESOS_CAT = [
    'gener', 'febrer', 'març', 'abril', 'maig', 'juny',
    'juliol', 'agost', 'setembre', 'octubre', 'novembre', 'desembre'
]


def main():
    p = Path(r"C:\Users\iadmin\bernatlab\projects\hort-osona\index.html")

    # Determinar el mes
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if re.match(r'^\d{4}-\d{2}$', arg):
            any_mes = arg.split('-')
            any_actual = int(any_mes[0])
            mes_actual = int(any_mes[1])
            nom_mes = MESOS_CAT[mes_actual - 1]
        elif re.match(r'^\d{4}-\d{2}-[a-zà-ú]+$', arg):
            parts = arg.split('-')
            any_actual = int(parts[0])
            mes_actual = int(parts[1])
            nom_mes = parts[2]
        else:
            print(f"Format invalid: {arg}")
            print("Formats acceptats: 2026-08 o 2026-08-agost")
            sys.exit(1)
    else:
        avui = datetime.date.today()
        any_actual = avui.year
        mes_actual = avui.month
        nom_mes = MESOS_CAT[mes_actual - 1]

    # Format del nom de fitxer
    nom_fitxer = f"{any_actual}-{mes_actual:02d}-{nom_mes}.html"
    url_pla = f"plans-mensuals/{nom_fitxer}"

    # Comprovar que el fitxer existeix
    fitxer_complet = p.parent / "docs" / "plans-mensuals" / nom_fitxer
    if not fitxer_complet.exists():
        print(f"[WARN] No existeix el fitxer: {nom_fitxer}")
        for mes in range(mes_actual, 0, -1):
            nom_mes_trobar = MESOS_CAT[mes - 1]
            fitxer_trobar = p.parent / "docs" / "plans-mensuals" / f"{any_actual}-{mes:02d}-{nom_mes_trobar}.html"
            if fitxer_trobar.exists():
                nom_mes = nom_mes_trobar
                mes_actual = mes
                nom_fitxer = f"{any_actual}-{mes:02d}-{nom_mes}.html"
                url_pla = f"plans-mensuals/{nom_fitxer}"
                print(f"  [OK] Usant: {nom_fitxer}")
                break
        else:
            print(f"[ERR] No sha trobat cap pla disponible. Crea primer un pla.")
            sys.exit(1)

    # Llegir el contingut
    content = p.read_text(encoding='utf-8')

    # IMPORTANT: nomes la URL (sense "plans-mensuals/" al davant)
    # El patro original te: data-path="plans-mensuals/AAAA-MM-mes.html"
    # Volem substituir nomes "AAAA-MM-mes.html" dins del data-path

    # El patro: data-path="plans-mensuals/AAAA-MM-mes.html" onclick="...">📅 Pla <mes> <any>
    patro = re.compile(
        r'(<a\s+href="#"\s+data-path="plans-mensuals/)\d{4}-\d{2}-[a-zà-ú]+\.html("\s+onclick="return openDoc\(this\.dataset\.path\)">📅 Pla )[a-zà-ú]+( \d{4})',
        re.MULTILINE
    )

    # Generar el text: mantenim el "plans-mensuals/" del grup 1, afegim la URL completa
    text_nou = rf'\g<1>{nom_fitxer}\g<2>{nom_mes}\g<3>'

    # Substituir
    matches = patro.findall(content)
    n_substitucions = len(matches)
    if n_substitucions > 0:
        content_nou = patro.sub(text_nou, content)
        p.write_text(content_nou, encoding='utf-8')
        print(f"[OK] {n_substitucions} substitucions fetes")
        print(f"  URL:   {url_pla}")
        print(f"  Text:  Pla {nom_mes} {any_actual}")
    else:
        print("[WARN] No sha trobat el patro del pla a la portada")
        print("  Comprova manualment que el link esta ben format")


if __name__ == "__main__":
    main()
