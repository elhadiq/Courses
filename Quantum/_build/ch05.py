# -*- coding: utf-8 -*-
"""Chapter 5 — Density Operators, Open Systems and Quantum Channels."""
from math import exp, log2, sqrt
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, flow_svg,
                    circuit_svg, interactive, C, SERIF, MONO)

S1 = (
    p("Pure states are insufficient for two reasons: we may be ignorant of which state was "
      "prepared, and a subsystem of an entangled pure state has no state vector of its own. "
      "Both are handled by the density operator.")
    + box('def', 'Density operator',
          "A density operator is \\(\\rho\\in\\mathcal B(\\mathcal H)\\) with \\(\\rho=\\rho^{\\dagger}\\), "
          "\\(\\rho\\ge0\\) and \\(\\operatorname{tr}\\rho=1\\). It is <em>pure</em> if "
          "\\(\\rho^{2}=\\rho\\) (equivalently \\(\\rho=|\\psi\\rangle\\langle\\psi|\\)), and "
          "<em>mixed</em> otherwise. The set of density operators is convex and compact; its "
          "extreme points are exactly the pure states.")
    + p("All postulates carry over: \\(\\rho\\mapsto U\\rho U^{\\dagger}\\), "
        "\\(p(k)=\\operatorname{tr}(P_k\\rho)\\), \\(\\langle A\\rangle=\\operatorname{tr}(A\\rho)\\), "
        "and post-measurement \\(\\rho\\mapsto P_k\\rho P_k/p(k)\\). For a qubit, expanding in the "
        "Pauli basis gives the Bloch ball:")
    + eq(r"\rho \;=\; \tfrac12\big(I + \vec r\cdot\vec\sigma\big), \qquad \|\vec r\|\le1, \qquad "
         r"\operatorname{tr}\rho^{2}=\tfrac12(1+\|\vec r\|^{2}) .")
    + box('warn', 'The ensemble is not recoverable from \\(\\rho\\)',
          "The uniform mixture of \\(|0\\rangle,|1\\rangle\\) and the uniform mixture of "
          "\\(|+\\rangle,|-\\rangle\\) are both \\(I/2\\). No measurement can distinguish them: "
          "\\(\\rho\\) contains all physically accessible information, and different ensembles "
          "yielding the same \\(\\rho\\) are operationally identical. (The unitary freedom is "
          "characterised by the Hughston–Jozsa–Wootters theorem.)")
)

S2 = (
    p("The state of a subsystem is obtained by the partial trace, the unique linear map "
      "satisfying \\(\\operatorname{tr}\\big[(A\\otimes I)\\rho_{AB}\\big]="
      "\\operatorname{tr}\\big[A\\,\\rho_A\\big]\\) for all \\(A\\) — i.e. the unique map that "
      "reproduces all local measurement statistics.")
    + eq(r"\rho_A \;=\; \operatorname{tr}_B \rho_{AB} \;=\; \sum_j (I\otimes\langle j|)\,\rho_{AB}\,(I\otimes|j\rangle)")
    + p("For the Bell state \\(|\\Phi^{+}\\rangle\\), \\(\\rho_A=I/2\\): a maximally entangled pure "
        "state has maximally mixed marginals. This is the precise sense in which entanglement "
        "\"hides\" information in correlations rather than in the parts.")
    + box('thm', 'Purification',
          "For any \\(\\rho_A\\) on \\(\\mathcal H_A\\) there is a pure "
          "\\(|\\psi\\rangle\\in\\mathcal H_A\\otimes\\mathcal H_R\\) with "
          "\\(\\operatorname{tr}_R|\\psi\\rangle\\langle\\psi|=\\rho_A\\), and "
          "\\(\\dim\\mathcal H_R=\\operatorname{rank}\\rho_A\\) suffices. Any two purifications of "
          "the same \\(\\rho_A\\) differ by an isometry on \\(R\\). Concretely, from a spectral "
          "decomposition \\(\\rho_A=\\sum_k p_k|a_k\\rangle\\langle a_k|\\), take "
          "\\(|\\psi\\rangle=\\sum_k\\sqrt{p_k}|a_k\\rangle|k\\rangle\\).")
    + p("Purification is the technical engine of the whole chapter: every mixed state is a pure "
        "state on a larger space, every channel is a unitary on a larger space, and every POVM "
        "is a projective measurement on a larger space. This is often called the \"church of the "
        "larger Hilbert space\".")
)

S3 = (
    p("Open-system dynamics — anything involving an environment — is described by a quantum "
      "channel: a linear map \\(\\mathcal E:\\mathcal B(\\mathcal H_A)\\to\\mathcal B(\\mathcal H_B)\\) that "
      "is completely positive and trace preserving (CPTP). Complete positivity (rather than "
      "mere positivity) is required because \\(\\mathcal E\\otimes\\mathrm{id}\\) must map states "
      "to states when the input is entangled with a spectator; transposition is the standard "
      "counterexample, and its failure is exactly the PPT criterion of Chapter 4.")
    + box('thm', 'Kraus / Stinespring / Choi — three equivalent pictures',
          "For a linear map \\(\\mathcal E\\) the following are equivalent: "
          "(i) \\(\\mathcal E\\) is CPTP; "
          "(ii) <strong>Kraus</strong>: \\(\\mathcal E(\\rho)=\\sum_k K_k\\rho K_k^{\\dagger}\\) with "
          "\\(\\sum_k K_k^{\\dagger}K_k=I\\); "
          "(iii) <strong>Stinespring</strong>: \\(\\mathcal E(\\rho)="
          "\\operatorname{tr}_E\\big[U(\\rho\\otimes|0\\rangle\\langle0|_E)U^{\\dagger}\\big]\\) for some "
          "isometry/unitary \\(U\\); "
          "(iv) <strong>Choi</strong>: the Choi matrix "
          "\\(J(\\mathcal E)=(\\mathrm{id}\\otimes\\mathcal E)\\big(|\\Omega\\rangle\\langle\\Omega|\\big)\\) "
          "is positive semidefinite with \\(\\operatorname{tr}_B J = I/d\\), where "
          "\\(|\\Omega\\rangle=\\tfrac1{\\sqrt d}\\sum_i|ii\\rangle\\).")
    + p("The Kraus representation is not unique: \\(K'_j=\\sum_k u_{jk}K_k\\) for any isometric "
        "\\(u\\) gives the same channel. The minimal number of Kraus operators equals "
        "\\(\\operatorname{rank}J(\\mathcal E)\\le d^{2}\\).")
    + table(['Channel', 'Kraus operators', 'Bloch action'],
            [['Depolarizing \\(\\mathcal D_p\\)',
              r'\(\sqrt{1-\tfrac{3p}{4}}I,\ \tfrac{\sqrt p}{2}X,\ \tfrac{\sqrt p}{2}Y,\ \tfrac{\sqrt p}{2}Z\)',
              r'\(\vec r\mapsto(1-p)\vec r\) — uniform contraction'],
             ['Dephasing \\(\\mathcal Z_p\\)', r'\(\sqrt{1-p}\,I,\ \sqrt p\,Z\)',
              r'\((r_x,r_y,r_z)\mapsto((1-2p)r_x,(1-2p)r_y,r_z)\)'],
             ['Amplitude damping \\(\\mathcal A_\\gamma\\)',
              r'\(\begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix},\ \begin{pmatrix}0&\sqrt\gamma\\0&0\end{pmatrix}\)',
              r'contracts toward \(|0\rangle\): \(r_z\mapsto\gamma+(1-\gamma)r_z\)'],
             ['Bit flip', r'\(\sqrt{1-p}\,I,\ \sqrt p\,X\)', r'contracts \(y,z\), preserves \(x\)']])
    + p("Amplitude damping models spontaneous emission (energy loss, \\(T_1\\)); dephasing models "
        "loss of coherence without energy exchange (\\(T_2\\)). Real superconducting and ion-trap "
        "devices are well approximated by a composition of the two, and these are precisely the "
        "error models that Chapter 9 corrects.")
)

