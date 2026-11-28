"""Lemma 1 for EVERY multiset of m elements containing 0 on Z_n, every divisor d > 1 and every residue x modulo d with
fewer than m elements in its class: #(signings bad at d) <= c_a c_(m-a) 2^m.  All signings, bad at d iff
|S(exp(2 pi i/d))| < 1e-9 (floating point; the sums have at most 7 terms).  Cases beyond the author's list.
NOT exact: zero is decided in floating point and the bound is compared in floating point.  The exact version,
made at the second look, is t_lemma1_all_exact.py (every zero confirmed in integers; same totals).
usage: t_lemma1_all.py SECONDS"""
import sys, math, cmath, itertools, time
from fractions import Fraction
import numpy as np
def c(r): return Fraction(1) if r <= 0 else Fraction(math.comb(r, r // 2), 2 ** r)
def blocks(n, m, size=150000):
    buf = []
    for rest in itertools.combinations_with_replacement(range(n), m - 1):
        buf.append((0,) + rest)
        if len(buf) == size: yield np.array(buf, dtype=np.int64); buf = []
    if buf: yield np.array(buf, dtype=np.int64)
if __name__ == '__main__':
    secs = float(sys.argv[1]); t0 = time.time(); total = 0; fails = 0
    for n, m in ((15, 7), (27, 6), (45, 5), (63, 4), (75, 4), (105, 4), (135, 4), (165, 3), (315, 3), (63, 5), (105, 5)):
        if time.time() - t0 > secs: print(f"n = {n} m = {m}: not started (time)"); continue
        divs = [d for d in range(3, n + 1) if n % d == 0]
        E = np.array([(1,) + e for e in itertools.product((1, -1), repeat=m - 1)], dtype=np.float64).T      # first sign +, count twice
        cases = 0; eq = 0; nms = 0; complete = True; worst = 0.0
        for X in blocks(n, m):
            if time.time() - t0 > secs: complete = False; break
            nms += len(X)
            for d in divs:
                z = np.exp(2j * np.pi * np.arange(d) / d)
                cnt = 2 * (np.abs(z[X % d] @ E) < 1e-9).sum(axis=1)                 # number of signings bad at d
                bnd = np.array([float(c(a) * c(m - a) * 2 ** m) for a in range(m)] + [np.inf])
                for x in range(d):
                    a = (X % d == x).sum(axis=1)
                    lim = bnd[a]; live = a < m
                    cases += int(live.sum())
                    f = live & (cnt > lim + 1e-9)
                    if f.any(): fails += int(f.sum()); print("LEMMA 1 FAILS:", n, d, x, X[f][0], flush=True)
                    eq += int((live & (np.abs(cnt - lim) < 1e-9) & (cnt > 0)).sum())
                    with np.errstate(invalid='ignore'): worst = max(worst, float(np.max(np.where(live, cnt / lim, 0))))
        total += cases
        print(f"n = {n:3d} m = {m}: {nms} multisets{'' if complete else ' (NOT all: time)'}, {cases} cases (multiset, d, x), largest count/bound {worst:.4f}, equal to the bound (count > 0) in {eq}", flush=True)
    print(f"{total} cases in all; failures {fails}")
