# -*- coding: utf-8 -*-
"""Chapter 1 — Mathematical Foundations of Quantum Computation."""
from math import log10, sqrt, cos, sin, pi
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, bar_chart, interactive,
                    nested_svg, flow_svg, C, SERIF, MONO)

S1 = (
    p("Quantum computation is linear algebra over the complex field, constrained by "
      "physics. Everything in this course lives in a finite-dimensional complex Hilbert "
      "space \\(\\mathcal H \\cong \\mathbb C^d\\): a complex vector space equipped with an "
      "inner product \\(\\langle\\cdot,\\cdot\\rangle\\) that is conjugate-linear in its first "
      "argument and linear in its second — the physicists' convention we adopt throughout.")
    + eq(r"\langle \phi | \psi \rangle \;=\; \sum_{i=0}^{d-1} \overline{\phi_i}\,\psi_i, "
         r"\qquad \|\psi\| = \sqrt{\langle\psi|\psi\rangle}")
    + p("Dirac notation encodes the duality \\(\\mathcal H \\leftrightarrow \\mathcal H^{*}\\) "
        "explicitly. A <em>ket</em> \\(|\\psi\\rangle\\) is a column vector; the corresponding "
        "<em>bra</em> \\(\\langle\\psi|\\) is the row vector \\(|\\psi\\rangle^{\\dagger}\\), i.e. the "
        "image of \\(|\\psi\\rangle\\) under the Riesz isomorphism. The two natural products are")
    + eq(r"\underbrace{\langle\phi|\psi\rangle}_{\text{scalar}} \in \mathbb C, \qquad "
         r"\underbrace{|\psi\rangle\langle\phi|}_{\text{operator}} \in \mathcal B(\mathcal H)")
    + box('def', 'Computational basis',
          "For a \\(d\\)-dimensional system the computational basis is the orthonormal set "
          "\\(\\{|0\\rangle,\\dots,|d-1\\rangle\\}\\) with \\(\\langle i|j\\rangle=\\delta_{ij}\\) and "
          "\\(\\sum_i |i\\rangle\\langle i| = I\\) (the <em>resolution of the identity</em> or "
          "completeness relation). For \\(d=2\\) we call the system a <strong>qubit</strong>.")
    + p("The completeness relation is the workhorse of all subsequent manipulations: inserting "
        "\\(I=\\sum_i|i\\rangle\\langle i|\\) between any two operators expands them in matrix "
        "components, \\(A_{ij}=\\langle i|A|j\\rangle\\).")
)

S2 = (
    p("Let \\(\\mathcal B(\\mathcal H)\\) denote the algebra of linear operators on "
      "\\(\\mathcal H\\). The <em>adjoint</em> \\(A^{\\dagger}\\) is defined by "
      "\\(\\langle\\phi|A\\psi\\rangle=\\langle A^{\\dagger}\\phi|\\psi\\rangle\\) for all "
      "\\(\\phi,\\psi\\); in coordinates it is the conjugate transpose. Four classes of "
      "operator carry all of the physics.")
    + table(['Class', 'Definition', 'Role in quantum theory'],
            [['Hermitian (self-adjoint)', r'\(A=A^{\dagger}\)', 'Observables; Hamiltonians'],
             ['Unitary', r'\(U^{\dagger}U=UU^{\dagger}=I\)', 'Closed-system evolution; quantum gates'],
             ['Projector', r'\(P=P^{\dagger}=P^{2}\)', 'Measurement outcomes; subspace selection'],
             ['Positive semidefinite', r'\(\langle\psi|A|\psi\rangle\ge 0\;\forall\psi\)', 'Density operators; POVM elements']])
    + box('thm', 'Spectral theorem',
          "Every normal operator \\(N\\) (i.e. \\(NN^{\\dagger}=N^{\\dagger}N\\)) on a "
          "finite-dimensional \\(\\mathcal H\\) admits an orthonormal eigenbasis. Equivalently "
          "\\(N=\\sum_k \\lambda_k P_k\\) with \\(P_k\\) mutually orthogonal projectors summing to "
          "\\(I\\). Hermitian operators have real \\(\\lambda_k\\); unitary operators have "
          "\\(|\\lambda_k|=1\\).")
    + box('proof', '',
          "Induct on \\(\\dim\\mathcal H\\). Over \\(\\mathbb C\\) the characteristic polynomial has "
          "a root \\(\\lambda\\), giving an eigenvector \\(v\\). Normality implies the orthogonal "
          "complement \\(v^{\\perp}\\) is invariant under \\(N\\) — indeed for \\(w\\perp v\\), "
          "\\(\\langle v|Nw\\rangle=\\langle N^{\\dagger}v|w\\rangle=\\overline{\\lambda}\\langle v|w\\rangle=0\\) "
          "using \\(N^{\\dagger}v=\\overline{\\lambda}v\\), itself a consequence of normality. "
          "Restrict and apply the inductive hypothesis. \\(\\blacksquare\\)")
    + p("The spectral theorem gives meaning to functions of operators. If "
        "\\(A=\\sum_k\\lambda_k P_k\\) and \\(f:\\mathbb R\\to\\mathbb C\\), then "
        "\\(f(A) := \\sum_k f(\\lambda_k)P_k\\). The single most important instance in this course:")
    + eq(r"U(t) \;=\; e^{-iHt/\hbar} \;=\; \sum_k e^{-i\lambda_k t/\hbar} P_k ,")
    + p("which is unitary precisely because \\(H\\) is Hermitian. We set \\(\\hbar=1\\) from here on. "
        "Conversely, Stone's theorem states every strongly continuous one-parameter unitary group "
        "is of this form for a unique Hermitian generator.")
)

S3 = (
    p("Composite systems are described by tensor products, not direct sums — this single "
      "algebraic fact is the origin of the exponential dimension that quantum computers "
      "exploit and of entanglement itself.")
    + box('def', 'Tensor product',
          "If \\(\\mathcal H_A\\cong\\mathbb C^{m}\\) with basis \\(\\{|i\\rangle_A\\}\\) and "
          "\\(\\mathcal H_B\\cong\\mathbb C^{n}\\) with basis \\(\\{|j\\rangle_B\\}\\), then "
          "\\(\\mathcal H_{AB}=\\mathcal H_A\\otimes\\mathcal H_B\\cong\\mathbb C^{mn}\\) has basis "
          "\\(\\{|i\\rangle\\otimes|j\\rangle\\}\\), written \\(|i\\rangle|j\\rangle\\) or "
          "\\(|ij\\rangle\\). Operators act factor-wise: "
          "\\((A\\otimes B)(|\\psi\\rangle\\otimes|\\phi\\rangle)=A|\\psi\\rangle\\otimes B|\\phi\\rangle\\).")
    + p("In coordinates the tensor product of operators is the <strong>Kronecker product</strong>. "
        "Ordering matters: with the standard little-endian convention used by most textbooks "
        "(and the opposite of Qiskit's, a recurring source of bugs), qubit \\(0\\) is the "
        "leftmost factor.")
    + eq(r"A \otimes B \;=\; \begin{pmatrix} a_{00}B & a_{01}B \\ a_{10}B & a_{11}B \end{pmatrix}")
    + p("An \\(n\\)-qubit register therefore has state space \\((\\mathbb C^{2})^{\\otimes n}\\cong"
        "\\mathbb C^{2^{n}}\\). Describing a general pure state needs \\(2^{n}-1\\) complex "
        "parameters: 20 qubits already exceed a million amplitudes, 50 qubits exceed a "
        "petabyte in single precision. This is the resource claim behind quantum advantage — "
        "and simultaneously the reason classical simulation of the exercises in this course "
        "is restricted to small \\(n\\).")
    + box('warn', 'Not every vector factorises',
          "The set of product states \\(\\{|\\psi\\rangle\\otimes|\\phi\\rangle\\}\\) is a measure-zero "
          "subvariety (the Segre variety) of the unit sphere in \\(\\mathbb C^{mn}\\). Vectors "
          "outside it are <strong>entangled</strong>; the Bell state "
          "\\((|00\\rangle+|11\\rangle)/\\sqrt2\\) is the canonical example. Chapter 4 develops "
          "this systematically via the Schmidt decomposition.")
    + p("Two identities used constantly: \\((A\\otimes B)(C\\otimes D)=AC\\otimes BD\\) whenever "
        "the products are defined, and \\(\\operatorname{tr}(A\\otimes B)="
        "\\operatorname{tr}(A)\\operatorname{tr}(B)\\).")
)

