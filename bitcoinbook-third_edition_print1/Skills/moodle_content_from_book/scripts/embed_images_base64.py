#!/usr/bin/env python3
"""Remplace tout src="../../images/NAME.png" par un data URI base64 dans les
resource.html et presentation.html d'un dossier de cours Moodle.

Usage:
    python3 embed_images_base64.py <dossier_cours> <dossier_images>

Sans cette étape, les figures ne s'affichent pas dans une Page Moodle
(Moodle ne connaît pas l'arborescence relative du disque).
"""
import base64, glob, os, re, sys

def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    course, imgdir = sys.argv[1], sys.argv[2]
    cache = {}
    def datauri(name):
        if name not in cache:
            with open(os.path.join(imgdir, name), "rb") as fh:
                cache[name] = "data:image/png;base64," + base64.b64encode(fh.read()).decode()
        return cache[name]
    pat = re.compile(r'(?:\.\./)+images/([\w\-]+\.png)')
    files = glob.glob(os.path.join(course, "section_*", "resource.html")) + \
            glob.glob(os.path.join(course, "section_*", "presentation.html"))
    total = 0
    for f in sorted(files):
        html = open(f, encoding="utf-8").read()
        names = pat.findall(html)
        if not names:
            continue
        missing = [n for n in set(names) if not os.path.exists(os.path.join(imgdir, n))]
        if missing:
            print("!! IMAGES MANQUANTES", f, missing); continue
        new = pat.sub(lambda m: datauri(m.group(1)), html)
        open(f, "w", encoding="utf-8").write(new)
        print("embed %2d img -> %s" % (len(names), os.path.relpath(f, course)))
        total += len(names)
    left = sum(1 for f in files if re.search(r'(?:\.\./)+images/', open(f, encoding="utf-8").read()))
    print("TOTAL images embarquées:", total, "| fichiers avec chemin relatif restant:", left)

if __name__ == "__main__":
    main()
