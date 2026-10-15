"""Cohérence entre parcours.yaml, le référentiel, les notebooks et la table des matières."""
import json
import pathlib
import sys

import yaml

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "scripts"))
from cbm_nb import charger_codes, charger_parcours, dimension_de  # noqa: E402

CODES = charger_codes()
PARCOURS = charger_parcours()


def activites():
    for mid, m in PARCOURS["modules"].items():
        for a in m["activites"]:
            yield mid, m, a


def test_codes_du_parcours_existent():
    for mid, _, a in activites():
        for c in a["codes"]:
            assert c in CODES, f"{a['fichier']} : code inconnu {c}"


def test_chaque_code_a_une_dimension():
    for code in CODES:
        assert dimension_de(code) == CODES[code]["dimension"]


def test_chaque_activite_a_son_notebook_et_ses_metadonnees():
    for mid, m, a in activites():
        chemin = RACINE / "fr" / m["dossier"] / f"{a['fichier']}.ipynb"
        assert chemin.exists(), f"notebook manquant : {chemin}"
        meta = json.loads(chemin.read_text(encoding="utf-8"))["metadata"]["cbm"]
        assert meta["module"] == mid
        assert meta["codes"] == a["codes"], f"{chemin.name} : codes différents de parcours.yaml"


def test_prerequis_valides_et_sans_cycle():
    modules = PARCOURS["modules"]
    ordre = list(modules)
    for mid, m in modules.items():
        for p in m["prerequis"]:
            assert p in modules
            assert ordre.index(p) < ordre.index(mid), f"{mid} dépend de {p}, déclaré après lui"


def test_table_des_matieres_pointe_vers_des_fichiers_existants():
    config = yaml.safe_load((RACINE / "myst.yml").read_text(encoding="utf-8"))

    def fichiers(toc):
        for entree in toc:
            if "file" in entree:
                yield entree["file"]
            yield from fichiers(entree.get("children", []))

    for f in fichiers(config["project"]["toc"]):
        assert (RACINE / f).exists(), f"table des matières : fichier absent {f}"


def test_etapes_des_projets_ont_leur_notebook():
    for cle, projet in PARCOURS["projets_integrateurs"].items():
        for etape in projet.get("etapes", []):
            chemin = RACINE / "fr" / projet["dossier"] / f"{etape['fichier']}.ipynb"
            assert chemin.exists(), f"notebook manquant : {chemin}"
            meta = json.loads(chemin.read_text(encoding="utf-8"))["metadata"]["cbm"]
            assert meta["module"] == f"projet-{cle}"
            assert meta["codes"] == etape["codes"], f"{chemin.name} : codes différents de parcours.yaml"
            for code in etape["codes"]:
                assert code in CODES, f"{chemin.name} : code inconnu {code}"
