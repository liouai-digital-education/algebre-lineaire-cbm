"""Outils communs du projet C : chargement des chiffres manuscrits, découpage, affichage.

Les données sont le jeu « Optical Recognition of Handwritten Digits » (E. Alpaydin et C. Kaynak,
UCI Machine Learning Repository, 1998, licence CC BY 4.0), dans la version distribuée avec
scikit-learn : 1 797 images de 8 × 8 pixels, chaque pixel valant de 0 (blanc) à 16 (noir).
"""
from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FICHIER = pathlib.Path(__file__).resolve().parent / "donnees" / "chiffres.csv"


def charger():
    """Renvoie (X, y) : une ligne de 64 pixels par image, et le chiffre écrit (0 à 9)."""
    tableau = pd.read_csv(FICHIER)
    return tableau.drop(columns="chiffre").to_numpy(dtype=float), tableau["chiffre"].to_numpy()


def decouper(X, y, part_test=0.25, graine=0):
    """Découpage au hasard, en gardant la même proportion de chaque chiffre dans les deux paquets."""
    rng = np.random.default_rng(graine)
    test = np.zeros(len(y), dtype=bool)
    for c in np.unique(y):
        indices = np.flatnonzero(y == c)
        rng.shuffle(indices)
        test[indices[:round(part_test * len(indices))]] = True
    return X[~test], y[~test], X[test], y[test]


def afficher(images, titres=None, colonnes=10, taille=1.1, cmap="gray_r", symetrique=False):
    """Affiche des images 8 × 8 (une par ligne de `images`) dans une grille.

    L'échelle va de 0 (blanc) à 16 (noir) ; avec `symetrique=True`, elle est centrée sur 0 (pour des directions signées).
    """
    images = np.atleast_2d(images)
    vmin, vmax = (-np.abs(images).max(), np.abs(images).max()) if symetrique else (0, 16)
    lignes = int(np.ceil(len(images) / colonnes))
    fig, axes = plt.subplots(lignes, colonnes, figsize=(taille * colonnes, taille * 1.15 * lignes), squeeze=False)
    for k, ax in enumerate(axes.ravel()):
        ax.axis("off")
        if k < len(images):
            ax.imshow(images[k].reshape(8, 8), cmap=cmap, vmin=vmin, vmax=vmax)
            if titres is not None:
                ax.set_title(str(titres[k]), fontsize=8)
    plt.tight_layout()
    return fig


def matrice_confusion(vrais, predits, n=10):
    """M[i, j] = nombre d'images du chiffre i reconnues comme j."""
    M = np.zeros((n, n), dtype=int)
    np.add.at(M, (vrais, predits), 1)
    return M
