# M8 — Décomposition en valeurs singulières et données

**Question directrice : comment garder l'essentiel d'une donnée ?**

Toute matrice, quelle que soit sa taille, se décompose en trois gestes simples : tourner, étirer selon des axes perpendiculaires, tourner. Cette **décomposition en valeurs singulières** (SVD) range l'information d'un tableau par ordre d'importance. En ne gardant que les premières couches, on résume des données, on les compresse, on en fait une image lisible.

Ce module rassemble presque tout le parcours : transformations (M3), conditionnement (M4), bases et rang (M5), projections et moindres carrés (M6), valeurs propres (M7). Il apprend aussi à se méfier : un résumé peut tromper.

Durée indicative : 8 h. Prérequis : M6 (M7 conseillé).

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [8.1 Ce que fait la SVD](8.1-ce-que-fait-la-svd.ipynb) | Le badge incliné d'une graphiste : les axes de l'ellipse, rotation-étirement-rotation, matrices rectangulaires, ce que résument les valeurs singulières | 1 h 15 |
| [8.2 Approximation de rang faible](8.2-rang-faible.ipynb) | Les normales de température de 80 stations : garder 2 couches sur 12, profils types et géographie, théorème d'Eckart-Young | 1 h 15 |
| [8.3 Analyse en composantes principales](8.3-acp.ipynb) | Les notes de 150 élèves de terminale : deux nombres par élève, cercle des corrélations, une figure pour le conseil de classe | 1 h 15 |
| [8.4 Quand l'ACP trompe](8.4-quand-l-acp-trompe.ipynb) | Les mesures d'un club d'athlétisme : unités, valeur aberrante, structure courbe, direction utile peu dispersée | 1 h 15 |
| [Mini-projet : compresser une image](M8-projet-compression.ipynb) | Un portrait pour une exposition en ligne : choisir $k$, comparer au JPEG, une fonction testée, déboguer, recommander | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Décrire géométriquement la SVD d'une matrice et lire ses valeurs singulières (étirements, rang, conditionnement).
- Approcher une matrice par une matrice de rang faible, choisir le nombre de couches selon un critère d'erreur, et interpréter les profils obtenus.
- Réaliser et interpréter une analyse en composantes principales, et en communiquer le résultat par une figure adaptée.
- Repérer les situations où une ACP donne une image trompeuse, et faire les contrôles nécessaires.
- Transformer une méthode en une fonction fiable, accompagnée de tests, et comparer honnêtement deux outils.

## Les trois idées à retenir

:::{important} Toute matrice : tourner, étirer, tourner
$$
A = U\,\Sigma\,V^{\mathsf{T}}, \qquad A\,\mathbf{v}_i = \sigma_i\,\mathbf{u}_i, \qquad \sigma_1 \geq \sigma_2 \geq \dots \geq 0 .
$$
Les valeurs singulières donnent les étirements ; leur rapport $\sigma_1/\sigma_n$ est le conditionnement.
:::

:::{important} Les premières couches sont les meilleures
$$
A_k = \sum_{i=1}^{k} \sigma_i\,\mathbf{u}_i\mathbf{v}_i^{\mathsf{T}}, \qquad \lVert A - A_k \rVert = \sqrt{\sigma_{k+1}^2 + \sigma_{k+2}^2 + \cdots}
$$
Aucune matrice de rang $k$ ne fait mieux (théorème d'Eckart-Young).
:::

:::{important} « Plus dispersé » ne veut pas dire « plus important »
L'ACP dépend des unités, craint les valeurs aberrantes, ne voit que des axes droits, et range les directions par dispersion, pas par intérêt pour votre question.
:::

## Outils utilisés

NumPy (`np.linalg.svd`, `np.linalg.eigh`), pandas, Matplotlib, Pillow pour le format JPEG, et l'instruction `assert` pour écrire des tests.

## Sources des données

Le portrait de Grace Hopper (photographie de l'US Navy, domaine public) est fourni avec Matplotlib. Les normales de température, les notes d'élèves et les mesures d'athlètes sont simulées à partir de modèles réalistes.

## Et ensuite ?

Le parcours se termine par trois **projets intégrateurs** : une recommandation de films, l'influence dans un réseau social, la reconnaissance de chiffres manuscrits. Chacun mobilise plusieurs modules à la fois, de la question au rapport.
