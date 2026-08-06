# -*- coding: utf-8 -*-
"""Chapter 2 — Qubits, the Bloch Sphere and Quantum Measurement."""
from math import sin, cos, pi, sqrt, acos
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, bloch_svg,
                    flow_svg, circuit_svg, C, SERIF, MONO)

S1 = (
    p("A qubit is a two-level quantum system: \\(\\mathcal H=\\mathbb C^{2}\\) with a "
      "distinguished orthonormal basis \\(\\{|0\\rangle,|1\\rangle\\}\\). A general pure state is "
      "\\(|\\psi\\rangle=\\alpha|0\\rangle+\\beta|1\\rangle\\) with \\(|\\alpha|^2+|\\beta|^2=1\\). "
      "Four real parameters, minus one for normalisation and one for the unobservable global "
      "phase, leave two — hence the sphere.")
    + eq(r"|\psi\rangle \;=\; \cos\tfrac{\theta}{2}\,|0\rangle \;+\; e^{i\varphi}\sin\tfrac{\theta}{2}\,|1\rangle,"
         r"\qquad \theta\in[0,\pi],\;\varphi\in[0,2\pi)")
    + box('def', 'Bloch vector',
          "For a pure qubit state the Bloch vector is "
          "\\(\\vec r=(\\langle X\\rangle,\\langle Y\\rangle,\\langle Z\\rangle)\\) with "
          "\\(\\langle A\\rangle=\\langle\\psi|A|\\psi\\rangle\\). In the parametrisation above "
          "\\(\\vec r=(\\sin\\theta\\cos\\varphi,\\ \\sin\\theta\\sin\\varphi,\\ \\cos\\theta)\\), a unit "
          "vector. Chapter 5 extends the map to mixed states, where \\(\\|\\vec r\\|\\le1\\) and the "
          "interior of the ball is populated.")
    + p("Landmarks worth memorising: \\(|0\\rangle\\) and \\(|1\\rangle\\) sit at the poles; "
        "\\(|\\pm\\rangle=(|0\\rangle\\pm|1\\rangle)/\\sqrt2\\) on the \\(\\pm x\\) axis; "
        "\\(|\\pm i\\rangle=(|0\\rangle\\pm i|1\\rangle)/\\sqrt2\\) on the \\(\\pm y\\) axis.")
    + box('warn', 'A common misconception',
          "Orthogonal states are <em>antipodal</em> on the Bloch sphere, not perpendicular. "
          "The map is two-to-one on angles: the angle between Bloch vectors is twice the "
          "Hilbert-space angle. Concretely \\(|\\langle\\psi|\\phi\\rangle|^{2}="
          "\\tfrac12(1+\\vec r_\\psi\\cdot\\vec r_\\phi)\\).")
)

S2 = (
    p("Chapter 1 established that any \\(U\\in SU(2)\\) is "
      "\\(R_{\\hat n}(\\theta)=e^{-i\\theta(\\hat n\\cdot\\vec\\sigma)/2}"
      "=\\cos\\tfrac\\theta2 I - i\\sin\\tfrac\\theta2(\\hat n\\cdot\\vec\\sigma)\\). Its action on the "
      "Bloch sphere is exactly a rotation of \\(\\vec r\\) by angle \\(\\theta\\) about the axis "
      "\\(\\hat n\\), which is the content of the two-to-one covering "
      "\\(SU(2)\\to SO(3)\\).")
    + box('thm', 'Adjoint action',
          "For any unit \\(\\hat n\\) and any qubit state, "
          "\\(R_{\\hat n}(\\theta)\\,(\\vec r\\cdot\\vec\\sigma)\\,R_{\\hat n}(\\theta)^{\\dagger}"
          "=(\\mathcal R_{\\hat n}(\\theta)\\vec r)\\cdot\\vec\\sigma\\), where "
          "\\(\\mathcal R_{\\hat n}(\\theta)\\in SO(3)\\) is the Rodrigues rotation matrix. "
          "Hence single-qubit gates are rigid rotations of the Bloch ball, and in particular "
          "cannot change \\(\\|\\vec r\\|\\) — they cannot create or destroy mixedness.")
    + table(['Gate', 'Matrix', 'Bloch action'],
            [['\\(X\\)', r'\(\begin{pmatrix}0&1\\1&0\end{pmatrix}\)', '\\(\\pi\\) about \\(x\\)'],
             ['\\(Z\\)', r'\(\begin{pmatrix}1&0\\0&-1\end{pmatrix}\)', '\\(\\pi\\) about \\(z\\)'],
             ['\\(H\\)', r'\(\tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\)',
              '\\(\\pi\\) about \\((\\hat x+\\hat z)/\\sqrt2\\); swaps \\(x\\leftrightarrow z\\)'],
             ['\\(S=\\sqrt Z\\)', r'\(\mathrm{diag}(1,i)\)', '\\(\\pi/2\\) about \\(z\\)'],
             ['\\(T=\\sqrt S\\)', r'\(\mathrm{diag}(1,e^{i\pi/4})\)', '\\(\\pi/4\\) about \\(z\\)']])
)