S4 = (
    p("Fix the Pauli matrices, the basis of \\(2\\times2\\) Hermitian traceless operators:")
    + eq(r"\sigma_x = X = \begin{pmatrix}0&1\\1&0\end{pmatrix},\quad "
         r"\sigma_y = Y = \begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad "
         r"\sigma_z = Z = \begin{pmatrix}1&0\\0&-1\end{pmatrix}")
    + p("They satisfy \\(X^2=Y^2=Z^2=I\\), anticommute pairwise "
        "(\\(\\{\\sigma_a,\\sigma_b\\}=2\\delta_{ab}I\\)), and obey "
        "\\([\\sigma_a,\\sigma_b]=2i\\,\\varepsilon_{abc}\\sigma_c\\). Together with \\(I\\) they "
        "form an orthogonal basis of \\(\\mathcal B(\\mathbb C^{2})\\) under the "
        "Hilbert–Schmidt inner product \\(\\langle A,B\\rangle_{HS}=\\operatorname{tr}(A^{\\dagger}B)\\).")
    + box('prop', 'Pauli expansion',
          "Any \\(A\\in\\mathcal B(\\mathbb C^{2})\\) can be written uniquely as "
          "\\(A=\\tfrac12\\big(a_0 I + a_x X + a_y Y + a_z Z\\big)\\) with "
          "\\(a_\\mu=\\operatorname{tr}(\\sigma_\\mu A)\\). For \\(n\\) qubits the "
          "\\(4^{n}\\) Pauli strings \\(\\sigma_{\\mu_1}\\otimes\\cdots\\otimes\\sigma_{\\mu_n}\\) "
          "form an orthogonal basis of \\(\\mathcal B((\\mathbb C^{2})^{\\otimes n})\\). "
          "This is the representation used by every variational algorithm of Chapter 10 and by "
          "the stabilizer formalism of Chapter 9.")
    + p("A key consequence of \\(\\hat n\\cdot\\vec\\sigma\\) squaring to \\(I\\) for any unit "
        "vector \\(\\hat n\\) is the rotation formula, obtained by splitting the exponential "
        "series into even and odd terms:")
    + eq(r"e^{-i\theta (\hat n\cdot\vec\sigma)/2} \;=\; \cos\!\tfrac{\theta}{2}\, I \;-\; "
         r"i\sin\!\tfrac{\theta}{2}\,(\hat n\cdot\vec\sigma)")
    + p("Every single-qubit unitary is, up to global phase, such a rotation — the isomorphism "
        "\\(SU(2)/\\{\\pm I\\}\\cong SO(3)\\) that Chapter 2 turns into the Bloch sphere picture.")
)

S5 = (
    p("Three matrix norms recur. The <em>operator norm</em> "
      "\\(\\|A\\|_{\\infty}=\\max_{\\|\\psi\\|=1}\\|A\\psi\\|\\) equals the largest singular value "
      "and controls worst-case error of a gate approximation. The <em>trace norm</em> "
      "\\(\\|A\\|_1=\\operatorname{tr}\\sqrt{A^{\\dagger}A}\\) governs distinguishability of "
      "quantum states (Chapter 5). The <em>Frobenius/Hilbert–Schmidt norm</em> "
      "\\(\\|A\\|_2=\\sqrt{\\operatorname{tr}(A^{\\dagger}A)}\\) is the one NumPy computes fastest.")
    + box('prop', 'Error accumulates at most linearly',
          "If \\(\\|U_j - V_j\\|_{\\infty}\\le\\varepsilon\\) for \\(j=1,\\dots,m\\) with all "
          "\\(U_j,V_j\\) unitary, then \\(\\|U_m\\cdots U_1 - V_m\\cdots V_1\\|_{\\infty}\\le m\\varepsilon\\). "
          "Proof: telescope the difference and use unitary invariance of the operator norm. "
          "This bound is what makes the Solovay–Kitaev theorem (Chapter 3) usable and what "
          "sets accuracy targets for fault-tolerant compilation.")
    + p("Numerically, unitarity is checked by \\(\\|U^{\\dagger}U-I\\|\\le\\)&nbsp;tolerance, never "
        "by exact equality: floating-point arithmetic is not exact, and repeated Kronecker "
        "products amplify rounding. Throughout the practical work we use "
        "<code>numpy.allclose</code> with the default tolerance \\(10^{-8}\\).")
    + code('''import numpy as np

def dagger(A):
    """Conjugate transpose (Hermitian adjoint)."""
    return A.conj().T

def is_unitary(U, tol=1e-9):
    U = np.asarray(U, dtype=complex)
    return np.allclose(dagger(U) @ U, np.eye(U.shape[0]), atol=tol)

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

# Kronecker product of an arbitrary list of operators
def kron_all(ops):
    out = np.array([[1.0 + 0j]])
    for op in ops:
        out = np.kron(out, op)
    return out

print(is_unitary(X), kron_all([X, Z]).shape)   # True (4, 4)''',
           'Reference implementation used throughout the practical exercises')
)

