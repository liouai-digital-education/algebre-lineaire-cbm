# Publier le parcours sur GitHub et le rendre visible depuis liouai-digital-education.github.io

Ce guide explique pas à pas comment :

1. **héberger** le projet `algebre-lineaire-cbm` sur GitHub, dans l'organisation **liouai-digital-education** ;
2. **publier** le site Jupyter Book automatiquement avec GitHub Pages, à l'adresse
   **https://liouai-digital-education.github.io/algebre-lineaire-cbm/** ;
3. **le faire connaître** depuis le site vitrine **https://liouai-digital-education.github.io**.

Comptez environ une heure la première fois. Ensuite, chaque mise à jour du cours se publie seule, en quelques minutes, après un simple envoi des modifications.

---

## Vue d'ensemble

```
Votre ordinateur                 GitHub                               Le web
─────────────────                ───────────────────────────          ─────────────────────────────────────────────
dossier                 envoi    dépôt                       build    site du cours
algebre-lineaire-cbm  ───────►   liouai-digital-education/  ───────►  liouai-digital-education.github.io/
                      (push)     algebre-lineaire-cbm        (Action) algebre-lineaire-cbm/
                                                                                ▲
                                 dépôt                                          │ lien
                                 liouai-digital-education/  ───────►  site vitrine
                                 liouai-digital-education.github.io   liouai-digital-education.github.io
```

Deux dépôts, deux sites :

| Dépôt | Rôle | Adresse publiée |
|---|---|---|
| `liouai-digital-education.github.io` (existe déjà) | le site vitrine de Liouaï | `https://liouai-digital-education.github.io` |
| `algebre-lineaire-cbm` (à créer) | le cours d'algèbre linéaire | `https://liouai-digital-education.github.io/algebre-lineaire-cbm/` |

Le nom du dépôt du cours devient la fin de son adresse. Choisissez-le une fois pour toutes : le changer plus tard casse les liens déjà partagés.

---

## Étape 0 — Ce qu'il vous faut

