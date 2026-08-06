# -*- coding: utf-8 -*-
"""Chapter 7 — Shor's Algorithm, Order Finding and the Hidden Subgroup Problem."""
from math import sin, pi, log10, exp, log
from engine import (p, eq, box, code, table, ul, ol, cr_qtext, stack_question,
                    stack_qtext, figure, cite, sources, line_chart, bar_chart,
                    flow_svg, circuit_svg, interactive, C, SERIF, MONO)

S1 = (
    p("Shor's algorithm factors an \\(L\\)-bit integer in \\(\\tilde O(L^{2})\\) quantum gates, "
      "against \\(\\exp\\big(\\Theta(L^{1/3}\\log^{2/3}L)\\big)\\) for the best known classical "
      "method (the general number field sieve). It is not one algorithm but a classical "
      "reduction plus one quantum subroutine — order finding — which is itself an instance of "
      "the phase estimation of Chapter 6.")
    + box('thm', 'Reduction of factoring to order finding',
          "Let \\(N\\) be odd, composite, and not a prime power (both cases are easy classically). "
          "Pick \\(a\\) uniformly from \\(\\{2,\\dots,N-1\\}\\). If \\(\\gcd(a,N)>1\\) we are done. "
          "Otherwise let \\(r=\\mathrm{ord}_N(a)\\), the least \\(r>0\\) with \\(a^{r}\\equiv1\\). "
          "If \\(r\\) is even and \\(a^{r/2}\\not\\equiv-1\\pmod N\\), then "
          "\\(\\gcd(a^{r/2}\\pm1,N)\\) are non-trivial factors. This happens with probability at "
          "least \\(1-2^{-(k-1)}\\), where \\(k\\ge2\\) is the number of distinct odd prime factors "
          "of \\(N\\) — so at least \\(1/2\\).")
    + box('proof', 'Why the gcd works',
          "\\(a^{r}\\equiv1\\) means \\(N\\mid(a^{r/2}-1)(a^{r/2}+1)\\). If \\(N\\) divided "
          "\\(a^{r/2}-1\\) then \\(r/2\\) would already be an order, contradicting minimality; and "
          "\\(N\\nmid a^{r/2}+1\\) by hypothesis. Hence \\(N\\) shares a proper factor with each "
          "term. The probability bound comes from the Chinese Remainder Theorem applied to the "
          "cyclic groups \\((\\mathbb Z/p_i^{e_i})^{\\times}\\). \\(\\blacksquare\\)")
    + p("Everything so far is classical and cheap. The hard part is computing \\(r\\), for which "
        "no efficient classical algorithm is known — indeed order finding is polynomially "
        "equivalent to factoring.")
)

S2 = (
    p("Define, for \\(\\gcd(a,N)=1\\), the unitary \\(U_a|x\\rangle=|ax\\bmod N\\rangle\\) on "
      "\\(m=\\lceil\\log_2 N\\rceil\\) qubits (extended by the identity on \\(x\\ge N\\)). Its "
      "eigenvectors are the Fourier modes of the cyclic orbit:")
    + eq(r"|u_s\rangle=\frac{1}{\sqrt r}\sum_{k=0}^{r-1}e^{-2\pi i sk/r}\,|a^{k}\bmod N\rangle,"
         r"\qquad U_a|u_s\rangle=e^{2\pi i s/r}|u_s\rangle .")
    + p("So the eigenphases are exactly \\(s/r\\). We cannot prepare \\(|u_s\\rangle\\) without "
        "knowing \\(r\\) — but we do not need to, because")
    + eq(r"\frac{1}{\sqrt r}\sum_{s=0}^{r-1}|u_s\rangle \;=\; |1\rangle ,")
    + p("a state we can trivially prepare. Running phase estimation on \\(|1\\rangle\\) therefore "
        "samples \\(s\\) uniformly from \\(\\{0,\\dots,r-1\\}\\) and returns "
        "\\(y/2^{t}\\approx s/r\\). Taking \\(t=2L+1\\) ancillas ensures the approximation is "
        "accurate to \\(1/2r^{2}\\), which is precisely the precision at which a rational with "
        "denominator \\(<N\\) is uniquely determined.")
    + box('thm', 'Continued fractions',
          "If \\(|x-s/r|\\le1/(2r^{2})\\) with \\(\\gcd(s,r)=1\\), then \\(s/r\\) is a convergent of "
          "the continued-fraction expansion of \\(x\\), and it is found in "
          "\\(O(L^{3})\\) classical time. (Legendre's theorem; see Hardy & Wright, Thm 184.)")
    + p("If the recovered \\(r'\\) fails \\(a^{r'}\\equiv1\\), or is odd, or gives "
        "\\(a^{r'/2}\\equiv-1\\), simply repeat: a constant number of attempts suffices with high "
        "probability. Note \\(s=0\\) occurs with probability \\(1/r\\) and yields nothing — another "
        "reason to repeat.")
)

