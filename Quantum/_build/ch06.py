# -*- coding: utf-8 -*-
"""Chapter 6 — The Quantum Fourier Transform and Phase Estimation."""
from math import sin, pi, log2, ceil
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, bar_chart,
                    circuit_svg, flow_svg, interactive, C, SERIF, MONO)

S1 = (
    p("Almost every exponential quantum speed-up known — Shor's factoring, discrete logarithm, "
      "Simon's problem, and the hidden subgroup framework that contains them — reduces to one "
      "primitive: the ability to apply a Fourier transform over an abelian group in "
      "polylogarithmic time. This chapter builds that primitive and its main consumer, phase "
      "estimation.")
    + box('def', 'Quantum Fourier transform',
          "For \\(N=2^{n}\\) and \\(\\omega_N=e^{2\\pi i/N}\\), the QFT is the unitary "
          "\\(F_N|j\\rangle=\\tfrac1{\\sqrt N}\\sum_{k=0}^{N-1}\\omega_N^{jk}|k\\rangle\\), i.e. the "
          "matrix \\((F_N)_{kj}=\\omega_N^{jk}/\\sqrt N\\). It is the discrete Fourier transform "
          "written as a unitary on amplitudes.")
    + box('warn', 'The QFT is not a fast DFT',
          "The QFT transforms <em>amplitudes</em>, which are not accessible. It does not let you "
          "Fourier-transform a classical vector and read the answer: preparing the input costs "
          "\\(\\Omega(N)\\) in general, and reading the output requires tomography. Its power lies "
          "entirely in being used <em>inside</em> a larger interference pattern, where only a "
          "coarse feature of the transform — typically a period — needs to be sampled.")
    + p("The key algebraic identity is the <strong>product form</strong>. Writing "
        "\\(j=j_1j_2\\cdots j_n\\) in binary and \\(0.j_\\ell\\cdots j_n\\) for the binary "
        "fraction \\(\\sum_{m}j_{\\ell+m}2^{-m-1}\\):")
    + eq(r"F_N|j\rangle \;=\; \frac{1}{\sqrt N}\bigotimes_{\ell=1}^{n}"
         r"\Big(|0\rangle + e^{2\pi i\,0.j_{n-\ell+1}\cdots j_n}|1\rangle\Big)")
    + p("The output is a <em>product</em> state — the QFT of a computational basis state carries no "
        "entanglement. This is exactly what makes the circuit short.")
)

S2 = (
    p("Reading the product form off qubit by qubit yields the standard circuit: on qubit "
      "\\(\\ell\\), a Hadamard followed by controlled phase rotations "
      "\\(R_m=\\mathrm{diag}(1,e^{2\\pi i/2^{m}})\\) controlled by each later qubit, and finally a "
      "reversal of the qubit order by \\(\\lfloor n/2\\rfloor\\) SWAPs.")
    + code('''for l in range(n):
    H on qubit l
    for m in range(2, n - l + 1):
        controlled-R_m  (control = qubit l+m-1, target = qubit l)
reverse the qubit order''', 'QFT on n qubits — pseudocode')
    + box('prop', 'Cost',
          "The circuit uses \\(n\\) Hadamards and \\(\\binom{n}{2}\\) controlled rotations, i.e. "
          "\\(\\Theta(n^{2})\\) gates, versus \\(\\Theta(N\\log N)=\\Theta(n2^{n})\\) for the classical "
          "FFT on \\(N=2^{n}\\) amplitudes. Truncating rotations with "
          "\\(m>O(\\log(n/\\varepsilon))\\) — they are exponentially close to the identity — gives an "
          "<strong>approximate QFT</strong> of size \\(O(n\\log(n/\\varepsilon))\\) and error "
          "\\(\\varepsilon\\) (Coppersmith 1994), which is what real implementations use.")
    + p("Two remarks for implementers. First, the final SWAP network is often omitted and the "
        "bit order simply reinterpreted classically. Second, the controlled rotations for large "
        "\\(m\\) require angles below any achievable gate precision, so the approximate QFT is "
        "not merely an optimisation — it is a necessity on real hardware.")
)

S3 = (
    p("<strong>Phase kickback</strong> is the mechanism by which a controlled operation writes "
      "information into the control register's phase. If \\(U|u\\rangle=e^{2\\pi i\\varphi}|u\\rangle\\), "
      "then")
    + eq(r"C\text{-}U\;\big(\tfrac{|0\rangle+|1\rangle}{\sqrt2}\otimes|u\rangle\big)"
         r"\;=\;\Big(\tfrac{|0\rangle+e^{2\pi i\varphi}|1\rangle}{\sqrt2}\Big)\otimes|u\rangle .")
    + p("The target is unchanged; the eigenvalue has been transferred to a relative phase on the "
        "control. Measuring the control in the \\(X\\) basis (the <em>Hadamard test</em>) yields "
        "\\(0\\) with probability \\(\\cos^{2}(\\pi\\varphi)\\), giving one bit of information about "
        "\\(\\varphi\\) per shot.")
    + box('def', 'Quantum phase estimation (Kitaev 1995; Cleve–Ekert–Macchiavello–Mosca 1998)',
          "Input: a controlled-\\(U^{2^{k}}\\) black box and an eigenstate \\(|u\\rangle\\) with "
          "\\(U|u\\rangle=e^{2\\pi i\\varphi}|u\\rangle\\). Procedure: prepare \\(t\\) ancillas in "
          "\\(|+\\rangle^{\\otimes t}\\); apply \\(C\\text{-}U^{2^{k}}\\) from ancilla \\(k\\); apply "
          "\\(F_{2^{t}}^{\\dagger}\\) to the ancillas; measure. Output: an integer \\(y\\) with "
          "\\(y/2^{t}\\approx\\varphi\\).")
    + p("After the controlled powers the ancilla register holds "
        "\\(\\tfrac1{\\sqrt{2^{t}}}\\sum_{y}e^{2\\pi i\\varphi y}|y\\rangle\\), which is exactly "
        "\\(F_{2^{t}}|2^{t}\\varphi\\rangle\\) when \\(2^{t}\\varphi\\) is an integer. Applying the "
        "inverse QFT then returns that integer with certainty. The interesting case is when it "
        "is not.")
)

