"""Crée les pages et notebooks manquants à partir de referentiel/parcours.yaml.

- Page d'accueil de chaque module (fr/<dossier>/index.md) si absente.
- Notebook squelette de chaque activité si absent, avec ses métadonnées cbm.
- Page de chaque projet intégrateur si absente.
- Régénère : la page du référentiel (fr/guide/referentiel.md), la carte du parcours
  dans fr/index.md et la table des matières (project.toc de myst.yml).

Les fichiers rédigés à la main ne sont jamais écrasés.

Usage : python scripts/generer_squelettes.py
"""
from __future__ import annotations

import re

import yaml

from cbm_nb import (DIMENSIONS_ORDRE, RACINE, Notebook, charger_dimensions,
                    charger_parcours, meta_activite, retirer_codes)

FR = RACINE / "fr"


def statut_activite(module: dict, activite: dict) -> str:
    return activite.get("statut", module.get("statut", "à rédiger"))


# --- Squelettes ----------------------------------------------------------------

def page_module(mid: str, module: dict) -> str:
    lignes = [f"# {mid} — {module['titre']}", "",
              f"**Question directrice : {module['question']}**", "",
              f"Objectif : {module['objectif']}", "",
              f"Durée indicative : {module['duree_h']} h. "
              f"Prérequis : {', '.join(module['prerequis']) or 'aucun'}.", ""]
    if module.get("statut") != "rédigé":
        lignes += [":::{note} Module en préparation",
                   "Les notebooks marqués « à rédiger » sont des squelettes : leur structure et leurs objectifs sont fixés, le contenu reste à écrire.",
                   ":::", ""]
    lignes += ["## Activités", "", "| Activité | Contenu | État |", "|---|---|---|"]
    for act in module["activites"]:
        etat = "rédigé" if statut_activite(module, act) == "rédigé" else "à rédiger"
        lignes.append(f"| [{act['titre']}]({act['fichier']}.ipynb) | {act['resume']} | {etat} |")
    return "\n".join(lignes) + "\n"


def notebook_squelette(mid: str, module: dict, act: dict) -> Notebook:
    nb = Notebook(meta_activite(mid, module, act))
    nb.entete(act["titre"], module["titre"])
    nb.md(f"""
:::{{note}} Notebook en préparation
**Intention :** {act['resume']}
:::
""")
    nb.md("""
## ① Définir la question

*À rédiger : une situation réelle, volontairement floue, en quelques lignes.*

**À vous (DQf, DQm, DQq).** Quelles informations sont utiles ? Lesquelles manquent ? Quelle question précise le calcul doit-il trancher ?

**Hypothèses (DQa).** Listez-les, avec la raison de chacune.
""")
    nb.md("## ② Estimer avant de calculer (IFe)\n\n*À rédiger : le pari à enregistrer avant tout calcul.*")
    nb.code("# Vos paris\npari = None")
    nb.md("## ③ Abstraire\n\n*À rédiger : schéma, choix du concept et de l'outil parmi 2 ou 3 options, calcul à la main sur une version réduite.*")
    nb.md("## ④ Calculer\n\n*À rédiger.*")
    nb.code("import numpy as np\nimport matplotlib.pyplot as plt")
    nb.md("## ⑤ Interpréter\n\n*À rédiger : lecture du résultat dans le contexte, traits remarquables, hypothèse nouvelle.*")
    nb.md("""
## ⑥ Critiquer et généraliser

- Quelle hypothèse est la plus fragile ? Que se passe-t-il si elle est fausse ? (CVa)
- Comment vérifier le résultat autrement ? (CVt)
- Quelle constante pourrait devenir un paramètre ? (GMv)
""")
    nb.bilan()
    return nb


