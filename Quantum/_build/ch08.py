# -*- coding: utf-8 -*-
"""Chapter 8 — Grover Search, Amplitude Amplification and Query Lower Bounds."""
from math import sin, asin, sqrt, pi, log10, floor
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, circuit_svg,
                    interactive, C, SERIF, MONO)

S1 = (
    p("Unstructured search: given oracle access to \\(f:\\{0,1\\}^{n}\\to\\{0,1\\}\\) with "
      "\\(M\\ge1\\) marked inputs among \\(N=2^{n}\\), find one. Classically "
      "\\(\\Theta(N/M)\\) queries are necessary and sufficient. Grover's algorithm uses "
      "\\(\\Theta(\\sqrt{N/M})\\) — a quadratic, not exponential, speed-up, and one that is "
      "provably optimal.")
    + box('def', 'Phase oracle',
          "\\(O_f|x\\rangle=(-1)^{f(x)}|x\\rangle\\). Given a standard bit oracle "
          "\\(|x\\rangle|b\\rangle\\mapsto|x\\rangle|b\\oplus f(x)\\rangle\\), set the ancilla to "
          "\\(|-\\rangle\\): phase kickback (Chapter 6) converts one into the other at no cost.")
    + p("Define \\(|\\psi\\rangle=H^{\\otimes n}|0\\rangle^{\\otimes n}\\), the uniform "
        "superposition, and the <em>diffusion operator</em> "
        "\\(D=2|\\psi\\rangle\\langle\\psi|-I\\), a reflection about \\(|\\psi\\rangle\\). The Grover "
        "iterate is \\(G=D\\,O_f\\): a reflection about the 'bad' subspace followed by a "
        "reflection about \\(|\\psi\\rangle\\).")
)

S2 = (
    p("The analysis is two-dimensional. Let "
      "\\(|\\text{good}\\rangle=\\tfrac1{\\sqrt M}\\sum_{f(x)=1}|x\\rangle\\) and "
      "\\(|\\text{bad}\\rangle=\\tfrac1{\\sqrt{N-M}}\\sum_{f(x)=0}|x\\rangle\\). Then "
      "\\(|\\psi\\rangle=\\sin\\theta\\,|\\text{good}\\rangle+\\cos\\theta\\,|\\text{bad}\\rangle\\) "
      "with \\(\\sin\\theta=\\sqrt{M/N}\\), and the span of these two vectors is invariant under "
      "\\(G\\).")
    + box('thm', 'Grover as a rotation',
          "On that plane, \\(G\\) acts as a rotation by \\(2\\theta\\). Hence "
          "\\(G^{k}|\\psi\\rangle=\\sin\\big((2k+1)\\theta\\big)|\\text{good}\\rangle+"
          "\\cos\\big((2k+1)\\theta\\big)|\\text{bad}\\rangle\\), and the success probability is "
          "\\(p_k=\\sin^{2}\\big((2k+1)\\theta\\big)\\).")
    + box('proof', '',
          "The product of two reflections in a plane, about lines at angle \\(\\alpha\\), is a "
          "rotation by \\(2\\alpha\\). \\(O_f\\) reflects about \\(|\\text{bad}\\rangle\\); \\(D\\) "
          "reflects about \\(|\\psi\\rangle\\); the angle between those axes is \\(\\theta\\). "
          "\\(\\blacksquare\\)")
    + p("Maximising \\(p_k\\) requires \\((2k+1)\\theta\\approx\\pi/2\\), i.e.")
    + eq(r"k_{\text{opt}} \;=\; \left\lfloor \frac{\pi}{4\theta} \right\rfloor "
         r"\;\approx\; \frac{\pi}{4}\sqrt{\frac{N}{M}} ,")
    + box('warn', 'Overcooking',
          "\\(p_k\\) is periodic. Running more iterations than \\(k_{\\text{opt}}\\) rotates past "
          "the target and <em>reduces</em> the success probability — unlike any classical search. "
          "If \\(M\\) is unknown, one cannot simply run 'long enough': the standard fix is the "
          "exponential-search schedule of Boyer–Brassard–Høyer–Tapp, which picks \\(k\\) uniformly "
          "from \\(\\{0,\\dots,\\lceil\\lambda^{j}\\rceil\\}\\) with \\(\\lambda=6/5\\) and still "
          "achieves \\(O(\\sqrt{N/M})\\) expected queries.")
)

S3 = (
    p("Nothing in the argument used the uniform superposition. Replace \\(H^{\\otimes n}\\) by any "
      "state-preparation unitary \\(A\\) with \\(A|0\\rangle=|\\psi\\rangle\\) and success amplitude "
      "\\(\\sin\\theta=\\|\\Pi_{\\text{good}}|\\psi\\rangle\\|\\).")
    + box('thm', 'Amplitude amplification (Brassard–Høyer–Mosca–Tapp 2002)',
          "With \\(Q=-A S_0 A^{\\dagger} S_f\\), where \\(S_0=I-2|0\\rangle\\langle0|\\) and "
          "\\(S_f\\) is the phase oracle, \\(O(1/\\sin\\theta)\\) applications of \\(Q\\) boost the "
          "success probability to \\(\\Theta(1)\\). This is a generic quadratic improvement over "
          "repeat-until-success, and it applies to any algorithm with a verifiable output.")
    + box('thm', 'Amplitude estimation',
          "Applying phase estimation (Chapter 6) to \\(Q\\), whose eigenvalues are "
          "\\(e^{\\pm2i\\theta}\\), yields an estimate \\(\\tilde a\\) of \\(a=\\sin^{2}\\theta\\) with "
          "\\(|\\tilde a-a|\\le 2\\pi\\frac{\\sqrt{a(1-a)}}{K}+\\frac{\\pi^{2}}{K^{2}}\\) using "
          "\\(K\\) applications of \\(Q\\). Setting \\(a\\) to a mean gives quadratically faster "
          "Monte Carlo estimation: \\(O(1/\\varepsilon)\\) instead of \\(O(1/\\varepsilon^{2})\\) "
          "samples. Counting the number of marked items is the special case "
          "\\(M=N\\sin^{2}\\theta\\).")
    + p("Grover-type speed-ups apply extremely widely — SAT, constraint satisfaction, collision "
        "finding, minimum finding, Monte Carlo integration, and preimage attacks on symmetric "
        "cryptography (which is why AES key lengths are doubled for post-quantum security). But "
        "the gain is quadratic, and the constant factors of fault tolerance are brutal: current "
        "estimates suggest Grover-based attacks are not practically threatening for "
        "well-parameterised symmetric primitives.")
)

