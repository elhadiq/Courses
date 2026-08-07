#!/usr/bin/env bash
# Compile l'énoncé et le corrigé d'une épreuve CNC (2 passes pdflatex chacun).
# Usage : bash verify.sh <slug>       (attend <slug>_enonce.tex et <slug>_corrige.tex)
set -u
slug="${1:?Usage: verify.sh <slug>}"
ok=1
for part in enonce corrige; do
  f="${slug}_${part}"
  if [ ! -f "$f.tex" ]; then echo "manquant: $f.tex"; ok=0; continue; fi
  pdflatex -interaction=nonstopmode -halt-on-error "$f.tex" >"/tmp/$f.log" 2>&1
  pdflatex -interaction=nonstopmode -halt-on-error "$f.tex" >"/tmp/$f.log" 2>&1
  if [ -f "$f.pdf" ]; then
    pages=$(pdfinfo "$f.pdf" 2>/dev/null | awk '/Pages/{print $2}')
    echo "OK  $f.pdf  (${pages} pages)"
  else
    echo "ÉCHEC $f :"
    grep -iE '^!' "/tmp/$f.log" | head -8
    ok=0
  fi
done
[ "$ok" = 1 ] && echo "== Compilation réussie ==" || { echo "== Des erreurs subsistent =="; exit 1; }
echo "Rappel : exécuter aussi le code Python du corrigé pour valider les valeurs annoncées."
