# Évaluation et profil de compétences

L'évaluation porte sur les codes du [référentiel](referentiel.md), pas sur des notes par chapitre. Chaque code visé par un notebook reçoit un niveau de 0 à 3. L'ensemble forme un profil sur les 11 dimensions.

## Les quatre niveaux

| Niveau | Intitulé | Description | Exemple pour CVt (corroborer ses résultats) |
|---|---|---|---|
| 0 | Non observé | le code n'apparaît pas dans le travail | aucune vérification du résultat |
| 1 | Guidé | réussi quand la consigne indique quoi faire | vérifie avec la méthode suggérée par le notebook |
| 2 | Autonome | réussi sans consigne, dans un contexte proche du cours | choisit seul une seconde méthode de résolution |
| 3 | Transfert | réussi dans un contexte nouveau, avec justification | conçoit un test sur données indépendantes et explique pourquoi il est pertinent |

Soyez exigeant avec vous-même : si la consigne vous a dit quoi faire, c'est le niveau 1, même si vous avez réussi.

## Où sont enregistrés vos bilans ?

La dernière cellule de chaque notebook ajoute une entrée au fichier `progression.json`, à la racine du site. Ce fichier vous appartient : il ne quitte pas votre ordinateur.

## Votre profil

Depuis la racine du site, lancez :

```bash
python scripts/radar.py          # trace le profil radar des 11 dimensions (profil.png)
python scripts/parcours.py       # propose les prochaines activités
```

Le profil prend, pour chaque code, le meilleur niveau atteint sur ses 3 dernières occurrences. Le niveau d'une dimension est la moyenne de ses codes déjà évalués.

`parcours.py` propose deux échelles :

- **macro** : l'ordre des modules pour atteindre un projet intégrateur, en respectant les prérequis (`--projet B`) ;
- **micro** : dans le module en cours, les activités qui travaillent vos codes les plus faibles.
