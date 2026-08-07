---
name: cnc_epreuve
description: >
  Crée une épreuve type Concours National Commun (CNC) Informatique filière MP/PSI (Maroc) à partir d'un thème ou d'exercices, en français, en deux fichiers LaTeX compilables : un énoncé (problème constructif à parties de difficulté croissante) et un corrigé détaillé. Chaque partie enchaîne écriture de fonctions Python, analyses de complexité, preuves de correction et de terminaison (variant et invariant de boucle), et démonstrations (séries, probabilités, programmation dynamique, NP-complétude). Utiliser dès que l'utilisateur demande une épreuve CNC, un problème type concours, un sujet d'informatique MP/PSI, un .tex énoncé et corrigé, un problème à difficulté progressive, ou de transformer des exercices ou un cours en sujet de concours. Applique la mise en page CNC : page de titre, auteur cliquable ORCID, lien et droits cpgeacademy.org, encadré initiative personnelle. Vérifie toujours la compilation pdflatex et l'exécution du code Python.
---

# cnc_epreuve — Épreuve CNC Informatique MP (énoncé + corrigé LaTeX)

Produit `<slug>_enonce.tex` et `<slug>_corrige.tex`, tous deux compilables, dans le style
d'une épreuve d'informatique du Concours National Commun marocain (filière MP/PSI).

## Cadrage (AskUserQuestion si besoin)
Thème du problème ; langage (Python par défaut, programme CPGE marocain) ; nombre de parties
(4–5) ; auteur (défaut : Pr Agrégé El Hadiq Zouhair, ORCID 0000-0002-6108-7176) ; branding
(défaut : cpgeacademy.org).

## Structure imposée (difficulté CROISSANTE)
1. **Préambule** : utiliser tel quel `assets/preamble.tex` (hyperref, listings Python,
   titlesec, repli babel FR, macro `\Q` à numérotation continue, page de titre CNC avec
   auteur/liens/avis). Personnaliser titre, auteur, thème.
2. **Présentation et notations** : notations mathématiques et conventions Python communes.
3. **Parties I → V**, de la plus simple à la plus difficile. Progression type
   (voir `references/structure.md`) :
   - I. Préliminaires arithmétiques (fonctions simples, décalages, séries géométriques).
   - II. Encodage / représentation (base b, variant de boucle, réciprocité encode/decode).
   - III. Structures récursives (arbres, hachage, complexité $O(n)$, preuve par récurrence).
   - IV. Probabilités / processus (loi géométrique, espérance, terminaison presque sûre).
   - V. Programmation dynamique (récurrence, invariant, complexité pseudo-polynomiale,
        situer un problème dans NP).
4. Numéroter les questions en continu avec `\Q` (une seule série sur tout le sujet).
5. Parties « largement indépendantes ». Barème implicite par montée en difficulté.

## Exigences pédagogiques (style CNC)
- Chaque fonction demandée est **écrite en Python 3** dans le corrigé (bloc `lstlisting`).
- Analyser systématiquement : **complexité** (temps/espace), **terminaison** (variant),
  **correction** (invariant, récurrence). Rédiger de vraies **démonstrations** ($\square$).
- Réutilisation autorisée des fonctions des questions précédentes.
- Mentionner les bornes exactes (ex. encadrements) et les prouver.

## Vérification (impérative)
1. `bash scripts/verify.sh <slug>` → compile les deux `.tex` en 2 passes pdflatex ;
   échoue proprement en affichant les erreurs `!`.
2. **Exécuter en Python** toutes les fonctions du corrigé et vérifier les valeurs annoncées
   (sorties, encadrements). Pour la programmation dynamique, comparer à une recherche
   exhaustive (`itertools`) sur des cas aléatoires. Ne coller dans le sujet que des valeurs
   RÉELLEMENT calculées (surtout condensats/hachages).
3. Le préambule charge babel FR si disponible, sinon repli anglais → compile partout.

## Livraison
Fournir les `.tex` ET les `.pdf` compilés via `present_files`.

## Fichiers fournis
- `assets/preamble.tex` — préambule + page de titre CNC complète (auteur, liens, avis).
- `references/structure.md` — plan détaillé des 5 parties et types de questions/preuves.
- `scripts/verify.sh` — compilation pdflatex (2 passes) des deux fichiers.
