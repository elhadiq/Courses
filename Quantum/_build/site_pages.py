# -*- coding: utf-8 -*-
"""site.py — page shells (index, chapter, exercises) built on assets/style.css.

The layout mirrors a printed manual: sticky breadcrumb bar with a light/dark
toggle, hero, quick-access entry points, one section per part, a card per
chapter with two actions, and previous/next navigation at the foot of every page.
"""

import html
import re
import xml.etree.ElementTree as ET

_STYLE_ATTR = re.compile(r'\s+style="[^"]*"')


def web(statement_html):
    """Strip the inline styling used for portable question banks so that a statement
    inherits the site's typography and adapts to the light/dark theme."""
    s = _STYLE_ATTR.sub('', statement_html)
    s = s.replace('<div>', '<div class="stmt">')
    return s

MATHJAX_CFG = (
    '<script>window.MathJax = {tex:{inlineMath:[["\\\\(","\\\\)"]],'
    'displayMath:[["\\\\[","\\\\]"]]}, svg:{fontCache:"global"}};</script>\n'
    '<script async id="MathJax-script" '
    'src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>')

JSX = ('<link rel="stylesheet" '
       'href="https://cdn.jsdelivr.net/npm/jsxgraph@1.9.2/distrib/jsxgraph.css">\n'
       '<script src="https://cdn.jsdelivr.net/npm/jsxgraph@1.9.2/distrib/jsxgraphcore.js"></script>')


def head(title, root='', description='', jsx=False):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#026573">
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="icon" type="image/svg+xml" href="{root}assets/favicon.svg">
<script src="{root}assets/theme.js"></script>
{MATHJAX_CFG}
{JSX if jsx else ''}
</head><body>'''


def header(root='', trail='', code='Graduate course'):
    return (f'<header class="site-header"><div class="container">'
            f'<div class="breadcrumb"><a href="{root}index.html">Quantum Computing</a>{trail}</div>'
            f'<span class="course-code">{code}</span></div></header>')


def footer():
    return ('<footer class="site-footer"><div class="container">'
            '<strong>Quantum Computing — Theory and Practice</strong> · '
            'ten chapters · forty programming exercises · thirty symbolic problems'
            '<span class="footer-meta">Edition 2026</span></div></footer>'
            '</body></html>')


def lesson_nav(prev_ch, next_ch, root='../', target='course.html'):
    def link(ch, cls, direction):
        if ch is None:
            return (f'<a class="{cls}" href="{root}index.html">'
                    f'<span class="dir">{direction}</span>'
                    f'<span class="ttl">Table of contents</span></a>')
        folder = f'chapter{ch["no"]:02d}-{ch["slug"]}'
        return (f'<a class="{cls}" href="{root}{folder}/{target}">'
                f'<span class="dir">{direction}</span>'
                f'<span class="ttl">{ch["no"]}. {html.escape(ch["title"])}</span></a>')
    return ('<nav class="lesson-nav">'
            + link(prev_ch, 'prev', 'Previous chapter')
            + link(next_ch, 'next', 'Next chapter') + '</nav>')


# ------------------------------------------------------------------- chapter
def build_course_html(ch, prev_ch, next_ch, n_fig, n_int):
    from engine import (h_prereq, h_objectives, h_section, h_references, box)
    folder = f'chapter{ch["no"]:02d}-{ch["slug"]}'
    body = [h_prereq(ch['prereq']), h_objectives(ch['objectives'])]
    for i, (heading, sec) in enumerate(ch['sections'], 1):
        body.append(h_section(i, heading, sec))
    if ch.get('summary'):
        body.append(box('note', 'Chapter summary', f'<p>{ch["summary"]}</p>'))
    body.append(f'''
<div class="exo-banner">
  <div><strong>Exercises for this chapter</strong>
    <span>{len(ch['coderunner'])} programming exercises in Python and NumPy ·
      {len(ch['stack'])} problems with symbolic answers, each with a worked solution</span></div>
  <a href="exercises.html">Open the exercise sheet</a>
</div>''')
    body.append(h_references(ch['references']))

    toc = ''.join(
        f'<li><a href="#s{i}">{heading}</a></li>'
        for i, (heading, _) in enumerate(ch['sections'], 1))

    return '\n'.join([
        head(f'Chapter {ch["no"]} — {ch["title"]}', root='../',
             description=ch['subtitle'], jsx=True),
        header(root='../', trail=f' · Chapter {ch["no"]}', code=f'Chapter {ch["no"]} of 10'),
        f'''<section class="lesson-hero"><div class="container">
  <div class="lesson-label">Chapter {ch['no']} · {n_fig} figures · {n_int} interactive</div>
  <h1>{html.escape(ch['title'])}</h1>
  <p class="lesson-sub">{ch['subtitle']}</p>
</div></section>''',
        f'''<div class="lesson-content">
<div class="other-activities">
  <h3>In this chapter</h3>
  <ul>{toc}
    <li><a href="#references">References &amp; further reading</a></li></ul>
