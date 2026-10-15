# M2 — Systèmes linéaires

**Question directrice : comment résoudre plusieurs contraintes à la fois ?**

Un alliage à doser, une réaction chimique à équilibrer, un circuit électrique, des forfaits à comparer, un repas à composer, le trafic d'un quartier : toutes ces situations imposent plusieurs contraintes en même temps. Ce module apprend à les traduire en **système d'équations linéaires**, à choisir un outil pour le résoudre, et surtout à interpréter les trois issues possibles. Il peut y avoir une solution, aucune, ou une infinité.

Il se termine par une question que l'on pose rarement : **peut-on faire confiance au résultat de la machine ?**

Durée indicative : 9 h. Prérequis : M1.

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [2.1 Mettre en équations](2.1-mettre-en-equations.ipynb) | Un bijoutier, une chimiste et un électricien : nommer les inconnues, traduire chaque contrainte, écrire $A\mathbf{x} = \mathbf{b}$ | 1 h 15 |
| [2.2 Le pivot de Gauss à la main puis à la machine](2.2-pivot-de-gauss.ipynb) | Les prix d'une fleuriste : élimination pas à pas en fractions exactes, puis SymPy et NumPy ; temps de calcul | 1 h 15 |
| [2.3 Zéro, une ou une infinité de solutions](2.3-nombre-de-solutions.ipynb) | Des forfaits téléphoniques et un repas de sportif : droites, plans, rang, et ce que chaque cas veut dire | 1 h 15 |
| [2.4 Quand l'ordinateur se trompe](2.4-quand-l-ordinateur-se-trompe.ipynb) | Deux laitons presque identiques : conditionnement, arrondis de la machine, pivot instable | 1 h 15 |
| [Mini-projet : équilibrer le trafic d'un quartier](M2-projet-trafic.ipynb) | Des flux de voitures inconnus : une infinité de solutions, dont certaines impossibles ; combien de capteurs installer ? | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Traduire une situation en système linéaire : inconnues, unités, une équation par contrainte.
- Résoudre un petit système à la main par le pivot de Gauss, et comprendre ce que fait la machine.
- Choisir entre calcul exact (SymPy) et calcul numérique (NumPy) selon le besoin.
- Diagnostiquer le nombre de solutions avec le rang, et traduire chaque cas dans le langage du problème.
- Décider si un résultat numérique est fiable, et repérer d'où viendrait une erreur : données, machine ou méthode.

## Les deux idées à retenir

:::{important} Le nombre de solutions est une information
« Aucune solution » signifie que les contraintes se contredisent : la cible est inatteignable, ou une donnée est fausse. « Une infinité » signifie qu'il manque une contrainte : il reste un choix à faire, qui appelle un critère supplémentaire. Dans les deux cas, ce n'est pas un échec du calcul, c'est une réponse sur le problème.
:::

:::{important} Un problème peut être mal posé pour toute machine
Quand deux contraintes se ressemblent beaucoup, une petite erreur sur les données produit une grande erreur sur la solution. Le **nombre de conditionnement** mesure ce risque. Aucun ordinateur ne le corrige : seule une meilleure formulation ou de meilleures mesures le peuvent.
:::

## Outils utilisés

NumPy (`np.linalg.solve`, `np.linalg.matrix_rank`, `np.linalg.cond`), SciPy (`null_space`, `hilbert`), SymPy (`Matrix.rref`, `linsolve`) et Matplotlib.

## Un aperçu du module suivant

Dans ce module, une matrice est un tableau de coefficients. Le module M3 change de regard : une matrice devient une **action** sur l'espace, qui tourne, étire ou projette les objets. Résoudre $A\mathbf{x} = \mathbf{b}$ reviendra alors à se demander quel point a été envoyé sur $\mathbf{b}$.
