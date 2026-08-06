# -*- coding: utf-8 -*-
"""Chapter 4 — Entanglement, Non-locality and Communication Protocols."""
from math import sin, cos, pi, sqrt, log2
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, circuit_svg,
                    flow_svg, interactive, C, SERIF, MONO)

S1 = (
    p("Entanglement is the statement that a joint pure state need not be a product of local "
      "pure states. The complete structural result for bipartite pure states is the Schmidt "
      "decomposition — nothing more than the singular value decomposition, written in Dirac "
      "notation.")
    + box('thm', 'Schmidt decomposition',
          "Every \\(|\\psi\\rangle\\in\\mathcal H_A\\otimes\\mathcal H_B\\) can be written "
          "\\(|\\psi\\rangle=\\sum_{k=1}^{r}\\lambda_k|a_k\\rangle\\otimes|b_k\\rangle\\) with "
          "\\(\\lambda_k>0\\), \\(\\sum_k\\lambda_k^{2}=1\\), and \\(\\{|a_k\\rangle\\}\\), "
          "\\(\\{|b_k\\rangle\\}\\) orthonormal sets in \\(\\mathcal H_A\\), \\(\\mathcal H_B\\). "
          "The number \\(r\\le\\min(\\dim\\mathcal H_A,\\dim\\mathcal H_B)\\) is the "
          "<em>Schmidt rank</em>, and \\(|\\psi\\rangle\\) is a product state iff \\(r=1\\).")
    + box('proof', '',
          "Write \\(|\\psi\\rangle=\\sum_{ij}C_{ij}|i\\rangle|j\\rangle\\) and take the SVD "
          "\\(C=U\\Sigma V^{\\dagger}\\). Then "
          "\\(|\\psi\\rangle=\\sum_k\\sigma_k\\big(\\sum_i U_{ik}|i\\rangle\\big)\\otimes"
          "\\big(\\sum_j \\overline{V_{jk}}\\,|j\\rangle\\big)\\), and orthonormality of the two "
          "families follows from the isometry of \\(U\\) and \\(V\\). \\(\\blacksquare\\)")
    + p("Two immediate corollaries. The reduced states "
        "\\(\\rho_A=\\operatorname{tr}_B|\\psi\\rangle\\langle\\psi|=\\sum_k\\lambda_k^{2}"
        "|a_k\\rangle\\langle a_k|\\) and \\(\\rho_B\\) have the <em>same</em> non-zero spectrum. "
        "And local unitaries \\(U_A\\otimes U_B\\) leave the Schmidt coefficients invariant, so "
        "any entanglement measure for pure states must be a function of \\(\\{\\lambda_k\\}\\) "
        "alone.")
    + box('def', 'Entropy of entanglement',
          "\\(E(|\\psi\\rangle)=S(\\rho_A)=-\\sum_k\\lambda_k^{2}\\log_2\\lambda_k^{2}\\). It "
          "vanishes iff \\(|\\psi\\rangle\\) is a product, and is maximal "
          "(\\(\\log_2 d\\)) iff all \\(\\lambda_k=1/\\sqrt d\\). It is <em>the</em> unique "
          "asymptotic measure for bipartite pure states: \\(n\\) copies of \\(|\\psi\\rangle\\) can "
          "be reversibly converted into \\(nE\\) Bell pairs by local operations and classical "
          "communication (entanglement concentration/dilution).")
)

S2 = (
    p("The four maximally entangled two-qubit states form the <strong>Bell basis</strong>:")
    + eq(r"|\Phi^{\pm}\rangle=\tfrac{1}{\sqrt2}(|00\rangle\pm|11\rangle),\qquad "
         r"|\Psi^{\pm}\rangle=\tfrac{1}{\sqrt2}(|01\rangle\pm|10\rangle)")
    + p("They are related by local Paulis on the second qubit: "
        "\\(|\\Psi^{+}\\rangle=(I\\otimes X)|\\Phi^{+}\\rangle\\), "
        "\\(|\\Phi^{-}\\rangle=(I\\otimes Z)|\\Phi^{+}\\rangle\\), "
        "\\(|\\Psi^{-}\\rangle=(I\\otimes XZ)|\\Phi^{+}\\rangle\\) up to phase. The circuit "
        "\\(\\mathrm{CNOT}_{01}(H\\otimes I)\\) maps the computational basis to the Bell basis; "
        "its inverse performs a Bell measurement.")
    + box('note', 'Local indistinguishability',
          "Each Bell state has maximally mixed reduced states, \\(\\rho_A=\\rho_B=I/2\\). "
          "Alice alone therefore cannot tell which Bell state she shares with Bob, nor whether "
          "Bob has acted — this is exactly why entanglement cannot be used to signal, and why "
          "superdense coding needs the physical transmission of a qubit.")
)

S3 = (
    p("Bell's theorem is the sharpest statement that quantum correlations exceed anything "
      "reproducible by shared classical randomness. We use the CHSH form.")
    + p("Alice chooses a setting \\(x\\in\\{0,1\\}\\) and outputs \\(a\\in\\{\\pm1\\}\\); Bob chooses "
        "\\(y\\in\\{0,1\\}\\) and outputs \\(b\\in\\{\\pm1\\}\\). Define "
        "\\(S=\\langle A_0B_0\\rangle+\\langle A_0B_1\\rangle+\\langle A_1B_0\\rangle-\\langle A_1B_1\\rangle\\).")
    + box('thm', 'CHSH inequality and Tsirelson bound',
          "Any <em>local hidden variable</em> model satisfies \\(|S|\\le2\\). Quantum mechanics "
          "allows \\(|S|\\le2\\sqrt2\\) (Tsirelson), attained on \\(|\\Phi^{+}\\rangle\\) with "
          "\\(A_0=Z\\), \\(A_1=X\\), \\(B_0=(Z+X)/\\sqrt2\\), \\(B_1=(Z-X)/\\sqrt2\\). "
          "No-signalling alone would permit \\(|S|=4\\) (Popescu–Rohrlich boxes), so quantum "
          "theory sits strictly between locality and the no-signalling limit.")
    + box('proof', 'Local bound',
          "In a deterministic local model, \\(a\\) depends only on \\(x\\) and a shared variable "
          "\\(\\lambda\\); similarly for \\(b\\). Then "
          "\\(A_0(B_0+B_1)+A_1(B_0-B_1)\\) has one bracket equal to \\(\\pm2\\) and the other to "
          "\\(0\\), so the expression is \\(\\pm2\\) pointwise; averaging over \\(\\lambda\\) "
          "preserves \\(|S|\\le2\\). General (stochastic) local models are convex mixtures of "
          "deterministic ones. \\(\\blacksquare\\)")
    + p("Loophole-free experimental violations were reported in 2015 by three groups (Delft, "
        "NIST, Vienna), closing the detection and locality loopholes simultaneously. Beyond "
        "foundations, CHSH violation is an operational certificate: it underlies "
        "device-independent QKD and certified randomness expansion, where security follows from "
        "the observed correlations without trusting the hardware.")
)

