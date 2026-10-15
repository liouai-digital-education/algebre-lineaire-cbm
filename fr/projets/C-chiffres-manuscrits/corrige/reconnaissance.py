"""Reconnaissance de chiffres manuscrits par algèbre linéaire (projet C) — version de référence.

Les élèves écrivent leur propre version ; celle-ci sert de corrigé et de point de comparaison.

Exemple :
    r = Reconnaisseur("sous-espaces", k=10).ajuster(X_app, y_app)
    r.predire(X_test)          # chiffres reconnus
    r.reussite(X_test, y_test) # taux de réussite
"""
import numpy as np

METHODES = ("moyenne", "voisins", "sous-espaces")


def distances(A, B):
    """Matrice des distances entre les lignes de A et celles de B, par un produit de matrices."""
    carres = (A ** 2).sum(axis=1)[:, None] + (B ** 2).sum(axis=1)[None, :] - 2 * A @ B.T
    return np.sqrt(np.clip(carres, 0, None))


class Reconnaisseur:
    """Reconnaît des images vectorisées par l'une des trois méthodes du projet.

    - "moyenne" : chiffre moyen le plus proche ;
    - "voisins" : vote des k plus proches images d'apprentissage ;
    - "sous-espaces" : plus petit résidu de projection sur un sous-espace affine de dimension k par chiffre.
    """

    def __init__(self, methode="sous-espaces", k=10):
        if methode not in METHODES:
            raise ValueError(f"Méthode inconnue : {methode!r}. Choisir parmi {METHODES}.")
        if int(k) != k or k < 0 or (methode == "voisins" and k < 1):
            raise ValueError("k doit être un entier positif (au moins 1 pour les voisins).")
        self.methode, self.k = methode, int(k)
        self.classes = None

    # --- apprentissage -------------------------------------------------------------------------
    def ajuster(self, X, y):
        X, y = self._verifier(X), np.asarray(y)
        if len(X) != len(y):
            raise ValueError("Il faut autant d'étiquettes que d'images.")
        self.classes = np.unique(y)
        if self.methode == "voisins":
            self.X_app, self.y_app = X.copy(), y.copy()
        else:
            self.modeles = []
            for c in self.classes:
                Xc = X[y == c]
                m = Xc.mean(axis=0)
                _, _, Vt = np.linalg.svd(Xc - m, full_matrices=False)
                k = 0 if self.methode == "moyenne" else min(self.k, len(Vt))
                self.modeles.append((m, Vt[:k].T))
        return self

    # --- décision ------------------------------------------------------------------------------
    def scores(self, X):
        """Une colonne par chiffre ; plus le score est petit, plus le chiffre est plausible."""
        X = self._verifier(X)
        if self.classes is None:
            raise RuntimeError("Appeler ajuster() avant de reconnaître.")
        if self.methode == "voisins":
            raise ValueError("La méthode des voisins ne produit pas de score par chiffre.")
        S = np.zeros((len(X), len(self.classes)))
        for j, (m, V) in enumerate(self.modeles):
            ecart = X - m
            S[:, j] = np.linalg.norm(ecart - ecart @ V @ V.T, axis=1)
        return S

    def predire(self, X):
        X = self._verifier(X)
        if self.classes is None:
            raise RuntimeError("Appeler ajuster() avant de reconnaître.")
        if self.methode != "voisins":
            return self.classes[np.argmin(self.scores(X), axis=1)]
        proches = np.argsort(distances(X, self.X_app), axis=1)[:, :self.k]
        resultat = []
        for ligne in self.y_app[proches]:
            valeurs, comptes = np.unique(ligne, return_counts=True)
            gagnants = valeurs[comptes == comptes.max()]
            resultat.append(next(c for c in ligne if c in gagnants))   # égalité : le plus proche l'emporte
        return np.array(resultat)

    def predire_avec_rejet(self, X, seuil=0.9):
        """Comme predire, mais renvoie -1 quand les deux meilleurs scores sont trop proches."""
        if not 0 < seuil <= 1:
            raise ValueError("Le seuil doit être compris entre 0 (exclu) et 1.")
        S = self.scores(X)
        tries = np.sort(S, axis=1)
        predits = self.classes[np.argmin(S, axis=1)].astype(int)
        hesitants = tries[:, 0] > seuil * tries[:, 1]
        predits[hesitants] = -1
        return predits

    def reussite(self, X, y):
        return float(np.mean(self.predire(X) == np.asarray(y)))

    def taille_memoire(self):
        """Nombre de valeurs à conserver pour reconnaître."""
        if self.methode == "voisins":
            return self.X_app.size
        return sum(m.size + V.size for m, V in self.modeles)

    # --- contrôles -----------------------------------------------------------------------------
    @staticmethod
    def _verifier(X):
        X = np.asarray(X, dtype=float)
        if X.ndim != 2:
            raise ValueError("Les images doivent former un tableau à deux dimensions (une ligne par image).")
        if not np.isfinite(X).all():
            raise ValueError("Les images contiennent des valeurs manquantes ou infinies.")
        return X
