# -*- coding: utf-8 -*-
"""Chapter 3 — Quantum Gates, Circuits and Universality."""
from math import log10, log2, log
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, circuit_svg,
                    flow_svg, C, SERIF, MONO)

S1 = (
    p("The circuit model is the standard computational model for quantum computation. A "
      "computation on \\(n\\) qubits is a triple: an initial product state (conventionally "
      "\\(|0\\rangle^{\\otimes n}\\)), a finite sequence of unitaries drawn from a fixed "
      "<em>gate set</em>, each acting on \\(O(1)\\) qubits, and a final computational-basis "
      "measurement. Wires carry qubits, time flows left to right, and the unitary implemented "
      "by a circuit is the product of its gates in reverse reading order.")
    + box('def', 'Circuit complexity',
          "The <em>size</em> of a circuit is its number of gates; its <em>depth</em> is the number "
          "of layers of gates that act on disjoint qubits and can be executed simultaneously. "
          "A family \\(\\{C_n\\}\\) is <em>uniform</em> if a classical Turing machine can output a "
          "description of \\(C_n\\) in time \\(\\mathrm{poly}(n)\\). Efficiency always means "
          "\\(\\mathrm{poly}(n)\\) size for a uniform family — otherwise one could smuggle "
          "uncomputable information into the circuit description.")
    + p("Deferred measurement and the principle of implicit measurement let us assume without "
        "loss of generality that all measurements occur at the end: any intermediate "
        "measurement followed by classically controlled gates can be replaced by a coherent "
        "controlled gate plus a measurement at the end. This is why the model above is fully "
        "general even though real devices measure mid-circuit.")
)

S2 = (
    p("Two single-qubit families cover everything: the rotations "
      "\\(R_x,R_y,R_z\\) of Chapter 2, and the discrete gates below.")
    + table(['Gate', 'Matrix', 'Comment'],
            [['\\(H\\)', r'\(\tfrac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\)',
              r'\(H^2=I\); creates superposition; \(HXH=Z\), \(HZH=X\)'],
             ['\\(S\\)', r'\(\mathrm{diag}(1,i)\)', r'\(=\sqrt Z\); Clifford'],
             ['\\(T\\)', r'\(\mathrm{diag}(1,e^{i\pi/4})\)', r'\(=\sqrt S\); NOT Clifford — the expensive gate'],
             ['\\(R_z(\\lambda)\\)', r'\(\mathrm{diag}(e^{-i\lambda/2},e^{i\lambda/2})\)', 'Virtual (free) on superconducting hardware'],
             ['CNOT', r'\(|0\rangle\langle0|\otimes I+|1\rangle\langle1|\otimes X\)', 'The canonical entangling gate'],
             ['CZ', r'\(\mathrm{diag}(1,1,1,-1)\)', r'Symmetric; \(\mathrm{CNOT}=(I\otimes H)\,\mathrm{CZ}\,(I\otimes H)\)'],
             ['Toffoli \\(CCX\\)', 'permutation on \\(|110\\rangle\\leftrightarrow|111\\rangle\\)',
              'Classically universal; reversible AND']])
    + box('thm', 'ZYZ (Euler) decomposition',
          "For every \\(U\\in U(2)\\) there exist \\(\\alpha,\\beta,\\gamma,\\delta\\in\\mathbb R\\) with "
          "\\(U=e^{i\\alpha}R_z(\\beta)R_y(\\gamma)R_z(\\delta)\\). Consequently three rotation angles "
          "plus a phase parametrise every single-qubit gate, and any hardware providing "
          "\\(R_z\\) and one fixed \\(R_y\\)-type pulse is single-qubit universal.")
    + p("A controlled-\\(U\\) can then be built from CNOTs and single-qubit gates: writing "
        "\\(U=e^{i\\alpha}AXBXC\\) with \\(ABC=I\\) (obtainable from the Euler angles), the circuit "
        "\\(C\\)–CNOT–\\(B\\)–CNOT–\\(A\\) plus a phase gate on the control implements it with "
        "exactly two CNOTs.")
)

S3 = (
    p("Entangling gates cannot be produced by local operations, so at least one two-qubit gate "
      "is indispensable. The good news is that one is enough.")
    + box('thm', 'Exact universality (Barenco et al. 1995; DiVincenzo 1995)',
          "The set \\(\\{\\text{CNOT}\\}\\cup U(2)\\) is universal: any \\(U\\in U(2^{n})\\) can be "
          "written exactly as a finite product of CNOTs and single-qubit gates. The proof "
          "proceeds in three steps: (i) any unitary is a product of two-level unitaries "
          "(Givens rotations), \\(O(4^{n})\\) of them; (ii) any two-level unitary is a "
          "multiply-controlled single-qubit gate conjugated by Gray-code permutations built "
          "from CNOTs; (iii) a multiply-controlled gate decomposes into "
          "\\(O(n^{2})\\) elementary gates (linear in \\(n\\) with one ancilla).")
    + box('warn', 'Universality is not efficiency',
          "The counting argument is brutal: \\(U(2^{n})\\) has \\(4^{n}\\) real parameters, while a "
          "circuit of \\(g\\) gates from a fixed finite set has \\(O(g\\log g)\\) bits of "
          "description. Hence <em>almost every</em> unitary needs "
          "\\(\\Omega(4^{n}/n)\\) gates. Quantum computers are fast only on the "
          "measure-zero set of structured problems; there is no general-purpose exponential "
          "speed-up.")
)

