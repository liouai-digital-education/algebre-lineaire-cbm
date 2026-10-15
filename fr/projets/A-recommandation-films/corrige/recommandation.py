"""Module de recommandation de films (projet A) — version de référence.

Les élèves écrivent leur propre version ; celle-ci sert de corrigé et de point de comparaison.
"""
import numpy as np

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from films import Index, ajuster_biais


class Recommandeur:
    """Recommandation de films par biais et facteurs latents (moindres carrés alternés).

    Utilisation :
        modele = Recommandeur(k=10, lam=5).ajuster(notes)     # notes : userId, movieId, rating
        modele.predire([1, 1], [10, 20])                     # notes prévues
        modele.recommander(1, n=10)                          # identifiants des films conseillés
        nouveau = modele.ajouter_spectateur({10: 4.5, 20: 2.0})
    """

    COLONNES = ("userId", "movieId", "rating")

    def __init__(self, k=10, lam=5.0, lam_biais=10.0, iterations=15, graine=0):
        if k < 1 or lam < 0 or lam_biais < 0 or iterations < 1:
            raise ValueError("Réglages invalides : il faut k ≥ 1, lam ≥ 0, lam_biais ≥ 0, iterations ≥ 1.")
        self.k, self.lam, self.lam_biais, self.iterations, self.graine = k, lam, lam_biais, iterations, graine
        self.ajuste = False

    # ---------------------------------------------------------------- apprentissage
    def ajuster(self, notes):
        manquantes = [c for c in self.COLONNES if c not in notes.columns]
        if manquantes:
            raise ValueError(f"Colonnes manquantes : {manquantes}")
        if len(notes) == 0:
            raise ValueError("Aucune note fournie.")
        if notes["rating"].isna().any() or (notes["rating"] < 0.5).any() or (notes["rating"] > 5).any():
            raise ValueError("Les notes doivent être comprises entre 0,5 et 5.")
        self.mu, bu, bf = ajuster_biais(notes, self.lam_biais)
        self.index = Index(notes)
        self.bu = np.array([bu[u] for u in self.index.spectateurs])
        self.bf = np.array([bf[f] for f in self.index.films])
        R = self.index.matrice(notes)
        connu = ~np.isnan(R)
        E = np.where(connu, R - self.mu - self.bu[:, None] - self.bf[None, :], 0.0)
        self.P, self.Q = self._alterner(E, connu)
        self.vus = {u: set(g) for u, g in notes.groupby("userId")["movieId"]}
        self.nouveaux = {}
        self.ajuste = True
        return self

    def _alterner(self, E, connu):
        rng = np.random.default_rng(self.graine)
        P = rng.normal(0, 0.1, (E.shape[0], self.k))
        Q = rng.normal(0, 0.1, (E.shape[1], self.k))
        I = self.lam * np.eye(self.k)
        for _ in range(self.iterations):
            for u in range(E.shape[0]):
                j = connu[u]
                P[u] = np.linalg.solve(Q[j].T @ Q[j] + I, Q[j].T @ E[u, j])
            for f in range(E.shape[1]):
                i = connu[:, f]
                Q[f] = np.linalg.solve(P[i].T @ P[i] + I, P[i].T @ E[i, f])
        return P, Q

    # ---------------------------------------------------------------- prévision
    def _verifier(self):
        if not self.ajuste:
            raise RuntimeError("Le modèle n'est pas ajusté : appelez d'abord ajuster(notes).")

    def _profil(self, u):
        # renvoie (biais, vecteur de goûts) d'un spectateur, connu, ajouté ou inconnu
        if u in self.nouveaux:
            return self.nouveaux[u]
        i = self.index.ligne.get(u)
        if i is None:
            return 0.0, np.zeros(self.k)           # spectateur inconnu : on ne sait rien de ses goûts
        return self.bu[i], self.P[i]

    def predire(self, user_ids, movie_ids):
        self._verifier()
        user_ids, movie_ids = np.atleast_1d(user_ids), np.atleast_1d(movie_ids)
        if len(user_ids) != len(movie_ids):
            raise ValueError("user_ids et movie_ids doivent avoir la même longueur.")
        resultat = np.empty(len(user_ids))
        for n, (u, f) in enumerate(zip(user_ids, movie_ids)):
            b_u, p_u = self._profil(u)
            j = self.index.colonne.get(f)
            if j is None:                               # film inconnu : moyenne corrigée du spectateur
                resultat[n] = self.mu + b_u
            else:
                resultat[n] = self.mu + b_u + self.bf[j] + p_u @ self.Q[j]
        return np.clip(resultat, 0.5, 5)

    def recommander(self, user_id, n=10, notes_minimum=0, nb_notes_films=None):
        """Les n films non vus à la meilleure note prévue (éventuellement parmi les films assez notés)."""
        self._verifier()
        if n < 1:
            raise ValueError("n doit être au moins 1.")
        b_u, p_u = self._profil(user_id)
        scores = self.mu + b_u + self.bf + self.Q @ p_u
        deja_vus = self.vus.get(user_id, set())
        candidats = [j for j, f in enumerate(self.index.films) if f not in deja_vus
                     and (nb_notes_films is None or nb_notes_films.get(f, 0) >= notes_minimum)]
        meilleurs = sorted(candidats, key=lambda j: -scores[j])[:n]
        return [self.index.films[j] for j in meilleurs]

    def ajouter_spectateur(self, notes_du_spectateur, identifiant=None):
        """Ajoute un spectateur à partir de quelques notes {movieId: note}, sans tout réajuster.

        Ses biais et ses goûts sont obtenus par moindres carrés régularisés, les profils des films étant fixés.
        """
        self._verifier()
        connus = {f: r for f, r in notes_du_spectateur.items() if f in self.index.colonne}
        if not connus:
            raise ValueError("Aucun des films notés n'est connu du modèle.")
        j = np.array([self.index.colonne[f] for f in connus])
        r = np.array(list(connus.values()), dtype=float)
        A = np.column_stack([np.ones(len(j)), self.Q[j]])                 # inconnues : b_u puis p_u
        regul = np.diag([self.lam_biais] + [self.lam] * self.k)
        x = np.linalg.solve(A.T @ A + regul, A.T @ (r - self.mu - self.bf[j]))
        if identifiant is None:
            identifiant = f"nouveau-{len(self.nouveaux) + 1}"
        self.nouveaux[identifiant] = (x[0], x[1:])
        self.vus[identifiant] = set(connus)
        return identifiant