S6 = (
    p("A postulate-level summary, stated here for pure closed systems and generalised in "
      "Chapter 5 to density operators and open dynamics.")
    + ol([
        "<strong>States.</strong> The state of an isolated system is a unit vector "
        "\\(|\\psi\\rangle\\in\\mathcal H\\), defined up to a global phase "
        "\\(e^{i\\alpha}\\) which is physically unobservable.",
        "<strong>Evolution.</strong> Closed-system dynamics is unitary: "
        "\\(|\\psi(t)\\rangle=U(t)|\\psi(0)\\rangle\\), equivalently "
        "\\(i\\,\\partial_t|\\psi\\rangle=H|\\psi\\rangle\\) (Schrödinger equation).",
        "<strong>Measurement.</strong> A projective measurement of observable "
        "\\(A=\\sum_k\\lambda_k P_k\\) yields outcome \\(\\lambda_k\\) with probability "
        "\\(p_k=\\langle\\psi|P_k|\\psi\\rangle\\), leaving the post-measurement state "
        "\\(P_k|\\psi\\rangle/\\sqrt{p_k}\\) (Born rule + projection postulate).",
        "<strong>Composition.</strong> The state space of a composite system is the tensor "
        "product of the component state spaces."])
    + box('note', 'Why global phase is unobservable but relative phase is not',
          "Probabilities depend on \\(|\\langle\\phi|\\psi\\rangle|^{2}\\), which is invariant "
          "under \\(|\\psi\\rangle\\mapsto e^{i\\alpha}|\\psi\\rangle\\). But "
          "\\((|0\\rangle+|1\\rangle)/\\sqrt2\\) and \\((|0\\rangle-|1\\rangle)/\\sqrt2\\) are "
          "orthogonal and perfectly distinguishable: the <em>relative</em> phase between basis "
          "components is physical, and interference — the source of every quantum speed-up in "
          "this course — is exactly the manipulation of relative phases.")
)

# =============================== figures, citations and added commentary =====
JS_ERR = '''  var b = JXG.JSXGraph.initBoard('ch1err', {boundingbox: [-130, 1.18, 1060, -0.16],
      axis: true, showCopyright: false, showNavigation: false});
  var k = b.create('slider', [[60, 1.08], [520, 1.08], [2, 3, 6]],
      {name: 'log&#8321;&#8320;(1/&#949;)', snapWidth: 0.25, strokeColor: '#026573'});
  b.create('functiongraph', [function (m) { return m * Math.pow(10, -k.Value()); }, 0, 1000],
      {strokeColor: '#026573', strokeWidth: 2.6});
  b.create('line', [[0, 0.1], [1000, 0.1]],
      {strokeColor: '#dc2626', dash: 2, straightFirst: false, straightLast: false});
  b.create('text', [610, 0.12, 'usable accuracy 0.1'], {fontSize: 12, strokeColor: '#dc2626'});
  b.create('text', [-110, 1.08, function () {
      var eps = Math.pow(10, -k.Value());
      return 'per-gate error ' + eps.toExponential(1) +
             '  \u2192  at most ' + Math.round(0.1 / eps) + ' gates';
  }], {fontSize: 14, strokeColor: '#0f172a'});
  b.create('text', [420, -0.13, 'circuit length m'], {fontSize: 13, strokeColor: '#475569'});
'''

DIRAC_SVG = f'''
<rect x="0" y="0" width="680" height="300" fill="#ffffff"/>
<text x="340" y="20" font-family="{SERIF}" font-size="13" fill="{C['accent']}" text-anchor="middle" font-weight="bold">The four objects of Dirac notation</text>
<rect x="34" y="44" width="26" height="92" rx="3" fill="#ecfeff" stroke="{C['accent']}" stroke-width="1.6"/>
<text x="47" y="74" font-family="{MONO}" font-size="13" fill="{C['ink']}" text-anchor="middle">a&#8320;</text>
<text x="47" y="98" font-family="{MONO}" font-size="13" fill="{C['ink']}" text-anchor="middle">a&#8321;</text>
<text x="47" y="122" font-family="{MONO}" font-size="13" fill="{C['ink']}" text-anchor="middle">&#8942;</text>
<text x="47" y="160" font-family="{SERIF}" font-size="13" fill="{C['accent']}" text-anchor="middle" font-weight="bold">|&#968;&#10217;</text>
<text x="47" y="180" font-family="{SERIF}" font-size="11.5" fill="{C['muted']}" text-anchor="middle">ket</text>
<text x="47" y="196" font-family="{SERIF}" font-size="11.5" fill="{C['muted']}" text-anchor="middle">column, d&#215;1</text>
<rect x="128" y="76" width="118" height="26" rx="3" fill="#fefce8" stroke="{C['gold']}" stroke-width="1.6"/>
<text x="187" y="94" font-family="{MONO}" font-size="13" fill="{C['ink']}" text-anchor="middle">a&#8320;&#773;  a&#8321;&#773;  &#8943;</text>
<text x="187" y="160" font-family="{SERIF}" font-size="13" fill="#92400e" text-anchor="middle" font-weight="bold">&#10216;&#968;|</text>
<text x="187" y="180" font-family="{SERIF}" font-size="11.5" fill="{C['muted']}" text-anchor="middle">bra</text>
<text x="187" y="196" font-family="{SERIF}" font-size="11.5" fill="{C['muted']}" text-anchor="middle">row, 1&#215;d</text>
<line x1="272" y1="44" x2="272" y2="230" stroke="{C['line']}" stroke-width="1.5"/>
<text x="368" y="70" font-family="{SERIF}" font-size="13" fill="{C['ink']}" text-anchor="middle">&#10216;&#966;| &#183; |&#968;&#10217;</text>
<rect x="344" y="82" width="48" height="30" rx="3" fill="#f5f3ff" stroke="#9333ea" stroke-width="1.6"/>
<text x="368" y="102" font-family="{MONO}" font-size="13" fill="#3b0764" text-anchor="middle">z</text>
<text x="368" y="134" font-family="{SERIF}" font-size="12" fill="{C['muted']}" text-anchor="middle">1&#215;d &#183; d&#215;1 = scalar</text>
<text x="368" y="152" font-family="{SERIF}" font-size="12" fill="{C['muted']}" text-anchor="middle">the inner product</text>
<text x="368" y="176" font-family="{SERIF}" font-size="11.5" fill="{C['muted']}" text-anchor="middle">overlap / probability amplitude</text>
<text x="560" y="70" font-family="{SERIF}" font-size="13" fill="{C['ink']}" text-anchor="middle">|&#968;&#10217; &#183; &#10216;&#966;|</text>
<rect x="524" y="82" width="72" height="72" rx="3" fill="#f0fdfa" stroke="{C['accent']}" stroke-width="1.6"/>
<line x1="524" y1="106" x2="596" y2="106" stroke="{C['accent2']}" stroke-width="0.8"/>
<line x1="524" y1="130" x2="596" y2="130" stroke="{C['accent2']}" stroke-width="0.8"/>
<line x1="548" y1="82" x2="548" y2="154" stroke="{C['accent2']}" stroke-width="0.8"/>
<line x1="572" y1="82" x2="572" y2="154" stroke="{C['accent2']}" stroke-width="0.8"/>
<text x="560" y="176" font-family="{SERIF}" font-size="12" fill="{C['muted']}" text-anchor="middle">d&#215;1 &#183; 1&#215;d = matrix</text>
<text x="560" y="194" font-family="{SERIF}" font-size="12" fill="{C['muted']}" text-anchor="middle">the outer product</text>
<text x="560" y="218" font-family="{SERIF}" font-size="11.5" fill="{C['muted']}" text-anchor="middle">projector when |&#966;&#10217;=|&#968;&#10217;, &#8214;&#968;&#8214;=1</text>
<rect x="34" y="244" width="612" height="40" rx="6" fill="{C['panel']}" stroke="{C['line']}"/>
<text x="340" y="262" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="middle">Completeness: &#8721;&#7522; |i&#10217;&#10216;i| = I &#8212; inserting this identity between operators is what produces matrix components A&#7522;&#11388; = &#10216;i|A|j&#10217;</text>
<text x="340" y="278" font-family="{SERIF}" font-size="12.5" fill="{C['muted']}" text-anchor="middle">Every manipulation in this course is one of these four products, repeated.</text>
'''

