"""Outils communs : lecture du référentiel, création de notebooks au format .ipynb v4.

Utilisé par generer_squelettes.py, couverture.py, parcours.py et radar.py.
Ne dépend que de PyYAML et de la bibliothèque standard.
"""
from __future__ import annotations

import json
import pathlib
import re

import yaml

RACINE = pathlib.Path(__file__).resolve().parent.parent
REFERENTIEL = RACINE / "referentiel"
DIMENSIONS_ORDRE = ["CP", "IF", "CV", "GM", "CC", "DQ", "AC", "C", "T", "MC", "IN"]


# --- Référentiel -----------------------------------------------------------

def charger_codes() -> dict:
    """Renvoie {code: {"dimension": "CV", "fr": ..., "en": ...}}."""
    data = yaml.safe_load((REFERENTIEL / "cbm_codes.yaml").read_text(encoding="utf-8"))
    codes = {}
    for dim, contenu in data["dimensions"].items():
        for code, libelles in contenu["codes"].items():
            codes[code] = {"dimension": dim, **libelles}
    return codes


def charger_dimensions() -> dict:
    data = yaml.safe_load((REFERENTIEL / "cbm_codes.yaml").read_text(encoding="utf-8"))
    return data["dimensions"]


def charger_parcours() -> dict:
    return yaml.safe_load((REFERENTIEL / "parcours.yaml").read_text(encoding="utf-8"))


def dimension_de(code: str) -> str:
    """CVt -> CV, MC6 -> MC, C1 -> C, Tb -> T."""
    for dim in sorted(DIMENSIONS_ORDRE, key=len, reverse=True):
        if code.startswith(dim) and (len(code) == len(dim) or not code[len(dim)].isupper()):
            return dim
    raise ValueError(f"Code inconnu : {code}")


def lire_metadonnees(chemin: pathlib.Path) -> dict | None:
    nb = json.loads(chemin.read_text(encoding="utf-8"))
    return nb.get("metadata", {}).get("cbm")


def tous_les_notebooks(langue: str = "fr") -> list[tuple[pathlib.Path, dict]]:
    resultats = []
    for chemin in sorted((RACINE / langue).rglob("*.ipynb")):
        if ".ipynb_checkpoints" in chemin.parts:
            continue
        meta = lire_metadonnees(chemin)
        if meta:
            resultats.append((chemin, meta))
    return resultats


# --- Charte graphique Liouaï -------------------------------------------------

# Couleurs du logo Liouaï Digital Education (voir assets/liouai.css)
COULEURS = {
    "navy": "#243743",        # texte, titres, élément principal
    "vert": "#28B78D",        # couleur de marque (aplats, barres)
    "vert_texte": "#167A5C",  # vert lisible sur fond blanc (traits fins, texte)
    "gris": "#A1A9AE",        # éléments secondaires
    "gris_texte": "#5C6870",  # légendes, axes
    "jaune": "#E5C800",       # mise en avant (jaune de marque assombri pour rester visible)
    "fond": "#F3F5F6",
}

# Cellule placée en tête de chaque notebook : applique la charte à Matplotlib.
STYLE_LIOUAI = """
# Style graphique Liouaï : couleurs du logo, axes sobres
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

LIOUAI = {"navy": "#243743", "vert": "#28B78D", "vert_texte": "#167A5C", "gris": "#A1A9AE",
          "gris_texte": "#5C6870", "jaune": "#E5C800", "fond": "#F3F5F6"}
plt.rcParams.update({
    "axes.prop_cycle": plt.cycler(color=[LIOUAI["vert"], LIOUAI["navy"], LIOUAI["gris"],
                                         LIOUAI["jaune"], LIOUAI["vert_texte"], LIOUAI["gris_texte"]]),
    "axes.edgecolor": LIOUAI["gris"], "axes.labelcolor": LIOUAI["navy"],
    "axes.titlecolor": LIOUAI["navy"], "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.color": LIOUAI["gris_texte"], "ytick.color": LIOUAI["gris_texte"],
    "text.color": LIOUAI["navy"], "grid.color": "#E1E6E9", "legend.frameon": False,
    "font.family": "sans-serif", "font.sans-serif": ["Roboto", "Helvetica", "Arial", "DejaVu Sans"],
    "figure.dpi": 100,
})
# Dégradé de marque : gris clair -> vert -> navy (et sa version inversée)
if "liouai" not in mpl.colormaps:
    _cmap = LinearSegmentedColormap.from_list("liouai", [LIOUAI["fond"], LIOUAI["vert"], LIOUAI["navy"]])
    mpl.colormaps.register(_cmap)
    mpl.colormaps.register(_cmap.reversed())
""".strip()


# --- Retrait des codes de compétences du texte visible ------------------------

def _motif_codes() -> re.Pattern:
    codes = sorted([*charger_codes(), *DIMENSIONS_ORDRE], key=len, reverse=True)   # codes et dimensions
    un = "(?:" + "|".join(map(re.escape, codes)) + ")"
    # « (DQf, DQm et DQq) », « (codes CPk et MC2) », « (IFe) » : parenthèses ne contenant que des codes
    return re.compile(r"[ \u00a0]?\((?:codes?\s+)?" + un + r"(?:\s*(?:,|et)\s*" + un + r")*\)")


def retirer_codes(texte: str) -> str:
    """Supprime les mentions de codes du référentiel entre parenthèses."""
    return _motif_codes().sub("", texte)


