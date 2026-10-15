# M0 — Python et NumPy comme outils

**Question directrice : comment faire calculer une machine ?**

Ce module ne fait pas encore d'algèbre linéaire. Il installe ce dont tout le parcours a besoin : manipuler des tableaux de nombres avec NumPy, et surtout **savoir s'auto-former à un outil nouveau**, en lisant sa documentation et en déboguant.

Même si vous connaissez déjà Python, faites au moins les notebooks 0.2 et 0.3 : la méthode d'apprentissage d'un outil et la méthode de débogage y sont fixées une fois pour toutes, et tous les modules suivants y renvoient.

Durée indicative : 6 h. Prérequis : aucun.

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [0.1 Faire calculer la machine](0.1-faire-calculer.ipynb) | Le budget de Camille : listes et boucles, puis tableaux NumPy, `sum`, `axis`, `argmax` | 1 h 15 |
| [0.2 Apprendre seul une fonction](0.2-apprendre-seul.ipynb) | L'épargne d'Hugo : découvrir `cumsum`, `where`, `linspace` par la seule documentation | 1 h 15 |
| [0.3 Les erreurs de forme](0.3-erreurs-de-forme.ipynb) | Le programme bogué d'une cantine : formes incompatibles, unités, mauvais axe | 1 h 15 |
| [Mini-projet : le panier de courses vectorisé](M0-projet-panier.ipynb) | Où Lina doit-elle faire ses courses ? Un magasin ou deux, trajets compris | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Choisir une technologie adaptée à la taille d'un calcul.
- Construire un tableau NumPy, lire sa forme et calculer le long d'un axe.
- Apprendre une fonction inconnue en 4 étapes : signature, valeur renvoyée, petit exemple connu, cas limites.
- Déboguer méthodiquement : formes, unités, forme du résultat, petit cas à la main, isolement.
- Sentir qu'un résultat est invraisemblable avant même de chercher l'erreur.

## Les deux méthodes à retenir

:::{admonition} Apprendre un outil nouveau
1. Lire la **signature** : nom, paramètres obligatoires et facultatifs.
2. Lire ce qu'il **renvoie** : type et forme.
3. **Tester sur un petit exemple** dont on connaît déjà la réponse.
4. Chercher les **cas limites**.
:::

:::{admonition} Déboguer un calcul
1. Vérifier les **formes** (`.shape`).
2. Vérifier les **unités**.
3. Vérifier la **forme du résultat** attendu.
4. Refaire un **petit cas à la main**.
5. **Isoler** l'étape fautive en exécutant morceau par morceau.
:::