S4 = (
    p("Real hardware offers a finite gate set, so exact universality is unattainable — the "
      "group generated by a finite set is countable. Approximate universality is the right "
      "notion.")
    + box('def', 'Approximate universality',
          "A gate set \\(\\mathcal G\\) is approximately universal if for every \\(U\\) and every "
          "\\(\\varepsilon>0\\) there is a product \\(V\\) of gates from \\(\\mathcal G\\) with "
          "\\(\\|U-V\\|_{\\infty}<\\varepsilon\\). Standard universal sets: "
          "\\(\\{H,T,\\text{CNOT}\\}\\) (Clifford+T), \\(\\{H,\\text{Toffoli}\\}\\), and "
          "\\(\\{\\text{CNOT}\\}\\cup\\{\\text{generic single-qubit }U\\}\\).")
    + box('thm', 'Solovay–Kitaev',
          "Let \\(\\mathcal G\\subset SU(d)\\) be finite, closed under inverses, and generate a "
          "dense subgroup. Then any \\(U\\in SU(d)\\) can be approximated to accuracy "
          "\\(\\varepsilon\\) by a product of \\(O(\\log^{c}(1/\\varepsilon))\\) gates with "
          "\\(c\\approx 3.97\\) for the standard proof (and \\(c\\to1\\) for specialised "
          "\\(z\\)-rotation synthesis over Clifford+T, by Ross–Selinger). The algorithm runs in "
          "time \\(O(\\log^{2.71}(1/\\varepsilon))\\).")
    + p("Combined with the linear error-accumulation bound of Chapter 1, this says a circuit of "
        "\\(m\\) ideal gates can be compiled into "
        "\\(O(m\\log^{c}(m/\\varepsilon))\\) physical gates with total error \\(\\varepsilon\\) — a "
        "polylogarithmic overhead, which is why the choice of universal gate set is "
        "computationally irrelevant. It is, however, extremely relevant to cost: in surface-code "
        "fault tolerance (Chapter 9) Clifford gates are nearly free while each \\(T\\) gate "
        "requires a distilled magic state, so <em>T-count</em> is the currency of "
        "fault-tolerant resource estimates.")
    + box('note', 'Gottesman–Knill, previewed',
          "Circuits built only from Clifford gates \\(\\{H,S,\\text{CNOT}\\}\\) acting on "
          "\\(|0\\rangle^{\\otimes n}\\) with computational-basis measurement are classically "
          "simulable in time \\(O(n^{2})\\) per gate. Entanglement alone therefore does not imply "
          "hardness; the non-Clifford resource (magic) is what makes simulation hard. "
          "Chapter 9 develops the stabilizer formalism behind this theorem.")
)

S5 = (
    p("Simulating a circuit naively as a \\(2^{n}\\times2^{n}\\) matrix product costs "
      "\\(O(8^{n})\\) per gate and is hopeless past \\(n\\approx 12\\). The standard trick is to "
      "keep the state as a rank-\\(n\\) tensor of shape \\((2,2,\\dots,2)\\) and contract each "
      "small gate against the relevant axes, costing \\(O(2^{n})\\) per one- or two-qubit gate.")
    + code('''import numpy as np

def apply_1q(state, U, q, n):
    """Apply single-qubit gate U to qubit q of an n-qubit state vector."""
    psi = state.reshape([2] * n)
    psi = np.tensordot(U, psi, axes=([1], [q]))      # new axis is at position 0
    psi = np.moveaxis(psi, 0, q)
    return psi.reshape(2 ** n)

def apply_2q(state, U, q0, q1, n):
    """Apply a 4x4 gate U to qubits (q0, q1); q0 is the more significant factor."""
    psi = state.reshape([2] * n)
    U4 = U.reshape(2, 2, 2, 2)                        # out0, out1, in0, in1
    psi = np.tensordot(U4, psi, axes=([2, 3], [q0, q1]))
    psi = np.moveaxis(psi, [0, 1], [q0, q1])
    return psi.reshape(2 ** n)

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)

psi = np.zeros(4, dtype=complex); psi[0] = 1
psi = apply_1q(psi, H, 0, 2)
psi = apply_2q(psi, CNOT, 0, 1, 2)
print(np.round(psi, 6))        # Bell state (|00> + |11>)/sqrt(2)''',
           'Tensor-contraction state-vector simulator — the pattern used in the exercises')
    + p("Two conventions must be fixed once and never mixed. We use "
        "<strong>qubit 0 = most significant</strong>, so the basis label of index \\(k\\) is the "
        "\\(n\\)-bit binary expansion of \\(k\\) read left to right. Qiskit uses the opposite "
        "(little-endian) convention; Chapter 10 flags the conversion explicitly.")
)

S6 = (
    p("A short catalogue of identities that make hand-compilation possible.")
    + ul([
        r'\(HXH=Z\), \(HZH=X\), \(HYH=-Y\).',
        r'\(\mathrm{CNOT}_{01}\,(X\otimes I)\,\mathrm{CNOT}_{01}=X\otimes X\); '
        r'\(\mathrm{CNOT}_{01}\,(I\otimes Z)\,\mathrm{CNOT}_{01}=Z\otimes Z\) — conjugation by '
        r'Cliffords maps Paulis to Paulis, the defining property of the Clifford group.',
        r'SWAP \(=\) three alternating CNOTs.',
        r'\(\mathrm{CZ}\) is symmetric under exchange of its two qubits; CNOT is not.',
        r'A Toffoli needs at least six CNOTs (Shende–Markov lower bound) and, in Clifford+T, '
        r'seven \(T\) gates (four with measurement and feed-forward).',
    ])
    + box('ex', 'Cost of an n-controlled NOT',
          "With \\(n-2\\) clean ancillas, \\(C^{n}X\\) costs \\(O(n)\\) Toffolis. With no ancillas "
          "it costs \\(O(n^{2})\\) elementary gates. With one <em>dirty</em> (arbitrary, "
          "must-be-restored) ancilla it is again \\(O(n)\\) — a trick due to Barenco et al. that "
          "is used constantly inside Shor's modular arithmetic (Chapter 7).")
)