S4 = (
    box('thm', 'BBBV optimality (Bennett–Bernstein–Brassard–Vazirani 1997)',
        "Any quantum algorithm that finds a marked item among \\(N\\) with bounded error using "
        "oracle access requires \\(\\Omega(\\sqrt N)\\) queries. Consequently \\(NP\\not\\subseteq "
        "BQP\\) relative to a random oracle, and Grover is optimal up to constants.")
    + box('proof', 'Hybrid argument, sketch',
          "Run the algorithm on the all-zero oracle and track the total 'query magnitude' each "
          "input \\(x\\) receives, \\(\\sum_t\\|\\Pi_x|\\phi_t\\rangle\\|^{2}\\). Its sum over "
          "\\(x\\) is at most \\(T\\), so some \\(x\\) receives at most \\(T/N\\). Flipping the "
          "oracle at that \\(x\\) changes the final state by \\(O(T/\\sqrt N)\\) in norm; to "
          "distinguish it we need that to be \\(\\Omega(1)\\), giving "
          "\\(T=\\Omega(\\sqrt N)\\). \\(\\blacksquare\\)")
    + p("Two general lower-bound techniques subsume this: the <em>polynomial method</em> "
        "(Beals–Buhrman–Cleve–Mosca–de Wolf), which bounds the degree of the acceptance "
        "polynomial, and the <em>adversary method</em> (Ambainis), later shown by the negative-weight "
        "generalisation to characterise quantum query complexity exactly up to constants "
        "(Reichardt). Both are standard graduate material and are the right tools for any "
        "'is my speed-up real?' question in the query model.")
)

S5 = (
    p("Quantum walks give speed-ups where the search space has structure. The discrete-time "
      "coined walk on a graph \\(G\\) alternates a coin unitary with a shift; the "
      "continuous-time walk is \\(e^{-iAt}\\) for the adjacency matrix \\(A\\).")
    + table(['Problem', 'Classical', 'Quantum', 'Technique'],
            [['Unstructured search', '\\(\\Theta(N)\\)', '\\(\\Theta(\\sqrt N)\\)', 'Grover'],
             ['Element distinctness', '\\(\\Theta(N)\\)', '\\(\\Theta(N^{2/3})\\)', 'Ambainis walk on Johnson graph'],
             ['Triangle finding', '\\(\\tilde O(n^{2})\\)', '\\(\\tilde O(n^{5/4})\\)', 'Learning graphs / walks'],
             ['Search on a 2-D grid', '\\(\\Theta(N)\\)', '\\(O(\\sqrt{N}\\log N)\\)', 'Spatial search'],
             ['Glued trees traversal', '\\(2^{\\Omega(n)}\\)', '\\(\\mathrm{poly}(n)\\)',
              'Continuous-time walk — a rare exponential separation']])
    + box('note', 'Where Grover-type speed-ups quietly fail',
          "Many claimed applications require loading \\(N\\) classical data items into "
          "superposition. A QRAM performing that in \\(O(\\mathrm{polylog}\\,N)\\) time is an "
          "additional, unbuilt hardware assumption; if data loading costs \\(\\Omega(N)\\), the "
          "quadratic gain evaporates. When evaluating a proposed speed-up, always ask: what is "
          "the input model, and who pays for state preparation?")
)

S6 = (
    code('''import numpy as np

def grover_operator(N, marked):
    """Explicit N x N Grover iterate G = D O_f."""
    O = np.eye(N, dtype=complex)
    for m in marked:
        O[m, m] = -1
    psi = np.full(N, 1 / np.sqrt(N), dtype=complex)
    D = 2 * np.outer(psi, psi.conj()) - np.eye(N, dtype=complex)
    return D @ O

def optimal_iterations(N, M):
    theta = np.arcsin(np.sqrt(M / N))
    return int(np.floor(np.pi / (4 * theta)))

N, marked = 16, [5]
G = grover_operator(N, marked)
psi = np.full(N, 1/np.sqrt(N), dtype=complex)
k = optimal_iterations(N, len(marked))
for _ in range(k):
    psi = G @ psi
print(k, round(float(abs(psi[5])**2), 4))     # 3  0.9613''',
         'Explicit Grover iterate — exact for the small N used in the exercises')
    + p("For large \\(N\\) never build the \\(N\\times N\\) matrix: the oracle is a sign flip on a "
        "sparse index set and the diffusion is "
        "\\(D|\\phi\\rangle=2\\bar\\phi\\,\\mathbf 1-|\\phi\\rangle\\) with \\(\\bar\\phi\\) the mean "
        "amplitude, both \\(O(N)\\) in time and memory — the 'inversion about the mean' picture.")
)

