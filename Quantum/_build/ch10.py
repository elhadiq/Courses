# -*- coding: utf-8 -*-
"""Chapter 10 — Quantum Complexity, NISQ Algorithms and Qiskit in Practice."""
from math import log10, cos, sin, pi, sqrt
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, nested_svg,
                    flow_svg, graph_svg, interactive, C, SERIF, MONO)

S1 = (
    p("<strong>BQP</strong> is the class of decision problems solvable by a uniform family of "
      "polynomial-size quantum circuits with error at most \\(1/3\\). The error constant is "
      "irrelevant: majority voting over \\(O(\\log(1/\\delta))\\) repetitions amplifies it to "
      "\\(1-\\delta\\) by the Chernoff bound.")
    + eq(r"\mathrm{P}\subseteq\mathrm{BPP}\subseteq\mathrm{BQP}\subseteq\mathrm{PP}"
         r"\subseteq\mathrm{PSPACE} .")
    + p("The last inclusions come from writing the acceptance amplitude as an exponentially "
        "large sum of path amplitudes, each computable in polynomial space — the Feynman path "
        "sum. No inclusion beyond \\(\\mathrm{BPP}\\subseteq\\mathrm{BQP}\\) is known to be strict, "
        "and proving \\(\\mathrm{BQP}\\ne\\mathrm{BPP}\\) would imply "
        "\\(\\mathrm P\\ne\\mathrm{PSPACE}\\). All evidence for quantum advantage is therefore "
        "either relative to an oracle, or conditional on standard cryptographic assumptions.")
    + box('note', 'Where the famous problems sit',
          "Factoring is in \\(\\mathrm{BQP}\\cap\\mathrm{NP}\\cap\\mathrm{coNP}\\) and is <em>not</em> "
          "believed NP-complete. Grover gives only a quadratic speed-up, and the BBBV bound of "
          "Chapter 8 shows that a black-box approach cannot do better — so there is no evidence "
          "that \\(\\mathrm{NP}\\subseteq\\mathrm{BQP}\\). Relative to a random oracle "
          "\\(\\mathrm{NP}\\not\\subseteq\\mathrm{BQP}\\). The honest summary: quantum computers "
          "are believed to be exponentially faster on a narrow, highly structured class of "
          "problems, not on optimisation in general.")
    + p("The quantum analogue of NP is <strong>QMA</strong>: problems whose yes-instances admit a "
        "polynomial-size quantum witness verifiable in \\(\\mathrm{BQP}\\). The canonical "
        "QMA-complete problem is the <em>local Hamiltonian problem</em> — decide whether the "
        "ground energy of a sum of \\(k\\)-local terms is below \\(a\\) or above \\(b\\) with "
        "\\(b-a\\ge1/\\mathrm{poly}(n)\\) — QMA-complete already for \\(k=2\\) "
        "(Kitaev; Kempe–Kitaev–Regev). This is the formal reason no quantum algorithm can be "
        "expected to find ground states of arbitrary Hamiltonians efficiently.")
)

S2 = (
    p("A second, weaker but experimentally accessible notion is <strong>sampling advantage</strong>: "
      "producing samples from a distribution that no classical algorithm can produce in "
      "polynomial time, under plausible complexity assumptions. Unlike BQP separations, these "
      "come with (conditional) proofs.")
    + table(['Proposal', 'Hardness basis', 'Status'],
            [['BosonSampling (Aaronson–Arkhipov 2011)', 'permanent is #P-hard; anti-concentration conjecture',
              'Photonic demonstrations 2020–2023; classical spoofing contested'],
             ['IQP / commuting circuits', 'collapse of the polynomial hierarchy', 'Theoretical'],
             ['Random circuit sampling (Google 2019)', 'average-case hardness of amplitude estimation',
              'Repeatedly challenged by improved tensor-network simulation'],
             ['Instantaneous quantum polynomial-time with noise', '—',
              'Noise generally destroys hardness — verification is the open problem']])
    + box('warn', 'How to read an advantage claim',
          "Three questions decide whether a demonstration means anything: (i) is the sampling "
          "task hard <em>on average</em>, or only in the worst case? (ii) does the fidelity of the "
          "noisy device still support the hardness argument? (iii) has the classical baseline "
          "been optimised, or is it a naive Schrödinger simulation? Several headline claims have "
          "been substantially reduced by better tensor-network contraction after publication. "
          "Sampling advantage is also, by construction, useless: the output solves no problem "
          "anyone wanted solved.")
)

S3 = (
    p("Current devices have \\(10^{2}\\)–\\(10^{3}\\) physical qubits, two-qubit error rates near "
      "\\(10^{-3}\\), and no error correction — the <strong>NISQ</strong> regime. Circuit depth is "
      "limited to roughly \\(1/\\varepsilon\\) gates before the signal is lost, which rules out "
      "Shor and full phase estimation. The response has been variational algorithms: short "
      "parameterised circuits optimised by a classical outer loop.")
    + box('def', 'Variational Quantum Eigensolver (Peruzzo et al. 2014)',
          "Given \\(H=\\sum_j c_j P_j\\) as a sum of Pauli strings, minimise "
          "\\(E(\\vec\\theta)=\\langle\\psi(\\vec\\theta)|H|\\psi(\\vec\\theta)\\rangle\\) over a "
          "parameterised circuit \\(|\\psi(\\vec\\theta)\\rangle=U(\\vec\\theta)|0\\rangle\\). "
          "The quantum device estimates each \\(\\langle P_j\\rangle\\) by sampling; a classical "
          "optimiser updates \\(\\vec\\theta\\). The variational principle guarantees "
          "\\(E(\\vec\\theta)\\ge E_0\\) for every \\(\\vec\\theta\\), so the output is always an "
          "upper bound on the ground energy.")
    + box('prop', 'Parameter-shift rule',
          "If \\(U(\\theta)=e^{-i\\theta P/2}\\) with \\(P^{2}=I\\), then the exact gradient of any "
          "expectation value is "
          "\\(\\partial_\\theta\\langle A\\rangle=\\tfrac12\\big[\\langle A\\rangle_{\\theta+\\pi/2}"
          "-\\langle A\\rangle_{\\theta-\\pi/2}\\big]\\). This is an <em>exact</em> identity, not a "
          "finite difference: gradients are obtained from the same circuit at shifted "
          "parameters, at no extra depth.")
    + p("<strong>QAOA</strong> (Farhi–Goldstone–Gutmann 2014) is the combinatorial-optimisation "
        "cousin: alternate \\(e^{-i\\gamma_k H_C}\\) and \\(e^{-i\\beta_k H_M}\\) for \\(p\\) layers, "
        "with \\(H_C\\) encoding the cost function and \\(H_M=\\sum_i X_i\\). As \\(p\\to\\infty\\) it "
        "recovers adiabatic evolution; at fixed small \\(p\\) its performance on MaxCut is known "
        "exactly for regular graphs, and is not competitive with the best classical "
        "approximation algorithms (Goemans–Williamson achieves 0.878).")
)