# =============================== figures, citations and added commentary =====
BELL_CIRCUIT = circuit_svg(
    2,
    [[('g', 0, 'H')],
     [('c', 0, 1, 'X')],
     [('m', 0), ('m', 1)]],
    wire_labels=['|0⟩', '|0⟩'], width=470,
    title='Preparing a Bell pair, then measuring')

GHZ_CIRCUIT = circuit_svg(
    4,
    [[('g', 0, 'H')],
     [('c', 0, 1, 'X')],
     [('c', 1, 2, 'X')],
     [('c', 2, 3, 'X')]],
    wire_labels=['|0⟩'] * 4, width=470,
    title='A 4-qubit GHZ state in depth 4')

SWAP_CIRCUIT = circuit_svg(
    2,
    [[('c', 0, 1, 'X')],
     [('c', 1, 0, 'X')],
     [('c', 0, 1, 'X')],
     [('swap', 0, 1)]],
    wire_labels=['a', 'b'], width=470,
    title='SWAP = three alternating CNOTs (the fourth column is the shorthand)')

CU_CIRCUIT = circuit_svg(
    2,
    [[('g', 0, 'Rz')],
     [('g', 1, 'C')],
     [('c', 0, 1, 'X')],
     [('g', 1, 'B')],
     [('c', 0, 1, 'X')],
     [('g', 1, 'A')]],
    wire_labels=['control', 'target'], width=560,
    title='Controlled-U with exactly two CNOTs, from U = e^{iα} A X B X C with ABC = I')

_ns3 = list(range(1, 21))
PARAMS = line_chart(
    [dict(label='parameters of SU(2ⁿ):  4ⁿ − 1', xs=_ns3,
          ys=[log10(4 ** n - 1) for n in _ns3], color='#dc2626'),
     dict(label='gates a poly(n) circuit can afford:  n³', xs=_ns3,
          ys=[3 * log10(n) for n in _ns3], color='#026573'),
     dict(label='gates in Shor for an n-bit modulus:  ~n³ log n', xs=_ns3,
          ys=[3 * log10(n) + log10(max(log2(n), 1) + 1) for n in _ns3], color='#c9a227', dash='6 4')],
    xlim=(1, 20), ylim=(0, 12), xticks=[1,5,10,15,20], yticks=[0,3,6,9,12],
    xlabel='number of qubits  n',
    ylabel='log₁₀ (count)', height=330)

_eps = [10 ** (-k / 2) for k in range(2, 25)]
SK = line_chart(
    [dict(label='Solovay–Kitaev, c ≈ 3.97', xs=[-log10(e) for e in _eps],
          ys=[(log(1 / e)) ** 3.97 / 400 for e in _eps], color='#dc2626'),
     dict(label='Ross–Selinger z-rotation synthesis:  3 log₂(1/ε)', xs=[-log10(e) for e in _eps],
          ys=[3 * log2(1 / e) for e in _eps], color='#026573')],
    xlim=(1, 12), ylim=(0, 160), xticks=[1,3,6,9,12], yticks=[0,40,80,120,160],
    xlabel='target accuracy  log₁₀(1/ε)',
    ylabel='number of T gates required', height=330)

S1 = S1 + figure(
    '3.1',
    'Circuit notation, established on the smallest non-trivial example. Wires carry qubits and time '
    'runs left to right, so the unitary implemented is the product of the columns in reverse reading '
    'order: (CNOT)(H ⊗ I). A filled dot marks a control, the crossed circle marks the NOT target, and '
    'the meter symbol marks a computational-basis measurement. This four-gate circuit turns a product '
    'state into a maximally entangled one.',
    BELL_CIRCUIT, width=470, height=142) + p(
    "Two conventions embedded in the picture are worth stating, because they are the source of most "
    "confusion when comparing sources. First, the matrix product runs opposite to the drawing: "
    "the leftmost gate is applied first and therefore appears rightmost in the algebra. Second, "
    "measurement is drawn at the end, which by the principle of deferred measurement costs no "
    "generality — any mid-circuit measurement followed by classically controlled gates can be "
    "replaced by a coherent controlled gate and a terminal measurement" + cite('7') + ". Real "
    "hardware does measure mid-circuit, and Chapter 9 depends on it, but for reasoning about what "
    "circuits can compute the terminal-measurement model suffices.") + sources(
    'Circuit model, uniformity and deferred measurement: Nielsen &amp; Chuang §4.4–4.5'
    + cite('7') + '.')

S2 = S2 + figure(
    '3.2',
    'Any controlled-U can be built from two CNOTs and three single-qubit gates. Writing the Euler '
    'decomposition as U = e^{iα}AXBXC with ABC = I, the circuit applies C, flips the target '
    'conditionally, applies B, flips again, and applies A; the phase e^{iα} is absorbed into a '
    'z-rotation on the control. When the control is |0⟩ the two flips cancel and the target sees '
    'ABC = I; when it is |1⟩ the target sees AXBXC = U.',
    CU_CIRCUIT, width=560, height=190) + p(
    "This construction is the workhorse of quantum compilation" + cite('1') + ". It is also optimal: "
    "Shende, Bullock and Markov proved that a generic two-qubit unitary requires exactly three CNOTs, "
    "and a controlled-U with \\(U\\in SU(2)\\) exactly two" + cite('6') + ". Since CNOT count is a "
    "reasonable proxy for error on most hardware — two-qubit gates are typically an order of "
    "magnitude noisier than single-qubit ones — these lower bounds translate directly into "
    "fidelity ceilings for compiled circuits.") + sources(
    'Euler decomposition and the two-CNOT construction: Barenco et al. §5' + cite('1') + '; '
    'optimality: Shende–Bullock–Markov' + cite('6') + '.')

