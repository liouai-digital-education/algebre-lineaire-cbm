# M3 — Matrices et transformations

**Question directrice : comment déformer une image ?**

Au module M2, une matrice était un tableau de coefficients. Ici, elle devient une **action** : elle fait tourner, agrandit, étire, incline, aplatit ou retourne les figures. Ce changement de regard est au cœur de l'informatique graphique, des logiciels de dessin aux jeux vidéo en 3D.

Une idée simple porte tout le module : une matrice est entièrement décrite par ce qu'elle fait aux vecteurs de base. Ses **colonnes** sont les images de $\mathbf{e}_1$ et de $\mathbf{e}_2$.

Durée indicative : 8 h. Prérequis : M2.

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [3.1 Déformer une grille](3.1-deformer-une-grille.ipynb) | Les boutons d'un logiciel de dessin : rotation, homothétie, étirement, cisaillement, projection, symétrie ; lire une matrice dans ses colonnes | 1 h 15 |
| [3.2 L'ordre compte](3.2-l-ordre-compte.ipynb) | Deux graphistes, deux résultats : composer, c'est multiplier ; $AB \neq BA$ ; formules d'addition et miroirs | 1 h 15 |
| [3.3 Translater avec une matrice](3.3-coordonnees-homogenes.ipynb) | Le moulin d'un jeu vidéo : pourquoi une translation n'est pas linéaire, et l'astuce des coordonnées homogènes | 1 h 15 |
| [Mini-projet : mini-moteur 3D fil de fer](M3-projet-moteur-3d.ipynb) | Un cube, puis une maison, qui tournent avec des curseurs : rotations 3D, projections orthographique et en perspective | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Écrire la matrice d'une transformation du plan en lisant les images des vecteurs de base, et inversement.
- Reconnaître ce qu'une transformation conserve : longueurs, angles, aires, orientation.
- Composer des transformations par un produit de matrices, dans le bon ordre.
- Utiliser les coordonnées homogènes pour traiter les translations et les rotations autour d'un point quelconque.
- Construire un petit moteur d'affichage 3D et expliquer d'où vient l'effet de perspective.

## Les trois idées à retenir

:::{important} Les colonnes racontent tout
$$
A = \begin{pmatrix} | & | \\ A\mathbf{e}_1 & A\mathbf{e}_2 \\ | & | \end{pmatrix}
\qquad\text{et}\qquad
A\begin{pmatrix} x \\ y \end{pmatrix} = x\,A\mathbf{e}_1 + y\,A\mathbf{e}_2
$$
:::

:::{important} Le produit se lit de droite à gauche
$(AB)\mathbf{x} = A(B\mathbf{x})$ : la transformation écrite à droite agit en premier. En général $AB \neq BA$.
:::

:::{important} Une dimension de plus pour les translations
Une translation n'envoie pas l'origine sur elle-même : ce n'est pas une application linéaire. En coordonnées homogènes $(x\,;\,y\,;\,1)$, elle devient un produit par une matrice $3 \times 3$.
:::

## Outils utilisés

NumPy (produit `@`, `np.column_stack`, `np.allclose`), Matplotlib (`fill`, `annotate`), SciPy (`ndimage.affine_transform`) et, si installé, ipywidgets pour les curseurs.

## Un aperçu du module suivant

Le bouton « Aplatir » écrase le logo sur une droite : impossible de revenir en arrière. Le module M4 étudie quand une transformation peut être **défaite** (la matrice inverse), et le nombre qui le décide : le **déterminant**, qui n'est autre que le facteur d'aire mesuré au notebook 3.1.
