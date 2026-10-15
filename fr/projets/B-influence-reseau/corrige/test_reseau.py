"""Tests du module reseau (corrigé). Lancer : python test_reseau.py  (ou pytest)."""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from reseau import centralites, coupe_spectrale, distances_et_chemins, intermediarite, portee, verifier_adjacence


def etoile(n=5):
    A = np.zeros((n, n))
    A[0, 1:] = A[1:, 0] = 1
    return A


def deux_triangles():
    A = np.zeros((6, 6))
    for i, j in [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 3)]:
        A[i, j] = A[j, i] = 1
    return A


def test_le_centre_d_une_etoile_domine_toutes_les_mesures():
    c = centralites(etoile())
    assert (c.idxmax() == 0).all()


def test_mesures_symetriques_pour_un_cycle():
    n = 6
    A = np.zeros((n, n))
    for i in range(n):
        A[i, (i + 1) % n] = A[(i + 1) % n, i] = 1
    c = centralites(A)
    assert np.allclose(c.std(), 0)                    # tous les membres jouent le même rôle


def test_distances_et_nombre_de_chemins_d_un_carre():
    A = np.zeros((4, 4))
    for i, j in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        A[i, j] = A[j, i] = 1
    D, S = distances_et_chemins(A)
    assert D[0, 2] == 2 and S[0, 2] == 2            # deux plus courts chemins entre sommets opposés


def test_intermediarite_d_un_chemin():
    A = np.zeros((3, 3))
    A[0, 1] = A[1, 0] = A[1, 2] = A[2, 1] = 1
    assert np.allclose(intermediarite(A), [0, 1, 0])


def test_coupe_spectrale_separe_les_deux_triangles():
    groupe, _ = coupe_spectrale(deux_triangles())
    assert list(groupe) in ([0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 0])


def test_portee_bornes():
    A = etoile()
    assert portee(A, [0], p=0) == 1
    assert portee(A, [0], p=1, etapes=1) == 5


def test_entrees_invalides():
    mauvaises = [np.ones((2, 3)), np.array([[0, 1], [0, 0]]), -etoile(), np.eye(3)]
    for A in mauvaises:
        try:
            verifier_adjacence(A)
        except ValueError:
            continue
        raise AssertionError("une matrice invalide aurait dû être refusée")
    A = etoile()
    A[0, 4] = A[4, 0] = 0                           # membre 4 isolé
    try:
        centralites(A)
        raise AssertionError("un membre isolé aurait dû être signalé")
    except ValueError:
        pass


if __name__ == "__main__":
    tests = [f for nom, f in sorted(globals().items()) if nom.startswith("test_")]
    for t in tests:
        t()
        print("ok", t.__name__)
    print(f"{len(tests)} tests réussis")