S4 = (
    box('thm', 'Barren plateaus (McClean et al. 2018)',
        "For a random parameterised circuit that forms a 2-design on \\(n\\) qubits, the "
        "expectation \\(\\mathrm E[\\partial_\\theta E]=0\\) and "
        "\\(\\mathrm{Var}[\\partial_\\theta E]=O(2^{-n})\\). Gradients vanish exponentially in the "
        "number of qubits, so the number of shots needed to resolve a descent direction grows "
        "exponentially. Deep hardware-efficient ansätze are therefore untrainable at scale.")
    + p("Later work showed barren plateaus also arise from global cost functions, from "
        "entanglement in the ansatz, and from noise itself (noise-induced barren plateaus, "
        "Wang et al. 2021). Avoiding them requires structure: shallow local cost functions, "
        "problem-informed ansätze such as UCCSD or the Hamiltonian variational ansatz, and "
        "careful initialisation. There is, at present, no variational algorithm with a proven "
        "asymptotic speed-up.")
    + box('def', 'Error mitigation (not correction)',
          "Techniques that reduce bias in an <em>expectation value</em> without correcting the "
          "state. <strong>Zero-noise extrapolation</strong>: rescale the noise by stretching gate "
          "durations or folding gates \\(U\\to UU^{\\dagger}U\\), then extrapolate to zero noise. "
          "<strong>Probabilistic error cancellation</strong>: invert the noise channel by "
          "quasi-probability sampling. <strong>Symmetry verification</strong>: post-select on "
          "conserved quantities. All of them pay an exponential sampling overhead in circuit "
          "size — mitigation buys accuracy, never scalability.")
    + p("The honest position for a graduate reader: variational NISQ algorithms are valuable as "
        "hardware benchmarks and as a research programme, but no instance is known where they "
        "beat the best classical method on a useful problem. The credible long-term route to "
        "advantage runs through the fault tolerance of Chapter 9.")
)

S5 = (
    p("The exercises in this course are deliberately NumPy-only so that they run on any "
      "auto-grading sandbox. The same constructions in Qiskit are given here for reference; they "
      "are not auto-graded, and you are encouraged to run them locally after "
      "<code>pip install qiskit qiskit-aer</code>.")
    + box('warn', 'Endianness',
          "Qiskit uses <strong>little-endian</strong> ordering: <code>qc.h(0)</code> acts on the "
          "<em>least</em> significant factor, and the string printed for a basis state is reversed "
          "relative to the convention used throughout these notes (qubit 0 = most significant). "
          "When comparing a Qiskit statevector to one of your NumPy vectors, reverse the qubit "
          "order — this is the single most common source of confusion.")
    + code('''from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

# --- Bell state -------------------------------------------------------------
qc = QuantumCircuit(2)
qc.h(0); qc.cx(0, 1)
print(Statevector(qc))                 # (|00> + |11>)/sqrt(2)

# --- A Hamiltonian as a sum of Pauli strings --------------------------------
H = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 0.5), ("IX", 0.5)])
print(Statevector(qc).expectation_value(H).real)

# --- A two-parameter variational ansatz and its energy ----------------------
def ansatz(theta, phi):
    qc = QuantumCircuit(2)
    qc.ry(theta, 0); qc.ry(phi, 1); qc.cx(0, 1)
    return qc

import numpy as np
grid = [(t, p, Statevector(ansatz(t, p)).expectation_value(H).real)
        for t in np.linspace(0, 2*np.pi, 25) for p in np.linspace(0, 2*np.pi, 25)]
print(min(grid, key=lambda r: r[2]))''',
           'Qiskit reference implementation — optional, not auto-graded')
    + code('''from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# --- sampling with a depolarizing noise model -------------------------------
noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(0.01, 2), ['cx'])

qc = QuantumCircuit(2, 2)
qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1])

sim = AerSimulator(noise_model=noise)
print(sim.run(transpile(qc, sim), shots=4096).result().get_counts())''',
           'Noisy simulation with Aer — compare with your Chapter 5 Kraus implementation')
)

S6 = (
    code('''import numpy as np
from itertools import product

I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
PAULI = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}

def pauli_string(s):
    out = np.array([[1.0+0j]])
    for ch in s:
        out = np.kron(out, PAULI[ch])
    return out

def hamiltonian(terms):
    """terms = [('ZZ', 1.0), ('XI', 0.5), ...]"""
    n = len(terms[0][0])
    H = np.zeros((2**n, 2**n), dtype=complex)
    for s, c in terms:
        H = H + c * pauli_string(s)
    return H

H = hamiltonian([('ZZ', 1.0), ('XI', 0.5), ('IX', 0.5)])
print(round(float(np.linalg.eigvalsh(H)[0]), 6))    # exact ground energy''',
         'Pauli-sum Hamiltonians in NumPy — the input format of every variational algorithm')
    + p("Two practical remarks. First, the number of Pauli terms for a chemistry Hamiltonian "
        "grows as \\(O(n^{4})\\) in the number of spin orbitals, and each must be measured "
        "separately unless terms are grouped into commuting cliques — measurement cost, not "
        "circuit depth, is usually the binding constraint. Second, estimating an energy to "
        "chemical accuracy (\\(1.6\\) mHa) by naive sampling needs on the order of \\(10^{8}\\) "
        "shots per term; this is the arithmetic behind most scepticism about near-term VQE.")
)