_ns = list(range(1, 61))
GROWTH = line_chart(
    [dict(label='complex amplitudes  2ⁿ', xs=_ns, ys=[n * log10(2) for n in _ns], color='#026573'),
     dict(label='memory at 16 bytes each (log₁₀ bytes)', xs=_ns,
          ys=[n * log10(2) + log10(16) for n in _ns], color='#c9a227', dash='6 4'),
     dict(label='classical bits  n', xs=_ns, ys=[log10(n) for n in _ns], color='#9333ea')],
    xlim=(1, 60), ylim=(0, 20), xticks=[1,10,20,30,40,50,60], yticks=[0,5,10,15,20],
    xlabel='number of qubits  n',
    ylabel='log₁₀ (quantity)',
    hlines=[(12, 'a terabyte of RAM', '#dc2626'), (18, 'an exabyte', '#dc2626')],
    vlines=[(50, 'n = 50', '#475569')], height=330)

KRON_SVG = f'''
<rect x="0" y="0" width="680" height="270" fill="#ffffff"/>
<text x="340" y="20" font-family="{SERIF}" font-size="13" fill="{C['accent']}" text-anchor="middle" font-weight="bold">The Kronecker product replicates B in blocks weighted by the entries of A</text>
<text x="72" y="130" font-family="{SERIF}" font-size="15" fill="{C['ink']}" text-anchor="middle">A</text>
<rect x="40" y="80" width="64" height="64" rx="3" fill="#ecfeff" stroke="{C['accent']}" stroke-width="1.6"/>
<text x="56" y="106" font-family="{MONO}" font-size="12" fill="{C['ink']}" text-anchor="middle">a&#8320;&#8320;</text>
<text x="88" y="106" font-family="{MONO}" font-size="12" fill="{C['ink']}" text-anchor="middle">a&#8320;&#8321;</text>
<text x="56" y="134" font-family="{MONO}" font-size="12" fill="{C['ink']}" text-anchor="middle">a&#8321;&#8320;</text>
<text x="88" y="134" font-family="{MONO}" font-size="12" fill="{C['ink']}" text-anchor="middle">a&#8321;&#8321;</text>
<text x="128" y="118" font-family="{SERIF}" font-size="18" fill="{C['muted']}" text-anchor="middle">&#8855;</text>
<rect x="150" y="80" width="64" height="64" rx="3" fill="#fefce8" stroke="{C['gold']}" stroke-width="1.6"/>
<text x="182" y="118" font-family="{MONO}" font-size="14" fill="#92400e" text-anchor="middle">B</text>
<text x="238" y="118" font-family="{SERIF}" font-size="18" fill="{C['muted']}" text-anchor="middle">=</text>
<rect x="272" y="52" width="180" height="180" rx="4" fill="#ffffff" stroke="{C['accent']}" stroke-width="2"/>
<rect x="276" y="56" width="86" height="86" rx="3" fill="#fefce8" stroke="{C['gold']}" stroke-width="1.3"/>
<rect x="366" y="56" width="86" height="86" rx="3" fill="#fefce8" stroke="{C['gold']}" stroke-width="1.3"/>
<rect x="276" y="146" width="86" height="86" rx="3" fill="#fefce8" stroke="{C['gold']}" stroke-width="1.3"/>
<rect x="366" y="146" width="86" height="86" rx="3" fill="#fefce8" stroke="{C['gold']}" stroke-width="1.3"/>
<text x="319" y="104" font-family="{MONO}" font-size="13" fill="#92400e" text-anchor="middle">a&#8320;&#8320; B</text>
<text x="409" y="104" font-family="{MONO}" font-size="13" fill="#92400e" text-anchor="middle">a&#8320;&#8321; B</text>
<text x="319" y="194" font-family="{MONO}" font-size="13" fill="#92400e" text-anchor="middle">a&#8321;&#8320; B</text>
<text x="409" y="194" font-family="{MONO}" font-size="13" fill="#92400e" text-anchor="middle">a&#8321;&#8321; B</text>
<text x="478" y="90" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">Ordering convention used here:</text>
<text x="478" y="110" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">qubit 0 is the LEFT factor, i.e.</text>
<text x="478" y="130" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">the most significant bit of the</text>
<text x="478" y="150" font-family="{SERIF}" font-size="12.5" fill="{C['body']}" text-anchor="start">basis-state index.</text>
<text x="478" y="178" font-family="{SERIF}" font-size="12" fill="{C['muted']}" text-anchor="start">|01&#10217; is index 1;</text>
<text x="478" y="196" font-family="{SERIF}" font-size="12" fill="{C['muted']}" text-anchor="start">|10&#10217; is index 2.</text>
'''

CLASSES = nested_svg(
    [('ℒ(ℋ) — all linear operators', '#94a3b8'),
     ('Normal:  NN† = N†N   ⇒  orthonormal eigenbasis', '#0891a1'),
     ('Hermitian:  A = A†   ⇒  real spectrum  (observables)', '#026573'),
     ('Positive semidefinite:  A ≥ 0  (density operators)', '#c9a227'),
     ('Projectors:  P = P² = P†  (measurement outcomes)', '#9333ea')],
    height=290)

_ms = list(range(0, 1001, 20))
ERRACC = line_chart(
    [dict(label='ε = 10⁻³ per gate', xs=_ms, ys=[m * 1e-3 for m in _ms], color='#dc2626'),
     dict(label='ε = 10⁻⁴', xs=_ms, ys=[m * 1e-4 for m in _ms], color='#c9a227'),
     dict(label='ε = 10⁻⁵', xs=_ms, ys=[m * 1e-5 for m in _ms], color='#026573')],
    xlim=(0, 1000), ylim=(0, 1.0), xticks=[0,200,400,600,800,1000],
    yticks=[0,0.25,0.5,0.75,1.0], xlabel='circuit length  m  (number of gates)',
    ylabel='worst-case error bound  mε',
    hlines=[(0.1, 'usable accuracy threshold', '#475569')], height=320)

PAULI_BARS = bar_chart(['a₀ (I)', 'aₓ (X)', 'a_y (Y)', 'a_z (Z)'],
                       [0.0, 1 / sqrt(2), 0.0, 1 / sqrt(2)],
                       ylim=(0, 1.0), ylabel='coefficient', highlight=None, height=290,
                       colors=['#94a3b8', '#026573', '#94a3b8', '#026573'])

