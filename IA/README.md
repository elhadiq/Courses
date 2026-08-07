# Intelligence artificielle — manuel complet

Introduction générale + 14 chapitres de cours HTML, 14 annexes algorithmiques sans code,
50 exercices Python auto-notés et 65 questions de compréhension.

> Ce fichier est destiné à l'enseignant. Il ne fait pas partie du contenu vu par les étudiants.

## Arborescence

```
IA/
├── index.html                    page d'accueil (sommaire des 14 chapitres)
├── assets/                       thème partagé (style.css, theme.js, favicon.svg)
├── lecons/
│   ├── 00-introduction/          page.html
│   ├── 01-qu-est-ce-que-l-ia/    page.html + algorithms.html
│   ├── 02-agents/                idem
│   ├── 03-recherche/             idem      (ancien chapitre 1)
│   ├── 04-metaheuristiques/      idem
│   ├── 05-jeux/                  idem      (ancien chapitre 2)
│   ├── 06-contraintes/           idem      (ancien chapitre 3)
│   ├── 07-logique/               idem
│   ├── 08-probabiliste/          idem
│   ├── 09-apprentissage/         idem      (ancien chapitre 4)
│   ├── 10-non-supervise/         idem
│   ├── 11-reseaux-neurones/      idem
│   ├── 12-renforcement/          idem
│   ├── 13-generative/            idem
│   └── 14-ethique/               idem
└── moodle/
    ├── 00-quiz-comprehension.xml       65 questions (types standards, aucun greffon)
    └── NN-<chapitre>-exercices.xml     14 fichiers, 50 exercices CodeRunner au total
```

## Sommaire

| Partie | Ch. | Sujet |
|--------|-----|-------|
| Ouverture | — | Introduction générale : boucle agent-environnement, carte du manuel, méthode de travail |
| I. Fondements | 1 | Qu'est-ce que l'IA ? Quatre définitions, jeu de l'imitation, chambre chinoise, hivers, symbolique contre connexionniste |
| | 2 | Agents rationnels : fonction d'agent, mesure de performance, six propriétés d'un environnement, cinq architectures, utilité espérée |
| II. Chercher | 3 | Recherche dans un espace d'états : largeur, profondeur, coût uniforme, A*, IDA* |
| | 4 | Métaheuristiques : montée stricte, redémarrages, recuit simulé, tabou, algorithmes génétiques |
| | 5 | Jeux à deux joueurs : min-max, alpha-bêta, évaluation, effet d'horizon, échantillonnage |
| | 6 | Contraintes : retour sur trace, MRV, AC-3, structure du graphe, réparation locale |
| III. Raisonner | 7 | Logique : modèles, conséquence, correction et complétude, résolution, DPLL, prédicats |
| | 8 | Probabilités : Bayes, indépendance conditionnelle, réseaux bayésiens, classifieur naïf, Markov |
| IV. Apprendre | 9 | Supervisé : risque empirique, kNN, régression, arbres, validation croisée |
| | 10 | Non supervisé : k-moyennes, silhouette, classification hiérarchique, composantes principales |
| | 11 | Réseaux de neurones : perceptron, OU exclusif, rétropropagation, approximation universelle, convolutions |
| | 12 | Renforcement : processus markovien, Bellman, itération sur les valeurs, Q-apprentissage |
| V. Aujourd'hui | 13 | Génératif : autorégressif, variationnel, adverse, diffusion, attention, transformeurs |
| | 14 | Éthique : sources de biais, théorème d'impossibilité, explicabilité, coût, régulation |

Chaque chapitre : 2 à 3 figures interactives, 1 à 2 images SVG, une analyse de correction,
terminaison et complexité, une synthèse et 8 à 13 références citées à leur source primaire.
Le manuel compte **49 figures SVG** et **29 planches interactives**.
**139 références au total, dont 101 avec DOI vérifié** et 38 avec lien permanent.

## Le code ne figure pas dans les chapitres

Les 15 pages de cours ne contiennent **aucun programme**. Les 30 algorithmes y sont donnés en
**pseudo-code mathématique**, au style des paquets LaTeX `algorithmic` et `algorithm2e` :

- encadré titré « Algorithme *N* — *nom* », avec un en-tête **Entrée / Sortie** ;
- lignes numérotées `1:`, `2:`, … et indentation par niveaux ;
- mots-clés en **gras romain** (`si`, `alors`, `tant que`, `pour tout`, `retourner`) ;
- variables en *italique mathématique*, noms de fonctions en romain droit ;
- flèche ← pour l'affectation, symboles réels ∅ ∪ ∈ ≠ ∞ ⌊⌋, formules composées par MathJax ;
- commentaires en fin de ligne après `//`, en italique grisé ;
- une note finale donnant l'invariant, le variant ou le théorème qui fonde l'algorithme.

13 chapitres sur 15 en comportent au moins un (les deux autres n'ont pas d'algorithme à
exposer).