# =============================== figures, citations and added commentary =====
CLASSES10 = nested_svg(
    [('PSPACE', '#94a3b8'),
     ('PP', '#0891a1'),
     ('BQP — efficient quantum computation', '#026573'),
     ('BPP — efficient randomised classical computation', '#c9a227'),
     ('P', '#9333ea')],
    height=300)

VQE_LOOP = flow_svg(
    [(24, 56, 154, 62, 'CLASSICAL|choose parameters θ', '#f8fafc', '#475569'),
     (216, 56, 158, 62, 'QUANTUM|run U(θ) on |0…0⟩', '#ecfeff', '#026573'),
     (412, 56, 158, 62, 'QUANTUM|measure each Pauli|term of H', '#ecfeff', '#0891a1'),
     (412, 158, 158, 58, 'CLASSICAL|E(θ) = Σⱼ cⱼ⟨Pⱼ⟩', '#fefce8', '#c9a227'),
     (216, 158, 158, 58, 'CLASSICAL|gradient by|parameter shift', '#fefce8', '#92400e'),
     (24, 158, 154, 58, 'update θ|and repeat', '#f5f3ff', '#6d28d9')],
    [(180, 87, 214, 87, ''), (376, 87, 410, 87, ''), (491, 120, 491, 156, ''),
     (410, 187, 376, 187, ''), (214, 187, 180, 187, ''), (101, 156, 101, 120, '')],
    height=246, title='The variational loop: a short quantum circuit inside a classical optimiser')

_nq = list(range(2, 31))
BARREN = line_chart(
    [dict(label='gradient variance  Var[∂E] ~ 2⁻ⁿ', xs=_nq, ys=[-n * 0.30103 for n in _nq],
          color='#dc2626'),
     dict(label='shots needed to resolve the sign  ~2ⁿ', xs=_nq, ys=[n * 0.30103 - 6 for n in _nq],
          color='#026573'),
     dict(label='shots available in one hour at 10 kHz  (3.6 × 10⁷)', xs=_nq,
          ys=[log10(3.6e7) - 6 for n in _nq], color='#94a3b8', dash='5 4')],
    xlim=(2, 30), ylim=(-10, 4), xticks=[2,5,10,15,20,25,30],
    yticks=[-10,-8,-6,-4,-2,0,2,4], xlabel='number of qubits  n',
    ylabel='log₁₀ (variance)   /   log₁₀ (shots) − 6',
    vlines=[(25, 'practical wall', '#475569')], height=330)

MAXCUT = graph_svg(
    {'0': (170, 90), '1': (280, 170), '2': (170, 250), '3': (60, 170)},
    [('0', '1'), ('1', '2'), ('2', '3'), ('3', '0'), ('0', '2')],
    node_colors={'0': '#026573', '2': '#026573', '1': '#c9a227', '3': '#c9a227'},
    width=680, height=330,
    title='MaxCut on a five-edge graph: colours show one optimal partition (cut = 4)')

JS_VQE = """
  var b = JXG.JSXGraph.initBoard('ch10vqe', {boundingbox: [-0.6, 1.55, 6.9, -1.65],
      axis: false, showCopyright: false, showNavigation: false});
  var hz = b.create('slider', [[0.1, 1.42], [2.4, 1.42], [-1, 0.6, 1]],
      {name: 'c_Z', snapWidth: 0.05, strokeColor: '#026573'});
  var hx = b.create('slider', [[3.4, 1.42], [5.9, 1.42], [-1, 0.8, 1]],
      {name: 'c_X', snapWidth: 0.05, strokeColor: '#c9a227'});
  b.create('line', [[0, 0], [2 * Math.PI, 0]], {strokeColor: '#0f172a', strokeWidth: 1.3,
      straightFirst: false, straightLast: false, fixed: true});
  b.create('line', [[0, -1.4], [0, 1.3]], {strokeColor: '#0f172a', strokeWidth: 1.3,
      straightFirst: false, straightLast: false, fixed: true});
  function E(t) { return hz.Value() * Math.cos(t) + hx.Value() * Math.sin(t); }
  b.create('functiongraph', [E, 0, 2 * Math.PI], {strokeColor: '#026573', strokeWidth: 2.8});
  b.create('functiongraph', [function () {
      return -Math.sqrt(hz.Value() * hz.Value() + hx.Value() * hx.Value());
  }, 0, 2 * Math.PI], {strokeColor: '#dc2626', dash: 2, strokeWidth: 1.8});
  var g = b.create('glider', [1.0, 0, b.create('functiongraph', [E, 0, 2 * Math.PI],
      {visible: false})], {name: '&#952;', size: 4, strokeColor: '#0f172a', fillColor: '#0f172a'});
  b.create('text', [0.0, -1.5, function () {
      var t = g.X();
      var grad = 0.5 * (E(t + Math.PI / 2) - E(t - Math.PI / 2));
      var exact = -Math.sqrt(hz.Value() * hz.Value() + hx.Value() * hx.Value());
      return 'E(&#952;) = ' + E(t).toFixed(4) +
             ',  parameter-shift gradient = ' + grad.toFixed(4) +
             ',  exact ground energy = ' + exact.toFixed(4);
  }], {fontSize: 13.5, strokeColor: '#0f172a'});
  b.create('text', [4.1, -1.22, 'red dashed: true ground energy'],
      {fontSize: 12, strokeColor: '#dc2626'});
  b.create('text', [2.3, 1.16, 'ansatz: R_y(&#952;)|0&#10217;,  H = c_Z Z + c_X X'],
      {fontSize: 13, strokeColor: '#475569'});
"""