S1 = S1 + figure(
    '1.1',
    'The four products of Dirac notation and their matrix shapes. Reading a quantum-mechanical '
    'expression is largely a matter of recognising which of these four it is: a ket (a column), '
    'a bra (its conjugate-transposed row), a bra applied to a ket (a number — an amplitude), or a '
    'ket applied to a bra (a matrix — an operator). The completeness relation shown at the bottom '
    'is the device that converts abstract statements into components.',
    DIRAC_SVG, height=300) + p(
    "It is worth dwelling on why the bra–ket split is more than notation" + cite('1') + ". A finite-dimensional "
    "Hilbert space is canonically isomorphic to its dual by the Riesz representation theorem, and "
    "Dirac notation makes that isomorphism typographically visible: the same physical state has a "
    "column form when it is being acted on and a row form when it is doing the acting. Once this "
    "is internalised, expressions such as \\(\\operatorname{tr}(A|\\psi\\rangle\\langle\\psi|)="
    "\\langle\\psi|A|\\psi\\rangle\\) can be read off by moving the bra cyclically around the trace "
    "rather than by computing anything.") + sources(
    'Nielsen &amp; Chuang §2.1' + cite('1') + '; Watrous ch. 1 develops the same material with '
    'full functional-analytic care' + cite('2') + '.')

S2 = S2 + figure(
    '1.2',
    'The operator classes used in this course form a chain of inclusions. Normality is exactly the '
    'condition for an orthonormal eigenbasis to exist; hermiticity adds a real spectrum; positivity '
    'adds a non-negative spectrum; and idempotence singles out the projectors, whose spectrum is '
    '{0,1}. Unitaries are normal but not generally Hermitian, so they sit inside the second ring '
    'without descending further.',
    CLASSES, height=290) + p(
    "The diagram makes one pedagogical point that is easy to lose in the algebra: the spectral "
    "theorem is a statement about the second ring, not the third" + cite('2,4') + ". Unitary "
    "operators are diagonalisable with orthonormal eigenvectors just as Hermitian ones are — their "
    "eigenvalues simply lie on the unit circle rather than the real line. This is why the same "
    "functional calculus \\(f(A)=\\sum_k f(\\lambda_k)P_k\\) applies to gates and to Hamiltonians "
    "alike, and why the map \\(H\\mapsto e^{-iHt}\\) is a bijection (up to \\(2\\pi\\) ambiguity) "
    "between the third ring and the unitaries.") + sources(
    'Spectral theorem and functional calculus: Watrous §1.1' + cite('2') + ', Bhatia ch. 1'
    + cite('4') + '; the physical reading of each class is Preskill ch. 2' + cite('5') + '.')

S3 = S3 + figure(
    '1.3',
    'Why the tensor product, and not the direct sum, is the source of quantum computational power. '
    'The number of complex amplitudes needed to describe an n-qubit pure state grows as 2ⁿ, so the '
    'classical memory required to store one crosses a terabyte near n = 40 and an exabyte near n = 60. '
    'A classical n-bit register, by contrast, needs only n bits (purple). The dashed line converts '
    'amplitudes to bytes at 16 bytes per double-precision complex number.',
    GROWTH, height=330) + figure(
    '1.4',
    'Block structure of the Kronecker product, and the index convention fixed once and for all in '
    'this course. Each entry of A is replaced by that entry times the whole of B. Reading the '
    'resulting basis label as a binary string, qubit 0 contributes the most significant bit. '
    'Software packages differ on this point; the exercises state the convention explicitly wherever '
    'it matters.',
    KRON_SVG, height=270) + p(
    "The exponential in Figure 1.3 is the whole argument for quantum computing, and also the whole "
    "argument for why it is hard to verify. A device holding 60 qubits manipulates a vector that no "
    "classical machine can write down; but the same device outputs only 60 classical bits per run, "
    "so the exponential is never directly visible. Every algorithm in Chapters 6 to 8 is a scheme "
    "for arranging interference so that a polynomial amount of extracted classical information is "
    "nevertheless useful" + cite('3,6') + ". It is also worth noting that exponential dimension "
    "alone is not sufficient for hardness: Chapter 9's stabilizer formalism describes states in "
    "\\(2^{n}\\)-dimensional spaces that are simulable in \\(O(n^{2})\\) time.") + sources(
    'Tensor products and the dimension argument: Nielsen &amp; Chuang §2.1.7' + cite('1') + '; the '
    'critical discussion of what the exponential does and does not buy is Aaronson lectures 9–10'
    + cite('6') + '.')

S4 = S4 + figure(
    '1.5',
    'Pauli coefficients of the Hadamard gate, H = (X + Z)/√2. Expanding an operator in the Pauli '
    'basis is an orthogonal projection under the Hilbert–Schmidt inner product, so the coefficients '
    'are read off by a single trace each: aμ = tr(σμ A)/2. This is the representation used by every '
    'variational algorithm and by the stabilizer formalism.',
    PAULI_BARS, height=290) + p(
    "The Pauli basis is not merely convenient; it is the unique basis in which the two structures "
    "that matter — the algebra (products of Paulis are Paulis up to phase) and the geometry "
    "(orthogonality under \\(\\operatorname{tr}A^{\\dagger}B\\)) — coincide" + cite('1') + ". "
    "Chapter 3 exploits the algebra when it shows that Clifford gates permute Pauli strings; "
    "Chapter 9 turns that permutation action into an error-correction scheme; and Chapter 10 uses "
    "the geometry, since measuring \\(\\langle P_j\\rangle\\) for each Pauli string in a "
    "Hamiltonian is precisely how a device estimates an energy.") + sources(
    'Pauli algebra and the SU(2)/SO(3) correspondence: Nielsen &amp; Chuang §4.2' + cite('1') +
    ', Preskill ch. 2' + cite('5') + '.')

S5 = S5 + figure(
    '1.6',
    'Linear accumulation of gate error. If every gate is implemented to accuracy ε in operator norm, '
    'a circuit of m gates is accurate to mε — no worse, because the operator norm is unitarily '
    'invariant, and no better in the worst case. Reading off the crossings with a usable-accuracy '
    'line gives the maximum circuit length at each per-gate fidelity: about 100 gates at ε = 10⁻³, '
    'and about 10⁴ at ε = 10⁻⁵.',
    ERRACC, height=320) + p(
    "This single plot explains the structure of the second half of the course. Present-day hardware "
    "sits near \\(\\varepsilon\\approx10^{-3}\\), so unmitigated circuits are limited to a few "
    "hundred gates — far short of the \\(10^{10}\\)-gate circuits that factoring a cryptographic "
    "modulus requires (Chapter 7). Two responses follow: design algorithms that fit inside the "
    "budget (Chapter 10), or change the budget by encoding logical qubits whose effective "
    "\\(\\varepsilon\\) is exponentially smaller than the physical one (Chapter 9)." + cite('4') +
    " The bound itself is elementary — telescope \\(U_m\\cdots U_1-V_m\\cdots V_1\\) into \\(m\\) "
    "terms, each of which is a product of unitaries around a single difference — but it is tight, "
    "and no cleverness at the compiler level can beat it.") + sources(
    'Norms, unitary invariance and perturbation bounds: Bhatia ch. 2–3' + cite('4') + '; the '
    'circuit-level consequence is spelled out in Nielsen &amp; Chuang §4.5.3' + cite('1') + '.')

