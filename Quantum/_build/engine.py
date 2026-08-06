"""
engine.py — Shared build engine for the Quantum Computing Moodle course.

Produces, for each chapter:
  * course.html                 — Moodle Page resource (inline styles + MathJax delimiters)
  * exercises_coderunner.xml    — CodeRunner Python questions (auto-graded)
  * exercises_stack.xml         — STACK (Maxima/CAS) questions
  * references.html             — annotated bibliography (also embedded in course.html)

CodeRunner XML is produced by the validated skill script (never by hand).
STACK XML is produced by string templates (never ElementTree) — see moodle-stack skill.
"""

import os
import sys
import xml.etree.ElementTree as ET

SKILL_CR = '/sessions/admiring-intelligent-knuth/mnt/.claude/skills/moodle-coderunner/scripts'
sys.path.insert(0, SKILL_CR)
from generate_xml import make_question as cr_question, build_quiz_xml, validate_xml  # noqa: E402

# ---------------------------------------------------------------- palette ----
C = {
    'ink':    '#0f172a',
    'body':   '#1e293b',
    'muted':  '#475569',
    'accent': '#026573',
    'accent2': '#0891a1',
    'gold':   '#c9a227',
    'line':   '#e2e8f0',
    'panel':  '#f8fafc',
    'code':   '#0b2b30',
}
SERIF = "Georgia,'Times New Roman',serif"
MONO = "'Courier New',Consolas,monospace"


# ================================================================ HTML ========
def h_title(chapter_no, title, subtitle):
    """Kept for compatibility; the hero is now emitted by build_course_html."""
    return ''


def h_objectives(items):
    lis = ''.join(f'<li>{i}</li>' for i in items)
    return ('<div class="keypoints"><h3>Learning outcomes</h3>'
            f'<ul>{lis}</ul></div>')


def h_prereq(text):
    return ('<div class="box tip"><span class="box-title">Prerequisites</span>'
            f'<p>{text}</p></div>')


def h_section(n, heading, body_html):
    return f'<h2 id="s{n}">{n}. {heading}</h2>\n{body_html}'


def p(text):
    return f'<p>{text}</p>'


def eq(latex):
    return ('<div style="text-align:center;overflow-x:auto;margin:1.3em 0;">'
            f'\\[{latex}\\]</div>')


_BOXCLASS = {'def': ('def', 'Definition'), 'thm': ('thm', 'Theorem'),
             'prop': ('prop', 'Proposition'), 'proof': ('proof', 'Proof'),
             'ex': ('example', 'Example'), 'warn': ('warn', 'Caution'),
             'note': ('tip', 'Remark')}


def box(kind, title, body):
    cls, default = _BOXCLASS[kind]
    label = title or default
    return (f'<div class="box {cls}"><span class="box-title">{label}</span>'
            f'<div>{body}</div></div>')


def code(src, caption=''):
    esc = src.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    cap = (f'<p style="color:var(--color-muted);font-size:0.85rem;margin:1.2em 0 -0.4em 0;'
           f'letter-spacing:0.06em;text-transform:uppercase;">{caption}</p>') if caption else ''
    return f'{cap}<pre><code>{esc}</code></pre>'


def table(headers, rows):
    th = ''.join(f'<th>{h}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return (f'<div style="overflow-x:auto;"><table><thead><tr>{th}</tr></thead>'
            f'<tbody>{tr}</tbody></table></div>')


def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def ol(items):
    return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'


def h_references(refs):
    """refs: list of dicts {authors, title, venue, year, link, note}"""
    items = ''
    for i, r in enumerate(refs, 1):
        link = (f' <a href="{r["link"]}" rel="noopener">{r["link"]}</a>') if r.get('link') else ''
        note = (f'<br><span style="color:var(--color-muted);font-size:0.92em;font-style:italic;">'
                f'{r["note"]}</span>') if r.get('note') else ''
        items += (f'<li id="ref{i}"><strong>{r["authors"]}</strong>. <em>{r["title"]}</em>. '
                  f'{r["venue"]}, {r["year"]}.{link}{note}</li>')
    return ('<h2 id="references">References &amp; further reading</h2>'
            f'<ol class="reflist">{items}</ol>')


# ============================================================ citations ======
def cite(nums):
    """Inline citation: cite('3') or cite('1,4') -> superscript links to the bibliography."""
    parts = [n.strip() for n in str(nums).split(',')]
    links = ', '.join(f'<a href="#ref{n}">{n}</a>' for n in parts)
    return (f'<sup class="cite" style="font-size:0.72em;white-space:nowrap;'
            f'color:var(--primary);">[{links}]</sup>')