# =============================== figures, citations and added commentary =====
ROT_SVG = f'''
<rect x="0" y="0" width="680" height="330" fill="#ffffff"/>
<text x="340" y="20" font-family="{SERIF}" font-size="13" fill="{C['accent']}" text-anchor="middle" font-weight="bold">Grover as two reflections composing to a rotation by 2&#952;</text>
<line x1="70" y1="270" x2="620" y2="270" stroke="{C['ink']}" stroke-width="1.6"/>
<line x1="70" y1="270" x2="70" y2="52" stroke="{C['ink']}" stroke-width="1.6"/>
<text x="620" y="264" font-family="{SERIF}" font-size="12.5" fill="{C['muted']}" text-anchor="end">|bad&#10217;  (unmarked items)</text>
<text x="78" y="48" font-family="{SERIF}" font-size="12.5" fill="{C['muted']}" text-anchor="start">|good&#10217;  (the M marked items)</text>
<line x1="70" y1="270" x2="520" y2="228" stroke="#94a3b8" stroke-width="2.4"/>
<circle cx="520" cy="228" r="4.5" fill="#94a3b8"/>
<text x="530" y="224" font-family="{SERIF}" font-size="12.5" fill="#475569" text-anchor="start" font-weight="bold">|&#968;&#10217;, angle &#952;</text>
<line x1="70" y1="270" x2="500" y2="310" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="5 4"/>
<text x="150" y="322" font-family="{SERIF}" font-size="12" fill="#dc2626" text-anchor="start">O&#7584;|&#968;&#10217;: reflected about |bad&#10217;</text>
<line x1="70" y1="270" x2="470" y2="145" stroke="{C['accent']}" stroke-width="2.6"/>
<circle cx="470" cy="145" r="4.5" fill="{C['accent']}"/>
<text x="480" y="141" font-family="{SERIF}" font-size="12.5" fill="{C['accent']}" text-anchor="start" font-weight="bold">G|&#968;&#10217;, angle 3&#952;</text>
<line x1="70" y1="270" x2="360" y2="92" stroke="{C['gold']}" stroke-width="2.6"/>
<circle cx="360" cy="92" r="4.5" fill="{C['gold']}"/>
<text x="370" y="88" font-family="{SERIF}" font-size="12.5" fill="#92400e" text-anchor="start" font-weight="bold">G&#178;|&#968;&#10217;, angle 5&#952;</text>
<path d="M 210 257 A 145 145 0 0 0 200 232" fill="none" stroke="#475569" stroke-width="1.3"/>
<text x="222" y="240" font-family="{SERIF}" font-size="12" fill="#475569" text-anchor="start">&#952;</text>
<path d="M 190 236 A 130 130 0 0 0 168 196" fill="none" stroke="{C['accent']}" stroke-width="1.3"/>
<text x="196" y="206" font-family="{SERIF}" font-size="12" fill="{C['accent']}" text-anchor="start">2&#952;</text>
<rect x="70" y="86" width="272" height="86" rx="7" fill="{C['panel']}" stroke="{C['line']}"/>
<text x="82" y="108" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">sin &#952; = &#8730;(M/N):  each iteration advances</text>
<text x="82" y="128" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">the state by exactly 2&#952; toward |good&#10217;.</text>
<text x="82" y="150" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">After k steps the angle is (2k+1)&#952;, so</text>
<text x="82" y="166" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">p&#8342; = sin&#178;((2k+1)&#952;).</text>
'''

GROVER_CIRCUIT = circuit_svg(
    3,
    [[('g', 0, 'H'), ('g', 1, 'H'), ('g', 2, 'H')],
     [('multi', 0, 2, 'O_f')],
     [('multi', 0, 2, 'D')],
     [('multi', 0, 2, 'O_f')],
     [('multi', 0, 2, 'D')],
     [('m', 0), ('m', 1), ('m', 2)]],
    wire_labels=['|0⟩', '|0⟩', '|0⟩'], width=620,
    title='Grover: uniform superposition, then k rounds of oracle + diffusion, then measure')


def _pk(N, M, k):
    th = asin(sqrt(M / N))
    return sin((2 * k + 1) * th) ** 2


_ks = list(range(0, 61))
OVERCOOK = line_chart(
    [dict(label='N = 1024, M = 1', xs=_ks, ys=[_pk(1024, 1, k) for k in _ks], color='#026573'),
     dict(label='N = 256,  M = 1', xs=_ks, ys=[_pk(256, 1, k) for k in _ks], color='#c9a227'),
     dict(label='N = 1024, M = 4', xs=_ks, ys=[_pk(1024, 4, k) for k in _ks], color='#9333ea')],
    xlim=(0, 60), ylim=(0, 1.05), xlabel='number of Grover iterations  k',
    ylabel='probability of finding a marked item',
    vlines=[(25, 'k_opt for N=1024, M=1', '#475569')],
    hlines=[(1.0, '', '#dc2626')], height=340)

_Ns = [2 ** e for e in range(4, 41)]
SCALING = line_chart(
    [dict(label='classical search:  N/2 queries on average', xs=[log10(N) for N in _Ns],
          ys=[log10(N / 2) for N in _Ns], color='#dc2626'),
     dict(label='Grover:  (π/4)√N queries', xs=[log10(N) for N in _Ns],
          ys=[log10(pi / 4 * sqrt(N)) for N in _Ns], color='#026573'),
     dict(label='BBBV lower bound:  Ω(√N)', xs=[log10(N) for N in _Ns],
          ys=[log10(sqrt(N)) for N in _Ns], color='#9333ea', dash='6 4')],
    xlim=(1, 12), ylim=(0, 12), xticks=[1,3,6,9,12], yticks=[0,3,6,9,12],
    xlabel='log₁₀ N   (size of the search space)',
    ylabel='log₁₀ (queries)',
    vlines=[(round(log10(2 ** 128), 1), 'AES-128 key space', '#475569')], height=330)

