# M7 — Valeurs propres et dynamique

**Question directrice : où va un système à long terme ?**

Une population d'oiseaux d'une année sur l'autre, la météo d'un jour au suivant, un internaute de page en page : beaucoup de systèmes évoluent **pas à pas**, chaque étape étant obtenue en multipliant l'état présent par une même matrice. Après de nombreuses étapes, leur comportement est dicté par quelques directions privilégiées de cette matrice : ses **vecteurs propres**.

Ce module apprend à trouver ces directions, à lire ce qu'elles disent du long terme (croissance, déclin, équilibre), et à les calculer efficacement pour de très grands systèmes.

Durée indicative : 9 h. Prérequis : M5.

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [7.1 Les directions qui ne tournent pas](7.1-directions-invariantes.ipynb) | Un tissu élastique étiré : explorer les directions qui ne tournent pas, polynôme caractéristique, `np.linalg.eig`, galerie de transformations | 1 h 15 |
| [7.2 Population structurée par âge](7.2-population-leslie.ipynb) | Des chouettes chevêches en déclin : matrice de Leslie, taux de croissance, structure d'âge stable, effet des nichoirs | 1 h 15 |
| [7.3 Chaînes de Markov](7.3-chaines-de-markov.ipynb) | La météo d'un camping et les parts de marché de trois opérateurs : état stationnaire, vitesse d'oubli, contre-exemples | 1 h 15 |
| [7.4 La méthode de la puissance](7.4-methode-de-la-puissance.ipynb) | Classer 1 200 pongistes avec la méthode de Keener : vecteur propre dominant sans tout calculer, coût, convergence, trois façons d'échouer | 1 h 15 |
| [Mini-projet : PageRank d'un mini-web](M7-projet-pagerank.ipynb) | Vingt pages sur le vélo en ville : surfeur aléatoire, classement, facteur d'amortissement, ferme de liens | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Reconnaître un vecteur propre comme une direction qu'une transformation ne fait pas tourner, et calculer les valeurs propres d'une matrice $2 \times 2$ à la main.
- Modéliser un système qui évolue par étapes par $\mathbf{x}_{t+1} = A\,\mathbf{x}_t$ et en déduire son comportement à long terme.
- Interpréter la valeur propre dominante (taux de croissance) et le vecteur propre associé (structure stable, état stationnaire, classement).
- Calculer un vecteur propre dominant par la méthode de la puissance, en connaître le coût et les cas d'échec.
- Étudier l'effet d'un paramètre sur le comportement à long terme d'un modèle.

## Les trois idées à retenir

:::{important} Un vecteur propre garde sa direction
$$
A\mathbf{v} = \lambda\,\mathbf{v}, \qquad \det(A - \lambda I) = 0 .
$$
La valeur propre $\lambda$ est le facteur d'étirement dans la direction de $\mathbf{v}$.
:::

:::{important} À long terme, la valeur propre dominante l'emporte
$$
A^t\mathbf{x}_0 \approx c\,\lambda_1^t\,\mathbf{v}_1 .
$$
$\lambda_1$ donne le rythme (croissance si $\lambda_1 > 1$), $\mathbf{v}_1$ la forme de l'état final. Pour une chaîne de Markov, $\lambda_1 = 1$ et $\mathbf{v}_1$ est l'état stationnaire.
:::

:::{important} Pas besoin de tout calculer
La méthode de la puissance n'utilise que des produits matrice-vecteur. Elle converge au rythme de $\lvert \lambda_2 / \lambda_1 \rvert^k$ : vite si la valeur propre dominante est bien détachée, lentement sinon.
:::

## Outils utilisés

NumPy (`np.linalg.eig`, `np.linalg.eigvals`, `np.real_if_close`, `np.linalg.matrix_power`, `np.add.at`), pandas, Matplotlib et, si installé, ipywidgets pour le curseur du notebook 7.1.

## Sources des données

Les paramètres de la population de chouettes, les relevés météo, les parts de marché, la ligue de tennis de table et le mini-web sont fictifs, construits pour être réalistes.

## Un aperçu du module suivant

La méthode de la puissance ne donne qu'une direction : la plus importante. Le module M8 généralise cette idée à **toutes** les directions d'un tableau de données, rangées par importance : la **décomposition en valeurs singulières**, qui permet de compresser une image ou de résumer des données en gardant l'essentiel.
