# M1 — Vecteurs et ressemblance

**Question directrice : comment mesurer la ressemblance ?**

Un déplacement, une couleur, un profil d'écoute musicale ou une recette de cuisine peuvent tous s'écrire comme une liste de nombres : un **vecteur**. Ce module apprend à faire ce passage du monde aux vecteurs, puis à choisir une mesure de ressemblance adaptée à la question posée.

Durée indicative : 7 h. Prérequis : M0.

## Activités

| Activité | Contenu | Durée |
|---|---|---|
| [1.1 Forces et déplacements](1.1-forces-deplacements.ipynb) | Une course d'orientation et un kayak dans le courant : somme, multiplication par un nombre, norme | 1 h 15 |
| [1.2 Mélanger des lumières](1.2-melanger-lumieres.ipynb) | Régler trois projecteurs de théâtre : combinaisons linéaires, couleurs atteignables ou non | 1 h 15 |
| [1.3 Distance ou angle ?](1.3-distance-ou-angle.ipynb) | Des profils d'écoute musicale : distances euclidienne et de Manhattan, similarité cosinus | 1 h 15 |
| [Mini-projet : recommander une recette](M1-projet-recettes.ipynb) | Calculer l'encadré « Vous aimerez aussi » d'un site de cuisine, et critiquer ses choix | 2 h 30 |

## Ce que vous saurez faire à la fin du module

- Représenter une situation réelle par des vecteurs, et justifier ce choix.
- Calculer et interpréter une somme de vecteurs, un produit par un nombre, une norme, un produit scalaire.
- Reconnaître quand un modèle linéaire s'applique, et quand il n'est qu'une approximation.
- Choisir entre distance et angle selon la question posée, et justifier ce choix.
- Corroborer un résultat en comparant plusieurs méthodes.

## L'idée clé du module

:::{important} Concept et outils
Le **concept** est le même du début à la fin : mesurer à quel point deux vecteurs se ressemblent. Les **outils** changent : distance euclidienne, distance de Manhattan, similarité cosinus, représentation en quantités ou en présence. Aucun n'est « le bon » dans l'absolu : le bon outil est celui qui répond à la question précise que l'on s'est posée à l'étape ①.
:::

## Un aperçu du module suivant

Dans le notebook 1.2, vous utilisez `np.linalg.solve` comme une boîte noire pour trouver les réglages des projecteurs. Le module M2 ouvre cette boîte : comment résoudre un système d'équations, et pourquoi il peut n'avoir aucune solution, une seule ou une infinité.
