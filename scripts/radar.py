"""Trace le profil de compétences sur les 11 dimensions du référentiel (profil.png).

Pour chaque code : meilleur niveau atteint sur ses 3 dernières occurrences.
Pour chaque dimension : moyenne des codes déjà évalués.

Usage : python scripts/radar.py [--sortie profil.png]
"""
from __future__ import annotations

import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from cbm_nb import DIMENSIONS_ORDRE, RACINE, charger_dimensions
from profil import charger_progression, niveaux_par_code, niveaux_par_dimension


def main() -> None:
    parser = argparse.ArgumentParser(description="Trace le profil radar des 11 dimensions.")
    parser.add_argument("--sortie", default=str(RACINE / "profil.png"))
    args = parser.parse_args()

    historique = charger_progression()
    if not historique:
        print("Aucun bilan dans progression.json : remplissez la cellule Bilan à la fin des notebooks.")
        return

    dims = charger_dimensions()
    par_code = niveaux_par_code(historique)
    par_dim = niveaux_par_dimension(par_code)

    print(f"{len(historique)} bilan(s), {len(par_code)} code(s) évalué(s)\n")
    for d in DIMENSIONS_ORDRE:
        v = par_dim[d]
        barre = "█" * round(2 * v) if v is not None else ""
        print(f"  {d:3s} {dims[d]['fr']:<50s} {('%.1f' % v) if v is not None else 'non évalué':>10s}  {barre}")

    valeurs = [par_dim[d] if par_dim[d] is not None else 0 for d in DIMENSIONS_ORDRE]
    angles = np.linspace(0, 2 * np.pi, len(DIMENSIONS_ORDRE), endpoint=False)
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"projection": "polar"})
    ax.plot(np.append(angles, angles[0]), valeurs + valeurs[:1], color="#167A5C", lw=2)
    ax.fill(np.append(angles, angles[0]), valeurs + valeurs[:1], color="#28B78D", alpha=0.25)
    etiquettes = [d if par_dim[d] is not None else f"{d}\n(non évaluée)" for d in DIMENSIONS_ORDRE]
    ax.set_xticks(angles, etiquettes)
    for etiquette, d in zip(ax.get_xticklabels(), DIMENSIONS_ORDRE):
        if par_dim[d] is None:
            etiquette.set_color("#A1A9AE")
    ax.set_ylim(0, 3)
    ax.set_yticks([1, 2, 3], ["guidé", "autonome", "transfert"], fontsize=8, color="#5C6870")
    ax.set_title("Profil de compétences — référentiel Computer-Based Maths", pad=20)
    fig.savefig(args.sortie, dpi=120, bbox_inches="tight")
    print(f"\nProfil enregistré dans {args.sortie}")


if __name__ == "__main__":
    main()