</div>
''' + '\n'.join(body) + '\n</div>',
        lesson_nav(prev_ch, next_ch, '../', 'course.html'),
        footer(), MATHJAX_ONCE])


MATHJAX_ONCE = ''      # MathJax is loaded from the head; nothing extra needed


# ----------------------------------------------------------------- exercises
def _stack_fields(xml_str):
    q = ET.fromstring(xml_str)

    def txt(path):
        el = q.find(path)
        return (el.text or '') if el is not None else ''
    return {'name': txt('name/text'),
            'questiontext': txt('questiontext/text'),
            'generalfeedback': txt('generalfeedback/text'),
            'inputs': [i.find('name').text for i in q.findall('input')]}


def build_exercises_html(ch, prev_ch, next_ch):
    out = [head(f'Chapter {ch["no"]} exercises — {ch["title"]}', root='../',
                description=f'Exercises for chapter {ch["no"]}: {ch["title"]}'),
           header(root='../',
                  trail=f' · <a href="course.html">Chapter {ch["no"]}</a> · Exercises',
                  code='Exercise sheet'),
           f'''<section class="lesson-hero"><div class="container">
  <div class="lesson-label">Chapter {ch['no']} · exercise sheet</div>
  <h1>{html.escape(ch['title'])}</h1>
  <p class="lesson-sub">{len(ch['coderunner'])} programming exercises ·
     {len(ch['stack'])} problems with symbolic answers. Every solution is hidden behind a
     toggle — attempt each one before opening it.</p>
</div></section>''',
           '<div class="lesson-content">',
           '<h2>Programming exercises</h2>',
           '<p>Each exercise is checked automatically against hidden test cases. Only NumPy is '
           'required, and the function names in the statement must be used exactly as written.</p>']

    for i, q in enumerate(ch['coderunner'], 1):
        examples = ''
        for tc in q['tests']:
            if tc.get('useasexample') == '1':
                examples += ('<pre><code>' + html.escape(tc['code'].rstrip()) +
                             '\n→ ' + html.escape(tc['expected'].rstrip()) + '</code></pre>')
        out.append(f'''<div class="exo">
  <div class="exo-head"><span class="exo-num">Exercise {ch['no']}.{i}</span>
    <span class="diff d2">Programming</span></div>
  {web(q['qtext'])}
  <p style="color:var(--color-muted);font-size:0.85rem;letter-spacing:0.06em;
     text-transform:uppercase;margin-bottom:0;">Starting point</p>
  <pre><code>{html.escape(q['preload'])}</code></pre>
  <p style="color:var(--color-muted);font-size:0.85rem;letter-spacing:0.06em;
     text-transform:uppercase;margin-bottom:0;">Worked examples</p>
  {examples}
  <details class="sol"><summary>Show the reference solution</summary>
    <pre><code>{html.escape(q['answer'])}</code></pre></details>
</div>''')

    out.append('<h2>Problems with symbolic answers</h2>')
    out.append('<p>Answers here are expressions rather than numbers, and any algebraically '
               'equivalent form is accepted. Give fractions and radicals exactly; decimal '
               'approximations are not accepted.</p>')
    for i, xml_str in enumerate(ch['stack'], 1):
        f = _stack_fields(xml_str)
        qt = f['questiontext']
        for name in f['inputs']:
            qt = qt.replace(f'[[input:{name}]]',
                            '<span style="display:inline-block;min-width:130px;'
                            'border-bottom:2px dotted var(--primary);color:var(--primary);'
                            'font-size:0.85em;text-align:center;">your answer</span>')
            qt = qt.replace(f'[[validation:{name}]]', '')
        out.append(f'''<div class="exo">
  <div class="exo-head"><span class="exo-num">Problem {ch['no']}.{i}</span>
    <span class="diff d4">Symbolic</span></div>
  {web(qt)}
  <details class="sol"><summary>Show the worked solution</summary>
    {web(f['generalfeedback'])}</details>