def sources(text):
    """A short 'where this comes from' strip closing a section."""
    return ('<p style="border-left:3px solid var(--tip-br);background:var(--tip-bg);'
            'border-radius:0 8px 8px 0;padding:9px 16px;margin:1.4em 0 0.4em 0;'
            'font-size:0.92rem;line-height:1.65;">'
            '<span style="color:var(--tip-fg);font-size:0.78rem;font-weight:700;'
            'letter-spacing:0.09em;text-transform:uppercase;">Sources&nbsp;&nbsp;</span>'
            f'<span style="color:var(--color-muted);">{text}</span></p>')


# =============================================================== figures =====
def figure(num, caption, svg_body, width=680, height=340):
    """Wrap an SVG body in a numbered, captioned figure block."""
    return (f'<figure class="viz" style="padding:14px 16px 12px 16px;">'
            f'<div class="viz-title">Figure {num}</div>'
            f'<div style="background:#ffffff;border:1px solid var(--color-rule);border-radius:8px;'
            f'padding:10px 8px;overflow-x:auto;text-align:center;">'
            f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'preserveAspectRatio="xMidYMid meet" style="max-width:100%;height:auto;" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">{svg_body}</svg></div>'
            f'<figcaption style="font-size:0.9rem;color:var(--color-muted);line-height:1.65;'
            f'margin-top:10px;text-align:left;">{caption}</figcaption></figure>')


_ENT = __import__('re').compile(r'&(?!#\d+;|#x[0-9A-Fa-f]+;|[A-Za-z]+;)')


def _svg_esc(s):
    """Escape bare &, < and > in SVG text while preserving existing HTML entities."""
    s = _ENT.sub('&amp;', str(s))
    return s.replace('<', '&lt;').replace('>', '&gt;')


def _txt(x, y, s, size=12, fill=None, anchor='middle', weight='normal', style='normal', family=SERIF):
    s = _svg_esc(s)
    fill = fill or C['body']
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
            f'font-style="{style}">{s}</text>')


PALETTE = ['#026573', '#c9a227', '#9333ea', '#dc2626', '#0891a1', '#65a30d']


def line_chart(series, xlim, ylim, xlabel='', ylabel='', width=680, height=340,
               xticks=None, yticks=None, hlines=(), vlines=(), notes=(), legend=True,
               xfmt='{:g}', yfmt='{:g}'):
    """series: list of dict(label, xs, ys, color=?, dash=?, marker=?)."""
    ml, mr, mt, mb = 62, 22, 26, 46
    x0, x1 = xlim
    y0, y1 = ylim
    W, H = width - ml - mr, height - mt - mb

    def X(v):
        return ml + (v - x0) / (x1 - x0) * W

    def Y(v):
        return mt + H - (v - y0) / (y1 - y0) * H

    xticks = list(xticks) if xticks is not None else [x0 + k * (x1 - x0) / 5 for k in range(6)]
    yticks = list(yticks) if yticks is not None else [y0 + k * (y1 - y0) / 4 for k in range(5)]
    s = [f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>']
    for t in xticks:
        s.append(f'<line x1="{X(t):.1f}" y1="{mt}" x2="{X(t):.1f}" y2="{mt+H}" '
                 f'stroke="{C["line"]}" stroke-width="1"/>')
        s.append(_txt(X(t), mt + H + 18, xfmt.format(t), 11.5, C['muted']))
    for t in yticks:
        s.append(f'<line x1="{ml}" y1="{Y(t):.1f}" x2="{ml+W}" y2="{Y(t):.1f}" '
                 f'stroke="{C["line"]}" stroke-width="1"/>')
        s.append(_txt(ml - 8, Y(t) + 4, yfmt.format(t), 11.5, C['muted'], anchor='end'))
    s.append(f'<line x1="{ml}" y1="{mt+H}" x2="{ml+W}" y2="{mt+H}" stroke="{C["ink"]}" stroke-width="1.5"/>')
    s.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+H}" stroke="{C["ink"]}" stroke-width="1.5"/>')
    for y, lab, col in hlines:
        s.append(f'<line x1="{ml}" y1="{Y(y):.1f}" x2="{ml+W}" y2="{Y(y):.1f}" stroke="{col}" '
                 f'stroke-width="1.6" stroke-dasharray="6 4"/>')
        if lab:
            s.append(_txt(ml + W - 4, Y(y) - 6, lab, 11.5, col, anchor='end', style='italic'))
    for x, lab, col in vlines:
        s.append(f'<line x1="{X(x):.1f}" y1="{mt}" x2="{X(x):.1f}" y2="{mt+H}" stroke="{col}" '
                 f'stroke-width="1.4" stroke-dasharray="4 4"/>')
        if lab:
            s.append(_txt(X(x), mt - 8, lab, 11.5, col))
    for k, ser in enumerate(series):
        col = ser.get('color', PALETTE[k % len(PALETTE)])
        pts = ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in zip(ser['xs'], ser['ys'])
                       if x0 - 1e-9 <= a <= x1 + 1e-9)
        dash = f' stroke-dasharray="{ser["dash"]}"' if ser.get('dash') else ''
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.2"{dash}/>')
        if ser.get('marker'):
            for a, b in zip(ser['xs'], ser['ys']):
                if x0 <= a <= x1:
                    s.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="3.1" fill="{col}"/>')
    for nx, ny, ntext, ncol in notes:
        s.append(_txt(X(nx), Y(ny), ntext, 12, ncol, anchor='start', style='italic'))
    if xlabel:
        s.append(_txt(ml + W / 2, height - 8, xlabel, 12.5, C['ink']))
    if ylabel:
        s.append(f'<g transform="translate(14,{mt+H/2}) rotate(-90)">'
                 f'{_txt(0, 0, ylabel, 12.5, C["ink"])}</g>')
    if legend and any(ser.get('label') for ser in series):
        lx, ly = ml + 12, mt + 12
        for k, ser in enumerate(series):
            if not ser.get('label'):
                continue
            col = ser.get('color', PALETTE[k % len(PALETTE)])
            s.append(f'<line x1="{lx}" y1="{ly}" x2="{lx+24}" y2="{ly}" stroke="{col}" stroke-width="2.6"/>')
            s.append(_txt(lx + 30, ly + 4, ser['label'], 12, C['body'], anchor='start'))
            ly += 18
    return ''.join(s)