S3 = (
    p("Measurement is where the linear, deterministic, reversible formalism meets irreversible "
      "classical data. The projective (von Neumann) case: given an observable "
      "\\(A=\\sum_k\\lambda_k P_k\\), outcome \\(\\lambda_k\\) occurs with probability")
    + eq(r"p(k) \;=\; \langle\psi|P_k|\psi\rangle \;=\; \|P_k|\psi\rangle\|^{2}, \qquad "
         r"|\psi\rangle \;\longmapsto\; \frac{P_k|\psi\rangle}{\sqrt{p(k)}} .")
    + p("Two consequences deserve emphasis. First, \\(\\sum_k p(k)=\\langle\\psi|I|\\psi\\rangle=1\\) "
        "automatically, by completeness. Second, the expectation value is "
        "\\(\\langle A\\rangle=\\sum_k\\lambda_k p(k)=\\langle\\psi|A|\\psi\\rangle\\) — an "
        "identity we exploit heavily in Chapter 10, where energies are estimated by averaging "
        "Pauli measurements.")
    + box('ex', 'Measuring in a rotated basis',
          "To measure \\(X\\) on a device that can only measure \\(Z\\), use \\(X=HZH\\): apply "
          "\\(H\\), measure \\(Z\\), and relabel. Generally, to measure "
          "\\(\\hat n\\cdot\\vec\\sigma\\), apply any \\(V\\) with "
          "\\(V(\\hat n\\cdot\\vec\\sigma)V^{\\dagger}=Z\\) and measure \\(Z\\). "
          "This 'basis-change-then-measure' pattern is how every real device implements "
          "non-computational-basis measurements.")
    + p("For a multi-qubit register measured in the computational basis, "
        "\\(p(x)=|\\langle x|\\psi\\rangle|^{2}\\) for \\(x\\in\\{0,1\\}^{n}\\). Sampling from this "
        "distribution — not reading out amplitudes — is all a quantum computer ever outputs. "
        "Algorithm design is therefore the art of arranging interference so that the useful "
        "\\(x\\) carries most of the weight.")
)

S4 = (
    p("Non-commuting observables cannot be sharply defined simultaneously. With "
      "\\(\\Delta A^{2}=\\langle A^{2}\\rangle-\\langle A\\rangle^{2}\\), the Robertson relation reads")
    + eq(r"\Delta A\,\Delta B \;\ge\; \tfrac12\big|\langle [A,B]\rangle\big| .")
    + box('proof', '',
          "Set \\(\\tilde A=A-\\langle A\\rangle\\), \\(\\tilde B=B-\\langle B\\rangle\\). Cauchy–Schwarz "
          "gives \\(\\Delta A^2\\Delta B^2\\ge|\\langle\\tilde A\\tilde B\\rangle|^{2}\\). Split "
          "\\(\\tilde A\\tilde B=\\tfrac12[\\tilde A,\\tilde B]+\\tfrac12\\{\\tilde A,\\tilde B\\}\\) into "
          "anti-Hermitian and Hermitian parts, whose expectations are respectively purely "
          "imaginary and real; keep the imaginary part. \\(\\blacksquare\\)")
    + p("For a qubit, \\([X,Y]=2iZ\\) gives \\(\\Delta X\\,\\Delta Y\\ge|\\langle Z\\rangle|\\). "
        "On \\(|0\\rangle\\) the right-hand side equals 1, and indeed "
        "\\(\\Delta X=\\Delta Y=1\\): the bound is tight.")
)

S5 = (
    p("Projective measurement is not the most general thing one can do. A "
      "<strong>POVM</strong> is a set \\(\\{E_k\\}\\) of positive operators with "
      "\\(\\sum_k E_k = I\\); outcome \\(k\\) has probability "
      "\\(p(k)=\\langle\\psi|E_k|\\psi\\rangle\\). Naimark's dilation theorem says every POVM is a "
      "projective measurement on a larger space — attach an ancilla, evolve unitarily, measure "
      "projectively. POVMs are therefore not new physics, but they are the right bookkeeping "
      "for measurements on subsystems.")
    + box('thm', 'Helstrom bound',
          "Given one of two known pure states \\(|\\psi_0\\rangle,|\\psi_1\\rangle\\) with equal prior, "
          "the maximal probability of correctly identifying which was prepared is "
          "\\(p_{\\text{succ}}=\\tfrac12\\big(1+\\sqrt{1-|\\langle\\psi_0|\\psi_1\\rangle|^{2}}\\big)\\), "
          "attained by projecting onto the eigenvectors of "
          "\\(\\tfrac12(|\\psi_0\\rangle\\langle\\psi_0|-|\\psi_1\\rangle\\langle\\psi_1|)\\). "
          "Non-orthogonal states are never perfectly distinguishable.")
    + p("This impossibility is not a technological limitation; it is the security argument of "
        "BB84 quantum key distribution and, in the form below, the reason quantum information "
        "cannot be copied.")
    + box('thm', 'No-cloning (Wootters–Zurek, Dieks 1982)',
          "There is no unitary \\(U\\) and fixed state \\(|s\\rangle\\) with "
          "\\(U(|\\psi\\rangle\\otimes|s\\rangle)=|\\psi\\rangle\\otimes|\\psi\\rangle\\) for all "
          "\\(|\\psi\\rangle\\). Proof: apply it to \\(|\\psi\\rangle\\) and \\(|\\phi\\rangle\\) and take "
          "inner products: unitarity forces "
          "\\(\\langle\\psi|\\phi\\rangle=\\langle\\psi|\\phi\\rangle^{2}\\), so "
          "\\(\\langle\\psi|\\phi\\rangle\\in\\{0,1\\}\\). Cloning works only on a set of mutually "
          "orthogonal states — i.e. on classical information. \\(\\blacksquare\\)")
    + p("The same linearity argument yields <em>no-deleting</em> and, combined with the "
        "structure of Chapter 5, <em>no-signalling</em>: local operations on \\(A\\) cannot change "
        "the measurement statistics available at \\(B\\).")
)