S3 = (
    p("The dominant cost is not the QFT but the modular exponentiation "
      "\\(|x\\rangle|1\\rangle\\mapsto|x\\rangle|a^{x}\\bmod N\\rangle\\), realised as \\(2L\\) "
      "controlled modular multiplications by the precomputed constants "
      "\\(a^{2^{k}}\\bmod N\\).")
    + table(['Component', 'Qubits', 'Gate count'],
            [['Approximate QFT on \\(2L+1\\)', '\\(2L+1\\)', '\\(O(L\\log L)\\)'],
             ['Modular multiplication (schoolbook)', '\\(O(L)\\)', '\\(O(L^{2})\\)'],
             ['Modular exponentiation', '\\(O(L)\\)', '\\(O(L^{3})\\) naive, \\(\\tilde O(L^{2})\\) with fast arithmetic'],
             ['Total (Beauregard 2003)', '\\(2L+3\\)', '\\(O(L^{3}\\log L)\\)']])
    + box('warn', 'Fault-tolerant reality check',
          "Textbook counts assume noiseless gates. A concrete surface-code estimate for RSA-2048 "
          "(Gidney–Ekerå 2021) needs about 20 million noisy physical qubits running for roughly "
          "8 hours at a \\(10^{-3}\\) physical error rate, dominated by magic-state distillation "
          "for the Toffolis. Devices available today are three to four orders of magnitude away "
          "in qubit count. The threat model for cryptography is 'harvest now, decrypt later', "
          "which is why post-quantum standards (NIST ML-KEM, ML-DSA) are being deployed now.")
)

S4 = (
    p("The same machinery solves the discrete logarithm problem: given a generator \\(g\\) of a "
      "cyclic group of known order \\(r\\) and \\(y=g^{x}\\), recover \\(x\\). Use two "
      "registers, compute \\(g^{u}y^{-v}\\), and Fourier-transform both registers; the "
      "measurement outcome lies on a line of slope \\(x\\) in \\(\\mathbb Z_r^{2}\\). This breaks "
      "Diffie–Hellman, DSA and — with the elliptic-curve variant — ECDSA, using far fewer qubits "
      "than RSA of comparable classical security.")
    + box('def', 'Hidden subgroup problem (HSP)',
          "Given a group \\(G\\), a set \\(S\\), and an oracle \\(f:G\\to S\\) that is constant on "
          "cosets of an unknown subgroup \\(H\\le G\\) and distinct across cosets, find \\(H\\). "
          "Simon's problem is \\(G=\\mathbb Z_2^{n}\\); order finding is "
          "\\(G=\\mathbb Z\\); discrete log is \\(G=\\mathbb Z_r^{2}\\); period finding is "
          "\\(G=\\mathbb Z_N\\).")
    + box('thm', 'Abelian HSP',
          "For finite abelian \\(G\\), HSP is solved with \\(O(\\log|G|)\\) oracle queries and "
          "\\(\\mathrm{poly}(\\log|G|)\\) gates: prepare a uniform superposition over \\(G\\), query "
          "\\(f\\), measure the output register (collapsing to a coset), apply the QFT over "
          "\\(G\\), and sample from \\(H^{\\perp}\\). Repeating \\(O(\\log|G|)\\) times generates "
          "\\(H^{\\perp}\\), and hence \\(H\\).")
    + p("The non-abelian case is largely open and is the main structural obstacle to broadening "
        "the class of exponential speed-ups. Graph isomorphism reduces to HSP over the symmetric "
        "group \\(S_n\\), and unique shortest vector (hence much of lattice cryptography) reduces "
        "to HSP over the dihedral group \\(D_n\\). Kuperberg's algorithm solves dihedral HSP in "
        "\\(2^{O(\\sqrt{\\log N})}\\) — subexponential but not polynomial, which is one reason "
        "lattice-based post-quantum schemes are believed safe.")
)

S5 = (
    code('''from math import gcd
from fractions import Fraction

def order_classical(a, N):
    """Brute-force order, for testing only."""
    r, x = 1, a % N
    while x != 1:
        x = (x * a) % N
        r += 1
    return r

def factors_from_order(a, r, N):
    if r % 2 or pow(a, r // 2, N) == N - 1:
        return None
    f1, f2 = gcd(pow(a, r // 2, N) - 1, N), gcd(pow(a, r // 2, N) + 1, N)
    return tuple(sorted({f1, f2} - {1, N})) or None

def convergents(x, qmax):
    """Denominators of the continued-fraction convergents of x, up to qmax."""
    out, f = [], Fraction(x).limit_denominator(qmax)
    return f

print(order_classical(7, 15), factors_from_order(7, 4, 15))   # 4  (3, 5)''',
         'The classical half of Shor: order, gcd extraction and continued fractions')
    + p("Simulating the quantum half exactly is possible only for tiny \\(N\\): the order-finding "
        "register needs \\(2L+1+L\\) qubits, so \\(N=15\\) already requires 13 qubits "
        "(\\(8192\\) amplitudes) and \\(N=21\\) requires 15. The exercises therefore simulate the "
        "eigenphase sampling directly, which is mathematically equivalent and lets you study the "
        "statistics for much larger \\(N\\).")
)

# =============================== figures, citations and added commentary =====
PIPELINE = flow_svg(
    [(20, 30, 128, 54, 'pick random a|2 ≤ a < N', '#f8fafc', '#475569'),
     (20, 118, 128, 54, 'gcd(a, N) > 1 ?|lucky: done', '#f8fafc', '#94a3b8'),
     (186, 30, 150, 54, 'QUANTUM|order finding r|of a mod N', '#ecfeff', '#026573'),
     (186, 128, 150, 54, 'phase estimation|on U: x ↦ ax mod N', '#ecfeff', '#0891a1'),
     (374, 30, 142, 54, 'continued fractions|recover r from y/2ᵗ', '#fefce8', '#c9a227'),
     (374, 128, 142, 54, 'r even and|a^(r/2) ≠ −1 ?', '#fefce8', '#92400e'),
     (548, 78, 118, 60, 'factors|gcd(a^(r/2)±1, N)', '#f5f3ff', '#6d28d9')],
    [(150, 57, 184, 57, ''), (336, 57, 372, 57, ''), (516, 90, 546, 90, ''),
     (261, 84, 261, 126, ''), (445, 84, 445, 126, ''), (84, 84, 84, 116, '')],
    height=210, title='Shor’s algorithm: one quantum subroutine inside a classical wrapper')


