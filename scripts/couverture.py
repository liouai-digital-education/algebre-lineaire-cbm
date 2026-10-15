"""Matrice de couverture : combien de fois chaque dimension du référentiel est évaluée, module par module.

Lit les métadonnées « cbm » de tous les notebooks de fr/.

Usage :
    python scripts/couverture.py              # tous les notebooks (rédigés et squelettes)
    python scripts/couverture.py --rediges    # seulement les notebooks rédigés
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict

from cbm_nb import DIMENSIONS_ORDRE, charger_codes, dimension_de, tous_les_notebooks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--rediges", action="store_true", help="ne compter que les notebooks rédigés")
    args = parser.parse_args()

    codes_ref = charger_codes()
    notebooks = tous_les_notebooks()
    if args.rediges:
        notebooks = [(c, m) for c, m in notebooks if m.get("statut") == "rédigé"]

    par_module: dict[str, Counter] = defaultdict(Counter)
    vus: Counter = Counter()
    inconnus = set()
    for _, meta in notebooks:
        for code in meta["codes"]:
            if code not in codes_ref:
                inconnus.add(code)
                continue
            par_module[meta["module"]][dimension_de(code)] += 1
            vus[code] += 1

    portee = "notebooks rédigés" if args.rediges else "tous les notebooks"
    print(f"Couverture des 11 dimensions ({portee}, {len(notebooks)} notebooks)\n")
    print("| Module | " + " | ".join(DIMENSIONS_ORDRE) + " |")
    print("|---|" + "---|" * len(DIMENSIONS_ORDRE))
    total = Counter()
    for module in sorted(par_module):
        c = par_module[module]
        total.update(c)
        print(f"| {module} | " + " | ".join(str(c[d]) if c[d] else "·" for d in DIMENSIONS_ORDRE) + " |")
    print("| **Total** | " + " | ".join(f"**{total[d]}**" for d in DIMENSIONS_ORDRE) + " |")

    jamais = [c for c in codes_ref if c not in vus]
    print(f"\nCodes évalués au moins une fois : {len(vus)} / {len(codes_ref)}")
    if jamais:
        print("Codes jamais évalués :", ", ".join(jamais))
    if inconnus:
        print("ATTENTION, codes absents du référentiel :", ", ".join(sorted(inconnus)))


if __name__ == "__main__":
    main()