Les 14 annexes `algorithms.html` vont plus loin : ni code, ni pseudo-code, ni notation. Chaque
procédure y est décrite en français — entrée, sortie, étapes numérotées, exemple déroulé à la
main en tableau, puis pourquoi c'est correct, pourquoi ça s'arrête, ce que ça coûte et où ça
se casse. Chaque annexe est de plus illustrée : une figure de synthèse pour treize d'entre
elles, **sept figures** pour celle du chapitre 3 — une par algorithme, plus un récapitulatif.

La programmation effective a lieu uniquement dans les exercices auto-notés.

## Mise en ligne des pages de cours

Les pages sont autonomes : déposer le dossier `IA/` sur un serveur web, ou ouvrir
`index.html` dans un navigateur. Deux bibliothèques sont chargées depuis un CDN (rendu des
formules et figures interactives) : une connexion réseau est nécessaire au premier affichage.
Pour un usage hors ligne, les télécharger dans `assets/` et remplacer les URL.

Pour intégrer une page dans une **Page Moodle**, copier le contenu de `<main>` dans l'éditeur
en mode HTML, et déposer `assets/style.css` dans les fichiers du cours.

## Import dans Moodle

1. Cours → **Banque de questions** → **Importer**
2. Format : **Format XML Moodle**
3. Déposer le fichier `.xml`, puis **Importer**

Importer d'abord `00-quiz-comprehension.xml` : il ne demande aucun greffon.

### Prérequis serveur

| Fichiers | Greffon | Bibliothèques Python côté Jobe |
|----------|---------|--------------------------------|
| `00-quiz-comprehension.xml` | aucun | aucune |
| chapitres 1, 2, 3, 4, 5, 6, 7, 8, 12, 14 | CodeRunner | bibliothèque standard |
| chapitres 10, 11, 13 | CodeRunner | **NumPy** |
| chapitre 9 | CodeRunner | **NumPy**, **scikit-learn** |

Test rapide du serveur : créer une question CodeRunner Python dont le test est
`import sklearn; print(sklearn.__version__)`. Si le module manque, seul l'exercice Q5 du
chapitre 9 est concerné.

### Réglages appliqués

`defaultgrade = 2`, `penaltyregime = 0`, `answerboxlines = 18`, code pré-rempli fourni pour
chaque exercice. 5 cas de test par question : 2 visibles comme exemples, 1 visible de
validation, 2 cachés (cas limites).

## Vérifications effectuées

- Les **30 pages HTML** passent **19 contrôles automatiques** : délimiteurs mathématiques,
  imbrication des balises, couleurs lisibles en thème sombre, citations vivantes, liens
  internes, présence des figures interactives et statiques, puis trois contrôles ajoutés
  après relecture :
  - **aucun débordement de texte** dans les 49 SVG — la largeur de chaque libellé est estimée
    caractère par caractère et comparée à celle de son cadre ; les légendes trop longues sont
    repliées automatiquement ;
  - **aucun chevauchement** entre deux textes d'une même figure — les boîtes englobantes sont
    calculées et croisées deux à deux ;
  - **aucune macro TeX inconnue de MathJax** — toute commande employée dans une zone
    mathématique est comparée aux paquets `base` et `ams`. La configuration définit en outre
    `\textsc`, `\nil`, `\vrai` et `\faux` comme filet de sécurité.
- Le code des **29 planches interactives** a été exécuté hors navigateur, chaque curseur
  balayé au minimum, au milieu et au maximum, chaque point déplaçable testé en cinq
  positions, **chaque gestionnaire de souris déclenché** (survol, sortie, clic) : aucune
  valeur indéfinie, aucune exception.
- Les **50 réponses modèles** ont été exécutées et les **252 sorties attendues** capturées à
  l'exécution, jamais écrites à la main.
- Les chiffres des légendes et des tableaux déroulés à la main ont été recalculés
  indépendamment : nœuds développés, feuilles élaguées, entropies, valeurs de Bayes, gradients,
  inerties, précision par groupe.
- Les DOI ont été recherchés sur le web avant d'être écrits ; les références sans DOI
  vérifiable reçoivent un lien permanent (éditeur, dépôt institutionnel, archive).

## Honnêteté du contenu

Plusieurs figures montrent des résultats **contre-intuitifs et non flatteurs**, parce qu'ils
sont ce que les données disent :

- ch. 4 : la montée avec redémarrages aléatoires bat largement le recuit simulé sur ce
  paysage à une dimension (38 succès sur 40 contre 18) ;
- ch. 2 : l'agent à utilité myope termine *derrière* l'agent à but, alors qu'il applique
  pourtant une règle de rentabilité correcte ;
- ch. 7 : la transition de phase mesurée sur 18 variables apparaît décalée par rapport au
  seuil asymptotique de 4,27, et la légende le dit ;
- ch. 12 : l'agent qui n'explore pas obtient le meilleur gain moyen et la plus mauvaise
  politique.
