"""Rend uniques, dans tout le site, les identifiants de cellules des notebooks.

Jupyter Book signale « Duplicate identifier in project » quand deux notebooks
ont des cellules de même identifiant. Ce script renomme les identifiants
(préfixe = nom du notebook) sans toucher au contenu des cellules.

Usage : python scripts/corriger_ids.py
"""
from __future__ import annotations

import json

from cbm_nb import RACINE, attribuer_ids


def main() -> None:
    modifies = 0
    for chemin in sorted(RACINE.rglob("*.ipynb")):
        if any(p in chemin.parts for p in (".ipynb_checkpoints", "_build", ".venv")):
            continue
        nb = json.loads(chemin.read_text(encoding="utf-8"))
        avant = [c.get("id") for c in nb["cells"]]
        identifiant = nb.get("metadata", {}).get("cbm", {}).get("id", chemin.stem)
        attribuer_ids(nb["cells"], identifiant)
        if [c["id"] for c in nb["cells"]] != avant:
            nb["nbformat_minor"] = max(nb.get("nbformat_minor", 5), 5)
            chemin.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            modifies += 1
    print(f"{modifies} notebook(s) corrigé(s).")


if __name__ == "__main__":
    main()