def bar_chart(labels, values, ylim=None, ylabel='', width=680, height=320,
              colors=None, valfmt='{:.3g}', highlight=None):
    ml, mr, mt, mb = 58, 18, 24, 52
    W, H = width - ml - mr, height - mt - mb
    ymax = ylim[1] if ylim else max(values) * 1.15
    ymin = ylim[0] if ylim else 0
    n = len(values)
    bw = W / n * 0.72
    gap = W / n
    s = [f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>']
    for k in range(5):
        t = ymin + k * (ymax - ymin) / 4
        y = mt + H - (t - ymin) / (ymax - ymin) * H
        s.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+W}" y2="{y:.1f}" stroke="{C["line"]}"/>')
        s.append(_txt(ml - 8, y + 4, valfmt.format(t), 11.5, C['muted'], anchor='end'))
    for i, (lab, v) in enumerate(zip(labels, values)):
        x = ml + i * gap + (gap - bw) / 2
        h = (v - ymin) / (ymax - ymin) * H
        col = (colors[i] if colors else
               (C['gold'] if (highlight is not None and i == highlight) else C['accent']))
        s.append(f'<rect x="{x:.1f}" y="{mt+H-h:.1f}" width="{bw:.1f}" height="{max(h,0.5):.1f}" '
                 f'fill="{col}" rx="2"/>')
        s.append(_txt(x + bw / 2, mt + H + 17, lab, 11, C['muted']))
    s.append(f'<line x1="{ml}" y1="{mt+H}" x2="{ml+W}" y2="{mt+H}" stroke="{C["ink"]}" stroke-width="1.5"/>')
    if ylabel:
        s.append(f'<g transform="translate(14,{mt+H/2}) rotate(-90)">{_txt(0,0,ylabel,12.5,C["ink"])}</g>')
    return ''.join(s)