S4 = (
    p("Two protocols show that entanglement is a <em>resource</em> that trades against classical "
      "and quantum communication.")
    + box('thm', 'Superdense coding (Bennett–Wiesner 1992)',
          "One shared Bell pair plus the transmission of one qubit conveys two classical bits. "
          "Alice applies \\(I,X,Z,XZ\\) to her half according to her two bits, sends her qubit, "
          "and Bob performs a Bell measurement on the pair. Resource identity: "
          "1 ebit + 1 qubit \\(\\ge\\) 2 cbits.")
    + box('thm', 'Teleportation (Bennett et al. 1993)',
          "One shared Bell pair plus two classical bits transmits one unknown qubit. Alice "
          "Bell-measures her unknown qubit against her half of the pair, obtaining "
          "\\(k\\in\\{00,01,10,11\\}\\) uniformly at random; Bob applies the corresponding "
          "Pauli correction \\(I,X,Z,ZX\\). Resource identity: 1 ebit + 2 cbits \\(\\ge\\) 1 qubit.")
    + p("Neither protocol violates causality. In teleportation Bob's state before receiving the "
        "classical bits is exactly \\(I/2\\) regardless of \\(|\\psi\\rangle\\) — no information "
        "until the classical channel is used. Nor does teleportation clone: Alice's copy is "
        "destroyed by the Bell measurement, consistent with Chapter 2.")
    + code('''import numpy as np

def teleport(psi, k):
    """Bob's state after Alice's Bell outcome k in {0,1,2,3}, with correction applied."""
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    corr = [I2, X, Z, Z @ X][k]
    pre  = [I2, X, Z, X @ Z][k] @ np.asarray(psi, dtype=complex).reshape(2)
    return corr @ pre        # equals psi up to global phase, for every k''',
           'The algebraic core of teleportation: the correction inverts the Pauli byproduct')
)

S5 = (
    p("For mixed states, entanglement is subtler: separable states are those of the form "
      "\\(\\rho=\\sum_i p_i\\,\\rho_A^{(i)}\\otimes\\rho_B^{(i)}\\), and deciding membership in that "
      "convex set is NP-hard in the dimension (Gurvits 2003).")
    + box('thm', 'Peres–Horodecki (PPT) criterion',
          "If \\(\\rho_{AB}\\) is separable then its partial transpose "
          "\\(\\rho^{T_B}\\) is positive semidefinite. For \\(2\\times2\\) and \\(2\\times3\\) systems "
          "the converse also holds, so PPT is necessary and sufficient there. In higher "
          "dimensions there exist entangled PPT states — <em>bound entanglement</em> — from which "
          "no pure entanglement can be distilled.")
    + p("Two further structural facts matter for the rest of the course. "
        "<strong>Monogamy</strong>: if \\(A\\) is maximally entangled with \\(B\\), it is "
        "uncorrelated with everything else; quantitatively "
        "\\(C_{AB}^{2}+C_{AC}^{2}\\le C_{A(BC)}^{2}\\) (Coffman–Kundu–Wootters). This is the "
        "reason eavesdroppers cannot share in a maximally entangled key, and it constrains the "
        "structure of quantum error-correcting codes. "
        "<strong>Area laws</strong>: ground states of gapped local Hamiltonians have entanglement "
        "entropy scaling with the boundary rather than the volume of a region, which is why "
        "tensor-network methods can classically simulate many physically relevant states — and "
        "why quantum advantage claims must avoid them.")
)

S6 = (
    p("A practical note on computing entanglement numerically. Given a bipartite state vector "
      "of dimension \\(d_Ad_B\\), reshape to a \\(d_A\\times d_B\\) matrix and take singular "
      "values: those are the Schmidt coefficients. Never form the reduced density matrix and "
      "diagonalise it unless you need \\(\\rho_A\\) itself — the SVD is more accurate and "
      "cheaper.")
    + code('''import numpy as np

def schmidt(psi, dA, dB):
    C = np.asarray(psi, dtype=complex).reshape(dA, dB)
    return np.linalg.svd(C, compute_uv=False)

def entanglement_entropy(psi, dA, dB):
    s = schmidt(psi, dA, dB) ** 2
    s = s[s > 1e-15]
    return float(-np.sum(s * np.log2(s)))

bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
print(round(entanglement_entropy(bell, 2, 2), 6))   # 1.0 ebit''',
           'Schmidt spectrum and entropy of entanglement via SVD')
)

# =============================== figures, citations and added commentary =====
def _h2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * log2(x) - (1 - x) * log2(1 - x)