S1 = S1 + figure(
    '10.1',
    'The complexity landscape as currently understood. Every inclusion drawn is proved; none is '
    'known to be strict, and proving BQP ≠ BPP would in particular prove P ≠ PSPACE, which is far '
    'beyond present technique. Note where NP does not appear: it is not known to contain BQP or to '
    'be contained in it, and relative to a random oracle NP ⊄ BQP, so there is no reason to expect '
    'quantum computers to solve NP-complete problems.',
    CLASSES10, height=300) + p(
    "The absence of unconditional separations is not a gap that better arguments will soon close; "
    "it is the same barrier that blocks all of classical complexity theory" + cite('1') + ". What "
    "the field offers instead are three weaker but rigorous statements: oracle separations, which "
    "are unconditional but relative to a black box; conditional separations, which assume standard "
    "cryptographic hardness; and sampling separations, which assume plausible average-case "
    "conjectures. Reading a quantum-advantage claim correctly means identifying which of the three "
    "is being asserted. For the local Hamiltonian problem the situation is sharper and more "
    "discouraging for applications: it is QMA-complete already for two-local terms" + cite('2,3')
    + ", so a general-purpose quantum ground-state solver would imply BQP = QMA, which nobody "
    "believes.") + sources(
    'BQP and its inclusions: Bernstein &amp; Vazirani' + cite('1') + '; QMA and the local '
    'Hamiltonian problem: Kitaev et al.' + cite('2') + ', Kempe–Kitaev–Regev' + cite('3') + '.')

S2 = S2 + sources(
    'BosonSampling and the framework for sampling hardness: Aaronson &amp; Arkhipov' + cite('4')
    + '; the superconducting demonstration and the subsequent classical-simulation debate'
    + cite('5') + '; a measured survey' + cite('6') + '.')

S3 = S3 + figure(
    '10.2',
    'The variational loop. The quantum device does only one thing: prepare a short parameterised '
    'circuit and measure Pauli expectation values. Everything else — energy assembly, gradients via '
    'the parameter-shift rule, and the parameter update — is classical. The design goal is to keep '
    'the quantum stage shallow enough that noise does not destroy the signal, which is what makes '
    'this family the natural response to hardware without error correction.',
    VQE_LOOP, height=246) + figure(
    '10.3',
    'A MaxCut instance. The cost Hamiltonian assigns energy ½(1 − zᵢzⱼ) to each edge, so minimising '
    '−H_C means finding the partition cutting the most edges. The colouring shown cuts four of the '
    'five edges, which is optimal here. QAOA prepares a superposition over all partitions and uses '
    'alternating cost and mixer evolutions to concentrate amplitude on good ones.',
    MAXCUT, height=330) + interactive(
    '10.4', 'ch10vqe',
    'A complete single-qubit variational problem. Set the Hamiltonian coefficients with the two '
    'sliders and drag the point along the energy curve. Three things are worth verifying: the curve '
    'never dips below the red line (the variational principle), the printed parameter-shift gradient '
    'agrees with the visible slope at every point (it is an exact identity, not a finite difference), '
    'and the landscape is a pure sinusoid — a single parameter always gives a trigonometric '
    'polynomial of degree one.',
    JS_VQE, aspect='16/9', max_width=660,
    hint='drag the sliders, then drag θ along the curve.') + p(
    "The variational principle guarantees that the output is an upper bound on the ground energy, "
    "which is genuinely useful: unlike a heuristic, the method cannot report an energy that is too "
    "low" + cite('7') + ". What it cannot guarantee is that the bound is tight, and there is the "
    "difficulty. Chemical accuracy for molecular energies is about \\(1.6\\times10^{-3}\\) hartree "
    "against total energies of order \\(10^{2}\\) hartree, a relative precision of \\(10^{-5}\\), "
    "reached only if the ansatz is expressive enough and the optimiser finds its global minimum. "
    "For QAOA on MaxCut the position is cleaner and less encouraging: the depth-one performance on "
    "3-regular graphs is exactly \\(0.6924\\) of optimal" + cite('8') + ", against the classical "
    "Goemans–Williamson guarantee of \\(0.878\\).") + sources(
    'VQE: Peruzzo et al.' + cite('7') + '; QAOA: Farhi, Goldstone &amp; Gutmann' + cite('8')
    + '; the parameter-shift rule is derived in the exercises of this chapter.')

S4 = S4 + figure(
    '10.5',
    'Why deep hardware-efficient ansätze cannot be trained. For a circuit random enough to form a '
    '2-design, the gradient has zero mean and variance falling as 2⁻ⁿ, so the number of shots needed '
    'merely to determine which way to step grows exponentially. The grey line marks the shots '
    'available in an hour on a device running at 10 kHz: beyond roughly 25 qubits the gradient is '
    'below the noise floor and the optimiser performs a random walk.',
    BARREN, height=330) + p(
    "Barren plateaus are not a numerical artefact but a concentration-of-measure phenomenon: on the "
    "unitary group with Haar measure, expectation values concentrate exponentially around their "
    "average, and a circuit deep enough to scramble inherits that behaviour" + cite('9') + ". The "
    "known escapes all amount to refusing to be random — shallow circuits with local cost "
    "functions, ansätze built from the problem's own Hamiltonian, layerwise training, or clever "
    "initialisation. Each restores trainability at the cost of expressivity, and there is a growing "
    "body of work showing that ansätze shallow enough to avoid plateaus are often also classically "
    "simulable, which would remove the advantage altogether. This tension is unresolved and is the "
    "central open question of the near-term programme." + cite('6')) + p(
    "Error mitigation faces a structurally similar wall. Zero-noise extrapolation and probabilistic "
    "error cancellation both reduce bias at the cost of variance, and the sampling overhead grows "
    "exponentially in the circuit volume times the error rate" + cite('10') + ". Mitigation is "
    "therefore a way to extract useful expectation values from circuits that are <em>almost</em> "
    "within reach, not a path to scaling. The distinction from Chapter 9 is sharp: correction "
    "restores the state and composes; mitigation repairs a number after the fact and does not."
) + sources(
    'Barren plateaus: McClean et al.' + cite('9') + '; error mitigation and its overheads: '
    'Cai et al.' + cite('10') + '; the NISQ framing: Preskill' + cite('6') + '.')

S5 = S5 + sources(
    'Library documentation for the optional code above' + cite('11') + '. The endianness warning '
    'applies whenever comparing against the NumPy conventions used throughout this course.')

