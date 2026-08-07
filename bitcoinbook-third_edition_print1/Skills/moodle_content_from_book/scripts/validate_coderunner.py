#!/usr/bin/env python3
"""Valide tous les exercises.xml (CodeRunner Python) d'un dossier de cours :
   - structure XML CodeRunner (champs requis, display = élément enfant),
   - EXECUTE chaque réponse modèle sur chaque testcode et compare à <expected>.

Usage:
    python3 validate_coderunner.py <dossier_cours>

Sortie : « ALL PASS ✓ » ou la liste des problèmes.
"""
import glob, os, subprocess, sys, xml.etree.ElementTree as ET

REQUIRED_EMPTY = ['idnumber','globalextra','useace','resultcolumns','template',
    'iscombinatortemplate','allowmultiplestdins','testsplitterre','language','sandbox',
    'grader','uiplugin','uiparameters','prototypeextra']
REQUIRED_VAL = {'coderunnertype':'python3','penaltyregime':'0','extractcodefromjson':'1',
    'templateparamslang':'None','giveupallowed':'0','hoisttemplateparams':'1'}

def main():
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(1)
    base = sys.argv[1]
    files = sorted(glob.glob(os.path.join(base, "section_*", "exercises.xml")))
    if not files:
        print("Aucun exercises.xml trouvé sous", base); sys.exit(1)
    tq = ttc = 0; fails = []
    for f in files:
        sec = os.path.basename(os.path.dirname(f))
        try:
            root = ET.parse(f).getroot()
        except Exception as e:
            fails.append(f"{sec}: XML PARSE ERROR {e}"); continue
        for q in root.findall('question'):
            if q.get('type') != 'coderunner':
                continue
            tq += 1
            name = q.find('name/text').text
            ans = (q.find('answer').text or "")
            for tag in REQUIRED_EMPTY:
                if q.find(tag) is None:
                    fails.append(f"{sec}/{name}: <{tag}> manquant")
            for tag, val in REQUIRED_VAL.items():
                el = q.find(tag)
                if el is None or (el.text or '') != val:
                    fails.append(f"{sec}/{name}: <{tag}> attendu {val!r}")
            for i, tc in enumerate(q.findall('.//testcase'), 1):
                ttc += 1
                if 'display' in tc.attrib:
                    fails.append(f"{sec}/{name} tc{i}: display doit être un élément enfant")
                code = tc.find('testcode/text').text or ""
                exp = tc.find('expected/text').text or ""
                try:
                    r = subprocess.run([sys.executable, '-c', ans + "\n" + code],
                                       capture_output=True, text=True, timeout=20)
                except Exception as e:
                    fails.append(f"{sec}/{name} tc{i}: EXC {e}"); continue
                if r.returncode != 0:
                    last = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else '?'
                    fails.append(f"{sec}/{name} tc{i}: RUNTIME {last}")
                elif r.stdout != exp:
                    fails.append(f"{sec}/{name} tc{i}: sortie {r.stdout!r} attendu {exp!r}")
    print(f"Fichiers {len(files)}  Questions {tq}  Testcases {ttc}")
    if fails:
        print(f"\n{len(fails)} PROBLÈME(S) :")
        for x in fails: print("  -", x)
        sys.exit(2)
    print("\nALL PASS ✓  (structure valide + chaque réponse modèle produit la sortie attendue)")

if __name__ == "__main__":
    main()
