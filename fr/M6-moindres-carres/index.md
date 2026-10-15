# M6 — Orthogonalité et moindres carrés

**Question directrice : quelle droite résume le mieux des données imparfaites ?**

Des mesures réelles ne s'alignent jamais parfaitement. Le système d'équations qu'elles définissent n'a alors **aucune solution** : trop d'équations, pas assez d'inconnues, et du bruit partout. Ce module apprend à chercher la **meilleure** réponse possible, puis à juger si elle est digne de confiance.

L'idée clé est géométrique. Le meilleur compromis est une **projection orthogonale** : le point le plus proche, atteint par un chemin perpendiculaire. Du randonneur qui rejoint un sentier à la courbe du CO₂ atmosphérique, c'est le même calcul.

Durée indicative : 9 h. Prérequis : M5.

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [6.1 Projeter](6.1-projeter.ipynb) | Rejoindre un sentier dans le brouillard, imiter une couleur avec une lampe à deux diodes : projection sur une droite, sur un plan, équations normales | 1 h 15 |
| [6.2 La meilleure droite](6.2-la-meilleure-droite.ipynb) | Le rebond d'une balle mesuré par deux groupes : moindres carrés, analyse des résidus, erreur systématique et mesure aberrante | 1 h 15 |
| [6.3 Trois outils, un problème](6.3-trois-outils.ipynb) | Étalonner un capteur : équations normales, `lstsq` et QR comparés en précision et en vitesse ; Gram-Schmidt programmé à la main | 1 h 15 |
| [6.4 Valider un modèle](6.4-valider-un-modele.ipynb) | La consommation électrique d'une école : apprentissage et test, surajustement, degrés-jours, résidus qui révèlent le mercredi | 1 h 15 |
| [Mini-projet : la courbe du CO₂ atmosphérique](M6-projet-co2.ipynb) | La série de Mauna Loa (1958-2026) : tendance et saison, validation, année de franchissement de 450 et 500 ppm avec une incertitude, rapport | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Projeter un vecteur sur une droite ou un plan, et interpréter la projection comme le point le plus proche.
- Poser un problème d'ajustement sous la forme $A\mathbf{x} \approx \mathbf{b}$, avec des colonnes choisies pour le phénomène étudié.
- Choisir un outil de résolution en connaissant ses forces et ses faiblesses numériques.
- Lire les résidus pour repérer une erreur systématique, une mesure aberrante ou un ingrédient manquant du modèle.
- Valider un modèle sur des données qu'il n'a pas vues, et accompagner une prévision d'une incertitude honnête.

## Les trois idées à retenir

:::{important} Le meilleur compromis est une projection
Si $A\mathbf{x} = \mathbf{b}$ n'a pas de solution, la solution des moindres carrés $\hat{\mathbf{x}}$ rend le reste $\mathbf{b} - A\hat{\mathbf{x}}$ orthogonal aux colonnes de $A$ :
$$
A^{\mathsf{T}}A\,\hat{\mathbf{x}} = A^{\mathsf{T}}\mathbf{b} .
$$
:::

:::{important} Mathématiquement équivalent ne veut pas dire numériquement équivalent
Les équations normales élèvent le conditionnement au carré : $\operatorname{cond}(A^{\mathsf{T}}A) = \operatorname{cond}(A)^2$. La décomposition $A = QR$ évite ce piège. Bien poser le problème (remettre les variables à l'échelle) compte souvent plus que le choix de l'outil.
:::

:::{important} Un modèle se juge sur ce qu'il n'a pas vu
L'erreur sur les données d'apprentissage baisse toujours quand on ajoute des paramètres. Seule l'erreur sur des données de test mesure la qualité d'une prévision. Des résidus qui ont une forme signalent ce que le modèle n'a pas compris.
:::

## Outils utilisés

NumPy (`np.linalg.lstsq`, `np.linalg.qr`, `np.linalg.solve`, `np.linalg.cond`, `np.polyfit`, `np.vander`), pandas, Matplotlib et le module `time` pour chronométrer.

## Sources des données

La série de Mauna Loa provient du Global Monitoring Laboratory de la NOAA (domaine public), via le dépôt `datasets/co2-ppm`. Les autres jeux de données du module sont simulés à partir de modèles réalistes.

## Un aperçu du module suivant

Dans la série du CO₂, on a cherché ce qui se **répète** (la saison) et ce qui **dure** (la tendance). Le module M7 étudie les systèmes qui évoluent pas à pas, comme une population ou la navigation sur le Web, et les directions privilégiées qui décident de leur comportement à long terme : les **vecteurs propres**.