S4 = (
    box('thm', 'Accuracy of phase estimation',
        "Let \\(\\varphi\\) be arbitrary and let \\(b\\) be the best \\(t\\)-bit approximation. "
        "Measuring \\(y\\) gives \\(|y/2^{t}-\\varphi|\\le2^{-t}\\) with probability at least "
        "\\(4/\\pi^{2}\\approx0.405\\). More generally, "
        "\\(\\Pr[|y-b|>e]\\le\\frac{1}{2(e-1)}\\). To obtain \\(n\\) bits with success probability "
        "\\(1-\\varepsilon\\) it suffices to take "
        "\\(t=n+\\big\\lceil\\log_2\\!\\big(2+\\tfrac1{2\\varepsilon}\\big)\\big\\rceil\\) ancillas.")
    + box('proof', 'Sketch',
          "The output amplitude at \\(y\\) is a geometric sum, "
          "\\(\\alpha_y=\\tfrac1{2^{t}}\\sum_{k}e^{2\\pi ik(\\varphi-y/2^{t})}"
          "=\\tfrac1{2^{t}}\\frac{1-e^{2\\pi i2^{t}\\delta}}{1-e^{2\\pi i\\delta}}\\) with "
          "\\(\\delta=\\varphi-y/2^{t}\\). Bounding \\(|1-e^{i\\theta}|\\ge2|\\theta|/\\pi\\) for "
          "\\(|\\theta|\\le\\pi\\) and \\(\\ge\\) the chord length above gives "
          "\\(|\\alpha_b|^{2}\\ge4/\\pi^{2}\\) for the nearest \\(b\\). \\(\\blacksquare\\)")
    + p("Note the resource scaling: reaching precision \\(\\varepsilon\\) needs "
        "\\(O(1/\\varepsilon)\\) applications of \\(U\\) in total (the controlled powers sum to "
        "\\(2^{t}-1\\)). This is the <em>Heisenberg limit</em>, quadratically better than the "
        "\\(O(1/\\varepsilon^{2})\\) that independent sampling would give — the same quadratic gain "
        "that reappears as amplitude estimation in Chapter 8.")
    + box('note', 'Iterative / Kitaev-style QPE',
          "The ancilla register can be replaced by a single qubit measured and reset \\(t\\) times, "
          "with classically fed-forward phase corrections. This removes the QFT entirely and "
          "reduces the qubit count from \\(t+m\\) to \\(1+m\\), at the cost of mid-circuit "
          "measurement. It is the version used in most NISQ-era experiments and in "
          "resource-optimised fault-tolerant designs.")
)

S5 = (
    p("If the input register is not an eigenstate but a superposition "
      "\\(|\\psi\\rangle=\\sum_u c_u|u\\rangle\\), linearity gives")
    + eq(r"\text{QPE}\;|0\rangle^{\otimes t}|\psi\rangle \;\longrightarrow\; "
         r"\sum_u c_u\,|\widetilde{\varphi_u}\rangle\,|u\rangle ,")
    + p("so measuring the ancillas samples an eigenphase with probability \\(|c_u|^{2}\\) and "
        "collapses the input onto the corresponding eigenvector. This single fact powers a great "
        "deal:")
    + ul([
        '<strong>Order finding and factoring</strong> (Chapter 7): \\(U\\) is modular '
        'multiplication; its eigenphases are \\(s/r\\).',
        '<strong>Quantum simulation</strong>: \\(U=e^{-iHt}\\) turns eigenphases into energies, '
        'giving ground-state energy estimation given a good trial state.',
        '<strong>Amplitude estimation</strong> (Chapter 8): QPE applied to the Grover operator '
        'estimates \\(\\sin^{2}\\theta\\) quadratically faster than sampling.',
        '<strong>Linear systems (HHL)</strong>: eigenphases of \\(e^{iAt}\\) are inverted in a '
        'controlled rotation to apply \\(A^{-1}\\).',
    ])
    + box('warn', 'The trial-state bottleneck',
          "QPE succeeds with probability \\(|c_u|^{2}\\), so it is only efficient given a trial "
          "state with non-negligible overlap on the target eigenvector. For generic local "
          "Hamiltonians, preparing such a state is QMA-hard (Chapter 10). Quoted exponential "
          "speed-ups for chemistry are therefore conditional on the physics supplying a good "
          "ansatz, not on the algorithm alone.")
)

S6 = (
    code('''import numpy as np

def qft_matrix(n):
    N = 2 ** n
    j, k = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
    return np.exp(2j * np.pi * j * k / N) / np.sqrt(N)

def qpe_distribution(phi, t):
    """Exact output distribution of t-qubit phase estimation for a phase phi."""
    N = 2 ** t
    y = np.arange(N)
    d = phi - y / N
    amp = np.where(np.abs(np.sin(np.pi * d)) < 1e-15,
                   1.0,
                   np.sin(np.pi * N * d) / (N * np.sin(np.pi * d)))
    return amp ** 2

pr = qpe_distribution(0.3, 5)
print(int(np.argmax(pr)), round(float(pr.max()), 4))    # 10 -> 10/32 = 0.3125''',
         'The QFT matrix and the exact Fejér-kernel output distribution of QPE')
    + p("The distribution \\(|\\alpha_y|^{2}=\\big(\\tfrac{\\sin(\\pi N\\delta)}{N\\sin(\\pi\\delta)}\\big)^{2}\\) "
        "is a Fejér-type kernel centred on \\(\\varphi\\); its \\(4/\\pi^{2}\\) mass bound at the "
        "nearest integer is the content of the theorem in §4, and its heavy tails are why "
        "repetition-and-median is the standard amplification strategy.")
)

