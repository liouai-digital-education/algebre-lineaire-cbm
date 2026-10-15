"""Propose un parcours personnalisé, à deux échelles.

- Macro : l'ordre des modules à suivre, en respectant les prérequis. Avec --projet,
  seulement les modules nécessaires au projet intégrateur choisi.
- Micro : dans le module en cours, les activités à faire en priorité, celles qui
  travaillent les codes où votre niveau est le plus bas (d'après progression.json).

Usage :
    python scripts/parcours.py
    python scripts/parcours.py --projet B
    python scripts/parcours.py --module M1
"""
from __future__ import annotations

import argparse

from cbm_nb import charger_codes, charger_parcours
from profil import charger_progression, niveaux_par_code, notebooks_faits

SEUIL_ACQUIS = 2   # niveau « autonome »


def fermeture_prerequis(modules: dict, cibles: list[str]) -> list[str]:
    """Modules nécessaires pour atteindre les cibles, dans un ordre compatible avec les prérequis."""
    ordre, vus = [], set()

    def visiter(m):
        if m in vus:
            return
        vus.add(m)
        for p in modules[m]["prerequis"]:
            visiter(p)
        ordre.append(m)

    for c in cibles:
        visiter(c)
    rang = {m: i for i, m in enumerate(modules)}        # ordre du fichier pour départager
    return sorted(ordre, key=lambda m: (profondeur(modules, m), rang[m]))


def profondeur(modules: dict, m: str) -> int:
    return 0 if not modules[m]["prerequis"] else 1 + max(profondeur(modules, p) for p in modules[m]["prerequis"])


def statut(module: dict, act: dict) -> str:
    return act.get("statut", module.get("statut", "à rédiger"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Propose un parcours personnalisé.")
    parser.add_argument("--projet", choices=["A", "B", "C"], help="projet intégrateur visé")
    parser.add_argument("--module", help="module en cours (sinon : le premier module non terminé)")
    args = parser.parse_args()

    parcours = charger_parcours()
    modules = parcours["modules"]
    libelles = charger_codes()
    historique = charger_progression()
    niveaux = niveaux_par_code(historique)
    faits = notebooks_faits(historique)

    # --- Macro ---------------------------------------------------------------
    if args.projet:
        projet = parcours["projets_integrateurs"][args.projet]
        ordre = fermeture_prerequis(modules, projet["modules"])
        print(f"Projet {args.projet} — {projet['titre']}")
        evites = [m for m in modules if m not in ordre]
        if evites:
            print("Modules non nécessaires :", ", ".join(evites))
    else:
        ordre = list(modules)
    duree = sum(modules[m]["duree_h"] for m in ordre)
    print(f"\nParcours macro ({duree} h environ) :")
    for m in ordre:
        acts = modules[m]["activites"]
        n_faits = sum(a["fichier"] in faits for a in acts)
        print(f"  {m} — {modules[m]['titre']:<48s} {n_faits}/{len(acts)} activité(s) faite(s)")

    # --- Micro ---------------------------------------------------------------
    en_cours = args.module or next(
        (m for m in ordre if any(a["fichier"] not in faits for a in modules[m]["activites"])), None)
    if en_cours is None:
        print("\nToutes les activités du parcours sont faites. Place au projet intégrateur !")
        return
    module = modules[en_cours]
    print(f"\nParcours micro — module {en_cours} ({module['titre']}) :")

    def deficit(act):
        # Somme des écarts au niveau « autonome » sur les codes de l'activité
        return sum(max(0, SEUIL_ACQUIS - niveaux.get(c, 0)) for c in act["codes"])

    a_faire = [a for a in module["activites"] if a["fichier"] not in faits]
    a_faire.sort(key=lambda a: (a.get("projet", False), -deficit(a)))   # mini-projet en dernier
    for a in a_faire:
        faibles = [c for c in a["codes"] if niveaux.get(c, 0) < SEUIL_ACQUIS]
        etat = "" if statut(module, a) == "rédigé" else "  [à rédiger]"
        if faibles:
            detail = ", ".join(f"{c} ({libelles[c]['fr']}, niveau {niveaux.get(c, 0)})" for c in faibles)
            print(f"  • {a['id']:10s} {a['titre']}{etat}\n      travaille : {detail}")
        else:
            print(f"  • {a['id']:10s} {a['titre']}{etat}\n      facultatif : tous ses codes sont déjà au niveau {SEUIL_ACQUIS} ou plus")

    if niveaux:
        faibles = sorted((n, c) for c, n in niveaux.items() if n < SEUIL_ACQUIS)
        if faibles:
            print("\nVos codes les plus faibles :", ", ".join(f"{c} ({n})" for n, c in faibles[:6]))
    else:
        print("\nAucun bilan enregistré pour l'instant : remplissez la cellule Bilan à la fin de chaque notebook.")


if __name__ == "__main__":
    main()