S3 = S3 + figure(
    '3.3',
    'Universality is not efficiency. The red curve counts the real parameters of an n-qubit unitary '
    'modulo global phase, 4ⁿ − 1; the teal and gold curves count the gates available to a circuit of '
    'polynomial size. The gap opens immediately and never closes, so almost every unitary needs '
    'exponentially many gates. Quantum algorithms live entirely in the thin, structured slice that '
    'the lower curves can reach.',
    PARAMS, height=330) + p(
    "The counting argument can be made rigorous by a dimension or a Kolmogorov-complexity argument: "
    "a circuit of \\(g\\) gates drawn from a fixed finite set is described by \\(O(g\\log g)\\) bits, "
    "so the set of unitaries reachable with \\(g\\) gates has covering number at most "
    "\\(2^{O(g\\log g)}\\), while covering \\(SU(2^{n})\\) to constant accuracy needs "
    "\\(2^{\\Omega(4^{n})}\\) balls" + cite('7') + ". Hence \\(g=\\Omega(4^{n}/n)\\) for almost all "
    "targets. The practical reading is that a claim of the form 'a quantum computer can implement "
    "this transformation' is empty unless accompanied by a circuit whose size is polynomial — a "
    "point that recurs in Chapter 10 when assessing algorithms that assume oracle access to large "
    "classical data.") + sources(
    'Exact universality and its constructive proof: Barenco et al.' + cite('1') + '; the counting '
    'argument: Nielsen &amp; Chuang §4.5.4' + cite('7') + '.')

S4 = S4 + figure(
    '3.4',
    'Cost of approximating a single z-rotation over the Clifford+T gate set. The generic '
    'Solovay–Kitaev construction gives a polylogarithmic but high-degree bound; the number-theoretic '
    'synthesis of Ross and Selinger reaches the information-theoretic optimum, 3 log₂(1/ε) T gates, '
    'and is what production compilers actually use. At the accuracy needed for a cryptographically '
    'relevant computation, ε ≈ 10⁻¹⁰, the difference is orders of magnitude in the number of '
    'distilled magic states.',
    SK, height=330) + p(
    "The reason T-count rather than total gate count is the right cost metric only becomes fully "
    "clear in Chapter 9, but the outline can be given now. In the surface code, Clifford operations "
    "are realised by lattice surgery or by relabelling and cost essentially nothing beyond the "
    "error-correction cycles that run anyway, whereas each \\(T\\) gate consumes a magic state "
    "produced by a distillation factory occupying a large fraction of the chip" + cite('4') + ". "
    "A fault-tolerant resource estimate is therefore, to first order, a T-count multiplied by a "
    "factory cost — which is why compilers optimise for T-count even at the price of more Cliffords."
) + sources(
    'Solovay–Kitaev: Kitaev' + cite('2') + ' and the constructive account of Dawson &amp; Nielsen'
    + cite('3') + '; optimal Clifford+T synthesis: Ross &amp; Selinger' + cite('4') + '; '
    'Gottesman–Knill: Gottesman' + cite('5') + '.')

S6 = S6 + figure(
    '3.5',
    'Two standard identities used constantly when compiling by hand. Left: SWAP decomposed into three '
    'alternating CNOTs — the last column shows the shorthand symbol for the same operation. On '
    'hardware with limited connectivity, SWAP networks are how distant qubits are brought together, '
    'and they often dominate the compiled gate count.',
    SWAP_CIRCUIT, width=470, height=190) + figure(
    '3.6',
    'A GHZ state on four qubits, prepared in linear depth by a chain of CNOTs. A logarithmic-depth '
    'variant exists by doubling the number of entangled qubits at each layer; on a device with '
    'nearest-neighbour connectivity only, however, the linear chain is often the cheaper option once '
    'routing is taken into account.',
    GHZ_CIRCUIT, width=470, height=234) + p(
    "Circuit identities of this kind are the quantum analogue of Boolean algebra, and the same "
    "caution applies: an identity that saves gates in the abstract may cost more after mapping to a "
    "physical device with a fixed coupling graph. Modern compilation is therefore a two-stage "
    "problem — logical synthesis, then routing — and the second stage can easily triple the CNOT "
    "count on a linear-connectivity architecture" + cite('6,7') + ".") + sources(
    'Gate identities and multiply-controlled constructions: Barenco et al. §6–7' + cite('1') + '; '
    'synthesis and routing costs: Shende–Bullock–Markov' + cite('6') + '.')

REFS = [
    dict(authors="A. Barenco, C. H. Bennett, R. Cleve, D. P. DiVincenzo, N. Margolus, P. Shor, "
                 "T. Sleator, J. A. Smolin and H. Weinfurter",
         title="Elementary gates for quantum computation",
         venue="Physical Review A 52, 3457", year="1995",
         link="https://arxiv.org/abs/quant-ph/9503016",
         note="The paper that established CNOT + single-qubit universality and the gate-count constructions of §3 and §6."),
    dict(authors="A. Yu. Kitaev", title="Quantum computations: algorithms and error correction",
         venue="Russian Mathematical Surveys 52(6), 1191–1249", year="1997",
         note="Original source of the Solovay–Kitaev theorem."),
    dict(authors="C. M. Dawson and M. A. Nielsen", title="The Solovay–Kitaev algorithm",
         venue="Quantum Information and Computation 6(1), 81–95", year="2006",
         link="https://arxiv.org/abs/quant-ph/0505030",
         note="The readable, constructive exposition; read this before the original."),
    dict(authors="N. J. Ross and P. Selinger",
         title="Optimal ancilla-free Clifford+T approximation of z-rotations",
         venue="Quantum Information and Computation 16(11–12), 901–953", year="2016",
         link="https://arxiv.org/abs/1403.2975",
         note="Near-optimal synthesis with T-count ~ 3log2(1/eps); the practical compiler algorithm."),
    dict(authors="D. Gottesman", title="The Heisenberg representation of quantum computers",
         venue="Proc. XXII Int. Colloquium on Group Theoretical Methods in Physics", year="1998",
         link="https://arxiv.org/abs/quant-ph/9807006",
         note="Stabilizer formalism and the Gottesman–Knill theorem previewed in §4."),
    dict(authors="V. V. Shende, S. S. Bullock and I. L. Markov",
         title="Synthesis of quantum-logic circuits",
         venue="IEEE Trans. CAD 25(6), 1000–1010", year="2006",
         link="https://arxiv.org/abs/quant-ph/0406176",
         note="Optimal CNOT counts for generic two- and three-qubit unitaries."),
    dict(authors="M. A. Nielsen and I. L. Chuang", title="Quantum Computation and Quantum Information",
         venue="Cambridge University Press", year="2010",
         note="Chapter 4 is the standard reference for everything in this chapter."),
]