# =============================== figures, citations and added commentary =====
QFT_CIRCUIT = circuit_svg(
    3,
    [[('g', 0, 'H')],
     [('c', 1, 0, 'R₂')],
     [('c', 2, 0, 'R₃')],
     [('g', 1, 'H')],
     [('c', 2, 1, 'R₂')],
     [('g', 2, 'H')],
     [('swap', 0, 2)]],
    wire_labels=['j₁', 'j₂', 'j₃'], width=640,
    title='The 3-qubit quantum Fourier transform: n Hadamards, C(n,2) controlled phases, one reversal')

QPE_CIRCUIT = circuit_svg(
    4,
    [[('g', 0, 'H'), ('g', 1, 'H'), ('g', 2, 'H')],
     [('c', 2, 3, 'U¹')],
     [('c', 1, 3, 'U²')],
     [('c', 0, 3, 'U⁴')],
     [('multi', 0, 2, 'QFT†')],
     [('m', 0), ('m', 1), ('m', 2)]],
    wire_labels=['|0⟩', '|0⟩', '|0⟩', '|u⟩'], width=640,
    title='Phase estimation with t = 3 ancillas: controlled powers, inverse transform, readout')


def _fejer(phi, t):
    N = 2 ** t
    out = []
    for y in range(N):
        d = phi - y / N
        if abs(sin(pi * d)) < 1e-14:
            out.append(1.0)
        else:
            out.append((sin(pi * N * d) / (N * sin(pi * d))) ** 2)
    return out


FEJER_EXACT = bar_chart([str(y) for y in range(32)], _fejer(0.25, 5),
                        ylim=(0, 1.05), ylabel='probability', height=300,
                        colors=['#c9a227' if y == 8 else '#026573' for y in range(32)])

FEJER_GEN = bar_chart([str(y) for y in range(32)], _fejer(0.3, 5),
                      ylim=(0, 1.05), ylabel='probability', height=300,
                      colors=['#c9a227' if y in (9, 10) else '#026573' for y in range(32)])

_tt = list(range(3, 17))
QPECOST = line_chart(
    [dict(label='applications of U:  2ᵗ − 1  (Heisenberg limit, error ~ 2⁻ᵗ)', xs=_tt,
          ys=[t for t in _tt], color='#026573', marker=True),
     dict(label='shots for the same error by naive sampling:  ~4ᵗ', xs=_tt,
          ys=[2 * t for t in _tt], color='#dc2626', marker=True)],
    xlim=(3, 16), ylim=(0, 34), xticks=[3,6,9,12,16], yticks=[0,8,16,24,32],
    xlabel='bits of precision  t',
    ylabel='log₂ (number of uses of U)', height=320)

JS_QPE = """
  var b = JXG.JSXGraph.initBoard('ch6qpe', {boundingbox: [-0.09, 1.18, 1.06, -0.28],
      axis: false, showCopyright: false, showNavigation: false});
  var phi = b.create('slider', [[0.02, 1.10], [0.44, 1.10], [0, 0.3, 1]],
      {name: '&#966;', snapWidth: 0.001, strokeColor: '#026573'});
  var tS = b.create('slider', [[0.58, 1.10], [0.98, 1.10], [2, 4, 7]],
      {name: 't', snapWidth: 1, strokeColor: '#c9a227'});
  b.create('line', [[0, 0], [1, 0]], {strokeColor: '#0f172a', strokeWidth: 1.4,
      straightFirst: false, straightLast: false, fixed: true});
  b.create('line', [[0, 0], [0, 1]], {strokeColor: '#0f172a', strokeWidth: 1.4,
      straightFirst: false, straightLast: false, fixed: true});
  function pr(y, N, ph) {
      var d = ph - y / N;
      var s = Math.sin(Math.PI * d);
      if (Math.abs(s) < 1e-14) { return 1; }
      var v = Math.sin(Math.PI * N * d) / (N * s);
      return v * v;
  }
  var bars = [];
  for (var i = 0; i < 128; i++) {
      (function (k) {
          var seg = b.create('segment', [
              [function () { var N = Math.pow(2, tS.Value()); return k < N ? k / N : -1; },
               0],
              [function () { var N = Math.pow(2, tS.Value()); return k < N ? k / N : -1; },
               function () {
                   var N = Math.pow(2, tS.Value());
                   return k < N ? pr(k, N, phi.Value()) : 0;
               }]],
              {strokeColor: '#026573', strokeWidth: 4, fixed: true, highlight: false});
          bars.push(seg);
      })(i);
  }
  b.create('line', [[0, 0.4053], [1, 0.4053]], {strokeColor: '#dc2626', dash: 2,
      straightFirst: false, straightLast: false});
  b.create('text', [0.75, 0.43, '4/&#960;&#178; = 0.405'], {fontSize: 12, strokeColor: '#dc2626'});
  b.create('text', [0.0, -0.13, function () {
      var N = Math.pow(2, tS.Value());
      var best = 0, bp = 0;
      for (var k = 0; k < N; k++) { var q = pr(k, N, phi.Value()); if (q > bp) { bp = q; best = k; } }
      return 'most likely y = ' + best + ' of ' + N + ',  estimate y/2^t = ' +
             (best / N).toFixed(4) + ',  probability ' + bp.toFixed(3);
  }], {fontSize: 14, strokeColor: '#0f172a'});
  b.create('text', [0.0, -0.235, 'horizontal axis: y / 2^t'],
      {fontSize: 12, strokeColor: '#475569'});
"""