JS_GROVER = """
  var b = JXG.JSXGraph.initBoard('ch8grov', {boundingbox: [-9, 1.22, 92, -0.30],
      axis: false, showCopyright: false, showNavigation: false});
  var nS = b.create('slider', [[2, 1.14], [34, 1.14], [4, 10, 16]],
      {name: 'n  (N = 2&#8319;)', snapWidth: 1, strokeColor: '#026573'});
  var mS = b.create('slider', [[48, 1.14], [80, 1.14], [1, 1, 16]],
      {name: 'M marked', snapWidth: 1, strokeColor: '#c9a227'});
  b.create('line', [[0, 0], [90, 0]], {strokeColor: '#0f172a', strokeWidth: 1.4,
      straightFirst: false, straightLast: false, fixed: true});
  b.create('line', [[0, 0], [0, 1]], {strokeColor: '#0f172a', strokeWidth: 1.4,
      straightFirst: false, straightLast: false, fixed: true});
  b.create('line', [[0, 1], [90, 1]], {strokeColor: '#94a3b8', dash: 2,
      straightFirst: false, straightLast: false, fixed: true});
  function theta() {
      var N = Math.pow(2, Math.round(nS.Value()));
      var M = Math.round(mS.Value());
      return Math.asin(Math.sqrt(M / N));
  }
  b.create('functiongraph', [function (k) {
      var s = Math.sin((2 * k + 1) * theta());
      return s * s;
  }, 0, 90], {strokeColor: '#026573', strokeWidth: 2.6});
  var kopt = b.create('point', [
      function () { return Math.floor(Math.PI / (4 * theta())); },
      function () {
          var k = Math.floor(Math.PI / (4 * theta()));
          var s = Math.sin((2 * k + 1) * theta());
          return s * s;
      }], {name: '', size: 4, strokeColor: '#dc2626', fillColor: '#dc2626', fixed: true});
  b.create('text', [0, -0.13, function () {
      var N = Math.pow(2, Math.round(nS.Value()));
      var M = Math.round(mS.Value());
      var k = Math.floor(Math.PI / (4 * theta()));
      var s = Math.sin((2 * k + 1) * theta());
      return 'N = ' + N + ',  M = ' + M + '  \\u2192  k_opt = ' + k +
             ',  success = ' + (s * s).toFixed(4) +
             ',  classical average = ' + Math.round(N / (M + 1)) + ' queries';
  }], {fontSize: 13.5, strokeColor: '#0f172a'});
  b.create('text', [0, -0.245, 'horizontal axis: number of iterations k'],
      {fontSize: 12, strokeColor: '#475569'});
"""

S1 = S1 + figure(
    '8.1',
    'Grover’s algorithm as a circuit. After a layer of Hadamards the same two-block pattern repeats: '
    'the oracle O_f flips the sign of marked basis states, and the diffusion operator D = 2|ψ⟩⟨ψ| − I '
    'reflects about the uniform superposition. Both blocks are drawn as multi-qubit boxes because '
    'their internal structure depends on the problem; the diffusion is always H^⊗n, a phase flip on '
    '|0…0⟩, and H^⊗n again.',
    GROVER_CIRCUIT, width=620, height=236) + sources(
    'The algorithm: Grover' + cite('1') + '; the phase-oracle convention and its equivalence to a '
    'bit oracle: Nielsen &amp; Chuang §6.1.')

S2 = S2 + figure(
    '8.2',
    'The geometry that makes the analysis two-dimensional. The start state makes an angle θ with the '
    '“bad” axis, where sin θ = √(M/N). The oracle reflects it about the bad axis (red, downwards); '
    'the diffusion reflects the result about the start state; the composition is a rotation by 2θ '
    'toward the good axis. Every subsequent iteration repeats the same rotation, so the state simply '
    'sweeps around the circle at constant angular speed.',
    ROT_SVG, height=330) + figure(
    '8.3',
    'Success probability against the number of iterations. It is periodic, not monotone: continuing '
    'past the optimum rotates the state past the good axis and the probability falls back toward '
    'zero. More marked items (purple) mean a larger θ and therefore a shorter, faster cycle. This '
    'behaviour has no classical analogue and is the main practical pitfall of the algorithm.',
    OVERCOOK, height=340) + interactive(
    '8.4', 'ch8grov',
    'Set the size of the search space and the number of marked items, and read off the optimal '
    'iteration count and the resulting success probability. Two experiments are worth doing: '
    'quadruple N and watch k_opt double, confirming the √N scaling; and increase M with N fixed and '
    'watch k_opt fall as √(N/M). The printed classical figure is the expected number of queries a '
    'random classical search would need.',
    JS_GROVER, aspect='16/9', max_width=660,
    hint='drag n and M to resize the problem.') + p(
    "The periodicity has a concrete algorithmic consequence when \\(M\\) is unknown, since "
    "\\(k_{\\text{opt}}\\) then cannot be computed in advance. The standard remedy, due to Boyer, "
    "Brassard, Høyer and Tapp, is an exponential schedule: run the algorithm with \\(k\\) chosen "
    "uniformly from \\(\\{0,\\dots,\\lceil\\lambda^{j}\\rceil\\}\\) for \\(j=0,1,2,\\dots\\) with "
    "\\(\\lambda=6/5\\), checking the output each time" + cite('2') + ". The expected number of "
    "oracle calls remains \\(O(\\sqrt{N/M})\\), and the same schedule handles the case \\(M=0\\) "
    "gracefully. Alternatively, one can first estimate \\(M\\) by quantum counting (§3) and then run "
    "a single optimally sized search.") + sources(
    'The rotation analysis and optimal k: Grover' + cite('1') + ', Boyer et al.' + cite('2') + '.')

S3 = S3 + sources(
    'Amplitude amplification and estimation, with the error bound quoted here: '
    'Brassard, Høyer, Mosca &amp; Tapp' + cite('3') + '.')