def retirer_codes_commentaires(code: str) -> str:
    """Même chose, mais seulement dans les commentaires (après #) d'une cellule de code."""
    motif = _motif_codes()
    lignes = []
    for ligne in code.split("\n"):
        if "#" in ligne:
            avant, apres = ligne.split("#", 1)
            ligne = avant + "#" + motif.sub("", apres)
        lignes.append(ligne)
    return "\n".join(lignes)


# --- Construction de notebooks ----------------------------------------------

CONSIGNE_REPONSE = "Indiquez vos réponses et justifiez-les."
_ETIQUETTES = re.compile(r"^\*\*(?:À vous|Calcul à la main|À la main|À faire|Question)\.\*\*[ \t]*", re.M)
_ZONES = re.compile(r"^\*(?:Votre|Vos) [^*\n]*?(?::\*[ \t]*…|: …\*|ici\.\*)[ \t]*$(?:\n\n?\d+\. …[ \t]*$)*", re.M)
_GABARIT = re.compile(r"\n*^Ce notebook suit (?:le gabarit|les étapes) du parcours :.*$", re.M)


def harmoniser_consignes(texte: str) -> str:
    """Consignes uniformes : « **Activité** : » et une invitation à répondre en justifiant."""
    texte = _GABARIT.sub("", texte)
    texte = _ETIQUETTES.sub(lambda m: "**Activité** : ", texte)
    texte = re.sub(r"^\*\*Activité\*\* : $", "**Activité** :", texte, flags=re.M)
    return _ZONES.sub(CONSIGNE_REPONSE, texte)


class Notebook:
    """Construit un notebook cellule par cellule."""

    def __init__(self, meta: dict):
        self.meta = meta
        self.cells: list[dict] = []

    def md(self, texte: str) -> "Notebook":
        self.cells.append({"cell_type": "markdown", "metadata": {},
                           "source": harmoniser_consignes(retirer_codes(texte.strip("\n")))})
        return self

    def code(self, texte: str, tags: list[str] | None = None) -> "Notebook":
        self.cells.append({"cell_type": "code", "metadata": {"tags": tags} if tags else {},
                           "execution_count": None, "outputs": [],
                           "source": retirer_codes_commentaires(texte.strip("\n"))})
        return self

    def entete(self, titre: str, module_titre: str) -> "Notebook":
        m = self.meta
        prerequis = ", ".join(m.get("prerequis", [])) or "aucun"
        return self.md(f"""
# {titre}

| Module | Durée | Prérequis |
|---|---|---|
| {m['module']} – {module_titre} | {m['duree_min']} min | {prerequis} |
""").style_graphique()

    def style_graphique(self) -> "Notebook":
        return self.code(STYLE_LIOUAI, tags=["hide-input", "style-liouai"])

    def bilan(self) -> "Notebook":
        libelles = charger_codes()
        niveaux = "".join(f'\n    "{libelles[c]["fr"]}": 1,' for c in self.meta["codes"])
        self.md("""
## Bilan — auto-évaluation

Pour chaque compétence travaillée dans ce notebook, choisissez un niveau : **0** non observé · **1** guidé · **2** autonome · **3** transfert.
La cellule enregistre votre bilan dans `progression.json`, à la racine du site.
""")
        return self.code(f"""
import json, datetime, pathlib

bilan = {{{niveaux}
}}   # modifiez les niveaux

ici = pathlib.Path.cwd()
racine = next((p for p in [ici, *ici.parents] if (p / "myst.yml").exists()), ici)
fichier = racine / "progression.json"
historique = json.loads(fichier.read_text(encoding="utf-8")) if fichier.exists() else []
historique.append({{"notebook": "{self.meta['id']}", "date": datetime.date.today().isoformat(), "niveaux": bilan}})
fichier.write_text(json.dumps(historique, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Bilan enregistré ({{len(historique)}} entrée(s) dans {{fichier.name}}).")
""")

    def ecrire(self, chemin: pathlib.Path) -> None:
        attribuer_ids(self.cells, self.meta["id"])
        nb = {
            "cells": self.cells,
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python"},
                "cbm": self.meta,
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def attribuer_ids(cellules: list[dict], identifiant_notebook: str) -> None:
    """Donne à chaque cellule un identifiant unique dans tout le site.

    Jupyter Book traite les identifiants de cellules comme des étiquettes globales :
    ils doivent différer d'un notebook à l'autre. Format nbformat : [a-zA-Z0-9-_], 64 caractères au plus.
    """
    prefixe = re.sub(r"[^a-zA-Z0-9_-]", "-", identifiant_notebook)[:56]
    for i, cellule in enumerate(cellules):
        cellule["id"] = f"{prefixe}-c{i:02d}"


def meta_activite(module_id: str, module: dict, activite: dict, langue: str = "fr") -> dict:
    """Métadonnées cbm d'une activité, à partir de parcours.yaml."""
    projet = activite.get("projet", False)
    statut = activite.get("statut", module.get("statut", "à rédiger"))
    return {
        "id": activite["fichier"],
        "module": module_id,
        "activite": activite["id"],
        "type": "mini-projet" if projet else "notebook",
        "langue": langue,
        "duree_min": 150 if projet else 75,
        "prerequis": module.get("prerequis", []),
        "codes": activite["codes"],
        "statut": statut,
    }
