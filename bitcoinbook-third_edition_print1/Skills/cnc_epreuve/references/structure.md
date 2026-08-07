# Plan type d'une épreuve CNC Informatique MP (difficulté croissante)

Cinq parties « largement indépendantes ». Chaque partie mêle : écrire une fonction Python,
prouver sa correction/terminaison, analyser sa complexité, démontrer une propriété.

## Partie I — Préliminaires (facile)
Fonctions arithmétiques simples. Objectifs pédagogiques : mise en jambe, manipulation
d'entiers, décalages binaires `>>`, sommes finies.
- Écrire des fonctions courtes.
- Prouver qu'une somme infinie n'a qu'un nombre fini de termes non nuls (complexité $O(1)$).
- Majorer une somme par une **série géométrique** et en déduire une borne.

## Partie II — Encodage / représentation (facile→moyen)
Représentation d'un entier en base $b$ ; encodage à longueur variable.
- Écrire `encode` et `decode`.
- **Nombre de tours** d'une boucle = $\lfloor\log_b n\rfloor+1$ ; en déduire la complexité.
- **Terminaison** : exhiber un *variant de boucle* (entier positif strictement décroissant).
- **Correction** : prouver `decode(encode(n)) == n` par disjonction de cas.

## Partie III — Structures récursives (moyen→difficile)
Arbres, hachage, arbres de Merkle, ou similaires.
- Construire une structure, gérer les cas limites (nombre impair d'éléments…).
- **Complexité** : $O(n)$ appels, prouvée par sommation des tailles de niveaux.
- **Preuve par récurrence** sur la hauteur / la longueur d'une preuve d'inclusion, sous une
  hypothèse (ex. résistance aux collisions d'une fonction de hachage).
- Taille d'un certificat en $O(\log n)$ et interprétation.

## Partie IV — Probabilités / processus aléatoire (difficile)
Modéliser un algorithme probabiliste (ex. recherche par essais indépendants).
- Justifier la probabilité de succès d'un essai.
- Reconnaître une **loi géométrique**, donner $\mathbb{E}[N]=1/p$.
- **Terminaison presque sûre** : $(1-p)^k \to 0$.
- Éventuellement un décodage compact + un réajustement avec **encadrement prouvé**.

## Partie V — Programmation dynamique (le plus difficile)
Problème d'optimisation sur sous-ensembles (type sac à dos / rendu de monnaie / sélection).
- **Situer** le problème de décision (ex. Subset-Sum) dans **NP-complet** (identification).
- Donner une **récurrence** sur les objets traités un par un ; préciser l'initialisation.
- Écrire la DP (attention au **sens de parcours** pour ne pas réutiliser un objet).
- **Complexité** $O(nC)$ temps, $O(C)$ espace ; expliquer « **pseudo-polynomial** ».
- **Correction** : prouver l'**invariant** par récurrence sur le nombre d'objets traités.
- **Terminaison** : boucles `for` finies.

## Rappels de rédaction
- Toujours écrire le code Python complet dans le corrigé.
- Distinguer clairement : *variant* (terminaison) vs *invariant* (correction).
- Terminer les démonstrations par $\square$.
- Vérifier numériquement en Python AVANT de figer les valeurs dans le sujet.