def page_projet(cle: str, projet: dict) -> str:
    return f"""# Projet {cle} — {projet['titre']}

**Question ouverte : {projet['question']}**

| Données | Modules réinvestis |
|---|---|
| {projet['donnees']} | {', '.join(projet['modules'])} |

:::{{note}} Projet en préparation
Le cahier des charges détaillé reste à rédiger. Les étapes ci-dessous sont communes aux trois projets.
:::

## Étapes

1. **Cadrage** (DQ) : reformuler la question, lister les sous-problèmes, écrire les hypothèses. Faire valider avant de coder.
2. **Prototype** (AC, MC) : une version volontairement simple, puis une version améliorée.
3. **Vérification** (CV) : au moins deux méthodes de corroboration, dont un test sur des données non utilisées pour construire le modèle.
4. **Généralisation** (GM) : transformer le code en module Python documenté, avec tests des cas limites.
5. **Communication** (CC) : un rapport de 4 à 6 pages généré depuis le notebook, et une présentation de 10 minutes.

## Livrables

- [ ] Notebook propre et exécutable
- [ ] Module Python testé
- [ ] Rapport
- [ ] Support de présentation
- [ ] Auto-évaluation sur les 11 dimensions
"""


def page_projets(projets: dict) -> str:
    lignes = ["# Projets intégrateurs", "",
              "Choisissez **un** projet parmi trois. Chacun part d'une question ouverte, sans méthode imposée, "
              "et mobilise les 11 dimensions du référentiel — en particulier la gestion d'un problème plus gros "
              "que ceux déjà résolus (CPm).", "",
              "| Projet | Question ouverte | Modules réinvestis |", "|---|---|---|"]
    for cle, p in projets.items():
        lignes.append(f"| [{cle} — {p['titre']}]({p['fichier']}.md) | {p['question']} | "
                      f"{', '.join(p['modules'])} |")
    lignes += ["", "Pour connaître les modules à suivre avant un projet : `python scripts/parcours.py --projet B`."]
    return "\n".join(lignes) + "\n"


# --- Pages régénérées ----------------------------------------------------------

def page_referentiel() -> str:
    dims = charger_dimensions()
    total = sum(len(d["codes"]) for d in dims.values())
    lignes = ["# Le référentiel de compétences", "",
              "<!-- Page générée par scripts/generer_squelettes.py à partir de referentiel/cbm_codes.yaml. -->", "",
              f"Le référentiel compte **{len(dims)} dimensions et {total} codes**. "
              "Cinq dimensions sont transversales ; six correspondent aux étapes du processus.", "",
              "Source : *Required Outcomes from Core Computational Thinking*, Computer-Based Maths, "
              "licence CC BY-NC 4.0. Traduction adaptée.", ""]
    for dim in DIMENSIONS_ORDRE:
        d = dims[dim]
        lignes += [f"## {dim} — {d['fr']}", "", f"*{d['en']}* · dimension {d['famille']}", "",
                   "| Code | Intitulé |", "|---|---|"]
        lignes += [f"| {code} | {lib['fr']} |" for code, lib in d["codes"].items()]
        lignes.append("")
    return "\n".join(lignes)


def etat_module(module: dict) -> str:
    acts = module["activites"]
    rediges = sum(statut_activite(module, a) == "rédigé" for a in acts)
    if rediges == len(acts):
        return "✓ Disponible"
    if rediges:
        return f"En préparation · {rediges}/{len(acts)} disponible"
    return "En préparation"


def carte_parcours(parcours: dict) -> str:
    """Pile verticale des étapes du parcours, une par module, puis les projets (classes CSS liouai-parcours)."""
    lignes = [":::::{div}", ":class: liouai-parcours", ""]

    def etape(titre, lien, question, meta, classe="liouai-etape"):
        return ["::::{div}", f":class: {classe}", "", f"**[{titre}]({lien})**", "", question, "",
                ":::{div}", ":class: liouai-etape-meta", "", meta, ":::", "::::", ""]

    for mid, m in parcours["modules"].items():
        prerequis = ", ".join(m["prerequis"]) or "aucun"
        lignes += etape(f"{mid} — {m['titre']}", f"{m['dossier']}/index.md", m["question"],
                        f"{etat_module(m)} · {m['duree_h']} h · prérequis : {prerequis}")
    projets = parcours["projets_integrateurs"]
    prets = sum(1 for p in projets.values() if p.get("statut") == "rédigé")
    etat = "✓ Disponible" if prets == len(projets) else (f"{prets}/{len(projets)} disponible" if prets else "En préparation")
    lignes += etape("Projets intégrateurs", "projets/index.md",
                    "Un problème ouvert, de la question au rapport : " + " ; ".join(p["titre"] for p in projets.values()) + ".",
                    f"{etat} · 10 à 15 h · un projet au choix", classe="liouai-etape liouai-etape-projets")
    lignes.append(":::::")
    return "\n".join(lignes)