def _orderdist(r, t):
    N = 2 ** t
    out = [0.0] * N
    for s in range(r):
        for y in range(N):
            d = s / r - y / N
            if abs(sin(pi * d)) < 1e-14:
                out[y] += 1.0
            else:
                out[y] += (sin(pi * N * d) / (N * sin(pi * d))) ** 2
    return [v / r for v in out]


_od = _orderdist(4, 6)
ORDERDIST = bar_chart([str(y) if y % 8 == 0 else '' for y in range(64)], _od,
                      ylim=(0, 0.28), ylabel='probability', height=310,
                      colors=['#c9a227' if y % 16 == 0 else '#026573' for y in range(64)])

_od6 = _orderdist(6, 6)
ORDERDIST6 = bar_chart([str(y) if y % 8 == 0 else '' for y in range(64)], _od6,
                       ylim=(0, 0.28), ylabel='probability', height=310,
                       colors=['#026573'] * 64)

_Ls = list(range(64, 2305, 64))
RUNTIME = line_chart(
    [dict(label='classical number field sieve  exp(1.9 L^{1/3} log^{2/3}L)', xs=_Ls,
          ys=[1.923 * (L * log(2)) ** (1 / 3) * (log(L * log(2))) ** (2 / 3) / log(10)
              for L in _Ls], color='#dc2626'),
     dict(label='Shor, idealised gate count  ~L³ log L', xs=_Ls,
          ys=[3 * log10(L) + log10(log10(L)) for L in _Ls], color='#026573'),
     dict(label='Shor, fault-tolerant physical operations (measured estimate)', xs=_Ls,
          ys=[3 * log10(L) + log10(log10(L)) + 6 for L in _Ls], color='#c9a227', dash='6 4')],
    xlim=(64, 2304), ylim=(0, 40), xticks=[64,512,1024,1536,2048],
    yticks=[0,10,20,30,40], xlabel='modulus size  L  (bits)',
    ylabel='log₁₀ (operations)',
    vlines=[(1024, 'RSA-1024', '#475569'), (2048, 'RSA-2048', '#475569')], height=340)

JS_ORDER = """
  var b = JXG.JSXGraph.initBoard('ch7ord', {boundingbox: [-0.09, 0.42, 1.06, -0.13],
      axis: false, showCopyright: false, showNavigation: false});
  var rS = b.create('slider', [[0.02, 0.385], [0.40, 0.385], [2, 4, 12]],
      {name: 'order r', snapWidth: 1, strokeColor: '#026573'});
  var tS = b.create('slider', [[0.56, 0.385], [0.98, 0.385], [3, 6, 8]],
      {name: 't', snapWidth: 1, strokeColor: '#c9a227'});
  function pr(y, N, r) {
      var tot = 0;
      for (var s = 0; s < r; s++) {
          var d = s / r - y / N;
          var q = Math.sin(Math.PI * d);
          if (Math.abs(q) < 1e-14) { tot += 1; }
          else { var v = Math.sin(Math.PI * N * d) / (N * q); tot += v * v; }
      }
      return tot / r;
  }
  b.create('line', [[0, 0], [1, 0]], {strokeColor: '#0f172a', strokeWidth: 1.4,
      straightFirst: false, straightLast: false, fixed: true});
  for (var i = 0; i < 256; i++) {
      (function (k) {
          b.create('segment', [
              [function () { var N = Math.pow(2, tS.Value()); return k < N ? k / N : -1; }, 0],
              [function () { var N = Math.pow(2, tS.Value()); return k < N ? k / N : -1; },
               function () {
                   var N = Math.pow(2, tS.Value());
                   return k < N ? pr(k, N, Math.round(rS.Value())) : 0;
               }]],
              {strokeColor: '#026573', strokeWidth: 3, fixed: true, highlight: false});
      })(i);
  }
  b.create('text', [0.0, -0.055, function () {
      var r = Math.round(rS.Value());
      return 'peaks sit at y/2^t &#8776; s/r for s = 0,1,...,' + (r - 1) +
             ';  the s = 0 peak carries no information (probability 1/' + r + ')';
  }], {fontSize: 13, strokeColor: '#0f172a'});
  b.create('text', [0.0, -0.105, 'horizontal axis: y / 2^t'],
      {fontSize: 12, strokeColor: '#475569'});
"""

S1 = S1 + figure(
    '7.1',
    'The structure of the algorithm. Only the shaded quantum stage has no efficient classical '
    'counterpart; everything else — choosing a, the greatest common divisors, the continued-fraction '
    'post-processing, and the final verification by multiplying the factors back — is cheap classical '
    'number theory. Each of the two diamond-shaped tests can fail, in which case a fresh a is drawn; '
    'the failure probability per round is at most one half.',
    PIPELINE, height=210) + p(
    "It is worth being explicit about what the reduction does and does not assume" + cite('1,2') + ". "
    "It requires \\(N\\) odd, composite and not a prime power, and all three conditions are testable "
    "in polynomial time classically — primality by AKS or Miller–Rabin, perfect powers by trying "
    "each root. The interesting content is therefore entirely in the case of a modulus with at "
    "least two distinct odd prime factors, which is exactly the RSA case. The probability bound "
    "\\(1-2^{-(k-1)}\\) comes from analysing, via the Chinese Remainder Theorem, the distribution "
    "of the 2-adic valuation of the order of a random element in each factor group.") + sources(
    'The reduction and its probability analysis: Shor' + cite('1') + '; a particularly clear '
    'exposition: Ekert &amp; Jozsa' + cite('2') + '.')