S4 = (
    p("Two operationally meaningful ways to compare states.")
    + box('def', 'Trace distance and fidelity',
          "\\(D(\\rho,\\sigma)=\\tfrac12\\|\\rho-\\sigma\\|_1=\\tfrac12\\operatorname{tr}|\\rho-\\sigma|\\) and "
          "\\(F(\\rho,\\sigma)=\\big(\\operatorname{tr}\\sqrt{\\sqrt\\rho\\,\\sigma\\sqrt\\rho}\\big)^{2}\\). "
          "For pure states \\(F=|\\langle\\psi|\\phi\\rangle|^{2}\\) and "
          "\\(D=\\sqrt{1-F}\\). For qubits, \\(D=\\tfrac12\\|\\vec r-\\vec s\\|\\).")
    + p("Trace distance has a direct meaning: the optimal probability of distinguishing "
        "\\(\\rho\\) from \\(\\sigma\\) given one copy and equal priors is "
        "\\(\\tfrac12(1+D(\\rho,\\sigma))\\) — the mixed-state Helstrom bound, generalising "
        "Chapter 2. Fidelity has an equally direct meaning via Uhlmann's theorem: "
        "\\(F(\\rho,\\sigma)=\\max|\\langle\\psi_\\rho|\\psi_\\sigma\\rangle|^{2}\\) over all "
        "purifications.")
    + box('thm', 'Data processing / contractivity',
          "For any channel \\(\\mathcal E\\): \\(D(\\mathcal E(\\rho),\\mathcal E(\\sigma))\\le D(\\rho,\\sigma)\\) "
          "and \\(F(\\mathcal E(\\rho),\\mathcal E(\\sigma))\\ge F(\\rho,\\sigma)\\). Physical processing "
          "never increases distinguishability. The same monotonicity holds for relative entropy "
          "\\(S(\\rho\\|\\sigma)=\\operatorname{tr}\\rho(\\log\\rho-\\log\\sigma)\\), from which most of "
          "quantum Shannon theory follows.")
)

S5 = (
    p("The von Neumann entropy \\(S(\\rho)=-\\operatorname{tr}\\rho\\log_2\\rho\\) is the Shannon "
      "entropy of the spectrum. It is zero for pure states, maximal (\\(\\log_2 d\\)) for "
      "\\(I/d\\), invariant under unitaries, and — unlike its classical counterpart — can be "
      "<em>smaller</em> for the whole than for a part: \\(S(AB)=0<S(A)\\) for a Bell state. That "
      "inversion is the information-theoretic signature of entanglement.")
    + ul([
        r'<strong>Subadditivity:</strong> \(S(AB)\le S(A)+S(B)\), equality iff \(\rho_{AB}=\rho_A\otimes\rho_B\).',
        r'<strong>Araki–Lieb:</strong> \(|S(A)-S(B)|\le S(AB)\).',
        r'<strong>Strong subadditivity (Lieb–Ruskai):</strong> \(S(ABC)+S(B)\le S(AB)+S(BC)\) — '
        r'the deepest inequality in the subject, equivalent to monotonicity of relative entropy.',
    ])
    + box('thm', 'Holevo bound',
          "If Alice encodes \\(x\\) with prior \\(p_x\\) into \\(\\rho_x\\) and Bob measures, the "
          "accessible information obeys \\(I(X:Y)\\le\\chi=S\\big(\\sum_x p_x\\rho_x\\big)-"
          "\\sum_x p_x S(\\rho_x)\\le\\log_2 d\\). Hence \\(n\\) qubits carry at most \\(n\\) "
          "classical bits — superdense coding does not contradict this, because it transmits "
          "\\(2n\\) bits using \\(n\\) qubits <em>plus</em> \\(n\\) pre-shared ebits.")
)

S6 = (
    code('''import numpy as np

def partial_trace(rho, dims, keep):
    """Trace out every subsystem not listed in `keep`. dims = list of local dimensions."""
    n = len(dims)
    keep = sorted(keep)
    rho = np.asarray(rho, dtype=complex).reshape(dims + dims)
    for ax in sorted(set(range(n)) - set(keep), reverse=True):
        rho = np.trace(rho, axis1=ax, axis2=ax + rho.ndim // 2)
    d = int(np.prod([dims[k] for k in keep]))
    return rho.reshape(d, d)

def apply_kraus(rho, Ks):
    return sum(K @ rho @ K.conj().T for K in Ks)

def depolarizing_kraus(p):
    I = np.eye(2, dtype=complex)
    X = np.array([[0,1],[1,0]], dtype=complex)
    Y = np.array([[0,-1j],[1j,0]], dtype=complex)
    Z = np.array([[1,0],[0,-1]], dtype=complex)
    return [np.sqrt(1 - 3*p/4)*I, np.sqrt(p)/2*X, np.sqrt(p)/2*Y, np.sqrt(p)/2*Z]

bell = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)
rho = np.outer(bell, bell.conj())
print(np.round(partial_trace(rho, [2,2], [0]).real, 6))   # I/2''',
         'Partial trace and Kraus application — the two primitives of open-system simulation')
    + p("A numerical warning: after applying a channel, floating-point error can push the "
        "smallest eigenvalue slightly negative. Before computing entropies, clip eigenvalues at "
        "zero and renormalise; do not feed raw eigenvalues to a logarithm.")
)