_th4 = [k * pi / 360 for k in range(0, 181)]          # 0 .. pi/2
ENTROPY = line_chart(
    [dict(label='entropy of entanglement  E = h(cos²θ)', xs=[t * 180 / pi for t in _th4],
          ys=[_h2(cos(t) ** 2) for t in _th4], color='#026573'),
     dict(label='larger Schmidt coefficient  cos²θ', xs=[t * 180 / pi for t in _th4],
          ys=[cos(t) ** 2 for t in _th4], color='#c9a227', dash='6 4'),
     dict(label='smaller Schmidt coefficient  sin²θ', xs=[t * 180 / pi for t in _th4],
          ys=[sin(t) ** 2 for t in _th4], color='#9333ea', dash='6 4')],
    xlim=(0, 90), ylim=(0, 1.05), xlabel='θ  (degrees)  in  cos θ|00⟩ + sin θ|11⟩',
    ylabel='ebits  /  probability',
    vlines=[(45, 'Bell state', '#dc2626')], height=330)

_bet = [k * pi / 180 for k in range(0, 181)]
CHSH = line_chart(
    [dict(label='S(β) for the optimal Alice settings', xs=[b * 180 / pi for b in _bet],
          ys=[2 * abs(cos(b)) + 2 * abs(sin(b)) if False else
              (cos(b) + cos(b) + sin(b) - (-sin(b))) for b in _bet], color='#026573')],
    xlim=(0, 180), ylim=(-3, 3), xlabel='Bob’s setting angle β  (degrees)',
    ylabel='CHSH value  S',
    hlines=[(2, 'local bound  |S| ≤ 2', '#dc2626'),
            (2 * sqrt(2), 'Tsirelson bound  2√2', '#9333ea'),
            (-2, '', '#dc2626')],
    vlines=[(45, 'optimum', '#c9a227')], height=340)

BELL_PREP = circuit_svg(
    2,
    [[('g', 0, 'H')], [('c', 0, 1, 'X')]],
    wire_labels=['|x⟩', '|y⟩'], width=470,
    title='Bell-state preparation: |xy⟩ ↦ one of the four Bell states')

BELL_MEAS = circuit_svg(
    2,
    [[('c', 0, 1, 'X')], [('g', 0, 'H')], [('m', 0), ('m', 1)]],
    wire_labels=['', ''], width=470,
    title='Bell measurement: the same circuit reversed, then read out')

TELEPORT = circuit_svg(
    3,
    [[('lab', 1, 'shared Bell pair')],
     [('g', 1, 'H')],
     [('c', 1, 2, 'X')],
     [('c', 0, 1, 'X')],
     [('g', 0, 'H')],
     [('m', 0), ('m', 1)],
     [('c', 1, 2, 'X')],
     [('c', 0, 2, 'Z')]],
    wire_labels=['|ψ⟩  (Alice)', '|0⟩  (Alice)', '|0⟩  (Bob)'], width=680,
    title='Teleportation: Bell pair, Bell measurement, two classical bits, Pauli correction')

DENSE = flow_svg(
    [(30, 60, 150, 64, 'Alice|two classical bits b₁b₂', '#ecfeff', '#026573'),
     (215, 60, 150, 64, 'apply I, X, Z or XZ|to her half of the pair', '#fefce8', '#c9a227'),
     (400, 60, 120, 64, 'send|1 qubit', '#f5f3ff', '#9333ea'),
     (550, 60, 110, 64, 'Bob|Bell measure', '#ecfeff', '#026573'),
     (215, 168, 305, 46, 'pre-shared entanglement: 1 ebit, distributed in advance',
      '#f8fafc', '#475569')],
    [(180, 92, 213, 92, ''), (365, 92, 398, 92, ''), (520, 92, 548, 92, ''),
     (290, 166, 290, 126, ''), (445, 166, 445, 126, '')],
    height=240, title='Superdense coding: 1 ebit + 1 qubit ≥ 2 classical bits')

JS_CHSH = """
  var b = JXG.JSXGraph.initBoard('ch4chsh', {boundingbox: [-20, 3.4, 200, -3.4],
      axis: true, showCopyright: false, showNavigation: false});
  var a0 = b.create('slider', [[10, 3.0], [90, 3.0], [0, 0, 180]],
      {name: 'A&#8320;', snapWidth: 1, strokeColor: '#026573'});
  var a1 = b.create('slider', [[10, 2.6], [90, 2.6], [0, 90, 180]],
      {name: 'A&#8321;', snapWidth: 1, strokeColor: '#c9a227'});
  var d = Math.PI / 180;
  function S(beta) {
      var A0 = a0.Value() * d, A1 = a1.Value() * d, B0 = beta * d, B1 = (beta + 90) * d;
      return Math.cos(A0 - B0) + Math.cos(A0 - B1) + Math.cos(A1 - B0) - Math.cos(A1 - B1);
  }
  b.create('functiongraph', [S, 0, 180], {strokeColor: '#026573', strokeWidth: 2.6});
  b.create('line', [[0, 2], [180, 2]], {strokeColor: '#dc2626', dash: 2,
      straightFirst: false, straightLast: false});
  b.create('line', [[0, -2], [180, -2]], {strokeColor: '#dc2626', dash: 2,
      straightFirst: false, straightLast: false});
  b.create('line', [[0, 2 * Math.sqrt(2)], [180, 2 * Math.sqrt(2)]],
      {strokeColor: '#9333ea', dash: 1, straightFirst: false, straightLast: false});
  b.create('text', [120, 2.12, 'local bound 2'], {fontSize: 12, strokeColor: '#dc2626'});
  b.create('text', [120, 2.95, 'Tsirelson 2&#8730;2'], {fontSize: 12, strokeColor: '#9333ea'});
  b.create('text', [100, 3.0, function () {
      var best = 0;
      for (var x = 0; x <= 180; x += 0.5) { if (Math.abs(S(x)) > Math.abs(best)) { best = S(x); } }
      return 'max |S| over &#946; = ' + Math.abs(best).toFixed(3);
  }], {fontSize: 14, strokeColor: '#0f172a'});
  b.create('text', [80, -3.1, 'Bob&#8217;s setting &#946; (degrees)'],
      {fontSize: 13, strokeColor: '#475569'});
"""

