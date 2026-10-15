"""Lecture de progression.json et calcul du niveau atteint par code et par dimension."""
from __future__ import annotations

import json
from collections import defaultdict

from cbm_nb import DIMENSIONS_ORDRE, RACINE, charger_codes, dimension_de

FICHIER = RACINE / "progression.json"


def charger_progression(chemin=FICHIER) -> list[dict]:
    if not chemin.exists():
        return []
    return json.loads(chemin.read_text(encoding="utf-8"))


def _vers_code() -> dict[str, str]:
    """Les bilans sont enregistrés avec l'intitulé de la compétence (ou, anciennement, son code)."""
    correspondance = {}
    for code, libelles in charger_codes().items():
        correspondance[code] = code
        correspondance[libelles["fr"]] = code
    return correspondance


def niveaux_par_code(historique: list[dict], fenetre: int = 3) -> dict[str, int]:
    """Meilleur niveau atteint sur les `fenetre` dernières occurrences de chaque code."""
    vers_code = _vers_code()
    occurrences = defaultdict(list)
    for entree in sorted(historique, key=lambda e: e.get("date", "")):
        for cle, niveau in entree["niveaux"].items():
            code = vers_code.get(cle)
            if code is None:
                continue                     # intitulé modifié ou inconnu : ignoré
            occurrences[code].append(int(niveau))
    return {code: max(valeurs[-fenetre:]) for code, valeurs in occurrences.items()}


def niveaux_par_dimension(par_code: dict[str, int]) -> dict[str, float | None]:
    """Moyenne des niveaux des codes déjà évalués de chaque dimension (None si aucun)."""
    groupes = defaultdict(list)
    for code, niveau in par_code.items():
        groupes[dimension_de(code)].append(niveau)
    return {d: (sum(groupes[d]) / len(groupes[d]) if groupes[d] else None) for d in DIMENSIONS_ORDRE}


def notebooks_faits(historique: list[dict]) -> set[str]:
    return {e["notebook"] for e in historique}