REFS = [
    dict(authors="E. Bernstein and U. Vazirani", title="Quantum complexity theory",
         venue="SIAM Journal on Computing 26(5), 1411–1473", year="1997",
         note="Defines BQP and proves BQP ⊆ PSPACE."),
    dict(authors="A. Yu. Kitaev, A. H. Shen and M. N. Vyalyi",
         title="Classical and Quantum Computation",
         venue="AMS Graduate Studies in Mathematics 47", year="2002",
         note="QMA and the local Hamiltonian problem."),
    dict(authors="J. Kempe, A. Kitaev and O. Regev",
         title="The complexity of the local Hamiltonian problem",
         venue="SIAM Journal on Computing 35(5), 1070–1097", year="2006",
         link="https://arxiv.org/abs/quant-ph/0406180",
         note="2-local Hamiltonian is QMA-complete."),
    dict(authors="S. Aaronson and A. Arkhipov", title="The computational complexity of linear optics",
         venue="Proc. 43rd STOC, 333–342", year="2011",
         link="https://arxiv.org/abs/1011.3245",
         note="BosonSampling and the sampling-advantage framework of §2."),
    dict(authors="F. Arute et al.",
         title="Quantum supremacy using a programmable superconducting processor",
         venue="Nature 574, 505–510", year="2019",
         link="https://arxiv.org/abs/1910.11333",
         note="Random circuit sampling; read alongside the subsequent classical-simulation rebuttals."),
    dict(authors="J. Preskill", title="Quantum computing in the NISQ era and beyond",
         venue="Quantum 2, 79", year="2018",
         link="https://arxiv.org/abs/1801.00862",
         note="The paper that named the era; the framing of §3."),
    dict(authors="A. Peruzzo, J. McClean, P. Shadbolt, M.-H. Yung, X.-Q. Zhou, P. J. Love, "
                 "A. Aspuru-Guzik and J. L. O'Brien",
         title="A variational eigenvalue solver on a photonic quantum processor",
         venue="Nature Communications 5, 4213", year="2014",
         link="https://arxiv.org/abs/1304.3061",
         note="The original VQE."),
    dict(authors="E. Farhi, J. Goldstone and S. Gutmann",
         title="A Quantum Approximate Optimization Algorithm",
         venue="arXiv:1411.4028", year="2014",
         link="https://arxiv.org/abs/1411.4028",
         note="QAOA."),
    dict(authors="J. R. McClean, S. Boixo, V. N. Smelyanskiy, R. Babbush and H. Neven",
         title="Barren plateaus in quantum neural network training landscapes",
         venue="Nature Communications 9, 4812", year="2018",
         link="https://arxiv.org/abs/1803.11173",
         note="The trainability obstruction of §4."),
    dict(authors="Z. Cai, R. Babbush, S. C. Benjamin, S. Endo, W. J. Huggins, Y. Li, "
                 "J. R. McClean and T. E. O'Brien",
         title="Quantum error mitigation", venue="Reviews of Modern Physics 95, 045005", year="2023",
         link="https://arxiv.org/abs/2210.00921",
         note="Comprehensive survey of mitigation methods and their sampling overheads."),
    dict(authors="Qiskit contributors", title="Qiskit documentation",
         venue="IBM Quantum", year="2025",
         link="https://quantum.cloud.ibm.com/docs",
         note="Reference for the optional code in §5; check the migration notes for API changes."),
]