</div>''')

    out.append('<div class="exo-banner"><div><strong>Back to the theory</strong>'
               '<span>Every exercise above is worked from a result proved in the chapter</span>'
               f'</div><a href="course.html">Open chapter {ch["no"]}</a></div>')
    out.append('</div>')
    out.append(lesson_nav(prev_ch, next_ch, '../', 'exercises.html'))
    out.append(footer())
    return '\n'.join(out)


# ---------------------------------------------------------------------- index
PARTS = [
    ('Part I — Foundations',
     'The algebraic and physical language the rest of the course assumes', [1, 2, 3]),
    ('Part II — Entanglement and open systems',
     'Correlations no classical model reproduces, and what noise does to them', [4, 5]),
    ('Part III — Quantum algorithms',
     'Where the speed-ups come from, and how far they actually reach', [6, 7, 8]),
    ('Part IV — Fault tolerance and the near term',
     'Making the machine reliable, and what can be attempted before it is', [9, 10]),
]

QUICK = [
    (1, 'Start here', 'Mathematical foundations',
     'Hilbert spaces · spectral theorem · tensor products'),
    (7, 'Flagship algorithm', 'Shor and factoring',
     'Order finding · continued fractions · consequences for cryptography'),
    (9, 'Hardware reality', 'Quantum error correction',
     'Stabilizer codes · surface code · the threshold theorem'),
]


def build_index(chapters):
    by_no = {c['no']: c for c in chapters}
    n_fig = sum(c.get('_figures', 0) for c in chapters)
    n_int = sum(c.get('_interactive', 0) for c in chapters)
    n_ref = sum(len(c['references']) for c in chapters)
    n_cr = sum(len(c['coderunner']) for c in chapters)
    n_st = sum(len(c['stack']) for c in chapters)

    out = [head('Quantum Computing — Theory and Practice', root='',
                description=('A graduate course in quantum computing: 10 chapters, '
                             f'{n_cr} programming exercises, {n_st} symbolic problems and '
                             f'{n_fig} figures, from Hilbert spaces to fault tolerance.')),
           header(root='', trail=' · Manual', code='Table of contents'),
           f'''<section class="hero"><div class="container">
  <h1>Quantum Computing</h1>
  <p class="subtitle">Foundations · Entanglement · Algorithms · Error correction · Near-term methods</p>
  <div class="instructors"><div class="instructor">
    <strong>Graduate course</strong>
    <span>Assumes linear algebra over ℂ, elementary probability and working Python</span>
  </div></div>
  <a class="cta" href="#contents">See the full table of contents</a>
</div></section>''',
           f'''<section class="section"><div class="container">
  <div class="quick-access">
    <a class="qa-card" href="#contents"><span class="qa-label">Contents</span>
      <span class="qa-title">{len(chapters)} chapters</span>
      <span class="qa-sub">Grouped into four parts, each building on the last</span></a>
    <a class="qa-card" href="#exercise-sheets"><span class="qa-label">Practice</span>
      <span class="qa-title">{n_cr + n_st} exercises</span>
      <span class="qa-sub">{n_cr} programming · {n_st} symbolic · all with worked solutions</span></a>
    <a class="qa-card" href="#contents"><span class="qa-label">Illustrations</span>
      <span class="qa-title">{n_fig} figures</span>
      <span class="qa-sub">{n_int} of them interactive · {n_ref} cited references</span></a>
  </div>
</div></section>''']

    out.append('<section class="section"><div class="container">'
               '<h2 class="section-title">Quick access</h2>'
               '<p class="section-subtitle">Three recommended entry points</p>'
               '<div class="quick-access">')
    for no, label, title, sub in QUICK:
        c = by_no[no]
        out.append(f'<a class="qa-card" href="chapter{no:02d}-{c["slug"]}/course.html">'
                   f'<span class="qa-label">{label}</span>'
                   f'<span class="qa-title">{html.escape(title)}</span>'
                   f'<span class="qa-sub">{sub}</span></a>')
    out.append('</div></div></section><div id="contents"></div>')

    for title, subtitle, nos in PARTS:
        out.append(f'<section class="section"><div class="container">'
                   f'<h2 class="section-title">{title}</h2>'
                   f'<p class="section-subtitle">{subtitle}</p><div class="sequences">')
        for no in nos:
            c = by_no[no]
            folder = f'chapter{no:02d}-{c["slug"]}'
            out.append(f'''<div class="seq-card">
  <div class="seq-meta">Chapter {no}</div>
  <h3>{html.escape(c['title'])}</h3>
  <p class="seq-topics">{len(c['sections'])} sections · {c.get('_figures', 0)} figures ·
     {len(c['coderunner'])} programming exercises · {len(c['stack'])} symbolic problems ·
     {len(c['references'])} references</p>
  <div class="seq-actions">
    <a class="btn primary" href="{folder}/course.html">Open the chapter</a>
    <a class="btn" href="{folder}/exercises.html">Exercises</a>
  </div>
</div>''')
        out.append('</div></div></section>')

    out.append('<section class="section" id="exercise-sheets"><div class="container">'
               '<h2 class="section-title">Exercise sheets</h2>'
               f'<p class="section-subtitle">{n_cr} programming exercises graded against hidden '
               f'test cases and {n_st} problems with symbolic answers, each accompanied by a '
               'worked solution</p><div class="quick-access">')
    for c in chapters:
        folder = f'chapter{c["no"]:02d}-{c["slug"]}'
        out.append(f'<a class="qa-card" href="{folder}/exercises.html">'
                   f'<span class="qa-label">Chapter {c["no"]}</span>'
                   f'<span class="qa-title">{html.escape(c["title"])}</span>'
                   f'<span class="qa-sub">{len(c["coderunner"])} programming · '
                   f'{len(c["stack"])} symbolic</span></a>')
    out.append('</div></div></section>')
    out.append(footer())
    return '\n'.join(out)