S1 = S1 + sources(
    'The QFT as an algorithmic primitive: Shor' + cite('1') + ' and Nielsen &amp; Chuang ch. 5'
    + cite('6') + '; its place in the hidden-subgroup framework: Childs &amp; van Dam' + cite('7') + '.')

S2 = S2 + figure(
    '6.1',
    'The quantum Fourier transform on three qubits. Each qubit receives one Hadamard and then a '
    'controlled phase rotation Rₘ = diag(1, e^{2πi/2^m}) from every later qubit; the final SWAP '
    'reverses the qubit order, which the product form requires. Counting gives n Hadamards and '
    'n(n−1)/2 controlled rotations — quadratic, against the classical FFT’s Θ(N log N) on N = 2ⁿ '
    'amplitudes.',
    QFT_CIRCUIT, width=640, height=236) + p(
    "Two refinements matter in practice. First, the rotations \\(R_m\\) for large \\(m\\) are "
    "exponentially close to the identity, so truncating at \\(m>O(\\log(n/\\varepsilon))\\) gives "
    "the <em>approximate</em> transform with \\(O(n\\log(n/\\varepsilon))\\) gates and total error "
    "\\(\\varepsilon\\)" + cite('4') + ". This is not merely an optimisation: for \\(n=2048\\) the "
    "smallest exact rotation would be by an angle of \\(2\\pi/2^{2048}\\), which no physical "
    "device can distinguish from the identity. Second, when the transform is immediately followed "
    "by a measurement — as it is inside phase estimation — the controlled rotations can be replaced "
    "by classically controlled single-qubit rotations conditioned on earlier measurement outcomes. "
    "This <em>semiclassical</em> Fourier transform reduces the ancilla register to a single qubit "
    "and is the basis of the iterative variant discussed in §4" + cite('2') + ".") + sources(
    'The circuit and its cost: Nielsen &amp; Chuang §5.1' + cite('6') + '; the approximate transform: '
    'Coppersmith' + cite('4') + '.')

S3 = S3 + figure(
    '6.2',
    'Phase estimation with three ancillas. The Hadamards create a uniform superposition of ancilla '
    'values; the controlled powers of U write the phase into the ancilla register by kickback, '
    'producing the state Σ_y e^{2πiφy}|y⟩; the inverse Fourier transform converts that phase ramp '
    'into a position, which the measurement reads out. Everything expensive is in the controlled '
    'powers: the k-th ancilla drives U raised to 2^k.',
    QPE_CIRCUIT, width=640, height=282) + p(
    "The kickback step repays close attention because it is the mechanism, in one form or another, "
    "behind every algorithm in Chapters 6 to 8. A controlled operation is usually read as 'do "
    "something to the target'; but when the target is an <em>eigenvector</em>, nothing happens to it "
    "at all, and the entire effect appears as a phase on the control. The target is a catalyst. "
    "This is why phase estimation does not consume \\(|u\\rangle\\) and why the same eigenstate can "
    "be reused across the \\(t\\) ancillas" + cite('3,6') + ".") + sources(
    'Phase kickback and the QFT-based circuit: Cleve, Ekert, Macchiavello &amp; Mosca' + cite('3')
    + '; the original iterative formulation: Kitaev' + cite('2') + '.')

S4 = S4 + figure(
    '6.3',
    'Output distribution when the phase is exactly representable: φ = 1/4 = 8/32 with t = 5 ancillas. '
    'The inverse Fourier transform inverts the phase ramp perfectly and the measurement returns '
    'y = 8 with certainty. This is the only case in which phase estimation is deterministic.',
    FEJER_EXACT, height=300) + figure(
    '6.4',
    'The generic case: φ = 0.3, which lies between 9/32 and 10/32. The distribution is a Fejér-type '
    'kernel centred on 2^t φ; the two neighbouring outcomes carry most of the weight, and the '
    'theorem of §4 guarantees at least 4/π² ≈ 0.405 on the nearest one. The tails decay only as '
    '1/|y − 2^t φ|², which is why the failure probability is reduced by repetition and median '
    'selection rather than by hoping for concentration.',
    FEJER_GEN, height=300) + interactive(
    '6.5', 'ch6qpe',
    'Move φ continuously and change the number of ancillas t. Two things are worth checking by hand: '
    'whenever 2^t φ happens to be an integer the distribution collapses to a single bar of height 1, '
    'and in every other case the tallest bar stays above the red 4/π² line no matter how badly φ '
    'falls between grid points. Increasing t by one halves the grid spacing and therefore doubles '
    'the precision — at the cost of doubling the number of applications of U.',
    JS_QPE, aspect='16/9', max_width=660,
    hint='drag φ and t and watch the output distribution.') + figure(
    '6.6',
    'Why phase estimation is the right way to learn a phase. Reaching t bits of precision costs '
    '2^t − 1 applications of U, i.e. error ε with O(1/ε) uses — the Heisenberg limit. Estimating the '
    'same phase by repeatedly running a Hadamard test and averaging costs O(1/ε²) uses. The vertical '
    'axis is logarithmic, so the constant gap is a quadratic saving.',
    QPECOST, height=320) + p(
    "The \\(4/\\pi^{2}\\) constant comes from bounding a geometric sum. Writing "
    "\\(\\delta=\\varphi-b/2^{t}\\) for the offset from the nearest grid point, the amplitude at "
    "\\(b\\) is \\(\\frac{1}{2^{t}}\\frac{1-e^{2\\pi i2^{t}\\delta}}{1-e^{2\\pi i\\delta}}\\); using "
    "\\(|1-e^{i\\theta}|\\le|\\theta|\\) in the numerator and \\(\\ge2|\\theta|/\\pi\\) in the "
    "denominator, with \\(|2^{t}\\delta|\\le1/2\\), gives \\(|\\alpha_b|\\ge2/\\pi\\)" + cite('3')
    + ". The bound is uniform in \\(t\\) and in \\(\\varphi\\), which is what makes the algorithm "
    "usable as a subroutine: the caller can assume constant success probability and amplify."
) + sources(
    'Accuracy analysis and the ancilla count: Cleve et al.' + cite('3') + ' and Nielsen &amp; '
    'Chuang §5.2' + cite('6') + '; the iterative single-ancilla variant: Kitaev' + cite('2') + '.')