S2 = S2 + figure(
    '7.2',
    'Output distribution of order finding for r = 4 with six ancillas. The order divides 2ᵗ here, so '
    'the distribution is exactly supported on the four multiples of 2ᵗ/r = 16, each with probability '
    '1/4. The peak at y = 0 corresponds to s = 0 and yields no information about r, which is why the '
    'algorithm expects to repeat.',
    ORDERDIST, height=310) + figure(
    '7.3',
    'The generic case, r = 6, which does not divide 64. The peaks now sit between grid points and '
    'each spreads over its neighbours in the same Fejér pattern as in Chapter 6. Continued fractions '
    'recover the exact rational s/r from the measured y/2ᵗ, provided the ancilla register is large '
    'enough that the approximation error is below 1/(2r²) — which is what fixes t = 2L + 1.',
    ORDERDIST6, height=310) + interactive(
    '7.4', 'ch7ord',
    'Vary the order r and the ancilla count t. Notice that whenever r divides 2ᵗ the distribution is '
    'perfectly sharp, and otherwise the peaks broaden; notice also that increasing t narrows every '
    'peak, which is exactly the precision the continued-fraction step needs. The s = 0 peak is '
    'always present and always useless.',
    JS_ORDER, aspect='16/9', max_width=660,
    hint='drag r and t to reshape the measured distribution.') + p(
    "The eigenvector trick in this section is the single most elegant step in the algorithm and "
    "deserves restating" + cite('1,2') + ". Phase estimation nominally requires the eigenstate "
    "\\(|u_s\\rangle\\), which cannot be prepared without knowing \\(r\\) — apparently circular. The "
    "escape is that \\(\\tfrac1{\\sqrt r}\\sum_s|u_s\\rangle=|1\\rangle\\), a trivially preparable "
    "state, and linearity then means the algorithm samples \\(s\\) uniformly. One pays a factor "
    "\\(1/r\\) in the probability of the useless \\(s=0\\) outcome and nothing else. The same "
    "device recurs whenever an eigenbasis is known abstractly but not constructively.") + sources(
    'Order finding by phase estimation: Shor' + cite('1') + ', Nielsen &amp; Chuang §5.3; the '
    'continued-fraction guarantee is Theorem 184 of Hardy &amp; Wright' + cite('7') + '.')

S3 = S3 + figure(
    '7.4b',
    'Asymptotic cost of factoring, classical against quantum, on a logarithmic vertical axis. The '
    'red curve is the general number field sieve, subexponential but superpolynomial; the teal curve '
    'is the idealised quantum gate count. The gold curve adds the fault-tolerance overhead measured '
    'in concrete surface-code estimates — roughly six orders of magnitude of physical operations per '
    'logical one at realistic error rates. The polynomial-versus-subexponential gap is real, but the '
    'constant is enormous, which is why the crossover happens at cryptographic sizes rather than at '
    'toy ones.',
    RUNTIME, height=340) + p(
    "The practical reading of this figure is the one that matters for security planning. Nothing in "
    "it says that RSA is broken today; the gold curve at \\(L=2048\\) corresponds to the "
    "twenty-million-qubit, eight-hour estimate of Gidney and Ekerå" + cite('4') + ", against "
    "devices with hundreds of noisy qubits. What it does say is that the threat is a matter of "
    "engineering rather than of mathematics, and that data encrypted today with public-key "
    "cryptography and recorded by an adversary may be readable later — the 'harvest now, decrypt "
    "later' model. That asymmetry is why the standardised post-quantum algorithms are being "
    "deployed now rather than when a machine exists" + cite('8') + ".") + sources(
    'Qubit-efficient arithmetic: Beauregard' + cite('3') + '; fault-tolerant resource estimate: '
    'Gidney &amp; Ekerå' + cite('4') + '; standardised replacements' + cite('8') + '.')

S4 = S4 + sources(
    'Simon\'s problem and the first exponential oracle separation' + cite('5') + '; the abelian '
    'framework: Childs &amp; van Dam (see Chapter 6); the dihedral case and its relevance to '
    'lattice cryptography: Kuperberg' + cite('6') + '.')

REFS = [
    dict(authors="P. W. Shor",
         title="Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer",
         venue="SIAM Journal on Computing 26(5), 1484–1509", year="1997",
         link="https://arxiv.org/abs/quant-ph/9508027",
         note="The journal version of the 1994 FOCS paper; both factoring and discrete log."),
    dict(authors="A. Ekert and R. Jozsa", title="Quantum computation and Shor's factoring algorithm",
         venue="Reviews of Modern Physics 68, 733", year="1996",
         note="The clearest early exposition of why the algorithm works."),
    dict(authors="S. Beauregard", title="Circuit for Shor's algorithm using 2n+3 qubits",
         venue="Quantum Information and Computation 3(2), 175–185", year="2003",
         link="https://arxiv.org/abs/quant-ph/0205095",
         note="The standard qubit-efficient arithmetic construction quoted in §3."),
    dict(authors="C. Gidney and M. Ekerå",
         title="How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits",
         venue="Quantum 5, 433", year="2021",
         link="https://arxiv.org/abs/1905.09749",
         note="The reference fault-tolerant resource estimate."),
    dict(authors="D. R. Simon", title="On the power of quantum computation",
         venue="SIAM Journal on Computing 26(5), 1474–1483", year="1997",
         note="The first exponential oracle separation; the HSP over Z_2^n."),
    dict(authors="G. Kuperberg",
         title="A subexponential-time quantum algorithm for the dihedral hidden subgroup problem",
         venue="SIAM Journal on Computing 35(1), 170–188", year="2005",
         link="https://arxiv.org/abs/quant-ph/0302112",
         note="The best known attack route on lattice problems via non-abelian HSP."),
    dict(authors="G. H. Hardy and E. M. Wright", title="An Introduction to the Theory of Numbers",
         venue="Oxford University Press (6th ed.)", year="2008",
         note="Theorem 184: the continued-fraction guarantee used in §2."),
    dict(authors="NIST", title="Post-Quantum Cryptography standards FIPS 203/204/205",
         venue="National Institute of Standards and Technology", year="2024",
         link="https://csrc.nist.gov/projects/post-quantum-cryptography",
         note="ML-KEM, ML-DSA, SLH-DSA — the deployed response to §3."),
]

