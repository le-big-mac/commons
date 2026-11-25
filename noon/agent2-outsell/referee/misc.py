"""Referee controls, part 2.  usage: misc.py part     parts: lead | gamma | least | sform"""
import sys
import numpy as np


def dp(N, prob, start=None, keep=()):
    """prob(k, n) = chance next buyer takes A when A has k of n. start=(n0, p0)."""
    n0, p = start if start else (0, np.array([1.0])); p = np.array(p, dtype=float); out = {}
    for n in range(n0, N):
        t = p * prob(np.arange(n + 1), n)
        new = np.empty(n + 2); new[0] = 0.0; new[1:] = t; new[:-1] += p - t; p = new
        if n + 1 in keep: out[n + 1] = p.copy()
    return p, out


def power(q, g, a):
    return lambda k, n: q * (a + k) ** g / (q * (a + k) ** g + (a + n - k) ** g)


def half(p):
    N = len(p) - 1
    return float(p[N // 2 + 1:].sum() + (0.5 * p[N // 2] if N % 2 == 0 else 0.0))


part = sys.argv[1]

if part == "lead":
    print("# early lead: leader after n0 sales is leader after 10,000 (ties at n0 left out, half ties at the end)")
    for g, a, n0 in ((1.0, 1.0, 100), (1.0, 0.1, 100), (1.0, 10.0, 100), (1.0, 100.0, 100), (1.0, 1.0, 10), (1.0, 1.0, 1000),
                     (1.5, 1.0, 100), (1.5, 1.0, 10), (1.5, 1.0, 1), (2.0, 1.0, 10), (2.0, 1.0, 1), (1.5, 10.0, 100), (0.0, 1.0, 100)):
        rule = power(1.1, g, a); p0, _ = dp(n0, rule); k = np.arange(n0 + 1)
        res = {}
        for name, mask in (("A", 2 * k > n0), ("B", 2 * k < n0)):
            w = p0[mask].sum(); pe, _ = dp(10000, rule, start=(n0, np.where(mask, p0, 0.0))); res[name] = (w, half(pe) / w)
        same = (res["A"][0] * res["A"][1] + res["B"][0] * (1 - res["B"][1])) / (res["A"][0] + res["B"][0])
        pe, _ = dp(10000, rule)
        print(f"g={g} a={a:g} n0={n0}: same leader {same:.4f}; B led at n0 -> A ahead at 10,000: {res['B'][1]:.4f}; P(10,000)={half(pe):.4f}", flush=True)
        if g > 1 and n0 == 100:
            lo = np.minimum(np.arange(10001), 10000 - np.arange(10001))
            print(f"    loser's sales at 10,000 (g={g}, a={a:g}): at most 10 w.p. {pe[lo <= 10].sum():.4f}; at most 100: {pe[lo <= 100].sum():.4f}; at most 1000: {pe[lo <= 1000].sum():.4f}; median {int(lo[np.argsort(lo)][np.searchsorted(np.cumsum(pe[np.argsort(lo)]), 0.5)])}")

elif part == "gamma":
    from mpmath import mp, mpf, quad, gammainc, gamma, exp, findroot, log, psi
    mp.dps = 25

    def Plim(q, a, m):
        """P(G' < G^(1/q) m^(1-1/q)), G, G' indep Gamma(a); substitution u = x^a removes the singularity at 0."""
        q = mpf(q); a = mpf(a); c = mpf(m) ** (1 - 1 / q)
        f = lambda u: gammainc(a, 0, c * u ** (1 / (a * q)), regularized=True) * exp(-u ** (1 / a))
        top = (a + 12 * mp.sqrt(a) + 60) ** a
        pts = [0] + [top * mpf(x) for x in ("0.01", "0.05", "0.1", "0.2", "0.35", "0.5", "0.7", "0.85")] + [top]
        return quad(f, pts) / gamma(a + 1)

    print("# large-N Gamma form against exact step-by-step values (g=1, q=1.1)")
    for a, m, exact in ((1, 500, "0.650664 (N=999)"), (10, 500, "0.7997 (N=999, author's formula)"), (0.1, 500, "0.5512"), (100, 500, "0.9069"), (3, 500000, "0.9094"), (0.1, 500000, "0.5795"), (0.3, 500000, "0.6547")):
        print(f"  a={a} m={m}: Gamma form {mp.nstr(Plim(1.1, a, m), 7)}   exact {exact}")
    print("# a = 0.1 and 0.3 at m = 1e15 (N = 2e15): is P < 0.9, and where does it reach 0.9?")
    for a in (0.1, 0.3, 1):
        p15 = Plim(1.1, a, mpf(10) ** 15)
        lo, hi = mpf(1), mpf(120)
        for _ in range(40):
            mid = (lo + hi) / 2
            if Plim(1.1, a, mpf(10) ** mid) >= mpf("0.9"): hi = mid
            else: lo = mid
        print(f"  a={a}: P at m=1e15 = {mp.nstr(p15, 7)}; P = 0.9 at N = 2m ~ 10^{mp.nstr(hi + log(2, 10), 5)}")
    print("# 'all that a does': a=10 scatter-only reading = formula at m*a; shift term psi(a) and scatter psi'(a)")
    for a in (0.1, 1, 10, 100):
        print(f"  a={a}: E ln G = {mp.nstr(psi(0, a), 5)}, sd ln G = {mp.nstr(mp.sqrt(psi(1, a)), 5)}")
    for a in (10, 100):
        print(f"  a={a}: Gamma form at m=500: {mp.nstr(Plim(1.1, a, 500), 5)}; with only the scatter changed (advantage (m)^(1-1/q) applied to G/a, i.e. m -> a*m): {mp.nstr(Plim(1.1, a, 500 * a), 5)}")

elif part == "least":
    print("# least N over ALL N (odd and even), by step-by-step DP")
    for q, a, target, claim in ((1.1, 10.0, 0.9, 8621), (1.1, 30.0, 0.9, 1777), (1.1, 100.0, 0.9, 923), (1.25, 1.0, 0.75, 187), (1.25, 1.0, 0.9, 19119),
                                (1.5, 1.0, 0.75, 19), (1.5, 1.0, 0.9, 243), (2.0, 1.0, 0.75, 5), (2.0, 1.0, 0.9, 25), (2.0, 1.0, 0.99, 383), (1.5, 1.0, 0.99, 34151)):
        keep = tuple(range(max(1, claim - 4), claim + 3)); p, out = dp(claim + 2, power(q, 1.0, a), keep=keep)
        vals = {n: half(out[n]) for n in keep}; first = min(n for n in keep if vals[n] >= target)
        print(f"  q={q} a={a:g} target={target}: author {claim}; P({claim - 2})={vals.get(claim - 2, float('nan')):.6f} P({claim - 1})={vals[claim - 1]:.6f} P({claim})={vals[claim]:.6f}; first N>=target in window: {first}", flush=True)
    # no imitation, even N
    from scipy.stats import binom
    pr = 1.1 / 2.1
    for N in (721, 722, 723):
        print(f"  no imitation N={N}: P={float(binom.sf(N // 2, N, pr) + (0.5 * binom.pmf(N // 2, N, pr) if N % 2 == 0 else 0.0)):.6f}")

elif part == "sform":
    print("# other form: share s copy an earlier buyer (with one phantom buyer per product); all N up to 2000")
    Nmax = 2000
    for q in (1.1, 2.0):
        pr = q / (1 + q); curves = {}
        for s in (0, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9):
            p = np.array([1.0]); c = np.zeros(Nmax + 1)
            for n in range(Nmax):
                k = np.arange(n + 1); t = p * ((1 - s) * pr + s * (1 + k) / (2 + n)); new = np.empty(n + 2); new[0] = 0; new[1:] = t; new[:-1] += p - t; p = new; c[n + 1] = half(p)
            curves[s] = c
        ss = sorted(curves); worst = max(float((curves[s1] - curves[s0])[1:].max()) for s0, s1 in zip(ss, ss[1:]))
        print(f"  q={q}: largest rise of P between neighbouring s over all N<=2000: {worst:+.2e}; P(1000) = " + ", ".join(f"s={s}: {curves[s][1000]:.4f}" for s in ss))
    # same form WITHOUT phantom buyers: first buyer judges alone, copiers copy a real earlier buyer
    for q in (1.1,):
        pr = q / (1 + q); curves = {}
        for s in (0, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9):
            p = np.array([1.0]); c = np.zeros(Nmax + 1)
            for n in range(Nmax):
                k = np.arange(n + 1); pa = ((1 - s) * pr + s * k / n) if n > 0 else np.array([pr]); t = p * pa; new = np.empty(n + 2); new[0] = 0; new[1:] = t; new[:-1] += p - t; p = new; c[n + 1] = half(p)
            curves[s] = c
        ss = sorted(curves); worst = max(float((curves[s1] - curves[s0])[1:].max()) for s0, s1 in zip(ss, ss[1:]))
        print(f"  no phantom buyers, q={q}: largest rise between neighbouring s over all N<=2000: {worst:+.2e}; P(100) = " + ", ".join(f"s={s}: {curves[s][100]:.4f}" for s in ss) + "; P(1000) = " + ", ".join(f"s={s}: {curves[s][1000]:.4f}" for s in ss))