S5 = S5 + sources(
    'Applications: order finding' + cite('1') + ', linear systems' + cite('5') + ', and the general '
    'abelian framework' + cite('7') + '. The trial-state caveat is discussed in Chapter 10.')

REFS = [
    dict(authors="P. W. Shor",
         title="Algorithms for quantum computation: discrete logarithms and factoring",
         venue="Proc. 35th FOCS, 124–134", year="1994",
         link="https://arxiv.org/abs/quant-ph/9508027",
         note="Introduces the QFT over Z_{2^n} as an algorithmic primitive."),
    dict(authors="A. Yu. Kitaev", title="Quantum measurements and the abelian stabilizer problem",
         venue="arXiv:quant-ph/9511026", year="1995",
         link="https://arxiv.org/abs/quant-ph/9511026",
         note="Original phase estimation, in its iterative single-ancilla form."),
    dict(authors="R. Cleve, A. Ekert, C. Macchiavello and M. Mosca",
         title="Quantum algorithms revisited",
         venue="Proc. Royal Society A 454, 339–354", year="1998",
         link="https://arxiv.org/abs/quant-ph/9708016",
         note="The QFT-based QPE circuit and the 4/pi^2 accuracy analysis of §4."),
    dict(authors="D. Coppersmith", title="An approximate Fourier transform useful in quantum factoring",
         venue="IBM Research Report RC19642", year="1994",
         link="https://arxiv.org/abs/quant-ph/0201067",
         note="The approximate QFT with O(n log n) gates."),
    dict(authors="A. W. Harrow, A. Hassidim and S. Lloyd",
         title="Quantum algorithm for linear systems of equations",
         venue="Physical Review Letters 103, 150502", year="2009",
         link="https://arxiv.org/abs/0811.3171",
         note="HHL; phase estimation used to invert eigenvalues (see the caveats in §5)."),
    dict(authors="M. A. Nielsen and I. L. Chuang", title="Quantum Computation and Quantum Information",
         venue="Cambridge University Press", year="2010",
         note="Chapter 5 is the standard treatment of the QFT and phase estimation."),
    dict(authors="A. M. Childs and W. van Dam", title="Quantum algorithms for algebraic problems",
         venue="Reviews of Modern Physics 82, 1", year="2010",
         link="https://arxiv.org/abs/0812.0380",
         note="Places the QFT in the hidden-subgroup framework developed in Chapter 7."),
]