# =============================== figures, citations and added commentary =====
BALL_SVG = f'''
<rect x="0" y="0" width="680" height="330" fill="#ffffff"/>
<text x="340" y="20" font-family="{SERIF}" font-size="13" fill="{C['accent']}" text-anchor="middle" font-weight="bold">The Bloch ball: mixed states fill the interior, and noise contracts it</text>
<circle cx="162" cy="182" r="104" fill="#f0fdfa" stroke="{C['accent']}" stroke-width="2"/>
<circle cx="162" cy="182" r="73" fill="none" stroke="{C['gold']}" stroke-width="1.8" stroke-dasharray="6 4"/>
<circle cx="162" cy="182" r="41" fill="none" stroke="#9333ea" stroke-width="1.8" stroke-dasharray="6 4"/>
<circle cx="162" cy="182" r="4.5" fill="#dc2626"/>
<line x1="162" y1="182" x2="236" y2="109" stroke="{C['accent']}" stroke-width="2.4"/>
<circle cx="236" cy="109" r="4.5" fill="{C['accent']}"/>
<text x="312" y="92" font-family="{SERIF}" font-size="12" fill="{C['accent']}" text-anchor="start" font-weight="bold">pure:  &#8214;r&#8214; = 1</text>
<text x="312" y="122" font-family="{SERIF}" font-size="12" fill="#92400e" text-anchor="start">p = 0.30:  &#8214;r&#8214; = 0.70</text>
<text x="312" y="146" font-family="{SERIF}" font-size="12" fill="#6d28d9" text-anchor="start">p = 0.61:  &#8214;r&#8214; = 0.39</text>
<text x="312" y="170" font-family="{SERIF}" font-size="12" fill="#dc2626" text-anchor="start">p = 1:  &#8214;r&#8214; = 0, the state is I/2</text>
<text x="312" y="206" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">Depolarizing noise maps r &#8614; (1&#8722;p) r,</text>
<text x="312" y="226" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">a uniform contraction toward the centre.</text>
<text x="312" y="252" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">Purity tr&#961;&#178; = &#189;(1 + &#8214;r&#8214;&#178;) falls from 1</text>
<text x="312" y="272" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">to its minimum &#189;.</text>
<text x="312" y="300" font-family="{SERIF}" font-size="12" fill="{C['muted']}" text-anchor="start">No unitary can move a state off its sphere &#8212;</text>
<text x="312" y="316" font-family="{SERIF}" font-size="12" fill="{C['muted']}" text-anchor="start">only a channel can.</text>
'''

STINESPRING = flow_svg(
    [(28, 74, 128, 62, 'system|ρ', '#ecfeff', '#026573'),
     (28, 158, 128, 52, 'environment|E, prepared in 0', '#f8fafc', '#475569'),
     (196, 74, 108, 136, 'unitary|U on|S ⊗ E', '#fefce8', '#c9a227'),
     (348, 74, 132, 62, 'system out|E(ρ)', '#ecfeff', '#026573'),
     (348, 158, 132, 52, 'traced out|(discarded)', '#f8fafc', '#94a3b8'),
     (520, 60, 138, 150, 'equivalently|E(ρ) = Σₖ Kₖ ρ Kₖ†|with ΣₖKₖ†Kₖ = I|(Kraus form)',
      '#f5f3ff', '#6d28d9')],
    [(158, 104, 194, 104, ''), (158, 184, 194, 184, ''),
     (306, 104, 346, 104, ''), (306, 184, 346, 184, ''),
     (484, 134, 518, 134, '')],
    height=240, title='Stinespring dilation: every channel is a unitary on a larger system')

_ts = [k / 20 for k in range(0, 81)]
DECAY = line_chart(
    [dict(label='excited-state population  e^(−t/T₁)', xs=_ts, ys=[exp(-t) for t in _ts],
          color='#026573'),
     dict(label='coherence  e^(−t/T₂),  T₂ = T₁', xs=_ts, ys=[exp(-t) for t in _ts],
          color='#c9a227', dash='7 4'),
     dict(label='coherence  e^(−t/T₂),  T₂ = T₁/3  (dephasing-dominated)', xs=_ts,
          ys=[exp(-3 * t) for t in _ts], color='#dc2626')],
    xlim=(0, 4), ylim=(0, 1.02), xlabel='time  t / T₁',
    ylabel='surviving signal',
    hlines=[(1 / 2.71828, '1/e', '#475569')], height=330)

_ps = [k / 100 for k in range(0, 101)]
DISTANCES = line_chart(
    [dict(label='trace distance after the channel = 1 − p', xs=_ps, ys=[1 - q for q in _ps],
          color='#026573'),
     dict(label='fidelity with the input = 1 − p/2', xs=_ps, ys=[1 - q / 2 for q in _ps],
          color='#c9a227'),
     dict(label='purity = ½(1 + (1−p)²)', xs=_ps,
          ys=[0.5 * (1 + (1 - q) ** 2) for q in _ps], color='#9333ea'),
     dict(label='von Neumann entropy (bits)', xs=_ps,
          ys=[(lambda r: 0.0 if r >= 1 - 1e-12 else
               -((1 + r) / 2) * log2((1 + r) / 2) - ((1 - r) / 2) * log2((1 - r) / 2))(1 - q)
              for q in _ps], color='#dc2626', dash='6 4')],
    xlim=(0, 1), ylim=(0, 1.05), xlabel='depolarizing strength  p',
    ylabel='value', yticks=[0, 0.25, 0.5, 0.75, 1.0], height=340)