S4 = S4 + figure(
    '8.5',
    'Query cost against problem size, both axes logarithmic. Grover halves the exponent: a search '
    'space of 2¹²⁸ needs about 2⁶⁴ quantum queries instead of 2¹²⁷ classical ones. The purple line '
    'is the BBBV lower bound, which Grover matches to within a constant, so no quantum algorithm '
    'can do better in the black-box model. Halving the exponent is exactly why post-quantum guidance '
    'recommends doubling symmetric key lengths.',
    SCALING, height=330) + p(
    "It is worth reading the figure pessimistically as well as optimistically. A quadratic speed-up "
    "does not survive contact with fault tolerance as easily as an exponential one: the "
    "\\(2^{64}\\) quantum queries must each be executed as a sequence of error-corrected gates with "
    "the overheads of Chapter 9, and Grover parallelises poorly — running \\(P\\) machines in "
    "parallel gives only a \\(\\sqrt P\\) improvement, against \\(P\\) classically" + cite('4,8') +
    ". Careful estimates therefore conclude that a Grover attack on AES-128 is not practical even "
    "with a large fault-tolerant machine, and that the doubling rule is conservative rather than "
    "tight.") + sources(
    'The Ω(√N) bound: Bennett, Bernstein, Brassard &amp; Vazirani' + cite('4') + '; the polynomial '
    'method' + cite('7') + '; a modern critical survey of when speed-ups are real' + cite('8') + '.')

S5 = S5 + sources(
    'Element distinctness and the adversary method: Ambainis' + cite('5') + '; the glued-trees '
    'exponential separation: Childs et al.' + cite('6') + '; the QRAM caveat' + cite('8') + '.')

REFS = [
    dict(authors="L. K. Grover", title="A fast quantum mechanical algorithm for database search",
         venue="Proc. 28th STOC, 212–219", year="1996",
         link="https://arxiv.org/abs/quant-ph/9605043",
         note="The original algorithm."),
    dict(authors="M. Boyer, G. Brassard, P. Høyer and A. Tapp",
         title="Tight bounds on quantum searching",
         venue="Fortschritte der Physik 46, 493–505", year="1998",
         link="https://arxiv.org/abs/quant-ph/9605034",
         note="Unknown M, the exponential-search schedule, and matching bounds (§2)."),
    dict(authors="G. Brassard, P. Høyer, M. Mosca and A. Tapp",
         title="Quantum amplitude amplification and estimation",
         venue="AMS Contemporary Mathematics 305, 53–74", year="2002",
         link="https://arxiv.org/abs/quant-ph/0005055",
         note="The generalisation in §3, including counting and estimation."),
    dict(authors="C. H. Bennett, E. Bernstein, G. Brassard and U. Vazirani",
         title="Strengths and weaknesses of quantum computing",
         venue="SIAM Journal on Computing 26(5), 1510–1523", year="1997",
         link="https://arxiv.org/abs/quant-ph/9701001",
         note="The Ω(√N) lower bound of §4."),
    dict(authors="A. Ambainis", title="Quantum walk algorithm for element distinctness",
         venue="SIAM Journal on Computing 37(1), 210–239", year="2007",
         link="https://arxiv.org/abs/quant-ph/0311001",
         note="The N^{2/3} walk algorithm and the adversary lower-bound method."),
    dict(authors="A. M. Childs, R. Cleve, E. Deotto, E. Farhi, S. Gutmann and D. A. Spielman",
         title="Exponential algorithmic speedup by a quantum walk",
         venue="Proc. 35th STOC, 59–68", year="2003",
         link="https://arxiv.org/abs/quant-ph/0209131",
         note="The glued-trees problem: an exponential separation from a walk."),
    dict(authors="R. Beals, H. Buhrman, R. Cleve, M. Mosca and R. de Wolf",
         title="Quantum lower bounds by polynomials",
         venue="Journal of the ACM 48(4), 778–797", year="2001",
         note="The polynomial method referenced in §4."),
    dict(authors="S. Aaronson", title="How much structure is needed for huge quantum speedups?",
         venue="arXiv:2209.06930 (Solvay Conference lecture)", year="2022",
         link="https://arxiv.org/abs/2209.06930",
         note="A careful modern survey of when speed-ups are real, including the QRAM caveat of §5."),
]

