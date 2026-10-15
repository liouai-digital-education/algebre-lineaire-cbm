"""Tests du module de recommandation (corrigé). Lancer : python test_recommandation.py  (ou pytest)."""
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from recommandation import Recommandeur


def petites_notes():
    # 4 spectateurs, 4 films : deux « camps » de goûts opposés
    lignes = [(1, 10, 5), (1, 11, 4.5), (1, 12, 1), (2, 10, 4.5), (2, 11, 5), (2, 13, 1.5),
              (3, 12, 5), (3, 13, 4.5), (3, 10, 1), (4, 12, 4.5), (4, 13, 5), (4, 11, 1.5)]
    return pd.DataFrame(lignes, columns=["userId", "movieId", "rating"])


def test_predictions_dans_l_intervalle():
    m = Recommandeur(k=2, lam=0.1, iterations=30).ajuster(petites_notes())
    p = m.predire([1, 2, 3, 4], [13, 12, 11, 10])
    assert ((p >= 0.5) & (p <= 5)).all()


def test_retrouve_les_deux_camps():
    m = Recommandeur(k=2, lam=0.1, iterations=30).ajuster(petites_notes())
    assert m.predire([1], [13])[0] < m.predire([1], [11])[0]       # le spectateur 1 préfère le camp 10-11
    assert m.predire([3], [11])[0] < m.predire([3], [12])[0]


def test_recommande_des_films_non_vus():
    m = Recommandeur(k=2, lam=0.1).ajuster(petites_notes())
    reco = m.recommander(1, n=5)
    assert 13 in reco and not {10, 11, 12} & set(reco)


def test_spectateur_et_film_inconnus():
    m = Recommandeur(k=2).ajuster(petites_notes())
    assert np.isfinite(m.predire([999], [10])).all()
    assert np.isfinite(m.predire([1], [999])).all()


def test_nouveau_spectateur():
    m = Recommandeur(k=2, lam=0.1, iterations=30).ajuster(petites_notes())
    u = m.ajouter_spectateur({10: 5, 11: 4.5})
    assert m.predire([u], [11])[0] > m.predire([u], [13])[0]
    assert set(m.recommander(u, n=2)) == {12, 13}


def test_entrees_invalides():
    for fabriquer in [lambda: Recommandeur(k=0),
                      lambda: Recommandeur().ajuster(pd.DataFrame({"userId": [1], "movieId": [1]})),
                      lambda: Recommandeur().ajuster(pd.DataFrame({"userId": [1], "movieId": [1], "rating": [7]})),
                      lambda: Recommandeur().predire([1], [1]),
                      lambda: Recommandeur(k=2).ajuster(petites_notes()).ajouter_spectateur({999: 4})]:
        try:
            fabriquer()
        except (ValueError, RuntimeError):
            continue
        raise AssertionError("une entrée invalide aurait dû être refusée")


if __name__ == "__main__":
    tests = [f for nom, f in sorted(globals().items()) if nom.startswith("test_")]
    for t in tests:
        t()
        print("ok", t.__name__)
    print(f"{len(tests)} tests réussis")
