# M5 — Espaces vectoriels et bases

**Question directrice : quelle information est redondante ?**

Au module M4, une matrice non inversible écrasait certaines directions. Ce module s'intéresse à ces directions, et plus largement à la manière de **décrire** un espace : avec combien de vecteurs, et lesquels ?

Deux idées le traversent. D'abord, un même objet (une couleur, un polynôme, une ligne de données) a des **coordonnées différentes selon la base** choisie, et certaines bases sont bien plus utiles que d'autres. Ensuite, le **rang** compte les informations réellement différentes d'un tableau : les colonnes en trop se calculent à partir des autres, et les relations qui les lient forment le **noyau**.

Durée indicative : 8 h. Prérequis : M4.

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [5.1 Changer de base de couleurs](5.1-changer-de-base-couleurs.ipynb) | Alléger les photos du club : passer de RVB à YCbCr, comprendre pourquoi le format JPEG réduit la teinte et pas la luminosité | 1 h 15 |
| [5.2 Variables redondantes](5.2-variables-redondantes.ipynb) | Les ventes d'une librairie en ligne : indépendance linéaire, rang avec tolérance, relations cachées, limites affines et non linéaires | 1 h 15 |
| [5.3 Les polynômes sont des vecteurs](5.3-polynomes-vecteurs.ipynb) | Une courbe de température : base canonique, base de Lagrange, matrice de Vandermonde et stabilité des coordonnées | 1 h 15 |
| [Mini-projet : détecter la redondance](M5-projet-redondance.ipynb) | Les étiquettes nutritionnelles de 42 produits : retrouver les formules de l'énergie et du sel, repérer les fiches mal saisies | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Calculer les coordonnées d'un vecteur dans une nouvelle base, en résolvant un système.
- Choisir une base adaptée au problème, et expliquer ce qu'elle fait gagner : compression, lisibilité, stabilité.
- Déterminer le rang d'un tableau de données avec une tolérance justifiée par la précision des données.
- Retrouver les relations linéaires entre colonnes et les interpréter comme des règles du domaine.
- Reconnaître les limites de la méthode : relations affines ou non linéaires, erreurs de saisie, échantillon trop petit.

## Les trois idées à retenir

:::{important} Changer de base, c'est résoudre un système
Si les vecteurs de la nouvelle base sont les colonnes d'une matrice $P$, les nouvelles coordonnées $\mathbf{c}$ d'un vecteur $\mathbf{v}$ vérifient
$$
P\,\mathbf{c} = \mathbf{v} .
$$
Le vecteur ne change pas : seule sa description change. Une bonne base concentre l'information (la luminance $Y$) ou la rend directement lisible (les valeurs mesurées dans la base de Lagrange).
:::

:::{important} Rang et noyau se partagent les colonnes
$$
\text{nombre de colonnes} = \operatorname{rang} A + \dim \ker A
$$
Le rang compte les informations indépendantes ; chaque vecteur du noyau est une relation entre colonnes. Sur des données réelles, arrondies, le rang dépend d'une **tolérance** qu'il faut choisir et justifier.
:::

:::{important} Une base presque dépendante est une mauvaise base
Les fonctions $t^4$ et $t^5$ sont presque parallèles sur une journée : la matrice de Vandermonde est très mal conditionnée, et une erreur de 0,05 °C bouleverse les coefficients. Changer de variable ou de base rend le calcul stable.
:::

## Outils utilisés

NumPy (`np.linalg.solve`, `np.linalg.matrix_rank`, `np.linalg.lstsq`, `np.linalg.cond`, `np.vander`, et `np.linalg.svd` en boîte noire), pandas et Matplotlib.

## Un aperçu du module suivant

Pour trouver les relations entre colonnes, on a cherché la combinaison qui approche **au mieux** une colonne, avec `np.linalg.lstsq`. Le module M6 explique ce que veut dire « au mieux » : la **projection orthogonale** et la méthode des **moindres carrés**, pour tracer la droite qui résume le mieux des données imparfaites.