CR = [
    dict(
        name='C6.Q1 — The QFT matrix',
        qtext=cr_qtext('C6.Q1', 'Definition and basic properties',
                       "\\((F_N)_{kj}=\\omega_N^{jk}/\\sqrt N\\) with \\(\\omega_N=e^{2\\pi i/N}\\). "
                       "It is unitary, symmetric, and satisfies \\(F_N^{4}=I\\).",
                       "Write <code>qft_matrix(n)</code> returning the \\(2^{n}\\times2^{n}\\) QFT "
                       "matrix, and <code>qft_apply(psi)</code> applying it to a state vector "
                       "whose length is a power of two.",
                       "qft_matrix(1)  ==  H\n"
                       "qft_apply(|0>^n)  ->  uniform superposition"),
        answer='''import numpy as np

def qft_matrix(n):
    N = 2 ** n
    j = np.arange(N).reshape(-1, 1)
    k = np.arange(N).reshape(1, -1)
    return np.exp(2j * np.pi * j * k / N) / np.sqrt(N)

def qft_apply(psi):
    psi = np.asarray(psi, dtype=complex).ravel()
    n = int(round(np.log2(len(psi))))
    return qft_matrix(n) @ psi
''',
        preload='''import numpy as np

def qft_matrix(n):
    ...

def qft_apply(psi):
    ...
''',
        tests=[
            {'code': 'import numpy as np\nH = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)\n'
                     'print(np.allclose(qft_matrix(1), H))\n',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nv = np.zeros(8, dtype=complex); v[0]=1\n'
                     'print(np.allclose(qft_apply(v), np.full(8, 1/np.sqrt(8))))\n',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nF = qft_matrix(3)\n'
                     'print(np.allclose(F.conj().T @ F, np.eye(8)), np.allclose(F, F.T))\n',
             'expected': 'True True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nF = qft_matrix(2)\n'
                     'print(np.allclose(np.linalg.matrix_power(F, 4), np.eye(4)))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nrng = np.random.default_rng(1)\n'
                     'v = rng.normal(size=16)+1j*rng.normal(size=16)\n'
                     'ref = np.fft.ifft(v) * np.sqrt(16)\n'
                     'print(np.allclose(qft_apply(v), ref))\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C6.Q2 — The QFT circuit: Hadamards, controlled phases, SWAPs',
        qtext=cr_qtext('C6.Q2', 'Building the O(n^2) circuit',
                       "The product form of §1 becomes a circuit with \\(n\\) Hadamards, "
                       "\\(\\binom{n}{2}\\) controlled rotations \\(R_m=\\mathrm{diag}(1,e^{2\\pi i/2^{m}})\\), "
                       "and a final qubit reversal.",
                       "Write <code>qft_circuit_matrix(n)</code> that <em>constructs</em> the QFT as "
                       "a product of these elementary gates (do not return "
                       "<code>qft_matrix(n)</code> directly) and returns the resulting "
                       "\\(2^{n}\\times2^{n}\\) matrix. Also write <code>gate_count(n)</code> "
                       "returning the tuple <code>(hadamards, controlled_rotations)</code>.",
                       "gate_count(4) -> (4, 6)\n"
                       "qft_circuit_matrix(3)  ==  qft_matrix(3)"),
        answer='''import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

def _embed1(U, q, n):
    ops = [np.eye(2, dtype=complex)] * n
    ops[q] = U
    out = np.array([[1.0 + 0j]])
    for o in ops:
        out = np.kron(out, o)
    return out

def _cphase(theta, c, t, n):
    N = 2 ** n
    diag = np.ones(N, dtype=complex)
    for x in range(N):
        bits = [(x >> (n - 1 - k)) & 1 for k in range(n)]
        if bits[c] == 1 and bits[t] == 1:
            diag[x] = np.exp(1j * theta)
    return np.diag(diag)

def _swap(a, b, n):
    N = 2 ** n
    P = np.zeros((N, N), dtype=complex)
    for x in range(N):
        bits = [(x >> (n - 1 - k)) & 1 for k in range(n)]
        bits[a], bits[b] = bits[b], bits[a]
        y = 0
        for k in range(n):
            y = (y << 1) | bits[k]
        P[y, x] = 1
    return P

def qft_circuit_matrix(n):
    N = 2 ** n
    U = np.eye(N, dtype=complex)
    for l in range(n):
        U = _embed1(H, l, n) @ U
        for m in range(2, n - l + 1):
            U = _cphase(2 * np.pi / 2 ** m, l + m - 1, l, n) @ U
    for a in range(n // 2):
        U = _swap(a, n - 1 - a, n) @ U
    return U

def gate_count(n):
    return (n, n * (n - 1) // 2)
''',
        preload='''import numpy as np

def qft_circuit_matrix(n):
    # H on qubit l, then controlled-R_m from qubit l+m-1, then reverse the qubit order
    ...

def gate_count(n):
    ...
''',
        tests=[
            {'code': 'print(gate_count(4))\n',
             'expected': '(4, 6)\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
def qft_matrix(n):
    N = 2 ** n
    j = np.arange(N).reshape(-1,1); k = np.arange(N).reshape(1,-1)
    return np.exp(2j*np.pi*j*k/N)/np.sqrt(N)
print(np.allclose(qft_circuit_matrix(3), qft_matrix(3)))
''',
             'expected': 'True\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': '''import numpy as np
U = qft_circuit_matrix(4)
print(np.allclose(U.conj().T @ U, np.eye(16)))
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': '''import numpy as np
def qft_matrix(n):
    N = 2 ** n
    j = np.arange(N).reshape(-1,1); k = np.arange(N).reshape(1,-1)
    return np.exp(2j*np.pi*j*k/N)/np.sqrt(N)
print(all(np.allclose(qft_circuit_matrix(n), qft_matrix(n)) for n in (1,2,3,4)))
''',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(gate_count(10))\n',
             'expected': '(10, 45)\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C6.Q3 — Phase estimation, simulated',
        qtext=cr_qtext('C6.Q3', 'Reading an eigenphase',
                       "With \\(t\\) ancillas, controlled powers of \\(U\\) followed by "
                       "\\(F^{\\dagger}\\) concentrate the ancilla register on the best "
                       "\\(t\\)-bit approximation of \\(\\varphi\\).",
                       "Write <code>qpe_state(phi, t)</code> returning the ancilla state "
                       "\\(\\tfrac1{\\sqrt{2^{t}}}\\sum_y e^{2\\pi i\\varphi y}|y\\rangle\\) "
                       "<em>after</em> applying the inverse QFT; "
                       "<code>qpe_probs(phi, t)</code> returning the measurement distribution "
                       "(rounded to 10 decimals); and "
                       "<code>qpe_estimate(phi, t)</code> returning the most likely "
                       "\\(y/2^{t}\\) as a float.",
                       "qpe_estimate(0.25, 3)  ->  0.25   (exact, 3 bits suffice)\n"
                       "qpe_estimate(0.3, 5)   ->  0.3125 (= 10/32, nearest 5-bit value)"),
        answer='''import numpy as np

def _qft(n):
    N = 2 ** n
    j = np.arange(N).reshape(-1, 1)
    k = np.arange(N).reshape(1, -1)
    return np.exp(2j * np.pi * j * k / N) / np.sqrt(N)

def qpe_state(phi, t):
    N = 2 ** t
    y = np.arange(N)
    pre = np.exp(2j * np.pi * phi * y) / np.sqrt(N)
    return _qft(t).conj().T @ pre

def qpe_probs(phi, t):
    return np.round(np.abs(qpe_state(phi, t)) ** 2, 10)

def qpe_estimate(phi, t):
    return float(int(np.argmax(qpe_probs(phi, t))) / 2 ** t)
''',
        preload='''import numpy as np

def qpe_state(phi, t):
    ...

def qpe_probs(phi, t):
    ...

def qpe_estimate(phi, t):
    ...
''',
        tests=[
            {'code': 'print(qpe_estimate(0.25, 3), qpe_estimate(0.5, 3))\n',
             'expected': '0.25 0.5\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(qpe_estimate(0.3, 5))\n',
             'expected': '0.3125\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(round(float(qpe_probs(0.25, 3).max()), 6))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(round(float(qpe_probs(0.3, 6).max()), 4) >= 0.405)\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\nprint(round(float(qpe_probs(0.123456, 8).sum()), 6))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C6.Q4 — The Hadamard test and the 4/pi^2 bound',
        qtext=cr_qtext('C6.Q4', 'One bit of phase per shot, and how many bits you really need',
                       "The Hadamard test measures \\(\\mathrm{Re}\\langle u|U|u\\rangle\\); "
                       "the accuracy theorem of §4 fixes the number of ancillas needed for "
                       "\\(n\\)-bit precision at confidence \\(1-\\varepsilon\\).",
                       "Write <code>hadamard_test_p0(phi)</code> returning "
                       "\\(\\cos^{2}(\\pi\\varphi)\\) rounded to 6 decimals; "
                       "<code>qpe_ancillas(n, eps)</code> returning "
                       "\\(t=n+\\lceil\\log_2(2+\\tfrac1{2\\varepsilon})\\rceil\\) as an "
                       "<code>int</code>; and <code>success_prob(phi, t)</code> returning the total "
                       "probability that the measured \\(y\\) satisfies "
                       "\\(|y/2^{t}-\\varphi|\\le2^{-t}\\) (taking the difference modulo 1), "
                       "rounded to 6 decimals.",
                       "qpe_ancillas(4, 0.01) -> 4 + ceil(log2(52)) = 4 + 6 = 10"),
        answer='''import numpy as np

def hadamard_test_p0(phi):
    return round(float(np.cos(np.pi * phi) ** 2), 6)

def qpe_ancillas(n, eps):
    return int(n + int(np.ceil(np.log2(2 + 1 / (2 * eps)))))

def _probs(phi, t):
    N = 2 ** t
    y = np.arange(N)
    d = phi - y / N
    with np.errstate(divide='ignore', invalid='ignore'):
        amp = np.where(np.abs(np.sin(np.pi * d)) < 1e-14, 1.0,
                       np.sin(np.pi * N * d) / (N * np.sin(np.pi * d)))
    return amp ** 2

def success_prob(phi, t):
    N = 2 ** t
    y = np.arange(N)
    d = np.abs((y / N - phi + 0.5) % 1.0 - 0.5)
    pr = _probs(phi, t)
    return round(float(pr[d <= 1 / N + 1e-12].sum()), 6)
''',
        preload='''import numpy as np

def hadamard_test_p0(phi):
    ...

def qpe_ancillas(n, eps):
    ...

def success_prob(phi, t):
    ...
''',
        tests=[
            {'code': 'print(hadamard_test_p0(0.0), hadamard_test_p0(0.5))\n',
             'expected': '1.0 0.0\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(qpe_ancillas(4, 0.01))\n',
             'expected': '10\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(success_prob(0.25, 3))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(success_prob(0.3, 5) >= 4/np.pi**2)\n',
             'expected': 'True\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(hadamard_test_p0(0.25), qpe_ancillas(8, 0.05))\n',
             'expected': '0.5 12\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

ST = [
    stack_question(
        name='C6.S1 — Matrix elements and cost of the QFT',
        questiontext=stack_qtext(
            'C6.S1', 'The transform itself',
            r'<p>Let \(n={@n@}\), \(N=2^{n}\) and \(F_N|j\rangle=\frac{1}{\sqrt N}\sum_k '
            r'e^{2\pi ijk/N}|k\rangle\).</p>'
            r'<p>(a) Give the matrix element \(\langle k|F_N|j\rangle\) for general \(j,k,N\) '
            r'(use <code>j</code>, <code>k</code>, <code>N</code>).</p>'
            r'<p>\(\langle k|F_N|j\rangle=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the number of controlled-rotation gates in the standard QFT circuit on '
            r'\(n\) qubits, as a function of <code>n</code>.</p>'
            r'<p>gates \(=\) [[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Evaluate that count for \(n={@n@}\).</p>'
            r'<p>value \(=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) Directly from the definition, \(\langle k|F_N|j\rangle=e^{2\pi ijk/N}/\sqrt N\).</p>'
            r'<p>(b) Qubit \(\ell\) receives one Hadamard and controlled rotations from every later '
            r'qubit, giving \(\sum_{\ell=1}^{n}(n-\ell)=\binom{n}{2}=\frac{n(n-1)}{2}\).</p>'
            r'<p>(c) For \(n={@n@}\) this is \({@ta3@}\).</p>'
            r'<p>Compare the classical FFT at \(\Theta(N\log N)=\Theta(n2^{n})\): the quantum circuit '
            r'is exponentially smaller, but it transforms amplitudes, which cannot be read out '
            r'directly. Truncating rotations below \(2\pi/2^{O(\log(n/\varepsilon))}\) yields the '
            r'approximate QFT with only \(O(n\log(n/\varepsilon))\) gates.</p>'),
        questionvariables='n : rand_with_step(4,9,1);\nta1 : exp(2*%pi*%i*j*k/N)/sqrt(N);\n'
                          'ta2 : n*(n-1)/2;\nta3 : n*(n-1)/2;',
        questionnote='n={@n@}, C(n,2)={@ta3@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=28, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Read the coefficient of \(|k\rangle\) straight off the definition.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=14, value='0.3333333',
                 truefb=r'<p>Correct: \(\binom{n}{2}\).</p>',
                 falsefb=r'<p>Sum \(n-\ell\) over \(\ell=1,\dots,n\).</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>Substitute the given \\(n\\).</p>')]),
    stack_question(
        name='C6.S2 — Phase kickback and the Hadamard test',
        questiontext=stack_qtext(
            'C6.S2', 'One qubit of phase information',
            r'<p>Let \(U|u\rangle=e^{2\pi i\varphi}|u\rangle\). Prepare the control in \(|+\rangle\), '
            r'apply controlled-\(U\), then a Hadamard on the control, then measure it.</p>'
            r'<p>(a) Give \(\Pr[0]\) as a simplified function of <code>phi</code>.</p>'
            r'<p>\(\Pr[0]=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give \(\Pr[0]-\Pr[1]\), again as a function of <code>phi</code>.</p>'
            r'<p>\(\Pr[0]-\Pr[1]=\) [[input:ans2]] [[validation:ans2]]</p>'),
        generalfeedback=(
            r'<p>After the controlled operation the control is \(\frac{1}{\sqrt2}'
            r'(|0\rangle+e^{2\pi i\varphi}|1\rangle)\) and the target is untouched — this is phase '
            r'kickback. The Hadamard turns it into '
            r'\(\frac{1+e^{2\pi i\varphi}}{2}|0\rangle+\frac{1-e^{2\pi i\varphi}}{2}|1\rangle\).</p>'
            r'<p>(a) \(\Pr[0]=\left|\frac{1+e^{2\pi i\varphi}}{2}\right|^{2}=\cos^{2}(\pi\varphi)\).</p>'
            r'<p>(b) \(\Pr[0]-\Pr[1]=\cos(2\pi\varphi)=\mathrm{Re}\,\langle u|U|u\rangle\).</p>'
            r'<p>Each shot therefore gives one Bernoulli sample of a quantity whose mean encodes the '
            r'phase. Estimating \(\varphi\) this way costs \(O(1/\varepsilon^{2})\) shots; full QPE '
            r'costs \(O(1/\varepsilon)\) applications of \(U\), the Heisenberg-limited scaling.</p>'),
        questionvariables='ta1 : cos(%pi*phi)^2;\nta2 : cos(2*%pi*phi);',
        questionnote='cos^2(pi phi), cos(2 pi phi)',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=20, value='0.5000000',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Compute \(|(1+e^{2\pi i\varphi})/2|^{2}\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=20, value='0.5000000',
                 truefb=r'<p>Correct — this is \(\mathrm{Re}\langle u|U|u\rangle\).</p>',
                 falsefb=r'<p>Use \(2\cos^2 x-1=\cos 2x\).</p>')]),
    stack_question(
        name='C6.S3 — Ancilla count and success probability of QPE',
        questiontext=stack_qtext(
            'C6.S3', 'Sizing the register',
            r'<p>(a) Give the guaranteed lower bound on the probability that \(t\)-qubit phase '
            r'estimation returns the nearest \(t\)-bit approximation of \(\varphi\) '
            r'(an exact expression).</p>'
            r'<p>\(p_{\min}=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the number of ancillas \(t\) needed for \(n\) bits of precision with '
            r'failure probability at most \(\varepsilon\) (use <code>n</code> and <code>eps</code>; '
            r'you may use <code>ceiling</code>).</p>'
            r'<p>\(t=\) [[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Evaluate it for \(n={@nn@}\) and \(\varepsilon=1/100\).</p>'
            r'<p>\(t=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) The geometric-sum amplitude at the nearest integer satisfies '
            r'\(|\alpha_b|^{2}\ge 4/\pi^{2}\approx0.405\), independently of \(t\) and \(\varphi\).</p>'
            r'<p>(b) Bounding the tail of the Fejér kernel gives '
            r'\(t=n+\left\lceil\log_2\left(2+\frac{1}{2\varepsilon}\right)\right\rceil\).</p>'
            r'<p>(c) With \(n={@nn@}\), \(\varepsilon=1/100\): '
            r'\(\lceil\log_2 52\rceil=6\), so \(t={@nn@}+6={@ta3@}\).</p>'
            r'<p>Alternatively, repeat the \(t=n\) circuit \(O(\log(1/\varepsilon))\) times and take '
            r'the median — the standard powering trick, cheaper in qubits but more expensive in '
            r'circuit repetitions.</p>'),
        questionvariables=('nn : rand_with_step(4,10,1);\n'
                           'ta1 : 4/%pi^2;\n'
                           'ta2 : n + ceiling(log(2+1/(2*eps))/log(2));\n'
                           'ta3 : nn + 6;'),
        questionnote='nn={@nn@}, t={@ta3@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=12, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>The classic bound is \(4/\pi^{2}\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=34, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>\(t=n+\lceil\log_2(2+1/(2\varepsilon))\rceil\).</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>\(\lceil\log_2(2+50)\rceil=\lceil\log_2 52\rceil=6\).</p>')]),
]

CHAPTER = dict(
    no=6, slug='qft-and-phase-estimation',
    title='The Quantum Fourier Transform and Phase Estimation',
    subtitle='The product form and O(n²) circuit of the QFT, the approximate QFT, phase kickback, '
             'the Hadamard test, and quantum phase estimation with its Heisenberg-limited accuracy.',
    prereq='Chapters 1–3 (circuits, controlled gates); Chapter 5 is not required.',
    objectives=[
        'Derive the product form of the QFT and read the O(n²) circuit off it.',
        'Explain why the QFT is not a fast classical DFT and what the approximate QFT costs.',
        'Use phase kickback and the Hadamard test to extract a phase, one bit per shot.',
        'State and use the QPE accuracy theorem, including the 4/π² bound and the ancilla count.',
        'Explain the Heisenberg-limited O(1/ε) scaling and the trial-state overlap bottleneck.',
        'Simulate QPE exactly and reproduce its Fejér-kernel output distribution.',
    ],
    sections=[
        ('The quantum Fourier transform', S1),
        ('The circuit and its cost', S2),
        ('Phase kickback and phase estimation', S3),
        ('Accuracy, resources and the iterative variant', S4),
        ('Superposed eigenstates and applications', S5),
        ('Numerical practice', S6),
    ],
    summary="The QFT is a \\(\\Theta(n^{2})\\) circuit — \\(O(n\\log n)\\) if approximated — because "
            "the Fourier transform of a basis state is a product state. Combined with phase "
            "kickback it yields phase estimation, which extracts an eigenphase to \\(t\\) bits "
            "using \\(O(2^{t})\\) applications of \\(U\\) and succeeds with probability at least "
            "\\(4/\\pi^{2}\\). Everything in Chapters 7 and 8 is an instance: order finding, "
            "discrete logarithm, amplitude estimation and eigenvalue estimation all call phase "
            "estimation on a suitable unitary.",
    references=REFS, coderunner=CR, stack=ST,
)
