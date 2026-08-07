---
name: moodle_content_from_book
description: >
  Génère un cours Moodle complet à partir d'un livre (AsciiDoc .adoc, Markdown ou PDF). Pour chaque chapitre : une page de lecture resource.html pour débutant (objectifs, schémas SVG, figures du livre en base64, glossaire, auto-évaluation) ; une présentation presentation.html au thème CPGE (mode diaporama, navigation flèches et espace, images base64) ; des exercices exercises.xml Moodle CodeRunner Python auto-notés ; un quiz comprehension.xml en types standards (multichoice, truefalse, numerical, sans plugin). Utiliser dès que l'utilisateur veut créer un cours Moodle à partir d'un livre, transformer un livre en cours, faire des sections, présentations ou quizzes à partir de book.adoc, un cours type Mastering Bitcoin ou Mastering Ethereum, ou mentionne Moodle avec livre et chapitres. Chaque chapitre devient une section (sous-dossier) avec un index.html cliquable ; toutes les images sont embarquées en base64 pour s'afficher dans une Page Moodle.
---

# moodle_content_from_book — Livre → cours Moodle complet

Transforme un livre en cours Moodle : une **section par chapitre**, chaque section réunissant
une page de lecture, une présentation, des exercices CodeRunner et un quiz de compréhension.

## Principe de dossier

```
<Cours>/
  index.html                       (accueil cliquable : liens vers chaque section)
  section_01_<slug>/
    resource.html                  (leçon complète, images base64)
    presentation.html              (diaporama thème CPGE, images base64)
    exercises.xml                  (3 exercices CodeRunner Python)
    comprehension.xml              (5–7 questions QCM/VF/numériques)
  section_02_<slug>/ ...
```

## Workflow (à suivre dans l'ordre)

### 1. Cadrer avec l'utilisateur (AskUserQuestion)
Langue (EN/FR) ; périmètre (tous les chapitres ou un sous-ensemble) ; nombre d'exercices
CodeRunner par section (défaut 3) ; profondeur (leçon débutant complète recommandée).

### 2. Lire la source
- AsciiDoc : le fichier maître (souvent `book.adoc`) liste les `include::chNN_*.adoc`.
  Récupérer les titres via `grep '^== '` et les figures via `grep 'image::'`
  (le chemin est en général `images/<nom>.png`).
- Établir la table des sections (numéro, titre, slug, figures pertinentes).

### 3. Construire chaque section
- **resource.html** : suivre `references/lesson_template.html`. Écrire une VRAIE leçon pour
  débutant : bandeau titre, encadré « objectifs », explication progressive avec analogies
  et exemples chiffrés, tables, schémas **SVG** quand il n'y a pas de figure, figures du
  livre, glossaire, encadré « check your understanding », mini-note « Practice » décrivant
  les exercices (SANS jamais écrire « importer le XML / CodeRunner » — l'utilisateur sait).
- **presentation.html** : partir de `assets/presentation_template.html` (thème CPGE teal,
  cartes, tags, hl-box, table.ref, mode diaporama, navigation flèches/espace, blocage léger
  Ctrl+S/U/P/A/F12/impression/glisser — SANS bloquer le clic droit ni la sélection de texte).
- **exercises.xml** : format CodeRunner exact — voir `references/coderunner_question.xml`.
  Concevoir des exercices Python autonomes (bibliothèque standard uniquement) issus du
  chapitre. Réponse modèle + préchargement élève + 3–4 testcases (`display` = élément
  enfant, jamais attribut).
- **comprehension.xml** : helpers de `references/comprehension_helpers.md`
  (multichoice/truefalse/numerical). 5–7 questions par section.

### 4. Embarquer les images en base64 (OBLIGATOIRE)
Lancer `scripts/embed_images_base64.py <dossier_cours> <dossier_images>` : remplace tout
`src="../../images/x.png"` par `data:image/png;base64,...`. Sans cela les figures ne
s'affichent pas dans une Page Moodle.

### 5. index.html cliquable
Tableau des sections ; le nom de chaque section est un lien `href="section_XX_.../resource.html"`.

### 6. Vérifier (impératif)
- `python3 scripts/validate_coderunner.py <dossier_cours>` : exécute chaque réponse modèle
  et compare la sortie aux `expected` ; contrôle la structure XML CodeRunner. Doit finir
  « ALL PASS ».
- Pour les questions à hachage (SHA-256, Merkle…), calculer les sorties attendues en Python
  d'abord, puis les coller dans le XML (ne jamais deviner un condensat).
- Vérifier que `comprehension.xml` parse et que chaque question a une réponse à 100 %.
- Vérifier que 0 chemin `../../images` ne subsiste et que chaque section a un visuel.

## Règles de style (leçon)
- Prose claire, un concept nouveau expliqué avant d'être nommé, exemples chiffrés.
- Aucun « bullet-point-only » : de vraies phrases. Glossaire + auto-évaluation systématiques.
- Thème lecture : bandeau bleu marine `#16213e` + accent orange `#f7931a` (adaptable).

## Déploiement Moodle (à rappeler à l'utilisateur, pas à écrire dans les pages)
- `resource.html` → activité **Page** (coller via la vue source HTML `<>`).
- `presentation.html` → **Fichier** en affichage **Intégré** (le JS ne tourne pas dans une Page).
- `exercises.xml` → **Banque de questions ▸ Importer ▸ Moodle XML** (plugin CodeRunner).
- `comprehension.xml` → **Banque de questions ▸ Importer ▸ Moodle XML** (aucun plugin).

## Fichiers fournis
- `assets/presentation_template.html` — gabarit diaporama thème CPGE (nav + espace + blocage léger).
- `references/lesson_template.html` — squelette de page de lecture (sections attendues).
- `references/coderunner_question.xml` — schéma exact d'UNE question CodeRunner.
- `references/comprehension_helpers.md` — gabarits multichoice / truefalse / numerical.
- `scripts/embed_images_base64.py` — remplace les chemins d'images par des data URIs.
- `scripts/validate_coderunner.py` — exécute et valide tous les `exercises.xml`.