JS_BALL = """
  var b = JXG.JSXGraph.initBoard('ch5ball', {boundingbox: [-1.9, 1.5, 1.9, -1.6],
      axis: false, showCopyright: false, showNavigation: false, keepaspectratio: true});
  var pS = b.create('slider', [[-1.75, 1.32], [-0.35, 1.32], [0, 0.3, 1]],
      {name: 'p', snapWidth: 0.01, strokeColor: '#026573'});
  b.create('circle', [[0, 0], 1], {strokeColor: '#026573', strokeWidth: 2,
      fillColor: '#f0fdfa', fillOpacity: 0.5, fixed: true});
  b.create('line', [[-1, 0], [1, 0]], {strokeColor: '#94a3b8', strokeWidth: 1, fixed: true});
  b.create('line', [[0, -1], [0, 1]], {strokeColor: '#94a3b8', strokeWidth: 1, fixed: true});
  b.create('text', [0.04, 1.06, '|0&#10217;'], {fontSize: 12, strokeColor: '#475569'});
  b.create('text', [0.04, -1.14, '|1&#10217;'], {fontSize: 12, strokeColor: '#475569'});
  b.create('text', [1.04, 0.06, '|+&#10217;'], {fontSize: 12, strokeColor: '#475569'});
  var P = b.create('glider', [0.6, 0.8, b.create('circle', [[0, 0], 1],
      {visible: false, fixed: true})], {name: '&#961;', size: 4, strokeColor: '#0f172a',
      fillColor: '#0f172a'});
  var out = b.create('point', [function () { return (1 - pS.Value()) * P.X(); },
                               function () { return (1 - pS.Value()) * P.Y(); }],
      {name: '&#8496;(&#961;)', size: 4, strokeColor: '#dc2626', fillColor: '#dc2626', fixed: true});
  b.create('segment', [[0, 0], P], {strokeColor: '#0f172a', strokeWidth: 1.6, dash: 2});
  b.create('segment', [[0, 0], out], {strokeColor: '#dc2626', strokeWidth: 2.4});
  b.create('circle', [[0, 0], function () { return 1 - pS.Value(); }],
      {strokeColor: '#dc2626', strokeWidth: 1.4, dash: 2, fillOpacity: 0});
  b.create('text', [-1.8, -1.3, function () {
      var r = 1 - pS.Value();
      var pur = 0.5 * (1 + r * r);
      var lam = (1 + r) / 2;
      var S = (r >= 1 - 1e-9) ? 0 :
              -lam * Math.log2(lam) - (1 - lam) * Math.log2(1 - lam);
      return '&#8214;r&#8214; = ' + r.toFixed(2) + '   purity = ' + pur.toFixed(3) +
             '   S = ' + S.toFixed(3) + ' bits';
  }], {fontSize: 14, strokeColor: '#0f172a'});
"""

S1 = S1 + figure(
    '5.1',
    'The Bloch ball. Pure states occupy the surface; mixed states fill the interior, with the '
    'maximally mixed state I/2 at the centre. Depolarizing noise of strength p shrinks every Bloch '
    'vector by the factor 1 − p, so the whole ball contracts uniformly onto its centre. Because '
    'purity is ½(1 + ‖r‖²), the same picture reads directly as a plot of how much information '
    'survives the channel.',
    BALL_SVG, height=330) + p(
    "The convexity visible in the figure has real content" + cite('1') + ". The set of density "
    "operators is convex, and its extreme points are exactly the pure states — which for a qubit "
    "means exactly the surface. Any interior point can be written as a mixture of surface points in "
    "infinitely many ways, and this non-uniqueness is not a defect of the description but a "
    "statement about physics: the Hughston–Jozsa–Wootters theorem says that any two ensembles with "
    "the same average state are related by a unitary on a purifying system, and no local "
    "measurement can tell them apart. In dimension \\(d>2\\) the state space is no longer a ball; "
    "its boundary contains both pure states and mixed states of deficient rank, which is why "
    "the Bloch picture does not generalise usefully.") + sources(
    'Density operators, ensembles and the HJW theorem: Nielsen &amp; Chuang §2.4' + cite('1') +
    '; Watrous ch. 2' + cite('2') + '.')

S3 = S3 + figure(
    '5.2',
    'The three equivalent pictures of a quantum channel. Physically, the system is coupled '
    'unitarily to a fresh environment which is then discarded (Stinespring); algebraically, this '
    'produces the operator-sum form with completeness condition ΣₖKₖ†Kₖ = I (Kraus). The third '
    'picture, the Choi matrix, is obtained by feeding half of a maximally entangled state through '
    'the channel and is what makes complete positivity checkable by a single eigenvalue computation.',
    STINESPRING, height=240) + figure(
    '5.3',
    'Hardware decoherence in the two-timescale model. Energy relaxation depletes the excited state '
    'with time constant T₁; coherence — the off-diagonal element of ρ — decays with T₂. Pure '
    'amplitude damping gives T₂ = 2T₁, and any additional dephasing shortens T₂ further, so the '
    'inequality T₂ ≤ 2T₁ always holds. The 1/e crossings are the numbers quoted on device '
    'datasheets.',
    DECAY, height=330) + p(
    "Complete positivity, rather than mere positivity, is the technically delicate point and it is "
    "worth seeing why with a concrete failure" + cite('4') + ". Transposition maps density "
    "operators to density operators, so it is positive. But applied to half of a Bell state it "
    "produces a matrix with an eigenvalue of \\(-1/2\\), which is not a state — so "
    "\\(T\\otimes\\mathrm{id}\\) is not positive and \\(T\\) is not a physical operation. This is "
    "exactly the computation behind the PPT criterion of Chapter 4: a map that is positive but not "
    "completely positive is precisely an <em>entanglement witness</em>. The Choi matrix packages "
    "this into a single test, since \\(\\mathcal E\\) is completely positive if and only if "
    "\\(J(\\mathcal E)\\ge0\\).") + sources(
    'Kraus form' + cite('3') + '; the Choi criterion' + cite('4') + '; Stinespring dilation and the '
    'equivalence of all three: Watrous ch. 2' + cite('2') + '; noise models and T₁/T₂: Nielsen '
    '&amp; Chuang §8.3' + cite('1') + '.')

S4 = S4 + figure(
    '5.4',
    'Four figures of merit for a qubit passing through a depolarizing channel of strength p. Trace '
    'distance between the images of two orthogonal inputs falls linearly and reaches zero at p = 1, '
    'where the channel forgets everything; fidelity with the input falls half as fast; purity '
    'reaches its floor of ½; and the von Neumann entropy rises to its ceiling of one bit. The '
    'monotone behaviour of the first two is not a property of this channel but a theorem — the '
    'data-processing inequality — valid for every channel whatsoever.',
    DISTANCES, height=340) + interactive(
    '5.5', 'ch5ball',
    'Drag the black point ρ around the Bloch circle and move the slider to set the depolarizing '
    'strength p. The red point is the output state and the dashed red circle is the image of the '
    'whole ball. Watch two invariants: the output always lies on the same ray from the centre '
    '(depolarizing noise never rotates a state), and purity and entropy depend only on the length '
    'of the output vector, not its direction.',
    JS_BALL, aspect='1/1', max_width=430,
    hint='drag ρ on the circle, and drag the slider to change p.') + p(
    "The operational reading of trace distance is what makes Figure 5.4 more than a plot of a "
    "formula. Given one copy of an unknown state that is either \\(\\rho\\) or \\(\\sigma\\) with "
    "equal prior, the best possible probability of guessing right is "
    "\\(\\tfrac12(1+D(\\rho,\\sigma))\\)" + cite('1') + " — the mixed-state Helstrom bound, "
    "generalising Chapter 2. So the teal curve is literally the advantage an optimal receiver "
    "retains after the channel, and its monotonicity says that no post-processing, however clever, "
    "can recover information the channel destroyed. Chapter 9 is the art of arranging that the "
    "information was never in a single qubit to begin with.") + sources(
    'Trace distance, fidelity, Uhlmann\'s theorem and contractivity: Nielsen &amp; Chuang ch. 9'
    + cite('1') + '; Wilde ch. 9' + cite('7') + '.')