S1 = S1 + figure(
    '4.1',
    'Entanglement of the one-parameter family cos θ|00⟩ + sin θ|11⟩. The two Schmidt coefficients are '
    'cos²θ and sin²θ; the entropy of entanglement is their binary entropy. It vanishes at θ = 0 and '
    'θ = 90°, where the state is a product, and reaches exactly one ebit at θ = 45°, the Bell state. '
    'Note that the entropy is flat near its maximum: a state can be far from maximally entangled in '
    'amplitude and still carry almost a full ebit.',
    ENTROPY, height=330) + p(
    "The operational meaning of the vertical axis is worth spelling out, because it is what "
    "justifies calling \\(E\\) <em>the</em> measure rather than one of many. Bennett, Bernstein, "
    "Popescu and Schumacher showed that \\(n\\) copies of \\(|\\psi\\rangle\\) can be converted by "
    "local operations and classical communication into \\(nE(|\\psi\\rangle)-o(n)\\) Bell pairs, and "
    "back again, with fidelity approaching one" + cite('7') + ". Entanglement of pure bipartite "
    "states is therefore a fungible currency with a well-defined exchange rate, and the rate is the "
    "entropy of the marginal. For mixed states the picture fragments: distillable entanglement and "
    "entanglement cost differ, and bound entangled states have the second strictly positive while "
    "the first is zero.") + sources(
    'Schmidt decomposition and entropy of entanglement: Nielsen &amp; Chuang §2.5, §12.5'
    + cite('1') + '; the reversibility theorem and the mixed-state complications: Horodecki et al.'
    + cite('7') + '.')

S2 = S2 + figure(
    '4.2',
    'Preparation and measurement in the Bell basis are the same circuit run in opposite directions. '
    'Left: a Hadamard followed by a CNOT maps the computational basis state |xy⟩ to the Bell state '
    'indexed by (x, y). Right: the adjoint circuit maps the Bell basis back to the computational '
    'basis, so a computational-basis readout after it constitutes a Bell measurement — the only way '
    'to implement one, since the Bell states are entangled and cannot be distinguished by any local '
    'measurement.',
    BELL_PREP, width=470, height=142) + figure(
    '4.3', 'The inverse circuit, which realises a Bell measurement.',
    BELL_MEAS, width=470, height=142) + p(
    "A subtlety with consequences for Chapter 9: this Bell measurement is <em>complete</em>, "
    "distinguishing all four states, only because it uses an entangling gate. With linear optics "
    "and no ancillas, unentangled photon detection can distinguish at most two of the four Bell "
    "states, which caps the success probability of optical teleportation at 50% — a practical "
    "limitation that shapes photonic architectures for quantum repeaters" + cite('5') + "."
) + sources(
    'Bell basis and its circuit: Nielsen &amp; Chuang §1.3.6' + cite('1') + '.')

S3 = S3 + figure(
    '4.4',
    'The CHSH value as Bob rotates his measurement axis, with Alice fixed at the optimal settings '
    'Z and X. Any local hidden-variable model is confined between the red lines at ±2; quantum '
    'mechanics on the Bell state reaches ±2√2 at β = 45°, and no quantum state or measurement can '
    'exceed the purple Tsirelson line. The gap between the red and purple lines is exactly what a '
    'loophole-free experiment certifies.',
    CHSH, height=340) + interactive(
    '4.5', 'ch4chsh',
    'Drag Alice’s two measurement angles and watch the whole CHSH curve deform. The maximum of |S| '
    'over Bob’s setting is printed above the plot. Two facts are worth discovering by hand: the '
    'value never exceeds 2√2 ≈ 2.828 whatever the settings, and it drops to the classical bound of '
    '2 whenever Alice’s two observables commute (A₀ and A₁ parallel or antiparallel) — non-locality '
    'requires incompatible local measurements on both sides.',
    JS_CHSH, aspect='16/9', max_width=640,
    hint='drag the two sliders to change Alice’s measurement axes.') + p(
    "What a violation certifies deserves precision, since it is routinely overstated. CHSH does "
    "not show that information travels faster than light — the marginal statistics on each side are "
    "unchanged by the other party's choice, so no signalling is possible. What it rules out is the "
    "conjunction of three assumptions: that measurement outcomes are determined by local variables "
    "carried by the particles, that the settings are chosen freely, and that the choice on one side "
    "does not influence the outcome on the other" + cite('1,2') + ". The 2015 loophole-free "
    "experiments closed the detection and locality loopholes simultaneously" + cite('6') + ", "
    "leaving only the superdeterminism and freedom-of-choice escapes, which are untestable in "
    "principle. Operationally, the violation is a certificate: device-independent key distribution "
    "and certified randomness derive their security from the observed value of \\(S\\) alone, "
    "without any assumption about the internal workings of the devices" + cite('8') + "."
) + sources(
    'Bell’s theorem' + cite('2') + '; the CHSH form' + cite('3') + '; the quantum bound'
    + cite('4') + '; loophole-free tests' + cite('6') + '; device-independent applications'
    + cite('8') + '.')

S4 = S4 + figure(
    '4.6',
    'Teleportation as a circuit. Alice entangles the unknown state with her half of the pair, '
    'measures both qubits, and sends the two classical bits; the final controlled-Z and controlled-X '
    'are the Pauli correction Bob applies conditioned on those bits. Bob’s qubit is exactly I/2 '
    'until the classical message arrives, which is why the protocol does not signal.',
    TELEPORT, width=680, height=236) + figure(
    '4.7',
    'Superdense coding as a resource flow. The entanglement is distributed in advance, at a time '
    'when Alice does not yet know her message; only one qubit travels afterwards, yet two classical '
    'bits arrive. The Holevo bound (Chapter 5) caps unassisted transmission at one bit per qubit, '
    'and the pre-shared ebit is exactly what pays for the second bit.',
    DENSE, height=240) + p(
    "The two protocols are formally dual, and the duality is worth making explicit: teleportation "
    "consumes an ebit and two classical bits to transmit one qubit; superdense coding consumes an "
    "ebit and one qubit to transmit two classical bits. Composing them returns the identity, so "
    "neither can be improved without violating the other" + cite('4,5') + ". This kind of "
    "resource-inequality bookkeeping was later systematised into a whole calculus of quantum "
    "Shannon theory, in which teleportation and dense coding play the role of the two elementary "
    "reactions from which most protocols are assembled.") + sources(
    'Superdense coding: Bennett &amp; Wiesner' + cite('4') + '; teleportation: Bennett et al.'
    + cite('5') + '; the resource calculus: Horodecki et al. §XII' + cite('7') + '.')

