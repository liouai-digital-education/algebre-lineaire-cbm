# Algèbre linéaire — penser, calculer, interpréter

**Un parcours *Computer-Based Maths* avec Python, par [Liouaï Digital Education](https://liouai-digital-education.github.io).**

**➜ Lire le cours en ligne : https://liouai-digital-education.github.io/algebre-lineaire-cbm/**

Ici, **Python fait le calcul ; vous faites tout le reste** : formuler le problème, choisir les concepts et les outils, critiquer le résultat, le généraliser et l'expliquer. Chaque notion part d'un problème réel et suit le processus en 4 étapes du référentiel *Computer-Based Maths* : **définir, abstraire, calculer, interpréter**. Le calcul à la main reste présent, sur de petites tailles, pour construire l'intuition.

[![Licence : CC BY-NC 4.0](https://img.shields.io/badge/licence-CC%20BY--NC%204.0-28B78D)](LICENSE)

## Le parcours

Neuf modules et trois projets intégrateurs, soit environ 70 heures de travail, en 52 notebooks Jupyter.

| Module | Question de départ | Durée | Prérequis |
|---|---|---|---|
| M0 — Python et NumPy comme outils | Comment faire calculer une machine ? | 6 h | — |
| M1 — Vecteurs et ressemblance | Comment mesurer la ressemblance ? | 7 h | M0 |
| M2 — Systèmes linéaires | Comment résoudre plusieurs contraintes à la fois ? | 9 h | M1 |
| M3 — Matrices et transformations | Comment déformer une image ? | 8 h | M2 |
| M4 — Inverse, déterminant, rang | Quand peut-on revenir en arrière ? | 8 h | M2 |
| M5 — Espaces vectoriels et bases | Quelle information est redondante ? | 8 h | M4 |
| M6 — Orthogonalité et moindres carrés | Quelle droite résume le mieux des données imparfaites ? | 9 h | M5 |
| M7 — Valeurs propres et dynamique | Où va un système à long terme ? | 9 h | M5 |
| M8 — Décomposition en valeurs singulières et données | Comment garder l'essentiel d'une donnée ? | 8 h | M6 |

Chaque module comprend des activités guidées et un mini-projet. Puis un **projet intégrateur** au choix (10 à 15 h, en quatre étapes) part d'une question ouverte et va jusqu'au rapport et à la présentation :

| Projet | Question ouverte | Modules réinvestis |
|---|---|---|
| A — Recommandation de films | Quels films proposer à un spectateur qu'on connaît peu ? | M1, M5, M6, M8 |
| B — Influence dans un réseau social | Qui sont les membres les plus influents d'un réseau, et selon quel critère ? | M1, M4, M7 |
| C — Reconnaître des chiffres manuscrits | Peut-on reconnaître un chiffre écrit à la main sans réseau de neurones ? | M1, M5, M6, M8 |

Tous les notebooks suivent le même gabarit : ① définir la question, ② estimer avant de calculer, ③ abstraire (schéma et calcul à la main), ④ calculer, ⑤ interpréter, ⑥ critiquer et généraliser, puis un exercice, son corrigé replié et un **bilan** qui alimente le profil de compétences de l'apprenant (11 dimensions du référentiel).

## État d'avancement

| Partie | État |
|---|---|
| Site, guides, référentiel encodé, charte Liouaï | prêts |
| Modules M0 à M8 (40 notebooks, mini-projets compris) | rédigés |
| Projets intégrateurs A, B et C (12 notebooks, modules Python corrigés et testés) | rédigés |
| Schémas TikZ (48) | compilés |
| Version anglaise | à traduire |

## Utiliser le cours

- **En ligne**, pour lire : https://liouai-digital-education.github.io/algebre-lineaire-cbm/
- **Sur votre ordinateur**, pour travailler les notebooks (recommandé) :

  ```bash
  git clone https://github.com/liouai-digital-education/algebre-lineaire-cbm.git
  cd algebre-lineaire-cbm
  pip install -r requirements.txt
  jupyter lab
  ```

  Commencez par `fr/M0-outils/`. Le guide d'installation détaillé est sur le site (Guide → Installation).

Vos bilans sont enregistrés dans `progression.json`, qui reste sur votre ordinateur (il est exclu du dépôt). `python scripts/radar.py` trace votre profil, et `python scripts/parcours.py --projet B` indique les modules à suivre avant un projet.

## Pour les contributeurs

### Organisation du dépôt

```
README.md, LICENSE        présentation du dépôt et licence (CC BY-NC 4.0)
GUIDE-PUBLICATION-GITHUB.md   publier le site sur GitHub Pages, pas à pas
myst.yml                  configuration du site (table des matières générée, logo, favicon, style)
assets/
  liouai.css              charte Liouaï appliquée au thème Jupyter Book (couleurs, Poppins/Roboto)
  liouai-mark*.svg        logo de l'en-tête (version claire et version mode sombre)
  favicon.svg             icône d'onglet
  liouai-digital-education.png   logo complet, affiché sur la page d'accueil
  schemas/                schémas compilés (SVG), générés à partir de schemas/*.tex
schemas/
  _preambule.tex          préambule TikZ commun : couleurs Liouaï, polices, bibliothèques
  schema-*.tex            un fichier par schéma (TikZ, circuitikz)
referentiel/
  cbm_codes.yaml          les 64 codes du référentiel, intitulés FR et EN
  parcours.yaml           modules, activités, prérequis : la source unique du parcours
fr/                       contenu en français (pages .md et notebooks .ipynb)
en/                       version anglaise (à venir)
scripts/
  cbm_nb.py               fonctions communes
  generer_squelettes.py   crée les pages et notebooks manquants, régénère la table des matières
                          et la pile du parcours de la page d'accueil
  corriger_ids.py         rend uniques les identifiants de cellules (à lancer après une modification hors Jupyter)
  compiler_schemas.py     compile les schémas TikZ en SVG (pdflatex + pdftocairo, dvisvgm ou Inkscape)
  couverture.py           matrice codes × modules à partir des métadonnées des notebooks
  parcours.py             propose un parcours personnalisé à partir de progression.json
  radar.py                trace le profil des 11 dimensions
tests/                    vérifie la structure et exécute les notebooks rédigés
fr/projets/X-.../         un dossier par projet intégrateur : notebooks, module commun, données,
                          corrige/ (module de référence et ses tests)
.github/workflows/        publication automatique sur GitHub Pages (à créer : voir GUIDE-PUBLICATION-GITHUB.md)
```

### Charte graphique

Les couleurs et typographies reprennent celles du site Liouaï : navy `#243743` pour le texte, vert `#28B78D` pour la marque, vert `#167A5C` pour les liens, gris `#A1A9AE`, jaune `#FFEE59` pour les mises en avant ; Poppins pour les titres, Roboto pour le texte.

- Le site : `assets/liouai.css`, déclaré dans `myst.yml` (`site.options.style`).
- Les graphiques : chaque notebook commence par une cellule « Style graphique Liouaï » (repliée sur le site) qui règle Matplotlib et fournit le dictionnaire `LIOUAI` et les dégradés `liouai` et `liouai_r`. Elle est ajoutée automatiquement aux nouveaux notebooks par `scripts/cbm_nb.py`.

### Formules et schémas

- **Formules** : en LaTeX dans les cellules Markdown, `$...$` dans le texte et `$$...$$` pour une formule centrée. Cette syntaxe est rendue à la fois par Jupyter (MathJax) et par Jupyter Book. Éviter la directive ```` ```{math} ````, que Jupyter n'affiche pas.
- **Schémas** : écrits en TikZ dans `schemas/schema-nom.tex`, compilés en `assets/schemas/schema-nom.svg` par `python scripts/compiler_schemas.py`, qui les agrandit d'un facteur 1,6 pour l'affichage web. Dans un notebook de `fr/Mx-.../`, on les insère avec `![description](../../assets/schemas/schema-nom.svg)`. Les SVG compilés sont versionnés : il n'est pas nécessaire d'avoir LaTeX pour construire le site, seulement pour modifier un schéma.
- Les graphiques calculés à partir de données (courbes, cartes de chaleur) restent produits par Matplotlib dans les cellules de code.

### Ajouter ou modifier une activité

1. Déclarez-la dans `referentiel/parcours.yaml` (identifiant, fichier, titre, résumé, codes).
2. Lancez `python scripts/generer_squelettes.py` : le notebook squelette est créé avec ses métadonnées, la table des matières et la carte du parcours sont mises à jour. Les fichiers existants ne sont jamais écrasés.
3. Rédigez le notebook en suivant le gabarit, puis passez son statut à `rédigé` dans `parcours.yaml`.
4. Lancez `python scripts/couverture.py` pour vérifier l'équilibre des codes, et `pytest` pour vérifier que tout s'exécute.

### Commandes utiles

```bash
pip install -r requirements.txt
python scripts/generer_squelettes.py
python scripts/couverture.py
python scripts/parcours.py --projet B
python scripts/radar.py
pytest
jupyter book start
```

## Licence

© 2026 Liouaï Digital Education. Sauf mention contraire, le contenu de ce dépôt (textes, notebooks, schémas, code et données simulées) est publié sous licence **[Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.fr)**. Le texte complet figure dans le fichier [LICENSE](LICENSE).

Vous pouvez **partager** et **adapter** ce cours, par exemple l'utiliser en classe, le traduire ou le modifier, à deux conditions :

- **Attribution** : citez la source, indiquez la licence et signalez vos modifications. Par exemple : *« Algèbre linéaire — penser, calculer, interpréter », Liouaï Digital Education, CC BY-NC 4.0*, avec le lien du dépôt.
- **Pas d'utilisation commerciale** : pas de vente du cours ni d'usage principalement destiné à un avantage commercial. Pour un usage commercial, contactez Liouaï Digital Education.

Ne sont pas couverts par cette licence, ou restent soumis à leurs propres conditions :

- le nom et les logos **Liouaï** (`assets/liouai-*`, `assets/favicon.svg`) ;
- le **référentiel de compétences**, traduction adaptée de *Required Outcomes from Core Computational Thinking* (projet Computer-Based Maths, CC BY-NC 4.0) ;
- les **données réelles** : CO₂ de Mauna Loa (NOAA, domaine public), chiffres manuscrits (UCI, CC BY 4.0), réseaux de Zachary, Padgett et Ansell, et Knuth (publications scientifiques, via networkx). Les notes MovieLens ne sont pas distribuées : elles sont téléchargées par l'apprenant.
