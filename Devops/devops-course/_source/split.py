#!/usr/bin/env python3
"""Split each module page into one navigable page per section.

module-N.html  -> becomes the module hub (lead + section index)
module-N/NN-slug.html -> one page per <h2 id=...> section
"""
import re, os, html as H, json

SRC = os.path.dirname(os.path.abspath(__file__))       # _source/  : single-page masters
OUT = os.path.dirname(SRC)                             # course root: generated site
MODULES = [f"module-{i}.html" for i in range(1, 8)]

def src_path(f): return os.path.join(SRC, f)
def out_path(f): return os.path.join(OUT, f)

def strip(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

def esc(s):
    return H.escape(s, quote=False)

def nonum(s):
    """drop a leading '2.8 ' so hub cards don't repeat the number badge"""
    return re.sub(r'^\d+\.\d+\s+', '', s)

# ---------- parse ----------
mods = []
for mi, f in enumerate(MODULES, start=1):
    src = open(src_path(f), encoding='utf-8').read()
    title  = re.search(r'<title>(.*?)</title>', src, re.S).group(1)
    kicker = re.search(r'<div class="kicker"[^>]*>(.*?)</div>', src, re.S).group(1).strip()
    h1     = re.search(r'<h1>(.*?)</h1>', src, re.S).group(1).strip()
    lead   = re.search(r'<p class="lead">(.*?)</p>', src, re.S).group(1).strip()

    body = src.split('</div>\n\n<h2', 1)          # cut everything before the first h2
    after_toc = '<h2' + src.split('<h2', 1)[1]
    after_toc = after_toc.split('<div class="pager">')[0]

    parts = re.split(r'(?=<h2 id=")', after_toc)
    parts = [p for p in parts if p.strip().startswith('<h2 id="')]

    # guard: refuse to run against an already-generated hub page
    if not parts:
        raise SystemExit(
            f"ABORT: {f} has no <h2 id=...> sections.\n"
            f"       _source/ must hold the single-page masters.")

    secs = []
    for p in parts:
        m = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', p, re.S)
        anchor, heading = m.group(1), m.group(2)
        secs.append({
            'anchor': anchor,
            'heading': heading.strip(),
            'text': strip(heading),
            'html': p.rstrip(),
        })
    mods.append({'file': f, 'n': mi, 'title': title, 'kicker': kicker,
                 'h1': h1, 'lead': lead, 'secs': secs})

# ---------- global anchor -> page map ----------
def slug(i, anchor):
    return f"{i:02d}-{anchor}"

amap = {}   # (module_file, anchor) -> "module-N/NN-anchor.html"
for m in mods:
    for i, s in enumerate(m['secs'], start=1):
        amap[(m['file'], s['anchor'])] = f"module-{m['n']}/{slug(i, s['anchor'])}.html"
        s['page'] = slug(i, s['anchor']) + '.html'
        s['idx'] = i

# flat ordering across the whole course, for prev/next across module edges
flat = [(m, s) for m in mods for s in m['secs']]

# ---------- link rewriting ----------
def rewrite(htm, depth):
    """depth 1 = inside module-N/ ; 0 = at course root"""
    up = '../' if depth else ''

    def sub_cross(mt):
        tgt, anc = mt.group(1), mt.group(2)
        key = (tgt, anc)
        if key in amap:
            return f'href="{up}{amap[key]}"'
        return f'href="{up}{tgt}#{anc}"'
    htm = re.sub(r'href="(module-\d+\.html)#([^"]+)"', sub_cross, htm)
    htm = re.sub(r'href="(module-\d+\.html)"', lambda m: f'href="{up}{m.group(1)}"', htm)
    htm = re.sub(r'href="(index\.html)"', lambda m: f'href="{up}index.html"', htm)
    return htm

def sidenav(m, cur_anchor, depth=1):
    out = ['<nav class="sidenav">', f'<p class="lbl">Module {m["n"]:02d}</p>']
    prev_grp = None
    for s in m['secs']:
        t = s['text']
        grp = 'Practice' if re.match(r'^(Lab|Exercises|Checkpoint|Capstone)', t) else 'Concepts'
        if grp != prev_grp:
            out.append(f'<a class="grp">{grp}</a>')
            prev_grp = grp
        cls = ' class="cur"' if s['anchor'] == cur_anchor else ''
        out.append(f'<a href="{s["page"]}"{cls}>{esc(t)}</a>')
    out.append('</nav>')
    return '\n'.join(out)

PAGE = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{ptitle}</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>

<header class="top"><div class="wrap wide">
  <a class="brand hm" href="../index.html">Practical <span>DevOps</span></a>
  <nav>
    <a href="../index.html">All modules</a>
    <a href="../module-{n}.html">Module {n} contents</a>
    <button class="theme" onclick="toggleTheme()">◐ theme</button>
  </nav>
</div></header>

<main class="wrap wide">
<div class="layout">
{side}
<div class="content">

<div class="crumb">
  <a href="../index.html">Course</a><span class="sep">/</span>
  <a href="../module-{n}.html">{mtitle}</a>
</div>
<div class="secmeta">Module {n:02d} · Section {i} of {tot}</div>

{body}

<div class="pager">
  {prev}
  {nextlink}
</div>

</div>
</div>
</main>
<footer><div class="wrap wide">Practical DevOps · Module {n} · {stext}</div></footer>
<script src="../assets/course.js"></script>
</body>
</html>
"""

def link(target_depth_page, sub, label, cls=''):
    c = f' class="{cls}"' if cls else ''
    return (f'<a href="{target_depth_page}"{c}>'
            f'<span class="sub">{sub}</span>{label}</a>')

written = []
for m in mods:
    tot = len(m['secs'])
    for s in m['secs']:
        gi = flat.index((m, s))

        # previous
        if s['idx'] > 1:
            p = m['secs'][s['idx'] - 2]
            prev = link(p['page'], '← Previous', esc(p["text"]))
        elif gi > 0:
            pm, ps = flat[gi - 1]
            prev = link(f"../module-{pm['n']}/{ps['page']}", f"← Module {pm['n']}", esc(ps["text"]))
        else:
            prev = link('../index.html', '←', 'Course index')

        # next
        if s['idx'] < tot:
            nx = m['secs'][s['idx']]
            next_ = link(nx['page'], 'Next →', esc(nx["text"]), 'nx')
        elif gi + 1 < len(flat):
            nm, ns = flat[gi + 1]
            next_ = link(f"../module-{nm['n']}/{ns['page']}", f"Module {nm['n']} →",
                         esc(ns["text"]), 'nx')
        else:
            next_ = link('../index.html', 'Done →', 'Back to the course index', 'nx')

        html = PAGE.format(
            ptitle=f"{s['text']} — Module {m['n']} | Practical DevOps",
            n=m['n'], i=s['idx'], tot=tot,
            mtitle=strip(m['h1']),
            stext=esc(s["text"]),
            side=sidenav(m, s['anchor']),
            body=rewrite(s['html'], depth=1),
            prev=prev, nextlink=next_)
        os.makedirs(out_path(f"module-{m['n']}"), exist_ok=True)
        path = f"module-{m['n']}/{s['page']}"
        open(out_path(path), 'w', encoding='utf-8').write(html)
        written.append(path)

# ---------- hub pages ----------
HUB = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<header class="top"><div class="wrap">
  <a class="brand hm" href="index.html">Practical <span>DevOps</span></a>
  <nav>
    <a href="index.html">All modules</a>
    {navprev}
    {navnext}
    <button class="theme" onclick="toggleTheme()">◐ theme</button>
  </nav>
</div></header>

<main class="wrap">

<div class="kicker" style="margin-top:40px">{kicker}</div>
<h1>{h1}</h1>
<p class="lead">{lead}</p>

<div class="box">
<b>How to work through this module</b>
{tot} short pages, in order. Each one is a single idea or a single lab step, with Next / Previous at
the bottom and the full module in the sidebar. Start at the top — later pages assume the earlier ones.
</div>

<h2>Contents</h2>
<div class="hubgrid">
{cards}
</div>

<div class="pager">
  {prev}
  <a class="nx" href="module-{n}/{first}"><span class="sub">Start here →</span>{firsttext}</a>
</div>

</main>
<footer><div class="wrap">Practical DevOps · Module {n}</div></footer>
<script src="assets/course.js"></script>
</body>
</html>
"""

for m in mods:
    cards = '\n'.join(
        f'  <a class="hub" href="module-{m["n"]}/{s["page"]}">'
        f'<span class="num">{m["n"]}.{s["idx"]}</span>'
        f'<span class="ttl">{esc(nonum(s["text"]))}</span></a>'
        for s in m['secs'])
    navprev = (f'<a href="module-{m["n"]-1}.html">← Prev</a>' if m['n'] > 1 else '')
    navnext = (f'<a href="module-{m["n"]+1}.html">Next →</a>' if m['n'] < 7 else '')
    prev = (f'<a href="module-{m["n"]-1}.html">← Module {m["n"]-1}</a>'
            if m['n'] > 1 else '<a href="index.html">← Course index</a>')
    open(out_path(m['file']), 'w', encoding='utf-8').write(HUB.format(
        title=m['title'], kicker=m['kicker'], h1=m['h1'], lead=rewrite(m['lead'], 0),
        tot=len(m['secs']), cards=cards, n=m['n'],
        first=m['secs'][0]['page'], firsttext=esc(m["secs"][0]["text"]),
        navprev=navprev, navnext=navnext, prev=prev))
    written.append(m['file'])

print(json.dumps({'section_pages': len(flat), 'hubs': len(mods),
                  'total_written': len(written)}, indent=1))