S5 = S5 + sources(
    'Entropies, subadditivity and strong subadditivity: Nielsen &amp; Chuang ch. 11' + cite('1') +
    ', Lieb &amp; Ruskai' + cite('5') + '; the Holevo bound' + cite('6') + '; a modern unified '
    'treatment: Wilde' + cite('7') + '.')

REFS = [
    dict(authors="M. A. Nielsen and I. L. Chuang", title="Quantum Computation and Quantum Information",
         venue="Cambridge University Press", year="2010",
         note="Chapters 2.4, 8 (channels, Kraus, noise models), 9 (distance measures), 11 (entropy)."),
    dict(authors="J. Watrous", title="The Theory of Quantum Information",
         venue="Cambridge University Press", year="2018",
         link="https://cs.uwaterloo.ca/~watrous/TQI/",
         note="Chapters 2–3 and 6: the definitive modern treatment of channels and Choi representations."),
    dict(authors="K. Kraus", title="States, Effects, and Operations",
         venue="Springer Lecture Notes in Physics 190", year="1983",
         note="Origin of the operator-sum representation."),
    dict(authors="M.-D. Choi", title="Completely positive linear maps on complex matrices",
         venue="Linear Algebra and its Applications 10(3), 285–290", year="1975",
         note="The Choi matrix and the characterisation of complete positivity."),
    dict(authors="E. H. Lieb and M. B. Ruskai",
         title="Proof of the strong subadditivity of quantum-mechanical entropy",
         venue="Journal of Mathematical Physics 14, 1938", year="1973",
         note="Strong subadditivity, quoted in §5."),
    dict(authors="A. S. Holevo",
         title="Bounds for the quantity of information transmitted by a quantum communication channel",
         venue="Problems of Information Transmission 9(3), 177–183", year="1973",
         note="The Holevo bound."),
    dict(authors="M. M. Wilde", title="Quantum Information Theory (2nd ed.)",
         venue="Cambridge University Press", year="2017",
         link="https://arxiv.org/abs/1106.1445",
         note="Free arXiv version; the standard graduate text for entropies and channel capacities."),
]

