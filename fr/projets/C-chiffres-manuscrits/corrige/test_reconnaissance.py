"""Tests du module reconnaissance (corrigé). Lancer : python test_reconnaissance.py  (ou pytest)."""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from reconnaissance import Reconnaisseur, distances


def nuages(n=40, graine=0):
    """Trois classes bien séparées dans R^6, chacune étalée le long d'une droite."""
    rng = np.random.default_rng(graine)
    X, y = [], []
    for c in range(3):
        centre = np.zeros(6); centre[c] = 10
        direction = np.zeros(6); direction[c + 3] = 1
        X.append(centre + rng.normal(0, 3, (n, 1)) * direction + rng.normal(0, 0.1, (n, 6)))
        y += [c] * n
    return np.vstack(X), np.array(y)


def leve(erreur, fonction, *args):
    try:
        fonction(*args)
    except erreur:
        return True
    return False


def test_distances_matricielles_egales_aux_distances_directes():
    rng = np.random.default_rng(1)
    A, B = rng.normal(size=(5, 4)), rng.normal(size=(7, 4))
    directes = np.linalg.norm(A[:, None, :] - B[None, :, :], axis=2)
    assert np.allclose(distances(A, B), directes)


def test_trois_methodes_reconnaissent_des_classes_separees():
    X, y = nuages()
    for methode in ("moyenne", "voisins", "sous-espaces"):
        assert Reconnaisseur(methode, k=1).ajuster(X, y).reussite(X, y) == 1.0


def test_sous_espaces_avec_k_nul_equivaut_au_chiffre_moyen():
    X, y = nuages(graine=2)
    Xn = np.random.default_rng(3).normal(5, 5, (50, 6))
    a = Reconnaisseur("sous-espaces", k=0).ajuster(X, y).predire(Xn)
    b = Reconnaisseur("moyenne").ajuster(X, y).predire(Xn)
    assert np.array_equal(a, b)


def test_un_sous_espace_reconstitue_exactement_les_points_de_sa_droite():
    X, y = nuages()
    r = Reconnaisseur("sous-espaces", k=1).ajuster(X, y)
    m, V = r.modeles[0]
    point = m + 7 * V[:, 0]
    assert r.scores(point[None, :])[0, 0] < 1e-9


def test_un_voisin_retrouve_les_etiquettes_d_apprentissage():
    X, y = nuages()
    assert np.array_equal(Reconnaisseur("voisins", k=1).ajuster(X, y).predire(X), y)


def test_ordre_des_pixels_sans_effet():
    X, y = nuages()
    Xn = np.random.default_rng(4).normal(5, 5, (30, 6))
    perm = np.random.default_rng(5).permutation(6)
    for methode in ("moyenne", "voisins", "sous-espaces"):
        a = Reconnaisseur(methode, k=2).ajuster(X, y).predire(Xn)
        b = Reconnaisseur(methode, k=2).ajuster(X[:, perm], y).predire(Xn[:, perm])
        assert np.array_equal(a, b)


def test_rejet_d_un_point_a_egale_distance():
    X, y = nuages()
    r = Reconnaisseur("moyenne").ajuster(X, y)
    milieu = (r.modeles[0][0] + r.modeles[1][0]) / 2
    assert r.predire_avec_rejet(milieu[None, :], seuil=0.9)[0] == -1
    assert r.predire_avec_rejet(r.modeles[2][0][None, :], seuil=0.9)[0] == 2


def test_memoire():
    X, y = nuages()
    assert Reconnaisseur("moyenne").ajuster(X, y).taille_memoire() == 3 * 6
    assert Reconnaisseur("sous-espaces", k=2).ajuster(X, y).taille_memoire() == 3 * 6 * 3
    assert Reconnaisseur("voisins", k=3).ajuster(X, y).taille_memoire() == X.size


def test_entrees_invalides():
    X, y = nuages()
    assert leve(ValueError, Reconnaisseur, "reseau-de-neurones")
    assert leve(ValueError, Reconnaisseur, "voisins", 0)
    assert leve(ValueError, Reconnaisseur, "sous-espaces", 2.5)
    assert leve(RuntimeError, Reconnaisseur().predire, X)
    assert leve(ValueError, Reconnaisseur().ajuster, X, y[:-1])
    assert leve(ValueError, Reconnaisseur().ajuster, X[0], y)
    X_trou = X.copy(); X_trou[0, 0] = np.nan
    assert leve(ValueError, Reconnaisseur().ajuster, X_trou, y)
    r = Reconnaisseur("moyenne").ajuster(X, y)
    assert leve(ValueError, r.predire_avec_rejet, X, 0)


if __name__ == "__main__":
    for nom, f in list(globals().items()):
        if nom.startswith("test_"):
            f()
            print("ok", nom)