CR = [
    dict(
        name='C8.Q1 — The Grover iterate and the optimal number of steps',
        qtext=cr_qtext('C8.Q1', 'Two reflections make a rotation',
                       "\\(G=D\\,O_f\\) rotates the state by \\(2\\theta\\) in the "
                       "good/bad plane, with \\(\\sin\\theta=\\sqrt{M/N}\\).",
                       "Write <code>grover_operator(N, marked)</code> returning the explicit "
                       "\\(N\\times N\\) iterate; <code>optimal_iterations(N, M)</code> returning "
                       "\\(\\lfloor\\pi/(4\\arcsin\\sqrt{M/N})\\rfloor\\) as an <code>int</code>; and "
                       "<code>success_probability(N, M, k)</code> returning "
                       "\\(\\sin^{2}((2k+1)\\theta)\\) rounded to 6 decimals.",
                       "optimal_iterations(1024, 1) -> 25\n"
                       "success_probability(16, 1, 3) -> 0.961319"),
        answer='''import numpy as np

def grover_operator(N, marked):
    O = np.eye(N, dtype=complex)
    for m in marked:
        O[m, m] = -1
    psi = np.full(N, 1 / np.sqrt(N), dtype=complex)
    D = 2 * np.outer(psi, psi.conj()) - np.eye(N, dtype=complex)
    return D @ O

def optimal_iterations(N, M):
    theta = np.arcsin(np.sqrt(M / N))
    return int(np.floor(np.pi / (4 * theta)))

def success_probability(N, M, k):
    theta = np.arcsin(np.sqrt(M / N))
    return round(float(np.sin((2 * k + 1) * theta) ** 2), 6)
''',
        preload='''import numpy as np

def grover_operator(N, marked):
    ...

def optimal_iterations(N, M):
    ...

def success_probability(N, M, k):
    ...
''',
        tests=[
            {'code': 'print(optimal_iterations(1024, 1), optimal_iterations(16, 1))\n',
             'expected': '25 3\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(success_probability(16, 1, 3))\n',
             'expected': '0.961319\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nG = grover_operator(8, [3])\n'
                     'print(np.allclose(G.conj().T @ G, np.eye(8)))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'print(success_probability(4, 1, 1))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(optimal_iterations(1000000, 1), success_probability(64, 4, 3))\n',
             'expected': '785 0.961319\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C8.Q2 — Running Grover, and overcooking it',
        qtext=cr_qtext('C8.Q2', 'The periodicity of the success probability',
                       "Because \\(G\\) is a rotation, iterating past \\(k_{\\text{opt}}\\) "
                       "<em>decreases</em> the success probability — a purely quantum failure "
                       "mode with no classical analogue.",
                       "Write <code>run_grover(N, marked, k)</code> returning the state after "
                       "\\(k\\) iterations starting from the uniform superposition, and "
                       "<code>marked_probability(psi, marked)</code> returning the total "
                       "probability on the marked indices, rounded to 6 decimals. Then "
                       "<code>best_k(N, marked, kmax)</code> returning the \\(k\\le k_{\\max}\\) "
                       "maximising that probability.",
                       "N=16, one marked: probabilities peak at k=3 and fall again by k=6"),
        answer='''import numpy as np

def _G(N, marked):
    O = np.eye(N, dtype=complex)
    for m in marked:
        O[m, m] = -1
    psi = np.full(N, 1 / np.sqrt(N), dtype=complex)
    return (2 * np.outer(psi, psi.conj()) - np.eye(N, dtype=complex)) @ O

def run_grover(N, marked, k):
    G = _G(N, marked)
    psi = np.full(N, 1 / np.sqrt(N), dtype=complex)
    for _ in range(k):
        psi = G @ psi
    return psi

def marked_probability(psi, marked):
    psi = np.asarray(psi, dtype=complex)
    return round(float(sum(abs(psi[m]) ** 2 for m in marked)), 6)

def best_k(N, marked, kmax):
    G = _G(N, marked)
    psi = np.full(N, 1 / np.sqrt(N), dtype=complex)
    best, bp = 0, marked_probability(psi, marked)
    for k in range(1, kmax + 1):
        psi = G @ psi
        pk = marked_probability(psi, marked)
        if pk > bp:
            best, bp = k, pk
    return best
''',
        preload='''import numpy as np

def run_grover(N, marked, k):
    ...

def marked_probability(psi, marked):
    ...

def best_k(N, marked, kmax):
    ...
''',
        tests=[
            {'code': 'print(marked_probability(run_grover(16, [5], 3), [5]))\n',
             'expected': '0.961319\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(best_k(16, [5], 5))\n',
             'expected': '3\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(marked_probability(run_grover(16, [5], 6), [5]) < '
                     'marked_probability(run_grover(16, [5], 3), [5]))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'print(marked_probability(run_grover(4, [2], 1), [2]))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(best_k(64, [1, 9, 17, 33], 5), '
                     'marked_probability(run_grover(64, [1,9,17,33], 3), [1,9,17,33]))\n',
             'expected': '3 0.961319\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C8.Q3 — Amplitude amplification with an arbitrary state preparation',
        qtext=cr_qtext('C8.Q3', 'Beyond the uniform superposition',
                       "Replace \\(H^{\\otimes n}\\) by any \\(A\\) with "
                       "\\(A|0\\rangle=|\\psi\\rangle\\). Then "
                       "\\(Q=-A S_0 A^{\\dagger} S_f\\) amplifies the good component at the same "
                       "quadratic rate, with \\(\\sin\\theta=\\|\\Pi_{\\text{good}}|\\psi\\rangle\\|\\).",
                       "Write <code>amplitude_amplification_operator(A, marked)</code> returning "
                       "\\(Q=-A S_0 A^{\\dagger} S_f\\) (with "
                       "\\(S_0=I-2|0\\rangle\\langle0|\\) and \\(S_f\\) the phase oracle), and "
                       "<code>amplify(A, marked, k)</code> returning the state after \\(k\\) "
                       "applications of \\(Q\\) to \\(A|0\\rangle\\).",
                       "With A = H^{tensor n} this reproduces the Grover iterate up to sign."),
        answer='''import numpy as np

def amplitude_amplification_operator(A, marked):
    A = np.asarray(A, dtype=complex)
    N = A.shape[0]
    S0 = np.eye(N, dtype=complex)
    S0[0, 0] = -1
    Sf = np.eye(N, dtype=complex)
    for m in marked:
        Sf[m, m] = -1
    return -A @ S0 @ A.conj().T @ Sf

def amplify(A, marked, k):
    A = np.asarray(A, dtype=complex)
    N = A.shape[0]
    e0 = np.zeros(N, dtype=complex)
    e0[0] = 1
    psi = A @ e0
    Q = amplitude_amplification_operator(A, marked)
    for _ in range(k):
        psi = Q @ psi
    return psi
''',
        preload='''import numpy as np

def amplitude_amplification_operator(A, marked):
    ...

def amplify(A, marked, k):
    ...
''',
        tests=[
            {'code': '''import numpy as np
H = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)
A = np.array([[1.0+0j]])
for _ in range(4):
    A = np.kron(A, H)
print(round(float(abs(amplify(A, [5], 0)[5])**2), 6))
''',
             'expected': '0.0625\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
H = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)
A = np.array([[1.0+0j]])
for _ in range(4):
    A = np.kron(A, H)
psi = amplify(A, [5], 3)
print(round(float(abs(psi[5])**2), 6))
''',
             'expected': '0.961319\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
H = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)
A = np.array([[1.0+0j]])
for _ in range(3):
    A = np.kron(A, H)
Q = amplitude_amplification_operator(A, [2])
print(np.allclose(Q.conj().T @ Q, np.eye(8)))
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
rng = np.random.default_rng(6)
M = rng.normal(size=(8,8)) + 1j*rng.normal(size=(8,8))
A, _ = np.linalg.qr(M)
psi0 = amplify(A, [3], 0)
psi1 = amplify(A, [3], 1)
print(abs(psi1[3])**2 > abs(psi0[3])**2)
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': '''import numpy as np
H = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)
A = np.array([[1.0+0j]])
for _ in range(2):
    A = np.kron(A, H)
print(round(float(abs(amplify(A, [1], 1)[1])**2), 6))
''',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C8.Q4 — Quantum counting by amplitude estimation',
        qtext=cr_qtext('C8.Q4', 'Estimating M without finding a marked item',
                       "The Grover iterate has eigenvalues \\(e^{\\pm2i\\theta}\\) on the "
                       "good/bad plane. Phase estimation on \\(G\\) therefore returns "
                       "\\(\\theta\\), and \\(M=N\\sin^{2}\\theta\\).",
                       "Write <code>grover_angle(N, M)</code> returning "
                       "\\(\\theta=\\arcsin\\sqrt{M/N}\\); "
                       "<code>counting_estimate(N, y, t)</code> returning the estimate "
                       "\\(N\\sin^{2}(\\pi y/2^{t})\\) rounded to 4 decimals; and "
                       "<code>counting_error_bound(N, M, t)</code> returning the worst-case "
                       "bound \\(2\\pi\\sqrt{M(N-M)}/2^{t}+\\pi^{2}N/4^{t}\\), rounded to 4 "
                       "decimals.",
                       "N=256, M=4  ->  theta ~ 0.1253\n"
                       "counting_estimate(256, 5, 6) -> 15.1141"),
        answer='''import numpy as np

def grover_angle(N, M):
    return float(np.arcsin(np.sqrt(M / N)))

def counting_estimate(N, y, t):
    return round(float(N * np.sin(np.pi * y / 2 ** t) ** 2), 4)

def counting_error_bound(N, M, t):
    K = 2 ** t
    return round(float(2 * np.pi * np.sqrt(M * (N - M)) / K + np.pi ** 2 * N / K ** 2), 4)
''',
        preload='''import numpy as np

def grover_angle(N, M):
    ...

def counting_estimate(N, y, t):
    ...

def counting_error_bound(N, M, t):
    ...
''',
        tests=[
            {'code': 'print(round(grover_angle(256, 4), 4))\n',
             'expected': '0.1253\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(counting_estimate(256, 5, 6))\n',
             'expected': '15.1141\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(counting_estimate(1024, 0, 8), round(grover_angle(16, 16), 4))\n',
             'expected': '0.0 1.5708\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'print(counting_error_bound(1024, 16, 10) < counting_error_bound(1024, 16, 8))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(counting_error_bound(256, 4, 8))\n',
             'expected': '0.8178\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

ST = [
    stack_question(
        name='C8.S1 — Iteration count and success probability',
        questiontext=stack_qtext(
            'C8.S1', 'Sizing a Grover search',
            r'<p>Let \(N=2^{ {@n@} }\) and let there be \(M={@M@}\) marked items. Write '
            r'\(\theta=\arcsin\sqrt{M/N}\).</p>'
            r'<p>(a) Give the success probability after \(k\) iterations, as a function of '
            r'<code>k</code> and <code>theta</code>.</p>'
            r'<p>\(p_k=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the leading-order optimal number of iterations '
            r'(ignoring the floor), in terms of <code>N</code> and <code>M</code>.</p>'
            r'<p>\(k_{\mathrm{opt}}\approx\) [[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Evaluate that expression numerically for the values above '
            r'(exact expression, no decimals).</p>'
            r'<p>[[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) \(G\) rotates by \(2\theta\) in the good/bad plane starting at angle \(\theta\), '
            r'so after \(k\) steps the good amplitude is \(\sin((2k+1)\theta)\) and '
            r'\(p_k=\sin^{2}((2k+1)\theta)\).</p>'
            r'<p>(b) Solving \((2k+1)\theta=\pi/2\) gives \(k=\frac{\pi}{4\theta}-\frac12\); for '
            r'\(M\ll N\), \(\theta\approx\sqrt{M/N}\) and '
            r'\(k_{\mathrm{opt}}\approx\frac{\pi}{4}\sqrt{N/M}\).</p>'
            r'<p>(c) With \(N=2^{ {@n@} }\) and \(M={@M@}\): \(k\approx{@ta3@}\).</p>'
            r'<p>Note \(p_k\) is periodic in \(k\): running too long rotates past the target and '
            r'lowers the success probability. This is why the number of iterations must be chosen '
            r'in advance, and why unknown \(M\) requires the BBHT exponential schedule.</p>'),
        questionvariables=('n : rand_with_step(8,16,2);\nM : rand_with_step(1,4,1);\n'
                           'ta1 : sin((2*k+1)*theta)^2;\n'
                           'ta2 : %pi/4*sqrt(N/M);\n'
                           'ta3 : %pi/4*sqrt(2^n/M);'),
        questionnote='n={@n@}, M={@M@}, k={@ta3@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=24, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>The state after \(k\) steps makes angle \((2k+1)\theta\) with \(|\text{bad}\rangle\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=20, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Set \((2k+1)\theta\approx\pi/2\) and use \(\theta\approx\sqrt{M/N}\).</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=20, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb='<p>Substitute the given \\(N\\) and \\(M\\).</p>')]),
    stack_question(
        name='C8.S2 — Two reflections, one rotation',
        questiontext=stack_qtext(
            'C8.S2', 'The geometry of the Grover iterate',
            r'<p>(a) The product of reflections about two lines meeting at angle \(\alpha\) is a '
            r'rotation. Give the rotation angle in terms of <code>alpha</code>.</p>'
            r'<p>[[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the two eigenvalues of the Grover iterate restricted to the good/bad '
            r'plane, as an ordered list, in terms of <code>theta</code> '
            r'(use <code>%e</code> and <code>%i</code>).</p>'
            r'<p>[[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Amplitude estimation with \(K\) applications of \(G\) estimates '
            r'\(a=\sin^2\theta\) to additive error scaling as \(K^{-\gamma}\) at leading order. '
            r'Give \(\gamma\).</p>'
            r'<p>\(\gamma=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) \(2\alpha\). Applied with \(\alpha=\theta\) (the angle between '
            r'\(|\text{bad}\rangle\) and \(|\psi\rangle\)) this gives the \(2\theta\) rotation per '
            r'Grover step.</p>'
            r'<p>(b) A planar rotation by \(2\theta\) has eigenvalues \(e^{\pm 2i\theta}\).</p>'
            r'<p>(c) \(\gamma=1\): the error is \(O(1/K)\), quadratically better than the '
            r'\(O(1/\sqrt K)\) of classical Monte Carlo. This is the same Heisenberg scaling as '
            r'phase estimation in Chapter 6 — unsurprising, since amplitude estimation <em>is</em> '
            r'phase estimation applied to \(G\).</p>'),
        questionvariables='ta1 : 2*alpha;\nta2 : [exp(2*%i*theta), exp(-2*%i*theta)];\nta3 : 1;',
        questionnote='2alpha, e^{+-2i theta}, gamma=1',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>Compose the two reflection matrices.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=30, value='0.3333333',
                 forbidfloat=0,
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>A rotation by \(2\theta\) in a plane has eigenvalues \(e^{\pm2i\theta}\).</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=6, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb='<p>Compare with classical Monte Carlo error \\(O(1/\\sqrt K)\\).</p>')]),
    stack_question(
        name='C8.S3 — Optimality and what a quadratic speed-up buys',
        questiontext=stack_qtext(
            'C8.S3', 'Lower bounds and cryptographic consequences',
            r'<p>(a) Give the BBBV lower bound on the number of oracle queries needed to search '
            r'\(N\) items with bounded error, as a function of <code>N</code> '
            r'(give the growth rate, e.g. <code>sqrt(N)</code>).</p>'
            r'<p>[[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) A symmetric cipher has a \(b\)-bit key. Give the number of Grover iterations '
            r'needed for exhaustive key search, in terms of <code>b</code> '
            r'(leading order, ignoring the \(\pi/4\)).</p>'
            r'<p>[[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Give the key length \(b\) needed so that a Grover attack costs at least '
            r'\(2^{ {@s@} }\) iterations.</p>'
            r'<p>\(b=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) \(\Omega(\sqrt N)\), by the hybrid argument: after \(T\) queries the algorithm '
            r'can only have distinguished the flipped oracle if \(T=\Omega(\sqrt N)\). Grover '
            r'matches it, so unstructured search is settled up to constants.</p>'
            r'<p>(b) \(N=2^{b}\), so \(\sqrt N=2^{b/2}\) iterations.</p>'
            r'<p>(c) \(2^{b/2}\ge 2^{ {@s@} }\) requires \(b\ge {@ta3@}\).</p>'
            r'<p>This is the origin of the "double your symmetric key length" rule for post-quantum '
            r'security: AES-256 retains roughly 128 bits of security against Grover. Note the rule '
            r'is conservative — Grover parallelises badly, and the fault-tolerant constant factors '
            r'are enormous, so the effective margin is larger than the bare exponent suggests.</p>'),
        questionvariables='s : rand_with_step(64,160,32);\nta1 : sqrt(N);\nta2 : 2^(b/2);\nta3 : 2*s;',
        questionnote='s={@s@}, b={@ta3@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>Grover is optimal, so the bound matches its cost.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>Substitute \\(N=2^{b}\\) into \\(\\sqrt N\\).</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=8, value='0.3333333',
                 truefb='<p>Correct — hence "double the key length".</p>',
                 falsefb='<p>Solve \\(2^{b/2}\\ge 2^{s}\\).</p>')]),
]

CHAPTER = dict(
    no=8, slug='grover-and-amplitude-amplification',
    title='Grover Search, Amplitude Amplification and Query Lower Bounds',
    subtitle='Unstructured search as a rotation, optimal iteration counts and overcooking, '
             'amplitude amplification and estimation, the BBBV optimality proof, and quantum walks.',
    prereq='Chapters 1–3 and Chapter 6 (phase kickback, phase estimation).',
    objectives=[
        'Construct the phase oracle and diffusion operator and prove G is a rotation by 2θ.',
        'Compute the optimal iteration count and explain why more iterations can hurt.',
        'Generalise to amplitude amplification with an arbitrary state preparation.',
        'Use amplitude estimation for counting and for quadratically faster Monte Carlo.',
        'Reproduce the BBBV Ω(√N) hybrid argument and name the two general lower-bound methods.',
        'Assess when a claimed Grover speed-up survives the input/QRAM model.',
    ],
    sections=[
        ('Unstructured search and the phase oracle', S1),
        ('Grover as a rotation in a two-dimensional plane', S2),
        ('Amplitude amplification and amplitude estimation', S3),
        ('Optimality: the BBBV lower bound', S4),
        ('Quantum walks and structured search', S5),
        ('Numerical practice', S6),
    ],
    summary="Grover's algorithm is two reflections composing to a rotation by \\(2\\theta\\) in a "
            "two-dimensional invariant plane, giving \\(\\Theta(\\sqrt{N/M})\\) queries — provably "
            "optimal by BBBV. The construction generalises to amplitude amplification for any "
            "verifiable algorithm and, through amplitude estimation, to quadratically faster "
            "counting and Monte Carlo. Quantum walks extend the toolkit to structured problems "
            "and even, in the glued-trees case, to an exponential separation. The recurring "
            "caveat is the input model: a speed-up that assumes free QRAM may not be a speed-up "
            "at all.",
    references=REFS, coderunner=CR, stack=ST,
)