def circuit_svg(nwires, columns, wire_labels=None, width=680, height=None, title=''):
    """columns: list of lists of ops.
       ('g', wire, 'H')            single-qubit box
       ('c', ctrl, targ, 'X')      controlled gate ('X' -> plus symbol, else box)
       ('cz', a, b)                controlled-Z (two dots)
       ('swap', a, b)
       ('m', wire)                 measurement
       ('multi', w0, w1, 'QFT')    box spanning wires w0..w1
       ('lab', wire, 'text')       floating label above a wire
    """
    lm, rm = 92, 26
    top = 52 if title else 30
    dy, dx = 46, 62
    height = height or top + nwires * dy + 20
    s = [f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>']
    if title:
        s.append(_txt(width / 2, 18, title, 13, C['accent'], weight='bold'))
    ncol = max(len(columns), 1)
    xend = min(width - rm, lm + (ncol + 0.6) * dx)

    def wy(w):
        return top + w * dy

    def cx(i):
        return lm + (i + 0.5) * dx

    for w in range(nwires):
        s.append(f'<line x1="{lm-18}" y1="{wy(w)}" x2="{xend}" y2="{wy(w)}" '
                 f'stroke="{C["ink"]}" stroke-width="1.3"/>')
        lab = (wire_labels[w] if wire_labels and w < len(wire_labels) else f'|0&#10217;')
        s.append(_txt(lm - 26, wy(w) + 5, lab, 13, C['ink'], anchor='end'))
    for i, col in enumerate(columns):
        x = cx(i)
        for op in col:
            kind = op[0]
            if kind == 'g':
                _, w, name = op
                s.append(f'<rect x="{x-17}" y="{wy(w)-16}" width="34" height="32" rx="4" '
                         f'fill="#ecfeff" stroke="{C["accent"]}" stroke-width="1.6"/>')
                s.append(_txt(x, wy(w) + 5, name, 13, C['accent'], weight='bold'))
            elif kind == 'c':
                _, c, t, name = op
                s.append(f'<line x1="{x}" y1="{wy(c)}" x2="{x}" y2="{wy(t)}" stroke="{C["ink"]}" stroke-width="1.6"/>')
                s.append(f'<circle cx="{x}" cy="{wy(c)}" r="5.5" fill="{C["ink"]}"/>')
                if name == 'X':
                    s.append(f'<circle cx="{x}" cy="{wy(t)}" r="12" fill="#ffffff" stroke="{C["ink"]}" stroke-width="1.6"/>')
                    s.append(f'<line x1="{x-12}" y1="{wy(t)}" x2="{x+12}" y2="{wy(t)}" stroke="{C["ink"]}" stroke-width="1.6"/>')
                    s.append(f'<line x1="{x}" y1="{wy(t)-12}" x2="{x}" y2="{wy(t)+12}" stroke="{C["ink"]}" stroke-width="1.6"/>')
                else:
                    s.append(f'<rect x="{x-19}" y="{wy(t)-16}" width="38" height="32" rx="4" '
                             f'fill="#fefce8" stroke="{C["gold"]}" stroke-width="1.6"/>')
                    s.append(_txt(x, wy(t) + 5, name, 12, '#92400e', weight='bold'))
            elif kind == 'cz':
                _, a, b = op
                s.append(f'<line x1="{x}" y1="{wy(a)}" x2="{x}" y2="{wy(b)}" stroke="{C["ink"]}" stroke-width="1.6"/>')
                for w in (a, b):
                    s.append(f'<circle cx="{x}" cy="{wy(w)}" r="5.5" fill="{C["ink"]}"/>')
            elif kind == 'swap':
                _, a, b = op
                s.append(f'<line x1="{x}" y1="{wy(a)}" x2="{x}" y2="{wy(b)}" stroke="{C["ink"]}" stroke-width="1.6"/>')
                for w in (a, b):
                    s.append(f'<line x1="{x-7}" y1="{wy(w)-7}" x2="{x+7}" y2="{wy(w)+7}" stroke="{C["ink"]}" stroke-width="2"/>')
                    s.append(f'<line x1="{x-7}" y1="{wy(w)+7}" x2="{x+7}" y2="{wy(w)-7}" stroke="{C["ink"]}" stroke-width="2"/>')
            elif kind == 'm':
                _, w = op
                s.append(f'<rect x="{x-18}" y="{wy(w)-16}" width="36" height="32" rx="4" '
                         f'fill="#f1f5f9" stroke="{C["ink"]}" stroke-width="1.5"/>')
                s.append(f'<path d="M {x-9} {wy(w)+7} A 9 9 0 0 1 {x+9} {wy(w)+7}" fill="none" '
                         f'stroke="{C["ink"]}" stroke-width="1.5"/>')
                s.append(f'<line x1="{x}" y1="{wy(w)+7}" x2="{x+7}" y2="{wy(w)-6}" stroke="{C["ink"]}" stroke-width="1.5"/>')
            elif kind == 'multi':
                _, w0, w1, name = op
                y0, y1_ = wy(w0) - 16, wy(w1) + 16
                s.append(f'<rect x="{x-26}" y="{y0}" width="52" height="{y1_-y0}" rx="5" '
                         f'fill="#f5f3ff" stroke="#9333ea" stroke-width="1.6"/>')
                s.append(_txt(x, (y0 + y1_) / 2 + 5, name, 12.5, '#6d28d9', weight='bold'))
            elif kind == 'lab':
                _, w, text = op
                s.append(_txt(x, wy(w) - 22, text, 11.5, C['muted'], style='italic'))
    return ''.join(s)


def graph_svg(nodes, edges, width=680, height=320, node_r=19, edge_labels=None,
              node_colors=None, title=''):
    """nodes: dict name -> (x, y) in SVG coordinates. edges: list of (a, b)."""
    s = [f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>']
    if title:
        s.append(_txt(width / 2, 20, title, 13, C['accent'], weight='bold'))
    for k, (a, b) in enumerate(edges):
        (xa, ya), (xb, yb) = nodes[a], nodes[b]
        s.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="{C["muted"]}" stroke-width="2"/>')
        if edge_labels and k < len(edge_labels) and edge_labels[k]:
            s.append(_txt((xa + xb) / 2, (ya + yb) / 2 - 6, edge_labels[k], 11.5, C['muted']))
    for name, (x, y) in nodes.items():
        col = (node_colors or {}).get(name, C['accent'])
        s.append(f'<circle cx="{x}" cy="{y}" r="{node_r}" fill="{col}" stroke="#ffffff" stroke-width="2.5"/>')
        s.append(_txt(x, y + 5, name, 13, '#ffffff', weight='bold'))
    return ''.join(s)


def bloch_svg(vectors=(), width=680, height=340, title=''):
    """vectors: list of (theta_deg, phi_deg, label, colour) drawn on a projected sphere."""
    import math
    cx0, cy0, R = width / 2, height / 2 + 6, 118
    s = [f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>']
    if title:
        s.append(_txt(width / 2, 18, title, 13, C['accent'], weight='bold'))
    s.append(f'<circle cx="{cx0}" cy="{cy0}" r="{R}" fill="#f0fdfa" stroke="{C["accent"]}" stroke-width="1.6"/>')
    s.append(f'<ellipse cx="{cx0}" cy="{cy0}" rx="{R}" ry="{R*0.32}" fill="none" '
             f'stroke="{C["accent2"]}" stroke-width="1" stroke-dasharray="4 4"/>')
    s.append(f'<ellipse cx="{cx0}" cy="{cy0}" rx="{R*0.34}" ry="{R}" fill="none" '
             f'stroke="{C["accent2"]}" stroke-width="1" stroke-dasharray="4 4"/>')
    # axes
    s.append(f'<line x1="{cx0}" y1="{cy0+R}" x2="{cx0}" y2="{cy0-R-14}" stroke="{C["ink"]}" stroke-width="1.4"/>')
    s.append(f'<line x1="{cx0-R-12}" y1="{cy0}" x2="{cx0+R+12}" y2="{cy0}" stroke="{C["ink"]}" stroke-width="1.4"/>')
    ax, ay = 0.62 * R, 0.30 * R
    s.append(f'<line x1="{cx0+ax}" y1="{cy0-ay}" x2="{cx0-ax}" y2="{cy0+ay}" stroke="{C["ink"]}" '
             f'stroke-width="1.2" stroke-dasharray="3 3"/>')
    s.append(_txt(cx0, cy0 - R - 20, '|0&#10217;   (+z)', 12.5, C['ink']))
    s.append(_txt(cx0, cy0 + R + 20, '|1&#10217;   (&#8722;z)', 12.5, C['ink']))
    s.append(_txt(cx0 + R + 30, cy0 + 5, '|+&#10217; (x)', 12.5, C['ink']))
    s.append(_txt(cx0 - R - 30, cy0 + 5, '|&#8722;&#10217;', 12.5, C['ink']))
    s.append(_txt(cx0 - ax - 26, cy0 + ay + 6, '|+i&#10217; (y)', 12, C['muted']))
    for th, ph, lab, col in vectors:
        t, pp = math.radians(th), math.radians(ph)
        X = math.sin(t) * math.cos(pp)
        Y = math.sin(t) * math.sin(pp)
        Z = math.cos(t)
        px = cx0 + R * (X - 0.42 * Y)
        py = cy0 - R * (Z - 0.30 * Y)
        s.append(f'<line x1="{cx0}" y1="{cy0}" x2="{px:.1f}" y2="{py:.1f}" stroke="{col}" stroke-width="2.6"/>')
        s.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{col}"/>')
        # label at 60% along the vector, offset perpendicular to it, to avoid the axis captions
        dxv, dyv = px - cx0, py - cy0
        L = math.hypot(dxv, dyv) or 1.0
        nx, ny = -dyv / L, dxv / L
        lx = cx0 + 0.60 * dxv + 15 * nx
        ly = cy0 + 0.60 * dyv + 15 * ny + 4
        s.append(_txt(lx, ly, lab, 12.5, col, weight='bold'))
    return ''.join(s)


def flow_svg(boxes, arrows, width=680, height=250, title=''):
    """boxes: list of (x, y, w, h, text, fill, stroke). arrows: list of (x1,y1,x2,y2,label)."""
    s = [f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
         '<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">'
         f'<path d="M0,0 L0,6 L9,3 z" fill="{C["muted"]}"/></marker></defs>']
    if title:
        s.append(_txt(width / 2, 18, title, 13, C['accent'], weight='bold'))
    for x1, y1, x2, y2, lab in arrows:
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{C["muted"]}" '
                 f'stroke-width="1.8" marker-end="url(#ah)"/>')
        if lab:
            s.append(_txt((x1 + x2) / 2, (y1 + y2) / 2 - 7, lab, 11.5, C['muted'], style='italic'))
    for x, y, w, h, text, fill, stroke in boxes:
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1.8"/>')
        lines = text.split('|')
        y_start = y + h / 2 - (len(lines) - 1) * 8 + 5
        for i, ln in enumerate(lines):
            s.append(_txt(x + w / 2, y_start + i * 16, ln, 12.5, stroke,
                          weight='bold' if i == 0 else 'normal'))
    return ''.join(s)


def nested_svg(layers, width=680, height=300, title=''):
    """layers: list of (label, colour) from outermost to innermost — nested rounded rectangles."""
    s = [f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>']
    if title:
        s.append(_txt(width / 2, 18, title, 13, C['accent'], weight='bold'))
    n = len(layers)
    for i, (lab, col) in enumerate(layers):
        pad = i * (min(width, height) * 0.055)
        x = 60 + pad
        y = 34 + pad * 0.62
        w = width - 120 - 2 * pad
        h = height - 56 - 1.24 * pad
        s.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="14" '
                 f'fill="none" stroke="{col}" stroke-width="2"/>')
        s.append(_txt(x + w / 2, y + 18, lab, 13, col, weight='bold'))
    return ''.join(s)


# ========================================================== interactive ======
JSXGRAPH_HEAD = (
    '<link rel="stylesheet" '
    'href="https://cdn.jsdelivr.net/npm/jsxgraph@1.9.2/distrib/jsxgraph.css">\n'
    '<script src="https://cdn.jsdelivr.net/npm/jsxgraph@1.9.2/distrib/jsxgraphcore.js"></script>')


def interactive(num, board_id, caption, body_js, aspect='3/2', max_width=620, hint=''):
    """A self-contained JSXGraph board: unique div id, explicit size, and a visible
    failure message if the drawing library cannot be loaded."""
    hint_html = (f'<p style="font-size:0.88rem;color:var(--primary);margin:0 0 10px 0;">'
                 f'<strong>Try it:</strong> {hint}</p>') if hint else ''
    return f'''
<figure class="viz" style="padding:16px 18px 12px 18px;">
  <div class="viz-title">Figure {num} · interactive</div>
  {hint_html}
  <div id="{board_id}" class="jxgbox" style="width:100%;max-width:{max_width}px;
       aspect-ratio:{aspect};margin:0 auto;background:#ffffff;
       border:1px solid var(--color-rule);border-radius:8px;"></div>
  <div id="{board_id}_err" style="display:none;font-size:0.9rem;color:var(--warn-fg);padding:10px;">
    The interactive figure could not load. The static figures carry the same information.</div>
  <figcaption style="font-size:0.9rem;color:var(--color-muted);line-height:1.65;
       margin-top:10px;text-align:left;">{caption}</figcaption>
</figure>
<script>
(function () {{
  if (typeof JXG === 'undefined') {{
    var e = document.getElementById('{board_id}_err');
    if (e) {{ e.style.display = 'block'; }}
    return;
  }}
{body_js}
}})();
</script>'''


MATHJAX = '''
<script>
if (!window.MathJax) {
  window.MathJax = {tex: {inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']]},
                    options: {skipHtmlTags: ['script','noscript','style','textarea','pre']}};
  var s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
  s.async = true; document.head.appendChild(s);
}
</script>'''


def build_course_html(ch):
    """ch: chapter dict. Returns full HTML string."""
    parts = [h_title(ch['no'], ch['title'], ch['subtitle']),
             h_prereq(ch['prereq']),
             h_objectives(ch['objectives'])]
    for i, (heading, body) in enumerate(ch['sections'], 1):
        parts.append(h_section(i, heading, body))
    if ch.get('summary'):
        parts.append(box('note', 'Chapter summary', ch['summary']))
    parts.append(h_references(ch['references']))
    inner = '\n'.join(parts)
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chapter {ch['no']} — {ch['title']}</title>
{JSXGRAPH_HEAD}</head>
<body style="margin:0;background:#ffffff;">
<div style="max-width:900px;margin:0 auto;padding:26px 20px 60px 20px;">
{inner}
</div>
{MATHJAX}
</body></html>
'''


# ========================================================== CodeRunner =======
def build_coderunner(questions, out_path):
    els = [cr_question(name=q['name'], qtext_html=q['qtext'], answer=q['answer'],
                       preload=q['preload'], testcases=q['tests']) for q in questions]
    xml_str = build_quiz_xml(els)
    rep = validate_xml(xml_str)
    if rep['errors']:
        raise SystemExit('CodeRunner XML errors: ' + '; '.join(rep['errors']))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    return rep


def cr_qtext(tag, title, context, task, example=''):
    ex = ''
    if example:
        esc = example.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        ex = (f'<div style="background:#fdf4ff;border:1px solid #e9d5ff;border-left:5px solid #9333ea;'
              f'border-radius:8px;padding:14px 20px;margin:14px 0;">'
              f'<pre style="color:#3b0764;font-family:{MONO};font-size:13.5px;margin:0;'
              f'background:none;border:none;">{esc}</pre></div>')
    return (f'<div style="background:{C["panel"]};border:1px solid {C["line"]};border-left:5px solid {C["gold"]};'
            f'border-radius:8px;padding:18px 24px;margin-bottom:18px;">'
            f'<p style="color:#92400e;font-family:{SERIF};font-size:13px;font-weight:bold;letter-spacing:2px;'
            f'text-transform:uppercase;margin:0 0 10px 0;">{tag} — {title}</p>'
            f'<p style="color:{C["ink"]};font-family:{SERIF};font-size:15px;line-height:1.8;margin:0;">{context}</p></div>'
            f'<p style="font-family:{SERIF};font-size:15px;color:{C["ink"]};line-height:1.8;">{task}</p>{ex}')


# =============================================================== STACK =======
STACK_INPUT = '''    <input>
      <name>{name}</name>
      <type>{type}</type>
      <tans>{tans}</tans>
      <boxsize>{boxsize}</boxsize>
      <strictsyntax>1</strictsyntax>
      <insertstars>0</insertstars>
      <syntaxhint>{syntaxhint}</syntaxhint>
      <syntaxattribute>0</syntaxattribute>
      <forbidwords></forbidwords>
      <allowwords></allowwords>
      <forbidfloat>{forbidfloat}</forbidfloat>
      <requirelowestterms>{lowestterms}</requirelowestterms>
      <checkanswertype>0</checkanswertype>
      <mustverify>1</mustverify>
      <showvalidation>1</showvalidation>
      <options></options>
    </input>
'''

STACK_PRT = '''    <prt>
      <name>{prt}</name>
      <value>{value}</value>
      <autosimplify>1</autosimplify>
      <feedbackstyle>1</feedbackstyle>
      <feedbackvariables>
        <text></text>
      </feedbackvariables>
      <firstnodename>0</firstnodename>
      <node>
        <name>0</name>
        <answertest>{answertest}</answertest>
        <sans>{sans}</sans>
        <tans>{tans}</tans>
        <testoptions>{testoptions}</testoptions>
        <quiet>0</quiet>
        <truescoremode>=</truescoremode>
        <truescore>1.0000000</truescore>
        <truepenalty></truepenalty>
        <truenextnode>-1</truenextnode>
        <trueanswernote>{prt}-1-T</trueanswernote>
        <truefeedback format="html">
          <text><![CDATA[{truefb}]]></text>
        </truefeedback>
        <falsescoremode>=</falsescoremode>
        <falsescore>0.0000000</falsescore>
        <falsepenalty></falsepenalty>
        <falsenextnode>-1</falsenextnode>
        <falseanswernote>{prt}-1-F</falseanswernote>
        <falsefeedback format="html">
          <text><![CDATA[{falsefb}]]></text>
        </falsefeedback>
      </node>
    </prt>
'''

STACK_QUESTION = '''  <question type="stack">
    <name>
      <text>{name}</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[{questiontext}]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text><![CDATA[{generalfeedback}]]></text>
    </generalfeedback>
    <defaultgrade>{defaultgrade}</defaultgrade>
    <penalty>0.1000000</penalty>
    <hidden>0</hidden>
    <idnumber></idnumber>
    <stackversion>
      <text>2024010100</text>
    </stackversion>
    <questionvariables>
      <text>{questionvariables}</text>
    </questionvariables>
    <specificfeedback format="html">
      <text><![CDATA[{specificfeedback}]]></text>
    </specificfeedback>
    <questionnote format="html">
      <text>{questionnote}</text>
    </questionnote>
    <questiondescription format="html">
      <text></text>
    </questiondescription>
    <questionsimplify>1</questionsimplify>
    <assumepositive>0</assumepositive>
    <assumereal>0</assumereal>
    <prtcorrect format="html">
      <text><![CDATA[<p>Correct answer, well done.</p>]]></text>
    </prtcorrect>
    <prtpartiallycorrect format="html">
      <text><![CDATA[<p>Your answer is partially correct.</p>]]></text>
    </prtpartiallycorrect>
    <prtincorrect format="html">
      <text><![CDATA[<p>Incorrect answer.</p>]]></text>
    </prtincorrect>
    <decimals>.</decimals>
    <scientificnotation>*10</scientificnotation>
    <multiplicationsign>dot</multiplicationsign>
    <sqrtsign>1</sqrtsign>
    <complexno>i</complexno>
    <inversetrig>cos-1</inversetrig>
    <logicsymbol>lang</logicsymbol>
    <matrixparens>[</matrixparens>
    <variantsselectionseed></variantsselectionseed>
{inputs}{prts}  </question>
'''


def stack_question(name, questiontext, generalfeedback, questionvariables,
                   questionnote, parts, defaultgrade='1.0000000'):
    """parts: list of dicts with keys
       input (ans1), prt (prt1), tans, type, boxsize, forbidfloat,
       lowestterms, syntaxhint, answertest, testoptions, truefb, falsefb, value
    """
    inputs, prts, fb = '', '', ''
    n = len(parts)
    for pt in parts:
        inputs += STACK_INPUT.format(
            name=pt['input'], type=pt.get('type', 'algebraic'), tans=pt['tans'],
            boxsize=pt.get('boxsize', 20), syntaxhint=pt.get('syntaxhint', ''),
            forbidfloat=pt.get('forbidfloat', 1), lowestterms=pt.get('lowestterms', 0))
        prts += STACK_PRT.format(
            prt=pt['prt'], value=pt.get('value', f'{1.0/n:.7f}'),
            answertest=pt.get('answertest', 'AlgEquiv'),
            sans=pt['input'], tans=pt['tans'],
            testoptions=pt.get('testoptions', ''),
            truefb=pt.get('truefb', '<p>Correct.</p>'),
            falsefb=pt.get('falsefb', '<p>Not correct — review the section above.</p>'))
        fb += f'<p>[[feedback:{pt["prt"]}]]</p>'
    return STACK_QUESTION.format(
        name=name, questiontext=questiontext, generalfeedback=generalfeedback,
        defaultgrade=defaultgrade,
        questionvariables=_xesc(questionvariables), questionnote=_xesc(questionnote),
        specificfeedback=fb, inputs=inputs, prts=prts)


def _xesc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build_stack(questions_xml, out_path):
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n' + ''.join(questions_xml) + '</quiz>\n'
    errors = []
    if ']]]]>' in xml_str:
        errors.append('CDATA break sequence ]]]]> found')
    if '<n>' in xml_str:
        errors.append('<n> tag found (should be <name>)')
    try:
        root = ET.fromstring(xml_str)
    except ET.ParseError as e:
        raise SystemExit(f'STACK XML not well formed: {e}')
    for i, q in enumerate(root.findall('question'), 1):
        for tag in ('name', 'questiontext', 'questionvariables', 'specificfeedback',
                    'questionnote', 'questiondescription', 'prtcorrect',
                    'prtpartiallycorrect', 'prtincorrect', 'questionsimplify'):
            if q.find(tag) is None:
                errors.append(f'Q{i}: <{tag}> missing')
        if not q.findall('input'):
            errors.append(f'Q{i}: no <input>')
        for prt in q.findall('prt'):
            for tag in ('name', 'value', 'autosimplify', 'feedbackstyle',
                        'feedbackvariables', 'firstnodename', 'node'):
                if prt.find(tag) is None:
                    errors.append(f'Q{i}: prt <{tag}> missing')
        qt = (q.find('questiontext/text').text or '') if q.find('questiontext/text') is not None else ''
        if '[[feedback:' in qt:
            errors.append(f'Q{i}: [[feedback:]] must not be in questiontext')
        for inp in q.findall('input'):
            if f'[[input:{inp.find("name").text}]]' not in qt:
                errors.append(f'Q{i}: missing [[input:{inp.find("name").text}]] placeholder')
    if errors:
        raise SystemExit('STACK XML errors: ' + '; '.join(errors))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    return {'questions': len(root.findall('question')), 'errors': []}


def stack_qtext(tag, title, body):
    return (f'<div style="background:{C["panel"]};border:1px solid {C["line"]};border-left:5px solid {C["accent"]};'
            f'border-radius:8px;padding:16px 22px;margin-bottom:14px;">'
            f'<p style="color:{C["accent"]};font-family:{SERIF};font-size:12.5px;font-weight:bold;'
            f'letter-spacing:2px;text-transform:uppercase;margin:0;">{tag} — {title}</p></div>{body}')


# ============================================================== driver =======
def emit_chapter(ch, root_dir):
    folder = os.path.join(root_dir, f"chapter{ch['no']:02d}-{ch['slug']}")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, 'course.html'), 'w', encoding='utf-8') as f:
        f.write(build_course_html(ch))
    cr = build_coderunner(ch['coderunner'], os.path.join(folder, 'exercises_coderunner.xml'))
    st = build_stack(ch['stack'], os.path.join(folder, 'exercises_stack.xml'))
    return folder, cr, st