- Un compte GitHub **propriétaire** (owner) de l'organisation `liouai-digital-education`, ou au moins autorisé à y créer des dépôts.
- **Git** installé sur votre ordinateur. Le plus simple sous Windows : installer **GitHub Desktop** (https://desktop.github.com), qui contient Git et évite la ligne de commande. Ce guide donne les deux façons de faire.
- Le dossier du projet, par exemple `Bureau\algebre-lineaire-cbm\algebre-lineaire-cbm-v0.2`.

> **À propos de OneDrive.** Le projet se trouve sur votre Bureau synchronisé par OneDrive. Git fonctionne dans un dossier OneDrive, mais la synchronisation peut gêner Git (fichiers verrouillés, conflits dans le dossier caché `.git`). Si vous rencontrez des erreurs étranges, copiez le projet dans un dossier non synchronisé, par exemple `C:\Users\bohne\Projets\algebre-lineaire-cbm`, et travaillez désormais depuis cette copie.

---

## Étape 1 — Préparer le dossier avant le premier envoi

Tout ce qui est dans le dossier sera public. Vérifiez ces quatre points.

**1.1 Les fichiers exclus.** Le fichier `.gitignore` du projet exclut déjà :

- `_build/` : le site généré et le cache du thème (lourd, et reconstruit automatiquement par GitHub) ;
- `progression.json` et `profil.png` : les données personnelles de l'apprenant ;
- `.ipynb_checkpoints/`, `__pycache__/`, `.venv/`.

Vous pouvez supprimer le dossier `_build/apercu-claude`, qui ne sert plus. De toute façon, il n'est pas envoyé.

**1.2 Les données.** Seules des données libres de diffusion sont dans le dépôt :

- jeux réels publics : CO₂ de Mauna Loa (NOAA), réseaux de Zachary, de Padgett et des *Misérables*, chiffres manuscrits UCI (CC BY 4.0) ;
- jeux simulés (films du projet A).

Les notes MovieLens ne sont **pas** dans le dépôt : `films.py` les télécharge chez l'apprenant, et le dossier correspondant est exclu.

**1.3 Une licence.** Sans licence, personne n'a légalement le droit de réutiliser le cours. Le référentiel CBM est sous **CC BY-NC 4.0**, et le cours en est une adaptation. Il est donc cohérent de publier :

- le **contenu** (textes, notebooks, schémas) sous **CC BY-NC-SA 4.0** ou **CC BY-NC 4.0** ;
- le **code** (scripts, modules Python) sous une licence logicielle, par exemple **MIT**.

Créez un fichier `LICENSE` à la racine du projet, qui le dit en quelques lignes. GitHub propose des modèles quand on crée le fichier depuis son site.

**1.4 Le README.** Le `README.md` est la vitrine du dépôt sur GitHub. Le tableau « État d'avancement » qu'il contient date du début du projet et annonce encore « squelettes à rédiger ». Mettez-le à jour (les 9 modules et les 3 projets sont rédigés) et ajoutez en tête le lien vers le site publié :

> **Lire le cours en ligne : https://liouai-digital-education.github.io/algebre-lineaire-cbm/**

---

## Étape 2 — Créer le dépôt sur GitHub

1. Connectez-vous sur https://github.com et ouvrez l'organisation : https://github.com/liouai-digital-education.
2. Cliquez sur **New repository** (ou **Repositories → New**).
3. Remplissez :
   - **Owner** : `liouai-digital-education` (et pas votre compte personnel) ;
   - **Repository name** : `algebre-lineaire-cbm` ;
   - **Description** : *Algèbre linéaire — penser, calculer, interpréter. Un parcours Computer-Based Maths avec Python.* ;
   - **Public** (GitHub Pages gratuit ne publie que les dépôts publics d'une organisation gratuite) ;
   - **ne cochez rien** dans « Initialize this repository with » : pas de README, pas de .gitignore, pas de licence. Le projet a déjà les siens, et un dépôt vide évite un conflit au premier envoi.
4. Cliquez sur **Create repository**. GitHub affiche une page avec l'adresse du dépôt : `https://github.com/liouai-digital-education/algebre-lineaire-cbm.git`.

---

## Étape 3 — Envoyer le projet sur GitHub

### Avec GitHub Desktop (recommandé si vous n'utilisez pas la ligne de commande)

1. Ouvrez GitHub Desktop et connectez votre compte (**File → Options → Accounts**).
2. **File → Add local repository…**, choisissez le dossier du projet.
3. GitHub Desktop signale que ce dossier n'est pas encore un dépôt Git : cliquez sur **create a repository**. Gardez le nom `algebre-lineaire-cbm`, et ne choisissez **ni** `.gitignore` **ni** licence (le projet a déjà son `.gitignore`). Validez.
4. Dans la colonne de gauche apparaît la liste des fichiers. Vérifiez qu'aucun fichier de `_build/` ni `progression.json` n'y figure.
5. En bas à gauche, écrivez un résumé, par exemple *Première publication du parcours*, puis cliquez sur **Commit to main**.
6. Cliquez sur **Publish repository**. Dans la fenêtre :
   - **décochez** « Keep this code private » ;
   - dans **Organization**, choisissez `liouai-digital-education`.

   Si GitHub Desktop indique que le dépôt existe déjà (vous l'avez créé à l'étape 2), utilisez plutôt **Repository → Repository settings → Remote** et collez l'adresse `https://github.com/liouai-digital-education/algebre-lineaire-cbm.git`, puis **Push origin**.

### Avec la ligne de commande

Ouvrez un terminal (PowerShell ou Git Bash) **dans le dossier du projet**, puis tapez une ligne après l'autre :

```bash
git init -b main
git add .
git status            # vérifiez la liste : pas de _build/, pas de progression.json
git commit -m "Première publication du parcours"
git remote add origin https://github.com/liouai-digital-education/algebre-lineaire-cbm.git
git push -u origin main
```

Au premier `push`, une fenêtre de connexion GitHub s'ouvre. Connectez-vous dans le navigateur.

**Vérification.** Rechargez la page https://github.com/liouai-digital-education/algebre-lineaire-cbm : les dossiers `fr`, `assets`, `schemas`, `scripts`… et le README s'affichent.

---

## Étape 4 — Ajouter la publication automatique (GitHub Actions)

Le site n'est pas construit sur votre ordinateur puis envoyé. C'est GitHub qui le reconstruit à chaque envoi, grâce à un fichier de « workflow » placé dans `.github/workflows/`.

### 4.1 Créer le fichier

**Option A — avec Jupyter Book.** Si Jupyter Book est installé sur votre ordinateur, ouvrez un terminal dans le dossier du projet et tapez :

```bash
jupyter book init --gh-pages
```

Répondez `main` pour la branche et `deploy.yml` pour le nom du fichier. La commande crée `.github/workflows/deploy.yml`.

**Option B — à la main.** Créez le dossier `.github` (avec le point), puis dedans le dossier `workflows`, puis dedans le fichier `deploy.yml` avec ce contenu :

```yaml
name: Publication du site (GitHub Pages)

on:
  push:
    branches: [main]        # chaque envoi sur main republie le site
  workflow_dispatch:        # permet aussi de relancer à la main depuis l'onglet Actions

env:
  # Adresse de base du site : le nom du dépôt, ici /algebre-lineaire-cbm
  BASE_URL: /${{ github.event.repository.name }}

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Préparer GitHub Pages
        uses: actions/configure-pages@v5
      - uses: actions/setup-node@v4
        with:
          node-version: 22.x
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Installer Jupyter Book
        run: pip install "jupyter-book>=2"
      - name: Construire le site
        run: jupyter book build --html
      - name: Déposer le site construit
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./_build/html
      - name: Publier sur GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

> **Pourquoi `BASE_URL` ?** Le cours n'est pas à la racine du domaine, mais dans le sous-dossier `/algebre-lineaire-cbm/`. Sans cette ligne, le site s'affiche sans style, ni images, ni menu.

### 4.2 Activer GitHub Pages

1. Sur la page du dépôt, ouvrez **Settings → Pages**.
2. Dans **Build and deployment → Source**, choisissez **GitHub Actions** (et non « Deploy from a branch »).

### 4.3 Envoyer le workflow

Envoyez le nouveau fichier comme à l'étape 3 : dans GitHub Desktop, **Commit to main** puis **Push origin**. En ligne de commande :

```bash
git add .github/workflows/deploy.yml
git commit -m "Publication automatique avec GitHub Pages"
git push
```

### 4.4 Suivre la construction

1. Ouvrez l'onglet **Actions** du dépôt. Une exécution « Publication du site » démarre. Comptez 2 à 5 minutes.
2. Une coche verte ✓ indique le succès. En cliquant dessus, l'étape **deploy** affiche l'adresse du site.
3. Ouvrez **https://liouai-digital-education.github.io/algebre-lineaire-cbm/** et vérifiez :
   - le logo, les couleurs Liouaï et la pile du parcours sur l'accueil ;
   - un notebook avec un schéma, par exemple M6 → 6.2 ;
   - les liens entre pages, la recherche (Ctrl + K) et le mode sombre.

Une croix rouge ✗ signale un échec. Voir la section **Dépannage** en fin de guide.

---

## Étape 5 — Soigner la présentation du dépôt

Ces réglages prennent cinq minutes et rendent le cours trouvable sur GitHub.

1. **Le lien vers le site.** Sur la page d'accueil du dépôt, cliquez sur l'engrenage ⚙ à côté de **About**. Cochez **Use your GitHub Pages website**, ce qui remplit automatiquement l'adresse du site.
2. **Les sujets (topics).** Dans la même fenêtre, ajoutez des mots-clés : `linear-algebra`, `algebre-lineaire`, `jupyter-book`, `python`, `numpy`, `computer-based-maths`, `education`, `french`. Ils servent à la recherche sur GitHub.
3. **Épingler le dépôt.** Sur la page de l'organisation, **Customize pins**, puis cochez `algebre-lineaire-cbm`. Le cours apparaît alors en tête du profil Liouaï.
4. **Le lien GitHub dans le site.** Pour afficher un lien vers le dépôt dans l'en-tête du cours, ajoutez dans `myst.yml`, section `project:`, la ligne :

   ```yaml
   github: https://github.com/liouai-digital-education/algebre-lineaire-cbm
   ```

5. **Le retour vers le site vitrine.** Pour qu'un visiteur du cours puisse revenir à Liouaï, ajoutez dans `myst.yml`, section `site:` (au même niveau que `options:`), un lien de navigation :

   ```yaml
   nav:
     - title: Liouaï Digital Education
       url: https://liouai-digital-education.github.io
   ```

   Vous pouvez aussi faire pointer le logo vers le site vitrine, avec `logo_url: https://liouai-digital-education.github.io` dans `site.options`.

Envoyez ces modifications : le site se republie seul.

---

## Étape 6 — Donner de la visibilité au cours sur liouai-digital-education.github.io

Le site vitrine est un autre dépôt, `liouai-digital-education/liouai-digital-education.github.io`. C'est une page unique, avec une section **Projets** (ancre `#projets`) et des appels à l'action, dont « Voir les projets ».

### 6.1 Ajouter le cours dans la section « Projets »

1. Ouvrez le dépôt https://github.com/liouai-digital-education/liouai-digital-education.github.io.
2. Ouvrez le fichier de la page d'accueil (en général `index.html`), puis cliquez sur le crayon ✎ pour le modifier directement dans le navigateur.
3. Repérez la section dont l'identifiant est `projets` : cherchez `id="projets"` avec **Ctrl + F**.
4. Ajoutez-y une « fiche » pour le cours. Si la section contient déjà des fiches, **copiez-en une** et remplacez son contenu. Sinon, prévoyez ces éléments :

   | Élément | Contenu proposé |
   |---|---|
   | Titre | Algèbre linéaire — penser, calculer, interpréter |
   | Accroche | Un parcours *Computer-Based Maths* : Python fait le calcul, vous faites tout le reste. |
   | Détails | 9 modules · 3 projets intégrateurs · environ 70 h · notebooks Jupyter |
   | Pour qui | Reconversion, étudiants, professionnels : bases de Python suffisantes |
   | Bouton principal | **Commencer le parcours** → `https://liouai-digital-education.github.io/algebre-lineaire-cbm/` |
   | Lien secondaire | **Voir le code** → `https://github.com/liouai-digital-education/algebre-lineaire-cbm` |
   | Image | le schéma des étapes d'un projet, ou une capture de la page d'accueil du cours |

5. En bas de la page, écrivez un message comme *Ajout du cours d'algèbre linéaire*, puis cliquez sur **Commit changes**. Le site vitrine se met à jour en une à deux minutes.

> **Pour l'image.** Faites une capture de l'accueil du cours, enregistrez-la dans le dépôt du site vitrine (par exemple `images/algebre-lineaire.png`, via **Add file → Upload files**), puis référencez-la dans la fiche. Une image hébergée dans le même dépôt ne casse jamais.

### 6.2 Les autres points d'entrée du site vitrine

- **Le menu** : si le menu comporte « Contenus » ou « Projets », un lien direct vers le cours peut y figurer.
- **Le bouton « Voir les projets »** de l'en-tête mène déjà à `#projets`, donc vers la nouvelle fiche.
- **La version anglaise** : la page a un sélecteur FR/EN. Rédigez la fiche aussi en anglais, en précisant *course in French*, puisque le dossier `en/` du cours n'est pas encore traduit.
- **Le lien LinkedIn** « Me contacter sur LinkedIn » pointe encore vers `#`, une adresse provisoire. Profitez-en pour le remplacer par l'adresse de votre profil.

### 6.3 Au-delà du site vitrine

- **Le profil de l'organisation sur GitHub.** Créez dans l'organisation un dépôt public nommé `.github`, contenant un fichier `profile/README.md`. Ce texte s'affiche en tête de https://github.com/liouai-digital-education : présentez Liouaï en deux phrases et listez vos cours avec leurs liens.
- **Le référencement Google.** Les sites GitHub Pages sont indexés, mais cela peut prendre quelques semaines. Pour accélérer, déclarez les deux adresses dans **Google Search Console** (gratuit), en vérifiant la propriété par la méthode du fichier HTML.
- **Le partage.** Un post LinkedIn avec une capture de la pile du parcours, ou d'une figure frappante (les chiffres propres du projet C, la scission du club de karaté du projet B), et le lien du cours.

---

## Étape 7 — Mettre à jour le cours ensuite

Le cycle devient très court :

1. Modifiez le cours sur votre ordinateur : notebooks, pages, `parcours.yaml`… Si vous avez changé `parcours.yaml`, lancez `python scripts/generer_squelettes.py`. Si vous avez modifié un notebook hors de Jupyter, lancez `python scripts/corriger_ids.py`.
2. Vérifiez localement, si vous le souhaitez, avec `jupyter book start`.
3. Envoyez vos modifications : **Commit to main** puis **Push origin** dans GitHub Desktop, ou `git add .`, `git commit -m "…"` et `git push`.
4. Deux à cinq minutes plus tard, le site en ligne est à jour. L'onglet **Actions** en garde l'historique.

> **Conseil.** Pour un gros chantier, comme la version anglaise ou un nouveau module, travaillez sur une **branche** (`Current branch → New branch` dans GitHub Desktop). Le site public ne change que lorsque vous fusionnez la branche dans `main`.

---

## Étape 8 (facultative) — Publier les notebooks avec leurs résultats

Les notebooks sont enregistrés **sans** leurs sorties, ce qui est voulu : l'apprenant les exécute lui-même, après avoir fait ses paris. Le site en ligne montre donc le code, sans les figures produites par Python. Seuls les schémas TikZ sont visibles, puisqu'il s'agit d'images.

Pour montrer aussi les figures sur le site, demandez à GitHub d'exécuter les notebooks pendant la construction. Dans `deploy.yml`, remplacez les deux étapes « Installer Jupyter Book » et « Construire le site » par :

```yaml
      - name: Installer Jupyter Book et les bibliothèques du cours
        run: pip install -r requirements.txt
      - name: Construire le site en exécutant les notebooks
        run: jupyter book build --html --execute
```

Points d'attention :

- la construction prend plus de temps (comptez 10 à 20 minutes) ;
- une cellule qui produit volontairement une erreur fait échouer la construction, sauf si elle porte le tag `raises-exception`. C'est déjà le cas de la cellule concernée dans le notebook 0.3 sur les erreurs de forme. Si vous en ajoutez une autre, posez-lui ce tag dans Jupyter (**View → Cell toolbar → Tags**) ;
- les corrigés s'exécutent aussi : ils restent repliés grâce au tag `hide-cell`, mais un lecteur curieux peut les déplier. C'est un choix pédagogique à faire : figures visibles, ou découverte entièrement laissée à l'apprenant.

---

## Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| Le site s'affiche sans couleurs, sans logo, ou en texte brut | `BASE_URL` absent ou faux | Vérifiez la ligne `BASE_URL: /${{ github.event.repository.name }}` dans `deploy.yml`, et que le dépôt s'appelle bien `algebre-lineaire-cbm`. |
| Erreur 404 à l'adresse du site | Pages pas activé, ou source mal choisie | **Settings → Pages → Source : GitHub Actions**, puis relancez le workflow (**Actions → Publication du site → Run workflow**). |
| Croix rouge dans **Actions**, à l'étape « Construire le site » | Erreur dans une page : lien cassé, fichier de la table des matières introuvable | Ouvrez le journal de l'étape et cherchez les lignes `error`. Lancez `python -m pytest tests` sur votre ordinateur : le test de la table des matières repère les fichiers manquants. |
| Croix rouge à l'étape « Publier », message *permission* ou *environment* | Règles de l'organisation | **Organization → Settings → Actions → General** : autorisez les Actions. **Settings → Environments → github-pages** : autorisez la branche `main`. |
| Les schémas n'apparaissent pas | SVG non envoyés | Vérifiez que `assets/schemas/*.svg` est bien dans le dépôt : ces fichiers doivent être envoyés, ils ne sont pas recompilés par GitHub. |
| `git push` refusé (*rejected*, *fetch first*) | Le dépôt GitHub contient un fichier absent chez vous, par exemple un README créé à l'étape 2 | `git pull --rebase origin main`, puis `git push`. |
| Erreurs de verrouillage dans `.git` | Synchronisation OneDrive | Mettez OneDrive en pause pendant les envois, ou déplacez le projet hors de OneDrive (voir l'étape 0). |
| Le site vitrine ne montre pas la nouvelle fiche | Cache du navigateur, ou publication en cours | Attendez deux minutes, puis rechargez avec **Ctrl + F5**. Vérifiez l'onglet **Actions** du dépôt du site vitrine. |

---

## Récapitulatif

- [ ] Licence ajoutée, README mis à jour avec le lien du site
- [ ] Dépôt `liouai-digital-education/algebre-lineaire-cbm` créé, public et vide
- [ ] Projet envoyé, sans `_build/` ni `progression.json`
- [ ] `.github/workflows/deploy.yml` ajouté, avec `BASE_URL`
- [ ] **Settings → Pages → Source : GitHub Actions**
- [ ] Coche verte dans **Actions**, et site vérifié en ligne
- [ ] Section **About** : lien du site et topics ; dépôt épinglé sur l'organisation
- [ ] Liens croisés : `github`, `nav` et `logo_url` dans `myst.yml`
- [ ] Fiche du cours ajoutée dans la section **Projets** du site vitrine (FR et EN)
- [ ] Facultatif : profil de l'organisation (`.github/profile/README.md`), Google Search Console, annonce LinkedIn

---

### Références

- Jupyter Book, *Publish your book online* : https://jupyterbook.org/latest/get-started/publish
- MyST, *Deploy to GitHub Pages* (workflow et `BASE_URL`) : https://mystmd.org/guide/deployment-github-pages
- GitHub Docs, *Configuring a publishing source for your GitHub Pages site* : https://docs.github.com/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Desktop : https://desktop.github.com