CR = [
    dict(
        name='C5.Q1 — Partial trace and reduced states',
        qtext=cr_qtext('C5.Q1', 'Marginals of a multipartite state',
                       "The partial trace is the unique operation reproducing all local "
                       "measurement statistics. Implemented on the reshaped tensor it is a "
                       "sequence of traces over paired axes.",
                       "Write <code>partial_trace(rho, dims, keep)</code> for a density matrix "
                       "on subsystems of dimensions <code>dims</code>, keeping the "
                       "(sorted) indices in <code>keep</code>; and "
                       "<code>purity(rho)</code> returning \\(\\operatorname{tr}\\rho^{2}\\) as a "
                       "float rounded to 6 decimals.",
                       "Bell state, keep=[0]  ->  I/2, purity 0.5\n"
                       "product state         ->  purity 1.0"),
        answer='''import numpy as np

def partial_trace(rho, dims, keep):
    n = len(dims)
    keep = sorted(keep)
    rho = np.asarray(rho, dtype=complex).reshape(list(dims) + list(dims))
    for ax in sorted(set(range(n)) - set(keep), reverse=True):
        half = rho.ndim // 2
        rho = np.trace(rho, axis1=ax, axis2=ax + half)
    d = int(np.prod([dims[k] for k in keep]))
    return rho.reshape(d, d)

def purity(rho):
    rho = np.asarray(rho, dtype=complex)
    return round(float(np.real(np.trace(rho @ rho))), 6)
''',
        preload='''import numpy as np

def partial_trace(rho, dims, keep):
    # reshape to dims+dims, then np.trace over the paired axes of the discarded systems
    ...

def purity(rho):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nbell = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)\n'
                     'rho = np.outer(bell, bell.conj())\n'
                     'print(np.round(partial_trace(rho, [2,2], [0]).real, 6).tolist())\n',
             'expected': '[[0.5, 0.0], [0.0, 0.5]]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nbell = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)\n'
                     'rho = np.outer(bell, bell.conj())\n'
                     'print(purity(rho), purity(partial_trace(rho, [2,2], [0])))\n',
             'expected': '1.0 0.5\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nv = np.zeros(4, dtype=complex); v[0]=1\n'
                     'rho = np.outer(v, v.conj())\n'
                     'print(purity(partial_trace(rho, [2,2], [1])))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nghz = np.zeros(8, dtype=complex); ghz[0]=ghz[7]=1/np.sqrt(2)\n'
                     'rho = np.outer(ghz, ghz.conj())\n'
                     'r01 = partial_trace(rho, [2,2,2], [0,1])\n'
                     'print(r01.shape, purity(r01))\n',
             'expected': '(4, 4) 0.5\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nrng = np.random.default_rng(4)\n'
                     'v = rng.normal(size=6) + 1j*rng.normal(size=6); v/=np.linalg.norm(v)\n'
                     'rho = np.outer(v, v.conj())\n'
                     'rA = partial_trace(rho, [2,3], [0])\n'
                     'print(rA.shape, round(float(np.real(np.trace(rA))), 6))\n',
             'expected': '(2, 2) 1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C5.Q2 — Kraus operators and standard noise channels',
        qtext=cr_qtext('C5.Q2', 'Applying and validating a channel',
                       "A CPTP map has Kraus operators with "
                       "\\(\\sum_k K_k^{\\dagger}K_k=I\\). Depolarizing, dephasing and amplitude "
                       "damping are the workhorse noise models.",
                       "Write <code>apply_kraus(rho, Ks)</code>; "
                       "<code>is_cptp(Ks, tol=1e-9)</code> returning a <code>bool</code>; and the "
                       "three constructors <code>depolarizing(p)</code>, "
                       "<code>dephasing(p)</code>, <code>amplitude_damping(g)</code> returning "
                       "lists of Kraus operators exactly as tabulated in §3.",
                       "depolarizing(1.0) applied to any rho  ->  I/2\n"
                       "amplitude_damping(1.0) applied to any rho  ->  |0><0|"),
        answer='''import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def apply_kraus(rho, Ks):
    rho = np.asarray(rho, dtype=complex)
    out = np.zeros_like(rho)
    for K in Ks:
        K = np.asarray(K, dtype=complex)
        out = out + K @ rho @ K.conj().T
    return out

def is_cptp(Ks, tol=1e-9):
    d = np.asarray(Ks[0]).shape[1]
    S = sum(np.asarray(K, dtype=complex).conj().T @ np.asarray(K, dtype=complex) for K in Ks)
    return bool(np.allclose(S, np.eye(d), atol=tol))

def depolarizing(p):
    return [np.sqrt(1 - 3 * p / 4) * I2, np.sqrt(p) / 2 * X,
            np.sqrt(p) / 2 * Y, np.sqrt(p) / 2 * Z]

def dephasing(p):
    return [np.sqrt(1 - p) * I2, np.sqrt(p) * Z]

def amplitude_damping(g):
    K0 = np.array([[1, 0], [0, np.sqrt(1 - g)]], dtype=complex)
    K1 = np.array([[0, np.sqrt(g)], [0, 0]], dtype=complex)
    return [K0, K1]
''',
        preload='''import numpy as np

def apply_kraus(rho, Ks):
    ...

def is_cptp(Ks, tol=1e-9):
    ...

def depolarizing(p):
    ...

def dephasing(p):
    ...

def amplitude_damping(g):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nprint(is_cptp(depolarizing(0.3)), is_cptp(dephasing(0.2)), '
                     'is_cptp(amplitude_damping(0.7)))\n',
             'expected': 'True True True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nrho = np.array([[1,0],[0,0]], dtype=complex)\n'
                     'print(np.round(apply_kraus(rho, depolarizing(1.0)).real, 6).tolist())\n',
             'expected': '[[0.5, 0.0], [0.0, 0.5]]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nrho = np.array([[0,0],[0,1]], dtype=complex)\n'
                     'print(np.round(apply_kraus(rho, amplitude_damping(1.0)).real, 6).tolist())\n',
             'expected': '[[1.0, 0.0], [0.0, 0.0]]\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nplus = np.array([1,1], dtype=complex)/np.sqrt(2)\n'
                     'rho = np.outer(plus, plus.conj())\n'
                     'out = apply_kraus(rho, dephasing(0.5))\n'
                     'print(np.round(out.real, 6).tolist())\n',
             'expected': '[[0.5, 0.0], [0.0, 0.5]]\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nrng = np.random.default_rng(9)\n'
                     'v = rng.normal(size=2)+1j*rng.normal(size=2); v/=np.linalg.norm(v)\n'
                     'rho = np.outer(v, v.conj())\n'
                     'out = apply_kraus(rho, depolarizing(0.37))\n'
                     'print(round(float(np.real(np.trace(out))), 6))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C5.Q3 — The Choi matrix and complete positivity',
        qtext=cr_qtext('C5.Q3', 'Channel–state duality',
                       "The Choi–Jamiołkowski isomorphism turns a channel into a state: "
                       "\\(J(\\mathcal E)=(\\mathrm{id}\\otimes\\mathcal E)(|\\Omega\\rangle\\langle\\Omega|)\\) "
                       "with \\(|\\Omega\\rangle=\\tfrac1{\\sqrt d}\\sum_i|ii\\rangle\\). "
                       "\\(\\mathcal E\\) is completely positive iff \\(J\\ge0\\).",
                       "Write <code>choi(Ks, d=2)</code> returning the \\(d^{2}\\times d^{2}\\) Choi "
                       "matrix of the channel with Kraus operators <code>Ks</code>; "
                       "<code>is_cp_from_choi(J, tol=1e-9)</code> returning a <code>bool</code> "
                       "(all eigenvalues \\(\\ge-\\)tol); and "
                       "<code>kraus_rank(J, tol=1e-9)</code> returning the number of strictly "
                       "positive eigenvalues.",
                       "identity channel   ->  Choi = |Omega><Omega|, rank 1\n"
                       "depolarizing(1.0)  ->  rank 4"),
        answer='''import numpy as np

def choi(Ks, d=2):
    omega = np.zeros(d * d, dtype=complex)
    for i in range(d):
        omega[i * d + i] = 1 / np.sqrt(d)
    rho = np.outer(omega, omega.conj()).reshape(d, d, d, d)
    out = np.zeros((d, d, d, d), dtype=complex)
    for K in Ks:
        K = np.asarray(K, dtype=complex)
        tmp = np.einsum('ab,ibjc,dc->iajd', K, rho.transpose(0, 1, 2, 3), K.conj())
        out = out + tmp
    return out.reshape(d * d, d * d)

def is_cp_from_choi(J, tol=1e-9):
    w = np.linalg.eigvalsh((np.asarray(J) + np.asarray(J).conj().T) / 2)
    return bool(np.all(w >= -tol))

def kraus_rank(J, tol=1e-9):
    w = np.linalg.eigvalsh((np.asarray(J) + np.asarray(J).conj().T) / 2)
    return int(np.sum(w > tol))
''',
        preload='''import numpy as np

def choi(Ks, d=2):
    # (id (x) E) applied to |Omega><Omega|
    ...

def is_cp_from_choi(J, tol=1e-9):
    ...

def kraus_rank(J, tol=1e-9):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nJ = choi([np.eye(2, dtype=complex)])\n'
                     'print(np.round(J.real, 6).tolist())\n',
             'expected': '[[0.5, 0.0, 0.0, 0.5], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.5, 0.0, 0.0, 0.5]]\n',
             'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nJ = choi([np.eye(2, dtype=complex)])\n'
                     'print(is_cp_from_choi(J), kraus_rank(J))\n',
             'expected': 'True 1\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
Ks = [np.sqrt(1-3*1.0/4)*I2, 0.5*X, 0.5*Y, 0.5*Z]
J = choi(Ks)
print(kraus_rank(J), np.allclose(J, np.eye(4)/4))
''',
             'expected': '4 True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
K0 = np.array([[1,0],[0,np.sqrt(1-0.3)]], dtype=complex)
K1 = np.array([[0,np.sqrt(0.3)],[0,0]], dtype=complex)
J = choi([K0, K1])
print(is_cp_from_choi(J), kraus_rank(J), round(float(np.real(np.trace(J))), 6))
''',
             'expected': 'True 2 1.0\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': '''import numpy as np
# transposition is positive but not completely positive: its Choi matrix has a negative eigenvalue
E = [np.array([[1,0],[0,0]], dtype=complex), np.array([[0,0],[0,1]], dtype=complex),
     np.array([[0,1],[0,0]], dtype=complex), np.array([[0,0],[1,0]], dtype=complex)]
J = choi([np.eye(2, dtype=complex)])
Jt = J.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
print(is_cp_from_choi(Jt))
''',
             'expected': 'False\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C5.Q4 — Trace distance, fidelity and data processing',
        qtext=cr_qtext('C5.Q4', 'How far apart are two states?',
                       "\\(D=\\tfrac12\\|\\rho-\\sigma\\|_1\\) is the optimal distinguishing "
                       "advantage; \\(F\\) is Uhlmann fidelity. Both are monotone under channels.",
                       "Write <code>trace_distance(rho, sigma)</code> and "
                       "<code>fidelity(rho, sigma)</code> "
                       "(\\(F=(\\operatorname{tr}\\sqrt{\\sqrt\\rho\\sigma\\sqrt\\rho})^{2}\\)), "
                       "each returning a float rounded to 6 decimals, and "
                       "<code>von_neumann(rho)</code> returning \\(S(\\rho)\\) in bits, rounded "
                       "to 6 decimals, with eigenvalues clipped at 0 before taking logs.",
                       "D(|0>,|1>) = 1.0,   F(|0>,|1>) = 0.0\n"
                       "S(I/2) = 1.0,       S(|0><0|) = 0.0"),
        answer='''import numpy as np

def _sqrtm_psd(A):
    w, v = np.linalg.eigh((A + A.conj().T) / 2)
    w = np.clip(w, 0, None)
    return (v * np.sqrt(w)) @ v.conj().T

def trace_distance(rho, sigma):
    D = np.asarray(rho, dtype=complex) - np.asarray(sigma, dtype=complex)
    w = np.linalg.eigvalsh((D + D.conj().T) / 2)
    return round(float(0.5 * np.sum(np.abs(w))), 6)

def fidelity(rho, sigma):
    r = _sqrtm_psd(np.asarray(rho, dtype=complex))
    M = r @ np.asarray(sigma, dtype=complex) @ r
    w = np.linalg.eigvalsh((M + M.conj().T) / 2)
    w = np.clip(w, 0, None)
    return round(float(np.sum(np.sqrt(w)) ** 2), 6)

def von_neumann(rho):
    w = np.linalg.eigvalsh((np.asarray(rho, dtype=complex) + np.asarray(rho, dtype=complex).conj().T) / 2)
    w = np.clip(w, 0, None)
    w = w[w > 1e-12]
    return round(float(abs(-np.sum(w * np.log2(w)))), 6)
''',
        preload='''import numpy as np

def trace_distance(rho, sigma):
    ...

def fidelity(rho, sigma):
    ...

def von_neumann(rho):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nr0 = np.array([[1,0],[0,0]], dtype=complex)\n'
                     'r1 = np.array([[0,0],[0,1]], dtype=complex)\n'
                     'print(trace_distance(r0,r1), fidelity(r0,r1))\n',
             'expected': '1.0 0.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nI2 = np.eye(2, dtype=complex)/2\n'
                     'r0 = np.array([[1,0],[0,0]], dtype=complex)\n'
                     'print(von_neumann(I2), von_neumann(r0))\n',
             'expected': '1.0 0.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nr0 = np.array([[1,0],[0,0]], dtype=complex)\n'
                     'plus = np.array([1,1], dtype=complex)/np.sqrt(2)\n'
                     'rp = np.outer(plus, plus.conj())\n'
                     'print(trace_distance(r0,rp), fidelity(r0,rp))\n',
             'expected': '0.707107 0.5\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
p = 0.4
Ks = [np.sqrt(1-3*p/4)*I2, np.sqrt(p)/2*X, np.sqrt(p)/2*Y, np.sqrt(p)/2*Z]
def ap(rho): return sum(K @ rho @ K.conj().T for K in Ks)
r0 = np.array([[1,0],[0,0]], dtype=complex)
r1 = np.array([[0,0],[0,1]], dtype=complex)
print(trace_distance(ap(r0), ap(r1)) <= trace_distance(r0, r1))
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nrho = np.diag([0.7, 0.3]).astype(complex)\n'
                     'print(von_neumann(rho))\n',
             'expected': '0.881291\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

ST = [
    stack_question(
        name='C5.S1 — Depolarizing noise on the Bloch ball',
        questiontext=stack_qtext(
            'C5.S1', 'Contraction of the Bloch vector',
            r'<p>The depolarizing channel acts as \(\mathcal D_p(\rho)=(1-p)\rho+p\,\frac{I}{2}\).</p>'
            r'<p>(a) Starting from \(|0\rangle\), give \(\langle Z\rangle\) after the channel, as a '
            r'function of <code>p</code>.</p>'
            r'<p>\(\langle Z\rangle=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the purity \(\operatorname{tr}\rho^{2}\) of the output, as a function of '
            r'<code>p</code>.</p>'
            r'<p>purity \(=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>In Bloch form \(\rho=\tfrac12(I+\vec r\cdot\vec\sigma)\) and '
            r'\(\mathcal D_p:\vec r\mapsto(1-p)\vec r\): the ball shrinks uniformly toward its centre.</p>'
            r'<p>(a) \(|0\rangle\) has \(\vec r=(0,0,1)\), so \(\langle Z\rangle=1-p\).</p>'
            r'<p>(b) \(\operatorname{tr}\rho^2=\tfrac12(1+\|\vec r\|^2)=\tfrac12(1+(1-p)^2)\).</p>'
            r'<p>At \(p=1\) the output is \(I/2\): all information is destroyed and the purity is '
            r'\(1/2\), the minimum for a qubit. Note \(p=1\) is <em>not</em> the worst case for '
            r'error correction — a fully depolarizing channel is at least known, whereas '
            r'intermediate \(p\) leaves partial, correctable information.</p>'),
        questionvariables='ta1 : 1-p;\nta2 : (1+(1-p)^2)/2;',
        questionnote='<Z>=1-p, purity=(1+(1-p)^2)/2',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=14, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Use \(\vec r\mapsto(1-p)\vec r\) and \(\langle Z\rangle=r_z\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=22, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>For a qubit, \(\operatorname{tr}\rho^2=\tfrac12(1+\|\vec r\|^2)\).</p>')]),
    stack_question(
        name='C5.S2 — Von Neumann entropy and the Holevo bound',
        questiontext=stack_qtext(
            'C5.S2', 'Entropy of a qubit',
            r'<p>Let \(\rho=\mathrm{diag}(q,1-q)\) with \(q\in(0,1)\).</p>'
            r'<p>(a) Give \(S(\rho)\) in bits (use <code>log(x)/log(2)</code>).</p>'
            r'<p>\(S=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the maximum of \(S\) over \(q\), and the value of \(q\) attaining it, as '
            r'the ordered pair <code>[Smax, qmax]</code>.</p>'
            r'<p>[[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>(a) \(S(\rho)=-q\log_2 q-(1-q)\log_2(1-q)=h(q)\), the binary entropy.</p>'
            r'<p>(b) \(h\) is concave with \(h\'(q)=\log_2\frac{1-q}{q}\), vanishing at \(q=1/2\), '
            r'where \(h=1\). So the maximum is \(1\) bit at \(q=1/2\), i.e. at \(\rho=I/2\).</p>'
            r'<p>Consequence (Holevo): the accessible information of an ensemble of qubit states '
            r'never exceeds \(\log_2 2=1\) bit per qubit. Superdense coding does not violate this — '
            r'it spends pre-shared entanglement, which is not counted in the Holevo \(\chi\).</p>'),
        questionvariables=('ta1 : -q*log(q)/log(2)-(1-q)*log(1-q)/log(2);\n'
                           'ta2 : [1,1/2];'),
        questionnote='S=h(q), max 1 at q=1/2',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=40, value='0.5000000',
                 truefb='<p>Correct — the binary entropy.</p>',
                 falsefb=r'<p>\(S=-\sum_k\lambda_k\log_2\lambda_k\) over the two eigenvalues.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=18, value='0.5000000',
                 forbidfloat=0,
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Differentiate \(h(q)\); enter the answer as a list <code>[Smax, qmax]</code>.</p>')]),
    stack_question(
        name='C5.S3 — Amplitude damping and the T1 model',
        questiontext=stack_qtext(
            'C5.S3', 'Energy relaxation',
            r'<p>Amplitude damping has Kraus operators '
            r'\(K_0=\begin{pmatrix}1&0\\0&\sqrt{1-\gamma}\end{pmatrix}\), '
            r'\(K_1=\begin{pmatrix}0&\sqrt\gamma\\0&0\end{pmatrix}\).</p>'
            r'<p>(a) Starting from \(|1\rangle\), give the probability of finding the qubit in '
            r'\(|0\rangle\) after the channel.</p>'
            r'<p>\(p_0=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) If the channel is applied \(n\) times in succession, give the probability of '
            r'still finding \(|1\rangle\).</p>'
            r'<p>\(p_1^{(n)}=\) [[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Writing \(\gamma=1-e^{-t/T_1}\) for a single application of duration \(t\), '
            r'give \(p_1\) as a function of <code>t</code> and <code>T1</code>.</p>'
            r'<p>\(p_1(t)=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) \(K_1|1\rangle=\sqrt\gamma\,|0\rangle\), so \(p_0=\gamma\).</p>'
            r'<p>(b) Each application leaves \(|1\rangle\) with probability \(1-\gamma\), and the '
            r'\(|1\rangle\) component is not repopulated, so \(p_1^{(n)}=(1-\gamma)^n\).</p>'
            r'<p>(c) With \(\gamma=1-e^{-t/T_1}\), \(p_1=e^{-t/T_1}\) — the exponential energy '
            r'relaxation measured on real hardware as \(T_1\). Dephasing gives the complementary '
            r'\(T_2\) timescale, with \(T_2\le 2T_1\).</p>'),
        questionvariables='ta1 : g;\nta2 : (1-g)^n;\nta3 : exp(-t/T1);',
        questionnote='p0=gamma, (1-gamma)^n, exp(-t/T1)',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=10, value='0.3333333',
                 syntaxhint='g',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Apply \(K_1\) to \(|1\rangle\) and take the squared norm. Write \(\gamma\) as <code>g</code>.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=14, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb='<p>The channel composes multiplicatively on the excited-state population.</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=16, value='0.3333333',
                 truefb=r'<p>Correct — this is the \(T_1\) decay curve.</p>',
                 falsefb=r'<p>Substitute \(\gamma=1-e^{-t/T_1}\) into \(p_1=1-\gamma\).</p>')]),
]

CHAPTER = dict(
    no=5, slug='density-matrices-and-channels',
    title='Density Operators, Open Systems and Quantum Channels',
    subtitle='Mixed states and the Bloch ball, partial trace and purification, CPTP maps in the '
             'Kraus/Stinespring/Choi pictures, realistic noise models, distance measures and entropies.',
    prereq='Chapters 1–4 (spectral theorem, tensor products, Schmidt decomposition).',
    objectives=[
        'Represent mixed states as density operators and locate them in the Bloch ball.',
        'Compute partial traces and construct purifications; state the church-of-the-larger-Hilbert-space principle.',
        'Move fluently between Kraus, Stinespring and Choi representations of a channel.',
        'Model realistic hardware noise (depolarizing, dephasing, amplitude damping) and relate it to T1/T2.',
        'Compute trace distance, fidelity and von Neumann entropy, and apply data-processing monotonicity.',
        'State the Holevo bound and reconcile it with superdense coding.',
    ],
    sections=[
        ('Density operators and the Bloch ball', S1),
        ('Partial trace and purification', S2),
        ('Quantum channels: Kraus, Stinespring, Choi', S3),
        ('Distinguishing states: trace distance and fidelity', S4),
        ('Von Neumann entropy and the Holevo bound', S5),
        ('Numerical practice', S6),
    ],
    summary="Density operators describe both classical ignorance and entanglement-induced "
            "mixedness, and every mixed state purifies. Physical evolution is CPTP, equivalently "
            "described by Kraus operators, a Stinespring dilation, or a positive Choi matrix. "
            "Hardware noise is captured by depolarizing, dephasing and amplitude-damping "
            "channels; trace distance and fidelity measure how much of the state survives, and "
            "both are monotone under any channel. These are exactly the tools Chapter 9 needs to "
            "define and analyse quantum error correction.",
    references=REFS, coderunner=CR, stack=ST,
)