S5 = S5 + sources(
    'Separability, PPT and bound entanglement: Horodecki et al. §III–VI' + cite('7') + '; '
    'monogamy and area laws are surveyed there and in Preskill\'s notes.')

REFS = [
    dict(authors="J. S. Bell", title="On the Einstein Podolsky Rosen paradox",
         venue="Physics Physique Fizika 1(3), 195–200", year="1964",
         link="https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195",
         note="The original theorem. Short and still the clearest statement of the assumptions."),
    dict(authors="J. F. Clauser, M. A. Horne, A. Shimony and R. A. Holt",
         title="Proposed experiment to test local hidden-variable theories",
         venue="Physical Review Letters 23, 880", year="1969",
         note="The CHSH form used in §3 and in the exercises."),
    dict(authors="B. S. Cirel'son (Tsirelson)", title="Quantum generalizations of Bell's inequality",
         venue="Letters in Mathematical Physics 4, 93–100", year="1980",
         note="Proof of the 2√2 quantum bound."),
    dict(authors="C. H. Bennett and S. J. Wiesner",
         title="Communication via one- and two-particle operators on Einstein–Podolsky–Rosen states",
         venue="Physical Review Letters 69, 2881", year="1992",
         note="Superdense coding."),
    dict(authors="C. H. Bennett, G. Brassard, C. Crépeau, R. Jozsa, A. Peres and W. K. Wootters",
         title="Teleporting an unknown quantum state via dual classical and EPR channels",
         venue="Physical Review Letters 70, 1895", year="1993",
         note="Teleportation; the protocol in §4."),
    dict(authors="B. Hensen et al.",
         title="Loophole-free Bell inequality violation using electron spins separated by 1.3 kilometres",
         venue="Nature 526, 682–686", year="2015",
         link="https://arxiv.org/abs/1508.05949",
         note="The Delft experiment; see also Giustina et al. and Shalm et al., PRL 115 (2015)."),
    dict(authors="R. Horodecki, P. Horodecki, M. Horodecki and K. Horodecki",
         title="Quantum entanglement", venue="Reviews of Modern Physics 81, 865", year="2009",
         link="https://arxiv.org/abs/quant-ph/0702225",
         note="The standard survey: separability criteria, measures, bound entanglement."),
    dict(authors="N. Brunner, D. Cavalcanti, S. Pironio, V. Scarani and S. Wehner",
         title="Bell nonlocality", venue="Reviews of Modern Physics 86, 419", year="2014",
         link="https://arxiv.org/abs/1303.2849",
         note="Device-independent protocols built on CHSH violation."),
]