CR = [
    dict(
        name='C3.Q1 — A state-vector simulator by tensor contraction',
        qtext=cr_qtext('C3.Q1', 'Applying gates without building 2^n x 2^n matrices',
                       "Building the full \\(2^{n}\\times2^{n}\\) matrix of a gate wastes "
                       "exponential memory. Reshaping the state to a rank-\\(n\\) tensor and "
                       "contracting only the relevant axes costs \\(O(2^{n})\\) per gate.",
                       "Write <code>apply_1q(state, U, q, n)</code> and "
                       "<code>apply_2q(state, U, q0, q1, n)</code> as described in §5, using "
                       "<code>numpy.tensordot</code> and <code>numpy.moveaxis</code>. "
                       "Convention: qubit 0 is the <strong>most significant</strong> factor. "
                       "Both return a flat length-\\(2^{n}\\) array.",
                       "H on qubit 0 of |00>, then CNOT(0,1)  ->  (|00> + |11>)/sqrt(2)"),
        answer='''import numpy as np

def apply_1q(state, U, q, n):
    psi = np.asarray(state, dtype=complex).reshape([2] * n)
    psi = np.tensordot(np.asarray(U, dtype=complex), psi, axes=([1], [q]))
    psi = np.moveaxis(psi, 0, q)
    return psi.reshape(2 ** n)

def apply_2q(state, U, q0, q1, n):
    psi = np.asarray(state, dtype=complex).reshape([2] * n)
    U4 = np.asarray(U, dtype=complex).reshape(2, 2, 2, 2)
    psi = np.tensordot(U4, psi, axes=([2, 3], [q0, q1]))
    psi = np.moveaxis(psi, [0, 1], [q0, q1])
    return psi.reshape(2 ** n)
''',
        preload='''import numpy as np

def apply_1q(state, U, q, n):
    # reshape -> tensordot -> moveaxis -> reshape
    ...

def apply_2q(state, U, q0, q1, n):
    ...
''',
        tests=[
            {'code': '''import numpy as np
H = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
psi = np.zeros(4, dtype=complex); psi[0] = 1
psi = apply_1q(psi, H, 0, 2)
psi = apply_2q(psi, CNOT, 0, 1, 2)
print(np.round(psi.real, 6).tolist())
''',
             'expected': '[0.707107, 0.0, 0.0, 0.707107]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
X = np.array([[0,1],[1,0]], dtype=complex)
psi = np.zeros(8, dtype=complex); psi[0] = 1
psi = apply_1q(psi, X, 2, 3)
print(int(np.argmax(np.abs(psi))))
''',
             'expected': '1\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
psi = np.zeros(4, dtype=complex); psi[2] = 1     # |10>
psi = apply_2q(psi, CNOT, 0, 1, 2)
print(int(np.argmax(np.abs(psi))))               # |11> = index 3
''',
             'expected': '3\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
psi = np.zeros(4, dtype=complex); psi[2] = 1     # |10>
psi = apply_2q(psi, CNOT, 1, 0, 2)               # control = qubit 1
print(int(np.argmax(np.abs(psi))))               # unchanged: |10> = index 2
''',
             'expected': '2\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': '''import numpy as np
rng = np.random.default_rng(3)
H = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)
psi = rng.normal(size=16) + 1j*rng.normal(size=16)
psi = psi/np.linalg.norm(psi)
out = apply_1q(apply_1q(psi, H, 2, 4), H, 2, 4)
print(np.allclose(out, psi))
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C3.Q2 — Controlled gates and the CNOT/CZ relation',
        qtext=cr_qtext('C3.Q2', 'Building two-qubit gates',
                       "\\(C\\text{-}U=|0\\rangle\\langle0|\\otimes I+|1\\rangle\\langle1|\\otimes U\\) "
                       "in the ordering where the control is the first factor.",
                       "Write <code>controlled(U)</code> returning the \\(4\\times4\\) "
                       "controlled-\\(U\\); and <code>cnot_from_cz()</code> returning the CNOT "
                       "matrix built <em>only</em> as \\((I\\otimes H)\\,\\mathrm{CZ}\\,(I\\otimes H)\\), "
                       "where CZ is constructed with <code>controlled</code>.",
                       "controlled(X)  ==  CNOT\n"
                       "cnot_from_cz() ==  CNOT"),
        answer='''import numpy as np

def controlled(U):
    U = np.asarray(U, dtype=complex)
    P0 = np.array([[1, 0], [0, 0]], dtype=complex)
    P1 = np.array([[0, 0], [0, 1]], dtype=complex)
    return np.kron(P0, np.eye(2, dtype=complex)) + np.kron(P1, U)

def cnot_from_cz():
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    CZ = controlled(Z)
    IH = np.kron(np.eye(2, dtype=complex), H)
    return IH @ CZ @ IH
''',
        preload='''import numpy as np

def controlled(U):
    # |0><0| (x) I  +  |1><1| (x) U
    ...

def cnot_from_cz():
    ...
''',
        tests=[
            {'code': '''import numpy as np
X = np.array([[0,1],[1,0]], dtype=complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
print(np.allclose(controlled(X), CNOT))
''',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
print(np.allclose(cnot_from_cz(), CNOT))
''',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
Z = np.array([[1,0],[0,-1]], dtype=complex)
print(np.round(np.diag(controlled(Z)).real, 6).tolist())
''',
             'expected': '[1.0, 1.0, 1.0, -1.0]\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
T = np.diag([1, np.exp(1j*np.pi/4)]).astype(complex)
CT = controlled(T)
print(np.allclose(CT.conj().T @ CT, np.eye(4)), np.allclose(np.linalg.matrix_power(CT, 8), np.eye(4)))
''',
             'expected': 'True True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': '''import numpy as np
Z = np.array([[1,0],[0,-1]], dtype=complex)
CZ = controlled(Z)
S = np.array([[0,0,1,0],[0,1,0,0],[1,0,0,0],[0,0,0,1]], dtype=complex)  # swap basis 00<->10
print(np.allclose(CZ, S @ CZ @ S))   # CZ is symmetric under qubit exchange
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C3.Q3 — ZYZ (Euler) decomposition of a single-qubit unitary',
        qtext=cr_qtext('C3.Q3', 'Compiling an arbitrary gate',
                       "Every \\(U\\in U(2)\\) factorises as "
                       "\\(e^{i\\alpha}R_z(\\beta)R_y(\\gamma)R_z(\\delta)\\). Extracting the angles "
                       "is the first step of every quantum compiler.",
                       "Write <code>zyz(U)</code> returning the tuple "
                       "<code>(alpha, beta, gamma, delta)</code> of floats, and "
                       "<code>from_zyz(alpha, beta, gamma, delta)</code> rebuilding the matrix, "
                       "with \\(R_z(\\lambda)=\\mathrm{diag}(e^{-i\\lambda/2},e^{i\\lambda/2})\\) and "
                       "\\(R_y(\\gamma)=\\begin{pmatrix}\\cos\\frac\\gamma2&-\\sin\\frac\\gamma2\\\\"
                       "\\sin\\frac\\gamma2&\\cos\\frac\\gamma2\\end{pmatrix}\\). "
                       "Grading only checks that <code>from_zyz(*zyz(U))</code> reproduces "
                       "<code>U</code>.",
                       "from_zyz(*zyz(H))  ==  H     (up to numerical tolerance)"),
        answer='''import numpy as np

def rz(l):
    return np.diag([np.exp(-1j * l / 2), np.exp(1j * l / 2)])

def ry(g):
    c, s = np.cos(g / 2), np.sin(g / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)

def from_zyz(alpha, beta, gamma, delta):
    return np.exp(1j * alpha) * (rz(beta) @ ry(gamma) @ rz(delta))

def zyz(U):
    U = np.asarray(U, dtype=complex)
    det = np.linalg.det(U)
    alpha = float(np.angle(det) / 2)
    V = U * np.exp(-1j * alpha)                 # V in SU(2)
    gamma = float(2 * np.arctan2(abs(V[1, 0]), abs(V[0, 0])))
    # V = [[e^{-i(b+d)/2} cos(g/2), -e^{-i(b-d)/2} sin(g/2)],
    #      [ e^{i(b-d)/2} sin(g/2),  e^{i(b+d)/2} cos(g/2)]]
    half_sum = np.angle(V[1, 1]) if abs(V[1, 1]) > 1e-12 else 0.0   # (b+d)/2
    half_dif = np.angle(V[1, 0]) if abs(V[1, 0]) > 1e-12 else 0.0   # (b-d)/2
    beta = float(half_sum + half_dif)
    delta = float(half_sum - half_dif)
    return (alpha, beta, gamma, delta)
''',
        preload='''import numpy as np

def rz(l):
    ...

def ry(g):
    ...

def from_zyz(alpha, beta, gamma, delta):
    ...

def zyz(U):
    # hint: remove the global phase via det(U), then read the angles off the SU(2) matrix
    ...
''',
        tests=[
            {'code': '''import numpy as np
H = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)
print(np.allclose(from_zyz(*zyz(H)), H, atol=1e-8))
''',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
T = np.diag([1, np.exp(1j*np.pi/4)]).astype(complex)
print(np.allclose(from_zyz(*zyz(T)), T, atol=1e-8))
''',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
X = np.array([[0,1],[1,0]], dtype=complex)
print(np.allclose(from_zyz(*zyz(X)), X, atol=1e-8))
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
rng = np.random.default_rng(2024)
ok = True
for _ in range(20):
    A = rng.normal(size=(2,2)) + 1j*rng.normal(size=(2,2))
    Q, R = np.linalg.qr(A)
    Q = Q @ np.diag(np.exp(1j*np.angle(np.diag(R))))
    ok = ok and np.allclose(from_zyz(*zyz(Q)), Q, atol=1e-7)
print(ok)
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': '''import numpy as np
I = np.eye(2, dtype=complex)
print(np.allclose(from_zyz(*zyz(I)), I, atol=1e-8))
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C3.Q4 — Running a circuit: Bell, GHZ and SWAP from CNOTs',
        qtext=cr_qtext('C3.Q4', 'A minimal circuit runner',
                       "A circuit is a list of instructions. This exercise assembles the "
                       "primitives of Q1–Q2 into a runner and verifies three standard "
                       "constructions.",
                       "Write <code>run(n, circuit)</code> where <code>circuit</code> is a list "
                       "of tuples <code>(gate_name, qubits)</code> with "
                       "<code>gate_name</code> in <code>{'H','X','Z','S','T','CNOT','CZ','SWAP'}</code> "
                       "and <code>qubits</code> a tuple of indices "
                       "(control first for CNOT/CZ). Start from \\(|0\\rangle^{\\otimes n}\\) and "
                       "return the final state vector. Implement SWAP as three CNOTs.",
                       "run(2, [('H',(0,)), ('CNOT',(0,1))])  ->  Bell state\n"
                       "run(3, [('H',(0,)), ('CNOT',(0,1)), ('CNOT',(1,2))])  ->  GHZ"),
        answer='''import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
S = np.diag([1, 1j]).astype(complex)
T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
CZ = np.diag([1, 1, 1, -1]).astype(complex)
ONE_Q = {'H': H, 'X': X, 'Z': Z, 'S': S, 'T': T}
TWO_Q = {'CNOT': CNOT, 'CZ': CZ}

def _apply1(state, U, q, n):
    psi = state.reshape([2] * n)
    psi = np.tensordot(U, psi, axes=([1], [q]))
    return np.moveaxis(psi, 0, q).reshape(2 ** n)

def _apply2(state, U, q0, q1, n):
    psi = state.reshape([2] * n)
    psi = np.tensordot(U.reshape(2, 2, 2, 2), psi, axes=([2, 3], [q0, q1]))
    return np.moveaxis(psi, [0, 1], [q0, q1]).reshape(2 ** n)

def run(n, circuit):
    psi = np.zeros(2 ** n, dtype=complex)
    psi[0] = 1
    for name, qs in circuit:
        if name in ONE_Q:
            psi = _apply1(psi, ONE_Q[name], qs[0], n)
        elif name in TWO_Q:
            psi = _apply2(psi, TWO_Q[name], qs[0], qs[1], n)
        elif name == 'SWAP':
            a, b = qs
            psi = _apply2(psi, CNOT, a, b, n)
            psi = _apply2(psi, CNOT, b, a, n)
            psi = _apply2(psi, CNOT, a, b, n)
        else:
            raise ValueError('unknown gate ' + name)
    return psi
''',
        preload='''import numpy as np

def run(n, circuit):
    # start from |0...0>, apply each instruction in order
    ...
''',
        tests=[
            {'code': "import numpy as np\n"
                     "psi = run(2, [('H',(0,)), ('CNOT',(0,1))])\n"
                     "print(np.round(psi.real, 6).tolist())\n",
             'expected': '[0.707107, 0.0, 0.0, 0.707107]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': "import numpy as np\n"
                     "psi = run(3, [('H',(0,)), ('CNOT',(0,1)), ('CNOT',(1,2))])\n"
                     "print(np.round(np.abs(psi)**2, 6).tolist())\n",
             'expected': '[0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5]\n',
             'useasexample': '1', 'display': 'SHOW'},
            {'code': "import numpy as np\n"
                     "psi = run(2, [('X',(0,)), ('SWAP',(0,1))])\n"
                     "print(int(np.argmax(np.abs(psi))))\n",
             'expected': '1\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': "import numpy as np\n"
                     "psi = run(1, [('H',(0,)), ('T',(0,)), ('T',(0,)), ('H',(0,))])\n"
                     "ref = np.array([1+1j, 1-1j])/2\n"
                     "print(np.allclose(np.abs(psi), np.abs(ref)))\n",
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': "import numpy as np\n"
                     "psi = run(4, [('H',(0,)), ('H',(1,)), ('H',(2,)), ('H',(3,))])\n"
                     "print(np.allclose(np.abs(psi)**2, np.full(16, 1/16)))\n",
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

ST = [
    stack_question(
        name='C3.S1 — Powers of the T gate',
        questiontext=stack_qtext(
            'C3.S1', 'Clifford hierarchy by hand',
            r'<p>Let \(T=\mathrm{diag}(1,e^{i\pi/4})\).</p>'
            r'<p>(a) Give the smallest positive integer \(k\) with \(T^{k}=Z\).</p>'
            r'<p>\(k=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the phase \(\lambda\) (a complex number) such that '
            r'\(T^{ {@m@} }=\mathrm{diag}(1,\lambda)\).</p>'
            r'<p>\(\lambda=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>(a) \(T^{k}=\mathrm{diag}(1,e^{ik\pi/4})\). We need \(e^{ik\pi/4}=-1=e^{i\pi}\), '
            r'i.e. \(k\pi/4\equiv\pi \pmod{2\pi}\), whose smallest positive solution is \(k=4\).</p>'
            r'<p>So \(T^2=S\), \(T^4=Z\), \(T^8=I\): \(T\) generates a cyclic group of order 8, and '
            r'\(S,Z\) are Clifford while \(T\) is not — \(T\) sits at level 3 of the Clifford '
            r'hierarchy. This is exactly why fault-tolerant cost is measured in T-count.</p>'
            r'<p>(b) \(T^{ {@m@} }=\mathrm{diag}(1,e^{i {@m@} \pi/4})={@ta2@}\) in the second entry.</p>'),
        questionvariables='m : rand_with_step(2,7,1);\nta1 : 4;\nta2 : exp(%i*m*%pi/4);',
        questionnote='m={@m@}, lambda={@ta2@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=8, value='0.5000000',
                 truefb=r'<p>Correct: \(T^4=Z\).</p>',
                 falsefb=r'<p>Solve \(e^{ik\pi/4}=-1\) for the smallest positive integer \(k\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=18, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>\(T^{m}\) multiplies the \(|1\rangle\) amplitude by \(e^{im\pi/4}\).</p>')]),
    stack_question(
        name='C3.S2 — Parameter counting and the limits of universality',
        questiontext=stack_qtext(
            'C3.S2', 'Why almost every unitary is hard',
            r'<p>Consider unitaries on \(n={@n@}\) qubits.</p>'
            r'<p>(a) Give the number of real parameters of \(SU(2^{n})\), i.e. of an \(n\)-qubit '
            r'unitary modulo global phase, as a function of <code>n</code> in general.</p>'
            r'<p>parameters \(=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Evaluate that expression for \(n={@n@}\).</p>'
            r'<p>value \(=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>(a) \(U(d)\) is a real Lie group of dimension \(d^{2}\); quotienting the global '
            r'phase \(U(1)\) leaves \(d^{2}-1\). With \(d=2^{n}\) this is \(4^{n}-1\).</p>'
            r'<p>(b) For \(n={@n@}\): \(4^{ {@n@} }-1={@ta2@}\).</p>'
            r'<p>A circuit of \(g\) gates from a fixed finite set is specified by \(O(g\log g)\) bits, '
            r'so reaching all of \(SU(2^n)\) to constant accuracy requires \(g=\Omega(4^{n}/n)\). '
            r'Universality therefore never implies efficiency: quantum speed-ups exist only for '
            r'structured problems.</p>'),
        questionvariables='n : rand_with_step(3,6,1);\nta1 : 4^n-1;\nta2 : 4^n-1;',
        questionnote='n={@n@}, 4^n-1={@ta2@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=14, value='0.5000000',
                 truefb=r'<p>Correct: \(\dim SU(2^{n})=4^{n}-1\).</p>',
                 falsefb=r'<p>\(\dim U(d)=d^{2}\) as a real Lie group; remove one dimension for the '
                         r'global phase, with \(d=2^{n}\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=12, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Substitute the given \(n\) into \(4^{n}-1\).</p>')]),
    stack_question(
        name='C3.S3 — Clifford conjugation of Pauli operators',
        questiontext=stack_qtext(
            'C3.S3', 'Heisenberg picture for Clifford gates',
            r'<p>Recall \(H=\frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\), '
            r'\(Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix}\).</p>'
            r'<p>(a) Give the matrix \(HYH\).</p>'
            r'<p>\(HYH=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>Enter it in the form <code>matrix([a,b],[c,d])</code>.</p>'
            r'<p>(b) Give the matrix \(SXS^{\dagger}\) where \(S=\mathrm{diag}(1,i)\).</p>'
            r'<p>\(SXS^{\dagger}=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>(a) \(HXH=Z\), \(HZH=X\) and, since \(Y=iXZ\), \(HYH=iHXH\cdot HZH=iZX=-Y\). '
            r'Explicitly \(HYH=\begin{pmatrix}0&i\\-i&0\end{pmatrix}\).</p>'
            r'<p>(b) \(SXS^{\dagger}=\begin{pmatrix}0&-i\\i&0\end{pmatrix}=Y\).</p>'
            r'<p>Both results illustrate the defining property of the Clifford group: conjugation '
            r'maps the Pauli group to itself. Tracking Paulis instead of state vectors is the '
            r'Heisenberg picture behind the Gottesman–Knill theorem and the stabilizer codes of '
            r'Chapter 9 — and it is why Clifford circuits are classically simulable.</p>'),
        questionvariables='ta1 : matrix([0,%i],[-%i,0]);\nta2 : matrix([0,-%i],[%i,0]);',
        questionnote='HYH=-Y, SXS+=Y',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', type='matrix', boxsize=12,
                 value='0.5000000', forbidfloat=0,
                 truefb=r'<p>Correct: \(HYH=-Y\).</p>',
                 falsefb=r'<p>Use \(Y=iXZ\) together with \(HXH=Z\) and \(HZH=X\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', type='matrix', boxsize=12,
                 value='0.5000000', forbidfloat=0,
                 truefb=r'<p>Correct: \(SXS^{\dagger}=Y\).</p>',
                 falsefb=r'<p>Multiply out \(\mathrm{diag}(1,i)\,X\,\mathrm{diag}(1,-i)\).</p>')]),
]

CHAPTER = dict(
    no=3, slug='gates-circuits-universality',
    title='Quantum Gates, Circuits and Universality',
    subtitle='The circuit model, standard gate library, exact and approximate universality, '
             'Solovay–Kitaev, T-count, and how to simulate a circuit efficiently in NumPy.',
    prereq='Chapters 1–2 (tensor products, Pauli algebra, rotations, operator norm).',
    objectives=[
        'Define circuit size, depth and uniformity, and justify deferred measurement.',
        'Decompose any single-qubit unitary into ZYZ Euler angles and any controlled-U into two CNOTs.',
        'State and outline the proof of CNOT + single-qubit universality.',
        'Explain why universality does not imply efficiency, via a parameter-counting argument.',
        'State Solovay–Kitaev and explain why T-count is the fault-tolerant cost metric.',
        'Implement an O(2^n)-per-gate state-vector simulator by tensor contraction.',
    ],
    sections=[
        ('The circuit model', S1),
        ('The standard gate library', S2),
        ('Exact universality', S3),
        ('Approximate universality and Solovay–Kitaev', S4),
        ('Simulating circuits efficiently', S5),
        ('Circuit identities and gate counts', S6),
    ],
    summary="Quantum circuits are products of \\(O(1)\\)-qubit unitaries. CNOT together with all "
            "single-qubit gates is exactly universal, and any finite dense set — Clifford+T, say — "
            "is approximately universal with only polylogarithmic overhead by Solovay–Kitaev. "
            "Counting parameters shows that almost every unitary nevertheless needs "
            "exponentially many gates, so the interesting question is always which structured "
            "unitaries admit short circuits. Chapters 6–8 answer that for the Fourier transform, "
            "period finding and amplitude amplification.",
    references=REFS, coderunner=CR, stack=ST,
)
