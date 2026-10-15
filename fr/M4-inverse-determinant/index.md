# M4 — Inverse, déterminant, rang

**Question directrice : quand peut-on revenir en arrière ?**

Au module M3, une matrice agissait sur le plan. Ce module pose la question inverse : peut-on **défaire** cette action ? Redresser un plan dessiné en perspective, déchiffrer un message, déflouer une photo, remonter de la demande finale à la production d'une économie : à chaque fois, il faut une matrice inverse.

Deux nombres guident la réponse. Le **déterminant** dit si l'inverse existe : c'est le facteur par lequel la matrice multiplie les aires. Le **conditionnement** dit si l'inverse est utilisable en pratique, quand les données sont imparfaites.

Durée indicative : 8 h. Prérequis : M2 (M3 conseillé).

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [4.1 Le déterminant comme facteur d'aire](4.1-determinant-et-aire.ipynb) | Le plan en perspective d'un jardin partagé : surface réelle des parcelles, signe et orientation, $\det(AB) = \det A \det B$, volumes en 3D | 1 h 15 |
| [4.2 Chiffrer et déchiffrer](4.2-chiffre-de-hill.ipynb) | Le chiffre de Hill : inverse modulo 26, clés valides et invalides, attaque à texte clair connu | 1 h 15 |
| [4.3 Presque singulière](4.3-presque-singuliere.ipynb) | Déflouer le code-barres d'un livre : l'inverse amplifie le bruit, le déterminant trompe, la régularisation sauve | 1 h 15 |
| [Mini-projet : modèle de Leontief](M4-projet-leontief.ipynb) | L'économie d'une région à trois secteurs : production nécessaire, effets d'entraînement, fiabilité des coefficients | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Calculer et interpréter un déterminant : facteur d'aire ou de volume, orientation, inversibilité.
- Inverser une matrice $2 \times 2$ à la main, et savoir quand il vaut mieux résoudre un système qu'inverser.
- Reconnaître que l'inversibilité dépend de l'arithmétique utilisée (nombres réels ou calcul modulo 26).
- Distinguer « non inversible » et « presque singulière », et juger la fiabilité d'une inversion avec le conditionnement.
- Construire et interpréter un modèle entrée-sortie de Leontief, et tester sa sensibilité aux données.

## Les trois idées à retenir

:::{important} Le déterminant est un facteur d'aire
$$
\det \begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc,
\qquad
\text{aire de l'image} = \lvert \det A \rvert \times \text{aire de départ}
$$
Un déterminant nul aplatit le plan : aucune information perdue ne peut être retrouvée, il n'y a pas d'inverse.
:::

:::{important} L'inverse existe, mais est-il utilisable ?
Un déterminant minuscule ne signale pas forcément un problème : $\det(0{,}1\,I_{10}) = 10^{-10}$. C'est le **conditionnement** qui mesure l'amplification des erreurs par l'inverse.
:::

:::{important} Résoudre plutôt qu'inverser
Pour obtenir $\mathbf{x} = A^{-1}\mathbf{b}$, on appelle `np.linalg.solve(A, b)`. On ne calcule $A^{-1}$ que lorsque la matrice inverse a elle-même un sens, comme l'inverse de Leontief.
:::

## Outils utilisés

NumPy (`np.linalg.det`, `np.linalg.inv`, `np.linalg.solve`, `np.linalg.cond`), SciPy (`linalg.toeplitz`), pandas, la fonction `pow(d, -1, 26)` de Python pour l'inverse modulaire, et Matplotlib.

## Un aperçu du module suivant

Une matrice non inversible écrase l'espace : certaines directions sont perdues. Le module M5 étudie précisément ces directions, avec les notions de **base**, de **dimension** et de **noyau**, et les applique à la détection d'informations redondantes dans des données.
