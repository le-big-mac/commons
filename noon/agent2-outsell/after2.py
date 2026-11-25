"""The weight a of a product that has sold nothing, taken further (after the sealed sheet; not registered).
For imitation in proportion (g = 1) the time A needs for m sales is -ln(B)/q and B's is -ln(B'), with B and B' independent Beta(a, m)
variables (a sum of exponentials of rates a, a+1, ..., a+m-1 is minus the logarithm of a Beta(a, m)). So after N = 2m - 1 sales

    P = chance that B' < B^(1/q) = integral over b of  I(b^(1/q); a, m) * density of Beta(a, m) at b,

where I is the regularised incomplete beta function. For a = 1 this is line R4's formula.
usage: python -u after2.py after2.json"""
import sys, json, math
import numpy as np
from scipy.special import betainc, betaln
from scipy.integrate import quad
import urn
def P(q, a, m):
    """exact for whole m; b is written as v/m so that the integrand lives on a scale of order a"""
    lognorm = -betaln(a, m)                         # accurate for very large m, where a difference of log-gammas is not
    def f(v):
        b = v / m
        if b >= 1: return 0.0
        return betainc(a, m, b ** (1 / q)) * math.exp(lognorm + (a - 1) * math.log(b) + (m - 1) * math.log1p(-b)) / m
    top = min(m, a + 60 * math.sqrt(a) + 200.0); pts = sorted(set([x for x in (a * 1e-4, a * 1e-3, a * 0.01, a * 0.1, a * 0.3, a, 2 * a, 4 * a, a + 10, a + 30, a + 100) if 0 < x < top]))
    return quad(f, 0, top, points=pts, limit=400, epsabs=1e-12, epsrel=1e-11)[0]
A = {}
print("1. The formula for any a against the step-by-step computation (g = 1, N = 2m - 1)")
worst = 0.0
for q in (1.1, 1.5):
    for a in (0.3, 1.0, 3.0, 10.0, 30.0):
        for m in (50, 500, 5000):
            ex = urn.ahead(urn.dist(q, 1.0, 2 * m - 1, a=a)); fo = P(q, a, m); worst = max(worst, abs(ex - fo))
print(f"   30 cases (q = 1.1, 1.5; a = 0.3, 1, 3, 10, 30; m = 50, 500, 5,000): the largest difference is {worst:.1e}"); A['worst'] = worst
print(f"   a = 1, q = 1.1, m = 5e9: {P(1.1, 1.0, 5e9):.6f} (the many-digit formula of after.py gave 0.9 at N = 9.82e9, that is m = 4.91e9: {P(1.1, 1.0, 4.91e9):.6f})")
print("2. The number of sales after which the better product is ahead nine times in ten (g = 1), by the weight a"); A['needed'] = {}
for q in (1.05, 1.1, 1.25, 1.5):
    row = {}
    for a in (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0):
        if P(q, a, 1e15) < 0.9: row[str(a)] = float('inf'); continue        # beyond what double precision can be trusted with
        lo, hi = 0.0, 15.0
        for it in range(50):
            mid = 0.5 * (lo + hi)
            if P(q, a, max(1.0, 10 ** mid)) >= 0.9: hi = mid
            else: lo = mid
        m = 10 ** hi
        if m < 2e6:
            m = max(1, int(m) - 3)
            while P(q, a, m) < 0.9: m += 1
        row[str(a)] = 2 * m - 1
    from scipy.stats import binom
    N = 1; pr = q / (1 + q)
    while binom.sf(N // 2, N, pr) < 0.9: N += 2
    row['none'] = N; A['needed'][str(q)] = row
    print(f"   q = {q}: " + "; ".join((f"a = {a}: {v:,.0f}" if v < 1e7 else f"a = {a}: more than 2e15" if v == float('inf') else f"a = {a}: {v:.2e}") for a, v in row.items() if a != 'none') + f"; no imitation: {N:,}", flush=True)
print("3. P after 1,000 and after 1,000,000 sales (g = 1, q = 1.1), by the weight a"); A['P'] = {}
for a in (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0): A['P'][str(a)] = [P(1.1, a, 500), P(1.1, a, 500000)]; print(f"   a = {a}: {A['P'][str(a)][0]:.4f} (N = 999), {A['P'][str(a)][1]:.4f} (N = 999,999)")
print("4. Is the formula still sound at very large m? P for a = 1, q = 1.1 against the many-digit computation of after.py, and whether P rises with m")
big = json.load(open("after-3.json"))['big']
for N in (10 ** 6, 10 ** 9, 10 ** 12): print(f"   N = {N:.0e}: {P(1.1, 1.0, N // 2):.6f} against {big[str(N)]:.6f}")
grid = [P(1.1, 3.0, 10 ** e) for e in np.arange(1, 15.01, 0.5)]; print(f"   a = 3, q = 1.1, m from 10 to 1e15 in half-decades: P rises at every step: {all(y > x for x, y in zip(grid, grid[1:]))}; from {grid[0]:.4f} to {grid[-1]:.4f}")
A['needed'] = {q: {a: (None if v == float('inf') else v) for a, v in row.items()} for q, row in A['needed'].items()}
json.dump(A, open(sys.argv[1], "w"))
