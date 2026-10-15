"""Mesures d'influence dans un réseau (projet B) — version de référence.

Les élèves écrivent leur propre version ; celle-ci sert de corrigé et de point de comparaison.
"""
import numpy as np
import pandas as pd


def verifier_adjacence(A):
    """Vérifie qu'une matrice décrit un réseau non orienté : carrée, symétrique, positive, sans boucle."""
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("La matrice d'adjacence doit être carrée.")
    if not np.allclose(A, A.T):
        raise ValueError("La matrice d'adjacence doit être symétrique (liens non orientés).")
    if (A < 0).any():
        raise ValueError("Les poids des liens doivent être positifs.")
    if np.any(np.diag(A) != 0):
        raise ValueError("Un membre ne peut pas être lié à lui-même.")
    return A


def distances_et_chemins(A):
    """Distances (longueur du plus court chemin) et nombre de plus courts chemins, par puissances de A."""
    B = (verifier_adjacence(A) > 0).astype(float)
    n = len(B)
    D = np.full((n, n), np.inf)
    S = np.zeros((n, n))
    np.fill_diagonal(D, 0)
    np.fill_diagonal(S, 1)
    P = np.eye(n)
    for k in range(1, n):
        P = P @ B                                   # P[i, j] = nombre de chemins de longueur k
        nouveaux = (P > 0) & np.isinf(D)
        D[nouveaux] = k
        S[nouveaux] = P[nouveaux]                   # les premiers chemins trouvés sont les plus courts
        if not nouveaux.any():
            break
    return D, S


def intermediarite(A):
    """Part des plus courts chemins entre deux autres membres qui passent par chaque membre."""
    D, S = distances_et_chemins(A)
    n = len(D)
    resultat = np.zeros(n)
    for k in range(n):
        for i in range(n):
            for j in range(i + 1, n):
                if k in (i, j) or not np.isfinite(D[i, j]):
                    continue
                if D[i, k] + D[k, j] == D[i, j]:
                    resultat[k] += S[i, k] * S[k, j] / S[i, j]
    paires = (n - 1) * (n - 2) / 2
    return resultat / paires


def centralites(A, alpha_relatif=0.5, d=0.85):
    """Tableau des mesures d'influence de chaque membre (une ligne par membre)."""
    A = verifier_adjacence(A)
    n = len(A)
    if n < 3:
        raise ValueError("Il faut au moins trois membres.")
    degre = A.sum(axis=1)
    if (degre == 0).any():
        raise ValueError("Le réseau contient un membre isolé : les mesures récursives ne sont pas définies.")
    valeurs, vecteurs = np.linalg.eigh(A)
    lam1 = valeurs[-1]
    propre = np.abs(vecteurs[:, -1])
    katz = np.linalg.solve(np.eye(n) - alpha_relatif / lam1 * A, np.ones(n)) - 1
    M = A / degre
    pagerank = np.ones(n) / n
    for _ in range(500):
        pagerank = d * M @ pagerank + (1 - d) / n
    D, _ = distances_et_chemins(A)
    if np.isinf(D).any():
        raise ValueError("Le réseau n'est pas connexe : traitez chaque partie séparément.")
    return pd.DataFrame({
        "degré": degre,
        "vecteur propre": propre / propre.sum(),
        "Katz": katz / katz.sum(),
        "PageRank": pagerank,
        "proximité": (n - 1) / D.sum(axis=1),
        "intermédiarité": intermediarite(A),
    })


def coupe_spectrale(A):
    """Sépare le réseau en deux groupes selon le signe du vecteur de Fiedler ; renvoie (groupe, vecteur)."""
    A = verifier_adjacence(A)
    L = np.diag(A.sum(axis=1)) - A
    _, vecteurs = np.linalg.eigh(L)
    v2 = vecteurs[:, 1]
    if v2[0] < 0:                                   # convention : le premier membre est dans le groupe 0
        v2 = -v2
    return (v2 < 0).astype(int), v2


def portee(A, departs, p=0.2, etapes=3, essais=300, graine=0):
    """Nombre moyen de membres touchés par une rumeur partie de `departs` (modèle en cascade)."""
    A = verifier_adjacence(A)
    if not 0 <= p <= 1:
        raise ValueError("La probabilité de transmission doit être comprise entre 0 et 1.")
    voisins = [np.nonzero(A[i])[0] for i in range(len(A))]
    rng = np.random.default_rng(graine)
    total = 0
    for _ in range(essais):
        informes, nouveaux = set(departs), list(departs)
        for _ in range(etapes):
            suivants = []
            for i in nouveaux:
                for j in voisins[i]:
                    if j not in informes and rng.random() < p:
                        informes.add(j)
                        suivants.append(j)
            nouveaux = suivants
        total += len(informes)
    return total / essais