S6 = (
    code('''import numpy as np

def bloch_vector(psi):
    """Bloch coordinates (x, y, z) of a normalised qubit state vector."""
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    psi = np.asarray(psi, dtype=complex).reshape(2)
    return tuple(float(np.real(psi.conj() @ (S @ psi))) for S in (X, Y, Z))

def sample(psi, shots=1000, seed=0):
    """Sample computational-basis outcomes of an n-qubit state."""
    psi = np.asarray(psi, dtype=complex).ravel()
    probs = np.abs(psi) ** 2
    probs = probs / probs.sum()
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(probs), size=shots, p=probs)
    n = int(np.log2(len(probs)))
    counts = {}
    for i in idx:
        key = format(int(i), '0%db' % n)
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))

plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
print(bloch_vector(plus))          # (1.0, 0.0, 0.0)
print(sample(plus, shots=8, seed=3))''',
         'Bloch coordinates and outcome sampling — the two primitives used in the exercises')
    + p("Note the discipline: probabilities are renormalised before sampling (floating-point "
        "sums rarely equal 1 exactly), and the random generator is seeded so that grading is "
        "reproducible. Real hardware offers no such determinism; shot noise scales as "
        "\\(1/\\sqrt{N}\\), which is why estimating an expectation value to precision "
        "\\(\\varepsilon\\) costs \\(\\Theta(1/\\varepsilon^{2})\\) shots — a bottleneck we revisit "
        "for variational algorithms.")
)

# =============================== figures, citations and added commentary =====
BLOCH_LANDMARKS = bloch_svg(
    [(0, 0, '|0⟩', '#026573'),
     (180, 0, '|1⟩', '#026573'),
     (90, 0, '|+⟩', '#c9a227'),
     (90, 90, '|+i⟩', '#9333ea'),
     (55, 40, 'ψ(θ,φ)', '#dc2626')],
    title='The Bloch sphere: every pure qubit state is a point on the surface')

BLOCH_ROT = bloch_svg(
    [(55, 0, 'ψ  before', '#94a3b8'),
     (55, 90, 'R_z(π/2) ψ', '#026573'),
     (125, 0, 'X ψ', '#dc2626')],
    title='Single-qubit gates are rigid rotations of the sphere')

_ths = [k * pi / 180 for k in range(0, 181, 3)]
BORN = line_chart(
    [dict(label='Pr[Z = +1] = cos²(θ/2)', xs=[t * 180 / pi for t in _ths],
          ys=[cos(t / 2) ** 2 for t in _ths], color='#026573'),
     dict(label='Pr[X = +1] = (1 + sin θ)/2, at φ = 0', xs=[t * 180 / pi for t in _ths],
          ys=[(1 + sin(t)) / 2 for t in _ths], color='#c9a227'),
     dict(label='Pr[Y = +1] = 1/2, at φ = 0', xs=[t * 180 / pi for t in _ths],
          ys=[0.5 for t in _ths], color='#9333ea', dash='6 4')],
    xlim=(0, 180), ylim=(0, 1), xlabel='polar angle θ  (degrees)',
    ylabel='outcome probability',
    vlines=[(90, 'equator', '#475569')], height=330)

UNC = line_chart(
    [dict(label='ΔX · ΔY  (attained)', xs=[t * 180 / pi for t in _ths],
          ys=[abs(cos(t)) for t in _ths], color='#026573'),
     dict(label='bound ½|⟨[X,Y]⟩| = |⟨Z⟩|', xs=[t * 180 / pi for t in _ths],
          ys=[abs(cos(t)) for t in _ths], color='#dc2626', dash='7 4'),
     dict(label='ΔX · ΔZ  (attained)', xs=[t * 180 / pi for t in _ths],
          ys=[abs(sin(t) * cos(t)) for t in _ths], color='#c9a227'),
     dict(label='bound |⟨Y⟩| = 0 for φ = 0', xs=[t * 180 / pi for t in _ths],
          ys=[0.0 for t in _ths], color='#9333ea', dash='4 4')],
    xlim=(0, 180), ylim=(0, 1.05), xlabel='polar angle θ  (degrees)',
    ylabel='uncertainty product', height=330)

_ovs = [k / 100 for k in range(0, 101)]
HELSTROM = line_chart(
    [dict(label='optimal success  ½(1 + √(1 − |⟨ψ|φ⟩|²))', xs=_ovs,
          ys=[0.5 * (1 + sqrt(max(0.0, 1 - o ** 2))) for o in _ovs], color='#026573'),
     dict(label='guessing without measuring', xs=_ovs, ys=[0.5 for _ in _ovs],
          color='#94a3b8', dash='5 4')],
    xlim=(0, 1), ylim=(0.4, 1.05), xlabel='overlap  |⟨ψ|φ⟩|',
    ylabel='probability of correct identification',
    vlines=[(1 / sqrt(2), '|+⟩ vs |0⟩', '#c9a227')],
    hlines=[(1.0, 'perfect discrimination', '#dc2626')], height=330)

BASIS_CHANGE = circuit_svg(
    1,
    [[('g', 0, 'V')], [('m', 0)]],
    wire_labels=['|ψ⟩'], width=470, height=118,
    title='Measuring an arbitrary axis on a device that only reads out Z')

