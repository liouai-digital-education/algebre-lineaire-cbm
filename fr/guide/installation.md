# Installation

Vous avez deux façons de travailler.

## Sans rien installer : JupyterLite

Les notebooks peuvent s'exécuter directement dans le navigateur avec [JupyterLite](https://jupyterlite.readthedocs.io). NumPy, Matplotlib et pandas y sont disponibles.

Limite : les fichiers que vous modifiez restent dans le stockage de votre navigateur. Téléchargez régulièrement vos notebooks et votre `progression.json`.

## Sur votre ordinateur

Il faut Python 3.10 ou plus récent.

```bash
git clone <adresse-du-depot> algebre-lineaire-cbm
cd algebre-lineaire-cbm
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Ouvrez ensuite `fr/M0-outils/0.1-faire-calculer.ipynb`.

## Construire le site

Le site est produit par [Jupyter Book](https://jupyterbook.org) à partir des notebooks et des pages Markdown :

```bash
jupyter book start               # aperçu local avec rechargement
jupyter book build --html        # site statique dans _build/html
```

Les notebooks ne sont pas exécutés à la construction : le site montre les énoncés, et c'est à vous de les exécuter.

:::{warning} Dossier synchronisé (Google Drive, OneDrive, Dropbox)
Au premier lancement, Jupyter Book télécharge un thème et installe ses dépendances Node.js dans `_build/templates`, soit des milliers de petits fichiers. Dans un dossier synchronisé, cette installation échoue souvent ; on obtient alors une erreur `Cannot find module 'express'`. Travaillez plutôt dans un dossier local, par exemple `C:\Projets\algebre-lineaire-cbm`, et utilisez Git ou une copie pour la sauvegarde.
:::