def table_des_matieres(parcours: dict) -> list:
    toc = [{"file": "fr/index.md"},
           {"title": "Guide", "children": [{"file": "fr/guide/processus.md"},
                                           {"file": "fr/guide/referentiel.md"},
                                           {"file": "fr/guide/evaluation.md"},
                                           {"file": "fr/guide/installation.md"}]}]
    for mid, m in parcours["modules"].items():
        enfants = [{"file": f"fr/{m['dossier']}/{a['fichier']}.ipynb"} for a in m["activites"]]
        toc.append({"file": f"fr/{m['dossier']}/index.md", "children": enfants})
    projets = []
    for p in parcours["projets_integrateurs"].values():
        entree = {"file": f"fr/projets/{p['fichier']}.md"}
        if p.get("etapes"):
            entree["children"] = [{"file": f"fr/{p['dossier']}/{e['fichier']}.ipynb"} for e in p["etapes"]]
        projets.append(entree)
    toc.append({"file": "fr/projets/index.md", "children": projets})
    toc.append({"file": "en/index.md"})
    return toc


def ecrire_si_absent(chemin, contenu, crees):
    if not chemin.exists():
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(retirer_codes(contenu), encoding="utf-8")
        crees.append(chemin)


def main() -> None:
    parcours = charger_parcours()
    crees = []

    for mid, module in parcours["modules"].items():
        dossier = FR / module["dossier"]
        ecrire_si_absent(dossier / "index.md", page_module(mid, module), crees)
        for act in module["activites"]:
            chemin = dossier / f"{act['fichier']}.ipynb"
            if not chemin.exists():
                notebook_squelette(mid, module, act).ecrire(chemin)
                crees.append(chemin)

    projets = parcours["projets_integrateurs"]
    ecrire_si_absent(FR / "projets" / "index.md", page_projets(projets), crees)
    for cle, p in projets.items():
        ecrire_si_absent(FR / "projets" / f"{p['fichier']}.md", page_projet(cle, p), crees)

    # Pages régénérées à chaque lancement
    (FR / "guide" / "referentiel.md").write_text(page_referentiel(), encoding="utf-8")

    accueil = FR / "index.md"
    texte = accueil.read_text(encoding="utf-8")
    texte = re.sub(r"<!-- carte:debut -->.*?<!-- carte:fin -->",
                   lambda _: f"<!-- carte:debut -->\n{carte_parcours(parcours)}\n<!-- carte:fin -->",
                   texte, flags=re.S)
    accueil.write_text(texte, encoding="utf-8")

    config_chemin = RACINE / "myst.yml"
    config = yaml.safe_load(config_chemin.read_text(encoding="utf-8"))
    config["project"]["toc"] = table_des_matieres(parcours)
    entete = ("# Configuration Jupyter Book 2 / MyST.\n"
              "# La clé project.toc est régénérée par scripts/generer_squelettes.py "
              "à partir de referentiel/parcours.yaml.\n")
    config_chemin.write_text(entete + yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
                             encoding="utf-8")

    print(f"{len(crees)} fichier(s) créé(s).")
    for c in crees:
        print("  +", c.relative_to(RACINE))
    print("Régénérés : fr/guide/referentiel.md, carte du parcours dans fr/index.md, table des matières de myst.yml.")


if __name__ == "__main__":
    main()