CR = [
    dict(
        name='C7.Q1 — Continued fractions and convergents',
        qtext=cr_qtext('C7.Q1', 'Recovering s/r from a noisy estimate',
                       "Phase estimation returns \\(x=y/2^{t}\\) with "
                       "\\(|x-s/r|\\le1/(2r^{2})\\). Legendre's theorem guarantees \\(s/r\\) is a "
                       "convergent of the continued-fraction expansion of \\(x\\).",
                       "Write <code>cf_expansion(x, depth)</code> returning the list of partial "
                       "quotients \\([a_0;a_1,\\dots]\\) (stopping early if the remainder "
                       "vanishes); <code>convergents(x, depth)</code> returning the list of "
                       "<code>(p, q)</code> pairs; and <code>best_denominator(x, qmax)</code> "
                       "returning the largest-\\(q\\) convergent denominator with "
                       "\\(q\\le q_{\\max}\\). Use integers only in the recurrences "
                       "\\(p_k=a_kp_{k-1}+p_{k-2}\\), \\(q_k=a_kq_{k-1}+q_{k-2}\\).",
                       "cf_expansion(0.3125, 10)   -> [0, 3, 5]        (5/16)\n"
                       "best_denominator(0.3125, 15) -> 3              (1/3 is the best q<=15)"),
        answer='''from fractions import Fraction

def cf_expansion(x, depth):
    # work in exact rational arithmetic: floating-point recurrences are unstable here
    x = Fraction(x).limit_denominator(10 ** 6)
    out = []
    for _ in range(depth):
        a = x.numerator // x.denominator
        out.append(a)
        x = x - a
        if x == 0:
            break
        x = 1 / x
    return out

def convergents(x, depth):
    a = cf_expansion(x, depth)
    res, pm1, pm2, qm1, qm2 = [], 1, 0, 0, 1
    for ak in a:
        pk = ak * pm1 + pm2
        qk = ak * qm1 + qm2
        res.append((pk, qk))
        pm2, pm1 = pm1, pk
        qm2, qm1 = qm1, qk
    return res

def best_denominator(x, qmax):
    best = 1
    for _, q in convergents(x, 40):
        if 0 < q <= qmax:
            best = q
    return best
''',
        preload='''from fractions import Fraction

def cf_expansion(x, depth):
    # hint: Fraction(x).limit_denominator(10**6) first, then exact integer recurrences
    ...

def convergents(x, depth):
    ...

def best_denominator(x, qmax):
    ...
''',
        tests=[
            {'code': 'print(cf_expansion(0.3125, 10))\n',
             'expected': '[0, 3, 5]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(convergents(0.3125, 10))\n',
             'expected': '[(0, 1), (1, 3), (5, 16)]\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(best_denominator(0.3125, 15))\n',
             'expected': '3\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'print(best_denominator(0.25, 100), best_denominator(0.75, 100))\n',
             'expected': '4 4\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(convergents(5/13, 12)[-1])\n',
             'expected': '(5, 13)\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C7.Q2 — The classical reduction: order to factors',
        qtext=cr_qtext('C7.Q2', 'From r to a non-trivial divisor',
                       "If \\(r=\\mathrm{ord}_N(a)\\) is even and "
                       "\\(a^{r/2}\\not\\equiv-1\\), then \\(\\gcd(a^{r/2}\\pm1,N)\\) are proper "
                       "factors.",
                       "Write <code>order(a, N)</code> (brute force is fine here), "
                       "<code>factors_from_order(a, r, N)</code> returning a sorted tuple of two "
                       "non-trivial factors or <code>None</code> when the order is unusable, and "
                       "<code>shor_classical(N, seed)</code> which loops over random "
                       "\\(a\\) drawn with <code>random.Random(seed)</code> until it succeeds, "
                       "returning the sorted tuple of factors. Use "
                       "<code>math.gcd</code> and <code>pow(a, e, N)</code>.",
                       "order(7, 15) -> 4\n"
                       "factors_from_order(7, 4, 15) -> (3, 5)\n"
                       "shor_classical(15, 0) -> (3, 5)"),
        answer='''from math import gcd
import random

def order(a, N):
    r, x = 1, a % N
    while x != 1:
        x = (x * a) % N
        r += 1
    return r

def factors_from_order(a, r, N):
    if r % 2 != 0:
        return None
    h = pow(a, r // 2, N)
    if h == N - 1:
        return None
    f = tuple(sorted({gcd(h - 1, N), gcd(h + 1, N)} - {1, N}))
    if len(f) != 2:
        cand = [d for d in (gcd(h - 1, N), gcd(h + 1, N)) if 1 < d < N]
        if not cand:
            return None
        d = cand[0]
        return tuple(sorted((d, N // d)))
    return f

def shor_classical(N, seed):
    rng = random.Random(seed)
    while True:
        a = rng.randrange(2, N)
        g = gcd(a, N)
        if g > 1:
            return tuple(sorted((g, N // g)))
        f = factors_from_order(a, order(a, N), N)
        if f:
            return f
''',
        preload='''from math import gcd
import random

def order(a, N):
    ...

def factors_from_order(a, r, N):
    ...

def shor_classical(N, seed):
    ...
''',
        tests=[
            {'code': 'print(order(7, 15), order(2, 15))\n',
             'expected': '4 4\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(factors_from_order(7, 4, 15))\n',
             'expected': '(3, 5)\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(factors_from_order(14, 2, 15))\n',
             'expected': 'None\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'print(shor_classical(15, 0), shor_classical(21, 1), shor_classical(35, 2))\n',
             'expected': '(3, 5) (3, 7) (5, 7)\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(order(2, 21), factors_from_order(2, order(2,21), 21))\n',
             'expected': '6 (3, 7)\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C7.Q3 — Simulating the eigenphase sampling of order finding',
        qtext=cr_qtext('C7.Q3', 'The quantum subroutine, exactly',
                       "Phase estimation on \\(U_a|x\\rangle=|ax\\bmod N\\rangle\\) starting from "
                       "\\(|1\\rangle\\) samples \\(s\\) uniformly in \\(\\{0,\\dots,r-1\\}\\) and "
                       "outputs \\(y\\) distributed as a Fejér kernel around \\(2^{t}s/r\\).",
                       "Write <code>phase_distribution(r, t)</code> returning the exact "
                       "distribution over the \\(2^{t}\\) outcomes \\(y\\), averaged uniformly "
                       "over \\(s=0,\\dots,r-1\\); and "
                       "<code>sample_order(a, N, t, seed, trials)</code> which draws "
                       "<code>trials</code> outcomes from that distribution, converts each to a "
                       "candidate denominator by continued fractions, and returns the smallest "
                       "candidate \\(r'\\) with \\(a^{r'}\\equiv1\\pmod N\\) "
                       "(or <code>None</code>).",
                       "phase_distribution(4, 4) is supported on y = 0, 4, 8, 12\n"
                       "sample_order(7, 15, 8, 0, 20) -> 4"),
        answer='''import numpy as np
from fractions import Fraction

def phase_distribution(r, t):
    N = 2 ** t
    y = np.arange(N)
    total = np.zeros(N)
    for s in range(r):
        d = s / r - y / N
        amp = np.where(np.abs(np.sin(np.pi * d)) < 1e-14, 1.0,
                       np.sin(np.pi * N * d) / (N * np.sin(np.pi * d)))
        total += amp ** 2
    return total / r

def sample_order(a, N, t, seed, trials):
    r_true = 1
    x = a % N
    while x != 1:
        x = (x * a) % N
        r_true += 1
    pr = phase_distribution(r_true, t)
    pr = pr / pr.sum()
    rng = np.random.default_rng(seed)
    ys = rng.choice(2 ** t, size=trials, p=pr)
    cands = []
    for y in ys:
        q = Fraction(int(y), 2 ** t).limit_denominator(N).denominator
        if q > 0 and pow(a, q, N) == 1:
            cands.append(q)
    return min(cands) if cands else None
''',
        preload='''import numpy as np
from fractions import Fraction

def phase_distribution(r, t):
    ...

def sample_order(a, N, t, seed, trials):
    ...
''',
        tests=[
            {'code': 'import numpy as np\npr = phase_distribution(4, 4)\n'
                     'print(np.round(pr, 6).tolist().count(0.25))\n',
             'expected': '4\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(sample_order(7, 15, 8, 0, 20))\n',
             'expected': '4\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'import numpy as np\nprint(round(float(phase_distribution(6, 8).sum()), 6))\n',
             'expected': '1.0\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'print(sample_order(2, 21, 10, 3, 30), sample_order(2, 15, 8, 1, 20))\n',
             'expected': '6 4\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'import numpy as np\npr = phase_distribution(1, 5)\nprint(int(np.argmax(pr)), round(float(pr.max()), 6))\n',
             'expected': '0 1.0\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
    dict(
        name='C7.Q4 — End-to-end Shor (simulated quantum subroutine)',
        qtext=cr_qtext('C7.Q4', 'Putting it together',
                       "Combine the classical reduction of Q2 with the sampled order finding of "
                       "Q3. This is the complete algorithm, with the only idealisation being that "
                       "the eigenphase distribution is computed analytically instead of by "
                       "state-vector simulation.",
                       "Write <code>shor(N, seed, t=None, trials=30)</code> returning a sorted "
                       "tuple of two non-trivial factors of \\(N\\). Default "
                       "\\(t=2\\lceil\\log_2N\\rceil+1\\). Handle the easy cases first: even "
                       "\\(N\\), and \\(\\gcd(a,N)>1\\).",
                       "shor(15, 0) -> (3, 5)\n"
                       "shor(21, 1) -> (3, 7)\n"
                       "shor(91, 5) -> (7, 13)"),
        answer='''import numpy as np
from math import gcd, ceil, log2
from fractions import Fraction
import random

def _phase_distribution(r, t):
    N = 2 ** t
    y = np.arange(N)
    total = np.zeros(N)
    for s in range(r):
        d = s / r - y / N
        amp = np.where(np.abs(np.sin(np.pi * d)) < 1e-14, 1.0,
                       np.sin(np.pi * N * d) / (N * np.sin(np.pi * d)))
        total += amp ** 2
    return total / r

def _true_order(a, N):
    r, x = 1, a % N
    while x != 1:
        x = (x * a) % N
        r += 1
    return r

def shor(N, seed, t=None, trials=30):
    if N % 2 == 0:
        return tuple(sorted((2, N // 2)))
    if t is None:
        t = 2 * int(ceil(log2(N))) + 1
    rng = random.Random(seed)
    nprng = np.random.default_rng(seed)
    while True:
        a = rng.randrange(2, N)
        g = gcd(a, N)
        if g > 1:
            return tuple(sorted((g, N // g)))
        pr = _phase_distribution(_true_order(a, N), t)
        pr = pr / pr.sum()
        for y in nprng.choice(2 ** t, size=trials, p=pr):
            r = Fraction(int(y), 2 ** t).limit_denominator(N).denominator
            if r == 0 or pow(a, r, N) != 1 or r % 2:
                continue
            h = pow(a, r // 2, N)
            if h == N - 1:
                continue
            for d in (gcd(h - 1, N), gcd(h + 1, N)):
                if 1 < d < N:
                    return tuple(sorted((d, N // d)))
''',
        preload='''import numpy as np
from math import gcd, ceil, log2
from fractions import Fraction
import random

def shor(N, seed, t=None, trials=30):
    ...
''',
        tests=[
            {'code': 'print(shor(15, 0))\n',
             'expected': '(3, 5)\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(shor(21, 1))\n',
             'expected': '(3, 7)\n', 'useasexample': '1', 'display': 'SHOW'},
            {'code': 'print(shor(91, 5))\n',
             'expected': '(7, 13)\n', 'useasexample': '0', 'display': 'SHOW'},
            {'code': 'print(shor(33, 7), shor(35, 2))\n',
             'expected': '(3, 11) (5, 7)\n', 'useasexample': '0', 'display': 'HIDE'},
            {'code': 'print(shor(143, 11))\n',
             'expected': '(11, 13)\n', 'useasexample': '0', 'display': 'HIDE'},
        ]),
]

ST = [
    stack_question(
        name='C7.S1 — Order finding by hand',
        questiontext=stack_qtext(
            'C7.S1', 'The arithmetic of the reduction',
            r'<p>Take \(N=15\) and \(a=7\).</p>'
            r'<p>(a) Give \(r=\mathrm{ord}_{15}(7)\).</p>'
            r'<p>\(r=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give \(7^{r/2}\bmod 15\).</p>'
            r'<p>[[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Give the two non-trivial factors \(\gcd(7^{r/2}\pm1,15)\), as an ordered list '
            r'<code>[smaller, larger]</code>.</p>'
            r'<p>[[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) \(7^1=7,\ 7^2=49\equiv4,\ 7^3\equiv28\equiv13,\ 7^4\equiv91\equiv1\pmod{15}\), '
            r'so \(r=4\).</p>'
            r'<p>(b) \(7^{2}=49\equiv4\pmod{15}\). Crucially \(4\not\equiv-1\equiv14\), so the '
            r'reduction succeeds.</p>'
            r'<p>(c) \(\gcd(3,15)=3\) and \(\gcd(5,15)=5\), giving \(15=3\cdot5\).</p>'
            r'<p>Had we drawn \(a=14\), we would have \(r=2\) and \(14^{1}\equiv-1\), the failure '
            r'case — which is why the algorithm retries with a fresh random \(a\). The failure '
            r'probability is at most \(1/2\) per attempt.</p>'),
        questionvariables='ta1 : 4;\nta2 : 4;\nta3 : [3,5];',
        questionnote='r=4, 7^2=4, factors 3 and 5',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=6, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Compute \(7^k\bmod 15\) until you reach 1.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=6, value='0.3333333',
                 truefb=r'<p>Correct — and \(4\ne 14\equiv-1\), so the reduction works.</p>',
                 falsefb=r'<p>\(7^{2}=49\); reduce modulo 15.</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=14, value='0.3333333',
                 forbidfloat=0,
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Compute \(\gcd(4-1,15)\) and \(\gcd(4+1,15)\).</p>')]),
    stack_question(
        name='C7.S2 — Precision required for continued fractions',
        questiontext=stack_qtext(
            'C7.S2', 'Sizing the ancilla register',
            r'<p>Order finding must resolve \(s/r\) with \(r<N\), where \(N\) has '
            r'\(L=\lceil\log_2 N\rceil\) bits.</p>'
            r'<p>(a) Legendre\'s theorem requires \(|x-s/r|\le\varepsilon\). Give the largest '
            r'\(\varepsilon\) that still determines \(s/r\) uniquely, in terms of <code>r</code>.</p>'
            r'<p>\(\varepsilon=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the number of ancilla qubits \(t\) that guarantees this for every '
            r'\(r<N=2^{L}\), in terms of <code>L</code>.</p>'
            r'<p>\(t=\) [[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Evaluate \(t\) for an \(L={@L@}\)-bit modulus.</p>'
            r'<p>\(t=\) [[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) \(\varepsilon=\frac{1}{2r^{2}}\): two distinct rationals with denominators '
            r'below \(r\) differ by at least \(1/r^{2}\), so half that gap identifies the right one.</p>'
            r'<p>(b) Since \(r<2^{L}\), it suffices that \(2^{-t}\le 2^{-(2L+1)}\), i.e. '
            r'\(t=2L+1\).</p>'
            r'<p>(c) For \(L={@L@}\): \(t=2\cdot{@L@}+1={@ta3@}\).</p>'
            r'<p>For RSA-2048 this is \(t=4097\) ancillas on top of the arithmetic register — before '
            r'any error-correction overhead. Fault-tolerant estimates instead use windowed '
            r'arithmetic and semi-classical Fourier readout to bring the logical qubit count down '
            r'to roughly \(3L\).</p>'),
        questionvariables='L : rand_with_step(8,20,4);\nta1 : 1/(2*r^2);\nta2 : 2*L+1;\nta3 : 2*L+1;',
        questionnote='L={@L@}, t={@ta3@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=12, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Distinct rationals with denominator \(<r\) are at least \(1/r^{2}\) apart.</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=12, value='0.3333333',
                 truefb='<p>Correct.</p>',
                 falsefb=r'<p>Require \(2^{-t}\le\frac{1}{2\cdot(2^{L})^{2}}\).</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=10, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>Substitute the given \\(L\\).</p>')]),
    stack_question(
        name='C7.S3 — Success probability and repetition',
        questiontext=stack_qtext(
            'C7.S3', 'How often must we retry?',
            r'<p>Assume each independent attempt of Shor\'s algorithm succeeds with probability '
            r'at least \(1/2\).</p>'
            r'<p>(a) Give the probability that at least one of \(k\) independent attempts succeeds, '
            r'as a function of <code>k</code> (using the worst case \(1/2\)).</p>'
            r'<p>\(p_k=\) [[input:ans1]] [[validation:ans1]]</p>'
            r'<p>(b) Give the smallest \(k\) with \(p_k\ge 1-2^{-{@m@}}\).</p>'
            r'<p>\(k=\) [[input:ans2]] [[validation:ans2]]</p>'
            r'<p>(c) Phase estimation returns \(s=0\) with probability \(1/r\), which yields no '
            r'information. For \(r={@r0@}\), give that probability.</p>'
            r'<p>[[input:ans3]] [[validation:ans3]]</p>'),
        generalfeedback=(
            r'<p>(a) Failures are independent, so \(p_k=1-2^{-k}\).</p>'
            r'<p>(b) \(1-2^{-k}\ge1-2^{-{@m@}}\) iff \(k\ge{@m@}\), so \(k={@m@}\).</p>'
            r'<p>(c) \(1/r=1/{@r0@}\).</p>'
            r'<p>The overall structure is typical of BQP algorithms: a constant success probability '
            r'per run amplified to \(1-2^{-m}\) with \(O(m)\) repetitions, at negligible cost '
            r'compared with the exponential classical alternative. Verification is classical and '
            r'cheap — multiply the factors back — so the algorithm is a Las Vegas procedure.</p>'),
        questionvariables=('m : rand_with_step(4,10,1);\nr0 : rand_with_step(3,12,1);\n'
                           'ta1 : 1-2^(-k);\nta2 : m;\nta3 : 1/r0;'),
        questionnote='m={@m@}, r0={@r0@}',
        parts=[
            dict(input='ans1', prt='prt1', tans='ta1', boxsize=14, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>All \\(k\\) attempts must fail, each with probability \\(1/2\\).</p>'),
            dict(input='ans2', prt='prt2', tans='ta2', boxsize=8, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>Solve \\(2^{-k}\\le 2^{-m}\\).</p>'),
            dict(input='ans3', prt='prt3', tans='ta3', boxsize=8, value='0.3333333',
                 truefb='<p>Correct.</p>', falsefb='<p>\\(s\\) is uniform on \\(\\{0,\\dots,r-1\\}\\).</p>')]),
]

CHAPTER = dict(
    no=7, slug='shor-and-hidden-subgroup',
    title="Shor's Algorithm, Order Finding and the Hidden Subgroup Problem",
    subtitle='The classical reduction of factoring to order finding, order finding by phase '
             'estimation, continued fractions, discrete logarithms, the abelian HSP, and '
             'fault-tolerant resource estimates for RSA.',
    prereq='Chapter 6 (QFT, phase estimation); elementary number theory (gcd, modular arithmetic, '
           'Euler\'s theorem).',
    objectives=[
        'Reduce factoring to order finding and prove why the gcd extraction works.',
        'Identify the eigenvectors and eigenphases of modular multiplication and explain why |1> suffices.',
        'Apply continued fractions to recover s/r and justify the 2L+1 ancilla count.',
        'Estimate the gate and qubit cost of Shor, including the fault-tolerant reality check.',
        'Place order finding, Simon and discrete log inside the abelian HSP framework.',
        'Explain why non-abelian HSP (dihedral, symmetric) remains open and what that means for post-quantum security.',
    ],
    sections=[
        ('From factoring to order finding', S1),
        ('Order finding as phase estimation', S2),
        ('Cost: modular arithmetic dominates', S3),
        ('Discrete logarithms and the hidden subgroup problem', S4),
        ('Numerical practice', S5),
    ],
    summary="Shor's algorithm is a classical reduction (factoring → order finding, via gcd) "
            "wrapped around one quantum subroutine (phase estimation on modular multiplication) "
            "and one classical post-processing step (continued fractions). It generalises to the "
            "abelian hidden subgroup problem, which covers discrete logarithms and Simon's "
            "problem, but not to the non-abelian cases underlying graph isomorphism and lattice "
            "cryptography. Concrete fault-tolerant estimates put RSA-2048 at roughly 20 million "
            "physical qubits — far from current hardware, but close enough that post-quantum "
            "migration is already underway.",
    references=REFS, coderunner=CR, stack=ST,
)
