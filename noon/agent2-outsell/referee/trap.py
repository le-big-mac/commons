"""Referee: (1) the author's double-precision P(q, a, m) (function body copied from after2.py, lines 14-22) at very large m,
against my own mpmath evaluation of the Gamma limit; (2) Gamma form for large a by direct integration; (3) variance shares of the waits for g > 1."""
import math
import numpy as np
from scipy.special import betainc, betaln
from scipy.integrate import quad
from mpmath import mp, mpf, gammainc, gamma, exp, log, zeta
import mpmath


def P_author(q, a, m):
    lognorm = -betaln(a, m)
    def f(v):
        b = v / m
        if b >= 1: return 0.0
        return betainc(a, m, b ** (1 / q)) * math.exp(lognorm + (a - 1) * math.log(b) + (m - 1) * math.log1p(-b)) / m
    top = min(m, a + 60 * math.sqrt(a) + 200.0); pts = sorted(set([x for x in (a * 1e-4, a * 1e-3, a * 0.01, a * 0.1, a * 0.3, a, 2 * a, 4 * a, a + 10, a + 30, a + 100) if 0 < x < top]))
    return quad(f, 0, top, points=pts, limit=400, epsabs=1e-12, epsrel=1e-11)[0]


mp.dps = 25


def Plim_small(q, a, m):
    q = mpf(q); a = mpf(a); c = mpf(m) ** (1 - 1 / q)
    f = lambda u: gammainc(a, 0, c * u ** (1 / (a * q)), regularized=True) * exp(-u ** (1 / a))
    top = (a + 12 * mp.sqrt(a) + 60) ** a
    return mpmath.quad(f, [0] + [top * mpf(x) for x in ("0.01", "0.05", "0.1", "0.2", "0.35", "0.5", "0.7", "0.85")] + [top]) / gamma(a + 1)


def Plim_direct(q, a, m):
    q = mpf(q); a = mpf(a); c = mpf(m) ** (1 - 1 / q); s = mp.sqrt(a)
    f = lambda x: gammainc(a, 0, c * x ** (1 / q), regularized=True) * exp((a - 1) * log(x) - x - mpmath.loggamma(a)) if x > 0 else mpf(0)
    pts = sorted(set([mpf(0)] + [max(mpf(0), a + k * s) for k in (-8, -5, -3, -2, -1, 0, 1, 2, 3, 5, 8, 12, 20)]))
    return mpmath.quad(f, pts)


print("# author's double-precision formula at very large m against the Gamma limit (mpmath, 25 digits), q = 1.1")
for a in (0.1, 0.3, 3.0):
    for m in (1e9, 1e12, 1e15):
        pa = P_author(1.1, a, m); pl = Plim_small(1.1, a, m) if a < 1 else Plim_direct(1.1, a, m)
        print(f"  a={a} m={m:.0e}: author's {pa:.7f}   Gamma limit {mp.nstr(pl, 8)}   diff {pa - float(pl):+.1e}")
print("# a = 0.1 at small m: author's formula against the Gamma form (the author's 30 cases have no a below 0.3)")
for m in (50, 500, 5000):
    print(f"  a=0.1 m={m}: author's {P_author(1.1, 0.1, m):.7f}   Gamma form {mp.nstr(Plim_small(1.1, 0.1, m), 8)}")
print("# Gamma form for large a (direct integration): needs m >> a")
for a, m, exact in ((10, 500, "0.7997"), (10, 5000, "~0.905 (0.9000 at N=8621)"), (100, 500, "0.9069"), (100, 500000, "1.0000")):
    print(f"  a={a} m={m}: Gamma form {mp.nstr(Plim_direct(1.1, a, m), 6)}   exact {exact}")
print("# g > 1: share of the variance of a clock's total time that comes from the first wait / first three / first ten (a = 1)")
for g in (1.25, 1.5, 2.0):
    tot = zeta(2 * g); print(f"  g={g}: first wait {float(1 / tot):.3f}; first three {float(sum(k ** (-2 * g) for k in (1, 2, 3)) / tot):.3f}; first ten {float(sum(mpf(k) ** (-2 * g) for k in range(1, 11)) / tot):.4f}")