CR = [
    dict(
        name='C10.Q1 — Pauli-sum Hamiltonians and expectation values',
        qtext=cr_qtext('C10.Q1', 'The input format of every variational algorithm',
                       "A Hamiltonian is given as a list of (Pauli string, coefficient) pairs. "
                       "Its expectation value on a state is the weighted sum of the individual "
                       "Pauli expectations — exactly what a device measures.",
                       "Write <code>pauli_string(s)</code> building the matrix of a string over "
                       "<code>{'I','X','Y','Z'}</code>; <code>hamiltonian(terms)</code> summing "
                       "the weighted terms; <code>expectation(psi, H)</code> returning "
                       "\\(\\langle\\psi|H|\\psi\\rangle\\) as a real float rounded to 6 decimals; "
                       "and <code>ground_energy(H)</code> returning the smallest eigenvalue, "
                       "rounded to 6 decimals.",
                       "hamiltonian([('ZZ',1.0)]) -> diag(1,-1,-1,1)\n"
                       "ground_energy(hamiltonian([('ZZ',1.0),('XI',0.5),('IX',0.5)])) -> -1.414214"),
        answer='''import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}

def pauli_string(s):
    out = np.array([[1.0 + 0j]])
    for ch in s:
        out = np.kron(out, PAULI[ch])
    return out

def hamiltonian(terms):
    n = len(terms[0][0])
    H = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for s, c in terms:
        H = H + c * pauli_string(s)
    return H

def expectation(psi, H):
    psi = np.asarray(psi, dtype=complex).ravel()
    psi = psi / np.linalg.norm(psi)
    return round(float(np.real(np.vdot(psi, np.asarray(H, dtype=complex) @ psi))), 6)

def ground_energy(H):
    H = np.asarray(H, dtype=complex)
    return round(float(np.linalg.eigvalsh((H + H.conj().T) / 2)[0]), 6)
''',
        preload='''import numpy as np

def pauli_string(s):
    ...

def hamiltonian(terms):
    ...

def expectation(psi, H):
    ...

def ground_energy(H):
    ...
''',
        tests=[
            {'code': "import numpy as np\nprint(np.round(np.diag(hamiltonian([('ZZ',1.0)])).real, 6).tolist())\n",
             'expected': '[1.0, -1.0, -1.0, 1.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': "import numpy as np\n"
                     "H = hamiltonian([('ZZ',1.0),('XI',0.5),('IX',0.5)])\nprint(ground_energy(H))\n",
             'expected': '-1.414214\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': "import numpy as np\nH = hamiltonian([('ZZ',1.0)])\n"
                     "psi = np.array([0,1,0,0], dtype=complex)\nprint(expectation(psi, H))\n",
             'expected': '-1.0\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': "import numpy as np\nprint(np.allclose(pauli_string('XY'), "
                     "np.kron(np.array([[0,1],[1,0]]), np.array([[0,-1j],[1j,0]]))))\n",
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': "import numpy as np\n"
                     "H = hamiltonian([('XX',1.0),('YY',1.0),('ZZ',1.0)])\nprint(ground_energy(H))\n",
             'expected': '-3.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C10.Q2 — VQE with the parameter-shift rule',
        qtext=cr_qtext('C10.Q2', 'A complete variational loop',
                       "For \\(U(\\theta)=e^{-i\\theta P/2}\\) with \\(P^{2}=I\\), "
                       "\\(\\partial_\\theta\\langle A\\rangle=\\tfrac12[\\langle A\\rangle_{\\theta+\\pi/2}"
                       "-\\langle A\\rangle_{\\theta-\\pi/2}]\\) exactly.",
                       "Take the single-qubit ansatz \\(|\\psi(\\theta)\\rangle=R_y(\\theta)|0\\rangle\\) "
                       "with \\(R_y(\\theta)=\\begin{pmatrix}\\cos\\frac\\theta2&-\\sin\\frac\\theta2\\\\"
                       "\\sin\\frac\\theta2&\\cos\\frac\\theta2\\end{pmatrix}\\). "
                       "Write <code>energy(theta, H)</code>; "
                       "<code>grad_parameter_shift(theta, H)</code> using the exact rule; and "
                       "<code>vqe(H, theta0, lr=0.3, steps=300)</code> returning "
                       "<code>(theta_final, energy_final)</code> with the energy rounded to 6 "
                       "decimals, by plain gradient descent.",
                       "H = Z:   ground energy -1 at theta = 0\n"
                       "H = X:   ground energy -1 at theta = -pi/2 (mod 2pi)"),
        answer='''import numpy as np

def _ry(theta):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)

def _state(theta):
    return _ry(theta) @ np.array([1, 0], dtype=complex)

def energy(theta, H):
    psi = _state(theta)
    return round(float(np.real(np.vdot(psi, np.asarray(H, dtype=complex) @ psi))), 6)

def _raw_energy(theta, H):
    psi = _state(theta)
    return float(np.real(np.vdot(psi, np.asarray(H, dtype=complex) @ psi)))

def grad_parameter_shift(theta, H):
    return round(0.5 * (_raw_energy(theta + np.pi / 2, H)
                        - _raw_energy(theta - np.pi / 2, H)), 6)

def vqe(H, theta0, lr=0.3, steps=300):
    th = float(theta0)
    for _ in range(steps):
        g = 0.5 * (_raw_energy(th + np.pi / 2, H) - _raw_energy(th - np.pi / 2, H))
        th = th - lr * g
    return (th, energy(th, H))
''',
        preload='''import numpy as np

def energy(theta, H):
    ...

def grad_parameter_shift(theta, H):
    ...

def vqe(H, theta0, lr=0.3, steps=300):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'print(energy(0.0, Z), energy(np.pi, Z))\n',
             'expected': '1.0 -1.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'print(grad_parameter_shift(np.pi/2, Z))\n',
             'expected': '-1.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'print(vqe(Z, 0.3)[1])\n',
             'expected': '-1.0\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nX = np.array([[0,1],[1,0]], dtype=complex)\n'
                     'print(vqe(X, 0.7)[1])\n',
             'expected': '-1.0\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': '''import numpy as np
Z = np.array([[1,0],[0,-1]], dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
H = 0.6*Z + 0.8*X
print(vqe(H, 0.1)[1], round(float(np.linalg.eigvalsh(H)[0]), 6))
''',
             'expected': '-1.0 -1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C10.Q3 — QAOA for MaxCut at depth p = 1',
        qtext=cr_qtext('C10.Q3', 'Combinatorial optimisation, variationally',
                       "MaxCut on a graph \\(G=(V,E)\\) maximises "
                       "\\(C=\\sum_{(i,j)\\in E}\\tfrac12(1-z_iz_j)\\). Encode it as "
                       "\\(H_C=\\sum_{(i,j)\\in E}\\tfrac12(I-Z_iZ_j)\\), and use the mixer "
                       "\\(H_M=\\sum_i X_i\\).",
                       "Write <code>maxcut_hamiltonian(n, edges)</code>; "
                       "<code>qaoa_state(n, edges, gamma, beta)</code> returning "
                       "\\(e^{-i\\beta H_M}e^{-i\\gamma H_C}|+\\rangle^{\\otimes n}\\); "
                       "<code>qaoa_expectation(n, edges, gamma, beta)</code> rounded to 6 "
                       "decimals; and <code>best_cut(n, edges)</code> returning the exact optimum "
                       "by brute force over the \\(2^{n}\\) assignments.",
                       "triangle graph: best_cut = 2\n"
                       "square graph:   best_cut = 4"),
        answer='''import numpy as np
from itertools import product

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def _embed(U, q, n):
    ops = [I2] * n
    ops[q] = U
    out = np.array([[1.0 + 0j]])
    for o in ops:
        out = np.kron(out, o)
    return out

def maxcut_hamiltonian(n, edges):
    H = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for i, j in edges:
        H = H + 0.5 * (np.eye(2 ** n, dtype=complex) - _embed(Z, i, n) @ _embed(Z, j, n))
    return H

def _expm_diag(H, t):
    w, v = np.linalg.eigh((H + H.conj().T) / 2)
    return (v * np.exp(-1j * t * w)) @ v.conj().T

def qaoa_state(n, edges, gamma, beta):
    HC = maxcut_hamiltonian(n, edges)
    HM = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for i in range(n):
        HM = HM + _embed(X, i, n)
    psi = np.full(2 ** n, 1 / np.sqrt(2 ** n), dtype=complex)
    psi = _expm_diag(HC, gamma) @ psi
    psi = _expm_diag(HM, beta) @ psi
    return psi

def qaoa_expectation(n, edges, gamma, beta):
    psi = qaoa_state(n, edges, gamma, beta)
    HC = maxcut_hamiltonian(n, edges)
    return round(float(np.real(np.vdot(psi, HC @ psi))), 6)

def best_cut(n, edges):
    best = 0
    for bits in product([0, 1], repeat=n):
        cut = sum(1 for i, j in edges if bits[i] != bits[j])
        best = max(best, cut)
    return best
''',
        preload='''import numpy as np
from itertools import product

def maxcut_hamiltonian(n, edges):
    ...

def qaoa_state(n, edges, gamma, beta):
    ...

def qaoa_expectation(n, edges, gamma, beta):
    ...

def best_cut(n, edges):
    ...
''',
        tests=[
            {'code': 'print(best_cut(3, [(0,1),(1,2),(0,2)]), best_cut(4, [(0,1),(1,2),(2,3),(3,0)]))\n',
             'expected': '2 4\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(np.round(np.diag(maxcut_hamiltonian(2, [(0,1)])).real, 6).tolist())\n',
             'expected': '[0.0, 1.0, 1.0, 0.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(qaoa_expectation(2, [(0,1)], 0.0, 0.0))\n',
             'expected': '0.5\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
n, edges = 2, [(0,1)]
best = max(qaoa_expectation(n, edges, g, b)
           for g in np.linspace(0, np.pi, 21) for b in np.linspace(0, np.pi, 21))
print(round(best, 4))
''',
             'expected': '0.9755\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': '''import numpy as np
n, edges = 3, [(0,1),(1,2),(0,2)]
psi = qaoa_state(n, edges, 0.7, 0.4)
print(round(float(np.vdot(psi, psi).real), 6))
''',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C10.Q4 — Zero-noise extrapolation and shot budgets',
        qtext=cr_qtext('C10.Q4', 'Error mitigation, and what it costs',
                       "Zero-noise extrapolation measures an observable at several amplified "
                       "noise levels \\(\\lambda_k\\) and extrapolates to \\(\\lambda=0\\). Richardson "
                       "extrapolation is polynomial interpolation evaluated at zero.",
                       "Write <code>richardson(lams, vals)</code> returning the value at "
                       "\\(\\lambda=0\\) of the interpolating polynomial through the given points "
                       "(use the Lagrange formula, no <code>numpy.polyfit</code> required but "
                       "allowed), rounded to 6 decimals; and "
                       "<code>shots_needed(variance, eps)</code> returning "
                       "\\(\\lceil \\mathrm{Var}/\\varepsilon^{2}\\rceil\\) as an <code>int</code> — "
                       "the sampling cost of estimating an expectation value to additive error "
                       "\\(\\varepsilon\\).",
                       "richardson([1,2,3], [0.9, 0.8, 0.7]) -> 1.0\n"
                       "shots_needed(1.0, 1e-3) -> 1000000"),
        answer='''import numpy as np
from math import ceil

def richardson(lams, vals):
    lams = [float(x) for x in lams]
    vals = [float(v) for v in vals]
    total = 0.0
    for i, (li, vi) in enumerate(zip(lams, vals)):
        term = vi
        for j, lj in enumerate(lams):
            if i != j:
                term *= (0.0 - lj) / (li - lj)
        total += term
    return round(total, 6)

def shots_needed(variance, eps):
    return int(ceil(float(variance) / float(eps) ** 2))
''',
        preload='''import numpy as np
from math import ceil

def richardson(lams, vals):
    ...

def shots_needed(variance, eps):
    ...
''',
        tests=[
            {'code': 'print(richardson([1,2,3], [0.9, 0.8, 0.7]))\n',
             'expected': '1.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(shots_needed(1.0, 1e-3))\n',
             'expected': '1000000\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(richardson([1,3], [0.8, 0.4]))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\n'
                     'lams = [1.0, 1.5, 2.0]\n'
                     'vals = [1 - 0.1*l + 0.02*l**2 for l in lams]\n'
                     'print(richardson(lams, vals))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(shots_needed(0.25, 0.01), shots_needed(1.0, 1.6e-3))\n',
             'expected': '2500 390625\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

ST = [
    stack_question(
        name='C10.S1 — The complexity landscape',
        questiontext=stack_qtext(
            'C10.S1', 'Counting and classifying',
            r'<p>(a) A general \(n\)-qubit Hamiltonian is expanded in the Pauli basis. Give the '
            r'number of terms, in terms of <code>n</code>.</p>'
            r'<p>[[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Evaluate that for \(n={@n@}\).</p>'
            r'<p>[[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) A BQP algorithm has success probability \(2/3\). By the Chernoff bound, the '
            r'number of repetitions needed for failure probability \(\delta\) scales as '
            r'\(c\cdot\log(1/\delta)\). Give the exponent \(\alpha\) in "repetitions '
            r'\(=\Theta(\log^{\alpha}(1/\delta))\)".</p>'
            r'<p>\(\alpha=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) The Pauli strings \(\sigma_{\mu_1}\otimes\cdots\otimes\sigma_{\mu_n}\) with '
            r'\(\mu_i\in\{I,X,Y,Z\}\) number \(4^{n}\), and they form an orthogonal basis of the '
            r'\(4^{n}\)-dimensional real space of Hermitian operators.</p>'
            r'<p>(b) For \(n={@n@}\): \({@ta2@}\).</p>'
            r'<p>(c) \(\alpha=1\): majority voting over \(O(\log(1/\delta))\) runs suffices, so the '
            r'constant \(2/3\) in the definition of BQP is arbitrary. Physically relevant '
            r'Hamiltonians are \(k\)-local with only \(O(n^{k})\) terms — the exponential count '
            r'above is why <em>arbitrary</em> Hamiltonians are hopeless and structure is '
            r'everything.</p>'),
        questionvariables='n : rand_with_step(3,8,1);\nta1 : 4^n;\nta2 : 4^n;\nta3 : 1;',
        questionnote='n={@n@}, 4^n={@ta2@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>Four choices per qubit.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=12, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>Substitute the given \\(n\\).</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=6, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb='<p>Chernoff gives exponential decay in the number of repetitions.</p>')]),
    stack_question(
        name='C10.S2 — The parameter-shift rule',
        questiontext=stack_qtext(
            'C10.S2', 'Exact gradients from shifted circuits',
            r'<p>Let \(U(\theta)=e^{-i\theta P/2}\) with \(P^{2}=I\), and let '
            r'\(f(\theta)=\langle 0|U^{\dagger}(\theta)\,A\,U(\theta)|0\rangle\).</p>'
            r'<p>(a) Write \(U(\theta)\) in the form \(\alpha(\theta)I-i\beta(\theta)P\) and give '
            r'\(\alpha(\theta)\).</p>'
            r'<p>\(\alpha(\theta)=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) The parameter-shift rule reads \(f\'(\theta)=r\,[f(\theta+s)-f(\theta-s)]\). '
            r'Give the ordered pair <code>[r, s]</code>.</p>'
            r'<p>[[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) \(f\) is a trigonometric polynomial in \(\theta\). Give its period.</p>'
            r'<p>[[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) Since \(P^2=I\), splitting the exponential series gives '
            r'\(U(\theta)=\cos(\theta/2)I-i\sin(\theta/2)P\), so \(\alpha=\cos(\theta/2)\) — the '
            r'same identity as in Chapter 1.</p>'
            r'<p>(b) Expanding, \(f(\theta)=a+b\cos\theta+c\sin\theta\). Then '
            r'\(f(\theta+\pi/2)-f(\theta-\pi/2)=-2b\sin\theta+2c\cos\theta=2f\'(\theta)\), so '
            r'\(r=1/2\) and \(s=\pi/2\).</p>'
            r'<p>(c) \(2\pi\), from the same expansion.</p>'
            r'<p>Note the rule is <em>exact</em>, not a finite-difference approximation: it '
            r'evaluates the same circuit at two shifted parameter values, so it adds no depth and '
            r'introduces no discretisation bias — only shot noise.</p>'),
        questionvariables='ta1 : cos(theta/2);\nta2 : [1/2, %pi/2];\nta3 : 2*%pi;',
        questionnote='cos(theta/2), [1/2, pi/2], 2pi',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=16, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Split \(e^{-i\theta P/2}\) into even and odd powers using \(P^{2}=I\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=18, value='0.3333333',
                 forbidfloat=0,
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Write \(f(\theta)=a+b\cos\theta+c\sin\theta\) and evaluate the shifts.</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>\(f\) contains only \(\cos\theta\) and \(\sin\theta\).</p>')]),
    stack_question(
        name='C10.S3 — Shot budgets and barren plateaus',
        questiontext=stack_qtext(
            'C10.S3', 'Why NISQ is hard, quantitatively',
            r'<p>(a) Estimating \(\langle A\rangle\) with \(A^{2}=I\) to additive error '
            r'\(\varepsilon\) requires how many shots, at leading order in <code>eps</code>? '
            r'(Use variance \(\le 1\).)</p>'
            r'<p>[[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) A chemistry Hamiltonian has \(M\) Pauli terms measured independently, each to '
            r'error \(\varepsilon/\sqrt M\). Give the total shot count in terms of <code>M</code> '
            r'and <code>eps</code>.</p>'
            r'<p>[[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) In a barren plateau the gradient variance scales as \(2^{-n}\). Give the '
            r'number of shots needed to resolve the gradient sign, in terms of <code>n</code> '
            r'(leading order).</p>'
            r'<p>[[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) The sample mean of a bounded random variable has standard error '
            r'\(\sigma/\sqrt N\), so \(N=\Theta(1/\varepsilon^{2})\).</p>'
            r'<p>(b) Each of the \(M\) terms needs \(M/\varepsilon^{2}\) shots, for a total of '
            r'\(M^{2}/\varepsilon^{2}\). With \(M=O(n^{4})\) spin-orbital terms and chemical '
            r'accuracy \(\varepsilon=1.6\times10^{-3}\) Ha, this reaches \(10^{9}\)–\(10^{12}\) '
            r'shots for molecules of interest — the arithmetic behind most scepticism about '
            r'near-term VQE. Grouping commuting terms into cliques reduces \(M\), but not '
            r'the asymptotic form.</p>'
            r'<p>(c) Resolving a quantity of size \(2^{-n/2}\) needs \(N\sim2^{n}\) shots: gradient '
            r'estimation becomes exponentially expensive, which is exactly the barren-plateau '
            r'obstruction. Note that this is a statement about <em>trainability</em>, independent of '
            r'whether the ansatz could in principle represent the ground state.</p>'),
        questionvariables='ta1 : 1/eps^2;\nta2 : M^2/eps^2;\nta3 : 2^n;',
        questionnote='1/eps^2, M^2/eps^2, 2^n',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=12, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb=r'<p>Standard error is \(\sigma/\sqrt N\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=14, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Each term needs \((\sqrt M/\varepsilon)^{2}\) shots, and there are \(M\) of them.</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Signal \(\sim2^{-n/2}\), noise \(\sim1/\sqrt N\).</p>')]),
]

CHAPTER = dict(
    no=10, slug='complexity-nisq-and-qiskit',
    title='Quantum Complexity, NISQ Algorithms and Qiskit in Practice',
    subtitle='BQP and QMA, sampling advantage and how to read an advantage claim, VQE and QAOA, '
             'the parameter-shift rule, barren plateaus, error mitigation, and the optional '
             'Qiskit implementation of everything above.',
    prereq='Chapters 1–9. Chapter 5 (channels) and Chapter 9 (fault tolerance) are assumed in §4.',
    objectives=[
        'Place BQP among the classical classes and explain why no unconditional separation is known.',
        'State the local Hamiltonian problem and its QMA-completeness, and its consequence for VQE.',
        'Critically assess a quantum-advantage sampling claim on hardness, fidelity and baseline.',
        'Implement VQE with exact parameter-shift gradients and QAOA for MaxCut.',
        'Explain barren plateaus and compute the resulting shot budgets.',
        'Distinguish error mitigation from error correction and quantify the sampling overhead.',
        'Reproduce the course constructions in Qiskit, minding the endianness convention.',
    ],
    sections=[
        ('BQP, QMA and the complexity landscape', S1),
        ('Sampling advantage and how to read a claim', S2),
        ('The NISQ regime: VQE and QAOA', S3),
        ('Barren plateaus and error mitigation', S4),
        ('Optional: the same constructions in Qiskit', S5),
        ('Numerical practice', S6),
    ],
    summary="BQP sits between BPP and PSPACE with no known unconditional separation; QMA-complete "
            "local Hamiltonians rule out generic ground-state algorithms. In the NISQ regime, "
            "variational methods (VQE, QAOA) trade depth for a classical outer loop and exact "
            "parameter-shift gradients, but face barren plateaus, prohibitive shot budgets and no "
            "proven speed-up. Error mitigation buys accuracy at exponential sampling cost and is "
            "not a substitute for the error correction of Chapter 9 — which remains the credible "
            "route to useful quantum advantage.",
    references=REFS, coderunner=CR, stack=ST,
)
