"""Referee's blind computation (Step 1). Usage: blind.py part
parts: small | big | g15 | five
"""
import sys
import numpy as np


def dp(N, q, g, a=1.0, checkpoints=()):
    """Exact distribution of nA after N sales. Returns final vector and dict of checkpoints."""
    w = (a + np.arange(N + 1, dtype=np.float64)) ** g
    p = np.array([1.0])
    out = {}
    for n in range(N):
        wA = q * w[: n + 1]
        wB = w[n::-1]  # w[n-k], k = 0..n
        t = p * (wA / (wA + wB))
        new = np.empty(n + 2)
        new[0] = 0.0
        new[1:] = t
        new[:-1] += p - t
        p = new
        if n + 1 in checkpoints:
            out[n + 1] = p.copy()
    return p, out


def P_of(p):
    N = len(p) - 1
    k = np.arange(N + 1)
    return float(p[2 * k > N].sum() + 0.5 * p[2 * k == N].sum())


def I_formula(i, j, q, dps=30):
    """P(T_A(i) < T_B(j)) for g=1,a=1: j * int_0^1 (1-u^q)^i (1-u)^(j-1) du (mpmath)."""
    from mpmath import mp, mpf, quad, log1p, exp
    mp.dps = dps
    i = mpf(i); j = mpf(j); q = mpf(q)
    f = lambda u: exp(i * log1p(-u ** q) + (j - 1) * log1p(-u)) if 0 < u < 1 else mpf(0)
    pts = [mpf(0)] + [mpf(x) / j for x in ("0.03", "0.1", "0.3", "1", "2", "4", "8", "16", "32", "64", "128")]
    pts = [x for x in pts if x < 1] + [mpf(1)]
    return j * quad(f, pts)


part = sys.argv[1]

if part == "small":
    print("# item 1: P after 1,000 sales, q=1.1, a=1")
    for g in (0, 0.25, 0.5, 0.75, 1, 1.5):
        p, _ = dp(1000, 1.1, g)
        print(f"g={g:<5} P={P_of(p):.6f}  (sum={p.sum():.12f})")
    p, _ = dp(1000, 1.1, 1.0, a=10.0)
    print(f"g=1 a=10 N=1000 P={P_of(p):.6f}")
    print("# item 2: g=1, N=1000")
    p, _ = dp(1000, 1.1, 1.0)
    # B sold more than 550  <=> nA <= 449
    print(f"q=1.1: chance B sold more than 550 = {p[:450].sum():.6f}; A more than 550 = {p[551:].sum():.6f}")
    prev = None
    first = None
    for i in range(1, 101):
        q = round(1 + 0.01 * i, 2)
        P = P_of(dp(1000, q, 1.0)[0])
        if first is None and P >= 0.9:
            first = q
            print(f"least q (step 0.01) with P>=0.9 at N=1000,g=1: q={q}  P={P:.6f}; at q={round(q-0.01,2)} P={prev:.6f}")
        if prev is not None and P < prev:
            print("NOT MONOTONE in q at", q)
        prev = P
    print("# item 4: formula m*int (1-u^q)^m (1-u)^(m-1) du vs step-by-step at N=2m-1")
    for q, m in ((1.1, 50), (2.0, 500), (1.1, 500), (2.0, 50)):
        P = P_of(dp(2 * m - 1, q, 1.0)[0])
        F = I_formula(m, m, q)
        print(f"q={q} m={m}: DP={P:.12f} formula={float(F):.12f} diff={float(F)-P:+.2e}")
    # even N via the same embedding: P(1000) = 0.5[I(501,500)+I(500,501)]
    F = 0.5 * (I_formula(501, 500, 1.1) + I_formula(500, 501, 1.1))
    print(f"even-N check N=1000 q=1.1: formula={float(F):.12f} DP={P_of(p):.12f}")

elif part == "big":
    p, _ = dp(100000, 1.1, 1.0)
    print(f"# item 1: g=1 q=1.1 a=1 N=100000 DP P={P_of(p):.6f} (sum={p.sum():.12f})")
    F = 0.5 * (I_formula(50001, 50000, 1.1) + I_formula(50000, 50001, 1.1))
    print(f"   formula 0.5[I(50001,50000)+I(50000,50001)] = {float(F):.9f}")

elif part == "g15":
    p, out = dp(10000, 1.1, 1.5, checkpoints=(100, 1000,))
    print(f"# item 3: g=1.5 q=1.1: P(100)={P_of(out[100]):.6f} P(1000)={P_of(out[1000]):.6f} P(10000)={P_of(p):.6f}")
    prev = None
    first = None
    for i in range(1, 81):
        q = round(1 + 0.05 * i, 2)
        P = P_of(dp(10000, q, 1.5)[0])
        if prev is not None and P < prev - 1e-12:
            print("NOT MONOTONE in q at", q)
        if first is None and P >= 0.9:
            first = q
            print(f"least q (step 0.05) with P>=0.9 at N=10000,g=1.5: q={q} P={P:.6f}; at q={round(q-0.05,2)} P={prev:.6f}")
        prev = P
        if first is not None and q >= first + 0.3:
            break

elif part == "five":
    from mpmath import mp, mpf, findroot
    q = 1.1
    # odd N = 2m-1: P = I(m,m). Solve I(m,m)=0.9 for real m by bisection in log m.
    lo, hi = mpf(10) ** 8, mpf(10) ** 12
    print("# item 5: g=1,q=1.1,a=1; exact formula at huge m (mpmath, 30 digits)")
    for m in (1e3, 1e5, 1e7, 1e9, 4e9, 5e9, 6e9, 1e10, 1e11):
        print(f"  m={m:.3g} N=2m-1: P={float(I_formula(m, m, q)):.9f}")
    for _ in range(60):
        mid = (lo * hi) ** 0.5
        if I_formula(mid, mid, q) >= mpf("0.9"):
            hi = mid
        else:
            lo = mid
    m0 = int(hi)
    print(f"  real-m root of I(m,m)=0.9: m={float(hi):.10g}  -> N=2m-1 ~ {2*float(hi)-1:.10g}")
    for dps in (30, 45):
        a_ = I_formula(m0, m0, q, dps)
        b_ = I_formula(m0 + 1000, m0 + 1000, q, dps)
        print(f"  dps={dps}: I(m0)={mp.nstr(a_, 18)}  I(m0+1000)-I(m0)={mp.nstr(b_ - a_, 6)}")
    # even N=2m: 0.5[I(m+1,m)+I(m,m+1)]
    e = 0.5 * (I_formula(m0 + 1, m0, q) + I_formula(m0, m0 + 1, q))
    o = I_formula(m0, m0, q)
    print(f"  parity: P(2m0)-P(2m0-1) = {mp.nstr(e - o, 6)}")
    # asymptotic check: P ~ E exp(-m^(1-q) W^q)
    from mpmath import quad, exp, inf
    eps = mpf(m0) ** (1 - mpf(q))
    asym = quad(lambda w: exp(-w - eps * w ** mpf(q)), [0, 1, 5, 20, 60, 200])
    print(f"  asymptotic E exp(-m^(1-q) W^q) at m0: {mp.nstr(asym, 12)}")
