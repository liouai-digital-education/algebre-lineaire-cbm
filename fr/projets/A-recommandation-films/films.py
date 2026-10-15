"""Outils communs du projet A : chargement des données, découpage, mesure d'erreur.

Les données MovieLens appartiennent au GroupLens Research Project (université du Minnesota).
Leur licence autorise un usage pédagogique, mais pas leur redistribution : ce module les
télécharge donc sur votre ordinateur, depuis le site de GroupLens, la première fois.
Sans connexion, il utilise un jeu de données simulé au même format (dossier donnees/simule).
"""
from __future__ import annotations

import io
import pathlib
import urllib.request
import zipfile

import numpy as np
import pandas as pd

ICI = pathlib.Path(__file__).resolve().parent
DONNEES = ICI / "donnees"
URL_MOVIELENS = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"


def _lire(dossier: pathlib.Path):
    notes = pd.read_csv(dossier / "ratings.csv")
    films = pd.read_csv(dossier / "movies.csv")
    return notes, films


def telecharger_movielens(delai: float = 30.0) -> pathlib.Path:
    """Télécharge et décompresse ml-latest-small dans donnees/ (environ 1 Mo)."""
    cible = DONNEES / "ml-latest-small"
    if (cible / "ratings.csv").exists():
        return cible
    with urllib.request.urlopen(URL_MOVIELENS, timeout=delai) as reponse:
        contenu = reponse.read()
    with zipfile.ZipFile(io.BytesIO(contenu)) as archive:
        archive.extractall(DONNEES)
    return cible


def charger_films(source: str = "auto"):
    """Renvoie (notes, films, nom_de_la_source).

    source = "movielens" : données réelles (téléchargées si besoin) ;
    source = "simule"    : jeu simulé fourni avec le projet ;
    source = "auto"      : MovieLens si possible, sinon le jeu simulé.
    """
    if source in ("auto", "movielens"):
        try:
            return (*_lire(telecharger_movielens()), "MovieLens (ml-latest-small, GroupLens)")
        except Exception as erreur:
            if source == "movielens":
                raise
            print(f"MovieLens indisponible ({type(erreur).__name__}) : utilisation du jeu simulé.")
    return (*_lire(DONNEES / "simule"), "jeu simulé au format MovieLens")


def decouper(notes: pd.DataFrame, part_test: float = 0.2, graine: int = 0):
    """Met de côté, pour chaque spectateur, une part de ses notes (au moins une)."""
    rng = np.random.default_rng(graine)
    aleatoire = pd.Series(rng.random(len(notes)), index=notes.index)
    rang = aleatoire.groupby(notes["userId"]).rank(pct=True)
    test = rang <= part_test
    return notes[~test].copy(), notes[test].copy()


def reqm(vraies, predites) -> float:
    """Racine de l'erreur quadratique moyenne."""
    vraies, predites = np.asarray(vraies, float), np.asarray(predites, float)
    return float(np.sqrt(np.mean((vraies - predites) ** 2)))


class Index:
    """Correspondance entre identifiants (userId, movieId) et numéros de ligne et de colonne."""

    def __init__(self, notes: pd.DataFrame):
        self.spectateurs = np.sort(notes["userId"].unique())
        self.films = np.sort(notes["movieId"].unique())
        self.ligne = {u: i for i, u in enumerate(self.spectateurs)}
        self.colonne = {f: j for j, f in enumerate(self.films)}

    def lignes(self, ids):
        return np.array([self.ligne[u] for u in ids])

    def colonnes(self, ids):
        return np.array([self.colonne.get(f, -1) for f in ids])

    def matrice(self, notes: pd.DataFrame, valeur: str = "rating"):
        """Matrice dense spectateurs × films (NaN là où il n'y a pas de note)."""
        R = np.full((len(self.spectateurs), len(self.films)), np.nan)
        j = self.colonnes(notes["movieId"])
        garde = j >= 0
        R[self.lignes(notes["userId"])[garde], j[garde]] = notes[valeur].to_numpy()[garde]
        return R


def ajuster_biais(notes: pd.DataFrame, lam: float = 10.0, iterations: int = 15):
    """Modèle note ≈ mu + b_spectateur + b_film, ajusté par moindres carrés régularisés.

    Renvoie (mu, biais_spectateurs, biais_films) sous forme de dictionnaires {identifiant: biais}.
    """
    mu = notes["rating"].mean()
    u, f, r = notes["userId"].to_numpy(), notes["movieId"].to_numpy(), notes["rating"].to_numpy()
    bu = pd.Series(0.0, index=np.unique(u))
    bf = pd.Series(0.0, index=np.unique(f))
    for _ in range(iterations):
        reste = r - mu - bf.loc[f].to_numpy()
        g = pd.Series(reste).groupby(u)
        bu = g.sum() / (g.count() + lam)
        reste = r - mu - bu.loc[u].to_numpy()
        g = pd.Series(reste).groupby(f)
        bf = g.sum() / (g.count() + lam)
    return mu, bu.to_dict(), bf.to_dict()


def predire_biais(modele, notes: pd.DataFrame) -> np.ndarray:
    mu, bu, bf = modele
    return np.array([mu + bu.get(u, 0.0) + bf.get(f, 0.0) for u, f in zip(notes["userId"], notes["movieId"])])