S1 = S1 + figure(
    '2.1',
    'The Bloch sphere. The two angles (θ, φ) of the standard parametrisation place every pure qubit '
    'state on the surface; the poles are the computational basis, the ±x points are |±⟩ and the ±y '
    'points are |±i⟩. Orthogonal states sit at antipodes, not at right angles: the angle between '
    'Bloch vectors is twice the angle in Hilbert space, which is the geometric content of the '
    'two-to-one covering SU(2) → SO(3).',
    BLOCH_LANDMARKS, height=340) + p(
    "The parameter count behind the picture deserves to be made explicit, because it is the reason "
    "the Bloch sphere has no useful analogue beyond one qubit. A vector in \\(\\mathbb C^{2}\\) has "
    "four real parameters; normalisation removes one and the unobservable global phase removes "
    "another, leaving two — the dimension of a sphere. Repeating the count for \\(n\\) qubits gives "
    "\\(2^{n+1}-2\\) real parameters, so already for two qubits the state space is a six-dimensional "
    "manifold that cannot be drawn" + cite('1') + ". Attempts to visualise multi-qubit states as "
    "several Bloch spheres are actively misleading: they represent exactly the product states, and "
    "therefore miss entanglement entirely (Chapter 4).") + sources(
    'Bloch-sphere parametrisation and its geometry: Nielsen &amp; Chuang §1.2' + cite('1') +
    '; the group-theoretic statement is standard, see Preskill ch. 2' + cite('7') + '.')

S2 = S2 + figure(
    '2.2',
    'Action of single-qubit gates. A z-rotation carries a state around a circle of constant latitude '
    '(grey → teal); the Pauli X gate is a π rotation about the x axis, which reflects the state '
    'through the equatorial plane (red). Because rotations are rigid motions, the length of the '
    'Bloch vector is preserved: no unitary can turn a pure state into a mixed one — that requires '
    'the channels of Chapter 5.',
    BLOCH_ROT, height=340) + p(
    "One consequence is worth stating precisely because it recurs in the hardware discussion of "
    "Chapter 10. On superconducting processors, \\(R_z\\) rotations are implemented not by a "
    "physical pulse but by relabelling the phase reference of all subsequent pulses — a so-called "
    "<em>virtual</em> \\(Z\\) gate, which takes zero time and introduces zero error" + cite('1') +
    ". Compilers therefore push as much of a circuit as possible into \\(z\\)-rotations, and the "
    "\\(ZYZ\\) decomposition of Chapter 3 is chosen precisely so that only one non-virtual pulse "
    "shape is needed per single-qubit gate.") + sources(
    'Rotation formula and the adjoint action: Nielsen &amp; Chuang §4.2' + cite('1') + '.')

S3 = S3 + figure(
    '2.3',
    'Born-rule probabilities as functions of the polar angle, for a state with φ = 0. The Z outcome '
    'follows cos²(θ/2), reaching certainty at the poles. The X outcome depends on θ through sin θ '
    'and is certain only at the equator with φ = 0. The Y outcome is exactly 1/2 for every θ on this '
    'meridian — a reminder that a state can be sharp for one observable while carrying no information '
    'at all about another.',
    BORN, height=330) + figure(
    '2.4',
    'Changing basis before measurement. To measure the observable n̂·σ⃗ on a device that only reads '
    'out Z, apply any unitary V with V(n̂·σ⃗)V† = Z, measure Z, and relabel the outcomes. Every '
    'non-computational-basis measurement performed on real hardware is implemented this way.',
    BASIS_CHANGE, width=470, height=118) + p(
    "Figure 2.3 also makes visible the fact that the three probability curves are affine in the "
    "Bloch coordinates: \\(\\Pr[\\hat n=+1]=\\tfrac12(1+\\hat n\\cdot\\vec r)\\)" + cite('1,6') + ". "
    "This linearity is not an accident of the qubit; it is the Born rule, and it is what forces "
    "probabilities to be quadratic in the amplitudes. Gleason's theorem sharpens the point: for "
    "\\(\\dim\\mathcal H\\ge3\\), the Born rule is the <em>only</em> probability assignment on "
    "projectors that is additive on orthogonal sets, so the quadratic form is not a postulate one "
    "is free to vary.") + sources(
    'Measurement postulate and the basis-change trick: Nielsen &amp; Chuang §2.2' + cite('1') +
    '; a careful discussion of what a measurement is: Peres ch. 2–3' + cite('6') + '.')

S4 = S4 + figure(
    '2.5',
    'The Robertson bound, tight and loose. For the meridian state cos(θ/2)|0⟩ + sin(θ/2)|1⟩ the pair '
    '(X, Y) saturates the bound at every θ — the two curves coincide — while the pair (X, Z) has a '
    'vanishing bound (⟨Y⟩ = 0 on this meridian) even though the product of uncertainties is strictly '
    'positive except at θ = 0, 90°, 180°. Robertson\'s inequality is therefore correct but can be '
    'uninformative; the Schrödinger refinement, which adds the anticommutator term, closes part of '
    'the gap.',
    UNC, height=330) + p(
    "The lesson generalises. Uncertainty relations of Robertson type bound a product of variances "
    "by an expectation value that may itself vanish on the state in question, which is why modern "
    "treatments prefer entropic uncertainty relations: for any two orthonormal bases, "
    "\\(H(\\mathcal A)+H(\\mathcal B)\\ge\\log_2(1/c)\\) with \\(c\\) the largest squared overlap "
    "between basis elements — a state-independent bound" + cite('7') + ". For \\(X\\) and \\(Z\\) "
    "on a qubit \\(c=1/2\\), so the Shannon entropies of the two outcome distributions must sum to "
    "at least one bit, no matter which state is prepared. That form is what underlies modern "
    "security proofs for quantum key distribution.") + sources(
    'Robertson\'s derivation: Nielsen &amp; Chuang §2.2.5' + cite('1') + '; entropic relations and '
    'their cryptographic use: Preskill ch. 3' + cite('7') + '.')