S5 = S5 + interactive(
    '1.7', 'ch1err',
    'Move the slider to set the per-gate error rate and read off the longest circuit that stays '
    'below a usable total error of 0.1. Superconducting and trapped-ion devices currently sit near '
    '10&#8315;&#179; and 10&#8315;&#8308; respectively; the plot shows directly why unencoded circuits '
    'of more than a few thousand gates are out of reach without the error correction of Chapter 9.',
    JS_ERR, aspect='16/9', max_width=640,
    hint='drag the slider to change the per-gate error rate &#949;.')

S6 = S6 + sources(
    'The postulates in this form: Nielsen &amp; Chuang §2.2' + cite('1') + ' and Preskill ch. 2'
    + cite('5') + '; the density-operator generalisation is deferred to Chapter 5.')

REFS = [
    dict(authors="M. A. Nielsen and I. L. Chuang",
         title="Quantum Computation and Quantum Information (10th Anniversary Edition)",
         venue="Cambridge University Press", year="2010",
         note="Chapter 2 (§2.1–2.2) is the canonical treatment of the linear algebra used here."),
    dict(authors="J. Watrous", title="The Theory of Quantum Information",
         venue="Cambridge University Press", year="2018",
         link="https://cs.uwaterloo.ca/~watrous/TQI/",
         note="Chapter 1 develops operator theory rigorously; free author PDF."),
    dict(authors="A. Yu. Kitaev, A. H. Shen and M. N. Vyalyi",
         title="Classical and Quantum Computation",
         venue="AMS Graduate Studies in Mathematics 47", year="2002",
         note="Concise, complexity-theoretic framing of the same formalism."),
    dict(authors="R. Bhatia", title="Matrix Analysis",
         venue="Springer GTM 169", year="1997",
         note="Reference for norms, unitary invariance and perturbation bounds used in §5."),
    dict(authors="J. Preskill", title="Lecture Notes for Physics 219: Quantum Computation",
         venue="Caltech", year="2022",
         link="http://theory.caltech.edu/~preskill/ph219/",
         note="Chapter 2 covers axioms and the density-operator generalisation."),
    dict(authors="S. Aaronson", title="Quantum Computing Since Democritus",
         venue="Cambridge University Press", year="2013",
         note="Lectures 9–10 give the conceptual 'why amplitudes, why the 2-norm' argument."),
]