CR = [
    dict(
        name='C4.Q1 — Schmidt decomposition and entropy of entanglement',
        qtext=cr_qtext('C4.Q1', 'Quantifying bipartite entanglement',
                       "The Schmidt coefficients of a bipartite pure state are the singular "
                       "values of its coefficient matrix; the entropy of entanglement is the "
                       "Shannon entropy of their squares.",
                       "Write <code>schmidt(psi, dA, dB)</code> returning the singular values in "
                       "descending order (as a NumPy array), <code>schmidt_rank(psi, dA, dB, "
                       "tol=1e-10)</code> returning an <code>int</code>, and "
                       "<code>entanglement_entropy(psi, dA, dB)</code> returning a "
                       "<code>float</code> in bits, rounded to 6 decimals.",
                       "Bell state    -> rank 2, entropy 1.0\n"
                       "|00>          -> rank 1, entropy 0.0"),
        answer='''import numpy as np

def schmidt(psi, dA, dB):
    C = np.asarray(psi, dtype=complex).reshape(dA, dB)
    s = np.linalg.svd(C, compute_uv=False)
    return np.sort(s)[::-1]

def schmidt_rank(psi, dA, dB, tol=1e-10):
    return int(np.sum(schmidt(psi, dA, dB) > tol))

def entanglement_entropy(psi, dA, dB):
    s = schmidt(psi, dA, dB) ** 2
    s = s[s > 1e-15]
    return round(float(abs(-np.sum(s * np.log2(s)))), 6)
''',
        preload='''import numpy as np

def schmidt(psi, dA, dB):
    # reshape to dA x dB and take singular values
    ...

def schmidt_rank(psi, dA, dB, tol=1e-10):
    ...

def entanglement_entropy(psi, dA, dB):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nbell = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)\n'
                     'print(schmidt_rank(bell,2,2), entanglement_entropy(bell,2,2))\n',
             'expected': '2 1.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprod = np.array([1,0,0,0], dtype=complex)\n'
                     'print(schmidt_rank(prod,2,2), entanglement_entropy(prod,2,2))\n',
             'expected': '1 0.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nth = np.pi/6\n'
                     'psi = np.array([np.cos(th),0,0,np.sin(th)], dtype=complex)\n'
                     'c2, s2 = np.cos(th)**2, np.sin(th)**2\n'
                     'ref = round(float(-c2*np.log2(c2)-s2*np.log2(s2)), 6)\n'
                     'print(entanglement_entropy(psi,2,2) == ref)\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nghz = np.zeros(8, dtype=complex); ghz[0]=1/np.sqrt(2); ghz[7]=1/np.sqrt(2)\n'
                     'print(schmidt_rank(ghz,2,4), entanglement_entropy(ghz,2,4))\n',
             'expected': '2 1.0\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nw = np.zeros(8, dtype=complex)\n'
                     'w[1]=w[2]=w[4]=1/np.sqrt(3)\n'
                     'print(schmidt_rank(w,2,4), entanglement_entropy(w,2,4))\n',
             'expected': '2 0.918296\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C4.Q2 — Bell basis and Bell measurement',
        qtext=cr_qtext('C4.Q2', 'The entangling circuit and its inverse',
                       "\\(\\mathrm{CNOT}_{01}(H\\otimes I)\\) maps \\(|xy\\rangle\\) to the Bell "
                       "state indexed by \\((x,y)\\); its adjoint implements a Bell measurement "
                       "in the computational basis.",
                       "Write <code>bell_state(x, y)</code> returning the 4-vector "
                       "\\(\\mathrm{CNOT}(H\\otimes I)|xy\\rangle\\), and "
                       "<code>bell_probs(psi)</code> returning the array of four probabilities "
                       "of the Bell outcomes \\(\\Phi^{+},\\Phi^{-},\\Psi^{+},\\Psi^{-}\\) "
                       "in the order produced by <code>bell_state(0,0), (1,0), (0,1), (1,1)</code>, "
                       "rounded to 8 decimals.",
                       "bell_state(0,0) -> (|00> + |11>)/sqrt(2)\n"
                       "bell_probs(bell_state(1,1)) -> [0, 0, 0, 1]"),
        answer='''import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

def bell_state(x, y):
    v = np.zeros(4, dtype=complex)
    v[2 * x + y] = 1
    return CNOT @ np.kron(H, np.eye(2, dtype=complex)) @ v

ORDER = [(0, 0), (1, 0), (0, 1), (1, 1)]

def bell_probs(psi):
    psi = np.asarray(psi, dtype=complex).ravel()
    psi = psi / np.linalg.norm(psi)
    return np.round([abs(np.vdot(bell_state(x, y), psi)) ** 2 for x, y in ORDER], 8)
''',
        preload='''import numpy as np

def bell_state(x, y):
    ...

def bell_probs(psi):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nprint(np.round(bell_state(0,0).real, 6).tolist())\n',
             'expected': '[0.707107, 0.0, 0.0, 0.707107]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(bell_probs(bell_state(1,1)).tolist())\n',
             'expected': '[0.0, 0.0, 0.0, 1.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(bell_probs(np.array([1,0,0,0], dtype=complex)).tolist())\n',
             'expected': '[0.5, 0.5, 0.0, 0.0]\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nB = np.column_stack([bell_state(x,y) for x,y in [(0,0),(1,0),(0,1),(1,1)]])\n'
                     'print(np.allclose(B.conj().T @ B, np.eye(4)))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nX = np.array([[0,1],[1,0]], dtype=complex)\n'
                     'v = np.kron(np.eye(2, dtype=complex), X) @ bell_state(0,0)\n'
                     'print(bell_probs(v).tolist())\n',
             'expected': '[0.0, 0.0, 1.0, 0.0]\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C4.Q3 — Teleportation, end to end',
        qtext=cr_qtext('C4.Q3', 'One ebit + two cbits = one qubit',
                       "Alice holds an unknown \\(|\\psi\\rangle\\) and half of "
                       "\\(|\\Phi^{+}\\rangle\\). She Bell-measures her two qubits, sends the two "
                       "classical bits, and Bob corrects.",
                       "Write <code>teleport(psi, outcome)</code> returning Bob's corrected state "
                       "for a Bell outcome in <code>{0,1,2,3}</code> (order "
                       "\\(\\Phi^{+},\\Phi^{-},\\Psi^{+},\\Psi^{-}\\)), and "
                       "<code>fidelity(a, b)</code> returning "
                       "\\(|\\langle a|b\\rangle|^{2}\\) rounded to 6 decimals. Correct output: "
                       "fidelity 1.0 for every outcome, for every input state.",
                       "corrections: Phi+ -> I,  Phi- -> Z,  Psi+ -> X,  Psi- -> XZ"),
        answer='''import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# byproduct operator applied to Bob's qubit, per Bell outcome
BYPRODUCT = [I2, Z, X, X @ Z]
CORRECTION = [I2, Z, X, Z @ X]

def teleport(psi, outcome):
    psi = np.asarray(psi, dtype=complex).reshape(2)
    psi = psi / np.linalg.norm(psi)
    bob = BYPRODUCT[outcome] @ psi
    return CORRECTION[outcome] @ bob

def fidelity(a, b):
    a = np.asarray(a, dtype=complex).ravel(); a = a / np.linalg.norm(a)
    b = np.asarray(b, dtype=complex).ravel(); b = b / np.linalg.norm(b)
    return round(float(abs(np.vdot(a, b)) ** 2), 6)
''',
        preload='''import numpy as np

def teleport(psi, outcome):
    # apply the byproduct Pauli, then the correction
    ...

def fidelity(a, b):
    ...
''',
        tests=[
            {'code': 'import numpy as np\npsi = np.array([0.6, 0.8], dtype=complex)\n'
                     'print([fidelity(teleport(psi, k), psi) for k in range(4)])\n',
             'expected': '[1.0, 1.0, 1.0, 1.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\npsi = np.array([1, 1j], dtype=complex)/np.sqrt(2)\n'
                     'print(fidelity(teleport(psi, 2), psi))\n',
             'expected': '1.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(fidelity([1,0],[0,1]), fidelity([1,0],[1,0]))\n',
             'expected': '0.0 1.0\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nrng = np.random.default_rng(17)\nok = True\n'
                     'for _ in range(30):\n'
                     '    v = rng.normal(size=2) + 1j*rng.normal(size=2)\n'
                     '    ok = ok and all(fidelity(teleport(v,k), v) == 1.0 for k in range(4))\n'
                     'print(ok)\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\npsi = np.array([1, 1], dtype=complex)/np.sqrt(2)\n'
                     'print(fidelity(np.array([[0,1],[1,0]], dtype=complex) @ psi, psi))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C4.Q4 — CHSH: computing S and hitting the Tsirelson bound',
        qtext=cr_qtext('C4.Q4', 'Certifying non-locality numerically',
                       "For observables \\(A_x,B_y\\) with \\(\\pm1\\) spectrum, "
                       "\\(S=\\langle A_0B_0\\rangle+\\langle A_0B_1\\rangle+\\langle A_1B_0\\rangle"
                       "-\\langle A_1B_1\\rangle\\). Locality forces \\(|S|\\le2\\); quantum "
                       "mechanics reaches \\(2\\sqrt2\\).",
                       "Write <code>correlator(psi, A, B)</code> returning "
                       "\\(\\langle\\psi|A\\otimes B|\\psi\\rangle\\) as a float rounded to 6 "
                       "decimals, and <code>chsh(psi, A0, A1, B0, B1)</code> returning \\(S\\) "
                       "rounded to 6 decimals. Do <em>not</em> round the intermediate correlators "
                       "inside <code>chsh</code> — round only the final sum.",
                       "Phi+, A0=Z, A1=X, B0=(Z+X)/sqrt2, B1=(Z-X)/sqrt2  ->  S = 2.828427"),
        answer='''import numpy as np

def _corr(psi, A, B):
    psi = np.asarray(psi, dtype=complex).ravel()
    psi = psi / np.linalg.norm(psi)
    M = np.kron(np.asarray(A, dtype=complex), np.asarray(B, dtype=complex))
    return float(np.real(np.vdot(psi, M @ psi)))

def correlator(psi, A, B):
    return round(_corr(psi, A, B), 6)

def chsh(psi, A0, A1, B0, B1):
    s = (_corr(psi, A0, B0) + _corr(psi, A0, B1)
         + _corr(psi, A1, B0) - _corr(psi, A1, B1))
    return round(float(s), 6)
''',
        preload='''import numpy as np

def correlator(psi, A, B):
    ...

def chsh(psi, A0, A1, B0, B1):
    ...
''',
        tests=[
            {'code': '''import numpy as np
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
phi = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)
B0 = (Z + X)/np.sqrt(2); B1 = (Z - X)/np.sqrt(2)
print(chsh(phi, Z, X, B0, B1))
''',
             'expected': '2.828427\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
phi = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)
print(correlator(phi, Z, Z), correlator(phi, X, X))
''',
             'expected': '1.0 1.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
prod = np.array([1,0,0,0], dtype=complex)
B0 = (Z + X)/np.sqrt(2); B1 = (Z - X)/np.sqrt(2)
print(chsh(prod, Z, X, B0, B1))
''',
             'expected': '1.414214\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
psi = np.array([0,1,-1,0], dtype=complex)/np.sqrt(2)   # singlet
B0 = (Z + X)/np.sqrt(2); B1 = (Z - X)/np.sqrt(2)
print(round(abs(chsh(psi, Z, X, B0, B1)), 6))
''',
             'expected': '2.828427\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': '''import numpy as np
Z = np.array([[1,0],[0,-1]], dtype=complex)
I = np.eye(2, dtype=complex)
phi = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)
print(correlator(phi, Z, I), correlator(phi, I, Z))
''',
             'expected': '0.0 0.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

ST = [
    stack_question(
        name='C4.S1 — Entropy of entanglement of a two-parameter state',
        questiontext=stack_qtext(
            'C4.S1', 'Schmidt coefficients and entropy',
            r'<p>Let \(|\psi\rangle=\cos\theta\,|00\rangle+\sin\theta\,|11\rangle\) with '
            r'\(\theta\in(0,\pi/2)\).</p>'
            r'<p>(a) Give the larger eigenvalue of the reduced state \(\rho_A\) '
            r'(assume \(\theta\in(0,\pi/4)\)).</p>'
            r'<p>\(\lambda_{\max}=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the entropy of entanglement in bits, as a function of <code>theta</code>. '
            r'Use <code>log(x)/log(2)</code> for \(\log_2 x\).</p>'
            r'<p>\(E=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>The state is already in Schmidt form with \(\lambda_1=\cos\theta\), '
            r'\(\lambda_2=\sin\theta\), so \(\rho_A=\mathrm{diag}(\cos^2\theta,\sin^2\theta)\).</p>'
            r'<p>(a) For \(\theta\in(0,\pi/4)\), \(\cos^2\theta>\sin^2\theta\), so '
            r'\(\lambda_{\max}=\cos^2\theta\).</p>'
            r'<p>(b) \(E=-\cos^2\theta\log_2\cos^2\theta-\sin^2\theta\log_2\sin^2\theta\).</p>'
            r'<p>Check the limits: \(\theta\to0\) gives a product state and \(E\to0\); '
            r'\(\theta=\pi/4\) gives the Bell state and \(E=1\) ebit. Since local unitaries cannot '
            r'change the Schmidt coefficients, \(E\) is invariant under \(U_A\otimes U_B\), as any '
            r'entanglement measure must be.</p>'),
        questionvariables=('ta1 : cos(theta)^2;\n'
                           'ta2 : -cos(theta)^2*log(cos(theta)^2)/log(2)'
                           ' - sin(theta)^2*log(sin(theta)^2)/log(2);'),
        questionnote='lambda=cos^2(theta), E=binary entropy',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=18, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Trace out \(B\): \(\rho_A=\mathrm{diag}(\cos^2\theta,\sin^2\theta)\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=45, value='0.5000000',
                 truefb=r'<p>Correct — this is the binary entropy \(h(\cos^2\theta)\).</p>',
                 falsefb=r'<p>\(E=-\sum_k\lambda_k^2\log_2\lambda_k^2\) over the two Schmidt values.</p>')]),
    stack_question(
        name='C4.S2 — CHSH: local bound, quantum value, Tsirelson',
        questiontext=stack_qtext(
            'C4.S2', 'Bell and Tsirelson bounds',
            r'<p>(a) Give the maximum of \(|S|\) over all local hidden-variable models.</p>'
            r'<p>\(S_{\mathrm{LHV}}=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the exact maximum of \(|S|\) allowed by quantum mechanics '
            r'(the Tsirelson bound), as an exact expression.</p>'
            r'<p>\(S_{Q}=\) [[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) On \(|\Phi^{+}\rangle\) with \(A_0=Z\), \(A_1=X\) and Bob measuring '
            r'\(\cos\beta\,Z+\sin\beta\,X\), the correlator \(\langle A_0 B\rangle\) equals a simple '
            r'function of \(\beta\). Give it.</p>'
            r'<p>\(\langle A_0B\rangle=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) In a deterministic local model \(A_0(B_0+B_1)+A_1(B_0-B_1)=\pm2\) pointwise, '
            r'and general local models are convex mixtures, so \(|S|\le2\).</p>'
            r'<p>(b) Tsirelson: \(|S|\le2\sqrt2\), attained with the settings of §3. '
            r'The gap between \(2\) and \(2\sqrt2\) is the experimentally certified non-locality; '
            r'no-signalling alone would allow \(4\).</p>'
            r'<p>(c) On \(|\Phi^{+}\rangle\), \(\langle Z\otimes Z\rangle=1\) and '
            r'\(\langle Z\otimes X\rangle=0\), so \(\langle A_0B\rangle=\cos\beta\).</p>'),
        questionvariables='ta1 : 2;\nta2 : 2*sqrt(2);\nta3 : cos(beta);',
        questionnote='2, 2sqrt2, cos(beta)',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=8, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Evaluate \(A_0(B_0+B_1)+A_1(B_0-B_1)\) for deterministic \(\pm1\) values.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=12, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>The quantum maximum is \(\sqrt2\) times the local bound.</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=14, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Use \(\langle Z\otimes Z\rangle=1\), \(\langle Z\otimes X\rangle=0\) on \(|\Phi^+\rangle\).</p>')]),
    stack_question(
        name='C4.S3 — Resource identities for teleportation and dense coding',
        questiontext=stack_qtext(
            'C4.S3', 'Counting resources',
            r'<p>(a) Teleporting one qubit consumes one ebit and how many classical bits?</p>'
            r'<p>cbits \(=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Superdense coding transmits how many classical bits per transmitted qubit, '
            r'given one shared ebit?</p>'
            r'<p>cbits \(=\) [[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Alice and Bob share \(n={@n@}\) Bell pairs. Give the maximum number of '
            r'classical bits Alice can convey to Bob by sending \(n\) qubits using dense coding.</p>'
            r'<p>bits \(=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) Two: the Bell measurement has four equally likely outcomes, so Alice must send '
            r'\(\log_2 4=2\) bits. Fewer would allow superluminal signalling, since Bob\'s marginal '
            r'is \(I/2\) until he learns the outcome.</p>'
            r'<p>(b) Two, by the Bennett–Wiesner protocol: the four Bell states are perfectly '
            r'distinguishable and are reached by \(I,X,Z,XZ\) acting on one half.</p>'
            r'<p>(c) \(2n=2\cdot{@n@}={@ta3@}\) bits. This is optimal: the Holevo bound caps the '
            r'accessible information at \(2n\) bits for \(n\) transmitted qubits assisted by '
            r'entanglement.</p>'),
        questionvariables='n : rand_with_step(3,9,1);\nta1 : 2;\nta2 : 2;\nta3 : 2*n;',
        questionnote='n={@n@}, 2n={@ta3@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=6, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>How many equally likely Bell outcomes are there?</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=6, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>How many Bell states can Alice steer to with local Paulis?</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=8, value='0.3333333',
                 truefb='<p>Correct — and this saturates the Holevo bound.</p>',
                 falsefb='<p>Apply the answer to (b) independently to each pair.</p>')]),
]

CHAPTER = dict(
    no=4, slug='entanglement-and-nonlocality',
    title='Entanglement, Non-locality and Communication Protocols',
    subtitle='Schmidt decomposition, entropy of entanglement, Bell/CHSH non-locality and the '
             'Tsirelson bound, teleportation, superdense coding, separability and monogamy.',
    prereq='Chapters 1–3 (tensor products, measurement, circuits).',
    objectives=[
        'Compute the Schmidt decomposition of a bipartite pure state and read off its rank.',
        'Quantify pure-state entanglement with the entropy of entanglement and justify its uniqueness.',
        'Derive the CHSH local bound and the Tsirelson bound, and state what a violation certifies.',
        'Execute and verify teleportation and superdense coding, including the resource identities.',
        'Apply the PPT criterion and explain bound entanglement and monogamy.',
        'Implement all of the above numerically with SVD-based tools.',
    ],
    sections=[
        ('Schmidt decomposition and the entropy of entanglement', S1),
        ('The Bell basis', S2),
        ('Bell non-locality: CHSH and Tsirelson', S3),
        ('Teleportation and superdense coding', S4),
        ('Mixed-state entanglement, separability and monogamy', S5),
        ('Numerical practice', S6),
    ],
    summary="Bipartite pure-state entanglement is completely characterised by the Schmidt "
            "spectrum, and quantified by the entropy of entanglement. CHSH shows these "
            "correlations exceed any local model, capped by Tsirelson's \\(2\\sqrt2\\). "
            "Entanglement is a fungible resource: 1 ebit + 2 cbits teleports a qubit, "
            "1 ebit + 1 qubit sends 2 cbits. For mixed states, separability is NP-hard to decide, "
            "PPT is only sufficient in low dimension, and monogamy constrains how entanglement "
            "can be shared — a fact used again in Chapter 9.",
    references=REFS, coderunner=CR, stack=ST,
)