S5 = S5 + figure(
    '2.6',
    'The Helstrom limit on distinguishing two equally likely pure states. Only orthogonal states '
    '(overlap 0) can be told apart with certainty; identical states (overlap 1) leave nothing better '
    'than a coin flip. The marked point is the |0⟩-versus-|+⟩ case, where even an optimal measurement '
    'succeeds only 85.4% of the time. The impossibility of doing better is what makes eavesdropping '
    'detectable in quantum key distribution, and it is the same linear-algebraic fact that forbids '
    'cloning.',
    HELSTROM, height=330) + p(
    "It is instructive to see the two statements as one. Suppose a perfect cloner existed. Given a "
    "single copy of \\(|\\psi\\rangle\\in\\{|0\\rangle,|+\\rangle\\}\\), make \\(N\\) copies and "
    "measure them all; the empirical statistics would identify the state with error "
    "\\(2^{-\\Omega(N)}\\), beating the 85.4% ceiling of Figure 2.6 for large \\(N\\). Cloning and "
    "perfect discrimination are therefore equivalent impossibilities, both traceable to the fact "
    "that a unitary preserves inner products" + cite('2,3,4') + ". BB84 turns the ceiling into a "
    "protocol: an eavesdropper who intercepts a qubit encoded in a randomly chosen one of two "
    "mutually unbiased bases necessarily disturbs it, and the disturbance shows up as an elevated "
    "error rate in the sifted key" + cite('5') + ".") + sources(
    'No-cloning: Wootters &amp; Zurek' + cite('2') + ' and Dieks' + cite('3') + '; optimal '
    'discrimination: Helstrom' + cite('4') + '; the cryptographic consequence: Bennett &amp; '
    'Brassard' + cite('5') + '; POVMs and Naimark dilation: Preskill ch. 3' + cite('7') + '.')

REFS = [
    dict(authors="M. A. Nielsen and I. L. Chuang", title="Quantum Computation and Quantum Information",
         venue="Cambridge University Press", year="2010",
         note="§1.2, §2.2 (measurement postulates, POVMs), §12.1 (no-cloning, distinguishability)."),
    dict(authors="W. K. Wootters and W. H. Zurek", title="A single quantum cannot be cloned",
         venue="Nature 299, 802–803", year="1982",
         link="https://doi.org/10.1038/299802a0",
         note="The original no-cloning argument; one page, worth reading in the original."),
    dict(authors="D. Dieks", title="Communication by EPR devices",
         venue="Physics Letters A 92(6), 271–272", year="1982",
         note="Independent, contemporaneous derivation motivated by no-signalling."),
    dict(authors="C. W. Helstrom", title="Quantum Detection and Estimation Theory",
         venue="Academic Press", year="1976",
         note="Source of the optimal-discrimination bound quoted in §5."),
    dict(authors="C. H. Bennett and G. Brassard",
         title="Quantum cryptography: public key distribution and coin tossing",
         venue="Proc. IEEE Int. Conf. Computers, Systems and Signal Processing, 175–179", year="1984",
         note="BB84 — indistinguishability of non-orthogonal states turned into a security proof."),
    dict(authors="A. Peres", title="Quantum Theory: Concepts and Methods",
         venue="Kluwer", year="1995",
         note="Chapters 2–3 give an unusually careful account of what a measurement is."),
    dict(authors="J. Preskill", title="Physics 219 Lecture Notes, Chapter 3: Foundations II",
         venue="Caltech", year="2022", link="http://theory.caltech.edu/~preskill/ph219/",
         note="POVMs, Naimark dilation and the measurement problem, at exactly this level."),
]

