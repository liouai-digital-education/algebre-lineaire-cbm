"""Outils communs du projet B : chargement des réseaux et dessin.

Trois réseaux publics, classiques en analyse des réseaux sociaux :

- karate : le club de karaté étudié par W. Zachary (1977), 34 membres, liens d'amitié
  observés hors du club ; le poids compte les contextes où deux membres se rencontraient ;
- florence : les mariages entre grandes familles florentines vers 1430 (J. Padgett) ;
- miserables : les personnages du roman de Victor Hugo, liés quand ils apparaissent
  dans un même chapitre (D. Knuth, Stanford GraphBase) ; le poids compte ces chapitres.

Les fichiers ont été exportés depuis la bibliothèque networkx. Les positions (x, y) ne servent
qu'au dessin.
"""
from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DONNEES = pathlib.Path(__file__).resolve().parent / "donnees"
RESEAUX = ("karate", "florence", "miserables")


def charger(nom: str, pondere: bool = False):
    """Renvoie (membres, liens, A) : deux tableaux et la matrice d'adjacence symétrique.

    La ligne et la colonne k de A correspondent à la ligne k du tableau des membres.
    Avec pondere=True, A contient les poids des liens au lieu de 1.
    """
    if nom not in RESEAUX:
        raise ValueError(f"Réseau inconnu : {nom}. Choix possibles : {', '.join(RESEAUX)}")
    membres = pd.read_csv(DONNEES / f"{nom}_membres.csv")
    liens = pd.read_csv(DONNEES / f"{nom}_liens.csv")
    position = {m: k for k, m in enumerate(membres["id"])}
    A = np.zeros((len(membres), len(membres)))
    for _, l in liens.iterrows():
        i, j = position[l["source"]], position[l["cible"]]
        A[i, j] = A[j, i] = l["poids"] if (pondere and "poids" in liens) else 1.0
    return membres, liens, A


def dessiner(A, membres, valeurs=None, ax=None, titre="", etiquettes=True, couleurs=None, taille_max=600):
    """Dessine le réseau ; la taille et la couleur des disques suivent `valeurs` (une par membre)."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 6))
    x, y = membres["x"].to_numpy(), membres["y"].to_numpy()
    i, j = np.nonzero(np.triu(A))
    for a, b in zip(i, j):
        ax.plot([x[a], x[b]], [y[a], y[b]], color="#A1A9AE", lw=0.6, zorder=1)
    if valeurs is None:
        valeurs = np.ones(len(membres))
    v = np.asarray(valeurs, dtype=float)
    echelle = (v - v.min()) / (v.max() - v.min()) if v.max() > v.min() else np.full(len(v), 0.5)
    ax.scatter(x, y, s=60 + taille_max * echelle, c=couleurs if couleurs is not None else echelle,
               cmap=None if couleurs is not None else "liouai", edgecolors="#243743", linewidths=0.8, zorder=2)
    if etiquettes:
        for k, nom in enumerate(membres["id"]):
            fonce = couleurs is None and echelle[k] > 0.55
            ax.text(x[k], y[k], str(nom), fontsize=7, ha="center", va="center", zorder=3,
                    color="white" if fonce else "#243743")
    ax.set_title(titre)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
    for cote in ax.spines.values():
        cote.set_visible(False)
    return ax