# ---------------------------------------------------------------- CodeRunner
CR = [
    dict(
        name='C1.Q1 — Adjoint, unitarity and hermiticity',
        qtext=cr_qtext('C1.Q1', 'Operator predicates',
                       "Numerical linear algebra is the substrate of every simulation in this "
                       "course. Before anything else we need reliable predicates for the "
                       "operator classes of \\S2.",
                       "Write three functions using <strong>NumPy only</strong>: "
                       "<code>dagger(A)</code> returning the conjugate transpose; "
                       "<code>is_unitary(A, tol=1e-9)</code> returning a Python <code>bool</code>; "
                       "and <code>is_hermitian(A, tol=1e-9)</code> returning a Python "
                       "<code>bool</code>. Use <code>numpy.allclose</code> with <code>atol=tol</code>; "
                       "do not test exact equality.",
                       "dagger([[0,1j],[0,0]])  ->  [[0, 0], [-1j, 0]]\n"
                       "is_unitary(X)           ->  True\n"
                       "is_hermitian(X @ Y)     ->  False"),
        answer='''import numpy as np

def dagger(A):
    return np.asarray(A, dtype=complex).conj().T

def is_unitary(A, tol=1e-9):
    A = np.asarray(A, dtype=complex)
    n = A.shape[0]
    return bool(np.allclose(dagger(A) @ A, np.eye(n), atol=tol))

def is_hermitian(A, tol=1e-9):
    A = np.asarray(A, dtype=complex)
    return bool(np.allclose(A, dagger(A), atol=tol))
''',
        preload='''import numpy as np

def dagger(A):
    # TODO: conjugate transpose
    ...

def is_unitary(A, tol=1e-9):
    # TODO
    ...

def is_hermitian(A, tol=1e-9):
    # TODO
    ...
''',
        tests=[
            {'code': 'import numpy as np\nX = np.array([[0,1],[1,0]], dtype=complex)\n'
                     'print(is_unitary(X), is_hermitian(X))\n',
             'expected': 'True True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nA = np.array([[0,1j],[0,0]], dtype=complex)\n'
                     'print(np.allclose(dagger(A), np.array([[0,0],[-1j,0]])))\n',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nY = np.array([[0,-1j],[1j,0]], dtype=complex)\n'
                     'Z = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'print(is_hermitian(Y @ Z), is_unitary(Y @ Z))\n',
             'expected': 'False True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nH = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)\n'
                     'print(is_unitary(H), is_hermitian(H))\n',
             'expected': 'True True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nD = np.diag([1, 2.0]).astype(complex)\n'
                     'print(is_unitary(D), is_hermitian(D))\n',
             'expected': 'False True\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C1.Q2 — Kronecker products and multi-qubit operators',
        qtext=cr_qtext('C1.Q2', 'Building the n-qubit algebra',
                       "Multi-qubit gates are built from single-qubit ones by tensoring with "
                       "identities. Getting the factor ordering right is the most common source "
                       "of simulator bugs.",
                       "Write <code>kron_all(ops)</code> returning the Kronecker product of a "
                       "list of matrices (returning the \\(1\\times1\\) identity for an empty "
                       "list), and <code>embed(op, target, n)</code> returning the "
                       "\\(2^{n}\\times2^{n}\\) operator that applies the single-qubit "
                       "<code>op</code> to qubit index <code>target</code> "
                       "(0 = leftmost/most significant factor) and the identity elsewhere.",
                       "embed(X, 0, 2)  ==  kron(X, I)\n"
                       "embed(Z, 1, 3)  ==  kron(I, kron(Z, I))"),
        answer='''import numpy as np

def kron_all(ops):
    out = np.array([[1.0 + 0j]])
    for op in ops:
        out = np.kron(out, np.asarray(op, dtype=complex))
    return out

def embed(op, target, n):
    I2 = np.eye(2, dtype=complex)
    factors = [np.asarray(op, dtype=complex) if k == target else I2 for k in range(n)]
    return kron_all(factors)
''',
        preload='''import numpy as np

def kron_all(ops):
    # TODO: iterate with np.kron starting from [[1]]
    ...

def embed(op, target, n):
    # TODO
    ...
''',
        tests=[
            {'code': 'import numpy as np\nX = np.array([[0,1],[1,0]], dtype=complex)\n'
                     'print(embed(X, 0, 2).shape)\n',
             'expected': '(4, 4)\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nX = np.array([[0,1],[1,0]], dtype=complex)\n'
                     'I = np.eye(2, dtype=complex)\n'
                     'print(np.allclose(embed(X, 1, 2), np.kron(I, X)))\n',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'I = np.eye(2, dtype=complex)\n'
                     'print(np.allclose(embed(Z, 1, 3), np.kron(I, np.kron(Z, I))))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(kron_all([]).shape, np.round(kron_all([]).real[0,0], 6))\n',
             'expected': '(1, 1) 1.0\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nX = np.array([[0,1],[1,0]], dtype=complex)\n'
                     'Z = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'M = kron_all([X, Z, X])\nprint(M.shape, int(round(np.trace(M @ M).real)))\n',
             'expected': '(8, 8) 8\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C1.Q3 — Spectral decomposition and operator functions',
        qtext=cr_qtext('C1.Q3', 'Exponentiating a Hamiltonian',
                       "By the spectral theorem, \\(f(A)=\\sum_k f(\\lambda_k)P_k\\). "
                       "Implementing \\(e^{-iHt}\\) this way — rather than by truncating the "
                       "power series — is both exact and numerically stable.",
                       "Write <code>spectral_projectors(H)</code> returning "
                       "<code>(eigenvalues, projectors)</code> where eigenvalues is a sorted "
                       "1-D real array and projectors[k] is the rank-one projector onto the "
                       "\\(k\\)-th eigenvector; and <code>evolve(H, t)</code> returning "
                       "\\(e^{-iHt}\\) built from that decomposition. Use "
                       "<code>numpy.linalg.eigh</code> (never <code>scipy</code>).",
                       "evolve(Z, pi/2)  ->  diag(exp(-i*pi/2), exp(+i*pi/2))"),
        answer='''import numpy as np

def spectral_projectors(H):
    H = np.asarray(H, dtype=complex)
    vals, vecs = np.linalg.eigh(H)
    projs = [np.outer(vecs[:, k], vecs[:, k].conj()) for k in range(len(vals))]
    return vals, projs

def evolve(H, t):
    vals, projs = spectral_projectors(H)
    n = np.asarray(H).shape[0]
    U = np.zeros((n, n), dtype=complex)
    for lam, P in zip(vals, projs):
        U = U + np.exp(-1j * lam * t) * P
    return U
''',
        preload='''import numpy as np

def spectral_projectors(H):
    # TODO: use np.linalg.eigh and np.outer
    ...

def evolve(H, t):
    # TODO: sum exp(-i*lambda*t) * P
    ...
''',
        tests=[
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'vals, projs = spectral_projectors(Z)\nprint(np.round(vals, 6).tolist())\n',
             'expected': '[-1.0, 1.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'U = evolve(Z, np.pi/2)\n'
                     'print(np.allclose(U, np.diag([np.exp(-1j*np.pi/2), np.exp(1j*np.pi/2)])))\n',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nX = np.array([[0,1],[1,0]], dtype=complex)\n'
                     'th = 0.7\nU = evolve(X, th/2)\n'
                     'R = np.cos(th/2)*np.eye(2) - 1j*np.sin(th/2)*X\n'
                     'print(np.allclose(U, R))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nrng = np.random.default_rng(7)\n'
                     'A = rng.normal(size=(4,4)) + 1j*rng.normal(size=(4,4))\n'
                     'H = A + A.conj().T\nU = evolve(H, 1.3)\n'
                     'print(np.allclose(U.conj().T @ U, np.eye(4)))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'vals, projs = spectral_projectors(Z)\n'
                     'print(np.allclose(sum(projs), np.eye(2)))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C1.Q4 — Pauli decomposition of an operator',
        qtext=cr_qtext('C1.Q4', 'Coordinates in the Pauli basis',
                       "Variational algorithms (Chapter 10) and the stabilizer formalism "
                       "(Chapter 9) both express Hamiltonians as real linear combinations of "
                       "Pauli strings. The coefficients come from the Hilbert–Schmidt inner "
                       "product \\(a_{\\mu}=\\tfrac{1}{2^{n}}\\operatorname{tr}(\\sigma_{\\mu}A)\\).",
                       "Write <code>pauli_coeffs(A)</code> for a single qubit, returning the "
                       "list <code>[a_i, a_x, a_y, a_z]</code> of coefficients such that "
                       "\\(A=a_I I + a_x X + a_y Y + a_z Z\\). Round each coefficient to 6 "
                       "decimals and return them as Python <code>complex</code> numbers is not "
                       "required — return floats when the imaginary part is negligible by "
                       "taking <code>numpy.real_if_close</code>, then convert with "
                       "<code>float</code> if real.",
                       "pauli_coeffs(Z)          ->  [0.0, 0.0, 0.0, 1.0]\n"
                       "pauli_coeffs(eye(2))     ->  [1.0, 0.0, 0.0, 0.0]"),
        answer='''import numpy as np

def pauli_coeffs(A):
    A = np.asarray(A, dtype=complex)
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    out = []
    for S in (I2, X, Y, Z):
        c = np.trace(S.conj().T @ A) / 2
        c = np.real_if_close(c, tol=1000)
        out.append(round(float(c.real), 6) if np.abs(np.imag(c)) < 1e-9 else complex(round(c.real, 6), round(c.imag, 6)))
    return out
''',
        preload='''import numpy as np

def pauli_coeffs(A):
    # coefficient a_mu = trace(sigma_mu^dagger @ A) / 2
    ...
''',
        tests=[
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'print(pauli_coeffs(Z))\n',
             'expected': '[0.0, 0.0, 0.0, 1.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(pauli_coeffs(np.eye(2, dtype=complex)))\n',
             'expected': '[1.0, 0.0, 0.0, 0.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nH = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)\n'
                     'print([round(c, 4) for c in pauli_coeffs(H)])\n',
             'expected': '[0.0, 0.7071, 0.0, 0.7071]\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nY = np.array([[0,-1j],[1j,0]], dtype=complex)\n'
                     'print(pauli_coeffs(Y))\n',
             'expected': '[0.0, 0.0, 1.0, 0.0]\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nP0 = np.array([[1,0],[0,0]], dtype=complex)\n'
                     'print(pauli_coeffs(P0))\n',
             'expected': '[0.5, 0.0, 0.0, 0.5]\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

# --------------------------------------------------------------------- STACK
ST = [
    stack_question(
        name='C1.S1 — Normalisation of a qubit state',
        questiontext=stack_qtext(
            'C1.S1', 'Normalisation',
            r'<p>A qubit is prepared in the state \(|\psi\rangle = \frac{1}{\sqrt{ {@a@} }}|0\rangle + b\,|1\rangle\) '
            r'with \(b\) real and positive.</p>'
            r'<p>Determine \(b\) so that \(\langle\psi|\psi\rangle = 1\). Give an exact expression '
            r'(no decimals).</p><p>\(b=\) [[input:ans1]] [[validation:ans1]]</p>'),
        generalfeedback=(
            r'<p>Normalisation requires \(|a_0|^2+|a_1|^2=1\), i.e. \(\frac{1}{ {@a@} } + b^2 = 1\).</p>'
            r'<p>Hence \(b^2 = 1-\frac{1}{ {@a@} } = \frac{ {@a-1@} }{ {@a@} }\) and, taking the '
            r'positive root, \(b = {@ta@}\).</p>'
            r'<p>Note that the global phase of \(|\psi\rangle\) is unobservable, but the sign of \(b\) '
            r'relative to the \(|0\rangle\) amplitude is not — it is a relative phase. Here positivity '
            r'was imposed by the statement.</p>'),
        questionvariables='a : rand_with_step(3,9,1);\nta : sqrt((a-1)/a);',
        questionnote='a={@a@}, b={@ta@}',
        parts=[dict(input='ans1', prt='prt1', tans='ta', boxsize=15,
                    truefb='<p>Correct — the amplitudes satisfy \\(|a_0|^2+|b|^2=1\\).</p>',
                    falsefb=r'<p>Not correct. Impose \(\left|\frac{1}{\sqrt{a}}\right|^2 + b^2 = 1\) '
                            r'and solve for the positive root.</p>')]),
    stack_question(
        name='C1.S2 — Expectation value of a Pauli observable',
        questiontext=stack_qtext(
            'C1.S2', 'Born rule and expectation values',
            r'<p>Let \(|\psi\rangle=\cos(\theta/2)|0\rangle+\sin(\theta/2)|1\rangle\) with '
            r'\(\theta\in[0,\pi]\).</p>'
            r'<p>(a) Give \(\langle\psi|Z|\psi\rangle\) as a simplified function of \(\theta\) '
            r'(use <code>theta</code> for \(\theta\)).</p>'
            r'<p>\(\langle Z\rangle=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give \(\langle\psi|X|\psi\rangle\) as a simplified function of \(\theta\).</p>'
            r'<p>\(\langle X\rangle=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>Write \(|\psi\rangle=(\cos(\theta/2),\sin(\theta/2))^{T}\).</p>'
            r'<p>\(Z|\psi\rangle=(\cos(\theta/2),-\sin(\theta/2))^{T}\), so '
            r'\(\langle Z\rangle=\cos^{2}(\theta/2)-\sin^{2}(\theta/2)=\cos\theta\).</p>'
            r'<p>\(X|\psi\rangle=(\sin(\theta/2),\cos(\theta/2))^{T}\), so '
            r'\(\langle X\rangle=2\sin(\theta/2)\cos(\theta/2)=\sin\theta\).</p>'
            r'<p>These are precisely the \(z\)- and \(x\)-coordinates of the Bloch vector of '
            r'\(|\psi\rangle\) (Chapter 2), confirming \(\langle X\rangle^2+\langle Y\rangle^2+'
            r'\langle Z\rangle^2=1\) for a pure state.</p>'),
        questionvariables='ta1 : cos(theta);\nta2 : sin(theta);',
        questionnote='<Z>=cos(theta), <X>=sin(theta)',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=18, value='0.5000000',
                 truefb='<p>Correct: \\(\\langle Z\\rangle=\\cos\\theta\\).</p>',
                 falsefb=r'<p>Recall \(\cos^2 u-\sin^2 u=\cos 2u\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=18, value='0.5000000',
                 truefb='<p>Correct: \\(\\langle X\\rangle=\\sin\\theta\\).</p>',
                 falsefb=r'<p>Recall \(2\sin u\cos u=\sin 2u\).</p>')]),
    stack_question(
        name='C1.S3 — Pauli algebra: commutator and rotation',
        questiontext=stack_qtext(
            'C1.S3', 'Pauli algebra',
            r'<p>(a) The Pauli matrices satisfy \([\sigma_a,\sigma_b]=2i\varepsilon_{abc}\sigma_c\). '
            r'Writing \([X,Y]=k\,Z\), give the scalar \(k\) (use <code>i</code> for the imaginary unit).</p>'
            r'<p>\(k=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Using \((\hat n\cdot\vec\sigma)^2=I\), the rotation '
            r'\(e^{-i\theta(\hat n\cdot\vec\sigma)/2}\) equals \(\alpha(\theta) I - i\beta(\theta)(\hat n\cdot\vec\sigma)\). '
            r'Give \(\beta(\theta)\) (use <code>theta</code>).</p>'
            r'<p>\(\beta(\theta)=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>(a) Direct computation: \(XY=iZ\) and \(YX=-iZ\), hence \([X,Y]=2iZ\) and \(k=2i\).</p>'
            r'<p>(b) Split the exponential series. Even powers give \(\sum_k \frac{(-1)^k(\theta/2)^{2k}}{(2k)!}I'
            r'=\cos(\theta/2)I\); odd powers give \(-i\sin(\theta/2)(\hat n\cdot\vec\sigma)\). '
            r'Therefore \(\beta(\theta)=\sin(\theta/2)\).</p>'
            r'<p>This identity is the algebraic content of the isomorphism \(SU(2)/\{\pm I\}\cong SO(3)\): '
            r'a \(2\pi\) rotation returns \(-I\), not \(I\).</p>'),
        questionvariables='ta1 : 2*%i;\nta2 : sin(theta/2);',
        questionnote='k=2i, beta=sin(theta/2)',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=12, value='0.5000000',
                 truefb='<p>Correct: \\([X,Y]=2iZ\\).</p>',
                 falsefb='<p>Compute \\(XY\\) and \\(YX\\) explicitly, then subtract.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=18, value='0.5000000',
                 truefb='<p>Correct: \\(\\beta(\\theta)=\\sin(\\theta/2)\\).</p>',
                 falsefb=r'<p>Split \(e^{-i\theta A/2}=\sum_n\frac{(-i\theta/2)^n}{n!}A^n\) into even '
                         r'and odd \(n\), using \(A^2=I\).</p>')]),
]

CHAPTER = dict(
    no=1, slug='mathematical-foundations',
    title='Mathematical Foundations of Quantum Computation',
    subtitle='Hilbert spaces, Dirac notation, spectral theory, tensor products and the Pauli algebra — '
             'the algebraic toolkit assumed by every later chapter.',
    prereq='Linear algebra over \\(\\mathbb C\\) (eigenvalues, inner products, matrix exponentials), '
           'elementary probability, and working Python/NumPy.',
    objectives=[
        'Manipulate states and operators fluently in Dirac notation and translate to matrices.',
        'State and apply the spectral theorem to define functions of operators, notably \\(e^{-iHt}\\).',
        'Construct multi-qubit operators via Kronecker products with correct factor ordering.',
        'Expand any operator in the Pauli basis and use the anticommutation relations.',
        'Bound error accumulation across a circuit using unitary invariance of the operator norm.',
        'Implement all of the above in NumPy with numerically sound tolerance-based tests.',
    ],
    sections=[
        ('Hilbert spaces and Dirac notation', S1),
        ('Operators: Hermitian, unitary, projective, positive', S2),
        ('Composite systems and the tensor product', S3),
        ('The Pauli algebra', S4),
        ('Norms, distances and error accumulation', S5),
        ('The postulates, stated for pure states', S6),
    ],
    summary="Quantum computation takes place in \\((\\mathbb C^{2})^{\\otimes n}\\). States are unit "
            "vectors up to global phase, evolution is unitary and generated by a Hermitian "
            "Hamiltonian via the spectral theorem, composition is tensorial, and measurement "
            "follows the Born rule. The Pauli strings give an orthogonal operator basis whose "
            "algebra will reappear as the stabilizer formalism and as the Hamiltonian encoding of "
            "variational algorithms.",
    references=REFS, coderunner=CR, stack=ST,
)