CR = [
    dict(
        name='C2.Q1 — Bloch vector of a pure qubit state',
        qtext=cr_qtext('C2.Q1', 'From amplitudes to the Bloch sphere',
                       "The Bloch vector \\(\\vec r=(\\langle X\\rangle,\\langle Y\\rangle,\\langle Z\\rangle)\\) "
                       "is the coordinate system in which single-qubit gates become rotations.",
                       "Write <code>bloch_vector(psi)</code> returning a tuple of three "
                       "<code>float</code>s (each rounded to 6 decimals) for a normalised "
                       "2-component state vector, and <code>state_from_angles(theta, phi)</code> "
                       "returning the NumPy array "
                       "\\((\\cos\\tfrac\\theta2,\\ e^{i\\varphi}\\sin\\tfrac\\theta2)\\).",
                       "bloch_vector([1, 0])             -> (0.0, 0.0, 1.0)\n"
                       "bloch_vector([1, 1]/sqrt(2))     -> (1.0, 0.0, 0.0)\n"
                       "bloch_vector([1, 1j]/sqrt(2))    -> (0.0, 1.0, 0.0)"),
        answer='''import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def bloch_vector(psi):
    psi = np.asarray(psi, dtype=complex).reshape(2)
    psi = psi / np.linalg.norm(psi)
    return tuple(round(float(np.real(psi.conj() @ (S @ psi))), 6) for S in (X, Y, Z))

def state_from_angles(theta, phi):
    return np.array([np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)], dtype=complex)
''',
        preload='''import numpy as np

def bloch_vector(psi):
    # <X>, <Y>, <Z> rounded to 6 decimals
    ...

def state_from_angles(theta, phi):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nprint(bloch_vector([1, 0]))\n',
             'expected': '(0.0, 0.0, 1.0)\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(bloch_vector(np.array([1, 1])/np.sqrt(2)))\n',
             'expected': '(1.0, 0.0, 0.0)\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(bloch_vector(np.array([1, 1j])/np.sqrt(2)))\n',
             'expected': '(0.0, 1.0, 0.0)\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nth, ph = 0.9, 2.1\n'
                     'r = bloch_vector(state_from_angles(th, ph))\n'
                     'exp = (np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph), np.cos(th))\n'
                     'print(np.allclose(r, exp, atol=1e-6))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nrng = np.random.default_rng(11)\n'
                     'v = rng.normal(size=2) + 1j*rng.normal(size=2)\n'
                     'r = np.array(bloch_vector(v))\nprint(round(float(np.linalg.norm(r)), 5))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C2.Q2 — Rotations act as SO(3) on the Bloch ball',
        qtext=cr_qtext('C2.Q2', 'Verifying the SU(2) → SO(3) homomorphism',
                       "\\(R_{\\hat n}(\\theta)=\\cos\\tfrac\\theta2 I-i\\sin\\tfrac\\theta2"
                       "(\\hat n\\cdot\\vec\\sigma)\\) rotates the Bloch vector by \\(\\theta\\) about "
                       "\\(\\hat n\\). This exercise checks that claim numerically.",
                       "Write <code>rot(n, theta)</code> returning the \\(2\\times2\\) unitary for a "
                       "unit axis <code>n = (nx, ny, nz)</code>, and "
                       "<code>rotate_bloch(n, theta, r)</code> returning the classical Rodrigues "
                       "rotation of the 3-vector <code>r</code>. Both must agree.",
                       "rot((0,0,1), pi)  ==  -1j * Z\n"
                       "rotate_bloch((0,0,1), pi, (1,0,0))  ->  (-1, 0, 0)"),
        answer='''import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)

def rot(n, theta):
    n = np.asarray(n, dtype=float)
    n = n / np.linalg.norm(n)
    ns = n[0] * X + n[1] * Y + n[2] * Z
    return np.cos(theta / 2) * I2 - 1j * np.sin(theta / 2) * ns

def rotate_bloch(n, theta, r):
    n = np.asarray(n, dtype=float); n = n / np.linalg.norm(n)
    r = np.asarray(r, dtype=float)
    return (r * np.cos(theta) + np.cross(n, r) * np.sin(theta)
            + n * np.dot(n, r) * (1 - np.cos(theta)))
''',
        preload='''import numpy as np

def rot(n, theta):
    # cos(theta/2) I - i sin(theta/2) (n . sigma)
    ...

def rotate_bloch(n, theta, r):
    # Rodrigues formula
    ...
''',
        tests=[
            {'code': 'import numpy as np\nZ = np.array([[1,0],[0,-1]], dtype=complex)\n'
                     'print(np.allclose(rot((0,0,1), np.pi), -1j*Z))\n',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(np.round(rotate_bloch((0,0,1), np.pi, (1,0,0)), 6).tolist())\n',
             'expected': '[-1.0, 0.0, 0.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nU = rot((1,1,0), 0.83)\n'
                     'print(np.allclose(U.conj().T @ U, np.eye(2)))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
def bv(psi):
    psi = psi/np.linalg.norm(psi)
    return np.array([np.real(psi.conj() @ (S @ psi)) for S in (X,Y,Z)])
psi = np.array([np.cos(0.4), np.exp(1j*1.1)*np.sin(0.4)], dtype=complex)
n, th = (0,1,0), 0.77
lhs = bv(rot(n, th) @ psi)
rhs = rotate_bloch(n, th, bv(psi))
print(np.allclose(lhs, rhs, atol=1e-8))
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nprint(np.allclose(rot((1,0,0), 2*np.pi), -np.eye(2)))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C2.Q3 — Projective measurement in an arbitrary basis',
        qtext=cr_qtext('C2.Q3', 'Born rule and state collapse',
                       "Given an orthonormal basis \\(\\{|b_k\\rangle\\}\\), outcome \\(k\\) occurs "
                       "with probability \\(|\\langle b_k|\\psi\\rangle|^{2}\\) and the state "
                       "collapses to \\(|b_k\\rangle\\).",
                       "Write <code>born_probs(psi, basis)</code> where <code>basis</code> is a "
                       "matrix whose <em>columns</em> are the basis vectors, returning a NumPy "
                       "array of probabilities (rounded to 8 decimals, summing to 1); and "
                       "<code>post_measurement(psi, basis, k)</code> returning the normalised "
                       "collapsed state.",
                       "psi = |0>, basis = columns [|+>, |->]  ->  [0.5, 0.5]"),
        answer='''import numpy as np

def born_probs(psi, basis):
    psi = np.asarray(psi, dtype=complex).ravel()
    psi = psi / np.linalg.norm(psi)
    B = np.asarray(basis, dtype=complex)
    amps = B.conj().T @ psi
    return np.round(np.abs(amps) ** 2, 8)

def post_measurement(psi, basis, k):
    B = np.asarray(basis, dtype=complex)
    v = B[:, k]
    return v / np.linalg.norm(v)
''',
        preload='''import numpy as np

def born_probs(psi, basis):
    # amplitudes = basis^dagger @ psi
    ...

def post_measurement(psi, basis, k):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nH = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)\n'
                     'print(born_probs([1,0], H).tolist())\n',
             'expected': '[0.5, 0.5]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(born_probs([1,0], np.eye(2, dtype=complex)).tolist())\n',
             'expected': '[1.0, 0.0]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nH = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)\n'
                     'v = post_measurement([1,0], H, 1)\n'
                     'print(np.allclose(v, np.array([1,-1])/np.sqrt(2)))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nrng = np.random.default_rng(5)\n'
                     'A = rng.normal(size=(4,4)) + 1j*rng.normal(size=(4,4))\n'
                     'B, _ = np.linalg.qr(A)\npsi = rng.normal(size=4) + 1j*rng.normal(size=4)\n'
                     'print(round(float(born_probs(psi, B).sum()), 6))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nY = np.array([[1,1],[1j,-1j]], dtype=complex)/np.sqrt(2)\n'
                     'print(np.round(born_probs(np.array([1,1j])/np.sqrt(2), Y), 6).tolist())\n',
             'expected': '[1.0, 0.0]\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C2.Q4 — Sampling, shot noise and the Helstrom bound',
        qtext=cr_qtext('C2.Q4', 'What a quantum computer actually outputs',
                       "A device returns samples, not amplitudes. Estimating "
                       "\\(\\langle Z\\rangle\\) from \\(N\\) shots incurs an error "
                       "\\(\\Theta(1/\\sqrt N)\\); distinguishing non-orthogonal states is capped by "
                       "the Helstrom bound.",
                       "Write <code>sample_counts(psi, shots, seed)</code> returning a dict "
                       "mapping bit-strings (MSB = qubit 0, zero-padded to \\(n\\) characters) to "
                       "counts, sorted by key, using "
                       "<code>numpy.random.default_rng(seed).choice</code>; and "
                       "<code>helstrom(psi, phi)</code> returning the optimal success probability "
                       "\\(\\tfrac12(1+\\sqrt{1-|\\langle\\psi|\\phi\\rangle|^{2}})\\), rounded to 6 "
                       "decimals.",
                       "helstrom(|0>, |0>)  ->  0.5      (indistinguishable)\n"
                       "helstrom(|0>, |1>)  ->  1.0      (orthogonal)\n"
                       "helstrom(|0>, |+>)  ->  0.853553"),
        answer='''import numpy as np

def sample_counts(psi, shots, seed):
    psi = np.asarray(psi, dtype=complex).ravel()
    probs = np.abs(psi) ** 2
    probs = probs / probs.sum()
    n = int(round(np.log2(len(probs))))
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(probs), size=shots, p=probs)
    counts = {}
    for i in idx:
        key = format(int(i), '0{}b'.format(n))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))

def helstrom(psi, phi):
    a = np.asarray(psi, dtype=complex).ravel(); a = a / np.linalg.norm(a)
    b = np.asarray(phi, dtype=complex).ravel(); b = b / np.linalg.norm(b)
    ov = abs(np.vdot(a, b)) ** 2
    return round(0.5 * (1 + np.sqrt(max(0.0, 1 - ov))), 6)
''',
        preload='''import numpy as np

def sample_counts(psi, shots, seed):
    ...

def helstrom(psi, phi):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nprint(helstrom([1,0], [0,1]), helstrom([1,0], [1,0]))\n',
             'expected': '1.0 0.5\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(helstrom([1,0], np.array([1,1])/np.sqrt(2)))\n',
             'expected': '0.853553\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nc = sample_counts(np.array([1,1])/np.sqrt(2), 1000, 0)\n'
                     'print(sorted(c.keys()), sum(c.values()))\n',
             'expected': "['0', '1'] 1000\n", 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\npsi = np.zeros(8, dtype=complex); psi[0]=1/np.sqrt(2); psi[7]=1/np.sqrt(2)\n'
                     'c = sample_counts(psi, 500, 42)\nprint(sorted(c.keys()), sum(c.values()))\n',
             'expected': "['000', '111'] 500\n", 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\npsi = np.array([1,0], dtype=complex)\n'
                     'print(sample_counts(psi, 7, 1))\n',
             'expected': "{'0': 7}\n", 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

ST = [
    stack_question(
        name='C2.S1 — Outcome probability in a rotated basis',
        questiontext=stack_qtext(
            'C2.S1', 'Born rule on the Bloch sphere',
            r'<p>A qubit is prepared in \(|\psi\rangle=\cos(\theta/2)|0\rangle+'
            r'e^{i\varphi}\sin(\theta/2)|1\rangle\).</p>'
            r'<p>Give the probability of obtaining the outcome \(+1\) when the observable \(X\) is '
            r'measured, as a simplified function of <code>theta</code> and <code>phi</code>.</p>'
            r'<p>\(p_{+}=\) [[input:ans1]] [[validation:ans1]]</p>'),
        generalfeedback=(
            r'<p>The \(+1\) eigenvector of \(X\) is \(|+\rangle=(|0\rangle+|1\rangle)/\sqrt2\), so</p>'
            r'\[ p_{+}=|\langle +|\psi\rangle|^{2}=\tfrac12\left|\cos\tfrac\theta2+e^{i\varphi}\sin\tfrac\theta2\right|^{2}. \]'
            r'<p>Expanding, \(p_+=\tfrac12\big(1+2\cos\tfrac\theta2\sin\tfrac\theta2\cos\varphi\big)'
            r'=\tfrac12(1+\sin\theta\cos\varphi)\).</p>'
            r'<p>Geometrically this is \(p_\pm=\tfrac12(1\pm\hat n\cdot\vec r)\) with \(\hat n=\hat x\): '
            r'the probability is an affine function of the projection of the Bloch vector onto the '
            r'measurement axis.</p>'),
        questionvariables='ta : (1+sin(theta)*cos(phi))/2;',
        questionnote='p+ = (1+sin(theta)cos(phi))/2',
        parts=[dict(input='ans1', prt='prt1', tans='ta', boxsize=28,
                    truefb=r'<p>Correct — this is \(\tfrac12(1+\hat x\cdot\vec r)\).</p>',
                    falsefb=r'<p>Compute \(|\langle+|\psi\rangle|^2\) and use \(2\sin u\cos u=\sin 2u\).</p>')]),
    stack_question(
        name='C2.S2 — Robertson uncertainty relation for a qubit',
        questiontext=stack_qtext(
            'C2.S2', 'Uncertainty',
            r'<p>For the state \(|0\rangle\):</p>'
            r'<p>(a) Give \(\Delta X=\sqrt{\langle X^2\rangle-\langle X\rangle^2}\).</p>'
            r'<p>\(\Delta X=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the Robertson lower bound \(\tfrac12|\langle[X,Y]\rangle|\) for this state.</p>'
            r'<p>bound \(=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>(a) \(X^2=I\) so \(\langle X^2\rangle=1\); and \(\langle 0|X|0\rangle=0\). Hence \(\Delta X=1\). '
            r'By symmetry \(\Delta Y=1\) as well.</p>'
            r'<p>(b) \([X,Y]=2iZ\) and \(\langle 0|Z|0\rangle=1\), so the bound is '
            r'\(\tfrac12|2i\cdot 1|=1\).</p>'
            r'<p>Since \(\Delta X\Delta Y=1\) equals the bound, \(|0\rangle\) is a minimum-uncertainty '
            r'state for the pair \((X,Y)\) — the qubit analogue of a coherent state.</p>'),
        questionvariables='ta1 : 1;\nta2 : 1;',
        questionnote='DeltaX=1, bound=1',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=10, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Use \(X^2=I\) and \(\langle 0|X|0\rangle=0\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=10, value='0.5000000',
                 truefb='<p>Correct — the bound is saturated.</p>',
                 falsefb=r'<p>\([X,Y]=2iZ\); evaluate \(\langle Z\rangle\) on \(|0\rangle\).</p>')]),
    stack_question(
        name='C2.S3 — Helstrom bound for two pure states',
        questiontext=stack_qtext(
            'C2.S3', 'Optimal state discrimination',
            r'<p>Two equally likely pure states satisfy \(\langle\psi_0|\psi_1\rangle=\cos\alpha\) '
            r'with \(\alpha\in[0,\pi/2]\).</p>'
            r'<p>(a) Give the maximal probability of correctly identifying the prepared state, as a '
            r'simplified function of <code>alpha</code>.</p>'
            r'<p>\(p_{\max}=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Evaluate it for \(\alpha=\pi/4\) (exact expression, no decimals).</p>'
            r'<p>\(p_{\max}(\pi/4)=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>(a) The Helstrom bound for equal priors and pure states is '
            r'\(p_{\max}=\tfrac12\big(1+\sqrt{1-|\langle\psi_0|\psi_1\rangle|^{2}}\big)\). With overlap '
            r'\(\cos\alpha\) and \(\alpha\in[0,\pi/2]\), \(\sqrt{1-\cos^2\alpha}=\sin\alpha\), so '
            r'\(p_{\max}=\tfrac12(1+\sin\alpha)\).</p>'
            r'<p>(b) At \(\alpha=\pi/4\): \(p_{\max}=\tfrac12\left(1+\tfrac{\sqrt2}{2}\right)'
            r'=\tfrac{2+\sqrt2}{4}\approx0.8536\).</p>'
            r'<p>Only orthogonal states (\(\alpha=\pi/2\)) give \(p_{\max}=1\); identical states give '
            r'\(1/2\), i.e. a coin flip. This is the quantitative form of the statement that '
            r'non-orthogonal states cannot be reliably distinguished, and it underpins BB84.</p>'),
        questionvariables='ta1 : (1+sin(alpha))/2;\nta2 : (2+sqrt(2))/4;',
        questionnote='pmax=(1+sin(alpha))/2',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=22, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Start from \(\tfrac12(1+\sqrt{1-|\langle\psi_0|\psi_1\rangle|^2})\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=18, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Substitute \(\sin(\pi/4)=\sqrt2/2\) into your answer to (a).</p>')]),
]

CHAPTER = dict(
    no=2, slug='qubits-and-measurement',
    title='Qubits, the Bloch Sphere and Quantum Measurement',
    subtitle='Geometry of the single qubit, the Born rule, uncertainty, POVMs, optimal state '
             'discrimination and the no-cloning theorem.',
    prereq='Chapter 1 (spectral theorem, Pauli algebra, operator norms).',
    objectives=[
        'Map between amplitudes, Bloch angles and Bloch vectors in both directions.',
        'Interpret any single-qubit unitary as a rotation of the Bloch ball.',
        'Apply the Born rule and projection postulate in an arbitrary orthonormal basis.',
        'Derive and saturate the Robertson uncertainty relation for Pauli observables.',
        'State the POVM formalism and compute the Helstrom limit on distinguishability.',
        'Prove no-cloning from linearity and connect it to quantum key distribution.',
    ],
    sections=[
        ('The qubit and the Bloch sphere', S1),
        ('Single-qubit unitaries as rotations', S2),
        ('Projective measurement and the Born rule', S3),
        ('Uncertainty relations', S4),
        ('POVMs, distinguishability and no-cloning', S5),
        ('Practical simulation: Bloch coordinates and sampling', S6),
    ],
    summary="A qubit is a point on the Bloch sphere; unitaries rotate it; measurement projects it "
            "and returns classical bits with probabilities given by the Born rule. Non-commuting "
            "observables obey Robertson's bound, non-orthogonal states obey Helstrom's, and "
            "unknown states cannot be cloned — three faces of the same linear-algebraic fact "
            "that will reappear as the security of QKD and the difficulty of quantum error "
            "correction.",
    references=REFS, coderunner=CR, stack=ST,
)
